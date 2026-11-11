"""Rank Republican-held Arkansas legislative seats as 2028 Democratic targets.

Input: data/derived/ar_2024_vs_2026_by_district.csv (from compare_2024_2026.py)

Method (deliberately simple; this is a ranking, not a forecast):
  - Latest result = 2026 if the seat was contested by a D and an R in 2026, else 2024 if so.
  - A seat is a target if it is 2028-class and the latest result is an R win (D2P < 50).
  - Ranked by latest D two-party share, highest first (closest to 50 first).
  - Seats with no contested result in either year are counted but not ranked.

Usage: python3 -I rank_2028_targets.py <comparison.csv> <out.csv>
"""

import csv
import sys

src, dst = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(src, newline="", encoding="utf-8")))


def f(x):
    return float(x) if x not in ("", None) else None


targets = []
unranked_2028 = 0
for r in rows:
    is_2028 = r["class"].startswith("2028") or r["chamber"] == "house"
    if not is_2028:
        continue
    d26, d24 = f(r["d2p_2026"]), f(r["d2p_2024"])
    if d26 is not None:
        latest_year, latest = 2026, d26
    elif d24 is not None:
        latest_year, latest = 2024, d24
    else:
        unranked_2028 += 1
        continue
    if d26 is None and r["dem_cand_2026"] == "Y" and r["rep_cand_2026"] == "N":
        continue  # Democrat unopposed in 2026: the seat is Democratic now, not a target
    if latest >= 50:
        continue  # latest result is a D win
    note = []
    if r["special_2026"]:
        note.append("2026 special election result")
    if d26 is None:
        note.append("no 2026 D-vs-R contest; 2024 baseline")
    if r["dem_cand_2026"] == "N" and d26 is None:
        note.append("no 2026 Democratic candidate")
    targets.append({
        "chamber": r["chamber"],
        "district": r["district"],
        "class": r["class"],
        "latest_year": latest_year,
        "latest_d2p": round(latest, 1),
        "d2p_2024": d24 if d24 is None else round(d24, 1),
        "d2p_2026": d26 if d26 is None else round(d26, 1),
        "swing_2026_minus_2024": r["swing_2026_minus_2024"],
        "note": "; ".join(note),
    })

targets.sort(key=lambda t: (-t["latest_d2p"], t["chamber"], int(t["district"])))
with open(dst, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(targets[0].keys()))
    w.writeheader()
    w.writerows(targets)

print(f"ranked targets: {len(targets)} (house {sum(t['chamber']=='house' for t in targets)}, senate {sum(t['chamber']=='senate' for t in targets)})")
print(f"2028-class seats with no contested result in either year: {unranked_2028}")
print(f"{'chamber':<7}{'dist':>5}  {'latest':>6} {'D2P':>6}  {'2024':>6}  {'2026':>6}  {'swing':>6}  note")
for t in targets:
    print(f"{t['chamber']:<7}{t['district']:>5}  {t['latest_year']:>6} {t['latest_d2p']:>6}  "
          f"{'-' if t['d2p_2024'] is None else t['d2p_2024']:>6}  "
          f"{'-' if t['d2p_2026'] is None else t['d2p_2026']:>6}  "
          f"{t['swing_2026_minus_2024'] or '-':>6}  {t['note']}")
