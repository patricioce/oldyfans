# OldyFans Store — Shopify + Printify (guía para Claude Code)

Leé este archivo primero. Tienda de remeras Gen X (oldyfans.store), print-on-demand con Printify, tema Shopify "BuildMyPOD - Fitness v2.0.0".

## Credenciales (archivo `.env`)
Abrí la carpeta con Claude Code y decile "leé el README". Si no tenés `.env`, copiá `.env.example` a `.env` y completalo con las credenciales que te pasen por gestor de contraseñas.
Todos los tokens y secretos viven en `.env` (en esta carpeta, ya está en .gitignore). Para arrancar: copiar `.env.example` a `.env` y completarlo. Nunca compartir `.env` por chat abierto ni subirlo a un repo.
- `PRINTIFY_TOKEN` → token personal de Printify (Printify > My account > Connections > Personal access token; scopes: shops, catalog, products r/w, uploads r/w). Cada persona genera el suyo.
- `SHOPIFY_ACCESS_TOKEN`, `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET` → app "Claude222" (pedirlos al dueño del proyecto por gestor de contraseñas).
- Claude Code: leer `.env` para las llamadas a las APIs (ej. `set -a; . ./.env; set +a`).

## Datos fijos
- Shopify: dominio API `s0vk8m-gj.myshopify.com`, API `2024-10`, header `X-Shopify-Access-Token`. Tema activo (main): id `187945418797`.
- Printify: shop id `27342731` ("Oldy Fans Store", canal Shopify), API `https://api.printify.com/v1`, headers `Authorization: Bearer` + `User-Agent: Claude`.
- Los productos se crean con el mismo modelo/proveedor de impresión (blueprint 145, provider 99), 39 variantes habilitadas, precio `$42.85` (el 30% de descuento es un descuento automático de Shopify, no cambia el precio base).
- Ubicación estándar del diseño (frente): x=0.5, y≈0.281, scale≈0.862, angle=0. Espalda vacía.

## Cargar un diseño nuevo
```
python3 scripts/printify_new_product.py --image diseno.png --title "Nombre T-Shirt"            # simulación, no crea nada
python3 scripts/printify_new_product.py --image diseno.png --title "Nombre T-Shirt" --create   # crea en Printify, SIN publicar
python3 scripts/printify_new_product.py ... --create --publish                                   # además publica a Shopify
```
Flujo recomendado: crear sin publicar → mirar los mockups → ajustar `--x --y --scale --angle` si hace falta → publicar.
Después del publish, ajustar en Shopify: colecciones, tags, precio tachado, descripción en inglés.

### Diseños con dos tintas (blanca y negra)
Con `--image-light clara.png` el producto lleva dos áreas de impresión: los colores de `--light-colors` (por defecto `Black,Navy`) usan la versión clara y el resto la de `--image` (oscura).
```
python3 scripts/printify_new_product.py --image oscura.png --image-light clara.png --title "Nombre T-Shirt" --colors "Black,Navy,White,Sport Grey"
```

### Antes de subir un diseño
- PNG con fondo transparente. Si llega en WebP/JPG, convertirlo a PNG (si ya trae transparencia, conservarla) y recortarlo al dibujo.
- Resolución: idealmente ~3000 px o más de alto. Con menos, Printify puede avisar baja calidad.
- Diseños altos (más altos que anchos): la escala estándar 0.862 los saca del área de impresión. Probado: `--scale 0.61 --y 0.46` para un diseño de proporción 1:1.58.
- Diseños negros no se ven en remeras oscuras: elegir colores con `--colors "White,Sage,Stone Blue,..."` (nombres exactos del catálogo de Printify; se usan los mismos talles que el modelo).

### Mockups propios
La API de Printify no permite subir mockups propios: se cargan en Shopify, asignando cada foto a las variantes de su color.
Carpeta con un archivo por color, con el nombre del color en el archivo (ej. `black-sheep-sport-grey.jpg`), máx. 20 MB c/u (2500 px alcanza).
```
python3 scripts/printify_new_product.py ... --create --publish --mockups carpeta/     # todo junto: publica OCULTO y carga los mockups
python3 scripts/shopify_mockups.py --printify-id <id> --dir carpeta/                  # simulación sobre un producto ya publicado
python3 scripts/shopify_mockups.py --printify-id <id> --dir carpeta/ --apply --replace --order "White,Purple"   # reemplaza las fotos
```
- Se publica desde Printify con `images: false`, así Printify no pisa los mockups. Si alguien republica desde Printify, dejar destildadas las imágenes.
- OJO: `visible: false` en Printify NO oculta el producto en Shopify. Unos minutos después de publicar, Printify hace una segunda pasada que lo deja activo y visible en la tienda. El script espera esa pasada, recién ahí lo pasa a borrador y lo vigila 5 minutos. Verificar igual en Shopify que quede en borrador.
- El producto queda en borrador: se activa a mano en Shopify después de revisarlo.

## Reglas
- No publicar sin revisar el mockup. Nunca mandar este kit con el `.env` adentro: las credenciales van por gestor de contraseñas. No crear pedidos ni webhooks en Printify. No descargar datos personales de clientes de Shopify.
- Todo el copy del sitio va en inglés (mercado USA).
- Cambios grandes de tema: probar primero en un tema duplicado (no publicado) con `themeDuplicate` y `?preview_theme_id=`.
- No hay API pública de WeScale (app.wescale.ai); se reemplazó su función con este flujo.

## Colores de marca vigentes
Rojo botones `#E73123`, barra de anuncio `#0F6D80`, footer `#0A4F72`, texto claro `#FDFCF9`.
