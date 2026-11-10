# Colecciones de OldyFans con el estilo de Sloth Hiking Club

`colecciones-sloth.css` cambia **todas** las páginas `/collections/*` de oldyfans.store:

- Título grande y descripción en gris, con una línea divisoria debajo
- Barra con "Sort by:", la cantidad de productos a la derecha y líneas arriba y abajo
- Grilla de 4 columnas en computadora (3 en tablet, 2 en celular)
- Fotos con esquinas redondeadas y un zoom suave al pasar el mouse
- Botón redondo blanco de "agregar" sobre la foto, abajo a la derecha (siempre visible, también en celular)
- Títulos en tipografía normal, sin mayúsculas
- Paginación en cajitas, con la página actual en negro
- "Sale" en rojo en el menú

El precio no se toca: el tema ya tiene una regla propia que pone el precio tachado primero.

## Instalación (5 minutos)

1. Shopify → Tienda online → Temas → (tema activo) → **⋯ → Editar código**.
2. En **Assets** → *Agregar un nuevo recurso* → *Crear un recurso en blanco*, tipo `.css`, nombre `colecciones-sloth`.
   Pegar todo el contenido de `colecciones-sloth.css` y guardar.
3. Abrir `layout/theme.liquid`, buscar la línea de `imagen-producto-sloth.css` y agregar debajo:

   ```liquid
   {{ 'colecciones-sloth.css' | asset_url | stylesheet_tag }}
   ```

4. Guardar.

## Para quedar igual que Sloth (se activa desde el editor, no por código)

- **Filtros "Availability" y "Price"**: instalar la app gratuita *Shopify Search & Discovery*, en *Filtros* agregar
  *Disponibilidad* y *Precio*. Después, en Personalizar → plantilla de colección → sección de productos,
  activar *Habilitar filtrado* con diseño horizontal.
- **Globitos de color debajo de la foto**: en Personalizar → plantilla de colección → tarjeta de producto,
  agregar el bloque *Muestras / Swatches*. El CSS ya los deja redondos y del tamaño de Sloth.
