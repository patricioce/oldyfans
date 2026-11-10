# OldyFans — Shopify

## Centro de ayuda (`/pages/contact?view=help`)
Copia del centro de ayuda de slothhikingclub.com (`?view=sbs-help`).

- `sections/oldyfans-help.liquid` — sección con todo editable desde el editor del tema
  (tarjetas, aviso, grupos, preguntas, tablas de talles, contacto) + FAQ en schema.org.
- `templates/page.help.json` — plantilla de página con el contenido cargado.

### Instalar
1. Tienda online → Temas → ⋯ → Editar código.
2. Sections → Agregar sección `oldyfans-help` → pegar `sections/oldyfans-help.liquid`.
3. Templates → Agregar plantilla → tipo `page`, nombre `help` → pegar `templates/page.help.json`.
4. Abrir `/pages/contact?view=help` (o asignar la plantilla `help` a una página nueva).

Antes de publicar revisar: umbral de envío gratis ($99+), política de reembolso (30 días),
prendas/tablas de talles y el email de soporte (vacío = email de la tienda).
