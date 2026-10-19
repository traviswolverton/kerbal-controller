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

## Joysticks (locked)
- **Two SaiDian JH-D400X-R4** 4-axis industrial joysticks, 10 kOhm potentiometers, 18.79 USD each
  ([Amazon listing](https://www.amazon.com/SaiDian-4-Axis-Joystick-Potentiometer-JH-D400X-R4/dp/B08CGYGMJL)).
  It is the part most KSP controller builds use.
- **Mapping:** right stick = pitch / yaw, twist = roll (Simpit rotation).
  Left stick = translation X / Y, twist = Z (Simpit translation). No separate rockers needed.
- **Electrical:** passive potentiometers, so power them from the Teensy's **3.3 V**, not 5 V,
  to stay inside the ADC range. Listings give +/-20 % resistance tolerance and +/-1 %
  linearity, so calibrate the centre point and ranges in firmware.
- **Solder quickly:** the listings warn that heat can burn the part.
- **Dimensions** from the seller's side-view drawing (`docs/reference/jh-d400x-r4-side-view.png`),
  my reading of it:
  - Tilt: +/-25 degrees each way. Sealed (boot) design.
  - Grip: 35 mm diameter, 42 mm tall, with the Z (twist) potentiometer inside it.
  - Fourth "axis": a **momentary button switch on top of the grip**, not an analog axis.
    Free for something like an RCS toggle or SAS hold.
  - Overall height 84 mm to the top of the grip, plus 10.5 mm for the button = 94.5 mm.
  - Body below the mounting plate: 25.5 mm deep. That leaves about 58.5 mm above the plate
    to the top of the grip (about 69 mm to the top of the button).
  - Body width 40.4 mm, 49.6 mm including the Y potentiometer bump on one side.
  - X and Y potentiometers sit on the body (Y on the side that adds 9.2 mm).
- **Still not known:** the mounting flange outline, mounting hole spacing and hole diameter
  (the drawing is a side view and does not show them) and the cutout depth in the other
  direction. **Measure the units when they arrive** before drawing the stick panels, or find a top-view drawing.
- **Clearance estimate:** at full +/-25 degree tilt the grip edge sweeps roughly 35-40 mm from
  the stick axis (estimated from the drawing scale). Keep keys and other controls at least that far
  from each stick, with margin.

## Throttle (proposed, not yet confirmed)
- Plain 100 mm fader with a "ghost" pixel strip showing the game's throttle, plus pickup mode
  (ignore the fader until it matches the game value) so nothing jumps.
- Keep the left module's 100 mm slot able to take a motorised fader later.

## Open items
- Measure the real pixel board (diameter and height) with calipers.
- Print the test plate (`cad/test_plate.scad`) and settle the MX cutout tolerance and
  diffuser thickness.
- Measure the joysticks on arrival (mounting flange, hole spacing and diameter, cutout).
- Decide what the two grip buttons do.
- Confirm plain fader with ghost strip, or motorised.
- Whether to include the round attitude TFT.
- Column pitch: 19.05 mm for now, 22-25 mm is an option for finger room.
- Firmware: key assignment map, Simpit channel list, serpentine pixel mapping.
