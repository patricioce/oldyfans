# Lote 2026-11-04 — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/oscura.png` y `clara.png` (o `unica.png`): recortados al dibujo (venían en lienzo 5000x5000).
  La clara (blanca) va en Black y Navy, cada uno en su área y con su propia imagen subida; la oscura, en el resto.
  - Aging Review: 10.png = oscura, 9.png = clara. Morons: 8 = oscura, 9 = clara. Personal Space: 9 = oscura, 8 = clara.
  - Record Sunset: un solo diseño (`unica.png`), igual en todos los colores. Ningún color oscuro tipo Black/Navy.
  - Did You Die: el zip trae `9.png` = "But did You diE?" (oscura) y `8.png` = "UNWILLING PARTICIPANT" (otro diseño).
    Falta la versión clara de "But did you die?" (los mockups de Black/Navy la muestran). **No creado: pendiente.**
- Tamaño: 85% del modelo (escala por defecto, ≈0.733).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`. Venían numerados:
  - dos tintas: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Record Sunset: 1 Military Green, 2 Charcoal, 3 Dark Chocolate, 4 Maroon, 5 Purple, 6 White, 7 Sport Grey, 8 Ice Grey.
- Título = nombre de la carpeta + " T-Shirt".

## Arreglos del script en este lote
- Printify deduplica las subidas por píxeles: el metadato PNG no alcanzaba y Black/Navy recibían el mismo id.
  Ahora `png_con_color` además marca un píxel de esquina con alfa 1/255 (invisible), distinto por color.
- Al reacomodar áreas, Printify rechazaba el PUT por el placeholder de la espalda sin imágenes: ahora se mandan
  solo los placeholders con imágenes.
- Los 3 primeros intentos de dos tintas (6aeb165a…, 6aeb167e…, 6aeb16a8…) quedaron mal y se borraron antes de publicarse.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-04
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/<Diseño>" --apply
```
