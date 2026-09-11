# 54 — THE DROPPED-COLUMNS FIX, all four parts

Brief: research/brief-packaging-display-columns.md, including the PART 4 addendum appended to it
by lead ruling after parts 1–3 were scoped. Defect verified in
research/53-defect-verification.md (read first, not re-litigated here).

## 1. WHAT CHANGED, per part

### PART 1 — `headings` and `structures` had NO `display_columns` at all
File: `research/build-manifest.py` (the generator; `data/schema-manifest.json` is generated,
never hand-edited — regenerated below).

- `tables["headings"]["display_columns"]` added: `["canonical_section", "Heading Text",
  "Language", "Is Primary"]` — all 4 data columns, the full set the census in research/53 found
  hidden (0 of 4 shown).
- `tables["structures"]["display_columns"]` added: `["Display Name", "Section Order",
  "Heading Language", "Heading Depth Max", "TOC Depth", "Front Matter Numbering",
  "Caption Position", "Cross-Ref Style"]` — all 8 data columns (2 were already shown via the
  searchable/FK-source default; the list is a superset per the module's own convention).

### PART 2 — `constraints` and `type-scales` declared an INCOMPLETE list
Same file, same generator. The existing lists were extended, not replaced with a fallback:

- `constraints`: `["Set Key", "Element Scope", "Parameter"]` →
  `["Set Key", "Applies To", "Check", "Element Scope", "Parameter", "Threshold", "Severity"]`
  (all 7 data columns; the 4 the census named — Applies To, Check, Threshold, Severity — are now
  in it).
- `type-scales`: `["Medium", "Role", "Size pt"]` →
  `["scale_key", "Medium", "Role", "Size pt", "Leading Ratio"]` (all 5; scale_key and Leading
  Ratio added).

Regenerated with `python3 research/build-manifest.py` (run from
`skill/document-design-intelligence/`): `wrote data\schema-manifest.json -- 14 tables, 174
columns, 13 foreign keys (5 group), 12 list columns, 1 reference columns, 12 distinct-token
columns, 8 tables with display_columns` (was 6). The module comment at the top of the generator
was updated to say eight and to name this brief, so the next reader doesn't have to recount.

### PART 3 — `ddi.py`'s `HANDOFF_VOCAB` had no `headings` or `structures` entry
File: `skill/document-design-intelligence/scripts/ddi.py`. Parts 1–2 alone put heading wording
into the resolved JSON and the plain-text path, but `ddi.py handoff` only ever reads names out of
`HANDOFF_VOCAB`, and that dict named neither table — confirmed by `grep -n "structures\|headings"
scripts/ddi.py` returning nothing before this change. So the handoff would have kept printing
nothing from either table even with parts 1–2 fully applied.

Added to `HANDOFF_VOCAB`: `structure_table`, `structure_section_order_column`,
`structure_heading_language_column`, `headings_table`, `headings_canonical_section_column`,
`headings_text_column`, `headings_language_column`, `headings_is_primary_column`.

Added `_section_headings(resolved)` — reads the resolved `structures` row's `Section Order` and
`Heading Language`, then for each section in order looks up the `headings` row where
`Language == Heading Language` and `Is Primary == "yes"`, returning `(lang, [(section, text_or_None), ...])`.
Added `_sections_lines(resolved)` to render that as a `sections (Section Order, wording in
Heading Language=<lang>):` block. Wired into both `_build_docx_lines` (after "TOC heading
levels") and `_build_pptx_lines` (after "font sizes") — not into `_build_pdf_lines`, which at the
time did not have a TOC-role section either. (Part 4, below, changed `_build_pdf_lines`
substantially; `sections` was deliberately NOT added there even so — my own judgement call, not
sourced to any research file: the pdf builder's "@page (native HTML -> Chromium/WeasyPrint
pipeline)" header already says this path renders from HTML, where a heading's TEXT is authored
directly into the markup at the `<hN>` element the "heading elements" block (part 4) names, unlike
docx/pptx which need the wording handed over as separate data to build a paragraph run. Flagged
here as CONVENTION/judgement, not verified against a renderer implementation that doesn't exist
yet in this repo.)

**The language-and-primary selection question, answered:** `structures."Heading Language"` is
already an authored, per-structure column in the schema (`data/base/structures.csv`, one value
per row: `cv-experienced` carries `en`) — it is the schema's own language selector, not a new
mechanism invented for this fix. `headings."Is Primary"` then picks the one wording per section
in that language. This is grep-verifiable in `data/base/structures.csv` and needed no new
vocabulary or flag.

### PART 4 — ADDED BY LEAD RULING: `_build_pdf_lines` never read `type_scale_table` or
### `palette_table` at all
File: same `ddi.py`. Confirmed the brief's own diagnosis first: before this change,
`_build_pdf_lines` read exactly `page_format_table`, `render_target_table` and `typeface_table`
— `type_scale_table` and `palette_table`, which `_build_docx_lines`/`_build_pptx_lines` both read,
never appeared in the function at all. The failure shape is one level worse than parts 1–3: the
**section headers themselves** (`font sizes`, `heading elements`, `palette`) were absent from the
output, not merely present-and-empty — a missing block is invisible in a way `(not present in
this resolution)` is not.

Added three blocks to `_build_pdf_lines`, inserted after the existing "font-face stack" block and
before "render command", in the pdf builder's own idiom (plain CSS `pt`, no DXA/half-point
conversion; `#`-prefixed hex, unlike pptx's stripped form; semantic `<hN>` elements instead of
docx's `HeadingLevel.HEADING_N` enum):
- `font sizes (CSS pt ...)` — one line per resolved `type-scales` row, `{role}: {size}pt`.
- `heading elements (semantic HTML ...)` — reuses the existing `_heading_roles()` helper (already
  shared with docx/pptx) to map each `h<n>` type-scale role to `<h{n}>`.
- `palette (CSS hex colour ...)` — one line per populated palette role column, hex kept as-authored
  (CSS requires the leading `#`, so no `_strip_hex()` call here, unlike pptx).

Each block emits `(not present in this resolution)` when its source table/row is empty or
resolves no matching rows, per the ruling's explicit instruction not to omit a block that
genuinely doesn't apply — so a family with no h-roles in its type scale (e.g. `invoice-tabular`,
`form-print` scale = body/legal only) still prints the `heading elements` header with that
sentence under it, rather than no header at all.

## 2. BEFORE / AFTER, quoted

### Resolved JSON — headings (BEFORE, on `cv-uk`)
```json
"headings": [
  { "key": "contact-en-1" },
  { "key": "contact-en-2" },
  { "key": "contact-en-3" },
  { "key": "contact-en-4" },
  { "key": "contact-fr-1" },
```
### Resolved JSON — headings (AFTER)
```json
"headings": [
  {
    "key": "contact-en-1",
    "canonical_section": "contact",
    "Heading Text": "Contact",
    "Language": "en",
    "Is Primary": "yes"
  },
  {
    "key": "contact-en-2",
    "canonical_section": "contact",
    "Heading Text": "Contact Information",
    "Language": "en",
    "Is Primary": "no"
  },
```
Grepping the full `cv-uk` resolved JSON for the four wordings named in the brief:
`Experience` x2, `Work Experience` x1, `Employment History` x1, `Professional Summary` x1 — all
present.

### Resolved JSON — structures (BEFORE)
```json
"structures": [
  {
    "key": "cv-experienced",
    "Display Name": "CV -- experienced hire",
    "Section Order": "contact;summary;experience;education;skills;certifications;projects;publications"
  }
]
```
### Resolved JSON — structures (AFTER)
```json
"structures": [
  {
    "key": "cv-experienced",
    "Display Name": "CV -- experienced hire",
    "Section Order": "contact;summary;experience;education;skills;certifications;projects;publications",
    "Heading Language": "en",
    "Heading Depth Max": "2",
    "TOC Depth": "0",
    "Front Matter Numbering": "none",
    "Caption Position": "fig=below;table=above",
    "Cross-Ref Style": "numbered"
  }
]
```

### Resolved JSON — constraints (BEFORE)
```json
{ "key": "ats-no-multi-column", "Set Key": "ats-strict", "Element Scope": "", "Parameter": "columns" }
```
### Resolved JSON — constraints (AFTER)
```json
{
  "key": "ats-no-multi-column",
  "Set Key": "ats-strict",
  "Applies To": "doctype:cv-*",
  "Check": "validate-ats-structure",
  "Element Scope": "",
  "Parameter": "columns",
  "Threshold": "0",
  "Severity": "fail"
}
```
(`Element Scope` is legitimately blank for this row — cv-uk's constraints are doc-level, not
element-scoped. That's authored data, not a dropped column; see the test's `ALLOWED_ALL_BLANK`.)

### Resolved JSON — type-scales (BEFORE / AFTER)
Before: `{ "key": "cv-print-print-body", "Medium": "print", "Role": "body", "Size pt": "11" }`
After: `{ "key": "cv-print-print-body", "scale_key": "cv-print", "Medium": "print", "Role": "body", "Size pt": "11", "Leading Ratio": "1.35" }`

### `ddi.py handoff --format docx` on `cv-uk` (BEFORE)
```
  TOC heading levels (docx-js HeadingLevel.* -- research/23 docx:33):
    h1  ->  HeadingLevel.HEADING_1
    h2  ->  HeadingLevel.HEADING_2
  characterSpacing (DXA -- docx (npm) TextRun option; UNSOURCED from research/23, see module docstring):
    (not present in this resolution)
```
No `sections` block exists at all before the fix — grepping the full before-fix handoff output
for `Experience`, `Work Experience`, `Employment History`, `Professional Summary` returns **0
matches**, matching research/53 exactly.

### `ddi.py handoff --format docx` on `cv-uk` (AFTER)
```
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
  characterSpacing (DXA -- docx (npm) TextRun option; UNSOURCED from research/23, see module docstring):
    (not present in this resolution)
```
`experience: Experience` is present — the primary English wording for that section, reaching the
handoff by name. The pptx handoff carries the identical `sections` block in the same position
(after "font sizes").

### Plain-text path (`resolve.py --doctype cv-uk`, no `--json`) — BEFORE / AFTER
Before (research/53's own finding, reproduced): `headings/contact-en-1` and nothing else.
After:
```
  headings/contact-en-1
    canonical_section: contact
    Heading Text: Contact
    Language: en
    Is Primary: yes
```
Confirms the fix reaches the second display call site (`resolve.py` line 577), not only the JSON
one — the brief's "unreachable by ANY path" claim is now closed on both.

### Second doctype, checked because a CV section can have 2-3 competing wordings and a non-CV
section has exactly one (RESUME.md's own v0.3 backlog note) — does the primary-selection logic
still work with nothing to choose between? `ddi.py handoff --format docx` on `report-long-toc`:
```
  sections (Section Order, wording in Heading Language=en):
    cover: Cover Page
    table-of-contents: Table of Contents
    executive-summary: Executive Summary
    introduction: Introduction
    methodology: Methodology
    findings: Findings
    conclusion: Conclusion
    recommendations: Recommendations
    appendices: Appendices
    bibliography: References
```
All 10 sections resolve, none read `(not present in this resolution)`. I then scanned the whole
of `data/base/structures.csv` (17 rows) and `data/base/headings.csv` programmatically: zero
structures carry a blank `Heading Language`, and every `(canonical_section, Heading Language)`
pair across all 17 structures has exactly one `Is Primary = yes` row. **The fix is not CV-only or
cv-uk-only; it holds for every shipped family.**

**Note on which wordings reach the handoff vs. the JSON, on purpose:** the resolved JSON carries
ALL authored variants for every language (`Experience`, `Work Experience`, `Employment History`,
`Professional Summary`, …) because the FK walk pulls every `headings` row whose
`canonical_section` is in the structure's `Section Order`, regardless of language or primacy —
that's the full picture a model reasons over. The handoff carries only ONE wording per section
(the primary, in the structure's own `Heading Language`) because that's what a renderer needs to
put on the page — it cannot print four alternate headings for one section. This is the intended
division of labour, not an oversight.

### `ddi.py handoff --format pdf` on `invoice-tabular` (BEFORE) — a pdf-only family
```
HANDOFF (format=pdf)
  @page (native HTML -> Chromium/WeasyPrint pipeline):
    size: 210mm 297mm
    margin: 15mm 20mm 15mm 20mm  (top right bottom left)
  font-face stack (embed vs. safe-stack per render target's Font Rule):
    headless-chromium (embed): Public Sans / Public Sans
    weasyprint (embed): Public Sans / Public Sans
    wkhtmltopdf (embed): Public Sans / Public Sans
  render command:
    headless-chromium: /opt/google/chrome/chrome --headless --no-sandbox --disable-gpu --print-to-pdf=%o --no-pdf-header-footer %i
    weasyprint: weasyprint (module)
    wkhtmltopdf: wkhtmltopdf
  constraints to preflight (Set Keys): report-typography
next: python3 scripts/preflight.py <rendered-file>.pdf
```
Note what's absent: it jumps straight from `font-face stack` to `render command`. No `font sizes`
header, no `heading elements` header, no `palette` header — not empty, ABSENT, exactly as the
ruling described.

### `ddi.py handoff --format pdf` on `invoice-tabular` (AFTER)
```
  font-face stack (embed vs. safe-stack per render target's Font Rule):
    headless-chromium (embed): Public Sans / Public Sans
    weasyprint (embed): Public Sans / Public Sans
    wkhtmltopdf (embed): Public Sans / Public Sans
  font sizes (CSS pt -- native unit for an HTML/Chromium/WeasyPrint pipeline, no conversion needed):
    body: 11pt
    legal: 8.5pt
  heading elements (semantic HTML, one <hN> per type-scale h<n> role):
    (not present in this resolution)
  palette (CSS hex colour, '#' kept -- unlike pptx, CSS requires the leading '#'):
    Primary: #22282E
    Secondary: #55606B
    Accent: #2E5C82
    Background: #FFFFFF
    Foreground: #1A1E22
  render command:
```
`heading elements` correctly reads `(not present in this resolution)` here — `invoice-tabular`'s
type scale (`form-print`) genuinely has no `h1`/`h2`/`h3` rows (body/legal only), so there is no
heading level to name. That's real authored data, not a residual bug; the block header still
prints, which is the point of the fix (a real absence is now visible, not silent).

### A pdf family that DOES have heading roles: `ddi.py handoff --format pdf` on `poster` (AFTER)
```
  font sizes (CSS pt -- native unit for an HTML/Chromium/WeasyPrint pipeline, no conversion needed):
    body: 11pt
    h3: 12pt
    h2: 16pt
    h1: 24pt
  heading elements (semantic HTML, one <hN> per type-scale h<n> role):
    h1  ->  <h1>
    h2  ->  <h2>
    h3  ->  <h3>
  palette (CSS hex colour, '#' kept -- unlike pptx, CSS requires the leading '#'):
    Primary: #1A1A1A
    Secondary: #4A4A4A
    Accent: #C81E3A
    Background: #FFFFFF
    Foreground: #1A1A1A
```
All three new blocks populate with real content here, proving `heading elements` works when the
data actually has heading roles to show, not only that it degrades gracefully when it doesn't.

**A finding, not a fix:** the ruling also named `infographic` as an affected family. I checked —
`infographic`'s only render target is `png-social` (not pdf at all), and its `doc-reasoning` row
has blank `Style Key`/`Palette Key`/`Typeface Key`, so no palette or type-scale could ever resolve
for it regardless of the pdf builder. Its pdf handoff output is unchanged by this fix because
`infographic` was never a pdf-target family to begin with — this looks like a stale reference in
the ruling (the family list may have shifted since it was written), not a bug this brief needs to
carry. `invoice-tabular` and `quote-devis`, the other two named families, both reproduce and are
both fixed.

**A sharper finding surfaced while checking this, flagged for the lead, NOT fixed here (out of
this brief's scope):** `infographic`'s only render target, `png-social`, has `Format: png`.
`_FORMAT_BUILDERS` and `cmd_handoff`'s `--format` choices only cover `docx`/`pptx`/`pdf` —
`render-targets.Format`'s enum has 5 values (`pdf, docx, pptx, png, html`), and `png`/`html` have
NO handoff builder at all. I grepped every doctype's `Render Target Keys` against `render-targets.
Format`: `infographic` is the ONE shipped family whose render targets resolve exclusively to a
format with no builder (no doctype currently resolves only to the one `html` target,
`html-static`). So `infographic` isn't just missing wording, the way headings were before this
brief — it has no handoff path at all, which is RESUME.md's own v0.3 standing rule ("a format is
DONE only when … handoff values reach the renderer") unmet for a shipped family. This is a new
finding, not part of parts 1–4, and I have not touched `_FORMAT_BUILDERS` or `cmd_handoff`.

## 3. PART 3 CONCLUSION
Heading wording belongs in the handoff block, as a `sections` list of `(canonical_section,
primary Heading Text)` pairs ordered by `Section Order`, selected in the structure's own
`Heading Language`. Implemented for docx and pptx (both need wording handed over as data to build
a run/paragraph). NOT added to pdf's handoff (see part 4's note above) — that pipeline renders
HTML, where the wording lives directly in the `<hN>` markup the "heading elements" block already
names, so a parallel `sections` list would duplicate rather than add information. A section with
no primary heading in its structure's language prints `(not present in this resolution)` for that
section specifically, rather than dropping it silently.

## 3b. PART 4 CONCLUSION
`_build_pdf_lines` gets the same two tables `_build_docx_lines`/`_build_pptx_lines` already read
(`type-scales`, `palette`), rendered in the pdf builder's own CSS-flavoured idiom rather than
docx's DXA/half-points or pptx's stripped hex. `heading elements` reuses the existing
`_heading_roles()` helper rather than re-deriving h-role detection a third time. Every new block
degrades to the ruled `(not present in this resolution)` sentence when its source data is
genuinely empty, per the explicit instruction that a missing block — not an empty one — was the
actual defect.

## 4. THE TEST
Added `TestDroppedColumnsReachResolvedOutput` to
`skill/document-design-intelligence/scripts/tests/test_ddi.py`, three test methods, run against
the real `data/base` (not a toy fixture), via the actual `ddi.py resolve` / `ddi.py handoff`
subprocess pipeline:

1. `test_every_authored_column_reaches_the_resolved_json` — for each of the four tables, every
   named data column (hardcoded independently of the manifest, not read back from it) must be a
   key on every resolved row, and at least one row must carry a non-blank value for it (except
   `constraints."Element Scope"`, which is legitimately all-blank for `cv-uk`).
2. `test_headings_carry_the_actual_authored_wording_not_bare_ids` — asserts the four wordings
   named in the brief are literally present in `resolved.headings`.
3. `test_handoff_docx_sections_carry_primary_heading_wording` — runs the full resolve → handoff
   pipeline on TWO doctypes, `cv-uk` (2-3 competing wordings per section) and `report-long-toc`
   (exactly one wording per section — so this also proves primary-selection doesn't only work
   when there's something to choose between), and asserts named section wordings appear in the
   rendered docx handoff text, not the intermediate JSON, with no `(not present in this
   resolution)` entries anywhere in the block.

For part 4, added `TestPdfHandoffCarriesTypeScaleAndPalette` (same file), two test methods:
4. `test_invoice_tabular_pdf_only_family_gets_sizes_and_palette` — the pdf-only family named in
   the ruling; asserts `font sizes` and `palette` blocks exist AND carry real `pt`/`#hex` content.
5. `test_poster_pdf_gets_sizes_headings_and_palette` — a pdf family whose type scale actually has
   `h1`/`h2`/`h3`, so `heading elements` is asserted against real `<h1>`/`<h2>`/`<h3>` content, not
   only its graceful-degradation path.

Both reuse `_section_values` from `TestHandoffEndToEndOnRealData`, which `self.fail()`s outright
if a section header is not found at all — this is exactly the assertion that catches a MISSING
block, as opposed to an empty one, which is precisely what part 4's defect was.

**What it would say if the feature produced NOTHING AT ALL:** every assertion reads a named
column out of a row dict, or a named line out of rendered handoff text. A resolved row that is
still `{"key": "contact-en-1"}` fails `column in row` for all four `headings` columns
immediately; blank-but-present columns fail the non-blank check; a handoff with no `sections`
block fails `assertIn` outright; a pdf handoff missing the `font sizes`/`heading elements`/
`palette` headers entirely fails `_section_values`'s own `self.fail()` before any content is even
checked. None of exit-code-0, row-count, or "the manifest declares the key" would have caught the
original defect — this test does not check any of those.

**Verified to fail before the fix, pass after — parts 1–3:** checked out the pre-fix commit
(`bfa25f7`, verification-only, before any manifest/ddi.py changes) into a throwaway worktree,
copied only the new test file in, ran `TestDroppedColumnsReachResolvedOutput`: exit summary
`22 failed, 3 passed, 26 deselected, 8 subtests passed` — every genuinely-new `EXPECTED_COLUMNS`
entry, all four heading wordings, and BOTH doctypes of the handoff-sections test failed. Ran
again on the fixed tree: all pass.

**Verified to fail before the fix, pass after — part 4:** checked out `c742b72` (parts 1–3 landed,
part 4 not yet started) into a throwaway worktree, copied the test file in, ran
`TestPdfHandoffCarriesTypeScaleAndPalette`: `2 failed, 29 deselected` — both fail with
`AssertionError: no handoff section starting 'font sizes '` (the header genuinely absent, matching
the defect exactly). Ran again on the fixed tree: both pass. Both worktrees were removed after use.

## 5. FULL PYTEST RESULT
```
164 passed, 68 subtests passed
```
Run from `skill/document-design-intelligence/` with `python3 -m pytest -q`. Zero failures, zero
skips. Pre-existing baseline (before this brief's tests were added) was **159 passed, 34 subtests
passed**. Parts 1–3's `TestDroppedColumnsReachResolvedOutput` (3 test methods) contribute exactly
**34 new subtests** (34 → 68), confirmed by running that class in isolation:
`3 passed, 34 subtests passed`. Part 4's `TestPdfHandoffCarriesTypeScaleAndPalette` adds 2 more
plain test methods with no subTests (159+3+2 = 164 test methods; subtests stay at 68). Breakdown
of the 34 subtests: 24 from the column-presence loop (4+8+7+5
columns across the four tables), 4 from the heading-wording check, 6 from the two-doctype handoff
test (2 outer `doctype` subTests, each containing 2 inner `section` subTests).

## 6. THE CR ARCHIVE FINDING
Checked the WHOLE published v0.2.0 archive, not one member, two ways: the cached copy at
`research/test-builds/_published-v0.2.0-reference.zip` (143209 bytes, matching research/53's
cited size) and a **fresh** `gh release download v0.2.0 --repo Magazem/Smart-design` into a
scratch directory. Both: 39 members, **total CR bytes across the entire archive: 0**. `ddi.py`
specifically: 0 CR bytes, md5 `09317cf262d3d8f6e914d9411556949e` — the exact hash research/53
itself recorded as the value "after stripping CR" from the local CRLF working copy, confirming
the published member was already LF-only.

**Conclusion: RESUME.md's "Zero CR bytes" claim for the published v0.2.0 asset is CORRECT and is
now verified against the full archive, not left as a loose thread — no correction needed there.**
The figure that does not reproduce is research/53 ADDENDUM's "the published `ddi.py` contains
1209 CR bytes": that number is not present in either the cached reference copy or a brand-new
download. This is not just unreproduced, it is **internally impossible on the addendum's own
numbers**: it also claims the local CRLF copy carries 1899 CR bytes "a difference of exactly 690,
matching the 690 lines in the file" — but a file with 690 lines has at most 690 line-ending
positions, so 1899 CR bytes cannot occur in it at all (a legitimately CRLF file of 690 lines caps
out at 690 CR bytes, not 1899). Both figures in that pairing cannot be literal CR-byte counts of
the same file; at least one, and probably both, measured something else (word count? a different
file? a stale cached read?) while being reported as CR bytes. I cannot reconstruct which
measurement it actually was, so I'm flagging the pairing as wrong rather than guessing at a
replacement number. Whoever owns research/53 should retract or correct that line; I have not
edited that file, since the brief scoped correction to RESUME.md and RESUME.md turned out not to
need one.

Separately, confirmed `build_zip.py` already normalises every text member's line endings on every
build: `normalize_newlines()` (line 135) is called on every member's bytes at the point it's
written into the archive (line 220, `zf.writestr(info, normalize_newlines(path.read_bytes()))`).
No code change was needed there; this was already in place before this brief.

## 7. A v0.3 BACKLOG LINE THIS FIX FALSIFIES — FLAGGED FOR THE LEAD, NOT EDITED
RESUME.md's v0.3 backlog says, under "HEADING VARIANTS for non-CV families": "Nothing reads Is
Primary today, so this is model-facing only." That is no longer true: `_section_headings` in
`ddi.py` now reads `Is Primary` to select the wording that reaches the docx/pptx handoff (part 3
above). This raises the stakes on the per-structure scan I ran for section 2 above — a family
where `Is Primary` was authored carelessly (two rows marked `yes` for the same section/language,
or none) would now visibly affect a renderer, not just model reasoning. I checked: no such case
exists across the 17 shipped structures (section 2's scan). Not editing RESUME.md for this per
standing instruction — flagging it here for whoever next touches that backlog line.

## 8. KNOWN-LIMITATION ENTRY
None. All four parts are fixed and verified end to end (resolved JSON, plain-text path, and the
docx/pptx/pdf handoffs all now carry the data the resolver already resolves); the CR sub-item
resolved with no defect found in the shipped artifact. Nothing here is left unfixed, so no
RELEASE-NOTES.md entry is drafted. (The `infographic` non-reproduction noted under part 4 is not
a limitation of this fix — that family was never a pdf-target family, so there was nothing for
this fix to touch there.)

## 9. WHAT I COULD NOT VERIFY
- The pptx handoff's `sections` block was checked by direct command output, not by a dedicated
  automated test (only the docx handoff has one, matching the existing test file's own docx-only
  precedent for `TestHandoffEndToEndOnRealData`). It is structurally the same code path
  (`_sections_lines`) as the tested docx block, so this is a coverage gap, not a known defect.
- I did not re-run the full activation/browser test suite — out of scope for this brief and
  unrelated to the resolver/generator/handoff code touched here.
- `research/53`'s specific "1209 CR bytes" figure could not be reproduced or explained from
  available artifacts; flagged above (section 6) as internally inconsistent rather than guessed
  at.
- Part 4's `sections`-vs-`heading elements` design call (pdf gets structural `<hN>` tags instead
  of a parallel wording list) is my own judgement, not sourced to any research file — flagged as
  such in section 1's PART 3 discussion.
- I did not build a fixture for a doctype whose type-scale has NO rows at all resolving for pdf
  (as opposed to `invoice-tabular`'s "rows exist but no h-roles" case) — I did not find a real
  shipped family in that state to test against, so the `(not present in this resolution)` path
  for a fully-absent `type-scales` table on pdf is exercised by code reading (the same `if
  scale_rows:`/`else:` guard already used elsewhere in this file) rather than an end-to-end run.
