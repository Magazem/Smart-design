#!/usr/bin/env python3
"""Fill the empty `Section Order` column of research/36-t10-structures-draft.csv.

Sources are the three phase-A section-order drafts (39/40/41). Reproducible and
idempotent: re-running it on an already-merged file is a no-op.

Line-based on purpose. The structures draft has no quoted fields, no BOM and LF
endings, so rewriting only the third field of the fifteen target lines leaves
every other byte -- including the two CV rows that already carry an order --
untouched. A csv round-trip would risk re-quoting unrelated cells.
"""
import csv
import pathlib
import sys

RES = pathlib.Path(__file__).resolve().parent
TARGET = RES / "36-t10-structures-draft.csv"
ORDERS = ["39-t10-section-orders-transactional.csv",
          "40-t10-section-orders-longform.csv",
          "41-t10-section-orders-marketing.csv"]
KEEP = {"cv-academic", "cv-experienced"}  # already authored; never overwritten

orders = {}
for name in ORDERS:
    with (RES / name).open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            key = r["structure_key"].strip()
            if key in orders:
                sys.exit("%s: duplicate structure_key %r" % (name, key))
            orders[key] = r["Section Order"].strip()

raw = TARGET.read_bytes()
if b"\r\n" in raw or b'"' in raw or raw.startswith(b"\xef\xbb\xbf"):
    sys.exit("36-t10-structures-draft.csv is no longer plain LF/unquoted/no-BOM; "
             "the line-based merge below is unsafe -- rewrite it before rerunning")
lines = raw.decode("utf-8").split("\n")
header = lines[0].split(",")
COL = header.index("Section Order")

changed, seen = 0, set()
for i, line in enumerate(lines[1:], 1):
    if not line:
        continue
    cells = line.split(",")
    key = cells[0]
    seen.add(key)
    if key in KEEP or key not in orders:
        continue
    if cells[COL] and cells[COL] != orders[key]:
        sys.exit("%s: Section Order already set to %r, refusing to overwrite"
                 % (key, cells[COL]))
    if cells[COL] == orders[key]:
        continue
    cells[COL] = orders[key]
    lines[i] = ",".join(cells)
    changed += 1

missing = sorted(k for k in orders if k not in seen)
if missing:
    sys.exit("order files name structure_key(s) absent from the draft: %s" % missing)
overlap = sorted(KEEP & set(orders))
if overlap:
    sys.exit("order files try to set a protected CV row: %s" % overlap)

TARGET.write_bytes("\n".join(lines).encode("utf-8"))
empty = [l.split(",")[0] for l in lines[1:] if l and not l.split(",")[COL]]
print("merged %d row(s); %d structure row(s) total; still empty: %s"
      % (changed, len(seen), empty or "none"))
