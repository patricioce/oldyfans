<?php
/**
 * Contenido inicial: al activar el tema por primera vez crea las páginas "Inicio" y "Blog",
 * carga las opiniones seleccionadas de Doctoralia y deja un artículo de ejemplo en borrador.
 * No toca nada que ya exista.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'after_switch_theme', 'aguirre_contenido_inicial' );

function aguirre_contenido_inicial() {
	if ( get_option( 'aguirre_contenido_inicial' ) ) {
		return;
	}

	// Páginas y ajustes de lectura.
	if ( 'page' !== get_option( 'show_on_front' ) ) {
		$inicio = wp_insert_post( array(
			'post_type'   => 'page',
			'post_status' => 'publish',
			'post_title'  => 'Inicio',
			'post_name'   => 'inicio',
		) );
		$blog = wp_insert_post( array(
			'post_type'   => 'page',
			'post_status' => 'publish',
			'post_title'  => 'Blog',
			'post_name'   => 'blog',
		) );
		if ( $inicio && ! is_wp_error( $inicio ) && $blog && ! is_wp_error( $blog ) ) {
			update_option( 'show_on_front', 'page' );
			update_option( 'page_on_front', $inicio );
			update_option( 'page_for_posts', $blog );
		}
	}

	// Opiniones de pacientes (Doctoralia), en el orden en que se muestran.
	$existing = get_posts( array( 'post_type' => 'opinion', 'posts_per_page' => 1, 'post_status' => 'any', 'fields' => 'ids' ) );
	if ( ! $existing ) {
		$opiniones = array(
			array( 'Gisela S.', '2026-08-27', true, 'Un proceso que me ayuda a desatar nudos y a mirar las cosas desde otro lugar. Valoro su escucha y los ida y vuelta que abren la puerta a nuevas preguntas y reflexiones. Un espacio donde puedo pensarme, comprenderme y avanzar. Gracias Marcelo.' ),
			array( 'Cristian J.', '2025-12-04', false, 'Marcelo es un gran profesional. La verdad es que acudí a él en un estado de ansiedad increíble y, gracias a sus herramientas, me ayudó muchísimo. Destaco especialmente sus palabras justas y claras, que realmente marcan la diferencia. Súper recomendable.' ),
			array( 'Flor M.', '2025-10-20', true, 'Fui a verlo en agosto sintiendome mal, deprimida, esa primera consulta me ayudo a entender lo que me pasaba y empece un recorrido que me trajo hasta aca. Si bien no estoy recuperada totalmente me siento mejor y mas contenida, voy a aprendiendo a ver las cosas de forma diferente.' ),
			array( 'Agustín', '2025-07-17', true, 'Muy claro y empatico, con puntualidad, la consulta fue pausada, detallada. Quede conforme con la contencion que me dio, habia llegado angustiado a la consulta. Me sirvio hablar con el.' ),
			array( 'Josefina', '2025-06-27', true, 'Estaba bastante nerviosa y con dudas, pero este psicologo me trato muy bien, pude hablar mas de lo que creía. Parece el comienzo de una buena experiencia. Gracias Marcelo.' ),
			array( 'Walter B.', '2025-08-09', true, 'Se tomo el tiempo de hablar conmigo y se intereso en lo que me pasaba, muy claro y buena predisposición, 100 % recomendable.' ),
			array( 'Agustina B.', '2026-08-07', true, 'Gracias Marcelo por tu profesionalismo y escucharme. Excelente profesional' ),
			array( 'María Cristina D.', '2025-07-31', true, 'Me atendio bien, con calidez pero tambien con el profesionalismo de alguien abocado a la salud mental. Muchas gracias Marcelo.' ),
			array( 'Juan Francisco', '2025-09-22', false, 'Voy desde que empezo el año, es un buen lugar para hablar de mi ansiedad y de mis proyectos, siempre estuve comodo. Gracias Marcelo' ),
			array( 'Verónica V.', '2025-06-30', true, 'Un buen psicologo, diferente de los que tuve antes, puede ser porque la terapia es distinta. Muy clara la explicación de la terapia.' ),
			array( 'Lizi', '2025-09-03', true, 'Me atendio bien en este momento de decisiones difíciles que debo tomar. Me parecio muy amable, parece que conoce su oficio. Un buen profesional, muy recomendable.' ),
			array( 'Rosana', '2025-07-20', false, 'Se tomo su tiempo para atenderme, me dejo hablar y recien despues dijo algo que me parecio muy preciso y profesional. Agradezco el tiempo que me dedico.' ),
		);
		foreach ( $opiniones as $i => $o ) {
			$id = wp_insert_post( array(
				'post_type'    => 'opinion',
				'post_status'  => 'publish',
				'post_title'   => $o[0],
				'post_content' => $o[3],
				'post_date'    => $o[1] . ' 12:00:00',
				'menu_order'   => $i + 1,
			) );
			if ( $id && ! is_wp_error( $id ) ) {
				update_post_meta( $id, 'aguirre_online', $o[2] );
			}
		}
	}

	// Artículo de ejemplo, en borrador para que el profesional lo revise antes de publicarlo.
	$cat = term_exists( 'Ansiedad', 'category' );
	if ( ! $cat ) {
		$cat = wp_insert_term( 'Ansiedad', 'category' );
	}
	$cat_id = is_array( $cat ) ? (int) $cat['term_id'] : 0;
	foreach ( array( 'Estado de ánimo', 'Vínculos', 'Sobre la terapia' ) as $name ) {
		if ( ! term_exists( $name, 'category' ) ) {
			wp_insert_term( $name, 'category' );
		}
	}
	wp_insert_post( array(
		'post_type'     => 'post',
		'post_status'   => 'draft',
		'post_title'    => 'Ataques de pánico: qué son y qué hacer en el momento',
		'post_excerpt'  => 'Por qué el cuerpo reacciona así y tres recursos para atravesar una crisis.',
		'post_category' => $cat_id ? array( $cat_id ) : array(),
		'post_content'  => aguirre_articulo_ejemplo(),
	) );

	update_option( 'aguirre_contenido_inicial', 1 );
}

function aguirre_articulo_ejemplo() {
	$p  = function ( $html ) {
		return "<!-- wp:paragraph -->\n<p>$html</p>\n<!-- /wp:paragraph -->\n\n";
	};
	$h2 = function ( $text ) {
		return "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">$text</h2>\n<!-- /wp:heading -->\n\n";
	};
	$list = function ( $items, $ordered = false ) {
		$tag   = $ordered ? 'ol' : 'ul';
		$attrs = $ordered ? ' {"ordered":true}' : '';
		$out   = "<!-- wp:list$attrs -->\n<$tag class=\"wp-block-list\">";
		foreach ( $items as $item ) {
			$out .= "<!-- wp:list-item -->\n<li>$item</li>\n<!-- /wp:list-item -->";
		}
		return $out . "</$tag>\n<!-- /wp:list -->\n\n";
	};

	return $p( 'Te late el corazón muy rápido, te falta el aire, sentís un hormigueo en las manos y la certeza de que algo grave está por pasar. Quien tuvo un ataque de pánico lo describe casi siempre igual: <strong>“pensé que me moría”</strong>.' )
		. $p( 'Es una experiencia muy intensa, pero tiene explicación y tiene tratamiento. Entender qué pasa en el cuerpo es el primer paso para dejar de tenerle miedo.' )
		. $h2( 'Qué es un ataque de pánico' )
		. $p( 'Es una descarga repentina de miedo intenso que llega a su pico en pocos minutos. El cuerpo activa su sistema de alarma, el mismo que nos prepara para escapar de un peligro, aunque no haya ningún peligro real.' )
		. $p( 'Los síntomas más frecuentes son:' )
		. $list( array(
			'Palpitaciones o taquicardia',
			'Sensación de falta de aire o de ahogo',
			'Mareo, temblores o sudoración',
			'Opresión en el pecho',
			'Sensación de irrealidad o de estar “fuera” de uno mismo',
			'Miedo a perder el control, a volverse loco o a morir',
		) )
		. $p( '<strong>Importante:</strong> si es la primera vez que te pasa, consultá a un médico para descartar otras causas. Ante una emergencia, llamá al 107 o acercate a la guardia más cercana.' )
		. $h2( 'Tres recursos para el momento de la crisis' )
		. $list( array(
			'<strong>Respirá lento, alargando la exhalación.</strong> Inhalá por la nariz contando hasta 4 y soltá el aire por la boca contando hasta 6. Repetilo varias veces.',
			'<strong>Ponele nombre a lo que pasa.</strong> Decite: “Esto es un ataque de pánico. Es muy desagradable, pero no es peligroso y va a pasar”.',
			'<strong>Volvé al presente con los sentidos.</strong> Buscá 5 cosas que puedas ver, 4 que puedas tocar, 3 que puedas escuchar, 2 que puedas oler y 1 que puedas saborear.',
		), true )
		. $h2( 'Por qué vuelven y cómo se tratan' )
		. $p( 'Después de una crisis es común empezar a tenerle miedo al próximo ataque y evitar lugares o situaciones. Ese “miedo al miedo” es justamente lo que mantiene el problema.' )
		. $p( 'La terapia cognitivo-conductual es el tratamiento con más evidencia para el trastorno de pánico. En sesión aprendemos a leer las señales del cuerpo sin interpretarlas como peligro, y a recuperar de a poco los espacios que se dejaron de lado.' );
}
