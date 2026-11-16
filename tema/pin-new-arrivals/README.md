# Fijar productos arriba en New Arrivals

- Colección auxiliar automática **New Arrivals Pinned** (`new-arrivals-pinned`, id 512616693805): incluye los productos con tag `pin-new`. Oculta de buscadores (seo.hidden).
- `sections/main-collection.liquid` (bloque `BMP-HOOK:pin-new`): en `/collections/new-arrivals`, página 1, muestra primero los productos de esa colección y después el resto (de nuevo a viejo) salteando los fijados en todas las páginas para que no se repitan.
  Solo con el orden por defecto y sin filtros; otras colecciones no cambian.
- Fijar / sacar un producto: agregarle / quitarle el tag `pin-new` en Shopify (tarda unos segundos en reflejarse).
- `main-collection.original.liquid`: la sección del tema activo antes del cambio (para volver atrás).
- Probado 2026-11-16 en el tema "Pin New Arrivals - Test" (189024141357), copia de "Cart Mobile Fix - 21 Oct 2026" (188814426157, el activo).
