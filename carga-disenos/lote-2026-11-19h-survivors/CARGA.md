# Lote 2026-11-19 (h) — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `clara.png` = Black y Navy, `oscura.png` = resto, `unica.png` = todos.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| Big Wheel | 6 colores | clara en Black y Navy; oscura en el resto | y 0.383 (1:1.06); 1128 px: resolución baja |
| I'll Be In The Garage 2 | Black, Navy, Military Green, Charcoal (sólo vinieron esos mockups) | unica (color) | y 0.448 (1:1.30) |
| I'll Be In The Garage 4 | Black, Navy, Military Green, Charcoal (sólo vinieron esos mockups) | unica (color) | y 0.450 (1:1.31) |
| Morons | 6 colores | clara en Black y Navy; oscura en el resto | y 0.390 (1:1.09); 1102 px: resolución baja |
| Personal Space | 6 colores | clara en Black y Navy; oscura en el resto | y 0.415 (1:1.18) |

Ubicación: escala 85% del modelo; en los diseños más altos se baja `y` para que el borde de arriba quede a ≈0.09 (y = 0.09 + 0.2755·alto/ancho).

## Comandos (desde `carga-disenos/kit`)
Crear: `bash ../lote-2026-11-19h-survivors/comandos.sh` (simulación) / `... --create`.
```
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "../lote-2026-11-19h-survivors/mockups/<Diseño>" --apply
```
