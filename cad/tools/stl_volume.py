# Volume and PLA mass of the per-piece shell and faceplate STLs.
# Export first: for i in 0 1 2 3 4; do for p in shell plate; do
#   openscad -D mod=$i -D part="\"$p\"" -o DIR/p${i}_$p.stl cad/console_mockup_v1.scad; done; done
# Then: python3 cad/tools/stl_volume.py DIR
import re, sys
def vol(fn):
    t = open(fn).read()
    v = [tuple(map(float, m)) for m in re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", t)]
    tot = 0.0
    for k in range(0, len(v) - 2, 3):
        a, b, c = v[k], v[k+1], v[k+2]
        tot += (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])) / 6
    return abs(tot) / 1000   # cm3
d = sys.argv[1]; names = ["Left wing","Right wing","Strip left","Strip middle","Strip right"]
rho = 1.24; tg = 0
print(f"{'piece':13} {'shell cc':>9} {'shell g':>8} {'plate cc':>9} {'plate g':>8} {'total g':>8}")
for i, n in enumerate(names):
    s, p = vol(f"{d}/p{i}_shell.stl"), vol(f"{d}/p{i}_plate.stl")
    g = (s + p) * rho; tg += g
    print(f"{n:13} {s:9.0f} {s*rho:8.0f} {p:9.0f} {p*rho:8.0f} {g:8.0f}")
print(f"\nmodelled shells + plates: {tg/1000:.2f} kg PLA (walls 100% solid, no ribs or bosses)")
print(f"with +15% for ribs, bosses, ballast retainers: {tg*1.15/1000:.2f} kg")
