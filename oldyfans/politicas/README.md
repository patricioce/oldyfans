# Políticas de OldyFans (oldyfans.store)

- `refund-policy.html`: texto de la Refund Policy, basado en la de Sloth Hiking Club
  (reembolso y cambio de talle sin devolución, 30 días) y adaptado a OldyFans.
- `policy-pages.css`: estilo de las páginas `/policies/*` copiado de Sloth Hiking Club
  (fondo gris, tarjeta blanca con borde superior grueso, título a la izquierda con línea),
  con los colores de OldyFans. Se aplica a todas las políticas (refund, shipping, privacy, terms).
- `new-refund-policy-d.png` / `new-refund-policy-m.png`: vista previa en escritorio y celular.

## Cómo publicar

Texto: Shopify Admin → Configuración → Políticas → Política de reembolso → botón `<>` →
pegar `refund-policy.html` → Guardar.

Estilo (el campo "CSS personalizado" tiene un límite de 1500 caracteres y no entra, así que va como archivo del tema):
1. Tienda online → Temas → `…` → Editar código.
2. Carpeta `assets` → Agregar un nuevo recurso → Crear un archivo en blanco → nombre `oldyfans-policies`, extensión `.css`.
3. Pegar el contenido de `policy-pages.css` → Guardar.
4. Abrir `layout/theme.liquid`, buscar `</head>` y pegar justo antes:
   `{{ 'oldyfans-policies.css' | asset_url | stylesheet_tag }}`
5. Guardar. El CSS solo afecta a las páginas `/policies/*`.
