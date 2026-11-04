# Lote 2026-11-04 — 1 diseño (Father), producto NUEVO

- `disenos/Father/oscura.png` (líneas negras, puntos rojos) y `clara.png` (líneas blancas, puntos celestes):
  llegaron en WebP 1125x1125 con transparencia; convertidos a PNG y recortados al dibujo (1095x984).
  Resolución baja para Printify (ideal ~3000 px): puede avisar baja calidad.
- La clara va en Black y Navy (cada uno con su área y su imagen subida); la oscura en el resto.
- `mockups/Father/Father - <Color>.jpg`: mockups de Patricio (venían 1–7 a 5000 px, reducidos a 2500 px):
  1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
- Título: nombre de la carpeta + " T-Shirt" (no había productos con "Father" en Shopify ni Printify).

## Corrección del script en este lote
- Printify deduplicó clara-black y clara-navy aunque tenían metadato PNG distinto (mismo id de imagen).
  Ahora `png_con_color` además cambia un píxel totalmente transparente a alpha 1–9 según el color
  (invisible al imprimir), y el script corta antes de crear si dos colores claros reciben el mismo id.
- El PUT de `normalizar_areas` mandaba el placeholder de la espalda con `images: []` y Printify lo rechazaba
  (code 8150): ahora se omiten los placeholders sin imágenes.
- El producto ya creado se corrigió por API (subida nueva para Black y Navy + PUT de print_areas).

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-04
python3 scripts/publicar_existente.py --printify-id 6aeb334d4c4394b66205f918 --mockups "$D/mockups/Father" --apply
```
