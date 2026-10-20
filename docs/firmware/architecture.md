# Firmware architecture (outline)

A starting outline for the controller firmware, written before any code. Nothing here is implemented or tested. Control
behaviour is in [controls.md](../design/controls.md), pin assignments in
[pin-map.md](../../hardware/electronics/wiring/pin-map.md), and the project is set up in [firmware/README.md](../../firmware/README.md).
Message names below come from the design discussion: check them against the Simpit documentation before relying on them.

## Inputs and what they send

| Input | Source | Goes to |
|---|---|---|
| Two 3-axis sticks | analog pins (X, Y, twist) | rotation (right stick) and translation (left stick) messages, scaled while the left grip button is held |
| Throttle fader | wiper on an analog pin | throttle command, only when the fader is touched |
| 4 x 6 key matrix | row and column pins | SAS modes, SAS and RCS, GEAR, LIGHT, BRAKE, action groups |
| Switch panel (16 inputs) | MCP23017 on I2C, interrupt on a pin | ABORT, STAGE (gated by the key switch), FULL, CUT, ENGAGE / DISENGAGE, utility keys through the keyboard emulator |
| Three encoders | pins | time warp, camera, display page |
| Grip buttons | pins | SAS toggle (right), fine control (left) |

## Outputs

| Output | Driven by |
|---|---|
| 65 WS2812B pixels (24 key pixels, 32 fuel-bar pixels, 9 annunciator windows) | game state: SAS mode, resources, flight status |
| Fader motor | throttle value from the game, so the fader follows when untouched |
| Two 3.5" TFT displays (ILI9488, SPI) | telemetry pages, chosen with the display-page encoder |
| Buzzer | alert events (to be decided) |

## Simpit messages in play (to verify)

Action groups, SAS mode, throttle (both directions), keyboard emulator (Windows only), nav-ball mode, and the resource,
altitude, apsides, atmosphere and flight-status telemetry. The fuel bars need the Alternate Resource Panel mod. Simpit has no
G-force message, so the annunciator has no G window.

## Planned structure

| Module | Job |
|---|---|
| `main` | setup, the main loop, ties the modules together |
| `simpit` | the serial link, message handlers and senders |
| `inputs` | matrix scan, expander, analog reads, encoders, debouncing |
| `calibration` | stick centre and range (the pots are loose-tolerance parts) |
| `throttle` | fader follow-and-touch logic and the FULL / CUT buttons |
| `controls` | ENGAGE / DISENGAGE interlock, STAGE key interlock, fine control |
| `pixels` | the 65-pixel chain, serpentine mapping and a brightness cap |
| `annunciator` | threshold logic for the nine windows |
| `display` | the two TFT pages (needs an ILI9488 library that works on the Teensy 4.1) |

## Open points

- Library and mod versions: confirm KerbalSimpitRevamped (mod) and its Arduino library are compatible.
- Fader touch sensing: Teensy 4.1 has no `touchRead()`, so FastTouch or a different method is needed.
- Brightness cap: the pixel chain's worst case is more than the 4 A supply can give.
- Throttle: how authority is handed back when the device stops sending.
- Annunciator thresholds and colours, display page contents and the buzzer's event list are undecided.
