# Control map

What every control does, panel by panel, so you can read it instead of asking. Labels match `cad/console_mockup_v1.scad`;
pins and conductors are in [pin-map.md](pin-map.md). **Status:** *decided* is in `decisions.md`; *proposed* is my reading of
the label and not yet settled; *open* means no function chosen. KSP actions go through
[KerbalSimpitRevamped](https://github.com/Simpit-team/KerbalSimpitRevamped). Nothing here is built or tested.

Rows below are listed **back row first**, the order you see them from the seat.

## Left strip: navigation keys

Twelve keys with a pixel above each that shows the real state (Simpit reports it). One key per SAS mode, plus the SAS and RCS switches.

| | | | | | |
|---|---|---|---|---|---|
| STAB | PRO | RETRO | NORM | A-NRM | MNVR |
| RAD-IN | RAD-OUT | TGT | A-TGT | SAS | RCS |

- STAB, PRO, RETRO, NORM, A-NRM, RAD-IN, RAD-OUT, TGT, A-TGT, MNVR: set the SAS mode (stability, prograde, retrograde,
  normal, anti-normal, radial in, radial out, target, anti-target, manoeuvre). *Proposed.*
- SAS: turn SAS on or off. RCS: turn RCS on or off. *Proposed.*

## Left strip: switch panel

Sixteen inputs on one MCP23017 expander (PA0 to PB7). All *decided* unless marked.

| Control | What it does | Expander pin |
|---|---|---|
| **ABORT** (guarded toggle, upper) | Fires the abort action group | PA0 |
| **ENGAGE / DISENGAGE** (guarded toggle, lower) | Controls-live interlock. Disengaged, the sticks and throttle send nothing (zero rotation and translation, no throttle), so SAS and the game stay in control. The annunciator's CONTROLS window lights while engaged | PB5 |
| **STAGE key switch** | Arms STAGE: the big button only fires while the key is on | PA1 |
| **STAGE** (big red button) | Next stage, only when the key is on | PA2 |
| FULL | Throttle to 100%; the fader follows | PA3 |
| CUT | Throttle to 0%; the fader follows | PA4 |
| PRECISION | Toggles precision control (the Caps Lock key) | PB2 |
| PAUSE | Pause menu (Esc) | PB3 |
| MAP | Map view (M) | PA5 |
| FOCUS- / FOCUS+ | Previous and next vessel | PA6, PA7 |
| UI HIDE | Hide the interface (F2) | PB4 |
| QSAVE / QLOAD | Quicksave and quickload (F5, F9) | PB0, PB1 |
| spare, spare | *Open.* Camera mode (V) and action group 10 are the suggestions | PB6, PB7 |

The 12 small buttons are a 3 x 4 grid, back row first: FULL CUT PRECISION PAUSE / MAP FOCUS- FOCUS+ UI HIDE / QSAVE QLOAD spare spare.
They have no pixels because KSP reports no state for them. Key presses (MAP, QSAVE and so on) use Simpit's keyboard emulator, which
works on Windows only.

## Middle strip

| Control | What it does |
|---|---|
| Two OLEDs | Telemetry pages, chosen with the display-page encoder. *Open:* the page contents are not decided (the reference build showed Surface, Orbital, Vessel and Mission) |
| Four fuel bars of 8 pixels | LF, OX, MONO and EC levels, from the resource messages (need the Alternate Resource Panel mod) |
| Buzzer | Audible alerts. *Open:* which events sound it |
| Master power switch | Cuts the 5 V rail (pixels, level shifter, fader driver). The Teensy stays on USB |

## Right strip: action-group keys

Twelve keys, each with a state pixel.

| | | | | | |
|---|---|---|---|---|---|
| GEAR | LIGHT | BRAKE | AG1 | AG2 | AG3 |
| AG4 | AG5 | AG6 | AG7 | AG8 | AG9 |

- GEAR, LIGHT, BRAKE: toggle landing gear, lights and brakes. AG1 to AG9: custom action groups. *Proposed.* AG10 has no key.

## Right strip: annunciator

Nine windows, one pixel each. *Decided as a concept; the thresholds are proposals.* Green, yellow or red per window.

| | | |
|---|---|---|
| LOW FUEL | LOW POWER | OVERHEAT |
| LOW ALT | STABLE ORBIT | ATMOSPHERE |
| CHUTE SAFE | LINK | CONTROLS |

CONTROLS lights while ENGAGE is on. There is no HIGH G window: Simpit has no G-force message.

## Left wing

| Control | What it does |
|---|---|
| Stick | Translation: X and Y with the stick, Z with the twist |
| Stick grip button | **Hold for fine control**: while held, this stick's X, Y and twist are scaled to about 25% in firmware. *Decided.* Teensy pin 5 |
| Motorised fader | Throttle. It follows the game's throttle when you are not touching it; touch it and you drive the throttle |
| Time-warp encoder | Time warp rate (turn). *Open:* the push function (suggest normal speed) |

## Right wing

| Control | What it does |
|---|---|
| Stick | Rotation: pitch and yaw with the stick, roll with the twist |
| Stick grip button | **SAS toggle.** *Decided.* Teensy pin 9 |
| Camera encoder | Camera rotation (turn). *Open:* the push function (suggest camera mode) |
| Display-page encoder | Chooses the OLED page (turn). *Open:* the push function |

## What is not on the console

The keyboard and mouse still handle typing, the VAB and SPH, EVA walking, and map-view clicks. The console is designed
around a 12.2 in 60% keyboard in the open middle (see `decisions.md`).
