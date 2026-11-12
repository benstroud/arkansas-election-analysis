"""Build the findings page (docs/index.html) from the derived CSVs.

Reads data/derived/ar_2024_vs_2026_by_district.csv and data/derived/ar_2028_target_ranking.csv.
Every number on the page is computed here, so the page can be rebuilt after the data changes.

Usage: python3 -I scripts/build_report.py
"""

import csv
import html
import math
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from tiger_reader import read_zip_shapefile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DERIVED = ROOT / "data" / "derived"
OUT = ROOT / "docs" / "index.html"


def ballotpedia_url(district):
    """Ballotpedia page for an Arkansas House district (pattern checked for District 81)."""
    return f"https://ballotpedia.org/Arkansas_House_of_Representatives_District_{district}"


def ballotpedia_senate_url(district):
    """Ballotpedia page for an Arkansas Senate district (pattern seen for District 1)."""
    return f"https://ballotpedia.org/Arkansas_State_Senate_District_{district}"

comparison = list(csv.DictReader(open(DERIVED / "ar_2024_vs_2026_by_district.csv", newline="", encoding="utf-8")))
targets = list(csv.DictReader(open(DERIVED / "ar_2028_target_ranking.csv", newline="", encoding="utf-8")))

# Seats contested by both parties in both years (House only; no Senate seat qualifies).
both = [r for r in comparison if r["chamber"] == "house" and r["contested_2024"] == "Y" and r["contested_2026"] == "Y"]
both.sort(key=lambda r: -float(r["d2p_2026"]))
swings = [float(r["swing_2026_minus_2024"]) for r in both]
mean_swing = statistics.mean(swings)
n_gained = sum(1 for s in swings if s > 0)

n_targets = len(targets)
n_house_targets = sum(1 for t in targets if t["chamber"] == "house")
n_senate_targets = n_targets - n_house_targets
n_no_d = sum(1 for t in targets if "no 2026 Democratic candidate" in t["note"])


def esc(s):
    return html.escape(str(s))


def fmt(x, signed=False):
    if x in ("", None):
        return "&mdash;"
    v = float(x)
    return f"{v:+.1f}" if signed else f"{v:.1f}"


def seat_label(chamber, district, special=""):
    name = f"{'House' if chamber == 'house' else 'Senate'} {int(district)}"
    return name + (" (special)" if special else "")


def humanize(note):
    parts = []
    if "2026 special" in note:
        parts.append("2026 special election")
    if "no 2026 D-vs-R contest" in note:
        parts.append("No 2026 contest")
    if "no 2026 Democratic candidate" in note:
        parts.append("No Democrat on 2026 ballot")
    return "; ".join(parts)


# --- Chart: dumbbell plot of 2024 and 2026 Democratic share, one row per seat ---
W = 760
X0, X1 = 150, 690
TOP, ROW = 30, 24
H = TOP + len(both) * ROW + 44


def sx(v):
    return X0 + (v / 100.0) * (X1 - X0)


rows_svg = []
for i, r in enumerate(both):
    y = TOP + i * ROW + ROW / 2
    v24 = float(r["d2p_2024"])
    v26 = float(r["d2p_2026"])
    winner_class = "m-dem" if v26 > 50 else "m-rep"
    rows_svg.append(
        f'<a href="{ballotpedia_url(int(r["district"]))}" target="_blank" rel="noopener">'
        f'<text class="lbl" x="0" y="{y + 4.5:.1f}">{esc(seat_label("house", r["district"]))}</text></a>'
        f'<line class="conn" x1="{sx(v24):.1f}" y1="{y:.1f}" x2="{sx(v26):.1f}" y2="{y:.1f}"/>'
        f'<circle class="hollow" cx="{sx(v24):.1f}" cy="{y:.1f}" r="4.5"/>'
        f'<circle class="{winner_class}" cx="{sx(v26):.1f}" cy="{y:.1f}" r="5.5"/>'
        f'<text class="val" x="{X1 + 22}" y="{y + 4:.1f}">{fmt(r["swing_2026_minus_2024"], signed=True)}</text>'
    )

grid_svg = []
for tick in (0, 25, 50, 75, 100):
    x = sx(tick)
    cls = "mid" if tick == 50 else "grid"
    grid_svg.append(f'<line class="{cls}" x1="{x:.1f}" y1="{TOP - 8}" x2="{x:.1f}" y2="{TOP + len(both) * ROW + 4}"/>')
    grid_svg.append(f'<text class="axis" x="{x:.1f}" y="{H - 14}" text-anchor="middle">{tick}%</text>')
grid_svg.append(f'<text class="axis" x="{X1 + 22}" y="{TOP - 14}" text-anchor="start">Swing</text>')

chart = (
    f'<svg class="chart" viewBox="0 0 {W} {H}" width="{W}" role="img" '
    f'aria-label="Dumbbell chart of Democratic share in 2024 and 2026 for {len(both)} House seats">'
    + "".join(grid_svg)
    + "".join(rows_svg)
    + "</svg>"
)

# --- Target table ---
def seat_link(t):
    label = esc(seat_label(t["chamber"], t["district"], "special" if "special" in t["note"] else ""))
    if t["chamber"] != "house":
        return label
    return f'<a href="{ballotpedia_url(int(t["district"]))}" target="_blank" rel="noopener">{label}</a>'


def short_class(t):
    if t["chamber"] == "house":
        return "2028"
    if "special" in t["class"]:
        return "2028 (special)"
    return "2028 (2024 cycle)"


table_rows = []
for t in targets:
    table_rows.append(
        "<tr>"
        f"<th scope=\"row\">{seat_link(t)}</th>"
        f"<td>{esc(short_class(t))}</td>"
        f"<td class=\"num\">{t['latest_year']}</td>"
        f"<td class=\"num strong\">{fmt(t['latest_d2p'])}</td>"
        f"<td class=\"num\">{fmt(t['d2p_2024'])}</td>"
        f"<td class=\"num\">{fmt(t['d2p_2026'])}</td>"
        f"<td class=\"num\">{fmt(t['swing_2026_minus_2024'], signed=True)}</td>"
        f"<td class=\"note\">{esc(humanize(t['note']))}</td>"
        "</tr>"
    )

# --- Map: district outlines from the 2024 TIGER/Line legislative files ---
# The 2022 and 2024 files describe the same 2021 plan (areas differ by at most 0.08%,
# centroids by at most 0.0003 degrees), so the newer vintage is used.
MAP_WIDTH = 540
MAP_EPS = 0.0008  # degrees (about 90 m), invisible at map scale, cuts the point count
ZIPS = {
    "house": ROOT / "data" / "raw" / "tiger2024_sldl" / "tl_2024_05_sldl.zip",
    "senate": ROOT / "data" / "raw" / "tiger2024_sldu" / "tl_2024_05_sldu.zip",
}
DISTRICT_FIELD = {"house": "SLDLST", "senate": "SLDUST"}
CHAMBER_NAME = {"house": "House", "senate": "Senate"}
TARGET_SET = {(t["chamber"], int(t["district"])) for t in targets}


def perp_dist(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(x - x1, y - y1)
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))


def simplify(pts, eps):
    """Douglas-Peucker on a closed ring; keeps the first and last points."""
    n = len(pts)
    if n < 4:
        return pts
    keep = [False] * n
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        s, e = stack.pop()
        dmax, idx = 0.0, None
        for i in range(s + 1, e):
            d = perp_dist(pts[i], pts[s], pts[e])
            if d > dmax:
                dmax, idx = d, i
        if idx is not None and dmax > eps:
            keep[idx] = True
            stack.append((s, idx))
            stack.append((idx, e))
    return [p for p, k in zip(pts, keep) if k]


def ring_area_centroid(ring):
    A = cx = cy = 0.0
    for i in range(len(ring) - 1):
        x0, y0 = ring[i]
        x1, y1 = ring[i + 1]
        c = x0 * y1 - x1 * y0
        A += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    A /= 2.0
    if A == 0:
        return 0.0, ring[0]
    return abs(A), (cx / (6 * A), cy / (6 * A))


def latest_shares(chamber):
    """Latest Democratic share per district: 2026 where contested, otherwise 2024."""
    out = {}
    for r in comparison:
        if r["chamber"] != chamber:
            continue
        d = int(r["district"])
        if r["contested_2026"] == "Y":
            out[d] = float(r["d2p_2026"])
        elif r["contested_2024"] == "Y":
            out[d] = float(r["d2p_2024"])
    return out


def step_class(share):
    """Map a share to one of ten 5-point steps on each side of 50, or 'nc' for no contest."""
    if share is None:
        return "nc"
    t = (share - 50.0) / 50.0
    step = min(9, int(abs(t) * 10))
    return ("d" if t >= 0 else "r") + str(step)


def gray_kinds(chamber):
    """For districts with no D-vs-R race in either year, say which party was missing from the 2026 ballot."""
    out = {}
    for r in comparison:
        if r["chamber"] != chamber:
            continue
        if r["contested_2026"] == "Y" or r["contested_2024"] == "Y":
            continue
        # Every House seat is on the 2026 ballot. A Senate seat with no 2026 candidates
        # is in the 2028 class and was on the 2024 ballot, so use the 2024 votes.
        on_2026 = chamber == "house" or r["dem_cand_2026"] == "Y" or r["rep_cand_2026"] == "Y"
        if on_2026:
            dem = r["dem_cand_2026"] == "Y"
            rep = r["rep_cand_2026"] == "Y"
        else:
            dem = int(r["d_votes_2024"] or 0) > 0
            rep = int(r["r_votes_2024"] or 0) > 0
        if dem and not rep:
            kind = "nr"  # Democrat only: no Republican on the ballot
        elif rep and not dem:
            kind = "nd"  # Republican only: no Democrat on the ballot
        else:
            kind = "nc"  # neither major party listed
        out[int(r["district"])] = kind
    return out


NO_CONTEST_TEXT = {
    "nd": "no Democrat on the latest ballot",
    "nr": "no Republican on the latest ballot",
    "nc": "one candidate with no major-party label",
}


def district_map(chamber):
    shapes, recs = read_zip_shapefile(ZIPS[chamber])
    field = DISTRICT_FIELD[chamber]
    shares = latest_shares(chamber)
    kinds = gray_kinds(chamber)
    parts = []
    lon_min = lat_min = float("inf")
    lon_max = lat_max = float("-inf")
    for shape, rec in zip(shapes, recs):
        d = int(rec[field])
        rings = [simplify(ring, MAP_EPS) for ring in shape if len(ring) >= 4]
        for ring in rings:
            for lon, lat in ring:
                lon_min, lon_max = min(lon_min, lon), max(lon_max, lon)
                lat_min, lat_max = min(lat_min, lat), max(lat_max, lat)
        parts.append((d, rings))

    cos_lat = math.cos(math.radians((lat_min + lat_max) / 2))
    scale = MAP_WIDTH / ((lon_max - lon_min) * cos_lat)
    height = (lat_max - lat_min) * scale

    def proj(lon, lat):
        return (lon - lon_min) * cos_lat * scale, (lat_max - lat) * scale

    paths, labels = [], []
    for d, rings in sorted(parts):
        share = shares.get(d)
        cls = step_class(share) if share is not None else kinds.get(d, "nc")
        is_target = (chamber, d) in TARGET_SET
        if is_target:
            cls += " tgt"
        if share is None:
            tip = f"{CHAMBER_NAME[chamber]} {d}: " + NO_CONTEST_TEXT[kinds.get(d, "nc")]
        else:
            tip = f"{CHAMBER_NAME[chamber]} {d}: {share:.1f}% Democratic in the latest race"
        d_attr = " ".join(
            "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (proj(lon, lat) for lon, lat in ring)) + " Z"
            for ring in rings
        )
        path_el = f'<path class="{cls}" d="{d_attr}"><title>{esc(tip)}</title></path>'
        url = ballotpedia_url(d) if chamber == "house" else ballotpedia_senate_url(d)
        path_el = f'<a href="{url}" target="_blank" rel="noopener">{path_el}</a>'
        paths.append(path_el)
        if is_target and rings:
            _, (clon, clat) = max((ring_area_centroid(r) for r in rings), key=lambda a: a[0])
            x, y = proj(clon, clat)
            labels.append(f'<text class="tl" x="{x:.1f}" y="{y:.1f}">{d}</text>')

    return (
        f'<svg class="map" viewBox="0 0 {MAP_WIDTH} {height:.1f}" role="img" '
        f'aria-label="Map of {CHAMBER_NAME[chamber]} districts, filled by latest Democratic share">'
        + "".join(paths) + "".join(labels) + "</svg>"
    )


STEP_CSS = "".join(
    f".d{s}{{fill:color-mix(in srgb, var(--dem) {20 + 8 * s}%, var(--surface));}}"
    f".r{s}{{fill:color-mix(in srgb, var(--rep) {20 + 8 * s}%, var(--surface));}}"
    f".sw.d{s}{{background:color-mix(in srgb, var(--dem) {20 + 8 * s}%, var(--surface));}}"
    f".sw.r{s}{{background:color-mix(in srgb, var(--rep) {20 + 8 * s}%, var(--surface));}}"
    for s in range(10)
) + ".nc{fill:var(--rule);} .sw.nc{background:var(--rule);}"

MAP_CSS = """
svg.map { width: 100%; height: auto; display: block; }
svg.map path { stroke: var(--surface); stroke-width: 0.6; stroke-linejoin: round; }
svg.map path.tgt { stroke: var(--ink); stroke-width: 1.6; }
svg.map text.tl { font: 600 10.5px var(--font-mono); fill: var(--ink); text-anchor: middle; dominant-baseline: middle; paint-order: stroke; stroke: var(--surface); stroke-width: 3px; stroke-linejoin: round; }
.maps { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px; }
.mapfig { margin: 0; }
.mapfig figcaption { font-size: 14px; color: var(--muted); margin-top: 10px; }
.scale { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; font: 400 12.5px/1.4 var(--font-mono); color: var(--muted); margin: 0 0 18px; }
.scale .strip { display: inline-flex; }
.sw { display: inline-block; width: 14px; height: 12px; }
.nd { fill: url(#hatch-rep); }
.nr { fill: url(#hatch-dem); }
.hl-bg { fill: var(--surface); }
.hl-rep { stroke: var(--rep); }
.hl-dem { stroke: var(--dem); }
.sw.nd { background: repeating-linear-gradient(45deg, var(--rep) 0 2px, var(--surface) 2px 5px); }
.sw.nr { background: repeating-linear-gradient(45deg, var(--dem) 0 2px, var(--surface) 2px 5px); }
svg.map a { cursor: pointer; }
svg.map a:hover path, svg.map a:focus-visible path { stroke: var(--ink); stroke-width: 1.2; }
svg.map a:focus-visible { outline: none; }
tbody th a { color: var(--ink); text-decoration-color: var(--rule-strong); }
tbody th a:hover { color: var(--dem); }
svg.chart a { cursor: pointer; }
svg.chart a:hover text.lbl, svg.chart a:focus-visible text.lbl { fill: var(--dem); text-decoration: underline; }
svg.chart a:focus-visible { outline: none; }
"""

STYLE = """
:root {
  /* Layout: one centered column. Prose at reading width, the chart and table
     on the same column, with the figures set in mono so they line up. */
  --ground: #F2F4F3;
  --surface: #FBFCFB;
  --ink: #15201E;
  --muted: #55625F;
  --rule: #D3DBD8;
  --rule-strong: #8E9C98;
  --dem: #1F5FA8;
  --rep: #A8402A;
  --font-display: "Source Serif 4", Georgia, "Times New Roman", serif;
  --font-text: "IBM Plex Sans", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground: #0F1514;
    --surface: #161E1D;
    --ink: #E4EBE8;
    --muted: #9BA9A5;
    --rule: #2B3634;
    --rule-strong: #5E6E6A;
    --dem: #7DB0E8;
    --rep: #E28A72;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --ground: #0F1514;
  --surface: #161E1D;
  --ink: #E4EBE8;
  --muted: #9BA9A5;
  --rule: #2B3634;
  --rule-strong: #5E6E6A;
  --dem: #7DB0E8;
  --rep: #E28A72;
  color-scheme: dark;
}
html, body { margin: 0; }
body {
  background: var(--ground);
  color: var(--ink);
  font: 16px/1.6 var(--font-text);
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 48px 64px;
}
.page { max-width: 980px; margin: 0 auto; display: flex; flex-direction: column; gap: 56px; }
.prose { max-width: 65ch; }
.kicker { font: 500 12px/1.4 var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin: 0 0 12px; }
h1 { font: 600 clamp(34px, 5vw, 48px)/1.1 var(--font-display); margin: 0 0 16px; text-wrap: balance; letter-spacing: -0.01em; }
h2 { font: 600 26px/1.2 var(--font-display); margin: 0 0 12px; text-wrap: balance; }
.deck { font-size: 19px; color: var(--muted); margin: 0; max-width: 60ch; }
.status { display: flex; flex-wrap: wrap; gap: 6px 24px; font: 400 12.5px/1.5 var(--font-mono); color: var(--muted); border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); padding: 12px 0; margin: 0; }
.summary { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; margin: 0; border-top: 1px solid var(--rule); }
.summary div { padding: 18px 20px 0 0; }
.summary div + div { padding-left: 20px; border-left: 1px solid var(--rule); }
.summary dt { font: 500 12px/1.4 var(--font-mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); }
.summary dd { margin: 8px 0 0; font: 600 34px/1.1 var(--font-display); font-variant-numeric: tabular-nums; }
.summary small { display: block; font-size: 14px; color: var(--muted); margin-top: 6px; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 22px; font-size: 14px; color: var(--muted); margin: 0 0 12px; }
.legend span { display: inline-flex; align-items: center; gap: 8px; }
.key { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
.key.filled { background: var(--dem); }
.key.hollow { border: 1.5px solid var(--muted); background: var(--surface); box-sizing: border-box; }
.figure { margin: 0; overflow-x: auto; }
.figure figcaption { font-size: 14px; color: var(--muted); margin-top: 12px; max-width: 65ch; }
svg.chart { display: block; height: auto; font-family: var(--font-text); }
svg.chart .lbl { font-size: 13px; fill: var(--ink); }
svg.chart .val { font: 500 12.5px var(--font-mono); fill: var(--ink); }
svg.chart .axis { font: 400 12px var(--font-mono); fill: var(--muted); }
svg.chart .grid { stroke: var(--rule); stroke-width: 1; }
svg.chart .mid { stroke: var(--rule-strong); stroke-width: 1.25; stroke-dasharray: 4 4; }
svg.chart .conn { stroke: var(--rule-strong); stroke-width: 2; }
svg.chart .hollow { fill: var(--surface); stroke: var(--muted); stroke-width: 1.5; }
svg.chart .m-dem { fill: var(--dem); }
svg.chart .m-rep { fill: var(--rep); }
.table-wrap { overflow-x: auto; border-top: 1px solid var(--rule); }
table { width: 100%; border-collapse: collapse; font-size: 14.5px; min-width: 760px; }
th, td { padding: 10px 12px 10px 0; text-align: left; vertical-align: baseline; border-bottom: 1px solid var(--rule); }
thead th { font: 500 11.5px/1.4 var(--font-mono); text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
tbody th { font-weight: 500; white-space: nowrap; }
td.num, thead th.num { text-align: right; font-variant-numeric: tabular-nums; font-family: var(--font-mono); font-size: 13.5px; }
td.strong { font-weight: 600; color: var(--ink); }
td.note { color: var(--muted); font-size: 13.5px; }
.defs { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px 32px; margin: 0; }
.defs div { border-top: 1px solid var(--rule); padding-top: 12px; }
.defs dt { font-weight: 600; }
.defs dd { margin: 4px 0 0; color: var(--muted); font-size: 15px; }
ul.sources { margin: 0; padding-left: 18px; color: var(--muted); }
ul.sources li + li { margin-top: 6px; }
a { color: var(--dem); text-underline-offset: 3px; }
a:focus-visible { outline: 2px solid var(--dem); outline-offset: 3px; border-radius: 2px; }
.foot { font: 400 12.5px/1.5 var(--font-mono); color: var(--muted); border-top: 1px solid var(--rule); padding-top: 16px; margin: 0; }
@media (max-width: 640px) {
  .summary { grid-template-columns: 1fr; }
  .summary div + div { padding-left: 0; border-left: 0; border-top: 1px solid var(--rule); margin-top: 16px; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
"""

def senate_chart():
    """One marker per Senate seat with a contested result, at its latest contested race. No cross-year comparison."""
    shares = latest_shares("senate")
    meta = {}
    for r in comparison:
        if r["chamber"] != "senate":
            continue
        d = int(r["district"])
        if r["contested_2026"] == "Y":
            meta[d] = "2026 special" if r["special_2026"] else "2026"
        elif r["contested_2024"] == "Y" and d not in meta:
            meta[d] = "2024"
    rows = sorted(((d, s, meta.get(d, "")) for d, s in shares.items()), key=lambda x: -x[1])

    W, X0, X1, TOP, ROW = 760, 170, 690, 30, 26
    H = TOP + len(rows) * ROW + 44

    def x_of(v):
        return X0 + (v / 100.0) * (X1 - X0)

    parts = []
    for tick in (0, 25, 50, 75, 100):
        x = x_of(tick)
        cls = "mid" if tick == 50 else "grid"
        parts.append(f'<line class="{cls}" x1="{x:.1f}" y1="{TOP - 8}" x2="{x:.1f}" y2="{TOP + len(rows) * ROW + 4}"/>')
        parts.append(f'<text class="axis" x="{x:.1f}" y="{H - 14}" text-anchor="middle">{tick}%</text>')
    parts.append(f'<text class="axis" x="110" y="{TOP - 14}">Race</text>')
    parts.append(f'<text class="axis" x="{X1 + 22}" y="{TOP - 14}">Share</text>')
    for i, (d, s, yr) in enumerate(rows):
        y = TOP + i * ROW + ROW / 2
        marker = "m-dem" if s > 50 else "m-rep"
        parts.append(
            f'<a href="{ballotpedia_senate_url(d)}" target="_blank" rel="noopener">'
            f'<text class="lbl" x="0" y="{y + 4.5:.1f}">Senate {d}</text></a>'
            f'<text class="axis" x="110" y="{y + 4:.1f}">{esc(yr)}</text>'
            f'<circle class="{marker}" cx="{x_of(s):.1f}" cy="{y:.1f}" r="5.5"/>'
            f'<text class="val" x="{X1 + 22}" y="{y + 4:.1f}">{s:.1f}</text>'
        )
    return (
        f'<svg class="chart" viewBox="0 0 {W} {H}" width="{W}" role="img" '
        f'aria-label="Democratic share in the latest contested race for {len(rows)} Senate seats">'
        + "".join(parts) + "</svg>"
    )


page = f"""<meta name="claude:viewport-fit-sides" content="cover">
<title>Arkansas 2028 Seat Targets</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=Source+Serif+4:opsz,wght@8..60,400..700&amp;display=swap">
<style>{STYLE}{STEP_CSS}{MAP_CSS}</style>
<main class="page">
  <header class="prose">
    <p class="kicker">Arkansas House and Senate &middot; 2024 and 2026 results</p>
    <h1>Arkansas 2028 Seat Targets</h1>
    <p class="deck">Republican-held legislative seats on the 2028 ballot, ranked by how close Democrats came in the latest contested race.</p>
  </header>

  <p class="status">
    <span>Unofficial 2026 results, last updated 11/10/2026, 4:31 PM CST</span>
    <span>Page built 11/11/2026</span>
  </p>

  <section aria-labelledby="summary">
    <h2 id="summary">The short version</h2>
    <dl class="summary">
      <div>
        <dt>Targets</dt>
        <dd>{n_targets}</dd>
        <small>{n_house_targets} House and {n_senate_targets} Senate seats</small>
      </div>
      <div>
        <dt>No Democrat on the 2026 ballot</dt>
        <dd>{n_no_d} of {n_targets}</dd>
        <small>These seats need a candidate before they can flip</small>
      </div>
      <div>
        <dt>Mean House swing</dt>
        <dd>{mean_swing:+.1f}</dd>
        <small>Points toward Democrats; {n_gained} of {len(both)} seats contested both years moved that way</small>
      </div>
    </dl>
    <p class="prose" style="margin-top:20px">Every House seat contested by both parties in both years moved toward Democrats. The statewide shift looks similar in size. The 2026 U.S. Senate race (Cotton against Shoffner) gave Democrats about 43.9% of the two-party vote, against about 34.3% for the 2024 presidential race, a gain of about 9.5 points. The district swings cluster around that figure, so the more useful question is which seats were already closest, not which moved most.</p>
  </section>

  <section aria-labelledby="shift">
    <h2 id="shift">Shift by seat</h2>
    <p class="prose">House seats contested by both parties in 2024 and 2026, sorted by 2026 Democratic share. The dashed line marks 50 percent.</p>
    <div class="legend">
      <span><i class="key filled"></i>2026 result, colored by winner</span>
      <span><i class="key hollow"></i>2024 result</span>
    </div>
    <figure class="figure">
      {chart}
      <figcaption>Scale runs from 0 to 100 percent of the two-party vote. Right column: change in Democratic share, 2024 to 2026, in points.</figcaption>
    </figure>
  </section>

  <section aria-labelledby="senate">
    <h2 id="senate">Senate seats</h2>
    <p class="prose">The latest contested race for each Senate seat with both a Democrat and a Republican on the ballot. Seats up in 2028 were last contested in 2024, and seats up in 2030 in 2026. Results are not compared across years, since no seat was contested in both.</p>
    <figure class="figure">
      {senate_chart()}
      <figcaption>Scale runs from 0 to 100 percent of the two-party vote. Marker color shows the winner. Senate District 1 shows its 2026 special election.</figcaption>
    </figure>
  </section>

  <section aria-labelledby="targets">
    <h2 id="targets">Target list</h2>
    <p class="prose">Republican-held seats on the 2028 ballot with a contested result, ranked by latest Democratic share, closest first. Figures are percent of the two-party vote. Senate seats up in 2028 have only a 2024 result.</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th scope="col">Seat</th>
            <th scope="col">2028 class</th>
            <th scope="col" class="num">Latest</th>
            <th scope="col" class="num">Latest share</th>
            <th scope="col" class="num">2024</th>
            <th scope="col" class="num">2026</th>
            <th scope="col" class="num">Swing</th>
            <th scope="col">Note</th>
          </tr>
        </thead>
        <tbody>
          {"".join(table_rows)}
        </tbody>
      </table>
    </div>
  </section>

  <section aria-labelledby="maps">
    <h2 id="maps">Where the seats are</h2>
    <p class="prose">Each district is filled by its latest Democratic share: 2026 where contested, otherwise 2024. Outlined districts are 2028 targets and carry their number. Hatched districts had no race between a Democrat and a Republican in the latest year: red hatch means no Democrat ran, blue hatch means no Republican ran. Hover a district for its exact share. Click a district to open its Ballotpedia page.</p>
    <div class="scale" aria-hidden="true">
      <span>Republican</span>
      <span class="strip">{"".join(f'<i class="sw r{s}"></i>' for s in range(9, -1, -1))}{"".join(f'<i class="sw d{s}"></i>' for s in range(10))}</span>
      <span>Democratic</span>
      <span><i class="sw nd"></i> No Democrat on ballot</span>
      <span><i class="sw nr"></i> No Republican on ballot</span>
      <span><i class="sw nc"></i> Other</span>
    </div>
    <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
      <defs>
        <pattern id="hatch-rep" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect class="hl-bg" width="6" height="6"/><line class="hl-rep" x1="0" y1="0" x2="0" y2="6" stroke-width="2"/>
        </pattern>
        <pattern id="hatch-dem" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect class="hl-bg" width="6" height="6"/><line class="hl-dem" x1="0" y1="0" x2="0" y2="6" stroke-width="2"/>
        </pattern>
      </defs>
    </svg>
    <div class="maps">
      <figure class="mapfig">
        {district_map("house")}
        <figcaption>House, 100 districts</figcaption>
      </figure>
      <figure class="mapfig">
        {district_map("senate")}
        <figcaption>Senate, 35 seats. Seat 1 shows its 2026 special election.</figcaption>
      </figure>
    </div>
  </section>

  <section aria-labelledby="read">
    <h2 id="read">How to read the numbers</h2>
    <dl class="defs">
      <div><dt>Democratic share</dt><dd>Democratic votes as a percentage of Democratic plus Republican votes. Third-party votes are left out.</dd></div>
      <div><dt>Latest race</dt><dd>The 2026 result where both parties ran. Otherwise the 2024 result.</dd></div>
      <div><dt>Swing</dt><dd>The 2026 share minus the 2024 share in the same district. Positive means a shift toward Democrats.</dd></div>
      <div><dt>Republican-held</dt><dd>Below 50 percent in the latest race. This is not confirmed incumbency.</dd></div>
      <div><dt>2028 Senate class</dt><dd>The 18 seats contested in 2024, including District 1. Inferred from the 2024 results. Not yet checked against the official roster.</dd></div>
      <div><dt>Not a forecast</dt><dd>The list ranks seats by how close the last contest was. It does not model 2028 turnout, candidates, or the national environment.</dd></div>
    </dl>
  </section>

  <section aria-labelledby="caveats">
    <h2 id="caveats">Caveats</h2>
    <ul class="sources prose">
      <li>The 2026 results are unofficial and may change after certification.</li>
      <li>2024 was a presidential year and 2026 a midterm. Turnout differs, so swings mix changes in opinion with changes in who voted.</li>
      <li>Incumbency, retirements, open seats, and 2028 candidates are not included. Seats without a Democrat on the 2026 ballot are ranked but cannot flip without a candidate.</li>
    </ul>
  </section>

  <section aria-labelledby="sources">
    <h2 id="sources">Sources and code</h2>
    <ul class="sources">
      <li>Arkansas Secretary of State, 2026 general election results, unofficial, from the Election Night Reporting site (arkansas.tally-enr.com), downloaded 11/11/2026.</li>
      <li>MIT Election Data and Science Lab, 2024 precinct-level returns, Harvard Dataverse, <a href="https://doi.org/10.7910/DVN/DODOBJ">doi:10.7910/DVN/DODOBJ</a> and <a href="https://doi.org/10.7910/DVN/NYTPDU">doi:10.7910/DVN/NYTPDU</a>. Licensed CC0.</li>
      <li>Code, data, and a step-by-step provenance log: <a href="https://github.com/benstroud/arkansas-election-analysis">github.com/benstroud/arkansas-election-analysis</a>. Definitions and method are in METHODS.md in that repository.</li>
    </ul>
  </section>

  <p class="foot">Built by scripts/build_report.py from data/derived/. {len(both)} House seats in the chart; {n_targets} targets in the table.</p>
</main>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT} ({len(page)} bytes): {len(both)} chart seats, {n_targets} targets, mean swing {mean_swing:+.2f}")
