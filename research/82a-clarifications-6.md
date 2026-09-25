# research/82a-clarifications-6 -- fill engine rules (DRAFT for orchestrator ratification)

Status: **DRAFT, not ratified.** Written 2026-09-25 by the Skill Implementer after the `proposal` fill
(research/designs-evidence/proposal-fill.md) and the `cv` print-scale correction. Amends research/82
section 8 only where a rule was silent or ambiguous; corrections to a family's results are listed at the
end. Once ratified these rules are what `research/designs-evidence/fill_family.py` implements (they are
already implemented there and tested in `test_fill_family.py`, so ratifying changes wording, not code;
rejecting one means changing the named function).

Nothing here changes section 6 (ranking), section 7 (gate) or section 9 (outputs).

## R1 -- Palette: evidence strength before class name (`palette_evidence_rank`, `propose_palette`)

Section 8 orders palette candidates "provenance class authority > ranked > convention". A legacy backfill
(`research/provenance/legacy-backfill.csv`) gave several seeded palettes an `authority` row whose
`Fetch` is `search-corroborated` (cv-dach-formal, cv-europass, cv-harvard, cv-editorial); the design-system
palettes (`lib-carbon-mono`, `lib-atlassian-ink`, `lib-radix-sand`, ...) are `authority` + `fetched`.

Rule: rank = 0 authority `fetched`; 1 authority with any other Fetch; 2 ranked; 3 convention; 4 no
provenance row. Take a palette's BEST row. Then, in order: accent hue bin (8 x 45 degrees) equals the
archetype's modal accent bin (only when per-item hues exist); Foreground/Background >= 4.5:1 and, for a
one-accent archetype, accent >= 4.5:1 on Background; not an A7 blue; key alphabetical.

Effect: mono -> `lib-carbon-mono`, one-accent -> `lib-atlassian-ink`: the answers the cv fill reached
before the backfill existed, so cv and proposal use the same palettes. Without R1 the backfill silently
moves every family's answer to a CV-named palette (`cv-dach-formal`).

Palette colour class is a hue count over Primary, Secondary, Accent, Rule Brand (section 4 chromatic
thresholds). A `fill-blocks` archetype is served by any palette whose Fill-Only Roles are non-empty
(`palette_serves`); Fill-Only Roles never turn a palette into a `fill-blocks` palette by themselves
(they are non-empty on almost every library palette, which would classify all of them as fill-blocks).

## R2 -- Typeface: medium rule first; pairing fallback keeps the heading class (`propose_typeface`)

Section 8 requires the chosen row's Scale Key to have the family's medium, and says "candidates = rows
whose heading class and body class (modal variant) match". Clarified order:

1. candidates: Category Contrast (heading-body) equals (archetype heading class, modal body class);
2. order by lowest Google Fonts popularity of the Heading Family (no popularity sorts last), then
   installable/editable Embedding Licence, then key;
3. **medium rule before the tie-break**: drop a candidate whose Scale Key has no row of the family's
   medium (deck projection, infographic screen, everything else print) -- e.g. `safe-serif-georgia`
   (`report-screen`) is not a print candidate;
4. **pairing fallback**: if step 1 finds no row, keep the IDENTITY feature and relax the VARIANT one:
   candidates by heading class alone, same ordering and medium rule. (Section 4: variant features never
   split archetypes. The previous reading -- log a gap and use the family default's typeface -- makes
   different archetypes resolve to identical fills; proposal ranks 1 and 2 would have been identical.)
   The relaxation is logged in the decisions log ("rule R2").
5. if still empty: the family default's typeface, logged as a typeface gap.

The safe-stack branch (modal declared font is OS/Office-bundled -> the `safe-*` row of that class) is
unchanged; the coded tables do not carry per-item declared fonts, so it stays a human decision and safe
rows otherwise compete as ordinary candidates.

## R3 -- Gate-dropped variants read the family default (`dropped_variants`, `propose_style`)

Section 7's last sentence ("a failing variant feature is not used in filling; the family default is used")
is now mechanical: the family's `*-agreement*.md` lines "dropped from filling ... does not fail the gate:
<features>" and "... not usable for filling either" name the variants (`rules_boxes`, `density`,
`cover_page`, ...); a spec may add `dropped_variants`. For a dropped `rules/boxes` the Table Rules value is
the family default style's (the style of the family's `Family Default = y` doctype, else its first
doctype); dropped `photo` adds no photo line; dropped `body` disables the body class in R2.
Dry-run prints the dropped list and each proposal notes it.

## R4 -- New doc-style rows for a coded header placement (decision guidance, not engine-derived)

Section 8's reuse test ignores header placement (centred / ruled title block), so strict reuse silently drops
a coded IDENTITY feature and makes plain-centered archetypes identical to the plain-left default. Guidance
for the human decisions layer (`fill-specs/<family>.json`): when the only existing match lacks a Checklist
line for the archetype's header placement, author a new `<family>-<header>` row carrying that line, and log
the deviation from strict reuse. Proposal did this (`proposal-plain-centered`, `proposal-ruled`); cv did
this from the start. The engine's reuse list is printed beside the decision so a reviewer sees it.

## Corrections this triggers

- **cv** (done): three reasoning rows used `safe-serif-georgia` (medium screen) for print CVs; R2 step 3
  yields `safe-serif-times`. Corrected 2026-09-25 (cv-fill.md, "corrected 2026-09-25: print scale");
  `research/library/doc-reasoning/cv.csv` three `Typeface Key` cells; nothing else changed.
- **proposal**: already follows R1-R3 and R4 (proposal-fill.md); no change.
- Families not yet filled apply R1-R4 from the start; `--dry-run` shows each rule's outcome.

## Open points for the orchestrator

1. R1 treats `search-corroborated` as weaker than `fetched` for palette provenance only. The same
   distinction may matter for typeface and doc-style provenance; not needed so far.
2. R2 step 4 could instead be limited to sans/serif classes; today it applies to any class mismatch.
3. Per-item declared fonts (the safe-stack branch) and per-item accent hexes (the hue-bin tie-break) are
   still not coded; adding two columns to the coded tables would make both branches evaluable.
