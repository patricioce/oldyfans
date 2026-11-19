"""Cliente mínimo Admin API de 80s Survivors Club (token en memoria)."""
import json, os, time, urllib.request, urllib.parse

DOM = os.environ["SURVIVORS_SHOPIFY_SHOP_DOMAIN"]
V = "2024-10"
_tok = None

TITULOS = ["Wise Man T-Shirt", "I Had Potential T-Shirt", "Warranty Expired T-Shirt", "Metal Slide T-Shirt",
           "I Can Write In Cursive T-Shirt", "Becoming A Legend T-Shirt", "Old School T-Shirt", "Aging Review T-Shirt"]
PRINTIFY = {"Wise Man T-Shirt": "6afd9f475d18cea8e70b12f3", "I Had Potential T-Shirt": "6afd9f6b1cb1d74e0a01b929",
            "Warranty Expired T-Shirt": "6afd9f8e07b4e3e480032442", "Metal Slide T-Shirt": "6afd9fb164b943792d07c948",
            "I Can Write In Cursive T-Shirt": "6afd9fdedfc27cd38c0bf675", "Aging Review T-Shirt": "6afda12fdfc27cd38c0bf727",
            "Old School T-Shirt": "6afda1511cb1d74e0a01ba5d", "Becoming A Legend T-Shirt": "6afda17837262f37de0beedf"}


def http(method, url, headers=None, data=None):
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    for i in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(2 + 2 * i); continue
            return {"_error": e.code, "_body": e.read()[:500].decode("utf8", "replace")}


def token():
    global _tok
    if not _tok:
        body = urllib.parse.urlencode({"grant_type": "client_credentials",
                                       "client_id": os.environ["SURVIVORS_SHOPIFY_CLIENT_ID"],
                                       "client_secret": os.environ["SURVIVORS_SHOPIFY_ACCESS_TOKEN"]}).encode()
        _tok = http("POST", f"https://{DOM}/admin/oauth/access_token",
                    {"Content-Type": "application/x-www-form-urlencoded"}, body)["access_token"]
    return _tok


def H():
    return {"X-Shopify-Access-Token": token(), "Content-Type": "application/json"}


def rest(method, path, body=None):
    return http(method, f"https://{DOM}/admin/api/{V}/{path}", H(), json.dumps(body).encode() if body else None)


def gql(q, v=None):
    return http("POST", f"https://{DOM}/admin/api/{V}/graphql.json", H(),
                json.dumps({"query": q, "variables": v or {}}).encode())
