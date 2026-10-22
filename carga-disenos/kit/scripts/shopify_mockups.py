#!/usr/bin/env python3
"""Carga mockups propios en un producto de Shopify, asignando cada foto a las variantes de su color.

La API de Printify no permite subir mockups propios: se cargan en Shopify despues de publicar.
Para que Printify no los pise, el producto tiene que publicarse desde Printify con "images": false
(printify_new_product.py --publish --mockups DIR ya lo hace asi).

Los archivos se asignan por nombre: cada archivo tiene que contener el nombre del color,
ej. "black-sheep-sport-grey.jpg" -> Sport Grey. El orden de las fotos sigue --order o el alfabetico.

Uso:
  python3 shopify_mockups.py --printify-id 6abc... --dir mockups/             # simulacion, no cambia nada
  python3 shopify_mockups.py --printify-id 6abc... --dir mockups/ --apply     # sube las fotos
  python3 shopify_mockups.py --shopify-id 1539... --dir mockups/ --apply --replace   # borra las fotos actuales antes
"""
import argparse, base64, json, os, re, subprocess, sys, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import printify_new_product as pf

MAX_BYTES = 20 * 1024 * 1024  # limite de Shopify por imagen
PRECIO, TACHADO, VENDOR = "29.99", "42.85", "OldyFans"  # precio de venta, compare_at y marca (Google Shopping / Meta)
EXTS = (".jpg", ".jpeg", ".png", ".webp")


def shopify(method, path, body=None):
    pf.load_env()
    dom, ver, tok = (os.environ.get(k) for k in ("SHOPIFY_SHOP_DOMAIN", "SHOPIFY_API_VERSION", "SHOPIFY_ACCESS_TOKEN"))
    if not (dom and ver and tok):
        sys.exit("Faltan SHOPIFY_SHOP_DOMAIN / SHOPIFY_API_VERSION / SHOPIFY_ACCESS_TOKEN en .env (ver README.md).")
    cmd = ["curl", "-sS", "-X", method, f"https://{dom}/admin/api/{ver}{path}",
           "-H", f"X-Shopify-Access-Token: {tok}", "-H", "Content-Type: application/json"]
    tmp = None
    if body is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(body, tmp)
        tmp.close()
        cmd += ["--data", f"@{tmp.name}"]
    try:
        for intento in range(5):
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if method == "DELETE" and r.returncode == 0 and not r.stdout.strip():
                return {}
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                if intento < 4:
                    time.sleep(2 ** intento)
                    continue
                sys.exit(f"Respuesta inesperada de Shopify (curl exit {r.returncode}): {r.stdout[:300] or r.stderr[:300]}")
    finally:
        if tmp:
            os.unlink(tmp.name)


def graphql(query, variables=None):
    """Admin API GraphQL con reintentos ante respuesta no-JSON (shopify() ya reintenta) o throttling."""
    for intento in range(6):
        r = shopify("POST", "/graphql.json", {"query": query, "variables": variables or {}})
        errs = r.get("errors") if isinstance(r, dict) else None
        if errs and ("THROTTLED" in json.dumps(errs) or "Exceeded" in json.dumps(errs)) and intento < 5:
            time.sleep(2 + 2 ** intento)
            continue
        if errs:
            sys.exit(f"Error de Shopify GraphQL: {json.dumps(errs)[:500]}")
        # si queda poco cupo, esperar a que se recargue
        cupo = r.get("extensions", {}).get("cost", {}).get("throttleStatus", {})
        if cupo and cupo.get("currentlyAvailable", 1000) < 200:
            time.sleep(2)
        return r["data"]


Q_VARIANTES = """query($id: ID!, $after: String) { product(id: $id) { id handle vendor
  variants(first: 100, after: $after) { nodes { id title price compareAtPrice } pageInfo { hasNextPage endCursor } } } }"""


def variantes(gid):
    """(producto, [variantes]) con todas las variantes, paginando."""
    out, after = [], None
    while True:
        p = graphql(Q_VARIANTES, {"id": gid, "after": after})["product"]
        if not p:
            sys.exit(f"No encontre {gid} en Shopify.")
        out += p["variants"]["nodes"]
        if not p["variants"]["pageInfo"]["hasNextPage"]:
            return p, out
        after = p["variants"]["pageInfo"]["endCursor"]


def corregir(gid, vendor_actual, vars_a_corregir):
    """Pone price/compare_at en las variantes dadas y el vendor si hace falta. Devuelve la lista de errores."""
    errores = []
    if vars_a_corregir:
        r = graphql("""mutation($pid: ID!, $v: [ProductVariantsBulkInput!]!) {
            productVariantsBulkUpdate(productId: $pid, variants: $v) { userErrors { field message } } }""",
                    {"pid": gid, "v": [{"id": v["id"], "price": PRECIO, "compareAtPrice": TACHADO} for v in vars_a_corregir]})
        errores += [e["message"] for e in r["productVariantsBulkUpdate"]["userErrors"]]
    if vendor_actual != VENDOR:
        r = graphql("""mutation($p: ProductInput!) { productUpdate(input: $p) { userErrors { field message } } }""",
                    {"p": {"id": gid, "vendor": VENDOR}})
        errores += [e["message"] for e in r["productUpdate"]["userErrors"]]
    return errores


def fijar_precio_y_vendor(shopify_id):
    """Producto nuevo: TODAS las variantes a price 29.99 / compare_at 42.85 y Vendor "OldyFans".
    Idempotente: solo escribe lo que no esta bien. Imprime un resumen y devuelve True si quedo bien."""
    gid = f"gid://shopify/Product/{shopify_id}"
    p, vs = variantes(gid)
    mal = [v for v in vs if v["price"] != PRECIO or v["compareAtPrice"] != TACHADO]
    errores = corregir(gid, p["vendor"], mal)
    p2, vs2 = variantes(gid)
    quedan = [v for v in vs2 if v["price"] != PRECIO or v["compareAtPrice"] != TACHADO]
    print(f"Precio y marca en Shopify: {p2['handle']} | variantes: {len(vs2)} | actualizadas: {len(mal)} | "
          f"vendor: {p['vendor']} -> {p2['vendor']} | errores: {'; '.join(errores) or 'ninguno'}")
    if quedan or p2["vendor"] != VENDOR:
        print(f"  AVISO: quedan {len(quedan)} variantes fuera de {PRECIO}/{TACHADO} o el vendor no es {VENDOR}.")
        return False
    return True


def norm(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def shopify_id_from_printify(printify_id, wait=0):
    """Id del producto en Shopify; con wait>0 espera a que Printify termine de publicar."""
    fin = time.time() + wait
    while True:
        d = pf.call("GET", f"/shops/{pf.SHOP_ID}/products/{printify_id}.json")
        ext = d.get("external") or {}
        if ext.get("id"):
            return int(ext["id"])
        if time.time() >= fin:
            sys.exit(f"El producto {printify_id} todavia no esta publicado en Shopify.")
        time.sleep(6)


def hide(shopify_id):
    shopify("PUT", f"/products/{shopify_id}.json",
            {"product": {"id": shopify_id, "status": "draft", "published": False}})


def wait_printify_done(shopify_id, wait=300):
    """Printify termina de publicar unos minutos despues de crear el producto en Shopify, y en esa
    pasada lo deja activo y visible aunque en Printify figure oculto. Esperar a que pase."""
    fin = time.time() + wait
    while time.time() < fin:
        p = shopify("GET", f"/products/{shopify_id}.json?fields=status,published_at").get("product", {})
        if p.get("published_at"):
            return True
        time.sleep(10)
    return False


def keep_hidden(shopify_id, minutes=5):
    """Vigila unos minutos y vuelve a ocultar si Printify lo reactiva."""
    fin = time.time() + minutes * 60
    while time.time() < fin:
        p = shopify("GET", f"/products/{shopify_id}.json?fields=status,published_at").get("product", {})
        if p.get("status") != "draft" or p.get("published_at"):
            print("AVISO: Printify volvio a activar el producto; lo oculto de nuevo.")
            hide(shopify_id)
        time.sleep(20)


def match_files(folder, colors):
    """{color: archivo}. Gana el color mas largo que aparezca en el nombre (Heather Military Green > Military Green)."""
    out, sobrantes = {}, []
    for fn in sorted(os.listdir(folder)):
        if not fn.lower().endswith(EXTS):
            continue
        n = f"-{norm(os.path.splitext(fn)[0])}-"
        hits = [c for c in colors if f"-{norm(c)}-" in n]
        if not hits:
            sobrantes.append(fn)
            continue
        c = max(hits, key=len)
        if c in out:
            sys.exit(f"Dos archivos para {c}: {out[c]} y {fn}")
        out[c] = os.path.join(folder, fn)
    return out, sobrantes


def upload(shopify_id, folder, apply=False, replace=False, order=None, draft=True):
    p = shopify("GET", f"/products/{shopify_id}.json").get("product")
    if not p:
        sys.exit(f"No encontre el producto {shopify_id} en Shopify.")
    names = [o["name"] for o in p["options"]]
    if "Color" not in names:
        sys.exit("El producto no tiene opcion Color.")
    ci = names.index("Color") + 1
    colors = sorted({v[f"option{ci}"] for v in p["variants"]})
    files, sobrantes = match_files(folder, colors)

    print(f"Producto Shopify {shopify_id} '{p['title']}' | estado: {p['status']} | fotos actuales: {len(p['images'])}")
    for c in colors:
        f = files.get(c)
        print(f"  {c:<24} {os.path.basename(f) if f else '(sin mockup)'}")
    for fn in sobrantes:
        print(f"  AVISO: {fn} no coincide con ningun color del producto")
    for f in files.values():
        if os.path.getsize(f) > MAX_BYTES:
            sys.exit(f"{os.path.basename(f)} pesa mas de 20 MB: achicalo antes de subirlo.")
    if not files:
        sys.exit("Ningun archivo coincide con los colores del producto.")

    if not apply:
        print("SIMULACION: no se cambio nada. Agrega --apply para subir las fotos.")
        return

    if draft and (p["status"] != "draft" or p.get("published_at")):
        hide(shopify_id)
        print("Producto pasado a borrador y sacado de la tienda online.")
    if replace:
        for im in p["images"]:
            shopify("DELETE", f"/products/{shopify_id}/images/{im['id']}.json")
        print(f"Borradas {len(p['images'])} fotos anteriores.")

    orden = [c for c in (order or []) if c in files] + sorted(c for c in files if c not in (order or []))
    for pos, c in enumerate(orden, 1):
        vids = [v["id"] for v in p["variants"] if v[f"option{ci}"] == c]
        body = {"image": {"attachment": base64.b64encode(open(files[c], "rb").read()).decode(),
                          "filename": os.path.basename(files[c]), "alt": f"{p['title']} - {c}",
                          "position": pos, "variant_ids": vids}}
        r = shopify("POST", f"/products/{shopify_id}/images.json", body)
        if "image" not in r:
            sys.exit(f"Fallo la subida de {c}: {r}")
        print(f"  {c}: foto {r['image']['id']} -> {len(vids)} variantes")
    faltan = [c for c in colors if c not in files]
    if faltan:
        print("Colores sin mockup propio:", ", ".join(faltan))
    print("Listo. El producto queda en borrador: revisalo en Shopify y activalo a mano." if draft else "Listo.")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--printify-id")
    g.add_argument("--shopify-id", type=int)
    ap.add_argument("--dir", required=True, help="carpeta con un mockup por color (el nombre del color en el archivo)")
    ap.add_argument("--order", default=None, help="orden de colores separado por coma; el primero es la foto principal")
    ap.add_argument("--replace", action="store_true", help="borra las fotos actuales del producto antes de subir")
    ap.add_argument("--keep-status", action="store_true", help="no pasar el producto a borrador")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    sid = a.shopify_id or shopify_id_from_printify(a.printify_id)
    order = [c.strip() for c in a.order.split(",")] if a.order else None
    upload(sid, a.dir, apply=a.apply, replace=a.replace, order=order, draft=not a.keep_status)


if __name__ == "__main__":
    main()
