# Console mockup

Renders of the current layout, generated from [`hardware/cad/console.scad`](../cad/console.scad). The panel
contents of each piece are in [controls.md](../../docs/design/controls.md); the sizes and layout choices are in
[decisions.md](../../docs/design/decisions.md).

## Renders (`renders/`)

| File | Shows |
|---|---|
| `iso.png`, `top.png`, `front.png`, `rear.png`, `side.png` | overall views |
| `seat-view.png` | what you see from a seat |
| `wing-cutaway.png`, `strip-cutaway.png` | the shells cut open: ballast, feet, jacks, wall thickness |

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
xvfb-run -a openscad -o out.png --imgsize=1800,900 --projection=p --camera=cx,cy,cz,rx,ry,rz,dist hardware/cad/console.scad
openscad -D flat=true -D mod=0 -o left_wing.svg hardware/cad/console.scad    # 1:1 template of piece 0
```

There is no one-step build script. Part proxies (keycaps, knobs, toggles, grips) are simple blocks, not real models.
The USB extension's cutout is still an orange placeholder.
