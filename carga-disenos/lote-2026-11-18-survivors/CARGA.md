# Lote 2026-11-18 — 80s Survivors Club — 5 diseños, productos NUEVOS

**Tienda: 80s Survivors Club** (Printify 29697371, Shopify drysff-xt). Todos los comandos llevan `--tienda survivors`.
No es OldyFans.

- `disenos/<Diseño>/oscura.png` y `clara.png`: recortados al dibujo. Las dos versiones venían en cada zip
  (nombres sin sentido); se clasificaron por luminosidad: blanca = `clara.png` (Black y Navy, cada uno en su área),
  negra = `oscura.png` (resto).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (1080 px). Venían numerados 1–6, iguales en los 5:
  1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Sport Grey, 6 White (deducidos mirando los mockups).
- `lote.json`: título = nombre de la carpeta del zip ("Wise Man T-Shirt", etc.) y esos 6 colores.
- Tamaño: 85% del modelo (escala por defecto, ≈0.733).
- Kit: rama con `scripts/tienda.py` + los arreglos de dedup/áreas del lote 2026-11-16.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-18-survivors; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --tienda survivors --image "$D/disenos/Wise Man/oscura.png" \
  --image-light "$D/disenos/Wise Man/clara.png" --title "Wise Man T-Shirt" --colors "$C"   # agregar --create para crear
python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "$D/mockups/Wise Man" --apply
```
