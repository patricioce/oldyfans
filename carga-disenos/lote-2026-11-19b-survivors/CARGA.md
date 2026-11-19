# Lote 2026-11-19 (b) — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `clara.png` = blanca (Black y Navy), `oscura.png` = negra (resto), `unica.png` = igual en todos.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| Still Alive | 6 colores | clara en Black y Navy (un área cada uno); oscura en el resto | estándar (scale 0.733, y 0.281) |
| Hairless Snail | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Sasquatch | 6 colores | unica (color) | y 0.308 (1:0.79) |
| 80s Survivor | Sport Grey, White (sólo vinieron esos mockups) | unica (color) | y 0.346 (1:0.93) |
| Bigfoot 2 | Sport Grey, White | unica (color) | y 0.382 (1:1.06); 1131×1200 px: Printify puede avisar baja resolución. **Los mockups del zip son los de 80s Survivor**: faltan los propios |

Ubicación: escala 85% del modelo; en los diseños más altos se baja `y` para que el borde de arriba quede a la misma altura (≈0.09).

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-19b-survivors; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --tienda survivors --image "$D/disenos/Still Alive/oscura.png" \
  --image-light "$D/disenos/Still Alive/clara.png" --title "Still Alive T-Shirt" --colors "$C"   # --create para crear
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "$D/mockups/Still Alive" --apply
```
