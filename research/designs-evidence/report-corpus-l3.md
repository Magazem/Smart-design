# Report / whitepaper — L3 juried: ARC Awards 2025 (MerComm); Mercury checked; authorities unreachable

Coder: Design Researcher. Retrieved 2026-09-23. Presence-based L3 (research/82 §2, §6 step 2): **no k/N, no share, no rank from this file**. Ranking Metric string for provenance rows: `award:ARC Awards:2025`, Evidence Class `juried`. Coded per §4/§5 + 82a. This file also covers **whitepaper**: no whitepaper corpus or award was found (R.6).

## R.1 Sources (all fetched 2026-09-23, curl -sL)
- ARC Awards home `https://www.arcawards.com` → 301 `https://www.mercommawards.com/arc.htm`. Category-winners index `https://www.mercommawards.com/arc/awardWinners/categoryWinners/{interior,design,pdf,cover,...}.htm` (2026 winners = company names only, no previews → not used).
- **2025 Grand Winners Book (Red Book)** `https://www.mercommawards.com/arc/arcmedia/ARCRedBook2025.pdf` (HTTP 200, 548 KB, 56 pp). Pages 6-56: one page per Grand/Best-of award = category, company, report title, report URL. Gallery page `https://www.mercommawards.com/arc/grandGallery.htm` carries the same list with `_viewlarger` report links. Red Book PDFs for 2008-2014 and 2019-2024 are also linked (not opened).
- Each report was coded from **the winner's own published report PDF (cover + first running-text page, rendered at 45-60 dpi into the system temp dir, never into the repo)**. Report URLs come from the Red Book. Award year 2025 = ARC 2025 competition (reports are FY2023/24).
- Mercury Excellence Awards: `https://www.mercommawards.com/mercury/awardWinners.htm` and `.../mercury/mercurymedia/NN_NNMRABlueBook.pdf` (2008-09 … 2018-19+) exist and fetch (18_19: HTTP 200, 775 KB, 22 pp). They are **text winner lists without design previews** and cover employee books, brochures etc., not chiefly annual reports (2018-19 Best of Show = Diehl Aviation "We are One" employee book) → **not coded**.

## R.2 Coded items (14)
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
