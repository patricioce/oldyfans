#!/bin/bash
# Desde carga-disenos/kit. Sin argumento: simulacion. Con "--create": crea en Printify (sin publicar).
D=../lote-2026-11-19h-survivors/disenos; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"; C4="Black,Charcoal,Military Green,Navy"; P="python3 scripts/printify_new_product.py --tienda survivors"
$P "$@" --title "Big Wheel T-Shirt" --colors "$C" --y 0.383 --image "$D/Big Wheel/oscura.png" --image-light "$D/Big Wheel/clara.png"
$P "$@" --title "I'll Be In The Garage 2 T-Shirt" --colors "$C4" --y 0.448 --image "$D/I'll Be In The Garage 2/unica.png"
$P "$@" --title "I'll Be In The Garage 4 T-Shirt" --colors "$C4" --y 0.450 --image "$D/I'll Be In The Garage 4/unica.png"
$P "$@" --title "Morons T-Shirt" --colors "$C" --y 0.390 --image "$D/Morons/oscura.png" --image-light "$D/Morons/clara.png"
$P "$@" --title "Personal Space T-Shirt" --colors "$C" --y 0.415 --image "$D/Personal Space/oscura.png" --image-light "$D/Personal Space/clara.png"
