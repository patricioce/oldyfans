# Lote 2026-11-19 — 80s Survivors Club — 4 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/`: recortados al dibujo. `clara.png` = versión para remeras oscuras, `oscura.png` = para claras.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.

| Diseño | Colores | Imagen | Ubicación |
|---|---|---|---|
| 867 | 6 colores | clara (roja/blanca) en Black, Navy y **Sport Grey** (así lo muestran los mockups); oscura (violeta) en Charcoal, Military Green, White | scale 0.733, y 0.406 (1:1.14) |
| Babysitter | 6 colores | clara en Black y Navy; oscura en el resto | estándar |
| Black Sheep | Charcoal, Military Green, Sport Grey, White (sólo vinieron esos mockups) | unica (negra) | scale 0.61, y 0.462 (1:1.58); 899×1422 px |
| Insert Coin | 6 colores | clara en Black y Navy; oscura en el resto | scale 0.733, y 0.386 (1:1.08). **No vinieron mockups** (el zip trae un `hero-desktop.webp` que no es de este diseño) |

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-19-survivors; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --tienda survivors --image "$D/disenos/867/oscura.png" --image-light "$D/disenos/867/clara.png" \
  --light-colors "Black,Navy,Sport Grey" --y 0.406 --title "867 T-Shirt" --colors "$C"   # --create para crear
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "$D/mockups/867" --apply
```
