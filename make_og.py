#!/usr/bin/env python3
"""
Moratine Open Graph image generator.

Produces og-image.png at 1200x630, the size Twitter, iMessage, Slack and
Facebook all crop from.

Requirements:
    pip install pillow

Usage:
    python make_og.py

Output:
    ./og-image.png

The card carries the argument in one line rather than the app name. A link
preview is usually the only thing someone sees before deciding whether to
click, and "Moratine" tells them nothing on its own.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SIZE = (1200, 630)
OUT = "og-image.png"

CREAM = (0xF8, 0xF5, 0xF0)
INK = (0x1A, 0x17, 0x15)
FAINT = (0x8A, 0x80, 0x78)

# Ochre, the stage the fixtures land in and the app's most recognisable face.
OCHRE_TOP = (0xA8, 0x86, 0x3B)
OCHRE_BOTTOM = (0xCB, 0xA9, 0x5F)

FRAUNCES = os.path.expanduser(
    "~/Developer/App Development Files/Moratine/Moratine/Moratine/Fonts/"
    "Fraunces_72pt-Regular.ttf"
)
PLEX_MONO = os.path.expanduser(
    "~/Developer/App Development Files/Moratine/Moratine/Moratine/Fonts/"
    "IBMPlexMono-Regular.ttf"
)

ICON = "apple-touch-icon.png"     # optional; skipped if missing

MARGIN = 84
CARD_W = 392
CARD_RADIUS = 26


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def font(path, size, label):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        print(f"  WARNING: could not load {label} at {path}")
        print("  Falling back to a default face. Fix the path before shipping.")
        return ImageFont.load_default(size)


def gradient(size, top, bottom):
    """135 degree linear gradient, matching the app."""
    w, h = size
    xs, ys = np.meshgrid(np.arange(w), np.arange(h))
    t = (xs + ys) / ((w - 1) + (h - 1))
    r = top[0] + (bottom[0] - top[0]) * t
    g = top[1] + (bottom[1] - top[1]) * t
    b = top[2] + (bottom[2] - top[2]) * t
    return Image.fromarray(np.stack([r, g, b], axis=-1).astype(np.uint8), "RGB")


def fit(path, lines, max_width, start_size, label, floor=34):
    """
    Largest size at which every line clears max_width.

    Measured rather than assumed: the headline sits beside a fixed card, and
    a line that overruns it slides underneath rather than wrapping. Different
    faces set at very different widths, so a size that fits one will not
    reliably fit another.
    """
    size = start_size
    while size > floor:
        f = font(path, size, label)
        widest = max(f.getbbox(line)[2] for line in lines)
        if widest <= max_width:
            return f, size
        size -= 2
    return font(path, floor, label), floor


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, img.size[0] - 1, img.size[1] - 1], radius=radius, fill=255
    )
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img.convert("RGB"), (0, 0), mask=mask)
    return out


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------

def main():
    serif_card = font(FRAUNCES, 76, "Fraunces")
    serif_mark = font(FRAUNCES, 30, "Fraunces")
    mono_sm = font(PLEX_MONO, 19, "IBM Plex Mono")

    headline = [
        "Two hours ten minutes",
        "on hold with your insurer.",
    ]

    # The text column runs from the left margin to the card, less a gutter.
    text_width = SIZE[0] - MARGIN - CARD_W - MARGIN - 56
    serif_lg, headline_size = fit(FRAUNCES, headline, text_width, 62, "Fraunces")
    leading = int(headline_size * 1.26)

    canvas = Image.new("RGBA", SIZE, CREAM + (255,))
    draw = ImageDraw.Draw(canvas)

    # --- Left column: the argument -----------------------------------------

    x = MARGIN
    y = MARGIN

    # Wordmark, with the icon beside it when available.
    if os.path.exists(ICON):
        icon = Image.open(ICON).convert("RGBA").resize((46, 46), Image.LANCZOS)
        canvas.alpha_composite(rounded(icon, 11), (x, y))
        draw.text((x + 62, y + 4), "Moratine", font=serif_mark, fill=INK)
    else:
        draw.text((x, y), "Moratine", font=serif_mark, fill=INK)

    # The line that does the work.
    y = 214
    for line in headline:
        draw.text((x, y), line, font=serif_lg, fill=INK)
        y += leading

    draw.text(
        (x, y + 26),
        "A RECORD OF TIME YOU DID NOT CHOOSE",
        font=mono_sm,
        fill=FAINT,
    )

    # --- Right: one gradient card ------------------------------------------

    card_h = SIZE[1] - (MARGIN * 2)
    card_x = SIZE[0] - MARGIN - CARD_W
    card = gradient((CARD_W, card_h), OCHRE_TOP, OCHRE_BOTTOM)
    card = rounded(card, CARD_RADIUS)

    cd = ImageDraw.Draw(card)
    on_gradient = (0, 0, 0, 217)
    on_gradient_soft = (0, 0, 0, 150)

    cd.text((40, 40), "THIS MONTH", font=mono_sm, fill=on_gradient_soft)
    cd.text((40, card_h - 168), "7h 13m", font=serif_card, fill=on_gradient)
    cd.text((40, card_h - 72), "20 WAITS", font=mono_sm, fill=on_gradient_soft)

    canvas.alpha_composite(card, (card_x, MARGIN))

    canvas.convert("RGB").save(OUT)
    print(f"wrote {OUT}  ({SIZE[0]} x {SIZE[1]})")
    print(f"headline set at {headline_size}px to clear the card")
    print("\nCheck it at thumbnail size before shipping. If the headline is")
    print("unreadable in a Slack preview, it is doing nothing.")


if __name__ == "__main__":
    main()
