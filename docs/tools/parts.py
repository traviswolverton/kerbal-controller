#!/usr/bin/env python3
"""Parts selection from Digi-Key and Mouser: search, build a shortlist, re-check price, stock and status.

Standard library only. Credentials come from the environment or the git-ignored .env file (see docs/tools/README.md):
DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET for Digi-Key, MOUSER_API_KEY for Mouser. They are never printed.
Every source that has credentials is searched, Digi-Key first. From the repo root:

    python3 docs/tools/parts.py search "key switch 2 position panel mount" --in-stock --active --max-price 20
    python3 docs/tools/parts.py part 504-10250T15712H620         # details and parameters for one part
    python3 docs/tools/parts.py add 504-10250T15712H620 --role "STAGE key switch" --qty 1
    python3 docs/tools/parts.py check --md                       # live price/stock/status, writes docs/parts-bom.md
    python3 docs/tools/parts.py budget --md                      # combined totals with the Amazon list, writes docs/budget.md

The shortlist is docs/parts-shortlist.json. A Digi-Key number ends in -ND; anything else is treated as a Mouser number
unless you pass --source.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

import digikey
import mouser
from common import REPO, PartsError, is_active, load_env, money, table

SOURCES = {"digikey": digikey, "mouser": mouser}
SHORTLIST = REPO / "docs" / "parts-shortlist.json"
BOM_FILE = REPO / "docs" / "parts-bom.md"
AMAZON_FILE = REPO / "docs" / "amazon-items.json"
BUDGET_FILE = REPO / "docs" / "budget.md"


def active_sources(choice):
    if choice in SOURCES:
        return [choice]
    got = [n for n in SOURCES if SOURCES[n].configured()]
    if not got:
        raise PartsError("no credentials found. Set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET and/or MOUSER_API_KEY "
                         "in .env (see docs/tools/README.md).")
    return got


def guess_source(pn, choice):
    if choice in SOURCES:
        return choice
    return "digikey" if pn.upper().endswith("-ND") else "mouser"


def search_rows(source, keywords, limit, in_stock):
    if source == "digikey":
        return [digikey.row(p) for p in digikey.search(keywords, limit)]
    return [mouser.row(p) for p in mouser.search(keywords, limit, in_stock)]


def fetch_row(source, pn, qty=1):
    mod = SOURCES[source]
    return mod.row(mod.details(pn), pn, qty)


def cmd_search(a):
    rows, notes = [], []
    for src in active_sources(a.source):
        try:
            rows += search_rows(src, a.keywords, a.limit, a.in_stock)
        except PartsError as e:
            notes.append(f"{src}: {e}")
    keep = []
    for r in rows:
        if a.in_stock and not (r["stock"] or 0) > 0:
            continue
        if a.active and not is_active(r["status"]):
            continue
        if a.max_price is not None and (r["unit_price"] is None or r["unit_price"] > a.max_price):
            continue
        keep.append(r)
    if a.json:
        print(json.dumps(keep, indent=2))
    else:
        print(table([(r["source"], r["pn"], r["mpn"][:24], r["manufacturer"][:16], r["description"][:42], r["stock"],
                      money(r["unit_price"]), r["status"]) for r in keep],
                    ["Source", "Part number", "MPN", "Maker", "Description", "Stock", "Unit", "Status"]))
        print(f"\n{len(keep)} shown. Use `part <part number>` for parameters and links.")
    for n in notes:
        print("warning: " + n, file=sys.stderr)


def cmd_part(a):
    src = guess_source(a.pn, a.source)
    r = fetch_row(src, a.pn)
    if a.json:
        print(json.dumps(r, indent=2))
        return
    print(f"{r['mpn']}  ({r['manufacturer']})  [{src}]\n{r['description']}\npart number {r['pn']}  minimum order {r['min_qty']}")
    print(f"stock {r['stock']}  unit {money(r['unit_price'])}  status {r['status']}\n{r['url']}\ndatasheet: {r['datasheet'] or '-'}\n")
    if r.get("variations") and len(r["variations"]) > 1:
        print("packaging options: " + "; ".join(f"{v['pn']} ({v['package']}, min {v['min_qty']})" for v in r["variations"]) + "\n")
    for k, v in r["params"].items():
        print(f"  {k}: {v}")


def load_shortlist():
    return json.loads(SHORTLIST.read_text()) if SHORTLIST.exists() else []


def save_shortlist(parts):
    SHORTLIST.write_text(json.dumps(parts, indent=2) + "\n")


def snapshot(r, qty):
    return {"mpn": r["mpn"], "manufacturer": r["manufacturer"], "description": r["description"],
            "unit_price": r["unit_price"], "stock": r["stock"], "status": r["status"], "url": r["url"],
            "datasheet": r["datasheet"], "qty": qty, "checked": datetime.date.today().isoformat()}


def cmd_add(a):
    src = guess_source(a.pn, a.source)
    r = fetch_row(src, a.pn, a.qty)
    parts = [p for p in load_shortlist() if not (p["pn"] == a.pn and p["source"] == src)]
    parts.append({"role": a.role, "source": src, "pn": a.pn, **snapshot(r, a.qty)})
    save_shortlist(parts)
    print(f"added {a.pn} ({r['mpn']}) from {src} as '{a.role}', qty {a.qty}, {money(r['unit_price'])} each, stock {r['stock']}")


def check_rows(parts, fetch=fetch_row, update=False):
    out, total = [], 0.0
    for p in parts:
        flags = []
        try:
            r = fetch(p["source"], p["pn"], p["qty"])
        except PartsError as e:
            out.append((p["role"], p["source"], p["pn"], p["qty"], "-", "-", "-", "ERROR: " + str(e)[:48]))
            continue
        ext = r["unit_price"] * p["qty"] if r["unit_price"] is not None else None
        if ext is not None:
            total += ext
        if not is_active(r["status"]):
            flags.append(f"status {r['status']}")
        if (r["stock"] or 0) < p["qty"]:
            flags.append("low stock")
        if p["qty"] < (r.get("min_qty") or 1):
            flags.append(f"minimum order {r['min_qty']}")
        if p.get("unit_price") and r["unit_price"] and abs(r["unit_price"] - p["unit_price"]) > 0.005:
            flags.append(f"price was {money(p['unit_price'])}")
        out.append((p["role"], p["source"], p["pn"], p["qty"], money(r["unit_price"]), money(ext), r["stock"],
                    "; ".join(flags) or "ok"))
        if update:
            p.update(snapshot(r, p["qty"]))
    return out, total


def cmd_check(a):
    parts = load_shortlist()
    if not parts:
        print("docs/parts-shortlist.json is empty. Use `add` first.")
        return
    rows, total = check_rows(parts, update=a.update)
    cols = ["Role", "Source", "Part number", "Qty", "Unit", "Extended", "Stock", "Flags"]
    print(table(rows, cols))
    print(f"\nTotal at current prices: {money(total)} (before shipping and tax)")
    if a.update:
        save_shortlist(parts)
    if a.md:
        md = ["# Parts shortlist", "", f"Checked {datetime.date.today().isoformat()} with `docs/tools/parts.py check`. Prices are USD "
              "from the US sites at that time, before shipping and tax.", "", "| " + " | ".join(cols) + " |",
              "|" + "---|" * len(cols)]
        md += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
        md += ["", f"**Total: {money(total)}**", ""]
        BOM_FILE.write_text("\n".join(md))
        print(f"wrote {BOM_FILE.relative_to(REPO)}")


def load_amazon():
    return json.loads(AMAZON_FILE.read_text()) if AMAZON_FILE.exists() else []


def budget_summary(shortlist, amazon):
    """Totals from the stored shortlist prices and the hand-kept Amazon list. Owned items are kept out of the total."""
    dk = [(p["role"], p["qty"], p.get("unit_price"), p["source"], p["pn"]) for p in shortlist]
    dk_total = sum(q * u for _, q, u, _, _ in dk if u is not None)
    buy = [a for a in amazon if a.get("status", "to buy") != "owned"]
    owned = [a for a in amazon if a.get("status") == "owned"]
    priced = [a for a in buy if a.get("unit_price") is not None]
    am_total = sum(a["qty"] * a["unit_price"] for a in priced)
    return {"dk": dk, "dk_total": dk_total, "buy": buy, "owned": owned, "unpriced": [a for a in buy if a.get("unit_price") is None],
            "am_total": am_total, "owned_total": sum(a["qty"] * a["unit_price"] for a in owned if a.get("unit_price") is not None),
            "grand": dk_total + am_total}


def cmd_budget(a):
    parts = load_shortlist()
    if a.live and parts:
        check_rows(parts, update=True)
        save_shortlist(parts)
    b = budget_summary(parts, load_amazon())
    n_un = len(b["unpriced"])
    lines = ["# Budget", "",
             f"Combined order totals, USD, **before shipping and tax**. Digi-Key and Mouser prices come from the shortlist "
             f"(`docs/parts-shortlist.json`, last checked {max((p.get('checked', '') for p in parts), default='never')}); Amazon prices are kept by hand in "
             "`docs/amazon-items.json` because Amazon has no price API. Regenerate with `python3 docs/tools/parts.py budget --md` "
             "(add `--live` to re-check the distributor prices first).", "",
             "| | Lines | Amount |", "|---|---|---|",
             f"| Digi-Key and Mouser | {len(b['dk'])} | {money(b['dk_total'])} |",
             f"| Amazon.com, priced | {len(b['buy']) - n_un} | {money(b['am_total'])} |",
             f"| Amazon.com, **no price yet** | {n_un} | not counted |",
             f"| **Total so far** | | **{money(b['grand'])}** |", ""]
    if n_un:
        lines += [f"The total is a floor: {n_un} Amazon item(s) have no price yet. Set one with "
                  "`python3 docs/tools/parts.py amazon-price ASIN PRICE`.", ""]
    lines += ["## Amazon.com to buy", "", "| Item | ASIN | Qty | Unit | Extended | Note |", "|---|---|---|---|---|---|"]
    for x in b["buy"]:
        u = x.get("unit_price")
        lines.append(f"| {x['item']} | {x['asin']} | {x['qty']} | {money(u) if u is not None else 'unchecked'} | "
                     f"{money(u * x['qty']) if u is not None else '-'} | {x.get('note', '')} |")
    lines += ["", "## Already owned", "", "Not in the total. Prices are the listing price seen, not necessarily what was paid.", "",
              "| Item | ASIN | Qty | Listing price | Note |", "|---|---|---|---|---|"]
    for x in b["owned"]:
        u = x.get("unit_price")
        lines.append(f"| {x['item']} | {x['asin']} | {x['qty']} | {money(u) if u is not None else 'unknown'} | {x.get('note', '')} |")
    lines += ["", "## Digi-Key and Mouser", "", "See [parts-bom.md](parts-bom.md) for the per-line list with stock and flags.", "",
              "| Role | Source | Part number | Qty | Unit | Extended |", "|---|---|---|---|---|---|"]
    for role, q, u, src, pn in b["dk"]:
        lines.append(f"| {role} | {src} | {pn} | {q} | {money(u)} | {money(u * q) if u is not None else '-'} |")
    lines += ["", "## Not counted at all", "", "Solder and flux, cable clips and zip ties, M3 screws and standoffs, silicone feet, filament (2 to 3 kg), "
              "mains-side extras, the stick and encoder connectors, and shipping and tax.", ""]
    text = "\n".join(lines)
    print(f"Digi-Key/Mouser {money(b['dk_total'])} ({len(b['dk'])} lines)   Amazon priced {money(b['am_total'])}   "
          f"Amazon unpriced: {n_un}   TOTAL so far {money(b['grand'])}")
    for x in b["unpriced"]:
        print(f"  no price: {x['item']} x{x['qty']} ({x['asin']})")
    if a.md:
        BUDGET_FILE.write_text(text)
        print(f"wrote {BUDGET_FILE.relative_to(REPO)}")


def cmd_amazon_price(a):
    items = load_amazon()
    hit = [x for x in items if x["asin"] == a.asin]
    if not hit:
        raise PartsError(f"no Amazon item with ASIN {a.asin} in docs/amazon-items.json")
    hit[0]["unit_price"] = a.price
    if a.qty:
        hit[0]["qty"] = a.qty
    if a.owned:
        hit[0]["status"] = "owned"
    AMAZON_FILE.write_text(json.dumps(items, indent=2) + "\n")
    print(f"{hit[0]['item']}: {money(a.price)} x {hit[0]['qty']} ({hit[0].get('status', 'to buy')})")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--source", choices=["auto", *SOURCES], default="auto", help="default: every source with credentials")

    s = sub.add_parser("search", help="keyword search")
    s.add_argument("keywords")
    s.add_argument("--limit", type=int, default=15, help="results per source")
    s.add_argument("--in-stock", action="store_true")
    s.add_argument("--active", action="store_true", help="only parts that are not obsolete or discontinued")
    s.add_argument("--max-price", type=float)
    s.add_argument("--json", action="store_true")
    common(s)
    s.set_defaults(fn=cmd_search)
    s = sub.add_parser("part", help="details for one part number")
    s.add_argument("pn")
    s.add_argument("--json", action="store_true")
    common(s)
    s.set_defaults(fn=cmd_part)
    s = sub.add_parser("add", help="add a part to the shortlist")
    s.add_argument("pn")
    s.add_argument("--role", required=True)
    s.add_argument("--qty", type=int, default=1)
    common(s)
    s.set_defaults(fn=cmd_add)
    s = sub.add_parser("check", help="re-check price, stock and status for the shortlist")
    s.add_argument("--update", action="store_true", help="save the new prices into the shortlist")
    s.add_argument("--md", action="store_true", help="write docs/parts-bom.md")
    s.set_defaults(fn=cmd_check)
    s = sub.add_parser("budget", help="combined totals: shortlist plus the hand-kept Amazon list")
    s.add_argument("--live", action="store_true", help="re-check the distributor prices first")
    s.add_argument("--md", action="store_true", help="write docs/budget.md")
    s.set_defaults(fn=cmd_budget)
    s = sub.add_parser("amazon-price", help="set the price (and optionally quantity) of an Amazon item")
    s.add_argument("asin")
    s.add_argument("price", type=float)
    s.add_argument("--qty", type=int)
    s.add_argument("--owned", action="store_true", help="mark the item as already owned")
    s.set_defaults(fn=cmd_amazon_price)
    a = ap.parse_args(argv)
    load_env()
    try:
        a.fn(a)
    except PartsError as e:
        print("parts: " + str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
