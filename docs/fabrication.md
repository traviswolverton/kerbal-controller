# Fabrication estimate

First estimate of filament, weight and print orientation for the five-piece console
(`cad/console_mockup_v1.scad`). The shells are modelled as plain hollow boxes: no ribs, screw bosses, cable
holes or joints yet, so treat the numbers as a floor and expect to add about 15%.

## Filament

Hollow shells (2.4 mm walls and floor, open top) plus separate 3 mm faceplates, exported to STL from OpenSCAD and
measured. PLA at 1.24 g/cm3, walls counted as 100% solid.

| Piece | Shell | Faceplate | Total |
|---|---|---|---|
| Left wing | 216 g | 136 g | 352 g |
| Right wing | 216 g | 139 g | 355 g |
| Strip left | 277 g | 98 g | 375 g |
| Strip middle | 277 g | 102 g | 379 g |
| Strip right | 259 g | 91 g | 350 g |
| **Modelled** | | | **1.81 kg** |
| **With +15% for ribs, bosses, retainers** | | | **about 2.1 kg** |

Budget 2 to 3 spools (1 kg each) once test prints and reprints are included. PETG is about 2% heavier.
Print time is about 70 to 140 hours at 15 to 30 g/h. A 0.6 mm nozzle roughly halves it.

## Weight and not sliding

The printed pieces plus parts weigh only about 3 kg, which a hand on the throttle or a tug on a cable can move.

- **Ballast:** two 6 x 6 x 1/4 in steel plates per wing (152.4 x 152.4 x 6.35 mm, about 1.16 kg each, 4.6 kg in all)
  lie on the floor of each wing. The 4-pack on Amazon is exactly four plates.
  [4-pack](https://www.amazon.com/clp/B07L7DPKW7), [single](https://www.amazon.com/Steel-Plate-A36-Steel-25-Thick/dp/B07VV618NN).
  Prices and stock not checked; one listing is nominally 15/64 in thick, so check before ordering.
  Wipe and paint the plates: they arrive oily and will rust.
- **Clearance:** the plates sit under the stick, clear of the fader body. The left wing's plates start at u = 58 mm,
  because the fader body occupies u 21 to 39 mm.
- **Feet:** four 20 mm self-adhesive silicone feet per piece, in recesses 30 mm in from each corner.
- **Total:** about 7 to 8 kg with the ballast. With rubber feet (friction about 0.6) that resists roughly 40 N
  before sliding. My assumed loads are 5 to 10 N from a stick and a few newtons from a cable tug. Not measured.
- **Join the pieces** with screws or dowels so the five act as one mass. Not designed yet.
- Avoid lead. Fall back to desk clamps if it still creeps.

## Print orientation

- Each shell prints floor down with the open sloped top facing up: the walls rise straight, so I expect no supports.
- Faceplates print flat.
- Largest envelopes: wings 220 x 176 x 67 mm, strips 220 to 240 x 119 x 128 mm (the left strip is now 240 mm wide, so the console is 700 mm across). All fit the 256 mm bed.

## Not designed yet

- Hold-down for the steel plates (a printed strap with two screws, or corner ribs).
- Faceplate screw bosses and the rebate lip.
- Joints and alignment between pieces.
- Cable management behind the console, and the cutouts for the DC jack, fuse holder and USB extension.
- DB25 jacks are modelled: cutouts 42.52 x 11.40 mm with two mounting holes, on each wing's outer end wall and the strips' back walls.
- Internal mounts: the fader, stick, encoders, OLEDs, Teensy and DC jack.

Renders: `docs/mockup/v1/renders/v1-wing-cutaway.png` and `v1-strip-cutaway.png`.
