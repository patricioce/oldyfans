Subí a Printify como productos NUEVOS los 3 diseños que faltan del lote carga-disenos/lote-2026-10-15 (A Wise Man, Call Me Antisocial y Hang In There) y dejalos en Shopify en BORRADOR con los mockups propios. Trabajá en la rama claude/exciting-mayer-frtssa. Usá la skill oldyfans-carga-disenos (está en .claude/skills/ del repo, en esa rama).

Contexto:
- Leé primero .claude/skills/oldyfans-carga-disenos/SKILL.md, carga-disenos/kit/README.md y carga-disenos/lote-2026-10-15/CARGA.md.
- Los tokens PRINTIFY_TOKEN y SHOPIFY_ACCESS_TOKEN están en las variables de entorno. No los muestres. Armá kit/.env con el resto de los valores de kit/.env.example.
- lote.json tiene el título y los colores de cada producto. A Wise Man y Call Me Antisocial: --image oscura.png --image-light clara.png (la clara, blanca, va en Black y en Navy, cada uno en su propia área). Hang In There: solo --image unica.png.
- Tamaño: el que trae el script por defecto (85% del modelo). No pases --scale salvo que yo lo pida.
- "I Had Potential T-Shirt" ya está hecho (está en creados.json): no lo toques. Tampoco toques los productos viejos con estos diseños.
- No crees pedidos ni webhooks.

Pasos (esperá mi OK donde lo indico):
1. Verificá los tokens leyendo Printify (shop 27342731) y Shopify, sin crear nada. Confirmá que exista el modelo "10 p.m T-Shirt".
2. Simulación (sin --create) de los 3. Revisá que los colores existan con el nombre exacto y que la clara quede en Black y en Navy. Mostrame una tabla diseño → colores → imagen.
3. Creá los 3 con --create, sin publicar, y pasame los IDs y los links del editor de Printify. Esperá mi OK.
4. Con mi OK, simulá y después publicá cada uno con scripts/publicar_existente.py --printify-id <id> --mockups carga-disenos/lote-2026-10-15/mockups/<Diseño> --apply (en paralelo). No uses --create --publish: duplicaría los productos.
5. Verificá en Shopify que todos queden en borrador, fuera de la tienda online y con un mockup por color.
6. Agregá los IDs de Printify y Shopify a carga-disenos/lote-2026-10-15/creados.json, commiteá y pusheá.

Respondé en español.
