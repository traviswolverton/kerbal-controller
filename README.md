# Kerbal controller

[![CI](https://github.com/traviswolverton/kerbal-controller/actions/workflows/ci.yml/badge.svg)](https://github.com/traviswolverton/kerbal-controller/actions/workflows/ci.yml)

![The five-piece console, rendered](hardware/mockup/renders/iso.png)

A physical control panel for **Kerbal Space Program 1** (a spaceflight game): two joysticks, a motorised throttle slider,
keys that light up to show the game's state, two small screens, and a row of guarded switches like a real cockpit. It plugs
into a Windows PC with one USB cable. It is designed and 3D printed in five pieces, and wired by hand.

This repo is the whole project, end to end, written for someone who knows none of it: why each choice was made, what every
part is, how it goes together, and what I got wrong along the way. **I am learning as I build, so I wrote it down.** If a
word or step is not explained where you meet it, that is a bug in the docs: please say so (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Where the project stands

Last updated 2026-10-21. Each stage is **Not started**, **In progress** or **Done**; [docs/README.md](docs/README.md) explains
how to read a fact's status (*Planned*, *Seller claim*, *Measured*, *Tested*).

| Stage | State | What exists |
|---|---|---|
| 1. Idea and requirements | Done | Goals and limits in [decisions.md](docs/design/decisions.md); what every control does in [controls.md](docs/design/controls.md) |
| 2. Choosing parts | In progress | Every part picked, priced and linked in [parts.md](hardware/sourcing/parts.md). **Nothing ordered yet.** Many specs are seller claims |
| 3. Shape and layout (CAD) | In progress | Five-piece model, renders and panel templates. A test plate is drawn but **not printed** |
| 4. Wiring design | In progress | Colour-coded diagrams and pin tables, generated from one data file. The Teensy's physical pin order is still from memory |
| 5. Firmware | Not started | A stub that compiles in principle and a design outline. The toolchain has not been run |
| 6. Printing | Not started | Waiting on the test plate |
| 7. Build and bring-up | Not started | The procedure is written: [bring-up.md](hardware/electronics/bring-up.md) |

The full list of what is left, in order and with what blocks what, is [docs/design/todo.md](docs/design/todo.md).

## New here? Read in this order

1. **[How it works](docs/how-it-works.md)**: one page, one picture, no jargon. How a twist of a knob becomes a rocket turning.
2. **[Glossary](docs/glossary.md)**: every term and part name used in the repo, in plain words. Keep it open in a tab.
3. **[Journey](docs/journey.md)**: the story so far, including the mistakes. The best place to see *how* the decisions were made.
4. **[Decisions](docs/design/decisions.md)** and **[Why not X?](docs/design/why-not.md)**: what was chosen, and what was rejected and why.
5. **[Controls](docs/design/controls.md)**: what each key, switch and knob does in the game.
6. **[Parts and budget](hardware/sourcing/parts.md)**: the shopping list at a glance, then every part with links.
7. **[CAD](hardware/cad/README.md)** and **[mockup](hardware/mockup/README.md)**: the shape of the console, and how it is printed.
8. **[Wiring](hardware/electronics/wiring/wiring.md)**, **[electronics build](hardware/electronics/electronics-build.md)** and the **[checklist](hardware/electronics/wiring/wiring-checklist.md)**.
9. **[First power-up](hardware/electronics/bring-up.md)**: the careful order for switching a new build on for the first time.
10. **[Firmware](firmware/README.md)** and its **[architecture outline](docs/firmware/architecture.md)**.

Want to build your own? Start with [Getting started](docs/getting-started.md): the tools you need and the one command that
rebuilds every generated file. Pictures are in the [gallery](docs/gallery.md).

## The five pieces

A raised, steep back strip of three pieces, with two lower wings at the front ends and the middle front left
open. Each piece is a printed shell with a removable 3 mm faceplate. The console is 735 mm wide and
**designed around a 12.2 in (310 mm) 60% keyboard** that stands in the open middle (a 345 mm gap). It is printed in pieces
because the printer's bed is only 256 mm across.

| Piece | Tilt | Holds |
|---|---|---|
| Left wing | 12 deg | translation stick, motorised throttle fader, time-warp encoder |
| Right wing | 12 deg | rotation stick, camera and display-page encoders |
| Strip left | 28 deg | 12 navigation / SAS keys and the switch panel: 16 inputs (ABORT, a STAGE key switch, big STAGE button, throttle FULL/CUT, utility buttons, ENGAGE / DISENGAGE) on an I2C expander |
| Strip middle | 28 deg | 2 TFT displays, 4 fuel bars, buzzer, guarded master power switch, Teensy, power input |
| Strip right | 28 deg | 12 action-group keys and a 3 x 3 annunciator (low fuel, low power, overheat, low altitude, ...) |

Key choices: two JH-D400X-R4 joysticks, 24 MX-style keys with a pixel above each one, a 100 mm motorised
fader, 5 V power from a wall adapter, and one DB25 cable from each outer piece to the middle strip.
(Every one of those terms is in the [glossary](docs/glossary.md).)

## Where things are

| Folder | What it has |
|---|---|
| `docs/` | project-wide prose and the GitHub Pages site: [README](docs/README.md) (map and conventions), [how-it-works](docs/how-it-works.md), [glossary](docs/glossary.md), [journey](docs/journey.md), [getting-started](docs/getting-started.md), [gallery](docs/gallery.md) |
| `docs/design/` | `decisions.md` (what is settled, why, what is open), `why-not.md` (what was rejected), `controls.md` (the key map) and `todo.md` (what is left) |
| `docs/firmware/` | the firmware architecture outline |
| `docs/pinout.html` | the wiring diagrams as one browser page (https://traviswolverton.github.io/kerbal-controller/pinout.html); generated |
| `hardware/cad/` | OpenSCAD source (`console.scad`, `test_plate.scad`), STLs, and `fabrication.md` (filament, weight, print orientation) |
| `hardware/electronics/` | `pinmap.json` (the pin data), `electronics-build.md`, `bring-up.md`, and `wiring/`: colour-coded diagrams, pin tables and the wiring checklist |
| `hardware/sourcing/` | `parts.md` (every part, links, notes and the budget; generated) and its two data files, `parts-shortlist.json` and `amazon-items.json` |
| `hardware/mockup/` | renders of the five-piece layout |
| `hardware/reference/` | joystick photo, pitch examples and manufacturer DXF outlines |
| `firmware/ksp/` | the PlatformIO project for the Teensy (a stub for now) |
| `tools/` | scripts: parts search and budget (`parts.py`), wiring and pin-header generator (`gen_wiring.py`), tests |

The pin assignment lives in `hardware/electronics/pinmap.json`. `python3 tools/gen_wiring.py` turns it into the wiring docs,
the Pages diagrams and `firmware/ksp/include/pins.h`, so the firmware and the wiring cannot drift apart. `make check` proves
it (see [Getting started](docs/getting-started.md)).

## Sourcing

Parts come from US retailers only. Selection uses the Digi-Key and Mouser APIs through `tools/parts.py` (free
accounts needed, see `tools/README.md`); Amazon.com covers what they do not carry. You do **not** need an account to read
the repo: `parts.md` is a saved, dated snapshot. See `CLAUDE.md`.

## Inspiration

The stepped layout (raised back panels, lower wings with the sticks) and the modular, swappable-faceplate
build style follow [Altitude Workshops' Simpit KSP](https://altitudeworkshops.weebly.com/simpit-ksp.html),
a five-panel Apollo-style KSP controller. That build uses one joystick and a throttle lever; this one uses
two joysticks and a motorised fader.

## Licence

MIT, see [LICENSE](LICENSE).
