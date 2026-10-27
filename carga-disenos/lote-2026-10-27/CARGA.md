# Lote 2026-10-27 — 2 diseños, productos NUEVOS

- **Allegedly** (`disenos/Allegedly/oscura.png` y `clara.png`, venían como 9.png y 8.png): dos tintas.
  La clara va en Black y Navy, cada uno con su área y su propia imagen subida; la oscura, en el resto. 7 colores.
- **My Wife Knows Everything** (`disenos/My Wife Knows Everything/unica.png`, venía como 9.png): una sola tinta (negra).
  En el zip el 8.png era OTRO diseño ("I don't have the time or the crayons to explain it to you") y no había
  mockups de Black ni Navy, así que se carga solo en los 5 colores claros: White, Sport Grey, Military Green, Charcoal, Ice Grey.
- Diseños recortados al dibujo (venían en 5000x5000 con margen transparente). Tamaño: 85% del modelo (escala ≈0.733).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio, reducidos a 2500 px. Venían numerados:
  1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.

## Correcciones al cargador (en este lote)
- Printify volvió a meter variantes de 18 colores en el área de Navy y el PUT de corrección se rechazaba porque
  reenviaba la espalda con `images: []`. Ahora se mandan solo los placeholders con imagen y solo los campos de ubicación.
- El metadato PNG no alcanzaba: Printify le dio a Navy el mismo id de imagen que a Black. Ahora cada copia lleva además
  un píxel transparente con alfa 1/255 (invisible) en otra posición. En Allegedly Navy se corrigió por API con su propia subida.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-10-27
python3 scripts/printify_new_product.py --image "$D/disenos/Allegedly/oscura.png" --image-light "$D/disenos/Allegedly/clara.png" \
  --title "Allegedly T-Shirt" --colors "Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/disenos/My Wife Knows Everything/unica.png" \
  --title "My Wife Knows Everything T-Shirt" --colors "Charcoal,Ice Grey,Military Green,Sport Grey,White"
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/<Diseño>" --apply
```
