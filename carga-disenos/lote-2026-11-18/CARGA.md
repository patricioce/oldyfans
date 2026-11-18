# Lote 2026-11-18 — 80s Survivors Club — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/`: recortados al dibujo. Antisocial y Hose Water: `oscura.png` + `clara.png` (clara en Black y Navy).
  Hang In There y Slow Me Down: `unica.png` (igual en todos los colores). Wise Man: pendiente (Patricio manda versión corregida).
- Mockups venían numerados 1–6: 1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.
  Hang In There y Wise Man solo traen 5 y 6 → solo Sport Grey y White.
- Los originales son de 1200 px (Antisocial 2048 px): Printify puede avisar baja calidad.
- Colección de Shopify "80s Survivors Club": nueva, manual, con los productos del lote.

## Script
- Printify ya no distingue Black/Navy solo por el metadato PNG (salían con el mismo id): `png_con_color` ahora
  además cambia el alfa de un píxel transparente de una esquina (distinta por color).
- `--fix-areas`/normalización: el PUT fallaba porque iban placeholders vacíos (espalda); ahora solo van los que tienen imágenes.
