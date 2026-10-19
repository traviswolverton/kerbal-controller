# Kerbal controller

KSP1 controller built around KerbalSimpitRevamped. Settled decisions and open items are in
`docs/decisions.md`; the mockup is described in `docs/mockup/README.md`.

## Sourcing parts

- **US only.** When searching for or recommending parts, use US retailers and listings that ship
  within the United States (Amazon.com, Adafruit, SparkFun, Digi-Key, Mouser, PJRC and similar). Do not
  search regional stores outside the US (.au, .uk, .ae, .eu and so on) and do not cite them as sources.
  Pass `allowed_domains` to web searches where it helps.
- **Digi-Key first.** For parts selection use `docs/tools/dk.py` (the Digi-Key API; see `docs/tools/README.md`): it
  gives live US price, stock, lifecycle status and datasheets, and it is more reliable than a retail page. It needs
  credentials in a git-ignored `.env`. If they are missing, say so instead of guessing. Fall back to Amazon.com for
  what Digi-Key does not carry (consumer modules, multi-packs), and say when a price or stock figure came from a web
  page rather than the API. Never print or commit the credentials.
- Quote prices in USD, and only as seen on a US listing. If stock or price was not verified, say so.
- When a part is only on Amazon.com, give its ASIN or URL. The owner is happy to buy there when Digi-Key does not carry it.
