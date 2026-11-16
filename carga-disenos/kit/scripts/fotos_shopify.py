"""Reemplaza las fotos de un producto Shopify activo: sube las nuevas (una por color) y despues borra las viejas.
No toca estado, handle ni variantes. uso: fotos_shopify.py <shopify_id> <carpeta> [--apply]"""
import sys, os, json, base64, time, urllib.request
ST = os.environ['SHOPIFY_ACCESS_TOKEN']; BASE = 'https://s0vk8m-gj.myshopify.com/admin/api/2024-10'
def req(m, u, body=None):
    for i in range(5):
        r = urllib.request.Request(BASE + u, method=m, data=json.dumps(body).encode() if body else None,
                                   headers={'X-Shopify-Access-Token': ST, 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(r, timeout=180) as x:
                t = x.read(); return json.loads(t) if t else {}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < 4: time.sleep(2 ** i); continue
            raise
sid, folder = sys.argv[1], sys.argv[2]; apply = '--apply' in sys.argv
p = req('GET', f'/products/{sid}.json')['product']
ci = [o['name'] for o in p['options']].index('Color') + 1
col = {v['id']: v[f'option{ci}'] for v in p['variants']}
colors = [o for o in p['options'] if o['name'] == 'Color'][0]['values']
old = p['images']
main = col[old[0]['variant_ids'][0]] if old and old[0]['variant_ids'] else colors[0]
files = {c: os.path.join(folder, f) for f in os.listdir(folder) for c in colors if f.rsplit(' - ', 1)[-1][:-4] == c}
orden = [main] + [c for c in colors if c != main]
print(p['handle'], p['status'], '| fotos actuales', len(old), '| principal:', main)
for c in orden: print('  ', c, '->', os.path.basename(files.get(c, '(FALTA)')))
sobran = [f for f in os.listdir(folder) if f.rsplit(' - ', 1)[-1][:-4] not in colors]
if sobran: print('  sin color en el producto (no se suben):', sobran)
if any(c not in files for c in colors): sys.exit('faltan mockups')
if not apply: sys.exit('SIMULACION')
for pos, c in enumerate(orden, 1):
    vids = [v for v, cc in col.items() if cc == c]
    r = req('POST', f'/products/{sid}/images.json', {'image': {'attachment': base64.b64encode(open(files[c], 'rb').read()).decode(),
        'filename': os.path.basename(files[c]).replace(' ', '_'), 'alt': f"{p['title']} - {c}", 'variant_ids': vids}})
    print('  subida', c, r['image']['id'], len(vids), 'variantes')
for im in old:
    req('DELETE', f'/products/{sid}/images/{im["id"]}.json')
print('  borradas', len(old), 'fotos viejas')
new = req('GET', f'/products/{sid}.json')['product']
# orden final: principal primero
for pos, im in enumerate(sorted(new['images'], key=lambda i: orden.index(col[i['variant_ids'][0]])), 1):
    if im['position'] != pos: req('PUT', f'/products/{sid}/images/{im["id"]}.json', {'image': {'id': im['id'], 'position': pos}})
new = req('GET', f'/products/{sid}.json')['product']
print('  final:', new['handle'], new['status'], 'published', bool(new['published_at']), '| fotos', [(i['position'], col[i['variant_ids'][0]], len(i['variant_ids'])) for i in new['images']])
