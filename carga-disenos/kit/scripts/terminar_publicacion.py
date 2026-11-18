"""Termina una publicacion cuando Printify ya creo el producto en Shopify pero no devuelve external.id
(publicar_existente.py corta con "todavia no esta publicado"). Uso: terminar_publicacion.py <shopify_id> <carpeta_mockups>
Pasa a borrador, fija precio/tachado y Vendor, reemplaza fotos por los mockups y vigila 8 min."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import shopify_mockups as sm
sid, folder = int(sys.argv[1]), sys.argv[2]
sm.hide(sid)
sm.fijar_precio_y_vendor(sid)
sm.upload(sid, folder, apply=True, replace=True)
sm.keep_hidden(sid, minutes=8)
ok = sm.fijar_precio_y_vendor(sid)
p = sm.shopify("GET", f"/products/{sid}.json?fields=id,title,handle,status,published_at,images,vendor").get("product", {})
print(f"Verificado en Shopify: {p.get('title')} ({p.get('handle')}) | estado: {p.get('status')} | "
      f"en tienda online: {'si' if p.get('published_at') else 'no'} | fotos: {len(p.get('images', []))} | "
      f"vendor: {p.get('vendor')} | precio/tachado: {'OK' if ok else 'REVISAR'}")
