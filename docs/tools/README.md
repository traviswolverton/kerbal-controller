# Tools

## Parts selection: `parts.py` (Digi-Key and Mouser)

Searches Digi-Key and Mouser through their APIs (US sites, USD), keeps a shortlist, and re-checks live price, stock
and status. Standard library only. Digi-Key is the primary source and its parametric data is richer; Mouser works
the same way and is simpler to set up. Every source that has credentials is searched.

**Status:**
- **Mouser:** tested live (search, part details, shortlist, check).
- **Digi-Key:** written and tested only against a fake API, because the developer portal would not let the owner
  create an app. The field names come from Digi-Key's docs and a community example, and the parser tolerates missing
  fields. Expect a small fix on the first real run.
- **Tests:** `python3 -B -m unittest` in this folder runs 16 offline tests.

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
python3 docs/tools/parts.py search "key switch 2 position panel mount" --in-stock --active --max-price 20
python3 docs/tools/parts.py part 612-KO131A102        # parameters, links, price, stock for one part
python3 docs/tools/parts.py add 612-KO131A102 --role "STAGE key switch" --qty 1
python3 docs/tools/parts.py check --md                # re-check the shortlist, write docs/parts-bom.md
```

- `search` queries every configured source and merges the rows. Filters (`--in-stock`, `--active`, `--max-price`) are
  applied locally. `--source digikey|mouser` limits it to one, and `--json` gives raw rows. If one source fails, the other's
  results still show, with a warning.
- A Digi-Key number ends in `-ND`; anything else is treated as a Mouser number unless you pass `--source`.
- `add` stores the part in `docs/parts-shortlist.json` with a price and stock snapshot.
- `check` flags a part that is no longer Active, below the quantity you need, below the minimum order, or changed in price.
  `--update` saves the new prices.
- Mind each service's API terms of use.

Neither distributor stocks everything we use (consumer modules, multi-packs). For those, fall back to Amazon.com and
say the price or stock came from a web page, not an API.

## Wiring diagrams: `gen_pinout.py`

Generates `docs/pinout.html`, `docs/wiring.md`, `docs/diagrams/*.svg` and `docs/pin-map.md` from one data set.
Run `python3 docs/tools/gen_pinout.py` from the repo root. Edit the data in the script, not the outputs.
