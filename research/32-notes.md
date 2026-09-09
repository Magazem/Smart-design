# T4 palettes draft — notes (research/32-t4-palettes-draft.csv)

5 rows, `csv.reader`-clean, 20 columns matching the manifest's `palettes` header exactly
(`palette_key,Display Name,Keywords,Brand Scope,Primary,On Primary,Secondary,On Secondary,
Accent,On Accent,Background,Foreground,Muted,On Muted,Rule Hair,Rule Strong,Rule Brand,
Text-Safe Roles,Fill-Only Roles,Category Marker Roles`). Verified by script against
`research/29-t2-doc-reasoning-draft.csv`: the 5 `palette_key` values here are the exact set
of 5 unique non-blank `Palette Key` values T2 references — zero missing, zero extra
(`infographic-scaffold`'s blank Palette Key is T2's own known gap, untouched here, same
disposition T3's notes gave the matching blank `Style Key`). The three list columns
(`Text-Safe Roles`, `Fill-Only Roles`, `Category Marker Roles`) use the manifest's `;`
delimiter; every field containing a literal comma is quoted, `csv.reader`-checked.

## Contrast verified by computation, not asserted

`09-library-schema.md`'s T4 section commits every `On X` pair to WCAG relative-luminance
4.5:1 and names the exact five derived checks (`schema-manifest.json`'s `derived` list):
`On Primary`×`Primary`, `On Secondary`×`Secondary`, `On Accent`×`Accent`, `Foreground`×
`Background`, `On Muted`×`Muted`. Ran all 25 pairs across the 5 rows through the repo's own
`skill/document-design-intelligence/scripts/lib/color.py` (`contrast_ratio`), not an eyeball
or an invented threshold — that module is itself a verbatim port of upstream
`ui-ux-pro-max`'s `validate_data.py` formula, so this is the exact function the real gate
will run. Sanity-checked it first against ENS's own stated ratios in
`ENS-plugin-rebuild-v2.md` (Primary/On Primary "6.4:1", script gives 6.15; Secondary/On
Secondary "5.6:1", script gives 5.58 — same formula, small rounding difference in the source
doc, method confirmed) before trusting it on new colours. All 25 pairs clear 4.5:1; lowest
margin is `print-neutral`'s `On Muted`×`Muted` at 5.62:1 (`#55606B` on `#EEF0F2`); full table:

| Row | On Primary/Primary | On Secondary/Secondary | On Accent/Accent | Foreground/Background | On Muted/Muted |
|---|---|---|---|---|---|
| mono-ink | 17.40:1 | 8.86:1 | — | 18.88:1 | 6.66:1 |
| brand-accent-print | 17.40:1 | 8.86:1 | 5.67:1 | 17.40:1 | 6.66:1 |
| print-neutral | 14.88:1 | 6.42:1 | 7.07:1 | 16.76:1 | 5.62:1 |
| deck-high-contrast | 18.73:1 | 13.27:1 | 13.09:1 | 19.17:1 | 10.17:1 |
| ens-core | 6.15:1 | 5.58:1 | 7.91:1 | 13.97:1 | 4.74:1 |

## Sourced rows (2) — the schema's and brand doc's own worked examples, not designed

- **`mono-ink`** is literally the "Example (generic)" column `09-library-schema.md:734-748`
  gives for T4 — same status T3's notes gave `cv-restrained`/`report-classic-serif`: the
  schema names these values, not me. `Accent`/`On Accent` and `Category Marker Roles` ship
  blank because the schema's own generic example shows `—` for both (monochrome has no brand
  colour to mark categories with).
- **`ens-core`** copies the same section's "Example (ENS)" column verbatim, cross-checked
  against `ENS-plugin-rebuild-v2.md` lines 35–44 and 66–74 hex-for-hex (`#1F6F43`/`#8B5E3C`/
  `#9ACD32`/`#F7F8F5`/`#1E2A23`/`#DCE8DF`/`#5B665F`/`#B9C4BC` all match the source doc
  exactly) — the same worked example `09-library-schema.md:441-444`,
  `29-t2-doc-reasoning-draft.csv`'s `ens-office-document` row, and `31-t3-doc-styles-draft.csv`'s
  `ens-document-grid` row all already cite. `Text-Safe Roles`/`Fill-Only Roles`/`Category
  Marker Roles` are the schema's own example values (line 746–748), not re-derived.

## Designed rows (3) — no source text gives hex values, so these are new authoring

T2 supplies only prose `Palette Bias Terms` for these three (`"brand accent, high contrast
for print"`, `"neutral ink, restrained accent"`, `"near-maximum contrast pairs, no mid-gray-
on-dark under projector washout"`) — no upstream file or brand doc gives real hex for a
generic marketing/report/deck palette, so these are authored, every value checked against
the same 4.5:1 floor above, not copied from anywhere. Flagged here as a real gap the way
T3's notes flagged `ens-social-bold`'s two inferred numbers, not silently presented as sourced.

- **`print-neutral`** (report-classic, whitepaper-formal, proposal-narrative, quote-devis,
  one-pager-restrained, invoice-tabular — 6 of T2's 19 doc_categories, the single most-shared
  Palette Key in the table): near-black-blue ink (`#22282E`/`#1A1E22`) rather than `mono-ink`'s
  pure grey, plus one desaturated slate-blue `Accent` (`#2E5C82`) for the "restrained accent"
  T2's bias terms name — restrained meaning *one* muted colour, used sparingly (a rule, a
  pull-quote), not *no* colour the way `mono-ink` is. `Accent` ships in `Text-Safe Roles`
  (7.07:1 against `Background`) rather than `Fill-Only`, since nothing in T2's bias terms or
  T3's `report-classic-serif`/`Emphasis Mechanism=weight` row asks for filled colour blocks —
  a restrained report accent reads as coloured heading text, not a badge.
- **`brand-accent-print`** (print-marketing only, T3's `marketing-print-bold` companion row):
  reuses `mono-ink`'s ink/secondary pair for body text (nothing in T2's bias terms asks for a
  different body ink) and adds one bold accent (`#C81E3A`) matching T3's own
  `Emphasis Mechanism=fill` ruling for this row (`31-notes.md`'s marketing-print-bold
  paragraph: "bold hierarchy... filled colour blocks, not hairline rules") — `Accent` ships in
  `Fill-Only Roles`, not `Text-Safe`, specifically because the T3 row this palette pairs with
  already decided emphasis here is a filled block, not coloured text, even though the accent
  passes the text contrast floor on its own (5.67:1). `Category Marker Roles=accent` for the
  same reason `ens-core` marks categories with its one brand colour.
- **`deck-high-contrast`** (deck-generic only): the one row that reverses the light-background
  convention every other palette here uses — dark `Background` (`#0F0F0F`) with near-white
  `Foreground`/`Primary` (19.17:1), on the reasoning that T2's own bias term text
  ("near-maximum contrast pairs, no mid-gray-on-dark under projector washout") is explicitly
  warning against a *specific* failure mode — a dark deck background with mid-grey text or
  panels, which loses contrast under a projector's limited black level — not against dark
  backgrounds generally. Every non-background/foreground colour here is chosen to stay off the
  mid-grey band the warning names: `Secondary`/`Muted` are `#D9D9D9`/`#2A2A2A`, both far from
  `#808080` mid-grey, not a softened version of it. One bright accent (`#FFD400`) for a single
  highlighted word/callout per slide, kept in `Text-Safe Roles` because T3's `deck-bold-minimal`
  row ships `Emphasis Mechanism=weight`, not `fill` (`31-notes.md`'s explicit reasoning: decks
  read closer to the CV/report family's bold-weight-callout mechanism than to marketing's
  filled badges) — the opposite call from `brand-accent-print`'s accent, made for the mirror
  reason. `Rule Brand` ships blank: `deck-bold-minimal`'s own `Rule Brand pt=0` (T3) says a
  generic deck has no brand-accent rule to give a colour to.

## Flagged, not fixed: `print-neutral`'s `Primary` sits just above the T4 `L*` ceiling

`09-library-schema.md`'s `validate-text-safe-color` design note (line 780–786) sets
`l_star_max=15` as an *absolute* lightness ceiling for the smallest text roles on
photocopy-safe doctypes — the check that made `12-typescale-and-fstype.md`'s mid-L* ENS-green
finding (`#1F6F43` at L*≈41 photocopies to grey) a real constraint. I computed CIE L* for
every dark ink in this draft as a precaution: `print-neutral`'s `Primary` (`#22282E`) comes out
at **L*≈15.8**, a hair above the ceiling; its `Foreground` (`#1A1E22`, the role that actually
carries body text) is L*≈11.0, comfortably under. This is not a violation today —
`print-neutral` is never reached by an `if_photocopied` condition anywhere in
`29-t2-doc-reasoning-draft.csv` (only `mono-ink` and `ens-core` are, both well under the
ceiling: `#111111`≈L*5.1, `#1E2A23`≈L*15.8 — note `ens-core`'s own `Foreground` sits at the
identical borderline value and ships anyway, since it is the schema's cited worked example,
not mine to adjust). Recorded so a future pass that reuses `print-neutral` on a
photocopy-safe doctype checks this first rather than rediscovering it.

## What this closes and what it doesn't

Closes: T4 is no longer wholly unauthored — every `Palette Key` T2 currently resolves to now
has somewhere to resolve, completing Step 6 alongside `research/31` (T3). Does not close: T2's
own remaining gaps (`infographic-scaffold`'s blank Style/Palette/Typeface Key, `ens-marketing`'s
unconfirmed fail-reachability) are untouched — this pass authors no new T2 rows and resolves no
T2 gap. `On Primary`/`On Secondary`/etc. contrast is checked here by hand against the schema's
stated formula, not run through `validate_data.py` — the gate script should still be run to
confirm before this leaves draft status, per this table's own `validate-contrast-print` /
`validate-contrast-screen` validators. T10 `structures.csv` (the schema's own "least confident
table," per `RESUME.md`'s critical path) remains the one wholly unauthored table.
