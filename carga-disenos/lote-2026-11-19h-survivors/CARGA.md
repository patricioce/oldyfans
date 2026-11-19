# Lote 2026-11-19 (h) — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `clara.png` = Black y Navy, `oscura.png` = resto, `unica.png` = todos.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| Bigfoot | Sport Grey, White (sólo vinieron esos mockups) | unica (color) | y 0.387 (1:1.08) |
| No Photos Please | 6 colores | clara en Black y Navy; oscura en el resto | y 0.340 (1:0.91); 1879 px: resolución baja |
| Odd Duck | Military Green, Sport Grey, White (sólo vinieron esos mockups) | unica (negra) | scale 0.57, y 0.452 (1:1.69, muy alto; mismo criterio que Black Sheep) |
| Retirement Definition | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Retirement Review | 6 colores | clara en Black y Navy; oscura en el resto | estándar |

Ubicación: escala 85% del modelo; en los diseños más altos se baja `y` para que el borde de arriba quede a ≈0.09 (y = 0.09 + 0.2755·alto/ancho).

## Comandos (desde `carga-disenos/kit`)
Crear: `bash ../lote-2026-11-19h-survivors/comandos.sh` (simulación) / `... --create`.
```
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "../lote-2026-11-19h-survivors/mockups/<Diseño>" --apply
```
