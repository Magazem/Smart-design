# memo — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10)

Computed by `research/designs-evidence/agreement.py`. `header treatment` and `colour use` are
pulled from `memo-recode-82ag.md` via `--recode`. `memo-corpus.md`'s M.6.2 table was itself
coded fresh under `research/82a-general.md` (not translated from an earlier §4 coding), so
`memo-recode-82ag.md` is a verification pass rather than a translation-recode: it re-derives
every header/colour call against 82a-general §A/§B line by line and reports **0 changes** — the
override is applied anyway, for auditability and consistency with the other three families, but
it has no numeric effect here. Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family memo \
  --first M:research/designs-evidence/memo-corpus.md \
  --recode research/designs-evidence/memo-recode-82ag.md \
  --second research/designs-evidence/memo-second-coder.md
```

**Note on sample scope:** the second coder sampled from the 11 ids present in `memo-items.csv`
at the time it read that file (`MSM:001`-`007`, `OLM:002/008/009/010`); a 12th id, `OLH:001`
(an Overleaf template added to `memo-items-pool.csv` while the second-coding was in progress),
was **not** in `memo-items.csv` yet and so was never sampled or coded by the second coder. This
run's sample is therefore drawn only from the 11 ids the second coder actually saw; `OLH:001` is
absent from both coders' evidence and out of scope for this gate computation.

## Inputs

- First coder [M] `memo-corpus.md`: 25 coded rows found (3 coded tables detected). The file grew
  while this project was in progress (its own note): the original 11-id M.6.2 table
  (`MSM:001`-`007`, `OLM:002/008/009/010`), a 12-id revision of the same pool adding `OLH:001`,
  and a 13-id GitHub-sourced pool table, all three carrying an `adm` column and qualifying as
  "coded". Per the script's per-file merge rule, a repeated id keeps the value from whichever
  qualifying table is parsed first — here that's the original 11-id M.6.2 table, so the 9
  sampled ids below resolve to that table's values, unaffected by the later additions.
- Second coder `memo-second-coder.md`: 9 coded rows found (1 coded table detected) — the 9
  ids actually drawn by the seeded sample out of the 11 available in the M.6.2 pool (`MSM:003`
  and one other were not selected; see the sample list below).

## Overrides applied

- `header` from `memo-recode-82ag.md`: 11 override rows found, all 11 matched an existing
  first-coder id, **0 values changed** (every header-treatment call verified correct).
- `colour` from `memo-recode-82ag.md`: 11 override rows found, all 11 matched, **0 values
  changed** (every colour-use call verified correct).

## Sample

9 ids (of the 10-id seeded draw over the 11-id pool — `MSM:003` was not selected by the second
coder's own `random.Random("82a:memo")` draw): `MSM:001, MSM:002, MSM:004, MSM:005, MSM:006,
OLM:002, OLM:008, OLM:009, OLM:010`. All 9 matched a first-coder row directly by id.

## Unknown/uncoded values excluded from n (82a C7)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| OLM:002 | body | serif | unknown |
| OLM:002 | density | airy | unknown |

## Per-feature agreement (post-recode, no-op)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 9 | 9 | 1.0000 | 1.0000 | PASS |
| heading | identity | 9 | 8 | 0.8889 | 0.7692 | PASS |
| colour | identity | 9 | 8 | 0.8889 | 0.8421 | PASS |
| header | identity | 9 | 3 | 0.3333 | 0.0182 | **FAIL** |
| body | variant | 8 | 8 | 1.0000 | 1.0000 | PASS |
| rules_boxes | variant | 9 | 9 | 1.0000 | 1.0000 | PASS |
| density | variant | 8 | 7 | 0.8750 | 0.6000 | PASS |
| admissible | admit/exclude | 9 | 9 | 1.0000 | 1.0000 | PASS |

## Disagreements (full sample)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| MSM:001 | heading | sans | serif |
| MSM:001 | colour | one-accent | fill-blocks |
| MSM:002 | header | ruled | plain-left |
| MSM:004 | header | ruled | plain-left |
| MSM:005 | header | ruled | plain-left |
| MSM:006 | header | plain-left | split |
| OLM:009 | header | plain-left | split |
| OLM:010 | header | plain-left | split |
| OLM:010 | density | airy | standard |

`header` disagreements are concentrated on the ruled-vs-plain-left boundary (MSM:002/004/005:
first coder reads a nearby rule as meeting the ruled thresholds, second coder does not) and the
plain-left-vs-split boundary (MSM:006, OLM:009, OLM:010: second coder reads a routing/address
block on the opposite side of the title as a genuine split, first coder does not).

## Gate verdict

**FAIL** — identity feature `header` (A_f=0.33) is below the 0.80 falsifier-gate threshold, even
though the recode confirmed every one of the 11 header values as correct under
research/82a-general.md — this is a genuine coder disagreement on where the ruled/plain-
left/split boundary lines fall, not a rubric-translation artifact. `columns` (1.00), `heading`
(0.89), `colour` (0.89) and `admissible` (1.00) pass.

One identity feature fails, so **memo fails the family-wide second-coder gate**. Memo
archetypes distinguished by `header` are not admissible for filling until re-examined; the
`colour` distinction (0.89) and all three variant features (body, rules_boxes, density) pass and
remain usable.
