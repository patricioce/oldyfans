# Menú de 80s Survivors Club (réplica del de OldyFans)

El menú de OldyFans tiene dos partes, y hay que replicar las dos:

1. **Los ítems del menú** (Shop con su desplegable, Bestsellers, New Arrivals, Sale, Help). Se cargan en el admin de Shopify, en **Contenido → Menús**.
2. **El estilo**: DM Sans semibold de 16px, el espacio entre palabras igual al de Sloth Hiking Club, la flechita de "Shop" a 8px del texto y "Sale" en rojo. Es el CSS de esta carpeta.

El desplegable de "Shop" (la tarjeta que se abre al hacer clic) no hace falta crearlo: viene con el tema BuildMyPOD y aparece solo cuando un ítem del menú tiene subítems.

## Archivos de esta carpeta

| Archivo | Para qué |
|---|---|
| `menu-sloth.css` | El CSS del menú, con comentarios. Es el que se sube al tema. |
| `menu-sloth.min.css` | El mismo CSS en una sola línea (1.071 caracteres), por si se pega en "CSS personalizado". |
| `INSTRUCTIVO.md` | Esta guía. |

---

## Paso 0 · Ver qué tema tiene 80s Survivors Club

En el admin de 80s Survivors Club, andá a **Tienda online → Temas** y fijate cuál es el tema publicado.

- **Si es el clon de OldyFans** (el que se subió con `tema-80s-survivors-club.zip`), **el CSS ya viene adentro**, al final de `tipografia-sloth.css`. Solo te falta el **Paso 1** (los ítems del menú) y el **Paso 3** (revisar). El paso 2 lo podés saltear. Si querés que "Sale" también salga en rojo en el menú del celular, hacé el paso 2B: al clon le falta una línea que sí está en este archivo.
- **Si es otro tema** (o el clon todavía no está subido), hacé los pasos 1, 2 y 3. Ojo: el CSS está hecho para el tema BuildMyPOD. En otro tema no va a romper nada, pero tampoco va a tener efecto.

Antes de tocar nada: en el tema, **… → Duplicar**. Si algo sale mal, volvés a la copia.

---

## Paso 1 · Cargar los ítems del menú

1. En el admin: **Contenido → Menús → Menú principal** (`main-menu`).
2. Dejalo así (arrastrá los subítems debajo de "Shop" para que queden adentro):

```
Shop                 → /collections
  ├ Sale             → /collections/sale
  ├ Bestsellers      → /collections/best-sellers
  ├ Gen X            → /collections/gen-x
  ├ Sarcastic & Dad Jokes → /collections/sarcastic-dad-jokes
  ├ Retro Nostalgia  → /collections/retro-nostalgia
  ├ Bald & Bold      → /collections/bald-bold
  └ All collections  → /collections
Bestsellers          → /collections/best-sellers
New Arrivals         → /collections/all?sort_by=created-descending
Sale                 → /collections/sale
Help                 → /pages/contact?view=help
```

3. **Guardar menú.**

Tres cosas a tener en cuenta:

- **Las colecciones tienen que existir en 80s Survivors Club** con esos mismos identificadores (`sale`, `best-sellers`, `gen-x`, etc.). Si una colección todavía no existe, cargá el enlace como dirección web escribiendo la ruta (por ejemplo `/collections/gen-x`); va a funcionar cuando crees la colección. Si las colecciones de 80SC van a ser otras, cambiá los subítems de "Shop": el desplegable muestra lo que pongas.
- **El rojo de "Sale" depende del enlace.** El CSS pinta de rojo cualquier ítem que lleve a `/collections/sale`. Si la colección de ofertas de 80SC se llama distinto, avisame y cambio el CSS.
- **New Arrivals:** en OldyFans ese ítem lleva a `/collections/sale?sort_by=created-descending`, o sea a Sale ordenado por fecha, no a las novedades. Para 80SC te propongo `/collections/all?sort_by=created-descending` (todos los productos, los más nuevos primero). Si en OldyFans era a propósito, copiá el de OldyFans.

---

## Paso 2 · Instalar el estilo (CSS)

Elegí **una** de estas dos opciones.

### 2A · Como archivo del tema (recomendada)

1. **Tienda online → Temas → … → Editar código**.
2. En la columna izquierda, en **Assets**, tocá **Agregar un nuevo asset → Crear un asset en blanco**, tipo **.css**, nombre `menu-sloth`. Se crea `menu-sloth.css`.
3. Pegá adentro todo el contenido de `menu-sloth.css` de esta carpeta y **Guardar**.
4. Abrí **Layout → `theme.liquid`**. Buscá (con Ctrl+F o Cmd+F) la línea de `tipografia-sloth.css`. Si no está, buscá `</head>`.
5. Pegá esta línea **justo debajo** de la de `tipografia-sloth.css` (o justo arriba de `</head>` si esa no existe):

```liquid
{{ 'menu-sloth.css' | asset_url | stylesheet_tag }}
```

6. **Guardar.**

Tiene que ir **después** de `tipografia-sloth.css`, porque ese archivo pone el menú en peso 500 y este lo sube a 600.

### 2B · Pegarlo al final de un archivo que ya existe

Sirve si el tema es el clon y solo querés sumar la línea del celular, o si preferís no tocar `theme.liquid`.

1. **Editar código → Assets → `tipografia-sloth.css`**.
2. Si al final ya hay un bloque que empieza con `/* ===== Menú principal igual al de Sloth Hiking Club ===== */`, **borralo entero** (hasta el final del archivo).
3. Pegá al final todo el contenido de `menu-sloth.css` y **Guardar**.

Si el tema no tiene `tipografia-sloth.css`, otra forma es **Personalizar → Configuración del tema → CSS personalizado**, pegando `menu-sloth.min.css` al final de lo que ya haya. Shopify limita el largo de ese campo; si no entra, usá la opción 2A.

---

## Paso 3 · Revisar que quedó bien

Abrí la tienda en una ventana de incógnito (o con Ctrl+Shift+R para recargar sin caché):

- **Computadora:** las palabras del menú en semibold (más gruesas que antes), separadas parejo, unos 35px entre cada una en una pantalla grande. "Shop" con la flechita al lado; al hacer clic se abre el desplegable con las colecciones. "Sale" en rojo.
- **Celular:** abrí el menú hamburguesa; "Sale" tiene que estar en rojo y en negrita.

Si no cambia nada: revisá que la línea del paso 2A esté **debajo** de la de `tipografia-sloth.css` y que el tema que estás mirando sea el publicado (o usá **Vista previa** sobre el tema que editaste).

## Qué hace el CSS, en detalle

- Ítems de primer nivel: DM Sans 600, 16px, interlineado 1.4, sin mayúsculas ni espaciado extra.
- Espacio entre ítems: se adapta al ancho de pantalla, entre 22 y 36px (`clamp(22px, 2.4vw, 36px)`), igual que Sloth Hiking Club.
- "Shop": flechita de 14px a 8px del texto.
- "Sale": rojo `#B72C28`, en el menú de computadora y en el del celular.
- Los demás ítems quedan en el color de texto del tema. Para cambiarlo: **Personalizar → Configuración del tema → Colores**.
