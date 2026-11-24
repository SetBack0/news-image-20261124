# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/setback0/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/setback0/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up the world's news of Tuesday 24 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## About the image

`entry.png` is a 1024x1024 front page for Tuesday 24 November 2026: 29 stories across six
regions, three leads, a day-in-numbers strip, eight story cards, eighteen briefs and a dotted
world map with pins. Every story happened, or was first reported, that day; each carries its
wire and a REPORTED / CLAIM / ONGOING status.

It is laid out as hand-written HTML/CSS with an SVG strait map, rasterised at 1024x1024, and
the dotted world map is generated from Natural Earth 110m land polygons
(`tools/build_map.py`, `tools/build_page.py`, `tools/poster.html`, `tools/map.png`).
Rendering needs the Inter Tight, Playfair Display and Barlow Condensed fonts installed;
without them the layout falls back to Arial and will not match byte-for-byte.

`main.py` copies it byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the write,
so two runs always produce identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=nm72wrzj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
