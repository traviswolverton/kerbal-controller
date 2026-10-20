# Parts list

Working list for the console. Status: **chosen** (part picked and checked), **owned**, **proposed** (candidate, not
confirmed), **open** (undecided). Sources are US retailers only. **Digi-Key is the primary source** and most parts
below are one Digi-Key order; Amazon.com covers what Digi-Key does not carry or sells at a much worse price.
Digi-Key prices and stock are from the Digi-Key API on 2026-10-19 (`docs/tools/parts.py`); the live order list with
a total is [parts-bom.md](parts-bom.md), and the shortlist is [parts-shortlist.json](parts-shortlist.json). Re-run
`python3 docs/tools/parts.py check --md` before ordering. Design context is in `decisions.md`.

## Digi-Key order

The table lists the 28 main lines. The shortlist also holds the perfboard, terminal blocks, headers, wire and heat shrink
from [electronics-build.md](electronics-build.md), 36 lines and $328.54 in all. Re-checked live on 2026-10-20 with no flags. **The combined Digi-Key and Amazon total is in
[budget.md](budget.md).**

| Part | Qty | Digi-Key PN | Unit | Notes |
|---|---|---|---|---|
| Teensy 4.1, headers fitted (SparkFun 20360) | 1 | 1568-20360-ND | $33.60 | 3.3 V pins, not 5 V tolerant. No `touchRead()` on 4.x. 16771 is the same board without headers, $31.50. |
| 5 V 4 A desktop adapter, Mean Well GST25A05-P1J | 1 | 1866-2087-ND | $14.30 | Positive centre, 2.1 x 5.5 mm plug, 1 m lead, cULus. IEC C14 inlet, **cord sold separately**. |
| Mains cord, NEMA 5-15 to IEC C13 | 1 | 839-11-00022-ND | $4.37 | For the adapter. |
| Panel DC jack 5.5 x 2.1 mm, Tensility 54-00151 | 1 | 839-54-00151-ND | $4.81 | 7.5 A, solder cup, rear nut. **Panel cutout (datasheet, read 2026-10-20):** 10.9 mm round with two flats 9.8 mm apart, panel 1.5 to 4.5 mm, M11 nut. |
| Panel fuse holder 5 x 20 mm, Würth | 1 | 732-952005000010000-ND | $2.15 | On the 5 V rail. **Panel hole (datasheet, read 2026-10-20):** 13 mm round with a 1.8 mm key out to 14 mm, panel 0.8 to 2.8 mm. |
| Fuse 4 A 5 x 20 mm, Littelfuse | 2 | F1724-ND | $0.57 | One spare. Rated for AC; fine at 5 V DC. |
| STAGE key switch, E-Switch KO133A801 | 1 | EG5876-ND | $7.07 | 2-position SPST, **12 mm cutout**, key removable in position 1 only. Confirm in the datasheet that position 1 is OFF. |
| Big STAGE button, Adafruit 3489 arcade, red LED | 1 | 1528-2316-ND | $2.50 | **30 mm cutout**, 5 V LED, 2.8 mm quick-connect tabs. LED wiring is open (always on, or driven later). |
| Motorised 100 mm fader, Adafruit 5466 | 1 | 1528-5466-ND | $24.95 | 6-10 V motor, run at 5 V. Two M3 holes 120 mm apart. Only 37 in stock. |
| L9110H fader driver, Adafruit 4489 | 1 | 1528-4489-ND | $1.50 | Next to the fader motor. |
| Conductive fader nubbin, Adafruit 5741 | 1 | 1528-5741-ND | $6.19 | For touch sensing. Only 37 in stock. |
| Rotary encoder with push switch, Bourns PEC11R-4215F-S0024 | 3 | PEC11R-4215F-S0024-ND | $2.95 | 24 detents, 6 mm flatted shaft. Bushing only about 5 mm long: keep the panel about 3 mm at the encoders. |
| Encoder knobs, CLIFF KMK25 silver, 25 x 15 mm | 3 | 4654-FC7254-ND | $4.90 | 6 mm D shaft, knurled aluminium, matches the mockup's 25 x 15 mm proxy. Only 9 in stock; silver only (the smaller KMK10E FC7259 comes in black). Set screw not confirmed. |
| MCP23017-E/SP I2C expander, DIP-28 | 1 | MCP23017-E/SP-ND | $1.69 | Replaces the breakout board: hand-wired on perfboard behind the switch panel. |
| DIP-28 socket | 1 | 1175-1490-ND | $1.29 | For the expander. |
| 74AHCT125N level shifter, DIP-14 | 1 | 296-4655-5-ND | $1.00 | Pixel data line. |
| DIP-14 socket | 1 | 1175-1487-ND | $0.73 | For the level shifter. |
| 1N4148 diode | 30 | 1N4148FS-ND | $0.06 | 24 matrix diodes plus spares. |
| 330 ohm resistor, 1/4 W | 2 | CF14JT330RCT-ND | $0.10 | Pixel data series resistor, one spare. |
| 4.7 kohm resistor, 1/4 W | 3 | CF14JT4K70CT-ND | $0.10 | SDA and SCL pull-ups, one spare. |
| 10 kohm resistor, 1/4 W | 3 | CF14JT10K0CT-ND | $0.10 | Expander reset pull-up, spares. |
| 1000 uF 16 V electrolytic | 2 | 1189-1147-ND | $0.71 | 5 V rail, one spare. |
| 47 uF 25 V electrolytic | 2 | 732-8823-1-ND | $0.10 | Across the fader driver's supply, one spare. |
| 0.1 uF 50 V ceramic | 12 | BC1101CT-ND | $0.17 | Decoupling, and one per stick and fader wiper. |
| DB25 female panel jack, ITT Cannon ZDB25S | 4 | 1003-ZDB25S-ND | $3.99 | Middle strip, one per outer piece. |
| DB25 male panel jack, ITT Cannon ZDB25P | 4 | 1003-ZDB25P-ND | $3.42 | One on each outer piece. |
| DB25 shielded cable, female to male, 1 m, Phoenix Contact 1656291 | 4 | 277-12299-ND | $15.70 | Straight-through, 25 conductors. Male end into a middle jack, female end onto an outer jack. |
| Panel USB micro-B extension, SparkFun 15464 | 1 | 1568-15464-ND | $4.42 | For the Teensy. |

**Packaging matters:** several small parts are only sold on reels (minimum 4,000 to 5,000). The part numbers above are
the cut-tape or bulk versions with a minimum order of 1. The tool now prefers those, and lists the alternatives.

## Amazon.com (not stocked by Digi-Key, or much cheaper there)

| Part | Qty | Status | Source | Notes |
|---|---|---|---|---|
| JH-D400X-R4 joystick | 2 | chosen | [SaiDian, Amazon](https://www.amazon.com/SaiDian-4-Axis-Joystick-Potentiometer-JH-D400X-R4/dp/B08CGYGMJL), $18.79 each | Mounting holes unmeasured. Power from 3.3 V. |
| MX-style switches, blue clicky, 3-pin | 37 of 72 | owned | [Josojoou](https://www.amazon.com/dp/B0GC33V4HK) | Bought 2026-10-10. |
| WS2812B 10 mm pixel boards | 65 of 100 | owned | BTF-LIGHTING | 24 keys, 32 fuel bars, 9 annunciator windows. GRB. One chain through three strip pieces. |
| Buzzer module, low-level trigger | 1 of 5 | owned | [DIYables, Amazon B0DHGP95K4](https://www.amazon.com/dp/B0DHGP95K4) | Ordered 2026-10-10. Bench-test whether it is passive. Power from 3V3. |
| DSA blank keycaps, 1u | 37 (two packs of 24) | chosen | [Mechkeeb](https://www.amazon.com/Mechkeeb-Profile-Switches-Keyboard-Replacement/dp/B0BWDQ3NKK) | Price and colours unchecked. Labels go on the panel. |
| Guarded toggle switch, 12 mm | 3 (of a 6-pack) | chosen | [AITRIP 6-pack with red covers, B0CL4GNMJX](https://www.amazon.com/Heavy-Rocker-Toggle-Switch-Cover/dp/B0CL4GNMJX) | ABORT, ENGAGE / DISENGAGE and the master power switch. Kept: Digi-Key sells the guard and the toggle separately, and its cover is made for CW Industries' own series, so fit is a risk. Check the photos show a bat-handle toggle. Price unchecked. |
| 2.42" OLED, 128x64, SSD1309 | 2 | proposed | [Waveshare](https://www.amazon.com/waveshare-Resolution-Raspberry-forArduino-Communication/dp/B0CM3RHMGP) | SPI, 3.3 V. Digi-Key's 2.42" OLEDs are $30 to $57 each, so this is a deliberate exception. Board outline vs the 58 x 31 mm window unchecked. |
| Ballast steel, about 4.6 kg in all | 4 plates | open | local metal supplier or hardware store | 6 x 6 x 1/4 in plates (152.4 x 152.4 x 6.35 mm, about 1.16 kg each), two per wing, or equivalent steel. The Amazon listings were dead links. Wipe and paint. |

## Not yet specified

M3 screws, countersunk M3 for the fader, heat-set inserts, silicone feet (20 mm), hookup wire, perfboard for the
expander, a round Attitude TFT (open), 3D-printer filament (about 2 to 3 kg), and the annunciator's translucent windows
and light box (printed).
