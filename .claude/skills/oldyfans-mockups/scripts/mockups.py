#!/usr/bin/env python3
"""Genera mockups de remeras OldyFans.

Uso:
  python3 -I mockups.py --input DIR --out DIR [--colors "Black,White"] [--map map.json]
                        [--size 2500] [--keep-low-contrast] [--only-report]

--input: carpeta con una subcarpeta por diseño (nombre de la carpeta = nombre del diseño)
         y/o PNGs sueltos (nombre del archivo = nombre del diseño).
         En cada subcarpeta: 1 PNG (va en todos los colores) o 2 PNG (tinta oscura + tinta clara;
         se detecta solo cuál es cuál por luminosidad, no por el nombre).
--map:   JSON {"Nombre diseño": ["Black", "White", ...]} para fijar colores por diseño.
--colors: colores por defecto para los diseños que no están en --map (default: todos).
"""
import argparse, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')
# Posición FIJA del diseño, igual en todas las variantes (escala 0-1000 de la imagen).
# Las remeras de assets/blanks/ ya vienen centradas (center_blanks.py): el centro de cada remera (promedio entre
# centro del cuello y centro del torso) está en x=500 de la imagen, así que el diseño en CX=500 queda centrado en todas.
# Tamaño y altura aprobados por Patricio sobre Slow Me Down y Raised On Hose Water.
# El diseño (recortado a su contenido) entra en un cuadro de BOX de lado, centrado en CX, con su borde de arriba en TOP.
BOX, CX, TOP = 318, 500, 293
INK_ALPHA = 0.96
LOW_CONTRAST = 0.45          # menos que esto: no se lee, se omite
DOUBTFUL = 0.70              # entre LOW_CONTRAST y esto: dudoso, mostrarlo y preguntar


def lum(rgb):
    return rgb[..., 0] * .299 + rgb[..., 1] * .587 + rgb[..., 2] * .114


def load_design(path):
    d = Image.open(path).convert('RGBA')
    bb = d.getchannel('A').getbbox()
    if not bb:
        raise ValueError(f'{path}: PNG sin contenido (todo transparente)')
    return d.crop(bb)


def ink_lum(d):
    a = np.asarray(d.resize((200, 200))).astype(float)
    m = a[..., 3] > 128
    return float(lum(a[..., :3])[m].mean())


def find_designs(root):
    out = {}
    for e in sorted(os.listdir(root)):
        p = os.path.join(root, e)
        if e.startswith(('.', '__MACOSX')):
            continue
        if os.path.isdir(p):
            pngs = []
            for dp, dn, fn in os.walk(p):
                dn[:] = [x for x in dn if not x.startswith(('.', '__MACOSX'))]
                pngs += [os.path.join(dp, f) for f in fn if f.lower().endswith('.png') and not f.startswith('.')]
            if pngs:
                out[e] = sorted(pngs)
        elif e.lower().endswith('.png'):
            out[os.path.splitext(e)[0]] = [p]
    res = {}
    for name, pngs in out.items():
        name = name.removesuffix('.png').removesuffix('.PNG').strip()
        if len(pngs) == 1:
            res[name] = {'dark': pngs[0], 'light': pngs[0], 'single': True}
        else:
            if len(pngs) > 2:
                print(f'AVISO: "{name}" tiene {len(pngs)} PNG; uso el más oscuro y el más claro', file=sys.stderr)
            ls = sorted(pngs, key=lambda f: ink_lum(load_design(f)))
            res[name] = {'dark': ls[0], 'light': ls[-1], 'single': False}
    return res


def blank_geom(base):
    k = base.width / 1000
    return BOX * k, CX * k, TOP * k


def compose(base, d, cfg):
    a = np.asarray(base)
    box, cx, top = blank_geom(base)
    sc = box / max(d.size)
    d = d.resize((max(1, round(d.width * sc)), max(1, round(d.height * sc))), Image.LANCZOS)
    x0, y0 = round(cx - d.width / 2), round(top)
    da = np.asarray(d).astype(float)
    reg = a[y0:y0 + d.height, x0:x0 + d.width].astype(float)
    L = np.asarray(base.convert('L').filter(ImageFilter.GaussianBlur(3))).astype(float)[y0:y0 + d.height, x0:x0 + d.width]
    shade = np.clip(L / np.median(L), .75, 1.15)[..., None]   # arrugas y sombras de la tela sobre la tinta
    ink = np.clip(da[..., :3] * (0.25 + 0.75 * shade), 0, 255)
    al = da[..., 3:] / 255 * INK_ALPHA
    out = a.copy()
    out[y0:y0 + d.height, x0:x0 + d.width] = (reg * (1 - al) + ink * al).astype(np.uint8)
    # contraste: qué parte de la tinta se distingue de la remera
    m = da[..., 3] > 128
    contrast = float((np.abs(lum(da[..., :3]) - np.median(lum(reg)))[m] >= 45).mean()) if m.any() else 0.0
    return Image.fromarray(out), contrast


def sheet(files, path):
    try:
        F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
    except OSError:
        F = ImageFont.load_default()
    n = len(files); cols = min(n, 4); rows = (n + cols - 1) // cols
    c = Image.new('RGB', (500 * cols, 540 * rows), 'white'); dr = ImageDraw.Draw(c)
    for i, (label, f) in enumerate(files):
        x, y = (i % cols) * 500, (i // cols) * 540
        c.paste(Image.open(f).resize((500, 500)), (x, y))
        dr.text((x + 250, y + 520), label, fill='black', font=F, anchor='mm')
    c.save(path, quality=85)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--colors'); ap.add_argument('--map')
    ap.add_argument('--size', type=int, default=2500)
    ap.add_argument('--keep-low-contrast', action='store_true')
    ap.add_argument('--only-report', action='store_true', help='solo calcula contraste, no guarda imágenes')
    A = ap.parse_args()

    blanks = json.load(open(os.path.join(ASSETS, 'blanks.json'), encoding='utf-8'))
    cmap = json.load(open(A.map, encoding='utf-8')) if A.map else {}
    default = [c.strip() for c in A.colors.split(',')] if A.colors else list(blanks)
    for c in default + [c for v in cmap.values() for c in v]:
        if c not in blanks:
            sys.exit(f'Color desconocido: "{c}". Disponibles: {", ".join(blanks)}')

    designs = find_designs(A.input)
    if not designs:
        sys.exit('No encontré PNGs de diseños en ' + A.input)
    os.makedirs(A.out, exist_ok=True)
    cache, report = {}, []
    for name, info in designs.items():
        colors = cmap.get(name, default)
        dk, lt = load_design(info['dark']), load_design(info['light'])
        made = []
        for c in colors:
            cfg = blanks[c]
            if c not in cache:
                cache[c] = Image.open(os.path.join(ASSETS, 'blanks', cfg['file'])).convert('RGB').resize((A.size, A.size), Image.LANCZOS)
            img, ct = compose(cache[c], lt if cfg['light_ink'] else dk, cfg)
            low = ct < LOW_CONTRAST
            report.append({'diseño': name, 'color': c, 'tinta': 'clara' if cfg['light_ink'] and not info['single'] else ('única' if info['single'] else 'oscura'),
                           'contraste': round(ct, 2), 'bajo_contraste': low, 'omitido': low and not A.keep_low_contrast})
            if A.only_report or (low and not A.keep_low_contrast):
                continue
            os.makedirs(os.path.join(A.out, name), exist_ok=True)
            f = os.path.join(A.out, name, f'{name} - {c}.jpg')
            img.save(f, quality=90); made.append((c, f))
        if made:
            sheet(made, os.path.join(A.out, f'{name} - preview.jpg'))
            # simulación del cambio de variante en la tienda: el diseño no debe moverse
            fr = [Image.open(f).convert('RGB').resize((800, 800)) for _, f in made]
            fr[0].save(os.path.join(A.out, f'{name} - cambio de variante.gif'), save_all=True,
                       append_images=fr[1:], duration=1000, loop=0)
    json.dump(report, open(os.path.join(A.out, 'reporte.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for r in report:
        flag = ('  <-- BAJO CONTRASTE' + (' (omitido)' if r['omitido'] else '')) if r['bajo_contraste'] else ('  <-- dudoso' if r['contraste'] < DOUBTFUL else '')
        print(f"{r['diseño']:<35} {r['color']:<15} tinta {r['tinta']:<7} contraste {r['contraste']:.2f}{flag}")


if __name__ == '__main__':
    main()
