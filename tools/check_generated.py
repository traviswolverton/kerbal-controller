#!/usr/bin/env python3
"""Fail if a generated file in the repo is out of date.

Runs the generators, compares every generated file with what was there before, puts the old contents back and exits 1
listing the stale files. Nothing is left changed, so it is safe on a working tree with edits in it.

Run from anywhere:  python3 tools/check_generated.py     (or: make check)
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GENERATORS = [
    [sys.executable, "tools/gen_wiring.py"],
    [sys.executable, "tools/parts.py", "budget", "--md"],
]
GENERATED = [
    "docs/pinout.html",
    "firmware/ksp/include/pins.h",
    "hardware/electronics/wiring/wiring.md",
    "hardware/electronics/wiring/pin-map.md",
    "hardware/electronics/wiring/diagrams",
    "hardware/sourcing/parts.md",
]


def snapshot():
    """Every generated file's bytes, keyed by repo-relative path."""
    files = {}
    for rel in GENERATED:
        p = REPO / rel
        for f in ([p] if p.is_file() else sorted(p.rglob("*")) if p.is_dir() else []):
            if f.is_file():
                files[f.relative_to(REPO).as_posix()] = f.read_bytes()
    return files


def main():
    before = snapshot()
    try:
        for cmd in GENERATORS:
            done = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
            if done.returncode:
                print(f"generator failed: {' '.join(cmd[1:])}\n{done.stdout}{done.stderr}")
                return 2
        after = snapshot()
    finally:
        for rel, data in before.items():
            (REPO / rel).write_bytes(data)
    stale = sorted(r for r in set(before) | set(after) if before.get(r) != after.get(r))
    if stale:
        print("Out of date (run `make` and commit the result):")
        for r in stale:
            print("  " + r)
        return 1
    print(f"ok: {len(before)} generated files are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
