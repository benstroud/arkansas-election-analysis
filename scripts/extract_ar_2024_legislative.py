"""Extract Arkansas 2024 state legislative rows from the MEDSL state precinct file.

Usage: python3 -I extract_ar_2024_legislative.py <STATE_precinct_general.csv> <out.csv>
Streams the file; does not load it into memory.
"""

import csv
import sys
from collections import Counter

src, dst = sys.argv[1], sys.argv[2]

office_counts = Counter()
written = 0
seen_state = 0
with open(src, newline="", encoding="utf-8") as fh, open(dst, "w", newline="", encoding="utf-8") as out:
    reader = csv.DictReader(fh)
    writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
    writer.writeheader()
    for r in reader:
        if r["state"] != "ARKANSAS":
            continue
        seen_state += 1
        office = r["office"]
        if "STATE" in office and ("HOUSE" in office or "SENATE" in office):
            office_counts[(office, r["year"], r["stage"])] += 1
            writer.writerow(r)
            written += 1

print(f"Arkansas rows in file: {seen_state}")
print(f"Arkansas state legislative rows written: {written}")
print("office/year/stage counts:")
for (office, year, stage), n in sorted(office_counts.items()):
    print(f"  {office:<20} {year} {stage:<4} {n}")
