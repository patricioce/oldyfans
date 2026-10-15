"""Auditoría del catálogo de oldyfans.store a partir de los endpoints públicos de Shopify.

Uso:
  mkdir -p data/js
  for p in 1 2; do curl -s "https://oldyfans.store/products.json?limit=250&page=$p" -o data/p$p.json; done
  python3 -c "import json;json.dump(json.load(open('data/p1.json'))['products']+json.load(open('data/p2.json'))['products'],open('data/all.json','w'))"
  python3 -c "import json;[print(p['handle']) for p in json.load(open('data/all.json'))]" \
    | xargs -P 8 -I{} curl -s "https://oldyfans.store/products/{}.js" -o "data/js/{}.json"
  python3 auditoria_catalogo.py data/all.json ../correcciones data/js
"""
import json,csv,re,collections,sys,unicodedata
ps=json.load(open(sys.argv[1])); out=sys.argv[2]; jsdir=sys.argv[3]
import os
def jsalt(h):
    d=json.load(open(os.path.join(jsdir,h+'.json')))
    return {m['src'].split('?')[0]:(m.get('alt') or '') for m in d.get('media',[])}
def slug(s):
    s=re.sub(r"['’´`]","",s)
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower(); return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def colkey(s): return slug(s)
STD='29.99'; CMP='42.85'
rows_price=[];rows_img=[];rows_alt=[];rows_handle=[];rows_size=[];rows_order=[];rows_colors=[]
SIZES=['S','M','L','XL','2XL','3XL']
palettes=collections.Counter()
for p in ps:
    t=p['title']; h=p['handle']; adm=f"https://admin.shopify.com/store/s0vk8m-gj/products/{p['id']}"
    opts=[o['name'] for o in p['options']]
    ci=opts.index('Color') if 'Color' in opts else None
    si=opts.index('Size') if 'Size' in opts else None
    if opts and opts[0]!='Size': rows_order.append([t,h,' / '.join(opts)])
    colors=collections.OrderedDict()
    for v in p['variants']:
        c=v[f'option{ci+1}'] if ci is not None else '-'
        s=v[f'option{si+1}'] if si is not None else '-'
        colors.setdefault(c,[]).append(s)
        if v['price']!=STD or v['compare_at_price']!=CMP:
            rows_price.append([t,h,c,s,v['sku'],v['price'],v['compare_at_price'],STD,CMP,adm])
        fi=v.get('featured_image')
        if fi and c!='-':
            fn=fi['src'].split('/')[-1].split('?')[0].lower()
            m=re.match(r'\d+-([a-z-]+?)(?:_[0-9a-f-]+)?\.(jpg|png|webp)$',fn)
            if m and not re.match(r'^\d{14}-',fn) and m.group(1)!=colkey(c):
                rows_img.append([t,h,c,s,fn,m.group(1),adm])
    pal=tuple(colors.keys()); palettes[pal]+=1
    for c,ss in colors.items():
        miss=[x for x in SIZES if x not in ss]
        if miss and si is not None: rows_size.append([t,h,c,' '.join(miss),adm])
    vcol={v['id']:(v[f'option{ci+1}'] if ci is not None else '') for v in p['variants']}
    alts=jsalt(h)
    for im in p['images']:
        alt=(alts.get(im['src'].split('?')[0]) or '').strip()
        prob=None
        if not alt: prob='vacío'
        elif re.match(r'^\d{14}-',alt) or re.search(r'[0-9a-f]{8}-[0-9a-f]{4}',alt): prob='código'
        if prob:
            fn=im['src'].split('/')[-1].split('?')[0].lower()
            m=re.match(r'\d+-([a-z-]+?)(?:_[0-9a-f-]+)?\.(jpg|png|webp)',fn)
            cols=sorted({vcol.get(i,'') for i in im.get('variant_ids',[])}-{''})
            col=cols[0] if len(cols)==1 else (m.group(1).replace('-',' ').title() if m and not re.match(r'^\d{14}',fn) else '')
            sug=f"{t} - {col}" if col else t
            rows_alt.append([t,h,im['position'],fn,alt[:60],prob,sug,adm])
    exp=slug(t); core=slug(re.sub(r'\bT-?Shirt\b','',t,flags=re.I))
    issues=[]
    if re.search(r'-\d+$',h): issues.append('sufijo numérico')
    if core and core not in h: issues.append('handle no coincide con título')
    if re.search(r'\s([1-9])\s*(T-?Shirt)?$',t.strip(),re.I): issues.append('título numerado (posible duplicado)')
    if not re.search(r'T-?Shirt',t,re.I): issues.append('sin "T-Shirt"')
    if issues == ['título numerado (posible duplicado)']:
        rows_handle.append([t,h,'(decidir: renombrar o unificar)','; '.join(issues),'',''])
    elif issues:
        new=exp if re.search(r'T-?Shirt',t,re.I) else exp+'-t-shirt'
        rows_handle.append([t,h,new,'; '.join(issues),f"/products/{h}",f"/products/{new}"])
allh={p['handle'] for p in ps}
for r in rows_handle:
    if r[2] in allh: r[3]+='; OJO: el handle sugerido ya existe'
with open(f"{out}/07-redirects-shopify-import.csv",'w',newline='') as f:
    cw=csv.writer(f); cw.writerow(['Redirect from','Redirect to'])
    for r in rows_handle:
        if r[4] and 'OJO' not in r[3]: cw.writerow([r[4],r[5]])
def w(name,hdr,rows):
    with open(f"{out}/{name}",'w',newline='') as f:
        cw=csv.writer(f); cw.writerow(hdr); cw.writerows(rows)
    print(name,len(rows))
w('01-variantes-precio-fuera-de-estandar.csv',['Producto','Handle','Color','Talle','SKU','Precio actual','Tachado actual','Precio estándar','Tachado estándar','Admin'],rows_price)
w('02-variantes-foto-color-incorrecto.csv',['Producto','Handle','Color de la variante','Talle','Archivo de foto asignado','Color que muestra la foto','Admin'],rows_img)
w('03-alt-text-a-corregir.csv',['Producto','Handle','Posición imagen','Archivo','Alt actual','Problema','Alt sugerido','Admin'],rows_alt)
w('04-handles-y-titulos.csv',['Título','Handle actual','Handle sugerido','Problema','Redirect desde','Redirect hacia'],rows_handle)
w('05-talles-faltantes.csv',['Producto','Handle','Color','Talles que faltan','Admin'],rows_size)
w('06-orden-de-opciones-color-talle.csv',['Producto','Handle','Orden actual'],rows_order)
print('paletas:',len(palettes))
for pal,n in palettes.most_common(): print(n,pal)
