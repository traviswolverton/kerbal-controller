# Parts and budget

Every part for the console, in one list. Sources are US retailers only: **Digi-Key** (primary, with Mouser as a back-up) through their APIs, and Amazon.com for what they do not carry. Prices are USD, **before shipping and tax**. Digi-Key and Mouser prices and stock are the shortlist snapshot from 2026-10-21; Amazon prices are kept by hand because Amazon has no price API. This file is generated: edit the data and notes in `parts-shortlist.json` and `amazon-items.json`, then run `python3 tools/parts.py budget --md` (add `--live` to re-check the distributors first). Design context is in `docs/design/decisions.md`.

## Totals

| | Lines | Amount |
|---|---|---|
| Digi-Key and Mouser | 36 | $400.03 |
| Amazon.com, priced | 4 | $117.53 |
| Amazon.com, **no price yet** | 0 | not counted |
| **Total so far** | | **$517.56** |

## Digi-Key and Mouser

| Part | Part number | Qty | Unit | Extended | Stock | Notes |
|---|---|---|---|---|---|---|
| Teensy 4.1 (headers fitted) | [1568-20360-ND](https://www.digikey.com/en/products/detail/sparkfun-electronics/20360/16688096) | 1 | $33.60 | $33.60 | 85 | 3.3 V pins, not 5 V tolerant. No `touchRead()` on 4.x. 16771 is the same board without headers, $31.50. |
| 5 V 4 A desktop adapter (Mean Well GST25A05-P1J) | [1866-2087-ND](https://www.digikey.com/en/products/detail/mean-well-usa-inc/GST25A05-P1J/7703645) | 1 | $14.30 | $14.30 | 3038 | Positive centre, 2.1 x 5.5 mm plug, 1 m lead, cULus. IEC C14 inlet, **cord sold separately**. |
| Mains cord NEMA 5-15 to IEC C13 for the adapter | [839-11-00022-ND](https://www.digikey.com/en/products/detail/tensility/11-00022/3900584) | 1 | $4.37 | $4.37 | 3557 | For the adapter. |
| Panel DC jack 5.5 x 2.1 mm | [839-54-00151-ND](https://www.digikey.com/en/products/detail/tensility/54-00151/9829987) | 1 | $4.81 | $4.81 | 6626 | 7.5 A, solder cup, rear nut. **Panel cutout (datasheet, read 2026-10-20):** 10.9 mm round with two flats 9.8 mm apart, panel 1.5 to 4.5 mm, M11 nut. |
| Panel fuse holder 5 x 20 mm | [732-952005000010000-ND](https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/952005000010000/28172649) | 1 | $2.15 | $2.15 | 1923 | On the 5 V rail. **Panel hole (datasheet, read 2026-10-20):** 13 mm round with a 1.8 mm key out to 14 mm, panel 0.8 to 2.8 mm. |
| 4 A fuse 5 x 20 mm (1 spare) | [F1724-ND](https://www.digikey.com/en/products/detail/littelfuse-inc/0217004-MXP/777547) | 2 | $0.57 | $1.14 | 19717 | One spare. Rated for AC; fine at 5 V DC. |
| STAGE key switch (12 mm cutout) | [EG5876-ND](https://www.digikey.com/en/products/detail/e-switch/KO133A801/1804779) | 1 | $7.07 | $7.07 | 458 | 2-position SPST, **12 mm cutout**, key removable in position 1 only. Confirm in the datasheet that position 1 is OFF. |
| Big STAGE button, 30 mm arcade, red LED | [1528-2316-ND](https://www.digikey.com/en/products/detail/adafruit-industries-llc/3489/7349495) | 1 | $2.50 | $2.50 | 355 | **30 mm cutout**, 5 V LED, 2.8 mm quick-connect tabs. LED wiring is open (always on, or driven later). |
| Motorised 100 mm fader (Adafruit 5466) | [1528-5466-ND](https://www.digikey.com/en/products/detail/adafruit-industries-llc/5466/16645060) | 1 | $24.95 | $24.95 | 37 | 6-10 V motor, run at 5 V. Two M3 holes 120 mm apart. Only 37 in stock. |
| L9110H fader driver | [1528-4489-ND](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4489/11594498) | 1 | $1.50 | $1.50 | 928 | Next to the fader motor. |
| Conductive nubbin for the fader | [1528-5741-ND](https://www.digikey.com/en/products/detail/adafruit-industries-llc/5741/20370638) | 1 | $6.19 | $6.19 | 36 | For touch sensing. Only 37 in stock. |
| Rotary encoders (time warp, camera, page) | [PEC11R-4215F-S0024-ND](https://www.digikey.com/en/products/detail/bourns-inc/PEC11R-4215F-S0024/4499665) | 3 | $2.95 | $8.85 | 12317 | 24 detents, 6 mm flatted shaft. Bushing only about 5 mm long: keep the panel about 3 mm at the encoders. |
| I2C expander for the switch panel | [MCP23017-E/SP-ND](https://www.digikey.com/en/products/detail/microchip-technology/MCP23017-E-SP/894272) | 1 | $1.69 | $1.69 | 7927 | Replaces the breakout board: hand-wired on perfboard behind the switch panel. |
| DIP-28 socket for the expander | [1175-1490-ND](https://www.digikey.com/en/products/detail/cnc-tech/245-28-1-06/3441586) | 1 | $1.29 | $1.29 | 1569 | For the expander. |
| 74AHCT125 level shifter, DIP | [296-4655-5-ND](https://www.digikey.com/en/products/detail/texas-instruments/SN74AHCT125N/375798) | 1 | $1.00 | $1.00 | 20099 | Pixel data line. |
| DIP-14 socket for the level shifter | [1175-1487-ND](https://www.digikey.com/en/products/detail/cnc-tech/245-14-1-03/3441580) | 1 | $0.73 | $0.73 | 5730 | For the level shifter. |
| Matrix diodes (24 plus spares) | [1N4148FS-ND](https://www.digikey.com/en/products/detail/onsemi/1N4148/458603) | 30 | $0.06 | $1.80 | 595777 | 24 matrix diodes plus spares. |
| 330 ohm pixel data resistor (1 spare) | [CF14JT330RCT-ND](https://www.digikey.com/en/products/detail/stackpole-electronics-inc/CF14JT330R/1741399) | 2 | $0.10 | $0.20 | 283061 | Pixel data series resistor, one spare. |
| 4.7 kohm I2C pull-ups (spares) | [CF14JT4K70CT-ND](https://www.digikey.com/en/products/detail/stackpole-electronics-inc/CF14JT4K70/1741428) | 3 | $0.10 | $0.30 | 248594 | SDA and SCL pull-ups, one spare. |
| 10 kohm expander reset pull-up (spares) | [CF14JT10K0CT-ND](https://www.digikey.com/en/products/detail/stackpole-electronics-inc/CF14JT10K0/1741265) | 3 | $0.10 | $0.30 | 566429 | Expander reset pull-up, spares. |
| 1000 uF 16 V rail capacitor (1 spare) | [1189-1147-ND](https://www.digikey.com/en/products/detail/rubycon/16ZLH1000MEFC10X16/3134105) | 2 | $0.71 | $1.42 | 15844 | 5 V rail, one spare. |
| 47 uF 25 V fader driver capacitor (1 spare) | [732-8823-1-ND](https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/860020472006/5727060) | 2 | $0.10 | $0.20 | 34958 | Across the fader driver's supply, one spare. |
| 0.1 uF decoupling and wiper capacitors | [BC1101CT-ND](https://www.digikey.com/en/products/detail/vishay-beyschlag-draloric-bc-components/K104K15X7RF5TH5/286555) | 12 | $0.17 | $2.04 | 304643 | Decoupling, and one per stick and fader wiper. |
| DB25 female panel jack (middle strip) | [1003-ZDB25S-ND](https://www.digikey.com/en/products/detail/itt-cannon-llc/ZDB25S/21361496) | 8 | $3.99 | $31.92 | 1587 | Middle strip, one per outer piece. Doubled to 8 (4 to fit plus 4 spares) so you can practise soldering the cups on 1 or 2 before the real ones. |
| DB25 male panel jack (outer pieces) | [1003-ZDB25P-ND](https://www.digikey.com/en/products/detail/itt-cannon-llc/ZDB25P/21361449) | 8 | $3.42 | $27.36 | 3640 | One on each outer piece. Doubled to 8 (4 to fit plus 4 spares) so you can practise soldering the cups on 1 or 2 before the real ones. |
| DB25 shielded cable, female to male, 1 m | [277-12299-ND](https://www.digikey.com/en/products/detail/phoenix-contact/1656291/4449846) | 4 | $15.70 | $62.80 | 1227 | Straight-through, 25 conductors. Male end into a middle jack, female end onto an outer jack. |
| Panel USB micro-B extension for the Teensy | [1568-15464-ND](https://www.digikey.com/en/products/detail/sparkfun-electronics/15464/10440474) | 1 | $4.42 | $4.42 | 1666 | For the Teensy. |
| Perfboard 94 x 63 mm (middle strip main board) | [1568-12070-ND](https://www.digikey.com/en/products/detail/sparkfun-electronics/12070/5230951) | 1 | $8.65 | $8.65 | 713 |  |
| Screw terminal 5.08 mm, 2 position | [ED2609-ND](https://www.digikey.com/en/products/detail/on-shore-technology-inc/OSTTC022162/614558) | 6 | $0.58 | $3.48 | 36435 |  |
| Screw terminal 5.08 mm, 4 position | [ED2611-ND](https://www.digikey.com/en/products/detail/on-shore-technology-inc/OSTTC042162/614560) | 8 | $1.08 | $8.64 | 12672 |  |
| Female header 24 position (Teensy sockets, spare) | [S7022-ND](https://www.digikey.com/en/products/detail/sullins-connector-solutions/PPTC241LFBN-RC/810162) | 3 | $1.34 | $4.02 | 20324 |  |
| Hookup wire 22 AWG stranded, 10 colours x 25 ft | [1528-3175-ND](https://www.digikey.com/en/products/detail/adafruit-industries-llc/3175/6198258) | 1 | $32.29 | $32.29 | 470 |  |
| Hookup wire 22 AWG solid, 6 colours x 25 ft (matrix) | [1528-1743-ND](https://www.digikey.com/en/products/detail/adafruit-industries-llc/1311/6198255) | 1 | $15.95 | $15.95 | 2420 |  |
| Encoder knobs, 25 mm D shaft (CLIFF KMK25) | [4654-FC7254-ND](https://www.digikey.com/en/products/detail/cliff-electronic-components-ltd/FC7254/21406846) | 3 | $4.90 | $14.70 | 9 | 6 mm D shaft, knurled aluminium, matches the mockup's 25 x 15 mm proxy. Only 9 in stock; silver only (the smaller KMK10E FC7259 comes in black). Set screw not confirmed. |
| Perfboard 78 x 58 mm, pad per hole (expander, wing and bus boards) | [1738-1001-ND](https://www.digikey.com/en/products/detail/dfrobot/FIT0203/6588423) | 4 | $2.90 | $11.60 | 3322 |  |
| 3.5in IPS TFT display 480x320 SPI (DFRobot DFR0669) | [1738-DFR0669-ND](https://www.digikey.com/en/products/detail/dfrobot/DFR0669/13280137) | 2 | $25.90 | $51.80 | 117 | 480 x 320, ILI9488, SPI, 73.44 x 48.96 mm display area, board 55.5 x 95 mm with 2 mm holes on a 90 x 50 mm pitch (DFRobot wiki). Capacitive touch and SD pins unused. 117 in stock. Window planned at 75 x 50 mm: measure where the display area sits relative to the holes. |

## Amazon.com to buy

| Item | Listing | Qty | Unit | Extended | Note |
|---|---|---|---|---|---|
| JH-D400X-R4 joystick (SaiDian) | [B08CGYGMJL](https://www.amazon.com/dp/B08CGYGMJL) | 2 | $18.79 | $37.58 | Mounting holes unmeasured. Power from 3.3 V. Price re-confirmed by the owner. |
| DSA blank keycaps, 1u, 24-pack (Mechkeeb) | [B0BWDQ3NKK](https://www.amazon.com/dp/B0BWDQ3NKK) | 2 | $8.99 | $17.98 | Two packs of 24 for 37 caps. Colours to pick. Labels go on the panel. |
| Guarded toggle switches with covers, 6-pack (AITRIP) | [B0CL4GNMJX](https://www.amazon.com/dp/B0CL4GNMJX) | 1 | $9.99 | $9.99 | ABORT, ENGAGE / DISENGAGE and the master power switch (3 of the 6 used). Kept over Digi-Key: its guard and toggle are sold separately, its cover is made for CW Industries' own series, so fit is a risk, and it costs far more. Check the photos show a bat-handle toggle with a flip cover. |
| Weight vest steel plates, 8-pack (Mavee, silver electroplated) | [listing](https://a.co/d/0axItt4q) | 2 | $25.99 | $51.98 | Ballast: 8 plates per wing (16 in all, 2 packs, about 3.2 kg); the pocket takes 12 per wing if a third pack is needed. ASIN not resolved; weigh one plate on arrival. 5.9 x 0.98 x 0.28 in, 0.44 lb each. |

## Already owned

Not in the total. Prices are the listing price seen, not necessarily what was paid.

| Item | Listing | Qty | Listing price | Note |
|---|---|---|---|---|
| MX-style blue clicky switches, 72-pack (Josojoou) | [B0GC33V4HK](https://www.amazon.com/dp/B0GC33V4HK) | 1 | $12.99 | Bought 2026-10-10. 37 of 72 used. |
| Passive buzzer module, 5-pack (DIYables) | [B0DHGP95K4](https://www.amazon.com/dp/B0DHGP95K4) | 1 | $6.99 | Ordered 2026-10-10; 1 of 5 used. Bench-test whether it is passive. Power from 3V3. |
| WS2812B 10 mm pixel boards, 100 (BTF-LIGHTING) | listing | 1 | unknown | 65 of 100 used: 24 keys, 32 fuel bars, 9 annunciator windows. GRB. One chain through the three strip pieces. |

## Not yet specified or counted

Solder and flux, cable clips and zip ties, M3 screws (countersunk for the fader) and standoffs, heat-set inserts, silicone feet (20 mm), printer filament (about 2 to 3 kg), connectors for the sticks and encoders, a round attitude TFT (open), the annunciator's translucent windows and light box (printed), and shipping and tax. Heat shrink is already owned.
