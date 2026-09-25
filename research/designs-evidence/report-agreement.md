# report — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10, C12)

Computed by `research/designs-evidence/agreement.py`. Three first-coder corpora: GitHub L1
(`report-corpus-github.md`, `GH:###`, 40), Microsoft Create L2 (`report-corpus-ms.md`,
`MSR:###`, 10), and ARC Awards L3 juried (`report-corpus-l3.md`, `ARC25:###`, 14). `header
treatment` and `colour use` are pulled from `report-recode-82ag.md` (fresh-worker recode under
`research/82a-general.md`, covering all 64 coded items across the three corpora). Every other
feature (columns, body, rules/boxes, density, cover page, admissible) is unchanged from the
three corpus files. Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family report \
  --first GH:research/designs-evidence/report-corpus-github.md \
          MSR:research/designs-evidence/report-corpus-ms.md \
          ARC25:research/designs-evidence/report-corpus-l3.md \
  --recode research/designs-evidence/report-recode-82ag.md \
  --second research/designs-evidence/report-second-coder.md
```

**Parser bug found and fixed while running this (generic, in `agreement.py`, not a data
edit):** `report-recode-82ag.md`'s `MSR:009` row quotes a footer credit line containing
un-escaped literal pipes (`"HENRY ROSS | FEDERAL GOVERNMENT | SEPTEMBER 9, 2023"`). The old
`split_row()` split on every `|`, shifting every later cell on that row and reporting `colour`
override = the literal string `FEDERAL GOVERNMENT` instead of `mono`. Fixed generically:
`split_row()` now also treats pipes inside a balanced double-quoted span within a cell as
literal (in addition to the existing backslash-escape handling), falling back to the old
plain split for any row with an odd quote count. Re-run after the fix: `MSR:009`'s colour
override reads correctly as `one-accent -> mono` (see table below). No other row in any
family's evidence files was found to have this shape, and no other value changed as a result
of the fix (checked by diffing before/after full output).

## Inputs

- First coder [GH] `report-corpus-github.md`: 40 coded rows found (1 coded table detected).
- First coder [MSR] `report-corpus-ms.md`: 10 coded rows found (1 coded table detected).
- First coder [ARC25] `report-corpus-l3.md`: 14 coded rows found (1 coded table detected).
- Second coder `report-second-coder.md`: 16 coded rows found (1 coded table detected).

## Overrides applied

- `header` from `report-recode-82ag.md`: 64 override rows found, all 64 matched an existing
  first-coder id, 15 values changed: `GH:022, GH:051, GH:077, GH:092, GH:094, GH:103, GH:104,
  GH:129, MSR:001, MSR:003, MSR:004, MSR:005, MSR:007, ARC25:018, ARC25:029`.
- `colour` from `report-recode-82ag.md`: 64 override rows found, all 64 matched, 23 values
  changed: `GH:010, GH:032, GH:060, GH:067, GH:079, GH:085, GH:103, GH:123, GH:134, GH:138,
  MSR:001, MSR:005, MSR:007, MSR:009, ARC25:011, ARC25:014, ARC25:018, ARC25:020, ARC25:021,
  ARC25:029, ARC25:033, ARC25:036, ARC25:037`.

## Sample

16 ids (family-wide over all three corpora, C10): `ARC25:011, ARC25:018, ARC25:020, ARC25:029,
GH:019, GH:025, GH:058, GH:060, GH:069, GH:094, GH:104, GH:129, MSR:002, MSR:003, MSR:005,
MSR:008`. All 16 matched a first-coder row directly by id.

## Unknown/uncoded values excluded from n (82a C7)

8 cells, all on the 4 sampled MSR items (`rules_boxes` and `density` are `unknown` for both
coders on `MSR:002, MSR:003, MSR:005, MSR:008` — the MS Create corpus discloses these two
features as uncodeable from a cover-only thumbnail, R2 of `report-corpus-ms.md`).

## Per-feature agreement (full sample, n=16, post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 16 | 16 | 1.0000 | 1.0000 | PASS |
| heading | identity | 16 | 15 | 0.9375 | 0.8750 | PASS |
| colour | identity | 16 | 15 | 0.9375 | 0.8769 | PASS |
| header | identity | 16 | 12 | 0.7500 | 0.6384 | **FAIL** |
| body | variant | 16 | 15 | 0.9375 | 0.8710 | PASS |
| rules_boxes | variant | 12 | 9 | 0.7500 | 0.6000 | **FAIL** |
| density | variant | 12 | 10 | 0.8333 | 0.7000 | PASS |
| cover_page | variant | 0 | - | n/a (no shared coded sample) | n/a | n/a |
| admissible | admit/exclude | 16 | 13 | 0.8125 | -0.0909 | PASS |

## Disagreements (full sample)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| ARC25:018 | rules_boxes | boxes | rules |
| ARC25:018 | admissible | yes | no |
| ARC25:020 | admissible | yes | no |
| ARC25:029 | colour | fill-blocks | mono |
| ARC25:029 | body | serif | sans |
| GH:019 | rules_boxes | rules | none |
| GH:025 | admissible | no | yes |
| GH:058 | heading | sans | serif |
| GH:060 | density | dense | standard |
| GH:094 | header | ruled | plain-centered |
| GH:094 | rules_boxes | none | rules |
| GH:104 | header | band | plain-centered |
| GH:129 | header | plain-centered | ruled |
| GH:129 | density | dense | standard |
| MSR:003 | header | band | image-hero |

## Gate verdict

**FAIL** — identity feature `header` is below A_f >= 0.80 (0.7500), even after the
header/colour recode. `columns`, `heading`, `colour` and `admissible` all pass; `header` alone
fails the falsifier gate (research/82 §7), so **report does not pass the §7 gate as a whole**
(a family passes only if every identity feature, including admissible, clears 0.80).

Variant feature `rules_boxes` also fails (0.7500) — non-gating, dropped from filling per §7's
last sentence; `density` and `body` pass; `cover_page` has n=0 shared coded sample (both
coders coded it `unknown`/uncodeable everywhere sampled) — not gating, not usable for filling
either, family default used.
