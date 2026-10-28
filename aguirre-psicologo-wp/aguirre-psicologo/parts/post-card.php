<?php
/**
 * Tarjeta de una entrada del blog.
 */
$aguirre_cat = aguirre_first_category();
?>
<a class="post" href="<?php the_permalink(); ?>">
	<?php echo aguirre_cover( get_the_ID() ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
	<div class="post-body">
		<?php if ( $aguirre_cat ) : ?>
			<span class="cat"><?php echo esc_html( $aguirre_cat->name ); ?></span>
		<?php endif; ?>
		<h3><?php the_title(); ?></h3>
		<?php if ( has_excerpt() || get_the_content() ) : ?>
			<p><?php echo esc_html( wp_strip_all_tags( get_the_excerpt() ) ); ?></p>
		<?php endif; ?>
		<span class="meta"><?php echo esc_html( aguirre_reading_time() ); ?> min de lectura</span>
	</div>
</a>
