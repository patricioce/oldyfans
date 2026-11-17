# Lote 2026-11-16 — productos NUEVOS

- `disenos/<Diseño>/unica.png`: una sola versión (tinta única), va igual en todos los colores. Recortados al dibujo.
  - Smart Ass: venía en la carpeta "Smart Ass 2" (5000x5000). Ya existe "Smartass T-Shirt" (6adf4e4dcb4bc654040ae191): no se tocó.
  - Sasquatch: vino como imagen suelta en WebP 2000x2000 → PNG 1879x1490 (resolución baja, Printify puede avisar).
- Mockups (numerados en los zips):
  - Smart Ass: 1 White, 2 Purple, 3 Sage, 4 Stone Blue, 5 Sport Grey, 6 Military Green, 7 Charcoal, 8 Ice Grey.
  - Sasquatch: 1 Light Blue, 2 Sage, 3 White, 4 Sport Grey, 5 Stone Blue, 6 Ice Grey.
- Heart: dos tintas (diseño llegó aparte el 17/11: 8.png = oscura, 9.png = clara). Clara en Black y Navy.
  Mockups: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.

## Arreglo del script (17/11)
Printify devolvió el MISMO id para clara-black y clara-navy: ahora deduplica por píxeles e ignora el metadato PNG.
`png_con_color` ahora también cambia el alfa de un píxel de la esquina (1–3, invisible) distinto por color.
Además `--fix-areas` fallaba (error 8150) porque reenviaba la espalda con `images` vacío: ahora se omite.
Heart se corrigió en el lugar (sin recrearlo): nueva subida para Black y Navy y PUT de las áreas.
- Tamaño: 85% del modelo (escala por defecto).
