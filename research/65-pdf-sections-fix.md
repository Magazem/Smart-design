# 65 — pdf handoff sections fix

Ruled 2026-09-11 (`research/brief-packaging-pdf-sections.md`). SHIP-BLOCKER: `_build_pdf_lines`
never called `_sections_lines`, so the pdf handoff had no `sections` block at all — not empty,
absent. 9 of 30 doctypes have a pdf render target and no docx/pptx target, so for those families
the release's headline P0 (heading wording reaching the output) was entirely unfixed.

## The fix

One line in `scripts/ddi.py`'s `_build_pdf_lines`, added in the same relative position the
docx/pptx/png builders already use it — after `heading elements` (pdf's TOC-heading-levels
equivalent), before `palette`:

```python
    lines.extend(_sections_lines(resolved))
```

No other change to `_build_pdf_lines`. `_sections_lines` was already correct and already used by
three of the four format builders (`ddi.py:513` docx, `:576` pptx, `:766` png) — this was purely a
missing call, not a logic gap.

## Page flow — investigated, NOT fixed, reporting per the brief's stop condition

The gate also filed D-J: pdf silently omits page flow where constraints had resolved. Checked
whether this is the same one-line omission. It is not, and per the brief ("if it is anything more
than that, STOP and report it") I left it alone.

Why it's not one line: docx's `_page_flow_docx_lines` and pptx's `_page_flow_pptx_lines` both read
`_page_flow_constraints()`, which finds resolved constraint rows carrying a `docx_property` key in
their `Parameter` column (`data/base/constraints.csv` rows 28-32: `keepNext` x2, `widowControl`,
`cantSplit`, `tblHeader` — five rows, matching the brief's count). docx prints these as OOXML
paragraph/table properties directly; pptx prints "NOT APPLICABLE" because slides don't paginate.

pdf's pipeline is native HTML → Chromium/WeasyPrint, not OOXML, and unlike pptx it **does**
paginate — so "NOT APPLICABLE" would be dishonest here. A correct pdf page-flow block needs each
`docx_property` mapped to its CSS/print equivalent (e.g. `keepNext` → `break-after: avoid`,
`cantSplit` → `break-inside: avoid`, `widowControl` → `widows`/`orphans`, `tblHeader` → CSS's
repeating-table-header mechanics, which differ across the three declared pdf engines
Chromium/WeasyPrint/wkhtmltopdf). No such mapping exists anywhere in this codebase today
(checked: no `css_property`/`pdf_property` column, no `break-inside`/`break-after` string anywhere
in `skill/document-design-intelligence`). Building it means authoring and sourcing a new
docx-property → CSS-property table, the same shape of work as the original `_page_flow_docx_lines`
build — a real feature, not a missed call site. Reporting it to the lead as a follow-up rather than
growing this task.

## The test — `scripts/tests/test_ddi.py`

Added `test_quote_devis_pdf_gets_a_sections_block` to `TestPdfHandoffCarriesTypeScaleAndPalette`
(the existing class covering pdf's other missing-block gap). Runs the real
`resolve --doctype quote-devis` → `handoff --format pdf` pipeline (`quote-devis`'s only render
target is `pdf-chromium`, `Structure Key` = `invoice-standard`), asserts the `sections` header is
present via `_section_values` (which fails outright if the header itself is missing — so a
still-absent block is caught before any content check runs), that at least one value is not
`ddi.NOT_PRESENT`, and asserts the real rendered wording `issuer: From` is present **within the
`sections` block's own values** (`assertIn("issuer: From", values)`, not a whole-`stdout` scan) —
not a check for the literal string `"sections"`.

**Confirmed failing before the fix**: `AssertionError: no handoff section starting 'sections '; got
[...]` — the `sections` header was absent from the section dict entirely.

**Confirmed passing after the fix.**

### Builder-parity addition (lead's follow-up message)

The lead added a second requirement mid-task: a test that would catch this SHAPE of defect (one
builder silently missing a call the others have) generically, not just this one instance, since
`_build_pdf_lines` missed `_sections_lines` for a full release cycle before the gate caught it.

Added `TestHandoffBuilderParity.test_all_four_builders_emit_the_shared_core`. It does **not**
assert all four builders emit identical headers — `@page` vs. DXA page math vs. slide layout vs.
a px canvas are real, correct format differences. It asserts a **shared core** of four concepts
that all four builders read from the same four resolved tables today (`headings`+`structures`,
`typefaces`, `type-scales`, `palette`): **sections, fonts/font-face, font sizes, palette**. Each
must produce a header (candidate prefixes per concept, since docx/pptx say `fonts:` and pdf/png
say `font-face`) carrying at least one line, `NOT_PRESENT` or real, never omitted outright. `page`/
`page flow` and `render command` were deliberately left out of the core: docx has no `render
command` (doesn't self-render) and pptx's `page flow` is legitimately `NOT APPLICABLE` text, not a
content block — both are real per-format differences, not a candidate omission shape.

**Verified it would have caught this defect**: temporarily removed the
`lines.extend(_sections_lines(resolved))` line just added to `_build_pdf_lines` and reran —
`SUBFAILED(format='pdf', concept='sections')`, message `no section header starting with any of
('sections ',) for concept 'sections'`. Restored the line, reran — passed clean, 16 subtests. Both
checked by hand.

## Before / after — proof on two pdf-only families

`quote-devis` (`issuer: From` — the exact wording the gate named):

Before (`--format pdf`, no `sections` block anywhere in the output):
```
  heading elements (semantic HTML, one <hN> per type-scale h<n> role):
    (not present in this resolution)
  palette (CSS hex colour, '#' kept -- unlike pptx, CSS requires the leading '#'):
    ...
```

After:
```
  heading elements (semantic HTML, one <hN> per type-scale h<n> role):
    (not present in this resolution)
  sections (Section Order, wording in Heading Language=en):
    issuer: From
    bill-to: Bill To
    invoice-details: Invoice Details
    line-items: Line Items
    totals: Total
    tax: Tax
    payment-terms: Payment Terms
  palette (CSS hex colour, '#' kept -- unlike pptx, CSS requires the leading '#'):
    ...
```

`invoice-tabular` (second pdf-only family, `Structure Key` also resolves to `invoice-standard`):
same before (no `sections` block), same after — identical seven-row block now present.

## SKILL.md correction

`SKILL.md`'s "Section-order guidance" section claimed `infographic` "has no Structure Key and so
gets no section order." Checked `data/base/doctypes.csv`: `infographic`'s `Structure Key` is
`infographic-canvas`, and `data/base/structures.csv` resolves it with three sections (`headline`,
`key-points`, `call-to-action`). Also checked with a real CSV parser (`csv.DictReader`, not naive
comma-splitting — `doctypes.csv` has a quoted `Keywords` column full of commas that breaks
positional field-splitting) whether any doctype still has an empty `Structure Key`:

```
python3 -c "import csv;rows=list(csv.DictReader(open('data/base/doctypes.csv',encoding='utf-8')));print([r['doc_key'] for r in rows if not r['Structure Key'].strip()])"
# []
```

Empty list — no doctype currently has a blank `Structure Key`, so the "one exception" framing is
stale, not just the named example. Rewrote the paragraph in the SKILL.md **body** (not the
extracted artefact, not the frontmatter description — untouched, budget and both test markers
undisturbed):

> `resolve` now returns a full section order for every document family this skill covers,
> `infographic` included — it resolves `infographic-canvas` (headline, key-points,
> call-to-action). Every document type gets layout, typography, colour, and print guidance
> alongside its section order.

## Verification

**pytest**: `145 passed, 88 subtests passed` — full green, no pre-existing failures carried over.

## Report

- Sections in pdf: **yes**, fixed, proven on `quote-devis` and `invoice-tabular`.
- Page-flow question: **answered** — not a one-line omission, needs a new docx-property → CSS
  mapping table; out of scope for this ship-blocker fix, reported above rather than built.
- Test added and confirmed failing-before / passing-after: **yes**, both the wording-specific test
  and the builder-parity test (parity test reverted/reran by hand, see above).
- SKILL.md corrected in source: **yes**, body only.
- pytest: **145 passed, 88 subtests passed**.
