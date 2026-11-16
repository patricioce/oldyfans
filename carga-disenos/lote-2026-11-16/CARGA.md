# Lote 2026-11-16 — productos NUEVOS

- `disenos/<Diseño>/`: PNG recortados al dibujo (venían en lienzo de 5000x5000 con margen transparente).
  - 80s Survivor y Bad Decision: diseño único (`unica.png`), igual en todos sus colores.
  - Crushing It: 8.png = negra (`oscura.png`), 9.png = blanca (`clara.png`).
  - Hairless Snail: 8.png = blanca (`clara.png`), 9.png = negra (`oscura.png`).
  - La clara va en Black y Navy, cada uno en su área; la oscura, en el resto.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`, colores identificados mirando los mockups numerados:
  - 80s Survivor: 1 Light Blue, 2 Sage, 3 White, 4 Sport Grey, 5 Stone Blue, 6 Ice Grey.
  - Bad Decision: 1 Black, 2 Navy, 3 Military Green, 4 Charcoal.
  - Crushing It y Hairless Snail: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
- Título = nombre de la carpeta + " T-Shirt". Tamaño: 85% del modelo (escala por defecto).
- Heart: el zip trae solo mockups (7 colores estándar), falta el PNG del diseño.

## Cambios en el script en este lote
- Printify ya deduplicaba Black y Navy aunque el PNG tuviera el metadato de color (mismo id de subida):
  ahora además se cambia un píxel de la esquina (alpha ≤ 1/255, invisible) con un color derivado del nombre.
- El reacomodo de áreas fallaba porque Printify rechaza placeholders sin imágenes (la espalda vacía):
  ahora se mandan solo los que tienen imágenes. Printify sigue metiendo 17 colores fuera del catálogo
  (Berry, Dark Chocolate, Fan Candy Pink...) en el área de Navy; el script los mueve al área general.
