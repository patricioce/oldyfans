#!/usr/bin/env python3
"""Busca en oldyfans.store los colores que ya vende cada diseño y arma map.json para mockups.py.

Uso: python3 -I store_colors.py --input DIR_DISEÑOS --out map.json
Los diseños que no aparecen en la tienda quedan fuera del map (mockups.py usa todos los colores
y descarta solo los de bajo contraste). Imprime una tabla con lo encontrado.
"""
import argparse, json, os, re, sys, urllib.request
from difflib import SequenceMatcher

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mockups import find_designs  # noqa: E402

STORE = 'https://oldyfans.store'


def norm(s):
    s = s.lower().replace('gray', 'grey').replace('t-shirt', '').replace('tee', '')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def fetch_products():
    out, page = [], 1
    while True:
        req = urllib.request.Request(f'{STORE}/products.json?limit=250&page={page}', headers={'User-Agent': 'Mozilla/5.0'})
        ps = json.load(urllib.request.urlopen(req, timeout=30))['products']
        if not ps:
            return out
        out += ps; page += 1


def colors_of(p):
    for i, o in enumerate(p['options']):
        if o['name'].lower() in ('color', 'colour'):
            return sorted({v[f'option{i + 1}'] for v in p['variants']})
    return []


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--input', required=True); ap.add_argument('--out', required=True)
    A = ap.parse_args()
    blanks = json.load(open(os.path.join(HERE, '..', 'assets', 'blanks.json'), encoding='utf-8'))
    bnorm = {norm(b): b for b in blanks}
    products = fetch_products()
    cmap = {}
    for name in find_designs(A.input):
        n = norm(name)
        sim = lambda p: max(SequenceMatcher(None, n, norm(p['title'])).ratio(),   # título o URL del producto
                            SequenceMatcher(None, n, norm(p['handle'].replace('-', ' '))).ratio())
        best = max(products, key=sim); score = sim(best)
        if score < 0.8:
            print(f'{name:<35} NO está en la tienda (más parecido: "{best["title"]}", {score:.2f}) -> todos los colores')
            continue
        store = colors_of(best)
        have = [bnorm[norm(c)] for c in store if norm(c) in bnorm]
        missing = [c for c in store if norm(c) not in bnorm]
        cmap[name] = have
        print(f'{name:<35} = "{best["title"]}" ({STORE}/products/{best["handle"]})')
        print(f'{"":<35}   colores: {", ".join(have)}' + (f'   | SIN mockup vacío: {", ".join(missing)}' if missing else ''))
    json.dump(cmap, open(A.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
