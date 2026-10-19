# Console mockup (v0 proposal)

A first full layout to react to, not a finished design. Everything is generated from
`cad/console_mockup.scad`; run `cad/build_mockup.sh` to rebuild the images and templates.

## Renders (`renders/`)
- `console-iso.png`, `console-top.png`, `console-front.png`: overall views.
- `console-side-center.png`: profile of the steeper centre module.
- `seat-view.png`: what you see from a seat (eye 450 mm above the desk, 400 mm in front).
- `seat-view-center-tilt12.png`: the same with the centre at 12 degrees, to show why it is steeper.

## Paper templates (`templates/`)
One 1:1 template per module, as SVG and PDF. The PDFs use a custom page size (about 240-260 mm
square), so print them at 100% on a large-format printer or a copy shop, or tile them from the SVG.
Each has a 100 mm scale bar: measure it on the printout. Cut the template out and rest your hands on it.

## What is in each module
| Module | Width | Tilt | Contents |
|---|---|---|---|
| Left | 220 mm | 12 deg | Left stick (translation X/Y, twist = Z), 100 mm throttle fader with a ghost strip of 8 pixels, time-warp encoder |
| Centre | 240 mm | 28 deg | 4 x 6 key bank with a pixel above each key, 4 guarded toggles (abort, stage arm, 2 spare), 2 OLEDs, 4 fuel bars of 8 pixels, buzzer |
| Right | 220 mm | 12 deg | Right stick (pitch/yaw, twist = roll), camera and display-page encoders |

Total width 680 mm. Each module is 245 mm deep, so it fits a 256 mm bed.

Key assignments, back row to front row:

| | | | | | |
|---|---|---|---|---|---|
| STAB | PRO | RETRO | NORM | A-NRM | MNVR |
| RAD-IN | RAD-OUT | TGT | A-TGT | SAS | RCS |
| GEAR | LIGHT | BRAKE | AG1 | AG2 | AG3 |
| AG4 | AG5 | AG6 | AG7 | AG8 | STAGE |

## Findings from the mockup
- **Pixels above the keys can be hidden by the keycap in front.** At the original 30 mm row pitch and a
  12 degree tilt they were invisible from a seated eye position; at 28 degrees only a sliver showed.
  With a 36 mm row pitch and a 28 degree centre panel they are fully visible. The side modules do not
  need to tilt as much because they have no tall keycaps.
- **Stick clearance.** A 38 mm ring around each stick (estimated tilt sweep of the grip) is drawn on the
  templates. Nothing else is inside it.

## What is provisional
- **Joystick flange and mounting holes are unknown.** The seller drawing is a side view only. The stick
  cutouts (52 x 42 mm) and flange outlines (62 x 62 mm) are placeholders, marked PROVISIONAL.
- Part proxies in the renders (keycaps, knobs, toggles, grips) are simple blocks, not real models.
- Positions are a proposal; move anything by editing the coordinates at the top of `console_mockup.scad`.
- Not modelled: the enclosure interior, wiring, the Teensy and the power supply.

## Questions for you
1. Does the left hand work with the fader and stick side by side, or do you want the fader on the inside?
2. Is the 28 degree centre panel comfortable, or too tall (back edge about 145 mm high)?
3. What should the two grip buttons do?
