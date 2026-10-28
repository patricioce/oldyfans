<?php
/**
 * Botón verde de WhatsApp. Recibe el texto en $args['label'].
 */
$aguirre_label = isset( $args['label'] ) ? $args['label'] : 'Escribir por WhatsApp';
?>
<a class="btn btn-wa" href="<?php echo esc_url( aguirre_wa_url() ); ?>" target="_blank" rel="noopener">
	<?php echo aguirre_icon( 'whatsapp' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
	<?php echo esc_html( $aguirre_label ); ?>
</a>
