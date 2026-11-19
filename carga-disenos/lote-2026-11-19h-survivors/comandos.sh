#!/bin/bash
# Desde carga-disenos/kit. Sin argumento: simulacion. Con "--create": crea en Printify (sin publicar).
D=../lote-2026-11-19h-survivors/disenos; C="Black,Charcoal,Military Green,Navy,Sport Grey,White"; P="python3 scripts/printify_new_product.py --tienda survivors"
$P "$@" --title "Bigfoot T-Shirt" --colors "Sport Grey,White" --y 0.387 --image "$D/Bigfoot/unica.png"
$P "$@" --title "No Photos Please T-Shirt" --colors "$C" --y 0.340 --image "$D/No Photos Please/oscura.png" --image-light "$D/No Photos Please/clara.png"
$P "$@" --title "Odd Duck T-Shirt" --colors "Military Green,Sport Grey,White" --scale 0.57 --y 0.452 --image "$D/Odd Duck/unica.png"
$P "$@" --title "Retirement Definition T-Shirt" --colors "$C" --image "$D/Retirement Definition/oscura.png" --image-light "$D/Retirement Definition/clara.png"
$P "$@" --title "Retirement Review T-Shirt" --colors "$C" --image "$D/Retirement Review/oscura.png" --image-light "$D/Retirement Review/clara.png"
