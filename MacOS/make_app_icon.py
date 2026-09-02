#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS uygulama ikonu üreticisi (AppIcon.icns)
=============================================

Projedeki images/ToDo.ico yalnızca 32x32 olduğu için Retina ekranlarda
bulanık kalıyor. Bu betik, uygulamanın kendi "Şeftali" tema paletiyle
1024x1024 vektörel keskinlikte bir defter/checklist ikonu çizer ve
macOS'un istediği tüm boyutları içeren AppIcon.icns dosyasını üretir.

Kullanim:  MacOS/.venv/bin/python MacOS/make_app_icon.py
"""

import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ICNS_OUT = os.path.join(HERE, "AppIcon.icns")

# ToDoList.py "Şeftali" temasindan alinan renkler
BG_TOP     = (247, 237, 227)   # kremimsi ust
BG_BOTTOM  = (240, 220, 203)   # kremimsi alt
CARD       = (253, 248, 243)
CARD_EDGE  = (229, 196, 176)
ACCENT     = (217, 107, 67)    # #D96B43 terracotta
ACCENT_SOFT= (244, 179, 146)   # #F4B392
TEXT_LINE  = (204, 180, 162)
SHADOW     = (150, 104, 76)

S = 2048           # supersample çözünürlüğü (1024'e küçültülecek)
PAD = int(S * 0.09)
RADIUS = int(S * 0.225)


def _vertical_gradient(size, top, bottom):
    grad = Image.new("RGB", (1, size), top)
    px = grad.load()
    for y in range(size):
        t = y / max(1, size - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return grad.resize((size, size))


def draw_icon():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # --- Squircle gövde (macOS tarzı yuvarlak kare) ---
    body = [PAD, PAD, S - PAD, S - PAD]
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle(body, radius=RADIUS, fill=255)
    img.paste(_vertical_gradient(S, BG_TOP, BG_BOTTOM), (0, 0), mask)

    # ince ic kenar
    d.rounded_rectangle(body, radius=RADIUS, outline=CARD_EDGE + (110,), width=int(S * 0.006))

    # --- Defter karti ---
    cw, ch = int(S * 0.585), int(S * 0.585)
    cx, cy = (S - cw) // 2, int(S * 0.255)
    card = [cx, cy, cx + cw, cy + ch]
    card_r = int(S * 0.045)

    # yumusak golge
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [card[0], card[1] + int(S * 0.018), card[2], card[3] + int(S * 0.018)],
        radius=card_r, fill=SHADOW + (46,))
    img.alpha_composite(sh)

    d.rounded_rectangle(card, radius=card_r, fill=CARD, outline=CARD_EDGE, width=int(S * 0.005))

    # --- Ust klips (clipboard) ---
    clw, clh = int(cw * 0.42), int(S * 0.075)
    clx = cx + (cw - clw) // 2
    cly = cy - clh // 2
    d.rounded_rectangle([clx, cly, clx + clw, cly + clh],
                        radius=clh // 2, fill=ACCENT)
    d.rounded_rectangle([clx + clw // 4, cly - int(clh * 0.42),
                         clx + clw - clw // 4, cly + clh // 2],
                        radius=int(clh * 0.34), fill=ACCENT_SOFT)

    # --- Gorev satirlari ---
    rows = 3
    box = int(S * 0.072)
    left = cx + int(cw * 0.12)
    line_x0 = left + box + int(S * 0.045)
    line_x1 = cx + cw - int(cw * 0.12)
    first_y = cy + int(ch * 0.28)
    gap = int(ch * 0.235)

    for i in range(rows):
        y = first_y + i * gap
        checked = i < 2

        # kutucuk
        d.rounded_rectangle([left, y, left + box, y + box],
                            radius=int(box * 0.28),
                            fill=ACCENT if checked else (0, 0, 0, 0),
                            outline=ACCENT if checked else CARD_EDGE,
                            width=int(S * 0.006))
        if checked:
            d.line([(left + box * 0.24, y + box * 0.52),
                    (left + box * 0.44, y + box * 0.72),
                    (left + box * 0.78, y + box * 0.28)],
                   fill=CARD, width=int(S * 0.012), joint="curve")

        # satir cizgisi
        lh = int(S * 0.020)
        x1 = line_x1 if i != rows - 1 else line_x1 - int(cw * 0.22)
        d.rounded_rectangle([line_x0, y + box // 2 - lh // 2, x1, y + box // 2 + lh // 2],
                            radius=lh // 2,
                            fill=ACCENT_SOFT if checked else TEXT_LINE)

    return img.resize((1024, 1024), Image.LANCZOS)


def main():
    icon = draw_icon()
    iconset = os.path.join(HERE, "AppIcon.iconset")
    shutil.rmtree(iconset, ignore_errors=True)
    os.makedirs(iconset)

    for size in (16, 32, 128, 256, 512):
        icon.resize((size, size), Image.LANCZOS).save(
            os.path.join(iconset, f"icon_{size}x{size}.png"))
        icon.resize((size * 2, size * 2), Image.LANCZOS).save(
            os.path.join(iconset, f"icon_{size}x{size}@2x.png"))

    res = subprocess.run(["iconutil", "-c", "icns", iconset, "-o", ICNS_OUT],
                         capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        sys.exit(1)
    shutil.rmtree(iconset, ignore_errors=True)
    print(f"OK -> {ICNS_OUT} ({os.path.getsize(ICNS_OUT)} bayt)")


if __name__ == "__main__":
    main()
