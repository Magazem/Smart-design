# letter — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10, C12)

Computed by `research/designs-evidence/agreement.py`. `header treatment` and `colour use` are
pulled from `letter-recode-82ag.md` via `--recode` — a fresh-worker recode under
`research/82a-general.md` covering all 34 items in `letter-items-l2.csv` (the L2/LibreOffice +
Microsoft-catalogue pool: `LOL:###`, `MSL:###`). The GitHub corpus (`letter-corpus-github.md`,
`GH:###`) was coded under `research/82a-general.md` directly by its own worker and is **not**
overridden — no recode file touches it. Every other feature (columns, body, rules/boxes,
density, letterhead position, admissible) is unchanged from the two corpus files. Exact
invocation used for this file:

```
python research/designs-evidence/agreement.py --family letter \
  --first L2:research/designs-evidence/letter-corpus-l2.md \
          GH:research/designs-evidence/letter-corpus-github.md \
  --recode research/designs-evidence/letter-recode-82ag.md \
  --second research/designs-evidence/letter-second-coder.md \
  --exclude MSL:001 MSL:003 MSL:005 MSL:009 LOL:001 LOL:021 LOL:027 LOL:046
```

(`letter-corpus-l2.md` carries two qualifying coded tables — L.3 `MSL:###` and L.4 `LOL:###` —
both parsed and merged under the `L2` label; `letter-corpus-github.md` carries one, `GH:###`.)

**Sensitivity exclusion (82a-general C12, exposure disclosure):** the second coder disclosed
having read part of the first-round (pre-82a-general) evidence file before this assignment —
directly-seen rows `MSL:001`/`003`, plus ids named as archetype exemplars in frequency rows also
seen (`MSL:005`, `MSL:009`, `LOL:001`, `LOL:021`, `LOL:027`, `LOL:046`) — 8 ids total, all of
which happen to fall in the sample. The exclusion list here is the second coder's own widened
list (all 8 exposed ids), not just the narrower `MSL:001-004` the orchestrator first flagged.

## Inputs

- First coder [L2] `letter-corpus-l2.md`: 34 coded rows found (2 coded tables detected).
- First coder [GH] `letter-corpus-github.md`: 40 coded rows found (1 coded table detected).
- Second coder `letter-second-coder.md`: 19 coded rows found (1 coded table detected).

## Overrides applied

- `header` from `letter-recode-82ag.md`: 34 override rows found (2 tables), all 34 matched an
  existing first-coder id, 8 values changed (`LOL:033`, `LOL:039`, `LOL:040`, `MSL:001`,
  `MSL:008`, `MSL:010`, `MSL:012`, `MSL:013`).
- `colour` from `letter-recode-82ag.md`: 34 override rows found (2 tables), all 34 matched, 8
  values changed (`LOL:021`, `LOL:022`, `LOL:040`, `LOL:046`, `MSL:001`, `MSL:012`, `MSL:013`,
  `MSL:019`).

## Sample

19 ids (family-wide over both corpora, 74 total coded ids, C10): `LOL:021, GH:034, GH:023,
MSL:003, LOL:027, LOL:001, GH:014, MSL:009, LOL:045, GH:030, GH:032, LOL:046, GH:046, GH:049,
GH:009, MSL:001, MSL:005, GH:039, GH:051`. All 19 matched a first-coder row directly by id.

## Per-feature agreement — full sample (n=19, post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 19 | 19 | 1.0000 | 1.0000 | PASS |
| heading | identity | 19 | 18 | 0.9474 | 0.8939 | PASS |
| colour | identity | 19 | 18 | 0.9474 | 0.8995 | PASS |
| header | identity | 19 | 17 | 0.8947 | 0.7901 | PASS |
| body | variant | 19 | 19 | 1.0000 | 1.0000 | PASS |
| rules_boxes | variant | 19 | 12 | 0.6316 | 0.4009 | **FAIL** |
| density | variant | 19 | 18 | 0.9474 | 0.8902 | PASS |
| letterhead_position | variant | 19 | 14 | 0.7368 | 0.5815 | **FAIL** |
| admissible | admit/exclude | 19 | 19 | 1.0000 | 1.0000 | PASS |

## Sensitivity run — excluding the 8 exposed ids (n=11)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 11 | 11 | 1.0000 | 1.0000 | PASS |
| heading | identity | 11 | 10 | 0.9091 | 0.0000 | PASS |
| colour | identity | 11 | 11 | 1.0000 | 1.0000 | PASS |
| header | identity | 11 | 11 | 1.0000 | 1.0000 | PASS |
| body | variant | 11 | 11 | 1.0000 | 1.0000 | PASS |
| rules_boxes | variant | 11 | 4 | 0.3636 | 0.0723 | **FAIL** |
| density | variant | 11 | 10 | 0.9091 | 0.0000 | PASS |
| letterhead_position | variant | 11 | 6 | 0.5455 | 0.3293 | **FAIL** |
| admissible | admit/exclude | 11 | 11 | 1.0000 | 1.0000 | PASS |

Every identity-feature disagreement in the full sample (`MSL:001` header/colour, `MSL:005`
header, `GH:051` heading) sits among the excluded exposed ids or is otherwise resolved once they
drop out — the sensitivity run's identity block reaches 1.00/0.91/1.00/1.00 (heading's one
remaining disagreement is `GH:051`, which was never flagged as exposed, so it survives the
sensitivity run unchanged; it alone doesn't move heading below 0.80).

## Disagreements (full sample)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| GH:034 | rules_boxes | none | rules |
| GH:023 | rules_boxes | none | rules |
| GH:030 | density | airy | standard |
| GH:030 | letterhead_position | top-right | top-left |
| GH:032 | rules_boxes | none | rules |
| GH:032 | letterhead_position | top-left | top-right |
| GH:046 | rules_boxes | none | rules |
| GH:046 | letterhead_position | top-left | top-right |
| GH:009 | rules_boxes | none | rules |
| MSL:001 | colour | multi | one-accent |
| MSL:001 | header | band | ruled |
| MSL:005 | header | ruled | plain-centered |
| GH:039 | rules_boxes | none | rules |
| GH:039 | letterhead_position | top-left | top-right |
| GH:051 | heading | sans | serif |
| GH:051 | rules_boxes | none | rules |
| GH:051 | letterhead_position | top-left | top-right |

`rules_boxes` disagreements are one-directional: the second coder reads a rule the first coder
missed (`none` -> `rules`) on 6 of 7 GH ids, never the reverse — a systematic under-detection by
one side, not random noise. `letterhead_position` disagreements are all `top-left` vs `top-right`
swaps on the same 4 GH ids as the rules_boxes misses — likely the same underlying
misidentification of which side of the header the sender block sits on.

## Gate verdict

**PASS** — every identity feature (columns 1.00, heading 0.95, colour 0.95, header 0.89) and
admissible (1.00) clears the 0.80 falsifier gate, in both the full sample and the sensitivity
run excluding the 8 disclosed-exposure ids. **Letter clears the family-wide second-coder gate.**

Two variant features fail and are dropped from filling (family default used instead) per §7's
last sentence — this does not fail the gate: `rules_boxes` (0.63 full / 0.36 sensitivity) and
`letterhead_position` (0.74 full / 0.55 sensitivity). `body` and `density` pass and remain usable.
