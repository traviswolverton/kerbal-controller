# Design decisions so far

Kerbal Space Program controller built around
[KerbalSimpitRevamped](https://github.com/Simpit-team/KerbalSimpitRevamped).
This file records what has been settled and what is still open.

## Fixed constraints
- **Game:** KSP1 (not KSP2).
- **OS:** Windows. The Simpit plugin's keyboard emulation works there.
- **Printer:** 256 x 256 x 256 mm build volume, so each module has to fit in about 245 mm each way.
- **Skill:** comfortable soldering, willing to hand-wire.

## Architecture
- One **Teensy 4.1** as the main board, talking Simpit over USB serial.
- Modular case, one printed module per area (left: translation stick and throttle,
  centre: key bank and displays, right: rotation stick).
- Simpit supports several `SerialPort` blocks in `Settings.cfg`, so extra boards can be
  added per module later.
- KSP1 mod dependency: **Alternate Resource Panel** (via CKAN) for liquid fuel,
  monoprop, electric charge and some other resource telemetry.

## Key bank
- **4 x 6 MX keys**, each with a state-feedback pixel (action groups, SAS mode bank, custom
  action groups).
- **Layout B, "annunciator rows":** 19.05 mm column pitch, **30 mm row pitch**, with
  one pixel in its own clear space directly above each key.
  See `docs/pitch-examples.png` (drawn at 28 mm rows; 30 mm gives about 1 mm clearance to the keycap footprint).
- **Matrix:** hand-wired diode matrix (one 1N4148 per switch), 4 rows + 6 columns.
  Adafruit NeoKey boards were considered and dropped because they are hard to find.
- **Pixels:** BTF-LIGHTING WS2812B, 5050 on 10 mm round white PCBs (100 pcs, owned).
  Colour order **GRB**. Four solder pads per board (5V, GND, DIN, DOUT).
  Roughly 56 are planned (24 keys + 4 fuel bars of 8), so about 44 stay spare.
- **Data line:** 74AHCT125 level shifter, a 330-470 ohm series resistor near the first pixel,
  a large capacitor across the 5 V rail, and a separate 5 V supply of at least 3 A.
  Cap brightness in firmware.

## Open items
- Measure the real pixel board (diameter and height) with calipers.
- Print the test plate (`cad/test_plate.scad`) and settle the MX cutout tolerance and
  diffuser thickness.
- Choose joystick parts (2-axis hall-effect gimbals plus roll and Z rockers, or 3-axis twist sticks).
- Plain or motorised throttle fader.
- Whether to include the round attitude TFT.
- Column pitch: 19.05 mm for now, 22-25 mm is an option for finger room.
- Firmware: key assignment map, Simpit channel list, serpentine pixel mapping.
