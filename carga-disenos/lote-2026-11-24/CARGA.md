# Lote 2026-11-24 — 5 diseños, productos NUEVOS

(No es el lote "80s Survivors Club".)

- Zips: Gamer, We Raised Ourselves, Whatever, Happily Analog, Memories.
- `disenos/<Diseño>/`: recortados al dibujo (venían en 5000x5000 con margen transparente).
  - Gamer: dos tintas. `oscura.png` (8.png, negra) y `clara.png` (9.png, blanca) en Black y Navy.
  - We Raised Ourselves, Whatever, Happily Analog: `unica.png`, igual en todos los colores.
  - Memories: el zip NO trae el PNG del diseño. Pendiente.
- `mockups/<Diseño>/<Diseño> - <Color>.jpg`: venían numerados; colores identificados mirando cada foto:
  - Gamer / We Raised Ourselves: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey.
  - Whatever: 1 Black, 2 Navy, 3 Dark Chocolate, 4 Maroon, 5 Military Green, 6 Charcoal, 7 Purple.
  - Happily Analog: 1 Black, 2 Dark Chocolate, 3 Maroon, 4 Navy, 5 Military Green, 6 Charcoal, 7 Purple.
  - Memories (12): 1 Black, 2 Navy, 3 Dark Chocolate, 4 Maroon, 5 Military Green, 6 Charcoal, 7 Purple,
    8 Stone Blue, 9 Sage, 10 White, 11 Sport Grey, 12 Ice Grey.
- Título: nombre del diseño + " T-Shirt". Tamaño: 85% del modelo (default del script).

## Arreglos al script en este lote
- La clara de Black y Navy recibía el MISMO id de Printify aunque llevara el metadato PNG del color
  (Printify deduplica por píxeles). Ahora además se marca un píxel de la esquina con alpha 1 y RGB propio del color.
- El reacomodo de áreas (PUT) fallaba con "placeholders.1.images field is required": se mandaba la espalda vacía.
  Ahora se omiten los placeholders sin imágenes.
