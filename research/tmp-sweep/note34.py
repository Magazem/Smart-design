#!/usr/bin/env python3
"""Every count and every blank in research/34-gate-invisible-gaps.md.

Run from the repo root:  python3 research/tmp-sweep/note34.py
Reads only. Writes nothing. Prints each claim with the number that backs it.

Logic, stated so the note is reproducible:
  A) UNDECLARED COLUMNS. A column is "undeclared" if it appears in the manifest's
     tables[t].columns and has no type row in 09-library-schema.md. Type rows are
     found the same way note 33 found them: inside the `## T<n>.` section for that
     table file, in a markdown table whose header is literally `| Column | Type | ...`,
     first cell entirely backticked. Here we only need the figures section, so the
     seven names are asserted against a literal list and re-derived from the section.
  B) ROLE BY ELIMINATION. A column's manifest role is the set of facets naming it:
     enums, foreign_keys, list_columns, searchable_columns, typed_json_columns,
     derived. Empty set => nothing can read it => P.
  C) BLANKS. A cell is blank iff value.strip() == "". Rows are identified by their
     key column, never by CSV line number.
  D) LIST-FK COVERAGE. A foreign key with list=true that is absent from the same
     table's list_columns gets no well-formedness check.
"""
import csv, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "skill/document-design-intelligence/data/base"
MAN  = json.loads((ROOT / "skill/document-design-intelligence/data/schema-manifest.json").read_text(encoding="utf-8"))
SCHEMA = (ROOT / "research/09-library-schema.md").read_text(encoding="utf-8").split("\n")

def rows(table):
    with open(BASE / (table + ".csv"), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def typed_columns_of_section(heading_re):
    """Column names carrying a type row, bounded by the next '##' of any kind."""
    start = next(i for i, l in enumerate(SCHEMA) if re.match(heading_re, l))
    end = next((i for i in range(start + 1, len(SCHEMA)) if SCHEMA[i].startswith("##")), len(SCHEMA))
    out, in_table = set(), False
    for l in SCHEMA[start:end]:
        if l.startswith("| Column | Type |"):
            in_table = True; continue
        if in_table:
            if not l.startswith("|"):
                in_table = False; continue
            cell = l.split("|")[1].strip()
            if re.fullmatch(r"(`[^`]+`)(\s*/\s*`[^`]+`)*", cell):   # backticked, '/'-joined
                out |= {n.strip("` ") for n in cell.split("/")}
    return out

print("=== A. figures columns with no type row ===")
declared = typed_columns_of_section(r"^## T11\.")
figcols = MAN["tables"]["figures"]["columns"]
key = MAN["tables"]["figures"]["key_column"]
undeclared = [c for c in figcols if c != key and c not in declared]
print("  manifest columns: %d   key: %s   typed: %d   UNDECLARED: %d"
      % (len(figcols), key, len(declared), len(undeclared)))
for c in undeclared:
    print("    -", c)
assert len(undeclared) == 7, undeclared

print("\n=== B. role by elimination, and populated-ness ===")
spec = MAN["tables"]["figures"]
facets = {"enums": set(spec.get("enums", {})),
          "foreign_keys": set(spec.get("foreign_keys", {})),
          "list_columns": set(spec.get("list_columns") or {}),
          "searchable_columns": set(spec.get("searchable_columns", [])),
          "typed_json_columns": set(spec.get("typed_json_columns", [])),
          "derived": set(spec.get("derived", []))}
frows = rows("figures")
for c in undeclared:
    named = [f for f, s in facets.items() if c in s]
    blanks = [r[key] for r in frows if not r[c].strip()]
    print("  %-20s facets=%-22s blank on %d/%d rows" % (c, ",".join(named) or "NONE", len(blanks), len(frows)))

print("\n=== B2. Accessibility Grade value distribution (the enum question) ===")
from collections import Counter
for v, n in Counter(r["Accessibility Grade"] for r in frows).most_common():
    print("  %3d  %s" % (n, v if len(v) < 60 else v[:57] + "..."))

print("\n=== C. blanks in the two R foreign keys of doctypes ===")
drows = rows("doctypes")
dkey = MAN["tables"]["doctypes"]["key_column"]
for col in ("Structure Key", "Constraint Set Keys"):
    blank = [r[dkey] for r in drows if not r[col].strip()]
    print("  %-20s blank on %d/%d: %s" % (col, len(blank), len(drows), ", ".join(blank)))

print("\n=== C2. the three deck rows, on the two columns 26-notes:148 proposes branching on ===")
for r in drows:
    if r[dkey].startswith("slide-deck-"):
        print("  %-22s Render=%-26s CSK=%r" % (r[dkey], r["Render Target Keys"], r["Constraint Set Keys"]))

print("\n=== D. list FKs undeclared in list_columns ===")
tot = 0
for t, s in MAN["tables"].items():
    lc = s.get("list_columns") or {}
    for c, v in (s.get("foreign_keys") or {}).items():
        if isinstance(v, dict) and v.get("list"):
            tot += 1
            print("  %-16s %-22s declared in list_columns: %s" % (t, c, c in lc))
print("  total list FKs: %d ; non-FK list columns covered: %d"
      % (tot, sum(len(s.get("list_columns") or {}) for s in MAN["tables"].values())))
