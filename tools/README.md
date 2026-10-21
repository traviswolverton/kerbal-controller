# Tools

> **What this covers:** the parts search and budget tool, the wiring generator, and the staleness check.  
> **Read it if:** you want live prices, or you are changing a generated file. For one-command use see [getting-started](../docs/getting-started.md).  
> **Status:** Tested. The offline tests pass, and both distributor APIs were used live.  
> **Next:** [getting started](../docs/getting-started.md).

## Parts selection: `parts.py` (Digi-Key and Mouser)

Searches Digi-Key and Mouser through their APIs (US sites, USD), keeps a shortlist, and re-checks live price, stock
and status. Standard library only. Digi-Key is the primary source and its parametric data is richer (panel cutout, ratings, mounting); Mouser works
the same way, is simpler to set up, and is the better fallback. Every source that has credentials is searched.

**Status:** both sources are tested live (search, part details, shortlist, check). Digi-Key returned real data on its
first run, including parameters such as panel cutout dimensions, with a daily limit of 1,000 requests that the tool
reports. `make test` (or `python3 -B -m unittest` in this folder) runs the 23 offline tests.

### Setup (an account sign-up, so you do it)

Copy `.env.example` to `.env` in the repo root (it is git-ignored; never commit it) and fill in what you have:

```
MOUSER_API_KEY=your-key
DIGIKEY_CLIENT_ID=your-client-id
DIGIKEY_CLIENT_SECRET=your-client-secret
```

- **Mouser:** create a My Mouser account and request a **Search** API key at https://www.mouser.com/en/api-hub/ (the
  cart and order key is separate). Limits: 50 results per call, 30 calls a minute, 1,000 a day. The tool paces itself.
- **Digi-Key:** register at [developer.digikey.com](https://developer.digikey.com), create an organization and a
  **production** app with the Product Information V4 API (the sandbox returns dummy data). The app form asks for an OAuth
  callback URL; this tool uses the two-legged client-credentials flow and never calls it, so any HTTPS URL such as
  `https://localhost` should do. `DIGIKEY_SANDBOX=true` switches to the sandbox.

Variables already set in your shell win over `.env`. Secrets are never printed, and the Digi-Key access token is cached
under `~/.cache/kerbal-controller/`, outside the repo.

### Use

```
python3 tools/parts.py search "key switch 2 position panel mount" --in-stock --active --max-price 20
python3 tools/parts.py part 612-KO131A102        # parameters, links, price, stock for one part
python3 tools/parts.py add 612-KO131A102 --role "STAGE key switch" --qty 1
python3 tools/parts.py check                     # re-check the shortlist against the live sites
python3 tools/parts.py budget --md               # totals and the full parts list, write hardware/sourcing/parts.md
python3 tools/parts.py amazon-price B0BWDQ3NKK 11.99   # record a price you saw on Amazon
```

- `search` queries every configured source and merges the rows. Filters (`--in-stock`, `--active`, `--max-price`) are
  applied locally. `--source digikey|mouser` limits it to one, and `--json` gives raw rows. If one source fails, the other's
  results still show, with a warning.
- A Digi-Key number ends in `-ND`; anything else is treated as a Mouser number unless you pass `--source`.
- `add` stores the part in `hardware/sourcing/parts-shortlist.json` with a price and stock snapshot.
- `check` flags a part that is no longer Active, below the quantity you need, below the minimum order, or changed in price.
  `--update` saves the new prices.
- `budget` adds the shortlist's stored prices to the hand-kept Amazon list in `hardware/sourcing/amazon-items.json` (Amazon has no price API) and
  writes `hardware/sourcing/parts.md`, the one parts-and-budget document (links, notes, totals). Owned items are listed but not counted, and Amazon items with no price are named, not guessed. `--live`
  re-checks the distributor prices first.
- Mind each service's API terms of use.

Neither distributor stocks everything we use (consumer modules, multi-packs). For those, fall back to Amazon.com and
say the price or stock came from a web page, not an API.

## Wiring docs and firmware pins: `gen_wiring.py`

Reads `hardware/electronics/pinmap.json` (the single source for the Teensy pin assignment and the four DB25 pinouts) and writes
`docs/pinout.html`, `hardware/electronics/wiring/wiring.md`, `hardware/electronics/wiring/diagrams/*.svg`,
`hardware/electronics/wiring/pin-map.md` and `firmware/ksp/include/pins.h`. Run `python3 tools/gen_wiring.py`.
Edit `pinmap.json`, not the outputs.

## Keeping generated files honest: `check_generated.py`

`make check` (or `python3 tools/check_generated.py`) re-runs both generators, compares every generated file with what is committed, puts the old
contents back, and exits 1 listing any that were out of date. CI runs it on every push.
