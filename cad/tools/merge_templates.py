#!/usr/bin/env python3
"""Merge the OpenSCAD 'cuts' and 'notes' SVG layers into one 1:1 template per module."""
import re
import sys

src, out = sys.argv[1], sys.argv[2]
names = ["left", "center", "right"]
W = [220, 240, 220]
D = 245
M = 10  # paper margin around the panel, mm


def paths(fn):
    s = open(fn).read()
    return re.findall(r"<path\b.*?/>", s, flags=re.S)


for i, n in enumerate(names):
    cuts = paths(f"{src}/m{i}_cuts.svg")
    notes = paths(f"{src}/m{i}_notes.svg")

    def style(p, fill, stroke, sw):
        p = re.sub(r'\s(fill|stroke|stroke-width|fill-rule)="[^"]*"', "", p)
        return p.replace("<path", f'<path fill="{fill}" fill-rule="evenodd" stroke="{stroke}" stroke-width="{sw}"', 1)

    w, h = W[i] + 2 * M, D + 2 * M
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
        f'viewBox="{-M} {-D - M} {w} {h}">'
        f'<rect x="{-M}" y="{-D - M}" width="{w}" height="{h}" fill="#fff"/>'
        + "".join(style(p, "#eef1f4", "#000", 0.3) for p in cuts)
        + "".join(style(p, "#1f4e9c", "#1f4e9c", 0.05) for p in notes)
        + "</svg>"
    )
    open(f"{out}/{n}-panel-template.svg", "w").write(svg)
    html = (
        f"<html><head><style>@page{{size:{w}mm {h}mm;margin:0}}"
        f"html,body{{margin:0;padding:0}}svg{{display:block}}</style></head><body>{svg}</body></html>"
    )
    open(f"{out}/{n}.html", "w").write(html)
    print("wrote", n, w, "x", h, "mm")
