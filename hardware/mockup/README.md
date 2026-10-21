# Console mockup

> **What this covers:** the renders of the five-piece console, the size of each piece, and how to regenerate the pictures.  
> **Read it if:** you want to see the design, or change it.  
> **Status:** Planned. A model only; part shapes are simple blocks and nothing is printed.  
> **Next:** [the CAD](../cad/README.md).

Renders of the current layout, generated from [`hardware/cad/console.scad`](../cad/console.scad). The panel
contents of each piece are in [controls.md](../../docs/design/controls.md); the sizes and layout choices are in
[decisions.md](../../docs/design/decisions.md).

## Renders (`renders/`)

| File | Shows |
|---|---|
| `iso.png`, `top.png`, `front.png`, `rear.png`, `side.png` | overall views |
| `seat-view.png` | what you see from a seat |
| `wing-cutaway.png`, `strip-cutaway.png` | the shells cut open: ballast, feet, jacks, wall thickness |

Regenerated 2026-10-21 from the current model: the two TFT windows, the horizontal fuel bars, and the DC jack and fuse holder cutouts from their datasheets. The USB extension's cutout is still an orange placeholder (see the rear view).

## Pieces

| Piece | Width | Tilt | Contents |
|---|---|---|---|
| Left wing | 195 mm | 12 deg | stick, motorised fader, time-warp encoder |
| Right wing | 195 mm | 12 deg | stick, camera and display-page encoders |
| Strip left | 245 mm | 28 deg | 12 navigation keys and the switch panel |
| Strip middle | 245 mm | 28 deg | 2 TFT displays, 4 fuel bars, buzzer, master power switch |
| Strip right | 245 mm | 28 deg | 12 action-group keys and the annunciator |

The console is 735 mm wide with a 345 mm open middle, designed around a 12.2 in (310 mm) 60% keyboard.

## Regenerating

```
make renders            # rewrites every picture in renders/ (needs openscad and xvfb-run)
make site               # then copies iso.png and seat-view.png to docs/img/ for the Pages landing page
openscad -D flat=true -D mod=0 -o left_wing.svg hardware/cad/console.scad    # 1:1 template of piece 0
```

The cameras for each picture are in [`hardware/cad/render.sh`](../cad/render.sh).

There is no one-step build script. Part proxies (keycaps, knobs, toggles, grips) are simple blocks, not real models.
The USB extension's cutout is still an orange placeholder.
