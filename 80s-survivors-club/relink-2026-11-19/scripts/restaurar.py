"""Deja un producto republicado como estaba antes: ACTIVO, mismos canales, mismas colecciones manuales.
Uso: restaurar.py "<Titulo T-Shirt>" [--apply]"""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shop

D = os.path.dirname(os.path.abspath(__file__))
t = sys.argv[1]
apply = "--apply" in sys.argv
old = json.load(open(os.path.join(D, "relink", "productos.json")))[t]

# vínculo en Printify
PH = {"Authorization": "Bearer " + os.environ["SURVIVORS_PRINTIFY_TOKEN"], "User-Agent": "Claude"}
pp = json.load(urllib.request.urlopen(urllib.request.Request(
    f"https://api.printify.com/v1/shops/29697371/products/{shop.PRINTIFY[t]}.json", headers=PH)))
ext = (pp.get("external") or {}).get("id")
if not ext:
    sys.exit(f"{t}: Printify todavía no tiene external.id: no restauro")
gid = f"gid://shopify/Product/{ext}"

q = """query($id:ID!){ product(id:$id){ id handle title status vendor
  resourcePublicationsV2(first:20){ nodes { isPublished publication { id name } } }
  collections(first:20){ nodes { id title } } images(first:50){ nodes { id } }
  variants(first:100){ nodes { sku price compareAtPrice image { id } } } } }"""
p = shop.gql(q, {"id": gid})["data"]["product"]
if not p:
    sys.exit(f"{t}: el external.id {ext} no existe en Shopify")

pubs_old = {n["publication"]["id"]: n["publication"]["name"] for n in old["resourcePublicationsV2"]["nodes"] if n["isPublished"]}
pubs_new = {n["publication"]["id"] for n in p["resourcePublicationsV2"]["nodes"] if n["isPublished"]}
cols_old = {c["id"]: c["title"] for c in old["collections"]["nodes"] if c["ruleSet"] is None}  # solo manuales
cols_new = {c["id"] for c in p["collections"]["nodes"]}
faltan_pubs = {k: v for k, v in pubs_old.items() if k not in pubs_new}
sobran_pubs = [k for k in pubs_new if k not in pubs_old]
faltan_cols = {k: v for k, v in cols_old.items() if k not in cols_new}
print(f"{t}: Shopify {ext} ({p['handle']}) | estado {p['status']} | vendor {p['vendor']} | fotos {len(p['images']['nodes'])}")
print(f"  canales a agregar: {list(faltan_pubs.values()) or '-'} | canales a quitar: {len(sobran_pubs) or '-'} | colecciones a agregar: {list(faltan_cols.values()) or '-'}")
if not apply:
    print("  SIMULACION"); sys.exit()

for cid in faltan_cols:
    r = shop.gql("mutation($id:ID!,$p:[ID!]!){ collectionAddProducts(id:$id, productIds:$p){ userErrors { message } } }",
                 {"id": cid, "p": [gid]})
    print("  colección", cols_old[cid], r.get("data", r))
if faltan_pubs:
    r = shop.gql("mutation($id:ID!,$in:[PublicationInput!]!){ publishablePublish(id:$id, input:$in){ userErrors { message } } }",
                 {"id": gid, "in": [{"publicationId": k} for k in faltan_pubs]})
    print("  publicar", r.get("data", r))
if sobran_pubs:
    r = shop.gql("mutation($id:ID!,$in:[PublicationInput!]!){ publishableUnpublish(id:$id, input:$in){ userErrors { message } } }",
                 {"id": gid, "in": [{"publicationId": k} for k in sobran_pubs]})
    print("  despublicar", r.get("data", r))
r = shop.gql("mutation($p:ProductInput!){ productUpdate(input:$p){ product { status } userErrors { message } } }",
             {"p": {"id": gid, "status": "ACTIVE"}})
print("  estado", r.get("data", r))

p = shop.gql(q, {"id": gid})["data"]["product"]
vs = p["variants"]["nodes"]
skus_old = {v["sku"] for v in old["variants"]["nodes"]}
ok = (p["status"] == "ACTIVE" and p["handle"] == old["handle"] and p["vendor"] == "80s Survivors Club"
      and all(v["price"] == "29.99" and v["compareAtPrice"] == "42.85" and v["image"] for v in vs)
      and {v["sku"] for v in vs} == skus_old
      and {n["publication"]["id"] for n in p["resourcePublicationsV2"]["nodes"] if n["isPublished"]} == set(pubs_old)
      and set(cols_old) <= {c["id"] for c in p["collections"]["nodes"]})
print(f"  VERIFICADO {t}: {'OK' if ok else 'REVISAR'} | handle {p['handle']} (antes {old['handle']}) | {p['status']} | "
      f"{len(vs)} variantes | fotos {len(p['images']['nodes'])} | canales "
      f"{sorted(n['publication']['name'] for n in p['resourcePublicationsV2']['nodes'] if n['isPublished'])} | "
      f"colecciones {sorted(c['title'] for c in p['collections']['nodes'])}")
