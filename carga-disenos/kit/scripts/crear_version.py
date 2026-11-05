#!/usr/bin/env python3
"""Crea en Printify la version Long Sleeve / Sweatshirt / Hoodie de un diseno que ya existe como remera.

Copia del producto remera (por su id de Printify): las imagenes ya subidas (oscura y clara, mismos ids),
la descripcion y los tags. Cambia blueprint, talles, precio y ubicacion segun la prenda (ver PRENDAS).
Los colores son los mismos de la remera, salvo los que no existan en la prenda (Ice Grey -> Ash cuando existe).

Uso:
  python3 crear_version.py --from <printify_id_remera> --garment hoodie                # simulacion
  python3 crear_version.py --from <printify_id_remera> --garment hoodie --create       # crea SIN publicar
  python3 crear_version.py --from <id> --garment sweatshirt --colors "Black,Sand" --create

No publica. Para publicar: publicar_existente.py (toma el precio de Printify y pone su tachado en Shopify).
Precios aprobados (iguales a Sloth Hiking Club): Long Sleeve 39.99 / 57.13, Sweatshirt 69.99 / 99.99.
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import printify_new_product as pnp  # call, colores, normalizar_areas, verificar_areas

SHOP_ID = pnp.SHOP_ID
SIZES = ["S", "M", "L", "XL", "2XL", "3XL"]  # mismos talles que la remera

# Ubicacion: misma medida fisica que en la remera (x/y/scale son relativos al area de impresion de cada prenda).
#  - remera 64000: scale 0.7365, y 0.2805 sobre un area de 3513x4011 (talle M)
#  - long sleeve 64400: area mas grande (4110x4658) -> scale 0.63, y 0.242 (mismo ancho y misma altura desde el borde)
#  - sweatshirt 18000: misma area que la remera -> mismos valores
#  - hoodie 18500: area apaisada sobre el bolsillo (3273x2180) -> scale 0.75, y 0.45 (el texto queda ~5% bajo el borde de arriba)
PRENDAS = {
    "long-sleeve": {"blueprint": 2806, "provider": 99, "price": 3999, "nombre": "Long Sleeve", "x": 0.5, "y": 0.242, "scale": 0.63},
    "sweatshirt": {"blueprint": 49, "provider": 99, "price": 6999, "nombre": "Sweatshirt", "x": 0.5, "y": 0.2805, "scale": 0.7365},
    # hoodie: desestimado por ahora (2026-11-05); queda la receta por si se retoma
    "hoodie": {"blueprint": 77, "provider": 99, "price": 5999, "nombre": "Hoodie", "x": 0.5, "y": 0.45, "scale": 0.75},
}
REEMPLAZOS = {"Ice Grey": "Ash"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="src", required=True, help="id de Printify de la remera")
    ap.add_argument("--garment", required=True, choices=sorted(PRENDAS))
    ap.add_argument("--title", default=None, help='por defecto "<Titulo remera sin T-Shirt> <Prenda>"')
    ap.add_argument("--colors", default=None, help="colores (nombres exactos del catalogo); por defecto los de la remera")
    ap.add_argument("--light-colors", default="Black,Navy")
    ap.add_argument("--x", type=float); ap.add_argument("--y", type=float); ap.add_argument("--scale", type=float)
    ap.add_argument("--price", type=int, help="precio en centavos")
    ap.add_argument("--create", action="store_true")
    a = ap.parse_args()
    pr = dict(PRENDAS[a.garment])
    for k in ("x", "y", "scale"):
        if getattr(a, k) is not None:
            pr[k] = getattr(a, k)
    price = a.price or pr["price"]

    src = pnp.call("GET", f"/shops/{SHOP_ID}/products/{a.src}.json")
    src_color = pnp.colores(src)
    src_cols = sorted({src_color[v["id"]] for v in src["variants"] if v["is_enabled"]})
    # imagen de cada color en la remera
    img_de = {}
    for pa in src["print_areas"]:
        ims = [im for ph in pa["placeholders"] if ph["position"] == "front" for im in ph["images"]]
        if len(ims) != 1:
            continue
        for v in pa["variant_ids"]:
            img_de.setdefault(src_color.get(v), ims[0])

    cat = pnp.call("GET", f"/catalog/blueprints/{pr['blueprint']}/print_providers/{pr['provider']}/variants.json")["variants"]
    color_of = {v["id"]: v["options"]["color"] for v in cat}
    disponibles = {v["options"]["color"] for v in cat}
    if a.colors:
        cols = [c.strip() for c in a.colors.split(",")]
    else:
        cols = []
        for c in src_cols:
            c2 = c if c in disponibles else REEMPLAZOS.get(c)
            if c2 in disponibles and c2 not in cols:
                cols.append(c2)
            if c2 != c:
                print(f"AVISO: {c} no existe en {pr['nombre']} -> {c2 if c2 in disponibles else 'se omite'}")
    faltan = [c for c in cols if c not in disponibles]
    if faltan:
        sys.exit(f"Colores que no existen en {pr['nombre']}: {', '.join(faltan)}")
    en = {v["id"] for v in cat if v["options"]["color"] in cols and v["options"]["size"] in SIZES}

    light = {c.strip() for c in a.light_colors.split(",")}
    light_cols = sorted(c for c in cols if c in light)
    dark_src = next((img_de[c] for c in src_cols if c not in light and c in img_de), None)
    if not dark_src:
        sys.exit("No encontre la imagen oscura en la remera.")
    todas = [v["id"] for v in cat]
    grupos = [(dark_src, [v for v in todas if color_of[v] not in light_cols], None)]
    for c in light_cols:
        im = img_de.get(c)
        if not im:
            sys.exit(f"La remera no tiene imagen para {c}")
        grupos.append((im, [v for v in todas if color_of[v] == c], c))

    title = a.title or f"{src['title'].replace(' T-Shirt', '').strip()} {pr['nombre']}"
    print(f"Remera: {src['title']} ({a.src}) -> {title}")
    print(f"Prenda: {pr['nombre']} | blueprint {pr['blueprint']} proveedor {pr['provider']} | precio Printify ${price/100:.2f}")
    print(f"Talles: {', '.join(SIZES)} | variantes habilitadas: {len(en)}")
    print(f"Ubicacion frente: x={pr['x']} y={pr['y']} scale={pr['scale']}")
    for im, vids, _ in grupos:
        print(f"  {im['id']} -> {', '.join(sorted({color_of[v] for v in vids if v in en}))}")
    if not a.create:
        print("SIMULACION: no se creo nada. Agrega --create.")
        return

    body = {
        "title": title,
        "description": src.get("description", ""),
        "blueprint_id": pr["blueprint"],
        "print_provider_id": pr["provider"],
        "tags": [t for t in src.get("tags", []) if t.lower() not in ("t-shirt", "t-shirts", "tee")] + [pr["nombre"]],
        "variants": [{"id": v, "price": price, "is_enabled": v in en} for v in todas],
        "print_areas": [{"variant_ids": vids, "placeholders": [{"position": "front", "images": [
            {"id": im["id"], "x": pr["x"], "y": pr["y"], "scale": pr["scale"], "angle": 0}]}]} for im, vids, _ in grupos],
    }
    prod = pnp.call("POST", f"/shops/{SHOP_ID}/products.json", body)
    if "id" not in prod:
        sys.exit(f"Fallo la creacion: {str(prod)[:500]}")
    print("Producto creado en Printify:", prod["id"])
    if light_cols:
        pnp.normalizar_areas(prod["id"], set(light_cols))
    esperado = [(set(vids) & en, im["id"], im.get("name", im["id"]), c) for im, vids, c in grupos]
    pnp.verificar_areas(prod["id"], esperado, set(light_cols))
    p = pnp.call("GET", f"/shops/{SHOP_ID}/products/{prod['id']}.json")
    # el orden del titulo de la variante cambia segun la prenda ("Talle / Color" o "Color / Talle")
    talle_de = {v["id"]: v["options"]["size"] for v in cat}
    costos = {}
    for v in p["variants"]:
        if v["is_enabled"]:
            costos.setdefault(talle_de[v["id"]], set()).add(v["cost"])
    print("Costo Printify por talle:", ", ".join(
        f"{s} ${min(costos[s])/100:.2f}" + (f"-{max(costos[s])/100:.2f}" if len(costos[s]) > 1 else "")
        for s in SIZES if s in costos))
    print(f"Editor: https://printify.com/app/editor/{prod['id']}")


if __name__ == "__main__":
    main()
