# Why not X?

> **What this covers:** the alternatives that were considered and rejected, and why. Each answer is a short version of an entry in [decisions.md](decisions.md).  
> **Read it if:** you are wondering "why didn't you just use...?"  
> **Status:** Planned. These are design reasons, mostly not yet proved on hardware.  
> **Next:** [controls](controls.md), the map of what every control does.

## Electronics

**Why not a custom circuit board (PCB)?** Hand-wiring on perfboard costs nothing to change. A PCB makes sense *after* the wiring is
proven, and the middle strip (about 45 signal wires) is where it would pay off first. That is listed as a later decision.

**Why not one wire per key, straight to the Teensy?** The Teensy's header pins (0 to 41) are all spoken for in the pin map. A **4 x 6 key
matrix** reads 24 keys with 10 pins. The 16 switches on the switch panel go through a chip (an I2C expander) and use only 3 pins
and the power wires.

**Why not buy ready-made key boards with lights (NeoKey)?** They were hard to find. Hand-wiring one diode per switch costs a few cents each.

**Why not a small computer in every piece?** One brain means one program and one USB link to debug. It does mean a lot of wires,
so each outer piece has one DB25 cable. It is revisited only if the cable count becomes a problem.

**Why a Teensy 4.1 and not an Arduino?** *To write up:* the repo does not yet record a comparison. What it does record: the console
needs a lot of pins and runs fast enough, and everything on it is wired for 3.3 V.

**Why not power the pots from 5 V?** The Teensy's analog pins only read up to 3.3 V, so the sticks and slider are powered from 3.3 V to keep their readings in range.

**Why not power the Teensy from the 5 V supply?** The Teensy gets its power only from USB. The supply feeds only the lights, the level shifter and the
slider motor, with the grounds joined. That way the two sources cannot fight each other.

**Why a level shifter on the pixel data line?** The lights run from 5 V and expect a 5 V signal. The Teensy's signal is 3.3 V. A small
chip (74AHCT125) lifts it.

**Why not 12 V for the throttle motor?** The slider's motor is specified for 6 to 10 V, and its maker runs it from 5 V. If it turns out too weak
on the bench, the fallback is a 12 V input and two step-down converters.

## Controls

**Why not a separate "roll" control?** The stick's twist handles roll, so no extra rockers are needed.

**Why a key switch and a big STAGE button, not a guarded toggle?** STAGE is irreversible in game. The key switch has to be on
before the button does anything. It replaced a second guarded toggle.

**Why no RESET button?** Recovering from a hang is unplugging and replugging the USB cable.

**Why no "high G" warning?** Simpit has no G-force message, so there is nothing to display.

**Why not rely on the game's own precision mode for fine control?** It stays on the PRECISION button of the switch panel. The left stick's thumb button
also scales that stick down to about 25% in firmware while held, which does not depend on the game and is useful for docking.

**Why ENGAGE / DISENGAGE?** A bump or a leaning arm should not steer the rocket. Disengaged, the sticks and throttle send nothing.

## The shell

**Why five pieces?** The print bed is 256 mm, so no piece is wider than about 245 mm. Five pieces also make a reprint cheap, since a failed print loses one.

**Why a 12.2 inch 60% keyboard?** The controller covers nearly all flight controls. The keyboard is for typing names and saves, the
building screens and the odd hotkey. A full-size keyboard would have forced six pieces and about 940 mm.

**Why a steeper middle (28 degrees)?** At 12 degrees, the light above each key is hidden behind the cap in front of it.

**Why plain DSA keycaps?** Low and flat, so lights above are visible. Labels go on the panel, not on the caps.

**Why steel plates inside the wings?** Printed pieces plus parts are only about 3 kg, which a hand on the throttle or a tug on a cable can move.
Weight-vest plates in the wings add about 3.2 kg.

**Why solder-cup DB25 connectors?** The chosen jacks have solder cups, so every joint (about 140) is hand-soldered. The alternative is a crimp D-sub with a crimp tool, held in reserve
if the soldering is too painful.

## Sourcing

**Why Digi-Key first and Amazon second?** Digi-Key gives live price, stock, lifecycle status and datasheets through an API,
which is more reliable than a retail page, and one order is simpler. Amazon is for what Digi-Key does not stock.

**Why US retailers only?** It is the owner's rule: US listings that ship within the United States. It is written in `CLAUDE.md`.

**Why not mix a Digi-Key guard with a Digi-Key toggle?** The guard is made for that maker's own toggles, so mixing is a fit risk. The matched Amazon pack stays.
