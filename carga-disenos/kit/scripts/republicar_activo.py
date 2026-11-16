#!/usr/bin/env python3
"""Publica desde Printify los cambios de diseno de un producto que YA esta activo en Shopify,
sin pisar fotos, titulo, descripcion ni tags, y sin pasarlo a borrador.
Despues vigila ~8 min: corrige precio/vendor, borra fotos que agregue Printify y restaura estado/handle si cambian.
uso: republicar_activo.py <printify_id> [--apply]"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import printify_new_product as pf
import shopify_mockups as sm

pid = sys.argv[1]; apply = '--apply' in sys.argv
pr = pf.call('GET', f'/shops/{pf.SHOP_ID}/products/{pid}.json')
sid = int(pr['external']['id'])
F = 'id,title,handle,status,published_at,body_html,tags,images'
antes = sm.shopify('GET', f'/products/{sid}.json?fields={F}')['product']
img_antes = {i['id'] for i in antes['images']}
print(f"{pr['title']} | Shopify {sid} {antes['handle']} {antes['status']} | fotos {len(img_antes)}")
if not apply:
    sys.exit('SIMULACION')
r = pf.call('POST', f'/shops/{pf.SHOP_ID}/products/{pid}/publish.json',
            {'title': False, 'description': False, 'images': False, 'variants': True, 'tags': False,
             'keyfeatures': False, 'shipping_template': False})
print('Publicacion solicitada:', r)

def revisar():
    p = sm.shopify('GET', f'/products/{sid}.json?fields={F}').get('product')
    if not p:  # respuesta transitoria de Shopify: se reintenta en la proxima vuelta
        return []
    cambios = []
    extra = [i for i in p['images'] if i['id'] not in img_antes]
    for i in extra:
        sm.shopify('DELETE', f'/products/{sid}/images/{i["id"]}.json')
    if extra: cambios.append(f'borradas {len(extra)} fotos agregadas por Printify')
    falt = img_antes - {i['id'] for i in p['images']}
    if falt: cambios.append(f'AVISO: faltan {len(falt)} fotos propias')
    fix = {}
    for k in ('title', 'handle', 'body_html', 'tags', 'status'):
        if p[k] != antes[k]: fix[k] = antes[k]
    if bool(p['published_at']) != bool(antes['published_at']): fix['published'] = bool(antes['published_at'])
    if fix:
        sm.shopify('PUT', f'/products/{sid}.json', {'product': {'id': sid, **fix}})
        cambios.append(f'restaurado {sorted(fix)}')
    return cambios

fin = time.time() + 8 * 60
while time.time() < fin:
    time.sleep(30)
    c = revisar()
    if c: print(time.strftime('%H:%M:%S'), '; '.join(c))
ok = sm.fijar_precio_y_vendor(sid)
revisar()
p = sm.shopify('GET', f'/products/{sid}.json?fields={F},vendor')['product']
print(f"FINAL {p['handle']} | estado {p['status']} | en tienda {'si' if p['published_at'] else 'no'} | fotos {len(p['images'])} | "
      f"vendor {p['vendor']} | precio/tachado {'OK' if ok else 'REVISAR'} | fotos propias intactas: {img_antes == {i['id'] for i in p['images']}}")
