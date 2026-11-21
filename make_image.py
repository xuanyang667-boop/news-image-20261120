"""Render the 20 November 2026 world-news broadsheet as a single image.

Fresh implementation for the news-image-20261120 entry. The program
draws one 1024x1024 PNG with Pillow: a one-page newspaper front page
summing up the day's world news. No network access and no randomness,
so running it twice produces a byte-identical file.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = (1024, 1024)
MARGIN = 46
RIGHT = SIZE[0] - MARGIN
CENTER_X = SIZE[0] / 2

PAPER = (247, 242, 230)
INK = (20, 20, 20)
RED = (163, 29, 33)
NAVY = (22, 35, 63)
RIVER = (63, 109, 150)
GOLD = (201, 154, 46)
DARK_GREY = (74, 74, 70)
STEEL = (198, 206, 216)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF = FONT_DIR / "DejaVuSerif.ttf"
SERIF_BOLD = FONT_DIR / "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"

LEAD_WIDTH = 560
ART_X0 = 624
MID_GAP = 28
MID_WIDTH = (SIZE[0] - 2 * MARGIN - MID_GAP) // 2
ALSO_GAP = 14
ALSO_WIDTH = (SIZE[0] - 2 * MARGIN - 3 * ALSO_GAP) // 4


def load_font(path, size):
    return ImageFont.truetype(str(path), size)


def advance(font):
    """Tight vertical advance of one line set in this font."""
    top, bottom = font.getmetrics()
    return top + bottom


def step(font, factor=1.3):
    return int(advance(font) * factor)


def wrap(draw, text, font, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_para(draw, x, y, lines, font, fill, factor=1.3):
    gap = step(font, factor)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += gap
    return y


def draw_centred(draw, y, text, font, fill):
    width = draw.textlength(text, font=font)
    draw.text((CENTER_X - width / 2, y), text, font=font, fill=fill)
    return y + advance(font)


def draw_tracked(draw, y, text, font, fill, tracking=16):
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * max(len(text) - 1, 0)
    x = CENTER_X - total / 2
    for ch, char_width in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += char_width + tracking
    return y + advance(font)


def hline(draw, y, width=2, fill=INK):
    draw.line([(MARGIN, y), (RIGHT, y)], fill=fill, width=width)
    return y + width


def draw_night_scene(draw, x0, y0, x1, y1):
    """Kyiv at night: dark sky, missile streaks, bridges, river."""
    width = x1 - x0
    height = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    draw.rectangle([x0, y0, x1, y1], outline=(10, 18, 34), width=2)
    # Stars at fixed positions, as fractions of the panel.
    for fx, fy, r in [
        (0.08, 0.10, 2), (0.24, 0.06, 2), (0.38, 0.14, 2),
        (0.55, 0.07, 2), (0.70, 0.12, 2), (0.86, 0.06, 2),
        (0.93, 0.20, 2), (0.16, 0.24, 2), (0.47, 0.22, 2),
        (0.63, 0.26, 2), (0.80, 0.30, 2), (0.31, 0.30, 2),
    ]:
        cx = x0 + fx * width
        cy = y0 + fy * height
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 238, 245))
    # Missile streaks.
    draw.line([(x0 + 0.30 * width, y0 + 0.05 * height),
               (x0 + 0.20 * width, y0 + 0.42 * height)], fill=GOLD, width=3)
    draw.line([(x0 + 0.82 * width, y0 + 0.04 * height),
               (x0 + 0.72 * width, y0 + 0.38 * height)], fill=GOLD, width=3)
    # Three bridge silhouettes above the river.
    river_top = y1 - 66
    deck_y = river_top - 26
    for i in range(3):
        bx = x0 + 18 + i * 112
        draw.line([(bx, deck_y), (bx + 84, deck_y)], fill=STEEL, width=3)
        draw.line([(bx, deck_y), (bx, river_top)], fill=STEEL, width=3)
        draw.line([(bx + 84, deck_y), (bx + 84, river_top)], fill=STEEL, width=3)
        draw.arc([bx + 8, deck_y - 22, bx + 76, deck_y + 22],
                 start=180, end=360, fill=STEEL, width=3)
    # Explosion bursts on the first two bridges.
    for cx, cy in [(x0 + 60, deck_y - 4), (x0 + 172, deck_y - 4)]:
        for k in range(8):
            ang = math.pi * k / 4.0
            x2 = cx + 26 * math.cos(ang)
            y2 = cy + 26 * math.sin(ang)
            draw.line([(cx, cy), (x2, y2)], fill=(232, 138, 32), width=3)
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(232, 138, 32))
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(245, 214, 110))
    # River band with caption.
    draw.rectangle([x0, river_top, x1, y1], fill=RIVER)
    caption_font = load_font(SANS_BOLD, 18)
    caption = wrap(draw, "Three bridges over the Dnipro hit",
                   caption_font, width - 28)
    cy = river_top + (66 - len(caption) * step(caption_font, 1.25)) / 2
    for line in caption:
        lw = draw.textlength(line, font=caption_font)
        draw.text((x0 + (width - lw) / 2, cy), line,
                  font=caption_font, fill=(255, 255, 255))
        cy += step(caption_font, 1.25)


def story_block(draw, x, width, kicker_text, headline_text, body_text, y):
    kf = load_font(SANS_BOLD, 19)
    draw.text((x, y), kicker_text, font=kf, fill=RED)
    y += advance(kf) + 4
    hf = load_font(SERIF_BOLD, 27)
    y = draw_para(draw, x, y, wrap(draw, headline_text, hf, width),
                  hf, INK, factor=1.12)
    y += 4
    bf = load_font(SERIF, 17)
    y = draw_para(draw, x, y, wrap(draw, body_text, bf, width),
                  bf, INK, factor=1.32)
    return y


def markets_chart(draw, x, y, width):
    base = y + 58
    draw.line([(x, base), (x + width - 130, base)], fill=INK, width=2)
    for bx, bh, colour in [(0, 54, RED), (72, 40, RED), (144, 22, GOLD)]:
        draw.rectangle([x + bx, base - bh, x + bx + 54, base], fill=colour)
    lab = load_font(SERIF_BOLD, 32)
    draw.text((x + width - 118, base - 44), "-4.8%", font=lab, fill=INK)
    return base + 6


def tanker_graphic(draw, x, y, width):
    top = y
    hull = [(x, top + 24), (x + 150, top + 24),
            (x + 176, top + 42), (x + 8, top + 42)]
    draw.polygon(hull, fill=RED)
    draw.rectangle([x + 18, top + 6, x + 62, top + 24], fill=(240, 240, 235))
    draw.rectangle([x + 118, top, x + 140, top + 24], fill=GOLD)
    draw.line([(x + 129, top), (x + 129, top - 10)], fill=INK, width=2)
    for wx in (x + 8, x + 62, x + 116):
        draw.arc([wx, top + 46, wx + 32, top + 56],
                 start=0, end=180, fill=RIVER, width=2)
    lab = load_font(SERIF_BOLD, 28)
    draw.text((x + 196, top + 8), "14 tankers", font=lab, fill=INK)
    return top + 60


def also_section(draw, y):
    hf = load_font(SANS_BOLD, 24)
    draw.text((MARGIN, y), "ALSO ON 20 NOVEMBER", font=hf, fill=INK)
    y += advance(hf) + 10
    items = [
        ("COP31 · ANTALYA", "Final day: draft drops fossil-fuel phase-out."),
        ("RIYADH", "Houthi missile damages PIF Tower in Riyadh."),
        ("ESTONIA", "Tallinn to shut road borders with Russia over "
                    "\"sustained aggression\"."),
        ("TATARSTAN", "Ukraine hits Druzhba oil pipeline station deep "
                      "inside Russia."),
    ]
    top = y
    bottom = top
    for i, (label, text) in enumerate(items):
        x = MARGIN + i * (ALSO_WIDTH + ALSO_GAP)
        lf = load_font(SANS_BOLD, 17)
        yy = draw_para(draw, x, top, wrap(draw, label, lf, ALSO_WIDTH),
                       lf, RED, factor=1.15)
        bf = load_font(SERIF, 17)
        yy = draw_para(draw, x, yy + 2, wrap(draw, text, bf, ALSO_WIDTH),
                       bf, INK, factor=1.28)
        bottom = max(bottom, yy)
    return bottom


def build():
    img = Image.new("RGB", SIZE, PAPER)
    draw = ImageDraw.Draw(img)
    y = 30

    # Masthead.
    y = draw_centred(draw, y, "THE WORLD", load_font(SERIF_BOLD, 84), INK)
    y += 2
    y = draw_tracked(draw, y, "IN ONE IMAGE", load_font(SANS_BOLD, 24),
                     INK, tracking=16)
    y += 8
    y = hline(draw, y, width=3)
    y += 5
    y = hline(draw, y, width=1)
    y += 10
    y = draw_centred(draw, y, "FRIDAY  ·  20 NOVEMBER 2026",
                     load_font(SANS_BOLD, 24), RED)
    y += 8
    y = hline(draw, y, width=1, fill=RED)
    y += 12

    # Lead story: text on the left, night scene on the right.
    lead_top = y
    kicker = load_font(SANS_BOLD, 22)
    draw.text((MARGIN, y), "KYIV  —  TOP STORY", font=kicker, fill=RED)
    y += advance(kicker) + 6
    head = load_font(SERIF_BOLD, 38)
    y = draw_para(draw, MARGIN, y,
                  wrap(draw, "Russia's biggest barrage hits Kyiv's bridges",
                       head, LEAD_WIDTH),
                  head, INK, factor=1.12)
    y += 6
    body = load_font(SERIF, 19)
    y = draw_para(draw, MARGIN, y,
                  wrap(draw, "404 drones and 111 missiles overnight — 27 of "
                             "them ballistic — struck three bridges over the "
                             "Dnipro and cut power across Kyiv. At least "
                             "eight killed.",
                       body, LEAD_WIDTH),
                  body, INK, factor=1.32)
    y += 4
    redline = load_font(SANS_BOLD, 20)
    draw.text((MARGIN, y), "Two Russian missiles fell in Poland.",
              font=redline, fill=RED)
    y += advance(redline)
    lead_bottom = y
    draw_night_scene(draw, ART_X0, lead_top, RIGHT, lead_bottom)
    print("lead_bottom", lead_bottom)

    y = lead_bottom + 12
    y = hline(draw, y, width=2)
    y += 12

    # Middle: two stories side by side.
    mid_top = y
    mid_bottom = mid_top
    x = MARGIN
    yy = story_block(draw, x, MID_WIDTH,
                     "MARKETS", "AI sell-off sweeps Asia",
                     "Nikkei -4.8% and Kospi -5.2% as Anthropic's record "
                     "$83 IPO fails to revive faith in AI spending.",
                     y)
    yy = markets_chart(draw, x, yy + 10, MID_WIDTH)
    mid_bottom = max(mid_bottom, yy)
    x = MARGIN + MID_WIDTH + MID_GAP
    yy = story_block(draw, x, MID_WIDTH,
                     "THE GULF", "US widens Iran blockade; Tehran masses tankers",
                     "Washington now targets ship-to-ship transfers. Iran "
                     "parks 14 tankers at Kharg Island and floats a convoy "
                     "to break the blockade.",
                     y)
    yy = tanker_graphic(draw, x, yy + 10, MID_WIDTH)
    mid_bottom = max(mid_bottom, yy)
    print("mid_bottom", mid_bottom)

    y = mid_bottom + 12
    y = hline(draw, y, width=2)
    y += 12

    # Also on 20 November.
    y = also_section(draw, y)
    print("also_bottom", y)

    # Footer.
    y = hline(draw, y + 10, width=1)
    y += 8
    y = draw_centred(draw, y, "20 NOVEMBER 2026  ·  THE WORLD'S NEWS IN ONE IMAGE",
                     load_font(SANS_BOLD, 18), DARK_GREY)
    print("final_y", y)
    return img


def render(path):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    build().save(out, format="PNG")
    return out
