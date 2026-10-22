# Lote 2026-10-22 — 3 diseños, productos NUEVOS

- `disenos/<Diseño>/oscura.png` (`_negro`) y `clara.png` (`_blanco`): recortados al dibujo (venían con 90 px de margen transparente).
  La clara va en Black y Navy, cada uno en su área y con su propia imagen subida; la oscura, en el resto.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (venían en PNG numerados 1–7, pasados a JPG):
  1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
- `lote.json`: título = nombre de la carpeta + " T-Shirt".

## Correcciones al script en este lote
Al crear, Navy volvió a quedar mal y Black/Navy con la misma imagen subida:
- El catálogo sin `show-out-of-stock=1` trae 425 variantes, pero el producto tiene 524: las que faltaban caían en el área de Navy.
- El PUT de corrección mandaba la espalda vacía y Printify lo rechazaba (`placeholders.1.images ... required`).
- Printify deduplica aunque el PNG tenga otro metadato: ahora además cambia el RGB de un píxel totalmente transparente de la esquina.
Los 3 productos se corrigieron con `--fix-areas <id> --image-light clara.png --apply`.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-10-22; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Don't Worry/oscura.png" --image-light "$D/disenos/Don't Worry/clara.png" \
  --title "Don't Worry T-Shirt" --colors "$C"            # simulación; agregar --create para crear
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Don't Worry" --apply
```
