#!/bin/bash
# Desde carga-disenos/kit. Sin argumento: simulacion. Con "--create": crea en Printify (sin publicar).
D=../lote-2026-11-19i-survivors/disenos; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"; P="python3 scripts/printify_new_product.py --tienda survivors"
$P "$@" --title "Second Rodeo T-Shirt" --colors "$C" --image "$D/Second Rodeo/oscura.png" --image-light "$D/Second Rodeo/clara.png"
$P "$@" --title "Night Owl T-Shirt" --colors "Sport Grey,White" --y 0.424 --image "$D/Night Owl/unica.png"
