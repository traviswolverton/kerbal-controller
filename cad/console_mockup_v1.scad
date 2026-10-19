// Kerbal controller - console mockup v1: five pieces (a proposal to react to)
//
// Modelled on the stepped layout of the reference builds: a raised, steep back STRIP of three
// pieces, and two lower WINGS at the front ends, with the middle front left open.
// Each piece is a printed shell with a removable 3 mm faceplate (shown dark).
//
//   piece 0  LEFT WING     translation stick, throttle fader, time-warp encoder
//   piece 1  RIGHT WING    rotation stick, camera and page encoders
//   piece 2  STRIP LEFT    12 navigation keys + the SWITCH PANEL (everything on the I2C expander, incl. the STAGE key switch and ENGAGE toggle)
//   piece 3  STRIP MIDDLE  2 OLEDs, 4 fuel bars, buzzer, master power, Teensy and power jack inside
//   piece 4  STRIP RIGHT   12 action-group keys + the ANNUNCIATOR (9 pixel windows)
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
W       = [220, 220, 240, 240, 220];      // width of each piece
x_off   = [0, 480, 0, 240, 480];          // left edge, across the console
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
             ["AG4","AG5","AG6","AG7","AG8","AG9"]];
function key_u(c) = key_u0 + 9.525 + c * pitch_c;
function key_v(r) = key_v0 + (1 - r) * pitch_r + 9.525;
// switch panel (strip left): every input here goes to the MCP23017 expander sitting behind it
sw_tog   = [[162, 125], [162, 104]];  sw_tog_lbl = ["ABORT", "ENGAGE"];       // guarded toggles, cover lies along u
sw_key   = [162, 82];                                                         // key switch that arms STAGE, 12 mm hole (E-Switch KO133)
sw_stage = [208, 103];                                                       // big STAGE button, 30 mm hole (Adafruit 3489)
sw_cols  = [150, 169.05, 188.1, 207.15];  sw_rows = [14, 35.3, 56.6];  // MX button grid, 3 rows front to back
sw_lbl   = ["FULL","CUT","PRECISION","PAUSE", "MAP","FOCUS-","FOCUS+","UI",
            "QSAVE","QLOAD","SPARE","SPARE"];                                  // 12 buttons, filled from the back row
function sw_pos(k) = [sw_cols[k % 4], sw_rows[2 - floor(k / 4)]];
// annunciator (strip right): one pixel behind each 24 x 12 mm window
ann_cols = [150, 176, 202];  ann_rows = [88, 72, 56];
ann_lbl  = ["LOW FUEL","LOW POWER","OVERHEAT", "LOW ALT","STABLE ORBIT","ATMOSPHERE", "CHUTE SAFE","LINK","CONTROLS"];
function ann_pos(k) = [ann_cols[k % 3], ann_rows[floor(k / 3)]];
oled_pos = [[50, 100], [120, 100]];                  // 58 x 31 windows
bar_u = [175, 189, 203, 217];  bar_v0 = 20;  bar_pitch = 11.5;   // 4 fuel bars of 8
bar_lbl = ["LF", "OX", "MONO", "EC"];
buzzer = [30, 45];

// ---- DB25 inter-piece jacks (ITT Cannon ZDB25S / ZDB25P, rear-mount cutout from the datasheet) ----
db25_cut   = [42.52, 11.40];   // cutout, long side x short side
db25_pitch = 47.04;            // two mounting holes, 3.05 mm + 0.15 mm
db25_hole  = 3.2;
db25_flange = [53.09, 12.55];
// jack centres, [along the wall, height]. Middle strip back wall: LS and RS on the top row, LW and RW below.
mid_jacks   = [[62, 80, "LS"], [178, 80, "RS"], [62, 40, "LW"], [178, 40, "RW"]];
strip_jack  = [[120, 40], [0, 0], [110, 40]];   // strip left / (unused) / strip right: back wall, [x, z]
wing_jack   = [118, 24];                          // wing outer end wall: [y, z]

// ---- PROVISIONAL rear-wall cutouts on the middle strip: the part sizes are NOT verified, these only hold the place ----
dc_jack_cut = [120, 100, 11];     // x, z, hole diameter. Tensility 54-00151: datasheet is an image, cutout unknown
fuse_cut    = [120, 70, 12.5];    // x, z, hole diameter. Wurth 952005000010000: hole unknown
usb_cut     = [120, 40];          // x, z: 15 x 8 slot and two 2.5 mm screw holes 22 mm apart. SparkFun 15464: unknown
master = [100, 45];      // master 5 V power switch

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
        for (p = sw_tog) place(p[0], p[1]) hole_round(12.2);
        place(sw_key[0], sw_key[1]) hole_round(12.2);
        place(sw_stage[0], sw_stage[1]) hole_round(30.2);
        for (k = [0 : len(sw_lbl) - 1]) place(sw_pos(k)[0], sw_pos(k)[1]) hole_rect(cut_mx, cut_mx);
    } else if (i == 3) {
        for (p = oled_pos) place(p[0], p[1]) hole_rect(58, 31);
        for (u = bar_u, k = [0 : 7]) place(u, bar_v0 + k * bar_pitch) hole_round(window_d);
        place(buzzer[0], buzzer[1]) hole_round(12);
        place(master[0], master[1]) hole_round(12.2);
    } else {
        key_cuts(key_lbl_r);
        for (k = [0 : 8]) place(ann_pos(k)[0], ann_pos(k)[1]) hole_rect(24, 12);
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
module guard_proxy() { toggle_proxy(); color([0.85, 0.1, 0.1, 0.55]) translate([-23.5, -8.5, 0]) cube([47, 17, 14]); }
module stage_proxy() color("#d22") cylinder(d = 33, h = 14, $fn = 48);
module key_switch_proxy() { color("#bbb") cylinder(d = 16, h = 10, $fn = 40); color("#cc9") translate([-1.5, -6, 10]) cube([3, 12, 8]); }
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
        for (p = sw_tog) place(p[0], p[1]) guard_proxy();
        place(sw_key[0], sw_key[1]) key_switch_proxy();
        place(sw_stage[0], sw_stage[1]) stage_proxy();
        for (k = [0 : len(sw_lbl) - 1]) place(sw_pos(k)[0], sw_pos(k)[1]) key_proxy();
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
        place(master[0], master[1]) toggle_proxy();
    } else {
        key_proxies(false);
        for (k = [0 : 8]) place(ann_pos(k)[0], ann_pos(k)[1])
            color(k == 0 ? "#fa0" : k == 3 ? "#e33" : k == 7 ? "#3c3" : "#3a2d12") translate([-12, -6, -0.3]) cube([24, 12, 0.6]);
    }
}

// ---- DB25 wall cutouts ---------------------------------------------------
module db25_back_cut(x, z, yb) {        // on a vertical back wall at y = yb
    translate([x - db25_cut[0] / 2, yb - wall - 1, z - db25_cut[1] / 2]) cube([db25_cut[0], wall + 2, db25_cut[1]]);
    for (s = [-1, 1]) translate([x + s * db25_pitch / 2, yb - wall - 1, z]) rotate([-90, 0, 0]) cylinder(d = db25_hole, h = wall + 2, $fn = 24);
}
module db25_side_cut(y, z, xw, dir) {   // on a vertical end wall at x = xw; dir +1 = wall faces +x
    xs = dir > 0 ? xw - wall - 1 : xw - 1;
    translate([xs, y - db25_cut[0] / 2, z - db25_cut[1] / 2]) cube([wall + 2, db25_cut[0], db25_cut[1]]);
    for (s = [-1, 1]) translate([xs, y + s * db25_pitch / 2, z]) rotate([0, 90, 0]) cylinder(d = db25_hole, h = wall + 2, $fn = 24);
}
module prov_back_round(x, z, d, yb) translate([x, yb - wall - 1, z]) rotate([-90, 0, 0]) cylinder(d = d, h = wall + 2, $fn = 40);
module prov_back_usb(x, z, yb) {
    translate([x - 7.5, yb - wall - 1, z - 4]) cube([15, wall + 2, 8]);
    for (s = [-1, 1]) translate([x + s * 11, yb - wall - 1, z]) rotate([-90, 0, 0]) cylinder(d = 2.5, h = wall + 2, $fn = 20);
}
module wall_cuts(i) {
    yb = DD() * cos(T());
    if (i == 0) db25_side_cut(wing_jack[0], wing_jack[1], 0, -1);                 // left wing: left end wall
    else if (i == 1) db25_side_cut(wing_jack[0], wing_jack[1], W[1], 1);          // right wing: right end wall
    else if (i == 3) {
        for (j = mid_jacks) db25_back_cut(j[0], j[1], yb);
        prov_back_round(dc_jack_cut[0], dc_jack_cut[1], dc_jack_cut[2], yb);
        prov_back_round(fuse_cut[0], fuse_cut[1], fuse_cut[2], yb);
        prov_back_usb(usb_cut[0], usb_cut[1], yb);
    }
    else db25_back_cut(strip_jack[i - 2][0], strip_jack[i - 2][1], yb);
}
// jack in its own frame: x along the wall, z up, y outward. The flange sits against the inside face, the body passes
// through the wall and stands 11 mm proud.
module jack3d(female) color(female ? "#9a9a9a" : "#c4c4c4") translate([-db25_flange[0] / 2, 0, -db25_flange[1] / 2]) {
    cube([db25_flange[0], 1.2, db25_flange[1]]);
    translate([(db25_flange[0] - 38.96) / 2, 1.2, (db25_flange[1] - 8.4) / 2]) cube([38.96, wall + 11, 8.4]);
}
module jack_proxies(i) {
    yb = DD() * cos(T());
    if (i == 3) {
        for (j = mid_jacks) translate([j[0], yb - wall - 1.2, j[1]]) jack3d(true);
        color("#e8a33d") {      // PROVISIONAL parts, orange so they read as placeholders
            translate([dc_jack_cut[0], yb - 1, dc_jack_cut[1]]) rotate([-90, 0, 0]) cylinder(d = dc_jack_cut[2] + 4, h = 9, $fn = 40);
            translate([fuse_cut[0], yb - 1, fuse_cut[1]]) rotate([-90, 0, 0]) cylinder(d = fuse_cut[2] + 4, h = 18, $fn = 40);
            translate([usb_cut[0] - 9, yb - 1, usb_cut[1] - 5]) cube([18, 8, 10]);
        }
    }
    else if (i >= 2) translate([strip_jack[i - 2][0], yb - wall - 1.2, strip_jack[i - 2][1]]) jack3d(false);
    else if (i == 0) translate([wall + 1.2, wing_jack[0], wing_jack[1]]) rotate([0, 0, 90]) jack3d(false);
    else translate([W[1] - wall - 1.2, wing_jack[0], wing_jack[1]]) rotate([0, 0, -90]) jack3d(false);
}

// ---- hollow shell, ballast and feet -------------------------------------
module shell_body(i) {
    difference() {
        wedge(W[i]);
        // cavity: a column from the floor up through the sloped top
        translate([wall, wall, wall]) cube([W[i] - 2 * wall, DD() * cos(T()) - 2 * wall, 400]);
        // rebate: everything above the plane one plate thickness below the panel surface
        place(0, 0) translate([-1, -1, -plate_t]) cube([W[i] + 2, DD() + 2, 400]);
        wall_cuts(i);
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
            if (part == "all") { proxies(i); extras(i); jack_proxies(i); }
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
