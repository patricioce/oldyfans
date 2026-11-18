# Lote 2026-11-18 — 80s Survivors Club — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/`: recortados al dibujo. Antisocial y Hose Water: `oscura.png` + `clara.png` (clara en Black y Navy).
  Hang In There y Slow Me Down: `unica.png` (igual en todos los colores). Wise Man: pendiente (Patricio manda versión corregida).
- Mockups venían numerados 1–6: 1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.
  Hang In There y Wise Man solo traen 5 y 6 → solo Sport Grey y White.
- Los originales son de 1200 px (Antisocial 2048 px): Printify puede avisar baja calidad.
- **Va a la tienda 80s Survivors Club, NO a OldyFans**: Printify shop 29697371 (canal Shopify, token `SURVIVORS_PRINTIFY_TOKEN`)
  y Shopify `drysff-xt.myshopify.com` (80ssurvivorsclub.com). Vendor "80s Survivors Club", precio 29.99 / tachado 42.85.
  Además una colección manual "80s Survivors Club" dentro de esa tienda con los productos del lote.
- La tienda estaba vacía: el modelo es el "10 p.m T-Shirt" de OldyFans exportado a JSON (sin tags de tema), vía `PRINTIFY_TEMPLATE_JSON`.
- `SURVIVORS_SHOPIFY_ACCESS_TOKEN` es en realidad el client secret (`shpss_`): el token de Admin API (`shpat_`, dura 24 h) se pide con
  `POST https://drysff-xt.myshopify.com/admin/oauth/access_token` grant_type=client_credentials + client_id + client_secret.
- Variables para correr los scripts contra esta tienda: PRINTIFY_TOKEN, PRINTIFY_SHOP_ID=29697371, PRINTIFY_TEMPLATE_JSON,
  SHOPIFY_SHOP_DOMAIN, SHOPIFY_ACCESS_TOKEN (shpat_), SHOPIFY_VENDOR="80s Survivors Club" (exportadas pisan al .env).

## Script
- Printify ya no distingue Black/Navy solo por el metadato PNG (salían con el mismo id): `png_con_color` ahora
  además cambia el alfa de un píxel transparente de una esquina (distinta por color).
- `--fix-areas`/normalización: el PUT fallaba porque iban placeholders vacíos (espalda); ahora solo van los que tienen imágenes.

## Publicación
- Printify creó los productos en Shopify pero nunca devolvió `external.id`, así que `publicar_existente.py` cortó por timeout
  y Printify los dejó ACTIVOS con Vendor "Printify". Se pasaron a borrador a mano y se terminó con `scripts/terminar_publicacion.py`.
- SKUs de Shopify = SKUs de Printify (36/36 en Antisocial). Colección manual "80s-survivors-club" con los 4, sin publicar en canales.
