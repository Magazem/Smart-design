# 59 — Infographic content authored (task 01a0903d)

Author: Document Design Researcher. Drafts edited, then loaded with `research/load-base.py`
(the only script permitted to write `data/base/`). No `data/base/*.csv` hand-edited. No git.

## 1. The five items

**1. Structure.** New `structures.csv` row `infographic-canvas` in
`research/36-t10-structures-draft.csv`: Section Order `headline;key-points;call-to-action`,
Heading Language `en`, Heading Depth Max `1`, TOC Depth `0`, Front Matter Numbering `none`,
Caption Position `fig=below;table=above`, Cross-Ref Style `numbered` — every field copied from
the existing single-canvas/minimal-marketing rows (`poster-single-canvas`, `flyer-single-sheet`),
CONVENTION (this project's own established pattern for a canvas structure row, not an external
source).

**2. Headings.** Zero new heading rows. `headline`, `key-points` and `call-to-action` already
carry en/fr/de rows (`headline-{en,fr,de}-1`, `key-points-{en,fr,de}-1`,
`call-to-action-{en,fr,de}-1`), grep-verified before the Section Order was written.

**3. Type scale.** New `scale_key` `infographic-screen` in `research/30-t6-type-scales-draft.csv`,
Medium `screen`, 4 rows: `lead` 108pt/1.05, `h1` 44pt/1.15, `body` 24pt/1.35, `caption` 14pt/1.20.
CONVENTION, not sourced — Bringhurst is cited in this library for print measure/leading only, per
the standing sourcing rule, and covers neither screen sizing nor a stat-callout numeral. Detailed
reasoning in section 3.

**4. Palette + typeface.** `doc-reasoning.csv` `infographic-scaffold` (edited in
`research/29-t2-doc-reasoning-draft.csv`): Palette Key `brand-accent-print` (REUSED), Typeface Key
`safe-sans-infographic` (NEW row in `research/19-t5-typefaces-draft.csv`, Arial/Arial, Scale Key
`infographic-screen`), Style Key `infographic-bold` (NEW row in
`research/31-t3-doc-styles-draft.csv`). Reuse/new rationale in section 2.

**5. Constraint Set Keys + Region Key.** `doctypes.csv` `infographic` (edited in
`research/26-t1-doctypes-draft.csv`): Constraint Set Keys `screen` — grep-verified against
`constraints.csv`, the same token `slide-deck-document` already uses; pulls in
`screen-body-floor` (`artifact-class:canvas`, `medium=screen;role=body`, threshold 18pt), which
the new body role (24pt) clears with margin. Region Key stays EMPTY, stated reason: every
`constraints.csv` row scoped to `cv-region` is `Applies To: doctype:cv-*`, and region overlays are
a CV-only mechanism throughout the schema (T12 cv-regions); an infographic has no regional
variant to select. Structure Key `infographic-canvas` (item 1).

## 2. What was reused, and why it's honest

- **Palette `brand-accent-print`**: the only T4 row carrying a populated Category Marker Roles
  token and a CTA-framed accent (`#C81E3A`), already the palette behind `print-marketing`
  (poster, brochures). Its On-X pairs are already gate-checked ≥4.5:1 project-wide (research/32).
  Reusing it does not borrow a print-only claim — nothing in the palette row is print-specific;
  the print/screen split lives in Render Target and Constraint Set Keys, not the palette.
- **Sections `headline`/`key-points`/`call-to-action`**: all three already exist in en/fr/de and
  already serve `poster-single-canvas`, `flyer-single-sheet` and `one-pager-standard`. No new
  canonical section authored — matches the project's established reuse discipline (phase A/B: an
  identical or overlapping Section Order is fine when the discriminating work happens in
  page-formats/doc-styles/type-scales, which it does here).
- **NOT reused: typeface/scale.** The nearest existing screen scale is `deck-projection`
  (carried by `safe-sans-deck`): h1 36 / body 24 / body-dense 18. It has no role for an
  infographic's defining element — an oversized stat number — so pointing `infographic-scaffold`
  at `safe-sans-deck` would have shipped a typeface with nothing to carry the thing that makes an
  infographic an infographic. New typeface row `safe-sans-infographic` follows the exact existing
  `safe-sans-arial`/`safe-sans-deck` precedent: same family (Arial/Arial), differs only in Scale
  Key. This is the library's own pattern for "same safe stack, different medium scale," not an
  invented shape.
- **NOT reused: doc-style.** `marketing-print-bold` (poster/brochure) is the nearest T3 row, but
  its Checklist hard-codes `Design the layout fold-aware for tri-fold or bi-fold` — wrong
  guidance reaching the renderer for a single, unfolded canvas, which is exactly the class of
  defect the v0.3 standing rule targets. `infographic-bold` keeps every numeric field identical
  (Rule Hair/Strong/Brand, Corner Radius, Table Rules/Fills, Emphasis Mechanism, Field Style — the
  same bold-fill family) and replaces only the Checklist, with items tied directly to this
  doctype's own already-shipped Anti-Pattern Tokens (`gradient;3d-chart`).

## 3. Why these sizes for a 1080×1350 screen canvas

`px-infographic-portrait` is already in the library at 285.75×357.19mm — confirmed to be exactly
1080×1350px at 96dpi (the render target's own `--window-size=1080,1350` flag; verified against the
handoff output below). This is read at thumbnail/feed scale, not at arm's-length reading distance,
which is the opposite of every other `screen`-medium row in this table (`report-screen-screen-body`
at 11pt assumes a reader with a full page open, not a scrolling glance).

The one anchor this project already has for screen-medium body text is `constraints.csv`'s
`screen-body-floor` (`medium=screen;role=body`, threshold 18pt, applies to any canvas-class
doctype naming `screen`). I did not sit the scale on that floor — 18pt sat at the edge of a
warn-only rule feels like tuning to the check, the same trap the project has refused before
("refusing the green tick," research/notes 2026-09-09). `body` is set to 24pt, matching
`deck-projection`'s body size (a scale already accepted for screen/projection legibility in this
library) with headroom above the floor rather than sitting on it.

`h1` (44pt) sits above `deck-projection`'s 36pt: a deck headline is seen for seconds on a large
projected surface, an infographic headline has to read at a glance in a scrolling feed on a small
device, which argues for larger, not smaller.

`lead` (108pt) is the infographic's signature element — the oversized stat number ("73%"). No
scale in this library carries anything like it; the closest kin is `ens-print-print-lead` at
12pt, which is a brand print row for a standout paragraph, not a display numeral. `lead` is
authored at roughly 2.5× `h1`, the standard "hero number dominates the headline" relationship in
infographic layout — CONVENTION, not sourced; no source in this library's citation set (Bringhurst,
Butterick, DIN 5008) speaks to display-numeral sizing.

`caption` (14pt) is the source/citation line — larger than the print `caption` roles (8.5–9pt)
because there is no print-DPI packing pressure on a screen canvas, but still clearly the smallest
role in the scale.

All four are tagged CONVENTION in the `doc-reasoning` Reasoning column (research/29), not
attributed to a source that doesn't cover them.

## 4. Before / after handoff output, in full

Before (data/base pre-load, i.e. the shipped state this brief was opened against):

```
HANDOFF (format=png)
  canvas (CSS px -- parsed from the render target's own Engine Invocation --window-size flag; a screenshot has no @page):
    headless-chromium: 1080px x 1350px
  font-face (CSS idiom, embed vs. safe-stack per render target's Font Rule):
    (not present in this resolution)
  font sizes (CSS px -- 1pt = 96/72px; the canvas above is already px-native, so px is the right unit here, not pt):
    (not present in this resolution)
  sections:
    (not present in this resolution)
  palette (CSS hex colour, '#' kept):
    (not present in this resolution)
  paged media (bleed / crop marks / @page): NOT APPLICABLE -- png-social's Supports Paged Media is n/a and Print Tier Max is none; a screenshot has no pages
  render command:
    headless-chromium: /opt/google/chrome/chrome --headless --no-sandbox --disable-gpu --screenshot=%o --window-size=1080,1350 %i
  constraints to preflight: (none found)
next: python3 scripts/preflight.py <rendered-file>.png
```

After (post `research/load-base.py`, gate zero):

```
HANDOFF (format=png)
  canvas (CSS px -- parsed from the render target's own Engine Invocation --window-size flag; a screenshot has no @page):
    headless-chromium: 1080px x 1350px
  font-face (CSS idiom, embed vs. safe-stack per render target's Font Rule):
    headless-chromium (embed): Arial / Arial
  font sizes (CSS px -- 1pt = 96/72px; the canvas above is already px-native, so px is the right unit here, not pt):
    lead: 108pt  ->  144.0px
    h1: 44pt  ->  58.7px
    body: 24pt  ->  32.0px
    caption: 14pt  ->  18.7px
  sections (Section Order, wording in Heading Language=en):
    headline: Headline
    key-points: Key Points
    call-to-action: Call to Action
  palette (CSS hex colour, '#' kept):
    Primary: #1A1A1A
    Secondary: #4A4A4A
    Accent: #C81E3A
    Background: #FFFFFF
    Foreground: #1A1A1A
  paged media (bleed / crop marks / @page): NOT APPLICABLE -- png-social's Supports Paged Media is n/a and Print Tier Max is none; a screenshot has no pages
  render command:
    headless-chromium: /opt/google/chrome/chrome --headless --no-sandbox --disable-gpu --screenshot=%o --window-size=1080,1350 %i
  constraints to preflight (Set Keys): screen
next: python3 scripts/preflight.py <rendered-file>.png
```

**Zero `(not present in this resolution)` lines after.** font-face, font sizes, sections and
palette all print real values. Acceptance bar met.

## 5. Gate and pytest

`validate_data.py data/base`: **`OK: validated 14 table(s), 432 row(s)`** (was 414 before this
load; +18 rows: 4 type-scales, 1 typeface, 1 doc-style, 1 structure, plus the loader's own
`Safe Stack Availability` derivation touching the existing typefaces file, and the previously-empty
`doctypes`/`doc-reasoning` cells filled in place, not counted as new rows).

`pytest -q`: **NOT fully green — 5 failed, 168 passed, 68 subtests passed.** Reported honestly
per the brief's own "a green gate is not the proof" instruction; not worked around.

1. **4 subtest failures**, all in one test:
   `test_ddi.py::TestPngHandoffBuilder::test_infographic_empty_reasoning_columns_degrade_to_not_present_not_omission`.
   This test's own docstring states its purpose: prove the handoff builder prints a header with
   `NOT_PRESENT` values rather than silently omitting the section, when the underlying columns are
   empty — a regression test for the degradation MECHANISM. It used the real `infographic` doctype
   as its fixture because that was, at the time, the one real doctype guaranteed to be empty. That
   coupling is now stale: `infographic` is no longer empty, so the fixture no longer exercises what
   the test claims to test. **This is not a defect in the data authored here** — the mechanism the
   test protects is untouched and still correct (see section 4's before-state, captured live moments
   before the load). The test needs a synthetic empty fixture, not a real doctype it can no longer
   assume stays empty. That is `ddi.py`/test-suite territory, not a data-authoring fix, and I have
   not touched it.

2. **1 test failure**: `test_description_coverage.py::DescriptionCoverageTest::test_every_structured_doctype_is_reachable`
   — `AssertionError: Lists differ: ['infographic'] != []`. Now that `infographic` has a
   Structure Key, the coverage test correctly flags that no keyword or display-name noun of
   `infographic` (checked: "infographic", "data visual", "visual summary", "statistics graphic",
   "infographie", "visuel de données", "infografik") appears anywhere in SKILL.md's description.
   Confirmed by reading the shipped description directly — genuinely absent, not a false positive.
   **This is a real, new-found gap, not something authored here to paper over.** I have not edited
   SKILL.md (the user vetoes description changes; "DESCRIPTION ITERATION IS CLOSED" per RESUME.md)
   and have not added `infographic` to the test's `GENERIC_COVERED` map either, since that map
   exists for doctypes genuinely reachable through an *already-present* broader noun — I checked
   and none of the description's existing nouns (poster, brochure, flyer, etc.) plausibly cover
   "infographic," so declaring it there would suppress a true finding rather than resolve it. Flagged
   to the lead for routing rather than decided unilaterally.

## 6. What could not be sourced

The four `infographic-screen` type-scale sizes (108/44/24/14pt) and the `lead` role's 2.5× ratio
to `h1` are CONVENTION — no source in this project's citation set (Bringhurst, Butterick, DIN 5008)
covers screen-thumbnail or stat-numeral sizing, and this is said plainly in `doc-reasoning`'s
Reasoning column rather than attributed to one of those names.
