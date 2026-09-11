# 51 — INVOKED-QUALITY PASS on published v0.2.0

Run 2026-09-11 by the Coverage and Gap Analyst, per `research/brief-coverage-invoked-quality.md`.
Scores OUTPUT QUALITY when the skill runs. Activation and routing are out of scope and are not
mentioned again below.

**Headline: zero refusals, a docx handoff that works, and a P0 that empties the v0.2.0 release
of its headline feature.** The 204 heading rows — the whole of what v0.2.0 added — reach every
output path as bare row ids with no wording attached, and `handoff` cannot recover them because
the resolved JSON is its only input. Seven more tables lose their payload columns the same way.
Two P1s follow: the pdf handoff emits no point sizes and no palette at all, and a projected deck
is handed the CV's 11pt print type scale.

---

## 1. Which asset was exercised, and how it was proved to be the published one

Exercised: `skill/dist/document-design-intelligence-0.0.1-dev.zip`, md5
`68276653bea670092d5adc860de2eb06`, extracted to a scratch directory and run from there so no
working copy could contaminate a result. Every command below was run with
`PYTHONIOENCODING=utf-8` so that console mojibake could not be mistaken for a data defect.

This is a local artefact and I did not download the published release myself. **That gap is now
closed by someone else's work and the results here stand as findings about the shipped product,
not about a dev build.** The sub-manager downloaded the real published v0.2.0
(`gh release download v0.2.0 --repo Magazem/Smart-design`) and re-ran D1's checks against it;
`research/53-defect-verification.md` records that it reproduces exactly — 63 heading entries
whose keys union to `["key"]`, zero heading wordings in the docx handoff, bare ids on the
plain-text path, and an identical hidden-column census.

Two files did differ by md5 between this local build and the published asset, and both
differences are cosmetic: `data/schema-manifest.json` diffs empty after JSON normalisation, and
`scripts/ddi.py` is byte-identical after stripping CR, the local copy carrying exactly 690 extra
CR bytes for its 690 lines. `scripts/resolve.py` and `data/base/headings.csv` were already
md5-identical, which matters because those are the two files D1 depends on.

**Method worth carrying forward, and it is a correction to what I did.** I treated six matching
reference values as sufficient identity evidence. They are not, for this class of defect: five
row counts and a description length cannot detect a difference in `resolve.py`, `ddi.py` or the
manifest, and D1 lives in exactly those three. My local results were sound, but nothing I checked
could have shown them sound. When the defect is in behaviour, match the behaviour files rather
than the row counts.

The reference values did all match, and are recorded here for completeness:

| Reference value | Brief | Measured |
|---|---|---|
| description length | 972 chars | 972 |
| description opening | "Creating any document type below" | "Creating any document type below is still this skill's job e…" |
| constraints rows | 47 | 47 |
| type-scales rows | 20 | 20 |
| headings rows | 204 | 204 |
| structures rows | 17 | 17 |
| doctypes rows | 30 | 30 |
| tables carrying `display_columns` | 6 | 6 — palettes, typefaces, type-scales, page-formats, render-targets, constraints |

One discrepancy that is not a content mismatch but should not go unrecorded: the asset's
`VERSION` file reads `0.0.1-dev`, not `0.2.0`. See D7.

---

## 2. Family selection

Six families, one per distinct output path, two phrasings each — one keyword-faithful and one
natural — for eleven prompts in total.

| Family | Path it represents | Why this one |
|---|---|---|
| `cv-uk` | CV control, docx | The best-exercised path. If this is weak everything is. |
| `report-long-toc` | multi-heading-tier print, docx | The only family exercising h1+h2+h3 and the page-flow properties together. |
| `slide-deck-projection` | pptx, non-paginating layout model | Different layout model, different handoff branch, no page-formats row. |
| `invoice-tabular` | short artefact, pdf | Tabular structure model rather than a prose section model. |
| `quote-devis` (French prompts) | non-English, pdf | Doubles the short-artefact path and is the only family exercising the fr heading rows. |
| `infographic` | documented no-structure family | Directly tests the ruled "no X guidance for Y" empty-value path, which is the exact defect shape this pass hunts. |

Between them these cover all five paths the brief requires, plus the empty-value path.

**Not run — 24 of the 30 doc keys**, each against the path it duplicates:

- `cv-us`, `cv-eu-generic`, `cv-eu-europass`, `cv-dach`, `cv-france`, `cv-gulf-gcc`,
  `cv-generic`, `cv-academic` — duplicate the `cv-uk` path. They differ only in the
  `cv-regions` row pulled in, and D1 shows that row's payload is invisible for all of them
  equally, so running eight more would restate one finding eight times.
- `report-short`, `whitepaper`, `proposal` — duplicate the `report-long-toc` path with a
  shorter section order.
- `slide-deck-document`, `slide-deck-handout` — duplicate the deck path with a different
  medium; note that D3 predicts they are the two decks that should have got a print scale.
- `brochure-trifold-letter`, `brochure-trifold-a4`, `brochure-gatefold`,
  `brochure-flyer-letter`, `brochure-flyer-a4`, `poster`, `one-pager` — panel/poster layout.
  **This is the real gap in this pass**: no folded or large-format family was exercised at all,
  and panel adjacency is a documented v0.2.0 non-feature, so I cannot say whether the path is
  merely unmodelled or actively wrong.
- `cover-letter`, `letter-formal`, `memo-internal`, `form-handfilled` — correspondence and
  hand-filled form. `form-handfilled` shares the `form-print` scale and `form-grid-underline`
  style with `invoice-tabular`, so the second real gap here is narrow.

---

## 3. Per-family scores

Fields, per the brief: (1) no refusal, (2) sections present and in documented order, (3) handoff
values individually, (4) plain-text path keeps the section model, (5) designed or generic.

### 3.1 `cv-uk` — the control

**(1) No refusal.** No `[NO MATCH]` on either phrasing. But `"Create a CV for an experienced
software engineer, print it"` did not resolve:

```
[ABSTAIN] no confident match for "Create a CV for an experienced software engineer, print it"
  top candidates -- ask the user which one they meant:
    'slide-deck-handout' "Slide deck -- handout / leave-behind (print-dense)"  score=2.7711
    'cv-uk' "CV -- UK"  score=2.4776
    'poster' "Poster"  score=2.474
```

This is not a refusal — the string the brief names as P0 never appears — but it is the control
family declining to answer a plain request, and a CV losing to a slide-deck handout is a ranking
result worth recording. `"Write me a UK CV"` resolved cleanly at `top_score=7.2689`. Filed as D5.

**(2) Sections.** Expected, from `structures/cv-experienced`:
`contact;summary;experience;education;skills;certifications;projects;publications`.
Produced, verbatim:

```
  structures/cv-experienced
    Display Name: CV -- experienced hire
    Section Order: contact;summary;experience;education;skills;certifications;projects;publications
```

Eight sections, same eight, same order. **PASS** — this is the one field that is unambiguously
healthy across every family.

**(3) Handoff, docx, value by value.** All present:

| Value | Present? | What it said |
|---|---|---|
| page size | yes | `Trim W mm: 210mm -> Width DXA: 11906`, `Trim H mm: 297mm -> Height DXA: 16838` |
| margins | yes | all four at 25mm -> 1417 DXA |
| fonts | yes | Heading / Body / Safe Stack Fallback all `Arial` |
| heading levels | yes | `h1 -> HeadingLevel.HEADING_1`, `h2 -> HeadingLevel.HEADING_2` |
| point sizes | yes | body 11pt -> 22.0 half-points, h2 16pt -> 32.0, h1 24pt -> 48.0 |
| palette | yes | Primary `#1A1A1A`, Secondary `#4A4A4A`, Background `#FFFFFF`, Foreground `#111111` |
| page flow | **no** | `(not present in this resolution)` |

Two absences, and they are different things. No h3 is deliberate and correct for cv-print; not
filed, per the brief. **No Accent is also correct** — I checked the source rather than assuming:
`palettes/mono-ink` carries `"Accent": ""` in the data, so the handoff is honestly reporting an
authored blank, not dropping a value. Page flow is absent because cv-uk's constraint sets are
`ats-strict;cv-region` and every page-flow row lives in `report-typography`. That is a data
scoping question, not an empty-block defect, and I am not filing it.

**(4) Plain-text path.** The section order survives — see (2). The heading wording does not. 63
heading rows print as this and nothing else:

```
  headings/contact-en-1
  headings/contact-en-2
  headings/contact-en-3
  ...
  headings/publications-de-1
```

**(5) Designed or generic.** Genuinely designed at the style layer: ATS reasoning selects a
restrained single-column style, a monochrome palette and a safe-stack Arial, and five ats-strict
constraints come along. Generic at the payload layer, and the loss is specific. A UK CV pulls two
`cv-regions` rows, and this is all that is printed of them:

```
  cv-regions/uk-early
    Section Order: contact;summary;education;experience;skills
  cv-regions/uk-experienced
    Section Order: contact;summary;experience;education;skills
```

`cv-regions.csv` has fourteen columns. Twelve are dropped, including `Max Pages`, `Photo`, `Date
of Birth`, `Nationality`, `Marital Status`, `Visa Status` and `Language Expectation` — which are
precisely what distinguishes a UK CV from a DACH Lebenslauf. The output shows a region was
consulted and then says nothing about what the region requires.

### 3.2 `report-long-toc` — multi-tier print

**(1) No refusal.** Both phrasings resolved. `"Write a long report with a table of contents"` at
`top_score=17.6703`, `"I need a 40-page annual report for our board"` at `7.5156`, both to
`report-long-toc`. Strongest resolution of the pass.

**(2) Sections.** Expected and produced are identical, ten sections:
`cover;table-of-contents;executive-summary;introduction;methodology;findings;conclusion;recommendations;appendices;bibliography`.
**PASS.** Note `table-of-contents` is present as a section, which is Ruling N landing.

**(3) Handoff, docx.** This is the healthiest block in the pass and deserves to be recorded as
working, since ruling M's fix is what is being checked:

```
  page (docx-js DXA; 1 mm = 56.6929 DXA, 1 pt = 20 DXA -- research/23 docx:25):
    Trim W mm: 210mm  ->  Width DXA: 11906
    Trim H mm: 297mm  ->  Height DXA: 16838
    Margin Top mm: 25mm  ->  Margin Top DXA: 1417
    Margin Bottom mm: 25mm  ->  Margin Bottom DXA: 1417
    Margin Inside mm: 30mm  ->  Margin Inside DXA: 1701
    Margin Outside mm: 20mm  ->  Margin Outside DXA: 1134
  fonts:
    Heading Family: Times New Roman
    Body Family: Times New Roman
    Safe Stack Fallback: Times New Roman
  font sizes (docx-js half-points ...):
    body: 11pt  ->  22.0 half-points
    h3: 12pt  ->  24.0 half-points
    h2: 16pt  ->  32.0 half-points
    h1: 24pt  ->  48.0 half-points
  TOC heading levels (docx-js HeadingLevel.* -- research/23 docx:33):
    h1  ->  HeadingLevel.HEADING_1
    h2  ->  HeadingLevel.HEADING_2
    h3  ->  HeadingLevel.HEADING_3
  palette (hex as stored ...):
    Primary: #22282E
    Secondary: #55606B
    Accent: #2E5C82
    Background: #FFFFFF
    Foreground: #1A1E22
  page flow (OOXML paragraph/table properties, mapped from each constraint's own Parameter column
  -- convention, not sourced to any authority this library cites):
    keepNext: heading bound to body-paragraph  [report-heading-keep-with-next]
    widowControl: body-paragraph, min_lines_together=2  [report-widow-orphan-control]
    cantSplit: table-row  [report-table-row-no-split]
    tblHeader: table-header-row  [report-table-header-repeat]
    keepNext: figure bound to caption-block  [report-figure-caption-keep-together]
  constraints to preflight (Set Keys): report-typography, print-legibility
```

Every one of the seven values the brief asks about is populated. Asymmetric margins (30mm inside,
20mm outside) survive the conversion correctly and separately, which is the check that would fail
if the block were being filled from a default. All five page-flow properties are present with the
constraint key that produced each — this is the v0.2.0 page-flow feature working end to end. The
block's own header says the mapping is convention and not sourced to any authority the library
cites, which is the correct attribution and matches what I could grep.

**(4) Plain-text path.** Section order survives, heading wording does not — 30 heading rows,
bare ids, same as cv-uk.

**(5) Designed or generic.** Designed. Compared against `cv-uk` the divergence is real and
across every layer at once: serif Times against sans Arial, `print-neutral` with a blue accent
against `mono-ink` with none, asymmetric binding margins against symmetric, an h3 tier that the
CV correctly lacks, and a wholly different constraint set. Two structurally distant families do
not collapse onto the same answer. That is the strongest evidence in this pass that the library
is doing design work rather than decorating a template.

### 3.3 `slide-deck-projection` — pptx

**(1) No refusal.** `"Build me a presentation to show on stage"` resolved to
`slide-deck-projection`, `top_score=3.4564`. `"Make a slide deck for a projected conference
talk"` abstained, all three decks inside 0.94 of each other:

```
[ABSTAIN] no confident match for "Make a slide deck for a projected conference talk"
  top candidates -- ask the user which one they meant:
    'slide-deck-projection' "Slide deck -- projection"  score=6.4669
    'slide-deck-document' "Slide deck -- read on screen (deck as document)"  score=6.1841
    'slide-deck-handout' "Slide deck -- handout / leave-behind (print-dense)"  score=5.5323
```

Naming the medium explicitly did not separate the three deck rows. Filed under D5. This is
distinct from the documented German-deck ambiguity, which is a tie broken the wrong way; here the
skill correctly declines rather than guessing.

**(2) Sections.** Expected and produced identical, seven sections:
`cover;agenda;problem-statement;proposed-solution;findings;call-to-action;contact`. **PASS.**

**(3) Handoff, pptx.**

| Value | Present? | What it said |
|---|---|---|
| slide layout | yes | `LAYOUT_16x9: 10in x 5.625in` |
| margins | n/a | no page-formats row emitted, correctly, per research/24 §3 item 2 |
| fonts | yes | Arial across heading, body and fallback |
| point sizes | yes, but **wrong** | `body: 11pt`, `h2: 16pt`, `h1: 24pt` |
| palette | yes | `Primary: #FFFFFF -> FFFFFF`, `Secondary: #D9D9D9 -> D9D9D9`, `Accent: #FFD400 -> FFD400`, `Background: #0F0F0F -> 0F0F0F`, `Foreground: #FFFFFF -> FFFFFF`, each with the '#' correctly stripped |
| page flow | yes, as a statement | `page flow: NOT APPLICABLE -- slides do not paginate, so docx's page-flow properties have no pptx equivalent` |

The page-flow line is the release-notes claim holding: the deck says so rather than staying
silent. The palette hex stripping is real and correct. The point sizes are the defect — see D3.

**(4) Plain-text path.** Section order survives; 28 heading rows print as bare ids.

**(5) Designed or generic.** Designed at palette and style — a near-black background with a
yellow accent and an explicit "no mid-gray under projector washout" rationale is a real
projection decision. Undermined at type: the deck is handed the CV's print scale.

### 3.4 `invoice-tabular` — short artefact

**(1) No refusal.** Both phrasings resolved to `invoice-tabular`, at `14.8851` and `10.6105`.
`"I need to bill a client for three items"` names neither "invoice" nor any keyword literally and
still resolved — the best natural-phrasing result of the pass.

**(2) Sections.** Expected and produced identical, seven:
`issuer;bill-to;invoice-details;line-items;totals;tax;payment-terms`. **PASS.** This is a field
model rather than a prose model and it survives intact.

**(3) Handoff, pdf.** Different branch from docx, and populated:

```
  @page (native HTML -> Chromium/WeasyPrint pipeline):
    size: 210mm 297mm
    margin: 15mm 20mm 15mm 20mm  (top right bottom left)
  font-face stack (embed vs. safe-stack per render target's Font Rule):
    headless-chromium (embed): Public Sans / Public Sans
    weasyprint (embed): Public Sans / Public Sans
    wkhtmltopdf (embed): Public Sans / Public Sans
  render command:
    headless-chromium: /opt/google/chrome/chrome --headless --no-sandbox --disable-gpu --print-to-pdf=%o --no-pdf-header-footer %i
  constraints to preflight (Set Keys): report-typography
```

Page size and margins present, fonts present per engine with the fallback chain, render commands
present. **Point sizes, heading levels and the palette are absent entirely — there is no block
for them at all**, not even a `(not present in this resolution)` line. I read the builder rather
than assuming it was by design: `_build_pdf_lines` (`scripts/ddi.py:523-582`) emits `@page`, the
font-face stack, the render command and an optional bleed/tier line, and has no code path that
emits a size or a colour. The docx and pptx builders both do. The values are present in the
resolved payload — `form-print-print-body` at 11pt, `form-print-print-legal` at 8.5pt, and
`print-neutral`'s five hex values — and the builder drops them. `invoice-tabular`'s only render
target is `pdf-chromium`, so there is no second path that could deliver them. Filed as D2.

**(4) Plain-text path.** Section order survives; 21 heading rows print as bare ids.

**(5) Designed or generic.** Partly. `form-grid-underline` is the right style choice and the
reasoning row explicitly says "tabular figures required", which is a genuinely expert call for an
invoice. But `doc-styles` prints only Display Name, Keywords and Best For:

```
  doc-styles/form-grid-underline
    Display Name: Form, grid underline
    Keywords: form, grid, underline fields, tabular, line-item, photocopy-safe, hairline
    Best For: hand-filled forms, fiches, quotes/devis, invoices, any field- or line-item-based document
```

`Table Rules`, `Table Fills`, `Field Style`, `Rule Hair pt`, `Rule Strong pt` and `Emphasis
Mechanism` are all dropped. The output names a grid-underline style and then never says what the
grid or the underline is. Likewise `typefaces.Has Tabular Figures` is dropped, so the one
property the reasoning row demands by name never reaches the renderer.

### 3.5 `quote-devis` — non-English

**(1) No refusal.** Both French prompts resolved to `quote-devis`.
`"Prépare un devis avec un tableau de prix"` at `9.0716`, `"Fais-moi un devis pour un client"`
at `8.5393`. No English prompt was needed. The French keywords in the doctype row are doing real
work.

**(2) Sections.** Shares `invoice-standard`. Expected and produced identical, seven sections.
**PASS.**

**(3) Handoff, pdf.** Byte-identical to `invoice-tabular`'s: same `@page`, same font stack, same
render commands, same constraint set. Correct, since both share `a4-form-standard`,
`ofl-public-sans` and `form-print` — and it carries the same missing point sizes, heading levels
and palette, for the same reason. See D2.

**(4) Plain-text path — this is the field that matters for this family.** 21 heading rows, bare
ids:

```
  headings/issuer-en-1
  headings/issuer-fr-1
  headings/issuer-de-1
```

A French devis resolves the French heading rows and then prints their ids next to the English and
German ones with no wording and no language label. `headings.csv` carries `Heading Text` and
`Language` per row, and neither is emitted. **The three-language heading feature cannot be
observed to work from any output this skill produces.** The French user is handed
`issuer-fr-1` and no French.

**(5) Designed or generic.** Cannot be judged favourably. Nothing in the resolved output for a
French request differs from the English invoice except the doctype row's own display name. The
language-specific work exists in the data and is invisible in the answer.

### 3.6 `infographic` — the documented no-structure family

**(1) No refusal.** `"Design an infographic"` resolved at `5.1153`. No `[NO MATCH]`.

**(2) Sections.** There is no structure row, by documented design. What the output actually says:

```
  doctypes/infographic
    Structure Key:
    Render Target Keys: png-social
    Constraint Set Keys: no constraint-set-keys guidance for infographic
    Region Key: no region-key guidance for infographic
```

Two of the three empty fields name themselves. `Structure Key:` prints a bare blank. **This is
the empty-answer shape the ruled message exists to prevent, surviving in the one family that
most needs it.** See D4.

**(3) Handoff, pdf.** Mostly empty:

```
  @page (native HTML -> Chromium/WeasyPrint pipeline):
    size: 285.75mm 357.19mm
    margin: 18mm 14mm 18mm 14mm  (top right bottom left)
  font-face stack (embed vs. safe-stack per render target's Font Rule):
    (not present in this resolution)
  render command:
    (not present in this resolution)
  constraints to preflight: (none found)
```

Page size and margins present. No fonts, no render command, no constraints. The cause is
upstream: `doc-reasoning/infographic-scaffold` carries an empty `Style Key`, `Palette Key` and
`Typeface Key`, so no typeface row is ever pulled and the font stack has nothing to build from.
`png-social` is also the only render target in the pass with no usable command.

**(4) Plain-text path.** No section model exists to survive, and the resolver prints zero heading
rows, which is correct.

**(5) Designed or generic.** Generic. The answer is a page size and two margins. A user asking
for an infographic gets a rectangle. RELEASE-NOTES documents that infographic has no section
order; it does not document that infographic also has no typography, no palette and no render
command, which is what the output actually shows.

---

## 4. DEFECTS RANKED

### D1 — P0 — Authored payload columns never reach any output path

**Hits:** every family. Worst on `headings` (all six), then `cv-regions` (all CV families),
`doc-styles` (all), `doc-reasoning` (all), `structures` (all), `constraints` (all),
`type-scales` (all), `typefaces` (all).

**What the output said.** For a UK CV, verbatim JSON:

```json
"headings": [{"key": "contact-en-1"}, {"key": "contact-en-2"}, {"key": "contact-en-3"}]
```

**What it should have said.** `headings.csv` row 2 is
`experience-en-1,experience,Experience,en,yes` — so the row carries `Heading Text`, `Language`
and `Is Primary`, and the output should carry the wording "Experience", its language and whether
it is the primary variant.

**Why this is P0 rather than cosmetic.** The `handoff` subcommand's only input is the resolved
JSON. `_handoff` builds its payload from one read — `payload = json.loads(Path(args.json_path)
.read_text(encoding="utf-8"))` at `ddi.py:624` — and passes it to `_build_handoff_lines(payload,
args.format)` at `ddi.py:637`, which takes no other argument. `ddi.py` does define
`DEFAULT_DATA_DIR` at line 68, but the only use is `data_dir = DEFAULT_DATA_DIR` at line 95,
inside the `check` subcommand; no handoff builder touches it. So the JSON above is the entire
universe the renderer sees. The plain-text path is no better: `resolve.py` has exactly two
display call sites, lines 548 and 577, both calling `_display_columns`, and
`research/53-defect-verification.md` confirms both were checked and both print bare ids. **The
phrase "by any path" is exact, not rhetorical: `Heading Text` cannot reach a docx or pptx
renderer, or a human reader, by any path that exists in this asset.** v0.2.0's headline addition — 52 canonical sections, 204 heading
rows in English, French and German — is authored, gated, shipped, and unreachable. This is not
covered by, and does not extend, any RELEASE-NOTES known limitation; the known limitation about
headings says only that non-CV sections carry one wording per language, which presumes the
wording is delivered at all.

**One root cause, eight surfaces.** `resolve.py:_display_columns` (line ~500) returns the
manifest's explicit `display_columns` if present, otherwise `searchable_columns` plus this
table's own FK source columns. The manifest declares `display_columns` on six tables. For the
other eight the default is computed, and for a table that is neither searched nor a FK source it
computes to an empty list. `_resolution_payload` and `_print_resolved` both call it, so JSON and
plain text are affected identically, and handoff inherits the JSON.

| Table | `display_columns` | Dropped | Cost |
|---|---|---|---|
| headings | none; searchable `[]`, FK `[]` → empty | Heading Text, Language, Is Primary | every heading row is an id with no words |
| cv-regions | none; searchable `[]`, FK `['Section Order']` | 12 of 14 cols incl. Max Pages, Photo, Date of Birth, Nationality, Visa Status, Language Expectation | regional CV intelligence invisible |
| doc-styles | none; searchable 3 cols | Rule Hair pt, Rule Strong pt, Rule Brand pt, Corner Radius mm, Table Rules, Table Fills, Emphasis Mechanism, Field Style, Not For | the style spec itself |
| doc-reasoning | none | Palette Bias Terms, Typeface Bias Terms, Anti-Pattern Tokens, Doc Conditions, Severity | the anti-patterns are the expert content |
| structures | none; searchable `['Display Name']` | Heading Language, Heading Depth Max, TOC Depth, Front Matter Numbering, Caption Position, Cross-Ref Style | 6 of 9 cols; a report hands over no TOC depth |
| constraints | declared, incomplete | Applies To, Check, Threshold, Severity — 4 of 7 | a rule arrives with no scope, no check, no limit and no fail/warn |
| type-scales | declared, incomplete | Leading Ratio | leading is the one measure this repo cites Bringhurst for, as CONVENTION (`research/03-document-design-knowledge.md`) |
| typefaces | declared | Has Tabular Figures, Embedding Licence, Category Contrast, Mono Family | invoice reasoning demands tabular figures by name |

**Two tables not exercised that carry the same defect.** `font-substitutes` has searchable `[]`
and FK `[]`, identical to `headings`, so it would print bare keys too; no family in this pass
resolved it. `figures` shows 3 of its 19 columns, dropping `When NOT to Use`, `Greyscale Safe`,
`Caption Must State` and `Anti-Patterns`. Both extend D1 and neither was exercised.

**Suspected location, verified not assumed.** The generator is `research/build-manifest.py`. I
opened it: line 2 says it emits `data/schema-manifest.json`, line 443 is
`out = pathlib.Path("data/schema-manifest.json")`, the six `display_columns` declarations are
literals at lines 135, 167, 184, 211, 237 and 265, and its own comment at line 37 states they
are "Written here and never by hand in data/schema-manifest.json -- that file is generated". So
for the six declared tables the fix belongs there. For the eight computed ones, the default logic
in `skill/document-design-intelligence/scripts/resolve.py:_display_columns` is real source and a
legitimate fix site. The base CSVs are correct and are written only by `research/load-base.py`;
no data change is needed.

**Two sub-causes, needing two different fixes. Do not write this up as one uniform change.**

- **Class A — no `display_columns` declared at all, so the computed default decides.**
  `headings`, `structures`, `cv-regions`, `doc-styles`, `doc-reasoning`, and the two unrun
  tables. `headings` is the extreme case: searchable `[]` and FK `[]` means the default computes
  to an empty list and the row shows nothing but its key. Fixing these means either declaring
  `display_columns` for each in `research/build-manifest.py`, or changing what the default
  computes to in `resolve.py:_display_columns`. A default that is empty for any table is the bug
  worth fixing on its own, since it can only ever print a key.
- **Class B — `display_columns` is declared and merely incomplete.** `constraints` (4 of 7
  columns hidden) and `type-scales` (`Leading Ratio` hidden). The declaration overrides the
  default outright, so no change to the default logic touches these. They are fixed only by
  editing the literal lists in `research/build-manifest.py` at lines 265 and 184.

**Proposed fix, in words.** Give the manifest generator a third category beside searchable and
FK: a payload column, declared per table, that is neither searched nor a reference but must
reach the reader. Declare it for every table above, which covers both classes in one mechanism.
The reason the default cannot simply become "all columns" is that `_display_columns`'s docstring
commits to never showing the whole row.

**How to confirm.** Resolve any family to JSON and assert that the `headings` array's first
element has more than one key; assert that a `cv-regions` element carries `Max Pages`. Both
assertions fail today. The test that matters is the one that fails when the feature produces
nothing — asserting a non-empty `headings` list would pass right now and prove nothing.

### D2 — P1 — The pdf handoff emits no point sizes, no heading levels and no palette

**Hits:** `invoice-tabular`, `quote-devis`, `infographic` — three of the six families run — and
every unrun family whose render target is pdf.

**What the output said.** The complete pdf handoff for an invoice, with nothing elided:

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

Three of the seven values the brief names are simply not there. Not reported empty — there is no
heading for them at all, so nothing in the output signals that a size or a colour was ever
decided.

**What it should have said.** The resolution behind that block contains
`form-print-print-body` at 11pt, `form-print-print-legal` at 8.5pt, and `palettes/print-neutral`
with Primary `#22282E`, Secondary `#55606B`, Accent `#2E5C82`, Background `#FFFFFF` and
Foreground `#1A1E22`. A CSS pipeline needs `font-size` and `color`; the font-face stack supplies
neither. The block should carry both, as the docx and pptx blocks do.

**Root cause.** `_build_pdf_lines` (`scripts/ddi.py:523-582`) appends exactly four sections —
`@page`, the font-face stack, the render command, and an optional tier line — plus bleed and
crop marks when `Print Tier Max` exceeds `submittable-rgb`. It reads `page_row`, `render_rows`
and `typeface_row` and never touches the resolved `type-scales` or `palettes` rows.
`_build_docx_lines` and `_build_pptx_lines` both do. This is an asymmetry between the three
builders, not a decision recorded anywhere I could find.

**Why this is P1.** It is ruling M's exact shape — the block is populated enough to look
healthy, and the values a renderer actually needs are missing — reappearing on the one output
format that two of my six families use exclusively. It is not P0 only because the docx and pptx
paths are unaffected, so the majority of families still get their type and colour.

**Suspected location.** `skill/document-design-intelligence/scripts/ddi.py`, function
`_build_pdf_lines`. Real source, not generated. The fix is to add a size block and a palette
block in CSS vocabulary — `pt` sizes as stored and `#RRGGBB` unmodified, since CSS takes both
natively, which is simpler than either the DXA or the strip-the-hash conversions the other two
builders already do correctly.

**How to confirm.** Run `ddi.py handoff --format pdf` on any resolved invoice and grep the
output for `11pt` and for `#22282E`. Neither appears today. The check that matters is grepping
for the values, not for the section headers — a header with `(not present in this resolution)`
under it would pass a header-only check and prove nothing.

### D3 — P1 — A projection deck is handed the CV's print type scale

**Hits:** `slide-deck-projection`, and by inheritance `slide-deck-document` and
`slide-deck-handout`, which were not run.

**What the output said.** pptx handoff, verbatim:

```
  font sizes (pptxgenjs pt -- research/23 pptx:561-564,576, no conversion):
    body: 11pt
    h2: 16pt
    h1: 24pt
```

and the resolved rows behind it:

```
  type-scales/cv-print-print-body
    Medium: print
    Role: body
    Size pt: 11
```

**What it should have said.** `type-scales.csv` contains a `deck-projection` scale —
`projection/body/24pt`, `projection/body-dense/18pt`, `projection/h1/36pt`. A projected deck
should receive 24pt body and 36pt h1. It receives 11pt body at `Medium: print`, and an h2 tier
that does not exist in the projection scale at all.

**Root cause.** The only path to a type scale is `typefaces.Scale Key`.
`doc-reasoning/deck-generic` sets `Typeface Key: safe-sans-arial`, and
`typefaces/safe-sans-arial` carries `Scale Key: cv-print`. No typeface references
`deck-projection`, so those three rows are unreachable by any query. The medium is never
consulted; the scale is a property of the font choice, not of the output medium.

**Why this is P1 and not P0.** It produces a wrong value rather than an empty one, and a model
reading `Medium: print` on a pptx handoff has a chance of noticing. But 11pt body text on a
projector is unreadable at the back of a room, and the deck reasoning row explicitly promises
"legible in projection" — the library states the goal and then hands over the opposite.

**Suspected location.** The relationship itself, not a single line: `Scale Key` hangs off
`typefaces` in `research/build-manifest.py`'s schema and in `research/load-base.py`'s authored
rows. A scale needs to be selectable by medium, or `deck-generic` needs its own typeface row
whose `Scale Key` is `deck-projection`. **Do not fix this by editing `safe-sans-arial`'s scale**
— Arial is also the CV's face and the CV needs `cv-print`. That is the shape of tuning one
constant to turn a bullet green, which this project has already refused once.

**How to confirm.** Resolve any deck and assert the resolved `type-scales` rows carry
`Medium: projection`. Fails today.

### D4 — P2 — `infographic` prints a bare blank field, and its handoff has no fonts or render command

**Hits:** `infographic`.

**What the output said.** `    Structure Key:` — nothing after the colon. Meanwhile the two
group-FK columns on the same row said `no constraint-set-keys guidance for infographic` and
`no region-key guidance for infographic`.

**What it should have said.** `no structure-key guidance for infographic`, by the same ruling.

**Root cause.** `resolve.py:_field_value` emits the ruled sentence only when the column is a FK
*and* `datalib.fk_spec(fk)[3]` — the is_group flag — is true. `Structure Key` is a single-valued
FK, so it falls through to `return value` and prints the empty string. The ruling was implemented
for group columns only.

**Second half.** The pdf handoff for this family reports `(not present in this resolution)` for
both the font-face stack and the render command, because `doc-reasoning/infographic-scaffold`
has empty `Style Key`, `Palette Key` and `Typeface Key`. RELEASE-NOTES says infographic "gets
layout, typography, colour and print only" — the output shows it gets layout and print, and
neither typography nor colour. **The release note is wrong about this family**, which is worth
correcting independently of the code.

**Suspected location.** `scripts/resolve.py:_field_value` for the blank field. For the empty
reasoning row, `research/load-base.py` and the authored draft behind
`doc-reasoning`'s `infographic-scaffold` row.

**How to confirm.** Resolve `infographic` and assert no line matches `^\s+[A-Z][^:]*:\s*$`.

### D5 — P2 — Shipped families abstain on natural phrasings

**Hits:** `cv-uk`, `slide-deck-projection`. Not seen on report, invoice or devis.

**What the output said.** Both abstain blocks are quoted in §3.1 and §3.3. For the CV, a
slide-deck handout outscored `cv-uk` on a prompt whose first noun is "CV". For the deck, naming
the medium explicitly left three deck rows within 0.94 of each other.

**What it should have said.** `cv-uk`, resolved.

**Why this is in scope.** This is not routing. The skill ran, scored its own library, and
declined to answer. That is output quality by the brief's definition of field 1, even though it
is not the refusal string.

**Suspected cause, stated as a hypothesis I did not confirm.** The word "print" appears in
`slide-deck-handout`'s display name as "print-dense", and BM25 appears to reward it enough to
overtake a two-letter-token match on "CV". I did not read the scorer, so I am not naming a fix
site. Confirm by re-scoring the same prompt with "print" removed and comparing rank.

### D6 — P3 — Unreachable data rows

**Hits:** library-wide, no family output affected.

- `font-safety` and `redesign` appear as `Set Key` values in `constraints.csv` but no doctype's
  `Constraint Set Keys` references either. Verified by differencing the set of all `Set Key`
  values against the union of all 30 doctypes' `Constraint Set Keys`. Their only other mentions
  in the whole tree are prose in `data/schema-manifest-NOTES.md`.
- `deck-projection` (3 rows) and `print-office-generic` (6 rows) in `type-scales.csv` are
  referenced by no typeface. That is 9 of the 20 type-scale rows unreachable; see D3 for the
  deck half, which is the half that causes a wrong answer.

**Why it matters.** The gate counts these rows as shipped and valid. Nine unreachable
type-scale rows out of twenty means the row count in the brief's own fingerprint overstates what
the library can actually deliver.

**Suspected location.** `research/load-base.py` and the authored drafts; a reachability check
belongs in `scripts/validate_data.py`, which today validates form and not reachability.

### D7 — P3 — The published asset's `VERSION` reads `0.0.1-dev`

The asset whose content matches published v0.2.0 on all six reference values ships a `VERSION`
file saying `0.0.1-dev`, and `ddi.py version` reports it. A user who runs the documented version
command cannot tell which release they have. Fix belongs in `scripts/build_zip.py` and whatever
writes `VERSION`, not in the built artefact.

---

## 5. What I could not determine

- **Whether this is byte-identical to the published release.** I proved content identity against
  all six reference values the brief supplies. I did not download the release, and I did not use
  `gh` or any git operation to try. If byte identity matters, someone with git authority must
  confirm it.
- **How this output was obtained, which bounds every claim in §3.** I ran the skill's own scripts
  directly — `ddi.py resolve` and `ddi.py handoff` against the extracted asset. I did not hold a
  conversation with Claude and did not append "Use the document-design-intelligence skill." to
  anything, because there was nothing to append it to. This is stronger evidence for the five
  scored fields than a transcript would be, since it shows exactly what the skill emits with no
  model paraphrasing in between. It is weaker in one specific way: **what a model does with this
  output is untested.** The prompt strings in §3 are resolver queries, not conversation turns.
- **Whether the deck abstain is the same defect as the documented German-deck ambiguity.** They
  have the same cause — three deck rows scoring close — but different outcomes: the documented
  one resolves wrongly, this one abstains. Whether one fix addresses both, I did not establish.
- **The whole folded and large-format path.** No brochure, flyer, poster or one-pager was run.
  Seven doc keys, and panel adjacency is a documented non-feature, so I cannot say whether that
  path produces a thin answer or a wrong one.
- **Whether a renderer given this handoff produces a good document.** I exercised the skill's own
  output end to end. I did not render a docx or a pptx from it. D1 is a claim about what the
  renderer can possibly receive, which I proved from `ddi.py:624`; it is not a claim about what a
  renderer does with it.

## 6. Attribution check

One named authority appears in anything I quote: the page-flow handoff header says the mapping
is "convention, not sourced to any authority this library cites", which is correct and needed no
name. I cite Bringhurst once, for leading in D1, and it is grep-verifiable —
`research/03-document-design-knowledge.md` carries "**Leading:** [CONVENTION, Bringhurst's rule
of thumb]". No claim in this report rests on Butterick or DIN 5008, which are cited nowhere in
this repo. The page-flow properties and the heading sizes are **CONVENTION**, as RELEASE-NOTES
already states.
