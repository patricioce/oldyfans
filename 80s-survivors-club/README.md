# 80s Survivors Club — clon de oldyfans.store

Destino: tienda Shopify **80ssurvivorsclub.com** (misma cuenta que OldyFans).
Tema origen: **BuildMyPOD v2.0.0**, publicado en OldyFans como "Cart Mobile Fix - 21 Oct 2026".
Idioma: inglés · Moneda: USD.

## Qué se clona
| Qué | Cómo | Estado |
|---|---|---|
| Tema (diseño + config de secciones) | Exportar zip → `tema/` en este repo → adaptar → subir | ⏳ falta el zip |
| Páginas (About, Contact, Reviews) | `contenido/paginas/` — copiar a Tienda online → Páginas | ✅ listo |
| Políticas (privacidad, reembolso, envíos, términos) | `contenido/politicas/` — copiar a Configuración → Políticas | ✅ listo, faltan emails |
| Menús principal y pie | `contenido/menus.md` | ✅ listo |
| Checkout y emails de notificación | Manual en el admin (no salen por el tema ni por API) | ⏳ ver abajo |
| Colecciones, imágenes, productos, apps | No por ahora | — |

Los textos ya tienen "OldyFans" → "80s Survivors Club" y el dominio cambiado.
Los emails de contacto quedaron como `[[EMAIL 80S SURVIVORS CLUB]]` para completar.
La página "Your Privacy Choices" la crea Shopify sola: no hay que copiarla.

## Pasos
1. **Exportar el tema**: en OldyFans → Tienda online → Temas → (tema publicado) → `…` → *Descargar archivo del tema*. Llega por mail; subir el zip a `tema/`.
2. Adaptar el tema (lo hace Claude): reemplazar textos/marca en `config/settings_data.json`, `locales/` y templates.
3. En 80s Survivors Club → Temas → *Agregar tema → Subir archivo zip*. Revisar en vista previa y publicar.
4. Crear páginas, políticas y menús con el contenido de `contenido/`.
5. **Checkout**: Configuración → Checkout — copiar opciones de OldyFans (campos, idioma, branding con el editor del tema).
6. **Emails**: Configuración → Notificaciones — copiar el código de cada plantilla personalizada de OldyFans cambiando "OldyFans" por "80s Survivors Club" (o pegarlas en `contenido/notificaciones/` y las adapto).
