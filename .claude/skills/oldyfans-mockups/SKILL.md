---
name: oldyfans-mockups
description: "Crear mockups de remeras OldyFans: poner los diseños (PNG) sobre las fotos de remeras vacías en todos los colores, con la posición y el tamaño de la tienda, y entregar vistas previas + zip. Usar cuando Patricio pase diseños de OldyFans (zip, carpetas o PNG) y pida mockups."
---

# Mockups de remeras OldyFans

Responder siempre en español. Patricio es el dueño de OldyFans (oldyfans.store).

Todo lo necesario viene en la skill:
- `assets/blanks/` — 13 remeras vacías (2500 px): Black, Charcoal, Ice Grey, Military Green, Navy, Sport Grey, White, Brown, Light Blue, Maroon, Sage, Sand, Stone Blue.
- `assets/blanks.json` — por color: archivo, contorno del torso (`left`, `right`, `top` en escala 0-1000) y `light_ink` (true solo en Black y Navy).
- `scripts/mockups.py` — arma los mockups, las vistas previas y `reporte.json`.
- `scripts/store_colors.py` — busca en oldyfans.store qué colores vende ya cada diseño y arma `map.json`.

## Reglas aprobadas (no volver a preguntar)
- **Ubicación y tamaño:** el diseño (recortado a su contenido) entra en un cuadro de lado = 54% del ancho del torso, centrado, con el borde de arriba a 36% del ancho del torso por debajo del cuello. Es lo que hay en la tienda y Patricio lo aprobó ("está perfecto"). No cambiarlo salvo que él lo pida.
- **Tinta:** Black y Navy llevan el diseño en **blanco/claro**; todos los demás colores, el diseño en **negro/oscuro**. Si una carpeta trae 2 PNG, el script detecta solo cuál es el oscuro y cuál el claro (por luminosidad, no por el nombre: suelen llamarse `8.png` = oscuro y `9.png` = claro). Si trae 1 solo PNG (diseño a color), va igual en todos los colores.
- **Colores por diseño:**
  1. Si el diseño ya está en la tienda → los colores que ya vende (los da `store_colors.py`).
  2. Si no está → todos los colores; el script descarta solo los que no se leen (bajo contraste) y marca como "dudoso" los límite.
- **Salida:** JPG 2500×2500, nombre `<Diseño> - <Color>.jpg`, una carpeta por diseño.

## Pasos

1. **Preparar entrada.** Descomprimir cada zip en una carpeta nueva y vacía de trabajo (los zips suelen traer zips adentro: descomprimir también esos). Ignorar `__MACOSX` y archivos `._*`. Dejar una carpeta `entrada/` con **una subcarpeta por diseño**, con el nombre del diseño tal como debe aparecer (ej. `Hang In There`; sacar sufijos como `.png`, `NEW`, `final`). Un PNG suelto puede ir directo en `entrada/` y el nombre del archivo es el diseño.
   Si en el zip hay PNG que no son diseños (mockups ya hechos, fotos), dejarlos afuera. Si hay dudas sobre qué es cada archivo, abrirlo y mirarlo.

2. **Colores de la tienda.**
   ```
   python3 -I <skill>/scripts/store_colors.py --input entrada --out map.json
   ```
   Revisar la tabla: que cada diseño haya encontrado SU producto (el título en la tienda puede ser distinto, ej. "Hair Would Only Slow Me Down" = "Slow Me Down T-Shirt"). Si un match es incorrecto, corregir `map.json` a mano. Si la tienda vende un color sin remera vacía, anotarlo para avisar. Si no hay acceso a internet, seguir sin `--map` y avisar que se usaron todos los colores.

3. **Generar.**
   ```
   python3 -I <skill>/scripts/mockups.py --input entrada --out salida --map map.json
   ```
   Opciones: `--colors "Black,White"` (colores por defecto para los diseños que no están en el map), `--keep-low-contrast` (no descartar nada), `--size 5000` (si pide más resolución).

4. **Revisar con los ojos antes de mostrar.** Abrir cada `salida/<Diseño> - preview.jpg` y chequear: que el diseño se lea, que esté centrado en el pecho y que la tinta clara/oscura sea la correcta. Mirar en el reporte los "dudoso" y los omitidos.

5. **Entregar.** Mandar las vistas previas (una por diseño) y un zip con las carpetas de diseños (sin las previews):
   ```
   cd salida && zip -qr ../mockups.zip . -x '*preview*' -x 'reporte.json'
   ```
   Con SendUserFile (previews con display "render", zip con "attach"). Si no existe esa herramienta, adjuntarlos en la respuesta como archivos.
   En la respuesta, breve y en español:
   - tabla diseño → colores generados;
   - colores omitidos por bajo contraste y los dudosos (para que decida);
   - colores que vende la tienda pero sin remera vacía;
   - diseños que no estaban en la tienda;
   - cualquier archivo que no se usó o faltó.
   Esperar su OK. No subir nada a Printify/Shopify desde esta skill (para eso está `oldyfans-carga-disenos`).

## Agregar una remera vacía nueva
Si Patricio pasa la foto de un color nuevo (misma toma de remera plana sobre fondo gris claro): guardarla en `assets/blanks/<color>.jpg` a 2500 px y agregar la entrada en `blanks.json`. Para el contorno del torso: con la imagen a 1000×1000, `left`/`right` = bordes del torso entre y=450 y y=650 (mediana), `top` = primer píxel de remera en x=500 (fondo ≈ 235,235,235; diferencia RGB > 40). En fotos de remera blanca la detección automática falla: medir a ojo. `light_ink: true` solo si Patricio dice que ese color lleva el diseño blanco.
