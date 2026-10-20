# Firmware

Code that runs on the Teensy 4.1 and talks to KSP through the
[KerbalSimpitRevamped](https://github.com/Simpit-team/KerbalSimpitRevamped) mod. Nothing is written yet; the design outline is
in [`docs/firmware/architecture.md`](../docs/firmware/architecture.md).

| Path | What it is |
|---|---|
| `ksp/` | the PlatformIO project for the controller |
| `ksp/platformio.ini` | board, framework and library pins |
| `ksp/src/` | firmware sources (currently an empty stub) |
| `ksp/include/pins.h` | **generated**: one constant per Teensy pin. Do not edit |
| `ksp/lib/`, `ksp/test/` | project-local libraries and tests (empty) |

## Build

Install [PlatformIO](https://platformio.org/) (the CLI is enough), then from the repo root:

```
pio run -d firmware/ksp                 # compile
pio run -d firmware/ksp -t upload       # flash a connected Teensy
```

The Teensy loader may need a button press on the board to accept an upload. The toolchain has not been run in this repo yet.

## Pins

The pin assignment lives in one place, `hardware/electronics/pinmap.json`. After changing it, run `python3 tools/gen_wiring.py`:
it rewrites the wiring docs and `ksp/include/pins.h` together, so the firmware cannot drift from the wiring.
