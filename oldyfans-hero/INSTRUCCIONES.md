# Portada nueva de OldyFans (estilo Sloth Hiking Club)

Qué hay en esta carpeta:

| Archivo | Para qué |
|---|---|
| `sections/oldyfans-hero.liquid` | La sección nueva de la portada (foto + textos + botón). |
| `imagenes/hero-desktop.jpg` | Foto para computadora y tablet (horizontal, el grupo entero). |
| `imagenes/hero-celular.jpg` | Foto para celular. |

Textos que ya trae cargados (se cambian desde el editor, sin tocar código):

- Línea chica: **GRAPHIC TEES FOR THE UNSUPERVISED GENERATION**
- Título: **WE TURNED OUT FINE. MOSTLY.**
- Frase: **Whatevering since the 80s**
- Botón: **Find your next favorite**

## Antes de empezar: trabajar sobre una copia

En **Tienda online → Temas**, en el tema publicado ("Cart Mobile Fix - 21 Oct 2026"), tocá **⋯ → Duplicar**. Hacé todo en la copia y publicala recién cuando esté bien. Si algo sale mal, la tienda real no se toca.

## 1. Agregar la sección al tema

1. En la copia: **⋯ → Editar código**.
2. En la carpeta **sections**, **Agregar una sección nueva** y llamarla `oldyfans-hero`.
3. Borrar todo lo que trae, pegar el contenido completo de `sections/oldyfans-hero.liquid` y **Guardar**.

## 2. Ponerla en la portada

1. En la copia: **Personalizar** (abre la página de inicio).
2. En la barra izquierda, ocultar el **Slideshow** actual (el ojito). No lo borres, así se puede volver atrás.
3. **Agregar sección → OldyFans hero** y arrastrarla arriba de todo, debajo del encabezado.
4. En la sección:
   - **Imagen computadora** → Subir → `hero-desktop.jpg`
   - **Imagen celular** → Subir → `hero-celular.jpg`
   - **Link del botón** → la colección a la que tiene que llevar (por ejemplo Bestsellers o All).
5. **Guardar.**

## 3. Encabezado igual al de Sloth (logo a la izquierda, menú al centro)

En **Personalizar**, tocar el **Encabezado (Header)**:

- **Posición del logo:** izquierda.
- **Posición del menú:** centro.
- La barra de arriba ("FREE SHIPPING ON ORDERS $35+") ya está negra; queda como está.

Si el tema no ofrece "menú al centro", avisame y paso el CSS para hacerlo.

**Menú (opcional, como Sloth):** en **Contenido → Menús → Main menu**: Shop, Bestsellers, New arrivals, Reviews, Help. Para "Bestsellers" y "New arrivals" tienen que existir esas colecciones.

## 4. Revisar y publicar

Usar **Vista previa** de la copia, mirarla en la compu y en el celular, y si está bien: **⋯ → Publicar**.

## Cómo se ve según la pantalla

- **Computadora (1100 px o más):** texto a la izquierda sobre fondo oscuro, foto a la derecha.
- **Tablet:** foto horizontal arriba, texto abajo.
- **Celular:** foto arriba, texto abajo en el bloque oscuro, botón a todo el ancho.

La altura en computadora se ajusta sola al ancho de la pantalla, para que la foto no recorte a nadie. Desde el editor se pueden cambiar también los colores (fondo, texto, botón) y la altura máxima.

## Nota sobre la foto

Las fotos salen de la imagen que ya estaba en la tienda, que tiene el texto viejo impreso del lado izquierdo; por eso se usa solo el lado del grupo. La imagen original mide 1672 px de ancho: en pantallas muy grandes puede verse apenas blanda. Si aparece la foto original (sin texto y en más resolución), conviene reemplazarla desde el editor.
