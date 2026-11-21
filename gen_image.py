#!/usr/bin/env python3
"""Generator for the News Image entry of Saturday 21 November 2026.

Builds one 1024x1024 PNG infographic that sums up the day's world news in
six panels, one per story. Every panel carries a category tag, a headline,
a line or two of context and a small motif drawn with PIL primitives, so
the picture explains itself to a reader who has no news feed.

The output is fully deterministic: fixed layout constants, no clock, no
randomness -- two runs always produce byte-identical PNG files.

Stories (each corroborated by at least two outlets; unconfirmed claims
are hedged as "reported"):
  1. Russian missiles and a drone reported down in Poland during a
     massive strike on Ukraine; at least 8 killed, Kyiv bridges hit.
  2. UK and EU seal a Brexit-reset deal in Brussels (20 Nov).
  3. Denmark accuses Russia of plotting to kill a US-Ukrainian rapper;
     Russia denies it and its defence attache is expelled.
  4. Myanmar calls the ICJ genocide ruling "unfair"; Malaysia plans to
     resettle 10,000 Rohingya refugees in Turkiye.
  5. Anthropic shares slide after its blockbuster IPO as a wider tech
     sell-off drags markets down.
  6. Nikhil Gupta sentenced in New York to 19+ years over a foiled plot
     to assassinate a US-based Sikh separatist leader.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# Layout constants (canvas 1024x1024)
# --------------------------------------------------------------------------
W = H = 1024
MARGIN = 24

BG = (236, 233, 224)          # warm paper
HEADER_BG = (18, 38, 58)      # deep navy
HEADER_FG = (245, 242, 235)
HEADER_SUB = (178, 196, 214)
PANEL_BG = (255, 253, 248)
PANEL_BORDER = (205, 199, 184)
INK = (26, 28, 32)
BODY_INK = (58, 62, 70)

HEADER_Y0, HEADER_Y1 = 24, 124
GRID_Y0, GRID_Y1 = 140, 976
COL_X = (24, 520)
PANEL_W = 480
ROW_GAP = 14
PANEL_H = (GRID_Y1 - GRID_Y0 - 2 * ROW_GAP) // 3   # 269
FOOTER_Y = 990

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(FONT_BOLD, 43)
F_SUBTITLE = font(FONT_SANS, 22)
F_CHIP = font(FONT_BOLD, 15)
F_HEADLINE = font(FONT_BOLD, 25)
F_BODY = font(FONT_SANS, 19)
F_FOOTER = font(FONT_SANS, 15)


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------
def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using real glyph widths."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, xy, text, fnt, fill, max_width, line_step, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_step
    return y


# --------------------------------------------------------------------------
# Motifs -- each drawn inside an 88x88 box whose top-left is (x, y).
# Simple, bold shapes that read at a glance.
# --------------------------------------------------------------------------
def motif_missile(draw, x, y, accent):
    """Missile arcing over a dashed border line into a burst.

    Kept fully inside the 88x88 box: tail at upper left, nose pointing
    down-right across the border dashes, burst at the impact point.
    """
    # dashed border
    for i in range(6):
        yy = y + 8 + i * 13
        draw.line([(x + 56, yy), (x + 56, yy + 6)], fill=accent, width=3)
    # missile body, angled up-left to down-right
    body = [(x + 16, y + 26), (x + 42, y + 46), (x + 49, y + 39),
            (x + 25, y + 18)]
    draw.polygon(body, fill=accent)
    # fins at the tail
    draw.polygon([(x + 18, y + 24), (x + 11, y + 33), (x + 22, y + 33)],
                 fill=accent)
    draw.polygon([(x + 25, y + 18), (x + 18, y + 11), (x + 29, y + 13)],
                 fill=accent)
    # flame at the tail
    draw.polygon([(x + 14, y + 27), (x + 7, y + 36), (x + 20, y + 34)],
                 fill=(232, 145, 42))
    # impact burst on the far side of the border
    cx, cy = x + 70, y + 68
    for ang in range(0, 360, 45):
        dx = int(10 * math.cos(math.radians(ang)))
        dy = int(10 * math.sin(math.radians(ang)))
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=(232, 145, 42),
                  width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=accent)


def motif_deal(draw, x, y, accent):
    """Two overlapping circles: a partnership sealed."""
    draw.ellipse([x + 6, y + 20, x + 54, y + 68], outline=accent, width=4)
    draw.ellipse([x + 34, y + 20, x + 82, y + 68], outline=(232, 145, 42),
                 width=4)
    # small star dots around the right circle (a nod to the EU flag)
    cx, cy = x + 58, y + 44
    for i in range(8):
        ang = math.radians(i * 45)
        sx = cx + int(17 * math.cos(ang))
        sy = cy + int(17 * math.sin(ang))
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(232, 145, 42))
    # link bar under the circles
    draw.rounded_rectangle([x + 26, y + 76, x + 62, y + 84], radius=4,
                           fill=accent)


def motif_microphone(draw, x, y, accent):
    """Microphone with a musical note: the rapper story."""
    # mic capsule
    draw.rounded_rectangle([x + 30, y + 4, x + 52, y + 44], radius=11,
                           fill=accent)
    for yy in (14, 24, 34):
        draw.line([(x + 34, y + yy), (x + 48, y + yy)], fill=(255, 255, 255),
                  width=2)
    # cradle arc + stem + base
    draw.arc([x + 22, y + 22, x + 60, y + 62], start=0, end=180,
             fill=accent, width=4)
    draw.line([(x + 41, y + 62), (x + 41, y + 76)], fill=accent, width=4)
    draw.line([(x + 28, y + 78), (x + 54, y + 78)], fill=accent, width=4)
    # musical note
    draw.ellipse([x + 62, y + 58, x + 74, y + 68], fill=(232, 145, 42))
    draw.line([(x + 73, y + 62), (x + 73, y + 38)], fill=(232, 145, 42),
              width=3)
    draw.polygon([(x + 73, y + 38), (x + 84, y + 42), (x + 73, y + 48)],
                 fill=(232, 145, 42))


def motif_scales(draw, x, y, accent):
    """Scales of justice: the ICJ ruling fallout."""
    cx = x + 44
    # beam and post
    draw.line([(x + 12, y + 18), (x + 76, y + 18)], fill=accent, width=4)
    draw.line([(cx, y + 12), (cx, y + 70)], fill=accent, width=4)
    draw.ellipse([cx - 4, y + 6, cx + 4, y + 14], fill=accent)
    # pans
    for px in (x + 18, x + 70):
        draw.line([(px - 6, y + 18), (px, y + 40)], fill=accent, width=2)
        draw.line([(px + 6, y + 18), (px, y + 40)], fill=accent, width=2)
        draw.arc([px - 13, y + 30, px + 13, y + 52], start=0, end=180,
                 fill=accent, width=3)
    # base
    draw.line([(x + 28, y + 74), (x + 60, y + 74)], fill=accent, width=5)


def motif_chart_down(draw, x, y, accent):
    """Falling bars and a diving arrow: the market slide."""
    base = y + 76
    draw.line([(x + 8, base), (x + 82, base)], fill=accent, width=3)
    heights = (44, 32, 18)
    for i, hgt in enumerate(heights):
        bx = x + 12 + i * 16
        draw.rectangle([bx, base - hgt, bx + 10, base], fill=accent)
    # diving line with arrowhead
    pts = [(x + 14, y + 16), (x + 38, y + 30), (x + 56, y + 26),
           (x + 78, y + 52)]
    draw.line(pts, fill=(179, 49, 42), width=4, joint="curve")
    draw.polygon([(x + 78, y + 52), (x + 64, y + 50), (x + 72, y + 38)],
                 fill=(179, 49, 42))


def _rot_rect(cx, cy, length, thick, ang):
    """Corners of a rectangle centred on (cx, cy), rotated by `ang`."""
    ux, uy = math.cos(ang), math.sin(ang)
    vx, vy = -math.sin(ang), math.cos(ang)
    hl, ht = length / 2, thick / 2
    return [(cx + sx * hl * ux + sy * ht * vx,
             cy + sx * hl * uy + sy * ht * vy)
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def motif_gavel(draw, x, y, accent):
    """A judge's gavel mid-strike over its sound block: the sentencing.

    The handle runs diagonally from lower-right up to a banded head at
    upper-left; orange ticks by the head mark the strike.
    """
    ang = math.radians(-38)
    cx, cy = x + 44, y + 40
    ux, uy = math.cos(ang), math.sin(ang)
    # handle: long and slim, head end toward upper-left
    draw.polygon(_rot_rect(cx, cy, 56, 7, ang), fill=accent)
    # head: block perpendicular to the handle at its upper-left end,
    # with a pale band at each end so it reads as a gavel head
    hx, hy = cx - 26 * ux, cy - 26 * uy
    draw.polygon(_rot_rect(hx, hy, 15, 34, ang), fill=accent)
    vx, vy = -math.sin(ang), math.cos(ang)
    for s in (-1, 1):
        bx, by = hx + s * 13 * vx, hy + s * 13 * vy
        draw.polygon(_rot_rect(bx, by, 16, 7, ang), fill=lighten(accent, 0.45))
    # sound block
    draw.rounded_rectangle([x + 12, y + 72, x + 76, y + 80], radius=3,
                           fill=accent)
    draw.rounded_rectangle([x + 20, y + 66, x + 68, y + 70], radius=2,
                           fill=lighten(accent, 0.45))
    # strike ticks beside the head
    for i in range(3):
        tx = x + 8 + i * 9
        draw.line([(tx, y + 16), (tx + 3, y + 6)], fill=(232, 145, 42),
                  width=3)


# --------------------------------------------------------------------------
# Stories
# --------------------------------------------------------------------------
STORIES = [
    {
        "tag": "UKRAINE WAR",
        "accent": (179, 49, 42),
        "headline": "Russian missiles cross into Poland",
        "body": ("Missiles and a drone reported down in Poland during a "
                 "huge strike on Ukraine: at least 8 dead, Kyiv bridges "
                 "hit, NATO jets scrambled."),
        "motif": motif_missile,
    },
    {
        "tag": "EUROPE",
        "accent": (36, 86, 166),
        "headline": "UK and EU seal Brexit-reset deal",
        "body": ("Signed in Brussels on 20 Nov: easier food trade, carbon "
                 "and youth-mobility deals. A row over student tuition "
                 "fees is still open."),
        "motif": motif_deal,
    },
    {
        "tag": "ESPIONAGE",
        "accent": (107, 63, 160),
        "headline": "Denmark: Russia plotted to kill rapper",
        "body": ("Copenhagen says a US-Ukrainian rapper was the target. "
                 "Russia denies it; Denmark expels Russia's defence "
                 "attache."),
        "motif": motif_microphone,
    },
    {
        "tag": "ASIA",
        "accent": (15, 118, 110),
        "headline": "Myanmar calls genocide ruling 'unfair'",
        "body": ("Fallout from the ICJ verdict: Malaysia plans to "
                 "resettle 10,000 Rohingya refugees in Turkiye."),
        "motif": motif_scales,
    },
    {
        "tag": "MARKETS",
        "accent": (180, 83, 9),
        "headline": "Anthropic shares slide after huge IPO",
        "body": ("The AI giant's stock drops as a wider tech sell-off "
                 "drags markets down."),
        "motif": motif_chart_down,
    },
    {
        "tag": "JUSTICE",
        "accent": (124, 74, 45),
        "headline": "19 years for plot to kill Sikh leader",
        "body": ("Nikhil Gupta is sentenced in New York for the foiled "
                 "plot against a US-based Sikh separatist leader."),
        "motif": motif_gavel,
    },
]


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def lighten(rgb, factor=0.88):
    return tuple(int(c + (255 - c) * factor) for c in rgb)


def draw_header(draw):
    draw.rounded_rectangle([MARGIN, HEADER_Y0, W - MARGIN, HEADER_Y1],
                           radius=14, fill=HEADER_BG)
    draw.text((MARGIN + 28, HEADER_Y0 + 14), "THE WORLD TODAY",
              font=F_TITLE, fill=HEADER_FG)
    draw.text((MARGIN + 30, HEADER_Y0 + 68),
              "Saturday 21 November 2026 - the day in six stories",
              font=F_SUBTITLE, fill=HEADER_SUB)


def draw_panel(draw, px, py, story):
    accent = story["accent"]
    draw.rounded_rectangle([px, py, px + PANEL_W, py + PANEL_H], radius=12,
                           fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    # accent spine on the left edge
    draw.rounded_rectangle([px, py, px + 8, py + PANEL_H], radius=4,
                           fill=accent)
    draw.rectangle([px + 4, py + 2, px + 8, py + PANEL_H - 2], fill=accent)

    # category chip
    chip_text = story["tag"]
    chip_w = int(draw.textlength(chip_text, font=F_CHIP)) + 20
    draw.rounded_rectangle([px + 18, py + 14, px + 18 + chip_w, py + 40],
                           radius=8, fill=accent)
    draw.text((px + 28, py + 19), chip_text, font=F_CHIP,
              fill=(255, 255, 255))

    # motif box, top-right
    box = 88
    bx, by = px + PANEL_W - 18 - box, py + 14
    draw.rounded_rectangle([bx, by, bx + box, by + box], radius=12,
                           fill=lighten(accent))
    story["motif"](draw, bx, by, accent)

    # headline beside the motif box; body follows directly under it so
    # short headlines do not leave a dead gap in the panel
    head_end = draw_block(draw, (px + 18, py + 52), story["headline"],
                          F_HEADLINE, INK, PANEL_W - 36 - box - 10, 31,
                          max_lines=3)
    body_y = max(head_end + 12, py + 118)
    draw_block(draw, (px + 18, body_y), story["body"], F_BODY,
               BODY_INK, PANEL_W - 36, 24, max_lines=4)


FOOTER_TEXT = ("Sources: BBC - Helsinki Times - GeoBrowser - Daily Jagran"
               "  |  unconfirmed claims hedged as reported")


def draw_footer(draw):
    tw = draw.textlength(FOOTER_TEXT, font=F_FOOTER)
    draw.text(((W - tw) / 2, FOOTER_Y), FOOTER_TEXT, font=F_FOOTER,
              fill=(110, 104, 90))


def build_image():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        px = COL_X[col]
        py = GRID_Y0 + row * (PANEL_H + ROW_GAP)
        draw_panel(draw, px, py, story)
    draw_footer(draw)
    return img


def write_entry(path):
    """Build the image and write it to `path` as a PNG."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    build_image().save(path, format="PNG")


if __name__ == "__main__":
    write_entry(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "entry.png"))
