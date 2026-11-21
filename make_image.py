#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

Deterministic: no network, no randomness, no timestamps. Running it twice
writes byte-identical output (Pillow's PNG encoder is deterministic for the
same pixels with fixed settings).

Stories (all reported on Friday 20 November 2026):
- Lead: Russia's overnight barrage on Kyiv — 404 drones, 111 missiles —
  hits three bridges over the Dnipro; two Russian missiles fall in Poland.
- Markets: AI sell-off sweeps Asia — Nikkei -4.8%, Kospi -5.2% — after
  Anthropic's record IPO fails to revive faith in AI spending.
- The Gulf: the US widens its naval blockade of Iran to ship-to-ship
  transfers; Iran masses tankers at Kharg Island.
- Briefs: COP31's final day in Antalya, the PIF Tower hit in Riyadh,
  Estonia closing road borders with Russia, Ukraine's Druzhba strike.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (25, 25, 25)
RED = (166, 30, 30)
NAVY = (24, 48, 84)
SKY = (16, 34, 64)
RIVER = (86, 130, 168)
GOLD = (194, 154, 43)
ORANGE = (214, 110, 30)
TEAL = (31, 111, 107)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
SMOKE = (120, 120, 118)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_B = os.path.join(FONT_DIR, "NotoSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
SANS_SB = os.path.join(FONT_DIR, "NotoSans-SemiBold.ttf")
SANS = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw a wrapped paragraph; return the y below it."""
    lh = leading or int(fnt.size * 1.24)
    for line in wrap_text(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def spaced_centre(draw, cx, y, text, fnt, fill, gap=6):
    """Draw text centred on cx with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + gap


def hline(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def burst(draw, cx, cy, r, core, halo):
    """Explosion flash: radiating spikes plus a bright core."""
    for k in range(12):
        ang = k * 30
        import math
        rad = math.radians(ang)
        x1 = cx + int(r * 0.55 * math.cos(rad))
        y1 = cy + int(r * 0.55 * math.sin(rad))
        x2 = cx + int(r * math.cos(rad))
        y2 = cy + int(r * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=halo, width=4)
    draw.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
                 fill=core)
    draw.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2],
                 fill=WHITE)


def bridge_panel(draw, x0, y0, x1, y1):
    """Night over the Dnipro: three bridges, two blasts, river below."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=SKY)
    # stars
    for sx, sy in [(660, 258), (720, 246), (800, 262), (880, 250), (940, 270),
                   (690, 300), (850, 296)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
    # missile trails arcing down from the top
    draw.line([(700, 236), (742, 330)], fill=GOLD, width=3)
    draw.line([(920, 236), (884, 322)], fill=GOLD, width=3)
    # river band
    draw.rectangle([x0, 400, x1, y1], fill=RIVER)
    draw.line([(x0, 400), (x1, 400)], fill=WHITE, width=2)
    # three bridge decks across the river, in pale steel so they read at night
    for bx in (668, 772, 876):
        draw.line([(bx - 34, 400), (bx + 34, 400)], fill=(214, 208, 192), width=7)
        draw.line([(bx - 34, 400), (bx - 34, 352)], fill=(214, 208, 192), width=5)
        draw.line([(bx + 34, 400), (bx + 34, 352)], fill=(214, 208, 192), width=5)
        draw.line([(bx - 34, 352), (bx, 372)], fill=(214, 208, 192), width=3)
        draw.line([(bx + 34, 352), (bx, 372)], fill=(214, 208, 192), width=3)
    # blasts on two of the bridges
    burst(draw, 772, 372, 34, ORANGE, GOLD)
    burst(draw, 668, 384, 24, ORANGE, GOLD)
    # smoke puffs
    for sx, sy, sr in [(800, 330, 14), (830, 318, 10), (700, 340, 11)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SMOKE)
    draw.text(((x0 + x1) // 2, y1 - 38), "Three bridges over the Dnipro hit",
              font=font(SANS_SB, 20), fill=WHITE, anchor="ma")


def falling_bars(draw, x, y, w, h, values, colors):
    """Bar chart falling left to right (largest first)."""
    n = len(values)
    bw = w / n * 0.55
    gap = w / n * 0.45
    mx = max(values)
    for i, v in enumerate(values):
        bh = h * v / mx
        bx = x + i * (bw + gap) + gap / 2
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=colors[i % len(colors)])
    draw.line([(x, y + h), (x + w, y + h)], fill=INK, width=3)


def tanker(draw, x, y, w, h):
    """Oil tanker on waves, bow to the right."""
    # hull
    draw.polygon([(x, y + h * 0.55), (x + w * 0.82, y + h * 0.55),
                  (x + w, y + h * 0.72), (x + w * 0.94, y + h * 0.95),
                  (x, y + h * 0.95)], fill=RED)
    # deck + superstructure + funnel
    draw.rectangle([x + w * 0.06, y + h * 0.30, x + w * 0.30, y + h * 0.55],
                   fill=WHITE, outline=INK, width=2)
    draw.rectangle([x + w * 0.62, y + h * 0.18, x + w * 0.74, y + h * 0.55],
                   fill=GOLD, outline=INK, width=2)
    draw.line([(x + w * 0.68, y + h * 0.18), (x + w * 0.68, y)],
              fill=INK, width=3)
    # waves
    for i in range(4):
        wx = x + i * (w / 4)
        draw.arc([wx, y + h * 0.92, wx + w / 4, y + h * 1.12],
                 start=180, end=360, fill=RIVER, width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead (0..212) ----------
    d.text((W // 2, 14), "THE WORLD", font=font(SERIF_B, 96), fill=INK, anchor="ma")
    spaced_centre(d, W // 2, 118, "IN ONE IMAGE", font(SANS_B, 26), INK, gap=10)
    hline(d, 60, 964, 158, fill=INK, width=3)
    d.text((W // 2, 168), "FRIDAY  ·  20 NOVEMBER 2026", font=font(SANS_B, 30),
           fill=RED, anchor="ma")
    hline(d, 60, 964, 212, fill=RED, width=2)

    # ---------- lead story (232..508) ----------
    lx, lw = 40, 556
    d.text((lx, 236), "KYIV  —  TOP STORY", font=font(SANS_B, 23), fill=RED)
    para(d, lx, 270, "Russia's biggest barrage hits Kyiv's bridges",
         font(SERIF_B, 42), lw, leading=47)
    para(d, lx, 382,
         "404 drones and 111 missiles overnight — 27 of them ballistic — "
         "struck three bridges over the Dnipro and cut power across Kyiv. "
         "At least eight killed.",
         font(SANS, 21), lw, leading=26)
    d.text((lx, 472), "Two Russian missiles fell in Poland.",
           font=font(SANS_B, 21), fill=RED)

    # lead visual: night over the Dnipro
    bridge_panel(d, 620, 232, 984, 500)

    hline(d, 40, 984, 522, fill=INK, width=2)

    # ---------- middle row (538..806) ----------
    # Markets (left)
    mx, mw = 40, 452
    d.text((mx, 538), "MARKETS", font=font(SANS_B, 22), fill=RED)
    para(d, mx, 566, "AI sell-off sweeps Asia",
         font(SERIF_B, 30), mw, leading=36)
    para(d, mx, 644,
         "Nikkei -4.8% and Kospi -5.2% as Anthropic's record $83 IPO "
         "fails to revive faith in AI spending.",
         font(SANS, 20), mw, leading=26)
    falling_bars(d, mx, 730, 300, 56, [1.0, 0.62, 0.34], [RED, RED, GOLD])
    d.text((mx + 316, 748), "-4.8%", font=font(SANS_B, 28), fill=INK)

    # The Gulf (right)
    rx, rw = 532, 452
    d.text((rx, 538), "THE GULF", font=font(SANS_B, 22), fill=RED)
    para(d, rx, 566, "US widens Iran blockade; Tehran masses tankers",
         font(SERIF_B, 30), rw, leading=36)
    para(d, rx, 644,
         "Washington now targets ship-to-ship transfers. Iran parks 14 "
         "tankers at Kharg Island and floats a convoy to break the blockade.",
         font(SANS, 20), rw, leading=26)
    tanker(d, rx, 724, 190, 62)
    d.text((rx + 210, 748), "14 tankers", font=font(SANS_B, 28), fill=INK)

    hline(d, 40, 984, 820, fill=INK, width=2)

    # ---------- briefs (836..960) ----------
    d.text((40, 836), "ALSO ON 20 NOVEMBER", font=font(SANS_B, 24), fill=INK)
    briefs = [
        ("COP31 · ANTALYA", "Final day: draft drops fossil-fuel phase-out."),
        ("RIYADH", "Houthi missile damages PIF Tower in Riyadh."),
        ("ESTONIA", "Tallinn to shut road borders with Russia over “sustained aggression”."),
        ("TATARSTAN", "Ukraine hits Druzhba oil pipeline station deep inside Russia."),
    ]
    for i, (kick, text) in enumerate(briefs):
        x = 40 + i * 242
        d.text((x, 872), kick, font=font(SANS_B, 18), fill=RED)
        para(d, x, 898, text, font(SANS, 19), 226, leading=23)

    # ---------- footer ----------
    hline(d, 40, 984, 972, fill=INK, width=2)
    d.text((W // 2, 982), "20 NOVEMBER 2026  ·  THE WORLD'S NEWS IN ONE IMAGE",
           font=font(SANS_B, 19), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    out = os.environ.get("OUT", "assets/entry.png")
    img = build()
    img.save(out, "PNG", optimize=True)
    print(out, img.size, os.path.getsize(out), "bytes")
