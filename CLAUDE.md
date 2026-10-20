# Kerbal controller

KSP1 controller built around KerbalSimpitRevamped. Settled decisions and open items are in
`docs/design/decisions.md`; the mockup is described in `hardware/mockup/README.md`. Layout: `hardware/` (CAD, electronics,
sourcing), `firmware/` (PlatformIO code for the Teensy), `docs/` (decisions, control map, to-do, the Pages site) and `tools/` (scripts).

## Sourcing parts

- **US only.** When searching for or recommending parts, use US retailers and listings that ship
  within the United States (Amazon.com, Adafruit, SparkFun, Digi-Key, Mouser, PJRC and similar). Do not
  search regional stores outside the US (.au, .uk, .ae, .eu and so on) and do not cite them as sources.
  Pass `allowed_domains` to web searches where it helps.
- **Use the APIs first.** For parts selection use `tools/parts.py` (see `tools/README.md`). It searches Digi-Key
  (primary: richer data) and Mouser through their APIs and gives live US price, stock, lifecycle status and datasheets, which
  is more reliable than a retail page. Credentials live in a git-ignored `.env`. If they are missing, say so instead of
  guessing. Fall back to Amazon.com for what the distributors do not carry (consumer modules, multi-packs), and say when a
  price or stock figure came from a web page rather than an API. Never print or commit the credentials.
- Quote prices in USD, and only as seen on a US listing. If stock or price was not verified, say so.
- When a part is only on Amazon.com, give its ASIN or URL. The owner is happy to buy there when Digi-Key does not carry it.
