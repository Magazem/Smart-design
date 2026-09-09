# T2 doc-reasoning draft — notes (research/29-t2-doc-reasoning-draft.csv)

19 rows, `csv.reader`-clean, 12 columns matching the manifest's `doc-reasoning.csv` header
exactly (10 manifest columns + draft-only `Reasoning`/`Confidence`, stripped to
`rationale/doc-reasoning.md` at load per Rule 2 — see `handover-ddr.md`). 19 rows is a
verified 1:1 match against T1's 19 *unique* `Reasoning Key` values in
`research/26-t1-doctypes-draft.csv` (checked by script this pass). The prior handover's "21
rows" figure is stale, not a discrepancy: it predates two later T1 events that each removed
a key — the `ens-web-tool` drop and, mainly, Revision 3's deck-split revert, which collapsed
`deck-projection`/`deck-screen`/`deck-handout` back into one `deck-generic` key (-2). 21 - 2
= 19, exactly what's on disk.

## Doc Conditions — action targets fixed against the real `constraints.csv`, not the T1 brief's guesses

`26-notes.md`'s "guidance for whoever authors T2" table (written before T9's `constraints.csv`
was authored) proposed two action targets that **do not exist** in the shipped
`data/base/constraints.csv`: `constraint:field-underline-only` (for `if_hand_filled`) and
`constraint:print-legibility-l-delta` (for `if_professional_print`). Neither string appears
anywhere in the constraints table — they were placeholders, not verified names. This pass
checked every Doc Conditions action against the real file and used what's actually there:

| Doc Condition | Guidance-table guess (nonexistent) | Real target used | What it resolves to |
|---|---|---|---|
| `if_ats_target` | `constraint:ats-strict` (this one happened to be right) | `constraint:ats-strict` | **Set Key**, 7 T9 rows (6 fail + 1 warn) |
| `if_photocopied` | `constraint:photocopy-safe-color` (also right) | `constraint:photocopy-safe-color` | single **constraint_key**, 1 warn row |
| `if_hand_filled` | `constraint:field-underline-only` | `constraint:field-legibility-min` | **does not exist either** — see gap below |
| `if_professional_print` | `constraint:print-legibility-l-delta` | `constraint:professional-print` | **Set Key**, 9 T9 rows (5 fail + 4 warn) |
| (`if_projected`, ens-slides only) | `constraint:proj-body-floor` | *(deleted this pass — see below)* | n/a |

Worth stating plainly since it isn't obvious from the column's one-line schema definition:
`constraint:<name>` targets are **not restricted to single `constraint_key` rows** — the
schema's own worked example (`09-library-schema.md:552`, `if_ats_target=constraint:ats-strict`)
targets a **Set Key** covering seven rows, and this file's `if_professional_print` and
`if_ats_target` both do the same. `if_photocopied` targets one specific `constraint_key`
(`photocopy-safe-color`) that happens to share almost its whole name with its own Set Key
(`photocopy-safe`) — easy to misread as the same kind of reference; it isn't. Whoever builds
`doc_reasoning_contract.py`'s parser needs to resolve `constraint:<name>` against **both**
the `constraint_key` column and the `Set Key` column of `constraints.csv`, not just one.

## `if_hand_filled` → `field-legibility-min` — a real, currently-open T9 gap

`field-legibility-min` is used as the `if_hand_filled` action target on both
`form-handfilled` (row 7) and `ens-formulaire` (row 18). It is **PROPOSED, not authored**:
no such `constraint_key` or `Set Key` exists anywhere in `data/base/constraints.csv` (43
rows, checked in full this pass). This is not a naming slip like the guidance-table guesses
above — a form doctype being hand-fillable is a real, load-bearing fact (T3's `Field Style`
already marks these doctypes as grid/underline-field forms) that currently has **no T9 check
behind it at all**. Left wired to the proposed name rather than deleted, so
`validate-doc-conditions` will correctly flag it as unreachable until T9 gains the row — a
visible gap beats a silently dropped condition. Whoever authors the next T9 pass should add
`field-legibility-min` (working title) under a new or existing Set Key, `Applies To
doctype:*`, checking a minimum type size on `role=legal`-adjacent hand-filled field labels.

## `ens-slides` condition fix (this pass) — `26` + `29`

`research/30-notes.md` (T6 pass) flagged that `29`'s `ens-slides` row carried
`if_projected=constraint:proj-body-floor` as its *only* path to a projection-medium
constraint — and that this is exactly the pattern Revision 3's admission test deleted
everywhere else. Checked directly: the flag was correct, and the row was still carrying the
now-invalid condition. `if_projected` was removed from `DOC_CONDITION_SIGNALS` outright at
Revision 3 (`09-library-schema.md:580-581`, `26-notes.md` UPDATE 2) — leaving it in `29`
means `validate-doc-conditions` would hard-fail at build time on an unknown condition key
(by design, `09-library-schema.md:584`), not silently degrade.

The admission test (`09-library-schema.md:616-619`, *"a condition is admissible only if its
truth value is not determined by the resolved T1 row"*) applies to `ens-slides` exactly as it
applied to the original `deck-generic`: `ens-slides` is a single, fixed doctype — whether it
is projected is a constant fact the resolved T1 row already knows, not something that varies
per request. A constant is not a condition; the row that knows the answer states it directly
in `Constraint Set Keys`, the same fix already applied to `slide-deck-projection`.

**Fix applied, split across the two tables the way the rule requires:**
- `research/26-t1-doctypes-draft.csv`: `ens-slides`' `Constraint Set Keys` changed from
  `ens-house;ens-deck-density` to `ens-house;ens-deck-density;projection` — the identical
  mechanism `slide-deck-projection` already uses to reach `proj-body-floor`,
  `proj-title-floor`, the `deck-density-*`/`deck-text-density`/`deck-chart-series-max`/
  `proj-contrast-margin`/`deck-aspect-ratio-default` warn rows, and `pptx-font-embedded`
  (fail) — 1 fail + 9 warn T9 rows, all now reachable.
- `research/29-t2-doc-reasoning-draft.csv`: `ens-slides`' `Doc Conditions` cell is now blank.
  `Severity` stays `warn` — unchanged, and still describes only the shared design-language
  check in this row (per `deck-generic`'s own precedent, row 13's Reasoning), independent of
  the fail-severity T9 row now reached directly through the Set Key.

**Not closed by this fix, stated so it isn't re-discovered as a surprise later:**
`ens-manrope-inter` (ens-slides' Typeface Key) still resolves to Scale Key `ens-print`,
which is print-medium only — `ens-slides` now *reaches* the projection constraints (T9 will
check it) but still has **no authored projection-medium type-scale numbers** for those checks
to measure against. That is a T5 (`typefaces.csv`) authoring decision — either a new ENS
typeface row pointing at `research/30`'s `deck-projection` Scale Key, or brand-specific
numbers — outside this task's scope (T1/T2 drafts only). Recorded in full in
`research/30-notes.md`'s "Remaining FK / design gaps" section; this note only closes the
Doc-Conditions half of that gap, not the Typeface/Scale half.

## T1 × T9 Constraint Set Keys cross-check — why every `29` Severity is what it is

`validate-severity-map` (`09-library-schema.md:657-659`) requires every `fail`-severity
reasoning row to reach at least one `fail`-severity T9 row through its bound doctypes'
`Constraint Set Keys`. Checked every non-blank `Constraint Set Keys` cell in `26` against
`data/base/constraints.csv`'s `Set Key`/`Severity` columns (43 rows) to confirm each `29`
Severity choice is actually earned, not asserted:

| `29` `doc_category` | T1 doctypes bound | `Constraint Set Keys` used | T9 reach (fail / warn) | `29` Severity |
|---|---|---|---|---|
| `cv-ats-strict` | 8 CV rows (7 regions + generic) | `ats-strict` (+ per-region keys, none in T9 yet) | **6 fail** + 1 warn | `fail` — earned |
| `cover-letter-professional` | `cover-letter` | `ats-strict` | **6 fail** + 1 warn | `fail` — earned |
| `print-marketing` | 5 brochures + `poster` | `professional-print` | **5 fail** + 4 warn | `fail` — earned |
| `cv-academic` | `cv-academic` | *(none — T1 row carries no Constraint Set Keys)* | 0 | `warn` — no fail path exists; correctly not `fail` |
| `letter-formal` | `letter-formal` | *(none)* | 0 | `warn` |
| `memo-internal` | `memo-internal` | *(none)* | 0 | `warn` |
| `form-handfilled` | `form-handfilled` | `photocopy-safe;legal-text` | 0 fail, 3 warn | `warn` — correct; `field-legibility-min` gap above doesn't change this, it's PROPOSED not counted |
| `report-classic` | `report-short`, `report-long-toc` | `report-typography;print-legibility` | 0 fail, 8 warn | `warn` |
| `whitepaper-formal` | `whitepaper` | `report-typography;print-legibility` | 0 fail, 8 warn | `warn` |
| `proposal-narrative` | `proposal` | `report-typography` | 0 fail, 6 warn | `warn` |
| `quote-devis` | `quote-devis` | `report-typography` | 0 fail, 6 warn | `warn` |
| `one-pager-restrained` | `one-pager` | `report-typography` | 0 fail, 6 warn | `warn` |
| `invoice-tabular` | `invoice-tabular` | `report-typography` | 0 fail, 6 warn | `warn` |
| `infographic-scaffold` | *(unbuilt scaffold)* | *(none)* | 0 | `warn` |
| `deck-generic` | `slide-deck-projection` (`projection`), `slide-deck-document` (`screen`), `slide-deck-handout` (none) | mixed per-doctype | **1 fail** (via `projection`, on the projected variant only) + up to 9 warn | `warn` — correct per the rule's direction: the rule constrains `fail` rows upward, it never forces a shared `warn` row to `fail` just because one bound doctype (of three) individually reaches a fail constraint |
| `ens-office-document` | `ens-note-interne` | `ens-house` (brand, unauthored); `photocopy-safe` | 0 fail, 1 warn *(ens-house has no rows in `data/brand/ens/`, which is empty)* | `warn` |
| `ens-formulaire` | `ens-formulaire` | `ens-house` (unauthored); `photocopy-safe`; `legal-text` | 0 fail, 3 warn | `warn` |
| `ens-marketing` | `ens-social` | `ens-marketing` (brand, unauthored) | 0 (cannot confirm) | `warn` — matches this row's own Reasoning, which already says the same thing |
| `ens-slides` | `ens-slides` | `ens-house`, `ens-deck-density` (both unauthored) **+ `projection`** (this pass) | **1 fail** + 9 warn via `projection` | `warn` — same rule as `deck-generic`: reaching a fail constraint doesn't obligate `fail` here; this row's Severity still describes only the shared brand design-language check |

Same reasoning as `deck-generic`'s own note applies twice more now (`ens-slides` here,
identically): **reaching** a fail-severity T9 row through a bound doctype's Constraint Set
Keys is not the same claim as this `Reasoning` row's `Severity` column, which grades the
Style/Palette/Typeface design-language check in `29` itself. `validate-severity-map`'s rule
runs one direction only — every `fail` here must be backed by a real fail path (verified
above for all three `fail` rows), but a `warn` row is free to sit upstream of a doctype that
also, independently, reaches a `fail`-severity T9 check through its own `Constraint Set Keys`
column. No inconsistency found: all three `29` `fail` rows are backed, and no `warn` row
claims a reach it doesn't have.

**Two brand Set Keys (`ens-house`, `ens-deck-density`) and one more (`ens-marketing`) are
named on T1 rows but have zero rows anywhere in the repo** — `data/brand/ens/` is empty
except `README`/`.gitkeep` (confirmed this pass, matching `26-notes.md`'s and `29`'s own
`ens-marketing` row's prior finding). This isn't a new gap, just re-confirmed while building
the cross-check table: three ENS-scoped Set Keys are currently pure names with no T9 payload,
which is fine for now (brand rows load from `examples/ens-brand.md` via `make_brand_kit.py`,
not this base pass) but means none of `ens-note-interne`/`ens-formulaire`/`ens-social`/
`ens-slides` reach anything through their brand-scoped keys yet — only their *generic*
Set Keys (`photocopy-safe`, `legal-text`, and now `projection` on `ens-slides`) do.

**One more naming mismatch surfaced while building this table, not fixed here.** T1's
per-region CV rows carry region-specific Constraint Set Keys (`us-cv-region`,
`uk-cv-region`, `eu-generic-cv-region`, etc., alongside `ats-strict`) — but
`data/base/constraints.csv` has no Set Key by any of those names. Its actual CV-scoped rows
(`cv-page-count`, `cv-field-norms`) use one generic Set Key, `cv-region`, and reach CV
doctypes through `Applies To: doctype:cv-*` (a doctype-pattern match, a second, independent
attachment path `constraints.csv` supports alongside Set-Key membership — see rows 9-10 of
that file). So the cross-check table above counts `cv-region`'s 2 warn rows as reachable by
`doctype:cv-*` pattern, not by the per-region Set Key names T1 actually wrote — those
per-region names currently resolve to nothing, which doesn't break anything today only
because the doctype-pattern path covers the same ground. Flagging so whoever authors T1's
next revision either renames those cells to match a real Set Key or confirms the
doctype-pattern path is the intended mechanism and the region-specific names are inert by
design — not this task's table to fix.

## Not resolved here

- `field-legibility-min` gap (above) — needs a real T9 row, not this task's table.
- `ens-slides`' Typeface→Scale Key gap (above) — T5 authoring, unchanged by this pass.
- The three empty ENS brand Set Keys (above) — brand-kit authoring, not this task's table.

## B4 fix (this pass, ruled — see research/brief-ddr.md)

- **`safe-sans-deck` did not exist as a T5 row.** `deck-generic`'s `Typeface Key` named a
  typeface with no row anywhere in the library. Of the seven real typeface keys
  (`safe-sans-arial`, `safe-serif-times`, `safe-serif-georgia`, `ofl-source-sans-serif`,
  `ofl-plex-superfamily`, `ofl-public-sans`, `ofl-roboto-slab`), the choice for a deck came
  down to `safe-sans-arial` vs. `ofl-source-sans-serif`. Picked **`safe-sans-arial`**:
  `deck-generic` covers `slide-deck-projection`, `slide-deck-document`, and
  `slide-deck-handout` — i.e. decks that get opened and projected on machines the author
  doesn't control (a client's laptop, a conference room PC). A safe-stack system font
  renders correctly with zero dependency on font embedding; `ofl-source-sans-serif` is the
  better-looking, more distinctive choice but only delivers that if PPTX font embedding is
  done correctly on every machine that opens the file, which is exactly the kind of
  projection-day failure `ens-slides`' own `pptx-font-embedded` T9 check exists to catch.
  For a document class defined by "must project reliably," the guaranteed-render option
  wins over the nicer-but-conditional one. Updated `research/30-notes.md`'s cross-reference
  is unaffected — it still needs a `deck-projection` Scale Key for whichever Typeface Key
  ends up here, and `safe-sans-arial` now has somewhere real to resolve to.
