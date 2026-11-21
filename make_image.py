"""Render the 20 November 2026 broadsheet: "The World in One Image".

A single 1024x1024 PNG newspaper front page, drawn with Pillow only.
No network, no randomness, no timestamps: running it twice produces
byte-identical output.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 240, 221)
INK = (28, 28, 28)
RED = (163, 22, 33)
NAVY = (18, 32, 62)
STEEL = (47, 93, 138)
GOLD = (201, 162, 39)
ORANGE = (255, 140, 0)
YELLOW = (255, 210, 60)
PALE = (205, 205, 205)
WAVE = (70, 120, 170)

SERIF_BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
SERIF_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
]
SANS_BOLD_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def _load(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


def serif_bold(size):
    return _load(SERIF_BOLD_PATHS, size)


def serif(size):
    return _load(SERIF_PATHS, size)


def sans_bold(size):
    return _load(SANS_BOLD_PATHS, size)


def wrap(text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    """Draw stacked lines; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_tracked(draw, cx, y, text, font, fill, tracking):
    """Draw `text` centred on cx with extra space between letters."""
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + tracking * max(len(text) - 1, 0)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def draw_rule(draw, x0, x1, y, height, fill=INK):
    draw.rectangle([x0, y, x1, y + height - 1], fill=fill)


def burst(draw, cx, cy, radius):
    """Orange starburst explosion with a yellow core."""
    for k in range(8):
        angle = math.pi * k / 4.0
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)
        draw.line([(cx, cy), (x2, y2)], fill=ORANGE, width=3)
    draw.ellipse(
        [cx - 13, cy - 13, cx + 13, cy + 13], fill=ORANGE
    )
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=YELLOW)


def draw_kyiv_panel(draw, px, py, pw, ph):
    """Night-sky illustration: missile trails over three Dnipro bridges."""
    draw.rectangle([px, py, px + pw - 1, py + ph - 1], fill=NAVY)
    stars = [
        (28, 28), (88, 16), (148, 42), (208, 24), (268, 38), (328, 18),
        (58, 78), (178, 68), (298, 84), (118, 108), (238, 98),
        (348, 118), (38, 138), (198, 138), (318, 148),
    ]
    for sx, sy in stars:
        draw.ellipse(
            [px + sx - 2, py + sy - 2, px + sx + 2, py + sy + 2],
            fill=(235, 235, 235),
        )
    # Two missile trails slanting down toward the bridges.
    for x_top, x_bottom in ((105, 150), (285, 330)):
        draw.line(
            [(px + x_top, py + 52), (px + x_bottom, py + 172)],
            fill=GOLD, width=4,
        )
        draw.ellipse(
            [px + x_top - 4, py + 48, px + x_top + 4, py + 56],
            fill=YELLOW,
        )
    # Three bridge arches with an explosion on each.
    for cx in (70, 190, 310):
        draw.arc(
            [px + cx - 48, py + 148, px + cx + 48, py + 244],
            180, 360, fill=PALE, width=3,
        )
        draw.line(
            [(px + cx - 48, py + 196), (px + cx - 48, py + 224)],
            fill=PALE, width=3,
        )
        draw.line(
            [(px + cx + 48, py + 196), (px + cx + 48, py + 224)],
            fill=PALE, width=3,
        )
        draw.line(
            [(px + cx - 48, py + 224), (px + cx + 48, py + 224)],
            fill=PALE, width=3,
        )
        burst(draw, px + cx, py + 203, 22)
    # Caption band.
    band_y = py + ph - 54
    draw.rectangle(
        [px, band_y, px + pw - 1, py + ph - 1], fill=STEEL
    )
    cap = sans_bold(20)
    draw.text(
        (px + pw // 2, band_y + 6), "Three bridges over the Dnipro",
        font=cap, fill=(255, 255, 255), anchor="ma",
    )
    draw.text(
        (px + pw // 2, band_y + 30), "hit",
        font=cap, fill=(255, 255, 255), anchor="ma",
    )


def draw_market_chart(draw):
    """Three falling bars with the Nikkei figure."""
    base = 810
    draw.line([(44, base), (470, base)], fill=INK, width=2)
    bars = [(60, 48, RED), (128, 36, RED), (196, 22, GOLD)]
    for x, height, color in bars:
        draw.rectangle([x, base - height, x + 52, base - 1], fill=color)
    draw.text(
        (300, 762), "-4.8%", font=serif_bold(38), fill=INK
    )


def draw_tanker(draw):
    """Red tanker hull, waves, and the count beside it."""
    hull = [(560, 786), (700, 786), (720, 806), (545, 806)]
    draw.polygon(hull, fill=RED)
    draw.rectangle([575, 770, 615, 786], fill=(240, 240, 240))
    draw.rectangle([640, 762, 658, 786], fill=GOLD)
    draw.line([(690, 786), (690, 766)], fill=INK, width=3)
    for wx in (560, 610, 660):
        draw.arc(
            [wx, 808, wx + 34, 818], 180, 360, fill=WAVE, width=2
        )
    draw.text(
        (740, 772), "14 tankers", font=serif_bold(34), fill=INK
    )


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    draw.text(
        (512, 20), "THE WORLD", font=serif_bold(88), fill=INK, anchor="ma"
    )
    draw_tracked(
        draw, 512, 122, "IN ONE IMAGE", serif_bold(28), INK, 14
    )
    draw_rule(draw, 44, 980, 164, 3)
    draw_rule(draw, 44, 980, 170, 1)
    draw.text(
        (512, 180), "FRIDAY \u00b7 20 NOVEMBER 2026",
        font=serif_bold(27), fill=RED, anchor="ma",
    )
    draw_rule(draw, 44, 980, 222, 2, fill=RED)

    # ---- Lead story: Kyiv ----
    draw.text(
        (44, 236), "KYIV \u2014 TOP STORY", font=sans_bold(24), fill=RED
    )
    head = serif_bold(38)
    y = draw_lines(
        draw, 44, 266,
        wrap("Russia's biggest barrage hits Kyiv's bridges", head, 520),
        head, INK, 43,
    )
    body = serif(20)
    y = draw_lines(
        draw, 44, y + 8,
        wrap(
            "404 drones and 111 missiles overnight \u2014 27 of them "
            "ballistic \u2014 struck three bridges over the Dnipro and "
            "cut power across Kyiv. At least eight killed.",
            body, 520,
        ),
        body, INK, 25,
    )
    draw.text(
        (44, y + 8), "Two Russian missiles fell in Poland.",
        font=serif_bold(21), fill=RED,
    )
    draw_kyiv_panel(draw, 600, 236, 380, 280)

    draw_rule(draw, 44, 980, 552, 2)

    # ---- Middle row ----
    draw.text((44, 566), "MARKETS", font=sans_bold(23), fill=RED)
    draw.text((540, 566), "THE GULF", font=sans_bold(23), fill=RED)

    m_head = serif_bold(36)
    draw_lines(
        draw, 44, 594,
        wrap("AI sell-off sweeps Asia", m_head, 456), m_head, INK, 42,
    )
    g_head = serif_bold(30)
    draw_lines(
        draw, 540, 594,
        wrap(
            "US widens Iran blockade; Tehran masses tankers",
            g_head, 440,
        ),
        g_head, INK, 38,
    )
    m_body = serif(19)
    draw_lines(
        draw, 44, 673,
        wrap(
            "Nikkei -4.8% and Kospi -5.2% as Anthropic's record "
            "$83 IPO fails to revive faith in AI spending.",
            m_body, 456,
        ),
        m_body, INK, 22,
    )
    draw_lines(
        draw, 540, 673,
        wrap(
            "Washington now targets ship-to-ship transfers. Iran "
            "parks 14 tankers at Kharg Island and floats a convoy "
            "to break the blockade.",
            m_body, 440,
        ),
        m_body, INK, 22,
    )
    draw_market_chart(draw)
    draw_tanker(draw)

    draw_rule(draw, 44, 980, 822, 2)

    # ---- Also on 20 November ----
    draw.text(
        (44, 836), "ALSO ON 20 NOVEMBER", font=sans_bold(27), fill=INK
    )
    columns = [
        ("COP31 \u00b7 ANTALYA",
         "Final day: draft drops fossil-fuel phase-out."),
        ("RIYADH",
         "Houthi missile damages PIF Tower in Riyadh."),
        ("ESTONIA",
         "Tallinn to shut road borders with Russia over "
         "\u201csustained aggression\u201d."),
        ("TATARSTAN",
         "Ukraine hits Druzhba oil pipeline station deep "
         "inside Russia."),
    ]
    col_font = serif(17)
    for i, (kicker, text) in enumerate(columns):
        x = 44 + i * 239
        draw.text((x, 874), kicker, font=sans_bold(17), fill=RED)
        draw_lines(
            draw, x, 898, wrap(text, col_font, 219), col_font, INK, 23
        )

    # ---- Footer ----
    draw_rule(draw, 44, 980, 980, 1)
    draw.text(
        (512, 990),
        "20 NOVEMBER 2026 \u00b7 THE WORLD'S NEWS IN ONE IMAGE",
        font=serif_bold(19), fill=(70, 70, 70), anchor="ma",
    )

    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    render(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "assets", "entry.png"))
