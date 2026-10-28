<?php
/**
 * Tipo de contenido "Opiniones": reseñas de pacientes que se muestran en la página de inicio.
 * El título es el nombre del paciente, el contenido es la opinión y la fecha de publicación
 * es la fecha de la reseña.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'init', function () {
	register_post_type( 'opinion', array(
		'labels'       => array(
			'name'               => 'Opiniones',
			'singular_name'      => 'Opinión',
			'add_new'            => 'Agregar opinión',
			'add_new_item'       => 'Agregar opinión',
			'edit_item'          => 'Editar opinión',
			'all_items'          => 'Todas las opiniones',
			'search_items'       => 'Buscar opiniones',
			'not_found'          => 'Todavía no hay opiniones.',
		),
		'public'       => false,
		'show_ui'      => true,
		'show_in_rest' => true,
		'menu_icon'    => 'dashicons-format-quote',
		'menu_position' => 21,
		'supports'     => array( 'title', 'editor', 'page-attributes' ),
	) );

	register_post_meta( 'opinion', 'aguirre_online', array(
		'type'          => 'boolean',
		'single'        => true,
		'default'       => false,
		'show_in_rest'  => true,
		'auth_callback' => function () {
			return current_user_can( 'edit_posts' );
		},
	) );
} );

add_filter( 'enter_title_here', function ( $text, $post ) {
	return 'opinion' === $post->post_type ? 'Nombre del paciente (ej: Gisela S.)' : $text;
}, 10, 2 );

// El editor de bloques sobra para un texto corto.
add_filter( 'use_block_editor_for_post_type', function ( $use, $post_type ) {
	return 'opinion' === $post_type ? false : $use;
}, 10, 2 );

add_action( 'add_meta_boxes_opinion', function () {
	add_meta_box( 'aguirre_opinion_datos', 'Datos de la opinión', function ( $post ) {
		wp_nonce_field( 'aguirre_opinion', 'aguirre_opinion_nonce' );
		$online = (bool) get_post_meta( $post->ID, 'aguirre_online', true );
		echo '<p><label><input type="checkbox" name="aguirre_online" value="1" ' . checked( $online, true, false ) . '> Fue una consulta online</label></p>';
		echo '<p class="description">La fecha de la opinión es la fecha de publicación (se cambia en el cuadro "Publicar").</p>';
		echo '<p class="description">Las 6 primeras se ven en la página de inicio; el resto aparece con "Ver más opiniones". Se ordenan por "Orden" (de menor a mayor) y después por fecha.</p>';
	}, 'opinion', 'side' );
} );

add_action( 'save_post_opinion', function ( $post_id ) {
	if ( ! isset( $_POST['aguirre_opinion_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['aguirre_opinion_nonce'] ), 'aguirre_opinion' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}
	update_post_meta( $post_id, 'aguirre_online', ! empty( $_POST['aguirre_online'] ) );
} );

/** Opiniones para la página de inicio. */
function aguirre_get_opiniones( $limit = 12 ) {
	return get_posts( array(
		'post_type'      => 'opinion',
		'posts_per_page' => $limit,
		'orderby'        => array( 'menu_order' => 'ASC', 'date' => 'DESC' ),
	) );
}
