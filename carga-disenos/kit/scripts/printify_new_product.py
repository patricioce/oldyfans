#!/usr/bin/env python3
"""Crea un producto nuevo en Printify (tienda OldyFans) copiando la receta de un producto modelo.

Uso:
  python3 printify_new_product.py --image diseno.png --title "Nombre T-Shirt"            # simulacion (no crea nada)
  python3 printify_new_product.py --image diseno.png --title "Nombre T-Shirt" --create   # crea el producto (sin publicar)
  python3 printify_new_product.py --image diseno.png --title "Nombre T-Shirt" --create --publish
  python3 printify_new_product.py ... --create --publish --mockups carpeta/       # publica OCULTO con mockups propios (ver shopify_mockups.py)
  python3 printify_new_product.py ... --colors "White,Sport Grey,Ice Grey"               # elegir colores (mismos talles que el modelo)
  python3 printify_new_product.py --image oscura.png --image-light clara.png ...          # dos tintas: clara en Black y Navy, oscura en el resto

Dos tintas: con --image-light se arman dos areas de impresion en el mismo producto. Los colores de
--light-colors (por defecto "Black,Navy") llevan --image-light; todos los demas, --image.

Opciones de ubicacion del diseno: --x --y --scale --angle (por defecto los del modelo, con la escala al 85%).
Para publicar un producto YA creado (sin duplicarlo): publicar_existente.py --printify-id <id> --mockups carpeta/
"""
import argparse, base64, json, os, subprocess, sys, tempfile, time

SHOP_ID = int(os.environ.get("PRINTIFY_SHOP_ID", "27342731"))
TEMPLATE_PRODUCT_TITLE = "10 p.m T-Shirt"
PRICE_CENTS = 4285
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--title", required=True)
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
    a = ap.parse_args()

    tpl = find_template()
    enabled = [v for v in tpl["variants"] if v["is_enabled"]]
    color_of = {v["id"]: v["title"].split(" / ")[0] for v in enabled}
    if a.colors:
        # mismos talles que el modelo, en los colores pedidos (nombre exacto del catalogo)
        sizes = {v["title"].split(" / ")[1] for v in enabled}
        wanted = {c.strip().lower() for c in a.colors.split(",")}
        cat = call("GET", f"/catalog/blueprints/{tpl['blueprint_id']}/print_providers/{tpl['print_provider_id']}/variants.json")
        enabled = [v for v in cat["variants"]
                   if v["options"]["color"].lower() in wanted and v["options"]["size"] in sizes]
        color_of = {v["id"]: v["options"]["color"] for v in enabled}
        missing = wanted - {v["options"]["color"].lower() for v in enabled}
        if missing:
            sys.exit(f"Colores que no existen en el catalogo: {', '.join(sorted(missing))}")
    front = next(ph for pa in tpl["print_areas"] for ph in pa["placeholders"] if ph["position"] == "front" and ph["images"])
    ref = front["images"][0]
    x = ref["x"] if a.x is None else a.x
    y = ref["y"] if a.y is None else a.y
    scale = ref["scale"] * SCALE_FACTOR if a.scale is None else a.scale
    angle = ref.get("angle", 0) if a.angle is None else a.angle
    tags = [t.strip() for t in a.tags.split(",")] if a.tags else tpl["tags"]

    print(f"Modelo: {tpl['title']} | variantes habilitadas: {len(enabled)} | precio: ${PRICE_CENTS/100:.2f}")
    if a.colors:
        print("Colores:", ", ".join(sorted({v["options"]["color"] for v in enabled})))
    print(f"Ubicacion frente: x={x:.3f} y={y:.3f} scale={scale:.3f} angle={angle}")

    light = {c.strip().lower() for c in a.light_colors.split(",") if c.strip()}
    groups = [(a.image, [v["id"] for v in enabled if not (a.image_light and color_of[v["id"]].lower() in light)])]
    if a.image_light:
        # un area por cada color claro: asi el editor de Printify lo muestra como
        # "specific design for Black" / "for Navy" (con Black y Navy juntos en una area no lo reconoce)
        for c in sorted({color_of[v["id"]] for v in enabled if color_of[v["id"]].lower() in light}):
            groups.append((a.image_light, [v["id"] for v in enabled if color_of[v["id"]] == c]))
        for img, vids in groups:
            cols = sorted({color_of[i] for i in vids})
            print(f"  {os.path.basename(img)} -> {', '.join(cols) or '(ningun color)'}")
        if len(groups) < 2:
            sys.exit(f"Ninguno de los colores elegidos esta en --light-colors ({a.light_colors}).")
    groups = [(img, vids) for img, vids in groups if vids]

    if a.mockups and not os.path.isdir(a.mockups):
        sys.exit(f"No existe la carpeta de mockups: {a.mockups}")

    if not a.create:
        print("SIMULACION: no se creo nada. Agrega --create para crear el producto.")
        return

    print_areas, subidas = [], {}
    for img, vids in groups:
        if img not in subidas:
            contents = base64.b64encode(open(img, "rb").read()).decode()
            subidas[img] = call("POST", "/uploads/images.json", {"file_name": os.path.basename(img), "contents": contents})
            if "id" not in subidas[img]:
                sys.exit(f"Fallo la subida: {subidas[img]}")
            print("Imagen subida:", os.path.basename(img), subidas[img]["id"],
                  f"{subidas[img].get('width')}x{subidas[img].get('height')}")
        up = subidas[img]
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
        "variants": [{"id": v["id"], "price": PRICE_CENTS, "is_enabled": True} for v in enabled],
        "print_areas": print_areas,
    }
    prod = call("POST", f"/shops/{SHOP_ID}/products.json", body)
    if "id" not in prod:
        sys.exit(f"Fallo la creacion: {prod}")
    print("Producto creado en Printify:", prod["id"])

    if a.publish:
        import publicar_existente
        publicar_existente.publicar(prod["id"], a.mockups)
    else:
        print("No publicado. Revisa los mockups en Printify y luego publica.")


if __name__ == "__main__":
    main()
