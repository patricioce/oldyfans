# Lote 2026-11-18 (b) — 80s Survivors Club — 3 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/oscura.png` y `clara.png`: recortados al dibujo, clasificados por luminosidad
  (blanca = `clara.png`, negra/azul = `oscura.png`).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px), numerados 1–6 en los zips:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White.
- **Becoming A Legend**: el mockup de Charcoal lleva la versión blanca, así que la clara va en Black, Navy y
  Charcoal (`--light-colors "Black,Navy,Charcoal"`, un área por color). Los otros dos: clara en Black y Navy.
- Becoming A Legend y Old School vienen en 1200 px (recortados ~1060 px): Printify puede avisar baja resolución.
- Tamaño: 85% del modelo (escala por defecto, ≈0.733).

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-18b-survivors; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --tienda survivors --image "$D/disenos/Old School/oscura.png" \
  --image-light "$D/disenos/Old School/clara.png" --title "Old School T-Shirt" --colors "$C"   # --create para crear
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "$D/mockups/Old School" --apply
```
