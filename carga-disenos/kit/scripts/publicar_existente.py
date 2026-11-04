#!/usr/bin/env python3
"""Publica en Shopify, en BORRADOR, un producto que ya existe en Printify, con los mockups propios.

No crea nada en Printify (para eso esta printify_new_product.py --create). Pasos:
  1. oculta el producto en Printify y lo publica SIN las fotos de Printify (images: false),
  2. espera a que Printify termine su segunda pasada en Shopify (lo deja activo y visible),
  3. borra las fotos que haya en Shopify y sube un mockup propio por color, asignado a sus variantes,
  4. lo deja en borrador y lo vigila 5 minutos por si Printify lo reactiva,
  5. deja todas las variantes en price 29.99 / compare_at 42.85 y el Vendor en "OldyFans"
     (Printify publica sin tachado y con Vendor "Printify"); lo repite al final por si Printify lo piso.

Uso:
  python3 publicar_existente.py --printify-id 6abc... --mockups carpeta/            # simulacion: muestra que mockup va en cada color
  python3 publicar_existente.py --printify-id 6abc... --mockups carpeta/ --apply    # publica (unos 10 minutos)
"""
import argparse, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import printify_new_product as pf
import shopify_mockups as sm


def publicar(printify_id, mockups):
    if mockups:
        if not os.path.isdir(mockups):
            sys.exit(f"No existe la carpeta de mockups: {mockups}")
        # oculto y sin las fotos de Printify, para que no pise los mockups propios
        pf.call("PUT", f"/shops/{pf.SHOP_ID}/products/{printify_id}.json", {"visible": False})
    r = pf.call("POST", f"/shops/{pf.SHOP_ID}/products/{printify_id}/publish.json",
                {"title": True, "description": True, "images": not mockups, "variants": True, "tags": True,
                 "keyfeatures": True, "shipping_template": True})
    print("Publicacion a Shopify solicitada:", r)
    # Printify publica de forma asincronica: esperar a que el producto tenga external.id (id en Shopify)
    sid = sm.shopify_id_from_printify(printify_id, wait=600)
    print("Producto en Shopify:", sid, "- esperando a que Printify termine de publicar...")
    if not sm.wait_printify_done(sid):
        print("AVISO: Printify no termino en 5 minutos; sigo igual y vigilo el estado.")
    sm.fijar_precio_y_vendor(sid)
    if mockups:
        sm.upload(sid, mockups, apply=True, replace=True)
        sm.keep_hidden(sid, minutes=5)
    else:
        time.sleep(120)  # margen por si Printify hace otra pasada
    # segunda pasada: si Printify piso el precio, el tachado o el vendor, se vuelve a corregir
    ok = sm.fijar_precio_y_vendor(sid)
    p = sm.shopify("GET", f"/products/{sid}.json?fields=id,title,handle,status,published_at,images,vendor").get("product", {})
    print(f"Verificado en Shopify: {p.get('title')} ({p.get('handle')}) | estado: {p.get('status')} | "
          f"en tienda online: {'si' if p.get('published_at') else 'no'} | fotos: {len(p.get('images', []))} | "
          f"vendor: {p.get('vendor')} | precio/tachado: {'OK' if ok else 'REVISAR'}")
    return sid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--printify-id", required=True)
    ap.add_argument("--mockups", required=True, help="carpeta con un mockup por color (el nombre del color en el archivo)")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    p = pf.call("GET", f"/shops/{pf.SHOP_ID}/products/{a.printify_id}.json")
    if "id" not in p:
        sys.exit(f"No encontre el producto {a.printify_id} en Printify: {p}")
    ext = (p.get("external") or {}).get("id")
    color_of = pf.colores(p)
    colores = sorted({color_of[v["id"]] for v in p["variants"] if v["is_enabled"]})
    files, sobrantes = sm.match_files(a.mockups, colores)
    print(f"Printify {p['id']} '{p['title']}' | ya en Shopify: {ext or 'no'}")
    for c in colores:
        print(f"  {c:<24} {os.path.basename(files[c]) if c in files else '(SIN MOCKUP)'}")
    for fn in sobrantes:
        print(f"  AVISO: {fn} no coincide con ningun color del producto")
    faltan = [c for c in colores if c not in files]
    if faltan:
        sys.exit(f"Faltan mockups para: {', '.join(faltan)}")
    if not a.apply:
        print("SIMULACION: no se publico nada. Agrega --apply para publicar en borrador.")
        return
    publicar(a.printify_id, a.mockups)


if __name__ == "__main__":
    main()
