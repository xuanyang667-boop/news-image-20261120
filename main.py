"""Entrypoint: render the 20 November 2026 broadsheet image.

Runs the renderer in make_image.py and writes the finished page to
assets/entry.png next to this file.
"""

from pathlib import Path

from make_image import render


def main():
    out = Path(__file__).resolve().parent / "assets" / "entry.png"
    render(out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
