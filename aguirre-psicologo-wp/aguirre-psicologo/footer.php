<footer class="site-foot">
	<div class="wrap foot">
		<span>© <?php echo esc_html( wp_date( 'Y' ) ); ?> Lic. Marcelo César Aguirre · Psicólogo · <?php echo esc_html( aguirre_opt( 'matricula' ) ); ?></span>
		<span>
			<a href="<?php echo esc_url( aguirre_blog_url() ); ?>">Blog</a>
			<?php if ( aguirre_opt( 'instagram_url' ) ) : ?> · <a href="<?php echo esc_url( aguirre_opt( 'instagram_url' ) ); ?>" target="_blank" rel="noopener">Instagram</a><?php endif; ?>
			<?php if ( aguirre_opt( 'facebook_url' ) ) : ?> · <a href="<?php echo esc_url( aguirre_opt( 'facebook_url' ) ); ?>" target="_blank" rel="noopener">Facebook</a><?php endif; ?>
			<?php if ( aguirre_opt( 'doctoralia_url' ) ) : ?> · <a href="<?php echo esc_url( aguirre_opt( 'doctoralia_url' ) ); ?>" target="_blank" rel="noopener">Doctoralia</a><?php endif; ?>
		</span>
	</div>
</footer>

<div class="actionbar">
	<a class="wa" href="<?php echo esc_url( aguirre_wa_url() ); ?>" target="_blank" rel="noopener">
		<?php echo aguirre_icon( 'whatsapp' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
		Pedir turno por WhatsApp
	</a>
	<?php if ( is_front_page() ) : ?>
		<a class="more" href="#contacto">Contacto</a>
	<?php else : ?>
		<a class="more" href="<?php echo esc_url( home_url( '/' ) ); ?>">Inicio</a>
	<?php endif; ?>
</div>

<?php wp_footer(); ?>
</body>
</html>
