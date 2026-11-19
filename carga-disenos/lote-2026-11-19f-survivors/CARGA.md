# Lote 2026-11-19 (f) — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `clara.png` = Black y Navy, `oscura.png` = resto.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| Latchkey Kid | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Processing | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Sponge-Worthy | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| We Do Not Subscribe | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| What Happened | 6 colores | clara en Black y Navy; oscura en el resto | estándar |

## Comandos (desde `carga-disenos/kit`)
```
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "../lote-2026-11-19f-survivors/mockups/<Diseño>" --apply
```
