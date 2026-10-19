// Kerbal controller - console mockup v1: five pieces (a proposal to react to)
//
// Modelled on the stepped layout of the reference builds: a raised, steep back STRIP of three
// pieces, and two lower WINGS at the front ends, with the middle front left open.
// Each piece is a printed shell with a removable 3 mm faceplate (shown dark).
//
//   piece 0  LEFT WING     translation stick, throttle fader, time-warp encoder
//   piece 1  RIGHT WING    rotation stick, camera and page encoders
//   piece 2  STRIP LEFT    12 navigation keys, ABORT and STAGE ARM toggles
//   piece 3  STRIP MIDDLE  2 OLEDs, 4 fuel bars, buzzer, Teensy and power jack inside
//   piece 4  STRIP RIGHT   12 action-group keys, 2 spare toggles
//
// Panel coordinates: u across the piece from its left edge, v away from you along the slope from
// its front edge, both in mm. Every piece fits a 256 mm print bed.
//
// 3D render: xvfb-run -a openscad -o out.png --imgsize=1800,900 --projection=p \
//              --camera=cx,cy,cz,rx,ry,rz,dist console_mockup_v1.scad
// 1:1 template of one piece:  openscad -D flat=true -D mod=0 -o left_wing.svg console_mockup_v1.scad

flat = false;      // true: 2D 1:1 cut template of one piece
mod  = -1;         // 3D: -1 = all pieces; flat: 0..4

// ---- the five pieces --------------------------------------------------
names   = ["LEFT WING", "RIGHT WING", "STRIP LEFT", "STRIP MIDDLE", "STRIP RIGHT"];
W       = [220, 220, 220, 240, 220];      // width of each piece
x_off   = [0, 460, 0, 220, 460];          // left edge, across the console
y_off   = [0, 0, 176, 176, 176];          // front edge, away from you (strip starts where the wings end)
tilt_m  = [12, 12, 28, 28, 28];           // panel tilt toward you, degrees
fh_m    = [30, 30, 65, 65, 65];           // height of the front edge above the desk
D_m     = [180, 180, 135, 135, 135];      // length of the panel along the slope
plate_t = 3;                              // removable faceplate thickness
hollow  = true;                           // shells are hollow: walls and floor, faceplate separate
wall    = 2.4;                            // shell wall and floor thickness
ballast = true;                           // 6 x 6 x 1/4 in steel plates in the wings (2 per wing)
cut_x   = -1;                             // >= 0: slice away everything beyond this x (local to the piece)
part    = "all";                          // "all", "shell" or "plate": one part for STL export (use with mod)
foot_d  = 20;                             // self-adhesive silicone foot diameter
steel   = [152.4, 152.4, 6.35];           // ballast plate

// ---- shared sizes -----------------------------------------------------
cut_mx   = 14.0;   // MX plate cutout
window_d = 6.5;    // light window above each pixel
pitch_c  = 19.05;  // key column pitch
pitch_r  = 36.0;   // key row pitch (pixel above each key stays visible past the keycap in front)

// ---- wings ------------------------------------------------------------
fader_u = 30;  fader_v0 = 45;  fader_len = 100;        // Adafruit 5466, 100 mm travel
fader_body = [17.2, 146.5, 26];  fader_hole_span = 120;
nubbin = [11, 26, 10];
stick_l = [140, 95];   stick_r = [105, 95];
enc_l = [[190, 140]];              enc_l_lbl = ["TIME WARP"];
enc_r = [[185, 55], [185, 120]];   enc_r_lbl = ["CAMERA", "PAGE"];

stick_cut = [52, 42];  stick_flange = [62, 62];        // PROVISIONAL, flange unmeasured
stick_clear = 38;  stick_h = 58.5;  stick_grip = [35, 42];  stick_btn = 10.5;

// ---- strip ------------------------------------------------------------
key_u0 = 12;  key_v0 = 30;
key_lbl_l = [["STAB","PRO","RETRO","NORM","A-NRM","MNVR"],
             ["RAD-IN","RAD-OUT","TGT","A-TGT","SAS","RCS"]];        // row 0 = back row
key_lbl_r = [["GEAR","LIGHT","BRAKE","AG1","AG2","AG3"],
             ["AG4","AG5","AG6","AG7","AG8","STAGE"]];
function key_u(c) = key_u0 + 9.525 + c * pitch_c;
function key_v(r) = key_v0 + (1 - r) * pitch_r + 9.525;
tog_l = [[175, 35], [175, 100]];  tog_l_lbl = ["ABORT", "STAGE ARM"];
tog_r = [[175, 35], [175, 100]];  tog_r_lbl = ["SPARE", "SPARE"];
oled_pos = [[50, 100], [120, 100]];                  // 58 x 31 windows
bar_u = [175, 189, 203, 217];  bar_v0 = 20;  bar_pitch = 11.5;   // 4 fuel bars of 8
bar_lbl = ["LF", "OX", "MONO", "EC"];
buzzer = [30, 45];

// ---- placement --------------------------------------------------------
function T()  = tilt_m[$m];
function FH() = fh_m[$m];
function DD() = D_m[$m];
module place(u, v) {
    if (flat) translate([u, v, 0]) children();
    else translate([u, v * cos(T()), FH() + v * sin(T())]) rotate([T(), 0, 0]) children();
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
        polygon([[0, 0], [DD() * cos(T()), 0],
                 [DD() * cos(T()), FH() + DD() * sin(T())], [0, FH()]]);
}

// ---- cuts (shared by the 3D holes and the 2D templates) ----------------
module key_cuts(lbl) {
    for (r = [0 : 1], c = [0 : 5]) {
        place(key_u(c), key_v(r)) hole_rect(cut_mx, cut_mx);
        place(key_u(c), key_v(r) + pitch_r / 2) hole_round(window_d);
    }
}
module cuts(i) {
    if (i == 0) {
        place(fader_u, fader_v0 + fader_len / 2) hole_rect(6, fader_len + 12);
        for (s = [-1, 1]) place(fader_u, fader_v0 + fader_len / 2 + s * fader_hole_span / 2) hole_round(3.4);
        place(stick_l[0], stick_l[1]) hole_rect(stick_cut[0], stick_cut[1]);
        for (p = enc_l) place(p[0], p[1]) hole_round(7);
    } else if (i == 1) {
        place(stick_r[0], stick_r[1]) hole_rect(stick_cut[0], stick_cut[1]);
        for (p = enc_r) place(p[0], p[1]) hole_round(7);
    } else if (i == 2) {
        key_cuts(key_lbl_l);
        for (p = tog_l) place(p[0], p[1]) hole_round(12.2);
    } else if (i == 3) {
        for (p = oled_pos) place(p[0], p[1]) hole_rect(58, 31);
        for (u = bar_u, k = [0 : 7]) place(u, bar_v0 + k * bar_pitch) hole_round(window_d);
        place(buzzer[0], buzzer[1]) hole_round(12);
    } else {
        key_cuts(key_lbl_r);
        for (p = tog_r) place(p[0], p[1]) hole_round(12.2);
    }
}

// ---- 3D proxies for the parts -----------------------------------------
module stick_proxy() {
    color("#555") translate([-stick_flange[0] / 2, -stick_flange[1] / 2, 0]) cube([stick_flange[0], stick_flange[1], 3]);
    color("#222") cylinder(d = 12, h = stick_h - stick_grip[1], $fn = 32);
    color("#333") translate([0, 0, stick_h - stick_grip[1]]) cylinder(d = stick_grip[0], h = stick_grip[1], $fn = 48);
    color("#c33") translate([0, 0, stick_h]) cylinder(d = 12, h = stick_btn, $fn = 32);
}
module encoder_proxy() color("#bbb") translate([0, 0, 2]) cylinder(d = 25, h = 13, $fn = 40);
module toggle_proxy() {
    color("#999") cylinder(d = 6, h = 20, $fn = 24);
    color("#c33") translate([-8, -6, 0]) cube([16, 12, 16]);
}
module key_proxy() {
    color("#222") translate([-7.8, -7.8, 0]) cube([15.6, 15.6, 5]);
    color("#e6e6e6") translate([-9, -9, 5.5]) cube([18, 18, 8]);
}
module glow(c = "#3c3") color(c) translate([0, 0, -0.2]) cylinder(d = window_d - 0.4, h = 0.6, $fn = 24);
module key_proxies(blue = false) {
    for (r = [0 : 1], c = [0 : 5]) {
        place(key_u(c), key_v(r)) key_proxy();
        place(key_u(c), key_v(r) + pitch_r / 2) glow(blue && r == 0 && c == 1 ? "#39f" : "#3c3");
    }
}
module proxies(i) {
    if (i == 0) {
        place(fader_u, fader_v0 + 0.6 * fader_len) color("#c33")
            translate([-nubbin[0] / 2, -nubbin[1] / 2, 0]) cube(nubbin);
        place(stick_l[0], stick_l[1]) stick_proxy();
        for (p = enc_l) place(p[0], p[1]) encoder_proxy();
    } else if (i == 1) {
        place(stick_r[0], stick_r[1]) stick_proxy();
        for (p = enc_r) place(p[0], p[1]) encoder_proxy();
    } else if (i == 2) {
        key_proxies(true);
        for (p = tog_l) place(p[0], p[1]) toggle_proxy();
    } else if (i == 3) {
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
        key_proxies(false);
        for (p = tog_r) place(p[0], p[1]) toggle_proxy();
    }
}

// ---- hollow shell, ballast and feet -------------------------------------
module shell_body(i) {
    difference() {
        wedge(W[i]);
        // cavity: a column from the floor up through the sloped top
        translate([wall, wall, wall]) cube([W[i] - 2 * wall, DD() * cos(T()) - 2 * wall, 400]);
        // rebate: everything above the plane one plate thickness below the panel surface
        place(0, 0) translate([-1, -1, -plate_t]) cube([W[i] + 2, DD() + 2, 400]);
    }
}
function foot_pos(i) = [[30, 30], [W[i] - 30, 30], [30, DD() * cos(T()) - 30], [W[i] - 30, DD() * cos(T()) - 30]];
module feet(i) color("#111") for (p = foot_pos(i)) translate([p[0], p[1], -3]) cylinder(d = foot_d, h = 3, $fn = 32);
module ballast_stack(i) color("#7d8a99") {
    u0 = i == 0 ? 58 : 20;                  // left wing: keep clear of the fader body at u 21..39
    for (k = [0, 1]) translate([u0, 12, wall + k * steel[2]]) cube(steel);
}
module extras(i) {
    feet(i);
    if (ballast && i < 2) ballast_stack(i);
}

// ---- top level --------------------------------------------------------
module piece3d(i) {
    $m = i;
    translate([x_off[i], y_off[i], 0]) difference() {
        union() {
            if (part == "all" || part == "shell")
                color("#9aa0a6") { if (hollow) shell_body(i); else difference() { wedge(W[i]); cuts(i); } }
            if (part == "all" || part == "plate")
                color("#1b1b1f") difference() {
                    place(0, 0) translate([0, 0, -plate_t]) cube([W[i], DD(), plate_t + (part == "all" ? 0.1 : 0)]);
                    cuts(i);
                }
            if (part == "all") { proxies(i); extras(i); }
        }
        if (cut_x >= 0) translate([cut_x, -50, -50]) cube([500, 800, 800]);
    }
}

if (flat) {
    $m = mod;
    difference() { square([W[mod], D_m[mod]]); cuts(mod); }
} else {
    for (i = [0 : 4]) if (mod < 0 || mod == i) piece3d(i);
}
