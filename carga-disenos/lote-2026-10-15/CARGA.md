# Lote 2026-10-15 — 4 diseños, productos NUEVOS

- `disenos/<Diseño>/oscura.png` y `clara.png`: diseño recortado al dibujo. La clara va en Black y Navy; la oscura, en el resto.
  `unica.png` (Hang In There): diseño a color, va igual en todos.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733). Black y Navy llevan cada uno su área con la clara.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups aprobados por Patricio (2500 px).
- `lote.json`: título y colores de cada producto (los que ya vende cada diseño en oldyfans.store).

Ya existen productos publicados con estos diseños (Wise Man, Antisocial, Hang In There, I Had Potential T-Shirt).
Patricio pidió crearlos igual como productos nuevos, en borrador. No tocar los productos existentes.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-10-15
# simulación (no crea nada)
python3 scripts/printify_new_product.py --image "$D/disenos/I Had Potential/oscura.png" --image-light "$D/disenos/I Had Potential/clara.png" \
  --title "I Had Potential T-Shirt" --colors "Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
# crear sin publicar: agregar --create
# publicar en borrador un producto ya creado, con los mockups propios:
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/I Had Potential" --apply
# Hang In There: solo --image "$D/disenos/Hang In There/unica.png" (sin --image-light)
```
