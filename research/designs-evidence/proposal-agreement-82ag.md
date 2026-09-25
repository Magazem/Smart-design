# proposal — inter-coder agreement, recomputed with the 82ag header/colour recode (research/82 §7)

Computed by `research/designs-evidence/agreement.py`. Same inputs and sample as the committed
`proposal-agreement.md`, with `--recode proposal-recode-82ag.md` added. Exact invocation used
for this file:

```
python research/designs-evidence/agreement.py --family proposal \
  --first GH:research/designs-evidence/proposal-corpus-github.md \
          MSP:research/designs-evidence/proposal-corpus-ms.md \
  --recode research/designs-evidence/proposal-recode-82ag.md \
  --second research/designs-evidence/proposal-second-coder.md
```

## The recode has no effect here — explained

`proposal-recode-82ag.md` recodes `header`/`colour` for `MSP:001` through `MSP:007` only
(the 7 rows of `proposal-items-ms.csv`, "a Microsoft-templates corroboration corpus — not a
ranked corpus"). But the `MSP` **first-coder** file, `proposal-corpus-ms.md`, has **0 coded
rows** (no coded table was ever built there — this is unchanged from the committed
`proposal-agreement.md`, which already reports "First coder [MSP] ... 0 coded rows found").
Per `agreement.py --override`'s own contract, "Only ids already present in a --first file are
affected" — since no `MSP:###` id exists as a first-coder row, the recode's 7 override rows
find 0 matches and change 0 values. The run below is therefore numerically identical to the
committed `proposal-agreement.md`, feature-for-feature.

The second coder's sample still names `MSP:006` and `MSP:007` (see the WARNING below) — these
remain unmatched to any first-coder row regardless of the recode, exactly as in the committed
file, and are excluded from every feature's n the same way (10 of 12 sampled ids resolve to a
first-coder row; the other 2 do not exist in the corpus this agreement run draws on).

## Inputs

- First coder [GH] `proposal-corpus-github.md`: 40 coded rows found (1 coded table detected).
- First coder [MSP] `proposal-corpus-ms.md`: 0 coded rows found (0 coded tables detected).
- Second coder `proposal-second-coder.md`: 12 coded rows found (1 coded table detected).

## Overrides applied

- `header` from `proposal-recode-82ag.md`: 7 override rows found, 0 matched an existing
  first-coder id, 0 values changed.
- `colour` from `proposal-recode-82ag.md`: 7 override rows found, 0 matched an existing
  first-coder id, 0 values changed.

## Sample

12 ids: `GH:012, GH:014, GH:018, GH:025, GH:027, GH:029, GH:036, GH:037, GH:063, GH:092,
MSP:006, MSP:007`.

## WARNING: unmatched sample ids (no first-coder row by id or name)

`MSP:006`, `MSP:007` — same as the committed file; effective n = 10.

## Per-feature agreement (full sample, n=10)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| heading | identity | 10 | 8 | 0.8000 | 0.6226 | PASS |
| colour | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| header | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| body | variant | 10 | 10 | 1.0000 | 1.0000 | PASS |
| rules_boxes | variant | 10 | 6 | 0.6000 | 0.3750 | FAIL |
| density | variant | 10 | 3 | 0.3000 | -0.1290 | FAIL |
| cover_page | variant | 0 | - | n/a (no shared coded sample) | n/a | n/a |
| admissible | admit/exclude | 10 | 10 | 1.0000 | 1.0000 | PASS |

## Disagreements (full sample) — unchanged from the committed file

| id | feature | coder1 | coder2 |
|---|---|---|---|
| GH:012 | heading | sans | serif |
| GH:012 | rules_boxes | rules | none |
| GH:018 | rules_boxes | boxes | none |
| GH:025 | density | airy | standard |
| GH:027 | density | standard | airy |
| GH:029 | density | dense | standard |
| GH:036 | rules_boxes | none | rules |
| GH:036 | density | airy | standard |
| GH:037 | density | airy | standard |
| GH:063 | density | standard | airy |
| GH:092 | heading | display | serif |
| GH:092 | rules_boxes | boxes | none |
| GH:092 | density | dense | standard |

## Gate verdict

**PASS — every identity feature (and admissible) A_f >= 0.80.** Unchanged by the recode: since
`proposal-corpus-ms.md` has no coded first-coder rows, the recode file has nothing to override
in this computation, so this result is numerically identical to the already-committed
`proposal-agreement.md`. **The committed PASS still holds**, plainly: recomputing with
`--recode proposal-recode-82ag.md` added does not change a single feature's A_f, kappa, or
disagreement list.

Variant features `rules_boxes` and `density` fail — non-gating, dropped from filling.
`cover_page` has n=0 shared coded sample — not gating, not usable for filling either.
