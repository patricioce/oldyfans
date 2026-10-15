#!/usr/bin/env python3
"""Centra una foto de remera vacía dentro de la imagen SIN escalarla ni deformarla: solo la desplaza.

Todas las remeras de assets/blanks/ quedan con el cuerpo de la remera en el mismo lugar relativo:
  - horizontal: el promedio entre el centro del cuello (punto medio entre los bordes exteriores del cuello
    acanalado, en su parte más ancha) y el centro del torso (entre los costados, a la altura del pecho) en x=500.
    En casi todas las fotos el cuello está corrido a la izquierda del torso: centrando solo por el cuello el diseño
    se ve corrido a la izquierda, y solo por el torso se ve corrido a la derecha (aprobado así por Patricio).
  - vertical:   el punto medio entre el borde inferior del cuello (adelante) y el ruedo, en y=557
(escala 0-1000). Así, al cambiar de variante en la tienda, la remera no "salta" ni parece más caída.

Paso 1 — medir el cuello (no se detecta bien solo): genera dos tiras ampliadas con regla.
  python3 -I center_blanks.py --src FOTO.jpg --ruler regla
  - regla_v.jpg: leer en qué número termina el borde de abajo del cuello (la costura acanalada) -> --collar
  - regla_h.jpg: leer los bordes exteriores izquierdo y derecho del cuello en su parte más ancha;
    el punto medio es --neck (conviene contrastarlo con el centro de la etiqueta: suelen diferir 0-10).

Paso 2 — centrar y guardar:
  python3 -I center_blanks.py --src FOTO.jpg --name "Color" --collar 150 --neck 490 [--hem 960] [--light-ink]
  --sides / --hem solo si no se detectan solos (ej. remera blanca: fondo y remera casi iguales).
Guarda assets/blanks/<color>.jpg (2500 px) y actualiza assets/blanks.json.
"""
import argparse, json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
SIZE = 2500
TARGET_X, TARGET_Y = 500, 557
# Encuadre: todas las fotos se alejan IGUAL (mismo factor, alrededor del centro de la imagen) para dejar
# margen y que ninguna manga toque el borde. No cambia la posición relativa de las remeras entre sí.
ZOOM = 0.92


def silhouette(im):
    s = np.asarray(im.convert('RGB').resize((1000, 1000)).filter(ImageFilter.GaussianBlur(1))).astype(int)
    return np.abs(s - s[20, 20]).sum(2) > 40


def sides(m):
    L, R = [], []
    for y in range(420, 700, 5):
        x = np.where(m[y, 100:900])[0] + 100
        if len(x):
            L.append(x.min()); R.append(x.max())
    return float(np.median(L)), float(np.median(R))


def hem(m, cx):
    """ruedo: mediana del último píxel de remera en las columnas bajo el torso."""
    cx = int(cx)
    return float(np.median([np.where(m[:, x])[0].max() for x in range(cx - 150, cx + 151, 10) if m[:, x].any()]))


def _strip(im, box, size, ticks, out, vertical):
    a = np.asarray(im.convert('L').resize((2000, 2000)).crop(tuple(v * 2 for v in box))).astype(float)
    lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    a = np.clip((a - lo) / max(hi - lo, 1), 0, 1) ** 0.8 * 255
    c = Image.fromarray(a.astype(np.uint8)).convert('RGB').resize(size); d = ImageDraw.Draw(c)
    k = size[1 if vertical else 0] / (box[3] - box[1] if vertical else box[2] - box[0])
    o = box[1] if vertical else box[0]
    for t in range(ticks[0], ticks[1] + 1, 5):
        p = (t - o) * k; col = (255, 0, 0) if t % 10 == 0 else (255, 170, 0)
        if vertical:
            d.line([(0, p), (size[0] if t % 10 == 0 else 30, p)], fill=col)
            if t % 10 == 0: d.text((size[0] - 35, p + 1), str(t), fill=(255, 0, 0))
        else:
            d.line([(p, 0), (p, size[1] if t % 10 == 0 else 20)], fill=col)
            if t % 10 == 0: d.text((p + 2, size[1] - 14), str(t), fill=(255, 0, 0))
    c.save(out)


def ruler(im, cx, out):
    cx = int(cx)
    _strip(im, (cx - 50, 80, cx + 50, 210), (400, 520), (80, 210), out + '_v.jpg', True)
    _strip(im, (340, 30, 680, 150), (1020, 360), (340, 680), out + '_h.jpg', False)


def shift(im, dx, dy, size=SIZE, zoom=ZOOM):
    """desplaza la foto (dx, dy en escala 0-1000) y la aleja ZOOM alrededor del centro de la imagen.
    Lo que queda fuera de la foto original se rellena estirando su borde, suavizado, para que no se note el corte."""
    im = im.convert('RGB').resize((size, size), Image.LANCZOS)
    P = size // 4
    a = np.pad(np.asarray(im), ((P, P), (P, P), (0, 0)), mode='edge').astype(np.float32)
    soft = np.asarray(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(size / 100))).astype(np.float32)
    m = np.zeros(a.shape[:2], np.uint8); m[P:-P, P:-P] = 255
    m = np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(size / 250))).astype(np.float32)[..., None] / 255
    m = np.minimum(m * 2, 1)
    padded = Image.fromarray((a * m + soft * (1 - m)).astype(np.uint8))
    k = size / 1000; c = size / 2
    # destino = ((origen + desplazamiento) - c) * zoom + c  ->  origen = (destino - c) / zoom + c - desplazamiento
    return padded.transform((size, size), Image.AFFINE,
                            (1 / zoom, 0, c - c / zoom - dx * k + P, 0, 1 / zoom, c - c / zoom - dy * k + P), Image.BICUBIC)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True); ap.add_argument('--name')
    ap.add_argument('--collar', type=float); ap.add_argument('--neck', type=float)
    ap.add_argument('--sides'); ap.add_argument('--hem', type=float)
    ap.add_argument('--ruler'); ap.add_argument('--light-ink', action='store_true')
    A = ap.parse_args()
    im = Image.open(A.src)
    m = silhouette(im)
    L, R = [float(v) for v in A.sides.split(',')] if A.sides else sides(m)
    cx = (L + R) / 2
    if A.ruler:
        ruler(im, cx, A.ruler); print(f'reglas guardadas en {A.ruler}_v.jpg y {A.ruler}_h.jpg'); return
    if not (A.name and A.collar and A.neck):
        ap.error('para centrar hacen falta --name, --collar y --neck (medir antes con --ruler)')
    H = A.hem if A.hem else hem(m, cx)
    dx, dy = TARGET_X - (A.neck + cx) / 2, TARGET_Y - (A.collar + H) / 2
    shift(im, dx, dy).save(os.path.join(ASSETS, 'blanks', A.name.lower().replace(' ', '-') + '.jpg'), quality=92)
    p = os.path.join(ASSETS, 'blanks.json')
    cfg = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    cfg[A.name] = {'file': A.name.lower().replace(' ', '-') + '.jpg', 'light_ink': A.light_ink,
                   'medidas_originales': {'centro_cuello': A.neck, 'centro_torso': round(cx, 1), 'cuello_abajo': A.collar, 'ruedo': round(H), 'torso': [round(L), round(R)]},
                   'desplazamiento': {'dx': round(dx, 1), 'dy': round(dy, 1)}}
    json.dump(cfg, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{A.name:<15} centro cuello {A.neck:.0f} torso {cx:.0f} cuello abajo {A.collar:.0f} ruedo {H:.0f} -> mover x {dx:+.1f}  y {dy:+.1f}')


if __name__ == '__main__':
    main()
