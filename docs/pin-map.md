# Pin map and cabling (draft, five-piece layout)

Teensy 4.1 pin assignment, the cabling between the five pieces, and the four DB25 pinouts. Matches
`cad/console_mockup_v1.scad`. Draft: nothing is built yet. Context is in `decisions.md` and `parts-list.md`.

## Topology

```
                         LEFT WING                          RIGHT WING
                         stick, fader, enc                  stick, 2 enc
                              |  DB25 (19)                       |  DB25 (13)
                              |                                  |
   STRIP LEFT  --DB25 (19)--  STRIP MIDDLE  --DB25 (18)--  STRIP RIGHT
   12 keys, 2 toggles         Teensy, 2 OLEDs, 32 fuel         12 keys, 2 spare toggles
   12 pixels                  pixels, buzzer, power jack       12 pixels
                              (5 V in, fuse, 1000 uF)
```

- The **middle strip** holds the Teensy, the 5 V input, the 74AHCT125 and everything that is not a switch.
  It has four DB25 jacks, one per outer piece.
- The two **wings** sit in front of the outer strip pieces. Their cables to the middle piece have to pass
  through the strip shell (a hole in the strip's front wall and one in its side wall). That routing is
  still to be designed in CAD.
- **Pixels are one chain of 56** on a single data pin: left strip (12), then the fuel bars in the middle
  (32), then the right strip (12). The data goes out to the left strip on pin 17, comes back on pin 18,
  runs through the fuel bars, and leaves for the right strip on pin 17 of that port. Put the 330-470 ohm
  series resistor at the first pixel (in the left strip). If a strip cable is unplugged, every pixel after
  it goes dark.
- **Keys are one 4 x 6 matrix** split across the strips: the left strip carries rows 0-1 and the right
  strip rows 2-3. Both carry all six column lines, which are paralleled in the middle piece.

## Constraints that shaped it

- All 3.3 V, none of the pins are 5 V tolerant. Analog inputs must stay at or below 3.3 V.
- Only header pins 0-41 are used. Pins 42 and up are bottom pads.
- **Pin 1** is the pixel data output: Serial1 TX, supported by the WS2812Serial library (non-blocking, DMA).
  It goes to the 74AHCT125 level shifter.
- **Pins 2 and 3** are the fader PWM pair: both are on timer FlexPWM4.2, so they share one frequency
  (default 4.482 kHz, changeable with `analogWriteFrequency`).
- **Pin 13** has the on-board LED and is the SPI clock for the OLEDs. **Pin 12** is MISO on SPI0 but is a
  plain GPIO here (OLED DC), because the OLEDs are write-only. **Pins 18 and 19** are the I2C pins but are
  used as GPIO, so there is no I2C on this map.
- Analog inputs are pins 14-27 and 38-41; the seven used are 14-17 and 20-22.
- The 3.3 V regulator is good for about 250 mA external. The pots draw almost nothing.
- The matrix is read by driving a row low and reading the columns with pull-ups. **Leave the other rows
  as inputs (high impedance), never driven high**, so a stray short cannot fight a driven pin.

## Teensy 4.1 assignment

| Pin | Signal | Direction | Piece |
|---|---|---|---|
| 0 | OLED_RES | out | middle (both OLEDs share reset and DC) |
| 1 | PIXEL_DATA | out | middle, via 74AHCT125 to left-strip port pin 17 |
| 2 | FADER_PWM_A | out | left wing |
| 3 | FADER_PWM_B | out | left wing |
| 4 | FADER_TOUCH | in | left wing (FastTouch pad on the nubbin) |
| 5 | L_STICK_BTN | in, pull-up | left wing |
| 6 | L_ENC_A | in, pull-up | left wing (time warp) |
| 7 | L_ENC_B | in, pull-up | left wing |
| 8 | L_ENC_SW | in, pull-up | left wing |
| 9 | R_STICK_BTN | in, pull-up | right wing |
| 10 | OLED_CS1 | out | middle |
| 11 | OLED_MOSI | out | middle |
| 12 | OLED_DC | out | middle |
| 13 | OLED_SCK | out | middle |
| 14 (A0) | L_STICK_X | analog | left wing |
| 15 (A1) | L_STICK_Y | analog | left wing |
| 16 (A2) | L_STICK_Z (twist) | analog | left wing |
| 17 (A3) | FADER_WIPER | analog | left wing |
| 18 | R_CAM_A | in, pull-up | right wing (camera) |
| 19 | R_CAM_B | in, pull-up | right wing |
| 20 (A6) | R_STICK_X | analog | right wing |
| 21 (A7) | R_STICK_Y | analog | right wing |
| 22 (A8) | R_STICK_Z (twist) | analog | right wing |
| 23 | R_CAM_SW | in, pull-up | right wing |
| 24 | OLED_CS2 | out | middle |
| 25 | BUZZER | out | middle (low = on, idle high) |
| 26 | TOG_ABORT | in, pull-up | left strip |
| 27 | TOG_ARM | in, pull-up | left strip |
| 28-29 | MATRIX_ROW0-1 | out | left strip (row 0 = back row) |
| 30-31 | MATRIX_ROW2-3 | out | right strip |
| 32-37 | MATRIX_COL0-5 | in, pull-up | both strips |
| 38 | R_PAGE_A | in, pull-up | right wing (display page) |
| 39 | R_PAGE_B | in, pull-up | right wing |
| 40 | R_PAGE_SW | in, pull-up | right wing |
| 41 | TOG_SPARE1 | in, pull-up | right strip |

All 42 header pins are used. The second spare toggle (TOG_SPARE2) has a conductor in the right-strip cable
but **no Teensy pin**: use a bottom pad or a small I2C expander if you ever need it.

## DB25 pinouts

Standard DB25 numbering, pins 1-13 on the wide row and 14-25 on the other. All four ports use the same
connector, so a cable can be plugged into the wrong port. The pins are laid out so that is **harmless**:

- Ground is on pins 1, 7, 13, 24, 25 on every port.
- 3.3 V (pin 2) is provided on the two wing ports only. 5 V (pins 20, 21) is provided on the left-wing and
  both strip ports.
- Everything the Teensy **drives** sits on pins 15-23 only: matrix rows and pixel data on pins 15-17 of the
  strip ports, fader PWM on pins 22 and 23 of the left-wing port. Pins that are not used by a module are left
  open, never wired to something else. So a module never connects a switch, a wiper or a ground to a pin the
  Teensy drives.
- A script check (all 16 combinations of module and port) found no conflict, only wrong behaviour.

| Pin | Left wing | Right wing | Left strip | Right strip |
|---|---|---|---|---|
| 1 | GND | GND | GND | GND |
| 2 | 3V3 | 3V3 | open | open |
| 3 | L_STICK_X | R_STICK_X | COL0 | COL0 |
| 4 | L_STICK_Y | R_STICK_Y | COL1 | COL1 |
| 5 | L_STICK_Z | R_STICK_Z | COL2 | COL2 |
| 6 | FADER_WIPER | open | COL3 | COL3 |
| 7 | GND | GND | GND | GND |
| 8 | L_STICK_BTN | R_STICK_BTN | COL4 | COL4 |
| 9 | L_ENC_A | R_CAM_A | COL5 | COL5 |
| 10 | L_ENC_B | R_CAM_B | TOG_ABORT | TOG_SPARE1 |
| 11 | L_ENC_SW | R_CAM_SW | TOG_ARM | TOG_SPARE2 |
| 12 | FADER_TOUCH | R_PAGE_A | open | open |
| 13 | GND | GND | GND | GND |
| 14 | open | R_PAGE_B | open | open |
| 15 | open | open | ROW0 | ROW2 |
| 16 | open | open | ROW1 | ROW3 |
| 17 | open | open | PIXEL_IN | PIXEL_IN |
| 18 | open | open | PIXEL_OUT | open |
| 19 | open | open | open | open |
| 20, 21 | 5V (in parallel) | open | 5V (in parallel) | 5V (in parallel) |
| 22 | FADER_PWM_A | open | open | open |
| 23 | FADER_PWM_B | open | open | open |
| 24, 25 | GND (in parallel) | open | GND (in parallel) | GND (in parallel) |
| **Conductors** | 19 | 13 | 19 | 18 |

Notes:
- Analog lines (stick X, Y, twist and the fader wiper) sit between ground pins so they are not neighbours of
  digital lines. Put a 0.1 uF capacitor from each wiper to ground at the Teensy end.
- **Cable shield:** ground it to the connector shell at the middle end only, to avoid a ground loop.
- **Pixel power:** each strip piece takes 5 V on pins 20 and 21 (two conductors, about 0.7 A worst case for
  12 pixels). The 32 fuel-bar pixels are in the middle piece and are fed straight from the 5 V rail. A
  100 uF capacitor across 5 V in each strip piece is optional.
- **Left wing:** the L9110H fader driver is in the wing next to the motor, so only the two PWM lines and 5 V
  cross the cable. Pots take 3V3 on pin 2, never 5 V.
- **Cables:** the wing cables go through a strip piece, so they are longer (about 0.5 m). The strip-to-middle
  cables can be about 0.3 m. Keep analog runs short.

## Open

- **Wing cable routing** through the strip shells (holes, strain relief): to be drawn in CAD.
- **Spare toggle 2:** no pin, see above.
- **OLED modules:** confirm their logic level and supply. They accept 3.3-5 V, so power them from 5 V, but
  check the SPI lines are 3.3 V safe in that case. Not verified.
- **Pixel chain through cables:** a break in the chain (an unplugged strip cable) kills the pixels after it.
  Fine for a build, worth knowing when debugging.
- **Confirm the physical Teensy pin positions** before wiring: this map uses pin numbers only.
- **DB25 jack cutouts** are not in the mockup yet.
