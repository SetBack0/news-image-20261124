#!/usr/bin/env python3
"""Build a dotted world map from Natural Earth 110m land polygons.

Fetches the land GeoJSON, rasterises each polygon to a mask at 2x
supersampling, then stamps evenly spaced dots onto every land cell.
Output: tools/map.png, 470x240, equirectangular (lon -180..180, lat 84..-58).

Standard library + Pillow only. Run from the repo root:

    python3 tools/make_map.py
"""

import json
import math
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw

LAND_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
    "geojson/ne_110m_land.geojson"
)

W, H = 470, 240          # output pixels
SS = 2                   # supersampling factor
LON0, LON1 = -180.0, 180.0
LAT0, LAT1 = 84.0, -58.0  # top, bottom
DOT = 3                  # dot diameter on the supersampled grid
STEP = 6                 # dot grid spacing on the supersampled grid

OUT = Path(__file__).resolve().parent / "map.png"

INK = (21, 23, 28)       # page ink, but softened below


def lonlat_to_xy(lon: float, lat: float, w: int, h: int) -> tuple[int, int]:
    """Equirectangular projection onto the pixel grid."""
    x = (lon - LON0) / (LON1 - LON0) * (w - 1)
    y = (LAT0 - lat) / (LAT0 - LAT1) * (h - 1)
    return int(round(x)), int(round(y))


def polygon_to_pixels(ring, w: int, h: int):
    """Yield every pixel (x, y) inside a single GeoJSON ring of [lon, lat]."""
    if not ring:
        return
    projected = [lonlat_to_xy(lon, lat, w, h) for lon, lat in ring]

    min_x = min(x for x, _ in projected)
    max_x = max(x for x, _ in projected)
    min_y = min(y for _, y in projected)
    max_y = max(y for _, y in projected)

    # Build a small canvas the size of the bounding box and scanline-fill.
    bw = max_x - min_x + 1
    bh = max_y - min_y + 1
    if bw <= 0 or bh <= 0:
        return
    mask = Image.new("1", (bw, bh), 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(
        [(x - min_x, y - min_y) for x, y in projected],
        outline=1,
        fill=1,
    )

    for py in range(bh):
        for px in range(bw):
            if mask.getpixel((px, py)):
                yield px + min_x, py + min_y


def render(land: list, out_path: Path) -> None:
    w, h = W * SS, H * SS
    mask = Image.new("1", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    for feature in land:
        geom = feature.get("geometry") or {}
        if geom.get("type") != "Polygon":
            continue
        coords = geom.get("coordinates") or []
        if not coords:
            continue
        # First ring is the outer boundary; the rest are holes, ignored here
        # (small islands matter more than inland lakes at 110m).
        outer = coords[0]
        for x, y in polygon_to_pixels(outer, w, h):
            if 0 <= x < w and 0 <= y < h:
                mask.putpixel((x, y), 1)

    # Stamp dots on a regular grid wherever we are on land.
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for y in range(STEP // 2, h, STEP):
        for x in range(STEP // 2, w, STEP):
            if mask.getpixel((x, y)):
                d.ellipse(
                    (x - DOT // 2, y - DOT // 2,
                     x - DOT // 2 + DOT, y - DOT // 2 + DOT),
                    fill=(21, 23, 28, 255),
                )

    img = img.resize((W, H), Image.Resampling.LANCZOS)
    # Convert to plain RGB on a transparent-cleared background; the page
    # places the map on its own cream card, so keep alpha.
    img.save(out_path, "PNG", optimize=True)
    print(f"wrote {out_path} ({img.width}x{img.height})")


def fetch_land() -> list:
    req = urllib.request.Request(
        LAND_URL,
        headers={"User-Agent": "make.fun-news-image/1.0 (stdlib map builder)"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    features = data.get("features", [])
    if not features:
        raise SystemExit("error: no features in land GeoJSON")
    print(f"fetched {len(features)} land features from Natural Earth")
    return features


def main() -> int:
    if not OUT.parent.exists():
        OUT.parent.mkdir(parents=True, exist_ok=True)
    land = fetch_land()
    render(land, OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
