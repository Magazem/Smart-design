#!/usr/bin/env python3
"""Recompute round-2 header-treatment agreement: cv-second-coder-r2.md vs the
recode column "header (r2a)" in cv-header-recode.md. Standalone, no deps beyond stdlib."""
import re

recode_path = "cv-header-recode.md"
second_path = "cv-second-coder-r2.md"

# Parse the per-item table in cv-header-recode.md for id -> header (r2a)
r2a = {}
with open(recode_path, encoding="utf-8") as f:
    lines = f.readlines()

in_table = False
for line in lines:
    if line.startswith("| id | item | header (r1)"):
        in_table = True
        continue
    if in_table:
        if not line.startswith("|"):
            if line.strip() == "":
                continue
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] in ("---", "") or cells[0].startswith("---"):
            continue
        if cells[0] == "id":
            continue
        item_id = cells[0]
        header_r2a_raw = cells[4]
        # strip trailing "**(A-change)**" markers
        header_r2a = re.sub(r"\s*\*\*\(A-change\)\*\*", "", header_r2a_raw).strip()
        r2a[item_id] = header_r2a

# Parse cv-second-coder-r2.md Results table for id -> header
second = {}
with open(second_path, encoding="utf-8") as f:
    lines2 = f.readlines()

in_table2 = False
for line in lines2:
    if line.startswith("| id | header | deciding test"):
        in_table2 = True
        continue
    if in_table2:
        if not line.startswith("|"):
            if line.strip() == "":
                continue
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0].startswith("---"):
            continue
        second[cells[0]] = cells[1]

assert len(second) == 20, f"expected 20 sampled ids, got {len(second)}"

n = len(second)
agree = 0
disagreements = []
for item_id, val2 in second.items():
    val1 = r2a.get(item_id)
    if val1 is None:
        raise SystemExit(f"id {item_id} not found in recode table")
    if val1 == val2:
        agree += 1
    else:
        disagreements.append((item_id, val1, val2))

A_f = agree / n
print(f"n={n} agreements={agree} A_f={A_f:.4f}")
print("Disagreements:")
for item_id, v1, v2 in disagreements:
    print(f"  {item_id}: recode(r2a)={v1!r}  second-coder(r2)={v2!r}")
