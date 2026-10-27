# Lote 2026-10-27 — 4 diseños, productos NUEVOS

- `disenos/<Diseño>/oscura.png` y `clara.png`: recortados al dibujo (venían en lienzo de 5000×5000).
  Venían como `8.png`/`9.png`: en todos la oscura era la 8, salvo Crayons (oscura = 9).
  La clara (blanca) va en Black y Navy; la oscura, en el resto.
- Tamaño: 85% del modelo (escala por defecto del script, ≈0.733).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio, reducidos de 5000 a 2500 px. Venían numerados 1–7
  (verificado por color de la remera): 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
- `lote.json`: título y colores. Título = nombre de la carpeta + " T-Shirt" ("I´m Trying" con apóstrofo recto).

## Qué pasó al crear
Con el script anterior, Black y Navy recibieron el mismo id de imagen (Printify deduplicó las copias aunque tenían
metadatos PNG distintos) y Navy quedó con 18 colores deshabilitados en su área; la corrección automática falló porque
Printify rechaza el PUT con el placeholder `back` vacío. Se corrigió en el script:
- `png_con_color` ahora cambia el RGB de un píxel totalmente transparente del borde (invisible): eso sí da un id propio.
- `normalizar_areas` saca los placeholders sin imágenes antes del PUT.
Los 4 productos ya creados se corrigieron en el lugar (sin duplicar): clara subida aparte para Black y para Navy y
3 áreas (oscura / Black / Navy) con todas las variantes. Verificado por API.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-10-27; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/Hesitate/oscura.png" --image-light "$D/disenos/Hesitate/clara.png" \
  --title "Hesitate T-Shirt" --colors "$C"            # simulación; agregar --create para crear
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/Hesitate" --apply
```
