# CAD

> **What this covers:** the OpenSCAD source, and the test plate that checks the key and light fit before the big print.  
> **Read it if:** you want to print the test plate or change the design.  
> **Status:** Planned. The test plate is drawn and its STLs are exported, but it has not been printed.  
> **Next:** [fabrication estimate](fabrication.md).

Parametric OpenSCAD source. STL exports live in `stl/`.

## test_plate.scad

A 2 x 2 test of layout B (19.05 mm columns, 36 mm rows), with a 10 mm WS2812B pixel
board in a pocket above each key. Three parts print separately and stack:

| Part | Thickness | Filament | Purpose |
|---|---|---|---|
| `test_plate_plate.stl` | 1.5 mm | black | MX cutouts, light window above each key, diffuser counterbore on the underside |
| `test_plate_diffusers.stl` | 0.4 / 0.6 / 0.8 / 1.0 mm | white or natural | thin discs that sit in the counterbores |
| `test_plate_spacer.stl` | 5.0 mm | black | key cavities, pixel pockets, wire channel |

Order, row-major from the top left (key 1 and 2, then 3 and 4):

- **MX cutout:** 13.95, 14.00, 14.10, 14.20 mm. Find the one where a switch clicks in snugly.
- **Diffuser disc:** 0.4, 0.6, 0.8, 1.0 mm. Pick the thinnest one that hides the LED chip.

Stack from the bottom: spacer, pixel in its pocket (LED up), diffuser disc, plate. Screw the
four corners (3.2 mm holes; use about 4.2 mm for heat-set inserts in the spacer).

Before printing, measure your pixel boards and edit `pixel_d` and `pixel_h` at the top of the file.

```
openscad -D 'part="plate"'     -o stl/test_plate_plate.stl     test_plate.scad
openscad -D 'part="spacer"'    -o stl/test_plate_spacer.stl    test_plate.scad
openscad -D 'part="diffusers"' -o stl/test_plate_diffusers.stl test_plate.scad
```

Not yet verified by a real print. In particular the MX cutout is a plain 14 mm square
(no side notches), and the pixel pad positions on the board are assumed.

## Checking pixel visibility

Fit the switches and keycaps, then prop the plate at about 28 degrees (a book or a wedge) and look at it from
where you would sit. The pixel above each key should be clearly visible past the keycap in front. If it is
not, we need a steeper tilt, a bigger row pitch, or a raised light post.

## console.scad

The five-piece console layout. See `../mockup/README.md`. The render and template commands are at the top of the file.
`hardware/cad/tools/stl_volume.py` measures shell and plate volume from exported STLs, and `fabrication.md` has the filament and weight estimate.
