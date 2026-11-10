# Lote 2026-11-10 — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/`: recortados al dibujo.
  - Retirement Definition / Retirement Review: dos tintas. `oscura.png` (venía como 8.png, negra) y `clara.png` (9.png, blanca).
    La clara va en Black y Navy, cada uno en su área y con su propia imagen subida.
  - Hedgehog, Keep On Truckin 2, TV Game Switch: una sola versión (`unica.png`), igual en todos los colores.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio. Venían numerados; el color se identificó por muestreo:
  - Retirement (los dos): 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Hedgehog: 1 Black, 2 Navy, 3 Dark Chocolate, 4 Maroon, 5 Military Green, 6 Charcoal, 7 Purple, 8 Stone Blue, 9 Sage.
  - Keep On Truckin 2: 1–7 igual que Hedgehog.
  - TV Game Switch: 1 Light Blue, 2 Stone Blue, 3 Sage, 4 White, 5 Sport Grey, 6 Military Green, 7 Charcoal, 8 Ice Grey.
- Tamaño: 85% del modelo (escala por defecto ≈0.733).

## Incidencias al crear
En los dos Retirement, Printify (1) le dio el mismo id a la clara de Black y de Navy (deduplica por píxeles: el metadato
PNG no alcanzaba) y (2) metió 17 colores deshabilitados en el área de Navy; la corrección automática falló porque el PUT
mandaba el placeholder de espalda vacío. Se corrigió el script (pixel transparente distinto por color, sin placeholders
vacíos, y corta si dos claras reciben el mismo id) y se arreglaron los dos productos por PUT.

## Comandos (desde `carga-disenos/kit`)
```
python3 scripts/publicar_existente.py --printify-id <id> --mockups "../lote-2026-11-10/mockups/<Diseño>" --apply
```
