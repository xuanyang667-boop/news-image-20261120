#!/usr/bin/env python3
"""News-image entry for make.fun's news-image-20261120 bounty.

Copies the pre-drawn front page (assets/entry.png, "The World in One
Image" for Friday 20 November 2026) to $MAKEFUN_OUTPUT_DIR/entry.png.

Standard library only. No network, no randomness, no timestamps: two
runs write byte-identical output.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    if not os.path.isfile(src):
        print("missing image: " + src, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) == 0:
        print("empty output: " + dst, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
