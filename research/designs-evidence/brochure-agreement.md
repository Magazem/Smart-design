# brochure — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10)

Computed by `research/designs-evidence/agreement.py` (generic, reusable — see that file's
docstring). This run uses the script's new `--recode` override: `header treatment` and
`colour use` are pulled from `brochure-recode-82ag.md` (a fresh worker's recode of those two
features under `research/82a-general.md`, superseding the first coder's original values for all
11 coded brochure items) instead of from `brochure-corpus.md`'s own header/colour cells. Every
other feature (panel count, body, rules/boxes, density, admissible) is unchanged, straight from
`brochure-corpus.md` B.3. Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family brochure \
  --first LOB:research/designs-evidence/brochure-corpus.md \
          MSB:research/designs-evidence/brochure-corpus.md \
  --recode research/designs-evidence/brochure-recode-82ag.md \
  --second research/designs-evidence/brochure-second-coder.md
```

(Both `--first` labels point at the same file, `brochure-corpus.md`, because its one coded
table — B.3 — already carries explicit `LOB:###`/`MSB:###` ids; the LABEL is only needed to
sanity-check the prefix and is never used to synthesize an id here.)

## Inputs

- First coder [LOB] `brochure-corpus.md`: 14 coded rows found (1 coded table detected).
- First coder [MSB] `brochure-corpus.md`: 14 coded rows found (1 coded table detected).
- Second coder `brochure-second-coder.md`: 10 coded rows found (1 coded table detected).

## Overrides applied

- `header` from `brochure-recode-82ag.md`: 11 override rows found, all 11 matched an existing
  first-coder id, 3 values changed:

  | id | old (r1) | new (recode) |
  |---|---|---|
  | MSB:007 | plain-left | image-hero |
  | MSB:008 | band | plain-left |
  | LOB:004 | plain-centered | plain-left |

- `colour` from `brochure-recode-82ag.md`: 11 override rows found, all 11 matched, 0 values
  changed (the recode confirms every colour-use call the first coder already made).

## Sample

10 ids (n=10 of 11, per C10's family-wide `ceil(0.25*n)` floor with a 10-item cap): `LOB:003,
LOB:004, MSB:001, MSB:002, MSB:003, MSB:005, MSB:007, MSB:008, MSB:009, MSB:010`. All sampled
ids matched a first-coder row directly by id (no name-based fallback needed).

## Per-feature agreement (post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| panel_count | identity | 10 | 9 | 0.9000 | 0.4737 | PASS |
| heading | identity | 10 | 8 | 0.8000 | 0.0000 | PASS |
| colour | identity | 10 | 6 | 0.6000 | 0.2857 | **FAIL** |
| header | identity | 10 | 4 | 0.4000 | 0.1549 | **FAIL** |
| body | variant | 10 | 9 | 0.9000 | 0.0000 | PASS |
| rules_boxes | variant | 10 | 8 | 0.8000 | 0.6825 | PASS |
| density | variant | 10 | 9 | 0.9000 | 0.6154 | PASS |
| admissible | admit/exclude | 10 | 9 | 0.9000 | 0.0000 | PASS |

## Disagreements (full sample)

| id | feature | coder1 (recode-superseded) | coder2 |
|---|---|---|---|
| LOB:003 | colour | mono | multi |
| LOB:003 | body | serif | sans |
| LOB:004 | panel_count | single-sheet | 2 |
| LOB:004 | header | plain-left | ruled |
| LOB:004 | rules_boxes | rules | boxes |
| LOB:004 | density | standard | airy |
| LOB:004 | admissible | no | yes |
| MSB:001 | header | plain-left | image-hero |
| MSB:003 | heading | sans | display |
| MSB:003 | colour | fill-blocks | one-accent |
| MSB:003 | header | plain-left | image-hero |
| MSB:005 | header | plain-left | image-hero |
| MSB:005 | rules_boxes | rules | none |
| MSB:007 | header | image-hero | ruled |
| MSB:008 | colour | fill-blocks | mono |
| MSB:009 | header | plain-left | image-hero |
| MSB:010 | heading | sans | plain-left title, sans |
| MSB:010 | colour | fill-blocks | mono |

(`MSB:010`'s heading disagreement — `sans` vs `plain-left title, sans` — is verbatim from
`brochure-second-coder.md`'s own heading-class cell, not a parser artifact.)

## Gate verdict

**FAIL** — identity features `colour` (A_f=0.60) and `header` (A_f=0.40, post-recode) are both
below the 0.80 falsifier-gate threshold. `panel_count` (0.90), `heading` (0.80) and `admissible`
(0.90) pass.

Both failing features are IDENTITY features, so **brochure fails the family-wide second-coder
gate**. Per §7, a failing identity feature does not merely drop that feature from filling — it
fails the family's archetype gate outright: brochure archetypes distinguished by `header`/
`colour` are not admissible for filling until re-examined. The passing variant features (body,
rules_boxes, density) are individually fine, but the family as a whole does not clear the gate.
