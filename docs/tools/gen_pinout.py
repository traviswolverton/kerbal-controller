#!/usr/bin/env python3
"""Generate docs/pinout.html, the wiring diagrams, in the same style as the goodnight-device pinout page.

Run from the repo root:  python3 docs/tools/gen_pinout.py
The pin data below is the single source for every diagram on the page. It must match docs/pin-map.md.
"""
import html
import sys
import xml.dom.minidom

OUT = sys.argv[1] if len(sys.argv) > 1 else "docs/pinout.html"

# ---- wire colours: one colour per signal class, same at both ends of a wire --------------------
COL = {n: f"var(--c-{n})" for n in
       ["red", "black", "white", "blue", "yellow", "green", "orange", "brown", "purple", "grey", "pink", "teal"]}
SIGCOL = {"3V3": "red", "5V": "orange", "GND": "black"}
for side in "LR":
    SIGCOL.update({f"{side}_STICK_X": "purple", f"{side}_STICK_Y": "grey", f"{side}_STICK_Z": "brown",
                   f"{side}_STICK_BTN": "white"})
SIGCOL.update({"FADER_WIPER": "green", "FADER_TOUCH": "white", "FADER_PWM_A": "pink", "FADER_PWM_B": "teal",
               "L_ENC_A": "blue", "L_ENC_B": "yellow", "L_ENC_SW": "white",
               "R_CAM_A": "blue", "R_CAM_B": "yellow", "R_CAM_SW": "white",
               "R_PAGE_A": "blue", "R_PAGE_B": "yellow", "R_PAGE_SW": "white",
               "TOG_ABORT": "white", "TOG_ARM": "white", "TOG_SPARE1": "white", "TOG_SPARE2": "white",
               "PIXEL_DATA": "pink", "PIXEL_IN": "pink", "PIXEL_OUT": "pink",
               "OLED_MOSI": "blue", "OLED_SCK": "yellow", "OLED_DC": "grey", "OLED_RES": "teal",
               "OLED_CS1": "green", "OLED_CS2": "purple", "BUZZER": "brown"})
for i in range(4):
    SIGCOL[f"ROW{i}"] = "green"
for i in range(6):
    SIGCOL[f"COL{i}"] = "blue"

# ---- Teensy 4.1 assignment (docs/pin-map.md) ---------------------------------------------------
TEENSY = {
    0: "OLED_RES", 1: "PIXEL_DATA", 2: "FADER_PWM_A", 3: "FADER_PWM_B", 4: "FADER_TOUCH", 5: "L_STICK_BTN",
    6: "L_ENC_A", 7: "L_ENC_B", 8: "L_ENC_SW", 9: "R_STICK_BTN", 10: "OLED_CS1", 11: "OLED_MOSI",
    12: "OLED_DC", 13: "OLED_SCK", 14: "L_STICK_X", 15: "L_STICK_Y", 16: "L_STICK_Z", 17: "FADER_WIPER",
    18: "R_CAM_A", 19: "R_CAM_B", 20: "R_STICK_X", 21: "R_STICK_Y", 22: "R_STICK_Z", 23: "R_CAM_SW",
    24: "OLED_CS2", 25: "BUZZER", 26: "TOG_ABORT", 27: "TOG_ARM", 28: "ROW0", 29: "ROW1", 30: "ROW2",
    31: "ROW3", 32: "COL0", 33: "COL1", 34: "COL2", 35: "COL3", 36: "COL4", 37: "COL5", 38: "R_PAGE_A",
    39: "R_PAGE_B", 40: "R_PAGE_SW", 41: "TOG_SPARE1"}
ANALOG = {14: "A0", 15: "A1", 16: "A2", 17: "A3", 20: "A6", 21: "A7", 22: "A8"}
# Physical header order, USB end at the top. Taken from memory of the Teensy 4.1 card, NOT yet checked
# against PJRC's pinout card: verify before wiring.
LEFT_COL = ["GND"] + list(range(0, 13)) + ["3V3"] + list(range(24, 33))
RIGHT_COL = ["VIN", "GND", "3V3"] + list(range(23, 12, -1)) + ["GND"] + list(range(41, 32, -1))
assert len(LEFT_COL) == 24 and len(RIGHT_COL) == 24

# ---- DB25 ports (docs/pin-map.md) --------------------------------------------------------------
GNDS = {1: "GND", 7: "GND", 13: "GND", 24: "GND", 25: "GND"}
V5 = {20: "5V", 21: "5V"}
PORTS = {
    "LW": ("LEFT WING", {**GNDS, 2: "3V3", 3: "L_STICK_X", 4: "L_STICK_Y", 5: "L_STICK_Z", 6: "FADER_WIPER",
                         8: "L_STICK_BTN", 9: "L_ENC_A", 10: "L_ENC_B", 11: "L_ENC_SW", 12: "FADER_TOUCH",
                         **V5, 22: "FADER_PWM_A", 23: "FADER_PWM_B"}),
    "RW": ("RIGHT WING", {1: "GND", 7: "GND", 13: "GND", 2: "3V3", 3: "R_STICK_X", 4: "R_STICK_Y",
                          5: "R_STICK_Z", 8: "R_STICK_BTN", 9: "R_CAM_A", 10: "R_CAM_B", 11: "R_CAM_SW",
                          12: "R_PAGE_A", 14: "R_PAGE_B", 19: "R_PAGE_SW"}),
    "LS": ("STRIP LEFT", {**GNDS, 3: "COL0", 4: "COL1", 5: "COL2", 6: "COL3", 8: "COL4", 9: "COL5",
                          10: "TOG_ABORT", 11: "TOG_ARM", 15: "ROW0", 16: "ROW1", 17: "PIXEL_IN",
                          18: "PIXEL_OUT", **V5}),
    "RS": ("STRIP RIGHT", {**GNDS, 3: "COL0", 4: "COL1", 5: "COL2", 6: "COL3", 8: "COL4", 9: "COL5",
                           10: "TOG_SPARE1", 11: "TOG_SPARE2", 15: "ROW2", 16: "ROW3", 17: "PIXEL_IN", **V5}),
}
MID_DEST = {"OLED_RES": "OLEDs", "OLED_CS1": "OLED 1", "OLED_CS2": "OLED 2", "OLED_MOSI": "OLEDs",
            "OLED_DC": "OLEDs", "OLED_SCK": "OLEDs", "BUZZER": "buzzer", "PIXEL_DATA": "chain, LS 17"}

e = html.escape


def dest(sig):
    if sig in MID_DEST:
        return MID_DEST[sig]
    hits = [(k, p) for k, (_, pins) in PORTS.items() for p, s in pins.items() if s == sig]
    if sig.startswith("COL"):
        return f"LS+RS {hits[0][1]}"
    return " ".join(f"{k} {p}" for k, p in hits)


# ---- svg helpers ---------------------------------------------------------------------------------
def line(x1, y1, x2, y2, colour, w=2.5):
    s = ""
    if colour == "black":
        s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#9aa5a0" stroke-width="{w + 2.1}"/>'
    return s + f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{COL[colour]}" stroke-width="{w}"/>'


def path(pts, colour, w=2):
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    s = ""
    if colour == "black":
        s += f'<path d="{d}" fill="none" stroke="#9aa5a0" stroke-width="{w + 2.1}" stroke-linejoin="round"/>'
    return s + f'<path d="{d}" fill="none" stroke="{COL[colour]}" stroke-width="{w}" stroke-linejoin="round"/>'


def dot(x, y, colour, r=3.2):
    extra = ' stroke="#9aa5a0" stroke-width="1"' if colour == "black" else ""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{COL[colour]}"{extra}/>'


def text(x, y, s, size=10.5, fill="var(--silk)", anchor="start", weight=None):
    wt = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}"{wt}>'
            f'{e(s)}</text>')


def pill(x, y, w, label, colour, dashed=False, size=10.5):
    """Outlined pill centred on y. GND uses the grey outline of the reference page."""
    stroke = "var(--wire-gnd)" if colour == "black" else COL[colour]
    fill = "var(--wire-gnd)" if colour == "black" else COL[colour]
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    return (f'<rect x="{x}" y="{y - 9}" width="{w}" height="18" rx="9" fill="none" stroke="{stroke}" '
            f'stroke-width="1.6"{dash}/>' + text(x + w / 2, y + 4, label, size, fill, "middle", 600))


def sigpill(x, y, w, sig, size=10.5):
    return pill(x, y, w, sig, SIGCOL[sig], size=size)


def box(x, y, w, h, title, sub=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>'
    s += text(x + w / 2, y + 20, title, 11, anchor="middle", weight=600)
    if sub:
        s += text(x + w / 2, y + 34, sub, 9, "var(--silk-dim)", "middle")
    return s


def svg(vb_w, vb_h, label, body):
    return (f'<svg class="wiring" viewBox="0 0 {vb_w} {vb_h}" role="img" aria-label="{e(label)}">{body}</svg>')


def svg_vb(vb, label, body):
    return f'<svg class="wiring" viewBox="{vb}" role="img" aria-label="{e(label)}">{body}</svg>'


def figure(svg_text, caption):
    return (f'<figure class="diagram-figure"><div class="diagram-scroll">{svg_text}</div>'
            f'<figcaption>{caption}</figcaption></figure>')


# ---- diagram 1: the five pieces ----------------------------------------------------------------------
def d_overview():
    b = pill(480, 28, 180, "PC · KSP + Simpit", "grey", size=12)
    b += line(570, 37, 570, 100, "grey") + text(582, 72, "USB serial", 11, "var(--silk-dim)")
    pieces = [
        (20, 100, "STRIP LEFT", "28° · 12 nav keys", "ABORT, STAGE ARM, 12 pixels"),
        (420, 100, "STRIP MIDDLE", "28° · Teensy 4.1", "2 OLEDs, buzzer, 32 fuel pixels"),
        (820, 100, "STRIP RIGHT", "28° · 12 action-group keys", "2 spare toggles, 12 pixels"),
        (20, 360, "LEFT WING", "12° · translation stick", "throttle fader, time-warp encoder"),
        (820, 360, "RIGHT WING", "12° · rotation stick", "camera and page encoders"),
    ]
    for x, y, t, s1, s2 in pieces:
        b += (f'<rect x="{x}" y="{y}" width="300" height="150" rx="5" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>'
              + text(x + 150, y + 36, t, 15, anchor="middle", weight=700)
              + text(x + 150, y + 68, s1, 11.5, "var(--silk-dim)", "middle")
              + text(x + 150, y + 90, s2, 11.5, "var(--silk-dim)", "middle"))
    b += text(570, 440, "open front: desk space", 12, "var(--silk-dim)", "middle")
    b += line(320, 175, 420, 175, "yellow", 4) + pill(330, 150, 80, "DB25 · 19", "yellow", size=10)
    b += line(720, 175, 820, 175, "yellow", 4) + pill(730, 150, 80, "DB25 · 18", "yellow", size=10)
    b += path([(320, 435), (470, 435), (470, 250)], "yellow", 4)
    b += pill(335, 410, 100, "DB25 · 19", "yellow", size=10) + text(335, 458, "through the strip shell", 10, "var(--silk-dim)")
    b += path([(820, 435), (670, 435), (670, 250)], "yellow", 4)
    b += pill(705, 410, 100, "DB25 · 14", "yellow", size=10) + text(690, 458, "through the strip shell", 10, "var(--silk-dim)")
    b += line(570, 250, 570, 300, "orange", 4) + text(582, 282, "DC jack, fuse", 10, "var(--silk-dim)")
    b += pill(480, 318, 180, "5 V 4 A wall adapter", "orange", size=11)
    b += text(20, 535, "Yellow = DB25 cable (conductor count). Orange = 5 V in.", 11, "var(--silk-dim)")
    return figure(svg(1140, 550, "Block diagram: five pieces joined by four DB25 cables to the middle strip", b),
                  "The middle strip holds the Teensy and everything that is not a switch. Each wing sits in front of "
                  "an outer strip piece, so its cable has to pass through that strip's shell on the way. The Teensy "
                  "is powered over USB only; the 5 V adapter feeds the pixels, the level shifter and the fader driver.")


# ---- diagram 2: the Teensy ---------------------------------------------------------------------------
def d_teensy():
    pitch, y0 = 34, 100
    b = f'<rect x="640" y="70" width="180" height="{24 * pitch + 50}" rx="6" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>'
    b += text(730, 118, "TEENSY 4.1", 13, anchor="middle", weight=700)
    b += text(730, 134, "USB end at the top", 9, "var(--silk-dim)", "middle")
    b += text(730, 150, "pins in physical order", 9, "var(--silk-dim)", "middle")
    b += text(730, 880, "powered over USB only", 9.5, "var(--wire-power)", "middle")
    b += '<rect x="690" y="76" width="80" height="22" rx="3" fill="#2b2f2c" opacity="0.55"/>'
    for i in range(24):
        y = y0 + i * pitch
        for side, item in (("L", LEFT_COL[i]), ("R", RIGHT_COL[i])):
            x_in, x_out = (640, 600) if side == "L" else (820, 860)
            anchor = "end" if side == "L" else "start"
            xt = x_out - 6 if side == "L" else x_out + 6
            xp = 440 if side == "L" else 960
            if item in ("GND", "3V3"):
                col = "black" if item == "GND" else "red"
                b += line(x_out, y, x_in, y, col) + dot(x_in, y, col)
                b += pill(xt - 46 if side == "L" else xt, y, 46, item, col)
                continue
            if item == "VIN":
                b += line(x_out, y, x_in, y, "grey") + text(xt, y + 4, "VIN (unused)", 10, "var(--silk-dim)", anchor)
                continue
            sig = TEENSY.get(item)
            if not sig:
                b += line(x_out, y, x_in, y, "grey", 1)
                b += text(xt, y + 4, f"D{item}", 10, "var(--silk-dim)", anchor)
                continue
            col = SIGCOL[sig]
            b += line(x_out, y, x_in, y, col) + dot(x_out, y, col)
            pn = f"D{item}" + (f" · {ANALOG[item]}" if item in ANALOG else "")
            b += text(xt, y - 5, pn, 12, anchor=anchor, weight=600)
            b += text(xt, y + 11, sig, 9.5, "var(--silk-dim)", anchor)
            b += pill(xp if side == "R" else xp - 10, y, 92, dest(sig), "grey", size=9.5)
    return figure(svg_vb("320 40 740 900", "Teensy 4.1 pin assignment in physical row order, each used pin drawn in its wire colour", b),
                  "Each used pin is drawn in the wire colour of its signal, with a grey tag showing where it goes: a DB25 "
                  "port and pin (LW, RW, LS, RS) or a device in the middle strip. Wires aren't drawn between the Teensy "
                  "and the ports, because forty of them would cross; use the tags and the pinout grid below. "
                  "<strong>The physical pin order is from memory and unchecked</strong>: compare it with "
                  '<a href="https://www.pjrc.com/store/teensy41.html">PJRC&rsquo;s pinout card</a> before wiring. '
                  "All pins are 3.3 V only.")


# ---- diagram 3: the four DB25 ports -------------------------------------------------------------------
def d_db25():
    b = ""
    cols = [("LW", 90), ("RW", 320), ("LS", 550), ("RS", 780)]
    for key, x in cols:
        name, pins = PORTS[key]
        b += text(x + 100, 36, f"{name}", 12, anchor="middle", weight=600)
        b += text(x + 100, 52, f"{len(pins)} conductors", 9.5, "var(--silk-dim)", "middle")
    for p in range(1, 26):
        y = 80 + (p - 1) * 24
        b += text(40, y + 4, str(p), 11, "var(--silk-dim)", "middle", 600)
        for key, x in cols:
            sig = PORTS[key][1].get(p)
            if sig:
                b += sigpill(x, y, 200, sig, 10)
            else:
                b += text(x + 100, y + 4, "open", 9.5, "var(--silk-dim)", "middle")
    b += text(40, 66, "pin", 9, "var(--silk-dim)", "middle")
    return figure(svg(1000, 700, "DB25 pinouts for the four ports, pin by pin", b),
                  "Standard DB25 numbering. Every port uses the same connector, and the pins are laid out so a cable "
                  "in the wrong port does no damage: ground and 5 V sit on the same pins everywhere, and everything "
                  "the Teensy drives (matrix rows, pixel data, fader PWM) is on pins 15&ndash;23, which any module "
                  "that does not use them leaves open. COL0&ndash;5 appear on both strip ports and join in the "
                  "middle piece.")


# ---- diagram 4: per-piece harness -----------------------------------------------------------------
def harness(title, port, devices, note, extra_h=0):
    pins = sorted(PORTS[port][1].items())
    pitch = 24
    b = text(60, 30, title, 12, anchor="start", weight=600) + text(60, 46, f"jack: DB25 {port}", 9.5, "var(--silk-dim)")
    # jack
    jy0 = 70
    jh = len(pins) * pitch + 20
    b += f'<rect x="60" y="{jy0 - 14}" width="170" height="{jh}" rx="5" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>'
    jack_y = {}
    for i, (p, sig) in enumerate(pins):
        y = jy0 + i * pitch
        jack_y[p] = y
        b += text(74, y + 4, str(p), 10.5, "var(--silk-dim)") + text(100, y + 4, sig, 10.5)
        b += dot(230, y, SIGCOL[sig])
    # devices
    dx, wires, k = 700, [], 0
    y = 70
    dev_pin_y = {}
    for dev in devices:
        h = 54 + 24 * len(dev["pins"])
        b += box(dx, y - 14, 300, h, dev["name"], dev.get("sub"))
        for j, (label, sig) in enumerate(dev["pins"]):
            py = y + 36 + 24 * j
            b += dot(dx, py, SIGCOL.get(sig, "grey")) + text(dx + 12, py + 4, label, 10.5)
            if sig in ("3V3", "5V", "GND") or sig is None:
                if sig:
                    b += pill(dx - 54, py, 46, sig, SIGCOL[sig])
            else:
                dev_pin_y[(dev["name"], j)] = (py, sig)
        y += h + 16
    # wires: jack pin -> device pin, one per signal; power is shown as tags, not wires
    for dev in devices:
        for j, (label, sig) in enumerate(dev["pins"]):
            if sig in ("3V3", "5V", "GND") or sig is None:
                continue
            pins_for = [p for p, s in pins if s == sig]
            if not pins_for:
                continue
            py, _ = dev_pin_y[(dev["name"], j)]
            jy = jack_y[pins_for[0]]
            mx = 270 + (k % 14) * 26
            b += path([(230, jy), (mx, jy), (mx, py), (dx, py)], SIGCOL[sig])
            k += 1
    for p, sig in pins:
        if sig in ("3V3", "5V", "GND"):
            b += pill(238, jack_y[p], 46, sig, SIGCOL[sig])
    height = max(jy0 + jh, y) + 40 + extra_h
    b += text(60, height - 14, note, 9.5, "var(--silk-dim)")
    return svg(1100, height, f"{title}: wiring from the DB25 jack to each device", b)


def d_pieces():
    out = []
    out.append(("Left wing", figure(harness("LEFT WING", "LW", [
        {"name": "JH-D400X-R4 · LEFT STICK", "sub": "3 pots + top button", "pins": [
            ("X pot wiper", "L_STICK_X"), ("Y pot wiper", "L_STICK_Y"), ("Twist (Z) pot wiper", "L_STICK_Z"),
            ("Top button", "L_STICK_BTN"), ("pot high ends", "3V3"), ("pot low ends, button", "GND")]},
        {"name": "FADER · Adafruit 5466", "sub": "10 kΩ, 100 mm, motorised", "pins": [
            ("pot high", "3V3"), ("wiper", "FADER_WIPER"), ("pot low", "GND"), ("touch pad (nubbin)", "FADER_TOUCH"),
            ("motor pin 1  ← OA", None), ("motor pin 2  ← OB", None)]},
        {"name": "L9110H FADER DRIVER", "sub": "next to the motor", "pins": [
            ("VCC", "5V"), ("GND", "GND"), ("IA  (PWM A)", "FADER_PWM_A"), ("IB  (PWM B)", "FADER_PWM_B"),
            ("OA → fader motor", None), ("OB → fader motor", None)]},
        {"name": "ENCODER · TIME WARP", "sub": "Bourns PEC11R", "pins": [
            ("A", "L_ENC_A"), ("B", "L_ENC_B"), ("Push", "L_ENC_SW"), ("Common", "GND")]},
    ], "Pots take 3V3, never 5 V. The motor wires go from the driver to the fader, either way round: swap them if the "
       "fader runs backwards. Add a 47 µF capacitor across the driver's supply. Pin order on each part is shown by "
       "function, not position: wire by the printed labels and check the stick's pin order on the real unit."),
        "The left wing: stick, throttle fader with its driver, and the time-warp encoder.")))
    out.append(("Right wing", figure(harness("RIGHT WING", "RW", [
        {"name": "JH-D400X-R4 · RIGHT STICK", "sub": "3 pots + top button", "pins": [
            ("X pot wiper", "R_STICK_X"), ("Y pot wiper", "R_STICK_Y"), ("Twist (Z) pot wiper", "R_STICK_Z"),
            ("Top button", "R_STICK_BTN"), ("pot high ends", "3V3"), ("pot low ends, button", "GND")]},
        {"name": "ENCODER · CAMERA", "sub": "Bourns PEC11R", "pins": [
            ("A", "R_CAM_A"), ("B", "R_CAM_B"), ("Push", "R_CAM_SW"), ("Common", "GND")]},
        {"name": "ENCODER · DISPLAY PAGE", "sub": "Bourns PEC11R", "pins": [
            ("A", "R_PAGE_A"), ("B", "R_PAGE_B"), ("Push", "R_PAGE_SW"), ("Common", "GND")]},
    ], "Pots take 3V3, never 5 V. Wire by the printed labels."),
        "The right wing: rotation stick and two encoders.")))
    for port, rows, toggles, pix_out, label in (
            ("LS", "rows 0 and 1", [("ABORT toggle", "TOG_ABORT"), ("STAGE ARM toggle", "TOG_ARM")], True, "Strip left"),
            ("RS", "rows 2 and 3", [("SPARE toggle 1", "TOG_SPARE1"), ("SPARE toggle 2", "TOG_SPARE2")], False, "Strip right")):
        r0 = 0 if port == "LS" else 2
        devs = [{"name": f"KEY MATRIX · {rows}", "sub": "12 keys, a diode on each", "pins": [
            (f"ROW{r0}", f"ROW{r0}"), (f"ROW{r0 + 1}", f"ROW{r0 + 1}")] + [(f"COL{c}", f"COL{c}") for c in range(6)]}]
        for name, sig in toggles:
            devs.append({"name": name.upper(), "sub": "guarded, 2 pin", "pins": [("pin 1", sig), ("pin 2", "GND")]})
        pix = [("DIN  (first pixel)", "PIXEL_IN")]
        if pix_out:
            pix.append(("DOUT (last pixel)", "PIXEL_OUT"))
        pix += [("5V", "5V"), ("GND", "GND")]
        devs.append({"name": "12 PIXELS", "sub": "one chain through the strip", "pins": pix})
        note = ("Each key's diode: anode to its column, cathode to its row. Series resistor 330–470 Ω in the data "
                "line at the first pixel. ") if port == "LS" else (
            "Spare toggle 2 has a conductor but no Teensy pin yet. Each key's diode: anode to its column, cathode to its row.")
        out.append((label, figure(harness(label.upper(), port, devs, note),
                                  f"{label}: the key matrix ({rows}), two toggles and 12 pixels.")))
    return out


# ---- diagram 5: the middle piece -------------------------------------------------------------------------
def d_middle():
    b = text(60, 30, "STRIP MIDDLE", 12, weight=600) + text(60, 46, "Teensy-side wiring inside the piece", 9.5, "var(--silk-dim)")
    sigs = ["OLED_SCK", "OLED_MOSI", "OLED_DC", "OLED_RES", "OLED_CS1", "OLED_CS2", "BUZZER", "PIXEL_DATA"]
    pin_of = {v: k for k, v in TEENSY.items()}
    b += f'<rect x="60" y="56" width="200" height="{len(sigs) * 24 + 24}" rx="5" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>'
    ty = {}
    for i, s in enumerate(sigs):
        y = 86 + i * 24
        ty[s] = y
        b += text(74, y + 4, f"D{pin_of[s]}", 10.5, "var(--silk-dim)") + text(112, y + 4, s, 10.5) + dot(260, y, SIGCOL[s])
    devs = [
        ("OLED 1 · 2.42″ SSD1309", [("SCK", "OLED_SCK"), ("SDA (MOSI)", "OLED_MOSI"), ("DC", "OLED_DC"),
                                     ("RES", "OLED_RES"), ("CS", "OLED_CS1"), ("VCC", "3V3"), ("GND", "GND")]),
        ("OLED 2 · 2.42″ SSD1309", [("SCK", "OLED_SCK"), ("SDA (MOSI)", "OLED_MOSI"), ("DC", "OLED_DC"),
                                     ("RES", "OLED_RES"), ("CS", "OLED_CS2"), ("VCC", "3V3"), ("GND", "GND")]),
        ("BUZZER MODULE · low-level trigger", [("I/O", "BUZZER"), ("VCC", "3V3"), ("GND", "GND")]),
        ("74AHCT125 LEVEL SHIFTER", [("1A  (input)", "PIXEL_DATA"), ("1OE", "GND"), ("VCC", "5V"), ("GND", "GND"),
                                      ("1Y  → 330 Ω → LS 17", None)]),
    ]
    dx, y, k, ypos = 720, 56, 0, []
    for name, pins in devs:
        h = 54 + 24 * len(pins)
        b += box(dx, y, 300, h, name)
        for j, (label, sig) in enumerate(pins):
            py = y + 38 + 24 * j
            b += dot(dx, py, SIGCOL.get(sig, "grey")) + text(dx + 12, py + 4, label, 10.5)
            if sig in ("3V3", "5V", "GND"):
                b += pill(dx - 54, py, 46, sig, SIGCOL[sig])
            elif sig:
                mx = 300 + (k % 14) * 26
                b += path([(260, ty[sig]), (mx, ty[sig]), (mx, py), (dx, py)], SIGCOL[sig])
                k += 1
        y += h + 16
    b += text(60, y + 24, "⚠ OLED VCC on 3V3 until you have checked that the modules' SPI lines are safe at 5 V. The "
                          "buzzer module must run from 3V3: at 5 V its transistor may not switch off.", 9.5, "var(--wire-warn)")
    return figure(svg(1100, y + 50, "Middle strip: Teensy to the OLEDs, buzzer module and level shifter", b),
                  "The two OLEDs share the SPI clock, data, DC and reset lines and have a chip-select each. The pixel "
                  "chain starts at the level shifter: its output goes through a 330&ndash;470 &Omega; resistor to "
                  "the left strip (LS pin 17), comes back on LS pin 18 into the 32 fuel-bar pixels here, and leaves "
                  "for the right strip on RS pin 17.")


# ---- diagram 6: power -------------------------------------------------------------------------------------
def d_power():
    b = pill(40, 50, 170, "5 V 4 A wall adapter", "orange") + line(210, 50, 270, 50, "orange", 4)
    b += pill(270, 50, 150, "DC jack, 12 mm", "orange") + line(420, 50, 470, 50, "orange", 4)
    b += pill(470, 50, 90, "fuse", "orange") + line(560, 50, 620, 50, "orange", 4)
    b += box(620, 18, 190, 64, "5 V RAIL", "1000 µF across it")
    b += text(860, 106, "everything below is fed from the rail", 10.5, "var(--silk-dim)")
    outs = [("Left strip pixels", "LS 20, 21"), ("Right strip pixels", "RS 20, 21"),
            ("Left wing: fader driver", "LW 20, 21"), ("32 fuel pixels (middle)", "direct, short wire"),
            ("74AHCT125 level shifter", "direct")]
    for i, (n, t) in enumerate(outs):
        y = 130 + i * 40
        b += path([(810, 50), (840, 50), (840, y), (860, y)], "orange") + pill(860, y, 190, n, "orange", size=10)
        b += text(1060, y + 4, t, 10, "var(--silk-dim)")
    b += text(40, 150, "Teensy: USB only.", 11, "var(--wire-power)")
    b += text(40, 170, "Never connect the 5 V rail to the", 10, "var(--silk-dim)")
    b += text(40, 184, "Teensy's VIN while USB is plugged in.", 10, "var(--silk-dim)")
    b += pill(40, 230, 46, "GND", "black") + text(96, 234, "one ground, shared by the adapter, the Teensy and every piece", 10, "var(--silk-dim)")
    b += pill(40, 262, 46, "3V3", "red") + text(96, 266, "from the Teensy only: pots, buzzer module and OLEDs", 10, "var(--silk-dim)")
    return figure(svg(1200, 330, "Power: adapter, jack, fuse and rail, feeding the pixels, level shifter and fader driver", b),
                  "The Teensy takes power over USB; the 5 V adapter feeds only the pixels, the level shifter and the fader "
                  "driver, with its ground joined to the Teensy's. Size the fuse just above the capped load (about 3&ndash;4 A) "
                  "and cap brightness in firmware.")


# ---- tables -------------------------------------------------------------------------------------
def swatch(c):
    border = "#888" if c in ("white", "black") else "transparent"
    return (f'<span style="display:inline-block;width:11px;height:11px;border-radius:50%;background:{COL[c]};'
            f'border:1px solid {border};vertical-align:-1px;margin-right:4px"></span>')


def t_teensy():
    rows = ""
    for pin in sorted(TEENSY):
        sig = TEENSY[pin]
        a = f" ({ANALOG[pin]})" if pin in ANALOG else ""
        rows += (f'<tr><td class="mono gpio">{pin}{a}</td><td>{swatch(SIGCOL[sig])}{e(sig)}</td>'
                 f'<td class="mono">{e(dest(sig))}</td></tr>')
    return ('<div class="table-wrap"><table><thead><tr><th>Teensy pin</th><th>Signal</th><th>Goes to</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def t_colours():
    items = [
        ("3V3", "red", "pots, buzzer module and OLEDs: from the Teensy"), ("5V", "orange", "pixels, level shifter, fader driver"),
        ("GND", "black", "everything; drawn with a light edge so it shows"),
        ("Stick X / Y / twist", "purple", "X purple, Y grey, twist brown: both sticks"),
        ("Fader wiper", "green", ""), ("Fader touch, every push switch and toggle", "white", "to ground"),
        ("Encoder A / B", "blue", "A blue, B yellow"), ("Fader PWM A / B", "pink", "A pink, B teal"),
        ("Matrix rows / columns", "green", "rows green, columns blue"), ("Pixel data", "pink", "in and out"),
        ("OLED SCK / MOSI / DC / RES / CS", "yellow", "yellow, blue, grey, teal, green (CS2 purple)"),
        ("Buzzer I/O", "brown", ""),
    ]
    rows = "".join(f"<tr><td>{e(n)}</td><td>{swatch(c)}{c}</td><td class=\"note\">{e(t)}</td></tr>" for n, c, t in items)
    return ('<div class="table-wrap"><table><thead><tr><th>Signal</th><th>Colour</th><th>Note</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


LEGEND = [("red", "3V3"), ("orange", "5 V"), ("black", "GND"), ("purple", "stick X"), ("grey", "stick Y, OLED DC"),
          ("brown", "stick twist, buzzer"), ("green", "fader wiper, matrix rows"), ("blue", "encoder A, matrix columns"),
          ("yellow", "encoder B, DB25 cables"), ("white", "switches and fader touch"), ("pink", "fader PWM A, pixel data"),
          ("teal", "fader PWM B, OLED reset")]


def legend():
    items = ""
    for c, label in LEGEND:
        edge = "border:1px solid #9aa5a0;" if c in ("black", "white") else ""
        items += f'<div class="legend-item"><span class="legend-swatch" style="background:{COL_HEX[c]};{edge}"></span>{e(label)}</div>'
    items += '<div class="legend-item">⚠ easy to get wrong: read the flag</div>'
    return f'<div class="legend">{items}</div>'


COL_HEX = {"red": "#e5484d", "black": "#161a18", "white": "#f4f4f4", "blue": "#3b82f6", "yellow": "#eab308",
           "green": "#22c55e", "orange": "#f97316", "brown": "#a35a2a", "purple": "#a855f7", "grey": "#9ca3af",
           "pink": "#ec4899", "teal": "#14b8a6"}

# ---- page ----------------------------------------------------------------------------------------------
CSS = """
  :root { --paper:#f5f2ea; --ink:#201d16; --ink-dim:#7a7566; --rule:#ded7c4; --accent:#8a5a2b; --card:#ffffff; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) { --paper:#14171a; --ink:#eae6d9; --ink-dim:#96917f; --rule:#2c2f2a; --accent:#d9a35f; --card:#1b1e1a; }
  }
  :root[data-theme="dark"] { --paper:#14171a; --ink:#eae6d9; --ink-dim:#96917f; --rule:#2c2f2a; --accent:#d9a35f; --card:#1b1e1a; }
  svg.wiring {
    --panel-bg:#0c1210; --pcb:#123d2e; --pcb-edge:#1f5c45; --silk:#eef1ea; --silk-dim:#8fa097; --pad:#d9a35f;
    --wire-power:#d9a35f; --wire-gnd:#7b8a82; --wire-signal:#45c2b3; --wire-warn:#e2666a;
    --c-red:#e5484d; --c-black:#161a18; --c-white:#f4f4f4; --c-blue:#3b82f6; --c-yellow:#eab308; --c-green:#22c55e;
    --c-orange:#f97316; --c-brown:#a35a2a; --c-purple:#a855f7; --c-grey:#9ca3af; --c-pink:#ec4899; --c-teal:#14b8a6;
    font-family: "IBM Plex Mono", monospace;
  }
  * { box-sizing: border-box; }
  body { background:var(--paper); color:var(--ink); font-family:"IBM Plex Sans", system-ui, sans-serif;
         padding:28px 20px 64px; max-width:1100px; margin:0 auto; }
  h1, h2, h3 { font-family:"IBM Plex Mono","SF Mono",monospace; text-wrap:balance; }
  h1 { font-size:clamp(1.4rem,1rem + 2vw,1.9rem); font-weight:700; margin:0 0 4px; letter-spacing:-0.01em; }
  .subtitle { color:var(--ink-dim); font-size:0.95rem; margin:0 0 28px; max-width:70ch; }
  .eyebrow { font-family:"IBM Plex Mono",monospace; font-size:0.72rem; letter-spacing:0.12em; text-transform:uppercase;
             color:var(--accent); margin:0 0 6px; }
  figure.diagram-figure { margin:0 0 20px; padding:0; }
  .diagram-scroll { overflow-x:auto; background:#0c1210; border-radius:10px; padding:6px; }
  svg.wiring { display:block; width:100%; height:auto; min-width:720px; }
  figcaption { font-size:0.85rem; color:var(--ink-dim); margin-top:10px; max-width:76ch; }
  .legend { display:flex; flex-wrap:wrap; gap:14px 18px; margin:0 0 40px; padding:14px 16px; background:var(--card);
            border:1px solid var(--rule); border-radius:8px; }
  .legend-item { display:flex; align-items:center; gap:8px; font-size:0.82rem; color:var(--ink-dim); }
  .legend-swatch { width:22px; height:4px; border-radius:2px; flex:none; }
  h2 { font-size:1.05rem; font-weight:600; margin:40px 0 4px; padding-bottom:10px; border-bottom:1px solid var(--rule); }
  .table-wrap { overflow-x:auto; margin-top:14px; }
  table { width:100%; border-collapse:collapse; font-size:0.88rem; }
  th, td { text-align:left; padding:7px 12px; border-bottom:1px solid var(--rule); }
  th { font-family:"IBM Plex Mono",monospace; font-size:0.68rem; letter-spacing:0.08em; text-transform:uppercase;
       color:var(--ink-dim); font-weight:500; }
  td.mono, .mono { font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums; }
  .gpio { color:var(--accent); font-weight:600; }
  .note { color:var(--ink-dim); font-size:0.85em; }
  footer { margin-top:48px; padding-top:18px; border-top:1px solid var(--rule); font-size:0.85rem; color:var(--ink-dim); }
  footer strong { color:var(--ink); }
  a { color:var(--accent); }
"""


def page():
    p = ['<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">',
         "<title>Kerbal Controller Wiring</title>",
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700'
         '&family=IBM+Plex+Sans:wght@400;500;600&display=swap">',
         f"<style>{CSS}</style>",
         '<p class="eyebrow">kerbal-controller · hardware reference</p><h1>Wiring reference</h1>',
         '<p class="subtitle">Every pin in use, drawn from <code>docs/pin-map.md</code>. Nothing is built yet and none of '
         "this has been checked against real hardware: treat it as the plan to wire from, and correct it when a part "
         "turns out different. Generated by <code>docs/tools/gen_pinout.py</code>; the same data is in "
         "<code>docs/pin-map.md</code>.</p>",
         "<h2>The five pieces</h2>", d_overview(), legend(),
         "<h2>Teensy 4.1</h2>", d_teensy(),
         "<h2>The four DB25 ports</h2>", d_db25()]
    p.append("<h2>Inside each piece</h2>")
    for name, fig in d_pieces():
        p.append(f"<h3>{e(name)}</h3>{fig}")
    p += ["<h3>Strip middle</h3>", d_middle(), "<h2>Power</h2>", d_power(),
          "<h2>Wire colours</h2>",
          '<p class="note" style="margin-top:14px;max-width:72ch">The same signal is the same colour at both ends of '
          "its wire. Red is always 3V3, black is always GND, orange is always 5 V. A colour can repeat when the wires "
          "never sit side by side, and inside a piece the pin labels settle which is which.</p>",
          t_colours(), "<h2>Teensy pins</h2>", t_teensy(),
          "<footer><strong>Wiring order:</strong> ground and power first. Check every ground and the 5 V rail with a "
          "multimeter, with nothing plugged in, before connecting a device. Then the Teensy side of each port, then "
          "each outer piece one at a time. The full checklist is in <code>docs/wiring-checklist.md</code>.</footer>"]
    return "\n".join(p)


if __name__ == "__main__":
    out = page()
    for chunk in out.split("<svg")[1:]:                      # every diagram must be well-formed XML
        xml.dom.minidom.parseString("<svg" + chunk.split("</svg>")[0] + "</svg>")
    open(OUT, "w").write(out)
    print("wrote", OUT, len(out), "bytes")
