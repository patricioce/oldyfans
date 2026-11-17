"""Perfil de tienda: a que Printify y a que Shopify va la carga.

Se elige con --tienda <nombre> en cualquier script (o la variable TIENDA). Sin nada: oldyfans, igual que siempre.

  oldyfans   Printify 27342731 (PRINTIFY_TOKEN), Shopify con SHOPIFY_* del .env / entorno, Vendor "OldyFans".
  survivors  80s Survivors Club: Printify 29697371 (SURVIVORS_PRINTIFY_TOKEN), Shopify drysff-xt
             (SURVIVORS_SHOPIFY_CLIENT_ID + SURVIVORS_SHOPIFY_CLIENT_SECRET -> token de 24 h por client credentials),
             Vendor "80s Survivors Club". El producto modelo se LEE (solo GET) de la tienda de OldyFans,
             porque los productos son los mismos.
"""
import json, os, subprocess, sys

ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")

PERFILES = {
    "oldyfans": {
        "nombre": "OldyFans",
        "printify_shop_id": lambda: int(os.environ.get("PRINTIFY_SHOP_ID", "27342731")),
        "printify_token_env": "PRINTIFY_TOKEN",
        "modelo_shop_id": lambda: int(os.environ.get("PRINTIFY_SHOP_ID", "27342731")),
        "modelo_token_env": "PRINTIFY_TOKEN",
        "vendor": "OldyFans",
        "shopify_domain_env": "SHOPIFY_SHOP_DOMAIN",
        "shopify_token_env": "SHOPIFY_ACCESS_TOKEN",
        "shopify_client_id_env": None,
        "shopify_client_secret_env": None,
    },
    "survivors": {
        "nombre": "80s Survivors Club",
        "printify_shop_id": lambda: int(os.environ.get("SURVIVORS_PRINTIFY_SHOP_ID", "29697371")),
        "printify_token_env": "SURVIVORS_PRINTIFY_TOKEN",
        "modelo_shop_id": lambda: 27342731,          # modelo "10 p.m T-Shirt" de OldyFans, solo lectura
        "modelo_token_env": "PRINTIFY_TOKEN",
        "vendor": "80s Survivors Club",
        "shopify_domain_env": "SURVIVORS_SHOPIFY_SHOP_DOMAIN",
        "shopify_token_env": "SURVIVORS_SHOPIFY_ACCESS_TOKEN",   # solo si es un shpat_; si es el secret shpss_ se usa como secret
        "shopify_client_id_env": "SURVIVORS_SHOPIFY_CLIENT_ID",
        "shopify_client_secret_env": "SURVIVORS_SHOPIFY_CLIENT_SECRET",
    },
}


def _elegir():
    nombre = os.environ.get("TIENDA", "oldyfans")
    argv = sys.argv
    for i, a in enumerate(list(argv)):
        if a == "--tienda" and i + 1 < len(argv):
            nombre = argv[i + 1]
            del argv[i:i + 2]
            break
        if a.startswith("--tienda="):
            nombre = a.split("=", 1)[1]
            del argv[i]
            break
    nombre = nombre.strip().lower()
    if nombre not in PERFILES:
        sys.exit(f"Tienda desconocida: {nombre!r}. Opciones: {', '.join(PERFILES)}")
    return nombre


def load_env():
    if os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


NOMBRE = _elegir()
P = PERFILES[NOMBRE]
load_env()

NOMBRE_TIENDA = P["nombre"]
VENDOR = P["vendor"]
PRINTIFY_SHOP_ID = P["printify_shop_id"]()
MODELO_SHOP_ID = P["modelo_shop_id"]()


def _env(k, falta_msg=None):
    v = (os.environ.get(k) or "").strip() if k else ""
    if not v and falta_msg:
        sys.exit(falta_msg)
    return v


def printify_token(modelo=False):
    k = P["modelo_token_env"] if modelo else P["printify_token_env"]
    return _env(k, f"Falta {k} (tienda {NOMBRE}): cargarla en las variables de entorno o en .env (ver README.md).")


def shopify_domain():
    k = P["shopify_domain_env"]
    d = _env(k, f"Falta {k} (tienda {NOMBRE}).")
    return d.replace("https://", "").replace("http://", "").strip("/")


def shopify_api_version():
    return os.environ.get("SHOPIFY_API_VERSION", "2024-10")


_shopify_tok = None


def shopify_token():
    """Token de Admin API. OldyFans: SHOPIFY_ACCESS_TOKEN. Survivors: shpat_ directo o client credentials."""
    global _shopify_tok
    if _shopify_tok:
        return _shopify_tok
    tok = _env(P["shopify_token_env"])
    if tok and not tok.startswith("shpss_"):
        _shopify_tok = tok
        return tok
    cid = _env(P["shopify_client_id_env"])
    secret = _env(P["shopify_client_secret_env"]) or (tok if tok.startswith("shpss_") else "")
    if not (cid and secret):
        sys.exit(f"Faltan credenciales de Shopify para {NOMBRE}: {P['shopify_token_env']} "
                 f"o {P['shopify_client_id_env']} + {P['shopify_client_secret_env']}.")
    r = subprocess.run(["curl", "-sS", "-X", "POST", f"https://{shopify_domain()}/admin/oauth/access_token",
                        "-H", "Content-Type: application/x-www-form-urlencoded",
                        "--data-urlencode", "grant_type=client_credentials",
                        "--data-urlencode", f"client_id={cid}",
                        "--data-urlencode", f"client_secret={secret}"],
                       capture_output=True, text=True, timeout=60)
    try:
        _shopify_tok = json.loads(r.stdout)["access_token"]
    except (json.JSONDecodeError, KeyError):
        motivo = "app_not_installed (instalar la app en la tienda)" if "app_not_installed" in r.stdout else r.stdout[:200]
        sys.exit(f"Shopify no dio el token para {NOMBRE}: {motivo}")
    return _shopify_tok


def resumen():
    return (f"Tienda: {NOMBRE_TIENDA} | Printify {PRINTIFY_SHOP_ID} | Shopify {shopify_domain()} | "
            f"modelo leido de Printify {MODELO_SHOP_ID} | Vendor {VENDOR!r}")
