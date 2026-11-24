# Lote 2026-11-24 — 5 diseños, productos NUEVOS (tienda OldyFans, no 80s Survivors Club)

- `disenos/<Diseño>/`: recortados al dibujo (venían en lienzos de 5000x5000).
  - First Word You See y 8-Bit Bat: dos tintas (`Disenos/8.png` = oscura, `9.png` = clara).
  - Bounty Hunter, Cool Bands 2, Ducks In A Row: `unica.png`, igual en todos los colores.
- First Word You See: en los mockups la versión blanca va en Black, Navy, **Military Green y Charcoal**,
  así que se creó con `--light-colors "Black,Navy,Military Green,Charcoal"` (un área por color).
- Ubicación: 85% del modelo (0.733) salvo Bounty Hunter (alto 1:1.39 → `--scale 0.62 --y 0.38`).
  Ducks (`--y 0.33`) y Cool Bands 2 (`--y 0.30`) bajados un poco para no salirse por arriba.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`. Los números de los zips eran:
  - First Word / 8-Bit Bat / Bounty Hunter: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Cool Bands 2: 1 Black, 2 Navy, 3 Sport Grey, 4 Military Green, 5 Charcoal, 6 Dark Chocolate, 7 Purple.
  - Ducks In A Row: 1 Military Green, 2 Charcoal, 3 Purple, 4 Stone Blue, 5 Sage, 6 White, 7 Sport Grey, 8 Ice Grey.
- Ya existe "Cool Bands T-Shirt" (handle cool-bands): no se tocó; Cool Bands 2 es otro producto.

## Arreglos al script en este lote
- Printify ahora deduplica las subidas por píxeles: el metadato PNG ya no alcanzaba y Black/Navy recibían el mismo id.
  `png_con_color` cambia además un píxel de esquina (alpha 1, invisible) distinto por color.
- `--fix-areas`/normalización: el PUT mandaba los placeholders vacíos (espalda, cuello) y Printify lo rechazaba.
  Ahora solo manda placeholders con imágenes.
- Los dos primeros intentos de First Word You See y 8-Bit Bat quedaron mal y se borraron (no estaban publicados).
