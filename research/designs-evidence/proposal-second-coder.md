# proposal — independent second coder (research/82 §7, seed "82a:proposal")

Coder: Opus Reviewer, 2026-09-24.

## 1. Method

**Read:**
- research/82 §4 (rubric; proposal variant `cover page`) and §5 (admissibility);
- research/82a-general.md (header treatment §A, colour use §B; binding);
- 82a-clarifications-1…5 (C13 cover and running page, C14, C25 declared fonts, C28);
- `proposal-items-github.csv` and `proposal-items-ms.csv`.

**Not opened:** any `proposal-*.md` corpus or recode file, any proposal agreement file,
research/91.

**Exposure disclosure (C12):** earlier (research/82b, research/91) I saw only
Microsoft proposal *titles* and the MS corpus file's section headings and counts ("7 Word docs,
corroboration"). I never saw any proposal item's feature codes or admissibility.

**Previews** (the csv's `preview_url`) were downloaded to `tmp-sc4/`, which was deleted at the end.

**GitHub PDFs:**
- Rasterised with PyMuPDF.
- Declared fonts were read from the PDF's embedded font list (§4: a declared font wins).
- Title, alignment, lines, fills and span colours were measured from the PDF's own text and
  vector data (`page.get_text('dict')`, `page.get_drawings()`), in PDF points.
- **Cover** = page 1 (C13).
- **Running page** = the first page with ≥ 250 words of running prose. Contents pages (dotted
  leaders), bibliographies and embedded forms are **not** running text. For CJK text, 2
  characters = 1 word.
- Where no page reaches 250 words (templates with little placeholder text), the page with the
  most running prose was used and flagged `<250`.
- Where page 1 already carries the title plus running text (no separate cover), page 1 serves as
  both, and `cover page` = no.

**Microsoft items** (only a cover thumbnail is published; C25):
- Heading class from the .docx theme `majorFont`; body class from `minorFont`.
- Columns from the declared `w:cols`, unless the thumbnail itself shows the running text (MSP:007
  is a one-page document, so it was coded from the page).
- Unobservable variants are coded `unknown` (C7).

**Colour** (82a-general §B):
- Excluded: the background, photos and logos (university crests, lab and company logos), and
  one-off elements failing B5.
- Chromatic test: S ≥ 0.20, 0.12 ≤ L ≤ 0.90, from span, vector and pixel core colours.

**Header** (82a-general §A, report/whitepaper/proposal row):
- The title is the largest text on the cover; logos are never the title.
- Centred = the title's centre within ±5% of page width of the page centre.
- A box edge counts only if the box spans ≥ 80% of page width.

**Density:** text lines on the running page (≤ 30 airy, ≥ 55 dense, per §4).

## 2. Sample

Ids from both csvs (47), sorted, then
`random.Random("82a:proposal").sample(ids, max(min(10, len(ids)), math.ceil(0.25*len(ids))))`
gives **n = 12**:

`GH:029, GH:092, GH:063, GH:037, GH:027, GH:036, GH:018, GH:014, MSP:006, GH:012, MSP:007, GH:025`

## 3. Coding table

| id | cover / running page | columns | heading | body | colour | header | rules/boxes | density | cover page | admissible |
|---|---|---|---|---|---|---|---|---|---|---|
| GH:012 | 1 / 2 (`<250`, instructions page) | 1 | serif | serif | mono | plain-centered | none | airy | yes | yes |
| GH:014 | 1 / 12 (`<250`) | 1 | sans | serif | mono | plain-centered | rules | airy | yes | yes |
| GH:018 | 1 / 2 (`<250`) | 1 | serif | serif | mono | plain-centered | none | standard | yes | yes |
| GH:025 | 1 / 3 | 1 | serif | serif | mono | plain-centered | rules | standard | yes | yes |
| GH:027 | 1 / 3 (`<250`) | 1 | serif | serif | mono | plain-centered | none | airy | yes | yes |
| GH:029 | 1 / 1 (`<250`) | 1 | sans | serif | mono | plain-left | boxes | standard | yes | yes |
| GH:036 | 1 / 2 | 1 | sans | sans | mono | plain-centered | rules | standard | yes | yes |
| GH:037 | 1 / 5 | 1 | serif | serif | mono | plain-centered | none | standard | yes | yes |
| GH:063 | 1 / 1 (no separate cover) | 1 | serif | serif | mono | plain-centered | none | airy | no | yes |
| GH:092 | 1 / 1 (`<250`) | 1 | serif | serif | mono | plain-centered | none | standard | yes | yes |
| MSP:006 | cover thumbnail only | 1 (declared) | display | sans | one-accent | image-hero | unknown | unknown | yes | yes |
| MSP:007 | single page (thumbnail = whole document) | 2-equal | serif | serif | mono | ruled | rules | airy | yes | yes |

### Per-item measurements

- **GH:012** — Title "研究生学位论文开题报告", SimSun (Song → serif), 26 pt; centre offset
  0.000W. Running text is KaiTi on the "说明" instructions page (brush-style Kai is coded serif).
  No drawings. 9 text lines.
- **GH:014** — Title in FandolHei-Bold (Hei → sans), 26 pt; offset 0.000W. The blue vector
  lockup at the top (62% of width) is the UCAS logo, so it's excluded; there is no other chromatic
  element. Running page 12 is FandolSong (serif), with one running-head rule. 15 lines.
- **GH:018** — Title "Proposal Full Title / PROPOSAL ACRONYM", TeX Gyre Termes, 22.8 pt; offset
  0.000W. The nearest wide line (81% of width, at y=325) is 112 pt below the title, more than
  4 body lines, and it's the abstract box, so not ruled. The grey instructional text has S < 0.20.
  43 lines.
- **GH:025** — Title in FandolSong-Bold, 18 pt, centred; the university crest is a logo.
  Running page 3 has a footnote separator line, so rules. 37 lines.
- **GH:027** — "Project Proposal Title", CMBX12, 24.8 pt; offset −0.003W. The blue circles and
  "b-it" box are institution logos (22 chromatic vectors, all logo). 25 lines.
- **GH:029** — The largest non-logo text is "Use and Disclosure of Data" (Nimbus Sans Bold,
  15.9 pt); offset −0.214W, so plain-left. The summary table spans 72% of page width (< 80%), so
  its edges are not header rules. The OpenBSD mascot is a logo. Page 1 is a BAA-style proposal
  cover sheet (cover page = yes), but it also carries the only prose (`<250`). The table has every
  cell bordered: boxes. (C7 applies only to invoice, quote and form.)
- **GH:036** — Title "Proposal to the Deutsche Forschungsgemeinschaft", Nimbus Sans Bold,
  centred (+0.012W). Running page 2 is Nimbus Sans, with one horizontal rule. The red and orange
  TODO notes are on the running page; colour is read from the cover only (C13).
- **GH:037** — "PROPOSAL SKRIPSI …", Nimbus Roman (Times), centred (+0.031W). Page 4 is a
  contents page (dotted leaders), so running page 5. 32 lines.
- **GH:063** — "CST3590: Proposal", CMR17, centred (−0.001W). Introduction text follows on page
  1, so there's no separate cover. Pages 4–5 are an embedded ethics form, not running text.
  25 lines.
- **GH:092** — "بسمه تعالی", B Nazanin Bold, 27 pt, centred (+0.024W). B Nazanin is a Naskh face,
  which I code serif (disclosed judgement: §4's class list has no Arabic-script category). One
  magenta link span fails B5. The field leaders are typed dots, not drawn lines, so rules/boxes =
  none. 36 lines.
- **MSP:006** — Theme major font Bebas Neue (Google category DISPLAY → display); minor font
  Tenorite (sans). The photo box is 44.2% of page area and starts at 6% of page height, so
  image-hero (C1). Title core `(113,32,11)` = H 12°, S 0.82, L 0.24, one element > 0.5% of the
  area: one-accent (the red logo is excluded). Title on white, not on the photo, so A3 doesn't
  apply.
- **MSP:007** — Theme fonts Baskerville Old Face ×2 (serif). Background is `#F9F5F2` (L 0.96),
  and there are no chromatic elements, so mono. A full-width rule sits below the 3-line un-headed
  summary under the title (82a-cv A1/A4 via 82a-general §A.2), so ruled. The body shows two side-by-side text
  columns (Problem Statement | Solution …), so 2-equal: the visible page overrides the declared
  single `w:cols`, which the layout achieves with a table. About 28 lines, so airy (near the
  threshold).

Summary: 12 coded, 12 admissible, 0 excluded.
