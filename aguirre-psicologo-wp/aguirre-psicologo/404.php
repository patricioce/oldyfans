<?php
/**
 * Página no encontrada.
 */
get_header();
?>
<main id="contenido">
	<section class="wrap notfound">
		<span class="kicker">Error 404</span>
		<h1 style="font-size:clamp(2.2rem,6vw,3.4rem)">No encontramos esta página</h1>
		<p class="lead">Puede que el link haya cambiado. Volvé al inicio o escribime directamente.</p>
		<div class="actions">
			<a class="btn btn-outline" href="<?php echo esc_url( home_url( '/' ) ); ?>">Ir al inicio</a>
			<?php get_template_part( 'parts/whatsapp-button', null, array( 'label' => 'Escribir por WhatsApp' ) ); ?>
		</div>
	</section>
</main>
<?php
get_footer();
