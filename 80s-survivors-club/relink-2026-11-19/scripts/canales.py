"""Publica cada producto ACTIVO en todos los canales que tienen la mayoría (los 5). [--apply]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shop

apply = "--apply" in sys.argv
pubs = shop.gql("{ publications(first:20){ nodes { id name } } }")
if "data" in pubs and pubs["data"]:
    todas = {n["id"]: n["name"] for n in pubs["data"]["publications"]["nodes"]}
else:
    todas = {}
prods, cur = [], None
while True:
    r = shop.gql("""query($c:String){ products(first:100, after:$c){ pageInfo{hasNextPage endCursor}
      nodes { id title status resourcePublicationsV2(first:20){ nodes { isPublished publication { id name } } } } } }""", {"c": cur})
    d = r["data"]["products"]; prods += d["nodes"]
    if not d["pageInfo"]["hasNextPage"]: break
    cur = d["pageInfo"]["endCursor"]
for p in prods:
    for n in p["resourcePublicationsV2"]["nodes"]:
        todas.setdefault(n["publication"]["id"], n["publication"]["name"])
print("Canales:", sorted(todas.values()))
cambios = 0
for p in prods:
    if p["status"] != "ACTIVE":
        continue
    tiene = {n["publication"]["id"] for n in p["resourcePublicationsV2"]["nodes"] if n["isPublished"]}
    faltan = [k for k in todas if k not in tiene]
    if not faltan:
        continue
    cambios += 1
    print(f"{p['title']}: agregar {[todas[k] for k in faltan]}")
    if apply:
        r = shop.gql("mutation($id:ID!,$in:[PublicationInput!]!){ publishablePublish(id:$id, input:$in){ userErrors { field message } } }",
                     {"id": p["id"], "in": [{"publicationId": k} for k in faltan]})
        errs = (r.get("data") or {}).get("publishablePublish", {}).get("userErrors") if r.get("data") else r
        if errs:
            print("   ERRORES:", errs)
print(f"{cambios} productos {'actualizados' if apply else 'a actualizar (SIMULACION)'}")
