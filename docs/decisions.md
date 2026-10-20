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

## Keyboard (decided): designed for a 12.2 in 60%
- **The console is sized around a 12.2 in (310 mm) 60% keyboard** standing in the open middle between the wings. Strips are
  245 mm wide (735 mm in all, the most the 256 mm bed allows after clearance) and the wings 195 mm, so the gap is **345 mm** wide
  and 176 mm deep: about 17 mm each side of the keyboard, with room for its depth (a 60% is roughly 100-125 mm) and your wrists.
  The mockup shows a 310 x 110 mm keyboard in the gap.
- **If the keyboard changes:** a board wider than about 330 mm will not fit; a full-size one (480 mm) does not, and would
  need six pieces and about 940 mm. A narrower one just leaves more room.
- **Why a keyboard at all:** the controller covers nearly all flight controls. The keyboard is for typing (names, saves, mod
  windows), the VAB and SPH, EVA and the odd hotkey. The mouse is needed throughout.
- **Wing layouts at 195 mm:** left wing fader at u=25, stick at u=108, time-warp encoder at u=168; right wing stick at u=75 and
  encoders at u=150. The stick clearance ring (38 mm) stays clear, and the ballast plates still fit.

## Sourcing (decided)
- **Digi-Key is the primary source,** through its API (`docs/tools/parts.py`): one order, live price, stock and
  parametric data (panel cutouts, ratings). It also sells SparkFun, Adafruit and PJRC items, so the Teensy, fader, driver,
  nubbin and arcade button all moved there from Adafruit, PJRC and Amazon.
- **Amazon.com exceptions:** the SaiDian joysticks (not stocked), the MX switches and buzzers already owned, the DSA keycaps,
  the matched AITRIP guarded toggles and the Waveshare OLEDs (Digi-Key's 2.42" OLEDs cost $30 to $57 each). The encoder knobs
  moved to Digi-Key. The ballast steel is bought locally (the Amazon plate listings were dead links).
- **Reel trap:** many small parts default to reels with minimums of 4,000 to 5,000. The tool prefers cut tape or bulk.

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
  Roughly 65 are planned (24 keys, 4 fuel bars of 8, 9 annunciator windows), so about 35 stay spare.
- **Data line:** 74AHCT125 level shifter, a 330-470 ohm series resistor near the first pixel,
  a large capacitor across the 5 V rail, and a separate 5 V supply of at least 3 A.
  Cap brightness in firmware.

## Joysticks (locked)
- **Two SaiDian JH-D400X-R4** 4-axis industrial joysticks, 10 kOhm potentiometers, 18.79 USD each
  ([Amazon listing](https://www.amazon.com/SaiDian-4-Axis-Joystick-Potentiometer-JH-D400X-R4/dp/B08CGYGMJL)).
  It is the part most KSP controller builds use.
- **Mapping:** right stick = pitch / yaw, twist = roll (Simpit rotation).
  Left stick = translation X / Y, twist = Z (Simpit translation). No separate rockers needed.
- **Grip buttons (decided):** the thumb button on each stick.
  - **Right stick (rotation): SAS toggle.** SAS is mostly about rotation, and the SAS key's pixel still shows the real state.
  - **Left stick (translation): hold for fine control.** While held, firmware scales that stick's X, Y and twist to about 25%
    (a tunable factor), then returns to full. It is done in firmware, so it does not depend on the game. Useful for docking.
    The game's own latching precision mode stays on the PRECISION button of the switch panel.
  - Both are direct Teensy inputs (pins 5 and 9), not on the expander, so a hold responds immediately.
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
- **Fader:** Adafruit 5466 motorised slide pot (Digi-Key 1528-5466-ND), 10 kOhm linear,
  100 mm travel, $24.95 (in stock on 2026-10-19, 37 left). Motor 6-10 V DC (Adafruit runs it at 5 V),
  pot and motor circuits isolated, slider moves freely by hand when the motor is off.
- **Driver:** Adafruit L9110H H-bridge (Digi-Key 1528-4489-ND), $1.50, 2.5-12 V,
  800 mA per channel. Adafruit's author runs it from 3.3 V logic. Add the 47 uF capacitor from their
  [Flying Faders guide](https://learn.adafruit.com/flying-faders/overview) near the driver.
- **Knob:** Adafruit conductive nubbin (Digi-Key 1528-5741-ND), $6.19, 26 x 11 x 10 mm,
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
- **Encoder:** Bourns PEC11R-4215F-S0024 (Digi-Key PEC11R-4215F-S0024-ND, $2.95 each, 3 needed). 24 detents and 24 pulses per revolution, push switch, 6 mm flatted shaft 15 mm
  long. Metal M7 bushing about 5 mm long, with a flat washer and nut included.
- **Pitch conflict:** Mouser lists M7 x 0.75, the Bourns datasheet text suggests M7 x 0.5. Only matters if
  you buy a different nut or print a thread; the supplied nut will fit.
- **Panel thickness matters:** the bushing is only about 5 mm long, so with the washer and nut the panel at
  the encoders should be about 3 mm or less, or counterbored from behind. The mockup's 7 mm hole is
  about right for the bushing, but confirm the diameter against the drawing.
- **Knobs:** CLIFF KMK25 silver, 25 x 15 mm knurled aluminium, 6 mm D shaft (Digi-Key 4654-FC7254-ND, $4.90, 3 needed, 9 in stock).
  It replaces the NMOWYBPY Amazon knobs, whose listing went dead. Same 25 mm diameter and the same 15 mm height as the
  mockup proxy. Silver only; the smaller KMK10E (10.7 mm, FC7259) comes in black if you prefer.
- **Open:** how the knob clamps to the shaft (set screw or friction). Check the CLIFF datasheet.

## Switch panel and annunciator (proposed)
- **Switch panel (left strip):** all inputs that are not wired to a stick or encoder go on one panel and one
  chip, an MCP23017 I2C expander sitting right behind it: ABORT (guarded toggle), a key switch that arms STAGE, a guarded ENGAGE / DISENGAGE toggle, a big STAGE
  button, throttle FULL and CUT, MAP, focus previous and next, quicksave, quickload, precision, pause, UI hide,
  and three spares. That is 16 inputs, listed in `pin-map.md`. Only SDA, SCL, the interrupt and 3V3 cross the
  cable to the Teensy.
- **Why:** the Teensy has no spare header pins, so extra buttons need an expander. A single panel keeps its
  wiring local and frees the toggle pins. This is also the part of the reference build (Altitude Workshops) we
  were missing: its guarded LOCK/STAGE block, throttle FULL button and utility buttons.
- **Buttons:** 13 small ones are the MX switches already owned, with blank DSA caps. A second pack of 24 caps is
  needed. STAGE moves off the key matrix to the big button, so its matrix slot becomes AG9.
- **Game side:** MAP, quicksave and the rest are key presses through Simpit's keyboard emulator (Windows only).
  FULL and CUT drive the throttle, and the motorised fader follows through Simpit's throttle command message.
- **Annunciator (right strip):** 3 x 3 windows, one pixel each: low fuel, low power, overheat, low altitude,
  stable orbit, atmosphere, chute safe, link, and CONTROLS (lit while engaged). Most of these come straight from Simpit messages
  (resources, temperature limit, atmosphere conditions, altitude, orbit, flight status). Chute-safe would be derived
  from altitude and airspeed. **High G was dropped: Simpit has no G-force message.**
- **Master power switch (middle strip, guarded):** in series with the 5 V rail. It cuts the pixels and the fader driver
  but leaves the Teensy and expander powered over USB. It is a third guarded toggle from the AITRIP pack, so a bump cannot
  kill the lights.
- **Layout effect:** the right strip's freed corner holds the annunciator and the middle strip gets the master switch. The
  strips are now 245 mm wide (see the keyboard decision below).
- **STAGE key (decided):** a key switch arms STAGE. The big STAGE button only fires while the key is on, which
  replaces the second guarded toggle. The key position is an expander input, so the firmware does the interlock.
- **RESET: skipped (decided).** Recovery from a hang is replugging the USB cable.
- **ENGAGE / DISENGAGE (decided):** a guarded toggle on the switch panel, modelled on the reference build's toggle by the
  throttle. Engaged, the sticks and throttle send input; disengaged, the firmware sends zero rotation and translation
  (which leaves SAS and the game in control) and stops sending throttle, so a bump or a leaning arm does nothing.
  The annunciator's ninth window, CONTROLS, lights while engaged. Check how Simpit hands the throttle back: its
  changelog mentions throttle authority being released.
- **Skipped, decided:** the reference's two arrow buttons beside its attitude stick. Our two sticks and the
  camera encoder cover that job; revisit only if you find you want attitude trim.
- **Parts picked (all Digi-Key):**
  - STAGE key switch: E-Switch KO133A801 (EG5876-ND, $7.07), 2-position SPST, **12 mm cutout**, key removable in
    position 1 only. Confirm in the datasheet that position 1 is OFF.
  - Big STAGE button: Adafruit 3489 arcade button (1528-2316-ND, $2.50), **30 mm cutout**, red 5 V LED, 2.8 mm quick-connect.
    The LED is open: always on, or driven later.
  - Master power switch: now a guarded AITRIP toggle (see below), replacing the E-Switch ST141D00 that was picked first.
  - Expander: MCP23017-E/SP (DIP-28, $1.69) with a socket, hand-wired on perfboard behind the panel instead of a breakout
    board. A0-A2 tied to GND (address 0x20), RESET through 10 k to 3V3, 0.1 uF across its supply.
- **Open:** the expander's interrupt behaviour is untested, and the Digi-Key key switch's key position needs confirming.

## Inter-module links (proposed, five-piece layout)
- **Approach:** direct wiring from the Teensy in the middle strip piece to each of the four outer pieces
  (two wings, left and right strip) through one **DB25 D-sub** each. One USB cable, no extra boards.
  Satellite microcontrollers with a 4-wire link would need fewer wires but add firmware and a second USB
  or serial path; revisit only if the cable count becomes a problem.
- **Conductors per port:** left wing 19, right wing 14, left strip 21, right strip 16, all of 25. Full
  pinouts and the Teensy pin table are in `pin-map.md`.
- **Pixels:** one chain of 65 on a single data pin: left strip (12), fuel bars in the middle (32), right strip
  (12 key pixels and 9 annunciator pixels). A break in the chain darkens everything after it.
- **Keys:** one 4 x 6 matrix. The left strip carries rows 0-1, the right strip rows 2-3, both carry all six
  column lines.
- **Parts (Digi-Key):** four **female** DB25 panel jacks on the middle piece (ITT Cannon ZDB25S) and one **male** jack
  on each outer piece (ZDB25P), joined by four straight-through shielded female-to-male cables, 1 m (Phoenix Contact
  1656291), listed in `parts-list.md`. The cables fit only one way round. The jacks mount from inside, with the flange
  against the inner wall and the body standing 11 mm proud. The wing jack is on the wing's outer end wall; the two outer
  strips and the middle strip carry theirs on the back wall, so every cable runs outside, behind the console (about 0.6 m of
  path for a wing cable). They are 1 m for all four to keep one part number; coil the slack.
  Keep analog runs short and put 0.1 uF on each wiper.
- **Swapped-cable rule:** all four ports use the same connector, so a cable in the wrong port must be
  harmless. Ground and 5 V sit on the same pins everywhere, and everything the Teensy drives (rows, pixel
  data, fader PWM) is on pins 15-23, which any module not using them leaves open. A script check of all 16
  module and port pairs found no conflict.
- **DB25 cutout (from the ITT Cannon ZD datasheet, rear mount):** 42.52 x 11.40 mm, with two 3.05 mm mounting holes
  47.04 mm apart (modelled 3.2 mm). The flange is 53.09 mm wide.
- **Provisional cutouts (orange in the mockup, sizes NOT verified):** DC jack 11 mm, fuse holder 12.5 mm and USB micro-B
  (15 x 8 mm slot with two 2.5 mm holes), in the middle strip's back wall between the DB25 columns. They only hold the place
  until the parts arrive and are measured.
- **Open:** cable management behind the console, and the real sizes of those three cutouts.

## 5 V power (chosen, not yet ordered)
- **Supply:** Mean Well GST25A05-P1J (Digi-Key 1866-2087-ND, $14.30): 5 V, 4 A max, 20 W, positive centre, 2.1 x 5.5 mm plug,
  1 m lead, cULus approved. It has an IEC C14 inlet, so a mains cord is a separate part (Tensility 11-00022, NEMA 5-15 to
  C13, $4.37). This replaces the Adafruit 1466.
- **Panel connector:** Tensility 54-00151 (Digi-Key 839-54-00151-ND, $4.81): 5.5 x 2.1 mm panel jack, 7.5 A, solder cup,
  rear nut. **Its panel cutout is not verified** (the datasheet is an image), so measure the jack or read the drawing
  before cutting. This replaces the Tugermoola kit from Amazon.
  - Wire from the solder cups: the centre pin is +. Check polarity with a meter before connecting anything.
  - Keep the jack close to the fuse and 5 V rail, or extend the wires.
- **Budget:** pixels are 65 x 60 mA = 3.9 A worst case (all white, which firmware must never allow); fader motor is unknown at 5 V, measure
  it. Cap total pixel draw in firmware so real use stays well under 4 A. The usual guidance is to keep
  the rail above 4.5 V at full load and to leave 20-25 % headroom.
- **Wiring plan:**
  - The Teensy is powered **only from USB**. The external 5 V feeds the pixels, the level shifter and the
    fader driver, with ground shared with the Teensy. Do not tie the 5 V rail to the Teensy's VIN.
  - Put a fuse sized just above the capped load on the 5 V rail, and the 1000 uF capacitor where the rail
    enters the pixel run.
  - The 2.42" OLED modules accept 3.3-5 V, so power them from the 5 V rail to keep load off the Teensy's
    3.3 V regulator. Confirm the module's logic level first.
  - The pixels are spread over the three strip pieces (12, 32, 21). Each outer strip takes 5 V over its DB25 cable; one power input in the middle strip feeds everything.

## Guarded toggles (chosen, not yet ordered)
- **Why not Digi-Key:** it sells the guard (e.g. CW Industries GT-4R, $5.72) and the toggle separately, and that
  cover is made for CW Industries' own toggle series, so mixing is a fit risk. The matched AITRIP pack stays.
- **Part:** [AITRIP 6-pack, 12 V 20 A, 2-pin SPST ON/OFF toggle switches with red aircraft-style covers](https://www.amazon.com/Heavy-Rocker-Toggle-Switch-Cover/dp/B0CL4GNMJX)
  (Amazon B0CL4GNMJX). Seller-reported 12 mm mounting hole; price and stock not checked.
  Three are used (ABORT and ENGAGE / DISENGAGE on the switch panel, and the master power switch), so three are left over. A guarded toggle is cheap enough to keep for ABORT;
  the price in the Amazon listing was not visible when checked. Its title calls it a "rocker toggle": check the photos
  before ordering that it is the bat-handle style with a flip cover.
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
- Whether to include the round attitude TFT.
- Column pitch: 19.05 mm for now, 22-25 mm is an option for finger room.
- Check the 28 degree centre tilt feels right at your desk (prop the test plate at that angle).
- Firmware: key assignment map, Simpit channel list, serpentine pixel mapping.
