# Form — fresh coding r2 of all 4 items under 82a-clarifications-7 C47 (unit of coding = prescribed specimen)

Coder: Design Researcher 3, 2026-09-25. First coder of form (Fm.8). This is a **fresh coding of every feature** of the 4 items in
`form-items.csv`. The Fm.3/Fm.8 codes were not used as input.

Independence: I did not open `form-agreement.md`, `form-second-coder.md` or §1–§9 of `82a-gate-failures.md`. I read only §10
(the rule texts) and `82a-clarifications-7.md`.

Rules applied:
- research/82 §4–§5;
- colour: 82a-general §B;
- C7/C29: answer grids are field style, not tables;
- **C47** (ratified draft C38):
  - the item is the prescribed specimen, never the documentation site;
  - site nav, TOC, headers/footers, code samples and site `<h1>`/link styling are ignored;
  - heading/body class = the typeface the authority prescribes for form text;
  - columns = the specimen's own question flow;
  - colour = at-rest colours only (error/focus/hover are UI states, B1d);
  - for ABS the diagram is the specimen.

Sources were fetched 2026-09-25 with `curl -s -L -A "smart-design-research"` (all HTTP 200). Files were kept in the system temp dir.
Hexes are read from the authority's own CSS. HSL comes from `colorsys` and contrast from `lib/color.contrast_ratio`. ABS pixels
were measured with `measure.py`: B1a 20×20 grid with 82a-deck §2 class tolerances, B3 opening with a square of 5% of the short
side, B4 core pixels.

**Specimen rule used, stated once.** Take the first rendered example the authority publishes for a form field. If the item's own
URL renders no specimen, take the authority's text-input component: that is where each authority's field style is prescribed,
and it is the NHS item's own page.
- For three of the four items, the `form-items.csv` url does **not** render a specimen:
  - USWDS `/components/form/` is guidance only in v3.14.0;
  - GOV.UK `/patterns/` is an index;
  - ABS `…lines-and-boxes` shows fragment diagrams only.
- The source actually used is recorded per item. **Recommendation to the orchestrator:** point the second coder's `preview_url`
  at these specimen URLs (the change carries no codes), or the two coders may code different specimens.

| id | columns | head | body | colour | field | rules | dens | adm | source used (C47) | colour-note | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FMA:001 | 1 | sans | sans | mono | box | boxes | airy | y | **USWDS Text input, "Component preview"**, the first example on `designsystem.digital.gov/components/text-input/`: label "Text input label" + `.usa-input`, and label "Text area label" + `.usa-textarea`. CSS `/assets/css/styles.css` (site v3.14.0). The item URL `/components/form/` has guidance only ("Keep your form blocks in a vertical pattern" → columns 1) and no rendered example | bg #ffffff. Label and input text #1b1b1b (S 0, L 0.106, near-black). Input/textarea border 1px #5c5c5c (S 0, L 0.361). 0 chromatic elements → mono. `.usa-hint--required` #b50909 is not in the specimen, so it is not coded. **Sensitivity**: if the form page's text prescription (a red asterisk on each required field) were drawn into the specimen, ≥ 2 asterisks would meet B5 → one-accent | type: `.usa-label`/`.usa-input` font-family "Source Sans Pro Web, Helvetica Neue, …, sans-serif" (Google Fonts SANS_SERIF). The specimen has no heading, so the heading class = the prescribed form typeface. Field = full 1px border, radius 0 → box. Density: 2 text lines. A6 #1b1b1b on #fff = 17.22:1. No A1–A8 hit |
| FMA:002 | 1 | sans | sans | mono | box | boxes | airy | y | **GOV.UK Text input, first example** (`design-system.service.gov.uk/components/text-input/default/index.html`): `h1 > label.govuk-label--l` "What is the name of the event?" + `.govuk-input`. CSS `govuk-frontend-19425e5e83713c223caeea2a404a39b8.min.css` (the example's own stylesheet). The item URL `/patterns/` is an index. Alternative specimen, recorded: the question-pages pattern's first example is a radios question with a Continue button; its at-rest colours are also #0b0c0c, and the green button is B1d | bg `--govuk-body-background-colour` #fff. Label `--govuk-text-colour` #0b0c0c; input border 2px `--govuk-input-border-colour` #0b0c0c (L 0.04, achromatic). 0 chromatic elements → mono. The error/focus colours are states (B1d) | type "GDS Transport", arial, sans-serif (non-Google; foundry class sans), both label and input. Field = 2px full border, radius 0 → box. Density: 1 label line. A6 19.59:1. No A1–A8 hit |
| FMA:003 | 1 | serif | serif | mono | box | boxes | standard | y | **ABS Forms Design Standards 2023, front of form, Diagram 6** "postal business survey form" (`abs.gov.au/system/files/77af96fd3ca6ec445f123db7878a0d01/D6%20FOF.png`, 560×799, from `…/paper-forms-design-standards-front-form`). It is the first full-sheet form illustration the standard publishes; the item URL `…lines-and-boxes` holds only fragment diagrams (Diagram 1 there is a split-page fragment). The diagram's own strokes and fills are coded (C47) | `measure.py`: background class #e8e8e8 (L 0.910, 222 of 277 kept grid points, B1a); white answer boxes #fefefe (L 0.996, B1e); blocks **0.00%**; **no chromatic core pixels**. ABS logo excluded (B1b), barcode excluded (B1c) → mono | type: the typography chapter allows either class ("We use both serif and san serif fonts in ABS paper forms"), so the class is read from the specimen: bold serif title "Economic Activity Survey 20XX-XX" and serif body. Columns: single-column front; the Telephone \| Mail pair is a contact/address block (C28) → 1. Field: white answer boxes bounded by solid lines, plus the contact grid (answer boxes per C29, not C7) → box. Density ≈ 37 text rows on the sheet → standard. A6: black on #e8e8e8 = 17.14:1. No A1–A8 hit |
| FMA:004 | 1 | sans | sans | one-accent | box | boxes | airy | y | **NHS service manual, Text input, first example** (`service-manual.nhs.uk/design-example/components/text-input/default`): `h1 > label.nhsuk-label--l` "What is your full name?" + `.nhsuk-input`. CSS `/stylesheets/nhsuk-frontend.bd25200.min.css` (the example's own stylesheet) | bg `body` #f0f4f5 (L 0.951, B1a/B1e). Label text = body colour #212b32 (H 205°, **S 0.2048**, L 0.163). Input border 2px #4c6272 (H 205°, **S 0.2000**, L 0.373). Both are chromatic at the literal thresholds (C29), in one cluster of **2 elements** (a text run and a shape), so B5 is met → one-accent. The error red is a state (B1d). Sensitivity (C29): as near-grey it would be mono | type `html{font-family:Frutiger W01, arial, sans-serif}` (non-Google; foundry class sans). Field = 2px full border, radius 0 → box. Density: 1 label line. A6 #212b32 on #f0f4f5 = 13.02:1. No A1–A8 hit |

## Value counts (4 items)

| feature | values |
|---|---|
| columns | 1: 4 |
| heading class | sans 3 (FMA:001, 002, 004); serif 1 (FMA:003) |
| body class | sans 3; serif 1 (FMA:003) |
| colour use | mono 3 (FMA:001, 002, 003); one-accent 1 (FMA:004) |
| field style | box 4 |
| rules/boxes | boxes 4 |
| density | airy 3; standard 1 (FMA:003) |
| admissible | y 4 |

Archetypes (`columns|heading|colour|field`):
- `1|sans|mono|box`: FMA:001, FMA:002;
- `1|serif|mono|box`: FMA:003;
- `1|sans|one-accent|box`: FMA:004.

Disclosed sensitivities:
- FMA:001: an asterisk-bearing specimen would be one-accent.
- FMA:002: the question-pages specimen is mono as well, but it has radios, not a text field.
- FMA:004: the C29 boundary.
