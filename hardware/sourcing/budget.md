# Budget

Combined order totals, USD, **before shipping and tax**. Digi-Key and Mouser prices come from the shortlist (`hardware/sourcing/parts-shortlist.json`, last checked 2026-10-20); Amazon prices are kept by hand in `hardware/sourcing/amazon-items.json` because Amazon has no price API. Regenerate with `python3 tools/parts.py budget --md` (add `--live` to re-check the distributor prices first).

| | Lines | Amount |
|---|---|---|
| Digi-Key and Mouser | 36 | $328.54 |
| Amazon.com, priced | 5 | $157.51 |
| Amazon.com, **no price yet** | 0 | not counted |
| **Total so far** | | **$486.05** |

## Amazon.com to buy

| Item | ASIN | Qty | Unit | Extended | Note |
|---|---|---|---|---|---|
| JH-D400X-R4 joystick (SaiDian) | B08CGYGMJL | 2 | $18.79 | $37.58 | Price from the listing when chosen. |
| DSA blank keycaps, 1u, 24-pack (Mechkeeb) | B0BWDQ3NKK | 2 | $8.99 | $17.98 | Two packs for 37 caps. Colours to pick. |
| Guarded toggle switches with covers, 6-pack (AITRIP) | B0CL4GNMJX | 1 | $9.99 | $9.99 | ABORT, ENGAGE / DISENGAGE and the master power switch. Check the photos show a bat-handle toggle. |
| 2.42 in OLED 128x64 SSD1309, SPI (Waveshare) | B0CM3RHMGP | 2 | $19.99 | $39.98 | Board outline vs the 58 x 31 mm window unchecked. |
| Weight vest steel plates, 8-pack (Mavee, silver electroplated) | unknown | 2 | $25.99 | $51.98 | Ballast: 8 plates per wing (16 in all, 2 packs, about 3.2 kg); the pocket takes 12 per wing if a third pack is needed. Link: https://a.co/d/0axItt4q (short link, ASIN not resolved). 5.9 x 0.98 x 0.28 in, 0.44 lb each. |

## Already owned

Not in the total. Prices are the listing price seen, not necessarily what was paid.

| Item | ASIN | Qty | Listing price | Note |
|---|---|---|---|---|
| MX-style blue clicky switches, 72-pack (Josojoou) | B0GC33V4HK | 1 | $12.99 | Bought 2026-10-10. 37 used. |
| Passive buzzer module, 5-pack (DIYables) | B0DHGP95K4 | 1 | $6.99 | Ordered 2026-10-10. |
| WS2812B 10 mm pixel boards, 100 (BTF-LIGHTING) | unknown | 1 | unknown | 65 used. |

## Digi-Key and Mouser

See [parts-bom.md](parts-bom.md) for the per-line list with stock and flags.

| Role | Source | Part number | Qty | Unit | Extended |
|---|---|---|---|---|---|
| Teensy 4.1 (headers fitted) | digikey | 1568-20360-ND | 1 | $33.60 | $33.60 |
| 5 V 4 A desktop adapter (Mean Well GST25A05-P1J) | digikey | 1866-2087-ND | 1 | $14.30 | $14.30 |
| Mains cord NEMA 5-15 to IEC C13 for the adapter | digikey | 839-11-00022-ND | 1 | $4.37 | $4.37 |
| Panel DC jack 5.5 x 2.1 mm | digikey | 839-54-00151-ND | 1 | $4.81 | $4.81 |
| Panel fuse holder 5 x 20 mm | digikey | 732-952005000010000-ND | 1 | $2.15 | $2.15 |
| 4 A fuse 5 x 20 mm (1 spare) | digikey | F1724-ND | 2 | $0.57 | $1.14 |
| STAGE key switch (12 mm cutout) | digikey | EG5876-ND | 1 | $7.07 | $7.07 |
| Big STAGE button, 30 mm arcade, red LED | digikey | 1528-2316-ND | 1 | $2.50 | $2.50 |
| Motorised 100 mm fader (Adafruit 5466) | digikey | 1528-5466-ND | 1 | $24.95 | $24.95 |
| L9110H fader driver | digikey | 1528-4489-ND | 1 | $1.50 | $1.50 |
| Conductive nubbin for the fader | digikey | 1528-5741-ND | 1 | $6.19 | $6.19 |
| Rotary encoders (time warp, camera, page) | digikey | PEC11R-4215F-S0024-ND | 3 | $2.95 | $8.85 |
| I2C expander for the switch panel | digikey | MCP23017-E/SP-ND | 1 | $1.69 | $1.69 |
| DIP-28 socket for the expander | digikey | 1175-1490-ND | 1 | $1.29 | $1.29 |
| 74AHCT125 level shifter, DIP | digikey | 296-4655-5-ND | 1 | $1.00 | $1.00 |
| DIP-14 socket for the level shifter | digikey | 1175-1487-ND | 1 | $0.73 | $0.73 |
| Matrix diodes (24 plus spares) | digikey | 1N4148FS-ND | 30 | $0.06 | $1.80 |
| 330 ohm pixel data resistor (1 spare) | digikey | CF14JT330RCT-ND | 2 | $0.10 | $0.20 |
| 4.7 kohm I2C pull-ups (spares) | digikey | CF14JT4K70CT-ND | 3 | $0.10 | $0.30 |
| 10 kohm expander reset pull-up (spares) | digikey | CF14JT10K0CT-ND | 3 | $0.10 | $0.30 |
| 1000 uF 16 V rail capacitor (1 spare) | digikey | 1189-1147-ND | 2 | $0.71 | $1.42 |
| 47 uF 25 V fader driver capacitor (1 spare) | digikey | 732-8823-1-ND | 2 | $0.10 | $0.20 |
| 0.1 uF decoupling and wiper capacitors | digikey | BC1101CT-ND | 12 | $0.17 | $2.04 |
| DB25 female panel jack (middle strip) | digikey | 1003-ZDB25S-ND | 4 | $3.99 | $15.96 |
| DB25 male panel jack (outer pieces) | digikey | 1003-ZDB25P-ND | 4 | $3.42 | $13.68 |
| DB25 shielded cable, female to male, 1 m | digikey | 277-12299-ND | 4 | $15.70 | $62.80 |
| Panel USB micro-B extension for the Teensy | digikey | 1568-15464-ND | 1 | $4.42 | $4.42 |
| Perfboard 94 x 63 mm (middle strip main board) | digikey | 1568-12070-ND | 1 | $8.65 | $8.65 |
| Screw terminal 5.08 mm, 2 position | digikey | ED2609-ND | 6 | $0.58 | $3.48 |
| Screw terminal 5.08 mm, 4 position | digikey | ED2611-ND | 8 | $1.08 | $8.64 |
| Female header 24 position (Teensy sockets, spare) | digikey | S7022-ND | 3 | $1.34 | $4.02 |
| Hookup wire 22 AWG stranded, 10 colours x 25 ft | digikey | 1528-3175-ND | 1 | $32.29 | $32.29 |
| Hookup wire 22 AWG solid, 6 colours x 25 ft (matrix) | digikey | 1528-1743-ND | 1 | $15.95 | $15.95 |
| Heat shrink assortment | digikey | 1528-4559-ND | 1 | $9.95 | $9.95 |
| Encoder knobs, 25 mm D shaft (CLIFF KMK25) | digikey | 4654-FC7254-ND | 3 | $4.90 | $14.70 |
| Perfboard 78 x 58 mm, pad per hole (expander, wing and bus boards) | digikey | 1738-1001-ND | 4 | $2.90 | $11.60 |

## Not counted at all

Solder and flux, cable clips and zip ties, M3 screws and standoffs, silicone feet, filament (2 to 3 kg), mains-side extras, the stick and encoder connectors, and shipping and tax.
