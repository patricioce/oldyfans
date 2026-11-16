# Lote 2026-11-16 — 3 diseños, productos NUEVOS

- `disenos/<Diseño>/`: recortados al dibujo (venían en 5000x5000 con margen transparente).
  - Big Wheel y Call Me: dos tintas. `oscura.png` (venía como 8.png) y `clara.png` (9.png, blanca) → la clara va en Black y Navy, cada uno en su área.
  - Bigfoot: una sola versión a color (`unica.png`), igual en todos los colores.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg` (2500 px). Venían numerados:
  - Big Wheel / Call Me: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Bigfoot: 1 Light Blue, 2 Sage, 3 White, 4 Sport Grey, 5 Stone Blue, 6 Ice Grey (identificados por el color de la remera).
- Tamaño: 85% del modelo (escala por defecto, ≈0.733).

## Cambio en el script
Printify ya no da ids distintos a la clara de Black y de Navy con solo el metadato PNG (las deduplicó igual).
Ahora `png_con_color` además cambia el RGB de un píxel totalmente transparente (sigue invisible).
Y el reacomodo de áreas fallaba porque Printify rechaza placeholders sin imágenes (la espalda vacía): ya no se mandan.
Los primeros Big Wheel / Call Me (6afaf8e4…, 6afaf903…) se borraron de Printify y se recrearon.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-16; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Call Me/oscura.png" --image-light "$D/disenos/Call Me/clara.png" --title "Call Me T-Shirt" --colors "$C"
python3 scripts/printify_new_product.py --image "$D/disenos/Bigfoot/unica.png" --title "Bigfoot T-Shirt" --colors "Ice Grey,Light Blue,Sage,Sport Grey,Stone Blue,White"
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/<Diseño>" --apply
```
