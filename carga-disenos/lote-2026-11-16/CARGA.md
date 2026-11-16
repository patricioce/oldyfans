# Lote 2026-11-16 — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/`: recortados al dibujo. Invaders tiene dos tintas (`oscura.png` = 8.png, `clara.png` = 9.png; la clara va en Black y Navy).
  Los otros cuatro tienen una sola versión (`unica.png`), que va igual en todos los colores.
- Odd Duck traía un velo de alfa casi invisible (alfa 1–4) en todo el fondo: se limpió (alfa ≤ 4 → 0) antes de recortar.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio, numerados en el zip:
  - Invaders: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey
  - Odd Duck / Old Dog: 1 White, 2 Purple, 3 Sage, 4 Stone Blue, 5 Sport Grey, 6 Military Green, 7 Charcoal, 8 Ice Grey
  - Bigfoot (carpeta "Bigfoot 2"): 1 Light Blue, 2 Sage, 3 White, 4 Sport Grey, 5 Stone Blue, 6 Ice Grey
  - Mona Lisa Trick: 1 Black, 2 Navy, 3 Military Green, 4 Charcoal
- Títulos: nombre de la carpeta + " T-Shirt" ("Bigfoot 2" → "Bigfoot T-Shirt": no había otro Bigfoot en la tienda).

## Ubicación
Los diseños altos con la ubicación estándar (scale 0.733, y 0.281) se salían del área por arriba. Se usó el precedente
del README (borde superior del diseño en ≈0.04 del área):
| Diseño | proporción alto/ancho | scale | y |
|---|---|---|---|
| Invaders | 0.51 | 0.733 | 0.281 (estándar) |
| Bigfoot | 1.08 | 0.733 | 0.386 |
| Old Dog | 1.13 | 0.733 | 0.403 |
| Mona Lisa Trick | 1.25 | 0.733 | 0.442 |
| Odd Duck | 1.69 | 0.571 | 0.462 (alto = 0.844 del área, como el precedente 0.61/0.46) |

## Arreglos al script en este lote
- Printify ahora deduplica también por píxeles: el metadato PNG ya no alcanzaba y Black/Navy recibían el mismo id.
  `png_con_color` además cambia el RGB de un píxel totalmente transparente según el color.
- `--fix-areas`/normalización: el PUT mandaba el placeholder de la espalda con `images` vacío y Printify lo rechazaba.
  Ahora se omiten los placeholders sin imágenes.
- Invaders (creado antes del arreglo) se corrigió por API: áreas reacomodadas y una imagen propia para Black y otra para Navy.
