<?php
/**
 * Aguirre Psicólogo: configuración del tema.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'AGUIRRE_VERSION', '1.0.0' );

require get_template_directory() . '/inc/helpers.php';
require get_template_directory() . '/inc/customizer.php';
require get_template_directory() . '/inc/opiniones.php';
require get_template_directory() . '/inc/contenido-inicial.php';

add_action( 'after_setup_theme', function () {
	load_theme_textdomain( 'aguirre', get_template_directory() . '/languages' );
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'align-wide' );
	add_image_size( 'aguirre-portada', 1280, 720, true );

	register_nav_menus( array(
		'principal' => __( 'Menú principal', 'aguirre' ),
	) );
} );

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style(
		'aguirre-fuentes',
		'https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Manrope:wght@400;500;600;700&display=swap',
		array(),
		null
	);
	wp_enqueue_style( 'aguirre-sitio', get_template_directory_uri() . '/assets/css/site.css', array( 'aguirre-fuentes' ), AGUIRRE_VERSION );
	wp_enqueue_script( 'aguirre-sitio', get_template_directory_uri() . '/assets/js/site.js', array(), AGUIRRE_VERSION, true );
} );

add_filter( 'wp_resource_hints', function ( $urls, $relation ) {
	if ( 'preconnect' === $relation ) {
		$urls[] = array( 'href' => 'https://fonts.gstatic.com', 'crossorigin' );
	}
	return $urls;
}, 10, 2 );

// Extracto corto y sin "[...]" para las tarjetas del blog.
add_filter( 'excerpt_length', function () {
	return 22;
} );
add_filter( 'excerpt_more', function () {
	return '…';
} );
