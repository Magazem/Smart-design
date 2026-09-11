# 63 — characterSpacing removed from the docx handoff

Ruled 2026-09-11 (`research/brief-packaging-characterspacing.md`). Scope: drop the docx
`characterSpacing` line, its dead vocabulary entry, and its stale test reference. pptx
`charSpacing` untouched.

## What changed
- `ddi.py` `HANDOFF_VOCAB`: removed `"docx_letter_spacing_key": "characterSpacing"`.
- `ddi.py` `_build_docx_lines`: removed the `characterSpacing` line (and the `spacing_pt =
  _letter_spacing_pt(...)` call that only fed it).
- `ddi.py`: removed `_pt_to_dxa()` and the `PT_TO_DXA` constant — both were now dead, having
  existed only to convert the value that line printed.
- `scripts/tests/test_ddi.py`: dropped the sentence in `TestHandoffEndToEndOnRealData`'s class
  docstring noting `characterSpacing` was "deliberately NOT asserted" — the key no longer exists
  to not-assert.

Note: the docx-line and vocab-entry removal had already landed on `main` (commit `6f345b1`,
authored ahead of this task reaching me) before I started. My work here was finishing the two
pieces that commit left behind — the stale test docstring and the now-dead `_pt_to_dxa`/
`PT_TO_DXA` helper — plus verification below.

`pptx_letter_spacing_key` / `charSpacing` (ddi.py:585-589 in the pptx builder) is untouched:
still sourced from research/23 pptx:458, still reads `_letter_spacing_pt`, which stays because
pptx still needs it.

## Verification

**pytest**: 36 passed, 4 subtest failures, in 1 test method — `52 subtests passed`. The failures
are `TestPngHandoffBuilder::test_infographic_empty_reasoning_columns_degrade_to_not_present_not_omission`,
pre-existing and unrelated to this change (confirmed by running the same test against `HEAD`
before my edits — identical failure). Not full green; the gap is the known open infographic
issue from the png-handoff-builder task, not something this change touched or introduced.

**docx handoff, `cv-uk`** (`python3 ddi.py handoff --json <resolved> --format docx`):

```
HANDOFF (format=docx)
  page (docx-js DXA; 1 mm = 56.6929 DXA, 1 pt = 20 DXA -- research/23 docx:25):
    Trim W mm: 210mm  ->  Width DXA: 11906
    Trim H mm: 297mm  ->  Height DXA: 16838
    Margin Top mm: 25mm  ->  Margin Top DXA: 1417
    Margin Bottom mm: 25mm  ->  Margin Bottom DXA: 1417
    Margin Inside mm: 25mm  ->  Margin Inside DXA: 1417
    Margin Outside mm: 25mm  ->  Margin Outside DXA: 1417
  fonts:
    Heading Family: Arial
    Body Family: Arial
    Safe Stack Fallback: Arial
  font sizes (docx-js half-points -- OOXML `sz` / docx `size`; UNSOURCED from research/23, see module docstring):
    body: 11pt  ->  22.0 half-points
    h2: 16pt  ->  32.0 half-points
    h1: 24pt  ->  48.0 half-points
  TOC heading levels (docx-js HeadingLevel.* -- research/23 docx:33):
    h1  ->  HeadingLevel.HEADING_1
    h2  ->  HeadingLevel.HEADING_2
  sections (Section Order, wording in Heading Language=en):
    contact: Contact
    summary: Summary
    experience: Experience
    education: Education
    skills: Skills
    certifications: Certifications
    projects: Projects
    publications: Publications
  palette (hex as stored -- docx-js color-argument format not documented in research/23, kept unmodified per research/24 section 3 item 3):
    Primary: #1A1A1A
    Secondary: #4A4A4A
    Background: #FFFFFF
    Foreground: #111111
  page flow (OOXML paragraph/table properties, mapped from each constraint's own Parameter column -- convention, not sourced to any authority this library cites):
    (not present in this resolution)
  constraints to preflight (Set Keys): ats-strict, cv-region
next: python3 scripts/preflight.py <rendered-file>.docx
```

`characterSpacing` is gone. No other block dropped or reordered — `page flow` still prints its
`(not present in this resolution)` line rather than being omitted, matching the "we are removing
a line, not learning to omit blocks again" guard.

## Opinion on the pptx asymmetry (for the record, not acted on)

I'd lean toward keeping `charSpacing` as-is, for the reason `RESUME.md`'s existing ruling already
gives: a sourced key that reads a missing column and reports `(not present in this resolution)`
is the system working as designed, not noise — the "not present" line exists precisely to make an
honest, citable, currently-empty value visible without fabricating one. The docx key was noise for
a different reason (unsourced *and* unfillable); pptx's is only unfillable. If the schema later
grows `Letter Spacing pt` on some table, `charSpacing` starts emitting real values for free with no
code change, so removing it now would just mean re-adding it later for no benefit. I'd only revisit
this if pptx's citation (research/23 pptx:458) turns out to be wrong or the key proves actively
misleading to whatever renders the handoff — neither is true today.
