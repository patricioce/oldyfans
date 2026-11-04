# Lote 2026-11-04 — productos NUEVOS

Mockups venían numerados 1–7: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
Se guardaron como `mockups/<Diseño>/<Diseño> - <Color>.jpg` (reducidos a 2500 px).

- **But Did You Die**: `oscura.png` = `Disenos/9.png` recortado. No vino versión blanca: `clara.png` se generó
  recoloreando la oscura a blanco (mismo alfa), coincide con los mockups de Black y Navy. Clara en Black y Navy.
  (El zip traía también `8.png` = "UNWILLING PARTICIPANT", otro diseño sin mockups: no se carga.)
- **My Dog Thinks I'm Cool**: vino aparte en WebP 2000 px (baja resolución). `clara.png` = versión celeste,
  `oscura.png` = versión roja. Según los mockups la celeste va en **Black, Navy y Sport Grey**
  (`--light-colors "Black,Navy,Sport Grey"`), la roja en White, Military Green, Charcoal e Ice Grey.
- **Sarcasm Detected**: diseño llegó en un zip aparte: `oscura.png` = `Disenos/8.png`, `clara.png` = `Disenos/9.png` (recortados). Clara en Black y Navy.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-04/disenos; C="Black,Charcoal,Ice Grey,Military Green,Navy,Sport Grey,White"
python3 scripts/printify_new_product.py --image "$D/But Did You Die/oscura.png" --image-light "$D/But Did You Die/clara.png" \
  --title "But Did You Die T-Shirt" --colors "$C"
python3 scripts/printify_new_product.py --image "$D/My Dog Thinks I'm Cool/oscura.png" --image-light "$D/My Dog Thinks I'm Cool/clara.png" \
  --light-colors "Black,Navy,Sport Grey" --title "My Dog Thinks I'm Cool T-Shirt" --colors "$C"
```
