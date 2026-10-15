# Menú por temas y limpieza de colecciones

Las colecciones temáticas **ya existen** (las vi en `/collections.json` el 2026-10-15) pero no están en el menú.
Se arma en Shopify → Online Store → Navigation → Main menu.

## Menú propuesto

| Ítem del menú | Colección | Productos |
|---|---|---|
| Best Sellers | `/collections/best-sellers` | 20 |
| Shop by Theme ▾ | — | — |
| ↳ Gen X Life | `/collections/gen-x` | 59 |
| ↳ Retro & Nostalgia | `/collections/retro-nostalgia` | 75 |
| ↳ Sarcastic & Dad Jokes | `/collections/sarcastic-dad-jokes` | 115 |
| ↳ Bald & Bold | `/collections/bald-bold` | 25 |
| ↳ Parenting | `/collections/parenting` | 15 |
| Gifts ▾ | — | — |
| ↳ 50th Birthday | `/collections/50th-birthday` | 42 |
| ↳ Gifts for Him | `/collections/gifts-for-him` | 55 |
| Shop All | `/collections/all` | 310 |
| Reviews | `/pages/reviews` | — |
| Contact | `/pages/contact` | — |

"About Us" pasa al footer. "Sale" sale del menú principal (hoy es el catálogo entero, 312 items).

## Limpieza
- **Colecciones de prueba publicadas:** `sale-test` (291) y `sale-test-2` (290). Despublicarlas o borrarlas.
- **`sale` vs `t-shirt-sale`:** `sale` tiene 312 items (todo); `t-shirt-sale` tiene 32. Si hay una oferta real, usar `t-shirt-sale` como "Sale" y redirigir `/collections/sale` → `/collections/t-shirt-sale`. Si todo está siempre "en oferta", ver el punto del precio tachado en el doc.
- **`core` (117)** y **`frontpage` (1)**: parecen colecciones internas; no ponerlas en el menú.

## Orden por defecto
En cada colección (Products → Collections → la colección → Sort), poner **Best selling**. Hoy `/collections/all` abre en A–Z ("10 p.m", "50 Years", "6 Hour Warranty"…).
