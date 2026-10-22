#!/usr/bin/env python3
"""Revisa todo el catalogo de Shopify y corrige Vendor y precio tachado (solo Admin API).

Detecta:
  - productos con Vendor distinto de "OldyFans" (Printify lo completa como "Printify"),
  - variantes con price 29.99 o 42.85 cuyo compare_at esta vacio o es menor/igual que el price.
Con --apply: guarda un backup en backups/ ANTES de escribir, pone Vendor "OldyFans" y deja esas variantes en
price 29.99 / compare_at 42.85, de a un producto con una pausa de ~0.4 s. Las variantes con otro precio no se tocan.
Es idempotente: lo que ya esta bien se saltea. No toca envios ni perfiles de envio.

Uso:
  python3 repair_products.py                                  # simulacion: lista lo que corregiria
  python3 repair_products.py --handle lost-my-mind-t-shirt    # simulacion sobre UN producto
  python3 repair_products.py --handle lost-my-mind-t-shirt --apply   # corrige solo ese producto
  python3 repair_products.py --apply                          # corrige todo el catalogo
  python3 repair_products.py --restore backups/repair-AAAAMMDD-HHMMSS.json [--apply]   # vuelve atras con un backup
"""
import argparse, datetime, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shopify_mockups as sm

BACKUPS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backups")
PRECIOS_ESTANDAR = {"29.99", "42.85"}
PAUSA = 0.4

# 10 productos x 90 variantes: queda por debajo del limite de costo de 1000 por consulta
Q_PRODUCTOS = """query($after: String, $q: String) { products(first: 10, after: $after, query: $q) {
  nodes { id handle title vendor status
    variants(first: 90) { nodes { id title price compareAtPrice } pageInfo { hasNextPage } } }
  pageInfo { hasNextPage endCursor } } }"""


def sin_tachado(v):
    if v["price"] not in PRECIOS_ESTANDAR:
        return False
    return v["compareAtPrice"] is None or float(v["compareAtPrice"]) <= float(v["price"])


def productos(handle=None):
    """Recorre el catalogo paginando con cursor."""
    after, q = None, (f"handle:{handle}" if handle else None)
    while True:
        d = sm.graphql(Q_PRODUCTOS, {"after": after, "q": q})["products"]
        for p in d["nodes"]:
            if p["variants"]["pageInfo"]["hasNextPage"]:
                _, p["variants"]["nodes"] = sm.variantes(p["id"])
            if handle and p["handle"] != handle:
                continue
            yield p
        if not d["pageInfo"]["hasNextPage"]:
            return
        after = d["pageInfo"]["endCursor"]


def revisar(handle=None):
    total, a_corregir, fuera = 0, [], 0
    for p in productos(handle):
        total += 1
        vs = p["variants"]["nodes"]
        malas = [v for v in vs if sin_tachado(v)]
        fuera += sum(1 for v in vs if v["price"] not in PRECIOS_ESTANDAR)
        if malas or p["vendor"] != sm.VENDOR:
            a_corregir.append((p, malas))
    return total, a_corregir, fuera


def resumen(total, a_corregir, fuera):
    vendor_printify = sum(1 for p, _ in a_corregir if p["vendor"] == "Printify")
    vendor_otro = sum(1 for p, _ in a_corregir if p["vendor"] not in ("Printify", sm.VENDOR))
    sin = sum(len(m) for _, m in a_corregir)
    print(f"\nEstado: {total} productos | Vendor \"Printify\": {vendor_printify} | otro vendor distinto de "
          f"\"{sm.VENDOR}\": {vendor_otro} | variantes sin tachado: {sin} | variantes con precio fuera de "
          f"29.99/42.85 (no se tocan): {fuera}")


def guardar_backup(a_corregir):
    os.makedirs(BACKUPS, exist_ok=True)
    path = os.path.join(BACKUPS, f"repair-{datetime.datetime.now():%Y%m%d-%H%M%S}.json")
    data = [{"id": p["id"], "handle": p["handle"], "vendor": p["vendor"],
             "variants": [{"id": v["id"], "title": v["title"], "price": v["price"], "compareAtPrice": v["compareAtPrice"]}
                          for v in p["variants"]["nodes"]]}
            for p, _ in a_corregir]
    with open(path, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    return path


def reparar(handle, apply):
    total, a_corregir, fuera = revisar(handle)
    print(f"Revisados: {total} productos | a corregir: {len(a_corregir)}")
    for p, malas in a_corregir:
        cambios = []
        if p["vendor"] != sm.VENDOR:
            cambios.append(f"vendor {p['vendor']!r} -> {sm.VENDOR!r}")
        if malas:
            precios = sorted({f"{v['price']}/{v['compareAtPrice']}" for v in malas})
            cambios.append(f"{len(malas)} variantes ({', '.join(precios)}) -> {sm.PRECIO}/{sm.TACHADO}")
        print(f"  {p['handle']:<45} {p['status']:<8} {'; '.join(cambios)}")
    if not a_corregir:
        resumen(total, a_corregir, fuera)
        print("Nada para corregir.")
        return
    if not apply:
        resumen(total, a_corregir, fuera)
        print("SIMULACION: no se cambio nada. Agrega --apply para corregir (primero guarda un backup en backups/).")
        return
    print("Backup guardado en", guardar_backup(a_corregir))
    ok = con_error = 0
    for p, malas in a_corregir:
        errores = sm.corregir(p["id"], p["vendor"], malas)
        if errores:
            con_error += 1
            print(f"  ERROR {p['handle']}: {'; '.join(errores)}")
        else:
            ok += 1
        time.sleep(PAUSA)
    print(f"Corregidos: {ok} | con error: {con_error}")
    print("Releyendo el catalogo para verificar...")
    resumen(*revisar(handle))


def restaurar(path, apply):
    data = json.load(open(path))
    print(f"Backup {path}: {len(data)} productos")
    for p in data:
        print(f"  {p['handle']:<45} vendor -> {p['vendor']!r} | {len(p['variants'])} variantes a sus precios anteriores")
    if not apply:
        print("SIMULACION: no se cambio nada. Agrega --apply para volver atras.")
        return
    for p in data:
        r = sm.graphql("""mutation($pid: ID!, $v: [ProductVariantsBulkInput!]!) {
            productVariantsBulkUpdate(productId: $pid, variants: $v) { userErrors { message } } }""",
                       {"pid": p["id"], "v": [{"id": v["id"], "price": v["price"], "compareAtPrice": v["compareAtPrice"]}
                                              for v in p["variants"]]})
        errores = [e["message"] for e in r["productVariantsBulkUpdate"]["userErrors"]]
        r = sm.graphql("""mutation($p: ProductInput!) { productUpdate(input: $p) { userErrors { message } } }""",
                       {"p": {"id": p["id"], "vendor": p["vendor"]}})
        errores += [e["message"] for e in r["productUpdate"]["userErrors"]]
        print(f"  {p['handle']}: {'ERROR ' + '; '.join(errores) if errores else 'restaurado'}")
        time.sleep(PAUSA)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", help="revisar/corregir solo este producto (para probar con uno)")
    ap.add_argument("--restore", metavar="BACKUP_JSON", help="vuelve atras los cambios guardados en un backup")
    ap.add_argument("--apply", action="store_true", help="escribe los cambios (por defecto solo simula)")
    a = ap.parse_args()
    if a.restore:
        restaurar(a.restore, a.apply)
    else:
        reparar(a.handle, a.apply)


if __name__ == "__main__":
    main()
