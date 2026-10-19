#!/usr/bin/env python3
"""Digi-Key parts selection: search, build a shortlist, and re-check price, stock and status.

Uses the Digi-Key Product Information V4 API with the two-legged OAuth client-credentials flow, and only the
Python standard library. Setup is in docs/tools/README.md. Typical use, from the repo root:

    python3 docs/tools/dk.py search "key switch 2 position panel mount" --in-stock --active
    python3 docs/tools/dk.py part 123-456-ND                  # full details and parameters for one part
    python3 docs/tools/dk.py add 123-456-ND --role "STAGE key switch" --qty 1
    python3 docs/tools/dk.py check --md                       # live price/stock/status, writes docs/digikey-bom.md

The shortlist lives in docs/digikey-parts.json. Credentials come from the environment or a git-ignored .env file
and are never printed or written to the repo.
"""
import argparse
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PARTS_FILE = REPO / "docs" / "digikey-parts.json"
BOM_FILE = REPO / "docs" / "digikey-bom.md"
TOKEN_CACHE = Path(os.environ.get("DIGIKEY_TOKEN_CACHE", Path.home() / ".cache" / "kerbal-controller" / "digikey_token.json"))


class DigiKeyError(Exception):
    pass


# ---- configuration and auth --------------------------------------------------------------------------
def load_env():
    """Read KEY=VALUE lines from <repo>/.env without overriding variables that are already set."""
    f = REPO / ".env"
    if not f.exists():
        return
    for line in f.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def base_url():
    sandbox = os.environ.get("DIGIKEY_SANDBOX", "").lower() in ("1", "true", "yes")
    return "https://sandbox-api.digikey.com" if sandbox else "https://api.digikey.com"


def credentials():
    cid, secret = os.environ.get("DIGIKEY_CLIENT_ID"), os.environ.get("DIGIKEY_CLIENT_SECRET")
    if not cid or not secret:
        raise DigiKeyError("DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET are not set. See docs/tools/README.md.")
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
        raise DigiKeyError(f"token request failed: HTTP {e.code} {e.read().decode(errors='replace')[:200]}") from None
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
            raise DigiKeyError(f"rate limited (HTTP 429). Retry-After: {e.headers.get('Retry-After', '?')} s") from None
        raise DigiKeyError(f"HTTP {e.code} for {method} {path}: {text}") from None


# ---- API calls ----------------------------------------------------------------------------------------
def search(keywords, limit=10):
    return api("POST", "/products/v4/search/keyword",
               {"Keywords": keywords, "Limit": min(limit, 50), "Offset": 0}).get("Products", [])


def details(dkpn):
    d = api("GET", "/products/v4/search/" + urllib.parse.quote(dkpn, safe="") + "/productdetails")
    return d.get("Product", d)


# ---- reading a product, tolerant of missing fields -----------------------------------------------------
def pick_variation(product, dkpn=None):
    vs = product.get("ProductVariations") or []
    if dkpn:
        for v in vs:
            if v.get("DigiKeyProductNumber") == dkpn:
                return v
    return vs[0] if vs else {}


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
        "dkpn": dkpn or v.get("DigiKeyProductNumber") or "",
        "mpn": product.get("ManufacturerProductNumber", ""),
        "manufacturer": (product.get("Manufacturer") or {}).get("Name", ""),
        "description": (product.get("Description") or {}).get("ProductDescription", ""),
        "stock": product.get("QuantityAvailable", v.get("QuantityAvailableforPackageType")),
        "unit_price": price_at(product, qty, dkpn),
        "status": (product.get("ProductStatus") or {}).get("Status", ""),
        "package": (v.get("PackageType") or {}).get("Name", ""),
        "url": product.get("ProductUrl", ""),
        "datasheet": product.get("DatasheetUrl", ""),
        "params": {p.get("ParameterText", ""): p.get("ValueText", "") for p in product.get("Parameters") or []},
    }


def money(x):
    return "-" if x is None else f"${x:,.2f}"


def table(rows, cols):
    widths = [max(len(h), *(len(str(r[i])) for r in rows)) if rows else len(h) for i, h in enumerate(cols)]
    out = ["  ".join(h.ljust(w) for h, w in zip(cols, widths)),
           "  ".join("-" * w for w in widths)]
    out += ["  ".join(str(c).ljust(w) for c, w in zip(r, widths)) for r in rows]
    return "\n".join(out)


# ---- commands ------------------------------------------------------------------------------------------
def cmd_search(a):
    rs = []
    for p in search(a.keywords, a.limit):
        r = row(p)
        if a.in_stock and not (r["stock"] or 0) > 0:
            continue
        if a.active and r["status"].lower() != "active":
            continue
        if a.max_price is not None and (r["unit_price"] is None or r["unit_price"] > a.max_price):
            continue
        rs.append(r)
    if a.json:
        print(json.dumps(rs, indent=2))
        return
    print(table([(r["dkpn"], r["mpn"][:24], r["manufacturer"][:18], r["description"][:46], r["stock"], money(r["unit_price"]),
                  r["status"]) for r in rs], ["Digi-Key PN", "MPN", "Maker", "Description", "Stock", "Unit", "Status"]))
    print(f"\n{len(rs)} shown. Use `part <Digi-Key PN>` for parameters and links.")


def cmd_part(a):
    p = details(a.dkpn)
    r = row(p, a.dkpn)
    if a.json:
        print(json.dumps(r, indent=2))
        return
    print(f"{r['mpn']}  ({r['manufacturer']})\n{r['description']}\nDigi-Key PN {r['dkpn']}  package: {r['package'] or '-'}")
    print(f"stock {r['stock']}  unit {money(r['unit_price'])}  status {r['status']}\n{r['url']}\ndatasheet: {r['datasheet'] or '-'}\n")
    for k, v in r["params"].items():
        print(f"  {k}: {v}")


def load_parts():
    return json.loads(PARTS_FILE.read_text()) if PARTS_FILE.exists() else []


def save_parts(parts):
    PARTS_FILE.write_text(json.dumps(parts, indent=2) + "\n")


def snapshot(r, qty):
    return {"mpn": r["mpn"], "manufacturer": r["manufacturer"], "description": r["description"], "unit_price": r["unit_price"],
            "stock": r["stock"], "status": r["status"], "url": r["url"], "datasheet": r["datasheet"],
            "qty": qty, "checked": datetime.date.today().isoformat()}


def cmd_add(a):
    r = row(details(a.dkpn), a.dkpn, a.qty)
    parts = [p for p in load_parts() if p["dkpn"] != a.dkpn]
    parts.append({"role": a.role, "dkpn": a.dkpn, **snapshot(r, a.qty)})
    save_parts(parts)
    print(f"added {a.dkpn} ({r['mpn']}) as '{a.role}', qty {a.qty}, {money(r['unit_price'])} each, stock {r['stock']}")


def check_rows(parts, fetch=details, update=False):
    out, total = [], 0.0
    for p in parts:
        flags = []
        try:
            r = row(fetch(p["dkpn"]), p["dkpn"], p["qty"])
        except DigiKeyError as e:
            out.append((p["role"], p["dkpn"], "-", "-", "-", "ERROR", str(e)[:50]))
            continue
        ext = r["unit_price"] * p["qty"] if r["unit_price"] is not None else None
        if ext is not None:
            total += ext
        if r["status"].lower() != "active":
            flags.append(f"status {r['status']}")
        if (r["stock"] or 0) < p["qty"]:
            flags.append("low stock")
        if p.get("unit_price") and r["unit_price"] and abs(r["unit_price"] - p["unit_price"]) > 0.005:
            flags.append(f"price was {money(p['unit_price'])}")
        out.append((p["role"], p["dkpn"], p["qty"], money(r["unit_price"]), money(ext), r["stock"], "; ".join(flags) or "ok"))
        if update:
            p.update(snapshot(r, p["qty"]))
    return out, total


def cmd_check(a):
    parts = load_parts()
    if not parts:
        print("docs/digikey-parts.json is empty. Use `add` first.")
        return
    rows, total = check_rows(parts, update=a.update)
    print(table(rows, ["Role", "Digi-Key PN", "Qty", "Unit", "Extended", "Stock", "Flags"]))
    print(f"\nTotal at current prices: {money(total)} (before shipping and tax)")
    if a.update:
        save_parts(parts)
    if a.md:
        md = ["# Digi-Key shortlist", "", f"Checked {datetime.date.today().isoformat()} with `docs/tools/dk.py check`. Prices are USD "
              "from the Digi-Key US site at that time, before shipping and tax.", "",
              "| Role | Digi-Key PN | Qty | Unit | Extended | Stock | Flags |", "|---|---|---|---|---|---|---|"]
        md += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
        md += ["", f"**Total: {money(total)}**", ""]
        BOM_FILE.write_text("\n".join(md))
        print(f"wrote {BOM_FILE.relative_to(REPO)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="keyword search")
    s.add_argument("keywords")
    s.add_argument("--limit", type=int, default=15)
    s.add_argument("--in-stock", action="store_true")
    s.add_argument("--active", action="store_true", help="only parts with status Active")
    s.add_argument("--max-price", type=float)
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_search)
    s = sub.add_parser("part", help="details for one Digi-Key part number")
    s.add_argument("dkpn")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_part)
    s = sub.add_parser("add", help="add a part to the shortlist")
    s.add_argument("dkpn")
    s.add_argument("--role", required=True)
    s.add_argument("--qty", type=int, default=1)
    s.set_defaults(fn=cmd_add)
    s = sub.add_parser("check", help="re-check price, stock and status for the shortlist")
    s.add_argument("--update", action="store_true", help="save the new prices into the shortlist")
    s.add_argument("--md", action="store_true", help="write docs/digikey-bom.md")
    s.set_defaults(fn=cmd_check)
    a = ap.parse_args(argv)
    load_env()
    try:
        a.fn(a)
    except DigiKeyError as e:
        print("digikey: " + str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
