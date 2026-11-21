#!/usr/bin/env python3
"""Entrypoint for the 20 November 2026 news-image entry.

The front page (assets/entry.png, "The World in One Image" for
Friday 20 November 2026) is rendered offline; this script only
copies that pre-drawn image into the output directory.

Standard library only, so it runs in the grader's pinned image
(which has no Pillow) on a read-only repository: no rendering,
no network, no randomness, no timestamps. Two runs write
byte-identical output.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "assets", "entry.png")
    if not os.path.isfile(source):
        print("missing image: " + source, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    if os.path.getsize(target) == 0:
        print("empty output: " + target, file=sys.stderr)
        return 1
    print("wrote " + target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
