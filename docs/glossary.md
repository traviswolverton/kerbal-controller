# Glossary

> **What this covers:** every term, acronym and part name used in the repo, in plain words, grouped by topic.  
> **Read it if:** a word in another doc stopped you. Use your browser's find (Ctrl+F).  
> **Status:** Reference. Where a spec is quoted it is a *Seller claim* until the part is measured (see [docs/README.md](README.md)).  
> **Next:** [How it works](how-it-works.md) if you have not read it, otherwise the [journey](journey.md).

## The game and the software

| Term | Plain meaning |
|---|---|
| **KSP / KSP1** | Kerbal Space Program, a game about building and flying rockets. KSP1 is the first game; this project does not support KSP2. |
| **Simpit / KerbalSimpitRevamped** | A mod (add-on) for KSP1 that lets a home-made controller talk to the game over a USB serial cable. It is the bridge between the console and the game. |
| **Simpit message** | One small packet of data sent either way across that cable: "throttle is 80%", "SAS mode is Prograde". |
| **Mod / CKAN** | A mod adds features to a game. CKAN is the tool KSP players use to install mods. |
| **Alternate Resource Panel** | A second KSP mod that makes fuel, electricity and similar levels available so the console's fuel bars can show them. |
| **SAS** | Stability Assist System: the game's autopilot that holds a direction. It has modes (hold, prograde, retrograde, and so on), one key per mode. |
| **RCS** | Reaction Control System: little thrusters for fine movement and docking. Switched on and off from the console. |
| **Stage / STAGE** | Rockets drop used-up sections in steps. "Staging" fires the next step: engines ignite, a booster separates. It is a big, irreversible action, so it is behind a key switch here. |
| **Action group** | A user-defined bundle of actions (for example "deploy solar panels") bound to a key. |
| **ABORT** | An emergency action group, usually to fire an escape system. It has a guarded toggle. |
| **Throttle** | How hard the engines push, 0 to 100%. A motorised slider here. |
| **Translation / rotation** | Rotation turns the craft (pitch, yaw, roll). Translation moves it sideways, up or down, forward or back, used mostly for docking. The right stick rotates and the left translates. |
| **Annunciator** | A panel of warning lights, each with a label (low fuel, low power, overheat, and so on). The word is from aircraft cockpits. |
| **Firmware** | The program that lives on the Teensy and runs the moment it is powered. |
| **PlatformIO** | The tool that compiles firmware and uploads it to the Teensy. |
| **Library** | Code someone else wrote that you reuse. |

## The brain and its connections

| Term | Plain meaning |
|---|---|
| **Teensy 4.1** | A small, fast microcontroller board (about the size of a stick of gum) with many pins to wire things to. The brain of the console. |
| **Microcontroller** | A tiny computer on one chip that runs one program and has pins to read switches and drive lights. |
| **Pin / GPIO** | A metal contact on the Teensy that the program can read (is the switch pressed?) or drive (turn this on). |
| **USB serial** | The way the Teensy and the PC exchange messages over an ordinary USB cable. |
| **3V3 / 5 V / GND** | The two voltages used and the zero-volt reference ("ground"). The Teensy's pins are **3.3 V only**: a 5 V signal into one can damage it. |
| **ADC / analog input** | A pin that measures a voltage (say 0 to 3.3 V) as a number. Used for sticks and the slider. |
| **Potentiometer (pot) / wiper** | A knob or slider that changes a resistance. Its middle contact, the *wiper*, outputs a voltage that depends on position. The sticks and slider are pots. |
| **Pull-up / `INPUT_PULLUP`** | A small current that holds an unused input at "high". A button that connects the pin to ground then pulls it "low" when pressed. It saves adding resistors. |
| **Debounce** | Ignoring the rapid on-off flicker a switch makes when pressed, so one press counts once. |
| **Interrupt** | A pin that taps the Teensy on the shoulder when something changes, so it need not keep checking. |
| **PWM** | Rapidly switching a pin on and off to control how much power something gets. It sets the speed of the throttle slider's motor. |
| **Rotary encoder / detent** | A knob that sends pulses as it turns, so the program counts steps. A *detent* is each click. |
| **I2C (SDA, SCL)** | A two-wire way for chips to talk. SDA is data, SCL is the clock. |
| **Expander / MCP23017** | A chip that adds 16 more input pins over I2C. The switch panel has 16 inputs and the Teensy has none to spare. |
| **Key matrix / diode matrix** | A way to read many keys with few pins. Keys sit at the crossings of rows and columns, and the program checks one row at a time. A *diode* at each key stops false readings when several keys are pressed. 24 keys need 10 pins this way, not 24. |
| **Pixel / WS2812B** | A tiny colour LED with its own chip, daisy-chained so one pin controls all 65. Also called NeoPixel. Each can show any colour. |
| **Level shifter / 74AHCT125** | A chip that converts the Teensy's 3.3 V signal up to the 5 V the pixels want. |
| **H-bridge / L9110H** | A chip that lets a small motor be driven in either direction from low-power signals. It moves the throttle slider. |
| **Capacitor (decoupling)** | A small component that smooths the power supply so sudden demand does not make it dip. |
| **Fuse** | A deliberately weak link that burns out before a wire does. |

## Wiring and soldering

| Term | Plain meaning |
|---|---|
| **Perfboard** | A board with a grid of holes for building circuits by hand. *Pad-per-hole* boards have one separate pad per hole, which is what you want. Boards with groups of five joined holes work like a breadboard and short out things placed across them (this was a mistake in the repo's history: see the [journey](journey.md)). |
| **Screw terminal** | A block where you clamp a wire with a screw. No soldering. Used for power and ground buses. |
| **DIP / socket** | DIP is the chip package with two rows of legs. A socket is a holder soldered to the board so the chip can be swapped. |
| **Header (male / female)** | Rows of pins (male) or sockets (female) used to plug boards together. The Teensy sits in female headers. |
| **DB25 / D-sub** | The 25-pin trapezoid connector from old computer printer and serial cables. Here it joins each outer piece to the middle strip. |
| **Solder cup** | The little cup at the back of each DB25 pin that a wire is soldered into. Cramped and fiddly, hence the practice jacks. |
| **Shield** | A foil or braid around a cable's wires that reduces interference. It is joined to ground at one end only. |
| **AWG** | Wire thickness. A bigger number is a thinner wire. 22 AWG is a common hookup wire. |
| **Hookup wire (stranded, solid)** | Stranded is flexible and good for moving parts. Solid is rigid and good for fixed runs. |
| **Heat shrink** | Tubing that shrinks over a joint when heated, to insulate it. |
| **Bus** | A shared wire or rail, for example every ground in a piece joined together. |
| **Multimeter / continuity test** | A meter. In continuity mode it beeps when two points are connected. It is how you find shorts before powering up. |
| **Short circuit** | An accidental direct connection between power and ground (or two signals). It can destroy parts, which is why [bring-up](../hardware/electronics/bring-up.md) is slow and careful. |
| **Polarity** | Which way round positive and negative go. Plugging power in backwards can destroy parts. |

## The shell and the printing

| Term | Plain meaning |
|---|---|
| **OpenSCAD** | Free software where you describe a 3D object in code, rather than drawing it. The console is defined in `hardware/cad/console.scad`. |
| **STL** | The file format a 3D printer's software reads. |
| **Slicer** | Software that turns an STL into layer-by-layer printer instructions. |
| **Print bed / build volume** | The area the printer can print on. Here 256 mm square, which is why the console is split into pieces. |
| **Brim / skirt** | A thin outline the slicer adds around a print. It takes up bed space. |
| **PLA / PETG** | Two common printing plastics. PLA is easier. PETG is tougher. |
| **Filament** | The plastic wire the printer melts. |
| **Shell / faceplate** | Each piece is a hollow box (the shell) with a removable lid (the faceplate) that holds the controls. |
| **Wing / strip** | The two low front pieces are wings. The three raised back pieces are strips. |
| **Tilt** | How steeply a panel leans toward you. Wings 12 degrees, strips 28 degrees. |
| **Ballast** | Weight inside the wings (steel plates) so the console does not slide when you push the throttle. |
| **Heat-set insert** | A brass nut pressed into plastic with a hot iron, giving a strong screw thread. |
| **Diffuser** | A thin white layer that spreads an LED's light so you see a soft glow, not a bright dot. |
| **Test plate** | A small print of 4 keys and pixels used to check the fit before printing the real pieces. |
| **Cutout** | The hole in a panel for a part. Its size comes from a datasheet or from measuring the real part. |
| **Mockup** | The 3D render of the finished design, used to check layout. |

## Controls and parts

| Term | Plain meaning |
|---|---|
| **MX switch** | The standard keyboard key switch. This project uses blue (clicky, loud) ones. |
| **Keycap / DSA** | The plastic cap on a key. DSA is a low, flat-topped style. |
| **Guarded toggle** | A switch under a flip-up cover so a bump cannot trigger it. Used for ABORT, ENGAGE / DISENGAGE and master power. |
| **Key switch** | A switch turned with a real key. It arms STAGE here. |
| **Joystick (JH-D400X-R4)** | An industrial 4-axis stick: tilt X, tilt Y, twist, plus a thumb button. |
| **Motorised fader** | A slider with a motor, so it can move itself to match the game's throttle, and move under your hand when you take over. |
| **Nubbin** | The small conductive knob on the slider. It is conductive so the Teensy can feel your finger. |
| **Touch sensing** | Detecting a finger by its electrical effect. The Teensy 4.1 has no ready-made function for it, so it is an open item in the [to-do](design/todo.md). |
| **TFT / IPS** | The small colour screens. IPS is a screen type that looks good from an angle. |
| **ENGAGE / DISENGAGE** | A switch that makes the sticks and throttle live or ignored, so a bump or a leaning arm does nothing. |

## Project terms

| Term | Plain meaning |
|---|---|
| **Piece** | One of the five printed units that make up the console. |
| **Pin map** | The table saying which Teensy pin goes where. Lives in `pinmap.json`. |
| **Generated file** | A file made by a script from data. It says "generated" at the top and must not be edited by hand. |
| **Seller claim** | A spec read off a listing or datasheet, not yet checked on the real part. |
| **Measured / Tested** | A spec checked with calipers or a meter / something that worked on the bench or in the game. |
| **Layout B** | The chosen key spacing: a 19.05 mm column pitch and a 36 mm row pitch, with a pixel in clear space above each key. |
| **Shortlist** | The saved list of parts picked from Digi-Key or Mouser, in `parts-shortlist.json`. |
| **ASIN** | Amazon's product code, used in `amazon-items.json`. |
| **Reel trap** | Small parts often come only in reels of thousands. The sourcing tool prefers cut tape or bulk. |
| **Digi-Key / Mouser** | US electronics distributors with web APIs the repo uses to get live price and stock. |
| **Bring-up** | The careful first switching-on of a new circuit. |
