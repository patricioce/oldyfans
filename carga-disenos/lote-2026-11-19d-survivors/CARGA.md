# Lote 2026-11-19 (d) — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `clara.png` = versión clara (Black y Navy), `oscura.png` = versión oscura (resto).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| Hose Water 3 | 6 colores | **4 tintas** (según mockups): blanca (`clara`) en Black, naranja en Navy, roja en Military Green y Charcoal, oscura en Sport Grey y White. Un área por color especial (`--image-color`) | estándar |
| How Do You Want Your No | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| My Dog | 6 colores | clara en Black y Navy; oscura en el resto | y 0.416 (1:1.18) |
| No Ragrets | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Red Rover Survivor | 6 colores | clara en Black y Navy; oscura en el resto | estándar |

Script: se agregó `--image-color "Color=archivo.png"` (repetible) a `printify_new_product.py` para diseños con más de dos tintas.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-19d-survivors/disenos; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --tienda survivors --image "$D/Hose Water 3/oscura.png" \
  --image-color "Black=$D/Hose Water 3/clara.png" --image-color "Navy=$D/Hose Water 3/naranja.png" \
  --image-color "Military Green=$D/Hose Water 3/roja.png" --image-color "Charcoal=$D/Hose Water 3/roja.png" \
  --title "Hose Water 3 T-Shirt" --colors "$C"     # --create para crear
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "../lote-2026-11-19d-survivors/mockups/<Diseño>" --apply
```
