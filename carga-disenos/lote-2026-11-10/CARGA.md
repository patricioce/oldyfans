# Lote 2026-11-10 — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/unica.png`: Are You Okay y los tres I'll Be In The Garage (2 = auto naranja, 3 = pickup, 4 = moto).
  Diseño único, va igual en todos los colores. Recortados al dibujo (venían en lienzo de 5000x5000).
- `disenos/Retirement Definition/clara.png` (blanca, Black y Navy) y `oscura.png` (negra, el resto). Venían como 8.png y 9.png.
- Tamaño: 85% del modelo (escala por defecto ≈0.733). **Garage: y=0.445** en vez de 0.281: son diseños altos (1:1.3)
  y con la y estándar se salían ~500 px del área de impresión por arriba (área frente 3185x3636).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio, reducidos a 2500 px. Venían numerados:
  - 9 colores (Are You Okay, Garage 2/3/4): 1 Black, 2 Navy, 3 Dark Chocolate, 4 Maroon, 5 Military Green,
    6 Charcoal, 7 Purple, 8 Stone Blue, 9 Sage.
  - 7 colores (Retirement Definition): 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
- Título = nombre de la carpeta + " T-Shirt".

## Script
Al crear Retirement, Printify devolvió el MISMO id para clara-black y clara-navy: ya no alcanza el metadato PNG
(deduplica por píxeles). Ahora cada copia lleva además un píxel de esquina con alfa 1/255 y tono propio del color.
Además `--fix-areas` fallaba porque mandaba los placeholders vacíos (espalda/cuello) con `images: []`; ahora se filtran.
El primer intento (6af30a4b388b693b4c09ed2c) se borró y se recreó.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-10; C9="Black,Charcoal,Dark Chocolate,Maroon,Military Green,Navy,Purple,Sage,Stone Blue"
python3 scripts/printify_new_product.py --image "$D/disenos/I'll Be In The Garage 2/unica.png" --title "I'll Be In The Garage 2 T-Shirt" --colors "$C9" --y 0.445
python3 scripts/printify_new_product.py --image "$D/disenos/Retirement Definition/oscura.png" --image-light "$D/disenos/Retirement Definition/clara.png" \
  --title "Retirement Definition T-Shirt" --colors "Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/<Diseño>" --apply
```
