<?php
/**
 * Datos editables desde Apariencia → Personalizar.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'customize_register', function ( $wp_customize ) {
	$defaults = aguirre_defaults();

	$add = function ( $section, $key, $label, $type = 'text', $description = '' ) use ( $wp_customize, $defaults ) {
		$sanitize = array(
			'text'     => 'sanitize_text_field',
			'textarea' => 'sanitize_textarea_field',
			'url'      => 'esc_url_raw',
			'email'    => 'sanitize_email',
			'number'   => 'absint',
			'html'     => 'aguirre_sanitize_inline_html',
		);
		$wp_customize->add_setting( $key, array(
			'default'           => $defaults[ $key ],
			'sanitize_callback' => $sanitize[ $type ],
		) );
		$wp_customize->add_control( $key, array(
			'section'     => $section,
			'label'       => $label,
			'description' => $description,
			'type'        => 'html' === $type ? 'textarea' : $type,
		) );
	};

	$wp_customize->add_panel( 'aguirre', array(
		'title'    => 'Sitio del Lic. Aguirre',
		'priority' => 30,
	) );

	$wp_customize->add_section( 'aguirre_contacto', array( 'title' => 'Contacto y redes', 'panel' => 'aguirre' ) );
	$add( 'aguirre_contacto', 'whatsapp', 'Número de WhatsApp', 'text', 'Con código de país y área, sin 0 ni 15. Ej: 5492215036216' );
	$add( 'aguirre_contacto', 'whatsapp_visible', 'Número como se muestra en la página' );
	$add( 'aguirre_contacto', 'whatsapp_mensaje', 'Mensaje precargado de WhatsApp', 'textarea' );
	$add( 'aguirre_contacto', 'email', 'Mail', 'email', 'Si lo dejás vacío, no se muestra.' );
	$add( 'aguirre_contacto', 'horarios', 'Días y horarios' );
	$add( 'aguirre_contacto', 'matricula', 'Matrícula' );
	$add( 'aguirre_contacto', 'instagram_url', 'Instagram (link)', 'url' );
	$add( 'aguirre_contacto', 'instagram_usuario', 'Instagram (usuario)' );
	$add( 'aguirre_contacto', 'facebook_url', 'Facebook (link)', 'url' );
	$add( 'aguirre_contacto', 'facebook_nombre', 'Facebook (nombre de la página)' );

	$wp_customize->add_section( 'aguirre_inicio', array( 'title' => 'Textos de la página de inicio', 'panel' => 'aguirre' ) );
	$add( 'aguirre_inicio', 'hero_titulo', 'Título principal', 'html', 'Lo que va entre <em> y </em> se muestra en cursiva y en color.' );
	$add( 'aguirre_inicio', 'hero_texto', 'Texto debajo del título', 'textarea' );
	$add( 'aguirre_inicio', 'temas_frecuentes', 'Temas más frecuentes (resaltados)', 'textarea', 'Uno por línea.' );
	$add( 'aguirre_inicio', 'temas_otros', 'Otros temas', 'textarea', 'Uno por línea.' );
	$add( 'aguirre_inicio', 'sobre_frase', 'Frase destacada de "Sobre mí"', 'textarea' );
	$add( 'aguirre_inicio', 'sobre_texto', 'Texto de "Sobre mí"', 'textarea', 'Dejá una línea en blanco entre párrafos.' );

	$wp_customize->add_setting( 'foto', array( 'default' => '', 'sanitize_callback' => 'absint' ) );
	$wp_customize->add_control( new WP_Customize_Media_Control( $wp_customize, 'foto', array(
		'section'   => 'aguirre_inicio',
		'label'     => 'Foto del profesional',
		'mime_type' => 'image',
	) ) );

	$wp_customize->add_section( 'aguirre_opiniones', array(
		'title'       => 'Opiniones',
		'panel'       => 'aguirre',
		'description' => 'Las opiniones se cargan en el menú "Opiniones" del panel. Acá van el total y los datos de Doctoralia.',
	) );
	$add( 'aguirre_opiniones', 'opiniones_total', 'Total de opiniones en Doctoralia', 'number' );
	$add( 'aguirre_opiniones', 'opiniones_destacan', 'Lo que más destacan los pacientes', 'textarea', 'Uno por línea.' );
	$add( 'aguirre_opiniones', 'doctoralia_url', 'Perfil de Doctoralia (link)', 'url' );
} );

/** Permite solo <em>, <strong> y <br> en el título principal. */
function aguirre_sanitize_inline_html( $value ) {
	return wp_kses( $value, array( 'em' => array(), 'strong' => array(), 'br' => array() ) );
}
