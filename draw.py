#!/usr/bin/env python3
"""The World Today — front page for Wednesday 18 November 2026 (v4).

Drawn from scratch with Pillow. Design goal: READABLE AT 300px.
Big type, one-line briefs, white space, strong hierarchy. No photo, no
network, no randomness: the same code always renders the same bytes.

Layout (1024 x 1024):
  masthead 0-96 | UTC timeline 98-136 | lead 136-328 | medium 2x2 328-512
  art briefs 512-640 | day in numbers 640-676 | brief grid 676-986 | footer 986-1024
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

W, H = 1024, 1024
PAPER = (253, 252, 248)
INK = (17, 17, 17)
INK_SOFT = (58, 58, 58)
GREY = (128, 128, 128)
RULE = (200, 200, 196)
RED = (169, 28, 28)
RED_SOFT = (214, 84, 84)
NAVY = (30, 58, 95)
NAVY_SOFT = (226, 232, 240)
BLUE = (37, 99, 235)
TEAL = (13, 148, 136)
GOLD = (180, 130, 29)
GREEN = (22, 101, 52)
SKY = (186, 218, 238)
SEA = (147, 190, 214)

_font_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(os.path.join(FONTS, name), size)
    return _font_cache[key]


def F_display(size):
    return font("Gloock-Regular.ttf", size)


def F_head(size):
    return font("Lora-Bold.ttf", size)


def F_serif(size):
    return font("Lora-Regular.ttf", size)


def F_italic(size):
    return font("Lora-Italic.ttf", size)


def F_sans(size):
    return font("InstrumentSans-Regular.ttf", size)


def F_sans_b(size):
    return font("InstrumentSans-Bold.ttf", size)


def F_mono(size):
    return font("JetBrainsMono-Regular.ttf", size)


def F_mono_b(size):
    return font("JetBrainsMono-Bold.ttf", size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, color, max_w, line_h, max_lines=None):
    lines = wrap(draw, s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=color)
        y += line_h
    return y


def rule(draw, x0, x1, y, color=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker(draw, x, y, s, size=16, color=RED):
    draw.text((x, y), s, font=F_sans_b(size), fill=color)


# ---------------------------------------------------------------- illustrations
# Every illustration is a small code drawing: flat shapes, no photos.

def draw_skyline(d, x0, y0, x1, y1):
    """Shenzhen skyline at dusk with three flags. Box (x0,y0)-(x1,y1)."""
    d.rectangle([x0, y0, x1, y1], fill=(250, 226, 196))
    # sky band
    d.rectangle([x0, y0, x1, y0 + (y1 - y0) * 0.45], fill=(253, 213, 170))
    sun_cx, sun_cy = x0 + (x1 - x0) * 0.72, y0 + (y1 - y0) * 0.22
    sun_r = (y1 - y0) * 0.13
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=(214, 84, 40))
    # towers, back row
    bw = (x1 - x0) / 9.0
    heights = [0.42, 0.58, 0.50, 0.72, 0.62, 0.46, 0.66, 0.55, 0.40]
    for i, hh in enumerate(heights):
        bx = x0 + i * bw
        top = y1 - (y1 - y0) * hh
        d.rectangle([bx + 2, top, bx + bw - 2, y1], fill=(96, 110, 128))
    # front row, darker, with lit windows
    heights2 = [0.30, 0.38, 0.28, 0.44, 0.36, 0.30, 0.40, 0.34, 0.26]
    for i, hh in enumerate(heights2):
        bx = x0 + i * bw
        top = y1 - (y1 - y0) * hh
        d.rectangle([bx + 1, top, bx + bw - 1, y1], fill=(52, 64, 80))
        for wy in range(int(top) + 6, int(y1) - 4, 12):
            for wx in range(int(bx) + 4, int(bx + bw) - 4, 9):
                if (wx * 7 + wy * 13) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 204, 92))
    # tallest tower spire
    tx = x0 + 3.5 * bw
    d.polygon([(tx, y1 - (y1 - y0) * 0.72), (tx + bw * 0.5, y1 - (y1 - y0) * 0.88),
               (tx + bw, y1 - (y1 - y0) * 0.72)], fill=(52, 64, 80))
    # three flags on poles above the skyline
    flag_cols = [(169, 28, 28), (30, 58, 95), (22, 101, 52)]
    for i, fc in enumerate(flag_cols):
        px = x0 + (i + 1) * (x1 - x0) / 4.0
        d.line([(px, y0 + 6), (px, y0 + 26)], fill=INK, width=2)
        d.polygon([(px, y0 + 6), (px + 16, y0 + 10), (px, y0 + 14)], fill=fc)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_gulf_map(d, x0, y0, x1, y1):
    """Stylised Gulf: sea, land, Hormuz strait, burst at Qeshm."""
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    # land masses
    d.polygon([(x0, y0), (x0 + (x1 - x0) * 0.55, y0), (x0 + (x1 - x0) * 0.42, y0 + (y1 - y0) * 0.42),
               (x0 + (x1 - x0) * 0.30, y0 + (y1 - y0) * 0.30), (x0, y0 + (y1 - y0) * 0.22)], fill=(226, 214, 178))
    d.polygon([(x1, y1), (x1, y0 + (y1 - y0) * 0.55), (x0 + (x1 - x0) * 0.72, y0 + (y1 - y0) * 0.62),
               (x0 + (x1 - x0) * 0.60, y1), (x1, y1)], fill=(226, 214, 178))
    # gulf water shape
    d.polygon([(x0 + (x1 - x0) * 0.30, y0 + (y1 - y0) * 0.30),
               (x0 + (x1 - x0) * 0.42, y0 + (y1 - y0) * 0.42),
               (x0 + (x1 - x0) * 0.72, y0 + (y1 - y0) * 0.62),
               (x0 + (x1 - x0) * 0.60, y1), (x0, y1),
               (x0, y0 + (y1 - y0) * 0.22)], fill=(147, 190, 214))
    # Hormuz strait pinch
    sx = x0 + (x1 - x0) * 0.66
    sy = y0 + (y1 - y0) * 0.60
    d.line([(sx - 8, sy - 14), (sx + 8, sy + 14)], fill=INK, width=2)
    d.text((sx - 26, sy + 16), "HORMUZ", font=F_sans_b(9), fill=INK)
    # burst at Qeshm island
    bx, by = x0 + (x1 - x0) * 0.52, y0 + (y1 - y0) * 0.48
    for r, c in [(16, (250, 204, 92)), (11, (214, 84, 40)), (6, (169, 28, 28))]:
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=c)
    d.text((x0 + 4, y0 + 3), "GULF", font=F_sans_b(10), fill=INK)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_senate_bars(d, x0, y0, x1, y1):
    """Senate 56-44 split bars."""
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    mid = x0 + (x1 - x0) * 0.56
    d.rectangle([x0 + 4, y0 + 10, mid - 2, y1 - 6], fill=BLUE)
    d.rectangle([mid + 2, y0 + 10, x1 - 4, y1 - 6], fill=RED)
    d.text((x0 + 12, y0 + 18), "56", font=F_sans_b(22), fill=(255, 255, 255))
    d.text((mid + 12, y0 + 18), "44", font=F_sans_b(22), fill=(255, 255, 255))
    d.text((x0 + 12, y1 - 22), "DEM", font=F_sans_b(11), fill=(255, 255, 255))
    d.text((x1 - 34, y1 - 22), "GOP", font=F_sans_b(11), fill=(255, 255, 255))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_cyclone(d, x0, y0, x1, y1):
    """Cyclone spiral over a coast line."""
    d.rectangle([x0, y0, x1, y1], fill=(219, 234, 245))
    cx, cy = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.48
    # spiral arms
    import math
    for arm in range(3):
        pts = []
        for t in range(0, 101):
            ang = math.radians(t * 3.6 + arm * 120)
            r = 4 + t * 0.32
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.85))
        d.line(pts, fill=NAVY, width=4)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255), outline=NAVY, width=2)
    # coast
    d.polygon([(x0, y1), (x0 + (x1 - x0) * 0.35, y1 - (y1 - y0) * 0.22),
               (x1, y1 - (y1 - y0) * 0.10), (x1, y1)], fill=(226, 214, 178))
    d.text((x0 + 4, y0 + 3), "INDIA", font=F_sans_b(10), fill=INK)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_btc_chart(d, x0, y0, x1, y1):
    """Bitcoin weekly slide: falling line, $62,387 marker."""
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    # grid
    for gy in range(1, 4):
        yy = y0 + (y1 - y0) * gy / 4.0
        d.line([(x0 + 4, yy), (x1 - 4, yy)], fill=RULE, width=1)
    pts = [(0.05, 0.18), (0.20, 0.24), (0.35, 0.22), (0.50, 0.38),
           (0.65, 0.52), (0.80, 0.66), (0.95, 0.82)]
    xy = [(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)) for fx, fy in pts]
    d.line(xy, fill=RED, width=4)
    for px, py in xy:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.text((x0 + 4, y0 + 3), "BTC $62,387", font=F_sans_b(12), fill=RED)
    d.text((x0 + 4, y1 - 16), "−12% WEEK", font=F_mono_b(10), fill=INK_SOFT)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_kerch(d, x0, y0, x1, y1):
    """Broken bridge span over a strait."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    # sea
    d.rectangle([x0, y0 + (y1 - y0) * 0.62, x1, y1], fill=SEA)
    # deck, left and right, middle span dropped
    deck_y = y0 + (y1 - y0) * 0.42
    d.rectangle([x0, deck_y, x0 + (x1 - x0) * 0.38, deck_y + 6], fill=INK)
    d.rectangle([x0 + (x1 - x0) * 0.62, deck_y, x1, deck_y + 6], fill=INK)
    # fallen span, tilted into the water
    fx0 = x0 + (x1 - x0) * 0.40
    d.polygon([(fx0, deck_y + 4), (fx0 + (x1 - x0) * 0.20, deck_y + 26),
               (fx0 + (x1 - x0) * 0.20, deck_y + 32), (fx0, deck_y + 10)], fill=(90, 90, 90))
    # pylons
    for px in (0.18, 0.82):
        x = x0 + (x1 - x0) * px
        d.rectangle([x - 3, y0 + (y1 - y0) * 0.18, x + 3, deck_y + 6], fill=INK)
    # smoke
    sx, sy = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.30
    d.ellipse([sx - 12, sy - 8, sx + 12, sy + 8], fill=(200, 200, 200))
    d.ellipse([sx - 6, sy - 14, sx + 10, sy - 2], fill=(220, 220, 220))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_ebola_dots(d, x0, y0, x1, y1):
    """Eleven dots for 11,000 cases; eight red, three navy."""
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    n = 11
    cols = 6
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / 2
    for i in range(n):
        r, c = divmod(i, cols)
        cx = x0 + c * cw + cw / 2
        cy = y0 + r * ch + ch / 2
        col = RED if i < 8 else NAVY
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=col)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_dow_chart(d, x0, y0, x1, y1):
    """Dow down, Nvidia up: two bars."""
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    base = y1 - 20
    # Dow bar down (red, below a zero line)
    zero = y0 + (y1 - y0) * 0.42
    d.line([(x0 + 4, zero), (x1 - 4, zero)], fill=INK, width=2)
    d.rectangle([x0 + 12, zero, x0 + 52, zero + (y1 - y0) * 0.38], fill=RED)
    # Nvidia bar up (green)
    d.rectangle([x0 + 66, zero - (y1 - y0) * 0.30, x0 + 106, zero], fill=GREEN)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_rocket(d, x0, y0, x1, y1):
    """Anthropic debut: rising arrow over a chart line."""
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    # rising line
    pts = [(0.08, 0.78), (0.28, 0.66), (0.48, 0.70), (0.68, 0.44), (0.88, 0.20)]
    xy = [(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)) for fx, fy in pts]
    d.line(xy, fill=TEAL, width=4)
    for px, py in xy:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=TEAL)
    # arrow head
    ax, ay = xy[-1]
    d.polygon([(ax, ay - 12), (ax - 9, ay + 2), (ax + 9, ay + 2)], fill=TEAL)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_voyager(d, x0, y0, x1, y1):
    """Voyager 1: sun, distance line, small probe."""
    d.rectangle([x0, y0, x1, y1], fill=(16, 24, 48))
    # sun
    sx, sy = x0 + (x1 - x0) * 0.16, y0 + (y1 - y0) * 0.55
    d.ellipse([sx - 12, sy - 12, sx + 12, sy + 12], fill=(250, 204, 92))
    # stars
    for i, (fx, fy) in enumerate([(0.35, 0.2), (0.55, 0.3), (0.75, 0.15), (0.45, 0.75), (0.85, 0.6)]):
        px, py = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255))
    # distance line
    ex, ey = x0 + (x1 - x0) * 0.86, y0 + (y1 - y0) * 0.42
    d.line([(sx + 12, sy), (ex, ey)], fill=(150, 170, 200), width=1)
    # probe: dish + body
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], outline=(255, 255, 255), width=2)
    d.rectangle([ex - 2, ey - 2, ex + 14, ey + 2], fill=(255, 255, 255))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_cricket(d, x0, y0, x1, y1):
    """Cricket bat and ball spot."""
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    # bat
    d.polygon([(x0 + 8, y1 - 4), (x0 + 16, y1 - 4), (x0 + 26, y0 + 10), (x0 + 18, y0 + 6)],
              fill=(180, 130, 60))
    d.rectangle([x0 + 22, y0 + 2, x0 + 27, y0 + 12], fill=INK)
    # ball
    bx, by = x0 + (x1 - x0) * 0.68, y0 + (y1 - y0) * 0.62
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED)
    d.arc([bx - 7, by - 7, bx + 7, by + 7], 200, 340, fill=(255, 255, 255), width=1)


def draw_darts(d, x0, y0, x1, y1):
    """Dartboard spot."""
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    cx, cy = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
    r = min(x1 - x0, y1 - y0) / 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    d.ellipse([cx - r * 0.68, cy - r * 0.68, cx + r * 0.68, cy + r * 0.68], fill=(255, 255, 255))
    d.ellipse([cx - r * 0.38, cy - r * 0.38, cx + r * 0.38, cy + r * 0.38], fill=RED)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GREEN)

# ---------------------------------------------------------------- sections

MX = 28            # side margin
CW = W - 2 * MX    # content width = 968


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=RED, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=RED, width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=RED, width=2)


def masthead(d):
    draw_globe(d, MX + 24, 30, 21)
    title = "THE WORLD TODAY"
    f = F_display(48)
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2, 2), title, font=f, fill=INK)
    # folio row
    fy = 58
    d.text((MX, fy), "WEDNESDAY, 18 NOVEMBER 2026", font=F_sans_b(13), fill=INK)
    mid = "INTERNATIONAL EDITION"
    d.text(((W - d.textlength(mid, font=F_sans_b(13))) / 2, fy), mid,
           font=F_sans_b(13), fill=INK_SOFT)
    right = "No. 322 — PRICE $2.50"
    d.text((W - MX - d.textlength(right, font=F_sans_b(13)), fy), right,
           font=F_sans_b(13), fill=INK)
    # count bar
    count = "41 STORIES  ·  7 REGIONS  ·  13 DRAWN ILLUSTRATIONS"
    cf = F_sans_b(14)
    d.text(((W - d.textlength(count, font=cf)) / 2, 74), count, font=cf, fill=RED)
    rule(d, 0, W, 90, INK, 3)
    rule(d, 0, W, 94, RED, 1)


def timeline(d):
    d.rectangle([0, 96, W, 136], fill=NAVY)
    label = "UTC TIMELINE"
    lf = F_sans_b(13)
    lx = 16
    d.text((lx, 109), label, font=lf, fill=(250, 204, 92))
    stops = [
        ("MORNING", "Xi hugs Trump"),
        ("AFTERNOON", "Jets hit Qeshm"),
        ("19:00", "Fed minutes"),
        ("21:17", "BTC $62,387"),
    ]
    # lay stops out left to right after the label; shrink font if needed
    size = 13
    while size >= 11:
        mf, bf = F_mono(size), F_mono_b(size)
        total = 0
        for tag, txt in stops:
            total += d.textlength(tag + "  ", font=bf) + d.textlength(txt, font=mf) + 26
        if lx + d.textlength(label, font=lf) + 24 + total <= W - 12:
            break
        size -= 1
    x = lx + d.textlength(label, font=lf) + 24
    for tag, txt in stops:
        d.text((x, 109), tag, font=bf, fill=(250, 204, 92))
        x += d.textlength(tag + "  ", font=bf)
        d.text((x, 109), txt, font=mf, fill=(255, 255, 255))
        x += d.textlength(txt, font=mf) + 26
        if tag != stops[-1][0]:
            d.text((x - 18, 109), "•", font=mf, fill=(150, 170, 200))


def lead(d):
    x0, x1 = MX, 640
    y = 144
    kicker(d, x0, y, "SUMMIT IN SHENZHEN", 17)
    y += 26
    d.text((x0, y), "XI HUGS TRUMP", font=F_head(40), fill=INK)
    y += 46
    d.text((x0, y), "IN SHENZHEN", font=F_head(40), fill=INK)
    y += 48
    dek = ("First-ever Trump–Xi–Putin summit set for Thursday; "
           "the U.S.–China tariff truce runs to 10 January.")
    y = draw_wrapped(d, x0, y, dek, F_italic(20), INK_SOFT, x1 - x0, 23, max_lines=2)
    y += 2
    # hand-drawn checkmark: the ✓ glyph is missing from JetBrainsMono (tofu)
    cx, cy = x0, y + 8
    d.line([(cx, cy), (cx + 4, cy + 5), (cx + 11, cy - 4)], fill=GREEN, width=2)
    d.text((x0 + 16, y), "DATE-CHECKED  ·  REUTERS / AFP / AP", font=F_mono_b(12), fill=GREEN)
    # hero illustration, right
    ix0, ix1 = 656, W - MX
    iy0, iy1 = 144, 290
    draw_skyline(d, ix0, iy0, ix1, iy1)
    cap = "Shenzhen: Xi met Trump on the tarmac; Putin joined at the APEC banquet."
    draw_wrapped(d, ix0, iy1 + 6, cap, F_italic(11), INK_SOFT, ix1 - ix0, 13, max_lines=2)
    rule(d, MX, W - MX, 328, INK, 2)


def medium_cell(d, x0, y0, w, illo_fn, head, dek, tag):
    ih = 84
    ix0, ix1 = x0, x0 + 112
    iy0, iy1 = y0, y0 + ih
    illo_fn(d, ix0, iy0, ix1, iy1)
    tx = x0 + 124
    tw = w - 124
    # region kicker on top, headline under it, dek below
    d.text((tx, y0 + 1), tag, font=F_sans_b(11), fill=RED)
    size = 23
    while size >= 19:
        if d.textlength(head, font=F_head(size)) <= tw:
            break
        size -= 1
    d.text((tx, y0 + 14), head, font=F_head(size), fill=INK)
    draw_wrapped(d, tx, y0 + 14 + size + 5, dek, F_serif(17), INK_SOFT, tw, 20, max_lines=2)


def mediums(d):
    col_w = (CW - 16) // 2
    row_h = 84
    y0 = 336
    medium_cell(d, MX, y0, col_w, draw_gulf_map, "GULF UNDER FIRE",
                "U.S. jets hit a Guard missile site on Qeshm after drones "
                "target Bahrain and Kuwait.", "MIDDLE EAST")
    medium_cell(d, MX + col_w + 16, y0, col_w, draw_senate_bars, "PELTOLA TAKES ALASKA",
                "Democrat unseats Sullivan; the Senate goes 56–44, "
                "a nine-seat gain.", "AMERICAS")
    medium_cell(d, MX, y0 + row_h + 8, col_w, draw_cyclone, "CYCLONE AKVAN NEARS INDIA",
                "Landfall on the Andhra coast Friday; winds 130 km/h, "
                "gusts to 145.", "ASIA")
    medium_cell(d, MX + col_w + 16, y0 + row_h + 8, col_w, draw_btc_chart,
                "BITCOIN SINKS", "BTC −3.8% to $62,387; a 12% weekly plunge as "
                "Fed minutes lift hike odds.", "MARKETS")
    rule(d, MX, W - MX, 512, INK, 2)


def art_band(d):
    n = 5
    gutter = 10
    cw = (CW - gutter * (n - 1)) // n
    cards = [
        (draw_kerch, "KERCH SPAN FALLS",
         "Second-day strike; the road deck drops into the strait."),
        (draw_ebola_dots, "EBOLA TOPS 11,000",
         "Congo toll passes 5,400; 3 in 4 sick children under five die."),
        (draw_dow_chart, "DOW −849, NVIDIA BEATS",
         "Chipmaker posts $115.8bn revenue as stocks slide."),
        (draw_rocket, "ANTHROPIC EYES $1.5TN",
         "Claude-maker valued up to $1.5tn ahead of listing."),
        (draw_voyager, "VOYAGER 1: ONE LIGHT-DAY",
         "First human object 25.9bn km from Earth."),
    ]
    y0 = 520
    for i, (fn, head, dek) in enumerate(cards):
        x0 = MX + i * (cw + gutter)
        x1 = x0 + cw
        fn(d, x0, y0, x1, y0 + 54)
        hy = y0 + 58
        lines = wrap(d, head, F_head(15), cw)
        for ln in lines[:2]:
            d.text((x0, hy), ln, font=F_head(15), fill=INK)
            hy += 15
        draw_wrapped(d, x0, hy + 2, dek, F_serif(12), INK_SOFT, cw, 12, max_lines=2)
    rule(d, MX, W - MX, 640, INK, 2)


def numbers_strip(d):
    d.text((MX, 650), "DAY IN NUMBERS", font=F_sans_b(14), fill=RED)
    nums = "DOW −849  ·  NVIDIA $115.8B  ·  BTC $62,387  ·  EBOLA 11,000  ·  SENATE 56–44"
    size = 16
    while size >= 12:
        if d.textlength(nums, font=F_mono_b(size)) <= (W - MX) - (MX + 150):
            break
        size -= 1
    d.text((MX + 150, 648), nums, font=F_mono_b(size), fill=INK)
    rule(d, MX, W - MX, 676, INK, 2)


def brief_line(d, x, y, w, text, spot=None):
    """One-line brief headline, shortened in code to fit the column."""
    tx = x
    if spot is not None:
        spot(d, x, y - 1, x + 22, y + 21)
        tx = x + 28
    avail = (x + w) - tx
    s = text
    while s and d.textlength(s, font=F_serif(15)) > avail:
        s = s.rsplit(" ", 1)[0]
    if s != text:
        s = s.rstrip(",;") + "…"
    d.text((tx, y), s, font=F_serif(15), fill=INK)


def region_header(d, x, y, w, name):
    d.text((x, y), name, font=F_sans_b(14), fill=RED)
    rule(d, x, x + w, y + 19, RULE, 1)


# (column, kind, text, spot) — kind "H" = region header, "B" = brief
GRID = [
    (0, "H", "ASIA", None),
    (0, "B", "Quad meets in Manila, first in two years", None),
    (0, "B", "Hundreds arrested in anti-Trump protests", None),
    (0, "B", "India condemns tanker attack in Hormuz", None),
    (0, "B", "India beats Pakistan 2–1, 10th SAFF title", None),
    (0, "B", "Dhoni retires, becomes CSK mentor", None),
    (0, "B", "Bombers near Japan; Taiwan logs sorties", None),
    (0, "B", "EU and Indonesia approve trade deal signing", None),
    (0, "H", "OCEANIA", None),
    (0, "B", "Duckett's 133 seals England win", draw_cricket),
    (0, "B", "Dunkley's 72 powers Sixers to WBBL win", None),
    (0, "B", "India fined for slow over-rate in NZ ODI", None),
    (0, "B", "Bancroft: team knew of sandpaper plot", None),
    (1, "H", "EUROPE", None),
    (1, "B", "EU proposes €45bn Ukraine loan for 2027", None),
    (1, "B", "EU halts UK talks until Brexit U-turn", None),
    (1, "B", "Littler stunned by Wattimena", draw_darts),
    (1, "B", "Zverev into ATP Finals semis", None),
    (1, "B", "Plane crashes in Siberia, 19 killed", None),
    (1, "H", "AMERICAS", None),
    (1, "B", "Measles-free status lost after 26 years", None),
    (1, "B", "Musk slams record midterm spending", None),
    (1, "B", "Hegseth makes surprise trip to Venezuela", None),
    (1, "B", "Bukele confirms airstrike on gang mansion", None),
    (1, "B", "Panama: 2nd arrest in journalist attack", None),
    (2, "H", "MIDDLE EAST", None),
    (2, "B", "Board of Peace faults both sides on Gaza", None),
    (2, "B", "Israeli raid displaces more Gazans", None),
    (2, "B", "WHO: 950,000 displaced in flood zones", None),
    (2, "B", "Knesset elects Matan Kahana as speaker", None),
    (2, "H", "AFRICA", None),
    (2, "B", "Mondlane goes on trial in Mozambique", None),
    (2, "B", "Senegal's Faye excluded from ruling party", None),
    (2, "B", "Lookman out for rest of 2026, knee injury", None),
    (2, "B", "Zimbabwe take Test series over Afghanistan", None),
    (2, "H", "GLOBAL", None),
    (2, "B", "Suno adds AI visuals and video for songs", None),
    (2, "B", "WhatsApp adds cloud backups for Android", None),
]


def brief_grid(d):
    col_w = (CW - 24) // 3
    row_h = 23
    y0 = 684
    counts = [0, 0, 0]
    for col, kind, text, spot in GRID:
        x = MX + col * (col_w + 12)
        y = y0 + counts[col] * row_h
        if kind == "H":
            region_header(d, x, y, col_w, text)
        else:
            brief_line(d, x, y, col_w, text, spot)
        counts[col] += 1
    rule(d, MX, W - MX, 986, INK, 2)


def footer(d):
    line1 = "ILLUSTRATIONS ARE ORIGINAL DRAWINGS, NOT PHOTOGRAPHS."
    line2 = "DATE-CHECKED 18 NOVEMBER 2026  ·  41 STORIES  ·  7 REGIONS  ·  13 DRAWN"
    f1, f2 = F_sans_b(12), F_sans(11)
    d.text(((W - d.textlength(line1, font=f1)) / 2, 994), line1, font=f1, fill=INK)
    d.text(((W - d.textlength(line2, font=f2)) / 2, 1010), line2, font=f2, fill=INK_SOFT)


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    timeline(d)
    lead(d)
    mediums(d)
    art_band(d)
    numbers_strip(d)
    brief_grid(d)
    footer(d)
    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    render(os.path.join(HERE, "entry.png"))
    print("rendered", os.path.join(HERE, "entry.png"))
