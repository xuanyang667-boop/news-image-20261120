#!/usr/bin/env python3
"""Entrypoint: render the 20 November 2026 broadsheet image.

Writes entry.png (1024x1024 PNG) and prints its size and sha256.
The output goes to $MAKEFUN_OUTPUT_DIR when that is set (the grader
runs with a read-only repository and a writable output directory),
otherwise to assets/entry.png next to this file.
Deterministic: two runs produce byte-identical output.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from make_image import render


def main() -> int:
    root = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        out = os.path.join(out_dir, "entry.png")
    else:
        out = os.path.join(root, "assets", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    render(out)
    with open(out, "rb") as fh:
        data = fh.read()
    print("wrote " + out)
    print("size " + str(len(data)) + " bytes")
    print("sha256 " + hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
