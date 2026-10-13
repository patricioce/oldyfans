<?php
/**
 * Plugin Name: La Conjura — Cupón en checkout + popup Día de la Madre
 * Description: Muestra el campo de cupón en carrito y checkout, crea el cupón MAMÁ (15% OFF) y suma un popup que pide el mail y asigna el código automáticamente.
 * Version: 1.0
 *
 * Instalación: pegar en Fragmentos de código (plugin Code Snippets) como fragmento PHP
 * "Ejecutar en todas partes", sin la primera línea "<?php". O subir este archivo a
 * wp-content/mu-plugins/.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const LC_MAMA_COUPON  = 'mamá';
const LC_MAMA_PERCENT = '15';

/* ===== 1. Cupón en el checkout ===== */

// Habilita los cupones aunque estén apagados en WooCommerce → Ajustes → Generales.
add_filter( 'woocommerce_coupons_enabled', '__return_true' );

// Crea el cupón MAMÁ (15% sobre el carrito) si todavía no existe.
add_action( 'admin_init', function () {
	if ( ! function_exists( 'wc_get_coupon_id_by_code' ) || wc_get_coupon_id_by_code( LC_MAMA_COUPON ) ) {
		return;
	}
	$coupon = new WC_Coupon();
	$coupon->set_code( LC_MAMA_COUPON );
	$coupon->set_description( 'Día de la Madre — popup de suscripción' );
	$coupon->set_discount_type( 'percent' );
	$coupon->set_amount( LC_MAMA_PERCENT );
	$coupon->save();
} );

// Acepta "MAMA" sin tilde como el mismo código.
add_filter( 'woocommerce_coupon_code', function ( $code ) {
	return 'mama' === $code ? LC_MAMA_COUPON : $code;
}, 20 );

// Formulario de cupón siempre abierto en el checkout (sin el "Hacé clic aquí").
add_action( 'wp_head', function () {
	if ( ! function_exists( 'is_checkout' ) || ! ( is_checkout() || is_cart() ) ) {
		return;
	}
	?>
	<style>
	.woocommerce-form-coupon-toggle{display:none!important}
	.woocommerce-checkout form.checkout_coupon{display:flex!important;flex-wrap:wrap;gap:10px;align-items:stretch;border:1.5px solid #E4E2DD!important;border-radius:4px;padding:16px!important;margin:0 0 24px!important;background:#F2F1EE}
	.woocommerce-checkout form.checkout_coupon>p:first-child{flex:1 1 100%;margin:0;font-size:0}
	.woocommerce-checkout form.checkout_coupon>p:first-child::after{content:"¿Tenés un cupón de descuento?";font-size:16px;font-weight:700;color:#111111}
	.woocommerce-checkout form.checkout_coupon .form-row{margin:0!important;float:none!important;width:auto!important}
	.woocommerce-checkout form.checkout_coupon .form-row-first{flex:1 1 180px}
	.woocommerce-checkout form.checkout_coupon .clear{display:none}
	.woocommerce-checkout form.checkout_coupon input.input-text,.woocommerce-cart .coupon input.input-text{min-height:48px;border-radius:999px;border:1.5px solid #111111;padding:0 18px;text-transform:uppercase;width:100%}
	</style>
	<?php
} );

/* ===== 2. Popup Día de la Madre ===== */

// Recibe el mail, lo guarda y deja el cupón asignado a la sesión del cliente.
function lc_mama_suscribir() {
	$email = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) ) : '';
	if ( ! is_email( $email ) ) {
		wp_send_json_error( array( 'message' => 'Revisá el mail, parece que no está bien escrito.' ), 400 );
	}

	$emails = get_option( 'lc_mama_emails', array() );
	if ( ! isset( $emails[ $email ] ) ) {
		$emails[ $email ] = current_time( 'mysql' );
		update_option( 'lc_mama_emails', $emails, false );
	}

	if ( function_exists( 'WC' ) && WC()->session ) {
		if ( ! WC()->session->has_session() ) {
			WC()->session->set_customer_session_cookie( true );
		}
		WC()->session->set( 'lc_mama_pendiente', true );
		WC()->session->set( 'lc_mama_email', $email );
		lc_mama_aplicar_cupon();
	}

	wp_send_json_success();
}
add_action( 'wp_ajax_lc_mama_suscribir', 'lc_mama_suscribir' );
add_action( 'wp_ajax_nopriv_lc_mama_suscribir', 'lc_mama_suscribir' );

// Aplica el cupón apenas haya algo en el carrito (WooCommerce no deja cupones en un carrito vacío).
function lc_mama_aplicar_cupon() {
	if ( ! function_exists( 'WC' ) || ! WC()->session || ! WC()->cart || ! WC()->session->get( 'lc_mama_pendiente' ) ) {
		return;
	}
	if ( WC()->cart->is_empty() ) {
		return;
	}
	if ( ! WC()->cart->has_discount( LC_MAMA_COUPON ) ) {
		WC()->cart->apply_coupon( LC_MAMA_COUPON );
	}
	WC()->session->set( 'lc_mama_pendiente', false );
}
add_action( 'woocommerce_add_to_cart', 'lc_mama_aplicar_cupon', 20 );
add_action( 'woocommerce_before_cart', 'lc_mama_aplicar_cupon' );
add_action( 'woocommerce_before_checkout_form', 'lc_mama_aplicar_cupon', 5 );

// Completa el mail del checkout con el que dejó en el popup.
add_filter( 'woocommerce_checkout_get_value', function ( $value, $input ) {
	if ( 'billing_email' === $input && ! $value && function_exists( 'WC' ) && WC()->session ) {
		return WC()->session->get( 'lc_mama_email' );
	}
	return $value;
}, 10, 2 );

// Popup: aparece a los 3 segundos, una sola vez (si lo cierra, vuelve a los 7 días).
add_action( 'wp_footer', function () {
	if ( function_exists( 'is_checkout' ) && ( is_checkout() || is_account_page() ) ) {
		return;
	}
	?>
	<div id="lc-mama" class="lc-mama" role="dialog" aria-modal="true" aria-labelledby="lc-mama-titulo" hidden>
		<div class="lc-mama__box">
			<button type="button" class="lc-mama__cerrar" aria-label="Cerrar">&times;</button>
			<div class="lc-mama__paso" data-paso="form">
				<p id="lc-mama-titulo" class="lc-mama__titulo">Déjanos tu mail y obtené un <strong>15% OFF</strong> por el <span>Día de la Madre</span></p>
				<form class="lc-mama__form" novalidate>
					<label class="screen-reader-text" for="lc-mama-email">Tu mail</label>
					<input id="lc-mama-email" type="email" name="email" placeholder="tu@mail.com" autocomplete="email" required>
					<button type="submit" class="button">Lo quiero</button>
					<p class="lc-mama__error" role="alert"></p>
				</form>
			</div>
			<div class="lc-mama__paso" data-paso="gracias" hidden>
				<p class="lc-mama__titulo">¡Gracias! Tu vieja se va a poner re contenta</p>
				<p class="lc-mama__codigo-label">Código:</p>
				<div class="lc-mama__codigo">
					<span>MAMÁ</span>
					<button type="button" class="button lc-mama__copiar">Copiar</button>
				</div>
				<p class="lc-mama__nota">Ya quedó aplicado en tu carrito.</p>
			</div>
		</div>
	</div>
	<style>
	.lc-mama{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(17,17,17,.6)}
	.lc-mama[hidden]{display:none}
	.lc-mama__box{position:relative;width:100%;max-width:440px;background:#FFFFFF;border-radius:6px;padding:40px 28px 28px;text-align:center;box-shadow:0 30px 60px rgba(0,0,0,.3);font-family:'Archivo',system-ui,sans-serif}
	.lc-mama__cerrar{position:absolute;top:8px;right:10px;background:none!important;border:0;font-size:30px;line-height:1;color:#111111!important;cursor:pointer;padding:4px 8px!important;min-height:0!important}
	.lc-mama__titulo{font-family:'Instrument Serif',Georgia,serif;font-size:32px;line-height:1.1;color:#111111;margin:0 0 20px}
	.lc-mama__titulo strong{font-family:'Archivo',system-ui,sans-serif;font-weight:800;color:#C2370A}
	.lc-mama__titulo span{text-transform:uppercase;font-family:'Archivo',system-ui,sans-serif;font-weight:800;font-size:.8em}
	.lc-mama__form{display:flex;flex-direction:column;gap:10px;margin:0}
	.lc-mama__form input{min-height:50px;border-radius:999px;border:1.5px solid #111111;padding:0 20px;font-size:16px;text-align:center}
	.lc-mama__form .button{width:100%;font-size:17px!important}
	.lc-mama__error{margin:0;min-height:1em;color:#C2370A;font-size:14px}
	.lc-mama__codigo-label{margin:0 0 6px;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#555555}
	.lc-mama__codigo{display:flex;align-items:center;justify-content:space-between;gap:10px;border:2px dashed #FF4F1F;border-radius:999px;padding:6px 6px 6px 22px}
	.lc-mama__codigo span{font-size:24px;font-weight:800;letter-spacing:.06em;color:#111111}
	.lc-mama__nota{margin:14px 0 0;font-size:14px;color:#555555}
	</style>
	<script>
	(function () {
		var popup = document.getElementById('lc-mama');
		if (!popup) return;
		var CLAVE = 'lc_mama_popup';
		function leer() { try { return JSON.parse(localStorage.getItem(CLAVE)) || {}; } catch (e) { return {}; } }
		function guardar(v) { try { localStorage.setItem(CLAVE, JSON.stringify(v)); } catch (e) {} }

		var estado = leer();
		if (estado.suscripto || (estado.cerrado && Date.now() - estado.cerrado < 7 * 864e5)) return;

		var form = popup.querySelector('.lc-mama__form');
		var input = popup.querySelector('#lc-mama-email');
		var error = popup.querySelector('.lc-mama__error');

		function cerrar() {
			popup.hidden = true;
			if (!leer().suscripto) guardar({ cerrado: Date.now() });
		}
		popup.querySelector('.lc-mama__cerrar').addEventListener('click', cerrar);
		popup.addEventListener('click', function (e) { if (e.target === popup) cerrar(); });
		document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !popup.hidden) cerrar(); });

		setTimeout(function () { popup.hidden = false; input.focus(); }, 3000);

		form.addEventListener('submit', function (e) {
			e.preventDefault();
			var email = input.value.trim();
			if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { error.textContent = 'Revisá el mail, parece que no está bien escrito.'; return; }
			error.textContent = '';
			var boton = form.querySelector('button');
			boton.disabled = true;
			var datos = new FormData();
			datos.append('action', 'lc_mama_suscribir');
			datos.append('email', email);
			fetch(<?php echo wp_json_encode( admin_url( 'admin-ajax.php' ) ); ?>, { method: 'POST', body: datos, credentials: 'same-origin' })
				.then(function (r) { return r.json(); })
				.then(function (r) {
					if (!r.success) throw new Error(r.data && r.data.message);
					guardar({ suscripto: true });
					popup.querySelector('[data-paso="form"]').hidden = true;
					popup.querySelector('[data-paso="gracias"]').hidden = false;
				})
				.catch(function (err) {
					boton.disabled = false;
					error.textContent = (err && err.message) || 'Algo falló, probá de nuevo.';
				});
		});

		popup.querySelector('.lc-mama__copiar').addEventListener('click', function () {
			var boton = this;
			function listo() { boton.textContent = '¡Copiado!'; setTimeout(function () { boton.textContent = 'Copiar'; }, 2000); }
			if (navigator.clipboard && window.isSecureContext) {
				navigator.clipboard.writeText('MAMÁ').then(listo);
			} else {
				var t = document.createElement('textarea');
				t.value = 'MAMÁ';
				document.body.appendChild(t);
				t.select();
				document.execCommand('copy');
				t.remove();
				listo();
			}
		});
	})();
	</script>
	<?php
} );

/* ===== 3. Mails recibidos: WooCommerce → Mails Día de la Madre ===== */

add_action( 'admin_menu', function () {
	add_submenu_page( 'woocommerce', 'Mails Día de la Madre', 'Mails Día de la Madre', 'manage_woocommerce', 'lc-mama-emails', function () {
		$emails = get_option( 'lc_mama_emails', array() );
		echo '<div class="wrap"><h1>Mails Día de la Madre (' . count( $emails ) . ')</h1>';
		echo '<p>Copiá la lista para importarla en tu herramienta de mailing.</p>';
		echo '<textarea readonly rows="20" style="width:100%;max-width:640px;font-family:monospace">';
		echo esc_textarea( "email,fecha\n" );
		foreach ( $emails as $email => $fecha ) {
			echo esc_textarea( $email . ',' . $fecha . "\n" );
		}
		echo '</textarea></div>';
	} );
} );
