// Kerbal controller - full console mockup, layout v0 (a proposal to react to)
//
// Three tilted wedge modules side by side: LEFT (translation + throttle),
// CENTER (key bank, toggles, displays, fuel bars) and RIGHT (rotation).
// Panel coordinates: u across the module from its left edge, v away from you
// from the front edge, both in mm. All three modules are 245 mm deep, so each
// prints on a 256 mm bed.
//
// PROVISIONAL numbers are marked. The joystick flange and mounting holes are
// NOT known yet (the seller drawing is a side view); the stick cutout below is
// a placeholder to be replaced after measuring the real unit.
//
// 3D render:   openscad -o out.png --imgsize=1600,800 --projection=p \
//                       --camera=cx,cy,cz,rx,ry,rz,dist console_mockup.scad
// Templates:   openscad -D 'flat=true' -D 'mod=0' -D 'layer="cuts"'  -o left_cuts.svg  console_mockup.scad
//              openscad -D 'flat=true' -D 'mod=0' -D 'layer="notes"' -o left_notes.svg console_mockup.scad
//              (mod 0 = left, 1 = center, 2 = right)

flat  = false;     // true: 2D 1:1 template of one module
mod   = -1;        // 3D: -1 = all modules; flat: 0, 1 or 2
layer = "cuts";    // flat only: "cuts" or "notes"

// ---- enclosure --------------------------------------------------------
tilt_m  = [12, 28, 12];   // panel tilt toward you per module, degrees (center is steeper so
                          // the pixels above the keys stay visible past the keycaps)
fh_m    = [45, 30, 45];   // height of each module's front edge above the desk
D       = 245;     // panel depth (fits a 256 mm bed)
W       = [220, 240, 220];
x_off   = [0, 220, 460];
mod_names = ["LEFT: translation + throttle", "CENTER: keys, displays", "RIGHT: rotation"];

// ---- shared sizes -----------------------------------------------------
cut_mx     = 14.0;   // MX plate cutout (tune after the test plate)
window_d   = 6.5;    // light window above each pixel
pitch_c    = 19.05;  // key column pitch
pitch_r    = 36.0;   // key row pitch (layout B, revised from 30: pixels were hidden behind the keycaps)

// ---- LEFT module layout ----------------------------------------------
fader_u   = 30;      // motorised fader (Adafruit 5466), pull toward you = less throttle
fader_v0  = 50;      // v of 0 %
fader_len = 100;     // travel
fader_body = [17.2, 146.5, 26];   // face width, length, depth below the panel (from the Soundwell drawing)
fader_hole_span = 120;            // two M3 threaded holes in the face, on the slot axis
nubbin    = [11, 26, 10];         // conductive knob (Adafruit 5741): across, along travel, height
ghost_strip = false; // 8 pixels beside the fader; not needed now the fader is motorised
ghost_u   = 52;      // ghost strip position
stick_l   = [140, 95];
enc_l     = [[190, 165]];
enc_l_lbl = ["TIME WARP"];

// ---- RIGHT module layout ---------------------------------------------
stick_r   = [105, 95];
enc_r     = [[185, 150], [185, 205]];
enc_r_lbl = ["CAMERA", "PAGE"];

// ---- CENTER module layout --------------------------------------------
key_u0    = 12;      // left edge of the key block
key_v0    = 14;      // front edge of the key block
// rows listed back (row 0) to front (row 3)
key_lbl = [
  ["STAB","PRO","RETRO","NORM","A-NRM","MNVR"],
  ["RAD-IN","RAD-OUT","TGT","A-TGT","SAS","RCS"],
  ["GEAR","LIGHT","BRAKE","AG1","AG2","AG3"],
  ["AG4","AG5","AG6","AG7","AG8","STAGE"]
];
function key_u(c) = key_u0 + 9.525 + c * pitch_c;
function key_v(r) = key_v0 + (3 - r) * pitch_r + 9.525;   // r = 0 is the back row
toggles   = [[165, 35], [205, 35], [165, 95], [205, 95]];
tog_lbl   = ["ABORT", "STAGE ARM", "SPARE", "SPARE"];
oled_pos  = [[45, 195], [115, 195]];  // 58 x 31 windows
bar_u     = [165, 179, 193, 207];     // 4 fuel bars of 8 pixels
bar_lbl   = ["LF", "OX", "MONO", "EC"];
bar_v0    = 150;
bar_pitch = 11.5;
buzzer    = [30, 225];

// ---- provisional joystick (JH-D400X-R4) ------------------------------
stick_cut    = [52, 42];   // PROVISIONAL cutout, 49.6 wide incl. Y pot bump
stick_flange = [62, 62];   // PROVISIONAL flange outline
stick_clear  = 38;         // estimated tilt sweep radius of the grip edge
stick_h      = 58.5;       // top of grip above the panel
stick_grip   = [35, 42];   // grip diameter, height
stick_btn    = 10.5;

// ---- placement and primitives ----------------------------------------
// $m is the module being built (set in module3d); tilt and front height are per module
function T()  = tilt_m[$m];
function FH() = fh_m[$m];
module place(u, v) {
    if (flat) translate([u, v, 0]) children();
    else translate([u, v * cos(T()), FH() + v * sin(T())])
         rotate([T(), 0, 0]) children();
}
module hole_round(d) {
    if (flat) circle(d = d, $fn = 48);
    else translate([0, 0, -40]) cylinder(d = d, h = 42, $fn = 48);
}
module hole_rect(w, h) {
    if (flat) square([w, h], center = true);
    else translate([-w / 2, -h / 2, -40]) cube([w, h, 42]);
}

module wedge(w) {
    rotate([90, 0, 90]) linear_extrude(height = w)
        polygon([[0, 0], [D * cos(T()), 0],
                 [D * cos(T()), FH() + D * sin(T())], [0, FH()]]);
}

// ---- cut geometry (shared by 3D holes and 2D templates) ---------------
module cuts(i) {
    if (i == 0) {
        place(fader_u, fader_v0 + fader_len / 2) hole_rect(6, fader_len + 12);
        for (s = [-1, 1]) place(fader_u, fader_v0 + fader_len / 2 + s * fader_hole_span / 2) hole_round(3.4);
        if (ghost_strip) for (k = [0 : 7]) place(ghost_u, fader_v0 + k * fader_len / 7) hole_round(window_d);
        place(stick_l[0], stick_l[1]) hole_rect(stick_cut[0], stick_cut[1]);
        for (p = enc_l) place(p[0], p[1]) hole_round(7);
    } else if (i == 1) {
        for (r = [0 : 3], c = [0 : 5]) {
            place(key_u(c), key_v(r)) hole_rect(cut_mx, cut_mx);
            place(key_u(c), key_v(r) + pitch_r / 2) hole_round(window_d);
        }
        for (p = toggles) place(p[0], p[1]) hole_round(12.2);
        for (p = oled_pos) place(p[0], p[1]) hole_rect(58, 31);
        for (u = bar_u, k = [0 : 7]) place(u, bar_v0 + k * bar_pitch) hole_round(window_d);
        place(buzzer[0], buzzer[1]) hole_round(12);
    } else {
        place(stick_r[0], stick_r[1]) hole_rect(stick_cut[0], stick_cut[1]);
        for (p = enc_r) place(p[0], p[1]) hole_round(7);
    }
}

// ---- 3D proxies for the parts ----------------------------------------
module stick_proxy() {
    color("#555") translate([-stick_flange[0] / 2, -stick_flange[1] / 2, 0]) cube([stick_flange[0], stick_flange[1], 3]);
    color("#222") cylinder(d = 12, h = stick_h - stick_grip[1], $fn = 32);
    color("#333") translate([0, 0, stick_h - stick_grip[1]]) cylinder(d = stick_grip[0], h = stick_grip[1], $fn = 48);
    color("#c33") translate([0, 0, stick_h]) cylinder(d = 12, h = stick_btn, $fn = 32);
}
module encoder_proxy() color("#bbb") translate([0, 0, 2]) cylinder(d = 25, h = 15, $fn = 40);
module toggle_proxy() {
    color("#999") cylinder(d = 6, h = 20, $fn = 24);
    color("#c33") translate([-8, -6, 0]) cube([16, 12, 16]);
}
module key_proxy() {
    color("#222") translate([-7.8, -7.8, 0]) cube([15.6, 15.6, 5]);
    color("#e6e6e6") translate([-9, -9, 5.5]) cube([18, 18, 8]);
}
module glow(c = "#3c3") color(c) translate([0, 0, -0.2]) cylinder(d = window_d - 0.4, h = 0.6, $fn = 24);

module proxies(i) {
    if (i == 0) {
        place(fader_u, fader_v0 + 0.6 * fader_len) color("#c33")
            translate([-nubbin[0] / 2, -nubbin[1] / 2, 0]) cube(nubbin);
        if (ghost_strip) for (k = [0 : 7]) place(ghost_u, fader_v0 + k * fader_len / 7) glow(k < 5 ? "#3c3" : "#555");
        place(stick_l[0], stick_l[1]) stick_proxy();
        for (p = enc_l) place(p[0], p[1]) encoder_proxy();
    } else if (i == 1) {
        for (r = [0 : 3], c = [0 : 5]) {
            place(key_u(c), key_v(r)) key_proxy();
            place(key_u(c), key_v(r) + pitch_r / 2) glow(r == 0 && c == 1 ? "#39f" : "#3c3");
        }
        for (p = toggles) place(p[0], p[1]) toggle_proxy();
        for (p = oled_pos) {
            place(p[0], p[1]) color("#112244") translate([-29, -15.5, -0.1]) cube([58, 31, 0.4]);
            place(p[0], p[1]) color("#333") difference() {
                translate([-33, -20, 0]) cube([66, 40, 2]);
                translate([-29, -15.5, -1]) cube([58, 31, 4]);
            }
        }
        for (b = [0 : 3], k = [0 : 7])
            place(bar_u[b], bar_v0 + k * bar_pitch) glow(k < 6 - b ? (b == 3 ? "#fc0" : "#3c3") : "#555");
    } else {
        place(stick_r[0], stick_r[1]) stick_proxy();
        for (p = enc_r) place(p[0], p[1]) encoder_proxy();
    }
}

// ---- 2D annotations for the paper templates ---------------------------
module ring_sq(w, h, t = 0.5) difference() { square([w + t, h + t], center = true); square([w - t, h - t], center = true); }
module ring_c(r, t = 0.5) difference() { circle(r = r + t / 2, $fn = 96); circle(r = r - t / 2, $fn = 96); }
module cross(s = 4, t = 0.3) { square([s * 2, t], center = true); square([t, s * 2], center = true); }
module lbl(s, x = 0, y = 0, size = 3.5, halign = "center") translate([x, y]) text(s, size = size, halign = halign, valign = "center", font = "DejaVu Sans:style=Bold");

function key_text(s) = len(s) <= 4 ? 2.6 : len(s) <= 6 ? 2.2 : 1.9;   // label sits inside the 14 mm cutout

module notes(i) {
    // panel outline, front marker, scale bar
    translate([W[i] / 2, D / 2]) ring_sq(W[i], D, 0.8);
    // title, front marker and scale bar sit in the paper margin, outside the panel
    lbl(mod_names[i], W[i] / 2, D + 6, 5);
    lbl("FRONT (toward you)", W[i] - 8, -6, 3.2, "right");
    translate([8, -4]) { square([100, 0.6]); for (x = [0, 50, 100]) translate([x, 0]) square([0.6, 3]); }
    lbl("100 mm scale bar: measure it on your print", 8, -8.5, 2.8, "left");
    if (i == 0) {
        place(fader_u, fader_v0 + fader_len / 2) { cross(6); ring_sq(fader_body[0], fader_body[1]); }   // body outline under the panel
        for (s = [-1, 1]) translate([fader_u, fader_v0 + fader_len / 2 + s * fader_hole_span / 2]) cross(3);
        lbl("2x M3, 120 mm apart", fader_u + 8, fader_v0 + fader_len / 2 + fader_hole_span / 2, 2.6, "left");
        lbl("THROTTLE", fader_u, fader_v0 + fader_len + 28, 3.5);
        lbl("0%", fader_u + 12, fader_v0, 3); lbl("100%", fader_u + 12, fader_v0 + fader_len, 3);
        if (ghost_strip) translate([ghost_u, fader_v0 + 55]) lbl("ghost strip", 12, 0, 3, "left");
        translate(stick_l) { ring_sq(stick_flange[0], stick_flange[1]); ring_c(stick_clear); cross(6);
            lbl("PROVISIONAL", 0, -34, 3); lbl("L STICK: X/Y + twist Z", 0, -46, 3.2); }
        for (k = [0 : len(enc_l) - 1]) translate(enc_l[k]) { cross(5); lbl(enc_l_lbl[k], 0, -17, 3.2); }
    } else if (i == 1) {
        for (r = [0 : 3], c = [0 : 5]) translate([key_u(c), key_v(r)]) lbl(key_lbl[r][c], 0, 0, key_text(key_lbl[r][c]));
        for (k = [0 : len(toggles) - 1]) translate(toggles[k]) { cross(5); lbl(tog_lbl[k], 0, -14, 2.8); }
        for (k = [0 : 1]) translate(oled_pos[k]) { cross(5); lbl(str("OLED ", k + 1), 0, -24, 3); }
        for (b = [0 : 3]) translate([bar_u[b], bar_v0 - 9]) lbl(bar_lbl[b], 0, 0, 3);
        translate(buzzer) { cross(5); lbl("BUZZER", 0, -11, 3); }
    } else {
        translate(stick_r) { ring_sq(stick_flange[0], stick_flange[1]); ring_c(stick_clear); cross(6);
            lbl("PROVISIONAL", 0, -34, 3); lbl("R STICK: pitch/yaw + twist roll", 0, -46, 3.2); }
        for (k = [0 : len(enc_r) - 1]) translate(enc_r[k]) { cross(5); lbl(enc_r_lbl[k], 0, -17, 3.2); }
    }
}

// ---- top level --------------------------------------------------------
module module3d(i) {
    $m = i;
    translate([x_off[i], 0, 0]) {
        color("#2b2b2e") difference() { wedge(W[i]); cuts(i); }
        proxies(i);
    }
}

if (flat) {
    if (layer == "cuts") difference() { square([W[mod], D]); cuts(mod); }
    else notes(mod);
} else {
    for (i = [0 : 2]) if (mod < 0 || mod == i) module3d(i);
}
