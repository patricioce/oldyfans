<?php
/**
 * Artículo del blog.
 */
get_header();

while ( have_posts() ) :
	the_post();
	$aguirre_cat = aguirre_first_category();
	?>
<main id="contenido">
	<article <?php post_class(); ?>>
		<header class="wrap">
			<div class="article-head">
				<nav class="crumbs" aria-label="Ruta">
					<a href="<?php echo esc_url( home_url( '/' ) ); ?>">Inicio</a><span>/</span>
					<a href="<?php echo esc_url( aguirre_blog_url() ); ?>">Blog</a>
					<?php if ( $aguirre_cat ) : ?>
						<span>/</span><a href="<?php echo esc_url( get_category_link( $aguirre_cat ) ); ?>"><?php echo esc_html( $aguirre_cat->name ); ?></a>
					<?php endif; ?>
				</nav>
				<?php if ( $aguirre_cat ) : ?>
					<span class="cat"><?php echo esc_html( $aguirre_cat->name ); ?></span>
				<?php endif; ?>
				<h1><?php the_title(); ?></h1>
				<div class="byline"><b>MA</b><div><strong>Lic. Marcelo César Aguirre</strong><?php echo esc_html( get_the_date() ); ?> · <?php echo esc_html( aguirre_reading_time() ); ?> min de lectura</div></div>
			</div>
		</header>

		<div class="wrap article-cover">
			<?php echo aguirre_cover( get_the_ID() ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
		</div>

		<div class="wrap">
			<div class="prose">
				<?php the_content(); ?>
			</div>

			<aside class="author-box">
				<b>MA</b>
				<div>
					<strong>Lic. Marcelo César Aguirre</strong>
					<p>Psicólogo (UNLP) especializado en terapia cognitivo-conductual. Atiendo online a adultos con ansiedad, pánico y depresión.</p>
					<?php get_template_part( 'parts/whatsapp-button', null, array( 'label' => 'Consultar por WhatsApp' ) ); ?>
				</div>
			</aside>
		</div>
	</article>

	<?php
	$aguirre_related = new WP_Query( array(
		'post_type'           => 'post',
		'posts_per_page'      => 3,
		'post__not_in'        => array( get_the_ID() ),
		'ignore_sticky_posts' => true,
	) );
	if ( $aguirre_related->have_posts() ) :
		?>
	<section class="band">
		<div class="wrap">
			<div class="head-row">
				<div class="head"><span class="kicker">Seguí leyendo</span><h2>Otros artículos</h2></div>
				<a class="textlink" href="<?php echo esc_url( aguirre_blog_url() ); ?>">Ver el blog →</a>
			</div>
			<div class="posts">
				<?php
				while ( $aguirre_related->have_posts() ) {
					$aguirre_related->the_post();
					get_template_part( 'parts/post-card' );
				}
				wp_reset_postdata();
				?>
			</div>
		</div>
	</section>
	<?php endif; ?>
</main>
	<?php
endwhile;

get_footer();
