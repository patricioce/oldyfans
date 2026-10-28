<?php
/**
 * Funciones de ayuda usadas en las plantillas.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Valores por defecto de los datos editables desde Apariencia → Personalizar. */
function aguirre_defaults() {
	return array(
		'whatsapp'         => '5492215036216',
		'whatsapp_visible' => '+54 9 221 503-6216',
		'whatsapp_mensaje' => 'Hola Marcelo, vi tu página y quería consultar por una primera entrevista.',
		'email'            => '',
		'matricula'        => 'M.P. 53.561',
		'horarios'         => 'A coordinar por WhatsApp',
		'instagram_url'    => 'https://www.instagram.com/dialogoensesion/',
		'instagram_usuario' => '@dialogoensesion',
		'facebook_url'     => 'https://www.facebook.com/psicologosenlaplata',
		'facebook_nombre'  => 'Psicólogos en La Plata',
		'doctoralia_url'   => 'https://www.doctoraliar.com/perfil/marcelo-cesar-aguirre',
		'opiniones_total'  => '437',
		'opiniones_destacan' => "Dedicación durante la sesión\nExplicaciones detalladas\nPuntualidad",
		'hero_titulo'      => 'Volver a sentirte <em>en eje</em> empieza con una conversación.',
		'hero_texto'       => 'Terapia cognitivo-conductual online para adultos. Trabajamos sobre lo que te preocupa hoy, con objetivos claros y herramientas concretas, desde donde estés.',
		'temas_frecuentes' => "Ansiedad\nAtaques de pánico\nDepresión",
		'temas_otros'      => "Estrés y burnout\nAutoestima\nFobias\nTOC\nInsomnio\nDuelos\nSeparaciones\nProblemas de pareja\nDependencia emocional",
		'sobre_frase'      => 'Mi trabajo es que lo que hablamos en sesión se convierta en cambios que notes en tu vida.',
		'sobre_texto'      => "Soy licenciado en Psicología por la Universidad Nacional de La Plata, con formación en terapia cognitivo-conductual. Me dedico a la psicología clínica de adultos, sobre todo a la ansiedad y la depresión, y atiendo online a pacientes de todo el país.\n\nMe gusta una terapia cercana y sin vueltas: entender qué te pasa y, sobre todo, encontrar qué podés hacer hoy para sentirte mejor.",
		'foto'             => '',
	);
}

/** Lee un dato del Personalizador con su valor por defecto. */
function aguirre_opt( $key ) {
	$defaults = aguirre_defaults();
	return get_theme_mod( $key, isset( $defaults[ $key ] ) ? $defaults[ $key ] : '' );
}

/** Convierte un textarea en lista, una entrada por línea. */
function aguirre_lines( $key ) {
	return array_values( array_filter( array_map( 'trim', explode( "\n", (string) aguirre_opt( $key ) ) ) ) );
}

/** Link de WhatsApp con el mensaje precargado. */
function aguirre_wa_url() {
	$number = preg_replace( '/\D+/', '', (string) aguirre_opt( 'whatsapp' ) );
	return 'https://wa.me/' . $number . '?text=' . rawurlencode( (string) aguirre_opt( 'whatsapp_mensaje' ) );
}

/** Link a una sección de la página de inicio. */
function aguirre_anchor( $id ) {
	return home_url( '/#' . $id );
}

/** Íconos SVG en línea. */
function aguirre_icon( $name ) {
	$icons = array(
		'whatsapp'  => '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5 5.1-1.3A9.9 9.9 0 1 0 12.04 2zm0 18.1a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3a8.2 8.2 0 1 1 6.9 3.8zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.4-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.2-.2-.5-.3z"/></svg>',
		'birrete'   => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/></svg>',
		'estrella'  => '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9 6.8 19.6l1-5.8L3.5 9.7l5.9-.9z"/></svg>',
		'mundo'     => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>',
		'video'     => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="13" height="14" rx="2"/><path d="m16 10 5-3v10l-5-3"/></svg>',
		'telefono'  => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 3h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 12l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>',
		'mail'      => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
		'instagram' => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
		'facebook'  => '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M15.5 8H14a2 2 0 0 0-2 2v11M9.5 13h5"/></svg>',
		'persona'   => '<svg viewBox="0 0 200 180" fill="currentColor" aria-hidden="true"><circle cx="100" cy="62" r="40"/><path d="M20 180c0-50 36-78 80-78s80 28 80 78z"/></svg>',
	);
	return isset( $icons[ $name ] ) ? $icons[ $name ] : '';
}

/** Portada de una entrada: imagen destacada o, si no tiene, círculos de color. */
function aguirre_cover( $post_id = null, $class = '' ) {
	$post_id = $post_id ? $post_id : get_the_ID();
	$alt     = ( $post_id % 2 ) ? ' alt' : '';
	$html    = '<div class="cover' . $alt . ( $class ? ' ' . esc_attr( $class ) : '' ) . '">';
	if ( has_post_thumbnail( $post_id ) ) {
		$html .= get_the_post_thumbnail( $post_id, 'aguirre-portada', array( 'alt' => '' ) );
	} else {
		$layouts = array(
			array( 230, 40, 90, 90, 150, 70, 160, 90, 30 ),
			array( 60, 40, 80, 250, 140, 90, 170, 60, 24 ),
			array( 280, 30, 60, 160, 200, 120, 60, 50, 36 ),
			array( 240, 60, 70, 70, 140, 100, 290, 160, 30 ),
		);
		$l     = $layouts[ $post_id % count( $layouts ) ];
		$html .= sprintf(
			'<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><circle class="c1" cx="%d" cy="%d" r="%d"/><circle class="c2" cx="%d" cy="%d" r="%d"/><circle class="c3" cx="%d" cy="%d" r="%d"/></svg>',
			$l[0], $l[1], $l[2], $l[3], $l[4], $l[5], $l[6], $l[7], $l[8]
		);
	}
	return $html . '</div>';
}

/** Minutos de lectura estimados. */
function aguirre_reading_time( $post_id = null ) {
	$text  = trim( wp_strip_all_tags( get_post_field( 'post_content', $post_id ? $post_id : get_the_ID() ) ) );
	$words = '' === $text ? 0 : count( preg_split( '/\s+/u', $text ) );
	return max( 1, (int) round( $words / 200 ) );
}

/** Primera categoría de la entrada. */
function aguirre_first_category( $post_id = null ) {
	$cats = get_the_category( $post_id );
	return $cats ? $cats[0] : null;
}

/** Menú de respaldo si todavía no se armó uno en Apariencia → Menús. */
function aguirre_menu_fallback( $mobile = false ) {
	$items = array(
		array( aguirre_anchor( 'temas' ), 'Temas' ),
		array( aguirre_anchor( 'metodo' ), 'Cómo trabajo' ),
	);
	if ( $mobile ) {
		$items[] = array( aguirre_anchor( 'online' ), 'Terapia online' );
	}
	$items[] = array( aguirre_anchor( 'opiniones' ), 'Opiniones' );
	if ( $mobile ) {
		$items[] = array( aguirre_anchor( 'sobre-mi' ), 'Sobre mí' );
	}
	$blog    = get_option( 'page_for_posts' ) ? get_permalink( get_option( 'page_for_posts' ) ) : home_url( '/?post_type=post' );
	$items[] = array( $blog, 'Blog' );
	$items[] = array( aguirre_anchor( 'preguntas' ), 'Preguntas' );
	if ( $mobile ) {
		$items[] = array( aguirre_anchor( 'contacto' ), 'Contacto' );
	}
	foreach ( $items as $item ) {
		printf( '<a href="%s">%s</a>', esc_url( $item[0] ), esc_html( $item[1] ) );
	}
}

/** URL del listado del blog. */
function aguirre_blog_url() {
	$page = get_option( 'page_for_posts' );
	return $page ? get_permalink( $page ) : home_url( '/' );
}
