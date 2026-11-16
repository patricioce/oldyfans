# Reemplazo de diseño y mockups en productos ya publicados (2026-11-16)

Mismo producto en Printify y en Shopify: no se crea nada nuevo, el handle/link no cambia.

1. Printify: `scripts/reemplazar_diseno.py <printify_id> oscura.png clara.png <x> <y> <scale> [--apply]`
   sube el diseño nuevo y rearma las áreas (oscura para el resto, una área propia para Black y otra para Navy).
   - En productos viejos Printify solo acepta las variantes que ya estaban en `print_areas` (si se mandan las 524 rechaza con 8251).
   - Printify deduplica las subidas por contenido de píxeles (el metadato PNG ya no alcanza): el script cambia un píxel casi invisible por color.
2. Shopify: `scripts/fotos_shopify.py <shopify_id> <carpeta mockups> [--apply]`
   sube primero las fotos nuevas (una por color, asignada a sus variantes), después borra las viejas y mantiene como principal el mismo color que antes. No toca el estado.

Diseños recortados al dibujo (bbox común de las dos tintas). Mockups originales numerados: 1 Black, 2 Navy, 3 White, 4 Sport Grey, 5 Military Green, 6 Charcoal, 7 Ice Grey (renombrados con el color y llevados a 2500 px).
Backup de áreas y fotos anteriores: `kit/backups/reemplazo-2026-11-16/`.

3. Publicar en Printify sin pisar Shopify: `scripts/republicar_activo.py <printify_id> [--apply]`
   (publica solo variantes: sin fotos, título, descripción ni tags; no pasa a borrador). Vigila 8 min:
   borra fotos que agregue Printify, restaura estado/visibilidad si cambian y deja 29.99/42.85 + Vendor OldyFans.
   Necesita `SHOPIFY_SHOP_DOMAIN=s0vk8m-gj.myshopify.com SHOPIFY_API_VERSION=2024-10` en el entorno o en `.env`.
   Publicado 2026-11-16: Printify volvió a poner Vendor "Printify" en los tres (corregido) y sacó Personal Space
   de la tienda online porque figura oculto en Printify (restaurado).
