#!/usr/bin/env python3
"""Crea en Shopify (80s Survivors Club) las colecciones de colecciones.json.

- Agrega a cada producto el tag `col-<handle>` de cada colección a la que pertenece (tagsAdd: no borra tags existentes).
- Crea una smart collection por colección con la regla TAG = col-<handle> (si ya existe una con ese handle, la saltea).
- Publica las colecciones en la tienda online (salvo --unpublished).

Simulación por defecto; --apply escribe.
Env: SURVIVORS_SHOPIFY_CLIENT_ID + SURVIVORS_SHOPIFY_CLIENT_SECRET (genera el token; si no están, usa SURVIVORS_SHOPIFY_ACCESS_TOKEN), SURVIVORS_SHOPIFY_SHOP_DOMAIN (default drysff-xt.myshopify.com).
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

API = "2024-10"
DOMAIN = os.environ.get("SURVIVORS_SHOPIFY_SHOP_DOMAIN", "drysff-xt.myshopify.com")
TOKEN = os.environ.get("SURVIVORS_SHOPIFY_ACCESS_TOKEN", "")
CLIENT_ID = os.environ.get("SURVIVORS_SHOPIFY_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("SURVIVORS_SHOPIFY_CLIENT_SECRET", "")


def token_nuevo():
    """Pide un token de Admin API con client credentials (app del Dev Dashboard; vence a las 24 h)."""
    body = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": CLIENT_ID,
                                   "client_secret": CLIENT_SECRET}).encode()
    req = urllib.request.Request(f"https://{DOMAIN}/admin/oauth/access_token", data=body,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"No pude generar el token (HTTP {e.code}): {e.read()[:300]!r}")
    print(f"Token generado con client credentials · scopes: {d.get('scope', '?')}")
    return d["access_token"]


def gql(query, variables=None, tries=5):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(f"https://{DOMAIN}/admin/api/{API}/graphql.json", data=body,
                                 headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503) and i < tries - 1:
                time.sleep(2 * (i + 1)); continue
            sys.exit(f"HTTP {e.code}: {e.read()[:300]!r}")
        if any(err.get("extensions", {}).get("code") == "THROTTLED" for err in d.get("errors", [])):
            time.sleep(2 * (i + 1)); continue
        if d.get("errors"):
            sys.exit(f"GraphQL: {d['errors']}")
        return d["data"]
    sys.exit("Demasiados reintentos")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--unpublished", action="store_true", help="no publicar las colecciones en la tienda online")
    a = ap.parse_args()
    global TOKEN
    if CLIENT_ID and CLIENT_SECRET:
        TOKEN = token_nuevo()
    if not TOKEN:
        sys.exit("Falta SURVIVORS_SHOPIFY_CLIENT_ID + SURVIVORS_SHOPIFY_CLIENT_SECRET (o SURVIVORS_SHOPIFY_ACCESS_TOKEN)")
    cat = json.load(open(Path(__file__).with_name("colecciones.json")))
    shop = gql("{ shop { name } }")["shop"]["name"]
    print(f"Tienda: {shop} ({DOMAIN})  modo: {'APPLY' if a.apply else 'simulación'}\n")

    # 1) tags en productos
    for name, d in sorted(cat["disenos"].items()):
        want = [f"col-{h}" for h in d["colecciones"]]
        p = gql("query($h:String!){ productByHandle(handle:$h){ id title tags } }", {"h": d["shopify_handle"]})["productByHandle"]
        if not p:
            print(f"  !! no existe en Shopify: {d['shopify_handle']}"); continue
        add = [t for t in want if t not in p["tags"]]
        print(f"  {name:28} +{add if add else ' (ya tiene los tags)'}")
        if a.apply and add:
            r = gql("mutation($id:ID!,$t:[String!]!){ tagsAdd(id:$id,tags:$t){ userErrors{ message } } }", {"id": p["id"], "t": add})
            if r["tagsAdd"]["userErrors"]:
                print("     error:", r["tagsAdd"]["userErrors"])
            time.sleep(0.3)

    # 2) colecciones
    pub_id = None
    if a.apply and not a.unpublished:
        pubs = gql("{ publications(first:20){ nodes{ id name } } }")["publications"]["nodes"]
        pub_id = next((p["id"] for p in pubs if p["name"] == "Online Store"), None)
        if not pub_id:
            print("  !! no encontré la publicación 'Online Store': las colecciones quedan sin publicar")
    print()
    for c in cat["colecciones"]:
        ex = gql("query($h:String!){ collectionByHandle(handle:$h){ id } }", {"h": c["handle"]})["collectionByHandle"]
        if ex:
            print(f"  = {c['titulo']}: ya existe ({ex['id']})"); continue
        print(f"  + {c['titulo']} ({c['handle']}) regla tag = {c['tag']} · {len(c['disenos'])} diseños")
        if not a.apply:
            continue
        r = gql("""mutation($in:CollectionInput!){ collectionCreate(input:$in){ collection{ id } userErrors{ field message } } }""",
                {"in": {"title": c["titulo"], "handle": c["handle"], "descriptionHtml": f"<p>{c['descripcion']}</p>",
                        "ruleSet": {"appliedDisjunctively": False,
                                    "rules": [{"column": "TAG", "relation": "EQUALS", "condition": c["tag"]}]}}})["collectionCreate"]
        if r["userErrors"]:
            print("     error:", r["userErrors"]); continue
        cid = r["collection"]["id"]
        if pub_id:
            e = gql("mutation($id:ID!,$p:ID!){ publishablePublish(id:$id,input:[{publicationId:$p}]){ userErrors{ message } } }",
                    {"id": cid, "p": pub_id})["publishablePublish"]["userErrors"]
            print("     publicada" if not e else f"     no se pudo publicar: {e}")


if __name__ == "__main__":
    main()
