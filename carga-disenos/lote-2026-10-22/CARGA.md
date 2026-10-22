# Lote 2026-10-22 — 3 diseños, productos NUEVOS

- `disenos/<Diseño>/oscura.png` (venía como `_negro`) y `clara.png` (`_blanco`): recortados al dibujo (venían con 40 px de margen transparente).
  La clara va en Black y Navy, cada uno con su propia área; la oscura, en el resto.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733). Son diseños apaisados (≈2.3–3:1).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio (PNG → JPG). Venían numerados 1–7:
  1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
- `lote.json`: título = nombre de la carpeta + " T-Shirt".

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-10-22; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Trouble/oscura.png" --image-light "$D/disenos/Trouble/clara.png" \
  --title "Trouble T-Shirt" --colors "$C"            # simulación; agregar --create para crear
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Trouble" --apply
```
