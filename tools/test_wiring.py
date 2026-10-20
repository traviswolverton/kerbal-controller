"""Checks on the pin data and the generated outputs. Run from the tools folder: python3 test_wiring.py"""
import json
import os
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_wiring  # noqa: E402


class PinMap(unittest.TestCase):
    def test_teensy_pins_are_valid_and_unique(self):
        pins = list(gen_wiring.TEENSY)
        self.assertEqual(len(pins), len(set(pins)))
        self.assertTrue(all(0 <= p <= 41 for p in pins))
        self.assertEqual(len(set(gen_wiring.TEENSY.values())), len(pins), "a signal is on two pins")

    def test_every_signal_reaches_a_port_or_a_local_part(self):
        ported = {s for _, pins in gen_wiring.PORTS.values() for s in pins.values()}
        for sig in gen_wiring.TEENSY.values():
            self.assertTrue(sig in ported or sig in gen_wiring.MID_DEST, f"{sig} has no DB25 conductor or local destination")

    def test_pins_h_is_current(self):
        with open(gen_wiring.PINS_H) as f:
            self.assertEqual(f.read(), gen_wiring.pins_h(), "firmware/ksp/include/pins.h is stale: run tools/gen_wiring.py")

    def test_pinmap_json_loads(self):
        with open(os.path.join(REPO, "hardware", "electronics", "pinmap.json")) as f:
            self.assertEqual(set(json.load(f)["ports"]), {"LW", "RW", "LS", "RS"})


if __name__ == "__main__":
    unittest.main()
