# To do

> **What this covers:** everything still to do, in the order it needs doing, with what blocks what.  
> **Read it if:** you want to know what happens next, or what has to happen before something else can.  
> **Status:** A live list. Compiled from the design session on 2026-10-20 and updated since.  
> **Next:** the first unchecked item in section 1.

Check items off as you go. Where something is already written down, the file is named. Many items are facts waiting to be promoted from
*Seller claim* to *Measured* or *Tested* (see [docs/README.md](../README.md)).

## The route in six steps

| Step | Done when | What it unlocks | Sections |
|---|---|---|---|
| A. Ready to order | The last prices and two photo checks are done, and the list is final | The order | 1 |
| B. Parts arrive | Every part is measured and bench-tested | Real cutout sizes for the CAD, and the electronics design is confirmed | 2 |
| C. Test print | The test plate fits and the key lights are visible | Printing the five pieces | 3 |
| D. Full CAD and print | Mounts, joints and templates are done and the pieces are printed | Putting the electronics in | 4 |
| E. Wire and bring up | Each piece passes the [first power-up](../../hardware/electronics/bring-up.md) | The firmware has real hardware to talk to | 7 |
| F. Firmware and game | The console flies a rocket | Done | 5, 6 |

A few things block others: the **joystick measurements** and **display board measurements** block the panel cutouts; the **Teensy pin order check** blocks all
wiring; the **test plate** blocks the strip prints; and the **bring-up test programs** (the first firmware to write) block phase 5 of bring-up.

## 1. Before you order

- [ ] **Fill in any remaining Amazon prices** (check `hardware/sourcing/amazon-items.json` for `null`), then run
  `python3 tools/parts.py budget --md`. Use `amazon-price ASIN PRICE`.
- [ ] **Order 2 packs of the Mavee vest plates** ($25.99 each, a third only if the console still creeps; link in `hardware/sourcing/parts.md`) and note the ASIN in `amazon-items.json`.
- [ ] **Check the AITRIP photos show a bat-handle toggle with a flip cover**, not a flat rocker. Three of the six switches depend on it
  (ABORT, ENGAGE / DISENGAGE, master power).
- [ ] **Confirm the key switch's key position**: in the E-Switch KO133A801 datasheet, is position 1 (key removable) OFF?
- [ ] **DFR0669 displays**: the board is 55.5 x 95 mm with 2 mm holes on a 90 x 50 mm pitch and a 73.44 x 48.96 mm active area, but the
  active area's offset from the holes is not stated: measure it on the real board before cutting the 75 x 50 mm windows. Also confirm the
  logic level (not stated), the backlight tie-off, and that an ILI9488 driver library works on the Teensy 4.1.
- [ ] **Verify the Teensy's physical pin order** against [PJRC's pinout card](https://www.pjrc.com/store/teensy41.html). The diagram's order is from memory.
- [ ] **Fader and nubbin stock** was only 37 each at Digi-Key; order early.
- [ ] Re-run `python3 tools/parts.py budget --live --md` right before ordering (it re-checks price and stock), then place the Digi-Key order (36 lines, about $370) and the Amazon order.
- [ ] **Not yet specified, buy as needed:** solder and flux, cable clips and zip ties, M3 screws and heat-set inserts (the fader needs two countersunk M3), 20 mm silicone feet, filament (2 to 3 kg), board standoffs, connectors for the sticks and encoders.

## 2. When the parts arrive: measure and bench-test

- [ ] **Joysticks**: measure the flange, mounting hole spacing and diameter, and cutout depth; find the pin order. Replace the provisional 52 x 42 mm cutout.
- [ ] **USB extension**: measure the real cutout and replace the orange placeholder in `hardware/cad/console.scad` (the datasheet has no cutout).
  The DC jack and fuse holder cutouts now come from their datasheets; check them against the real parts.
- [ ] **Fader**: confirm the dimensions I read from a scanned drawing (face about 146.5 x 17.2 mm, M3 holes 120 mm apart, 26 mm deep).
- [ ] **Encoders**: check the bushing diameter and thread against the 7 mm hole; the sources disagree on M7 x 0.75 vs 0.5.
- [ ] **Pixel boards**: measure the diameter and height with calipers; set `pixel_d` and `pixel_h` in `hardware/cad/test_plate.scad`.
- [ ] **Keycaps**: measure the real height from the plate with a switch fitted (the mockup assumes 13.5 mm).
- [ ] **Buzzer module**: 5 V across it with I/O held low. Continuous tone means active (one pitch); a click means passive. Measure the board and buzzer diameter.
- [ ] **Phoenix cables**: measure one conductor's resistance (a 1 m, 28 AWG conductor is about 0.2 ohm) to infer the gauge, since the datasheet has none, and re-check the 5 V pin budget in `hardware/electronics/wiring/wiring-checklist.md`.
- [ ] **Fader motor**: measure its current at 5 V, check it moves smoothly. If it is weak, switch to a 12 V input with two bucks (see the 12 V discussion).
- [ ] **Fader touch sensing**: Teensy 4.1 has no `touchRead()`. Try the FastTouch library on the conductive nubbin, or fall back to detecting your hand
  from wiper movement the motor did not cause.
- [ ] **Expander**: bus-scan the MCP23017 (expect 0x20 with A0 to A2 on GND), check the interrupt, and test I2C over the DB25 cable at about 30 cm, 400 kHz, 4.7 k pull-ups.
- [ ] **Simpit**: confirm the throttle command's value range, and how throttle authority is handed back when you stop sending it. Install the Alternate Resource Panel mod.
- [ ] **STAGE key and big button**: wire and test the interlock. Decide the LED (always on, or driven).

## 3. Printing

- [ ] **Print the key-and-pixel test plate** (`hardware/cad/test_plate.scad`): MX cutout tolerance (13.95 to 14.2 mm), diffuser thickness (0.4 to 1.0 mm).
- [ ] **Prop the plate at 28 degrees with real DSA caps** and check the pixel above each key is visible past the cap in front.
- [ ] **Print one wing shell**: check the ballast fit, the bed fit, the narrower wings under your hands, and that the stick clears the encoder.
- [ ] **Bed fit**: the strips use 245 of the 256 mm bed. Check your slicer's brim and skirt leave room.
- [ ] **Keyboard**: stand the 12.2 in 60% in the 345 mm gap and check the fit and your wrist room.
- [ ] Choose PLA or PETG, and colours.
- [ ] Paint the steel plates (they arrive oily and will rust).

## 4. CAD still to do

- [ ] Screw bosses and the rebate lip for the faceplates.
- [ ] Joints and alignment between the five pieces (screws or dowels, so they act as one mass).
- [ ] Internal mounts: fader, sticks, encoders, TFT displays, Teensy, perfboards (printed standoffs).
- [ ] Ballast hold-down for the steel plates (a strap with two screws, or corner ribs).
- [ ] Cable management behind the console (clips or a channel, strain relief). Leave a few centimetres beside each wing for the cable plugs.
- [ ] Annunciator light box: separate cells, diffuser windows, legend.
- [ ] Panel labels: engraved, printed, or a two-colour plate like goodnight-device.
- [ ] 1:1 paper templates for the five pieces (`openscad -D flat=true -D mod=N`, see `hardware/mockup/README.md`).

## 5. Decisions still open

- [ ] **Encoder push functions** (time warp, camera, display page). Suggestions in `design/controls.md`.
- [ ] **Display page contents**, and which events sound the buzzer.
- [ ] **The two spare switch-panel buttons**: camera mode (V) and action group 10 are the suggestions.
- [ ] **Annunciator**: thresholds, colour bands, and the CHUTE SAFE and STABLE ORBIT logic; off when fine or green when fine.
- [ ] **Round attitude TFT**: include or not.
- [ ] **Column pitch**: 19.05 mm for now, 22 to 25 mm gives more finger room.
- [ ] **Keycap colours** and the labelling approach.
- [ ] **Fine-control factor** for the left grip button (25% proposed).
- [ ] **Later**: whether to design a PCB for the middle strip once the wiring is proven.

## 6. Firmware to write

- [ ] Key assignment map and the Simpit channel list.
- [ ] Matrix scan (rows driven low one at a time, others high impedance) and the expander handling.
- [ ] Pixel chain: serpentine mapping across 65 pixels, and a **brightness cap** (worst case is 3.9 A, which the 4 A adapter cannot sustain).
- [ ] ENGAGE / DISENGAGE logic, the STAGE key interlock, and the grip buttons (SAS toggle right, fine control left).
- [ ] Throttle: fader follows the game when untouched, you drive it when touched; FULL and CUT buttons.
- [ ] Stick calibration (the pots are +/-20% tolerance): centre and range.
- [ ] Annunciator logic and the buzzer events.

## 7. Build and bring-up

- [ ] Wire the electronics per `hardware/electronics/wiring/wiring-checklist.md` and `hardware/electronics/electronics-build.md`.
- [ ] Check the 5 V rail polarity on the panel jack with a meter before connecting anything.
- [ ] Run the continuity checks before first power-up, then bring up one outer piece at a time.

## 8. Housekeeping

- [ ] Keep `hardware/sourcing/amazon-items.json` and `hardware/sourcing/parts-shortlist.json` current as you order, then run `make` to regenerate `hardware/sourcing/parts.md`.
- [ ] Run `make check` before each push. CI runs it too.

## 9. Documentation (so a beginner can follow it)

- [ ] **First build photos** as they exist: see the list in [gallery.md](../gallery.md).
- [ ] **A journey entry after each stage**, with a row in the mistakes table for anything that went wrong: [journey.md](../journey.md).
- [ ] **Fill in "Why a Teensy 4.1 and not an Arduino?"** in [why-not.md](why-not.md) in your own words.
- [ ] **Promote a fact's status** (Seller claim to Measured to Tested) in the docs whenever you check one on a real part.
- [ ] **Run the PlatformIO build once** and update the status in [firmware/README.md](../../firmware/README.md) and [getting-started.md](../getting-started.md).
- [ ] **Write the bring-up test programs** (raw pin readings over USB) that phase 5 of [bring-up.md](../../hardware/electronics/bring-up.md) needs.
- [ ] **Set the GitHub repo description and topics**, and turn on Pages if it is not on (Settings, Pages, branch `main`, folder `/docs`).

## Maintainer notes (not part of the build)

- Optional: ask GitHub Support to garbage-collect the repo so the old pre-scrub commits are no longer reachable by hash.
