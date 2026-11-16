# Lote 2026-11-16 — 5 diseños, productos NUEVOS

- `disenos/<Diseño>/`: recortados al dibujo.
  - Record y Warrant: `oscura.png` (venía como 8.png, negra) y `clara.png` (9.png, blanca). La clara va en Black y Navy.
  - Night Owl, Pickles y Patience: `unica.png`, igual en todos los colores.
- Tamaño: 85% del modelo (escala por defecto ≈0.733).
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: mockups de Patricio. Venían numerados:
  - Record / Warrant: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Night Owl: 1 White, 2 Purple, 3 Sage, 4 Stone Blue, 5 Sport Grey, 6 Military Green, 7 Charcoal, 8 Ice Grey.
  - Pickles: 1 Light Blue, 2 Sage, 3 White, 4 Sport Grey, 5 Stone Blue, 6 Ice Grey.
  - Patience: 1 Black, 2 Navy, 3 Military Green, 4 Charcoal.
- `lote.json`: título (nombre de la carpeta + " T-Shirt") y colores (los de los mockups).

## Corrección del cargador en este lote
Al crear Record y Warrant, Printify volvió a deduplicar la clara de Black y Navy (ignora el metadato PNG) y metió
en el área de Navy 17 colores que el catálogo de la API no lista; la corrección automática fallaba porque mandaba la
espalda vacía. Se borraron esos dos borradores y se recrearon con el script corregido:
- cada copia de la clara lleva un píxel casi invisible (alfa 1) distinto por color → imagen distinta para Printify;
- ~~el área general va última~~ ERROR: el editor de Printify toma la **primera** área como diseño general.
  Con Black primera, el editor mostraba la clara como diseño general y en la remera blanca no se veía nada
  (lo marcó Patricio). Corregido con `--fix-areas --apply`: general primera, después Black y Navy (igual que
  I Take Pills), y el PUT asigna TODAS las variantes del producto para que Printify no tire las que no están
  en el catálogo en el área de Navy;
- el PUT de `--fix-areas` omite placeholders sin imágenes;
- la verificación corta si los colores claros comparten imagen.

## Comandos (desde `carga-disenos/kit`)
```
D=../lote-2026-11-16
python3 scripts/publicar_existente.py --printify-id <id> --mockups "$D/mockups/<Diseño>" --apply
```

## Verificación (2026-11-16)
Se bajaron las vistas previas de Printify (images.printify.com) y se compararon color por color con los mockups:
los 5 productos coinciden (Record y Warrant: blanca en Black y Navy, negra en el resto).
