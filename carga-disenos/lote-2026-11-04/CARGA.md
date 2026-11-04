# Lote 2026-11-04 — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/oscura.png` y `clara.png`: recortados al dibujo (venían en lienzo 5000×5000 con mucho margen transparente).
  La clara (blanca) va en Black y Navy; la oscura, en el resto. Cada color claro con su propia área e imagen subida.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio, reducidos de 5000 a 2500 px. Venían numerados 1–7:
  - Second Rodeo, Unwilling Participant, Wait, What, Whiskey Tango Foxtrot: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Sarcasm (otro orden): 1 Military Green, 2 Black, 3 Navy, 4 Charcoal, 5 White, 6 Sport Grey, 7 Ice Grey.
- Archivos originales: en Sarcasm `Sarcasm w.png` = clara y `Sarcasm b.png` = oscura; en Second Rodeo `9.png` = clara;
  en los demás `8.png` = clara.
- `lote.json`: título y colores. La carpeta "Wait, what_" (el `?` no se puede en nombres de archivo) es "Wait, What" y el título "Wait, What? T-Shirt".

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-04; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Sarcasm/oscura.png" --image-light "$D/disenos/Sarcasm/clara.png" \
  --title "Sarcasm T-Shirt" --colors "$C"            # simulación; agregar --create para crear
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Sarcasm" --apply
```
