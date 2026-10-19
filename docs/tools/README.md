# Tools

## Digi-Key parts selection: `dk.py`

Searches Digi-Key through its Product Information V4 API (US site, USD), keeps a shortlist, and re-checks live
price, stock and status. Standard library only. Digi-Key is the **primary** source for parts selection: it
returns real price, stock, lifecycle status and datasheet links, which Amazon pages do not give reliably.

**Status:** written and tested offline against a fake API (`python3 -B -m unittest` in this folder). It has not
been run against the live API yet, because that needs your credentials. The response field names come from
Digi-Key's own docs and a community example, and the parser tolerates missing fields.

### One-time setup (you do this, it is an account sign-up)

1. Sign in or register at [developer.digikey.com](https://developer.digikey.com).
2. Create an organization, then an app. Add the **Product Information V4** API to it. Create a **production** app:
   the sandbox returns incomplete or dummy data. The app form asks for an OAuth callback URL; this tool uses the
   two-legged client-credentials flow and never calls it, so any HTTPS URL such as `https://localhost` should do.
3. Copy the app's **Client ID** and **Client Secret** into a file named `.env` in the repo root (it is
   git-ignored; never commit it):

   ```
   DIGIKEY_CLIENT_ID=your-client-id
   DIGIKEY_CLIENT_SECRET=your-client-secret
   ```

   Variables already set in your shell win over `.env`. `DIGIKEY_SANDBOX=true` switches to the sandbox.
   `DIGIKEY_SITE` and `DIGIKEY_CURRENCY` default to `US` and `USD`; keep them, since this project sources from the US.

### Use

```
python3 docs/tools/dk.py search "key switch 2 position panel mount" --in-stock --active --max-price 15
python3 docs/tools/dk.py part 123-456-ND            # parameters, links, price, stock for one part
python3 docs/tools/dk.py add 123-456-ND --role "STAGE key switch" --qty 1
python3 docs/tools/dk.py check --md                 # re-check the shortlist, write docs/digikey-bom.md
```

- `search` is a keyword search. Filters (`--in-stock`, `--active`, `--max-price`) are applied locally. Add
  `--json` for raw rows.
- Use the **Digi-Key part number** (ends in `-ND`) with `part` and `add`: manufacturer numbers can repeat.
- `add` stores the part in `docs/digikey-parts.json` with a price and stock snapshot.
- `check` flags a part that is no longer Active, below the quantity you need, or changed in price. `--update`
  saves the new prices.
- The access token is cached under `~/.cache/kerbal-controller/`, outside the repo, and secrets are never printed.
- The API has rate limits per app. The tool prints the remaining request count when the API reports it. Check your
  app's limit in the developer portal, and mind Digi-Key's API terms of use.

Digi-Key does not stock everything we use (consumer modules, multi-packs, printed-part hardware). For those,
fall back to Amazon.com and say the price or stock came from a web page, not the API.

## Wiring diagrams: `gen_pinout.py`

Generates `docs/pinout.html`, `docs/wiring.md`, `docs/diagrams/*.svg` and `docs/pin-map.md` from one data set.
Run `python3 docs/tools/gen_pinout.py` from the repo root. Edit the data in the script, not the outputs.
