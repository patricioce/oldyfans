"""Reemplaza el diseno de un producto Printify YA publicado (mismo producto, mismos links).
uso: reemplazar_diseno.py <printify_id> <oscura.png> <clara.png> <x> <y> <scale> [--apply]"""
import sys, os, base64, json
sys.path.insert(0, '/home/user/oldyfans/carga-disenos/kit/scripts')
import printify_new_product as P
pid, osc, cla, x, y, sc = sys.argv[1:7]; x, y, sc = float(x), float(y), float(sc)
apply = '--apply' in sys.argv
SH = P.SHOP_ID
p = P.call('GET', f'/shops/{SH}/products/{pid}.json')
color_of = P.colores(p)
todas = [v for pa in p['print_areas'] for v in pa['variant_ids']]
light = ['Black', 'Navy']
habil = sorted({color_of[v['id']] for v in p['variants'] if v['is_enabled']})
print(p['title'], '| colores habilitados:', habil, '| variantes en areas:', len(todas), 'de', len(p['variants']))
grupos = [('oscura', osc, [v for v in todas if color_of.get(v) not in light], None)]
for c in light:
    grupos.append((f'clara-{c.lower()}', cla, [v for v in todas if color_of.get(v) == c], c))
for n, f, vids, c in grupos:
    print(f'  area {n}: {len(vids)} variantes ->', os.path.basename(f), f'x={x} y={y:.4f} scale={sc:.4f}')
if not apply:
    sys.exit('SIMULACION: no se cambio nada.')
areas, esperado = [], []
for n, f, vids, c in grupos:
    if c:
        from PIL import Image
        import io
        im = Image.open(f).convert('RGBA')
        # pixel casi invisible distinto por color: Printify deduplica por contenido
        im.putpixel((light.index(c), 0), (255, 255, 255, 1))
        buf = io.BytesIO(); im.save(buf, format='PNG'); data = buf.getvalue()
    else:
        data = open(f, 'rb').read()
    up = P.call('POST', '/uploads/images.json', {'file_name': n + '.png', 'contents': base64.b64encode(data).decode()})
    if 'id' not in up: sys.exit(f'fallo upload {n}: {str(up)[:300]}')
    print('  subida', n, up['id'])
    if c and any(a['placeholders'][0]['images'][0]['id'] == up['id'] for a in areas): sys.exit('Printify devolvio la misma imagen para Black y Navy')
    areas.append({'variant_ids': vids, 'placeholders': [{'position': 'front', 'images': [
        {'id': up['id'], 'x': x, 'y': y, 'scale': sc, 'angle': 0}]}]})
    if any(v in {w['id'] for w in p['variants'] if w['is_enabled']} for v in vids):
        esperado.append(({v for v in vids if v in {w['id'] for w in p['variants'] if w['is_enabled']}}, up['id'], n + '.png', None))
r = P.call('PUT', f'/shops/{SH}/products/{pid}.json', {'print_areas': areas})
if 'id' not in r: sys.exit(f'Printify rechazo el cambio: {str(r)[:400]}')
print('  print_areas actualizadas')
P.normalizar_areas(pid, set(light), apply=True)
P.verificar_areas(pid, esperado, set(light))
