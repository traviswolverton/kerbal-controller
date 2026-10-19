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
- **Layout B, "annunciator rows":** 19.05 mm column pitch, **36 mm row pitch**, with
  one pixel in its own clear space directly above each key.
  `docs/pitch-examples.png` is the earlier 28 mm drawing and is superseded for row pitch.
- **Revised after the mockup:** at 30 mm rows and a 12 degree tilt the pixel above each key is
  hidden behind the keycap in front of it (a keycap is about 13.5 mm tall). The seat-view renders in
  `docs/mockup/renders/` show it. The fix is a **steeper centre panel (28 degrees)** plus the
  **36 mm row pitch**; the two side modules stay at 12 degrees. Needs a real-world check with the test plate.
- **Switches (owned):** Josojoou 72-piece pack of **blue clicky, 3-pin, pre-lubricated** MX-style switches
  ([Amazon listing](https://www.amazon.com/dp/B0GC33V4HK)), bought 2026-10-10. 24 are used, so 48 spare.
  3-pin means no plastic side pegs, so a plain 14 mm square cutout should work. Clicky is loud;
  fine for a desk controller. Check snap-fit on the test plate (1.5 mm plate) and measure the
  housing below the plate (about 5 mm, plus pins) against the spacer depth.
- **Keycaps (chosen):** blank 1u **DSA profile** (about 7.6 mm tall, flat top), 24 pieces, from the
  [Mechkeeb 24 pcs DSA blank PBT listing](https://www.amazon.com/Mechkeeb-Profile-Switches-Keyboard-Replacement/dp/B0BWDQ3NKK)
  (B0BWDQ3NKK, Amazon.com). Colours still to pick: group by function (SAS / navigation, action groups,
  red for STAGE). Key labels go on the panel, not on the caps. The mockup's keycap proxy
  (18 mm wide, top at 13.5 mm above the plate) already assumes DSA. When they arrive, measure the real
  height with a switch fitted and re-check pixel visibility at 28 degrees.
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

## Throttle (motorised fader chosen)
- **Fader:** [Adafruit 5466](https://www.adafruit.com/product/5466) motorised slide pot, 10 kOhm linear,
  100 mm travel, $24.95 (US, in stock on 2026-10-19). Motor 6-10 V DC (Adafruit runs it at 5 V),
  pot and motor circuits isolated, slider moves freely by hand when the motor is off.
- **Driver:** [Adafruit L9110H H-bridge (4489)](https://www.adafruit.com/product/4489), $1.50, 2.5-12 V,
  800 mA per channel. Adafruit's author runs it from 3.3 V logic. Add the 47 uF capacitor from their
  [Flying Faders guide](https://learn.adafruit.com/flying-faders/overview) near the driver.
- **Knob:** [Adafruit conductive nubbin (5741)](https://www.adafruit.com/product/5741), $4.95, 26 x 11 x 10 mm,
  shaft slot 18.8 x 1.8 mm. It has to be conductive so the touch pad on the slider works.
- **Behaviour:** the motor follows the game's throttle while you are not touching the fader; when you
  touch it, you drive the throttle. Simpit's `THROTTLE_CMD_MESSAGE` (game to device) gives the game
  value (value range not yet verified, check the current Simpit source). The fader shows the throttle
  itself, so the 8-pixel ghost strip is no longer needed (mockup: `ghost_strip = false`).
- **Mechanical (Soundwell drawing linked from the Adafruit page, my reading of a scanned image):**
  - Face 146.5 x 17.2 mm (74 + 72.5 long). Adafruit says 144 x 28.6 x 17 mm. Plan a 150 mm cavity.
  - **Mounting: two M3 x 0.5 threaded holes in the front face, 120 mm apart on the slot axis.**
    Screw them from the front through the panel. The panel sits directly on the face.
  - Body 26 mm deep below the face, plus 3.5 mm of PCB pins.
  - Slider tab: about 1.2 mm thick, 18.5 mm wide, about 8.2 mm above the face, with two 2 mm holes.
    The nubbin slot (1.8 mm) is loose on a 1.2 mm tab, so it may need glue or tape.
  - Pins at 3.75 mm pitch (pot: 1, T = touch, 3, 2) at one end, motor pins (A, B) 8 mm apart at the other.
- **Still open:**
  - Teensy 4.1 has no `touchRead()`. Options: FastTouch or CapacitiveSensor library, or treat wiper
    movement the motor did not cause as a hand.
  - Motor current at 5 V is not listed: measure it. Expect ADC noise while it moves.
  - Panel thickness vs the tab: the tab is only about 8 mm tall, so a thick panel may bury the holes.
    Use a thin panel or spacers behind it.
  - Confirm every dimension on the real unit before printing the left module.

## Encoders and knobs (proposed)
- **Encoder:** [Bourns PEC11R-4215F-S0024](https://www.amazon.com/BOURNS-PEC11R-4215F-S0024-Incremental-Momentary-Mechanical-6pack/dp/B093P29XL8)
  (6-pack, 3 used). 24 detents and 24 pulses per revolution, push switch, 6 mm flatted shaft 15 mm
  long. Metal M7 bushing about 5 mm long, with a flat washer and nut included.
- **Pitch conflict:** Mouser lists M7 x 0.75, the Bourns datasheet text suggests M7 x 0.5. Only matters if
  you buy a different nut or print a thread; the supplied nut will fit.
- **Panel thickness matters:** the bushing is only about 5 mm long, so with the washer and nut the panel at
  the encoders should be about 3 mm or less, or counterbored from behind. The mockup's 7 mm hole is
  about right for the bushing, but confirm the diameter against the drawing.
- **Knobs:** [NMOWYBPY 25 x 13 mm aluminium, D-shaped bore](https://www.amazon.com/NMOWYBPY-Aluminum-Potentiometer-25x13mm-Control/dp/B0H3NXPL9Z),
  2 per pack, so buy 2 packs for 3 knobs plus a spare. The D-hole should seat positively on the flatted
  shaft. The mockup knob proxy is 25 x 15 mm; this one is 2 mm shorter, which changes nothing that matters.
- **Open:** whether the listing includes a set screw, and prices. Both unchecked.

## Inter-module links (proposed)
- **Approach:** direct wiring from the Teensy in the centre module to each side module through one
  **DB25 D-sub** per side. One USB cable, no extra boards. Satellite microcontrollers with a 4-wire link
  would need fewer wires but add firmware and a second USB or serial path; revisit only if the cable
  count becomes a problem.
- **Conductor count (my estimate):**
  - Left, about 16 of 25: stick X, Y, twist Z and grip button (4), fader wiper and touch (2), fader driver
    PWM pair (2), time-warp encoder A, B, push (3), 3.3 V, 5 V, and 2-3 grounds. The fader driver sits in
    the left module next to the motor, so only two PWM lines and 5 V travel.
  - Right, about 13 of 25: stick X, Y, twist and button (4), two encoders A, B, push (6), 3.3 V, and 2-3 grounds.
- **Parts:** four female panel-mount DB25 solder-cup jacks and two male-to-male straight-through shielded
  cables (not null modem), listed in `parts-list.md`. Short cables matter: the analog stick signals run
  down these, so use about 0.5 m, not 1.5 m, and put 0.1 uF on each wiper.
- **Cross-plug rule:** both side ports use the same connector, so make a swapped cable harmless. Put 3.3 V and
  ground on the same pins on both ports, put 5 V on a pin the right module leaves unconnected, and never
  put a signal on a pin that is 5 V at the other port. Pin maps are still to be drawn once the Teensy pin
  assignment is done.
- **Open:** exact panel cutout and screw spacing for the chosen jack (measure it; standard D-sub shell B
  hardware should match but I have not checked), and prices.

## 5 V power (chosen, not yet ordered)
- **Supply:** [Adafruit 1466](https://www.adafruit.com/product/1466), 5 V 4 A regulated, UL listed,
  5.5 x 2.1 mm plug with positive tip, US 2-prong, $14.95. Adafruit's own warning: it is not for
  powering an Arduino through its DC jack (not an issue here, see below).
- **Panel connector:** [Adafruit 5607](https://www.adafruit.com/product/5607), round panel-mount 5.5/2.1 mm
  jack on a 30 cm lead, $4.95. Needs a 1" (25.4 mm) hole, flange 30 mm, threaded part 23 mm, panels up
  to 16 mm. Current rating not stated on the page: confirm before running 4 A through it. Cheaper
  threaded jacks on Amazon were also seen, one rated only 1.5-2 A, so do not buy those blind.
- **Budget:** pixels are 56 x 60 mA = 3.4 A worst case (all white); fader motor is unknown at 5 V, measure
  it. Cap total pixel draw in firmware so real use stays well under 4 A. The usual guidance is to keep
  the rail above 4.5 V at full load and to leave 20-25 % headroom.
- **Wiring plan:**
  - The Teensy is powered **only from USB**. The external 5 V feeds the pixels, the level shifter and the
    fader driver, with ground shared with the Teensy. Do not tie the 5 V rail to the Teensy's VIN.
  - Put a fuse sized just above the capped load on the 5 V rail, and the 1000 uF capacitor where the rail
    enters the pixel run.
  - The 2.42" OLED modules accept 3.3-5 V, so power them from the 5 V rail to keep load off the Teensy's
    3.3 V regulator. Confirm the module's logic level first.
  - All 56 pixels are in the centre module, so one power feed is enough.

## Guarded toggles (chosen, not yet ordered)
- **Part:** [AITRIP 6-pack, 12 V 20 A, 2-pin SPST ON/OFF toggle switches with red aircraft-style covers](https://www.amazon.com/Heavy-Rocker-Toggle-Switch-Cover/dp/B0CL4GNMJX)
  (Amazon B0CL4GNMJX). Seller-reported 12 mm mounting hole; price and stock not checked.
  Four are used (ABORT, STAGE ARM, 2 spare), so two are left over.
- **Wiring:** one pin to ground, the other to a Teensy input with `INPUT_PULLUP`; debounce in firmware.
- **To check on arrival:** thread length against panel thickness, and the closed-cover footprint against
  the mockup's 40 x 60 mm toggle spacing (a cover seen earlier was about 47 mm long).

## Buzzer (owned)
- **Part:** DIYables "Passive Buzzer Module, 5V", 5 pieces, $6.99
  ([Amazon B0DHGP95K4](https://www.amazon.com/dp/B0DHGP95K4)), ordered 2026-10-10. Seen in the listing
  photos: a small PCB with a black cylindrical buzzer, a 3-pin header (GND, I/O, VCC), one SMD
  transistor and one SMD resistor marked 102, and a mounting hole beside the buzzer. The board text
  (Chinese) reads "low level trigger".
- **Wiring (my reading of the photo, not verified against a schematic):** the on-board transistor drives
  the buzzer, so no external transistor is needed. "Low level trigger" means the I/O pin LOW switches it
  on. Power VCC from the Teensy's **3.3 V**, not 5 V: with VCC at 5 V and a 3.3 V logic high, a PNP
  transistor stays partly on and the buzzer would not switch off cleanly.
- **Bench test before relying on it:** apply power with I/O held low. A continuous tone means it is
  actually an **active** buzzer (fixed pitch, no `tone()` melodies); a single click means it is passive.
- **Mounting idea:** PCB behind the panel, buzzer poking through a hole of about 12.4 mm (the mockup has
  12 mm), or a 3-4 mm sound port if the buzzer stays behind. Measure the buzzer diameter and height first.
- **Open:** the board size and mounting hole position are not known. Measure one.

## Mockup (v0 proposal)
See `docs/mockup/README.md`. Three modules of 220 / 240 / 220 mm width, 245 mm deep, tilted
12 / 28 / 12 degrees. All positions are a first proposal to react to.

## Open items
- Measure the real pixel board (diameter and height) with calipers.
- Print the test plate (`cad/test_plate.scad`) and settle the MX cutout tolerance and
  diffuser thickness.
- Measure the joysticks on arrival (mounting flange, hole spacing and diameter, cutout).
- Decide what the two grip buttons do.
- Confirm plain fader with ghost strip, or motorised.
- Whether to include the round attitude TFT.
- Column pitch: 19.05 mm for now, 22-25 mm is an option for finger room.
- Check the 28 degree centre tilt feels right at your desk (prop the test plate at that angle).
- Firmware: key assignment map, Simpit channel list, serpentine pixel mapping.
