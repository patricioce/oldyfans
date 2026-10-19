# Prompts de diseño OldyFans — ChatGPT y Gemini

Basado en "OldyFans — WeScalers Prompting System" (oct 2026) y en los diseños aprobados de la tienda.

## Cómo usarlo

1. **Paso 1 (igual para los dos):** abrí un chat nuevo, adjuntá la imagen de referencia y pegá el PROMPT 1 con la frase completada. Te devuelve la ecuación de la referencia y 3 opciones en el estilo OldyFans.
2. **Paso 2:** elegí una opción y pegá el PROMPT 2 de la herramienta que estés usando (ChatGPT o Gemini). Genera la versión de **tinta oscura** (para remeras claras).
3. **Paso 3:** pegá el PROMPT 3 para la versión de **tinta clara** (para Black y Navy).
   - Atajo más fiel: como el diseño es de una sola tinta, en Photoshop podés hacer la versión clara bloqueando la transparencia de la capa y rellenándola de blanco. Queda idéntica, cosa que el modelo no siempre logra.
4. **Después:** sacar fondo (Gemini), escalar a 4500×5400 px y revisar letra por letra que el texto esté bien escrito.

Notas:
- ChatGPT: elegí formato vertical si te lo ofrece. Si en vez de transparencia aparece un cuadriculado gris y blanco "dibujado", pedí: `The checkerboard is fake. Re-export with real alpha transparency.`
- Gemini: si sale cuadrada, pedí: `Same image, portrait 4:5 aspect ratio.`
- Para ver otra opción, repetí el PROMPT 2 cambiando el número.

---

## PROMPT 1 — Análisis + 3 opciones (ChatGPT y Gemini)

Adjuntar la imagen de referencia. Completar `[PHRASE]` respetando los saltos de línea.

```
You are a senior t-shirt graphic designer for OldyFans, a US apparel brand. Do NOT generate any image yet. This step is text only.

I attached a REFERENCE design. My phrase for the new design is (keep exact spelling, punctuation, capitalization and line breaks):
"""
[PHRASE]
"""

STEP A — Break the REFERENCE into its design equation:
DESIGN EQUATION = PRINT STYLE + GRAPHIC DESIGN STYLE + MOOD
- PRINT STYLE: how it is physically made (screen print, embroidery, patch, distressed print, etc.)
- GRAPHIC DESIGN STYLE: typefaces, layout, hierarchy, illustration, ornaments
- MOOD: tone of the humor and the feeling it gives
Keep it to one line per layer.

STEP B — Propose 3 different design options for my phrase in the OLDYFANS HOUSE STYLE below. The reference is only inspiration for mood and idea: do NOT copy its colors, layout, materials, logos, signatures or watermarks.

OLDYFANS HOUSE STYLE
- Audience: adults 40+ (Gen X and boomers) in the US. Humor is deadpan, sarcastic, self-deprecating, often nostalgic for a 70s/80s childhood (unsupervised kids, playground games, "back in my day").
- Typography is the design. The phrase must read instantly from 3 meters away.
- Allowed type styles (max 2 per design):
  1. Condensed athletic / collegiate block sans-serif, all caps, tight leading
  2. Retro baseball-script with a swash tail underline, used for ONE accent word or line
  3. Chunky 70s soft-serif (Cooper Black feel)
  4. Classic roman serif capitals
  5. Bold hand-lettered marker caps
- Layout: centered, stacked lines, strong hierarchy. The punchline gets the emphasis (bigger size, or a switch to script).
- Optional: ONE simple iconic illustration (e.g. a ball, a toy, stick-figure kids) in single-color line art, centered, with the text above/below or arched around it like a badge. Only if it makes the joke stronger.
- Optional: light vintage distress, but only as small hard-edged holes knocked out of the ink (no soft grain, no gray).
- ONE ink color only. Flat color, clean sharp edges. No gradients, shadows, glows, outlines in a second color, 3D, or photo effects.
- No frames, boxes, patches, filled shapes or background panels: the shirt color shows through the negative space and is part of the design.
- Composition: front chest print, 5:6 portrait proportion, centered, even margins.

Each option must use this format:
OPTION [N] — [short name]
- Design equation: Flat one-color screen print + [graphic design style] + [mood]
- Type styles: ...
- Layout: line by line, what is big, what is small, what is script, any illustration
- Why it works: one sentence

Then stop and wait for me to pick an option.
```

---

## PROMPT 2 — ChatGPT (fondo transparente, tinta oscura)

```
Generate OPTION [N] as a print-ready t-shirt graphic.

- Text, exactly as written, nothing added or removed, every letter spelled correctly:
"""
[PHRASE]
"""
- Design equation: Flat one-color screen print + [graphic design style of OPTION N] + [mood of OPTION N]
- Follow the OLDYFANS HOUSE STYLE and the layout of OPTION [N].
- Ink: a single flat color, pure black #000000. No other colors, no gray, no gradients, no shadows, no soft grain. If distressed, only hard-edged holes.
- Background: REAL transparent background (alpha channel, PNG). Not white, not gray, not a checkerboard pattern.
- No t-shirt, no mockup, no frame, no border, no patch, no watermark, no signature, no extra text.
- Portrait canvas (vertical). Compose the design for a 5:6 front chest print area: centered, even margins, filling about 85% of the width.
- Flat 2D artwork, clean sharp edges, high resolution.
```

## PROMPT 2 — Gemini (fondo liso, tinta oscura)

```
Generate OPTION [N] as a print-ready t-shirt graphic.

- Text, exactly as written, nothing added or removed, every letter spelled correctly:
"""
[PHRASE]
"""
- Design equation: Flat one-color screen print + [graphic design style of OPTION N] + [mood of OPTION N]
- Follow the OLDYFANS HOUSE STYLE and the layout of OPTION [N].
- Ink: a single flat color, pure black #000000. No other colors, no gray, no gradients, no shadows, no soft grain. If distressed, only hard-edged holes.
- Background: one solid flat pure white #FFFFFF, perfectly uniform edge to edge. No texture, no paper, no vignette, no lighting, no shadow under the design. It will be removed with a background eraser, so the ink and the background must never blend.
- No t-shirt, no mockup, no frame, no border, no patch, no watermark, no signature, no extra text.
- Portrait 4:5 aspect ratio. Compose the design for a 5:6 front chest print area: centered, even margins, filling about 85% of the width.
- Flat 2D artwork, clean sharp edges, high resolution.
```

---

## PROMPT 3 — Versión de tinta clara (Black y Navy)

ChatGPT:

```
Now make the light-ink version of this exact image. Keep everything identical: same text, typefaces, layout, size, position, illustration and distress holes. Only change the ink from black to pure white #FFFFFF. Real transparent background (alpha channel, PNG), not a checkerboard pattern. No other changes.
```

Gemini:

```
Now make the light-ink version of this exact image. Keep everything identical: same text, typefaces, layout, size, position, illustration and distress holes. Only change the ink from black to pure white #FFFFFF, and the background to one solid flat pure black #000000, perfectly uniform edge to edge. Portrait 4:5. No other changes.
```
