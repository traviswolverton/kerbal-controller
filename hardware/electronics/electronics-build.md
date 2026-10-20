# Electronics build notes (rough recommendation)

How I'd build the electronics: hand-wired on perfboard, no custom PCB. Digi-Key part numbers and prices are from
the API on 2026-10-19 and are in the shortlist and the budget. Nothing here is built or tested.

## Approach

- Plated-through perfboard (2.54 mm grid), a screw-terminal bus for GND, 3V3 and 5 V in each piece, and stranded wire in the
  colours from [wiring-checklist.md](wiring/wiring-checklist.md). The goodnight-device "bus board" worked the same way.
- Sockets for every chip (Teensy, 74AHCT125, MCP23017) so a bad part is a swap, not a desolder.
- Solder each DB25 jack's cups straight to its board or devices. No breakout boards: they would not fit a panel jack.
- The matrix and the pixel chain are point-to-point on the back of each strip's faceplate: diodes in line with the key wires,
  pixel boards daisy-chained with short wires. No board needed.

## Per piece

| Piece | Board | What goes on it |
|---|---|---|
| Middle strip | one large board, plus a small bus board | Teensy on two 24-pin female headers, 74AHCT125 in a socket with its 330 ohm resistor, SDA/SCL pull-ups, decoupling, the 1000 uF at the 5 V entry, terminal blocks for 5 V in and the GND and 3V3 buses. Wires out to the four female DB25 jacks, two TFT headers (8 of the 13 pins each), the buzzer. This is the busiest piece: about 45 signal wires, so it is where a custom PCB would later pay off. |
| Left strip | one small board | MCP23017 in a DIP-28 socket, 10 k reset pull-up, 0.1 uF decoupling, terminal blocks for the 16 switch inputs and the GND bus, SDA/SCL/INT/3V3 to the DB25 jack. |
| Right strip | none or a tiny bus board | Matrix wiring and pixel chain only. |
| Left wing | one small board | L9110H in a socket, the 47 uF capacitor, three 0.1 uF wiper capacitors, terminal blocks for 3V3, 5 V and GND, wires to the stick, fader, encoder and the DB25 jack. |
| Right wing | one small board | Wiper capacitors, a 3V3 and GND bus, wires to the stick, two encoders and the DB25 jack. |

## Candidate parts (Digi-Key)

| Part | Qty | Digi-Key PN | Unit | Notes |
|---|---|---|---|---|
| Perfboard 78 x 58 mm, PTH, pad per hole, DFRobot FIT0203 | 4 | 1738-1001-ND | $2.90 | Expander, wing and bus boards. Replaces the DigiKey SOLDERBREAD-02, which is breadboard-style 5-hole pads and would short anything placed in a pad. |
| Perfboard 94 x 63 mm, PTH, SparkFun 12070 | 1 | 1568-12070-ND | $8.65 | Middle strip main board. **Open:** this is also 5-hole-pad (breadboard-style), which suits the busiest board badly. The pad-per-hole Chip Quik SBBTH3040-1 (SBBTH3040-1-ND, 104 x 81 mm, $12.59) is the likely swap and fits the strip in plan view; height clearance under the sloped face is not checked. |
| Screw terminal, 5.08 mm, 2 position | 6 | ED2609-ND | $0.58 | 5 V in, bus joins. |
| Screw terminal, 5.08 mm, 4 position | 8 | ED2611-ND | $1.08 | GND, 3V3 and switch inputs. Chain several for the 16 inputs. |
| Female header, 24 position, 2.54 mm (Sullins) | 3 | S7022-ND | $1.34 | Two for the Teensy, one spare for the TFT headers and cuts. |
| Hookup wire 22 AWG stranded, 10 colours x 25 ft (Adafruit 3175) | 1 | 1528-3175-ND | $32.29 | Wire colours follow the checklist. Pink and teal are not in it: use tape or striped wire. |
| Hookup wire 22 AWG solid, 6 colours x 25 ft (Adafruit 1311) | 1 | 1528-1743-ND | $15.95 | Matrix rows and columns on the strips. |
| Heat shrink assortment (Adafruit 4559) | 1 | 1528-4559-ND | $9.95 | |

Rough total about $95. Not in the list yet: solder and flux, zip ties and cable clips for the cables behind the console, a
pin-header strip, M3 screws and standoffs for mounting the boards, and the connector for each stick and encoder (check
what the sticks arrive with).

## Open

- A decision on whether to design a PCB for the middle strip once the wiring is proven.
- Mounting the boards: printed standoffs on the shell floor are the obvious route, not yet modelled.
