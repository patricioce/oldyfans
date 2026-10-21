"""Diseños de solo texto OldyFans: placa de opciones y entrega en PNG.

Uso:
  python3 -I texto.py placa    --spec opciones.json --out placa.png
  python3 -I texto.py entregar --spec opciones.json --opcion 2 --out entrega/ [--colores blanco,negro,mostaza]

El spec (JSON) describe la frase y las opciones; ver SKILL.md.
"""
import argparse, json, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
W = 2400  # ancho de trabajo del bloque de texto (px); la textura está calibrada para este ancho

COLORES = {
    "blanco": (255, 255, 255),
    "negro": (0, 0, 0),
    "mostaza": (226, 166, 20),   # #E2A614, el amarillo aprobado
}
UI_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
UI_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def hex_rgb(s):
    if s in COLORES:
        return COLORES[s]
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def font(name, px=600):
    path = os.path.join(FONTS, name if name.endswith(".ttf") else name + ".ttf")
    if not os.path.exists(path):
        disponibles = sorted(f[:-4] for f in os.listdir(FONTS) if f.endswith(".ttf"))
        sys.exit(f"Tipografía '{name}' no existe. Disponibles: {', '.join(disponibles)}")
    return ImageFont.truetype(path, px)


# ---------------------------------------------------------------- armado

def render_line(text, fontname, tracking=0.0, px=600):
    """Renderiza una línea y la recorta a la tinta. tracking en fracción del tamaño."""
    f = font(fontname, px)
    tr = int(tracking * px)
    widths = [f.getlength(c) for c in text]
    total = int(sum(widths) + tr * (len(text) - 1)) + px
    img = Image.new("L", (total, int(px * 1.6)), 0)
    d = ImageDraw.Draw(img)
    if tr == 0:
        d.text((px // 2, px // 4), text, font=f, fill=255)
    else:
        x = px // 2
        for c, w in zip(text, widths):
            d.text((x, px // 4), c, font=f, fill=255)
            x += w + tr
    return img.crop(img.getbbox())


def _rows(bloques, line_gap, block_gap, width):
    rows = []
    for bi, bloque in enumerate(bloques):
        for li, ln in enumerate(bloque):
            m = render_line(ln["texto"], ln["fuente"], ln.get("tracking", 0))
            if ln.get("modo", "ancho") == "ancho":
                # la línea ocupa el ancho del bloque (x escala)
                tw = int(width * ln.get("escala", 1.0))
                th = round(m.height * tw / m.width)
            else:
                # "alto": altura de mayúscula fija, en fracción del ancho
                th = int(width * ln["alto"])
                tw = round(m.width * th / m.height)
            m = m.resize((tw, th), Image.LANCZOS)
            gap = 0 if (bi == 0 and li == 0) else int(width * (block_gap if li == 0 else line_gap))
            rows.append((m, gap))
    return rows


def _height(bloques, line_gap, block_gap, width):
    return sum(m.height + g for m, g in _rows(bloques, line_gap, block_gap, width))


def balance_bloques(bloques, line_gap, width=W, max_track=0.07):
    """Iguala la altura de las frases (bloques) sumando un poco de tracking a la línea
    'ancho' más alta del bloque más alto. Tope max_track: más que eso desarma la palabra."""
    bloques = [[dict(ln) for ln in b] for b in bloques]
    for _ in range(40):
        hs = [_height([b], line_gap, 0, width) for b in bloques]
        hi, lo = max(range(len(hs)), key=hs.__getitem__), min(hs)
        if hs[hi] <= lo * 1.03:
            break
        fits = [ln for ln in bloques[hi] if ln.get("modo", "ancho") == "ancho" and ln.get("tracking", 0) < max_track]
        if not fits:
            break
        tallest = max(fits, key=lambda ln: _height([[ln]], 0, 0, width))
        tallest["tracking"] = round(tallest.get("tracking", 0) + 0.01, 3)
    return bloques


def build(op, width=W):
    """Máscara L (255 = tinta) de una opción del spec."""
    bloques = op["bloques"]
    lg, bg = op.get("interlineado", 0.035), op.get("separacion_frases", 0.035)
    if op.get("parejas") and len(bloques) > 1:
        bloques = balance_bloques(bloques, lg, width)
    rows = _rows(bloques, lg, bg, width)
    H = sum(m.height + g for m, g in rows)
    Wt = max(m.width for m, _ in rows)
    out = Image.new("L", (Wt, H), 0)
    y = 0
    for m, g in rows:
        y += g
        out.paste(m, ((Wt - m.width) // 2, y))
        y += m.height
    return out


def distress(mask, amount=1.0, seed=7):
    """Textura gastada tipo serigrafía: motas que agujerean la tinta (quedan transparentes)."""
    if amount <= 0:
        return mask
    rng = np.random.default_rng(seed)
    w, h = mask.size
    a = np.asarray(mask, dtype=np.float32) / 255
    n1 = rng.random((h // 5 + 1, w // 5 + 1)).astype(np.float32)
    n1 = np.asarray(Image.fromarray((n1 * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR), dtype=np.float32) / 255
    n2 = rng.random((h // 14 + 1, w // 14 + 1)).astype(np.float32)
    n2 = np.asarray(Image.fromarray((n2 * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
                    .filter(ImageFilter.GaussianBlur(2)), dtype=np.float32) / 255
    thr = 1 - 0.16 * amount
    holes = (n1 > thr) | ((n1 > thr - 0.12 * amount) & (n2 > 0.72))
    a = a * (~holes)
    return Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))


def render(op, idx):
    """Máscara final (con textura) de la opción idx. Misma semilla en placa y entrega."""
    return distress(build(op), op.get("gastado", 1.0), seed=op.get("semilla", 11 + idx))


def colorize(mask, rgb, pad=0.0):
    p = int(max(mask.size) * pad)
    img = Image.new("RGBA", (mask.width + 2 * p, mask.height + 2 * p), rgb + (0,))
    full = Image.new("L", img.size, 0)
    full.paste(mask, (p, p))
    img.putalpha(full)
    return img


# ---------------------------------------------------------------- placa

def placa(spec, out):
    ops = spec["opciones"]
    T, M, head, foot = 900, 60, 170, 130
    cols = min(3, len(ops))
    rows = (len(ops) + cols - 1) // cols
    Wb = cols * T + (cols + 1) * M
    Hb = head + rows * (T + foot) + (rows + 1) * M - 40
    b = Image.new("RGB", (Wb, Hb), (246, 243, 236))
    d = ImageDraw.Draw(b)
    titulo = "OLDYFANS · " + spec["frase"].replace("\n", " ")
    size = 64
    while size > 30:
        fH = ImageFont.truetype(os.path.join(FONTS, "Anton.ttf"), size)
        if d.textlength(titulo, font=fH) <= Wb - 2 * M:
            break
        size -= 4
    fT, fS = ImageFont.truetype(UI_BOLD, 34), ImageFont.truetype(UI_REG, 26)
    d.text((M, 50), titulo, font=fH, fill=(20, 20, 20))
    for i, op in enumerate(ops):
        r, c = divmod(i, cols)
        x, y = M + c * (T + M), head + M + r * (T + foot + M)
        d.rectangle([x, y, x + T, y + T], fill=(255, 255, 255))
        art = colorize(render(op, i), hex_rgb(op.get("color", "mostaza")))
        s = (T * 0.8) / max(art.size)
        art = art.resize((round(art.width * s), round(art.height * s)), Image.LANCZOS)
        b.paste(art, (x + (T - art.width) // 2, y + (T - art.height) // 2), art)
        d.text((x, y + T + 18), f"{op.get('id', i + 1)} · {op.get('titulo', '')}", font=fT, fill=(20, 20, 20))
        d.text((x, y + T + 64), op.get("detalle", ""), font=fS, fill=(110, 110, 110))
    b.save(out)
    print(f"placa: {out} ({len(ops)} opciones)")


# ---------------------------------------------------------------- entrega

def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower().replace("'", "")).strip("-")
    return s or "diseno"


def entregar(spec, opcion, outdir, colores, ancho):
    ops = spec["opciones"]
    idx = next((i for i, o in enumerate(ops) if str(o.get("id", i + 1)) == str(opcion)), None)
    if idx is None:
        sys.exit(f"No hay opción '{opcion}' en el spec.")
    op = ops[idx]
    m = render(op, idx)  # misma máscara y textura que se vio en la placa
    m = m.resize((ancho, round(m.height * ancho / m.width)), Image.LANCZOS)
    a = np.asarray(m, dtype=np.float32)
    m = Image.fromarray(np.clip((a - 128) * 3 + 128, 0, 255).astype(np.uint8))  # bordes nítidos tras escalar
    os.makedirs(outdir, exist_ok=True)
    base = spec.get("nombre") or slug(spec["frase"])
    files = []
    for c in colores:
        img = colorize(m, hex_rgb(c), pad=0.02)
        f = os.path.join(outdir, f"{base}_{c.lstrip('#')}.png")
        img.save(f, dpi=(300, 300))
        files.append((c, f))
        print(f"{c}: {f} {img.size[0]}x{img.size[1]}")
    # vista previa: cada versión sobre remera oscura y clara
    pv = Image.new("RGB", (2000, 1000 * len(files)), (30, 30, 30))
    dd = ImageDraw.Draw(pv)
    for i, (c, f) in enumerate(files):
        dd.rectangle([1000, i * 1000, 2000, (i + 1) * 1000], fill=(235, 232, 225))
        t = Image.open(f)
        t.thumbnail((860, 860))
        for k in range(2):
            pv.paste(t, (k * 1000 + (1000 - t.width) // 2, i * 1000 + (1000 - t.height) // 2), t)
    pf = os.path.join(outdir, f"{base}_preview.png")
    pv.save(pf)
    print(f"preview: {pf}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["placa", "entregar"])
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--opcion")
    ap.add_argument("--colores", default="blanco,negro")
    ap.add_argument("--ancho", type=int, default=4500)
    a = ap.parse_args()
    with open(a.spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    if a.cmd == "placa":
        placa(spec, a.out)
    else:
        if not a.opcion:
            sys.exit("Falta --opcion")
        entregar(spec, a.opcion, a.out, [c.strip() for c in a.colores.split(",") if c.strip()], a.ancho)


if __name__ == "__main__":
    main()
