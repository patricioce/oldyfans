---
name: oldyfans-disenos-texto
description: "Crear diseños de remera OldyFans de solo texto (frases): dada una frase, armar una placa con 5 opciones de tipografía/armado; cuando Patricio elige una, entregarla en PNG con texto blanco y otro con texto negro, fondo transparente. Usar cuando Patricio pase una frase para remera y pida opciones, una placa o un diseño de texto."
---

# Diseños de solo texto OldyFans

Responder siempre en español. Patricio es el dueño de OldyFans (oldyfans.store). Las remeras son para gente grande con humor sobre la edad: frases cortas en inglés, en mayúsculas, con un remate.

Todo lo necesario viene en la skill:
- `scripts/texto.py`: arma la **placa** de opciones y la **entrega** en PNG, a partir de un spec JSON.
- `fonts/`: tipografías (todas OFL de Google Fonts): `BebasNeue`, `Anton`, `LeagueGothic`, `Oswald-Bold`, `BarlowCondensed-ExtraBold`, `BigShouldersDisplay-Black`, `Antonio-Bold`, `FjallaOne`, `AlfaSlabOne`, `ArchivoBlack`.
- `ejemplos/ride-or-die.json`: el spec del primer diseño aprobado. Copiarlo como punto de partida.

## Flujo (3 pasos)

1. **Patricio da una frase.** Si no está claro dónde se corta (qué es la frase principal y qué el remate), no preguntar: probar los cortes posibles como opciones distintas en la placa.
2. **Placa con 5 opciones.** Escribir el spec en un archivo de trabajo, en una carpeta nueva (no dentro de la skill), y correr:
   ```
   python3 -I <skill>/scripts/texto.py placa --spec opciones.json --out placa.png
   ```
   Abrir la placa y mirarla antes de mandarla: que nada se corte, que se lea y que las 5 opciones sean distintas entre sí. Mandarla con SendUserFile (`render`) y una lista corta: número, nombre de la opción y qué la distingue. Después vienen rondas de ajuste. Patricio suele pedir cambiar cortes de línea o textos sobre la opción que le gustó. Cada ronda es una placa nueva con 2 o 3 variantes en el mismo spec.
3. **Entrega.** Cuando elige una opción:
   ```
   python3 -I <skill>/scripts/texto.py entregar --spec opciones.json --opcion <id> --out entrega/
   ```
   Esto genera `<nombre>_blanco.png`, `<nombre>_negro.png` (fondo transparente, 4500 px de ancho de texto + 2% de margen, 300 dpi) y `<nombre>_preview.png`, que muestra cada versión sobre remera oscura y clara. La entrega usa **la misma textura (semilla) que la placa**, así que sale idéntica a lo aprobado. Si pide otro color, agregarlo: `--colores blanco,negro,mostaza` (o un hex, `#1C2D50`). Mirar la preview y mandar los PNG + preview con SendUserFile (`attach`). Avisar que los archivos están en una carpeta temporal y que los baje.

## Estilo aprobado (no cambiar sin pedido de Patricio)
Referencias: *Hair would only slow me down* (mostaza, muy gastado) y *A wise man once said nothing* (negro, poco gastado).
- **Bloque justificado:** cada línea se escala para ocupar el mismo ancho (`"modo": "ancho"`, el default). Es el estilo que Patricio eligió. Las líneas con menos letras salen más grandes: eso se usa a propósito para destacar.
- **Base:** Bebas Neue. **El remate** (la parte graciosa, donde tiene que ir la vista) va en **Anton**, más gruesa, y tiene que quedar **más grande** que la frase principal. La medida aprobada es de 1,3 a 1,6 veces la altura de la primera línea. Más de eso (por ejemplo "9 PM" solo, a todo el ancho, unas 3 veces) le pareció **demasiado**.
- Truco para agrandar el remate sin exagerar: pasar palabras o puntos suspensivos a la línea principal. Así quedó "I'M RIDE OR DIE..." / "UNTIL 9 PM" (aprobado). Con "...UNTIL 9 PM" abajo el remate salía más chico.
- **Forma ideal: cuadrada**, con las dos frases ocupando lo mismo (`"parejas": true`, que iguala alturas sumando un poco de espacio entre letras, con tope). Pero **si hay conflicto, manda que el remate sea grande**: un diseño en franja de 2 líneas está bien.
- **Gastado:** `"gastado": 1.0` (el default) es el aprobado. 0.45 es el liviano, tipo *A wise man*. Las motas quedan transparentes: se ve el color de la remera a través, como en serigrafía.
- **Colores de la placa:** mostaza `#E2A614` por defecto. En la placa inicial se pueden variar (negro, rojo `#B22820`, azul `#1C2D50`, verde `#2E523A`) para que las opciones se distingan. La entrega siempre es blanco + negro. El mostaza se entrega si lo pide (ya lo pidió una vez).

## Las 5 opciones de la placa inicial
Que sean realmente distintas: cortes de línea, tipografía y jerarquía. Una buena base para empezar:
1. Bloque justificado en Bebas Neue (siempre incluirla: es la favorita).
2. Bloque justificado en Bebas Neue con el remate en Anton y grande (la fórmula aprobada).
3. Centrado parejo, mismo tamaño en todas las líneas (`"modo": "alto"`), en Anton, poco gastado, como *A wise man*.
4. Mezcla de pesos: frase en una letra pesada (Archivo Black / Alfa Slab One) y remate en una angosta (League Gothic).
5. Condensada alta (Big Shoulders / League Gothic) o slab vintage (Alfa Slab One).

## Formato del spec
```json
{
  "frase": "I'M RIDE OR DIE... UNTIL 9 PM",
  "nombre": "im-ride-or-die-until-9pm",
  "opciones": [
    {
      "id": 1,
      "titulo": "Remate grande",
      "detalle": "Bebas arriba, remate en Anton",
      "color": "mostaza",
      "gastado": 1.0,
      "interlineado": 0.035,
      "separacion_frases": 0.035,
      "parejas": false,
      "bloques": [
        [{"texto": "I'M RIDE OR DIE...", "fuente": "BebasNeue"}],
        [{"texto": "UNTIL 9 PM", "fuente": "Anton"}]
      ]
    }
  ]
}
```
- `bloques`: una lista por frase. Cada frase es una lista de líneas.
- Por línea: `texto`, `fuente` (nombre del archivo en `fonts/` sin `.ttf`) y opcionalmente:
  - `modo`: `"ancho"` (default, ocupa el ancho del bloque) o `"alto"` (con `"alto": 0.2`, altura fija en fracción del ancho, centrada).
  - `escala`: fracción del ancho; por ejemplo `0.75` para una línea más angosta y centrada.
  - `tracking`: espacio entre letras, en fracción del tamaño.
- `interlineado` y `separacion_frases`: espacio entre líneas y entre frases, en fracción del ancho.
- `semilla` (opcional): fija la textura. Si no se pone, es `11 + posición` de la opción. No cambiar el orden de las opciones entre la placa y la entrega, o usar `semilla`.
- `nombre`: nombre base de los archivos. Si falta, se arma con la frase.

## Notas
- Las tipografías ya están en `fonts/`, no hace falta internet. Para sumar una nueva, bajar el TTF de Google Fonts, por ejemplo `curl -s "https://fonts.googleapis.com/css2?family=Nombre"` y del CSS tomar la URL `.ttf`, y guardarlo en `fonts/`.
- No subir nada a Printify/Shopify. Para mockups está `oldyfans-mockups` y para cargar productos, `oldyfans-carga-disenos`.
