# cover-letter — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10, C12)

Computed by `research/designs-evidence/agreement.py`. `header treatment` and `colour use` are
pulled from `cover-letter-recode-82ag.md` via `--recode` (fresh-worker recode under
`research/82a-general.md`, covering all 15 items in the L2 pool, `MSC:###`). The GitHub corpus
(`cover-letter-corpus-github.md`, `GH:###`) is not overridden. Exact invocation used for this
file:

```
python research/designs-evidence/agreement.py --family cover-letter \
  --first L2:research/designs-evidence/cover-letter-corpus-l2.md \
          GH:research/designs-evidence/cover-letter-corpus-github.md \
  --recode research/designs-evidence/cover-letter-recode-82ag.md \
  --second research/designs-evidence/cover-letter-second-coder.md \
  --exclude MSC:007
```

**Sensitivity exclusion (82a-general C12):** `MSC:007` is a worked example in
`research/82a-general.md` §C (colour -> multi); the second coder disclosed this exposure and the
orchestrator ruled a sensitivity run excluding it (n=13).

## Inputs

- First coder [L2] `cover-letter-corpus-l2.md`: 15 coded rows found (1 coded table detected).
- First coder [GH] `cover-letter-corpus-github.md`: 40 coded rows found (1 coded table detected).
- Second coder `cover-letter-second-coder.md`: 14 coded rows found (1 coded table detected).

## Overrides applied

- `header` from `cover-letter-recode-82ag.md`: 15 override rows found, all 15 matched an
  existing first-coder id, 3 values changed:

  | id | old (r1) | new (recode) |
  |---|---|---|
  | MSC:003 | ruled | plain-left |
  | MSC:013 | plain-left | ruled |
  | MSC:015 | plain-centered | ruled |

- `colour` from `cover-letter-recode-82ag.md`: 15 override rows found, all 15 matched, 4 values
  changed:

  | id | old (r1) | new (recode) |
  |---|---|---|
  | MSC:002 | fill-blocks | mono |
  | MSC:003 | fill-blocks | one-accent |
  | MSC:004 | fill-blocks | mono |
  | MSC:009 | fill-blocks | multi |

## Sample

14 ids: `MSC:013, GH:021, MSC:005, GH:060, GH:079, GH:042, GH:004, GH:024, GH:101, GH:122,
MSC:007, MSC:003, GH:067, GH:066`. All 14 matched a first-coder row directly by id.

## Per-feature agreement — full sample (n=14, post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 14 | 13 | 0.9286 | 0.0000 | PASS |
| heading | identity | 14 | 13 | 0.9286 | 0.8772 | PASS |
| colour | identity | 14 | 12 | 0.8571 | 0.7956 | PASS |
| header | identity | 14 | 12 | 0.8571 | 0.7627 | PASS |
| body | variant | 14 | 13 | 0.9286 | 0.8372 | PASS |
| rules_boxes | variant | 14 | 13 | 0.9286 | 0.8571 | PASS |
| density | variant | 14 | 10 | 0.7143 | 0.4167 | **FAIL** |
| photo | variant | 14 | 14 | 1.0000 | 1.0000 | PASS |
| admissible | admit/exclude | 14 | 12 | 0.8571 | 0.4400 | PASS |

## Sensitivity run — excluding MSC:007 (n=13)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 13 | 12 | 0.9231 | 0.0000 | PASS |
| heading | identity | 13 | 12 | 0.9231 | 0.8713 | PASS |
| colour | identity | 13 | 11 | 0.8462 | 0.7658 | PASS |
| header | identity | 13 | 11 | 0.8462 | 0.7547 | PASS |
| body | variant | 13 | 12 | 0.9231 | 0.8312 | PASS |
| rules_boxes | variant | 13 | 12 | 0.9231 | 0.8471 | PASS |
| density | variant | 13 | 9 | 0.6923 | 0.3500 | **FAIL** |
| photo | variant | 13 | 13 | 1.0000 | 1.0000 | PASS |
| admissible | admit/exclude | 13 | 11 | 0.8462 | 0.4348 | PASS |

Dropping `MSC:007` removes 1 shared item and does not change any gate outcome: `colour` moves
0.8571 -> 0.8462 (still PASS), `density` moves 0.7143 -> 0.6923 (still FAIL). `MSC:007` itself
never appears in the disagreement list below — it was a coder-agreement item, not a driver of
any of the failures.

## Disagreements (full sample)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| MSC:013 | header | ruled | plain-left |
| MSC:013 | density | standard | airy |
| GH:060 | colour | mono | fill-blocks |
| GH:060 | rules_boxes | none | rules |
| GH:060 | density | standard | airy |
| GH:079 | columns | 2-sidebar | 1 |
| GH:042 | body | serif | sans |
| GH:042 | admissible | yes | no |
| GH:101 | heading | sans | mono |
| MSC:003 | colour | one-accent | fill-blocks |
| MSC:003 | header | plain-left | ruled |
| GH:067 | density | airy | standard |
| GH:067 | admissible | yes | no |
| GH:066 | density | airy | standard |

## Gate verdict

**PASS** — every identity feature (columns 0.93, heading 0.93, colour 0.86, header 0.86) and
admissible (0.86) clears the 0.80 falsifier gate, in both the full sample and the
`MSC:007`-excluded sensitivity run. **Cover-letter clears the family-wide second-coder gate.**

One variant feature fails and is dropped from filling (family default used instead) — this does
not fail the gate: `density` (0.71 full / 0.69 sensitivity; disagreements split evenly between
airy-vs-standard in both directions, not a systematic bias). `body`, `rules_boxes` and `photo`
pass and remain usable.
