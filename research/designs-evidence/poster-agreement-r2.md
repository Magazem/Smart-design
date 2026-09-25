# poster — inter-coder agreement, ROUND 2 (research/82 §7, amended by research/82a-clarifications-1.md C10, C12)

**Note on why this file exists:** the task that produced this file was framed as "the existing
`poster-agreement.md` was computed WITHOUT the recode; write a round-2 file WITH the recode."
That premise does not hold: `poster-agreement.md` (already in the repo) already invokes
`agreement.py` with `--override header=poster-recode-82ag.md colour=poster-recode-82ag.md`
(equivalent to `--recode poster-recode-82ag.md`), and its per-feature numbers already reflect
the recode. Checked directly: re-running the same inputs **without** any recode/override
produces different numbers (`colour` A_f 0.5000, `header` A_f 0.7857, both additionally
failing) — confirming `poster-agreement.md` is the recoded run, not a pre-recode one. This file
reproduces that same recoded computation (same command, same inputs) for the record, per the
instruction to write it regardless; its numbers are therefore identical to
`poster-agreement.md`'s. `poster-agreement.md` itself was left untouched, as instructed.

Computed by `research/designs-evidence/agreement.py`. `header treatment` and `colour use` are
pulled from `poster-recode-82ag.md` (fresh-worker recode under `research/82a-general.md`,
scoped to the 40 `poster-items-github.csv` / `GH:###` items only — the recoder never opened the
MS+Typst pool file or any agreement file). `poster-corpus-ms.md`'s P.5 pool (`PM:###`/`PT:###`/
`PIM:###`, 15 items) was coded fresh under `research/82a-general.md` by its own worker and is
**not** overridden. Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family poster \
  --first GH:research/designs-evidence/poster-corpus-github.md \
          MS:research/designs-evidence/poster-corpus-ms.md \
  --recode research/designs-evidence/poster-recode-82ag.md \
  --second research/designs-evidence/poster-second-coder.md \
  --exclude GH:019
```

**Sensitivity exclusion (82a-general C12):** the second coder disclosed prior exposure
concerning `GH:019` (its gold headings); the exclusion here rests specifically on that
exposure, not on its body-text reading. No other poster codes were flagged as exposed.

## Inputs

- First coder [GH] `poster-corpus-github.md`: 40 coded rows found (1 coded table detected).
- First coder [MS] `poster-corpus-ms.md`: 15 coded rows found (1 coded table detected) — the
  P.5 pool (8 MS Create + 7 Typst Universe posters).
- Second coder `poster-second-coder.md`: 14 coded rows found (1 coded table detected).

## Overrides applied

- `header` from `poster-recode-82ag.md`: 39 override rows found (of 40 GH items — `GH:014`'s
  preview is a GitHub star-history badge, uncodeable, excluded from N by the recode itself), all
  39 matched an existing first-coder id, 11 values changed: `GH:005, GH:006, GH:013, GH:017,
  GH:022, GH:029, GH:032, GH:036, GH:037, GH:051, GH:052`.
- `colour` from `poster-recode-82ag.md`: 39 override rows found, all 39 matched, 13 values
  changed: `GH:006, GH:009, GH:010, GH:013, GH:017, GH:020, GH:022, GH:029, GH:032, GH:036,
  GH:039, GH:043, GH:046`.

## Sample

14 ids (family-wide over both GH and MS/Typst pools, C10): `GH:003, GH:008, GH:019, GH:020,
GH:021, GH:022, GH:036, GH:040, GH:046, GH:051, PIM:004, PT:pasquino, PT:pollux,
PT:simple-research-poster`. All 14 matched a first-coder row directly by id.

## Per-feature agreement — full sample (n=14, post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 14 | 14 | 1.0000 | 1.0000 | PASS |
| heading | identity | 14 | 12 | 0.8571 | 0.7143 | PASS |
| colour | identity | 14 | 10 | 0.7143 | 0.5882 | **FAIL** |
| header | identity | 14 | 12 | 0.8571 | 0.7941 | PASS |
| body | variant | 14 | 10 | 0.7143 | 0.3913 | **FAIL** |
| rules_boxes | variant | 14 | 7 | 0.5000 | 0.2403 | **FAIL** |
| density | variant | 14 | 9 | 0.6429 | 0.4444 | **FAIL** |
| orientation | variant | 0 | - | n/a (no shared coded sample) | n/a | n/a |
| admissible | admit/exclude | 14 | 9 | 0.6429 | -0.2069 | **FAIL** |

## Disagreements (full sample)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| GH:003 | rules_boxes | boxes | none |
| GH:008 | colour | one-accent | multi |
| GH:019 | rules_boxes | none | boxes |
| GH:019 | density | airy | standard |
| GH:019 | admissible | yes | no |
| GH:020 | heading | serif | sans |
| GH:021 | body | sans | serif |
| GH:021 | rules_boxes | boxes | none |
| GH:021 | density | dense | standard |
| GH:022 | body | sans | serif |
| GH:036 | colour | fill-blocks | mono |
| GH:036 | header | band | plain-centered |
| GH:036 | rules_boxes | boxes | rules |
| GH:036 | density | standard | dense |
| GH:040 | rules_boxes | boxes | rules |
| GH:040 | density | standard | dense |
| GH:040 | admissible | yes | no |
| GH:046 | body | sans | serif |
| GH:046 | admissible | no | yes |
| GH:051 | heading | serif | sans |
| GH:051 | colour | one-accent | fill-blocks |
| GH:051 | header | ruled | plain-centered |
| PIM:004 | density | dense | standard |
| PIM:004 | admissible | no | yes |
| PT:pasquino | colour | mono | multi |
| PT:pasquino | body | serif | sans |
| PT:pasquino | rules_boxes | none | rules |
| PT:pasquino | admissible | no | yes |
| PT:pollux | rules_boxes | none | rules |

## Sensitivity run — excluding GH:019 (n=13)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 13 | 13 | 1.0000 | 1.0000 | PASS |
| heading | identity | 13 | 11 | 0.8462 | 0.6977 | PASS |
| colour | identity | 13 | 9 | 0.6923 | 0.5517 | **FAIL** |
| header | identity | 13 | 11 | 0.8462 | 0.7719 | PASS |
| body | variant | 13 | 9 | 0.6923 | 0.3659 | **FAIL** |
| rules_boxes | variant | 13 | 7 | 0.5385 | 0.3036 | **FAIL** |
| density | variant | 13 | 9 | 0.6923 | 0.5185 | **FAIL** |
| orientation | variant | 0 | - | n/a (no shared coded sample) | n/a | n/a |
| admissible | admit/exclude | 13 | 9 | 0.6923 | -0.1304 | **FAIL** |

Dropping `GH:019` moves `colour` 0.7143 -> 0.6923 and `admissible` stays FAIL either way
(0.6429 full / 0.6923 sensitivity) — the sensitivity exclusion does not change the gate
verdict.

## Gate verdict

**FAIL** — identity features `colour` and `admissible` are below A_f >= 0.80 in both the full
sample and the sensitivity run, even after the header/colour recode. `columns`, `heading` and
`header` all pass. Poster does not pass the §7 gate.

Variant features `body`, `rules_boxes` and `density` also fail — non-gating, dropped from
filling per §7's last sentence. `orientation` has n=0 shared coded sample — not gating, not
usable for filling either, family default used.

This matches `poster-agreement.md` exactly (both are the recoded computation; see the note at
the top of this file).
