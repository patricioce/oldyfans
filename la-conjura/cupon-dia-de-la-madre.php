<?php
/**
 * Plugin Name: La Conjura — Cupón en checkout + popup Día de la Madre
 * Description: Agrega el campo de cupón al checkout, crea el cupón MAMÁ (15% OFF) y muestra a los 3 segundos un popup que pide el mail y aplica el cupón automáticamente.
 * Version: 1.0.0
 * Author: La Conjura
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'LC_MAMA_CODE', 'mamá' );            // WooCommerce guarda los códigos en minúscula.
define( 'LC_MAMA_LABEL', 'MAMÁ' );
define( 'LC_MAMA_PERCENT', 15 );
define( 'LC_MAMA_COOKIE', 'lc_cupon_mama' );
define( 'LC_MAMA_EMAIL_COOKIE', 'lc_cupon_mama_email' );
define( 'LC_MAMA_EMAILS_OPT', 'lc_mama_emails' );

/* ===================================================================
 * 1. Cupones habilitados + campo de cupón dentro del checkout
 * =================================================================== */

// Fuerza "Habilitar el uso de cupones" aunque esté apagado en los ajustes.
add_filter( 'woocommerce_coupons_enabled', '__return_true' );

// Saca el aviso desplegable "¿Tenés un cupón?" de arriba del checkout:
// lo reemplazamos por un campo a la vista, junto al resumen del pedido.
add_action( 'init', function () {
	remove_action( 'woocommerce_before_checkout_form', 'woocommerce_checkout_coupon_form', 10 );
} );

// Entre la tabla del pedido (10) y los medios de pago (20). Queda fuera de
// los fragmentos que WooCommerce refresca, así que no se borra al recalcular.
add_action( 'woocommerce_checkout_order_review', function () {
	?>
	<div class="lc-coupon" id="lc-coupon">
		<label for="lc-coupon-code" class="lc-coupon__label">¿Tenés un cupón de descuento?</label>
		<div class="lc-coupon__row">
			<input type="text" id="lc-coupon-code" class="input-text lc-coupon__input" placeholder="Código del cupón" autocomplete="off" autocapitalize="characters">
			<button type="button" class="button lc-coupon__apply">Aplicar</button>
		</div>
		<div class="lc-coupon__msg" aria-live="polite"></div>
	</div>
	<?php
}, 15 );

add_action( 'wp_footer', function () {
	if ( ! function_exists( 'is_checkout' ) || ! is_checkout() || is_order_received_page() ) {
		return;
	}
	?>
	<script>
	jQuery(function ($) {
		if (typeof wc_checkout_params === 'undefined') return;
		function aplicar() {
			var $box = $('#lc-coupon'), $in = $box.find('.lc-coupon__input'), $msg = $box.find('.lc-coupon__msg');
			var code = $.trim($in.val());
			if (!code) { $in.trigger('focus'); return; }
			$box.addClass('is-loading');
			$.post(wc_checkout_params.wc_ajax_url.toString().replace('%%endpoint%%', 'apply_coupon'), {
				security: wc_checkout_params.apply_coupon_nonce,
				coupon_code: code,
				billing_email: $('#billing_email').val() || ''
			}).done(function (html) {
				$msg.html(html);
				if (html.indexOf('woocommerce-error') === -1) $in.val('');
				$(document.body).trigger('applied_coupon_in_checkout', [code]);
				$(document.body).trigger('update_checkout', { update_shipping_method: false });
			}).always(function () { $box.removeClass('is-loading'); });
		}
		$(document.body).on('click', '.lc-coupon__apply', aplicar);
		$(document.body).on('keydown', '.lc-coupon__input', function (e) {
			// Enter acá no tiene que enviar el pedido.
			if (e.key === 'Enter') { e.preventDefault(); aplicar(); }
		});
		$(document.body).on('removed_coupon_in_checkout', function () { $('#lc-coupon .lc-coupon__msg').empty(); });
	});
	</script>
	<?php
} );

// "Cupón: MAMÁ" en vez de "Cupón: mamá" en carrito y checkout.
add_filter( 'woocommerce_cart_totals_coupon_label', function ( $label, $coupon ) {
	return 'Cupón: ' . mb_strtoupper( $coupon->get_code(), 'UTF-8' );
}, 10, 2 );

// Quien escriba "MAMA" sin tilde también recibe el descuento.
add_filter( 'woocommerce_coupon_code', function ( $code ) {
	return 'mama' === $code ? LC_MAMA_CODE : $code;
}, 20 );

/* ===================================================================
 * 2. Cupón MAMÁ: se crea solo la primera vez
 * =================================================================== */

add_action( 'init', function () {
	if ( get_option( 'lc_mama_coupon_created' ) || ! class_exists( 'WC_Coupon' ) ) {
		return;
	}
	if ( ! wc_get_coupon_id_by_code( LC_MAMA_CODE ) ) {
		$coupon = new WC_Coupon();
		$coupon->set_code( LC_MAMA_CODE );
		$coupon->set_description( 'Popup Día de la Madre — ' . LC_MAMA_PERCENT . '% OFF' );
		$coupon->set_discount_type( 'percent' );
		$coupon->set_amount( LC_MAMA_PERCENT );
		$coupon->set_individual_use( true );
		$coupon->save();
	}
	update_option( 'lc_mama_coupon_created', 1, false );
}, 20 );

/* ===================================================================
 * 3. Asignación automática del cupón a quien dejó su mail
 * =================================================================== */

function lc_mama_has_cookie() {
	return ! empty( $_COOKIE[ LC_MAMA_COOKIE ] );
}

function lc_mama_maybe_apply() {
	if ( ! function_exists( 'WC' ) || ! WC()->cart || WC()->cart->is_empty() ) {
		return;
	}
	if ( WC()->cart->has_discount( LC_MAMA_CODE ) ) {
		return;
	}
	// Si la persona lo quitó a mano, o ya usa otro cupón, no insistimos.
	if ( WC()->session && WC()->session->get( 'lc_mama_removed' ) ) {
		return;
	}
	if ( WC()->cart->get_applied_coupons() ) {
		return;
	}
	WC()->cart->apply_coupon( LC_MAMA_CODE );
}

// Antes de mostrar carrito o checkout (así los totales ya salen con descuento).
add_action( 'template_redirect', function () {
	if ( lc_mama_has_cookie() && ( is_cart() || is_checkout() ) && ! is_order_received_page() ) {
		lc_mama_maybe_apply();
	}
} );

// Al agregar un producto al carrito.
add_action( 'woocommerce_add_to_cart', function () {
	if ( lc_mama_has_cookie() ) {
		lc_mama_maybe_apply();
	}
}, 20 );

add_action( 'woocommerce_removed_coupon', function ( $code ) {
	if ( LC_MAMA_CODE === $code && WC()->session ) {
		WC()->session->set( 'lc_mama_removed', true );
	}
} );

// El mail del popup aparece ya cargado en el checkout.
add_filter( 'woocommerce_checkout_get_value', function ( $value, $input ) {
	if ( 'billing_email' === $input && null === $value && ! is_user_logged_in() && ! empty( $_COOKIE[ LC_MAMA_EMAIL_COOKIE ] ) ) {
		$email = sanitize_email( wp_unslash( $_COOKIE[ LC_MAMA_EMAIL_COOKIE ] ) );
		return is_email( $email ) ? $email : $value;
	}
	return $value;
}, 10, 2 );

/* ===================================================================
 * 4. Recepción del mail del popup
 * =================================================================== */

// Sin nonce a propósito: con caché de páginas el nonce vence y el formulario
// dejaría de andar. El endpoint solo guarda un mail válido.
add_action( 'wp_ajax_lc_mama_signup', 'lc_mama_signup' );
add_action( 'wp_ajax_nopriv_lc_mama_signup', 'lc_mama_signup' );

function lc_mama_signup() {
	// Trampa para bots: campo oculto que una persona nunca completa.
	if ( ! empty( $_POST['website'] ) ) {
		wp_send_json_success( array( 'code' => LC_MAMA_LABEL ) );
	}

	$email = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) ) : '';
	if ( ! is_email( $email ) ) {
		wp_send_json_error( array( 'message' => 'Revisá el mail, parece que tiene un error.' ), 400 );
	}

	$emails = get_option( LC_MAMA_EMAILS_OPT, array() );
	if ( ! is_array( $emails ) ) {
		$emails = array();
	}
	$key = strtolower( $email );
	if ( ! isset( $emails[ $key ] ) ) {
		$emails[ $key ] = current_time( 'mysql' );
		update_option( LC_MAMA_EMAILS_OPT, $emails, false );
	}

	$expires = time() + 30 * DAY_IN_SECONDS;
	$secure  = is_ssl();
	setcookie( LC_MAMA_COOKIE, '1', $expires, COOKIEPATH ?: '/', COOKIE_DOMAIN, $secure, true );
	setcookie( LC_MAMA_EMAIL_COOKIE, $email, $expires, COOKIEPATH ?: '/', COOKIE_DOMAIN, $secure, true );
	$_COOKIE[ LC_MAMA_COOKIE ] = '1';

	// Si ya tiene productos en el carrito, el cupón queda aplicado ahora mismo.
	if ( function_exists( 'WC' ) && WC()->session ) {
		WC()->session->set( 'lc_mama_removed', false );
	}
	lc_mama_maybe_apply();

	do_action( 'lc_mama_signup', $email );

	wp_send_json_success( array( 'code' => LC_MAMA_LABEL ) );
}

/* ===================================================================
 * 5. Popup (aparece a los 3 segundos)
 * =================================================================== */

add_action( 'wp_footer', function () {
	if ( is_admin() || ( function_exists( 'is_checkout' ) && ( is_checkout() || is_cart() ) ) ) {
		return;
	}
	?>
	<div class="lc-mama" id="lc-mama" role="dialog" aria-modal="true" aria-labelledby="lc-mama-title" hidden>
		<div class="lc-mama__backdrop" data-lc-close></div>
		<div class="lc-mama__box">
			<button type="button" class="lc-mama__close" aria-label="Cerrar" data-lc-close>&times;</button>

			<form class="lc-mama__step lc-mama__step--form" novalidate>
				<h2 id="lc-mama-title" class="lc-mama__title">Déjanos tu mail y obtené un <strong>15% OFF</strong> por el DÍA DE LA MADRE</h2>
				<label for="lc-mama-email" class="screen-reader-text">Tu mail</label>
				<input type="email" id="lc-mama-email" name="email" class="lc-mama__input" placeholder="tu@mail.com" autocomplete="email" required>
				<input type="text" name="website" tabindex="-1" autocomplete="off" class="lc-mama__hp" aria-hidden="true">
				<button type="submit" class="button lc-mama__cta">Lo quiero</button>
				<p class="lc-mama__error" aria-live="polite"></p>
			</form>

			<div class="lc-mama__step lc-mama__step--done" hidden>
				<p class="lc-mama__title">¡Gracias! Tu vieja se va a poner re contenta</p>
				<div class="lc-mama__code">
					<span>CÓDIGO: <strong><?php echo esc_html( LC_MAMA_LABEL ); ?></strong></span>
					<button type="button" class="button lc-mama__copy">Copiar</button>
				</div>
				<p class="lc-mama__note">Ya quedó aplicado a tu compra.</p>
			</div>
		</div>
	</div>
	<script>
	(function () {
		var KEY = 'lc_mama_popup', DELAY = 3000, REPEAT_DAYS = 3;
		var box = document.getElementById('lc-mama');
		if (!box) return;

		function get() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } }
		function set(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} }

		var state = get();
		if (document.cookie.indexOf('<?php echo esc_js( LC_MAMA_COOKIE ); ?>=') !== -1) return; // Ya se suscribió.
		if (state && state.done) return;
		if (state && state.closed && Date.now() - state.closed < REPEAT_DAYS * 864e5) return;

		var form = box.querySelector('form'), input = box.querySelector('#lc-mama-email'),
			error = box.querySelector('.lc-mama__error'), cta = box.querySelector('.lc-mama__cta'),
			done = box.querySelector('.lc-mama__step--done'), copy = box.querySelector('.lc-mama__copy');

		function open() {
			box.hidden = false;
			document.documentElement.classList.add('lc-mama-open');
			requestAnimationFrame(function () { box.classList.add('is-open'); });
			setTimeout(function () { input.focus({ preventScroll: true }); }, 250);
		}
		function close() {
			box.classList.remove('is-open');
			document.documentElement.classList.remove('lc-mama-open');
			setTimeout(function () { box.hidden = true; }, 250);
			if (!(get() || {}).done) set({ closed: Date.now() });
		}

		box.addEventListener('click', function (e) { if (e.target.closest('[data-lc-close]')) close(); });
		document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) close(); });

		form.addEventListener('submit', function (e) {
			e.preventDefault();
			var email = input.value.trim();
			if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { error.textContent = 'Escribí un mail válido.'; input.focus(); return; }
			error.textContent = '';
			cta.disabled = true; cta.textContent = 'Un segundo…';

			var body = new FormData(form);
			body.append('action', 'lc_mama_signup');
			fetch('<?php echo esc_url( admin_url( 'admin-ajax.php' ) ); ?>', { method: 'POST', body: body, credentials: 'same-origin' })
				.then(function (r) { return r.json(); })
				.then(function (res) {
					if (!res || !res.success) throw { msg: res && res.data && res.data.message };
					set({ done: Date.now() });
					form.hidden = true;
					done.hidden = false;
					copy.focus();
				})
				.catch(function (err) {
					error.textContent = (err && err.msg) || 'No pudimos guardar tu mail. Probá de nuevo.';
					cta.disabled = false; cta.textContent = 'Lo quiero';
				});
		});

		copy.addEventListener('click', function () {
			var code = '<?php echo esc_js( LC_MAMA_LABEL ); ?>';
			function ok() { copy.textContent = '¡Copiado!'; setTimeout(function () { copy.textContent = 'Copiar'; }, 2000); }
			if (navigator.clipboard && window.isSecureContext) {
				navigator.clipboard.writeText(code).then(ok, fallback);
			} else { fallback(); }
			function fallback() {
				var t = document.createElement('textarea');
				t.value = code; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
				document.body.appendChild(t); t.select();
				try { document.execCommand('copy'); ok(); } catch (e) {}
				document.body.removeChild(t);
			}
		});

		setTimeout(open, DELAY);
	})();
	</script>
	<?php
} );

/* ===================================================================
 * 6. Estilos (cupón en checkout + popup)
 * =================================================================== */

add_action( 'wp_head', function () {
	?>
	<style id="lc-mama-css">
	/* Cupón en el checkout */
	.lc-coupon{margin:20px 0;padding:16px;background:#F2F1EE;border-radius:4px}
	.lc-coupon__label{display:block;font-weight:700;font-size:15px;color:#111111;margin-bottom:10px}
	.lc-coupon__row{display:flex;gap:10px}
	.lc-coupon__input{flex:1 1 auto;min-width:0;height:48px;border-radius:999px!important;border:1.5px solid #111111!important;padding:0 18px!important;background:#FFFFFF!important;text-transform:uppercase}
	.lc-coupon__input::placeholder{text-transform:none}
	.lc-coupon__apply{flex:0 0 auto}
	.lc-coupon.is-loading{opacity:.6;pointer-events:none}
	.lc-coupon__msg:empty{display:none}
	.lc-coupon__msg{margin-top:12px}
	.lc-coupon__msg .woocommerce-error,.lc-coupon__msg .woocommerce-message,.lc-coupon__msg .woocommerce-info{margin:0!important}

	/* Popup Día de la Madre */
	.lc-mama{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px}
	.lc-mama[hidden]{display:none}
	.lc-mama__backdrop{position:absolute;inset:0;background:rgba(17,17,17,.6);opacity:0;transition:opacity .25s ease}
	.lc-mama__box{position:relative;width:100%;max-width:440px;background:#FFFFFF;border-radius:6px;padding:44px 28px 28px;text-align:center;box-shadow:0 30px 60px rgba(0,0,0,.3);border-top:8px solid #FF4F1F;opacity:0;transform:translateY(16px);transition:opacity .25s ease,transform .25s ease;font-family:'Archivo',system-ui,-apple-system,'Segoe UI',sans-serif}
	.lc-mama.is-open .lc-mama__backdrop,.lc-mama.is-open .lc-mama__box{opacity:1;transform:none}
	.lc-mama__close{position:absolute;top:8px;right:10px;width:40px;height:40px;border:0;background:transparent;font-size:30px;line-height:1;color:#111111;cursor:pointer;padding:0}
	.lc-mama__title{font-family:'Instrument Serif',Georgia,serif!important;font-weight:400!important;font-size:32px!important;line-height:1.08!important;color:#111111!important;margin:0 0 22px!important;letter-spacing:-.01em}
	.lc-mama__title strong{color:#C2370A;font-weight:400}
	.lc-mama__input{width:100%;height:52px;border-radius:999px;border:1.5px solid #111111;padding:0 20px;font-size:16px;margin-bottom:12px;box-sizing:border-box;background:#FFFFFF;color:#111111;text-align:center}
	.lc-mama__cta{width:100%;min-height:54px!important;font-size:18px!important}
	.lc-mama__cta:disabled{opacity:.7}
	.lc-mama__hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;opacity:0}
	.lc-mama__error{color:#C2370A;font-size:14px;margin:10px 0 0;min-height:1em}
	.lc-mama__error:empty{display:none}
	.lc-mama__code{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;background:#F2F1EE;border:2px dashed #111111;border-radius:6px;padding:14px 16px;font-size:18px;color:#111111;letter-spacing:.04em}
	.lc-mama__code strong{font-size:24px}
	.lc-mama__copy{min-height:40px!important;padding:0 20px!important;font-size:15px!important}
	.lc-mama__note{margin:14px 0 0;font-size:14px;color:#555555}
	html.lc-mama-open{overflow:hidden}
	@media (max-width:480px){.lc-mama__title{font-size:28px!important}.lc-mama__box{padding:40px 20px 22px}}
	@media (prefers-reduced-motion:reduce){.lc-mama__backdrop,.lc-mama__box{transition:none}}
	</style>
	<?php
} );

/* ===================================================================
 * 7. Listado de mails en el panel (WooCommerce → Mails Día de la Madre)
 * =================================================================== */

add_action( 'admin_menu', function () {
	add_submenu_page( 'woocommerce', 'Mails Día de la Madre', 'Mails Día de la Madre', 'manage_woocommerce', 'lc-mama-emails', 'lc_mama_admin_page' );
}, 99 );

add_action( 'admin_init', function () {
	if ( empty( $_GET['page'] ) || 'lc-mama-emails' !== $_GET['page'] || empty( $_GET['csv'] ) ) {
		return;
	}
	if ( ! current_user_can( 'manage_woocommerce' ) ) {
		return;
	}
	check_admin_referer( 'lc_mama_csv' );
	$emails = (array) get_option( LC_MAMA_EMAILS_OPT, array() );
	header( 'Content-Type: text/csv; charset=utf-8' );
	header( 'Content-Disposition: attachment; filename=mails-dia-de-la-madre.csv' );
	$out = fopen( 'php://output', 'w' );
	fputcsv( $out, array( 'email', 'fecha' ) );
	foreach ( $emails as $email => $date ) {
		fputcsv( $out, array( $email, $date ) );
	}
	fclose( $out );
	exit;
} );

function lc_mama_admin_page() {
	$emails = array_reverse( (array) get_option( LC_MAMA_EMAILS_OPT, array() ), true );
	$csv    = wp_nonce_url( admin_url( 'admin.php?page=lc-mama-emails&csv=1' ), 'lc_mama_csv' );
	?>
	<div class="wrap">
		<h1>Mails Día de la Madre <span class="title-count"><?php echo (int) count( $emails ); ?></span></h1>
		<p><a class="button button-primary" href="<?php echo esc_url( $csv ); ?>">Descargar CSV</a></p>
		<table class="widefat striped" style="max-width:640px">
			<thead><tr><th>Mail</th><th>Fecha</th></tr></thead>
			<tbody>
			<?php if ( ! $emails ) : ?>
				<tr><td colspan="2">Todavía no hay mails.</td></tr>
			<?php endif; ?>
			<?php foreach ( $emails as $email => $date ) : ?>
				<tr><td><?php echo esc_html( $email ); ?></td><td><?php echo esc_html( $date ); ?></td></tr>
			<?php endforeach; ?>
			</tbody>
		</table>
	</div>
	<?php
}
