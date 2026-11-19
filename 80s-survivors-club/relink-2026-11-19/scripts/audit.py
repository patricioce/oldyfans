"""Auditoría SOLO LECTURA de 80s Survivors Club (Shopify drysff-xt + Printify 29697371)."""
import json, os, sys, time, urllib.request, urllib.parse

DOM = os.environ["SURVIVORS_SHOPIFY_SHOP_DOMAIN"]
V = "2024-10"


def http(method, url, headers=None, data=None):
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    for i in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2 + i); continue
            return {"_error": e.code, "_body": e.read()[:300].decode("utf8", "replace")}


body = urllib.parse.urlencode({"grant_type": "client_credentials",
                               "client_id": os.environ["SURVIVORS_SHOPIFY_CLIENT_ID"],
                               "client_secret": os.environ["SURVIVORS_SHOPIFY_ACCESS_TOKEN"]}).encode()
tok = http("POST", f"https://{DOM}/admin/oauth/access_token",
           {"Content-Type": "application/x-www-form-urlencoded"}, body)
if "access_token" not in tok:
    sys.exit(f"sin token: {tok}")
SH = {"X-Shopify-Access-Token": tok["access_token"], "Content-Type": "application/json"}
print("SCOPES:", tok.get("scope"))


def rest(path):
    return http("GET", f"https://{DOM}/admin/api/{V}/{path}", SH)


def gql(q, v=None):
    return http("POST", f"https://{DOM}/admin/api/{V}/graphql.json", SH,
                json.dumps({"query": q, "variables": v or {}}).encode())


out = {}
out["shop"] = rest("shop.json")
out["gql_shop"] = gql("""{ shop { name email currencyCode plan { displayName partnerDevelopment shopifyPlus }
  primaryDomain { host sslEnabled } checkoutApiSupported setupRequired taxesIncluded
  billingAddress { country countryCodeV2 } contactEmail
  shopPolicies { type title body url }
  features { storefront } }
  publications(first:20){ nodes { id name } }
}""")
out["locations"] = rest("locations.json")
out["shipping_zones"] = rest("shipping_zones.json")
out["delivery_profiles"] = gql("""{ deliveryProfiles(first:10){ nodes { name default
  productVariantsCount { count }
  profileLocationGroups { locationGroup { locations(first:5){ nodes { name } } }
    locationGroupZones(first:20){ nodes { zone { name countries { code { countryCode restOfWorld } } }
      methodDefinitions(first:20){ nodes { name active rateProvider { ... on DeliveryRateDefinition { price { amount currencyCode } } } } } } } } } } }""")
out["themes"] = rest("themes.json")
out["policies"] = rest("policies.json")
out["pages"] = rest("pages.json?limit=250&fields=id,title,handle,published_at")
out["collections_custom"] = rest("custom_collections.json?limit=250&fields=id,title,handle,published_at")
out["collections_smart"] = rest("smart_collections.json?limit=250&fields=id,title,handle,published_at,rules")
out["menus"] = gql("{ menus(first:20){ nodes { handle title items { title url items { title url } } } } }")
out["payments"] = gql("{ shopifyPaymentsAccount { activated chargeStatementDescriptor country onboardable } }")
out["markets"] = gql("{ markets(first:20){ nodes { name enabled primary } } }")
out["discounts"] = gql("{ discountNodes(first:20){ nodes { discount { __typename ... on DiscountCodeBasic { title status } ... on DiscountAutomaticBasic { title status } ... on DiscountCodeFreeShipping { title status } } } } }")
out["webhooks"] = rest("webhooks.json")
out["apps"] = gql("{ appInstallations(first:30){ nodes { app { title } } } }")
out["fulfillment_services"] = rest("fulfillment_services.json?scope=all")
out["carrier_services"] = rest("carrier_services.json")
out["orders_count"] = rest("orders/count.json?status=any")

# Productos (Admin API)
prods, cur = [], None
while True:
    r = gql("""query($c:String){ products(first:100, after:$c){ pageInfo{hasNextPage endCursor}
      nodes { id handle title status vendor productType tags totalInventory tracksInventory
        onlineStoreUrl publishedAt descriptionHtml
        resourcePublicationsV2(first:10){ nodes { isPublished publication { name } } }
        images(first:50){ nodes { id } }
        collections(first:20){ nodes { title } }
        seo { title description }
        variants(first:100){ nodes { id title price compareAtPrice sku inventoryPolicy
          inventoryQuantity availableForSale image { id }
          inventoryItem { tracked requiresShipping measurement { weight { value unit } } } } } } } }""", {"c": cur})
    if "data" not in r:
        print("ERR productos", r); break
    d = r["data"]["products"]; prods += d["nodes"]
    if not d["pageInfo"]["hasNextPage"]: break
    cur = d["pageInfo"]["endCursor"]
out["products"] = prods

# Printify
PH = {"Authorization": "Bearer " + os.environ["SURVIVORS_PRINTIFY_TOKEN"], "User-Agent": "Claude"}
PB = "https://api.printify.com/v1"
out["pf_shops"] = http("GET", f"{PB}/shops.json", PH)
pf, page = [], 1
while True:
    r = http("GET", f"{PB}/shops/29697371/products.json?limit=50&page={page}", PH)
    if "data" not in r:
        print("ERR printify", r); break
    pf += r["data"]
    if not r.get("next_page_url"): break
    page += 1
for p in pf:
    for k in ("print_areas", "images", "options"):
        p.pop(k, None)
    p["variants"] = [{k: v[k] for k in ("id", "price", "is_enabled", "is_available", "title")} for v in p["variants"]]
out["pf_products"] = pf
out["pf_orders"] = http("GET", f"{PB}/shops/29697371/orders.json?limit=10", PH)

json.dump(out, open(sys.argv[1], "w"), indent=1)
print("productos shopify", len(prods), "| printify", len(pf))
