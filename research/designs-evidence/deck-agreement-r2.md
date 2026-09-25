# deck — inter-coder agreement, ROUND 2 (research/82 §7, amended by research/82a-deck.md)

Computed by `research/designs-evidence/agreement.py`, using its new generic
`--override-features F1,F2,... --override-file PATH` flag. `deck-recode.md` already carries a
coded-shaped table (`id | heading | colour | title layout | admissible | rule | ...`) — round 2
recodes exactly these 4 features (heading, colour, title_layout, admissible) under
`research/82a-deck.md`; `background` and `rules_boxes` are **not** touched by this recode and are
**not** re-tested by the round-2 second coder either — both are carried over unchanged from round
1 (`deck-agreement.md`: background A_f=0.8148 PASS on n=27). Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family deck \
  --first NPM:research/designs-evidence/deck-corpus-npm.md \
          LO:research/designs-evidence/deck-corpus-lo-ms.md \
  --override-features heading,colour,title_layout,admissible \
  --override-file research/designs-evidence/deck-recode.md \
  --second research/designs-evidence/deck-second-coder-r2.md \
  --exclude LO:021 LO:029 MS:010 MS:013 NPM:006 NPM:018
```

**Script note (expected, not a bug):** `deck-second-coder-r2.md`'s coded table has no
`background` or `rules_boxes` column — round 2 only re-codes heading/colour/title_layout/
admissible, per 82a-deck's own scope. The script correctly reports `background` (a gating
identity feature for `deck` in its general `FAMILY_FEATURES` table) as n=0 and exits with an
ERROR rather than a silent PASS (its own C9-style safety rule: n=0 on a gating feature is never
a pass). This is expected here — round 2 is deliberately narrower than the family's full
identity set — so this file's gate verdict below is computed **manually over the 4 features round
2 actually tested**, quoting the script's own per-feature numbers for each; `background` is
carried forward from round 1 unchanged and is not re-adjudicated here. `rules_boxes` (variant,
non-gating) is likewise carried over from round 1 and out of scope.

**Sensitivity exclusion (82a-deck worked examples):** `LO:021, LO:029, MS:010, MS:013, NPM:006,
NPM:018` are the items the second coder names as matching 82a-deck's own worked table (i.e.
items whose call the second coder could have anchored on the worked example rather than coding
independently) — excluded for a sensitivity re-run per 82a-general/82a-deck's C12-style exposure
disclosure.

## Inputs

- First coder [NPM] `deck-corpus-npm.md`: 40 coded rows found (1 coded table detected).
- First coder [LO] `deck-corpus-lo-ms.md`: 65 coded rows found (2 coded tables detected).
- Second coder `deck-second-coder-r2.md`: 27 coded rows found (1 coded table detected).

## Overrides applied

`deck-recode.md`'s single 105-row coded table supplies all 4 overridden features for all 105
first-coder ids (40 NPM + 65 LO/MS):

| feature | rows found | matched | values changed vs r1 |
|---|---|---|---|
| heading | 105 | 105 | 12 |
| colour | 105 | 105 | 38 |
| title_layout | 105 | 105 | 22 |
| admissible | 105 | 105 | 31 |

`admissible` shows the largest swing: 31 items flip from the first coder's `no` to the recode's
`yes` (0 flip the other way) — a systematic loosening of round-1's admissibility calls, not
random noise; see `deck-recode.md`'s own worked reasoning per id.

## Sample

27 ids: `LO:011, LO:014, LO:015, LO:016, LO:021, LO:029, LO:031, LO:035, LO:041, MS:007, MS:010,
MS:013, MS:014, MS:018, MS:019, MS:020, NPM:002, NPM:006, NPM:018, NPM:025, NPM:026, NPM:031,
NPM:032, NPM:035, NPM:041, NPM:044, NPM:073`. All 27 matched a first-coder row directly by id.

## Per-feature agreement — full sample (n=27, post-recode)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| background | identity | *(round 1: 27)* | *(round 1: 22)* | *(round 1: 0.8148)* | *(round 1: 0.6973)* | PASS *(carried from round 1, not re-tested)* |
| heading | identity | 27 | 22 | 0.8148 | 0.6419 | PASS |
| colour | identity | 27 | 19 | 0.7037 | 0.5619 | **FAIL** |
| title_layout | identity | 27 | 25 | 0.9259 | 0.8858 | PASS |
| admissible | admit/exclude | 27 | 24 | 0.8889 | -0.0519 | PASS |

## Sensitivity run — excluding the 6 worked-example ids (n=21)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| background | identity | — | — | — | — | *(not re-tested in round 2)* |
| heading | identity | 21 | 16 | 0.7619 | 0.4324 | **FAIL** |
| colour | identity | 21 | 14 | 0.6667 | 0.4913 | **FAIL** |
| title_layout | identity | 21 | 19 | 0.9048 | 0.8462 | PASS |
| admissible | admit/exclude | 21 | 18 | 0.8571 | -0.0678 | PASS |

**This is the headline finding of round 2:** the full sample has only 1 identity failure
(`colour`), but once the 6 items the second coder flags as matching 82a-deck's own worked
examples are dropped, `heading` *also* drops below 0.80 (0.8148 -> 0.7619) — a second identity
feature fails. Per 82a-deck's stated gate rule, ≥2 failing identity features means **deck ships
no ranked archetypes** under the sensitivity view, even though the naive full-sample reading
would only drop `colour` and still ship archetypes on background/heading/title_layout.

## Disagreements (full sample)

| id | feature | coder1 (recode-superseded) | coder2 |
|---|---|---|---|
| LO:014 | heading | sans | display |
| LO:015 | admissible | yes | no |
| LO:031 | heading | sans | serif |
| LO:031 | colour | mono | one-accent |
| LO:041 | colour | one-accent | fill-blocks |
| MS:007 | heading | display | sans |
| MS:007 | colour | multi | mono |
| MS:007 | admissible | no | yes |
| MS:014 | heading | serif | sans |
| MS:018 | title_layout | centered | full-bleed-image |
| MS:019 | title_layout | left | split |
| NPM:002 | colour | mono | fill-blocks |
| NPM:018 | colour | multi | one-accent |
| NPM:026 | colour | one-accent | mono |
| NPM:031 | colour | one-accent | fill-blocks |
| NPM:032 | heading | sans | serif |
| NPM:073 | colour | mono | one-accent |
| NPM:073 | admissible | yes | no |

(`NPM:006` and `NPM:018` disagreements/agreements sit among the 6 excluded worked-example ids;
`NPM:018`'s `colour` disagreement — `multi` vs `one-accent` — is the item the second coder
disclosed hinges on whether a yellow annotation box is counted, so its removal in the
sensitivity run is expected to matter.)

## Gate verdict

**Full sample:** 1 of 4 tested identity features fails (`colour`, A_f=0.70), plus `background`
passing from round 1 (0.81) and `title_layout` (0.93) and `admissible` (0.89) all passing here.
Per 82a-deck's "a second failure drops that identity feature" rule, a single failing identity
feature is dropped from filling (deck archetypes lose the `colour` distinction) but deck still
ships ranked archetypes on `background`/`heading`/`title_layout`.

**Sensitivity run (excluding the 6 worked-example ids):** 2 of 4 tested identity features fail
(`heading` 0.76, `colour` 0.67). Per 82a-deck's stated rule, **≥2 failing identity features means
deck ships no ranked archetypes** under this view — the exposure to 82a-deck's own worked
examples appears to have propped up `heading` agreement in the full sample specifically on the
items the second coder could anchor on.

**Net statement:** deck round 2's gate outcome is exposure-sensitive. The disclosed, more
conservative reading (excluding the 6 worked-example ids) is the one that should govern: deck
does not clear the round-2 gate on 2 of its 4 recoded identity features, and — combined with the
`≥2 failing identity features -> no ranked archetypes` rule — **deck ships no ranked archetypes**
pending a further recode/re-sampling that avoids the worked-example anchoring.
