# flyer — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10)

Computed by `research/designs-evidence/agreement.py`. `header treatment` and `colour use` are
pulled from `flyer-recode-82ag.md` (fresh-worker recode under `research/82a-general.md`,
superseding `flyer-corpus.md`'s own header/colour cells for all 20 coded flyer items — both the
original F.x pool and the F.11.2 recount addition). Every other feature is unchanged, straight
from `flyer-corpus.md`. Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family flyer \
  --first MSF:research/designs-evidence/flyer-corpus.md \
  --recode research/designs-evidence/flyer-recode-82ag.md \
  --second research/designs-evidence/flyer-second-coder.md
```

(`flyer-corpus.md` carries two qualifying coded tables — the original pool and the F.11.2
recount — both keyed by explicit `MSF:###`/`MSFP:###` ids; both are parsed and merged. The
recode file likewise carries two tables, one per pool, both consumed by `--recode`.)

## Inputs

- First coder [MSF] `flyer-corpus.md`: 20 coded rows found (2 coded tables detected).
- Second coder `flyer-second-coder.md`: 10 coded rows found (1 coded table detected).

## Overrides applied

- `header` from `flyer-recode-82ag.md`: 20 override rows found (2 tables), all 20 matched an
  existing first-coder id, 5 values changed:

  | id | old (r1) | new (recode) |
  |---|---|---|
  | MSF:006 | plain-left | band |
  | MSF:010 | plain-centered | image-hero |
  | MSF:014 | band | plain-left |
  | MSF:017 | plain-centered | band |
  | MSF:027 | plain-centered | ruled |

- `colour` from `flyer-recode-82ag.md`: 20 override rows found (2 tables), all 20 matched, 4
  values changed:

  | id | old (r1) | new (recode) |
  |---|---|---|
  | MSF:012 | multi | fill-blocks |
  | MSF:017 | multi | fill-blocks |
  | MSF:018 | multi | one-accent |
  | MSFP:009 | multi | one-accent |

## Sample

10 ids (family-wide, C10): `MSF:006, MSF:007, MSF:008, MSF:009, MSF:010, MSF:012, MSF:022,
MSFP:007, MSFP:009, MSFP:010`. All sampled ids matched a first-coder row directly by id (no
name-based fallback needed).

## Per-feature agreement (post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 10 | 9 | 0.9000 | 0.0000 | PASS |
| heading | identity | 10 | 9 | 0.9000 | 0.7826 | PASS |
| colour | identity | 10 | 3 | 0.3000 | 0.1358 | **FAIL** |
| header | identity | 10 | 5 | 0.5000 | 0.3421 | **FAIL** |
| body | variant | 10 | 10 | 1.0000 | 1.0000 | PASS |
| rules_boxes | variant | 10 | 8 | 0.8000 | 0.6429 | PASS |
| density | variant | 10 | 9 | 0.9000 | 0.6154 | PASS |
| admissible | admit/exclude | 10 | 4 | 0.4000 | 0.0000 | **FAIL** |

## Disagreements (full sample)

| id | feature | coder1 (recode-superseded) | coder2 |
|---|---|---|---|
| MSF:006 | columns | 2-sidebar | 1 |
| MSF:006 | colour | fill-blocks | mono |
| MSF:006 | header | band | split |
| MSF:006 | admissible | no | yes |
| MSF:007 | heading | sans | display |
| MSF:007 | colour | fill-blocks | multi |
| MSF:007 | header | plain-left | ruled |
| MSF:007 | rules_boxes | none | rules |
| MSF:007 | admissible | no | yes |
| MSF:008 | colour | fill-blocks | multi |
| MSF:008 | admissible | no | yes |
| MSF:009 | colour | fill-blocks | one-accent |
| MSF:009 | rules_boxes | none | rules |
| MSF:009 | admissible | no | yes |
| MSF:010 | colour | one-accent | multi |
| MSF:010 | header | image-hero | ruled |
| MSF:010 | admissible | no | yes |
| MSF:012 | colour | fill-blocks | one-accent |
| MSF:012 | admissible | no | yes |
| MSF:022 | header | plain-centered | ruled |
| MSFP:007 | density | standard | airy |
| MSFP:010 | colour | fill-blocks | mono |
| MSFP:010 | header | plain-centered | image-hero |

The `admissible` disagreements (MSF:006, 007, 008, 009, 010, 012 — all "no" (first coder) vs
"yes" (second coder)) are a real coder split, not a data artifact: the first coder excluded
these under A3 (text directly on an un-opacified photo) or A5 (repeated decorative motif), the
second coder read the same items as passing. Checked against `flyer-corpus.md`'s exclusions log
(lines recording A3/A5 reasons for MSF:007-010) and `flyer-second-coder.md`'s own admissible
column.

## Gate verdict

**FAIL** — identity features `colour` (A_f=0.30), `header` (A_f=0.50, post-recode) and
`admissible` (A_f=0.40) are all below the 0.80 falsifier-gate threshold. `columns` (0.90) and
`heading` (0.90) pass.

Three gating features fail (two identity + admissible), so **flyer fails the family-wide
second-coder gate** decisively. Flyer archetypes distinguished by `header`/`colour`, and the
admissibility calls themselves, are not usable for filling until re-examined. The passing
variant features (body, rules_boxes, density) are individually fine but do not rescue the gate.
