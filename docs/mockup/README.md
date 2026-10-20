# Console mockup (v1, five pieces)

Renders of the current layout, generated from [`cad/console_mockup_v1.scad`](../../cad/console_mockup_v1.scad). The panel
contents of each piece are in [controls.md](../design/controls.md); the sizes and layout choices are in
[decisions.md](../design/decisions.md). The earlier three-module layout is archived in
[`docs/archive/v0-mockup/`](../archive/v0-mockup/README.md).

## Renders (`renders/`)

| File | Shows |
|---|---|
| `v1-iso.png`, `v1-top.png`, `v1-front.png`, `v1-rear.png`, `v1-side.png` | overall views |
| `v1-seat-view.png` | what you see from a seat |
| `v1-wing-cutaway.png`, `v1-strip-cutaway.png` | the shells cut open: ballast, feet, jacks, wall thickness |

The renders were last generated before the DC jack and fuse holder cutouts were corrected, so the middle strip's back wall differs slightly.

## Pieces

| Piece | Width | Tilt | Contents |
|---|---|---|---|
| Left wing | 195 mm | 12 deg | stick, motorised fader, time-warp encoder |
| Right wing | 195 mm | 12 deg | stick, camera and display-page encoders |
| Strip left | 245 mm | 28 deg | 12 navigation keys and the switch panel |
| Strip middle | 245 mm | 28 deg | 2 OLEDs, 4 fuel bars, buzzer, master power switch |
| Strip right | 245 mm | 28 deg | 12 action-group keys and the annunciator |

The console is 735 mm wide with a 345 mm open middle, designed around a 12.2 in (310 mm) 60% keyboard.

## Regenerating

```
xvfb-run -a openscad -o out.png --imgsize=1800,900 --projection=p --camera=cx,cy,cz,rx,ry,rz,dist cad/console_mockup_v1.scad
openscad -D flat=true -D mod=0 -o left_wing.svg cad/console_mockup_v1.scad    # 1:1 template of piece 0
```

There is no one-step build script for v1. Part proxies (keycaps, knobs, toggles, grips) are simple blocks, not real models.
The USB extension's cutout is still an orange placeholder.
