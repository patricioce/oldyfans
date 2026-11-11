# 80s Survivors Club — clon de oldyfans.store

Destino: tienda Shopify **80ssurvivorsclub.com** (misma cuenta que OldyFans).
Tema origen: **BuildMyPOD v2.0.0**, publicado en OldyFans como "Cart Mobile Fix - 21 Oct 2026".
Idioma: inglés · Moneda: USD.

## Qué se clona
| Qué | Cómo | Estado |
|---|---|---|
| Tema (diseño + config de secciones) | `tema/` (código) · `tema-80s-survivors-club.zip` (para subir) | ✅ listo |
| Imágenes que usa el tema (logo, banners, íconos, guía de talles) | `archivos-para-subir/` → Contenido → Archivos, **con el mismo nombre** | ✅ listo |
| Páginas (About, Contact, Reviews) | `contenido/paginas/` — copiar a Tienda online → Páginas | ✅ listo |
| Políticas (privacidad, reembolso, envíos, términos) | `contenido/politicas/` — copiar a Configuración → Políticas | ✅ listo, faltan emails |
| Menús principal y pie | `contenido/menus.md` | ✅ listo |
| Checkout y emails de notificación | Manual en el admin (no salen por el tema ni por API) | ⏳ ver abajo |
| Colecciones, imágenes, productos, apps | No por ahora | — |

Los textos ya tienen "OldyFans" → "80s Survivors Club" y el dominio cambiado.
Emails: `info@` y `support@oldyfans.store` → `info@` y `support@80ssurvivorsclub.com`. El gmail de los Términos quedó como `[[EMAIL 80S SURVIVORS CLUB]]`.
La página "Your Privacy Choices" la crea Shopify sola: no hay que copiarla.

## Cambios hechos al tema (respecto del original exportado)
- Dominio `oldyfans.store` → `80ssurvivorsclub.com` en links (portada, ficha de producto, aviso de reembolso).
- Emails de soporte → `@80ssurvivorsclub.com` (contacto, ayuda, ficha de producto).
- "OldyFans" → "80s Survivors Club" en textos visibles (contacto, FAQ de ayuda, `llms.txt`).
- **Google Tag Manager desactivado** (era `GTM-WD2HNPKW`, el de OldyFans). Para activar uno propio: `layout/theme.liquid`, variable `gtm_id`.
- Sin tocar: nombres técnicos (`oldyfans-hero`, `oldyfans-help`, archivos CSS) y comentarios de código, para no romper nada.
- Pendiente a propósito: Facebook e Instagram siguen apuntando a OldyFans (Configuración del tema → Redes sociales), y el logo es el de OldyFans.

## Pasos para instalar
1. En 80s Survivors Club → **Contenido → Archivos** → subir las 10 imágenes de `archivos-para-subir/` sin renombrarlas (el tema las busca por nombre). Si Shopify les agrega un sufijo (`_1`, etc.) es porque ya existía una: borrarla y volver a subir.
2. **Tienda online → Temas → Agregar tema → Subir archivo zip** → `tema-80s-survivors-club.zip`. No publicar todavía.
3. Crear **páginas** (Tienda online → Páginas) con `contenido/paginas/`: About Us (`about`), Contact (`contact`, plantilla `page.contact`), Reviews (`reviews`). En "Contact" el cuerpo va vacío: el texto sale del tema.
4. **Políticas**: Configuración → Políticas → pegar cada archivo de `contenido/politicas/` (en modo código `<>`).
5. **Menús**: Contenido → Menús → según `contenido/menus.md`.
6. Abrir el tema en el editor y revisar la portada, una página de producto, contacto y `/pages/contact?view=help`. Las secciones de Bestsellers/colecciones van a salir vacías hasta que haya productos.
7. **Checkout**: Configuración → Checkout — repetir las opciones de OldyFans.
8. **Emails**: Configuración → Notificaciones — si OldyFans tiene plantillas personalizadas, pegarlas en `contenido/notificaciones/` y las adapto.
9. Publicar el tema.

## Apps que el tema espera
- **Loox Reviews** (bloque en la ficha de producto): si no se instala, el bloque simplemente no aparece.
- **Klaviyo** (está en OldyFans como app embed): no viaja con el tema.
