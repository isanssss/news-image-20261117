#!/usr/bin/env python3
"""Compose entry.png: a one-page newspaper front page summing up the world
news of Tuesday 17 November 2026.

Build-time only script (uses PIL). The shipped entry program, main.py, is
standard-library only and simply copies the finished entry.png.

Layout: cream paper, serif masthead with the date as the largest text,
a wide lead story, two half-width stories, a wide bottom story and a
dark ticker band with the day's remaining headlines.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT
OUT = ROOT / "entry.png"

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # content width: 968

PAPER = (246, 241, 229)
INK = (22, 22, 22)
NAVY = (15, 27, 53)
WHITE = (245, 245, 240)


def panel(keyword):
    """Find the generated panel PNG whose file name contains keyword."""
    for path in sorted(ASSETS.glob("*.png")):
        if keyword in path.name:
            return Image.open(path).convert("RGB")
    raise FileNotFoundError(keyword)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, max_width, start):
    """Largest size <= start at which text fits max_width on one line."""
    size = start
    while size > 10:
        if draw.textlength(text, font=font(path, size)) <= max_width:
            return size
        size -= 1
    return size


def wrap(draw, text, fnt, max_width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill=INK, tracking=0):
    if tracking:
        widths = [draw.textlength(ch, font=fnt) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (W - total) / 2
        for ch, wch in zip(text, widths):
            draw.text((x, y), ch, font=fnt, fill=fill)
            x += wch + tracking
    else:
        wtext = draw.textlength(text, font=fnt)
        draw.text(((W - wtext) / 2, y), text, font=fnt, fill=fill)


def story(draw, page, x, y, width, img, img_h, headline, subline,
          head_size, sub_size, centering=(0.5, 0.5)):
    """Paste a fitted panel and draw its headline and subline under it.

    Returns the y just below the subline.
    """
    fitted = ImageOps.fit(img, (width, img_h), method=Image.LANCZOS,
                          centering=centering)
    page.paste(fitted, (x, y))
    draw.rectangle([x, y, x + width - 1, y + img_h - 1], outline=INK, width=2)
    y += img_h + 8
    hf = font(SERIF_BOLD, head_size)
    for line in wrap(draw, headline, hf, width):
        draw.text((x, y), line, font=hf, fill=INK)
        y += int(head_size * 1.18)
    y += 2
    sf = font(SANS, sub_size)
    for line in wrap(draw, subline, sf, width):
        draw.text((x, y), line, font=sf, fill=INK)
        y += int(sub_size * 1.25)
    return y


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # ---- Masthead ------------------------------------------------------
    y = 18
    draw.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=INK)
    y += 10
    kicker = "THE WORLD IN ONE DAY"
    kf = font(SERIF_BOLD, 34)
    centered(draw, y, kicker, kf, tracking=6)
    y += 44
    date = "TUESDAY 17 NOVEMBER 2026"
    dsize = fit_font(draw, date, SERIF_BOLD, CW, 66)
    centered(draw, y, date, font(SERIF_BOLD, dsize))
    y += dsize + 12
    draw.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=INK)
    draw.rectangle([MARGIN, y + 6, W - MARGIN, y + 7], fill=INK)
    y += 14

    # ---- Lead story -----------------------------------------------------
    y = story(draw, page, MARGIN, y, CW, panel("bridge"), 170,
              "UKRAINE STRIKES THE KERCH BRIDGE",
              "Crimea\u2013Russia link partly collapses in a missile "
              "and drone attack",
              41, 23, centering=(0.5, 0.45))
    y += 6
    draw.rectangle([MARGIN, y, W - MARGIN, y + 1], fill=INK)
    y += 10

    # ---- Two half stories ----------------------------------------------
    half = (CW - 20) // 2  # 474
    y_left = story(draw, page, MARGIN, y, half, panel("tanker"), 150,
                   "TANKER HIT BY MINE IN HORMUZ",
                   "A fourth tanker ablaze as the US\u2013Iran war "
                   "threatens the strait",
                   33, 20, centering=(0.5, 0.5))
    y_right = story(draw, page, MARGIN + half + 20, y, half,
                    panel("climate"), 150,
                    "COP31 DRAFT: END FOSSIL FUELS FASTER",
                    "Antalya talks seek $120bn a year in climate finance "
                    "by 2035",
                    33, 20, centering=(0.5, 0.42))
    y = max(y_left, y_right) + 6
    draw.rectangle([MARGIN, y, W - MARGIN, y + 1], fill=INK)
    y += 10

    # ---- Bottom wide story ----------------------------------------------
    y = story(draw, page, MARGIN, y, CW, panel("measles"), 148,
              "US LOSES MEASLES-FREE STATUS",
              "Cases pass 5,400 \u2014 a 40-year high \u2014 as elimination "
              "status ends after 26 years",
              36, 21, centering=(0.5, 0.32))
    y += 10

    # ---- Ticker ----------------------------------------------------------
    ticker = ("ALSO TODAY \u2014 Japan scrambles jets after Russian jets "
              "breach its airspace \u00b7 Russian military plane crash "
              "kills 19 in Kemerovo \u00b7 Nvidia chip-spy scandal shakes "
              "the AI race \u00b7 146,000 march across France over "
              "living costs")
    band_h = H - y - 12
    draw.rectangle([0, y, W, y + band_h], fill=NAVY)
    tsize = 21
    while tsize > 12:
        tf = font(SANS_BOLD, tsize)
        lines = wrap(draw, ticker, tf, W - 32)
        if len(lines) <= 2:
            break
        tsize -= 1
    tf = font(SANS_BOLD, tsize)
    lines = wrap(draw, ticker, tf, W - 32)
    line_h = int(tsize * 1.25)
    ty = y + (band_h - line_h * len(lines)) // 2
    for line in lines:
        wtext = draw.textlength(line, font=tf)
        draw.text(((W - wtext) / 2, ty), line, font=tf, fill=WHITE)
        ty += line_h

    page.save(OUT, optimize=True)
    size = OUT.stat().st_size
    if size > 950_000:
        # Stay comfortably under the competition's 1 MiB cap: the page is
        # flat illustration and text, so an adaptive palette keeps it
        # crisp; fall back to a smaller canvas if that is not enough.
        page.convert("P", palette=Image.ADAPTIVE, colors=256).save(
            OUT, optimize=True)
        size = OUT.stat().st_size
    if size > 1_048_576:
        small = page.resize((960, 960), Image.LANCZOS)
        small.save(OUT, optimize=True)
        size = OUT.stat().st_size
    print("wrote", OUT, page.size, size, "bytes")


if __name__ == "__main__":
    main()
