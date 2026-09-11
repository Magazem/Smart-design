# HANDOVER — invoked-quality pass (task 01a08f75) — PAUSED mid-run

Written by the Coverage and Gap Analyst before a context clear, on orchestrator instruction.
Nothing below is the deliverable. `research/51-invoked-quality.md` is NOT yet written.

## Asset exercised — provenance PROVEN
`skill/dist/document-design-intelligence-0.0.1-dev.zip`, md5 `68276653bea670092d5adc860de2eb06`,
extracted to a temp dir and run from there. All six of the brief's published-asset reference
values match exactly:

| Reference value | Brief says | Measured |
|---|---|---|
| description length | 972 chars, starts "Creating any document type below" | 972, same opening |
| constraints rows | 47 | 47 |
| type-scales rows | 20 | 20 |
| headings rows | 204 | 204 |
| structures rows | 17 | 17 |
| doctypes rows | 30 | 30 |
| tables with `display_columns` | 6 | 6 (palettes, typefaces, type-scales, page-formats, render-targets, constraints) |

Caveat to carry into the report: the asset's `VERSION` file reads `0.0.1-dev`, not `0.2.0`.
Content matches published v0.2.0; the version stamp does not say so.

## Families run (6 of 30 doc keys), two phrasings each
cv-uk, report-long-toc, slide-deck-projection, invoice-tabular, quote-devis (French prompt),
infographic. Paths covered: CV control / multi-tier print (h1+h2+h3) / pptx layout model /
short tabular artefact / non-English / documented no-structure family.

## Findings so far — NOT yet ranked or written up

**A. `headings` rows reach every output path as bare keys with NO wording. Candidate P0.**
`data/base/headings.csv` has columns `heading_key, canonical_section, Heading Text, Language,
Is Primary`. The manifest gives `headings` no `display_columns` and no searchable columns, so
`resolve.py:_display_columns` (line ~500) returns an empty column list. Actual JSON for a UK CV:
```
"headings": [{"key": "contact-en-1"}, {"key": "contact-en-2"}, {"key": "contact-en-3"}]
```
Plain-text path prints the same thing, one bare id per line, 63 of them for cv-uk.
`ddi.py handoff` reads ONLY the resolved JSON (`ddi.py` line 624, `json.loads(Path(...).read_text())`;
no CSV access anywhere in the file), so `Heading Text` cannot reach a renderer by ANY path.
v0.2.0's headline feature — 204 heading rows in three languages — is authored, gated, shipped
and unreachable. Not covered by any RELEASE-NOTES known limitation.
Fix site: `research/build-manifest.py` (the manifest is generated — never hand-edit
`data/schema-manifest.json`), and/or the default-column logic in `scripts/resolve.py`.

**B. Same root cause, other dropped columns.** One defect, four surfaces:
- `headings` — Heading Text, Language, Is Primary
- `structures` — Heading Language, Heading Depth Max, TOC Depth, Front Matter Numbering,
  Caption Position, Cross-Ref Style (6 of 9 columns invisible; this IS the section model)
- `constraints` — Threshold, Severity (the rule's actual limit and whether it fails or warns)
- `type-scales` — Leading Ratio (leading is the one thing this repo does cite Bringhurst for)

**C. `infographic` prints a bare empty field.** Resolve output:
```
    Structure Key:
    Constraint Set Keys: no constraint-set-keys guidance for infographic
    Region Key: no region-key guidance for infographic
```
`_field_value` only emits the ruled "no X guidance for Y" sentence for GROUP foreign keys.
`Structure Key` is a single FK, so it silently prints blank — the exact empty-answer shape.
Extends, but is not covered by, the known limitation "infographic has no section order at all".
Its pdf handoff is also mostly empty: no font-face stack, no render command, no constraints.

**D. `slide-deck-projection` inherits the CV type scale.** Its resolved type-scales are
`cv-print-print-body/h2/h1` at 11/16/24pt — print sizes on a projected deck. A
`deck-projection` scale_key exists in `type-scales.csv` (projection body = 24pt) and is NOT
the one resolved. The pptx handoff therefore hands 11pt body to a projector. Needs one more
check of how the scale is selected before filing severity.

**E. Two constraint sets are unreachable.** `font-safety` and `redesign` appear in
`constraints.csv` `Set Key` but no doctype's `Constraint Set Keys` references either
(verified by set difference across all 30 doctypes; the only other mentions in the tree are
prose in `data/schema-manifest-NOTES.md`). Dead rows.

**F. Handoff blocks that ARE populated — report this as working.**
- report-long-toc docx: page 210x297mm -> 11906x16838 DXA; margins 25/25/30/20mm -> DXA;
  fonts Times New Roman x3; sizes body 11/h3 12/h2 16/h1 24pt with half-point conversions;
  HeadingLevel.HEADING_1/2/3; palette 5 values incl. Accent #2E5C82; page flow keepNext,
  widowControl min 2, cantSplit, tblHeader, figure/caption keepNext — all five present.
- cv-uk docx: same shape, h1/h2 only (correct, do not file), palette Accent empty because
  `mono-ink` genuinely has no Accent — NOT a defect.
- deck pptx: LAYOUT_16x9 10x5.625in, palette hex stripped of '#', and page flow correctly says
  "NOT APPLICABLE -- slides do not paginate".
- invoice/devis pdf: @page 210mm 297mm, margin 15/20/15/20mm, three-engine font stack and
  render commands present.

## Zero refusals
No `[NO MATCH]` in any of the 11 prompts run. Two `[ABSTAIN]`s, both on a shipped family:
"Create a CV for an experienced software engineer, print it" (top candidate slide-deck-handout)
and "Make a slide deck for a projected conference talk" (three deck rows within 0.9). These are
the resolver running and declining to answer, which is output quality, not routing.

## What is left to do
1. Settle finding D — read how `Scale Key` is chosen for the deck path.
2. Field 5 (designed vs generic) — diff two structurally distant families' full resolve output.
3. Rank the defects and write `research/51-invoked-quality.md` per the brief's section list.
4. Record the 24 doc keys not run, each against the path it duplicates.
