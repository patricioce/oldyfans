# Lote 2026-11-10 — 1 diseño, producto NUEVO

- `disenos/Metal Slide 2/unica.png`: diseño de una sola versión ("Over 100 Million Butts Served", azul marino y rojo),
  recortado al dibujo (venía 5000x5000 en PNG paletizado con margen transparente; convertido a RGBA).
  Va igual en todos los colores (solo colores claros: no hay Black ni Navy).
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733).
- `mockups/Metal Slide 2/Metal Slide 2 - <Color>.jpg`: mockups de Patricio, reducidos de 5000 a 2500 px. Venían numerados 1–7:
  1 White, 2 Sand, 3 Sage, 4 Light Blue, 5 Stone Blue, 6 Sport Grey, 7 Ice Grey
  (identificados por el tono de la remera, comparando con los mockups de "Hang In There" del lote 2026-10-15).
- Ya existe "Metal Slide T-Shirt" (Printify 6a4bb88bfa1cf48f0f036a13): no se toca. Este es un producto nuevo: "Metal Slide 2 T-Shirt".

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-10; C="Ice Grey,Light Blue,Sage,Sand,Sport Grey,Stone Blue,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Metal Slide 2/unica.png" --title "Metal Slide 2 T-Shirt" --colors "$C"   # simulación; --create para crear
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Metal Slide 2" --apply
```
