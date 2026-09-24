# report — independent second coder (research/82 §7, seed "82a:report")

Coder: Opus Reviewer, 2026-09-25.

## 1. Method

**Read:**
- research/82 §4 (rubric; report variant `cover page`) and §5;
- research/82a-general.md (§A header, §B colour; binding for report);
- 82a-clarifications-1…5, incl. C13 (cover / running page), C14 (display text on photos: ≥ 3:1
  at ≥ 24 pt, ≥ 4.5:1 below), C25 (MS declared theme fonts and `w:cols`), C29 (literal
  thresholds), C30, C32 (faint watermarks);
- `report-items-github.csv`, `report-items-ms.csv`, and `report-items.csv` (ARC, with its
  `pages` column: cover;running).

**Not opened:** any report `.md` file, research/91.

**Exposure disclosure (C12):** while compiling research/91, the output of a grep over
`report-corpus-github.md` showed two item-level admissibility facts: GH:025 excluded under A3
(watermark) and GH:051 excluded under A6 (2.55:1). GH:051 is not in this sample. **GH:025 is.**
I recoded it by measurement under C32 (§3), which post-dates that exclusion. A sensitivity line
excluding GH:025 is in §4.

**Previews** went to `tmp-sc5/`, deleted at the end. PDFs were rendered with PyMuPDF. Declared
fonts, text spans and image and drawing extents were read from the PDF.

**Pages (C13):**
- ARC items: cover and running page from the csv `pages` column.
- GitHub PDFs: cover = page 1. Running page = the first page with ≥ 250 words of running prose.
  Contents pages (dotted leaders), bibliographies, code listings and title-only pages are
  excluded. For CJK text, 2 characters = 1 word.
- Where no page reaches 250 words, the page with the most prose is used and flagged `<250`.
- Where page 1 already holds the title plus running text, page 1 is both, and `cover page` = no.

**MS items (C25):** heading and body classes come from the .docx theme major and minor fonts;
columns from `w:cols`. Rules/boxes and density are `unknown` (C7).

**Colour** (§B):
- Background = the modal colour class.
- Excluded: logos, crests, logo placeholders, photos, tints (L > 0.90) and a C32 watermark.
- Fill blocks: L ≤ 0.90, thickness ≥ 5% of the short side, together ≥ 10% of the area.
- A hue needs ≥ 2 elements, or 1 element ≥ 0.5% of the area.

**Contrast** with `scripts/lib/color.py contrast_ratio`.

## 2. Sample

Ids from the three csvs (64), sorted, then
`random.Random("82a:report").sample(ids, max(min(10, len(ids)), math.ceil(0.25*len(ids))))`
gives **n = 16**:

`MSR:008, GH:060, ARC25:011, MSR:003, GH:129, MSR:002, ARC25:018, GH:104, GH:069, GH:025, GH:019, MSR:005, GH:094, ARC25:020, ARC25:029, GH:058`

## 3. Coding table

| id | cover / running page | columns | heading | body | colour | header | rules/boxes | density | cover page | admissible |
|---|---|---|---|---|---|---|---|---|---|---|
| ARC25:011 | 1 / 2 | 3+ | sans | sans | mono | image-hero | boxes | dense | yes | yes |
| ARC25:018 | 1 / 2 | 3+ | sans | sans | one-accent | plain-centered | rules | dense | yes | **no — C14/A6** |
| ARC25:020 | 1 / 32 | 2-equal | serif | serif | mono | image-hero | none | standard | yes | **no — C14/A6** |
| ARC25:029 | 1 / 10 | 2-equal | serif | sans | mono | plain-left | none | standard | yes | yes |
| GH:019 | 1 / 1 (no separate cover) | 1 | serif | serif | mono | plain-centered | none | standard | no | yes |
| GH:025 | 1 / 4 | 1 | serif | serif | mono | plain-centered | boxes | standard | yes | yes |
| GH:058 | 1 / 3 | 1 | serif | serif | mono | plain-centered | none | standard | yes | yes |
| GH:060 | 1 / 4 (`<250`, 245 w) | 1 | serif | serif | mono | plain-centered | rules | standard | yes | yes |
| GH:069 | 1 / 3 (`<250`) | 1 | sans | serif | mono | plain-centered | none | airy | yes | yes |
| GH:094 | 1 / 3 | 1 | serif | serif | mono | plain-centered | rules | standard | yes | yes |
| GH:104 | 1 / 1 (no separate cover) | 2-equal | serif | serif | fill-blocks | plain-centered | none | dense | no | yes |
| GH:129 | preview 1 / preview 2 | 1 | serif | serif | fill-blocks | ruled | boxes | standard | yes | yes |
| MSR:002 | cover thumbnail | 1 (declared) | sans | sans | mono | plain-left | unknown | unknown | yes | yes |
| MSR:003 | cover thumbnail | 1 (declared) | sans | sans | fill-blocks | image-hero | unknown | unknown | yes | yes |
| MSR:005 | cover thumbnail | 1 (declared) | sans | sans | mono | plain-left | unknown | unknown | yes | yes |
| MSR:008 | cover thumbnail | 1 (declared) | sans | sans | one-accent | plain-left | unknown | unknown | yes | yes |

### Per-item measurements

- **ARC25:011** — Cover photo covers 92% from y = 1.7%, so image-hero. The white display title
  sits on green with a median of `(34,108,10)` = 6.53:1 (passes C14). The green is photographic,
  so excluded. Running page 2 is Museo Sans in 3–4 columns, 901 words.
- **ARC25:018** — Pastel background (full-page tint). The flowing line art is decorative vector,
  not pictorial, so not image-hero. **Teal title `(0,169,157)` on `(253,229,234)` = 2.45:1, below
  the C14 3:1 floor for display text: excluded.** Teal title plus teal line art make one cluster:
  one-accent.
- **ARC25:020** — Full-bleed sky photo, so image-hero. "Vision" is on a median of
  `(36,93,174)` = 6.46:1 (passes). **"Action" is on a median of `(121,177,224)` = 2.29:1, below
  3:1 (C14): excluded.** The fonts are ABC Arizona Flare / Arizona Text (flared serif), coded
  serif. The thin red arrow outline is 1 element under 0.5% (B5 fail): mono.
- **ARC25:029** — Slate background `(63,78,85)` is the background. The disc image starts at
  y = **20.9%** of H (58% of the area), which misses the top 20% (C1), so not image-hero; this is
  a borderline value, recorded. "Yearbook 2025" (Gothia Serif) sits top-left: plain-left. The
  running page (Foreword) is Fago Pro (sans), two text columns.
- **GH:019** — Page 1 carries the title "Assignment Report" (Libertinus Serif) plus 333 words of
  running text, so there's no separate cover.
- **GH:025** — The cover is framed by a full-page border (boxes on the running page as well).
  The running page (Executive Summary) carries a faint college-seal watermark: tint `#e5e5e5`
  vs white = **1.26:1 (≤ 1.3)**, and black body text on the tint = **16.7:1 (≥ 4.5)**. Both C32
  tests pass, so it is **not A3**: admissible, and the watermark is ignored for colour. Page 5
  is a contents page.
- **GH:058** — Title "本科生实验报告" in FandolSong-Bold (Song → serif). The university crest is
  a logo. Page 2 is a contents page; page 3 has 565 CJK characters.
- **GH:060** — Title in Book Antiqua Bold; the NUS logo is excluded. Page 4 is the first prose
  page (245 words, `<250`). Page 7 is a code listing, not prose. A rule under the running head
  gives rules.
- **GH:069** — Title "操作系统原理实验报告" in SimHei (Hei → sans); body SimSun (serif). The
  calligraphic university logo is an image logo. Page 2 is a contents page. Page 3 is sparse
  (`<250`).
- **GH:094** — The largest span, "C" at 56.7 pt, is a logo placeholder. The title is "[Project
  Title]" (LMRoman12-Bold, 20.1 pt), centred (+0.014W), in a rounded box 69% wide (< 80%, so not
  a rule). Pages 4–5 are contents; running page 3 (Acknowledgements) has a heading rule.
  3 families (LM Roman, LM Sans, Miama Nueva), which does not trip A1.
- **GH:104** — Page 1 holds the title plus 1,018 words in 2 columns. The grey abstract box
  `(229,230,229)` has **L = 0.900 (C29: ≤ 0.90 is a fill)** and covers about 12% of the page:
  fill-blocks (borderline, disclosed).
- **GH:129** — The Warwick purple field covers 40.5% of the cover: fill-blocks. The crest and
  wordmark on it are logos. The title sits below the purple field, not on it, so not band. The
  field's lower edge is full width, directly above the title block, about 2 body lines away:
  ruled (82a-cv rule 3, fill not behind the title). Running page (preview 2) has a bordered
  theorem box: boxes.
- **MSR:002** — Theme Aptos / Aptos. The pale blue panel `(238,246,255)` is L 0.967, a tint:
  mono. Title flush left.
- **MSR:003** — Theme Franklin Gothic Demi / Book. A full-bleed B&W city photo, so image-hero.
  The yellow panel `(253,232,0)` behind the title covers about 35%: fill-blocks.
- **MSR:005** — Theme Grandview. Blue `(11,29,210)` is the modal colour class, so it's the
  background; the title sits on the background. The duotone photo starts at y = 27% (not
  image-hero). Mono (hue 235°; not an A7 hex).
- **MSR:008** — Theme Franklin Gothic Demi / Book. The photo starts at y = **22.5%** of H, missing
  the top 20% (borderline), so not image-hero. The title is off-centre (+0.07W): plain-left.
  Navy title and navy dot-grid ornament form one cluster: one-accent.

## 4. Summary and sensitivity

- 16 coded: 14 admissible, 2 excluded (ARC25:018, ARC25:020; both C14/A6 on cover display text).
- Borderline values recorded, each within 10% of its threshold: GH:104 fill L 0.900;
  ARC25:029 image top 20.9%; MSR:008 photo top 22.5%; GH:060 running-page words 245.
- Sensitivity excluding GH:025 (exposure): n = 15, 13 admissible, 2 excluded.
