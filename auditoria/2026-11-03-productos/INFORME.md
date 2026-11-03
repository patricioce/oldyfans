# Auditoría de productos — oldyfans.store (2026-11-03)

Revisé los **351 productos publicados** en la tienda online: el JSON público de la tienda, las 14 colecciones y las 2245 fotos, que bajé en miniatura y medí una por una. Printify quedó afuera a pedido.
Tomé como modelo el **"10 p.m T-Shirt"**, el mismo que usa la skill de carga.

Detalle por producto en [`auditoria-productos.csv`](auditoria-productos.csv): una fila por producto con link y la lista de problemas.

**Resumen:** 323 de 351 productos tienen al menos una diferencia con el resto. Lo que coincide en todos: Vendor `OldyFans`, tipo `T-Shirt`, precio 29.99 / tachado 42.85, 100 g, todo disponible y fotos cuadradas.

---

## 1. Errores reales (afectan lo que ve o compra el cliente)

### 1.1 Foto de color equivocado
| Producto | Problema |
|---|---|
| In The Woods T-Shirt | La variante **Light Blue** muestra una remera **Stone Blue** |
| Therapy T-Shirt | La variante **Light Blue** muestra una remera **Stone Blue** |

### 1.2 Colores sin foto (al elegir ese color no cambia la imagen)
| Producto | Color sin foto |
|---|---|
| The First 50 Years T-Shirt | Black (la foto negra existe, es la principal, pero no está asignada; además se llama `Copia_de_The_Unfiltred_Generation.png`) |
| Grow Up T-Shirt | Navy (la foto está, pero sin asignar) |
| Well Seasoned T-Shirt | Black |
| Still Alive T-Shirt | White y Sand (las fotos están, pero sin asignar) |
| Make The Donuts T-Shirt | Navy y Black (faltan las fotos) |
| Garbage T-Shirt | Sand y Navy (faltan las fotos) |
| Hot Wife T-Shirt | Charcoal (falta la foto) |
| Figureoutability T-Shirt | White (falta la foto) |

### 1.3 Fotos de colores que no se venden (sobran en la galería)
Casi todas son mockups **Sand** de productos que no tienen Sand:
Sold Out!, Well Seasoned, The Rona, Aged Well, Music Rules, Well Done, The Gang, Can You Dig It?, Cool Bands (1 foto Sand cada uno) · Gen X Definition (Sand + Charcoal) · Who Peed In The Pool?! (Sand + Military Green + Charcoal; solo vende White y Sport Grey) · Paused Since 1987 (Sand + White + Sport Grey; solo vende colores oscuros).

### 1.4 Fondo de foto distinto
- **57 productos** tienen la foto **Black con fondo blanco puro**; el resto de las fotos tiene fondo gris claro. En la grilla de la tienda se nota mucho. Afecta a: Allegedly, I'm Trying, Crayons, Hesitate, Diapers, Who Came First?, Smartass, Surprise Party, Gifted, Positive Energy, Lincoln Music, Washington Music, Circle Back (los 2), Shake Well, Pre-Owned, Senior Discount, Eye-Rolling, Viewer Discretion Advised, Warranty Expired, Not Responsible, Manufacturer Support, Results May Vary, Processing, Do Not Bend, Old School, Nobody Owes You, No Photos Please, Look Bald, Trade For A Donut, Shit In General, Oh Hell No, Woke Up Bald Again, I'm Lost Too, The Forgotten Gen, Who Needs Hair, Nap Enthusiast Club, Seriously, FM Whatever, Not Shy, Apologies In Cash, Stop To Think, I Am Awake, Not A Tree, Unwritten Rules, Don't Call, Confuse Them, Paranoia, Feral, Midlife Crisis, I Want To Break Free, Care Less, Hypotheticals, Dry Humping, No Idea, Giving Blood, 50 Years.
- **Somebody's Therapist**: la foto Black tiene **fondo verde**.

### 1.5 Tamaño y posición del diseño en los mockups
En las miniaturas se ve que el diseño no está al mismo tamaño ni a la misma altura en todos los productos. Algunos quedan muy chicos o muy arriba (Press Any Key, Arm Candy, I Don't Care, Peaked, Meets Minimum Requirements, Record Sunset, Coding Sarcasm, I'm The Secret Ingredient) y otros ocupan casi todo el pecho (The Right Questions, Lost Signal, For Sale). La medición automática sale con ruido en remeras grises y verdes, así que esto hay que confirmarlo a ojo: no lo cuento como dato exacto.

---

## 2. Diferencias de estructura (cómo está cargado el producto)

| Qué | Estándar (mayoría / modelo) | Diferentes |
|---|---|---|
| Orden de opciones | Color → Size (277) | **74 productos con Size → Color**, entre ellos el propio modelo "10 p.m" |
| Talles | S, M, L, XL, 2XL, 3XL (333) | 9 con 4XL; 4 de XS a 5XL (Sounds Like A You Problem, Garbage, Someone Cares, Still Alive); 1 de XS a 4XL (Hose Water); 2 hasta 2XL (You Make A Better Door, Who Peed In The Pool?!); **2 con talles desordenados S, M, L, 2XL, XL, 3XL** (Gaming Because Murder Is Wrong, Paused Since 1987) |
| Variantes | 39 (150 productos) | Va de 10 a 57. Lo normal es que falte 3XL en White, Sport Grey y Black (219 productos); 52 tienen las 42 combinaciones, 32 solo pierden White y Sport Grey en 3XL, 11 solo Black 3XL, y **22 productos no tienen Military Green en XL** |
| Descripción | Lista Gildan de 5 ítems (339) | **12 con el bloque GPSR/EU** agregado: You Make A Better Door, Whatever, Gen X Definition, Glitching Cat, Gaming Because Murder Is Wrong, Dreaming About Her, Who Peed In The Pool?!, Still Alive, Paused Since 1987, Press Any Key, Yada Yada Yada, Antisocial |
| Tags | `BMP_HOME` + `niche:…` | **Hang In There T-Shirt** sin tags |
| Título | "Nombre T-Shirt" | **"I'll Be In My Office"** (sin "T-Shirt") |
| Handle | `nombre-t-shirt` (285) | **66 productos** con otro formato: sin "-t-shirt" (`bad-idea`, `cool-bands`…), con sufijos (`-1`, `-new`, `-white`, `-blanco`, `-music`, `-boat`, `-plane`), en español (`definicion-gen-x`) o con errores de tipeo (**`midelife-crisis`**, **`gaming-because-morder-is-wrong-white`**, `dreaming-about-me` para "Dreaming About Her") |
| Resolución de fotos | Una sola por producto | Varía entre productos (5000, 4000, 2500, 1254, 1080 px). Dentro de un mismo producto mezclan: The First 50 Years (1254/2500) y Break Some Eggs (1254/5000) |
| Nombre de archivos | — | Mezcla de 4 convenciones (Printify, `Nombre_-_Color.jpg`, `nombre-color.jpg`, `1.png…7-sand.png`). En 9 productos el archivo de Ice Grey se llama `7-sand`/`8-sand`, pero la foto sí es Ice Grey: es solo el nombre |
| Orden de la galería | — | En la mayoría no sigue el orden de los colores, y la foto principal es de un color distinto en cada producto (Black 67, Navy 67, Sport Grey 54, Military Green 52…) |

### Títulos duplicados
- Dos productos se llaman exactamente **"Circle Back T-Shirt"** y otros dos **"Fixer T-Shirt"** (handles `…-t-shirt` y `…-t-shirt-1`).
- Hay series con número que pueden ser a propósito: Slow Me Down (3), Hose Water (4), Daily Dose (3), Sumbitch, Raised By Wolves, 80s Fan, Antisocial, Woke Up Bald Again, Ew People, Whatever, Well Seasoned, I'll Be In My Office (2 cada uno).

---

## 3. Colores (revisar si fue a propósito)
El modelo tiene 7 colores: White, Ice Grey, Sport Grey, Military Green, Charcoal, Navy, Black. Solo **167 productos** tienen exactamente esos 7; los otros 184 forman 54 combinaciones distintas:
- **82 sin Ice Grey** (seguramente se cargaron antes de que se sumara Ice Grey) y **22 más con Sand en lugar de Ice Grey**.
- 12 sin los claros (White, Ice Grey, Sport Grey) y 12 sin Ice Grey, Navy ni Black: tiene sentido para diseños de una sola tinta.
- Hay colores sueltos que usan pocos productos: Stone Blue (14), Sage (9), Purple (8), Dark Chocolate (8), Light Blue (8), Maroon (5), Graphite Heather (1), Natural (1).
- 4 productos tienen los 7 colores estándar, pero en otro orden en el selector: Peaked, Dodge Ball Survivor, Sumbitch, Confuse Them.

Si la idea es que todos queden iguales, para cada producto hay que decidir si suma Ice Grey (y sacar Sand) o si el diseño no se lee en ese color.

---

## 4. Colecciones
- Todos están en `sale`. `sale-test` y `sale-test-2` (286–287 productos cada una) parecen de prueba: conviene revisar si siguen haciendo falta.
- **96 productos no están en ninguna colección temática** (50th Birthday, Bald & Bold, Core, Gen X, Gifts For Him, Parenting, Retro Nostalgia, Sarcastic Dad Jokes). Entre ellos está el modelo "10 p.m". La lista completa está en el CSV.

---

## Orden sugerido para corregir
1. Lo que ve el cliente: las fotos de color equivocado, los colores sin foto, las fotos sueltas de colores que no se venden y los 57 fondos blancos más el verde.
2. Talles desordenados (2 productos), título sin "T-Shirt", producto sin tags y las 12 descripciones con GPSR (o sumarle GPSR a todos, si hace falta por la UE).
3. Unificar el orden de opciones (Color → Size) y el orden de colores.
4. Decidir Ice Grey vs Sand y la paleta por producto.
5. Handles: renombrar los que tienen errores de tipeo, **siempre con redirección 301** desde el viejo para no perder SEO ni links.
6. Colecciones temáticas para los 96 productos que no tienen.
