# Lote 2026-10-21 — 4 diseños, productos NUEVOS

- `disenos/<Diseño>/oscura.png` y `clara.png`: recortados al dibujo (venían con 90 px de margen transparente).
  La clara va en Black y Navy (en I'm Ride Or Die la clara es la amarilla); la oscura, en el resto.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733). Black y Navy llevan cada uno su área con la clara,
  y **cada uno con su propia imagen subida** (ver abajo).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio. Venían numerados 1–7:
  1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
- `lote.json`: título y colores. No había productos previos con estos diseños: título = nombre de la carpeta + " T-Shirt".

## Navy
En el lote 2026-10-20 Navy apareció en el editor de Printify con el diseño regular y Patricio lo corrigió a mano.
Por API las áreas estaban bien, pero Black y Navy compartían la misma imagen subida (Printify deduplica las subidas
por contenido). Ahora el script sube la clara una vez por color con un metadato PNG del color, así cada una tiene
un id propio, y después de crear relee el producto y corta con error si algún color no quedó en su área.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-10-21; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Lost My Mind/oscura.png" --image-light "$D/disenos/Lost My Mind/clara.png" \
  --title "Lost My Mind T-Shirt" --colors "$C"            # simulación; agregar --create para crear
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Lost My Mind" --apply
```
