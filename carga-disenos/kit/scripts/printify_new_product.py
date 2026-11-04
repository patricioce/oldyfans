#!/usr/bin/env python3
"""Crea un producto nuevo en Printify (tienda OldyFans) copiando la receta de un producto modelo.

Uso:
  python3 printify_new_product.py --image diseno.png --title "Nombre T-Shirt"            # simulacion (no crea nada)
  python3 printify_new_product.py --image diseno.png --title "Nombre T-Shirt" --create   # crea el producto (sin publicar)
  python3 printify_new_product.py --image diseno.png --title "Nombre T-Shirt" --create --publish
  python3 printify_new_product.py ... --create --publish --mockups carpeta/       # publica OCULTO con mockups propios (ver shopify_mockups.py)
  python3 printify_new_product.py ... --colors "White,Sport Grey,Ice Grey"               # elegir colores (mismos talles que el modelo)
  python3 printify_new_product.py --image oscura.png --image-light clara.png ...          # dos tintas: clara en Black y Navy, oscura en el resto
  python3 printify_new_product.py --fix-areas <printify_id> [--apply]                   # reordena las areas de un producto ya creado

Dos tintas: con --image-light cada color de --light-colors (por defecto "Black,Navy") tiene su propia area
de impresion con --image-light, con TODAS sus variantes (tambien los talles deshabilitados); todos los demas
colores, habilitados o no, van en el area de --image. Si Printify deja variantes de otros colores en el area
de Navy (las pone en la ultima area), el editor no reconoce el diseno de Navy: el script lo corrige despues de crear.

Precio: se carga en Printify a $29.99 (PRICE_CENTS) para que una republicacion desde Printify vuelva a 29.99.
Al publicar, publicar_existente.py deja en Shopify price 29.99 / compare_at 42.85 y Vendor "OldyFans".

Opciones de ubicacion del diseno: --x --y --scale --angle (por defecto los del modelo, con la escala al 85%).
Para publicar un producto YA creado (sin duplicarlo): publicar_existente.py --printify-id <id> --mockups carpeta/
"""
import argparse, base64, io, json, os, subprocess, sys, tempfile, time

SHOP_ID = int(os.environ.get("PRINTIFY_SHOP_ID", "27342731"))
TEMPLATE_PRODUCT_TITLE = "10 p.m T-Shirt"
PRICE_CENTS = 2999  # precio de venta; el tachado (42.85) se pone en Shopify al publicar
SCALE_FACTOR = 0.85  # el diseno va al 85% del tamano del modelo (aprobado por Patricio, lote 2026-10-15)
ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
API = "https://api.printify.com/v1"


def load_env():
    if os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def token():
    load_env()
    t = os.environ.get("PRINTIFY_TOKEN")
    if not t:
        sys.exit("Falta PRINTIFY_TOKEN: copia .env.example a .env y completalo (ver README.md).")
    return t.strip()


def call(method, path, body=None):
    cmd = ["curl", "-s", "-X", method, f"{API}{path}",
           "-H", f"Authorization: Bearer {token()}", "-H", "User-Agent: Claude",
           "-H", "Content-Type: application/json"]
    tmp = None
    if body is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(body, tmp)
        tmp.close()
        cmd += ["--data", f"@{tmp.name}"]
    try:
        # Printify devuelve 502 de vez en cuando: reintentar antes de rendirse
        for intento in range(5):
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            out = r.stdout
            try:
                return json.loads(out)
            except json.JSONDecodeError:
                if intento < 4 and (r.returncode != 0 or "502" in out or "503" in out or not out.strip()):
                    time.sleep(2 ** intento)
                    continue
                sys.exit(f"Respuesta inesperada de Printify (curl exit {r.returncode}): {out[:300] or r.stderr[:300]}")
    finally:
        if tmp:
            os.unlink(tmp.name)


def find_template():
    page = 1
    while True:
        d = call("GET", f"/shops/{SHOP_ID}/products.json?limit=50&page={page}")
        for p in d["data"]:
            if p["title"] == TEMPLATE_PRODUCT_TITLE:
                return p
        if page >= d["last_page"]:
            sys.exit(f"No encontre el producto modelo '{TEMPLATE_PRODUCT_TITLE}'")
        page += 1


def colores(p):
    """{variant_id: color} segun las opciones del producto (el titulo de la variante es "Talle / Color")."""
    vals = {val["id"]: val["title"] for o in p["options"] if o["type"] == "color" for val in o["values"]}
    return {v["id"]: next(vals[o] for o in v["options"] if o in vals) for v in p["variants"]}


def png_con_color(path, color):
    """Misma imagen, con un metadato del color: bytes distintos para que Printify le de un id propio."""
    from PIL import Image, PngImagePlugin
    info = PngImagePlugin.PngInfo()
    info.add_text("oldyfans-color", color)
    buf = io.BytesIO()
    Image.open(path).save(buf, format="PNG", pnginfo=info)
    return buf.getvalue()


def areas_esperadas(p, light_cols):
    """Reparte las variantes de las areas actuales: una area por color claro y el resto en la primera."""
    color_of = colores(p)
    todas = [v for pa in p["print_areas"] for v in pa["variant_ids"]]
    def ph_de(cond):
        # placeholders del area donde estan las variantes habilitadas que cumplen cond
        en = {v["id"] for v in p["variants"] if v["is_enabled"] and cond(color_of[v["id"]])}
        pa = max(p["print_areas"], key=lambda pa: len(en & set(pa["variant_ids"])))
        return pa["placeholders"] if en & set(pa["variant_ids"]) else None
    areas = [{"variant_ids": [v for v in todas if color_of.get(v) not in light_cols],
              "placeholders": ph_de(lambda c: c not in light_cols)}]
    for c in sorted(light_cols):
        areas.append({"variant_ids": [v for v in todas if color_of.get(v) == c], "placeholders": ph_de(lambda x, c=c: x == c)})
    return [a for a in areas if a["variant_ids"] and a["placeholders"]]


def problemas_areas(p, light_cols):
    """Lista de problemas: un color claro que comparte area con otros colores o esta repartido en varias."""
    color_of = colores(p)
    out = []
    for c in sorted(light_cols):
        con_c = [pa for pa in p["print_areas"] if any(color_of.get(v) == c for v in pa["variant_ids"])]
        if len(con_c) != 1:
            out.append(f"{c} esta repartido en {len(con_c)} areas")
            continue
        otros = sorted({color_of.get(v, "?") for v in con_c[0]["variant_ids"]} - {c})
        if otros:
            out.append(f"el area de {c} tambien tiene {len(otros)} colores mas ({', '.join(otros[:4])}{'...' if len(otros) > 4 else ''})")
    return out


def normalizar_areas(pid, light_cols, apply=True):
    """Deja cada color claro solo en su area (con todos sus talles) y el resto en el area general."""
    p = call("GET", f"/shops/{SHOP_ID}/products/{pid}.json")
    if len(p["print_areas"]) < 2:
        print("  Una sola area (diseno unico en todos los colores): nada que corregir.")
        return True
    color_of = colores(p)
    # solo los colores claros que el producto tiene habilitados
    light_cols = {color_of[v["id"]] for v in p["variants"]
                  if v["is_enabled"] and color_of[v["id"]].lower() in {x.lower() for x in light_cols}}
    probs = problemas_areas(p, light_cols)
    if not probs:
        print("  Areas OK: cada color claro tiene su area propia.")
        return True
    for pr in probs:
        print("  A CORREGIR:", pr)
    if not apply:
        return False
    r = call("PUT", f"/shops/{SHOP_ID}/products/{pid}.json", {"print_areas": areas_esperadas(p, light_cols)})
    if "id" not in r:
        sys.exit(f"Printify rechazo el cambio de areas: {str(r)[:300]}")
    print("  Areas reacomodadas.")
    return True


def verificar_areas(pid, esperado, light_cols):
    """Relee el producto y confirma que cada grupo de colores quedo en su area con su imagen."""
    p = call("GET", f"/shops/{SHOP_ID}/products/{pid}.json")
    color_of = colores(p)
    habilitadas = {v["id"] for v in p["variants"] if v["is_enabled"]}
    ok = True
    for pr in problemas_areas(p, light_cols):
        ok = False
        print("  ERROR", pr)
    for vids, img_id, fname, _ in esperado:
        area = next((pa for pa in p["print_areas"] if vids <= set(pa["variant_ids"])), None)
        ids = [im["id"] for ph in (area or {}).get("placeholders", []) if ph["position"] == "front" for im in ph["images"]]
        cols = ", ".join(sorted({color_of[v] for v in vids}))
        if area is None or ids != [img_id]:
            ok = False
            print(f"  ERROR area de {cols}: imagenes {ids} (esperada {fname})")
        else:
            print(f"  OK {cols} -> {fname}")
    sin_area = habilitadas - {v for pa in p["print_areas"] for v in pa["variant_ids"]}
    if sin_area:
        ok = False
        print(f"  ERROR {len(sin_area)} variantes habilitadas sin area de impresion")
    if not ok:
        sys.exit(f"El producto {pid} no quedo con las areas esperadas: revisarlo antes de publicar.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image")
    ap.add_argument("--title")
    ap.add_argument("--image-light", default=None, help="version clara del diseno, para los colores de --light-colors")
    ap.add_argument("--light-colors", default="Black,Navy", help="colores que llevan --image-light (por defecto Black,Navy)")
    ap.add_argument("--description", default=None)
    ap.add_argument("--tags", default=None, help="tags separados por coma; por defecto los del modelo")
    ap.add_argument("--colors", default=None, help="colores separados por coma (ej. \"White,Sport Grey\"); por defecto los del modelo")
    ap.add_argument("--x", type=float, default=None)
    ap.add_argument("--y", type=float, default=None)
    ap.add_argument("--scale", type=float, default=None)
    ap.add_argument("--angle", type=float, default=None)
    ap.add_argument("--mockups", default=None, help="carpeta con mockups propios (uno por color); con --publish publica oculto y los carga en Shopify")
    ap.add_argument("--create", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--fix-areas", metavar="PRINTIFY_ID", help="revisa (y con --apply corrige) las areas de un producto ya creado")
    ap.add_argument("--apply", action="store_true", help="con --fix-areas: escribe el cambio")
    a = ap.parse_args()
    light = {c.strip().lower() for c in a.light_colors.split(",") if c.strip()}

    if a.fix_areas:
        print(f"Producto {a.fix_areas}:")
        if not normalizar_areas(a.fix_areas, light, apply=a.apply) and not a.apply:
            print("SIMULACION: no se cambio nada. Agrega --apply para corregir.")
        return
    if not (a.image and a.title):
        ap.error("--image y --title son obligatorios (salvo con --fix-areas)")

    tpl = find_template()
    enabled_tpl = [v for v in tpl["variants"] if v["is_enabled"]]
    # catalogo completo del modelo: todas las variantes van a alguna area (tambien las deshabilitadas),
    # asi Printify no las tira en el area de Navy
    cat = call("GET", f"/catalog/blueprints/{tpl['blueprint_id']}/print_providers/{tpl['print_provider_id']}/variants.json")["variants"]
    color_of = {v["id"]: v["options"]["color"] for v in cat}
    sizes = {v["options"]["size"] for v in cat if v["id"] in {t["id"] for t in enabled_tpl}}
    if a.colors:
        # mismos talles que el modelo, en los colores pedidos (nombre exacto del catalogo)
        wanted = {c.strip().lower() for c in a.colors.split(",")}
        enabled = [v["id"] for v in cat if v["options"]["color"].lower() in wanted and v["options"]["size"] in sizes]
        missing = wanted - {color_of[v].lower() for v in enabled}
        if missing:
            sys.exit(f"Colores que no existen en el catalogo: {', '.join(sorted(missing))}")
    else:
        enabled = [v["id"] for v in enabled_tpl if v["id"] in color_of]
        if len(enabled) != len(enabled_tpl):
            print(f"AVISO: {len(enabled_tpl) - len(enabled)} variantes del modelo ya no estan en el catalogo; se omiten.")
    front = next(ph for pa in tpl["print_areas"] for ph in pa["placeholders"] if ph["position"] == "front" and ph["images"])
    ref = front["images"][0]
    x = ref["x"] if a.x is None else a.x
    y = ref["y"] if a.y is None else a.y
    scale = ref["scale"] * SCALE_FACTOR if a.scale is None else a.scale
    angle = ref.get("angle", 0) if a.angle is None else a.angle
    tags = [t.strip() for t in a.tags.split(",")] if a.tags else tpl["tags"]

    print(f"Modelo: {tpl['title']} | variantes habilitadas: {len(enabled)} | precio en Printify: ${PRICE_CENTS/100:.2f}")
    print("Colores:", ", ".join(sorted({color_of[v] for v in enabled})))
    print(f"Ubicacion frente: x={x:.3f} y={y:.3f} scale={scale:.3f} angle={angle}")

    # colores claros que el producto realmente tiene habilitados
    light_cols = sorted({color_of[v] for v in enabled if a.image_light and color_of[v].lower() in light})
    if a.image_light and not light_cols:
        sys.exit(f"Ninguno de los colores elegidos esta en --light-colors ({a.light_colors}).")
    todas = [v["id"] for v in cat]
    groups = [(a.image, [v for v in todas if color_of[v] not in light_cols], None)]
    # un area por cada color claro, con todos sus talles: asi el editor de Printify lo muestra como
    # "specific design for Black" / "for Navy" (con Black y Navy juntos en una area no lo reconoce)
    for c in light_cols:
        groups.append((a.image_light, [v for v in todas if color_of[v] == c], c))
    en = set(enabled)
    for img, vids, _ in groups:
        cols = sorted({color_of[i] for i in vids if i in en})
        print(f"  {os.path.basename(img)} -> {', '.join(cols)}  ({len(vids)} variantes en el area, {len(en & set(vids))} habilitadas)")

    if a.mockups and not os.path.isdir(a.mockups):
        sys.exit(f"No existe la carpeta de mockups: {a.mockups}")

    if not a.create:
        print("SIMULACION: no se creo nada. Agrega --create para crear el producto.")
        return

    # cada color claro sube su propia copia de la clara (clara-black.png, clara-navy.png).
    # Printify deduplica las subidas por contenido, asi que cada copia lleva un metadato PNG con su color.
    print_areas, esperado = [], []
    for img, vids, color in groups:
        base, ext = os.path.splitext(os.path.basename(img))
        fname = f"{base}-{color.lower().replace(' ', '-')}{ext}" if color else os.path.basename(img)
        contents = base64.b64encode(png_con_color(img, color) if color else open(img, "rb").read()).decode()
        up = call("POST", "/uploads/images.json", {"file_name": fname, "contents": contents})
        if "id" not in up:
            sys.exit(f"Fallo la subida: {up}")
        print("Imagen subida:", fname, up["id"], f"{up.get('width')}x{up.get('height')}")
        esperado.append((set(vids) & en, up["id"], fname, color))
        print_areas.append({
            "variant_ids": vids,
            "placeholders": [{"position": "front",
                              "images": [{"id": up["id"], "x": x, "y": y, "scale": scale, "angle": angle}]}],
        })

    body = {
        "title": a.title,
        "description": a.description if a.description is not None else tpl.get("description", ""),
        "blueprint_id": tpl["blueprint_id"],
        "print_provider_id": tpl["print_provider_id"],
        "tags": tags,
        "variants": [{"id": v, "price": PRICE_CENTS, "is_enabled": v in en} for v in todas],
        "print_areas": print_areas,
    }
    prod = call("POST", f"/shops/{SHOP_ID}/products.json", body)
    if "id" not in prod:
        sys.exit(f"Fallo la creacion: {prod}")
    print("Producto creado en Printify:", prod["id"])
    if light_cols:
        normalizar_areas(prod["id"], set(light_cols))
    verificar_areas(prod["id"], esperado, set(light_cols))
    print(f"Editor: https://printify.com/app/editor/{prod['id']}")

    if a.publish:
        import publicar_existente
        publicar_existente.publicar(prod["id"], a.mockups)
    else:
        print("No publicado. Revisa los mockups en Printify y luego publica con publicar_existente.py.")


if __name__ == "__main__":
    main()
