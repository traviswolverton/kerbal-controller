# Pin map (draft)

Teensy 4.1 pin assignment and the two DB25 inter-module pinouts. Draft: nothing is built yet.
Context is in `decisions.md` (architecture, inter-module links) and `parts-list.md`.

## Constraints that shaped it

- All 3.3 V, none of the pins are 5 V tolerant. Analog inputs must stay at or below 3.3 V.
- Only header pins 0-41 are used. Pins 42 and up are bottom pads.
- **Pin 1** is the pixel data output: Serial1 TX, supported by the WS2812Serial library (non-blocking, DMA).
  It goes to the 74AHCT125 level shifter.
- **Pins 2 and 3** are the fader PWM pair: both are on timer FlexPWM4.2, so they share one frequency
  (default 4.482 kHz, changeable with `analogWriteFrequency`).
- **Pin 13** has the on-board LED and is the SPI clock for the OLEDs. Harmless for an output.
- **Pin 12** is MISO on SPI0 but is used as a plain GPIO for OLED DC, because the OLEDs are write-only.
- **Pins 18 and 19** are the I2C pins but are used as GPIO here, so there is no I2C on this map.
- Analog inputs are pins 14-27 and 38-41; the seven used are 14-17 and 20-22.
- The 3.3 V regulator is good for about 250 mA external. The joystick and fader pots draw almost nothing.

## Teensy 4.1 assignment

| Pin | Signal | Direction | Where |
|---|---|---|---|
| 0 | OLED_RES | out | centre (both OLEDs share reset and DC) |
| 1 | PIXEL_DATA | out | centre, to 74AHCT125 |
| 2 | FADER_PWM_A | out | left, to L9110H |
| 3 | FADER_PWM_B | out | left, to L9110H |
| 4 | FADER_TOUCH | in | left, FastTouch pad on the nubbin |
| 5 | L_STICK_BTN | in, pull-up | left |
| 6 | L_ENC_A | in, pull-up | left (time warp) |
| 7 | L_ENC_B | in, pull-up | left |
| 8 | L_ENC_SW | in, pull-up | left |
| 9 | R_STICK_BTN | in, pull-up | right |
| 10 | OLED_CS1 | out | centre |
| 11 | OLED_MOSI | out | centre |
| 12 | OLED_DC | out | centre |
| 13 | OLED_SCK | out | centre |
| 14 (A0) | L_STICK_X | analog | left |
| 15 (A1) | L_STICK_Y | analog | left |
| 16 (A2) | L_STICK_Z (twist) | analog | left |
| 17 (A3) | FADER_WIPER | analog | left |
| 18 | R_CAM_A | in, pull-up | right (camera) |
| 19 | R_CAM_B | in, pull-up | right |
| 20 (A6) | R_STICK_X | analog | right |
| 21 (A7) | R_STICK_Y | analog | right |
| 22 (A8) | R_STICK_Z (twist) | analog | right |
| 23 | R_CAM_SW | in, pull-up | right |
| 24 | OLED_CS2 | out | centre |
| 25 | BUZZER | out | centre (low = on, idle high) |
| 26 | TOG_ABORT | in, pull-up | centre |
| 27 | TOG_ARM | in, pull-up | centre |
| 28-31 | MATRIX_ROW0-3 | out | centre (row 0 = back row) |
| 32-37 | MATRIX_COL0-5 | in, pull-up | centre |
| 38 | R_PAGE_A | in, pull-up | right (display page) |
| 39 | R_PAGE_B | in, pull-up | right |
| 40 | R_PAGE_SW | in, pull-up | right |
| **41** | **free** | | one spare pin |

41 of the 42 header pins are used. The two SPARE toggles have **no pin yet**: they need pin 41 plus one more
(a bottom pad, or a small I2C expander if you give up the 18/19 GPIO use).

Matrix: diode per key, rows driven low one at a time, columns read with pull-ups. Diode cathode toward the
row line, as usual for column-to-row scanning; check against the firmware you write.

## DB25 pinouts

Standard DB25 numbering, pins 1-13 on the wide row and 14-25 on the other. Both side ports use the same
connector, so the rule is: **power pins sit on the same pins at both ports, and every pin the Teensy drives
(fader PWM and 5 V) is a pin the right module leaves open.** A left cable in the right port or the reverse
then cannot damage anything. Pins are as seen on the **centre** jacks.

| Pin | Left module | Right module |
|---|---|---|
| 1 | GND | GND |
| 2 | 3V3 | 3V3 |
| 3 | L_STICK_X | R_STICK_X |
| 4 | L_STICK_Y | R_STICK_Y |
| 5 | L_STICK_Z | R_STICK_Z |
| 6 | FADER_WIPER | open |
| 7 | GND | GND |
| 8 | L_STICK_BTN | R_STICK_BTN |
| 9 | L_ENC_A | R_CAM_A |
| 10 | L_ENC_B | R_CAM_B |
| 11 | L_ENC_SW | R_CAM_SW |
| 12 | FADER_TOUCH | R_PAGE_A |
| 13 | GND | GND |
| 14 | open | R_PAGE_B |
| 15-19 | open | open |
| 20, 21 | 5V (two conductors in parallel) | **open** |
| 22 | FADER_PWM_A | **open** |
| 23 | FADER_PWM_B | **open** |
| 24, 25 | GND (5 V and motor return, in parallel) | open |

Left uses 19 conductors, right 13, of 25. Pins 15-19 are spare on both.

Notes:
- Analog signals (3 to 6) sit between ground pins 1/7 so they are not neighbours of the digital lines. Put a
  0.1 uF capacitor from each wiper to ground at the Teensy end.
- Ground the cable shield to the connector shell at the **centre** end only, to avoid a ground loop through
  the side modules.
- The fader driver (L9110H) is in the left module and takes 5 V on pins 20 and 21, return on 24 and 25. The
  motor current stays local to the driver; only the two PWM lines cross the cable as signals.
- Joystick and fader pots take 3V3 (pin 2), not 5 V.

## Open

- Spare toggles: no pins, see above.
- OLED modules: confirm their logic level and supply. They accept 3.3-5 V, so power them from the 5 V rail,
  but check that the SPI lines are 3.3 V safe in that case. Not verified.
- Matrix diode direction and the row/column scan order are decided in firmware.
- Confirm the physical Teensy pin positions before wiring: this map uses pin numbers only.
- DB25 jack cutout dimensions are not in the mockup yet.
