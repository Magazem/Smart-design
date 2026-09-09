# T3 doc-styles draft — notes (research/31-t3-doc-styles-draft.csv)

12 rows, `csv.reader`-clean, 15 columns matching the manifest's `doc-styles` header
exactly (`style_key,Display Name,Keywords,Best For,Not For,Brand Scope,Rule Hair pt,
Rule Strong pt,Rule Brand pt,Corner Radius mm,Table Rules,Table Fills,Emphasis Mechanism,
Field Style,Checklist`). Verified by script against `research/29-t2-doc-reasoning-draft.csv`:
the 12 `style_key` values here are the exact set of 12 unique non-blank `Style Key` values
T2 references — zero missing, zero extra. `Checklist` is the manifest's one list column
(`;`-delimited); every field containing a literal comma is quoted, `csv.reader`-checked.
All four enum columns (`Table Rules`, `Table Fills`, `Emphasis Mechanism`, `Field Style`)
checked against `schema-manifest.json`'s closed value lists — zero violations.

## Sourced rows (3) — the schema's and brand doc's own worked examples, not re-derived

- **`cv-restrained`** and **`report-classic-serif`** are literally the "Example (generic)"
  values `09-library-schema.md` gives for T2's `Style Key` (line 559) and T3's own
  `style_key` (line 685) respectively — the schema names them, not me. `report-classic-serif`
  additionally reuses that section's given `Corner Radius mm` (`0`/`0`, line 683),
  `Emphasis Mechanism` (`weight`/`weight`, line 686), and `Field Style` (`underline`/`none`,
  line 687) example values verbatim, and its `Checklist` opens with the doc's own partial
  example ("headings H1–H3 only;figure captions below;…", line 688) extended to a full list.
- **`ens-document-grid`** copies `ENS-plugin-rebuild-v2.md`'s explicit design-system-variable
  block (line 73: `--radius: 0; --rule-hair: 0.5pt; --rule-strong: 1pt; --rule-brand: 1.6pt`)
  and its implementation checklist (line 74) near-verbatim — this is the same worked example
  `09-library-schema.md:441-444` and `29-t2-doc-reasoning-draft.csv`'s `ens-office-document`/
  `ens-formulaire`/`ens-slides` rows all cite, so the T3 row is sourced from the one place
  the numbers already live, not re-invented.

## Generic-family rows (7) inherit the schema's own generic Rule Weights convention

`09-library-schema.md:682` gives the generic `Rule Weights` example as `hair=0.5pt;strong=1pt`
— no third (brand) value, because a brand-less style has no brand-accent rule. Applied
literally as `Rule Hair pt=0.5, Rule Strong pt=1, Rule Brand pt=0` to every generic row for
which no source text asks for a different visual weight: `cv-restrained`, `cv-academic-plain`,
`letter-restrained`, `letter-formal-grid`, `memo-plain`, `form-grid-underline`,
`one-pager-tight`. All seven also get `Corner Radius mm=0`, matching every given example in
the schema (T3's own ENS/generic examples are both `0`) and the repeated house rule that a
restrained/photocopy-safe grammar has no rounded elements.

`memo-plain` is the deliberate generic analogue of `ens-document-grid`'s
`ens-note-interne`/`ens-office-document` pairing — T2's own note on the `memo-internal` row
("shares Style/Palette/Typeface intent with letter-formal; this is also the schema's own
worked brand two-pass example doc_category") is why `memo-plain` and `letter-formal-grid`
get near-identical rows here, differentiated only by `Checklist` (header block with
to/from/date/subject vs. a letterhead block).

## Two rows deliberately break the generic 0.5/1/0 convention

- **`marketing-print-bold`**: `Rule Hair pt=0, Rule Strong pt=1.5, Rule Brand pt=2.5`,
  `Emphasis Mechanism=fill` (not `weight`). T2's bias terms for `print-marketing` ("bold
  hierarchy, generous white space, fold-aware layout") and its anti-patterns
  (`low-contrast-text;gradient-banding;stock-photo-cliche`) describe a poster/brochure
  grammar built from bold filled colour blocks and CTA bars, not fine document hairlines —
  the opposite visual register from the CV/letter/report family. Heavier rule weights and
  fill-based emphasis are a reasoned deviation, not an oversight; every other generic row
  keeps the schema's literal 0.5/1/0 convention specifically because nothing asks it to move.
- **`deck-bold-minimal`**: `Rule Hair pt=0` (slides don't carry document hairlines at all;
  dividers, where used, are the one `Rule Strong pt=1`). Kept `Emphasis Mechanism=weight`
  rather than `fill` — T2's bias terms describe *high contrast between text and background*,
  which is a colour-pair property of the whole slide, not a per-word emphasis mechanism; the
  "6x6 heuristic" register still reads as bold-weight callouts on a plain field, closer to
  the CV/report family's mechanism than to marketing's filled badges.

## Real authoring tension, flagged not silently resolved: `form-grid-underline`'s `Table Rules`

This one `style_key` is shared by three T2 `doc_category` rows with textually different
`Style Bias Terms`: `form-handfilled` says "**hairline** rules", `invoice-tabular` says
"header-and-total **table rules**" explicitly by name, `quote-devis` says only "tabular,
line-item grid" (silent on which). Shipped `Table Rules=header-and-total` here, on two
grounds: (1) it is the literal enum value `invoice-tabular`'s own bias terms name, and two of
the three sharing categories (`quote-devis`, `invoice-tabular`) are financial line-item
tables where a total row is the entire reason the pattern exists; (2) `form-handfilled`'s own
"hairline" language is already satisfied by this row's `Rule Hair pt=0.5` (the rule *weight*)
and `Field Style=underline` (how its fields render) — `Table Rules` only activates when the
document actually contains a multi-row table, which is closer to universal for the two
invoice/quote categories than for a hand-filled fiche. Recorded as a real, inherited tension
(not introduced here — it was already latent across three T2 rows pointing at one T3 key),
not as something this pass invented or silently papered over. If a future pass wants both
patterns to render exactly as each category's own bias terms describe, the fix is a second
`style_key` (e.g. `invoice-grid-total`) splitting `invoice-tabular`/`quote-devis` off from
`form-handfilled` — out of scope here (T3 authoring only, keys fixed by what T2 already
references).

## Flagged gap, not fixed: `ens-social-bold`'s rule weights and corner radius are inferred, not sourced

Unlike `ens-document-grid`, `ENS-plugin-rebuild-v2.md` gives **no `--rule-*` design-system-
variable block for the marketing/social treatment** (lines 149–152 describe layout: full-
bleed background, lime kicker pill, photo card, fact tiles, CTA bar — no rule-weight numbers
at all). Two values in this row are therefore inference, not citation, and should be
confirmed by whoever owns the ENS brand kit before this ships:

- **`Corner Radius mm=5`** is a unit conversion, not a sourced constant. The brand doc states
  "**20 px**-radius card" (line 150) for the one rounded element ENS marketing allows; T3's
  column is `mm`, a print-physical unit, applied here to a screen/social asset
  (`research/26-t1-doctypes-draft.csv`'s `ens-social` row resolves to page format
  `px-ens-social-1080` — a 1080 px canvas, confirming this is pixel-native, not print). `20px
  ≈ 5.3mm` only holds at a specific, unstated reference density (96 dpi); at social-media
  export resolutions the same visual proportion is a different mm figure. Rounded to `5` as a
  placeholder that preserves the *relationship* ("small, one rounded element") rather than
  claiming px-accuracy the schema's unit can't carry. This is the same category of problem
  T6's notes already flagged for `deck-projection`/`ens-print` — a schema column authored for
  one medium (print, mm) reused for a row that lives in a different medium (screen, px) with
  no native column for it.
- **`Rule Hair pt=0, Rule Strong pt=1.5, Rule Brand pt=0`**: `Rule Strong pt=1.5` borrows the
  "1.5 px white 28% border" figure the brand doc gives for the fact-tile border (line 152) as
  the closest thing to a sourced rule weight in this section — a genuine stretch, since that
  line describes a tile border, not a structural document rule the way `ens-document-grid`'s
  `--rule-strong` does. `Rule Brand pt=0` because no accent-colour rule line exists anywhere
  in the marketing section (colour there is carried by fills — the lime kicker pill, the
  green full-bleed background — not by a rule stroke). Recommend the brand-kit owner supply
  or confirm real numbers here rather than treating these two values as settled.

## `Emphasis Mechanism=weight` on both ENS rows, not `fill`, despite fill-heavy layouts

`ens-social-bold`'s layout is fill-driven (lime badge fill, tile fills, full-bleed background
fill) but `Emphasis Mechanism` tracks how *text within body content* is emphasised, not the
general layout grammar — and the brand doc is explicit and narrow on that exact point: "Body
Inter 23–27 px white; **emphasis = bold white, not lime text**" (v2 line 151), directly
echoing the same house rule already cited for `ens-document-grid` ("Emphasis = bold … never
background", v2 line 136, `09-library-schema.md:696-699`). Both ENS rows therefore ship
`weight`, matching the brand's own explicit contrast between how text is emphasised (bold)
and how layout blocks carry meaning (fill) — a distinction the schema's single-purpose
`Emphasis Mechanism` column exists to make checkable.

## What this closes and what it doesn't

Closes: T3 is no longer wholly unauthored (12 of the ~20–30 the schema's own size estimate,
`09-library-schema.md:2119`, projects for this table) — specifically, every `Style Key` T2
currently resolves to now has somewhere to resolve. Does not close: T2's own remaining gaps
(`infographic-scaffold`'s blank Style/Palette/Typeface Key, `safe-sans-deck`'s still-PROPOSED
Typeface Key, `ens-marketing`'s unconfirmed fail-reachability) are untouched — this pass adds
no new T2 rows and resolves no T2 gap, it only authors the T3 payload for keys T2 already
names. T4 palettes (the other half of Step 6, ~10 generic keys) is not started here.

## Tidy (Step 6b pass): `Checklist` phrasing is mixed on purpose, not sloppily

Two rows quote a source verbatim and stay exactly as shipped above:
`report-classic-serif`'s `Checklist` opens with `09-library-schema.md:688`'s own partial
example extended to a full list (see "Sourced rows" above), and `ens-document-grid`'s copies
`ENS-plugin-rebuild-v2.md:74`'s implementation checklist near-verbatim. Both are noun-phrase
style ("headings H1-H3 only", "one green rule under title") because that is the source
text's own register — changing it to imperative would break the verbatim-quote guarantee
these two rows exist to give.

Every other row uses imperative phrasing ("Keep single column only", "Remove colour-coded
sections") — that was the intended house style throughout, but three rows shipped in the
original 12 with the same noun-phrase register as the two verbatim rows even though nothing
sources them to a specific wording: `deck-bold-minimal`, `one-pager-tight`, `ens-social-bold`.
Normalised those three to imperative form in this pass (no content change, phrasing only) so
the mixed register in the shipped file now signals something real — verbatim-quoted vs.
freely authored — instead of being an accidental inconsistency.
