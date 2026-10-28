<!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip-link screen-reader-text" href="#contenido">Ir al contenido</a>

<div class="topbar" id="top">
	<div class="wrap">
		<div class="pill">
			<a class="mono" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="Inicio">
				<b>MA</b>
				<span>Lic. Marcelo Aguirre<small>Psicólogo · Terapia online</small></span>
			</a>
			<nav class="links" aria-label="Secciones">
				<?php
				if ( has_nav_menu( 'principal' ) ) {
					wp_nav_menu( array( 'theme_location' => 'principal', 'container' => false, 'depth' => 1, 'menu_id' => 'menu-escritorio' ) );
				} else {
					aguirre_menu_fallback();
				}
				?>
			</nav>
			<a class="cta-pill" href="<?php echo esc_url( aguirre_wa_url() ); ?>" target="_blank" rel="noopener">Pedir turno</a>
			<button class="burger" id="burger" aria-expanded="false" aria-controls="sheet" aria-label="Abrir menú">
				<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path id="burger-path" d="M4 8h16M4 16h16"/></svg>
			</button>
		</div>
		<nav class="sheet" id="sheet" aria-label="Menú">
			<?php
			if ( has_nav_menu( 'principal' ) ) {
				wp_nav_menu( array( 'theme_location' => 'principal', 'container' => false, 'depth' => 1, 'menu_id' => 'menu-celular' ) );
			} else {
				aguirre_menu_fallback( true );
			}
			?>
		</nav>
	</div>
</div>
