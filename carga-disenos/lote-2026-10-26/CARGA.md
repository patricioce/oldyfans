# Lote 2026-10-26 — 6 diseños, productos NUEVOS

- `disenos/<Diseño>/oscura.png` y `clara.png`: recortados al dibujo (venían en lienzos de 5000x5000).
  Venían como 8.png/9.png: en Who Came First la blanca es 8.png; en el resto, 9.png.
- **Surprise Party** vino sin versión blanca: 8.png era otro diseño ("Don't try to change him", no se usó) y 9.png la negra.
  La clara se armó desde la negra pasando el negro a blanco con el mismo alfa (coincide con los mockups de Black/Navy).
- **Diapers** ("Don't try to change him") llegó después en su propio zip, con blanca (9.png) y negra (8.png).
- La clara va en Black y Navy, cada uno con su área y su propia imagen subida; la oscura, en el resto.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (reducidos a 2500 px). Venían numerados 1–7:
  1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.

## Navy / Black: corrección del script
Con este lote Printify devolvió el mismo id de imagen para clara-black y clara-navy pese al metadato PNG
(deduplica por píxeles). Ahora cada copia cambia el alfa de un píxel invisible de la primera fila, y el script
corta antes de crear si dos colores claros reciben el mismo id. Además, el reacomodo de áreas fallaba porque
mandaba la espalda vacía (`images: []`), que Printify rechaza: ya no se manda.
Los 5 productos del primer intento se borraron (borradores sin publicar) y se recrearon.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-10-26; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Gifted/oscura.png" --image-light "$D/disenos/Gifted/clara.png" \
  --title "Gifted T-Shirt" --colors "$C"            # simulación; agregar --create para crear
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Gifted" --apply
```
