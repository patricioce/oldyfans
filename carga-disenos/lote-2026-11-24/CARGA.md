# Lote 2026-11-24 — "Miss You" (bici BMX azul + texto rojo), producto NUEVO

- No confundir con "80s Survivor T-Shirt" (otro producto de la tienda): este es un producto aparte.
- `disenos/Miss You/unica.png`: diseño de una sola versión (azul + rojo), va igual en todos los colores.
  Llegó como WebP de 1125 px; se recortó al dibujo (1014x996) y se escaló x3 a 3042x2988 (sin detalle extra: pedir original en alta si Printify avisa baja calidad).
- `mockups/Miss You/`: mockups de Patricio, venían numerados 1–12 (5000 px, reducidos a 2500 px):
  1 Black, 2 Navy, 3 Dark Chocolate, 4 Maroon, 5 Military Green, 6 Charcoal, 7 Purple, 8 Stone Blue, 9 Sage, 10 White, 11 Sport Grey, 12 Ice Grey.
- Tamaño: 85% del modelo (escala por defecto ≈0.733).

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-24
python3 scripts/printify_new_product.py --image "$D/disenos/Miss You/unica.png" --title "Miss You T-Shirt" \
  --colors "Black,Charcoal,Dark Chocolate,Ice Grey,Maroon,Military Green,Navy,Purple,Sage,Sport Grey,Stone Blue,White"
python3 scripts/publicar_existente.py --printify-id 6b0589043deddaecb50e6617 --mockups "$D/mockups/Miss You" --apply
```
