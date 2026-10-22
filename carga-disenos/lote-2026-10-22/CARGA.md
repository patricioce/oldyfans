# Lote 2026-10-22 — 1 diseño, producto NUEVO

- `disenos/Five Bucks/oscura.png` y `clara.png`: recortados al dibujo (venían con 90 px de margen transparente).
  La clara (blanca, "Five Bucks.png") va en Black y Navy; la oscura ("..._negro.png"), en el resto.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733). Black y Navy llevan cada uno su área con la clara.
- `mockups/Five Bucks/Five Bucks - <Color>.jpg`: mockups de Patricio. Venían numerados 1–7:
  1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
- `lote.json`: título y colores. Título = nombre de la carpeta + " T-Shirt".

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-10-22; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Five Bucks/oscura.png" --image-light "$D/disenos/Five Bucks/clara.png" \
  --title "Five Bucks T-Shirt" --colors "$C"            # simulación; agregar --create para crear
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Five Bucks" --apply
```
