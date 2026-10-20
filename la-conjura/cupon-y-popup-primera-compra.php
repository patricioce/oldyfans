<?php
/**
 * Plugin Name: La Conjura — Cupón en checkout + popup primera compra
 * Description: Muestra el campo de cupón en carrito y checkout y suma un popup que pide el mail, asigna el cupón PrimeraConjura (15% OFF) automáticamente y manda el mail a Brevo.
 * Version: 2.0
 *
 * Instalación: pegar en Fragmentos de código (plugin Code Snippets) como fragmento PHP
 * "Ejecutar en todas partes", sin la primera línea "<?php". O subir este archivo a
 * wp-content/mu-plugins/.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// El cupón se crea y se configura en Marketing → Cupones.
const LC_POPUP_COUPON = 'PrimeraConjura';

/* ===== 1. Cupón en el checkout ===== */

// Habilita los cupones aunque estén apagados en WooCommerce → Ajustes → Generales.
add_filter( 'woocommerce_coupons_enabled', '__return_true' );

// Formulario de cupón siempre abierto en el checkout (sin el "Hacé clic aquí").
add_action( 'wp_head', function () {
	if ( ! function_exists( 'is_checkout' ) || ! ( is_checkout() || is_cart() ) ) {
		return;
	}
	echo <<<'LC_CSS'
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
LC_CSS;
} );

/* ===== 2. Popup primera compra ===== */

// Recibe el mail, lo guarda y deja el cupón asignado a la sesión del cliente.
function lc_popup_suscribir() {
	$email = isset( $_POST['email'] ) ? sanitize_email( wp_unslash( $_POST['email'] ) ) : '';
	if ( ! is_email( $email ) ) {
		wp_send_json_error( array( 'message' => 'Revisá el mail, parece que no está bien escrito.' ), 400 );
	}

	$emails = get_option( 'lc_popup_emails', array() );
	if ( ! isset( $emails[ $email ] ) ) {
		$emails[ $email ] = current_time( 'mysql' );
		update_option( 'lc_popup_emails', $emails, false );
	}
	lc_popup_brevo_enviar( $email );

	if ( function_exists( 'WC' ) && WC()->session ) {
		if ( ! WC()->session->has_session() ) {
			WC()->session->set_customer_session_cookie( true );
		}
		WC()->session->set( 'lc_popup_pendiente', true );
		WC()->session->set( 'lc_popup_email', $email );
		lc_popup_aplicar_cupon();
	}

	wp_send_json_success();
}
add_action( 'wp_ajax_lc_popup_suscribir', 'lc_popup_suscribir' );
add_action( 'wp_ajax_nopriv_lc_popup_suscribir', 'lc_popup_suscribir' );

// Aplica el cupón apenas haya algo en el carrito (WooCommerce no deja cupones en un carrito vacío).
function lc_popup_aplicar_cupon() {
	if ( ! function_exists( 'WC' ) || ! WC()->session || ! WC()->cart || ! WC()->session->get( 'lc_popup_pendiente' ) ) {
		return;
	}
	if ( WC()->cart->is_empty() ) {
		return;
	}
	if ( ! WC()->cart->has_discount( LC_POPUP_COUPON ) ) {
		WC()->cart->apply_coupon( LC_POPUP_COUPON );
	}
	WC()->session->set( 'lc_popup_pendiente', false );
}
add_action( 'woocommerce_add_to_cart', 'lc_popup_aplicar_cupon', 20 );
add_action( 'woocommerce_before_cart', 'lc_popup_aplicar_cupon' );
add_action( 'woocommerce_before_checkout_form', 'lc_popup_aplicar_cupon', 5 );

// Completa el mail del checkout con el que dejó en el popup.
add_filter( 'woocommerce_checkout_get_value', function ( $value, $input ) {
	if ( 'billing_email' === $input && ! $value && function_exists( 'WC' ) && WC()->session ) {
		return WC()->session->get( 'lc_popup_email' );
	}
	return $value;
}, 10, 2 );

// Popup: aparece a los 3 segundos, una sola vez (si lo cierra, vuelve a los 7 días).
add_action( 'wp_footer', function () {
	if ( function_exists( 'is_checkout' ) && ( is_checkout() || is_account_page() ) ) {
		return;
	}
	$html = <<<'LC_HTML'
	<div id="lc-popup" class="lc-popup" role="dialog" aria-modal="true" aria-labelledby="lc-popup-titulo" hidden>
		<div class="lc-popup__box">
			<button type="button" class="lc-popup__cerrar" aria-label="Cerrar">&times;</button>
			<div class="lc-popup__paso" data-paso="form">
				<p id="lc-popup-titulo" class="lc-popup__titulo">Dejanos tu mail y obtené un <strong>15% OFF</strong> en tu <span>primera compra</span></p>
				<form class="lc-popup__form" novalidate>
					<label class="screen-reader-text" for="lc-popup-email">Tu mail</label>
					<input id="lc-popup-email" type="email" name="email" placeholder="tu@mail.com" autocomplete="email" required>
					<button type="submit" class="button">Lo quiero</button>
					<p class="lc-popup__error" role="alert"></p>
				</form>
			</div>
			<div class="lc-popup__paso" data-paso="gracias" hidden>
				<p class="lc-popup__titulo">¡Gracias! Ya tenés tu 15% OFF</p>
				<p class="lc-popup__codigo-label">Código:</p>
				<div class="lc-popup__codigo">
					<span>PrimeraConjura</span>
					<button type="button" class="button lc-popup__copiar">Copiar</button>
				</div>
				<p class="lc-popup__nota">Se aplica solo en tu carrito.</p>
			</div>
		</div>
	</div>
	<style>
	.lc-popup{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(17,17,17,.6)}
	.lc-popup[hidden]{display:none}
	.lc-popup__box{position:relative;width:100%;max-width:440px;background:#FFFFFF;border-radius:6px;padding:40px 28px 28px;text-align:center;box-shadow:0 30px 60px rgba(0,0,0,.3);font-family:'Archivo',system-ui,sans-serif}
	.lc-popup__cerrar{position:absolute;top:8px;right:10px;background:none!important;border:0;font-size:30px;line-height:1;color:#111111!important;cursor:pointer;padding:4px 8px!important;min-height:0!important}
	.lc-popup__titulo{font-family:'Instrument Serif',Georgia,serif;font-size:32px;line-height:1.1;color:#111111;margin:0 0 20px}
	.lc-popup__titulo strong{font-family:'Archivo',system-ui,sans-serif;font-weight:800;color:#C2370A}
	.lc-popup__titulo span{text-transform:uppercase;font-family:'Archivo',system-ui,sans-serif;font-weight:800;font-size:.8em}
	.lc-popup__form{display:flex;flex-direction:column;gap:10px;margin:0}
	.lc-popup__form input{min-height:50px;border-radius:999px;border:1.5px solid #111111;padding:0 20px;font-size:16px;text-align:center}
	.lc-popup__form .button{width:100%;font-size:17px!important}
	.lc-popup__error{margin:0;min-height:1em;color:#C2370A;font-size:14px}
	.lc-popup__codigo-label{margin:0 0 6px;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#555555}
	.lc-popup__codigo{display:flex;align-items:center;justify-content:space-between;gap:10px;border:2px dashed #FF4F1F;border-radius:999px;padding:6px 6px 6px 22px}
	.lc-popup__codigo span{font-size:20px;font-weight:800;letter-spacing:.02em;color:#111111}
	.lc-popup__nota{margin:14px 0 0;font-size:14px;color:#555555}
	</style>
	<script>
	(function () {
		var popup = document.getElementById('lc-popup');
		if (!popup) return;
		var CLAVE = 'lc_popup_primera_compra';
		function leer() { try { return JSON.parse(localStorage.getItem(CLAVE)) || {}; } catch (e) { return {}; } }
		function guardar(v) { try { localStorage.setItem(CLAVE, JSON.stringify(v)); } catch (e) {} }

		var estado = leer();
		if (estado.suscripto || (estado.cerrado && Date.now() - estado.cerrado < 7 * 864e5)) return;

		var form = popup.querySelector('.lc-popup__form');
		var input = popup.querySelector('#lc-popup-email');
		var error = popup.querySelector('.lc-popup__error');

		function cerrar() {
			popup.hidden = true;
			if (!leer().suscripto) guardar({ cerrado: Date.now() });
		}
		popup.querySelector('.lc-popup__cerrar').addEventListener('click', cerrar);
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
			datos.append('action', 'lc_popup_suscribir');
			datos.append('email', email);
			fetch(LC_AJAX_URL, { method: 'POST', body: datos, credentials: 'same-origin' })
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

		popup.querySelector('.lc-popup__copiar').addEventListener('click', function () {
			var boton = this;
			function listo() { boton.textContent = '¡Copiado!'; setTimeout(function () { boton.textContent = 'Copiar'; }, 2000); }
			if (navigator.clipboard && window.isSecureContext) {
				navigator.clipboard.writeText('PrimeraConjura').then(listo);
			} else {
				var t = document.createElement('textarea');
				t.value = 'PrimeraConjura';
				document.body.appendChild(t);
				t.select();
				document.execCommand('copy');
				t.remove();
				listo();
			}
		});
	})();
	</script>
LC_HTML;
	echo str_replace( 'LC_AJAX_URL', wp_json_encode( admin_url( 'admin-ajax.php' ) ), $html );
} );

/* ===== 3. Brevo: cada mail del popup entra a la lista "Primera compra (popup)" ===== */

// La clave se carga en WooCommerce → Mails popup primera compra (o con LC_BREVO_API_KEY en wp-config.php).
function lc_popup_brevo_key() {
	return defined( 'LC_BREVO_API_KEY' ) ? LC_BREVO_API_KEY : get_option( 'lc_popup_brevo_key', get_option( 'lc_mama_brevo_key', '' ) );
}

function lc_popup_brevo_api( $metodo, $ruta, $cuerpo = null ) {
	$args = array(
		'method'  => $metodo,
		'timeout' => 8,
		'headers' => array(
			'api-key'      => lc_popup_brevo_key(),
			'accept'       => 'application/json',
			'content-type' => 'application/json',
		),
	);
	if ( null !== $cuerpo ) {
		$args['body'] = wp_json_encode( $cuerpo );
	}
	$respuesta = wp_remote_request( 'https://api.brevo.com/v3' . $ruta, $args );
	if ( is_wp_error( $respuesta ) ) {
		return $respuesta;
	}
	$codigo = wp_remote_retrieve_response_code( $respuesta );
	$datos  = json_decode( wp_remote_retrieve_body( $respuesta ), true );
	if ( $codigo >= 300 ) {
		return new WP_Error( 'brevo', 'Brevo respondió ' . $codigo . ': ' . ( isset( $datos['message'] ) ? $datos['message'] : '' ) );
	}
	return is_array( $datos ) ? $datos : array();
}

// Usa la lista guardada o la crea la primera vez.
function lc_popup_brevo_lista() {
	$id = (int) get_option( 'lc_popup_brevo_lista', 0 );
	if ( $id ) {
		return $id;
	}
	$carpetas = lc_popup_brevo_api( 'GET', '/contacts/folders?limit=1&offset=0' );
	if ( is_wp_error( $carpetas ) ) {
		return $carpetas;
	}
	if ( empty( $carpetas['folders'][0]['id'] ) ) {
		return new WP_Error( 'brevo', 'No hay ninguna carpeta de listas en Brevo.' );
	}
	$lista = lc_popup_brevo_api( 'POST', '/contacts/lists', array(
		'name'     => 'Primera compra (popup)',
		'folderId' => (int) $carpetas['folders'][0]['id'],
	) );
	if ( is_wp_error( $lista ) ) {
		return $lista;
	}
	update_option( 'lc_popup_brevo_lista', (int) $lista['id'], false );
	return (int) $lista['id'];
}

function lc_popup_brevo_enviar( $email ) {
	if ( ! lc_popup_brevo_key() ) {
		return false;
	}
	$lista = lc_popup_brevo_lista();
	if ( ! is_wp_error( $lista ) ) {
		$lista = lc_popup_brevo_api( 'POST', '/contacts', array(
			'email'         => $email,
			'listIds'       => array( $lista ),
			'updateEnabled' => true,
		) );
	}
	if ( is_wp_error( $lista ) ) {
		update_option( 'lc_popup_brevo_error', current_time( 'mysql' ) . ' — ' . $email . ' — ' . $lista->get_error_message(), false );
		return false;
	}
	return true;
}

/* ===== 4. WooCommerce → Mails popup primera compra ===== */

add_action( 'admin_menu', function () {
	add_submenu_page( 'woocommerce', 'Mails popup primera compra', 'Mails popup primera compra', 'manage_woocommerce', 'lc-popup-emails', function () {
		$emails = get_option( 'lc_popup_emails', array() );

		if ( isset( $_POST['lc_popup_guardar'] ) && check_admin_referer( 'lc_popup_brevo' ) ) {
			if ( ! defined( 'LC_BREVO_API_KEY' ) && isset( $_POST['lc_popup_brevo_key'] ) && '' !== $_POST['lc_popup_brevo_key'] ) {
				update_option( 'lc_popup_brevo_key', sanitize_text_field( wp_unslash( $_POST['lc_popup_brevo_key'] ) ), false );
			}
			delete_option( 'lc_popup_brevo_error' );
			$enviados = 0;
			foreach ( array_keys( $emails ) as $email ) {
				$enviados += lc_popup_brevo_enviar( $email ) ? 1 : 0;
			}
			echo '<div class="notice notice-info"><p>Enviados a Brevo: ' . (int) $enviados . ' de ' . count( $emails ) . '.</p></div>';
		}

		$error = get_option( 'lc_popup_brevo_error' );
		echo '<div class="wrap"><h1>Mails popup primera compra (' . count( $emails ) . ')</h1>';

		echo '<h2>Brevo</h2>';
		if ( $error ) {
			echo '<div class="notice notice-error inline"><p>Último error: ' . esc_html( $error ) . '</p></div>';
		}
		echo '<form method="post">';
		wp_nonce_field( 'lc_popup_brevo' );
		if ( defined( 'LC_BREVO_API_KEY' ) ) {
			echo '<p>Clave de API cargada desde wp-config.php.</p>';
		} else {
			echo '<p><label>Clave de API de Brevo (Brevo → SMTP y API → Claves API)<br>';
			echo '<input type="password" name="lc_popup_brevo_key" class="regular-text" autocomplete="off" placeholder="' . ( lc_popup_brevo_key() ? 'Ya está cargada — dejá vacío para no cambiarla' : 'xkeysib-…' ) . '"></label></p>';
		}
		$lista = (int) get_option( 'lc_popup_brevo_lista', 0 );
		echo '<p>Lista: ' . ( $lista ? 'Primera compra (popup) (ID ' . $lista . ')' : 'se crea sola, "Primera compra (popup)", con el primer envío' ) . '</p>';
		echo '<p><button class="button button-primary" name="lc_popup_guardar" value="1">Guardar y enviar a Brevo los mails ya recibidos</button></p>';
		echo '</form>';

		echo '<h2>Lista</h2>';
		echo '<textarea readonly rows="20" style="width:100%;max-width:640px;font-family:monospace">';
		echo esc_textarea( "email,fecha\n" );
		foreach ( $emails as $email => $fecha ) {
			echo esc_textarea( $email . ',' . $fecha . "\n" );
		}
		echo '</textarea></div>';
	} );
} );
