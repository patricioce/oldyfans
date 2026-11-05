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
- Los productos se crean con el mismo modelo/proveedor de impresión (blueprint 145, provider 99), 39 variantes habilitadas. Precio: en Printify `$29.99` (así una republicación desde Printify vuelve a 29.99); en Shopify **price 29.99 y compare_at 42.85 en todas las variantes** y **Vendor `OldyFans`** (de eso depende la marca en Google Shopping y Meta Catalog). El descuento automático del 30% venció el 2026-10-13: el descuento ahora es el precio tachado.
- Ubicación estándar del diseño (frente): x=0.5, y≈0.281, angle=0, escala = 85% de la del modelo (≈0.733; el modelo usa 0.862). Espalda vacía.

## Cargar un diseño nuevo
```
python3 scripts/printify_new_product.py --image diseno.png --title "Nombre T-Shirt"            # simulación, no crea nada
python3 scripts/printify_new_product.py --image diseno.png --title "Nombre T-Shirt" --create   # crea en Printify, SIN publicar
python3 scripts/printify_new_product.py ... --create --publish                                   # además publica a Shopify
```
Flujo recomendado: crear sin publicar (`--create`) → revisar en el editor de Printify → ajustar `--x --y --scale --angle` si hace falta → publicar con `publicar_existente.py`.
OJO: `--create --publish` crea un producto NUEVO; para publicar uno ya creado usá `publicar_existente.py`.

Al publicar, el script espera a que Printify cree el producto en Shopify (consulta el `external.id` del producto en Printify, con timeout) y después, por la Admin API GraphQL:
- `productVariantsBulkUpdate`: price `29.99` y compareAtPrice `42.85` en todas las variantes,
- `productUpdate`: Vendor `OldyFans`.
Lo hace dos veces (al terminar Printify y al final, por si Printify lo pisó) e imprime un resumen: producto, variantes actualizadas, vendor y errores.
Después del publish, ajustar en Shopify: colecciones, tags, descripción en inglés.

### Verificación después de cargar
- La salida del script tiene que terminar con `Precio y marca en Shopify: <handle> | ... | errores: ninguno` y `Verificado en Shopify: ... vendor: OldyFans | precio/tachado: OK`.
- Con dos tintas, después de `--create` tiene que decir `OK Black -> clara-black.png` y `OK Navy -> clara-navy.png` (si algo no cierra, corta con error antes de publicar).
- Revisar el producto en el editor de Printify (`https://printify.com/app/editor/<id>`): tiene que aparecer el diseño propio para Black **y** para Navy.
- Chequeo rápido de un producto en Shopify: `python3 scripts/repair_products.py --handle <handle>` tiene que decir "Nada para corregir".

### Diseños con dos tintas (blanca y negra)
Con `--image-light clara.png` los colores de `--light-colors` (por defecto `Black,Navy`) usan la versión clara y el resto la de `--image` (oscura). Cada color claro lleva su **propia área de impresión** (una para Black y otra para Navy): así el editor de Printify lo muestra como "specific design for Black / for Navy". Con los dos juntos en una sola área, el editor no lo reconoce.
**Por qué Navy quedaba sin su diseño:** el script mandaba solo las variantes habilitadas y Printify tiraba todas las demás (cientos de variantes deshabilitadas de otros colores, y hasta los talles XS/4XL/5XL de Black) en la **última** área, que era la de Navy. El editor toma esa área como el diseño general, y Navy dejaba de tener diseño propio. Ahora el script reparte **todas** las variantes del catálogo: el área de cada color claro tiene solo ese color (todos sus talles) y todo lo demás va en el área de la oscura. Después de crear, relee el producto, reacomoda las áreas si Printify las cambió y corta con error si algo no quedó bien.
Para revisar o corregir un producto ya creado: `python3 scripts/printify_new_product.py --fix-areas <printify_id>` (simulación) y agregar `--apply` para corregirlo.
Además, Black y Navy tienen que tener **imágenes subidas distintas**: Printify deduplica las subidas por contenido, y con la misma imagen en las dos áreas el editor mostraba Navy con el diseño regular. El script sube la clara una vez por color con un metadato PNG del color (id propio para cada una) y, después de crear, relee el producto y corta con error si algún color no quedó en su área.
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
python3 scripts/publicar_existente.py --printify-id <id> --mockups carpeta/ --apply  # publica en borrador un producto YA creado (sin duplicarlo)
python3 scripts/shopify_mockups.py --printify-id <id> --dir carpeta/                  # simulación sobre un producto ya publicado
python3 scripts/shopify_mockups.py --printify-id <id> --dir carpeta/ --apply --replace --order "White,Purple"   # reemplaza las fotos
```
- Se publica desde Printify con `images: false`, así Printify no pisa los mockups. Si alguien republica desde Printify, dejar destildadas las imágenes.
- OJO: `visible: false` en Printify NO oculta el producto en Shopify. Unos minutos después de publicar, Printify hace una segunda pasada que lo deja activo y visible en la tienda. El script espera esa pasada, recién ahí lo pasa a borrador y lo vigila 5 minutos. Verificar igual en Shopify que quede en borrador.
- El producto queda en borrador: se activa a mano en Shopify después de revisarlo.

## Reparar precio tachado y Vendor en todo el catálogo
`scripts/repair_products.py` recorre todos los productos de Shopify (Admin API GraphQL, paginado con cursor; nunca el storefront público) y detecta:
- Vendor distinto de `OldyFans`,
- variantes con price 29.99 o 42.85 cuyo compare_at está vacío o es menor/igual que el price.
Las variantes con otros precios no se tocan (se cuentan al final). No toca envíos ni perfiles de envío.
```
python3 scripts/repair_products.py                                   # simulación de todo el catálogo
python3 scripts/repair_products.py --handle lost-my-mind-t-shirt     # simulación de UN producto
python3 scripts/repair_products.py --handle lost-my-mind-t-shirt --apply   # probar primero con uno
python3 scripts/repair_products.py --apply                           # todo el catálogo
```
Con `--apply`: guarda un backup en `backups/repair-AAAAMMDD-HHMMSS.json` (id, handle, vendor y precio/compare_at de cada variante) **antes** de escribir; después corrige de a un producto con una pausa de ~0.4 s (reintenta ante respuestas no-JSON o throttling). Es idempotente: lo que ya está bien lo saltea. Al final relee el catálogo y cuenta cuántos productos quedan con Vendor "Printify" y cuántas variantes sin tachado.
Si un producto se republica desde Printify, Printify vuelve a poner su precio (29.99), puede borrar el tachado y volver a poner Vendor "Printify": correr el repair después.

### Volver atrás con el backup
```
python3 scripts/repair_products.py --restore backups/repair-AAAAMMDD-HHMMSS.json            # simulación: muestra qué restauraría
python3 scripts/repair_products.py --restore backups/repair-AAAAMMDD-HHMMSS.json --apply    # deja vendor y precios como estaban
```

## Reglas
- No publicar sin revisar el mockup. Nunca mandar este kit con el `.env` adentro: las credenciales van por gestor de contraseñas. No crear pedidos ni webhooks en Printify. No descargar datos personales de clientes de Shopify.
- Todo el copy del sitio va en inglés (mercado USA).
- Cambios grandes de tema: probar primero en un tema duplicado (no publicado) con `themeDuplicate` y `?preview_theme_id=`.
- No hay API pública de WeScale (app.wescale.ai); se reemplazó su función con este flujo.

## Colores de marca vigentes
Rojo botones `#E73123`, barra de anuncio `#0F6D80`, footer `#0A4F72`, texto claro `#FDFCF9`.
