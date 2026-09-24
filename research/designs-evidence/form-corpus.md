# Form corpus — L3 authority only (USWDS, GOV.UK Design System); no L2 catalogue reachable

Coder: Design Researcher. Counts only (research/82 §1). Retrieved 2026-09-23. **Plain statement: this is a Shortfall family. Evidence is two web-UI design-system authorities coding to ONE archetype; no ranked (L1/L2) evidence exists.** Values below are read from the authorities' own published CSS/text (fetched raw with curl), not from a model paraphrase.

## Fm.1 Sources
| Authority | Pages fetched | Ranking Metric (§2) |
|---|---|---|
| USWDS | `https://designsystem.digital.gov/components/form/`, `.../components/text-input/`, CSS `https://designsystem.digital.gov/assets/css/styles.css` | `authority:USWDS form component` |
| GOV.UK Design System | `https://design-system.service.gov.uk/patterns/` (index), `.../components/text-input/`, `.../components/error-message/`, `.../patterns/question-pages/`, CSS `https://design-system.service.gov.uk/stylesheets/main-474eaefb2b0b7a31f2ea78a1079e0727.css` | `authority:GOV.UK Design System patterns` |

**L2 attempts:** MS(forms) and MS(form-templates) both redirect (HTTP 200) to the generic `https://m365.cloud.microsoft/create?...` landing page: an SPA with no static item cards (0 template cards in the payload) → **unreachable 2026-09-23**, disclosed, not reconstructed (82a C5). research/82's probe had already found no forms category. LibreOffice not counted (§10 lists none for form; `q=form` is full-text noise).

## Fm.2 What each authority prescribes (prescription → coded feature)
| Feature | USWDS | GOV.UK |
|---|---|---|
| Label position | `.usa-label` is `display:block`, above the `.usa-input`; label max-width 30rem | "You should align labels above the text input they refer to"; sentence case, no trailing colon |
| Field style | box: `.usa-input` `border:1px solid #5c5c5c; border-radius:0; height:2.5rem; max-width:30rem; padding:.5rem` | box: `.govuk-input` `border:2px solid #0b0c0c; border-radius:0; height:2.5rem; padding:5px` |
| Spacing | `.usa-form-group` margin-top 1.5rem; label margin-top 1.5rem, input margin-top .5rem | `.govuk-form-group` margin-bottom 20px in the base rule (responsive overrides not read) |
| Layout | "Keep your form blocks in a vertical pattern" (single column) | one thing per page; fieldset/legend with a large heading for the question |
| Colour use | greys for input/hint (#5c5c5c border, #757575 hint); red only for state: `.usa-input--error` 0.25rem #b50909 border, bold red message; red asterisk for required | near-black borders; red only for state: `#ca3535` border and message on error |
| Required/optional | red asterisk + explanatory text; optional fields marked "(optional)" | not asserted in the pages read |
| Placeholders | "Avoid placeholder text" | "Do not use placeholder text in place of a label" |

## Fm.3 Coded authority archetypes (§4 applied to the prescribed design)
Archetype = `columns|heading|colour|field style` (field style replaces header treatment).

| id | Authority | columns | heading | colour | field | rules/boxes | Admissible |
|---|---|---|---|---|---|---|---|
| FMA:001 | USWDS | 1 | sans (Source Sans Pro Web / Helvetica stack) | mono at rest (red is state-only) | box | boxes | y — no C7 all-cells table, no A1-A8 hit |
| FMA:002 | GOV.UK | 1 | sans (GDS Transport / Arial stack) | mono at rest (red is state-only) | box | boxes | y — same |

Both code to the **same archetype `1|sans|mono|box`** → one design with two independent L3 sources (§6 step 2: authority, ordered by number of sources = 2).

## Fm.4 Frequency and rank
No corpus is coded, so there is no k/N and no Rank Value. Rank list = L3 only:
1. `1|sans|mono|box` — `authority:USWDS form component` + `authority:GOV.UK Design System patterns` (2 sources).

Everything else is convention (L4, max 1) and the seeded doctype default.

## Fm.5 Shortfall (plain)
- Non-convention designs shippable: **1** (target 1-3 per §10, lower end; the floor of 5 is not reachable).
- **Caveat that matters for filling:** both authorities are screen web-UI systems. They prescribe boxed inputs; neither prescribes or discusses **underline** fields, the common print/office form style. So `field style = box` is evidence about web forms, not printed or Word forms, and cannot by itself justify demoting `underline`. The archetype reconstructs *their* component, not a paper form.
- `colour = mono` is my §4 reading of a form page whose only red is error state; a reviewer could code that as `one-accent`.
- C7 (`all-cells` table rules fail for forms) does not apply: neither prescribes a bordered grid table.

## Fm.6 Bias statement
Two public-sector design systems (US federal, UK government): accessibility-first, English, screen-first, single-column. No commercial or print form evidence. Authority is not popularity (§13).

## Fm.7 Ambiguities met
1. GOV.UK spacing: only the base `margin-bottom:20px` was read; responsive overrides not checked.
2. WebFetch alone returned "not explicitly prescribed" for USWDS label/field style; the raw CSS was fetched with curl to obtain the values above.
3. No second-coder list (nothing coded from a corpus).

## Fm.8 82b additions (Design Researcher 3, 2026-09-24): ABS paper-forms authority + NHS; 82b A3 cap

82b A3 (adopted 2026-09-24): form has **zero ranked K≥2 designs**, so the L3 cap is **5**. Each L3 design must code to a **distinct** archetype, and same-archetype authorities merge (extra provenance row). Colour use is coded under **research/82a-general.md §B** (82a C26; the form header is replaced by field style, which is unchanged). Everything above Fm.8 is unchanged, apart from the colour re-check of FMA:001/002 in Fm.8.4.

### Fm.8.1 Sources (fetched 2026-09-24, `curl -s -L -A "smart-design-research"`, all HTTP 200)
| Authority | Pages fetched | Ranking Metric |
|---|---|---|
| **ABS Forms Design Standards 2023** (Australian Bureau of Statistics; released 11/08/2023) | `https://www.abs.gov.au/statistics/standards/abs-forms-design-standards/2023/paper-forms-design-standards-lines-and-boxes`, `…/paper-forms-design-standards-typography`, `…/paper-forms-design-standards-layout`, `…/paper-forms-design-standards-front-form`, `…/general-forms-design-principles-layout-lines-boxes-and-typography`. Front-of-form illustrations Diagrams 6-8 downloaded from the front-form page (`/system/files/styles/complex_image/private/…/D6%20FOF.png` etc.) into the temp dir | `authority:ABS Forms Design Standards 2023 (paper forms)` |
| **NHS digital service manual**, text input | `https://service-manual.nhs.uk/design-system/components/text-input` + its CSS `https://service-manual.nhs.uk/stylesheets/main.dee0a48.min.css` (raw values read with grep, not paraphrased) | `authority:NHS service manual text input` |

### Fm.8.2 What each prescribes (quoted or read from source)
| Feature | ABS (paper, print) | NHS (web) |
|---|---|---|
| Field style | "All answer spaces should be white and bounded by a continuous solid line"; "Use a 0.5-point line for normal answer boxes"; "1-point line for 'Total' answer boxes"; 8 mm × 4 mm segmented boxes for numeric/OCR; 4 mm ballot boxes; 0.5 pt dotted **eye-guide lines** link the label to the box | `.nhsuk-input{… height:2.5rem; border:2px solid #4c6272; border-radius:0 …}`; "Align labels above the text inputs they refer to"; "Do not use placeholder text for a label" |
| Columns | "Use single column layouts for the front of form to minimise visual clutter"; double column allowed inside the form; "Do not use triple columns"; a 0.5 pt black (B/W forms) or 2 pt white (coloured forms) line divides split-page columns | single column (component page) |
| Typography | "We use both serif and san serif fonts in ABS paper forms"; titles 36 pt bold (24 pt if long), subtitles 18 pt bold, section headings 14 pt bold, questions 12 pt; line length ≈110 mm, max 115 mm | `font-family: Frutiger W01` (sans); labels 1-1.1875 rem |
| Colour | two variants: **coloured forms** (a background colour fill printed to 5 mm bleed; 10% screened instruction boxes with 2 pt white lines; white answer boxes; drop-out colour for OCR boxes) and **black-and-white forms** (0.5 pt black lines around instruction boxes) | text `#212b32`, input border `#4c6272`, page `#f0f4f5`; error `#d5281b` (state only) |
| Margins | top 5 mm, bottom 5 mm, inside 7 mm, outside 5 mm (scanner-specific; "your measurements may differ") | — |

### Fm.8.3 Coded authority archetypes (`columns|heading|colour|field style`)
| id | Authority | Specimen coded | columns | heading | colour (82a-general §B) | field | rules/boxes | adm | archetype |
|---|---|---|---|---|---|---|---|---|---|
| FMA:003 | ABS Forms Design Standards 2023 | **Diagram 6**, "postal business survey form", front of form (the first of the three front-form illustrations; Diagrams 7-8 are household forms, listed below) | 1 | serif (bold serif title "Economic Activity Survey 20XX-XX", serif body, as drawn) | **mono**. `measure.py`: background #ececec (L 0.925, B1a/B1e); ABS logo and barcode excluded (B1b/c); fill blocks 0%; no chromatic element meets B5 (the residual hue pixels are anti-alias fringe, B2) | box | boxes | y (see C7 note) | `1\|serif\|mono\|box` |
| FMA:004 | NHS service manual, text input | the component as specified in the CSS | 1 | sans (Frutiger W01) | **one-accent, BORDERLINE**. Text #212b32 (H 205°, L 0.163, **S 0.2048**) and input border #4c6272 (H 205°, L 0.373, **S 0.2000**) both meet the §4/B4 chromatic threshold S ≥ 0.20 exactly, so they form one cluster of ≥2 elements (B5). Page #f0f4f5 L 0.951 is excluded (B1e). The red error colour is state-only. Read as near-grey, it would be mono | box | boxes | y | `1\|sans\|one-accent\|box` |

Specimens not coded (same authority, listed for the record): ABS **Diagram 7** (household form, cream #f7f0d0 background, serif, boxes) and **Diagram 8** (household diary, pink #f0e0f0 background with a darker pink panel: fill blocks 7.45% < 10%, serif, boxes). Both would also code `1|serif|…|box`. Diagram 8's pink panel elements would make it one-accent, not mono, but §3.2's "first design shown" rule picks Diagram 6.

**C7 note (ABS).** The Diagram 6 contact block (Name / Date / Signature / Telephone / Email) is a grid of bordered label cells and answer boxes. It is coded as field style `box`, not as a table. C7 (`all-cells` table rules) is for data tables, and ABS prescribes these as answer boxes. The reviewer may rule otherwise, and if they do, FMA:003 is excluded.

### Fm.8.4 Existing authorities re-checked for colour under 82a-general §B (C26; values from Fm.2)
- FMA:001 USWDS: borders #5c5c5c and hint #757575 are achromatic (S = 0); red is state-only → **mono**, unchanged.
- FMA:002 GOV.UK: borders #0b0c0c (L 0.04 < 0.12, achromatic) → **mono**, unchanged.
- Both still code `1|sans|mono|box` and stay merged (Fm.3).

### Fm.8.5 Rank list (L3 only; 82b A3 cap 5; juried before authority; then number of sources; then key alphabetical)
| order | archetype | L3 sources | Ranking Metric strings |
|---|---|---|---|
| 1 | `1\|sans\|mono\|box` | 2 (USWDS, GOV.UK) | `authority:USWDS form component`; `authority:GOV.UK Design System patterns` |
| 2 | `1\|sans\|one-accent\|box` | 1 (NHS) | `authority:NHS service manual text input` |
| 3 | `1\|serif\|mono\|box` | 1 (ABS) | `authority:ABS Forms Design Standards 2023 (paper forms)` |

Order 2 vs 3 is decided by key alphabetical, since both have one source (`…one-accent…` < `…serif…` as archetype codes; the orchestrator substitutes the real design keys). **Sensitivity:** if FMA:004 is read as mono, NHS **merges** into order 1 (3 sources), and the list becomes 2 designs: `1|sans|mono|box` (3 sources) and `1|serif|mono|box` (ABS).

### Fm.8.6 Shortfall and caveats (plain)
- Non-convention form designs: **3** (2 under the sensitivity reading). The floor of 5 is not reached. No public source ranks form designs (82b §5).
- **ABS is the first print-form authority.** It addresses Fm.5's caveat that the existing authorities are screen-only. It still prescribes **boxed** answer spaces (0.5 pt) with dotted eye-guide lines, not underline fields. Evidence for `underline` remains absent from every authority read.
- DSFR and AGDS/GOLD (82b §1f: 403/timeout) were not retried; they are outside this task's list.
- Bias: four public-sector sources (US, UK ×2, Australia), English. ABS measurements are tuned to its scanning software ("Your measurements may differ"). Authority is not popularity (§13).

### Fm.8.7 Orchestrator ruling C29 (2026-09-24), recorded
Thresholds are literal at the boundary. NHS stays `1|sans|one-accent|box` (the grey reading is a disclosed sensitivity only). The ABS contact grid counts as answer boxes (field style `box`), not a C7 table. **Form ships 3 authority designs** (Fm.8.5 order).
