# AMULETO: arquitectura del nuevo sitio (etapa 1: sitemap)

> Documento de trabajo para revisar y aprobar antes de pasar a la maqueta. No incluye diseño visual ni código.

---

## 0. Alcance y limitaciones del análisis

- **No pude abrir cheweb.com.ar ni amuletoweb.com.ar directamente.** El entorno donde trabajé bloquea el acceso a esos dominios. El diagnóstico de la referencia se basa solo en lo que los buscadores tienen indexado de cheweb.com.ar: la home, un artículo del blog y una página de plantilla.
- Por eso **no puedo afirmar** cómo es el menú de CheWeb, el orden exacto de los bloques de su home, si tiene testimonios, preguntas frecuentes o botón flotante de WhatsApp, ni cómo es su estilo visual. En el punto 1 separo lo verificado de lo que falta verificar.
- **Del sitio actual de AMULETO no obtuve ningún dato.** Todo lo que menciono sobre AMULETO sale de este pedido. Lo que falta quedó como supuesto explícito o como decisión pendiente (punto 9).
- Recomendación: antes de la maqueta, que alguien del equipo recorra cheweb.com.ar con la checklist del punto 1.3 (son 10 minutos) y confirme o corrija el diagnóstico.

---

## 1. Diagnóstico de la referencia (cheweb.com.ar)

### 1.1 Lo que pude verificar

| Aspecto | Lo observado |
|---|---|
| **Foco de la home** | El título de la home es «Diseño de Páginas Web en Buenos Aires»: servicio y ubicación en la primera línea, sin eslogan abstracto. Es una frase pensada para la búsqueda en Google. |
| **Posicionamiento** | Se presenta como un estudio digital independiente y no como una agencia. El mensaje es que la misma persona piensa, diseña, construye y entrega cada sitio. La cercanía es el diferencial. |
| **Oferta** | Tres formatos fáciles de entender: landing o web institucional, web personalizada (con funciones como turnos o formularios) y tienda online. Están organizados por tipo de resultado y no por tecnología. |
| **Beneficios** | Diseño propio, carga rápida y optimización para Google. Son atributos concretos y verificables. |
| **Conversión** | La CTA principal es pedir presupuesto online, con una promesa concreta: la propuesta llega en 24 horas. |
| **Trabajos** | La home tiene una sección de trabajos recientes con casos nombrados (Mecanizados NV, un ecommerce industrial; Viandas H&G, un sitio de viandas). Cada caso describe qué se hizo (catálogo, pago con MercadoPago, panel propio). |
| **Contacto visible** | Teléfono celular, email y horario de atención (lunes a viernes, de 9 a 19 h) en la home. |
| **Precios públicos** | Modelo de abono mensual con configuración inicial, sin contrato. El blog publica precios y la plantilla de muestra indica un precio «desde». |
| **Plantillas** | Hay un catálogo de plantillas por rubro (`/plantillas/{rubro}/`). El blog habla de más de 87. Cada plantilla es una página propia con precio. |
| **Blog** | Tiene artículos con intención comercial, por ejemplo «¿Cuánto cuesta una página web en Argentina? Precios 2026». Responde la pregunta que el cliente busca antes de contratar y compara con alternativas (freelancer, desarrollo a medida). |
| **URLs** | Son cortas y descriptivas: `/blog/{tema}/`, `/plantillas/{rubro}/`. |

### 1.2 Principios que hacen efectiva a la referencia (mi lectura)

1. **Dice qué hace en la primera línea**, con las palabras que usa el cliente («páginas web», «tienda online») y no con jerga.
2. **Reduce la incertidumbre de la compra**: precio visible, plazo de respuesta concreto, sin contrato y una persona identificable.
3. **Muestra prueba real**: casos con nombre y con lo que se construyó, no capturas genéricas.
4. **Tiene una sola acción principal** (pedir presupuesto), siempre a mano.
5. **Usa el contenido como captación**: el blog responde preguntas de compra («cuánto cuesta») y no publica noticias del sector.

### 1.3 Lo que no pude verificar (checklist para confirmar)

- [ ] Ítems del menú principal y si hay submenús.
- [ ] Orden de los bloques de la home.
- [ ] Si hay testimonios, logos de clientes o reseñas de Google.
- [ ] Si hay preguntas frecuentes y dónde.
- [ ] Si hay botón flotante de WhatsApp y si el formulario es corto o un asistente de varios pasos.
- [ ] Si los servicios tienen páginas propias o solo bloques en la home.
- [ ] Contenido del footer.
- [ ] Estilo visual: paleta, tipografía, tipo de imágenes.

Nada de lo que propongo para AMULETO depende de estos puntos. Si al verificarlos aparece algo útil, se incorpora en la maqueta.

### 1.4 Diferencia clave entre CheWeb y AMULETO

CheWeb vende **una sola cosa**: sitios web, con un modelo de abono y plantillas. AMULETO vende **tres cosas distintas** (web, sistemas y publicidad) a públicos que llegan con problemas diferentes. Por eso de la referencia conviene tomar la **claridad, la reducción de incertidumbre y la prueba real**, pero **no la estructura de una sola página con catálogo de plantillas**. AMULETO necesita una página por eje.

---

## 2. Criterios estratégicos para AMULETO

### 2.1 Posicionamiento

- **Qué somos**: un equipo que arma la parte digital de un negocio (el sitio, las herramientas internas y la publicidad) y se ocupa de que funcione en conjunto.
- **Diferencial a comunicar**: un solo interlocutor para el sitio web, los sistemas y la publicidad. El valor concreto es que la publicidad lleva a un sitio pensado para convertir, las consultas entran a un sistema ordenado y nadie se pasa la pelota entre proveedores. *Supuesto: AMULETO efectivamente hace proyectos que combinan áreas. Si no es así, este bloque se reformula (ver decisiones pendientes).*
- **Tono**: frases cortas, con verbos de acción y ejemplos concretos («que las consultas de la web lleguen directo a tu planilla»). Nada de «soluciones innovadoras».

### 2.2 Jerarquía de servicios

| Eje | Rol comercial | Por qué |
|---|---|---|
| **Diseño web** | **Puerta de entrada principal** | Es lo que más se busca y lo que el cliente sabe pedir. Primer lugar en el menú y en la home. |
| **Publicidad** | Segundo eje | Tiene demanda clara (Google Ads) y se complementa con la web: «ya tengo web y no me llegan consultas». |
| **Sistemas** | Eje de mayor valor y menor comprensión | El cliente no busca «sistemas», busca resolver un problema («pierdo tiempo pasando pedidos a mano»). Hay que comunicarlo con problemas y ejemplos, nunca con tecnologías. |

*El orden es una recomendación. Si la facturación real de AMULETO tiene otra jerarquía, se ajusta (decisión pendiente 2).*

### 2.3 Públicos

*Supuesto, a confirmar con la cartera real de clientes:*

1. **Pymes y comercios** que necesitan un sitio nuevo o renovar uno que no les trae consultas.
2. **Negocios que quieren vender online** (WooCommerce).
3. **Profesionales y estudios** (salud, legales, contables, servicios) que necesitan presencia y turnos o consultas.
4. **Empresas con procesos manuales** (pedidos, stock, presupuestos, planillas) que necesitan automatizar o integrar.
5. **Negocios que ya tienen web** y quieren más clientes con Google Ads o redes.

### 2.4 Conversión

- **Una acción principal en todo el sitio**: «Pedir presupuesto», que lleva a `/contacto/` con el área preseleccionada según la página de origen (`/contacto/?servicio=publicidad`).
- **Una acción secundaria**: WhatsApp, con un mensaje precargado distinto en cada página («Hola, vengo de la página de Tiendas online…»).
- **Medición desde el día 1**: envíos de formulario, clics en WhatsApp, en el teléfono y en el email. Si vendemos publicidad, el sitio tiene que medir sus propias conversiones.
- **Reducir la incertidumbre**, como hace la referencia: plazo de respuesta concreto, cómo es el proceso, qué incluye cada servicio y, si se decide, precios orientativos.

### 2.5 Alternativas evaluadas

**A. ¿Dónde van los servicios en la URL?**

| Opción | Ejemplo | A favor | En contra |
|---|---|---|---|
| Con prefijo | `/servicios/diseno-web/tiendas-online/` | Agrupa todo bajo un padre | URLs largas y una página `/servicios/` que repite la home |
| **Sin prefijo (recomendada)** | `/diseno-web/tiendas-online/` | URLs cortas y claras; cada eje es un pilar de SEO | Ninguno relevante con solo tres ejes |

**B. ¿Cuántas subpáginas por eje en el lanzamiento?**

| Opción | A favor | En contra |
|---|---|---|
| Todas las subpáginas desde el inicio | Más superficie para SEO | Páginas flacas sin casos, más trabajo de redacción y lanzamiento más lento |
| **Pilar + solo las subpáginas con búsqueda propia y oferta real (recomendada)** | Cada URL tiene contenido suficiente; se lanza antes | Algunas búsquedas quedan cubiertas por la página pilar hasta la fase 2 |

**C. ¿Formulario de presupuesto aparte o un único contacto?**

**Recomiendo un único `/contacto/`** con un selector de servicio. Una página `/presupuesto/` separada duplicaría la función y dividiría la medición. Si más adelante se quiere un formulario guiado, se reemplaza el formulario dentro de la misma URL.

---

## 3. Sitemap propuesto

**Leyenda:** ● imprescindible (fase 1) · ◐ recomendada (fase 2) · ○ opcional o condicionada a una decisión (fase 2 o 3)

```
amuletoweb.com.ar/
│
├── ● Inicio                                   /
│
├── ● Diseño web                               /diseno-web/
│   ├── ● Tiendas online (WooCommerce)          /diseno-web/tiendas-online/
│   ├── ◐ Sitios WordPress para empresas        /diseno-web/sitios-wordpress/
│   └── ○ Mantenimiento web                     /diseno-web/mantenimiento/        (solo si se ofrece como servicio)
│
├── ● Sistemas                                 /sistemas/
│   ├── ◐ Automatizaciones e integraciones      /sistemas/automatizaciones/
│   └── ◐ Desarrollo a medida                   /sistemas/desarrollo-a-medida/
│
├── ● Publicidad                               /publicidad/
│   ├── ● Google Ads                            /publicidad/google-ads/
│   └── ◐ Publicidad en redes sociales          /publicidad/redes-sociales/
│
├── ● Trabajos                                 /trabajos/                         (si hay al menos 3 casos publicables)
│   └── ● Caso individual                       /trabajos/{cliente-o-proyecto}/
│
├── ◐ Nosotros                                 /nosotros/
│
├── ● Contacto                                 /contacto/
│   └── ● Gracias (noindex)                     /contacto/gracias/
│
├── ○ Blog                                     /blog/
│   └── ○ Artículo                              /blog/{tema}/
│
└── ● Política de privacidad                   /politica-de-privacidad/
```

### Justificación de cada URL

| URL | Por qué existe | Por qué no se fusiona con otra |
|---|---|---|
| `/` | Orienta y deriva a cada eje | — |
| `/diseno-web/` | Pilar del eje principal; responde a «diseño web» y «página web para empresa» | — |
| `/diseno-web/tiendas-online/` | Búsqueda propia («tienda online», «WooCommerce»), otro público (quien vende) y otra oferta (pagos, envíos, stock) | Dentro de la página pilar quedaría diluida |
| `/diseno-web/sitios-wordpress/` | Captura «diseño web WordPress» y explica qué gana el cliente (autonomía para editar) | En fase 1 su contenido vive en el pilar. Se separa cuando haya casos y texto suficientes |
| `/diseno-web/mantenimiento/` | Público distinto (ya tiene web) y posible ingreso recurrente | Solo existe si AMULETO lo vende como servicio |
| `/sistemas/` | Pilar del eje con más necesidad de explicación; en fase 1 cubre todas las soluciones con ejemplos | — |
| `/sistemas/automatizaciones/` | Problema muy concreto (tareas repetitivas, datos copiados a mano, herramientas que no se conectan) | Se separa cuando haya casos para mostrar |
| `/sistemas/desarrollo-a-medida/` | Otro tamaño de proyecto y otro ciclo de venta (paneles, sistemas de gestión) | Ídem |
| `/publicidad/` | Pilar; para quien sabe que necesita clientes pero no qué canal usar | — |
| `/publicidad/google-ads/` | Es la búsqueda con más intención del eje y el cliente la nombra explícitamente | Merece una explicación propia (gestión, inversión, medición) |
| `/publicidad/redes-sociales/` | Meta Ads e Instagram tienen otro público y otro objetivo (descubrimiento) | Se separa en fase 2 si hay oferta y casos |
| `/trabajos/` y casos | La prueba real es el principal generador de confianza (principio observado en la referencia) | Un caso por URL permite enlazarlo desde cada página de servicio |
| `/nosotros/` | Pone cara y respaldo a la empresa; la referencia muestra que la cercanía vende | Puede empezar como bloque de la home si no hay material (decisión 5) |
| `/contacto/` | Conversión centralizada y medible | — |
| `/contacto/gracias/` | Permite medir conversiones de Google Ads y Analytics con una URL de destino; confirma el envío y dice qué pasa después | Sin indexar; no aparece en menús |
| `/blog/` | Captación con preguntas de compra, como el artículo de precios de la referencia | Solo si hay capacidad de publicar (decisión 8). Un blog vacío resta |
| `/politica-de-privacidad/` | Obligatoria si hay formularios y píxeles de medición (Ley 25.326) | — |

### Páginas descartadas a propósito

- **`/servicios/`**: repetiría la home. El menú «Servicios» despliega los tres ejes directamente.
- **`/plantillas/`**: solo tiene sentido con un modelo de venta por plantilla y abono, como el de CheWeb. Queda descartada salvo que AMULETO quiera ese modelo (decisión 4).
- **`/precios/` independiente**: si se publican precios, van dentro de cada página de servicio, donde el visitante decide (decisión 4).
- **`/presupuesto/`**: duplicaría `/contacto/` (ver 2.5 C).
- **Páginas por ciudad o rubro** (por ejemplo, «diseño web en Rosario», «webs para odontólogos»): solo en fase 3, con datos de búsqueda que las justifiquen y casos reales del rubro.
- **Testimonios como página aparte**: los testimonios rinden más junto a la decisión, en la home y en cada servicio, que en una página que nadie visita.

---

## 4. Menú de navegación

### 4.1 Header (desktop)

```
[Logo AMULETO]   Diseño web ▾   Sistemas ▾   Publicidad ▾   Trabajos   Nosotros   Contacto    [ Pedir presupuesto ]
```

Los tres ejes van **directo en el menú**, sin un «Servicios» que obligue a un clic más. Son solo tres y son la oferta.

**Submenús** (desplegables simples, no un megamenú):

- **Diseño web** → Diseño web (vista general) · Tiendas online · *(fase 2: Sitios WordPress · Mantenimiento)*
- **Sistemas** → Sistemas (vista general) · *(fase 2: Automatizaciones e integraciones · Desarrollo a medida)*. **En fase 1 no tiene submenú**: es un enlace directo.
- **Publicidad** → Publicidad (vista general) · Google Ads · *(fase 2: Redes sociales)*

Cada submenú repite la página pilar como primer ítem. En mobile, el ítem padre abre el submenú y no navega, así que el pilar tiene que estar como hijo.

**CTA destacado**: botón «Pedir presupuesto» → `/contacto/`. Se distingue visualmente del resto del menú. En el header fijo queda visible al hacer scroll.

*Alternativa evaluada*: poner WhatsApp como CTA del header. Recomiendo «Pedir presupuesto» en el header y WhatsApp como botón flotante. Así cada canal tiene su lugar y se pueden medir por separado.

### 4.2 Mobile

- Header fijo compacto: logo, icono de WhatsApp y botón de menú.
- Menú desplegado: los tres ejes como acordeón, luego Trabajos, Nosotros y Contacto, y al final el botón «Pedir presupuesto» a todo el ancho.
- Botón flotante de WhatsApp en todas las páginas excepto `/contacto/`, donde el canal ya está dentro de la página.

### 4.3 Footer

| Columna 1: Marca | Columna 2: Diseño web | Columna 3: Sistemas | Columna 4: Publicidad | Columna 5: Contacto |
|---|---|---|---|---|
| Logo + una frase que diga qué hace AMULETO | Diseño web · Tiendas online · *(fase 2: subpáginas)* | Sistemas · *(fase 2: subpáginas)* | Publicidad · Google Ads · *(fase 2: Redes)* | WhatsApp · Email · Teléfono · Horario · Zona de trabajo |
| Trabajos · Nosotros · Blog *(si existe)* | | | | Redes sociales de AMULETO *(solo las activas)* |

Barra inferior: © AMULETO · Política de privacidad · *(datos fiscales, si se quieren mostrar)*.

---

## 5. Wireframe textual de la home

Lógica de la secuencia: **qué hacemos → para qué problema → prueba → cómo trabajamos → dudas → contacto.**

### B0. Header
- **Objetivo**: navegación y acceso permanente a la conversión.
- **Contenido**: logo, menú (4.1) y botón «Pedir presupuesto».
- **CTA**: Pedir presupuesto → `/contacto/`.

### B1. Hero
- **Objetivo**: que en 5 segundos se entienda qué hace AMULETO y para quién.
- **Mensaje**: hacemos sitios web, sistemas y publicidad digital para empresas, comercios y profesionales.
- **Contenido**:
  - H1 descriptivo, al estilo de la referencia: servicio + público (y ubicación si se decide). Ejemplo de dirección, no texto final: *«Diseño web, sistemas y publicidad digital para empresas y profesionales»*.
  - Bajada de una o dos líneas con el problema y el resultado: *sitios que generan consultas, herramientas que ahorran tiempo, campañas que traen clientes*.
  - Prueba breve debajo de los botones, **solo con datos reales**: años de trabajo, cantidad de proyectos o un logo de cliente.
- **Visual**: captura real de un sitio hecho por AMULETO en un dispositivo, o un collage de 2 o 3 trabajos. Sin imágenes de stock ni carruseles.
- **CTA principal**: «Pedir presupuesto» → `/contacto/`. **CTA secundario**: «Ver trabajos» → `/trabajos/` (o WhatsApp si todavía no hay casos).

### B2. Los tres ejes («¿Qué necesitás resolver?»)
- **Objetivo**: derivar a cada visitante a su eje lo antes posible.
- **Mensaje**: cada eje resuelve un problema distinto, explicado con palabras del cliente.
- **Contenido**: tres tarjetas iguales.
  - **Diseño web**: *«Necesito una web nueva, que la actual funcione mejor o vender online.»* Viñetas: sitios WordPress, tiendas online WooCommerce. → `/diseno-web/`
  - **Sistemas**: *«Pierdo tiempo en tareas manuales, planillas y herramientas que no se conectan.»* Viñetas: automatizaciones, integraciones, herramientas a medida. → `/sistemas/`
  - **Publicidad**: *«Necesito más consultas y clientes.»* Viñetas: Google Ads, publicidad en redes. → `/publicidad/`
- **Visual**: un icono simple por eje. Las tarjetas son un componente reutilizable.
- **CTA**: «Ver Diseño web», «Ver Sistemas», «Ver Publicidad».

### B3. Accesos directos por necesidad *(opcional; puede integrarse en B2)*
- **Objetivo**: llevar a quien ya sabe lo que busca directo a la subpágina.
- **Contenido**: fila de enlaces o chips: «Quiero vender online» → Tiendas online · «Quiero aparecer en Google» → Google Ads · «Quiero automatizar pedidos o presupuestos» → Sistemas.
- **Visual**: chips o lista horizontal.

### B4. El diferencial: web, sistemas y publicidad en un solo equipo
- **Objetivo**: explicar por qué contratar a AMULETO y no a tres proveedores separados.
- **Mensaje**: la publicidad lleva a un sitio preparado para convertir, el sitio entrega las consultas ordenadas y todo se mide. Un solo interlocutor.
- **Contenido**: un esquema simple de tres pasos (*atraer → convertir → organizar*) con un ejemplo concreto, idealmente un caso real que combine ejes.
- **Visual**: diagrama lineal de 3 pasos.
- **CTA**: «Contanos tu caso» → `/contacto/`.
- *Condicionado a la decisión 3 (si AMULETO hace proyectos combinados).*

### B5. Trabajos destacados
- **Objetivo**: mostrar prueba real, como hace la referencia con sus casos con nombre.
- **Contenido**: 3 casos. Cada uno con captura, nombre del cliente, rubro, etiqueta de eje (Web, Sistemas o Publicidad) y una línea que diga qué se hizo y qué resolvió. Solo se incluyen resultados numéricos si son reales y el cliente autoriza mostrarlos.
- **Visual**: grilla de tarjetas (el mismo componente que en `/trabajos/`).
- **CTA**: «Ver todos los trabajos» → `/trabajos/`.

### B6. Cómo trabajamos
- **Objetivo**: reducir la incertidumbre sobre qué pasa después de escribir.
- **Contenido**: 4 pasos. 1) Nos contás qué necesitás. 2) Te enviamos una propuesta con alcance, plazo y costo. 3) Desarrollamos y revisamos con vos. 4) Publicamos, te capacitamos y hacemos seguimiento. *El plazo de respuesta (por ejemplo, «propuesta en X días hábiles») se publica solo si AMULETO puede cumplirlo siempre (decisión 6).*
- **Visual**: pasos numerados. Componente reutilizable en las páginas de servicio.
- **CTA**: «Empezar por el paso 1» → `/contacto/`.

### B7. Confianza: testimonios y clientes *(solo con material real)*
- **Objetivo**: prueba de terceros.
- **Contenido**: 2 o 3 testimonios con nombre, empresa y foto o logo, y/o una franja de logos de clientes, y/o la calificación de Google Business si existe.
- **Visual**: tarjetas de testimonio y franja de logos en escala de grises.
- **Si no hay material**: se omite en fase 1. No se reemplaza por textos genéricos.

### B8. Preguntas frecuentes
- **Objetivo**: responder las objeciones antes del contacto.
- **Contenido sugerido** (5 o 6 preguntas, con respuestas que defina AMULETO): ¿Cuánto cuesta? · ¿Cuánto tarda? · ¿El sitio y el dominio quedan a mi nombre? · ¿Puedo editar el sitio yo mismo? · ¿Trabajan con clientes de todo el país? · En publicidad, ¿la inversión en anuncios está incluida?
- **Visual**: acordeón (componente reutilizable, con preguntas propias en cada servicio).

### B9. CTA final
- **Objetivo**: cierre para quien llegó al final.
- **Mensaje**: *«Contanos qué necesitás y te respondemos con una propuesta concreta.»*
- **Contenido**: formulario corto (nombre, email o WhatsApp, servicio y mensaje) o botón a `/contacto/` + botón de WhatsApp.
- **Visual**: banda de color de marca. Componente reutilizable en todas las páginas.
- **CTA**: Enviar / Escribir por WhatsApp.

### B10. Footer
Según 4.3.

---

## 6. Fichas de las páginas internas

> Todas las páginas de servicio comparten un **esqueleto común** para que en WordPress se arme con los mismos componentes:
> **Hero → Problemas que resolvemos → Qué hacemos / qué incluye → Casos relacionados → Proceso → (Precios, si se decide) → FAQ propias → CTA final.**

### 6.1 Diseño web — `/diseno-web/` ●
- **Objetivo comercial**: captar proyectos de sitios nuevos y rediseños, y derivar a Tiendas online cuando corresponde.
- **Público**: pymes, comercios y profesionales sin web o con una web vieja que no genera consultas.
- **Problema que resuelve**: «Mi web no me trae clientes, se ve mal en el celular, no la puedo editar o no tengo web».
- **Secciones**:
  1. Hero: qué hacemos (sitios WordPress y tiendas online) y para quién.
  2. Señales de que necesitás una web nueva (lista de problemas reconocibles).
  3. Tipos de proyecto (tarjetas): sitio institucional / landing · sitio WordPress completo · tienda online (→ subpágina).
  4. Qué incluye cada sitio. *A confirmar por AMULETO, por ejemplo: adaptación a celulares, SEO básico, formulario y WhatsApp, medición, capacitación para editar.*
  5. Trabajos de diseño web (filtrados por eje).
  6. Proceso.
  7. Precios orientativos *(si se decide)*.
  8. FAQ: plazos, dominio y hosting, quién carga los contenidos, ¿puedo editarlo?
  9. Puente a otros ejes: «¿Ya tenés web y necesitás más visitas? → Publicidad».
  10. CTA final.
- **CTA principal**: Pedir presupuesto (`/contacto/?servicio=diseno-web`). **Secundario**: WhatsApp.
- **Relaciones**: hija → Tiendas online; laterales → Publicidad (tráfico) y Sistemas (integraciones del sitio); casos → `/trabajos/`.

### 6.2 Tiendas online — `/diseno-web/tiendas-online/` ●
- **Objetivo comercial**: captar proyectos de ecommerce con WooCommerce.
- **Público**: comercios que venden por Instagram o WhatsApp y quieren su tienda, o que quieren dejar una plataforma con comisiones o limitaciones.
- **Problema que resuelve**: «Vendo por mensajes y no doy abasto», «quiero cobrar online», «mi tienda actual me limita».
- **Secciones**: Hero · Por qué tener tienda propia (sin comisión por venta de la plataforma, control del catálogo y de los datos) · Qué incluye (catálogo, carrito, medios de pago y de envío *disponibles según lo que AMULETO implemente*) · Qué podés administrar vos (productos, stock, pedidos) · Integraciones posibles (→ Sistemas: stock, facturación, ERP) · Casos de tiendas · Proceso · FAQ (pagos, envíos, carga de productos, migración desde otra plataforma) · CTA.
- **CTA principal**: Pedir presupuesto para tu tienda. **Secundario**: Ver tiendas que hicimos.
- **Relaciones**: padre → Diseño web; laterales → Sistemas/automatizaciones (stock, facturación) y Publicidad/Google Ads (Shopping o campañas de ventas).

### 6.3 Sitios WordPress para empresas — `/diseno-web/sitios-wordpress/` ◐
- **Objetivo comercial**: posicionar para «diseño web WordPress» y vender sitios institucionales completos.
- **Público**: empresas y profesionales que quieren un sitio que puedan administrar.
- **Problema**: «Dependo de alguien para cambiar un texto» o «mi web no aparece en Google».
- **Secciones**: Hero · Por qué WordPress, en términos de beneficio (autonomía, sin depender del proveedor) · Qué incluye · Casos · Proceso · FAQ · CTA.
- **CTA**: Pedir presupuesto. **Relaciones**: padre → Diseño web; lateral → Mantenimiento.
- *En fase 1 su contenido vive dentro de `/diseno-web/`.*

### 6.4 Mantenimiento web — `/diseno-web/mantenimiento/` ○
- **Condición**: existe solo si AMULETO ofrece mantenimiento, actualizaciones y soporte como servicio (decisión 7).
- **Objetivo comercial**: ingreso recurrente y puerta de entrada para clientes con un sitio existente.
- **Público**: quien ya tiene un WordPress (hecho por AMULETO o por otro).
- **Problema**: «Mi web está desactualizada, se cayó, me hackearon o no tengo a quién llamar».
- **Secciones**: Hero · Qué cubre · Qué no cubre · Modalidad (plan mensual o por hora, según la decisión) · FAQ · CTA.
- **CTA**: Consultar por mantenimiento.

### 6.5 Sistemas — `/sistemas/` ●
- **Objetivo comercial**: hacer comprensible y deseable el eje menos conocido y captar consultas calificadas.
- **Público**: empresas y negocios con procesos manuales o herramientas desconectadas.
- **Problema que resuelve**: tiempo perdido en tareas repetitivas, errores al copiar datos e información dispersa en planillas, mails y WhatsApp.
- **Secciones**:
  1. Hero orientado al problema (no «desarrollo de software»). Dirección: *«Herramientas para que tu negocio funcione con menos trabajo manual»*.
  2. «¿Te pasa esto?»: 4 a 6 situaciones reconocibles (pasar pedidos a mano, presupuestos en Word, stock en una planilla que nadie actualiza, consultas perdidas en WhatsApp, etc.).
  3. Qué hacemos, en dos grupos: **Automatizaciones e integraciones** (conectar herramientas que ya usás) y **Desarrollo a medida** (paneles, sistemas de gestión, portales). En fase 2 cada grupo pasa a ser una subpágina.
  4. Ejemplos concretos con «antes y después» del proceso (casos reales o ejemplos marcados como ilustrativos).
  5. Cómo trabajamos en sistemas: relevamiento → propuesta → desarrollo por etapas → puesta en marcha → soporte. Esto tranquiliza en proyectos menos tangibles.
  6. Casos de sistemas.
  7. FAQ: ¿tengo que cambiar las herramientas que uso? ¿qué pasa si algo falla? ¿quién es dueño del desarrollo? ¿cuánto cuesta un relevamiento?
  8. CTA final.
- **CTA principal**: «Contanos tu proceso» (`/contacto/?servicio=sistemas`). **Secundario**: agendar una llamada *(si se decide ofrecer reuniones agendables, decisión 6)*.
- **Relaciones**: hijas (fase 2); laterales → Tiendas online (integración de stock y pedidos) y Diseño web (formularios conectados).

### 6.6 Automatizaciones e integraciones — `/sistemas/automatizaciones/` ◐
- **Objetivo**: captar proyectos chicos y medianos de rápida implementación, que son una buena puerta de entrada al eje.
- **Público**: negocios que ya usan herramientas (planillas, CRM, tienda, facturación, mail) y las quieren conectar.
- **Problema**: datos que se copian a mano y tareas repetitivas.
- **Secciones**: Hero · Ejemplos de automatizaciones (lista concreta) · Herramientas con las que trabajamos *(solo las que AMULETO domine efectivamente)* · Casos · Proceso · FAQ · CTA.
- **CTA**: Contanos qué tarea querés automatizar.

### 6.7 Desarrollo a medida — `/sistemas/desarrollo-a-medida/` ◐
- **Objetivo**: captar proyectos de mayor tamaño (paneles, sistemas de gestión, portales de clientes).
- **Público**: empresas para las que ninguna herramienta estándar resuelve su proceso.
- **Problema**: «Lo que hay en el mercado no se adapta a cómo trabajamos».
- **Secciones**: Hero · Cuándo conviene desarrollar a medida y cuándo no (honestidad que genera confianza) · Tipos de desarrollo · Proceso por etapas · Casos · FAQ (propiedad del código, soporte, escalabilidad) · CTA.
- **CTA**: Pedir una reunión de relevamiento.

### 6.8 Publicidad — `/publicidad/` ●
- **Objetivo comercial**: captar gestión de campañas y orientar a quien no sabe qué canal le conviene.
- **Público**: negocios con web (o en vías de tenerla) que necesitan más consultas o ventas.
- **Problema**: «No me llegan clientes», «invertí en publicidad y no sé qué resultado tuvo».
- **Secciones**:
  1. Hero: campañas para conseguir consultas y ventas, con medición clara.
  2. Google Ads vs. redes sociales: cuándo conviene cada uno (comparativa breve; ayuda a elegir y deriva a la subpágina).
  3. Qué incluye la gestión: configuración, anuncios, medición de conversiones, optimización y reportes. *Alcance y frecuencia de reportes a confirmar.*
  4. La importancia de la página de destino (puente natural con Diseño web: el diferencial de AMULETO).
  5. Casos de publicidad (solo con métricas reales autorizadas).
  6. Proceso.
  7. FAQ: ¿la inversión en anuncios está incluida? ¿cuánto hay que invertir como mínimo? ¿hay permanencia? ¿de quién es la cuenta publicitaria?
  8. CTA final.
- **CTA principal**: Pedir propuesta de campaña (`/contacto/?servicio=publicidad`). **Secundario**: WhatsApp.
- **Relaciones**: hijas → Google Ads y Redes; lateral → Diseño web (páginas de destino).

### 6.9 Google Ads — `/publicidad/google-ads/` ●
- **Objetivo**: captar la búsqueda de mayor intención del eje («agencia Google Ads», «campañas en Google»).
- **Público**: negocios que quieren aparecer cuando alguien busca su servicio o producto.
- **Problema**: «No aparezco en Google» o «gasto en Google Ads y no veo resultados».
- **Secciones**: Hero · Tipos de campaña que gestiona AMULETO *(búsqueda, Shopping, Performance Max, etc., solo las que efectivamente gestione)* · Cómo medimos (conversiones: formularios, WhatsApp, llamadas, ventas) · Auditoría de cuentas existentes *(si se ofrece)* · Casos · FAQ · CTA.
- **CTA principal**: Pedir propuesta. **Secundario**: Pedir revisión de mi cuenta actual *(si se ofrece)*.
- **Relaciones**: padre → Publicidad; laterales → Tiendas online y Diseño web.

### 6.10 Publicidad en redes sociales — `/publicidad/redes-sociales/` ◐
- **Objetivo**: captar campañas en Meta (Instagram y Facebook) y otras redes que AMULETO gestione.
- **Público**: negocios con producto visual o de compra por impulso, o que buscan generar demanda.
- **Problema**: «Publico pero no vendo», «impulso publicaciones sin estrategia».
- **Secciones**: Hero · Qué hacemos (y qué no: aclarar si incluye gestión de contenido orgánico o solo anuncios, decisión 7) · Medición · Casos · FAQ · CTA.
- **CTA**: Pedir propuesta.

### 6.11 Trabajos — `/trabajos/` ● y `/trabajos/{slug}/` ●
- **Objetivo**: demostrar capacidad con evidencia real; es la página de apoyo de todas las demás.
- **Público**: cualquier visitante en etapa de evaluación.
- **Archivo `/trabajos/`**: H1 + filtro por eje (Todos · Diseño web · Sistemas · Publicidad) + grilla de tarjetas + CTA final. El filtro funciona con enlaces (`/trabajos/?area=sistemas` o por taxonomía), sin dependencias pesadas.
- **Ficha de caso** (plantilla fija, para que cargar un caso nuevo sea completar campos):
  1. Cliente, rubro y ejes involucrados (etiquetas).
  2. El desafío (qué problema tenía).
  3. Qué hicimos (alcance concreto).
  4. Resultado (cualitativo, o cuantitativo solo si es real y está autorizado).
  5. Capturas o galería.
  6. Testimonio del cliente *(si existe)*.
  7. Enlace al sitio *(si está publicado y el cliente lo permite)*.
  8. «¿Necesitás algo parecido?» → CTA al servicio relacionado y a contacto.
- **CTA**: Pedir presupuesto / Ver servicio relacionado.
- **Relaciones**: cada caso se muestra automáticamente en la página del eje correspondiente (bloque «Casos relacionados»).
- *Condición*: con menos de 3 casos publicables se recomienda postergar el archivo y mostrar los casos solo dentro de la home y las páginas de servicio (decisión 1).

### 6.12 Nosotros — `/nosotros/` ◐
- **Objetivo**: poner cara y respaldo, siguiendo el principio de cercanía observado en la referencia.
- **Público**: visitantes en evaluación, sobre todo en proyectos de sistemas y en presupuestos grandes.
- **Secciones**: quiénes somos (en concreto: desde cuándo, dónde, cómo trabajamos) · equipo con foto, rol y especialidad *(si se quiere mostrar)* · forma de trabajo y compromisos (por ejemplo: el cliente es dueño de su dominio y de sus cuentas, si es política de AMULETO) · CTA.
- **CTA**: Contanos tu proyecto.
- *Sin datos reales de trayectoria y equipo, conviene reemplazarla por un bloque breve en la home (decisión 5).*

### 6.13 Contacto — `/contacto/` ●
- **Objetivo**: convertir con la menor fricción posible.
- **Público**: todo visitante decidido.
- **Secciones**:
  1. H1 directo y promesa de respuesta *(plazo a definir, decisión 6)*.
  2. Formulario: nombre · email · teléfono/WhatsApp · **servicio** (Diseño web / Tienda online / Sistemas / Publicidad / No estoy seguro) · mensaje. El servicio se preselecciona según el parámetro de la URL de origen. Nada más: cada campo extra baja la conversión.
  3. Canales directos: WhatsApp, email, teléfono y horario.
  4. Qué pasa después de enviar (los tres primeros pasos del proceso).
  5. Zona de trabajo / modalidad remota *(a definir)*.
- **CTA**: Enviar consulta. **Secundario**: WhatsApp.
- **Relaciones**: destino de todas las CTA; redirige a `/contacto/gracias/`.

### 6.14 Gracias — `/contacto/gracias/` ●
- **Objetivo**: confirmar el envío, medir la conversión y aprovechar el momento.
- **Contenido**: confirmación y plazo de respuesta · casos destacados del eje elegido · WhatsApp para urgencias.
- **Técnico**: `noindex` y fuera de menús y sitemap XML.

### 6.15 Blog — `/blog/` y `/blog/{tema}/` ○
- **Condición**: solo si hay capacidad de publicar al menos 1 o 2 artículos útiles por mes (decisión 8).
- **Objetivo**: captar búsquedas previas a la compra, como el artículo de precios de la referencia.
- **Temas con intención comercial** (ejemplos, cada uno enlazado a su servicio): cuánto cuesta una web o una tienda online · WooCommerce vs. otras plataformas · cuánto invertir en Google Ads · qué procesos de una pyme conviene automatizar primero.
- **CTA en cada artículo**: banda hacia el servicio relacionado.
- **Estructura**: sin categorías al inicio, o solo las tres de los ejes. Sin etiquetas, para no generar páginas vacías indexables.

### 6.16 Política de privacidad — `/politica-de-privacidad/` ●
- **Objetivo**: cumplimiento legal (formularios, cookies de medición y píxeles publicitarios).
- **Contenido**: texto legal a revisar por el asesor de AMULETO. Se enlaza desde el footer y desde el formulario.

---

## 7. Recorridos de usuario

### 7.1 Diseño web
- **A. Búsqueda en Google («diseño web para empresas»)** → `/diseno-web/` → Trabajos relacionados (en la misma página o en un caso) → CTA «Pedir presupuesto» → `/contacto/?servicio=diseno-web` → `/contacto/gracias/`.
- **B. Quiere vender online** → Home → chip «Quiero vender online» o tarjeta Diseño web → `/diseno-web/tiendas-online/` → caso de tienda → Contacto con «Tienda online» preseleccionado.
- **C. Llega por recomendación y quiere hablar rápido** → Home → hero → WhatsApp con mensaje precargado.

### 7.2 Sistemas
- **A. No sabe que «sistemas» es lo que necesita** → Home → tarjeta «Pierdo tiempo en tareas manuales» → `/sistemas/` → se reconoce en «¿Te pasa esto?» → ejemplo antes/después → «Contanos tu proceso» → Contacto.
- **B. Cliente de tienda online** → `/diseno-web/tiendas-online/` → bloque «Integraciones» → `/sistemas/` → Contacto.
- **C. Empresa que busca desarrollo a medida (fase 2)** → Google → `/sistemas/desarrollo-a-medida/` → Nosotros (evalúa al equipo) → pedido de reunión.

### 7.3 Publicidad
- **A. Búsqueda «agencia Google Ads»** → `/publicidad/google-ads/` → cómo medimos → FAQ sobre inversión → Contacto con «Publicidad» preseleccionado.
- **B. Tiene web y no le llegan consultas** → Home → tarjeta Publicidad → `/publicidad/` → comparativa Google vs. redes → subpágina → Contacto.
- **C. Venta cruzada** → Lee `/publicidad/` → bloque «La página de destino importa» → `/diseno-web/` → presupuesto combinado (selector «No estoy seguro» o mensaje libre).

### 7.4 Regla general
Toda página tiene **como máximo dos clics hasta el formulario** y **un clic hasta WhatsApp** (botón flotante).

---

## 8. Arquitectura para WordPress

| Necesidad | Propuesta | Justificación |
|---|---|---|
| Páginas de servicio | **Páginas jerárquicas** (padre/hija) | Generan las URLs del sitemap sin configuración extra y se editan como cualquier página. |
| Trabajos | **Tipo de contenido «Trabajo» + taxonomía «Área»** (Diseño web, Sistemas, Publicidad), registrados en el tema o en un mu-plugin propio | Permite el archivo filtrable, la plantilla fija de caso y mostrar casos por eje en cada servicio. Usar entradas del blog con categorías los mezclaría con los artículos. |
| Blog | Entradas nativas en `/blog/` | Nativo, sin plugins. |
| Componentes reutilizables | **Patrones sincronizados** del editor de bloques: CTA final, proceso, franja de confianza, tarjetas de ejes, FAQ | Se edita una vez y se actualiza en todo el sitio. Es lo que pide la maqueta componente por componente. |
| Tema | Tema propio liviano (de bloques o clásico), construido a partir de la maqueta | Mejor rendimiento y control que un tema comercial genérico. *Alternativa*: un constructor visual (por ejemplo, Elementor) da más autonomía de edición a cambio de peso y velocidad; decidir según quién mantenga el sitio (decisión 9). |
| SEO | **Un solo** plugin de SEO (Yoast o Rank Math): títulos, descripciones, sitemap XML, canonical, migas de pan, `noindex` en Gracias | Cubre todo el SEO técnico necesario; no hace falta más. |
| Formulario | **Un solo** plugin de formularios con parámetro de URL para preseleccionar el servicio y redirección a `/contacto/gracias/` | Requisito de conversión y medición. |
| Antispam | Honeypot o Cloudflare Turnstile | Evita el captcha visible que baja la conversión. |
| Medición | Google Tag Manager + GA4 + etiquetas de conversión de Google Ads / Meta, con eventos: envío de formulario, clic en WhatsApp, teléfono y email | Imprescindible para un sitio que vende publicidad. |
| Rendimiento | Imágenes WebP/AVIF con tamaños correctos, carga diferida, fuentes alojadas en el propio sitio, sin sliders ni animaciones pesadas, caché del hosting o un plugin de caché | Objetivo: buenas Core Web Vitals en mobile. Es también un argumento de venta. |
| Semántica | Un H1 por página; jerarquía H2/H3 según los bloques de este documento; migas de pan en subpáginas y casos; datos estructurados `Organization`/`LocalBusiness`, `Service`, `BreadcrumbList` | SEO técnico básico y correcto. |
| Migración | **Mapa de redirecciones 301** desde las URLs actuales de amuletoweb.com.ar | Para no perder el posicionamiento existente. Requiere relevar el sitio actual (decisión 10). |
| Escalabilidad | Nuevo servicio = nueva página hija con el esqueleto común; nuevo caso = completar la plantilla de «Trabajo» | Crecer no exige tocar el diseño ni la estructura. |

**Lo que no recomiendo sin una justificación concreta**: chat en vivo, megamenús, plugins de cotizador, multilenguaje, área de clientes o login, sliders y popups de entrada.

---

## 9. Prioridades de implementación

### Fase 1: estructura mínima para publicar
- Home (bloques B0–B10; B4 y B7 solo si hay material real).
- `/diseno-web/` + `/diseno-web/tiendas-online/`.
- `/sistemas/` (todas las soluciones en una sola página).
- `/publicidad/` + `/publicidad/google-ads/`.
- `/trabajos/` + casos (o casos solo dentro de las páginas, si hay menos de 3).
- `/contacto/` + `/contacto/gracias/`.
- `/politica-de-privacidad/`.
- Medición (GTM, GA4, conversiones), SEO técnico, redirecciones 301 y WhatsApp flotante.

**Total: 10 a 11 URLs indexables.**

### Fase 2: mejoras comerciales y contenido
- `/nosotros/`.
- Subpáginas: `/sistemas/automatizaciones/`, `/sistemas/desarrollo-a-medida/`, `/publicidad/redes-sociales/`, `/diseno-web/sitios-wordpress/`, `/diseno-web/mantenimiento/` *(si aplica)*.
- Más casos, testimonios reales y franja de logos; reseñas de Google Business.
- Blog con 4 a 6 artículos de intención comercial.
- Precios orientativos *(si se decide)*.
- Revisión de mensajes y CTA con datos reales de Analytics.

### Fase 3: funcionalidades y optimizaciones
- Formulario guiado de presupuesto (varios pasos) en `/contacto/`, si los datos muestran consultas poco calificadas.
- Agenda de reuniones integrada, si la venta de sistemas lo requiere.
- Landings por rubro o por ciudad, con datos de búsqueda y casos que las respalden.
- Landings específicas para campañas propias de AMULETO (sin indexar).
- Pruebas A/B de hero y CTA.

---

## 10. Decisiones pendientes antes de la maqueta

1. **Casos publicables**: ¿cuántos trabajos reales hay, de qué ejes y con permiso de los clientes para mostrarlos? Define si `/trabajos/` existe en fase 1 y qué muestra la home.
2. **Jerarquía real del negocio**: ¿qué eje factura más y cuál se quiere hacer crecer? Confirma o cambia el orden propuesto (Diseño web → Publicidad → Sistemas).
3. **Proyectos combinados**: ¿AMULETO hace proyectos que integran web, sistemas y publicidad? Define si el diferencial del bloque B4 es real o se reformula.
4. **Precios**: ¿se publican precios orientativos, rangos o «desde», o nada? ¿Hay algún modelo de abono o de plantillas, como el de la referencia? Define si se agregan bloques de precios a los servicios.
5. **Nosotros**: ¿quiénes son, desde cuándo trabajan, dónde están y si se quiere mostrar el equipo con fotos? Define si `/nosotros/` es página o bloque.
6. **Compromisos de servicio**: plazo de respuesta que se puede garantizar siempre, si se ofrecen reuniones agendables y si hay relevamiento sin costo para Sistemas.
7. **Alcance exacto por eje**: ¿se ofrece mantenimiento web? En redes, ¿solo anuncios o también contenido? ¿Qué tipos de campaña de Google Ads? ¿Qué herramientas o integraciones domina el equipo en Sistemas? Define qué subpáginas existen.
8. **Blog**: ¿hay alguien que pueda escribir 1 o 2 artículos por mes? Si no, el blog queda fuera.
9. **Mantenimiento del sitio y flujo de trabajo**: ¿quién va a editar el sitio después del lanzamiento (equipo técnico o personas no técnicas)? Define tema propio vs. constructor visual. Además, el pedido menciona «sitio estático» y también WordPress como destino final. **Supuesto**: la maqueta se hace en HTML estático y el sitio definitivo en WordPress. Confirmar.
10. **Sitio actual**: acceso o listado de las URLs actuales de amuletoweb.com.ar (y si tiene tráfico o posiciones relevantes) para armar las redirecciones, y saber si hay contenido reutilizable.
11. **Zona geográfica**: ¿se apunta a una ciudad o provincia concreta (para el H1, el SEO local y Google Business) o a todo el país de forma remota?

---

## Fuentes consultadas

- [Diseño de Páginas Web en Buenos Aires — CheWeb (home)](https://cheweb.com.ar/) (vía índice de buscadores)
- [¿Cuánto cuesta una página web en Argentina? Precios 2026 — CheWeb](https://cheweb.com.ar/blog/cuanto-cuesta-pagina-web-argentina/) (vía índice de buscadores)
- [Web para Tienda de Zapatillas — CheWeb (plantilla)](https://cheweb.com.ar/plantillas/zapatillas-urbano/) (vía índice de buscadores)
