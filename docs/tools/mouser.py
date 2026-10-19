"""Mouser backend: Search API (API key in the query string), standard library only.

Limits per Mouser: 50 results per call, 30 calls a minute, 1,000 a day. The key comes from MOUSER_API_KEY.
"""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from common import PartsError

NAME = "mouser"
BASE = "https://api.mouser.com/api/v1"
_last_call = [0.0]


def configured():
    return bool(os.environ.get("MOUSER_API_KEY"))


def api(path, body):
    key = os.environ.get("MOUSER_API_KEY")
    if not key:
        raise PartsError("MOUSER_API_KEY is not set. See docs/tools/README.md.")
    wait = 2.1 - (time.time() - _last_call[0])          # stay under 30 calls a minute
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(f"{BASE}{path}?apiKey={urllib.parse.quote(key)}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        raise PartsError(f"HTTP {e.code} for {path}: {e.read().decode(errors='replace')[:200].replace(key, '***')}") from None
    finally:
        _last_call[0] = time.time()
    errs = data.get("Errors") or []
    if errs:
        raise PartsError("Mouser: " + "; ".join(str(e.get("Message", e)) for e in errs)[:200])
    return data


def search(keywords, limit=10, in_stock=False):
    body = {"SearchByKeywordRequest": {"keyword": keywords, "records": min(limit, 50), "startingRecord": 0,
                                       "searchOptions": "InStock" if in_stock else "None",
                                       "searchWithYourSignUpLanguage": "false"}}
    return (api("/search/keyword", body).get("SearchResults") or {}).get("Parts") or []


def details(pn):
    body = {"SearchByPartRequest": {"mouserPartNumber": pn, "partSearchOptions": "Exact"}}
    parts = (api("/search/partnumber", body).get("SearchResults") or {}).get("Parts") or []
    for p in parts:
        if p.get("MouserPartNumber", "").lower() == pn.lower():
            return p
    if parts:
        return parts[0]
    raise PartsError(f"Mouser has no part {pn}")


def _num(s):
    m = re.sub(r"[^0-9.]", "", (s or "").replace(",", ""))
    return float(m) if m else None


def price_at(part, qty):
    breaks = sorted(part.get("PriceBreaks") or [], key=lambda b: b.get("Quantity", 0))
    best = None
    for b in breaks:
        if b.get("Quantity", 0) <= qty:
            best = b
    if best is None and breaks:
        best = breaks[0]
    return _num(best.get("Price")) if best else None


def stock_of(part):
    n = _num(str(part.get("AvailabilityInStock") or ""))
    if n is None:
        n = _num((part.get("Availability") or "").split(" ")[0])
    return int(n or 0)


def row(part, pn=None, qty=1):
    status = (part.get("LifecycleStatus") or "").strip() or "Active"
    return {
        "source": NAME,
        "pn": pn or part.get("MouserPartNumber", ""),
        "mpn": part.get("ManufacturerPartNumber", ""),
        "manufacturer": part.get("Manufacturer", ""),
        "description": part.get("Description", ""),
        "stock": stock_of(part),
        "unit_price": price_at(part, qty),
        "status": status,
        "min_qty": int(_num(str(part.get("Min") or "1")) or 1),
        "package": "",
        "url": part.get("ProductDetailUrl", ""),
        "datasheet": part.get("DataSheetUrl", ""),
        "params": {a.get("AttributeName", ""): a.get("AttributeValue", "") for a in part.get("ProductAttributes") or []},
    }
