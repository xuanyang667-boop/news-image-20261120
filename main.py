#!/usr/bin/env python3
"""Entrypoint: render the 20 November 2026 broadsheet image.

Writes assets/entry.png (1024x1024 PNG) and prints its size and sha256.
Deterministic: two runs produce byte-identical output.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from make_image import render


def main() -> int:
    root = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(root, "assets", "entry.png")
    render(out)
    with open(out, "rb") as fh:
        data = fh.read()
    print("wrote " + out)
    print("size " + str(len(data)) + " bytes")
    print("sha256 " + hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
