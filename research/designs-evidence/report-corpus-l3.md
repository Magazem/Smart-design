# Report / whitepaper — L3 juried: ARC Awards 2025 (MerComm); Mercury checked; authorities unreachable

Coder: Design Researcher. Retrieved 2026-09-23. Presence-based L3 (research/82 §2, §6 step 2): **no k/N, no share, no rank from this file**. Ranking Metric string for provenance rows: `award:ARC Awards:2025`, Evidence Class `juried`. Coded per §4/§5 + 82a. This file also covers **whitepaper**: no whitepaper corpus or award was found (R.6).

## R.1 Sources (all fetched 2026-09-23, curl -sL)
- ARC Awards home `https://www.arcawards.com` → 301 `https://www.mercommawards.com/arc.htm`. Category-winners index `https://www.mercommawards.com/arc/awardWinners/categoryWinners/{interior,design,pdf,cover,...}.htm` (2026 winners = company names only, no previews → not used).
- **2025 Grand Winners Book (Red Book)** `https://www.mercommawards.com/arc/arcmedia/ARCRedBook2025.pdf` (HTTP 200, 548 KB, 56 pp). Pages 6-56: one page per Grand/Best-of award = category, company, report title, report URL. Gallery page `https://www.mercommawards.com/arc/grandGallery.htm` carries the same list with `_viewlarger` report links. Red Book PDFs for 2008-2014 and 2019-2024 are also linked (not opened).
- Each report was coded from **the winner's own published report PDF (cover + first running-text page, rendered at 45-60 dpi into the system temp dir, never into the repo)**. Report URLs come from the Red Book. Award year 2025 = ARC 2025 competition (reports are FY2023/24).
- Mercury Excellence Awards: `https://www.mercommawards.com/mercury/awardWinners.htm` and `.../mercury/mercurymedia/NN_NNMRABlueBook.pdf` (2008-09 … 2018-19+) exist and fetch (18_19: HTTP 200, 775 KB, 22 pp). They are **text winner lists without design previews** and cover employee books, brochures etc., not chiefly annual reports (2018-19 Best of Show = Diehl Aviation "We are One" employee book) → **not coded**.

## R.2 Coded items (14)
**Superseded in part by R.8 (re-check under 82a round 3, 2026-09-24):** the running-text page and body features of ARC25:011, 013, 018 and 024 are recoded, and admissibility of 011, 012, 013, 018, 020 and 024 changes. The table below is the first coding, kept for audit.

Id = `ARC25:<Red Book page of first listing>`. `award` = Red Book category. Page coded: cover + first running-text page. Header treatment and heading class read from the **cover**; columns/body/rules/density from the **first running-text page**; colour from text/rules/marks/solid panels on both, page background and photos excluded (R.5).

| id | Report (org, title) and fetched PDF | award (Red Book) | columns | head | body | colour | header | rules | dens | cover | adm | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ARC25:014 | ADCB, "2024 Annual Report / Beyond the Finish Line" `https://www.adcb.com/en/multimedia/pdfs/2025/february/adcb-2024-annual-report-english.pdf` p.11 | Best of Interior Design – International | 3+ | sans | sans | one-accent | image-hero | rules | standard | yes | y | month timeline in 6 columns; red accent |
| ARC25:007 | Aktif Bank, "Shining Values, Empowered Tomorrows" `https://www.aktifbank.com.tr/api/uploads/2025061915353851523.pdf` p.3 | Best of Cover Design – Abstract; Best of Türkiye | 1 | display | sans | mono | image-hero | rules | airy | yes | y | chrome-star illustration ≈45% of cover; light display title |
| ARC25:012 | Fast Retailing, "Integrated Report 2024" `https://www.fastretailing.com/eng/ir/library/pdf/ar2024_en_sp.pdf` p.5 | Best of Chairman's Letter; Photography; Specialized | 1 | sans | sans | one-accent | image-hero | none | airy | yes | y | red on white; building photo ≈55% of cover |
| ARC25:036 | Granite Construction, "Sustainability Value Add" `https://www.graniteconstruction.com/sites/default/files/Granite_2024_Sustainability_Report.pdf` p.4 | Best of PDF Specialized – Americas/Europe | 2-equal | sans | sans | one-accent | image-hero | none | standard | yes | y | portrait photo + 2 text columns; green accent |
| ARC25:021 | Halkbank, "Integrated Annual Report 2024" `https://www.halkbank.com.tr/content/dam/corporate-website/en/documents/investor-relations/annual-reports/2024-Annual-report.pdf` p.11 | Best of Written Text – International | 3+ | sans | sans | fill-blocks | image-hero | none | standard | yes | y | navy full-height panel ≈40% + 3 text columns; child-photo cover |
| ARC25:013 | Hongkong & Shanghai Hotels, "Annual Report 2024" `https://www.hshgroup.com/-/media/files/hsh/investors/financial-results/2024/2024-annual-report-en.pdf` p.13 | Best of Interior Design – HK/PRC; Traditional – HK/PRC; Best of HK | 1 | serif | sans | one-accent | image-hero | rules | dense | yes | y | financial-highlights table; ornate rule header; small-caps serif title |
| ARC25:033 | Banca March, "Annual Report 2023" `https://www.bancamarch.es/informe-anual-2023/en/downloads/BancaMarch_AnnualReport_2023.pdf` p.5 | Best of PDF Version – Americas/Europe | 2-equal | sans | sans | fill-blocks | image-hero | none | standard | yes | y | grey panel behind text ≈55% of page; photo + 2 columns |
| ARC25:024 | Mission Investment Fund, "Many Pieces. One Purpose." `https://www.mif.elca.org/s/MIF40725_AnnualReport_2025_R4_nocrops.pdf` p.3 | Best of Non-Profit – International | 2-equal | serif | sans | one-accent | image-hero | boxes | standard | yes | y | mosaic illustration; outlined stat box over image; 3 families (serif, script, sans), not >3 |
| ARC25:018 | Petronas Dagangan, "Thriving Forward" `https://www.mymesra.com.my/integrated-report-2024/images/downloads/Petronas_Dagangan_Berhad_IR24.pdf` p.3 | Best of Infographics; Financial Data | 3+ | sans | sans | fill-blocks | image-hero | boxes | dense | yes | y | contents in 3 columns; pale teal panel ≈20% of page; faint gradient behind panel text (borderline A3, applied only to body paragraphs → admissible) |
| ARC25:011 | Petronas Gas, "Catalysing Growth, Shaping Tomorrow" `https://www.petronas.com/pgb/sites/default/files/2025-03/PGB%20Integrated%20Report%202024.pdf` p.3 | Best of Cover Design – Specialty; Best of Malaysia | 3+ | sans | sans | one-accent | image-hero | boxes | dense | yes | y | contents in 4 columns; teal bars |
| ARC25:010 | Urban Renewal Authority, "Annual Report 2023-24" `https://www.ura.org.hk/f/publication/7523/URA_annual_report_2023-2024_ENG.pdf` p.7 | Best of Cover Design – Non-Profit; Best of Non-Profit HK | 1 | sans | sans | multi | image-hero | none | standard | yes | **n** | **A4** fluid-paint/splatter-like cover graphic (borderline judgement) |
| ARC25:020 | California Water Service Group, "Vision → Action" (summary AR) `https://www.calwatergroup.com/_assets/_79993305ff43daa98d0fec842002d64b/calwatergroup/db/2510/24333/annual_report/2024+AR+final+-+single+pages.pdf` p.32 (via `https://tinyurl.com/CalWaterAR2024`) | Best of Written Text – USA | 2-equal | serif | serif | multi | image-hero | none | standard | yes | y | sky-photo cover; green serif heading; yellow chart bars; chart labels over blurred photo (chart, not body) |
| ARC25:037 | Uzabase, "Sustainability Report 2024" `https://files.microcms-assets.io/assets/c3cd69bb37354c7585915b242fdd0236/e90aa8a3bb4f4967967e83bd217eeca3/Uzabase_Sustainability%20Report_2024_EN.pdf` p.5 (via `https://tinyurl.com/25ARCUzabaseSR`) | Best of PDF Specialized – East Asia; Best of Japan | 2-sidebar | serif | sans | fill-blocks | image-hero | none | airy | yes | **n** | **A6** small white/teal text on #00a0a0 = 3.21:1 (`color.py`, sampled from render) |
| ARC25:029 | GRAWE Bankengruppe, "Yearbook 2025" `https://www.grawe-bankengruppe.at/media/file/2267_sectiond_GRAWE_BG_Yearbook_2025_KERN_ENG_FIN_WEB.pdf` p.10 (via `https://tinyurl.com/25ARCGRAWEBankengruppe`) | Best of Traditional – International; Best of Austria | 2-equal | serif | serif | mono | image-hero | none | standard | yes | y | slate cover with abstract ring art ≈40%; foreword page photo + 2 columns |

14 items coded, 12 admissible, 2 excluded. All from one competition (ARC 2025); several appear under 2-3 award listings (merged, coded once).

## R.3 Exclusions log
| id | rule | evidence |
|---|---|---|
| ARC25:010 | A4 | cover is a fluid-paint/splatter-like abstract graphic; judgement-borderline, second coder should check |
| ARC25:037 | A6 | `contrast_ratio('#ffffff','#00a0a0')` = 3.213 (<4.5) for small white text on the teal panel (teal text on white gives the same ratio); sampled from a 100-dpi render |

## R.4 Descriptive tally (presence only — not shares, not ranks)
**Superseded by R.8.4.** First-coding tally kept for audit.

Archetype `columns|heading|colour|header` : exemplars
- `3+|sans|one-accent|image-hero`: ADCB, PGB (2)
- `3+|sans|fill-blocks|image-hero`: Halkbank, PDB (2)
- `1|sans|one-accent|image-hero`: Fast Retailing
- `1|serif|one-accent|image-hero`: HSH
- `1|display|mono|image-hero`: Aktif
- `2-equal|sans|one-accent|image-hero`: Granite
- `2-equal|sans|fill-blocks|image-hero`: Banca March
- `2-equal|serif|one-accent|image-hero`: MIF
- `2-equal|serif|multi|image-hero`: California Water
- `2-equal|serif|mono|image-hero`: GRAWE
- excluded: `1|sans|multi|image-hero` (URA, A4); `2-sidebar|serif|fill-blocks|image-hero` (Uzabase, A6)

Header `image-hero` 14/14 and cover page `yes` 14/14: an artefact of award selection (jury-winning covers are photo/illustration-led) and of the cover-based header reading; the 4th identity feature is constant here, so effectively only columns/heading/colour discriminate. Body class: sans 12, serif 2 (Cal Water, GRAWE). Density: standard 8, dense 3 (HSH, PDB, PGB), airy 3 (Aktif, FR, Uzabase). Rules: none 8, rules 3 (ADCB, Aktif, HSH), boxes 3 (MIF, PDB, PGB).

L3 semantics (§6 step 2): all 12 admissible archetypes have one independent juried source (ARC 2025). Max 3 L3 designs may ship; nothing here ranks them among each other beyond §6's tie order (juried, then source count = 1 each, then key alphabetical).

## R.5 Ambiguities met (for 82a)
1. **What is "page 1" of a report?** §4 says code page 1, but a report's page 1 is a cover (photo, no columns). I coded header/heading from the cover and columns/body/rules/density from the first running-text page (first page ≥250 words, index ≥3). Needs an 82a clause; otherwise every report is `image-hero` and columns are unrecoverable.
2. **Colour use with photo covers/backgrounds:** page background and photos excluded, solid panels counted; a full-bleed slate cover (GRAWE) is background, not a fill.
3. **A3/C8 on covers:** titles set directly on a photo occur on nearly every cover; applying 82a C8 to covers would exclude almost all winners. I applied A3 only to body paragraphs of the coded running page (PDB disclosed as borderline).
4. **Heading class where a title mixes families** (Uzabase italic serif + bold sans): the largest word decides (serif).
5. Contrast: eye estimate everywhere except Uzabase (sampled); all estimates per 82a C9.
6. Some PDFs are spreads or 16:9 pages (Uzabase 1920×1080); the coded page is the dominant text page of the rendered page.

## R.6 Not fetched / unreachable (2026-09-23)
- Abbott (ARC Best of Show 2025) `abbottinvestor.com/static-files/…`: curl HTTP 000 (twice, two user agents).
- China Overseas Grand Oceans (403), People's Leasing & Finance `plc.lk` (302 → empty body), Bilibili ESG (404), Shiseido (HTML viewer), Dubai Taxi (Google Drive), Genesis Energy (indd.adobe.com viewer), ÖAMTC / Lotte / PT PGN LNG (tinyurl → Adobe Acrobat viewer HTML), Harbin Bank (pdf.js viewer HTML), Kanro (eir-parts PDF not tried), Porsche, IOM, Rusagro, Mubadala, China Unicom, Walmex (interactive web reports, no PDF). ARC 2026 category-winner pages list names only.
- Mercury: winner lists only, no design previews (R.1).
- **NISO Z39.18**: `niso.org/publications/z3918-2005-r2010` 404; `niso.org/publications/ansiniso-z3918-2005-r2010` 404; Wikipedia `ANSI/NISO_Z39.18` 404 (article absent). **APA 7**: `apastyle.apa.org/style-grammar-guidelines/paper-format/title-page` and `/font` blocked (Incapsula, ~1 KB body, also via WebFetch); Purdue OWL rejected; Scribbr 403; USC libguide 404. → **no authority source fetched for report/whitepaper structure; no `authority:` row can be written.** Nothing reconstructed from memory.
- **Whitepaper**: no corpus, no L3 award source found; per §10 whitepaper stays seeds + Shortfall (GitHub `whitepaper+template` belongs to the other worker).

## R.7 Second-coder handoff
Ids: `ARC25:007 010 011 012 013 014 018 020 021 024 029 033 036 037` (14). Sample per §7 / 82a C10 is family-wide (the GitHub report corpus ids join the pool later). The second coder needs R.5 (1) clarified first. Page chosen for the running-text coding (1-based): ADCB 11, Aktif 3, FR 5, Granite 4, Halkbank 11, HSH 13, March 5, MIF 3, PDB 3, PGB 3, URA 7, Cal Water 32, Uzabase 5, GRAWE 10.

## R.8 Re-check under 82a round 3 (C13, C14, C16), 2026-09-24

Re-checker: Design Researcher 2. All 14 winner PDFs were re-fetched on 2026-09-24 (`curl -sL`, HTTP 200 each) into the system temp dir. They were analysed with PyMuPDF: per-page word counts, cover text spans with their point size and fill colour, and page renders. Contrast was computed with `skill/document-design-intelligence/scripts/lib/color.py` `contrast_ratio`.

**Background sampling method:** the cover's text layer was removed with a text-only redaction (images and vector art kept), the page was re-rendered at 144 dpi, and every text span's own box was sampled on that text-free render against the span's exact PDF fill colour. The median over the box is the reported ratio. These are measurements from the published PDFs, not thumbnail estimates, except where "render-sampled" is noted (outlined text without a span).

### R.8.1 C13 page numbers (cover = PDF page 1; running page = first PDF page with ≥250 words of running text)

PDF page indices are 1-based. Several PDFs are two-page spreads; features are read from the physical page (spread half) that carries the running text, as in R.5 (6).

| id | cover | running page, first coding | running page per C13 | evidence |
|---|---|---|---|---|
| ARC25:007 Aktif | 1 | 3 | **3** confirmed | p2 = 3 words; p3 = 258 words of prose |
| ARC25:010 URA | 1 | 7 | **7** confirmed | p2-6 ≤174 words each; p7 = 354 |
| ARC25:011 PGB | 1 | 3 | **2** CHANGED | p2 "About this Report" = 398 words of prose (left page) |
| ARC25:012 FR | 1 | 5 | **5** confirmed | p2-4 ≤214 words; p5 = 286 prose |
| ARC25:013 HSH | 1 | 13 | **2** CHANGED | p2 = two prose blocks, 164 + 156 = 320 words (integrated-reporting note and cover note) |
| ARC25:014 ADCB | 1 | 11 | **11** confirmed (borderline) | p2-10 ≤182 words; p11 = 443 words in short highlight paragraphs, accepted as running text |
| ARC25:018 PDB | 1 | 3 | **2** CHANGED | p2 "Basis of this Report" = 503 words of prose (left page) |
| ARC25:020 Cal Water | 1 | 32 | **32** confirmed | p2-31 all <250 words (photo-led summary report); p32 = 392 |
| ARC25:021 Halkbank | 1 | 11 | **11** confirmed | p2 has 690 words, but 511 are the contents list; its prose ("About the Report") is 172 words < 250. p3-10 ≤103 |
| ARC25:024 MIF | 1 | 3 | **2** CHANGED | p2 = president's letter, 578 words (right page); p3 is the next spread |
| ARC25:029 GRAWE | 1 | 10 | **10** confirmed | p2-9 ≤207 words; p10 = 453 |
| ARC25:033 March | 1 | 5 | **5** confirmed | p2-4 ≤100 words; p5 = 383 |
| ARC25:036 Granite | 1 | 4 | **4** confirmed | p2-3 ≤175 words; p4 = CEO message, 440 words |
| ARC25:037 Uzabase | 1 | 5 | **5** confirmed | p2-4 ≤86 words; p5 = 270 prose |

The first coding used "first page ≥250 words, index ≥3" (R.5 (1)). C13 has no index floor, so four items move to PDF p2.

### R.8.2 Recode of body features for the four changed pages (cover-read features unchanged)

| id | columns | body | rules/boxes | density | colour (cover + running page) | notes |
|---|---|---|---|---|---|---|
| ARC25:011 PGB | 3+ → **2-equal** | sans | boxes → **rules** | dense (85 lines) | one-accent → **fill-blocks** | left page: wide intro block, then 2 flowing columns; rule under the running head; teal→green **gradient panel** behind the intro text ≥10% of page (gradients are fills, C17) |
| ARC25:013 HSH | 1 | sans | rules → **none** | dense → **airy** (~25 lines) | one-accent | two single-column prose blocks among photos |
| ARC25:018 PDB | 3+ → **2-equal** | sans | boxes | dense (119 lines, left page) | fill-blocks | physical left page = 2 columns (the spread has 4) |
| ARC25:024 MIF | 2-equal | sans | boxes → **none** | standard → **dense** (80 lines, right page) | one-accent | right page = letter in 2 columns; left page = illustration with a 3-line quote |

### R.8.3 C14 cover check (and A3/A6 on the new running pages)

Thresholds: title/display text on a photo must reach ≥4.5:1 under 24 pt and ≥3:1 at ≥24 pt (median over the span box). A3 applies to running text and to any text block of 3+ lines on a gradient, texture or photo.

| id | cover text on photo/texture (size, colour, median contrast) | C14 result | running-page check | admissible |
|---|---|---|---|---|
| ARC25:007 Aktif | 4-line title black on a flat light-grey ground (not a photo; the chrome star only touches the last line), 17.78 | pass | — | **y** (unchanged) |
| ARC25:010 URA | 6-line outlined title (no span) blue/green on the white part of the paint-flow image | not needed | — | n (A4, unchanged) |
| ARC25:011 PGB | 2-line title 45/42 pt white on green photo, 6.46 / 7.14; 9-11 pt labels ≥13 | pass | **p2: white running text on the teal→green gradient panel = A3; sampled 2.01:1 = A6** | **n** (was y) |
| ARC25:012 FR | tagline "LifeWear, Changing the World" 26.5 pt white on sky photo: **2.58 / 2.20** (need 3); "2024" 61.6 pt #e60012: 3.05 | **FAIL** | — | **n** (was y) |
| ARC25:013 HSH | "Annual Report 2024" 14 pt #886f52 on the faded photo ground #faf9f9: **4.498** (need 4.5; knife-edge) | FAIL (by 0.002) | **p2: white running text on sky photo = A3; sampled 2.03:1 = A6** | **n** (was y); A3/A6 on p2 make it robust to the knife-edge |
| ARC25:014 ADCB | 2-line title 34 pt white on red track photo, 5.22 / 5.06; 10 pt label 6.58 | pass | — | **y** (unchanged) |
| ARC25:018 PDB | labels "PETRONAS DAGANGAN BERHAD / INTEGRATED REPORT 2024" 9 pt #00a99d on iridescent texture: **2.41 / 2.40** (need 4.5); outlined title "THRIVING FORWARD" (≈43 pt, render-sampled) #00a99d: **2.53** (need 3) | **FAIL** | — | **n** (was y) |
| ARC25:020 Cal Water | "Vision" 51.9 pt 6.78; **"Action" 51.9 pt 2.92** (need 3); **"2024" 12.2 pt 4.07** (need 4.5); white on sky photo | **FAIL** | — | **n** (was y) |
| ARC25:021 Halkbank | 2-line title 44 pt #1b4778 on photo, 9.22 / 8.60; report label on a flat white disc | pass | — | **y** (unchanged) |
| ARC25:024 MIF | **3-line block** "MANY PIECES. / ONE PURPOSE. / Together, for good." on the gradient sky of the illustration = **A3**; contrast would pass (4.11-5.70 at 30-40 pt) | **FAIL (A3)** | p2 left page: 3-line quote on the illustration (A3 again) | **n** (was y) |
| ARC25:029 GRAWE | titles 30.5-35.2 pt #9d9d9c on flat slate (uniform ground), 3.18; 2-line blocks | pass | — | **y** (unchanged) |
| ARC25:033 March | "2023" 62 pt 4.01, "Annual Report" 23 pt 6.62; white on sea photo; 2 lines | pass | — | **y** (unchanged) |
| ARC25:036 Granite | single-line title 62 pt white on forest photo, 16.38 | pass | — | **y** (unchanged) |
| ARC25:037 Uzabase | titles pass by median (≥4.78); the 3-line subtitle on the photo is also A3 under C14 | (A3) | — | n (A6 on running page, unchanged; A3 added) |

**Admissibility after R.8: 6 of 14** (was 12). Newly excluded: 011 (A3, A6 running text), 012 (C14 A6), 013 (A3, A6 running text; C14 A6 knife-edge), 018 (C14 A6), 020 (C14 A6), 024 (C14 A3).

### R.8.4 Descriptive tally after R.8 (presence only: no shares, no ranks)

Archetype `columns|heading|colour|header`:
- **Admissible (6), all singletons:**
  - `1|display|mono|image-hero`: Aktif (007)
  - `3+|sans|one-accent|image-hero`: ADCB (014)
  - `3+|sans|fill-blocks|image-hero`: Halkbank (021)
  - `2-equal|sans|fill-blocks|image-hero`: Banca March (033)
  - `2-equal|sans|one-accent|image-hero`: Granite (036)
  - `2-equal|serif|mono|image-hero`: GRAWE (029)
- **Excluded (8):**
  - `2-equal|sans|fill-blocks|image-hero`: PGB (011), PDB (018)
  - `1|sans|one-accent|image-hero`: Fast Retailing (012)
  - `1|serif|one-accent|image-hero`: HSH (013)
  - `2-equal|serif|multi|image-hero`: Cal Water (020)
  - `2-equal|serif|one-accent|image-hero`: MIF (024)
  - `1|sans|multi|image-hero`: URA (010)
  - `2-sidebar|serif|fill-blocks|image-hero`: Uzabase (037)

**C16:** `header` = `image-hero` for 14 of 14 (6 of 6 admissible), so it is reported and kept; report archetypes are effectively 3-feature. **Cover page** = yes for 14 of 14.

**Variants over the 6 admissible** (codes from R.2, none recoded):
- body: sans 5, serif 1 (GRAWE)
- rules: rules 2 (ADCB, Aktif), none 4
- density: standard 5, airy 1 (Aktif)

§6 step 2 (L3, max 3): all 6 admissible designs have one juried source each (ARC 2025), so their relative order is by key alphabetical per §6. Any that code to a step-1 ranked archetype from the GH report corpus merge there.

### R.8.5 Notes and flags
1. **HSH cover title = 4.498:1**, a 0.002 miss. It is measured from the vector fill against the image pixel, not estimated. The exclusion does not depend on it: HSH's C13 running page (p2) sets white prose on a sky photo (A3, 2.03:1).
2. **ADCB p11** (short highlight paragraphs) is accepted as running text. If rejected, the next candidates are p12 (334 words, same style) and p14 (315), so the call recurs.
3. **Halkbank p2** passes the raw 250-word count only because of the contents list, so it is not running text. p11 is kept.
4. **Items file pages (82a C24):** `report-items.csv` carries a `pages` column `<cover>;<running page>` (1-based PDF page indices from R.8.1, e.g. `1;11`); page numbers only, no codes. preview_url = PDF `#page=1` (the cover).
5. A3 on covers (C14, 3+ line blocks) and on running pages newly removes MIF, PGB and HSH. Of the admissible set, only GRAWE and Aktif have multi-line cover blocks, and both sit on flat grounds.
6. `research/designs-evidence/report-items.csv` is written: 14 rows, id/name/url/preview_url only.
