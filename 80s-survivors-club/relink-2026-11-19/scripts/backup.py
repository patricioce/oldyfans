"""Respaldo de los 8 productos sin vincular: JSON completo + una foto por color (para usar como mockups)."""
import json, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shop

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
res = {}
for t in shop.TITULOS:
    r = shop.gql("""query($q:String){ products(first:5, query:$q){ nodes { id handle title status vendor tags
        productType descriptionHtml seo { title description }
        resourcePublicationsV2(first:20){ nodes { isPublished publication { id name } } }
        collections(first:20){ nodes { id title handle ruleSet { appliedDisjunctively } } }
        images(first:50){ nodes { id url altText } }
        options { name values }
        variants(first:100){ nodes { id title sku price compareAtPrice selectedOptions { name value } image { id url } } } } } }""",
                 {"q": f'title:"{t}"'})
    nodes = [n for n in r["data"]["products"]["nodes"] if n["title"] == t]
    assert len(nodes) == 1, (t, len(nodes))
    p = nodes[0]
    res[t] = p
    d = os.path.join(OUT, "mockups", t.replace(" T-Shirt", ""))
    os.makedirs(d, exist_ok=True)
    porcolor = {}
    for v in p["variants"]["nodes"]:
        c = next(o["value"] for o in v["selectedOptions"] if o["name"].lower() == "color")
        porcolor.setdefault(c, set()).add(v["image"]["url"] if v["image"] else None)
    for c, urls in porcolor.items():
        assert len(urls) == 1 and None not in urls, (t, c, urls)
        url = urls.pop()
        ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
        fn = os.path.join(d, f"{t.replace(' T-Shirt', '')} - {c}{ext}")
        local = re.sub(r"^https://cdn\.shopify\.com/s/files/1/[\d/]+/files/", "https://80ssurvivorsclub.com/cdn/shop/files/", url)
        assert local != url, url
        data = urllib.request.urlopen(urllib.request.Request(local, headers={"User-Agent": "Mozilla/5.0"})).read()
        assert len(data) > 10000, (local, len(data))
        open(fn, "wb").write(data)
    print(t, p["id"], p["handle"], p["status"], "| colores:", sorted(porcolor), "| colecciones:",
          [c["title"] for c in p["collections"]["nodes"]], "| canales:",
          [n["publication"]["name"] for n in p["resourcePublicationsV2"]["nodes"] if n["isPublished"]])
json.dump(res, open(os.path.join(OUT, "productos.json"), "w"), indent=1)
