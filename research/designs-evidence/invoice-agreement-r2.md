# invoice — inter-coder agreement, ROUND 2 (research/82 §7, amended by research/82a-clarifications-1.md C10, C12)

Round 1 (`invoice-agreement.md`) predates the header/colour recode; this file supersedes it for
`header`/`colour`, using a fresh second-coder sample (`invoice-second-coder-r2.md`, 12 ids).
Computed by `research/designs-evidence/agreement.py`. `header treatment` and `colour use` are
pulled from `invoice-recode-82ag.md` via `--recode` (fresh-worker recode under
`research/82a-general.md`, covering all 48 coded invoice items — 40 GitHub + 8 Microsoft
Create). Every other feature (columns, body, rules/boxes, density, totals position, table
rules, admissible) is unchanged from `invoice-corpus.md`. Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family invoice \
  --first GH:research/designs-evidence/invoice-corpus.md \
          MS:research/designs-evidence/invoice-corpus.md \
  --recode research/designs-evidence/invoice-recode-82ag.md \
  --second research/designs-evidence/invoice-second-coder-r2.md \
  --exclude GH:075
```

(Both `--first` labels point at the same file, `invoice-corpus.md`, since it carries two
qualifying coded tables — one keyed `GH:###` (40 items), one keyed `MS:###` (8 items) — both
parsed and merged.)

**Sensitivity exclusion (82a-general C12):** `GH:075` is a worked example in
`research/82a-general.md` §C (colour -> one-accent) and is in this sample; the second coder
disclosed this exposure and reports the measurement was made independently regardless. Per
82a-general D.3, A_f is also reported excluding it (n=11).

## Inputs

- First coder [GH] `invoice-corpus.md`: 48 coded rows found (2 coded tables detected — the
  GH-keyed and MS-keyed tables are both picked up and merged under this one label; the script
  reports the same merged 48-row count for each of the two `--first` entries since they read
  the same file).
- First coder [MS] `invoice-corpus.md`: 48 coded rows found (2 coded tables detected).
- Second coder `invoice-second-coder-r2.md`: 12 coded rows found (1 coded table detected).

## Overrides applied

- `header` from `invoice-recode-82ag.md`: 48 override rows found, all 48 matched an existing
  first-coder id, 24 values changed (half the corpus) — heavily concentrated on flipping
  `split` to `ruled`/`plain-left`/`band` (17 of the 24 changes touch a `split` value on either
  side), e.g. `GH:004, GH:009, GH:011, GH:012, GH:058, GH:066, GH:068, GH:075, GH:080, GH:096,
  GH:097, GH:099, MS:003, MS:005, MS:006` move away from `split`, while `MS:002, MS:004, MS:008`
  move onto `split` from `band`; `GH:016, GH:054, GH:061, GH:119` involve `plain-centered`.
- `colour` from `invoice-recode-82ag.md`: 48 override rows found, all 48 matched, 25 values
  changed — concentrated on the `fill-blocks`/`one-accent`/`mono` boundary (`fill-blocks` is
  the old value in 8 of the 25 changes, always moving to `one-accent` or `mono`).

## Sample

12 ids: `GH:035, GH:096, GH:090, GH:058, MS:002, GH:060, GH:075, GH:009, GH:011, GH:027, GH:005,
MS:004`. All 12 matched a first-coder row directly by id.

## Unknown/uncoded value excluded from n (82a C7)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| MS:002 | totals_position | other | unknown |

## Per-feature agreement — full sample (n=12, post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 12 | 12 | 1.0000 | 1.0000 | PASS |
| heading | identity | 12 | 12 | 1.0000 | 1.0000 | PASS |
| colour | identity | 12 | 10 | 0.8333 | 0.7209 | PASS |
| header | identity | 12 | 10 | 0.8333 | 0.7778 | PASS |
| body | variant | 12 | 11 | 0.9167 | 0.0000 | PASS |
| rules_boxes | variant | 12 | 11 | 0.9167 | 0.8235 | PASS |
| density | variant | 12 | 6 | 0.5000 | 0.2174 | **FAIL** |
| totals_position | variant | 11 | 11 | 1.0000 | 1.0000 | PASS |
| table_rules | variant | 12 | 10 | 0.8333 | 0.7551 | PASS |
| admissible | admit/exclude | 12 | 9 | 0.7500 | 0.5000 | **FAIL** |

## Sensitivity run — excluding GH:075 (n=11)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 11 | 11 | 1.0000 | 1.0000 | PASS |
| heading | identity | 11 | 11 | 1.0000 | 1.0000 | PASS |
| colour | identity | 11 | 9 | 0.8182 | 0.6901 | PASS |
| header | identity | 11 | 9 | 0.8182 | 0.7500 | PASS |
| body | variant | 11 | 10 | 0.9091 | 0.0000 | PASS |
| rules_boxes | variant | 11 | 10 | 0.9091 | 0.7925 | PASS |
| density | variant | 11 | 5 | 0.4545 | 0.1852 | **FAIL** |
| totals_position | variant | 10 | 10 | 1.0000 | 1.0000 | PASS |
| table_rules | variant | 11 | 9 | 0.8182 | 0.7317 | PASS |
| admissible | admit/exclude | 11 | 8 | 0.7273 | 0.4407 | **FAIL** |

`GH:075` was a full-agreement item (no row in the disagreement list), so excluding it only
shrinks n by 1 per feature and nudges `colour`/`header` down slightly (0.8333 -> 0.8182, both
still PASS) — no gate outcome changes between the two runs.

## Disagreements (full sample)

| id | feature | coder1 (recode-superseded) | coder2 |
|---|---|---|---|
| GH:096 | colour | one-accent | mono |
| GH:096 | body | sans | serif |
| GH:090 | admissible | yes | no |
| GH:058 | header | plain-left | split |
| GH:058 | rules_boxes | boxes | rules |
| GH:058 | density | dense | standard |
| GH:058 | table_rules | header-and-total | row-hairlines |
| MS:002 | table_rules | header-and-total | row-hairlines |
| GH:060 | density | dense | standard |
| GH:009 | density | airy | standard |
| GH:011 | header | band | plain-left |
| GH:011 | density | standard | airy |
| GH:027 | density | dense | standard |
| GH:005 | admissible | no | yes |
| MS:004 | colour | mono | fill-blocks |
| MS:004 | density | dense | airy |
| MS:004 | admissible | yes | no |

`density` fails almost entirely in one direction: 5 of 6 disagreements are the first coder
reading `dense`/`standard` where the second coder reads one level airier (`dense`->`standard`
x3, `standard`->`airy` x1, `airy`->`standard` x1 the other way) — a systematic density-scale
calibration gap between coders, not random noise. `admissible` disagreements go both ways
(2 no->yes, 1 yes->no on the 3 disagreeing ids), no systematic bias there.

## Gate verdict

**FAIL** — `admissible` (A_f=0.75 full / 0.73 sensitivity) is below the 0.80 falsifier-gate
threshold in both runs. All 4 tested identity features pass: `columns` (1.00), `heading` (1.00),
`colour` (0.83 full / 0.82 sensitivity, post-recode) and `header` (0.83 full / 0.82 sensitivity,
post-recode).

Only the `admissible` gating feature fails, so **invoice round 2 fails the family-wide
second-coder gate on admissibility alone** — the header/colour recode itself is vindicated
(both now clear 0.80), but the admissibility calls need review before invoice archetypes are
used for filling. `density` (0.50 full / 0.45 sensitivity) is a variant feature and is
individually dropped from filling (family default used instead) per §7's last sentence; `body`,
`rules_boxes`, `totals_position` and `table_rules` all pass and remain usable.
