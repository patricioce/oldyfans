<?php
/**
 * Página de inicio.
 */
get_header();

$aguirre_total     = (int) aguirre_opt( 'opiniones_total' );
$aguirre_opiniones = aguirre_get_opiniones( 12 );
$aguirre_foto      = (int) aguirre_opt( 'foto' );
$aguirre_posts     = new WP_Query( array( 'post_type' => 'post', 'posts_per_page' => 3, 'ignore_sticky_posts' => true ) );
?>

<main id="contenido">
	<section class="hero">
		<div class="wrap">
			<div class="panel">
				<div class="hero-copy">
					<span class="kicker">Psicólogo · Terapia online</span>
					<h1><?php echo wp_kses( aguirre_opt( 'hero_titulo' ), array( 'em' => array(), 'strong' => array(), 'br' => array() ) ); ?></h1>
					<p><?php echo esc_html( aguirre_opt( 'hero_texto' ) ); ?></p>
					<div class="actions">
						<?php get_template_part( 'parts/whatsapp-button', null, array( 'label' => 'Consultar por WhatsApp' ) ); ?>
						<a class="btn btn-light" href="#online">Cómo es la terapia online</a>
					</div>
				</div>
				<aside class="first-card">
					<span class="tag">Primera entrevista</span>
					<h3>Un primer encuentro para conocernos</h3>
					<ul>
						<li>Me contás qué te trae a consulta</li>
						<li>Vemos si este espacio es para vos</li>
						<li>Por videollamada, desde tu casa</li>
					</ul>
				</aside>
			</div>
			<div class="creds">
				<span><?php echo aguirre_icon( 'birrete' ); // phpcs:ignore ?>Lic. en Psicología · UNLP</span>
				<?php if ( $aguirre_total ) : ?>
					<a href="#opiniones"><span><?php echo aguirre_icon( 'estrella' ); // phpcs:ignore ?><?php echo esc_html( number_format_i18n( $aguirre_total ) ); ?> opiniones en Doctoralia</span></a>
				<?php endif; ?>
				<span><?php echo aguirre_icon( 'mundo' ); // phpcs:ignore ?>Todo el país y el exterior</span>
			</div>
		</div>
	</section>

	<section class="band" id="temas">
		<div class="wrap topics-layout">
			<div class="head">
				<span class="kicker">Temas</span>
				<h2>¿Qué te trae a consulta?</h2>
				<p class="lead">La terapia cognitivo-conductual tiene muy buenos resultados en estos motivos de consulta. Los resaltados son los más frecuentes.</p>
			</div>
			<div>
				<div class="chips">
					<?php foreach ( aguirre_lines( 'temas_frecuentes' ) as $aguirre_tema ) : ?>
						<span class="chip hl"><?php echo esc_html( $aguirre_tema ); ?></span>
					<?php endforeach; ?>
					<?php foreach ( aguirre_lines( 'temas_otros' ) as $aguirre_tema ) : ?>
						<span class="chip"><?php echo esc_html( $aguirre_tema ); ?></span>
					<?php endforeach; ?>
				</div>
				<p class="topic-note">¿No ves lo que te pasa en la lista? <a href="<?php echo esc_url( aguirre_wa_url() ); ?>" target="_blank" rel="noopener">Escribime igual</a> y lo charlamos.</p>
			</div>
		</div>
	</section>

	<section class="band sand" id="metodo">
		<div class="wrap method">
			<div class="method-text">
				<span class="kicker">Cómo trabajo</span>
				<h2>Terapia cognitivo-conductual</h2>
			</div>
			<div class="method-text">
				<p>La TCC trabaja sobre cómo se conectan <strong>lo que pensás, lo que sentís y lo que hacés</strong>. Identificamos los patrones que te hacen daño y practicamos formas nuevas de responder.</p>
				<p>Es una terapia <strong>activa y con objetivos medibles</strong>. Sabés en qué estamos trabajando y cómo vas avanzando. Es el enfoque con más evidencia científica para la ansiedad, la depresión, las fobias y el TOC.</p>
			</div>
		</div>
	</section>

	<section class="band" id="online">
		<div class="wrap">
			<div class="head">
				<span class="kicker">Terapia online</span>
				<h2>Tu sesión, desde donde estés</h2>
				<p class="lead">Todas las sesiones son por videollamada. Mismo encuadre, mismo compromiso y la misma confidencialidad que en un consultorio.</p>
			</div>
			<div class="modes">
				<article class="mode dark">
					<div class="ico"><?php echo aguirre_icon( 'mundo' ); // phpcs:ignore ?></div>
					<h3>Sin moverte de tu casa</h3>
					<p>Atiendo a pacientes de todo el país y a argentinos que viven en el exterior. Sin viajes ni tiempos muertos.</p>
				</article>
				<article class="mode">
					<div class="ico"><?php echo aguirre_icon( 'video' ); // phpcs:ignore ?></div>
					<h3>Qué necesitás</h3>
					<p>Un celular o computadora, buena conexión y un lugar tranquilo donde puedas hablar con privacidad.</p>
				</article>
			</div>
		</div>
	</section>

	<?php if ( $aguirre_opiniones || $aguirre_total ) : ?>
	<section class="band sand" id="opiniones">
		<div class="wrap">
			<div class="reviews-top">
				<div class="counter">
					<span class="num"><?php echo esc_html( number_format_i18n( $aguirre_total ) ); ?></span>
					<span class="lbl">opiniones de pacientes</span>
					<span class="src">Publicadas en Doctoralia por pacientes con teléfono verificado</span>
					<?php if ( aguirre_opt( 'doctoralia_url' ) ) : ?>
						<a href="<?php echo esc_url( aguirre_opt( 'doctoralia_url' ) ); ?>" target="_blank" rel="noopener">Ver todas en Doctoralia ↗</a>
					<?php endif; ?>
				</div>
				<div class="reviews-intro">
					<span class="kicker">Opiniones</span>
					<h2>Lo que dicen quienes hicieron terapia conmigo</h2>
					<?php $aguirre_destacan = aguirre_lines( 'opiniones_destacan' ); ?>
					<p class="lead">Una selección de opiniones recientes de pacientes.<?php echo $aguirre_destacan ? ' Lo que más destacan:' : ''; ?></p>
					<?php if ( $aguirre_destacan ) : ?>
						<div class="mentions">
							<?php foreach ( $aguirre_destacan as $aguirre_item ) : ?>
								<span><?php echo esc_html( $aguirre_item ); ?></span>
							<?php endforeach; ?>
						</div>
					<?php endif; ?>
				</div>
			</div>
			<?php if ( $aguirre_opiniones ) : ?>
				<div class="reviews">
					<?php foreach ( $aguirre_opiniones as $aguirre_i => $aguirre_op ) : ?>
						<?php
						$aguirre_fecha = ucfirst( get_the_date( 'M Y', $aguirre_op ) );
						$aguirre_extra = $aguirre_i >= 6;
						?>
						<article class="review<?php echo $aguirre_extra ? ' more-review' : ''; ?>"<?php echo $aguirre_extra ? ' hidden' : ''; ?>>
							<span class="qmark" aria-hidden="true">“</span>
							<p><?php echo esc_html( wp_strip_all_tags( $aguirre_op->post_content ) ); ?></p>
							<footer>
								<b><?php echo esc_html( get_the_title( $aguirre_op ) ); ?></b>
								<span><?php echo esc_html( $aguirre_fecha . ( get_post_meta( $aguirre_op->ID, 'aguirre_online', true ) ? ' · Online' : '' ) ); ?></span>
							</footer>
						</article>
					<?php endforeach; ?>
				</div>
				<div class="reviews-more">
					<?php if ( count( $aguirre_opiniones ) > 6 ) : ?>
						<button class="btn btn-outline" id="more-reviews" aria-expanded="false">Ver más opiniones</button>
					<?php endif; ?>
					<?php if ( aguirre_opt( 'doctoralia_url' ) ) : ?>
						<a class="textlink" href="<?php echo esc_url( aguirre_opt( 'doctoralia_url' ) ); ?>" target="_blank" rel="noopener">Leer las <?php echo esc_html( number_format_i18n( $aguirre_total ) ); ?> en Doctoralia ↗</a>
					<?php endif; ?>
				</div>
			<?php endif; ?>
		</div>
	</section>
	<?php endif; ?>

	<section class="band" id="sobre-mi">
		<div class="wrap about">
			<div class="photo-wrap">
				<?php if ( $aguirre_foto ) : ?>
					<div class="photo"><?php echo wp_get_attachment_image( $aguirre_foto, 'medium_large', false, array( 'alt' => 'Lic. Marcelo César Aguirre', 'style' => 'width:100%;height:100%;object-fit:cover' ) ); ?></div>
				<?php else : ?>
					<div class="photo" role="img" aria-label="Espacio para la foto del profesional">
						<span>Foto del profesional</span>
						<?php echo aguirre_icon( 'persona' ); // phpcs:ignore ?>
					</div>
				<?php endif; ?>
			</div>
			<div class="about-text">
				<span class="kicker">Sobre mí</span>
				<h2>Marcelo César Aguirre</h2>
				<?php if ( aguirre_opt( 'sobre_frase' ) ) : ?>
					<p class="signature"><?php echo esc_html( aguirre_opt( 'sobre_frase' ) ); ?></p>
				<?php endif; ?>
				<?php echo wp_kses_post( wpautop( esc_html( aguirre_opt( 'sobre_texto' ) ) ) ); ?>
				<div class="badges">
					<div class="badge"><small>Formación</small><span>Lic. en Psicología, UNLP</span></div>
					<div class="badge"><small>Enfoque</small><span>Cognitivo-conductual</span></div>
					<div class="badge"><small>Matrícula</small><span><?php echo esc_html( aguirre_opt( 'matricula' ) ); ?></span></div>
				</div>
			</div>
		</div>
	</section>

	<?php if ( $aguirre_posts->have_posts() ) : ?>
	<section class="band sand" id="blog">
		<div class="wrap">
			<div class="head-row">
				<div class="head">
					<span class="kicker">Blog</span>
					<h2>Para leer entre sesiones</h2>
				</div>
				<a class="textlink" href="<?php echo esc_url( aguirre_blog_url() ); ?>">Ver todos los artículos →</a>
			</div>
			<div class="posts">
				<?php
				while ( $aguirre_posts->have_posts() ) {
					$aguirre_posts->the_post();
					get_template_part( 'parts/post-card' );
				}
				wp_reset_postdata();
				?>
			</div>
		</div>
	</section>
	<?php endif; ?>

	<section class="band" id="preguntas">
		<div class="wrap faq-layout">
			<div class="head">
				<span class="kicker">Preguntas frecuentes</span>
				<h2>Lo que suelen preguntarme</h2>
				<p class="lead">Si tenés otra duda, mandame un mensaje y te respondo.</p>
			</div>
			<div class="faq">
				<details open><summary>¿Cómo son las sesiones online?</summary><p>Son por videollamada. Antes de cada sesión te paso el link. Solo necesitás conexión a internet y un lugar tranquilo.</p></details>
				<details><summary>¿Funciona igual que ir a un consultorio?</summary><p>Sí. Para la mayoría de los motivos de consulta, los resultados de la terapia online son equivalentes a los de la presencial.</p></details>
				<details><summary>¿Atendés por obra social o prepaga?</summary><p>Atiendo de forma particular y entrego factura para que pidas el reintegro a tu obra social o prepaga. Consultame por los convenios vigentes.</p></details>
				<details><summary>¿Lo que hablamos es confidencial?</summary><p>Siempre. El secreto profesional está garantizado por el código de ética y por la ley de ejercicio profesional de la psicología.</p></details>
			</div>
		</div>
	</section>

	<section class="band" id="contacto" style="padding-top:0">
		<div class="wrap">
			<div class="contact-box">
				<div class="contact-intro">
					<span class="kicker">Contacto</span>
					<h2>Pedí tu primera entrevista</h2>
					<p>Escribime por WhatsApp y coordinamos día y horario. Te respondo en el día.</p>
					<?php get_template_part( 'parts/whatsapp-button', null, array( 'label' => 'Escribir por WhatsApp' ) ); ?>
					<div class="hours">
						<div><b>Días y horarios</b><span><?php echo esc_html( aguirre_opt( 'horarios' ) ); ?></span></div>
						<div><b>Modalidad</b><span>Online por videollamada</span></div>
					</div>
				</div>
				<div class="cards">
					<div class="c-item">
						<span class="ic"><?php echo aguirre_icon( 'telefono' ); // phpcs:ignore ?></span>
						<div><small>WhatsApp</small><span class="v" id="v-tel"><?php echo esc_html( aguirre_opt( 'whatsapp_visible' ) ); ?></span></div>
						<button class="copy" data-copy="v-tel">Copiar</button>
					</div>
					<?php if ( aguirre_opt( 'email' ) ) : ?>
						<div class="c-item">
							<span class="ic"><?php echo aguirre_icon( 'mail' ); // phpcs:ignore ?></span>
							<div><small>Mail</small><a class="v" id="v-mail" href="mailto:<?php echo esc_attr( antispambot( aguirre_opt( 'email' ) ) ); ?>"><?php echo esc_html( antispambot( aguirre_opt( 'email' ) ) ); ?></a></div>
							<button class="copy" data-copy="v-mail">Copiar</button>
						</div>
					<?php endif; ?>
					<?php if ( aguirre_opt( 'instagram_url' ) ) : ?>
						<a class="c-item" href="<?php echo esc_url( aguirre_opt( 'instagram_url' ) ); ?>" target="_blank" rel="noopener">
							<span class="ic"><?php echo aguirre_icon( 'instagram' ); // phpcs:ignore ?></span>
							<div><small>Instagram</small><span class="v"><?php echo esc_html( aguirre_opt( 'instagram_usuario' ) ); ?></span></div>
							<span class="go">Abrir ↗</span>
						</a>
					<?php endif; ?>
					<?php if ( aguirre_opt( 'facebook_url' ) ) : ?>
						<a class="c-item" href="<?php echo esc_url( aguirre_opt( 'facebook_url' ) ); ?>" target="_blank" rel="noopener">
							<span class="ic"><?php echo aguirre_icon( 'facebook' ); // phpcs:ignore ?></span>
							<div><small>Facebook</small><span class="v"><?php echo esc_html( aguirre_opt( 'facebook_nombre' ) ); ?></span></div>
							<span class="go">Abrir ↗</span>
						</a>
					<?php endif; ?>
				</div>
			</div>
		</div>
	</section>
</main>

<?php
get_footer();
