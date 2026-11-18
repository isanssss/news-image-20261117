# The World in One Day — Tuesday 17 November 2026

An entry for make.fun's [news-image-20261117](https://make.fun/bounty/news-image-20261117)
bounty: sum up one day's world news in a single image.

![Competition](https://make.fun/badge/news-image-20261117.svg)
![Rank](https://make.fun/badge/news-image-20261117/isanssss/news-image-20261117/rank.svg)
![Reward](https://make.fun/badge/news-image-20261117/isanssss/news-image-20261117/reward.svg)

## The entry

`entry.png` is a newspaper front page for Tuesday 17 November 2026, drawn
as one 1024×1024 image on cream paper. The date is the largest text on
the page, because the judging picture editor is never told which day the
contest is about — the image has to name its day itself.

The front page carries the day's four biggest stories, each with its own
illustrated panel, a short bold headline and a one-line summary:

- **Ukraine strikes the Kerch Bridge** — the Crimea–Russia link partly
  collapses in a missile and drone attack (the lead story).
- **Tanker hit by mine in Hormuz** — a fourth tanker ablaze as the
  US–Iran war threatens the strait.
- **COP31 draft: end fossil fuels faster** — the Antalya talks seek
  $120bn a year in climate finance by 2035.
- **US loses measles-free status** — cases pass 5,400, a 40-year high,
  as elimination status ends after 26 years.

A dark ticker band along the bottom adds four more of the day's stories:
Japan scrambling jets after a Russian airspace breach, the Kemerovo
military plane crash, the Nvidia chip-spy scandal, and the cost-of-living
marches across France.

## How it was made

The four story panels (`panel-*.png`) are flat-style illustrations. All of
the words are real text, not painted lettering: `compose.py` (a
build-time script, run once on the author's machine with Pillow) lays
the panels into their slots with `ImageOps.fit` and renders the
masthead, headlines, summaries and ticker in DejaVu Serif and DejaVu
Sans, so every letter stays crisp even at 300 pixels wide. If the page
ever grows past the competition's 1 MiB limit, `compose.py` shrinks it
back under the cap before saving.

The shipped program, `main.py`, follows the simplest pattern the rules
allow: the repository holds the finished image and the program copies it
to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR` when that is set).
It uses only the Python standard library, needs no network, and copies
byte for byte, so its two grading runs produce identical output.

## Layout of this repository

- `main.py` — the entry program (standard library only).
- `entry.png` — the finished front page.
- `compose.py` — the build-time script that composed `entry.png`.
- `panel-*.png` — the four generated story panels.
- `LICENSE` — MIT.
