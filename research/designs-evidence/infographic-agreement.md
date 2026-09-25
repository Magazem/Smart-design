# infographic — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10)

Computed by `research/designs-evidence/agreement.py`. First coder is the single juried pool
`infographic-corpus-iib.md` (IIB:###, N=12, I.8.4's coded table, coded under
`research/82a-general.md` with the "charts are marks" reading flagged there). No
`infographic-recode-82ag.md` exists, so `--recode` was not used. Exact invocation used for
this file:

```
python research/designs-evidence/agreement.py --family infographic \
  --first IIB:research/designs-evidence/infographic-corpus-iib.md \
  --second research/designs-evidence/infographic-second-coder.md
```

Infographic has no family-specific identity/variant feature slot (research/82 §4 default:
identity = columns, heading, colour, header; variant = body, rules/boxes, density) and no
family fail constraint.

## Inputs

- First coder [IIB] `infographic-corpus-iib.md`: 12 coded rows found (1 coded table detected).
- Second coder `infographic-second-coder.md`: 10 coded rows found (1 coded table detected).

## Sample

Per 82a C10, the sample is drawn family-wide over the 12 pool ids, seeded
`random.Random("82a:infographic")`: IIB:148, 171, 142, 139, 135, 075, 049, 116, 125, 163 (n=10,
`max(min(10, 12), ceil(0.25*12))`).

## id-scheme check

All 10 sampled ids matched a first-coder row directly by id (no name-based fallback needed) —
the first coder's I.8.4 table and the second coder's file use the identical `IIB:###` scheme.

## Per-feature agreement (full sample, n=10)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (≥0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 10 | 7 | 0.7000 | 0.5455 | **FAIL** |
| heading | identity | 10 | 8 | 0.8000 | 0.6296 | PASS (at threshold) |
| colour | identity | 10 | 7 | 0.7000 | 0.5000 | **FAIL** |
| header | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| body | variant | 10 | 8 | 0.8000 | 0.6000 | PASS (at threshold) |
| rules_boxes | variant | 10 | 3 | 0.3000 | 0.0141 | **FAIL** |
| density | variant | 10 | 4 | 0.4000 | 0.0625 | **FAIL** |
| admissible | admit/exclude | 10 | 9 | 0.9000 | 0.7368 | PASS |

## Disagreements (full sample)

| id | feature | coder1 (first) | coder2 (second) |
|---|---|---|---|
| IIB:049 | density | standard | airy |
| IIB:075 | heading | sans | display |
| IIB:075 | colour | fill-blocks | one-accent |
| IIB:075 | rules_boxes | none | rules |
| IIB:075 | density | standard | airy |
| IIB:116 | columns | 1 | 2-sidebar |
| IIB:116 | colour | fill-blocks | multi |
| IIB:116 | rules_boxes | none | rules |
| IIB:116 | admissible | yes | no |
| IIB:125 | colour | fill-blocks | mono |
| IIB:125 | rules_boxes | none | rules |
| IIB:125 | density | standard | airy |
| IIB:135 | heading | serif | sans |
| IIB:135 | body | serif | sans |
| IIB:135 | rules_boxes | none | rules |
| IIB:139 | columns | 1 | grid |
| IIB:139 | body | sans | serif |
| IIB:139 | rules_boxes | rules | boxes |
| IIB:139 | density | standard | airy |
| IIB:142 | columns | 1 | 2-sidebar |
| IIB:142 | rules_boxes | none | boxes |
| IIB:142 | density | standard | airy |
| IIB:148 | rules_boxes | rules | boxes |
| IIB:148 | density | dense | standard |

24 disagreements across 8 of the 10 sampled ids (IIB:163 and IIB:171 matched on every feature).

## Gate verdict

**FAIL** — identity feature(s) `columns` (A_f 0.7000) and `colour` (A_f 0.7000) are below A_f
>= 0.80 (falsifier gate, C29: thresholds applied literally). `heading` (0.8000) and `admissible`
(0.9000) clear the gate.

Variant feature(s) below A_f >= 0.80, dropped from filling (family default used instead), per
§7's last sentence — does not fail the gate: rules_boxes, density.

Since the gate fails, infographic as coded from this pool + this second coder is not eligible
to fill from (research/82 §7/§8): the identity-feature disagreement rate on `columns` (grid vs.
`1`/`2-sidebar`/`3+`) and `colour` (`fill-blocks` vs. `multi`/`mono`/`one-accent`) is too high to
trust the pool's archetype counts as ground truth. This does not by itself contradict I.8.6's
frequency table (which counts the first coder's own codes, not a cross-coder agreement); it
means those counts have not been independently verified at the required threshold.
