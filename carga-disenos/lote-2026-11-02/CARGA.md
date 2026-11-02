# Lote 2026-11-02 — 6 diseños, productos NUEVOS

- Títulos = nombre del zip + " T-Shirt" (ya existen "Hose Water", "Hose Water 3", "Slow Me Down", "Slow Me Down 2": estos son versiones nuevas, no se tocan los viejos).
- `disenos/<Diseño>/`: recortados al dibujo. Dos tintas (`oscura.png` = 8.png, `clara.png` = 9.png): Hose Water 4, I'm Fine, Old People, Slow Me Down 3.
  Una sola versión (`unica.png`): Here Comes The Sun (amarillo) y Lincoln (negro).
- Mockups (venían numerados):
  - Dos tintas: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Here Comes The Sun: 1 Black, 2 Navy, 3 Military Green, 4 Charcoal, 5 Dark Chocolate, 6 Maroon, 7 Purple (identificados por color de la foto).
  - Lincoln: 1 White, 2 Sport Grey, 3 Military Green, 4 Charcoal, 5 Ice Grey.
- Tamaño: 85% del modelo (escala por defecto ≈0.733).

## Arreglos al cargador en este lote
- Printify ya ignora el metadato PNG: clara-black y clara-navy salían con el mismo id. Ahora cada copia lleva
  un píxel totalmente transparente con RGB distinto (invisible) y Printify le da un id propio (probado).
- El PUT de áreas fallaba (code 8150) porque mandaba la espalda vacía (`placeholders.1.images` requerido):
  ahora se omiten los placeholders sin imágenes.
- Los 4 de dos tintas se corrigieron en el lugar (clara-navy propia + áreas reacomodadas), sin recrearlos.

## Comandos (desde `carga-disenos/kit`)
```
python3 scripts/publicar_existente.py --printify-id <id> --mockups "../lote-2026-11-02/mockups/<Diseño>" --apply
```
