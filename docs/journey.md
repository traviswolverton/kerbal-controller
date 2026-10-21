<!-- Drafted from the git history and docs/design/decisions.md. Edit in your own voice; add dated entries as the build goes on. -->
# Journey

> **What this covers:** the story of the project so far, stage by stage, including what went wrong and what I changed.  
> **Read it if:** you want to see *how* the decisions were made, not only what they were. It is the most useful page for a beginner.  
> **Status:** A log. It grows with the build. Last entry 2026-10-21.  
> **Next:** the [decisions](design/decisions.md) behind each entry, and [why not X?](design/why-not.md).

I started this project knowing how to solder and wanting a KSP controller. I did not know the parts, the vocabulary or the
traps. So every stage below ends with what I learned, and there is a list of mistakes at the bottom. If you are learning too,
the mistakes are the cheap way to learn.

## Stage 1: Deciding what to build (2026-10-10 to 10-19)

I fixed the limits first: KSP1 on Windows, a printer with a 256 mm bed, and comfortable with hand-wiring. A 256 mm bed means
a console wider than that has to be several pieces. I chose a **Teensy 4.1** as the one brain, and the **Simpit** mod to talk to the game.

Early purchases were things I already knew I wanted: a 72-pack of clicky keyboard switches and a pack of buzzer modules
(both owned, 2026-10-10). Then I picked the sticks: two industrial **JH-D400X-R4** joysticks, because they are what most KSP
controller builds use.

*Learned:* decide the limits (bed size, game version, skill) before the parts. They rule things out early.

## Stage 2: A layout you can see (2026-10-19)

I made a test plate for four keys with a light above each, then a full 3D mockup of the console in OpenSCAD with renders and
1:1 paper templates. I started with a three-piece idea, then moved to **five pieces**: a raised back strip in three parts and two
lower wings that hold the sticks.

Two big layout facts came from looking at the mockup and not from guessing:

- At a 12 degree tilt and a 30 mm row pitch, the light above each key was **hidden behind the keycap in front of it**. The fix was a steeper
  centre panel (28 degrees) and a 36 mm row pitch.
- I sized the whole console around a **12.2 inch 60% keyboard** standing in the gap between the wings. A full-size keyboard would
  have needed six pieces and about 940 mm.

*Learned:* draw it to scale early. A render found in an hour what would have cost a reprint.

## Stage 3: Choosing parts, and learning where to buy them (2026-10-19 to 10-21)

First I searched retail sites by hand. Then I wrote `tools/parts.py`, which uses the Digi-Key and Mouser APIs to get live price,
stock and datasheets. It is the more reliable source, and one distributor order is simpler than five. I kept Amazon for what
the distributors do not carry (the joysticks, switches, keycaps, guarded toggles, ballast plates).

Choices I changed as I learned more:

| Choice | Changed to | Why |
|---|---|---|
| Two small OLED screens | Two 3.5 inch **IPS** TFTs | The screens sit at 28 degrees, and an IPS panel looks right from an angle |
| An Adafruit 5 V adapter | A Mean Well adapter | Safety approval and a spec sheet I could read |
| A kit of panel DC jacks from Amazon | A Digi-Key jack with a datasheet | The datasheet gave the exact cutout size |
| An E-Switch toggle for master power | A guarded toggle from the same pack as ABORT | A bump cannot kill the lights, and a matched guard and toggle avoid a fit risk |
| Hand-picked knobs from an Amazon listing | A Digi-Key knob | The listing went dead |
| Plate listings for ballast | Weight-vest plates | The first listings were dead links |

*Learned:* a datasheet beats a product photo. Link rot is real: a part that vanishes from a shop vanishes from your plan.

## Stage 4: Wiring on paper (2026-10-19 to 10-21)

With dozens of wires to run from the Teensy to five pieces, I chose **one DB25 cable per outer piece**: one USB cable out,
one power input, no extra boards. I wrote the pin map once in `pinmap.json`, and a script (`gen_wiring.py`) turns it into the
diagrams, the pin tables and the firmware's `pins.h`. That removed the biggest risk, the wiring and the code disagreeing.

I also designed the cables so that a **cable plugged into the wrong port does no damage**: power and ground are on the same pins
on every connector, and everything the Teensy drives is kept off the pins another piece uses. A script checked all 16 combinations.

Then, because the DB25 connectors have very small solder cups, I **doubled the jack order** so there are spares to practise on
before wiring the real ones, and added a soldering-order diagram.

*Learned:* design for the mistake you will make (a cable in the wrong socket). And practise on a spare before the real thing.

## Stage 5: What is still ahead

Nothing has been ordered. Next is the [to-do list](design/todo.md): check the last Amazon prices and the guarded-toggle photos,
order, then measure everything when it arrives, print the test plate, and bring the electronics up one piece at a time.

## Things I got wrong, or that surprised me (and what fixed them)

| What went wrong | How it showed up | The fix |
|---|---|---|
| **Perfboard that shorts.** I picked a board whose pads are groups of five joined holes, like a breadboard | Found before ordering | Switched to **pad-per-hole** boards. The board for the busiest piece is still open |
| **Light hidden behind the keycap** | The 3D mockup | 28 degree centre tilt and 36 mm row pitch. Still to confirm on the printed test plate |
| **Dead shop links** | Knobs and ballast plates vanished from listings | Moved to Digi-Key or another live listing |
| **A "G-force" warning light** | I planned one. Then I found Simpit has no G-force message | Dropped. The window is now "CONTROLS" (lit while engaged) |
| **Assuming the Teensy can sense a touch** | The 4.1 has no `touchRead()` | Open: a library, or detect a hand from slider movement the motor did not cause |
| **The pixel chain can use the whole supply** | Adding up 65 lights at 60 mA each, all white, is 3.9 A from a 4 A adapter: no headroom | Cap brightness in firmware, and size the fuse to the capped load |
| **Pin order drawn from memory** | I drew the Teensy's physical pin order without checking | Flagged on the diagrams and in the checklist. To verify against PJRC's card before wiring |
| **A cable with no stated wire gauge** | The datasheet gave 1 A and no gauge | Treat each conductor as 1 A, share the heavy 5 V across two conductors, measure a real cable when it arrives |
| **Sources that disagree** | The encoder's thread is M7 x 0.75 on one site and M7 x 0.5 in the datasheet text | Use the nut that comes with it, and check on arrival |
| **A connector that is hard to solder** | The DB25 solder cups are tiny and 22 AWG wire barely fits | Thin stranded wire for signals, test-fit first, practise on the spare jacks |

## How to add an entry

Add a dated heading under the right stage, say what you did, and finish with *Learned:* in one line. If something went wrong,
add a row to the table above. Put photos in `docs/photos/` and link them (see [the gallery](gallery.md)).
