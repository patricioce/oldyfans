# Lote 2026-11-19 (c) — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `clara.png` = versión clara (Black y Navy), `oscura.png` = versión oscura (resto).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| Father | 6 colores | clara (cian) en Black y Navy; oscura (roja) en el resto | y 0.343 (1:0.92); 1064 px de ancho: resolución baja |
| Invaders | 6 colores | clara en Black y Navy; oscura en el resto | estándar (scale 0.733, y 0.281) |
| Music Helps | 6 colores | clara en Black y Navy; oscura en el resto | y 0.358 (1:0.97); 1069 px de ancho: resolución baja |
| Retirement Definition | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Social Vegan | 6 colores | clara en Black y Navy; oscura en el resto | estándar |

Ubicación: escala 85% del modelo; en los diseños más altos se baja `y` para que el borde de arriba quede a ≈0.09 (y = 0.09 + 0.2755·alto/ancho).

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-19c-survivors; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --tienda survivors --image "$D/disenos/Father/oscura.png" \
  --image-light "$D/disenos/Father/clara.png" --title "Father T-Shirt" --colors "$C" --y 0.343   # --create para crear
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "$D/mockups/Father" --apply
```
