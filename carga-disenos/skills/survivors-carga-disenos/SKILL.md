---
name: survivors-carga-disenos
description: Cargar un lote de diseños de remeras de 80s Survivors Club (carpeta de lote con diseños y mockups) a Printify como productos nuevos y publicarlos en Shopify (80ssurvivorsclub.com) en borrador con los mockups propios. No es para OldyFans (para eso está oldyfans-carga-disenos).
---

# Carga de diseños 80s Survivors Club

Es el mismo flujo que OldyFans, con los mismos scripts y **siempre con `--tienda survivors`**. Sin esa opción, los scripts cargan en OldyFans: no olvidarla en ningún comando.

Todo vive en el repo `patricioce/oldyfans`, carpeta `carga-disenos/`. Usar la rama `claude/cool-albattani-1b7rl4` hasta que se mergee: es la que tiene `scripts/tienda.py`.
Leé primero la sección "Otra tienda: 80s Survivors Club" de `carga-disenos/kit/README.md` y el `CARGA.md` del lote. Los scripts están en `carga-disenos/kit/scripts/`.

## Credenciales
- Vienen en las variables de entorno. Nunca mostrarlas en el chat:
  - `SURVIVORS_PRINTIFY_TOKEN`
  - `SURVIVORS_SHOPIFY_SHOP_DOMAIN`
  - `SURVIVORS_SHOPIFY_CLIENT_ID` + `SURVIVORS_SHOPIFY_CLIENT_SECRET` (el script pide con eso un token de Shopify de 24 h)
  - `PRINTIFY_TOKEN` (de OldyFans, solo para LEER el producto modelo)
- **No tocar ni renombrar `PRINTIFY_TOKEN` ni `SHOPIFY_ACCESS_TOKEN`: son de OldyFans y esa skill las sigue usando.**
- Armar `carga-disenos/kit/.env` copiando `.env.example` si no existe (`.env` está en .gitignore; no commitearlo).
- Paso 1 siempre: verificar sin crear nada.
  - Correr `python3 scripts/repair_products.py --tienda survivors`: tiene que obtener el token de Shopify y decir "Nada para corregir" o listar productos.
  - Hacer una simulación de `printify_new_product.py --tienda survivors`: tiene que imprimir `Tienda: 80s Survivors Club | Printify 29697371 | Shopify drysff-xt.myshopify.com | modelo leido de Printify 27342731 | Vendor '80s Survivors Club'` y encontrar el modelo "10 p.m T-Shirt".

## Datos fijos
- Printify: tienda `29697371` ("80s Survivors Club", conectada a Shopify). En esa misma cuenta hay otra tienda, `29697320`, desconectada: no usarla.
- Shopify: `drysff-xt.myshopify.com`, en USD.
- Producto modelo: no hay uno propio. Se lee "10 p.m T-Shirt" de OldyFans, solo con GET; el script corta si se intenta escribir con ese token. **Nunca crear, editar ni publicar nada en la tienda de OldyFans desde esta skill.**
- Vendor **"80s Survivors Club"**. Precio en Printify $29.99. En Shopify, price 29.99 / compare_at 42.85.

## Decisiones que NO se vuelven a preguntar (iguales a OldyFans)
- Un producto por diseño, siempre producto NUEVO.
- Título y colores: los de `lote.json` del lote (nombres exactos del catálogo de Printify). El gris claro es **Ice Grey**.
- Descripción, tags, talles, blueprint y proveedor: los del modelo "10 p.m T-Shirt".
- **Dos tintas:** `--image oscura.png --image-light clara.png`.
  - La clara (blanca) va en **Black y Navy**; la oscura va en el resto de los colores.
  - El script arma un área de impresión propia para Black y otra para Navy, cada una con SOLO ese color.
  - Para corregir un producto ya creado: `printify_new_product.py --tienda survivors --fix-areas <id> [--apply]`.
- Diseño de una sola versión (`unica.png`): solo `--image`, va igual en todos los colores.
- **Tamaño: 85% del tamaño del modelo.** Es el valor por defecto; no pasar `--scale` salvo que Patricio pida otro ajuste.
- Mockups: los de `mockups/<Diseño>/`, un archivo por color con el nombre del color. Se cargan en Shopify al publicar.
- No crear pedidos ni webhooks.

## Pasos (esperar el OK de Patricio donde se indica)
1. Verificar las credenciales (ver arriba).
2. Simulación (sin `--create`) de cada diseño, con `--tienda survivors`.
   - Confirmar que todos los colores existen y que la clara cae en Black y Navy, cada uno en su área.
   - Mostrar una tabla diseño → colores → imagen.
3. Crear con `--tienda survivors --create`, sin publicar, y pasar los IDs de Printify.
   - **Esperar OK.** Patricio revisa cada producto en `https://printify.com/app/editor/<id>`, con la cuenta de Printify de 80s Survivors Club.
   - Si pide mover o achicar el diseño: usar `--x --y --scale`, o hacer un PUT de `print_areas` que incluya TODAS las variantes.
4. Con OK, publicar cada producto ya creado:
   `python3 scripts/publicar_existente.py --tienda survivors --printify-id <id> --mockups "<lote>/mockups/<Diseño>" --apply`
   - Simular antes sin `--apply`.
   - Tarda ~10 min por producto: correrlos en paralelo y en segundo plano.
   - **No usar `--create --publish` para algo ya creado: crea un duplicado.**
5. Verificar en Shopify que cada producto quede:
   - en `draft` y fuera de la tienda online;
   - con una foto por color;
   - con Vendor "80s Survivors Club" y precio 29.99/42.85.
   Comprobarlo con `repair_products.py --tienda survivors --handle <handle>`, que tiene que decir "Nada para corregir".
6. Guardar los IDs en `<lote>/creados.json` con el formato `{"<Diseño>": {"titulo", "printify_id", "shopify_id", "estado"}}`. Commitear y pushear.

Responder siempre en español.
