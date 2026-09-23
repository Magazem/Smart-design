# deck — inter-coder agreement (research/82 §7, amended by research/82a-clarifications-1.md C10)

Computed by `research/designs-evidence/agreement.py` (generic, reusable — takes `--family`,
one or more `--first LABEL:path` first-coder evidence files, and `--second path`; see that
file's docstring). This run required generalizing the script beyond its original cv-only
feature set (§0 below). Exact invocation used for this file:

```
python research/designs-evidence/agreement.py --family deck \
  --first NPM:research/designs-evidence/deck-corpus-npm.md \
          LO:research/designs-evidence/deck-corpus-lo-ms.md \
  --second research/designs-evidence/deck-second-coder.md
```

## 0. Bug found and fixed in `agreement.py`

The script was written against the cv family's feature names (`columns`, `heading`,
`colour`, `header`) and detected "the coded table" in a file by requiring an exact superset
match on those five header cells (+ `admissible`). Running it for `deck` — whose identity
features are `background`/`title-slide layout` (replacing `columns`/`header`), and whose two
first-coder corpora use different abbreviated header spellings (`bg`/`head`/`title`/`rules`/
`dens`/`adm` in `deck-corpus-lo-ms.md` vs `background`/`title-layout`/`rules/boxes`/`density`/
`Admissible` in `deck-corpus-npm.md`) — matched **zero** tables in every file, so every
feature's `n` was 0, and the script's gate check (`n>0 and po<0.80` ⇒ FAIL) never triggered
for any feature with `n==0`, printing a bare **PASS**. That is a false pass on no data, not a
verified pass.

Fixed by:
1. **Per-family feature set** (research/82 §4): `agreement.py` now has a `FAMILY_FEATURES`
   table giving each family's identity features (2 universal — heading, colour — + 2
   family-specific, e.g. deck's `background`/`title_layout` replacing `columns`/`header`,
   brochure's `panel_count` replacing `columns`, form's `field_style` replacing `header`) and
   variant features (3 universal — body, rules/boxes, density — + family extras: cv/
   cover-letter `photo`; invoice/quote `totals_position`/`table_rules`; letter
   `letterhead_position`; poster `orientation`; report/whitepaper/proposal `cover_page`).
   `admissible` is implicit and gating in every family.
2. **Tolerant coded-table detection**: a much larger header-alias table (`bg`→background,
   `head`→heading, `title`/`title-layout`/`title-slide layout`→title_layout, `rules`→
   rules/boxes, `dens`→density, `adm`→admissible, `colour use`→colour, etc.), and a table now
   qualifies as "coded" if it has an admissible/adm column and matches *at least* all-but-one
   of the family's identity features (not a strict all-5 superset) — this also lets a single
   file hold more than one coded table under different id prefixes: `deck-corpus-lo-ms.md`
   has an `LO.3` section (`LO:###`, 40 rows) and a separate `MS.2–3` section (`MS:###`, 25
   rows), both parsed and merged.
3. **82a C7 (`unknown` handling)**: a coded value of `unknown` (optionally with a disclosed
   parenthetical reason) or a bare `-` placeholder (the MS table's own convention for a
   feature it structurally cannot code, since Microsoft Create only publishes one thumbnail
   per template) is not a real code. Agreement for a feature is now computed only over items
   where **both** coders recorded a non-unknown value, and `n` (that shared count) is
   reported per feature — never silently averaged in as an agreement or a disagreement.
4. **n=0 on a gating feature (identity or admissible) is now a hard ERROR** (non-zero exit),
   never a silent PASS — this is the actual fix for the reported bug.
5. (Found in the same pass, same fix batch): the second coder's own evidence file appends
   disclosed detail after the coded enum value (e.g. `one-accent (gold)`, `display
   (handwriting-style "Excalifont"/Virgil glyphs)`, `standard (~30 words on content slide)`).
   The old `clean_feature_cell` kept that whole string, so almost every feature showed
   near-total "disagreement" against the first coder's bare `one-accent` — a formatting
   artifact, not a coding disagreement (cv's second-coder file never does this, so cv was
   unaffected). Cell values are now truncated at the first `(` or em/en-dash annotation
   marker; enum values never contain those characters (`one-accent`, `full-bleed-image`,
   `2-sidebar`, … only ever use a plain hyphen), so this is safe.

**cv reproduction check:** re-running the cv invocation (identical to
`research/designs-evidence/cv-agreement.md`'s own recorded command) after this rewrite
reproduces every number in that file exactly — `header` A_f=0.7000 (n=20, 14/20), `density`
A_f=0.6500 (n=20, 13/20), `colour` A_f=0.8000 (n=20, 16/20), same disagreement list, same
sensitivity-run numbers excluding GH:003/007/008. cv's feature set (columns/heading/colour/
header + body/rules_boxes/density/photo) is unchanged by the family-table refactor.

## 1. Inputs

- First coder [NPM] `research/designs-evidence/deck-corpus-npm.md`: 40 coded rows (1 coded
  table detected).
- First coder [LO] `research/designs-evidence/deck-corpus-lo-ms.md`: 65 coded rows (2 coded
  tables detected — `LO:001`–`LO:045` section, 40 rows; `MS:001`–`MS:025` section, 25 rows;
  the label `LO` only matters for Pos-only rows, which don't occur here since both sections
  already carry an explicit `id` column).
- Second coder `research/designs-evidence/deck-second-coder.md`: 27 coded rows (the §7/C10
  family-wide sample, seed `"82:deck"`, drawn by the second coder's own orchestrator-computed
  script over all 105 coded ids across the three corpora — see that file §2).

Total coded population: 40 (NPM) + 40 (LO) + 25 (MS) = 105, matching the second coder's own
stated total.

## 2. id-scheme check

All 27 sampled ids (`NPM:###`, `LO:###`, `MS:###`) resolved to a first-coder row by direct id
lookup — no name-based fallback was needed.

## 3. Unknown/uncoded values excluded from n (82a C7)

38 cells across the 27×8 feature grid were `unknown` (or `-`) on at least one side and are
excluded from that feature's `n` rather than counted as agreement or disagreement — almost
all on `body` and `density`, because a majority of sampled decks (MS templates especially,
which publish only slide 1) have no genuine second/content slide to read body text or word
count from. This is why `body` (n=9) and `density` (n=9) have a much smaller sample than the
identity features (n=26–27): per 82a C7, filling for these two variants falls back on the
family default wherever the archetype's own value is unknown, and the same floor applies to
this agreement computation.

## 4. Per-feature agreement (full sample, n=27 sampled; n per feature per §3 above)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (≥0.80) |
|---|---|---|---|---|---|---|
| background | identity | 27 | 22 | 0.8148 | 0.6973 | PASS |
| heading | identity | 26 | 20 | 0.7692 | 0.5679 | **FAIL** |
| colour | identity | 27 | 18 | 0.6667 | 0.5000 | **FAIL** |
| title-layout | identity | 26 | 19 | 0.7308 | 0.6136 | **FAIL** |
| body | variant | 9 | 7 | 0.7778 | 0.0000 | **FAIL** |
| rules/boxes | variant | 27 | 23 | 0.8519 | 0.7677 | PASS |
| density | variant | 9 | 2 | 0.2222 | -0.1053 | **FAIL** |
| admissible | admit/exclude | 27 | 21 | 0.7778 | 0.4564 | **FAIL** |

## 5. Disagreements (full sample)

46 disagreements across 22 of the 27 sampled ids; only 5 ids matched the first coder on
every non-unknown feature (`LO:030`, `NPM:054`, `NPM:032`, `NPM:069`, `MS:011`):

| id | feature | coder1 | coder2 |
|---|---|---|---|
| MS:010 | colour | one-accent | mono |
| MS:001 | background | image | light |
| NPM:018 | title-layout | centered | left |
| NPM:018 | body | display | sans |
| NPM:018 | density | airy | standard |
| LO:021 | heading | sans | serif |
| LO:021 | colour | fill-blocks | one-accent |
| LO:021 | admissible | no | yes |
| NPM:017 | heading | serif | sans |
| NPM:046 | title-layout | left | full-bleed-image |
| NPM:046 | rules/boxes | none | boxes |
| NPM:046 | density | standard | dense |
| LO:040 | density | airy | standard |
| NPM:139 | title-layout | centered | left |
| NPM:139 | density | airy | standard |
| LO:029 | background | dark | light |
| LO:029 | heading | sans | serif |
| LO:029 | colour | fill-blocks | multi |
| LO:029 | title-layout | split | centered |
| MS:013 | colour | fill-blocks | multi |
| MS:002 | rules/boxes | boxes | rules |
| MS:002 | admissible | no | yes |
| NPM:049 | title-layout | left | split |
| NPM:006 | admissible | no | yes |
| LO:028 | colour | fill-blocks | mono |
| LO:028 | density | standard | dense |
| LO:028 | admissible | no | yes |
| LO:025 | colour | multi | mono |
| LO:025 | title-layout | left | split |
| LO:025 | density | airy | standard |
| LO:025 | admissible | no | yes |
| NPM:009 | title-layout | left | centered |
| NPM:041 | colour | mono | one-accent |
| NPM:041 | rules/boxes | none | boxes |
| MS:024 | background | light | image |
| MS:024 | heading | sans | serif |
| LO:009 | heading | serif | sans |
| LO:009 | colour | fill-blocks | one-accent |
| LO:009 | body | serif | sans |
| LO:009 | density | standard | dense |
| LO:009 | admissible | no | yes |
| MS:003 | background | dark | image |
| MS:003 | heading | display | sans |
| MS:003 | rules/boxes | none | rules |
| MS:023 | colour | fill-blocks | mono |
| MS:025 | background | light | image |

Notable patterns:
- **`colour` is the worst identity feature** (A_f=0.6667), and the dominant failure mode is
  `fill-blocks` (first coder) vs. `multi`/`one-accent`/`mono` (second coder) on the *same*
  item six times (LO:021, LO:029, MS:013, LO:028, LO:009, MS:023) — i.e. not random noise but
  a systematic boundary dispute on when a solid non-white fill counts as `fill-blocks`
  (≥10% of page area, §4) versus reading the page as a plain accent/mono/multi-hue page.
  `background`-vs-`image` disagreement on largely-photographic slides (MS:001, MS:024,
  MS:003, MS:025) is the second cluster, all on Microsoft Create items with a partial photo
  treatment near the `image` threshold.
- **`title-layout` disagreements cluster on `centered`/`left`/`split` boundaries** (7 of 8),
  the same kind of soft-threshold dispute the cv family's `header` feature showed on
  `split`/`plain-centered`/`band`/`ruled`.
- **`admissible` disagreements are one-directional**: every one of the 6 mismatches is first
  coder `no` vs. second coder `yes` (never the reverse) — the second coder's sample did not
  independently flag any additional A2/A3/A5/A7 violation the first coder missed; it simply
  didn't confirm six of the first coder's own admissibility exclusions on re-inspection
  (LO:021, MS:002, NPM:006, LO:028, LO:025, LO:009 — all `no` reasons the first coder logged
  as A3/A5 fill/photo-behind-text or icon-repeat calls that the second coder's independent
  read did not reproduce).
- **`density` (n=9) is unusable**: only 2 of 9 shared-value items agree, and kappa is
  slightly negative — with a sample this small, and given both coders independently
  recorded `unknown` for the large majority of items (§3), this variant feature is not
  informative either way at this sample size.

## 6. Gate verdict

Per research/82 §7, the literal gate is **every** `A_f ≥ 0.80` across all eight features
(identity + variant + admissibility). That is **not** met:

- **Identity gate: FAIL.** Of the four identity features, only `background` (A_f=0.8148)
  clears 0.80. `heading` (0.7692), `colour` (0.6667) and `title-layout` (0.7308) all fail.
- **`admissible` (admit/exclude): FAIL** at A_f=0.7778 — the one-directional
  first-coder-`no`/second-coder-`yes` pattern noted above.
- **Variant features**: `rules/boxes` PASSes (0.8519); `body` (0.7778, n=9) and `density`
  (0.2222, n=9) both FAIL, but on very small shared samples (§3, §5).

Because three of the four **identity** features fail (not just one, as in cv's single-feature
`header` failure), and `admissible` also fails, this is a full **F1 falsifier failure** per
research/82 §7: it requires an Opus-authored `research/82a-deck.md` amendment sharpening the
`colour` (fill-blocks threshold), `heading`/`title-layout` (boundary calls) and admissibility
(A3/A5 literalness) rules, a full recode of the deck family by the first coder, and a fresh
second-coder sample seeded `"82a:deck"`. This report does not perform that recode — it only
computes and discloses the agreement numbers, per the task brief.

Read narrowly per the task brief's own framing (identity features individually gate; a
failing variant feature only disqualifies that variant from filling rather than failing the
whole family):
- **Identity gate: FAIL** — `heading`, `colour`, `title-layout` are each individually below
  0.80; only `background` clears it.
- **Variant features `body` and `density` are disqualified from filling** — the family
  default is used instead of each archetype's own modal value for those two variants,
  wherever filling (§8) would otherwise consult them. `rules/boxes` passes and remains usable
  for filling.
- **`admissible` also fails** (0.7778) — per §7 this is one of the features the gate is
  computed over ("including admissibility"), so it is part of the same F1 falsifier failure
  above, not merely dropped from filling (admissibility isn't a filling input in the first
  place — it decides which items are even eligible to be counted, per §5/§6).

**Bottom line: the deck family's inter-coder agreement gate FAILS.** Three of four identity
features and admissibility itself are below the 0.80 threshold; per §7 the family requires a
sharpened rubric (`research/82a-deck.md`), a full recode, and a fresh second-coder sample
before its ranking can be trusted to the same standard as a family that passed.
