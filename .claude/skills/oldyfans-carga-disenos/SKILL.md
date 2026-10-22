---
name: oldyfans-carga-disenos
description: Cargar un lote de diseños de remeras de OldyFans (carpeta de lote con diseños y mockups) a Printify como productos nuevos y publicarlos en Shopify en borrador con los mockups propios.
---

# Carga de diseños OldyFans

Todo vive en el repo `patricioce/oldyfans`, carpeta `carga-disenos/` (rama `claude/exciting-mayer-frtssa` hasta que se mergee).
Leé primero `carga-disenos/kit/README.md` y el `CARGA.md` del lote. Los scripts están en `carga-disenos/kit/scripts/`.

## Credenciales
- `PRINTIFY_TOKEN` y `SHOPIFY_ACCESS_TOKEN` vienen en las variables de entorno. Nunca mostrarlas en el chat.
- Armar `carga-disenos/kit/.env` copiando `.env.example` y completando los dos tokens desde el entorno (`.env` está en .gitignore; no commitearlo).
- Paso 1 siempre: verificar los dos tokens leyendo (sin crear nada) la tienda de Printify 27342731 y Shopify, y que exista el modelo "10 p.m T-Shirt".

## Decisiones que NO se vuelven a preguntar
- Un producto por diseño, siempre producto NUEVO. No tocar los productos existentes aunque tengan el mismo diseño o título.
- Título y colores: los de `lote.json` del lote (nombres exactos del catálogo de Printify). El gris claro es **Ice Grey**.
- Descripción, tags, talles, blueprint/proveedor: los del modelo "10 p.m T-Shirt". Precio en Printify $29.99; al publicar, el script deja en Shopify price 29.99 / compare_at 42.85 y Vendor "OldyFans".
- **Dos tintas:** `--image oscura.png --image-light clara.png`. La clara (blanca) va en **Black y Navy**; la oscura en el resto. El script arma **un área de impresión propia para Black y otra para Navy** (en el editor de Printify se ve como "specific design for Black / for Navy"). Con Black y Navy juntos en una sola área el editor no lo reconoce: no hacerlo así. El área de Navy (y la de Black) tiene que tener SOLO ese color: si Printify le mete variantes deshabilitadas de otros colores, el editor la toma como diseño general y Navy queda sin su diseño. El script lo corrige solo; para un producto ya creado: `printify_new_product.py --fix-areas <id> [--apply]`.
- Diseño de una sola versión (`unica.png`): solo `--image`, va igual en todos los colores.
- **Tamaño: 85% del tamaño del modelo** (escala ≈ 0.733, x=0.5, y≈0.281). Es el valor por defecto del script; no pasar `--scale` salvo que Patricio pida otro ajuste.
- Mockups: los de `mockups/<Diseño>/` (un archivo por color, con el nombre del color). La API de Printify no acepta mockups propios: en Printify quedan los de por defecto y los propios se cargan en Shopify al publicar, reemplazando las fotos.
- No crear pedidos ni webhooks.

## Pasos (esperar el OK de Patricio donde se indica)
1. Verificar tokens (ver arriba).
2. Simulación (sin `--create`) de cada diseño: confirmar que todos los colores existen y que la clara cae en Black y Navy (cada uno en su área). Mostrar tabla diseño → colores → imagen.
3. Crear con `--create` (sin publicar) y pasar los IDs de Printify. **Esperar OK** (desde la nube no se ven las vistas previas de Printify: Patricio las revisa en `https://printify.com/app/editor/<id>`). Si pide mover o achicar: `--x --y --scale`, o corregir el producto existente por API con PUT de `print_areas` (incluir TODAS las variantes, también las deshabilitadas, o Printify rechaza el cambio).
4. Con OK, publicar cada producto YA creado con
   `python3 scripts/publicar_existente.py --printify-id <id> --mockups "<lote>/mockups/<Diseño>" --apply`
   (simular antes sin `--apply`). Publica sin fotos de Printify, reemplaza las fotos por los mockups propios (uno por color, asignado a sus variantes) y deja el producto en BORRADOR. Tarda ~10 min por producto: correrlos en paralelo y en segundo plano.
   **No usar `--create --publish` para algo ya creado: crea un duplicado.**
5. Verificar en Shopify que cada producto quede en `draft`, fuera de la tienda online, con una foto por color, Vendor "OldyFans" y 29.99/42.85 (`repair_products.py --handle <handle>` tiene que decir "Nada para corregir").
6. Guardar los IDs en `<lote>/creados.json` (`{"<Diseño>": {"titulo", "printify_id", "shopify_id", "estado"}}`), commitear y pushear.

Responder siempre en español.
