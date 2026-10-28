<?php
/**
 * Listado del blog y de cada categoría (archive.php usa esta misma plantilla).
 */
get_header();

$aguirre_current = is_category() ? get_queried_object_id() : 0;
$aguirre_cats    = get_categories( array( 'hide_empty' => true ) );
?>

<main id="contenido">
	<section class="wrap page-head">
		<div class="head">
			<span class="kicker">Blog</span>
			<?php if ( is_category() ) : ?>
				<h1 style="font-size:clamp(2.4rem,6.5vw,3.8rem)"><?php single_cat_title(); ?></h1>
				<?php if ( category_description() ) : ?>
					<div class="lead"><?php echo wp_kses_post( category_description() ); ?></div>
				<?php endif; ?>
			<?php else : ?>
				<h1 style="font-size:clamp(2.4rem,6.5vw,3.8rem)">Para leer entre sesiones</h1>
				<p class="lead">Artículos breves sobre ansiedad, estado de ánimo, vínculos y herramientas de la terapia cognitivo-conductual para usar en el día a día.</p>
			<?php endif; ?>
		</div>
	</section>

	<section class="wrap" style="padding-bottom:clamp(64px,10vw,116px)">
		<?php if ( count( $aguirre_cats ) > 1 ) : ?>
			<nav class="filters" aria-label="Categorías">
				<a class="filter" href="<?php echo esc_url( aguirre_blog_url() ); ?>"<?php echo $aguirre_current ? '' : ' aria-current="page"'; ?>>Todas</a>
				<?php foreach ( $aguirre_cats as $aguirre_cat ) : ?>
					<a class="filter" href="<?php echo esc_url( get_category_link( $aguirre_cat ) ); ?>"<?php echo $aguirre_current === $aguirre_cat->term_id ? ' aria-current="page"' : ''; ?>><?php echo esc_html( $aguirre_cat->name ); ?></a>
				<?php endforeach; ?>
			</nav>
		<?php endif; ?>

		<?php if ( have_posts() ) : ?>
			<div class="posts">
				<?php
				while ( have_posts() ) {
					the_post();
					get_template_part( 'parts/post-card' );
				}
				?>
			</div>
			<?php
			the_posts_pagination( array(
				'mid_size'           => 1,
				'prev_text'          => '←',
				'next_text'          => '→',
				'screen_reader_text' => 'Más artículos',
			) );
			?>
		<?php else : ?>
			<p class="empty">Todavía no hay artículos publicados.</p>
		<?php endif; ?>
	</section>
</main>

<?php
get_footer();
