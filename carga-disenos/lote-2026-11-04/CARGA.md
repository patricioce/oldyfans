# Lote 2026-11-04 — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/`: recortados al dibujo.
  - Alibi: dos tintas (`clara.png` = 8.png blanca en Black y Navy; `oscura.png` = 9.png negra en el resto).
  - Openly Gray, Tutto Passa, 80s Survivor: una sola versión (`unica.png`) en todos los colores.
  - **Sarcasm Detected: el zip no trae el PNG del diseño** (solo mockups). Pendiente.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio, reducidos a 2500 px. Venían numerados:
  - Alibi y Sarcasm Detected: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Openly Gray y Tutto Passa: 1 Light Blue, 2 Stone Blue, 3 Sage, 4 White, 5 Sport Grey, 6 Military Green, 7 Charcoal, 8 Ice Grey.
  - 80s Survivor: 1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Dark Chocolate, 6 Purple, 7 Maroon.
  (Los nombres de color se dedujeron mirando los mockups.)
- Título = nombre de la carpeta + " T-Shirt". Tamaño: 85% del modelo (escala por defecto).

## Cambio en el script
Printify ya no da id propio a la clara de Navy solo por el metadato PNG (Black y Navy salieron con la misma imagen
subida). `png_con_color` ahora además cambia el RGB de un píxel totalmente transparente del borde (invisible).
Y al reacomodar áreas se mandan solo los placeholders con imagen (con la espalda vacía Printify rechazaba el PUT).
El primer Alibi (6aeb15bc74b27e78040a932f, no publicado) salió mal por esto y se borró.
