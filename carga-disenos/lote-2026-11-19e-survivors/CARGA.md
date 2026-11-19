# Lote 2026-11-19 (e) — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `unica.png` = una sola versión (todos los colores); `clara.png` = Black y Navy, `oscura.png` = resto.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| Figureoutability | Black, Navy, Military Green, Charcoal, Sport Grey | única | estándar |
| Hose Water 2 | Black, Navy, Military Green, Charcoal | única | estándar |
| Nobody Owes You | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Pain | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Retirement Plan | 6 colores | clara en Black y Navy; oscura en el resto | estándar |

## Comandos (desde `carga-disenos/kit`)
```
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "../lote-2026-11-19e-survivors/mockups/<Diseño>" --apply
```
