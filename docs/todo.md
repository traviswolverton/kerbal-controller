# To do

Compiled from the design session on 2026-10-20. Check items off as you go. Where something is already written down, the file is named.

## 1. Before you order

- [ ] **Fill in any remaining Amazon prices** (check `docs/amazon-items.json` for `null`), then run
  `python3 docs/tools/parts.py budget --md`. Use `amazon-price ASIN PRICE`.
- [ ] **Buy about 4.6 kg of ballast steel locally** (see `fabrication.md`); the Amazon plate listings were dead.
- [ ] **Check the AITRIP photos show a bat-handle toggle with a flip cover**, not a flat rocker. Three of the six switches depend on it
  (ABORT, ENGAGE / DISENGAGE, master power).
- [ ] **Confirm the key switch's key position**: in the E-Switch KO133A801 datasheet, is position 1 (key removable) OFF?
- [ ] **Waveshare OLED**: check the board outline against the 58 x 31 mm window, and decide 3.3 V or 5 V supply. I never verified its price,
  so the earlier "about $15" claim is unconfirmed.
- [ ] **Verify the Teensy's physical pin order** against [PJRC's pinout card](https://www.pjrc.com/store/teensy41.html). The diagram's order is from memory.
- [ ] **Fader and nubbin stock** was only 37 each at Digi-Key; order early.
- [ ] Re-run `python3 docs/tools/parts.py check --md` right before ordering, then place the Digi-Key order (35 lines, about $316) and the Amazon order.
- [ ] **Not yet specified, buy as needed:** solder and flux, cable clips and zip ties, M3 screws and heat-set inserts (the fader needs two countersunk M3), 20 mm silicone feet, filament (2 to 3 kg), board standoffs, connectors for the sticks and encoders.

## 2. When the parts arrive: measure and bench-test

- [ ] **Joysticks**: measure the flange, mounting hole spacing and diameter, and cutout depth; find the pin order. Replace the provisional 52 x 42 mm cutout.
- [ ] **Panel jack, fuse holder, USB extension**: measure real cutouts and replace the three orange placeholders in `cad/console_mockup_v1.scad`
  (the jack's datasheet is an image, so its cutout was never verified).
- [ ] **Fader**: confirm the dimensions I read from a scanned drawing (face about 146.5 x 17.2 mm, M3 holes 120 mm apart, 26 mm deep).
- [ ] **Encoders**: check the bushing diameter and thread against the 7 mm hole; the sources disagree on M7 x 0.75 vs 0.5.
- [ ] **Pixel boards**: measure the diameter and height with calipers; set `pixel_d` and `pixel_h` in `cad/test_plate.scad`.
- [ ] **Keycaps**: measure the real height from the plate with a switch fitted (the mockup assumes 13.5 mm).
- [ ] **Buzzer module**: 5 V across it with I/O held low. Continuous tone means active (one pitch); a click means passive. Measure the board and buzzer diameter.
- [ ] **Fader motor**: measure its current at 5 V, check it moves smoothly. If it is weak, switch to a 12 V input with two bucks (see the 12 V discussion).
- [ ] **Fader touch sensing**: Teensy 4.1 has no `touchRead()`. Try the FastTouch library on the conductive nubbin, or fall back to detecting your hand
  from wiper movement the motor did not cause.
- [ ] **Expander**: bus-scan the MCP23017 (expect 0x20 with A0 to A2 on GND), check the interrupt, and test I2C over the DB25 cable at about 30 cm, 400 kHz, 4.7 k pull-ups.
- [ ] **Simpit**: confirm the throttle command's value range, and how throttle authority is handed back when you stop sending it. Install the Alternate Resource Panel mod.
- [ ] **STAGE key and big button**: wire and test the interlock. Decide the LED (always on, or driven).

## 3. Printing

- [ ] **Print the key-and-pixel test plate** (`cad/test_plate.scad`): MX cutout tolerance (13.95 to 14.2 mm), diffuser thickness (0.4 to 1.0 mm).
- [ ] **Prop the plate at 28 degrees with real DSA caps** and check the pixel above each key is visible past the cap in front.
- [ ] **Print one wing shell**: check the ballast fit, the bed fit, the narrower wings under your hands, and that the stick clears the encoder.
- [ ] **Bed fit**: the strips use 245 of the 256 mm bed. Check your slicer's brim and skirt leave room.
- [ ] **Keyboard**: stand the 12.2 in 60% in the 345 mm gap and check the fit and your wrist room.
- [ ] Choose PLA or PETG, and colours.
- [ ] Paint the steel plates (they arrive oily and will rust).

## 4. CAD still to do

- [ ] Screw bosses and the rebate lip for the faceplates.
- [ ] Joints and alignment between the five pieces (screws or dowels, so they act as one mass).
- [ ] Internal mounts: fader, sticks, encoders, OLEDs, Teensy, perfboards (printed standoffs).
- [ ] Ballast hold-down for the steel plates (a strap with two screws, or corner ribs).
- [ ] Cable management behind the console (clips or a channel, strain relief). Leave a few centimetres beside each wing for the cable plugs.
- [ ] Annunciator light box: separate cells, diffuser windows, legend.
- [ ] Panel labels: engraved, printed, or a two-colour plate like goodnight-device.
- [ ] 1:1 paper templates for the v1 pieces (the old v0 PDFs are stale and Chromium is not installed here to rebuild them).
- [ ] Update `docs/mockup/README.md`, which still describes the earlier three-module layout.

## 5. Decisions still open

- [ ] **Encoder push functions** (time warp, camera, display page). Suggestions in `controls.md`.
- [ ] **OLED page contents**, and which events sound the buzzer.
- [ ] **The two spare switch-panel buttons**: camera mode (V) and action group 10 are the suggestions.
- [ ] **Annunciator**: thresholds, colour bands, and the CHUTE SAFE and STABLE ORBIT logic; off when fine or green when fine.
- [ ] **Round attitude TFT**: include or not.
- [ ] **Column pitch**: 19.05 mm for now, 22 to 25 mm gives more finger room.
- [ ] **Keycap colours** and the labelling approach.
- [ ] **Fine-control factor** for the left grip button (25% proposed).
- [ ] **Later**: whether to design a PCB for the middle strip once the wiring is proven; a Star Citizen firmware.

## 6. Firmware to write

- [ ] Key assignment map and the Simpit channel list.
- [ ] Matrix scan (rows driven low one at a time, others high impedance) and the expander handling.
- [ ] Pixel chain: serpentine mapping across 65 pixels, and a **brightness cap** (worst case is 3.9 A, which the 4 A adapter cannot sustain).
- [ ] ENGAGE / DISENGAGE logic, the STAGE key interlock, and the grip buttons (SAS toggle right, fine control left).
- [ ] Throttle: fader follows the game when untouched, you drive it when touched; FULL and CUT buttons.
- [ ] Stick calibration (the pots are +/-20% tolerance): centre and range.
- [ ] Annunciator logic and the buzzer events.

## 7. Build and bring-up

- [ ] Wire the electronics per `docs/wiring-checklist.md` and `docs/electronics-build.md`.
- [ ] Check the 5 V rail polarity on the panel jack with a meter before connecting anything.
- [ ] Run the continuity checks before first power-up, then bring up one outer piece at a time.

## 8. Housekeeping

- [ ] Optional: ask GitHub Support to garbage-collect the repo so the old pre-scrub commits are no longer reachable by hash.
- [ ] Keep `docs/amazon-items.json` and `docs/parts-shortlist.json` current as you order, then regenerate `docs/budget.md`.
