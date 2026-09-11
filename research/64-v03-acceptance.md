# 64 — v0.3 ACCEPTANCE GATE — invoked-quality pass on the extracted built artefact

Run 2026-09-11 by the Coverage and Gap Analyst, per `research/brief-coverage-v03-acceptance.md`.
This is the gate before tagging v0.3. Verdict in §6.

**Asset under test, and nothing else was touched:**
`research/test-builds/v03-extracted/document-design-intelligence/`

Provenance was established before this pass and is not re-derived here: 147016 bytes, md5
`1cb0b8c9388567708d855b3c6f570fb6`, 39 members, zero CR bytes, same member list as published
v0.2.0 with 12 expected diffs itemised in `research/test-builds/README.md`.

**Contamination control.** Every command below passes `--data-dir` as an absolute path into the
extracted tree, so no invocation can resolve against `skill/` even if the shell's working
directory moves. `PYTHONIOENCODING=utf-8` on every run so console mojibake cannot be mistaken
for a data defect. `python3`, never `python`.

**Version-string carve-out, applied as the brief directs.** `VERSION` reads `0.0.1-dev` and CI
rewrites it and the SKILL.md stamp from the git tag. Findings about behaviour carry to the
release; findings about the version string's *value* do not. Where a finding below touches
versioning I state explicitly which side of that line it falls on.

---


## 1. Headline

**DO NOT SHIP.**

Four of the five claimed fixes are real, verified independently from the artefact, and one of them
is the P0. The fifth is **incomplete in a way that reproduces the P0 for nine of the thirty
document families.** `_sections_lines` — the helper that carries authored heading wording into a
handoff — is wired into the docx builder, the pptx builder and the png builder, and **not into the
pdf builder.** The pdf handoff block has no `sections` heading at all. Not empty, not
`(not present in this resolution)` — absent.

Nine doctypes have a pdf render target and no docx or pptx target, so for those nine the pdf
handoff is the only handoff that exists, and v0.2.0's headline feature still does not reach a
renderer for any of them. The brief's own statement of what was fixed — "Heading wording reaches
Word, PowerPoint, PDF and plain text" — is true for three of those four and false for PDF.

Two P1s follow, both of them the same defect class the P0 belonged to, still live on tables the
release did not touch: `cv-regions` still hides twelve of its fourteen columns on the control
family, and `page-formats` still hides `Fold Type` and `Panels mm`, which is the whole geometry of
a folded brochure.

Two further P2s are new. The pdf builder omits page flow as silently as it omits sections, on the
same families. And `ddi.py version` can never report a build stamp on a correctly built artefact,
because the writer and the reader disagree about which line the stamp goes on; that one is a
behaviour defect, not a version-string value, so the brief's carve-out does not reach it.

**The cleanest statement of the problem is the per-family judgement in section 3A.** Scoring each
family designed or generic, four of seven are designed and three are generic. Every family whose
primary format is pdf scores generic. No family on docx, pptx or png does. One builder accounts
for the entire difference.

---

## 2. How contamination was excluded, and the one thing that is green and means nothing

Every command was `python3 <abs>/scripts/ddi.py <sub> --data-dir <abs>/data`, with the absolute
path into `research/test-builds/v03-extracted/document-design-intelligence`. Passing `--data-dir`
explicitly on every invocation is deliberate: the shell's working directory moved three times
during this session, and cwd-relative resolution is exactly how the last pass ended up arguing
about a local build. No command in this pass could resolve against `skill/` even if cwd moved.

`ddi.py check` returns `OK: validated 14 table(s), 432 row(s)`. **That is reported here only to be
dismissed.** It would return exactly that if every payload column in the library were invisible to
every output path, because that is what it returned for v0.2.0, when they were. Row
well-formedness is not an output. Every finding below is a value read out of an actual handoff
block or an actual resolution, quoted verbatim.

---

## 3. Coverage

Families were pinned with `--doctype`, not `--query`, so that a ranking miss could not silently
remove a family from the pass. Routing was then exercised separately, as its own field, in D-F.
`--doctype` is itself new since my v0.2.0 pass, where only `--query` existed.

| Family | Format(s) exercised | Why this one |
|---|---|---|
| `cv-uk` | docx (+ pdf, pptx, png forced) | the control; a regression here is the worst finding available |
| `report-long-toc` | docx | only family with h1+h2+h3, TOC depth and page flow together |
| `slide-deck-projection` | pptx | D3's family; different layout model |
| `invoice-tabular` | pdf | pdf-only; D2's family |
| `quote-devis` | pdf | pdf-only, non-English (fr), the only French-keyword family run |
| `infographic` | png | png's only home in the whole library; new family |
| `brochure-trifold-a4` | pdf | closes the folded / large-format gap the last pass declared against itself |

Seven families times four formats is **28 handoff invocations, all exit 0, all non-empty, zero
bytes on stderr.** That uniformity is the reason section 4 exists: exit 0 and a populated-looking
block is precisely the failure shape this gate hunts.

`png` needed deciding before families were picked. `render-targets.csv` has exactly one png row,
`png-social`, and exactly one doctype references it — `infographic`. So png coverage and
infographic coverage are the same test, and there is no second png path to miss.

**Still not covered: 23 of 30 doctypes.** Nineteen duplicate a path exercised above and are named
in section 7. The genuinely untested paths are `form-handfilled`, the only hand-filled form and
also a pdf-only family, so D-A applies to it unverified; and `brochure-gatefold` and `poster`,
different fold and canvas geometry from the tri-fold but the same `page-formats` drop.

---

## 3A. PER-FAMILY SCORES

Fields are the brief's, kept separate: (1) refusals, (2) sections present and in documented order,
(3) each handoff value individually, (4) the plain-text path, (5) designed or generic.

**No checkmarks appear below.** Every cell is either a value read out of the block or the literal
word ABSENT. ABSENT means the block has no heading for that value at all; `(not present)` means the
block names the value and reports it empty, which is a different and much better outcome.

### Field 3 — the handoff values, per family, on its own primary format

| Value | `cv-uk` docx | `report-long-toc` docx | `slide-deck-projection` pptx | `invoice-tabular` pdf | `quote-devis` pdf | `brochure-trifold-a4` pdf | `infographic` png |
|---|---|---|---|---|---|---|---|
| page / canvas | 210x297mm -> 11906x16838 DXA | 210x297mm -> 11906x16838 DXA | LAYOUT_16x9 10in x 5.625in | 210mm 297mm | 210mm 297mm | 210mm 297mm + bleed 3mm, crop marks | 1080px x 1350px |
| margins | 25/25/25/25mm -> 1417 DXA each | 25/25/30/20mm -> 1417/1417/1701/1134 | n/a for slides, none emitted | 15/20/15/20mm | 15/20/15/20mm | 5/5/5/5mm | 18/18/14/14mm via page row |
| fonts | Arial / Arial / Arial | Times New Roman x3 | Arial / Arial / Arial | Public Sans, per engine x3 | Public Sans, per engine x3 | Source Sans 3 / Source Serif 4, x4 | Arial / Arial |
| heading levels | HEADING_1, HEADING_2 | HEADING_1, HEADING_2, HEADING_3 | ABSENT by design, no h-levels in pptx | `(not present)` — no h-role in `form-print` | `(not present)` — same | h1/h2/h3 -> `<h1>/<h2>/<h3>` | ABSENT — png block emits no h-element mapping |
| sizes | 11/16/24pt -> 22/32/48 half-pt | 11/12/16/24pt -> 22/24/32/48 | 24/18/36pt, projection | 11pt, 8.5pt | 11pt, 8.5pt | 11/12/16/24pt | 108/44/24/14pt -> 144/58.7/32/18.7px |
| palette | 4 roles; Accent omitted, `mono-ink` has none | 5 roles, #22282E..#1A1E22 | 5 roles + de-hashed form | 5 roles | 5 roles | 5 roles | 5 roles |
| page flow | `(not present)`, correct — no page-flow constraint in `ats-strict`/`cv-region` | 5 properties: keepNext, widowControl, cantSplit, tblHeader, keepNext | NOT APPLICABLE, with the reason stated | **ABSENT** though 5 page-flow constraints resolved — see D-J | **ABSENT**, same 5 constraints — see D-J | ABSENT; none resolved, so nothing lost | paged media NOT APPLICABLE, with the reason stated |
| **sections** | 8, with wording | 10, with wording | 7, with wording | **ABSENT — see D-A** | **ABSENT — see D-A** | **ABSENT — see D-A** | 3, with wording |
| constraints to preflight | ats-strict, cv-region | report-typography, print-legibility | projection | report-typography | report-typography | professional-print | screen |

### Fields 1, 2, 4 and 5, per family

**`cv-uk` — the control.** (1) No refusal; `Write me a UK CV` resolves at 7.2689, though
`Create a CV for an experienced software engineer, print it` still mis-resolves, see D-F. (2) All
eight sections of `cv-experienced` present, in the documented `Section Order`, wording attached:
`contact: Contact`, `summary: Summary`, `experience: Experience`, `education: Education`,
`skills: Skills`, `certifications: Certifications`, `projects: Projects`,
`publications: Publications`. (3) See table. (4) Plain text carries all 63 heading rows with
wording across three languages, `Heading Text: Contact`, `Heading Text: Coordonnées`,
`Heading Text: Kontakt`, and the full `Section Order`. (5) **Designed.** ATS-strict reasoning,
a single-column A4 at 25mm all round, a mono-ink palette with no accent — every choice is
defensible for an ATS-parsed CV and none of it is generic. **No regression against v0.2.0 on any
field**, which is the most important negative result in this pass.

**`report-long-toc`.** (1) No refusal, resolves at 20.483, the highest score of the fourteen
prompts. (2) All ten sections in documented order, `bibliography` correctly worded as
`References`. (3) See table — **this is the most complete block in the artefact**: the only one
with a populated page-flow section, the only docx with three heading levels, and the only family
that exercises `TOC Depth: 2` with `Front Matter Numbering: roman`. (4) Plain text carries 30
heading rows and all nine structure columns. (5) **Designed.** Times New Roman at 11/12/16/24pt,
asymmetric 30mm inside and 20mm outside margins for binding, roman front matter, widow control at
two lines. That is a specification, not a theme.

**`slide-deck-projection`.** (1) No `[NO MATCH]`, but `I need slides for Monday, projected in a
boardroom` abstains; the doctype-pinned run is what is scored here. (2) All seven `deck-standard`
sections in order, with wording. (3) See table. `charSpacing` reads `(not present in this
resolution)` and page flow reads NOT APPLICABLE **with its reason given**, which is the
explicitness D-A lacks. (4) Plain text carries 28 heading rows and the projection scale. (5)
**Designed, and this is the family that improved most.** 24pt body and 36pt h1 at
`Medium: projection`, a `deck-high-contrast` palette of #FFFFFF on #0F0F0F with a #FFD400 accent.
v0.2.0 handed this family 11pt print body text. It is now a projection deck.

**`invoice-tabular`.** (1) No refusal, resolves at 16.7634. (2) **ABSENT from the handoff.** The
seven `invoice-standard` sections are in the resolution and in the plain-text path in documented
order, and reach neither the pdf block nor, therefore, a renderer. (3) See table; sizes and
palette are the D2 fix landing. (4) Plain text carries all 21 heading rows with wording. (5)
**Generic, and the only family I score that way.** Not for lack of reasoning — `invoice-tabular`
reasoning, `form-grid-underline` style and the `form-print` scale are all resolved and sensible.
It scores generic because what is *handed over* is a bordered A4 page in Public Sans with five
colours and no section names, which describes any business document. The reasoning exists and does
not reach the deliverable.

**`quote-devis` — the non-English family.** (1) No refusal on any of the four French or German
prompts; `Fais-moi un devis client avec une ligne de prix` resolves at 14.3185,
`Rédige un devis` at 6.6381, `Erstelle ein Angebot mit Preisliste` at 8.935. **Zero refusals, and
the French path is the strongest of the three languages.** (2) ABSENT from the handoff, as for the
invoice, and additionally the sections it would have carried are an invoice's and in English — see
D-E. (3) See table; byte-identical to `invoice-tabular`. (4) Plain text carries 21 heading rows
including `Heading Text: Accroche` and `Heading Text: Kernbotschaft`, so the French and German
wording is authored, resolved, and visible to a human reading the text path. (5) **Generic.** A
French quote that is handed an English invoice's structure with no section names is a generic
document wearing the skill's name, and this is the family where that phrase is most literally true.

**`brochure-trifold-a4` — the folded path, first time exercised.** (1) No refusal;
`Turn this into a tri-fold A4 brochure` at 15.4946 and `Dépliant A4 trois volets` at 11.7671. (2)
ABSENT from the handoff; the five `brochure-3panel` sections are in the resolution in documented
order. (3) See table. Best print block in the artefact — bleed 3mm, crop and registration marks,
PDF/X-4 tier stated with its honest caveat — and simultaneously **no fold and no panel widths, see
D-C**, plus duplicated engine keys, see D-G. (4) Plain text carries 22 heading rows in three
languages. (5) **Generic, and the most consequential of the three.** The block describes a flat A4
sheet. A renderer following it produces a document that folds through its own body text. The
authored geometry that would have made it a brochure, `Panels mm: 99.5;99.5;98.0`, is in the CSV
and reaches nothing.

**`infographic` — the png path and the new family.** (1) No refusal;
`Build me an infographic summarising these statistics` at 8.9777,
`Make me a visual summary graphic for social` at 11.7595. (2) All three `infographic-canvas`
sections present with wording, in documented order. **v0.2.0 gave this family no section order at
all and printed a bare blank `Structure Key:` field; there is no blank field anywhere in this
output.** (3) See table — **the most complete of the four format blocks**, and the only one that
names the reason an inapplicable section is inapplicable and cites the data columns it read to
decide. (4) Plain text carries nine heading rows in three languages. (5) **Designed, and the
biggest single improvement in the release.** A 1080x1350 social canvas at 150 DPI, a 108pt lead
over 24pt body — a 4.5x ratio appropriate to a scroll-past graphic and to nothing else in the
library — and a red accent on near-black. v0.2.0 gave this family no typography, no colour and no
render command.

**Score summary: four designed, three generic. All three generic verdicts have the same cause**,
which is D-A. Every family whose primary format is pdf scores generic, and no family on docx, pptx
or png does. That correlation is the strongest single argument for the verdict in section 6.

---

## 4. DEFECTS RANKED

### D-A — P0 — The pdf handoff emits no section headings, so the release's P0 fix misses nine families

**Hits:** `invoice-tabular`, `quote-devis`, `brochure-trifold-a4` — three of the seven families
run — and by the same code path `form-handfilled`, `brochure-trifold-letter`,
`brochure-gatefold`, `brochure-flyer-letter`, `brochure-flyer-a4` and `poster`, which were not all
run. **Nine of thirty doctypes.**

**What the output said.** The complete pdf handoff for `quote-devis`, nothing elided:

```
HANDOFF (format=pdf)
  @page (native HTML -> Chromium/WeasyPrint pipeline):
    size: 210mm 297mm
    margin: 15mm 20mm 15mm 20mm  (top right bottom left)
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
    headless-chromium: /opt/google/chrome/chrome --headless --no-sandbox --disable-gpu --print-to-pdf=%o --no-pdf-header-footer %i
    weasyprint: weasyprint (module)
    wkhtmltopdf: wkhtmltopdf
  constraints to preflight (Set Keys): report-typography
next: python3 scripts/preflight.py <rendered-file>.pdf
```

There is no `sections` block. **Note what this is not: it is not an empty block.** The docx, pptx
and png blocks all announce themselves — `sections (Section Order, wording in Heading
Language=en):` — so a reader of a pdf block gets no signal that a section order was resolved at
all, and no signal that anything is missing.

**What it should have said.** The resolution behind that block carries the wording. For the same
family, `resolve --doctype quote-devis --json` returns 21 heading rows in three languages, fully
populated, for example:

```json
{"key": "headline-fr-1", "canonical_section": "headline", "Heading Text": "Accroche", "Language": "fr", "Is Primary": "yes"}
```

and `structures/invoice-standard` carries
`Section Order: issuer;bill-to;invoice-details;line-items;totals;tax;payment-terms`. The docx
builder, handed this identical JSON, produces the block correctly. So the data is present, the
helper exists and works, and only the pdf builder does not call it.

**Root cause, verified by reading the artefact's own source.** `scripts/ddi.py` defines
`_sections_lines` at line 359. It is called at exactly three sites:

```
513:    lines.extend(_sections_lines(resolved))     # _build_docx_lines
576:    lines.extend(_sections_lines(resolved))     # _build_pptx_lines
766:    lines.extend(_sections_lines(resolved))     # _build_png_lines
```

`_build_pdf_lines` spans lines 603 to 706 and contains no such call. Its section list is `@page`,
font-face stack, font sizes, heading elements, palette, render command, optional tier. The
in-function comment shows the D2 fix landing precisely here and citing its own brief:

```python
# research/brief-packaging-display-columns.md PART 4: this builder read only
# page_format_table, render_target_table and typeface_table -- never
# type_scale_table or palette_table, both of which docx and pptx DO read.
```

So the same builder was opened during this release cycle to add sizes and palette, and the section
wording was not added alongside them. **This is D2's asymmetry, not eliminated but narrowed from
three missing values to one.**

**Why this is P0 and not P1.** D2 was P1 because docx and pptx were unaffected, so most families
still received their type and colour by some path. That argument does not transfer. For the nine
families above there is no other path: `Render Target Keys` for `quote-devis` is `pdf-chromium`,
for `invoice-tabular` is `pdf-chromium`, and for all five brochures and `poster` is
`pdf-weasyprint-pdfx4;pdf-chromium`. A pdf-only family whose pdf handoff omits the headings has no
handoff that delivers them, which is the literal definition of the v0.2.0 P0, unchanged, for 30
percent of the shipped library. It is also the specific claim a v0.3 release note would make and
would be wrong about.

**Fix site.** `scripts/ddi.py`, function `_build_pdf_lines`. Real source, not generated. One
`lines.extend(_sections_lines(resolved))`, placed to match the other three builders' ordering —
they put it after the size and heading-level block and before the palette block. No data change
and no manifest change; `_sections_lines` already produces correct output for every family tested.

**How to confirm the fix.** Run `handoff --json quote-devis.json --format pdf` and grep for
`issuer:` followed by a word. Grepping for the string `sections` would pass on an empty block and
prove nothing; grep for a wording that only the `headings` table can supply.

**The decisive control.** Handing the *same* `quote-devis.json` to the docx builder produces the
block that the pdf builder omits:

```
  sections (Section Order, wording in Heading Language=en):
    issuer: From
    bill-to: Bill To
    invoice-details: Invoice Details
    line-items: Line Items
    totals: Total
    tax: Tax
    payment-terms: Payment Terms
```

Identical input, one builder delivers seven headings, the other delivers none. There is no
resolution-side explanation available.

**The one link in this chain that needed checking, and does not break it.** `SKILL.md` says PDF is
the exception, the format "this skill renders PDF itself", which raises the question of whether the
handoff block is even the pdf path — if some renderer inside the package read the resolution
directly, it could see `Heading Text` and D-A would be a P1 about an incomplete block rather than a
P0. **It cannot.** There is no PDF renderer in the artefact:

- `scripts/lib/pdf.py` is a stdlib-only PDF *reader*. Its public functions are `page_count`,
  `page_boxes`, `embedded_fonts` and `raster_dpi`, it is imported by exactly one module,
  `scripts/preflight.py`, and it contains no reference to `headings`, `Heading Text`,
  `Section Order`, a data directory or a resolution.
- Grepping the whole `scripts/` tree for `subprocess`, `weasyprint`, `--print-to-pdf`, `<html` or
  `<!DOCTYPE` returns one file, `build_zip.py`, and its only hit is the word "subprocess" inside a
  comment about not using one.
- `preflight.py` checks font embedding, page boxes and raster DPI. It has no heading check, so
  nothing downstream catches the omission either.

So "renders PDF itself" means the model authors the HTML from the handoff block and runs the render
command the block supplies. **The handoff block is the complete and only specification for a pdf
family, which makes it exactly as sole-source as the resolved JSON was for v0.2.0's P0.** The
argument I made about v0.2.0 — that the JSON was the entire universe the renderer saw — transfers
to the pdf block unchanged.

### D-B — P1 — `cv-regions` still hides twelve of fourteen columns, on the control family

**Hits:** all nine CV families. Exercised on `cv-uk`.

**What the output said.** Verbatim, the entire `cv-regions` payload of a resolved UK CV:

```json
"cv-regions": [
  {"key": "uk-early",       "Section Order": "contact;summary;education;experience;skills"},
  {"key": "uk-experienced", "Section Order": "contact;summary;experience;education;skills"}
]
```

**What it should have said.** `cv-regions.csv` has 14 columns. Twelve are absent from the
resolution: `region_key`, `Seniority Band`, `Max Pages`, `Photo`, `Date of Birth`, `Nationality`,
`Marital Status`, `Visa Status`, `Education Before Experience`, `Format`, `Language Expectation`,
`Evidence Class`. Two rows are returned with no `Seniority Band`, which is the only column that
distinguishes `uk-early` from `uk-experienced` other than the key itself. A consumer receives two
alternative section orders and nothing that says which one applies.

**Why this survived.** My v0.2.0 pass sorted D1 into Class A, no `display_columns` declared, and
Class B, declared but incomplete. v0.3 fixed four tables. Below is the measured result across all
seven families. It is identical for every family, so this table is the whole census.

| Table | v0.2.0 | v0.3 | Status |
|---|---|---|---|
| `headings` | key only | `Heading Text`, `Language`, `Is Primary`, `canonical_section` present | **FIXED** |
| `structures` | 3 of 9 | 9 of 9, including `TOC Depth` and `Heading Depth Max` | **FIXED** |
| `constraints` | 3 of 7 | 8 of 8, including `Applies To`, `Check`, `Threshold`, `Severity` | **FIXED** |
| `type-scales` | `Leading Ratio` hidden | 6 of 6, `Leading Ratio: 1.35` present | **FIXED** |
| `cv-regions` | 2 of 14 | **2 of 14** | unfixed |
| `doc-styles` | 4 of 15 | **4 of 15** | unfixed |
| `doc-reasoning` | 6 of 10 | **6 of 10** | unfixed |
| `typefaces` | 8 of 15 | **8 of 15** | unfixed |
| `palettes` | not measured | **8 of 20** | unfixed |
| `page-formats` | not measured | **10 of 21** | unfixed, see D-C |
| `render-targets` | not measured | **8 of 14** | unfixed |
| `doctypes` | not measured | **9 of 11** | unfixed |

The four tables the brief names as fixed are fixed, completely, and I could not break them. Eight
tables still drop payload. The `key` column is excluded from every count above: the resolver
renames each table's own `*_key` column to `key`, which is a rename and not a drop, and counting
it would have inflated every row of this table by one.

**The costliest drops among the unfixed eight**, judged by what a renderer or a reader cannot do
without them:

- `palettes` hides `On Primary`, `On Secondary`, `On Accent`, `Muted`, `On Muted`, `Text-Safe
  Roles`, `Fill-Only Roles` and `Category Marker Roles`. Every handoff block delivers
  `Primary: #22282E` with no companion foreground, so nothing in the output says what colour of
  text on a primary fill is legible. `Text-Safe Roles`, the column that exists to stop a fill-only
  colour being used for type, never reaches the consumer on any path or format.
- `typefaces` hides `Has Tabular Figures`. The `invoice-tabular` reasoning row calls for tabular
  figures by name in its own bias terms, and the column recording which faces have them is
  invisible to the family that needs it most.
- `doc-reasoning` hides `Anti-Pattern Tokens`, `Palette Bias Terms`, `Typeface Bias Terms`,
  `Doc Conditions` and `Severity`. The anti-patterns are the expert content, the "looks like AI"
  material the skill description advertises by name, and no output path carries them.
- `doc-styles` hides eleven columns including `Rule Hair pt`, `Table Rules`, `Table Fills`,
  `Emphasis Mechanism`, `Field Style` and `Not For`. A resolved style arrives as a display name
  and a "best for" sentence, with none of its actual specification.

**Fix site.** Unchanged from my v0.2.0 analysis and still correct: `research/build-manifest.py`,
which generates the schema manifest and states in its own comment that these declarations are
written there and never by hand. **Do not edit `data/schema-manifest.json`, in the artefact or in
the working tree.** For the tables carrying no declaration at all, the alternative fix site is the
computed default in `scripts/resolve.py`, function `_display_columns`.

**Why P1 and not P0.** Unlike D-A this does not empty a handoff block a renderer depends on. The
handoff builders read specific named columns and all of those are surfaced. It degrades the
plain-text and JSON answer a model reasons from, which is serious but recoverable, and it is the
continuation of a known defect rather than a new hole in a claimed fix.

### D-C — P1 — A tri-fold brochure handoff carries no fold and no panel widths

**Hits:** `brochure-trifold-a4`, run. Also `brochure-trifold-letter`, `brochure-gatefold`,
`brochure-flyer-letter` and `brochure-flyer-a4` by the same path.

**What the output said.** The page block of the tri-fold's pdf handoff, complete:

```
  @page (native HTML -> Chromium/WeasyPrint pipeline):
    size: 210mm 297mm
    margin: 5mm 5mm 5mm 5mm  (top right bottom left)
    bleed: 3mm
    marks: crop, registration
```

A flat A4 page with 5mm margins. Nothing in the block, and nothing in the resolution behind it,
distinguishes this from a single-sheet flyer.

**What it should have said.** The `a4-trifold` row of `page-formats.csv` carries the geometry,
authored and shipped:

```
a4-trifold,A4 - tri-fold brochure,"a4, trifold, tri-fold, brochure, leaflet, fold",210,297,3,5,5,5,5,5,88,1,none,none,tri-fold,99.5;99.5;98.0,120,professional,300,600
```

`Fold Type` is `tri-fold` and `Panels mm` is `99.5;99.5;98.0`, three unequal panels with the short
third being the standard allowance for the inward fold. `Measure mm` is `88`, the per-panel text
measure, and `Stock gsm` is `120`. **None of these reach any output path.** They are four of the
eleven `page-formats` columns in D-B's census, and there is no panel or fold block anywhere in the
pdf builder.

**Why this matters more than the other D-B drops.** For every other table the consumer loses
reasoning it could partly reconstruct. Here it loses the document's physical structure. A renderer
handed this block lays out one continuous A4 page, and the artefact then folds through its own body
text. The panel widths are the one value a tri-fold cannot be built without. A per-panel measure of
88mm against roughly 200mm of usable flat width is a 2.3-times difference in line length, which is
the exact quantity the `professional-print` constraint set exists to police.

**This closes the gap my last pass declared against itself.** No folded or large-format family was
exercised for v0.2.0, so I could not then say whether the path was unmodelled or actively wrong. It
is modelled, and modelled correctly, in the data. The modelling does not reach the output.

**Fix site, two changes, and they are separable.** Surfacing the columns is
`research/build-manifest.py`, as in D-B. Emitting them is a fold and panel block in
`_build_pdf_lines` in `scripts/ddi.py`, conditional on `Fold Type` being neither empty nor `none`.
That condition has real rows on both sides: `a3-poster` and `px-infographic-portrait` both carry
`Fold Type: none` with an empty `Panels mm`.

**How to confirm.** The pdf handoff for a resolved tri-fold must contain the string `99.5`.
Checking for a fold heading would pass on an empty block and prove nothing.

### D-D — P2 — `ddi.py version` can never report a build stamp, at any version

**This finding is not covered by the brief's version-string carve-out, and that distinction is the
finding.** The carve-out exempts the *value* `0.0.1-dev`, because CI rewrites it from the git tag.
This defect is in the code that reads the stamp, and rewriting the value does not move it to a
different line.

**What the output said**, run in the artefact:

```
VERSION: 0.0.1-dev
SKILL.md stamp: not yet stamped (no leading '<!-- version: ... -->' comment)
```

The artefact's SKILL.md is stamped. It is on line 5:

```
     1  ---
     2  name: document-design-intelligence
     3  description: "Creating any document type below is still this skill's job even as Wo...
     4  ---
     5  <!-- version: 0.0.1-dev (generated at build - do not edit) -->
```

**Root cause. The writer and the reader disagree, and the writer is right.**
`scripts/build_zip.py`, function `stamp_version` at line 147, inserts the stamp after the closing
`---` of the frontmatter, and the module docstring says why, explicitly:

```
  3. Stamp `<!-- version: X (generated at build - do not edit) -->` as the
     first line of SKILL.md's body, immediately after the closing `---` of
     the YAML frontmatter (never before it - claude.ai requires SKILL.md to
```

`scripts/ddi.py` line 869 reads the file's first line and requires it to start with
`<!-- version:`. Line 1 of a valid SKILL.md is `---`, so that test can never pass. **The two are
structurally contradictory. Any artefact built correctly reports "not yet stamped", and the only
artefact that would report a stamp is one that violates the frontmatter requirement claude.ai
imposes.** The released v0.3 will print this same line with `VERSION: 0.3.0` above it.

**Fix site.** `scripts/ddi.py`, the `version` subcommand around line 869. Search the file for the
first line matching a version-stamp pattern rather than testing line 1. `build_zip.py` already
compiles the right pattern at line 76 with the multiline flag set, so reusing that is the smaller
change. **Do not fix this by moving the stamp to line 1.** That breaks the frontmatter contract
`build_zip.py` documents, and it is the shape of tuning a constant to turn a check green, which
this project has refused before.

**Why P2.** Nothing about a rendered document is wrong. It misreports provenance to anyone
debugging which build they have, which is the situation this project spent most of today in.

### D-E — P2 — A French devis is handed an invoice's English structure

**Hits:** `quote-devis`. By the same mechanism, every non-English request in the library.

**What the output said.** `quote-devis` and `invoice-tabular` resolve to identical content apart
from the `doctypes` row: the same `structures/invoice-standard`, the same
`Section Order: issuer;bill-to;invoice-details;line-items;totals;tax;payment-terms`, the same
`form-print` scale at 11pt and 8.5pt, the same `a4-form-standard` page, the same `print-neutral`
palette, the same 21 heading rows. Their pdf handoff blocks differ by zero bytes. And every family
run, `quote-devis` included, reports:

```
  sections (Section Order, wording in Heading Language=en):
```

**What it should have said. Two separate defects share this row.**

First, the language. The resolution does carry French wording. The `headings` array contains
`{"Heading Text": "Accroche", "Language": "fr"}` and its siblings, 21 rows across `en`, `fr` and
`de`, so the data is present. The section block picks `en` because `structures.Heading Language`
says `en`. **All 18 rows of `structures.csv` say `en`.** There is no structure in the library from
which a non-English heading can be selected, so the French and German heading rows are
unreachable through the section block on every path and every format. That is **126 of the 204
authored heading rows** -- the split is 78 `en`, 63 `fr`, 63 `de` -- so nearly two thirds of the
table v0.2.0 was built around can only ever be read by a human scrolling the plain-text
resolution, and never selected by the block that hands headings to a renderer. A devis is handed
`issuer: From`, never `Émetteur`.

Second, the structure. A devis is not an invoice. It needs a validity period and an acceptance
signature, and `invoice-standard` has neither. `totals;tax;payment-terms` describes a bill for work
already done, not an offer for work proposed. `quote-devis` has no structure of its own.

**Fix site, stated as the two changes it is.** For the language, `Heading Language` is the wrong
place to decide this. It is a property of the structure, and structures are shared across
languages, so a French report and an English report cannot differ in it. The selection has to come
from the request, which means `_section_headings` in `scripts/ddi.py` needs a language input that
`resolve` supplies. **Tagged CONVENTION**: nothing in the artefact states where request language
should be detected, and I am not naming a detection mechanism I cannot point at a line for. For
the structure, a `quote-standard` row among `research/load-base.py`'s authored structures and a
repointed `Structure Key` on the `quote-devis` doctype.

**Why P2.** The output is a usable business document with the wrong section names in the wrong
language, not an empty one. It ranks below D-D only because D-D is a two-line fix and this is a
design decision someone has to make.

### D-F — P2 — A CV request resolves to a slide-deck handout, and a deck request abstains

**Unchanged from v0.2.0's D5. Neither fixed nor worsened.** Fourteen natural-language prompts, each
with `Use the document-design-intelligence skill.` appended, across English, French and German:
**zero `[NO MATCH]` refusals, twelve correct, one wrong family, one abstain.**

```
Create a CV for an experienced software engineer, print it.
  -> RESOLVED doctypes/slide-deck-handout  (method=bm25, top_score=4.2437)

I need slides for Monday, projected in a boardroom.
  -> [ABSTAIN] no confident match
```

These are the same two prompts that failed the same two ways against v0.2.0. `Write me a UK CV`
resolves at 7.2689 and `Erstelle einen britischen Lebenslauf` at 3.8415, so the German path works
but sits close to the abstain floor. French prompts were the strongest of the three:
`Fais-moi un devis client avec une ligne de prix` at 14.3185 and `Dépliant A4 trois volets` at
11.7671, both correct.

Recorded, not re-diagnosed. The brief closes routing to this pass, and a wrong family from a scorer
is a different class of problem from a builder that drops a value it was handed.

### D-G — P3 — Duplicate engine keys with conflicting commands in the brochure pdf handoff

**What the output said**, tri-fold pdf, verbatim:

```
  font-face stack (embed vs. safe-stack per render target's Font Rule):
    weasyprint (embed): Source Sans 3 / Source Serif 4
    headless-chromium (embed): Source Sans 3 / Source Serif 4
    weasyprint (embed): Source Sans 3 / Source Serif 4
    wkhtmltopdf (embed): Source Sans 3 / Source Serif 4
  render command:
    weasyprint: weasyprint (module) --pdf-variant=pdf/x-4 --output-intent=srgb
    headless-chromium: /opt/google/chrome/chrome --headless --no-sandbox --disable-gpu --print-to-pdf=%o --no-pdf-header-footer %i
    weasyprint: weasyprint (module)
    wkhtmltopdf: wkhtmltopdf
```

`weasyprint` appears twice with two different commands. The family declares
`pdf-weasyprint-pdfx4;pdf-chromium`, both entries expand their fallback chains, and
`pdf-weasyprint-pdfx4` and `pdf-weasyprint` both report `Engine: weasyprint`. A consumer keying on
the engine name gets the PDF/X-4 invocation or the plain one depending on whether it takes the
first match or the last.

**Why P3 and not higher.** The PDF/X-4 command is listed first and is the correct choice, so
first-wins yields the right answer, and the `tier:` line below the block states the PDF/X-4 intent
unambiguously. This is a latent ambiguity, not a wrong value.

**Fix site.** `_build_pdf_lines` in `scripts/ddi.py`: key the loop on the render key rather than on
`Engine`, or de-duplicate on engine while keeping the highest `Print Tier Max`. The render key is
one of the `render-targets` columns D-B shows is currently hidden, so surfacing it serves both
findings.

### D-H — P3 — Six type-scale rows and two constraint sets are still unreachable

**Improved, not closed.** Re-running the reachability difference against the artefact:

| Check | v0.2.0 | v0.3 |
|---|---|---|
| unreachable type-scale rows | 9 of 20 | **6 of 24** |
| unreachable scale keys | `deck-projection`, `print-office-generic` | **`print-office-generic`** |
| unreachable constraint sets | `font-safety`, `redesign` | **`font-safety`, `redesign`** |
| unreachable structures | not measured | none |
| unreachable cv-region keys | not measured | none |
| canonical sections with no heading row | not measured | none |
| heading sections no structure uses | not measured | `volunteering` |

`deck-projection` became reachable as a consequence of the D3 fix, which is the reachability
half of that fix landing. `print-office-generic`'s six rows remain referenced by no typeface, and
`font-safety` and `redesign` remain referenced by no doctype's `Constraint Set Keys`. Every one of
the 52 canonical heading sections now has at least one heading row, and every structure and every
region is reachable. Those three results are new and are good.

**Fix site.** A reachability assertion in `scripts/validate_data.py`, which today validates form
and not reachability, plus a decision in `research/load-base.py` about whether the orphan rows
should be referenced or removed. `ddi.py check` reporting 432 rows valid while six of them can
never be selected is the specific way a green gate overstates the library.

### D-I — P3 — The description is 13 characters from the hard upload limit

**Passes, and is recorded because it passes narrowly.** `build_zip.py` checks the SKILL.md
description against a 1,024-character upload limit, at line 249, with the test
`desc_len < 1024`. Measured in `python3`, because `wc -m` returns bytes in this environment and
the description contains non-ASCII:

| Measure | Value |
|---|---|
| description characters | 1010 |
| description bytes | 1013 |
| limit | under 1024 |
| max passing length | 1023 |
| headroom | **13 characters** |

At v0.2.0 the same description was 972 characters with 51 characters of headroom. Fix 5 spent 38
of those 51 adding `infographic`, `infographie` and `Infografik` plus the surrounding phrasing.
**The next keyword addition in any language will fail the build**, and it will fail at packaging
time rather than at authoring time, which is the expensive place to find out.

**The mirror is consistent, which is worth stating because it could have drifted.**
`references/activation.md` reproduces the description verbatim — byte-for-byte, checked — and its
own length caption reads 1010 characters, matching the measurement above. A description edit that
missed either the mirror or the caption would have shipped an inconsistency; this one did not.

**Not a defect in this artefact.** No behaviour is wrong and the gate is honest about the number.
It is recorded so that the next person to add a trigger word knows the budget is 14 characters and
plans a removal alongside the addition. The gate is `desc_len < 1024`, so 1023 is the longest
string that passes and 13 is the exact remaining budget.

**Fix site if one is wanted.** Nothing to fix now. If headroom is wanted, the description's
redundant keyword pairs are the place to find it, in the SKILL.md source under
`skill/document-design-intelligence/`, never in the extracted artefact.

### D-J — P2 — The pdf handoff also omits page flow, silently, where the constraints resolved

_Found after D-I was written and filed here to keep the numbering stable. Its rank is P2, between
D-F and D-G; section 6's table is the authoritative ordering._

**Hits:** `invoice-tabular` and `quote-devis`, run. Any pdf family whose constraint sets carry
page-flow rules.

**Same builder and same silence as D-A, different value, lower cost.** Filed separately because the
severity is different and so is the correct fix.

**What the output said.** Nothing. The pdf block has no page-flow heading of any kind. Compare the
other three builders, all of which address it:

```
docx (report-long-toc), populated:
  page flow (OOXML paragraph/table properties, mapped from each constraint's own Parameter column ...):
    keepNext: heading bound to body-paragraph  [report-heading-keep-with-next]
    widowControl: body-paragraph, min_lines_together=2  [report-widow-orphan-control]
    cantSplit: table-row  [report-table-row-no-split]
    tblHeader: table-header-row  [report-table-header-repeat]
    keepNext: figure bound to caption-block  [report-figure-caption-keep-together]

docx (cv-uk), correctly empty and says so:
  page flow (...):
    (not present in this resolution)

pptx, correctly inapplicable and says why:
  page flow: NOT APPLICABLE -- slides do not paginate, so docx's page-flow properties have no pptx equivalent

pdf:
  <no such block>
```

**What it should have said.** `quote-devis` resolves the identical five page-flow constraints that
`report-long-toc` does, because both carry the `report-typography` set:

```
report-heading-keep-with-next        Parameter: docx_property=keepNext;applies_to_block=heading;binds_to=body-paragraph
report-widow-orphan-control          Parameter: docx_property=widowControl;min_lines_together=2
report-table-row-no-split            Parameter: docx_property=cantSplit;applies_to_block=table-row
report-table-header-repeat           Parameter: docx_property=tblHeader;applies_to_block=table-header-row
report-figure-caption-keep-together  Parameter: docx_property=keepNext;applies_to_block=figure;binds_to=caption-block
```

Every one has a CSS paged-media equivalent that the target engines support: `widows: 2` and
`orphans: 2`, `break-after: avoid` for the heading binding, `break-inside: avoid` for the table
row, and `display: table-header-group` for the repeating header. A pdf-only invoice that spans two
pages will split a table row and orphan a heading, and nothing in the handoff told the renderer not
to.

**There is a real reason the pdf builder skipped this, and it is not an excuse.** The `Parameter`
column is authored in docx vocabulary — every value literally begins `docx_property=`. The docx
builder can pass it through; the pdf builder would have to translate it. That is a genuine design
question, which is exactly why the pptx builder's answer is the right pattern: state the value, or
state that it is not applicable and why. **Emitting nothing is the only option that leaves a
renderer unable to tell the difference between "no rules apply" and "rules apply and were not
delivered".**

**Why P2 and not part of D-A.** D-A removes the document's section names, which no renderer can
invent. This removes pagination hints, which a competent renderer partly gets right by default, and
the underlying data is genuinely docx-shaped. It is a real gap in the deliverable, not a hole in a
claimed fix.

**Fix site.** `_build_pdf_lines` in `scripts/ddi.py`. The minimum honest fix is a one-line
NOT APPLICABLE statement in the pptx builder's style, naming the docx-vocabulary reason. The full
fix is a `docx_property` to CSS mapping, which is new design work and **tagged CONVENTION** —
nothing in the artefact states a mapping, and I am not naming one as sourced.

---

## 5. The five claimed fixes, confirmed independently

Each was verified from the artefact alone. A fix I could not demonstrate is marked as such.

**1. The P0 — heading wording reaches Word, PowerPoint, PDF and plain text; hidden columns on
constraints, structures and type-scales surfaced. PARTIALLY CONFIRMED.**

Word: confirmed. `cv-uk` docx carries `contact: Contact`, `summary: Summary`,
`experience: Experience` and five more. PowerPoint: confirmed, `slide-deck-projection` pptx carries
`cover: Cover Page`, `agenda: Agenda` and five more. Plain text: confirmed, the text resolution
prints `Heading Text: Contact`, `Heading Text: Coordonnées`, `Heading Text: Kontakt` for all 63
`cv-uk` heading rows. **PDF: refuted. See D-A.** The three named tables are surfaced completely:
`constraints` now carries `Applies To`, `Check`, `Element Scope`, `Parameter`, `Threshold` and
`Severity`; `structures` carries all nine columns including `TOC Depth: 2` and
`Heading Depth Max: 3` on `report-long-toc`; `type-scales` carries `Leading Ratio: 1.35`.

**2. The PDF handoff gained sizes, heading levels and palette. CONFIRMED.**

The invoice pdf block that emitted none of these for v0.2.0 now emits `body: 11pt`,
`legal: 8.5pt`, and `Primary: #22282E` through `Foreground: #1A1E22`. The heading-elements block
populates where roles exist: the tri-fold brochure, on the `report-print` scale, gets
`h1 -> <h1>`, `h2 -> <h2>`, `h3 -> <h3>`. On the invoice it reads
`(not present in this resolution)`, which is correct rather than defective — `form-print` has only
`body` and `legal` roles, so there is no h-role to map, and the block says so rather than staying
silent. That explicitness is exactly what D-A's missing `sections` block does not do.

**3. A projected deck gets its own type scale. CONFIRMED, and fixed the right way.**

`slide-deck-projection` now resolves `typefaces/safe-sans-deck` with `Scale Key: deck-projection`,
and the pptx handoff reads `body: 24pt`, `body-dense: 18pt`, `h1: 36pt`, with every resolved
type-scale row carrying `Medium: projection`. **The lazy fix was avoided.** My last pass warned
specifically against repointing `safe-sans-arial`'s scale, because the CV needs `cv-print`. A new
typeface row was added instead. The control confirms it: `cv-uk` still resolves
`typefaces/safe-sans-arial` with `Scale Key: cv-print` and still gets `body: 11pt`, `h2: 16pt`,
`h1: 24pt` at `Medium: print`. **No regression on the control family, on this or anything else I
measured.**

**4. The png handoff builder exists and `--format png` is accepted. CONFIRMED, and it is a real
block, not an accepted flag.**

`--format png` exiting 0 would be an activation result and is not what is reported here. The png
block for `infographic` carries, individually: canvas `1080px x 1350px` parsed from the render
target's own window-size flag; `font-face headless-chromium (embed): Arial / Arial`; four sizes
converted to px, `lead: 108pt -> 144.0px`, `h1: 44pt -> 58.7px`, `body: 24pt -> 32.0px`,
`caption: 14pt -> 18.7px`; the three sections with wording, `headline: Headline`,
`key-points: Key Points`, `call-to-action: Call to Action`; the full five-role palette; and the
screenshot render command. Paged media is reported as `NOT APPLICABLE` with the reason given from
the render target's own columns. **This is the most complete of the four format blocks**, and it is
the only one of the four that names why an inapplicable section is inapplicable.

**5. `infographic` is a real family and the description names it in three languages. CONFIRMED.**

`infographic` now resolves `structures/infographic-canvas` with
`Section Order: headline;key-points;call-to-action`, `typefaces/safe-sans-infographic`,
`type-scales/infographic-screen` at 108/44/24/14pt, and `palettes/brand-accent-print`. **D4 is
fixed on both halves**: there is no bare `Structure Key:` field anywhere in the output, and the
handoff has both fonts and a render command. The description names `infographic`, `infographie` and
`Infografik`.

**One documentation defect follows from fix 5 and should not ship with it.** `SKILL.md` still
says, under "Section-order guidance", that `infographic` "has no Structure Key and so gets no
section order — the resolver says so explicitly rather than returning an empty list". That was true
of v0.2.0 and is false of this artefact: `doctypes.csv` gives `infographic` the
`infographic-canvas` structure and the resolver returns three sections with wording. `SKILL.md` is
the router the model reads first, so it now describes a behaviour the code no longer has. Fix in
the `SKILL.md` source under `skill/document-design-intelligence/`, not in the extracted artefact.

---

## 6. VERDICT

**DO NOT SHIP.**

The gate turns on one finding. D-A means the sentence a v0.3 release note would lead with —
heading wording now reaches Word, PowerPoint, PDF and plain text — is false for PDF, and false for
the nine of thirty families that have no other handoff format. That is the v0.2.0 P0, unmodified,
for 30 percent of the library, in a release whose stated purpose was to fix it.

The per-family scores make the same point without reference to any release note: three of seven
families score generic rather than designed, all three are the pdf families, and all three score
that way for this one reason.

It is also the cheapest defect in this report to fix: one `lines.extend(_sections_lines(resolved))`
in `_build_pdf_lines`, matching three existing call sites, with no data change, no manifest change
and no new helper. **Ship-blocking and small are not in tension here.** The argument for tagging
anyway would be that four fixes are real and the fifth is three-quarters done; the argument against
is that the remaining quarter is the release's headline claim, and shipping it would put a false
statement in the release notes about the exact defect the release exists to close.

**Ranked worst first:**

| # | Defect | Sev | Ship-blocking |
|---|---|---|---|
| D-A | pdf handoff emits no section headings; 9 of 30 families have no other format | P0 | **yes** |
| D-B | `cv-regions` hides 12 of 14 columns; 8 tables still drop payload | P1 | no |
| D-C | tri-fold brochure handoff carries no `Fold Type` and no `Panels mm` | P1 | no |
| D-D | `ddi.py version` can never report a stamp on a correctly built artefact | P2 | no |
| D-E | French devis gets an invoice's sections, in English; no structure allows non-English | P2 | no |
| D-F | one prompt resolves to the wrong family, one abstains; unchanged from v0.2.0 | P2 | no |
| D-J | pdf handoff omits page flow silently where the constraints resolved | P2 | no |
| D-G | duplicate `weasyprint` engine keys with conflicting commands | P3 | no |
| D-H | 6 type-scale rows and 2 constraint sets unreachable | P3 | no |
| D-I | description is 13 characters from the 1,024-char upload limit | P3 | no |

Plus the `SKILL.md` infographic paragraph in section 5, which is a documentation correction rather
than a numbered defect.

**Recommendation.** Fix D-A, re-run the three pdf-only families in this pass and assert
`issuer: From` appears in the pdf block, then tag. D-B through D-H are all legitimate v0.4 work; D-C
is the one I would most want in v0.4, because it is the difference between a tri-fold brochure and
a sheet of A4 that folds through its own text.

**Confidence.** High on D-A, and it is the finding I tried hardest to break. The defect is a
missing call at a known line; the three sibling call sites are quoted from the artefact's own
source; the docx builder producing the block from the identical JSON rules out any resolution-side
cause; and the one alternative explanation available — that `SKILL.md`'s "this skill renders PDF
itself" implies a second route from the resolution to a rendered file — was checked and refuted,
because `scripts/lib/pdf.py` is a reader used only by `preflight.py` and there is no renderer in
the package at all. High on D-B, D-C, D-D, D-F and D-H, all of which
are direct reads of artefact output or artefact source. Medium on D-E, where the observation is
certain but the right fix is a design decision I am not authorised to make and have tagged
CONVENTION. Medium on D-G, where I have not read a consumer that would be confused by the duplicate.

---

## 7. What this pass did not cover, and what that leaves open

**23 of 30 doctypes were not resolved.** Nineteen duplicate an exercised path and running them
would restate one finding many times: `cv-us`, `cv-eu-generic`, `cv-eu-europass`, `cv-dach`,
`cv-france`, `cv-gulf-gcc`, `cv-generic` and `cv-academic` duplicate `cv-uk` and inherit D-B
identically; `report-short`, `whitepaper` and `proposal` duplicate `report-long-toc`;
`slide-deck-document` and `slide-deck-handout` duplicate the deck path;
`brochure-trifold-letter`, `brochure-flyer-letter`, `brochure-flyer-a4` and `brochure-gatefold`
duplicate the tri-fold and inherit D-A and D-C; `cover-letter`, `letter-formal`, `memo-internal`
and `one-pager` are correspondence paths on docx.

**The four real gaps, stated as gaps and not as findings:**

- `form-handfilled` is the only hand-filled form and is pdf-only, so D-A applies to it by code
  path but I did not run it. Its `form-standard` structure and `form-print` scale are shared with
  the invoice, so the gap is narrow.
- `poster` and `brochure-gatefold` have different canvas and fold geometry from the tri-fold.
  `a3-poster` carries `Fold Type: none`, so D-C's conditional fix has a real negative case there,
  but I did not resolve either family to confirm the block that results.
- **No document was rendered and no `preflight` was run on a real artefact.** Every finding here
  is about what the handoff block says, which is the brief's scope, but it means I cannot say
  whether a renderer handed a correct block produces a correct file. Worth noting for whoever
  does render: `preflight.py` checks font embedding, page boxes and raster DPI, and has no heading
  or section check, so it would pass a pdf built from a block missing its sections.
- Brand-kit paths were not touched: `make_brand_kit.py`, `merge_brand_kit.py` and
  `--brand` on `resolve` were not exercised at all.

**One thing I deliberately did not do.** I did not verify the artefact's byte identity to what will
be published, because no git operation is available to me and the orchestrator owns git. I relied
on the provenance the brief supplied as already verified. Every finding above is a read of the
extracted artefact's own files and output, so if that provenance holds, these findings are findings
about the release.

---

## 8. Method notes worth carrying to the next pass

**The census beat the spot check, and the brief's own summary would have hidden the gap.** The
brief named three tables as surfaced. Checking those three would have passed. Diffing every
resolved table's key set against its CSV header, for all seven families, is what turned up the
eight tables that still drop payload and the `page-formats` drop behind D-C. The census cost one
script and found two of the eight defects.

**Comparing the four format builders against each other found the P0.** D-A is invisible if you
read the pdf block on its own: it looks complete, every section it has is populated, and it exits
0. It is obvious the moment you put the docx block next to it and notice one heading is missing
from one of them. The generalisation: when a feature has N implementations, diff the
implementations, do not test each in isolation.

**Absence of a block is worse than an empty block, and the artefact shows both.** The pdf builder
prints `heading elements: (not present in this resolution)` where an invoice has no h-roles. That
is good behaviour. It prints nothing at all where the sections belong. A reader can act on the
first and cannot notice the second, so "does the output name what it is not giving you" is worth
scoring as its own field next time.

**`--doctype` changes how this pass should be run.** It did not exist for v0.2.0, and pinning
families with it separates output quality from ranking cleanly, which is what the brief asks for.
Routing can then be exercised as its own field with real queries, as in D-F, instead of
contaminating every family's result.
