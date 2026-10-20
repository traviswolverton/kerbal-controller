// Kerbal controller - key + pixel test plate (layout B "annunciator rows")
//
// 2 x 2 keys. Each key has a 10 mm round WS2812B pixel board in a pocket
// directly above it. Three printed parts, stacked:
//
//   plate     1.5 mm, black. MX cutouts + a round light window above each key.
//   diffuser  thin white discs that sit in a counterbore on the plate underside.
//   spacer    5.0 mm, black. Key cavities, pixel pockets, wire channels.
//
// Every key uses a different cutout tolerance and every diffuser a different
// thickness, so one print tells you what fits and what looks right.
// Row-major from the top left: key 1, 2 / 3, 4.
//
// Render one part at a time:
//   openscad -D 'part="plate"'     -o stl/test_plate_plate.stl    test_plate.scad
//   openscad -D 'part="spacer"'    -o stl/test_plate_spacer.stl   test_plate.scad
//   openscad -D 'part="diffusers"' -o stl/test_plate_diffusers.stl test_plate.scad
//   (part="assembly" shows all three stacked for a visual check)

part = "assembly";

// ---- layout -----------------------------------------------------------
cols      = 2;
rows      = 2;
col_pitch = 19.05;
row_pitch = 36.0;     // 19.05 key slot + 16.95 for the pixel above it (36 so it clears the keycap in front)
margin    = 6;        // plate border outside the keys / pixels

// ---- MX switch --------------------------------------------------------
cut        = 14.0;                    // nominal plate cutout
cut_tols   = [-0.05, 0.0, 0.10, 0.20]; // added to cut, per key (row-major)
plate_t    = 1.5;                     // MX clips grip a 1.5 mm plate
cavity     = 15.6;                    // key cavity in the spacer
cap        = 18.0;                    // keycap footprint (for pixel placement)

// ---- pixel board (measure yours with calipers) ------------------------
pixel_d     = 10.0;
pixel_clear = 0.4;                    // pocket = pixel_d + clear
pixel_h     = 3.2;                    // board + LED stack height
window_d    = 6.5;                    // light window through the plate

// ---- diffuser discs ---------------------------------------------------
diff_t      = [0.4, 0.6, 0.8, 1.0];   // thickness per key (row-major)
diff_d      = 8.0;                    // disc diameter
diff_clear  = 0.3;                    // counterbore = diff_d + clear

// ---- spacer -----------------------------------------------------------
spacer_t    = 5.0;
channel_w   = 3.0;                    // wire channel along each pixel row
channel_d   = 2.0;
screw_d     = 3.2;                    // M3 clearance (use ~4.2 for heat-set inserts in the spacer)

eps = 0.01;

// ---- geometry ---------------------------------------------------------
slot       = 19.05;                   // key slot height inside a row cell
extra      = row_pitch - slot;
width      = cols * col_pitch;

function key_x(c) = (c + 0.5) * col_pitch;
function key_y(r) = -(r * row_pitch + extra + slot / 2);   // y grows upward
function pix_y(r) = key_y(r) + row_pitch / 2;               // centred between caps

x0 = -margin;
x1 = width + margin;
y1 = pix_y(0) + pixel_d / 2 + margin;
y0 = key_y(rows - 1) - slot / 2 - margin;

module outline(t) {
    translate([x0, y0, 0]) cube([x1 - x0, y1 - y0, t]);
}

module screw_holes(t) {
    for (x = [x0 + 3, x1 - 3], y = [y0 + 3, y1 - 3])
        translate([x, y, -eps]) cylinder(d = screw_d, h = t + 2 * eps, $fn = 32);
}

function idx(r, c) = r * cols + c;

module plate() {
    difference() {
        outline(plate_t);
        screw_holes(plate_t);
        for (r = [0 : rows - 1], c = [0 : cols - 1]) {
            i = idx(r, c);
            // MX cutout
            translate([key_x(c) - (cut + cut_tols[i]) / 2,
                       key_y(r) - (cut + cut_tols[i]) / 2, -eps])
                cube([cut + cut_tols[i], cut + cut_tols[i], plate_t + 2 * eps]);
            // light window above the key
            translate([key_x(c), pix_y(r), -eps])
                cylinder(d = window_d, h = plate_t + 2 * eps, $fn = 48);
            // counterbore on the underside for the diffuser disc
            translate([key_x(c), pix_y(r), -eps])
                cylinder(d = diff_d + diff_clear, h = diff_t[i] + eps, $fn = 48);
        }
    }
}

module spacer() {
    difference() {
        outline(spacer_t);
        screw_holes(spacer_t);
        for (r = [0 : rows - 1], c = [0 : cols - 1]) {
            // key cavity, through
            translate([key_x(c) - cavity / 2, key_y(r) - cavity / 2, -eps])
                cube([cavity, cavity, spacer_t + 2 * eps]);
            // pixel pocket from the top, LED flush with the plate underside
            translate([key_x(c), pix_y(r), spacer_t - pixel_h])
                cylinder(d = pixel_d + pixel_clear, h = pixel_h + eps, $fn = 64);
        }
        // wire channel along each pixel row, open to the top
        for (r = [0 : rows - 1])
            translate([x0 + 3.5, pix_y(r) - channel_w / 2, spacer_t - channel_d])
                cube([x1 - x0 - 7, channel_w, channel_d + eps]);
    }
}

module diffusers() {
    for (i = [0 : len(diff_t) - 1])
        translate([i * (diff_d + 3), 0, 0])
            cylinder(d = diff_d, h = diff_t[i], $fn = 48);
}

if (part == "plate")           plate();
else if (part == "spacer")     spacer();
else if (part == "diffusers")  diffusers();
else {
    // assembly, exploded slightly so the layers are visible
    color("#222")    translate([0, 0, spacer_t + 6]) plate();
    color("#eee")    for (r = [0 : rows - 1], c = [0 : cols - 1])
        translate([key_x(c), pix_y(r), spacer_t + 3]) cylinder(d = diff_d, h = diff_t[idx(r, c)], $fn = 48);
    color("#444")    spacer();
}
