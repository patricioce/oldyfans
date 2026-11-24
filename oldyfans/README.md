# OldyFans: footer

Sección de Shopify con el footer aprobado (nov 2026). La estructura copia el footer de slothhikingclub.com: newsletter centrado arriba, logo con columnas de links al medio, y medios de pago con políticas abajo.

Archivo: `sections/oldyfans-footer.liquid`

## Instalación (unos 5 minutos)

1. Shopify admin → **Online Store → Themes**. En el tema publicado, usá **⋯ → Duplicate** para tener respaldo.
2. En el tema: **⋯ → Edit code**. En la carpeta **sections**, elegí **Add a new section**, ponele de nombre `oldyfans-footer` y pegá todo el contenido del archivo. Guardá.
3. Andá a **Customize**. En el grupo **Footer** del panel izquierdo:
   - **Add section → OldyFans footer**. Ya viene cargado con los textos y links aprobados.
   - Ocultá (ícono del ojo) o eliminá la sección **Footer** vieja.
   - Si queda la barra de copyright o de redes anterior (secciones tipo *Utilities* o *Bottom bar*), ocultala también.
4. **Save**.

## Qué se edita desde Customize

- **Newsletter:** el título, el texto, el placeholder, el botón y el mensaje de éxito. Las suscripciones quedan como clientes de Shopify con email marketing aceptado y la etiqueta `newsletter`, igual que el formulario actual.
- **Marca:** el logo (si lo dejás vacío usa el del tema), la frase, la bajada y los links de Facebook e Instagram.
- **Columnas:** cada una tiene un título y sus links, uno por línea con el formato `Texto | /url`. También podés elegir un menú de Navigation, que reemplaza a esos links.
- **Barra inferior:** los íconos de pago salen solos según los medios activos en Shopify. Las políticas salen de **Settings → Policies**.
- **Colores:** el fondo es `#1F1D20` y el botón `#E73123`.
