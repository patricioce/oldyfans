# Sellos de la home, bloques de la ficha y footer

Todos se editan en Shopify → Online Store → Themes → Customize (secciones de la home y plantilla de producto).

## 1. Sellos de la home (sección de íconos al pie)

| Sello | Texto actual | Texto nuevo |
|---|---|---|
| Envío | Free Shipping / Buy 2 T-shirts and get free shipping | **Free US Shipping** / On 2+ T-shirts. Buy 3, save $10. |
| Checkout | Secure Checkout / 100% Encrypted & Private | (sin cambios) |
| Materiales | Sustainable Materials / Eco-friendly, plant-based, and recycled fabrics | **100% Ring-Spun Cotton** / Soft, pre-shrunk, printed to order (nada de "recycled": la ficha dice 100% algodón) |
| Devoluciones (versión A, si aceptás cambio de talle) | Easy 30-Day Returns / Hassle-free returns for peace of mind | **30-Day Fit Guarantee** / Free reprint if it's damaged, wrong or doesn't fit |
| Devoluciones (versión B, si NO aceptás cambio de talle) | ídem | **We Make It Right** / Damaged or wrong item? Free replacement within 30 days |

## 2. Barra de reputación de la home
- Actual: `★★★★★ 4.9/5 +800 Happy Gen Xers`
- La página de reseñas muestra 28–31 reseñas. Si "+800" son pedidos/clientes reales, cambiar a: `★★★★★ 4.9/5 from verified buyers · 800+ orders shipped`.
- Si no tenés el dato de 800, usar: `★★★★★ 4.9/5 from verified Gen X buyers`.

## 3. Ficha de producto: íconos bajo "Add to cart"
- Actual: `Free Returns · Fast Shipping · Premium Quality`
- Nuevo (A): `30-Day Fit Guarantee · Free US Shipping on 2+ · Printed in the USA`
- Nuevo (B): `We Make It Right · Free US Shipping on 2+ · Printed in the USA`

## 4. Ficha: acordeón "Free & Easy Returns"
Título nuevo: **Returns & Exchanges**

> Love it or we'll make it right.
> - Damaged, misprinted or wrong item? Free replacement or full refund. No need to send it back.
> - Wrong size? We'll reprint it in another size, free, once per order. *(borrar esta línea en la versión B)*
> - You have 30 days from delivery. Email **info@oldyfans.store** with your order number and a photo.
>
> Every shirt is printed to order, so we can't accept returns for a change of mind.

(Se va "support@oldyfans.store", "Item needs to be unused" y "enjoy the trail", que viene de una plantilla de otra marca.)

## 5. Ficha: acordeón "Fast Shipping"
Título nuevo: **Shipping & Delivery**

> **Free US shipping on 2+ T-shirts.** Buy 3 and save $10.
> Each shirt is printed to order in 2–5 business days, then USPS delivers in 2–5 business days.
> Most US orders arrive in **4–10 business days**. International: 6–20 business days.
> You'll get a tracking number by email as soon as it ships.

## 6. Ficha: bloque "Real customer service, not a bot"
Reemplazar la última frase "Every order is backed by a 30-day guarantee — if you're not happy, we make it right." por:
> Every order is backed by our 30-day guarantee: if it arrives damaged, wrong *(A: or doesn't fit)*, we make it right. Email info@oldyfans.store.

## 7. Selector de talle
- Etiqueta actual: `Size: Size Guide`. Cambiar el texto del bloque a `Size` y dejar el link `Size guide` aparte, a la derecha.
- Preselección: en el editor del tema, bloque "Variant picker", activar la opción de seleccionar la primera variante disponible (si el tema la tiene). Si no, pedírselo al dev del tema.

## 8. Footer: formulario de email
- Título actual: `Get the good ones first`
- Nuevo: **Get 15% off your first order**
- Subtítulo: `Plus first dibs on new designs. No spam, unsubscribe anytime.`
- Por qué: el flujo de bienvenida de Klaviyo (Welcome Series - Standard, en vivo) ya manda un 15% OFF en el primer email, pero la tienda no lo anuncia.
- **Verificar antes:** que los suscriptores del footer de Shopify entren a la lista que dispara ese flujo en Klaviyo (lista `S8aQnC`). Los 3 formularios de Klaviyo están en borrador, así que la única puerta de entrada hoy es el footer.

## 9. Barra de anuncios
Hoy rota "BUY 2 T-SHIRTS & GET FREE SHIPPING" y "BUY 3 T-SHIRTS & GET $10 OFF + FREE SHIPPING". Agregar "US" para no prometer envío gratis internacional:
- `FREE US SHIPPING ON 2+ T-SHIRTS 🚚`
- `BUY 3, GET $10 OFF + FREE US SHIPPING 💰`
