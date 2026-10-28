<?php
/**
 * Páginas sueltas (por ejemplo, política de privacidad).
 */
get_header();

while ( have_posts() ) :
	the_post();
	?>
<main id="contenido">
	<article <?php post_class(); ?>>
		<header class="wrap">
			<div class="article-head">
				<h1><?php the_title(); ?></h1>
			</div>
		</header>
		<div class="wrap">
			<div class="prose" style="padding-top:0;padding-bottom:clamp(64px,10vw,116px)">
				<?php the_content(); ?>
			</div>
		</div>
	</article>
</main>
	<?php
endwhile;

get_footer();
