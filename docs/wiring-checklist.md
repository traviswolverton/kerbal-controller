# Wiring checklist

Companion to [pinout.html](pinout.html), the wiring diagrams. Pin numbers and signal names are in
[pin-map.md](pin-map.md). Nothing is built yet and none of this has been checked on real hardware: tick a box
only after you have checked it on the actual part.

Five pieces: two wings and three strip pieces. The **middle strip** holds the Teensy, the 5 V input and
everything that is not a switch. Each of the four outer pieces has one DB25 cable to it.

## Wire colours

Red is always 3V3, black is always GND, orange is always 5 V. The same signal is the same colour at both ends
of its wire. A colour can repeat when the wires never sit side by side; inside a piece the pin labels settle
which is which.

| Signal | Colour | Where |
|---|---|---|
| 3V3 | red | pots, buzzer module, OLEDs: from the Teensy |
| 5 V | orange | pixels, level shifter, fader driver |
| GND | black | everything |
| Stick X | purple | both sticks |
| Stick Y | grey | both sticks |
| Stick twist | brown | both sticks |
| Fader wiper | green | left wing |
| Fader touch, push switches, toggles | white | to ground |
| Encoder A | blue | all three encoders |
| Encoder B | yellow | all three encoders |
| Fader PWM A / B | pink / teal | left wing, to the driver |
| Matrix rows | green | strips |
| Matrix columns | blue | strips |
| Pixel data | pink | strips and middle |
| OLED SCK / SDA / DC / RES | yellow / blue / grey / teal | middle |
| OLED chip select 1 / 2 | green / purple | middle |
| Buzzer I/O | brown | middle |

Pink and teal are not in a basic Dupont set. Use striped wire or tape a coloured band on instead.

## Teensy pins

- [ ] **Check the physical pin order** against [PJRC's pinout card](https://www.pjrc.com/store/teensy41.html) before wiring. The order in `pinout.html` is from memory.
- [ ] All pins are 3.3 V only. Nothing at 5 V ever touches a Teensy pin.
- [ ] The Teensy is powered **only over USB**. Do not connect the 5 V rail to its VIN pin.
- [ ] Wire the Teensy side of each DB25 jack as in the pinout grid (pins 15 to 23 are the pins the Teensy drives).

## Middle strip

- [ ] 5 V adapter plugs into the panel jack. **Check the jack's polarity with a meter** (centre pin should be +) before wiring it: red and black leads do not prove which is which.
- [ ] Jack, then a fuse just above the capped load (about 3 to 4 A), then the 5 V rail with a 1000 µF capacitor across it.
- [ ] 74AHCT125: input from Teensy pin 1, its output enable pin tied to ground, VCC on 5 V, then 330 to 470 Ω to the left strip's data pin (LS 17). Tie the unused buffer inputs to ground.
- [ ] 32 fuel-bar pixels: data in from LS 18 (the return from the left strip), data out to RS 17. 5 V and GND straight from the rail with short wires.
- [ ] Both OLEDs on 3V3 until you have confirmed their SPI lines are safe at 5 V. Share SCK, MOSI, DC and RES; one chip select each (pins 10 and 24).
- [ ] Buzzer module on **3V3**, I/O to pin 25. At 5 V its transistor may not switch off.
- [ ] Four DB25 jacks, one per outer piece. All four are the same connector, so label them LW, RW, LS and RS.

## Wings

Left wing (DB25 LW, 19 conductors):

- [ ] Stick: three pot wipers (X, Y, twist) to pins 3, 4, 5, top button to pin 8, pot ends to 3V3 (pin 2) and GND. **Check the stick's pin order on the real unit.**
- [ ] Fader: wiper to pin 6, high end to 3V3, low end to GND, touch pad on the nubbin to pin 12.
- [ ] L9110H next to the motor: 5 V on pins 20 and 21 (two conductors in parallel), PWM A to pin 22, PWM B to pin 23, return on pins 24 and 25. A 47 µF capacitor across its supply. Outputs to the fader's two motor pins; swap them if it runs backwards.
- [ ] Time-warp encoder: A to pin 9, B to pin 10, push to pin 11, common to GND.

Right wing (DB25 RW, 14 conductors):

- [ ] Stick as above: X, Y, twist on pins 3, 4, 5, button on pin 8, pot ends on 3V3 and GND.
- [ ] Camera encoder: A pin 9, B pin 10, push pin 11. Page encoder: A pin 12, B pin 14, push pin 19. Commons to GND.
- [ ] Leave pins 20 to 25 open.

## Strips

Left strip (DB25 LS, 19 conductors) and right strip (DB25 RS, 18 conductors):

- [ ] Every key has a diode: **anode to its column, cathode to its row**. Left strip carries rows 0 and 1, right strip rows 2 and 3. Both carry all six columns, on pins 3, 4, 5, 6, 8, 9.
- [ ] Rows are on pins 15 and 16 of both strip jacks. They are rows 0 and 1 for the left strip and rows 2 and 3 for the right strip, which the Teensy side of each jack handles.
- [ ] Toggles: one pin to GND, the other to pins 10 and 11. The right strip's second spare toggle has a conductor but no Teensy pin.
- [ ] Pixels: data in on pin 17. The left strip's last pixel returns on pin 18 (the right strip has no return). 330 to 470 Ω in the data line at the first pixel on the left strip. 5 V on pins 20 and 21, GND on 24 and 25. Optional 100 µF across 5 V in each strip.

## Cables

- [ ] Four male-to-male straight-through shielded DB25 cables, **not null modem**. Short for the strips, longer for the wings, which pass through a strip shell.
- [ ] Ground each cable's shield at the **middle** end only.
- [ ] A cable in the wrong port does no damage by design (see the DB25 grid in `pinout.html`) but will not work, so plug each into its labelled port.

## Before first power-up

Multimeter in continuity mode, with nothing plugged into the devices and the 5 V adapter and USB both disconnected.

- [ ] No beep between the 5 V rail and GND, none between 3V3 and GND, and none between 5 V and 3V3. A beep means a short or a stray strand.
- [ ] On each DB25 jack, no beep between any two adjacent pins.
- [ ] Each Teensy-to-jack wire beeps end to end.
- [ ] Each key beeps between its row and column only while pressed, and the diode blocks the other way.
- [ ] Only then plug in the USB, then check 3V3 on the pots' supply pin.
- [ ] Then the 5 V adapter with the outer pieces unplugged: the rail should read 5 V, and the fuse should hold.
- [ ] Then plug in one outer piece at a time, and test it in firmware (stick axes move, encoders count, keys register) before the next.

If an axis jumps or a key sticks, the usual causes are a device with no ground, a pot on 5 V instead of 3V3, a swapped row and column, or a loose solder joint.
