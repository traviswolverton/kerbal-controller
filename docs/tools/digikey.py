"""Digi-Key backend: Product Information V4 API, two-legged OAuth (client credentials), standard library only."""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from common import PartsError

NAME = "digikey"
TOKEN_CACHE = Path(os.environ.get("DIGIKEY_TOKEN_CACHE", Path.home() / ".cache" / "kerbal-controller" / "digikey_token.json"))


def configured():
    return bool(os.environ.get("DIGIKEY_CLIENT_ID") and os.environ.get("DIGIKEY_CLIENT_SECRET"))


# ---- configuration and auth --------------------------------------------------------------------------
def base_url():
    sandbox = os.environ.get("DIGIKEY_SANDBOX", "").lower() in ("1", "true", "yes")
    return "https://sandbox-api.digikey.com" if sandbox else "https://api.digikey.com"


def credentials():
    cid, secret = os.environ.get("DIGIKEY_CLIENT_ID"), os.environ.get("DIGIKEY_CLIENT_SECRET")
    if not cid or not secret:
        raise PartsError("DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET are not set. See docs/tools/README.md.")
    return cid, secret


def get_token(force=False):
    cid, secret = credentials()
    if not force and TOKEN_CACHE.exists():
        try:
            c = json.loads(TOKEN_CACHE.read_text())
            if c.get("client_id") == cid and c.get("expires_at", 0) > time.time() + 60:
                return c["access_token"]
        except (ValueError, KeyError):
            pass
    data = urllib.parse.urlencode({"client_id": cid, "client_secret": secret,
                                   "grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(base_url() + "/v1/oauth2/token", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            tok = json.load(r)
    except urllib.error.HTTPError as e:
        raise PartsError(f"token request failed: HTTP {e.code} {e.read().decode(errors='replace')[:200]}") from None
    TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_CACHE.write_text(json.dumps({"client_id": cid, "access_token": tok["access_token"],
                                       "expires_at": time.time() + int(tok.get("expires_in", 600))}))
    TOKEN_CACHE.chmod(0o600)
    return tok["access_token"]


def api(method, path, body=None, _retry=True):
    cid, _ = credentials()
    headers = {"Authorization": "Bearer " + get_token(), "X-DIGIKEY-Client-Id": cid,
               "Accept": "application/json", "Content-Type": "application/json",
               "X-DIGIKEY-Locale-Site": os.environ.get("DIGIKEY_SITE", "US"),
               "X-DIGIKEY-Locale-Language": "en",
               "X-DIGIKEY-Locale-Currency": os.environ.get("DIGIKEY_CURRENCY", "USD")}
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base_url() + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            left = r.headers.get("X-RateLimit-Remaining")
            if left is not None:
                print(f"[digikey] requests remaining: {left} of {r.headers.get('X-RateLimit-Limit', '?')}", file=sys.stderr)
            return json.load(r)
    except urllib.error.HTTPError as e:
        text = e.read().decode(errors="replace")[:300]
        if e.code == 401 and _retry:
            get_token(force=True)
            return api(method, path, body, _retry=False)
        if e.code == 429:
            raise PartsError(f"rate limited (HTTP 429). Retry-After: {e.headers.get('Retry-After', '?')} s") from None
        raise PartsError(f"HTTP {e.code} for {method} {path}: {text}") from None


# ---- API calls ----------------------------------------------------------------------------------------
def search(keywords, limit=10):
    return api("POST", "/products/v4/search/keyword",
               {"Keywords": keywords, "Limit": min(limit, 50), "Offset": 0}).get("Products", [])


def details(dkpn):
    d = api("GET", "/products/v4/search/" + urllib.parse.quote(dkpn, safe="") + "/productdetails")
    return d.get("Product", d)


# ---- reading a product, tolerant of missing fields -----------------------------------------------------
def pick_variation(product, dkpn=None):
    """The variation for a Digi-Key number, else the one with the lowest minimum order (reels lose to cut tape)."""
    vs = product.get("ProductVariations") or []
    if dkpn:
        for v in vs:
            if v.get("DigiKeyProductNumber") == dkpn:
                return v
    return min(vs, key=lambda v: v.get("MinimumOrderQuantity") or 1, default={})


def price_at(product, qty, dkpn=None):
    """Unit price at a quantity from the standard price breaks; falls back to the product's UnitPrice."""
    v = pick_variation(product, dkpn)
    breaks = sorted(v.get("StandardPricing") or [], key=lambda b: b.get("BreakQuantity", 0))
    best = None
    for b in breaks:
        if b.get("BreakQuantity", 0) <= qty:
            best = b
    if best is None and breaks:
        best = breaks[0]
    if best and best.get("UnitPrice") is not None:
        return float(best["UnitPrice"])
    up = product.get("UnitPrice")
    return float(up) if up is not None else None


def row(product, dkpn=None, qty=1):
    v = pick_variation(product, dkpn)
    return {
        "source": NAME,
        "pn": dkpn or v.get("DigiKeyProductNumber") or "",
        "mpn": product.get("ManufacturerProductNumber", ""),
        "manufacturer": (product.get("Manufacturer") or {}).get("Name", ""),
        "description": (product.get("Description") or {}).get("ProductDescription", ""),
        "stock": product.get("QuantityAvailable", v.get("QuantityAvailableforPackageType")),
        "unit_price": price_at(product, qty, dkpn),
        "status": (product.get("ProductStatus") or {}).get("Status", ""),
        "min_qty": v.get("MinimumOrderQuantity", 1),
        "variations": [{"pn": x.get("DigiKeyProductNumber", ""), "package": (x.get("PackageType") or {}).get("Name", ""),
                        "min_qty": x.get("MinimumOrderQuantity", 1)} for x in product.get("ProductVariations") or []],
        "package": (v.get("PackageType") or {}).get("Name", ""),
        "url": product.get("ProductUrl", ""),
        "datasheet": product.get("DatasheetUrl", ""),
        "params": {p.get("ParameterText", ""): p.get("ValueText", "") for p in product.get("Parameters") or []},
    }
