#!/bin/bash
# Desde carga-disenos/kit. Sin argumento: simulacion. Con "--create": crea en Printify (sin publicar).
D=../lote-2026-11-19g-survivors/disenos; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"; P="python3 scripts/printify_new_product.py --tienda survivors"
$P "$@" --title "50 Years T-Shirt" --colors "$C" --y 0.364 --image "$D/50 Years/color.png" --image-color "Black=$D/50 Years/clara.png" --image-color "Navy=$D/50 Years/clara.png" --image-color "Military Green=$D/50 Years/oscura.png" --image-color "Charcoal=$D/50 Years/oscura.png"
$P "$@" --title "Be Kind, Rewind T-Shirt" --colors "$C" --y 0.390 --image "$D/Be Kind Rewind/unica.png"
$P "$@" --title "Do Not Bend T-Shirt" --colors "$C" --y 0.375 --image "$D/Do Not Bend/oscura.png" --image-light "$D/Do Not Bend/clara.png"
$P "$@" --title "How Eye Roll T-Shirt" --colors "$C" --image "$D/How Eye Roll/oscura.png" --image-light "$D/How Eye Roll/clara.png"
$P "$@" --title "The Light T-Shirt" --colors "Charcoal,Military Green,Sport Grey,White" --y 0.384 --image "$D/The Light/unica.png"
