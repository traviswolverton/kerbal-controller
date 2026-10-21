# Getting started

> **What this covers:** the tools you need, how to rebuild every generated file with one command, and how to check nothing is stale.  
> **Read it if:** you want to run, change or build on the repo. You do **not** need any of this just to read it.  
> **Status:** Tested for the Python tools and the wiring generator (the offline tests pass). **Not yet run:** the firmware build with PlatformIO and the OpenSCAD renders from this page's commands on a clean machine.  
> **Next:** [how it works](how-it-works.md) if you are new, or the [to-do](design/todo.md) to see what is next.

## What you need

| Tool | Needed for | Required? | Notes |
|---|---|---|---|
| **Git** | getting the repo | yes | `git clone https://github.com/traviswolverton/kerbal-controller.git` |
| **Python 3** (written with 3.12) | the scripts in `tools/` | yes | Standard library only. There is nothing to `pip install` |
| **make** | the one-command build | recommended | Pre-installed on Linux and macOS. On Windows use WSL or run the commands by hand |
| **OpenSCAD** | rebuilding STLs and renders | only for CAD | https://openscad.org. Renders also need a virtual display (`xvfb-run`) on a server |
| **PlatformIO** | compiling and uploading firmware | only for firmware | The CLI is enough: https://platformio.org |
| **Digi-Key / Mouser API keys** | the live parts search | **no**, optional | Free accounts. See [tools/README.md](../tools/README.md). The committed `parts.md` needs none |

## The one command

From the repo root:

```bash
make
```

That runs, in order: the wiring generator, the parts-list generator and the site image copy. Everything it writes is a **generated file**.

| Command | What it does |
|---|---|
| `make` | Regenerates the wiring docs, diagrams, `pins.h`, `parts.md` and the site images |
| `make test` | Runs the offline tests (no network, no keys) |
| `make check` | Regenerates everything in memory and fails if a committed file is out of date. This is what proves the wiring and the firmware pins cannot drift |
| `make help` | Lists the targets |

The GitHub Action in `.github/workflows/ci.yml` runs `make test` and `make check` on every push, so a stale generated file shows as a red mark.

## Change something

| I want to... | Edit this | Then run |
|---|---|---|
| Move a pin | `hardware/electronics/pinmap.json` | `make` |
| Change a part, its note or its price | `hardware/sourcing/parts-shortlist.json` or `amazon-items.json` | `make` (or `python3 tools/parts.py budget --md --live` to re-check live prices) |
| Change a panel layout | `hardware/cad/console.scad` | see [mockup](../hardware/mockup/README.md) for the render commands |
| Write firmware | `firmware/ksp/src/main.cpp` | `pio run -d firmware/ksp` |

Do not hand-edit a file marked **generated**: the next `make` overwrites it, and `make check` will fail.

## Build the firmware

```bash
pio run -d firmware/ksp               # compile
pio run -d firmware/ksp -t upload     # upload to a connected Teensy (you may need to press its button)
```

The first run downloads the Teensy toolchain and the Simpit library. As of 2026-10-21 this has not been run in this repo, and the
firmware is a stub, so expect to fix a pin or version problem on the first try. The [firmware README](../firmware/README.md) has details.

## Rebuild the images

See [hardware/mockup/README.md](../hardware/mockup/README.md) for the OpenSCAD commands. The test-plate STLs are made as shown in
[hardware/cad/README.md](../hardware/cad/README.md).
