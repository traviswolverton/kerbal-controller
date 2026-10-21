#!/usr/bin/env bash
# Regenerate the console renders in hardware/mockup/renders/ from console.scad. Needs openscad and xvfb-run.
# Camera is "centre x,y,z, rotation x,y,z, distance". Run from anywhere:  bash hardware/cad/render.sh   (or: make renders)
set -euo pipefail
cd "$(dirname "$0")"
OUT=../mockup/renders
mkdir -p "$OUT"
r() {   # name, camera, then any extra openscad arguments
  local name=$1 cam=$2 size=$3; shift 3
  xvfb-run -a openscad -o "$OUT/$name.png" --imgsize="$size" --projection=p --camera="$cam" "$@" console.scad 2>&1 | grep -iE "ERROR:" || true
  echo "wrote $OUT/$name.png"
}
r iso            "350,150,45,62,0,20,1400"   1800,900
r top            "350,150,40,0,0,0,1300"     1800,900
r front          "350,150,60,90,0,0,1550"    1800,900
r rear           "350,150,60,90,0,180,1550"  1800,900
r side           "350,150,60,90,0,90,1100"   1800,900
r seat-view      "350,-400,450,350,150,50"   1800,900
r wing-cutaway   "110,88,30,60,0,60,620"     1600,900 -D mod=0 -D cut_x=120
r strip-cutaway  "110,236,60,60,0,60,640"    1600,900 -D mod=2 -D cut_x=130
