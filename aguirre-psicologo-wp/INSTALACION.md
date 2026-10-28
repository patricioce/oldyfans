# Sitio del Lic. Marcelo César Aguirre: instalación en WordPress

El sitio completo es un tema de WordPress (`aguirre-psicologo.zip`): página de inicio, opiniones, blog y artículos. Todo lo que cambia seguido se edita desde el panel, sin tocar código.

## 1. Instalar WordPress en SitiosHispanos

1. En el cPanel del dominio, abrí **Softaculous** (o el instalador de apps que tenga tu reseller) y elegí **WordPress**.
2. Elegí el dominio, idioma **Español (Argentina)**, y creá un usuario administrador.
3. Activá el certificado SSL (en cPanel: **SSL/TLS Status** o **Let's Encrypt**) para que el sitio abra con `https://`.

## 2. Subir y activar el tema

1. En WordPress: **Apariencia → Temas → Añadir nuevo → Subir tema**.
2. Elegí `aguirre-psicologo.zip`, **Instalar ahora** y después **Activar**.

Al activarlo por primera vez, el tema hace esto solo:

- Crea las páginas **Inicio** y **Blog** y las configura en **Ajustes → Lectura** (Inicio como portada, Blog como página de entradas).
- Carga las **12 opiniones** seleccionadas de Doctoralia en el menú **Opiniones**.
- Crea las categorías del blog (Ansiedad, Estado de ánimo, Vínculos, Sobre la terapia).
- Deja el artículo **"Ataques de pánico: qué son y qué hacer en el momento"** como **borrador**, para que Marcelo lo revise antes de publicarlo.

Si WordPress trae la entrada de ejemplo "¡Hola, mundo!", borrala desde **Entradas**.

## 3. Ajustes recomendados

- **Ajustes → Enlaces permanentes:** elegí **Nombre de la entrada**, así los artículos quedan como `/ataques-de-panico-que-son/`.
- **Ajustes → Generales:** zona horaria **Buenos Aires**.
- Plugins útiles (opcionales):
  - **Yoast SEO** o **Rank Math**: título y descripción para Google.
  - **UpdraftPlus**: copias de seguridad automáticas.

## 4. Qué se edita y dónde

| Qué | Dónde |
|---|---|
| WhatsApp, mail, horarios, matrícula, Instagram, Facebook | **Apariencia → Personalizar → Sitio del Lic. Aguirre → Contacto y redes** |
| Título principal, texto de bienvenida, temas, "Sobre mí" y foto | **Personalizar → Sitio del Lic. Aguirre → Textos de la página de inicio** |
| Total de opiniones de Doctoralia y "lo que más destacan" | **Personalizar → Sitio del Lic. Aguirre → Opiniones** |
| Opiniones de pacientes | Menú **Opiniones** del panel (título = nombre, texto = opinión, fecha de publicación = fecha de la reseña, casilla "Fue una consulta online") |
| Artículos del blog | **Entradas → Añadir nueva**. La "Imagen destacada" se usa como portada; si no tiene, se muestra un dibujo con los colores del sitio |
| Menú de arriba | Opcional: **Apariencia → Menús**, ubicación "Menú principal". Si no se arma ninguno, se usa el menú por defecto (Temas, Cómo trabajo, Opiniones, Blog, Preguntas) |

Notas:

- En la página de inicio se ven las 6 primeras opiniones y el resto aparece con **"Ver más opiniones"**. El orden se cambia con el campo **Orden** de cada opinión (de menor a mayor).
- El **mail** no se muestra hasta que lo cargues en el Personalizador.
- La sección **Blog** de la página de inicio aparece sola cuando hay al menos un artículo publicado.
