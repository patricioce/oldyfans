# 80s Survivors Club: re-vinculación con Printify y ajustes (2026-11-19)

## Problema
8 productos activos en Shopify no estaban vinculados en Printify (`external` vacío). Se publicaron el 18/11, cuando estaba
el error del perfil de envío duplicado. Si alguien los compraba, Printify no recibía el pedido. Además cotizaban otro envío
("Estándar" $3.56, de otro perfil). Eran Wise Man, I Had Potential, Warranty Expired, Metal Slide, I Can Write In Cursive,
Becoming A Legend, Old School y Aging Review.

## Qué se hizo
1. Respaldo de cada producto (`backup-productos-sin-vincular.json`) y de sus fotos publicadas, una por color, usadas como mockups.
2. Se borró la copia sin vincular en Shopify y se republicó desde Printify con
   `publicar_existente.py --tienda survivors --printify-id <id> --mockups <fotos> --apply` (logs en `logs/`).
3. `scripts/restaurar.py`: se dejaron como estaban (ACTIVO, mismo handle/URL, mismos canales y colecciones manuales
   "Home page" y "80s Survivors Club"). Verificado: 36 variantes, 6 fotos, 29.99/42.85, Vendor "80s Survivors Club".
4. `scripts/canales.py --apply`: los 61 productos activos quedaron publicados en los 5 canales
   (Online Store, Shop, Point of Sale, Facebook & Instagram, Google & YouTube).
5. Había dos "Retirement Definition T-Shirt" con diseños distintos: el de "Whatevering on a fixed income"
   (Printify 6afef9b93ea2512a5a0313b6, Shopify 11074215084316) pasó a llamarse **"Fixed Income Retirement T-Shirt"**
   en Shopify y Printify (el handle `retirement-definition-t-shirt-1` no se cambió).

## Auditoría final
62/62 productos vinculados, sin vínculos rotos; 2004 variantes en 29.99/42.85 y todas con foto; carrito de prueba en EE. UU.:
Standard Delivery $4.95 (1 remera) / $7.35 (2).

Los scripts leen las credenciales de las variables de entorno (`SURVIVORS_*`) y no guardan el token.
