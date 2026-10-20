# Fabrication estimate

First estimate of filament, weight and print orientation for the five-piece console
(`hardware/cad/console.scad`). The shells are modelled as plain hollow boxes: no ribs, screw bosses, cable
holes or joints yet, so treat the numbers as a floor and expect to add about 15%.

## Filament

Hollow shells (2.4 mm walls and floor, open top) plus separate 3 mm faceplates, exported to STL from OpenSCAD and
measured. PLA at 1.24 g/cm3, walls counted as 100% solid.

| Piece | Shell | Faceplate | Total |
|---|---|---|---|
| Left wing | 195 g | 120 g | 315 g |
| Right wing | 195 g | 122 g | 317 g |
| Strip left | 280 g | 100 g | 380 g |
| Strip middle | 274 g | 105 g | 379 g |
| Strip right | 280 g | 103 g | 383 g |
| **Modelled** | | | **1.77 kg** |
| **With +15% for ribs, bosses, retainers** | | | **about 2.0 kg** |

Budget 2 to 3 spools (1 kg each) once test prints and reprints are included. PETG is about 2% heavier.
Print time is about 70 to 140 hours at 15 to 30 g/h. A 0.6 mm nozzle roughly halves it.

## Weight and not sliding

The printed pieces plus parts weigh only about 3 kg, which a hand on the throttle or a tug on a cable can move.

- **Ballast:** 8 weight-vest steel plates per wing, 16 in all (Mavee, [Amazon short link](https://a.co/d/0axItt4q), 2 packs of 8
  at $25.99). Each is 5.9 x 0.98 x 0.28 in (150 x 25 x 7.1 mm), listed at 0.44 lb, so a wing takes about 1.6 kg and the pair
  about 3.2 kg. They lie on the floor of each wing as 4 side by side in two layers: a block about 100 x 150 x 14.2 mm. The
  pocket takes 12 per wing (6 across), so a third pack (4.8 kg in all) can be added later if the console still creeps.
  They are plated, so no painting. Weigh one on arrival, and any equivalent steel totalling about 3 kg will do.
- **Clearance:** the block sits under the stick, clear of the fader body (the left wing's block starts at u = 38 mm). By my
  calculation from the 30 mm front height, the 12 degree tilt and the 3 mm faceplate, the roof is only about 13 mm above the
  block at its front edge (y = 12 mm), rising to about 45 mm at the back. Check the stick, encoder and fader fit.
- **Hold-down:** thin loose plates need holding: a printed tray with a strap or lid. Not designed yet.
- **Feet:** four 20 mm self-adhesive silicone feet per piece, in recesses 30 mm in from each corner.
- **Total:** about 6 kg with the ballast (about 8 kg with the third pack). With rubber feet (friction about 0.6) that resists
  roughly 36 N before sliding (about 46 N with three packs). A wing on its own, about 2.6 kg, resists about 15 N, so joining the
  pieces matters. My assumed loads are 5 to 10 N from a stick and a few newtons from a cable tug. Not measured.
- **Join the pieces** with screws or dowels so the five act as one mass. Not designed yet.
- Avoid lead. Fall back to desk clamps if it still creeps.

## Print orientation

- Each shell prints floor down with the open sloped top facing up: the walls rise straight, so I expect no supports.
- Faceplates print flat.
- Largest envelopes: wings 195 x 176 x 67 mm, strips 245 x 119 x 128 mm. All fit the 256 mm bed, with 11 mm to spare on the strips. The console is 735 mm across (see the keyboard note in `design/decisions.md`).

## Not designed yet

- Hold-down for the steel plates (a printed strap with two screws, or corner ribs).
- Faceplate screw bosses and the rebate lip.
- Joints and alignment between pieces.
- Cable management behind the console. The DC jack and fuse holder cutouts come from their datasheets; only the USB extension's cutout is still a provisional placeholder.
- DB25 jacks are modelled: cutouts 42.52 x 11.40 mm with two mounting holes, on each wing's outer end wall and the strips' back walls.
- Internal mounts: the fader, stick, encoders, TFT displays, Teensy and DC jack.

Renders: `hardware/mockup/renders/wing-cutaway.png` and `strip-cutaway.png`.
