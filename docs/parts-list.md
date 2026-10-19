# Parts list

Working list for the console. Status: **chosen** (part picked), **owned**, **proposed** (candidate,
not confirmed), **open** (undecided). Sources are US retailers only; prices are USD as seen on the US
listing on the date given, and a blank price means it has not been checked. Design context is in
`decisions.md`.

## Electronics

| Part | Qty | Status | Part / source | Notes |
|---|---|---|---|---|
| Teensy 4.1 | 1 | chosen | [PJRC](https://www.pjrc.com/store/teensy41.html) | 3.3 V pins, not 5 V tolerant. No `touchRead()` on 4.x. |
| WS2812B 10 mm pixel boards | 56 of 100 owned | owned | BTF-LIGHTING | 24 keys + 4 fuel bars of 8. GRB. No ghost strip any more. |
| 74AHCT125 level shifter | 1 | chosen | - | For the pixel data line. |
| 5 V supply, 4 A | 1 | chosen | [Adafruit 1466, UL listed, 5.5 x 2.1 mm centre-positive](https://www.adafruit.com/product/1466), $14.95, in stock 2026-10-19 | Powers pixels and the fader motor. Cap pixel brightness in firmware. Not ordered yet. |
| Panel-mount DC jack, 5.5 x 2.1 mm | 1 of 6 sets | chosen | [Tugermoola 6-set kit OLA012, Amazon B0D9B7WR23](https://www.amazon.com/Tugermoola-Threaded-Female-Connector-Adapter/dp/B0D9B7WR23), $9.99 for 6 sets | Seller specs: about 12 mm mounting hole, 5 A / 50 V, 20 AWG, female jack on 150 mm leads, male plug on 200 mm leads, gaskets and dust caps included. Only one female jack is needed; the male plugs and spares can make power pigtails. Not ordered yet. Check which colour/head variant the link is, and check polarity with a meter. |
| 330-470 ohm resistor, 1000 uF cap (10 V+) | 1 each | chosen | - | Pixel data line and 5 V rail. |
| 1N4148 diodes | 24 | chosen | - | One per key. |
| DB25 female panel-mount connector, solder cup | 8 (two 5-packs) | proposed | [uxcell DB25 female, 5-pack, Amazon B07LCN17K9](https://www.amazon.com/uxcell-Connector-Mechanical-Equipment-Computers/dp/B07LCN17K9) | Four on the middle strip piece (one per outer piece) and one on each outer piece. Listing says 5 A. No hood. Price unchecked. |
| DB25 male-to-male straight-through shielded cable | 4: 2 strip (1.5 ft), 2 wing (3 ft) | proposed | [Amphenol CS-DSPMDB25MM-001.5, 1.5 ft, Amazon B00O0759BO](https://www.amazon.com/Amphenol-CS-DSPMDB25MM-001-5-25-Pin-Premium-Shielded/dp/B00O0759BO) | All 25 lines pin-to-pin, not a null modem. Wing cables pass through a strip shell, so use the 3 ft: [CablesOnline 3 ft S-0003](https://www.amazon.com/CablesOnline-25-Conductor-Fully-Wired-Straight-Through-S-0003/dp/B09T8LYBTZ). Price unchecked. |

## Controls

| Part | Qty | Status | Part / source | Notes |
|---|---|---|---|---|
| JH-D400X-R4 joystick | 2 | chosen | [SaiDian, Amazon](https://www.amazon.com/SaiDian-4-Axis-Joystick-Potentiometer-JH-D400X-R4/dp/B08CGYGMJL), $18.79 each | Mounting holes unmeasured. Power from 3.3 V. |
| MX-style switches, blue clicky, 3-pin | 24 of 72 owned | owned | [Josojoou, Amazon](https://www.amazon.com/dp/B0GC33V4HK) | Bought 2026-10-10. |
| DSA blank keycaps, 1u | 24 | chosen | [Mechkeeb, Amazon](https://www.amazon.com/Mechkeeb-Profile-Switches-Keyboard-Replacement/dp/B0BWDQ3NKK) | Price and colours unchecked. Labels go on the panel. |
| Motorised slide pot, 100 mm | 1 | chosen | [Adafruit 5466](https://www.adafruit.com/product/5466), $24.95 | 6-10 V motor, run at 5 V. Two M3 holes, 120 mm apart. |
| L9110H H-bridge motor driver | 1 | chosen | [Adafruit 4489](https://www.adafruit.com/product/4489), $1.50 | Drives the fader motor. Add a 47 uF capacitor near it. |
| **Conductive slide pot nubbin** | 1 | chosen | [Adafruit 5741](https://www.adafruit.com/product/5741), $4.95 | 26 x 11 x 10 mm, slot 18.8 x 1.8 mm. Conductive, for fader touch sensing. |
| 47 uF 25 V electrolytic capacitor | 1 | chosen | - | From Adafruit's Flying Faders guide. |
| Rotary encoder with push switch | 3 | proposed | [Bourns PEC11R-4215F-S0024, 6-pack, Amazon](https://www.amazon.com/BOURNS-PEC11R-4215F-S0024-Incremental-Momentary-Mechanical-6pack/dp/B093P29XL8) | 24 detents, 6 mm flatted shaft 15 mm long, M7 bushing only about 5 mm long, nut and washer included. Thread pitch conflicts between sources (0.75 vs 0.5 mm): check the Bourns drawing. |
| Encoder knobs, 25 x 13 mm aluminium, D-shaped bore | 3 (buy 2 packs) | proposed | [NMOWYBPY 2-pack, Amazon B0H3NXPL9Z](https://www.amazon.com/NMOWYBPY-Aluminum-Potentiometer-25x13mm-Control/dp/B0H3NXPL9Z) | D-hole should seat on the flatted shaft. Listing wording on the set screw is ambiguous. Price unchecked. Alternatives: [Taiss 25 x 15 mm](https://www.amazon.com/clp/B07F26WT4R), [GD-PARTS 25 x 15.5 mm](https://www.amazon.com/clp/B07BTGL1JK). |
| Guarded toggle switch, 12 mm | 4 (6-pack) | chosen | [AITRIP 6-pack, 12 V 20 A, 2-pin SPST ON/OFF with red covers, Amazon B0CL4GNMJX](https://www.amazon.com/Heavy-Rocker-Toggle-Switch-Cover/dp/B0CL4GNMJX) | Not ordered yet; price and stock unchecked. Listing says 12 mm mounting hole. 2 spares cover the two SPARE slots. Wire one pin to ground and the other to a Teensy pin with `INPUT_PULLUP`. Measure the thread length vs panel thickness and the closed-cover footprint (the 40 x 60 mm toggle spacing assumes about 47 x 17 mm). |
| Buzzer module, low-level trigger | 1 of 5 owned | owned | DIYables "Passive Buzzer Module, 5V", [Amazon B0DHGP95K4](https://www.amazon.com/dp/B0DHGP95K4), $6.99 for 5, ordered 2026-10-10 | 3 pins (GND, I/O, VCC), on-board transistor, board marked "low level trigger". The black cylinder with a "+" looks like a magnetic buzzer. Bench-test whether it is really passive. Measure the board and buzzer diameter. |

## Displays

| Part | Qty | Status | Part / source | Notes |
|---|---|---|---|---|
| 2.42" OLED, 128x64, SSD1309 | 2 | proposed | [Waveshare, Amazon](https://www.amazon.com/waveshare-Resolution-Raspberry-forArduino-Communication/dp/B0CM3RHMGP) | SPI, 3.3 V. Board outline vs the 58 x 31 mm window unchecked. |
| Round attitude TFT | 0 or 1 | open | - | |

## Hardware and consumables (not yet specified)

M3 screws and heat-set inserts (the fader needs two M3 screws, countersunk), hookup wire, panel-mount
USB extension, power switch, rail fuse, filament.
