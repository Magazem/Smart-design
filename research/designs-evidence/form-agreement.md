# form — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10)

**Corrected 2026-09-25 per research/82a-gate-failures.md §0/§9/§4.1:** `agreement.py`'s
`clean_feature_cell` now strips an after-comma note the same way it already stripped a
parenthetical one (e.g. `one-accent, BORDERLINE` -> `one-accent`). `FMA:004`'s colour cell
carried exactly that trailing note, which the parser previously compared verbatim against the
second coder's plain `one-accent`, counting a real agreement as a disagreement. Re-running the
committed invocation below now reports colour `A_f = 0.2500` (1/4 agreements) instead of the
prior `0.0000` (0/4) — still a FAIL, but the corrected number (matching §4.1's "0.25 corrected").
No other value in this file changed.

Computed by `research/designs-evidence/agreement.py`. Form has no `header treatment` slot (its
identity feature in that position is `field_style`, unchanged by 82a-general) — only `colour use`
is recoded, from `form-recode-82ag.md`, via the generic `--override colour=PATH` flag (not the
`--recode` header+colour shorthand, since there is no header column here to override). Exact
invocation used for this file:

```
python research/designs-evidence/agreement.py --family form \
  --first FMA:research/designs-evidence/form-corpus.md \
  --override colour=research/designs-evidence/form-recode-82ag.md \
  --second research/designs-evidence/form-second-coder.md
```

## Inputs

- First coder [FMA] `form-corpus.md`: 4 coded rows found (2 coded tables detected — the original
  2-authority table, `FMA:001` USWDS/`FMA:002` GOV.UK, plus the Fm.8 addendum's 2-authority
  table, `FMA:003` ABS/`FMA:004` NHS).
- Second coder `form-second-coder.md`: 4 coded rows found (1 coded table detected).

## Overrides applied

- `colour` from `form-recode-82ag.md`: 4 override rows found (2 tables — a `(r1)`/`(r2ag)`
  translation-recode table for `FMA:001`/`002`, and a direct verification table for `FMA:003`/
  `004`), all 4 matched an existing first-coder id, 4 values changed:

  | id | old (r1) | new (recode) |
  |---|---|---|
  | FMA:001 | mono at rest | mono |
  | FMA:002 | mono at rest | mono |
  | FMA:003 | *(not extracted — see note)* | mono |
  | FMA:004 | *(not extracted — see note)* | one-accent |

  Note: `form-corpus.md`'s Fm.8 addendum table spells its colour column
  `"colour (82a-general §B)"`; this header text does not match any of the script's plain
  `colour`/`color`/`colour use` aliases, so the first coder's own colour value for `FMA:003`/
  `004` was never picked up from the corpus table directly (`old` shows as empty above). The
  override still supplies the correct value for both ids, since `form-recode-82ag.md`'s own
  addendum table (Fm.8.3-sourced) uses a header the override matcher does recognize
  (`find_value_column` strips the parenthetical and matches the bare `colour` left over). No
  numeric value is lost — `mono`/`one-accent` are exactly the corpus's Fm.8.3 values,
  independently re-derived by the recoder and confirmed unchanged (the recode's raw cell reads
  `one-accent, BORDERLINE`; the after-comma `BORDERLINE` note is now stripped the same way a
  parenthetical one would be — 2026-09-25 correction above).

## Sample

4 ids (n=4, all items — form has only 4 coded items total, below the 10-item family-wide floor,
so the second coder's own draw is "all 4, order immaterial"): `FMA:001, FMA:002, FMA:003,
FMA:004`. All 4 matched a first-coder row directly by id.

**Small-n caveat:** n=4 is far below the ~10-item family-wide sample size used for every other
family. A single disagreement moves A_f by 0.25; the per-feature numbers below should be read as
indicative, not as statistically comparable to the other families' n=9/10 runs.

## Per-feature agreement (post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 4 | 0 | 0.0000 | 0.0000 | **FAIL** |
| heading | identity | 4 | 2 | 0.5000 | -0.3333 | **FAIL** |
| colour | identity | 4 | 1 | 0.2500 | 0.0000 | **FAIL** |
| field_style | identity | 4 | 4 | 1.0000 | 1.0000 | PASS |
| body | variant | 0 | - | n/a (no shared coded sample) | n/a | n/a |
| rules_boxes | variant | 4 | 4 | 1.0000 | 1.0000 | PASS |
| density | variant | 0 | - | n/a (no shared coded sample) | n/a | n/a |
| admissible | admit/exclude | 4 | 4 | 1.0000 | 1.0000 | PASS |

## Disagreements (full sample)

| id | feature | coder1 (recode-superseded) | coder2 |
|---|---|---|---|
| FMA:001 | columns | 1 | 2-sidebar |
| FMA:001 | heading | sans | serif |
| FMA:001 | colour | mono | one-accent |
| FMA:002 | columns | 1 | 2-sidebar |
| FMA:002 | colour | mono | one-accent |
| FMA:003 | columns | 1 | 2-sidebar |
| FMA:003 | heading | serif | sans |
| FMA:003 | colour | mono | one-accent |
| FMA:004 | columns | 1 | 2-sidebar |

`FMA:004` colour is no longer listed as a disagreement: coder 1's (recode-superseded) cell
`one-accent, BORDERLINE` and coder 2's `one-accent` now compare equal once the after-comma note
is stripped (2026-09-25 correction above).

`columns` disagrees on all 4/4 items: the first coder reads each authority's own left-hand
navigation/TOC panel as not a "column" for a form (a component-doc page, not the form itself),
the second coder reads the same panel as a genuine `2-sidebar` layout. `colour` disagrees on 3/4
(FMA:001, FMA:002, FMA:003; `FMA:004` is now a real agreement per the 2026-09-25 correction
above, so the agreement count moved from 0/4 to 1/4): the second coder counts each authority's
link colour (`one-accent`) where the first coder
(post-recode) reads it as state-only/excluded (`mono`) — this is the same error-state-red
ambiguity `form-recode-82ag.md` itself flags as unresolved.

## Gate verdict

**FAIL** — identity features `columns` (A_f=0.00), `heading` (A_f=0.50) and `colour` (A_f=0.25,
post-recode, corrected 2026-09-25) are all below the 0.80 falsifier-gate threshold. Only
`field_style` (1.00) passes among the identity set.

Three identity features fail, so **form fails the family-wide second-coder gate** — decisively,
not marginally, though on an n=4 sample this should be read as "the two coders read this small,
unusual (no-raster, CSS-sourced) corpus very differently" rather than as a precise rate estimate.
`rules_boxes` and `admissible` (both 1.00) pass; `body` and `density` have no shared coded sample
(n=0, non-gating, not usable for filling either).
