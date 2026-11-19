# Lote 2026-11-19 (g) — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `clara.png` = Black y Navy, `oscura.png` = resto, `unica.png` = todos.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| 50 Years | 6 colores | **3 tintas** (según mockups): blanca (`clara`) en Black y Navy, negra (`oscura`) en Military Green y Charcoal, color (`color`, azul/naranja) en Sport Grey y White | y 0.364 (1:1.00). `oscura` es de 1069 px: resolución baja |
| Be Kind Rewind | 6 colores | unica (color) | y 0.390 (1:1.09); 1082 px: resolución baja |
| Do Not Bend | 6 colores | clara en Black y Navy; oscura en el resto | y 0.375 (1:1.03); 966 px: resolución baja |
| How Eye Roll | 6 colores | clara (amarilla) en Black y Navy; oscura en el resto | estándar |
| The Light | Charcoal, Military Green, Sport Grey, White (sólo vinieron esos mockups) | unica (negra) | y 0.384 (1:1.07) |

Ubicación: escala 85% del modelo; en los diseños más altos se baja `y` para que el borde de arriba quede a ≈0.09 (y = 0.09 + 0.2755·alto/ancho).

## Comandos (desde `carga-disenos/kit`)
Crear: `bash ../lote-2026-11-19g-survivors/comandos.sh` (simulación) / `... --create`.
```
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "../lote-2026-11-19g-survivors/mockups/<Diseño>" --apply
```
