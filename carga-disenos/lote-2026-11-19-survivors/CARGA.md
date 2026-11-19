# Lote 2026-11-19 — 80s Survivors Club — 4 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/oscura.png` y `clara.png`: recortados al dibujo (Level Up: misma caja para las dos versiones).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados 1–6 en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.
- Clara en Black y Navy (un área por color); oscura en el resto. Tamaño 85% del modelo (escala por defecto).

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-19-survivors; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --tienda survivors --image "$D/disenos/See-Saw/oscura.png" \
  --image-light "$D/disenos/See-Saw/clara.png" --title "See-Saw T-Shirt" --colors "$C"   # --create para crear
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "$D/mockups/See-Saw" --apply
```
