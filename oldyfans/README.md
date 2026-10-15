# OldyFans: correcciones de la auditoría (2026-10-15)

Material listo para aplicar en Shopify, preparado a partir del doc
"OldyFans: auditoría de inconsistencias, bloqueos de venta e ideas de mejora".
Se generó con los endpoints públicos de la tienda (`products.json` y `/products/<handle>.js`) sobre los **310 productos**, no solo la muestra del doc.
No hubo cambios en Shopify: no hay acceso de escritura desde acá.

Los links "Admin" de los CSV abren el producto en `admin.shopify.com/store/s0vk8m-gj`.

## correcciones/ (listas por producto)

| Archivo | Filas | Qué es | Cómo aplicarlo |
|---|---|---|---|
| `01-variantes-precio-fuera-de-estandar.csv` | 51 variantes / 11 productos | Variantes que no están en $29.99 / $42.85. Incluye Hose Water (versión fem) con XS a **$11.52**, probablemente por debajo del costo de Printify. | Revisar cada una: si no es intencional, poner 29.99 / 42.85 desde el link Admin o el bulk editor. |
| `02-variantes-foto-color-incorrecto.csv` | 54 variantes / 9 productos | Variante Ice Grey con la foto `7-sand`. Afecta a Former Contender, Odd Ball, Free Range Human, I Don't Care, Peaked, Meets Minimum Requirements, Top Banana, No Further Questions y Dodge Ball Survivor. | En cada producto: Ice Grey → cambiar imagen de variante por la foto Ice Grey. Si no hay foto Ice Grey, generar el mockup con el skill `oldyfans-mockups`. |
| `03-alt-text-a-corregir.csv` | 1.884 imágenes / 298 productos | 1.191 con código de fecha de Printify como alt y 693 vacíos. Trae el alt sugerido "Producto - Color" (sacado de la variante asociada a la imagen). | Con Matrixify / una app de alt text, o a mano en los más vendidos primero. |
| `04-handles-y-titulos.csv` | 39 | Handles con typos (`apalogies`, `midelife`, `wll-seasoned`, `morder`, `therpy`), sufijo `-1`, títulos sin "T-Shirt" y títulos numerados ("80s Fan 2", "Daily Dose 1/2/3"…). | Cambiar el handle en el producto (tildar "Create a URL redirect"). Los numerados piden decisión: renombrar o unificar. |
| `07-redirects-shopify-import.csv` | 24 | Redirects 301 de los handles viejos a los nuevos (excluye los que chocan con un duplicado). | Solo si NO usaste el tilde de redirect: Online Store → Navigation → URL Redirects → Import. |
| `08-productos-duplicados.csv` | 5 pares | Mismo título publicado dos veces: Circle Back, Fixer, Well Seasoned, Whatever y Hose Water. | Comparar diseños. Si son iguales, despublicar el más nuevo y redirigirlo al más viejo (que tiene las reseñas). |
| `05-talles-faltantes.csv` | 819 combinaciones / 294 productos | Colores sin 3XL (796) o sin XL y 3XL (22). | Informativo: es lo que ofrece Printify por color. Si el proveedor lo permite, habilitar 3XL. |
| `06-orden-de-opciones-color-talle.csv` | 229 | Productos con opciones Color/Talle (los nuevos usan Talle/Color). | Informativo; reordenar opciones solo si el tema lo muestra raro. |

## textos/ (copiar y pegar)

| Archivo | Dónde va |
|---|---|
| `01-refund-policy.md` | Settings → Policies → Refund policy |
| `02-shipping-policy.md` | Settings → Policies → Shipping policy (completar costos) |
| `03-sellos-y-bloques-de-ficha.md` | Theme editor: sellos de la home, íconos y acordeones de la ficha, footer, barra de anuncios |
| `04-faq.md` | Bloque FAQ de la home y de la ficha |
| `05-terms-y-contacto.md` | Terms of service (2 reemplazos) y página Contact |
| `06-menu-y-colecciones.md` | Navigation → Main menu y limpieza de colecciones |

## scripts/
`auditoria_catalogo.py` regenera los CSV de `correcciones/` (instrucciones de uso arriba del archivo).
