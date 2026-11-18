#!/usr/bin/env python3
"""Render the front page for 17 November 2026 world news.

Draws a 1024x1024 newspaper front page with PIL: a big masthead naming
the date, then six illustrated panels, each with a short factual headline
and one supporting line. Run: python3 gen_image.py -> entry.png
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
PAPER = (252, 248, 238)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
INK = (28, 28, 28)
GREY = (90, 90, 86)
SKY = (176, 208, 224)
SEA = (52, 110, 150)
GOLD = (201, 162, 39)
ORANGE = (224, 122, 32)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_MAST = font("DejaVuSans-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 40)
F_SUB = font("DejaVuSans.ttf", 22)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 19)
F_TAG = font("DejaVuSans-Bold.ttf", 17)
F_FOOT = font("DejaVuSans.ttf", 18)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def panel_frame(draw, x, y, w, h, tag, tag_color):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=PAPER, outline=NAVY, width=2)
    # tag ribbon top-left
    tw = draw.textlength(tag, font=F_TAG) + 18
    draw.rounded_rectangle([x, y, x + tw, y + 30], radius=8, fill=tag_color)
    draw.text((x + 9, y + 5), tag, font=F_TAG, fill=(255, 255, 255))
    return x, y, w, h


def headline(draw, x, y, w, text, body=None):
    lines = wrap(draw, text, F_HEAD, w - 16)
    yy = y
    for ln in lines:
        draw.text((x + 8, yy), ln, font=F_HEAD, fill=NAVY)
        yy += 32
    if body:
        blines = wrap(draw, body, F_BODY, w - 16)
        for ln in blines[:2]:
            draw.text((x + 8, yy + 2), ln, font=F_BODY, fill=INK)
            yy += 24
    return yy


# ---- pictograms, each drawn inside a box (bx, by, bw, bh) ----
def pic_bridge(draw, bx, by, bw, bh):
    draw.rectangle([bx, by + bh * 0.62, bx + bw, by + bh], fill=SEA)
    # waves
    for i in range(5):
        wx = bx + 8 + i * (bw - 16) / 5
        draw.arc([wx, by + bh * 0.70, wx + 34, by + bh * 0.86],
                 0, 180, fill=(255, 255, 255), width=3)
    # two bridge towers
    for tx in (bx + bw * 0.18, bx + bw * 0.68):
        draw.rectangle([tx, by + bh * 0.08, tx + 12, by + bh * 0.62],
                       fill=NAVY)
    # deck with a collapsed gap in the middle
    draw.rectangle([bx + 6, by + bh * 0.42, bx + bw * 0.42, by + bh * 0.50],
                   fill=(120, 120, 118))
    draw.rectangle([bx + bw * 0.58, by + bh * 0.42, bx + bw - 6, by + bh * 0.50],
                   fill=(120, 120, 118))
    # falling span piece, tilted
    draw.polygon([(bx + bw * 0.44, by + bh * 0.50),
                  (bx + bw * 0.56, by + bh * 0.52),
                  (bx + bw * 0.54, by + bh * 0.66),
                  (bx + bw * 0.45, by + bh * 0.64)], fill=(150, 60, 50))
    # cables
    draw.line([bx + bw * 0.18 + 6, by + bh * 0.08, bx + bw * 0.42,
               by + bh * 0.42], fill=NAVY, width=2)
    draw.line([bx + bw * 0.68 + 6, by + bh * 0.08, bx + bw * 0.58,
               by + bh * 0.42], fill=NAVY, width=2)
    # smoke puff over the gap
    for cx, cy, r in ((0.50, 0.30, 16), (0.55, 0.24, 12), (0.45, 0.26, 10)):
        draw.ellipse([bx + bw * cx - r, by + bh * cy - r,
                      bx + bw * cx + r, by + bh * cy + r],
                     fill=(200, 200, 196))


def pic_tanker(draw, bx, by, bw, bh):
    draw.rectangle([bx, by + bh * 0.62, bx + bw, by + bh], fill=SEA)
    # hull
    draw.polygon([(bx + 10, by + bh * 0.52), (bx + bw - 10, by + bh * 0.52),
                  (bx + bw - 30, by + bh * 0.70), (bx + 30, by + bh * 0.70)],
                 fill=(140, 40, 36))
    draw.rectangle([bx + bw * 0.30, by + bh * 0.34, bx + bw * 0.42,
                    by + bh * 0.52], fill=(230, 230, 225))
    draw.rectangle([bx + bw * 0.60, by + bh * 0.38, bx + bw * 0.70,
                    by + bh * 0.52], fill=(230, 230, 225))
    # flames above the deck
    for fx, fh in ((0.36, 34), (0.50, 46), (0.65, 30)):
        cx = bx + bw * fx
        draw.polygon([(cx - 14, by + bh * 0.38), (cx, by + bh * 0.38 - fh),
                      (cx + 14, by + bh * 0.38)], fill=ORANGE)
        draw.polygon([(cx - 7, by + bh * 0.38), (cx, by + bh * 0.38 - fh * 0.55),
                      (cx + 7, by + bh * 0.38)], fill=(245, 200, 60))
    # mine in the water
    mx, my = bx + bw * 0.86, by + bh * 0.82
    draw.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=INK)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        draw.line([mx + 10 * math.cos(rad), my + 10 * math.sin(rad),
                   mx + 17 * math.cos(rad), my + 17 * math.sin(rad)],
                  fill=INK, width=3)


def pic_summit(draw, bx, by, bw, bh):
    # three flag poles: US, China, Russia (simplified)
    flags = [((178, 34, 34), "US"), ((200, 30, 30), "CN"),
             ((255, 255, 255), "RU")]
    step = bw / 3
    for i, (col, label) in enumerate(flags):
        fx = bx + i * step + 12
        draw.line([fx + 6, by + 6, fx + 6, by + bh - 8], fill=INK, width=3)
        draw.rectangle([fx + 9, by + 8, fx + step - 14, by + bh * 0.42],
                       fill=col, outline=INK, width=1)
        if label == "US":
            draw.rectangle([fx + 9, by + 8, fx + step * 0.45,
                            by + bh * 0.22], fill=NAVY)
        elif label == "CN":
            draw.text((fx + 14, by + 12), "*", font=F_HEAD, fill=(245, 200, 60))
        else:
            draw.rectangle([fx + 9, by + 8 + (bh * 0.34) / 3,
                            fx + step - 14, by + 8 + 2 * (bh * 0.34) / 3],
                           fill=(30, 60, 160))
        draw.text((fx + 10, by + bh * 0.48), label, font=F_TAG, fill=NAVY)


def pic_rocket(draw, bx, by, bw, bh):
    # sky
    draw.rectangle([bx, by, bx + bw, by + bh], fill=SKY)
    # falling rocket, tilted
    cx, cy = bx + bw * 0.42, by + bh * 0.42
    draw.polygon([(cx - 12, cy - 44), (cx + 12, cy - 44),
                  (cx + 16, cy + 30), (cx - 16, cy + 30)], fill=(230, 230, 225))
    draw.polygon([(cx - 12, cy - 44), (cx, cy - 62), (cx + 12, cy - 44)],
                 fill=RED)
    draw.polygon([(cx - 16, cy + 30), (cx - 30, cy + 52), (cx - 10, cy + 34)],
                 fill=RED)
    draw.polygon([(cx + 16, cy + 30), (cx + 30, cy + 52), (cx + 10, cy + 34)],
                 fill=RED)
    # explosion burst
    ex, ey = bx + bw * 0.72, by + bh * 0.30
    for r, col in ((30, ORANGE), (20, (245, 200, 60)), (10, (255, 240, 180))):
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    # debris dots / lost satellites
    for dx, dy in ((0.15, 0.75), (0.25, 0.85), (0.80, 0.70), (0.88, 0.55)):
        sx, sy = bx + bw * dx, by + bh * dy
        draw.rectangle([sx - 8, sy - 4, sx + 8, sy + 4], fill=NAVY)
        draw.rectangle([sx - 3, sy - 8, sx + 3, sy + 8], fill=NAVY)


def pic_bank(draw, bx, by, bw, bh):
    # bank building with columns
    draw.rectangle([bx + bw * 0.12, by + bh * 0.30, bx + bw * 0.88,
                    by + bh * 0.88], fill=(232, 226, 210))
    draw.polygon([(bx + bw * 0.06, by + bh * 0.30), (bx + bw * 0.50,
                 by + bh * 0.06), (bx + bw * 0.94, by + bh * 0.30)],
                 fill=NAVY)
    for i in range(4):
        cx = bx + bw * (0.22 + i * 0.19)
        draw.rectangle([cx - 10, by + bh * 0.36, cx + 10, by + bh * 0.82],
                       fill=(255, 255, 255), outline=NAVY, width=2)
    draw.rectangle([bx + bw * 0.08, by + bh * 0.88, bx + bw * 0.92,
                    by + bh * 0.96], fill=NAVY)
    # big red X over a bug symbol: "not a cyberattack"
    draw.text((bx + bw * 0.78, by + bh * 0.02), "✕", font=F_HEAD, fill=RED)


def pic_pentagon(draw, bx, by, bw, bh):
    cx, cy = bx + bw * 0.42, by + bh * 0.48
    r = min(bw, bh) * 0.34
    pts = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=(120, 130, 140), outline=NAVY, width=3)
    r2 = r * 0.55
    pts2 = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        pts2.append((cx + r2 * math.cos(a), cy + r2 * math.sin(a)))
    draw.polygon(pts2, fill=PAPER, outline=NAVY, width=2)
    draw.text((cx - 8, cy - 12), "?", font=F_HEAD, fill=RED)
    # audit stamp, bottom-right of the pictogram box
    sx, sy = bx + bw * 0.68, by + bh * 0.86
    draw.rounded_rectangle([sx - 40, sy - 14, sx + 40, sy + 14], radius=6,
                           outline=RED, width=4)
    draw.text((sx - 30, sy - 10), "FAIL", font=F_TAG, fill=RED)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=4)

    # masthead
    text_center(d, 34, "THE WORLD IN ONE DAY", F_MAST, NAVY)
    d.line([40, 118, W - 40, 118], fill=NAVY, width=3)
    text_center(d, 130, "TUESDAY, 17 NOVEMBER 2026", F_DATE, RED)
    d.line([40, 182, W - 40, 182], fill=NAVY, width=3)
    text_center(d, 192, "Ten stories that defined the day — Kyiv to Hormuz to Manila",
                F_SUB, GREY)

    panels = [
        ("WAR", RED, "KERCH BRIDGE HIT AGAIN",
         "Span collapses; Kyiv bridges struck",
         pic_bridge),
        ("GULF", SEA, "TANKERS HIT BY MINES",
         "Two tankers burn off Hormuz",
         pic_tanker),
        ("SUMMIT", GOLD, "TRUMP IN MANILA",
         "Xi–Trump–Putin to meet Thursday",
         pic_summit),
        ("SPACE", NAVY, "VULCAN ROCKET FAILS",
         "40 Amazon satellites lost",
         pic_rocket),
        ("MONEY", (34, 120, 60), "JPMORGAN BLAMES BUG",
         "Bank outage was software, not hackers",
         pic_bank),
        ("USA", (90, 60, 110), "PENTAGON FAILS AUDIT",
         "$4.8 trillion unverified, 9th year",
         pic_pentagon),
    ]
    pw, ph = 480, 208
    gx, gy = 24, 236
    for i, (tag, col, head, body, pic) in enumerate(panels):
        x = gx + (i % 2) * (pw + 8)
        y = gy + (i // 2) * (ph + 10)
        panel_frame(d, x, y, pw, ph, tag, col)
        # pictogram on the left, headline on the right
        pic_w = 170
        pic(d, x + 10, y + 38, pic_w, 158)
        headline(d, x + pic_w + 20, y + 40, pw - pic_w - 28, head, body)
    # bottom strip: four more stories from the same day
    sy = gy + 3 * ph + 2 * 10 + 8
    d.rounded_rectangle([gx, sy, gx + 2 * pw + 8, sy + 92], radius=10,
                        fill=NAVY)
    d.text((gx + 16, sy + 8), "ALSO ON 17 NOVEMBER", font=F_TAG,
           fill=(245, 200, 60))
    also = ["ESTONIA TO SHUT RUSSIA BORDER 1 DEC",
            "5 EU STATES PLAN RWANDA HUB",
            "NVIDIA: FIRST EARNINGS SINCE HUANG EXIT",
            "13 US BABIES BORN WITH MEASLES"]
    f_also = font("DejaVuSans-Bold.ttf", 16)
    for j, item in enumerate(also):
        ix = gx + 16 + (j % 2) * 486
        iy = sy + 36 + (j // 2) * 26
        d.text((ix, iy), "•  " + item, font=f_also, fill=(255, 255, 255))
    return img


if __name__ == "__main__":
    im = build()
    im.save("entry.png", optimize=True)
    print("saved entry.png", im.size)
