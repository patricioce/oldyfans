---
name: oldyfans-mockups
description: "Crear mockups de remeras OldyFans: poner los diseños (PNG) sobre las fotos de remeras vacías en los colores de cada producto, con el diseño centrado y en el mismo lugar en todas las variantes, y entregar zip + vista previa + GIF de cambio de variante. Usar cuando Patricio pase diseños de OldyFans (zip, carpetas o PNG) y pida mockups."
---

# Mockups de remeras OldyFans

Responder siempre en español. Patricio es el dueño de OldyFans (oldyfans.store).

Todo lo necesario viene en la skill:
- `assets/blanks/` — 13 remeras vacías YA CENTRADAS (2500 px): Black, Charcoal, Ice Grey, Military Green, Navy, Sport Grey, White, Brown, Light Blue, Maroon, Sage, Sand, Stone Blue. No volver a procesarlas.
- `assets/blanks.json` — por color: archivo, `light_ink` (true solo en Black y Navy) y las medidas usadas para centrarla.
- `scripts/mockups.py` — pega los diseños y genera, por diseño: los JPG, `<Diseño> - preview.jpg`, `<Diseño> - cambio de variante.gif` y `reporte.json`.
- `scripts/store_colors.py` — busca en oldyfans.store qué colores vende ya cada diseño y arma `map.json`.
- `scripts/center_blanks.py` — solo para agregar una remera vacía nueva (ver al final).

## Reglas aprobadas (no volver a preguntar ni cambiar sin pedido de Patricio)
Se llegó a esto después de varias rondas de prueba con Patricio y su jefe:
- **El diseño va en el MISMO lugar en todas las variantes** (mismos píxeles), para que al cambiar de color en la tienda no se mueva. Por eso la posición es fija en `mockups.py` (`BOX, CX, TOP = 318, 500, 293`, escala 0-1000): el diseño, recortado a su contenido, entra en un cuadro de 318 de lado, centrado en x=500, con su borde de arriba en y=293. Es lo que se aprobó; no tocarlo.
- **Las remeras están centradas en la imagen, no el diseño en cada remera.** Cada foto se desplazó (sin escalarla ni deformarla) para que el centro de la remera quede en x=500. El centro de la remera es el promedio entre el centro del cuello y el centro del torso: centrando solo por el cuello el diseño se veía corrido a la izquierda, y solo por el torso, a la derecha. Verticalmente, el punto medio entre cuello y ruedo queda a la misma altura en todas.
- Todas las fotos se alejaron igual (92%) para que ninguna manga toque el borde.
- **Tinta:** Black y Navy llevan el diseño blanco/claro; todos los demás colores, el negro/oscuro. Si la carpeta trae 2 PNG, el script detecta solo cuál es cuál por luminosidad (no por el nombre). Si trae 1 solo PNG (diseño a color), va igual en todos.
- **Colores:** si el diseño ya está en la tienda, los que ya vende (`store_colors.py`). Si no está, todos; el script descarta los que no se leen (bajo contraste) y marca los "dudosos".
- **Salida:** JPG 2500×2500, `<Diseño> - <Color>.jpg`, una carpeta por diseño.

## Pasos

1. **Preparar entrada.** Descomprimir cada zip en una carpeta nueva y vacía (pueden venir zips dentro de zips). Ignorar `__MACOSX` y `._*`. Dejar `entrada/` con **una subcarpeta por diseño**, con el nombre limpio del diseño (ej. `Raised On Hose Water`; sacar sufijos como `.png`, `NEW`, `final`, `Black`, `White`). Si hay PNG que no son diseños (mockups, fotos), dejarlos afuera; ante la duda, abrirlos y mirarlos.

2. **Colores de la tienda.**
   ```
   python3 -I <skill>/scripts/store_colors.py --input entrada --out map.json
   ```
   Revisar que cada diseño haya encontrado SU producto: el título en la tienda puede ser distinto (ej. "Hair Would Only Slow Me Down" = "Slow Me Down T-Shirt", "Raised On Hose Water" = "Hose Water T-Shirt"). Si un match está mal, corregir `map.json`. Anotar los colores que la tienda vende pero no tienen remera vacía. Sin internet: seguir sin `--map` y avisar.

3. **Generar.**
   ```
   python3 -I <skill>/scripts/mockups.py --input entrada --out salida --map map.json
   ```
   Opciones: `--colors "Black,White"` (colores para los diseños que no están en el map), `--keep-low-contrast`, `--size 5000`.

4. **Revisar con los ojos antes de entregar.** Abrir cada `salida/<Diseño> - preview.jpg`: que el diseño se lea, que se vea centrado sobre la remera y que la tinta clara/oscura sea la correcta. Mirar los "dudosos" y omitidos del reporte.

5. **Entregar.** Un zip por diseño (o uno con todos) con las carpetas de JPG, sin previews ni reporte:
   ```
   cd salida && zip -qr ../mockups.zip . -x '*preview*' -x '*.gif' -x 'reporte.json'
   ```
   Mandar el zip y, para que lo vea, la preview y el GIF (SendUserFile: zip con "attach", preview y GIF con "render"; si no existe esa herramienta, adjuntarlos en la respuesta).
   En la respuesta, breve: tabla color → tinta, colores omitidos o dudosos, colores sin remera vacía, diseños que no estaban en la tienda, archivos que no se usaron. Esperar su OK. No subir nada a Printify/Shopify (para eso está `oldyfans-carga-disenos`).

## Agregar una remera vacía nueva
Solo si Patricio pasa la foto de un color nuevo (remera plana sobre fondo gris claro, misma toma que las demás):
1. `python3 -I <skill>/scripts/center_blanks.py --src FOTO.jpg --ruler regla` → genera `regla_v.jpg` y `regla_h.jpg`.
2. Abrir las reglas: en `regla_v` leer dónde termina el borde de abajo del cuello acanalado (adelante) → `--collar`; en `regla_h` leer los bordes exteriores izquierdo y derecho del cuello en su parte más ancha, el punto medio es `--neck` (contrastarlo con el centro de la etiqueta).
3. `python3 -I <skill>/scripts/center_blanks.py --src FOTO.jpg --name "Color" --collar N --neck N [--light-ink]` (agregar `--sides L,R --hem N` si los costados o el ruedo no se detectan solos, como en remeras blancas). Guarda la remera centrada en `assets/blanks/` y la suma a `blanks.json`.
4. Verificar con un mockup de prueba que el diseño se vea centrado igual que en los otros colores.
