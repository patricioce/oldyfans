# Lote 2026-11-04 — 1 diseño, producto NUEVO

- `disenos/Scrabble/unica.png`: diseño a todo color de una sola versión ("Fifty Is Only 14 In Scrabble"),
  recortado al dibujo (venía en un lienzo de 5000x5000 con margen transparente). Va igual en todos los colores.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733).
- `mockups/Scrabble/Scrabble - <Color>.jpg`: mockups de Patricio, reducidos de 5000 a 2500 px. Venían numerados 1–7:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Dark Chocolate, 6 Purple, 7 Maroon
  (colores identificados por el tono de la remera; Charcoal y Military Green coinciden exacto con los mockups del lote 2026-10-21).
- `lote.json`: título y colores. Título = nombre de la carpeta + " T-Shirt".

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-04; C="Black,Charcoal,Dark Chocolate,Maroon,Military Green,Navy,Purple"
python3 scripts/printify_new_product.py --image "$D/disenos/Scrabble/unica.png" --title "Scrabble T-Shirt" --colors "$C"   # simulación; agregar --create
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Scrabble" --apply
```
