#!/usr/bin/env python3
"""Generate the wiring docs and the firmware pin header from hardware/electronics/pinmap.json.

Run from anywhere:  python3 tools/gen_wiring.py
Writes docs/pinout.html (the page GitHub Pages serves, in the style of the goodnight-device pinout page),
hardware/electronics/wiring/{wiring.md,pin-map.md,diagrams/*.svg} and firmware/ksp/include/pins.h.
Edit the pin data in pinmap.json, not the outputs.
"""
import html
import json
import os
import sys
import xml.dom.minidom

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "docs", "pinout.html")
WIRING_DIR = os.path.join(REPO, "hardware", "electronics", "wiring")
PINS_H = os.path.join(REPO, "firmware", "ksp", "include", "pins.h")

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
               "TFT_MOSI": "blue", "TFT_SCK": "yellow", "TFT_DC": "grey", "TFT_RES": "teal",
               "TFT_CS1": "green", "TFT_CS2": "purple", "BUZZER": "brown",
               "EXP_SDA": "purple", "EXP_SCL": "grey", "EXP_INT": "teal"})
for i in range(4):
    SIGCOL[f"ROW{i}"] = "green"
for i in range(6):
    SIGCOL[f"COL{i}"] = "blue"

# ---- pin data: hardware/electronics/pinmap.json is the single source ----------------------------
PINMAP = json.load(open(os.path.join(REPO, "hardware", "electronics", "pinmap.json")))
TEENSY = {int(k): v for k, v in PINMAP["teensy"].items()}
ANALOG = {int(k): v for k, v in PINMAP["analog"].items()}
# Physical header order, USB end at the top. Taken from memory of the Teensy 4.1 card, NOT yet checked
# against PJRC's pinout card: verify before wiring.
LEFT_COL = ["GND"] + list(range(0, 13)) + ["3V3"] + list(range(24, 33))
RIGHT_COL = ["VIN", "GND", "3V3"] + list(range(23, 12, -1)) + ["GND"] + list(range(41, 32, -1))
assert len(LEFT_COL) == 24 and len(RIGHT_COL) == 24

# ---- DB25 ports (hardware/electronics/pinmap.json) -----------------------------------------------
PORTS = {k: (v["name"], {int(p): sig for p, sig in v["pins"].items()}) for k, v in PINMAP["ports"].items()}
MID_DEST = PINMAP["mid_dest"]

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


FIGS = []        # (svg, caption) in the order the page builds them


def figure(svg_text, caption):
    FIGS.append((svg_text, caption))
    return (f'<figure class="diagram-figure"><div class="diagram-scroll">{svg_text}</div>'
            f'<figcaption>{caption}</figcaption></figure>')


# ---- diagram 1: the five pieces ----------------------------------------------------------------------
def d_overview():
    b = pill(480, 28, 180, "PC · KSP + Simpit", "grey", size=12)
    b += line(570, 37, 570, 100, "grey") + text(582, 72, "USB serial", 11, "var(--silk-dim)")
    pieces = [
        (20, 100, "STRIP LEFT", "28° · 12 nav keys", "switch panel + expander, 12 pixels"),
        (420, 100, "STRIP MIDDLE", "28° · Teensy 4.1", "2 TFTs, buzzer, master switch, 32 pixels"),
        (820, 100, "STRIP RIGHT", "28° · 12 action-group keys", "annunciator, 21 pixels"),
        (20, 360, "LEFT WING", "12° · translation stick", "throttle fader, time-warp encoder"),
        (820, 360, "RIGHT WING", "12° · rotation stick", "camera and page encoders"),
    ]
    for x, y, t, s1, s2 in pieces:
        b += (f'<rect x="{x}" y="{y}" width="300" height="150" rx="5" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>'
              + text(x + 150, y + 36, t, 15, anchor="middle", weight=700)
              + text(x + 150, y + 68, s1, 11.5, "var(--silk-dim)", "middle")
              + text(x + 150, y + 90, s2, 11.5, "var(--silk-dim)", "middle"))
    b += text(570, 440, "open front: desk space", 12, "var(--silk-dim)", "middle")
    b += line(320, 175, 420, 175, "yellow", 4) + pill(330, 150, 80, "DB25 · 21", "yellow", size=10)
    b += line(720, 175, 820, 175, "yellow", 4) + pill(730, 150, 80, "DB25 · 16", "yellow", size=10)
    b += path([(320, 435), (470, 435), (470, 250)], "yellow", 4)
    b += pill(335, 410, 100, "DB25 · 19", "yellow", size=10) + text(335, 458, "round the back", 10, "var(--silk-dim)")
    b += path([(820, 435), (670, 435), (670, 250)], "yellow", 4)
    b += pill(705, 410, 100, "DB25 · 14", "yellow", size=10) + text(705, 458, "round the back", 10, "var(--silk-dim)")
    b += line(570, 250, 570, 300, "orange", 4) + text(582, 282, "DC jack, fuse", 10, "var(--silk-dim)")
    b += pill(480, 318, 180, "5 V 4 A wall adapter", "orange", size=11)
    b += text(20, 535, "Yellow = DB25 cable (conductor count). Orange = 5 V in.", 11, "var(--silk-dim)")
    return figure(svg(1140, 550, "Block diagram: five pieces joined by four DB25 cables to the middle strip", b),
                  "The middle strip holds the Teensy and everything that is not a switch. Each wing sits in front of "
                  "an outer strip piece, so its jack is on the wing's outer end wall and its cable runs round the back. The Teensy "
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
                  "Standard DB25 numbering. All four middle jacks are alike, and the pins are laid out so a cable "
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
    import textwrap
    lines = textwrap.wrap(note, 140)
    height = max(jy0 + jh, y) + 30 + 14 * len(lines) + extra_h
    for i, ln in enumerate(lines):
        b += text(60, height - 14 * (len(lines) - i), ln, 9.5, "var(--silk-dim)")
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
            ("LS", "rows 0 and 1", [], True, "Strip left"),
            ("RS", "rows 2 and 3", [], False, "Strip right")):
        r0 = 0 if port == "LS" else 2
        devs = [{"name": f"KEY MATRIX · {rows}", "sub": "12 keys, a diode on each", "pins": [
            (f"ROW{r0}", f"ROW{r0}"), (f"ROW{r0 + 1}", f"ROW{r0 + 1}")] + [(f"COL{c}", f"COL{c}") for c in range(6)]}]
        for name, sig in toggles:
            devs.append({"name": name.upper(), "sub": "guarded, 2 pin", "pins": [("pin 1", sig), ("pin 2", "GND")]})
        if port == "LS":
            devs.append({"name": "SWITCH PANEL EXPANDER", "sub": "MCP23017, behind the panel", "pins": [
                ("SDA", "EXP_SDA"), ("SCL", "EXP_SCL"), ("INT (INTA)", "EXP_INT"), ("VCC", "3V3"), ("GND", "GND")]})
        pix = [("DIN  (first pixel)", "PIXEL_IN")]
        if pix_out:
            pix.append(("DOUT (last pixel)", "PIXEL_OUT"))
        pix += [("5V", "5V"), ("GND", "GND")]
        devs.append({"name": "12 PIXELS" if port == "LS" else "21 PIXELS", "sub":
                     "one chain through the strip" if port == "LS" else "12 key pixels + 9 annunciator", "pins": pix})
        note = ("Each key's diode: anode to its column, cathode to its row. Series resistor 330–470 Ω in the data "
                "line at the first pixel. The 16 switch-panel inputs wire locally to the expander, see the next diagram.") if port == "LS" else (
            "Each key's diode: anode to its column, cathode to its row. The 9 annunciator pixels follow the 12 key pixels in the chain.")
        out.append((label, figure(harness(label.upper(), port, devs, note),
                                  f"{label}: the key matrix ({rows}), two toggles and 12 pixels.")))
    return out


# ---- diagram 4b: the switch panel -------------------------------------------------------------------
SWITCHES = ["ABORT (guarded toggle)", "STAGE KEY (arms STAGE)", "STAGE (big button)", "THROTTLE FULL",
            "THROTTLE CUT", "MAP", "FOCUS PREVIOUS", "FOCUS NEXT", "QUICKSAVE", "QUICKLOAD", "PRECISION",
            "PAUSE", "UI HIDE", "ENGAGE / DISENGAGE (guarded toggle)", "SPARE 1", "SPARE 2"]


def d_switch_panel():
    pins = [f"PA{i}" for i in range(8)] + [f"PB{i}" for i in range(8)]
    y0, pitch = 100, 24
    b = text(60, 30, "SWITCH PANEL · LEFT STRIP", 12, weight=600)
    b += text(60, 46, "every input on the I²C expander, wired locally", 9.5, "var(--silk-dim)")
    last = y0 + pitch * 15
    iy = last + 50
    box_bottom = iy + 24 * 4 + 22
    b += (f'<rect x="60" y="62" width="210" height="{box_bottom - 62}" rx="5" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>')
    b += text(165, 82, "MCP23017 expander", 11, anchor="middle", weight=600)
    for k, pn in enumerate(pins):
        y = y0 + pitch * k
        b += text(74, y + 4, pn, 10.5, "var(--silk-dim)") + dot(270, y, "white")
        b += line(270, y, 640, y, "white", 2)
    b += (f'<rect x="640" y="{y0 - 44}" width="330" height="{pitch * 16 + 48}" rx="5" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>')
    b += text(805, y0 - 22, "THE 16 SWITCHES", 11, anchor="middle", weight=600)
    for k, name in enumerate(SWITCHES):
        y = y0 + pitch * k
        b += dot(640, y, "white") + text(654, y + 4, name, 10.5)
        b += pill(912, y, 46, "GND", "black", size=9.5)
    for j, (label, sig, tag) in enumerate([("SDA", "EXP_SDA", "DB25 LS 10"), ("SCL", "EXP_SCL", "DB25 LS 11"),
                                           ("INTA", "EXP_INT", "DB25 LS 12"), ("VCC", "3V3", "DB25 LS 2"),
                                           ("GND", "GND", "DB25 LS 1, 7, 13")]):
        y = iy + 24 * j
        b += text(74, y + 4, label, 10.5, "var(--silk-dim)") + dot(270, y, SIGCOL[sig])
        b += pill(290, y, 150, "→ " + tag, "grey", size=10)
    b += text(60, box_bottom + 24, "Other leg of every switch to GND. Pull-ups are inside the expander. Mirror both interrupt ports onto INTA.", 9.5, "var(--silk-dim)")
    b += text(60, box_bottom + 40, "A0-A2 to GND (0x20), RESET through 10 k to 3V3, 0.1 uF decoupling. Confirm the address with a bus scan.", 9.5, "var(--silk-dim)")
    return figure(svg(1100, box_bottom + 64, "Switch panel: the MCP23017 expander and its 16 inputs", b),
                  "All sixteen inputs live on one panel and one chip. The expander sits right behind the panel, so only "
                  "its I&sup2;C lines (SDA, SCL), the interrupt and 3V3 cross the DB25 cable to the Teensy. Fit 4.7 k&Omega; "
                  "pull-ups on SDA and SCL at the Teensy end. Buttons are MX switches with blank DSA caps; the guarded ABORT "
                  "and ENGAGE / DISENGAGE toggles, the STAGE key switch and the big STAGE button are separate parts.")


# ---- diagram 5: the middle piece -------------------------------------------------------------------------
def d_middle():
    b = text(60, 30, "STRIP MIDDLE", 12, weight=600) + text(60, 46, "Teensy-side wiring inside the piece", 9.5, "var(--silk-dim)")
    sigs = ["TFT_SCK", "TFT_MOSI", "TFT_DC", "TFT_RES", "TFT_CS1", "TFT_CS2", "BUZZER", "PIXEL_DATA",
            "EXP_SDA", "EXP_SCL", "EXP_INT"]
    pin_of = {v: k for k, v in TEENSY.items()}
    b += f'<rect x="60" y="56" width="200" height="{len(sigs) * 24 + 24}" rx="5" fill="var(--pcb)" stroke="var(--pcb-edge)" stroke-width="2"/>'
    ty = {}
    for i, s in enumerate(sigs):
        y = 86 + i * 24
        ty[s] = y
        b += text(74, y + 4, f"D{pin_of[s]}", 10.5, "var(--silk-dim)") + text(112, y + 4, s, 10.5) + dot(260, y, SIGCOL[s])
    devs = [
        ("TFT 1 · 3.5″ DFR0669", [("SCLK", "TFT_SCK"), ("MOSI", "TFT_MOSI"), ("DC", "TFT_DC"),
                                   ("RES", "TFT_RES"), ("CS", "TFT_CS1"), ("VCC", "3V3"), ("BL  (tie to VCC)", "3V3"), ("GND", "GND")]),
        ("TFT 2 · 3.5″ DFR0669", [("SCLK", "TFT_SCK"), ("MOSI", "TFT_MOSI"), ("DC", "TFT_DC"),
                                   ("RES", "TFT_RES"), ("CS", "TFT_CS2"), ("VCC", "3V3"), ("BL  (tie to VCC)", "3V3"), ("GND", "GND")]),
        ("BUZZER MODULE · low-level trigger", [("I/O", "BUZZER"), ("VCC", "3V3"), ("GND", "GND")]),
        ("74AHCT125 LEVEL SHIFTER", [("1A  (input)", "PIXEL_DATA"), ("1OE", "GND"), ("VCC", "5V"), ("GND", "GND"),
                                      ("1Y  → 330 Ω → LS 17", None)]),
        ("DB25 LS · to the switch panel", [("pin 10  SDA  (4.7 kΩ to 3V3)", "EXP_SDA"), ("pin 11  SCL  (4.7 kΩ to 3V3)", "EXP_SCL"),
                                            ("pin 12  INT", "EXP_INT"), ("pin 2  3V3", "3V3")]),
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
    b += text(60, y + 24, "⚠ TFT VCC on 3V3: the modules take 3.3-5.5 V (about 50 mA each) but state no logic level. MISO, touch and SD stay unconnected.", 9.5, "var(--wire-warn)")
    b += text(60, y + 40, "⚠ The buzzer module must run from 3V3: at 5 V its transistor may not switch off.", 9.5, "var(--wire-warn)")
    return figure(svg(1100, y + 64, "Middle strip: Teensy to the TFT displays, buzzer module and level shifter", b),
                  "The two TFT displays share the SPI clock, data, DC and reset lines and have a chip-select each. The pixel "
                  "chain starts at the level shifter: its output goes through a 330&ndash;470 &Omega; resistor to "
                  "the left strip (LS pin 17), comes back on LS pin 18 into the 32 fuel-bar pixels here, and leaves "
                  "for the right strip on RS pin 17.")


# ---- diagram 6: power -------------------------------------------------------------------------------------
def d_power():
    b = pill(20, 50, 170, "5 V 4 A wall adapter", "orange") + line(190, 50, 230, 50, "orange", 4)
    b += pill(230, 50, 140, "DC jack, 12 mm", "orange") + line(370, 50, 400, 50, "orange", 4)
    b += pill(400, 50, 130, "master switch", "orange") + line(530, 50, 560, 50, "orange", 4)
    b += pill(560, 50, 80, "fuse", "orange") + line(640, 50, 690, 50, "orange", 4)
    b += box(690, 18, 190, 64, "5 V RAIL", "1000 µF across it")
    b += text(930, 106, "everything below is fed from the rail", 10.5, "var(--silk-dim)")
    outs = [("Left strip pixels", "LS 20, 21"), ("Right strip pixels", "RS 20, 21"),
            ("Left wing: fader driver", "LW 20, 21"), ("32 fuel pixels (middle)", "direct, short wire"),
            ("74AHCT125 level shifter", "direct")]
    for i, (n, t) in enumerate(outs):
        y = 130 + i * 40
        b += path([(880, 50), (910, 50), (910, y), (930, y)], "orange") + pill(930, y, 190, n, "orange", size=10)
        b += text(1130, y + 4, t, 10, "var(--silk-dim)")
    b += text(40, 150, "Teensy: USB only.", 11, "var(--wire-power)")
    b += text(40, 170, "Never connect the 5 V rail to the", 10, "var(--silk-dim)")
    b += text(40, 184, "Teensy's VIN while USB is plugged in.", 10, "var(--silk-dim)")
    b += pill(40, 230, 46, "GND", "black") + text(96, 234, "one ground, shared by the adapter, the Teensy and every piece", 10, "var(--silk-dim)")
    b += pill(40, 262, 46, "3V3", "red") + text(96, 266, "from the Teensy only: pots, buzzer module, TFTs and the expander", 10, "var(--silk-dim)")
    return figure(svg(1300, 330, "Power: adapter, jack, master switch, fuse and rail, feeding the pixels, level shifter and fader driver", b),
                  "The Teensy takes power over USB; the 5 V adapter feeds only the pixels, the level shifter and the fader "
                  "driver, with its ground joined to the Teensy's. The master switch cuts the 5 V rail only, so the Teensy and the "
                  "expander stay alive. Size the fuse just above the capped load (about 3&ndash;4 A) and cap brightness in firmware.")


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


COLOUR_ROWS = None


def t_colours():
    global COLOUR_ROWS
    items = [
        ("3V3", "red", "pots, buzzer module and TFTs: from the Teensy"), ("5V", "orange", "pixels, level shifter, fader driver"),
        ("GND", "black", "everything; drawn with a light edge so it shows"),
        ("Stick X / Y / twist", "purple", "X purple, Y grey, twist brown: both sticks"),
        ("Fader wiper", "green", ""), ("Fader touch, every push switch and toggle", "white", "to ground"),
        ("Encoder A / B", "blue", "A blue, B yellow"), ("Fader PWM A / B", "pink", "A pink, B teal"),
        ("Matrix rows / columns", "green", "rows green, columns blue"), ("Pixel data", "pink", "in and out"),
        ("TFT SCLK / MOSI / DC / RES / CS", "yellow", "yellow, blue, grey, teal, green (CS2 purple)"),
        ("Buzzer I/O", "brown", ""), ("Expander SDA / SCL / INT", "purple", "SDA purple, SCL grey, INT teal"),
    ]
    COLOUR_ROWS = items
    rows = "".join(f"<tr><td>{e(n)}</td><td>{swatch(c)}{c}</td><td class=\"note\">{e(t)}</td></tr>" for n, c, t in items)
    return ('<div class="table-wrap"><table><thead><tr><th>Signal</th><th>Colour</th><th>Note</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


LEGEND = [("red", "3V3"), ("orange", "5 V"), ("black", "GND"), ("purple", "stick X"), ("grey", "stick Y, TFT DC"),
          ("brown", "stick twist, buzzer"), ("green", "fader wiper, matrix rows"), ("blue", "encoder A, matrix columns"),
          ("yellow", "encoder B, DB25 cables"), ("white", "switches and fader touch"), ("pink", "fader PWM A, pixel data"),
          ("teal", "fader PWM B, TFT reset")]


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
         '<p class="subtitle">Every pin in use, drawn from <code>hardware/electronics/wiring/pin-map.md</code>. Nothing is built yet and none of '
         "this has been checked against real hardware: treat it as the plan to wire from, and correct it when a part "
         "turns out different. Generated by <code>tools/gen_wiring.py</code>; the same data is in "
         "<code>hardware/electronics/wiring/pin-map.md</code>.</p>",
         "<h2>The five pieces</h2>", d_overview(), legend(),
         "<h2>Teensy 4.1</h2>", d_teensy(),
         "<h2>The four DB25 ports</h2>", d_db25()]
    p.append("<h2>Inside each piece</h2>")
    for name, fig in d_pieces():
        p.append(f"<h3>{e(name)}</h3>{fig}")
    p += ["<h3>Switch panel</h3>", d_switch_panel(), "<h3>Strip middle</h3>", d_middle(), "<h2>Power</h2>", d_power(),
          "<h2>Wire colours</h2>",
          '<p class="note" style="margin-top:14px;max-width:72ch">The same signal is the same colour at both ends of '
          "its wire. Red is always 3V3, black is always GND, orange is always 5 V. A colour can repeat when the wires "
          "never sit side by side, and inside a piece the pin labels settle which is which.</p>",
          t_colours(), "<h2>Teensy pins</h2>", t_teensy(),
          "<footer><strong>Wiring order:</strong> ground and power first. Check every ground and the 5 V rail with a "
          "multimeter, with nothing plugged in, before connecting a device. Then the Teensy side of each port, then "
          "each outer piece one at a time. The full checklist is in <code>hardware/electronics/wiring/wiring-checklist.md</code>.</footer>"]
    return "\n".join(p)



# ---- hardware/electronics/wiring/pin-map.md (generated, so it cannot drift from the diagrams) --------------------------------
OUTPUTS = {"PIXEL_DATA", "TFT_RES", "TFT_CS1", "TFT_CS2", "TFT_MOSI", "TFT_DC", "TFT_SCK", "BUZZER",
           "FADER_PWM_A", "FADER_PWM_B", "ROW0", "ROW1", "ROW2", "ROW3"}
ANALOG_SIGS = {"L_STICK_X", "L_STICK_Y", "L_STICK_Z", "R_STICK_X", "R_STICK_Y", "R_STICK_Z", "FADER_WIPER"}


def direction(sig):
    if sig in OUTPUTS:
        return "out"
    if sig in ANALOG_SIGS:
        return "analog"
    if sig in ("EXP_SDA", "EXP_SCL"):
        return "I2C, 4.7 kΩ pull-up to 3V3"
    if sig == "FADER_TOUCH":
        return "in (FastTouch)"
    return "in, pull-up"


def piece_of(sig):
    if sig.startswith("COL"):
        return "both strips"
    if sig in ("ROW0", "ROW1"):
        return "left strip"
    if sig in ("ROW2", "ROW3"):
        return "right strip"
    if sig.startswith("EXP_"):
        return "left strip, switch panel expander"
    if sig in MID_DEST:
        return "middle strip"
    hits = [k for k, (_, pins) in PORTS.items() if sig in pins.values()]
    return {"LW": "left wing", "RW": "right wing"}.get(hits[0], "strip") if hits else "?"


def pinmap_md():
    t = ["| Pin | Signal | Direction | Piece |", "|---|---|---|---|"]
    for pin in sorted(TEENSY):
        sig = TEENSY[pin]
        a = f" ({ANALOG[pin]})" if pin in ANALOG else ""
        t.append(f"| {pin}{a} | {sig} | {direction(sig)} | {piece_of(sig)} |")
    teensy_table = "\n".join(t)
    heads = " | ".join(PORTS[k][0].title() for k in PORTS)
    d = [f"| Pin | {heads} |", "|---|---|---|---|---|"]
    for pin in range(1, 26):
        cells = []
        for k in PORTS:
            sig = PORTS[k][1].get(pin)
            cells.append(sig if sig else "open")
        d.append(f"| {pin} | " + " | ".join(cells) + " |")
    d.append("| **Conductors** | " + " | ".join(str(len(PORTS[k][1])) for k in PORTS) + " |")
    db25_table = "\n".join(d)
    return PINMAP_TEMPLATE.replace("@TEENSY@", teensy_table).replace("@DB25@", db25_table)


PINMAP_TEMPLATE = """# Pin map and cabling (draft, five-piece layout)

Teensy 4.1 pin assignment, the cabling between the five pieces, and the four DB25 pinouts. Matches
`hardware/cad/console.scad`. **This file is generated by `tools/gen_wiring.py`, the same script that draws
the diagrams in [wiring.md](wiring.md) (renders on GitHub) and [pinout.html](../../../docs/pinout.html) (for a browser).
Edit the data in the script, not this file.** Draft: nothing is built yet. Context is in `docs/design/decisions.md` and
`hardware/sourcing/parts-list.md`.

## Topology

```
                         LEFT WING                          RIGHT WING
                         stick, fader, enc                  stick, 2 enc
                              |  DB25 (19)                       |  DB25 (14)
                              |                                  |
   STRIP LEFT  --DB25 (21)--  STRIP MIDDLE  --DB25 (16)--  STRIP RIGHT
   12 nav keys                Teensy, 2 TFTs, 32 fuel         12 action-group keys
   switch panel + expander    pixels, buzzer, master switch,   annunciator
   12 pixels                  power jack                       21 pixels
                              (5 V in, fuse, 1000 uF)
```

- The **middle strip** holds the Teensy, the 5 V input, the 74AHCT125 and the TFT displays and buzzer. It has four DB25
  jacks, one per outer piece.
- The **left strip** carries a **switch panel**: 16 inputs on one MCP23017 I2C expander that sits right behind
  the panel. The inputs wire locally, so only SDA, SCL, the interrupt and 3V3 cross the cable. The inputs are
  the guarded ABORT toggle, a key switch that arms STAGE, a big STAGE button, throttle FULL and CUT, MAP, focus
  previous and next, quicksave, quickload, precision, pause, UI hide, a guarded ENGAGE / DISENGAGE toggle and two spares.
- The **right strip** carries a 3 x 3 **annunciator**: one pixel behind each of nine windows.
- The two **wings** sit in front of the outer strip pieces, so their jacks are on the wings' outer end walls. The
  strip pieces and the middle strip have their jacks on their back walls. Every cable runs outside, behind the console
  (the middle strip has the four female jacks in two rows). About 0.6 m of path for a wing cable, so a 1 m cable has slack.
- **Pixels are one chain of 65** on a single data pin: left strip (12 key pixels), then the 32 fuel bars in the
  middle, then the right strip (12 key pixels and 9 annunciator pixels). The data goes out to the left strip on
  pin 17, comes back on pin 18, runs through the fuel bars, and leaves for the right strip on pin 17 of that
  port. Put the 330-470 ohm series resistor at the first pixel (in the left strip). If a strip cable is
  unplugged, every pixel after it goes dark.
- **Keys are one 4 x 6 matrix** split across the strips: the left strip carries rows 0-1 and the right
  strip rows 2-3. Both carry all six column lines, which are paralleled in the middle piece. STAGE is no longer
  a matrix key: its slot is AG9.

## Constraints that shaped it

- All 3.3 V, none of the pins are 5 V tolerant. Analog inputs must stay at or below 3.3 V.
- Only header pins 0-41 are used. Pins 42 and up are bottom pads.
- **Pin 1** is the pixel data output: Serial1 TX, supported by the WS2812Serial library (non-blocking, DMA).
  It goes to the 74AHCT125 level shifter.
- **Pins 2 and 3** are the fader PWM pair: both are on timer FlexPWM4.2, so they share one frequency
  (default 4.482 kHz, changeable with `analogWriteFrequency`).
- **Pins 18 and 19** are the Teensy's I2C pins (SDA, SCL), used for the switch-panel expander. Fit 4.7 kΩ
  pull-ups to 3V3 at the Teensy end.
- **Pin 13** has the on-board LED and is the SPI clock for the TFT displays. **Pin 12** is MISO on SPI0 but is a
  plain GPIO here (TFT DC), because the displays are write-only.
- Analog inputs are pins 14-27 and 38-41; the seven used are 14-17 and 20-22.
- The 3.3 V regulator is good for about 250 mA external. The pots and the expander draw almost nothing.
- The matrix is read by driving a row low and reading the columns with pull-ups. **Leave the other rows
  as inputs (high impedance), never driven high**, so a stray short cannot fight a driven pin.

## Teensy 4.1 assignment

@TEENSY@

All 42 header pins are used. Any further switch goes on the expander (16 inputs, all assigned including 3
spares) or a second MCP23017 at another address.

## Switch-panel expander

MCP23017-E/SP (DIP-28), hand-wired on perfboard behind the panel. Address pins A0-A2 tied to GND (address 0x20), RESET
through 10 kΩ to 3V3, 0.1 uF across its supply. Mirror both interrupt ports onto INTA. Internal pull-ups on, the other
leg of every switch to GND.

| Expander pin | Input |
|---|---|
| PA0 | ABORT (guarded toggle) |
| PA1 | STAGE KEY (key switch: STAGE only works while it is on) |
| PA2 | STAGE (big button) |
| PA3 | THROTTLE FULL |
| PA4 | THROTTLE CUT |
| PA5 | MAP |
| PA6 | FOCUS PREVIOUS |
| PA7 | FOCUS NEXT |
| PB0 | QUICKSAVE |
| PB1 | QUICKLOAD |
| PB2 | PRECISION |
| PB3 | PAUSE |
| PB4 | UI HIDE |
| PB5 | ENGAGE / DISENGAGE (guarded toggle: sticks and throttle live or ignored) |
| PB6-PB7 | spare |

MAP, quicksave, quickload and the rest go to the game as key presses through Simpit's keyboard emulator
(Windows only). FULL and CUT drive the throttle, and the motorised fader follows through the throttle command
Simpit sends back. ENGAGE / DISENGAGE is a controls-live interlock: disengaged, the firmware sends zero rotation and
translation (so SAS and the game keep control) and stops sending throttle; the annunciator's CONTROLS window lights
while engaged. Check how Simpit hands the throttle back (its changelog mentions throttle authority being released).

## DB25 pinouts

Standard DB25 numbering, pins 1-13 on the wide row and 14-25 on the other. The outer pieces have male jacks and the
middle strip female jacks, joined by female-to-male cables, but all four middle jacks are alike, so a cable can still go
in the wrong middle port. The pins are laid out so that is **harmless**:

- Ground is on pins 1, 7, 13, 24, 25 on every port.
- 3.3 V (pin 2) is provided on the two wing ports and the left-strip port. 5 V (pins 20, 21) is provided on the
  left-wing and both strip ports.
- Everything the Teensy **drives** sits on pins 15-23 only: matrix rows and pixel data on pins 15-17 of the
  strip ports, fader PWM on pins 22 and 23 of the left-wing port. Pins that are not used by a module are left
  open, never wired to something else. So a module never connects a switch, a wiper or a ground to a pin the
  Teensy drives.
- SDA and SCL (pins 10 and 11 of the left-strip port) are weak pulled-up open-drain lines, so a switch pulling
  them low on another cable only upsets the bus, it cannot damage anything.
- A script check (all 16 combinations of module and port) found no conflict, only wrong behaviour.

@DB25@

Notes:
- Analog lines (stick X, Y, twist and the fader wiper) sit between ground pins so they are not neighbours of
  digital lines. Put a 0.1 uF capacitor from each wiper to ground at the Teensy end.
- **Cable shield:** ground it to the connector shell at the middle end only, to avoid a ground loop.
- **Pixel power:** each strip piece takes 5 V on pins 20 and 21 (two conductors, up to about 1.3 A worst case
  for 21 pixels on the right strip). The 32 fuel-bar pixels are in the middle piece and are fed straight from the
  5 V rail. A 100 uF capacitor across 5 V in each strip piece is optional.
- **Left wing:** the L9110H fader driver is in the wing next to the motor, so only the two PWM lines and 5 V
  cross the cable. Pots take 3V3 on pin 2, never 5 V.
- **Cables:** a wing cable runs from the wing's end wall round the back to the middle strip, about 0.6 m of path. The
  strip-to-middle cables are about 0.3 m. All four are 1 m, so coil the slack. Keep analog and I2C runs short.

## Open

- **Cable management** behind the console (clips or a cable channel, strain relief): not designed.
- **I2C over the cable:** about 30 cm at 400 kHz with 4.7 kΩ pull-ups should be fine; not tested.
- **TFT modules (DFR0669):** the wiki gives a 3.3-5.5 V supply and about 48 mA each, but no logic level. They are wired to 3V3
  here (about 100 mA for both, within the Teensy's 3.3 V regulator). Check the SPI lines before moving them to 5 V. Not verified.
- **Pixel chain through cables:** a break in the chain (an unplugged strip cable) kills the pixels after it.
  Fine for a build, worth knowing when debugging.
- **HIGH G** annunciator window dropped: Simpit has no G-force message.
- **Confirm the physical Teensy pin positions** before wiring: this map uses pin numbers only.
- **DB25 jack cutouts** are not in the mockup yet.
"""

FIG_NAMES = ["overview", "teensy", "db25", "left-wing", "right-wing", "strip-left", "strip-right",
             "switch-panel", "strip-middle", "power"]
FIG_TITLES = ["The five pieces", "Teensy 4.1", "The four DB25 ports", "Left wing", "Right wing", "Strip left",
              "Strip right", "Switch panel", "Strip middle", "Power"]
SVG_VARS = ("--pcb:#123d2e;--pcb-edge:#1f5c45;--silk:#eef1ea;--silk-dim:#8fa097;--wire-power:#d9a35f;"
            "--wire-gnd:#7b8a82;--wire-warn:#e2666a;--c-red:#e5484d;--c-black:#161a18;--c-white:#f4f4f4;"
            "--c-blue:#3b82f6;--c-yellow:#eab308;--c-green:#22c55e;--c-orange:#f97316;--c-brown:#a35a2a;"
            "--c-purple:#a855f7;--c-grey:#9ca3af;--c-pink:#ec4899;--c-teal:#14b8a6;")


def standalone(svg_text):
    """A self-contained .svg: namespace, the colour variables, and the dark panel as a background rectangle."""
    import re
    m = re.search(r'viewBox="([\d.\- ]+)"', svg_text)
    x, y, w, h = (float(v) for v in m.group(1).split())
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{m.group(1)}" width="{int(w)}" height="{int(h)}" '
            f'font-family="IBM Plex Mono, DejaVu Sans Mono, monospace">'
            f'<style>svg{{{SVG_VARS}}}</style><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0c1210"/>')
    body = svg_text.split(">", 1)[1]                       # drop the original opening <svg ...> tag
    return head + body


def markdown():
    md = ["# Wiring diagrams", "",
          "Colour-coded wiring for the five-piece console, in the same style as the goodnight-device diagrams. "
          "Nothing is built yet and none of this has been checked on real hardware: treat it as the plan to wire from. "
          "The pin tables are in [pin-map.md](pin-map.md), the checklist in [wiring-checklist.md](wiring-checklist.md), "
          "and [pinout.html](../../../docs/pinout.html) is the same page for a browser. Generated by "
          "`tools/gen_wiring.py`.", ""]
    for name, title, (_, cap) in zip(FIG_NAMES, FIG_TITLES, FIGS):
        md += [f"## {title}", "", f"![{title}](diagrams/{name}.svg)", "", cap, ""]
    md += ["## Wire colours", "", "The same signal is the same colour at both ends of its wire. Red is always 3V3, "
           "black is always GND, orange is always 5 V.", "", "| Signal | Colour | Note |", "|---|---|---|"]
    for n, c, t in COLOUR_ROWS:
        md.append(f"| {n} | {c} | {t} |")
    md += ["", "## Teensy pins", "", "| Teensy pin | Signal | Goes to |", "|---|---|---|"]
    for pin in sorted(TEENSY):
        a = f" ({ANALOG[pin]})" if pin in ANALOG else ""
        md.append(f"| {pin}{a} | {TEENSY[pin]} | {dest(TEENSY[pin])} |")
    return "\n".join(md) + "\n"


def pins_h():
    """C++ header with one constant per Teensy pin, so the firmware cannot drift from the wiring docs."""
    singles = {sig: pin for pin, sig in sorted(TEENSY.items()) if not (sig.startswith("ROW") or sig.startswith("COL"))}
    rows = [pin for pin, sig in sorted(TEENSY.items()) if sig.startswith("ROW")]
    cols = [pin for pin, sig in sorted(TEENSY.items()) if sig.startswith("COL")]
    out = ["// Generated by tools/gen_wiring.py from hardware/electronics/pinmap.json. Do not edit by hand.",
           "// Teensy 4.1 pin assignment. Matches hardware/electronics/wiring/pin-map.md.", "#pragma once", "#include <stdint.h>", "",
           "namespace pin {"]
    width = max(len(n) for n in singles) + 1
    for sig, pin in singles.items():
        a = f"  // {ANALOG[pin]}" if pin in ANALOG else ""
        out.append(f"constexpr uint8_t {sig + ' ':<{width}}= {pin};{a}")
    out += ["", "// key matrix: rows are driven, columns are read",
            f"constexpr uint8_t ROWS[] = {{{', '.join(map(str, rows))}}};",
            f"constexpr uint8_t COLS[] = {{{', '.join(map(str, cols))}}};", "}  // namespace pin", ""]
    return "\n".join(out)


if __name__ == "__main__":
    out = page()
    for chunk in out.split("<svg")[1:]:                      # every diagram must be well-formed XML
        xml.dom.minidom.parseString("<svg" + chunk.split("</svg>")[0] + "</svg>")
    open(OUT, "w").write(out)
    print("wrote", OUT, len(out), "bytes")
    ddir = os.path.join(WIRING_DIR, "diagrams")
    os.makedirs(ddir, exist_ok=True)
    os.makedirs(os.path.dirname(PINS_H), exist_ok=True)
    assert len(FIGS) == len(FIG_NAMES), (len(FIGS), len(FIG_NAMES))
    for name, (svg_text, _) in zip(FIG_NAMES, FIGS):
        xml.dom.minidom.parseString(standalone(svg_text))
        open(os.path.join(ddir, name + ".svg"), "w").write(standalone(svg_text))
    open(os.path.join(WIRING_DIR, "wiring.md"), "w").write(markdown())
    open(os.path.join(WIRING_DIR, "pin-map.md"), "w").write(pinmap_md())
    open(PINS_H, "w").write(pins_h())
    print("wrote", len(FIGS), "svg files, wiring.md, pin-map.md and", os.path.relpath(PINS_H, REPO))
