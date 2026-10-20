#!/usr/bin/env bash
# Regenerate the console mockup: 1:1 panel templates (SVG + PDF) and 3D renders (PNG).
# Needs: openscad, python3, chromium (for the PDFs), xvfb-run (for the PNG renders).
set -euo pipefail
cd "$(dirname "$0")"
OUT=../../../docs/archive/v0-mockup
TMP=$(mktemp -d)
if [ -z "${CHROME:-}" ]; then
  for c in chromium chromium-browser google-chrome /opt/pw-browsers/chromium-1194/chrome-linux/chrome; do
    if command -v "$c" >/dev/null 2>&1; then CHROME=$(command -v "$c"); break; fi
  done
fi
: "${CHROME:?set CHROME to a chromium/chrome binary}"
mkdir -p "$OUT/templates" "$OUT/renders"

# 1:1 templates
for m in 0 1 2; do
  for l in cuts notes; do
    openscad -D flat=true -D mod=$m -D "layer=\"$l\"" -o "$TMP/m${m}_$l.svg" console_mockup.scad
  done
done
python3 -I merge_templates.py "$TMP" "$OUT/templates"
for n in left center right; do
  "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$OUT/templates/$n-panel-template-1to1.pdf" "file://$OUT/templates/$n.html" >/dev/null 2>&1
  rm -f "$OUT/templates/$n.html"
done

# 3D renders: name, camera "cx,cy,cz,rx,ry,rz,dist"
render() {
  local name=$1 cam=$2; shift 2
  xvfb-run -a openscad -o "$OUT/renders/$name.png" --imgsize=1800,900 --projection=p \
    --camera="$cam" "$@" console_mockup.scad
}
render console-iso   "340,110,45,62,0,20,1050"
render console-top   "340,122,40,0,0,0,1100"
render console-front "340,120,60,90,0,0,1250"
render console-side-center "340,120,80,90,0,90,950" -D mod=1
# what you see from the seat: eye 450 mm above the desk, 400 mm in front of the console
render seat-view     "340,-400,450,340,120,50"
render seat-view-center-tilt12 "340,-400,450,340,120,50" -D 'tilt_m=[12,12,12]' -D 'fh_m=[45,45,45]'
rm -rf "$TMP"
echo "done: $OUT"
