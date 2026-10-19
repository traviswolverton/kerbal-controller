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
| Panel-mount DC jack | 1 | chosen | [Adafruit 5607 round panel mount 5.5/2.1 mm barrel jack extension cable, 30 cm](https://www.adafruit.com/product/5607), $4.95, in stock 2026-10-19 | 1" (25.4 mm) hole, panels up to 16 mm. Current rating not listed: check before relying on it at 4 A. Cut or terminate the plug end inside. Not ordered yet. |
| 330-470 ohm resistor, 1000 uF cap (10 V+) | 1 each | chosen | - | Pixel data line and 5 V rail. |
| 1N4148 diodes | 24 | chosen | - | One per key. |
| Inter-module connectors | 2 sets | open | - | Link the left and right modules to the centre module, which holds the Teensy. |

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
| Rotary encoder with push switch | 3 | proposed | [Bourns PEC11R-4215F-S0024, 6-pack, Amazon](https://www.amazon.com/BOURNS-PEC11R-4215F-S0024-Incremental-Momentary-Mechanical-6pack/dp/B093P29XL8) | 24 detents. Check bushing vs the 7 mm hole. |
| Encoder knobs, 25 mm, flatted 6 mm shaft | 3 | open | - | |
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
