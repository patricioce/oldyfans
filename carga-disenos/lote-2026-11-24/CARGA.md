# Lote 2026-11-24 — Sandwich Generation, producto NUEVO

No confundir con "80s Survivor T-Shirt" (otro diseño). En Printify ya existía un "Sandwich Generation T-Shirt"
viejo (6a8c44a761a8fed568047ef1): NO se toca; este lote crea uno nuevo.

## Tres tintas (según los mockups de Patricio)
| Versión | Archivo | Colores |
|---|---|---|
| texto blanco | `clara.png` | Black, Navy, Charcoal (cada uno con su área) |
| texto negro | `oscura.png` | White, Sport Grey, Military Green |
| texto rojo | `roja.png` | Ice Grey (su área) |

- Los diseños venían en WebP 2000×2000 con transparencia: pasados a PNG y recortados con el MISMO recuadro
  (28,82,1971,1948) para que las tres queden en la misma posición y tamaño.
- `clara.png`: se limpiaron unas manchas violetas en la línea del piso (no estaban en la negra ni la roja).
  Los mockups de Black/Navy/Charcoal todavía muestran un puntito violeta debajo del bastón.
- Mockups: venían numerados 1–7 → 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey
  (verificado mirando cada foto).

## Comandos (desde `carga-disenos/kit`)
```
D="../lote-2026-11-24/disenos/Sandwich Generation"
python3 scripts/printify_new_product.py --image "$D/oscura.png" --image-light "$D/clara.png" \
  --light-colors "Black,Navy,Charcoal" --image-for "Ice Grey=$D/roja.png" \
  --title "Sandwich Generation T-Shirt" --colors "Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"   # + --create
python3 scripts/printify_new_product.py --fix-areas <id> --light-colors "Black,Navy,Charcoal,Ice Grey"   # revisar áreas
python3 scripts/publicar_existente.py --printify-id <id> --mockups "../lote-2026-11-24/mockups/Sandwich Generation" --apply
```

## Cambios en el script en este lote
- `--image-for "Color=archivo.png"` (repetible): otra versión para un color puntual, con área propia.
- Printify devolvió el mismo id para la clara de Black/Charcoal/Navy aunque llevaban metadato distinto:
  ahora cada copia lleva además un píxel transparente con alpha 1/255 en un lugar distinto por color, y el
  script corta antes de crear si dos subidas devuelven el mismo id.
- El reacomodo de áreas fallaba (Printify rechaza placeholders de espalda con `images` vacío): ahora se omiten.
