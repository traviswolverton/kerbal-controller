"""Shared helpers for the parts-selection tools: paths, .env loading, errors and table output."""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class PartsError(Exception):
    pass


def load_env():
    """Read KEY=VALUE lines from <repo>/.env without overriding variables that are already set."""
    f = REPO / ".env"
    if not f.exists():
        return
    for line in f.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if v:
                os.environ.setdefault(k.strip(), v)


def money(x):
    return "-" if x is None else f"${x:,.2f}"


def is_active(status):
    return (status or "").strip().lower() in ("", "active", "new product")


def table(rows, cols):
    widths = [max(len(h), *(len(str(r[i])) for r in rows)) if rows else len(h) for i, h in enumerate(cols)]
    out = ["  ".join(h.ljust(w) for h, w in zip(cols, widths)), "  ".join("-" * w for w in widths)]
    out += ["  ".join(str(c).ljust(w) for c, w in zip(r, widths)) for r in rows]
    return "\n".join(out)
