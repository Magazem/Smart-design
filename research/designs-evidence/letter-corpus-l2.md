# Letter corpus (L2): Microsoft Create letters + LibreOffice `q=letter` (thin, coded as L2), plus a DIN 5008 L3 presence entry

Coder: Design Researcher 2 (Phase 4 first coder, research/82 §1: counts, never judges). Retrieved **2026-09-23**. Task F.a, no GitHub search API used: the `GH("letter template")` L1 corpus from research/82 §10 is **not** in this file. It belongs to another worker, and the orchestrator merges the corpora. Conventions follow `brochure-corpus.md` and `deck-corpus-lo-ms.md`. Binding: research/82 and 82a C1-C23 (recoded 2026-09-24 under C19/C22, see L.13).

Letter identity archetype = `columns|heading|colour|header` (§4). Variants: body class, rules/boxes, density, **letterhead position** (§4 family table).

Items file for second coders (82a C11): `research/designs-evidence/letter-items-l2.csv` (id, name, url, preview_url only).

## L.0 Coder conventions used (82a C17-C21 RATIFIED these on 2026-09-24; C22 overruled the side-column reading, see L.13)

1. **"Non-white fill" (colour rule a).** A filled area counts only if its sampled HSL lightness is **L ≤ 0.90**. That is the upper bound of the §4 chromatic definition, and the "(chromatic or grey/black)" wording refers back to it. Paper tints with L > 0.90 (cream, pale lavender, pale grey page colours) are treated as paper. Fill areas were measured with PIL: the share of pixels with L ≤ 0.90 inside the fill region, as a share of the page. Items within about ±1.5 percentage points of the 10% line, or within 0.01 of L = 0.90, are marked **BORDERLINE** in the notes.
2. **Gradient fills count as fills** (they are filled areas, not photos). "Solid" is read as opaque, not as single-hue.
3. **Header treatment `band`** requires header text to sit on the band. A decorative strip at the page top with no header text on it is not a band. The band's fill uses the same L ≤ 0.90 test.
4. **`split`** is applied when the sender name/logo and the sender's meta or contact, or a document title, sit on opposite sides of the same top strip. The priority order image-hero > band > ruled > split > plain-centered > plain-left is kept. A right-aligned sender block with nothing opposite it falls through to `plain-left`: §4 has no right value.
5. **Letterhead position**: coded by the **82a C19** rule (ratified 2026-09-24; my original (d) branch differed and is superseded). The first match wins:
   - (a) a return-address line above the recipient → `address-window`;
   - (b) else sender text in the top 25% → `top-left` / `top-centered` / `top-right` by its alignment;
   - (c) else the sender logo in the top 25% → same;
   - (d) else the sender block's position is recorded in the note ("foot") and the item is coded `top-left`.
   Affected: LOL:039, recoded from top-centered to top-left. MSL:004 is foot-left and already coded top-left.
6. **A5 (≥3 identical decorative repeats)** is applied to identical discrete motifs: LOL:040 flowers, LOL:039 pennant strings. It is not applied to tessellated or confetti pattern bands (MSL:001, MSL:004) or to tile strips whose motifs differ (MSL:007). Brochure precedent: the LOB:004 chevron tabs (A5).
7. **Screenshot UI.** LibreOffice screenshots taken in edit mode show field shading, text-boundary lines, spell-check squiggles and, for LOL:043/044, a yellow application background. These are non-printing and are ignored; each case is disclosed per item.
8. Transparent PNG previews (LOL:040 and others) were composited on white before viewing.
9. Contrast: no body-text pair fell in the 3.5–5.5:1 band by eye, so no `contrast_ratio` sample was needed (82a C9). All colour hexes are thumbnail estimates.

## L.1 Sources

### Corpus MSL: Microsoft Create `letters` (L2, catalogue prevalence)
- URL: `https://create.microsoft.com/en-us/templates/letters`. `curl -sL -A "smart-design-research"` returned HTTP 200 after a redirect to `https://word.cloud.microsoft/create/en/letters-templates/?source=create_flow`, the same vendor catalogue (82a C5). The items are present in the static payload (`office-template-grid-card`), so the catalogue is reachable.
- Order: editorial page order, not a metric. The static slice holds **25 cards**; the research/82 probe had seen 18. Of these, 5 are newsletters (excluded per §10), 2 are duplicate listings of the same .docx, and 1 is a cover letter from another family. **N_MSL = 17** on-topic, all codeable (400-px webp thumbnail of page 1).
- Ranking Metric string: `prevalence:ms-create-letters:k/17`.

### Corpus LOL: LibreOffice Extensions, Templates tag, `q=letter` (numeric corpus with 10-39 on-topic items → thin, coded in full as L2)
- URL: `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&q=letter&ord=download_d`, plus `&start=30`. Sort `ord=download_d` (cumulative downloads since the 03-2020 migration). **47 raw items** (30 + 17).
- Full-text `q=` is noisy: 29 of the 47 raw items are off-topic (CD cases, calendars, CVs, cover letters, "Letter"-size paper). 18 are on-topic; 1 (raw 042) is an 82a C3 blank scaffold. **N_LOL = 17** coded.
- Previews: the un-scaled `/assets/screenshots/...` image from each detail page `/en/extensions/show/<id>`. Raw 032 and raw 046 have no screenshot, so their own published listing image (`/assets/logos/...ScaleMaxHeightWzMwMF0.png`, a page preview) was used (82a C6, disclosed).
- Ranking Metric string: `prevalence:libreoffice-letter:k/17` (thin L1 coded as L2 per §2). Downloads are recorded per item in L.2b.

### Fallbacks
Apache OpenOffice, Google and Apple are not retried here: research/82 already records them as blocked or 403.

## L.2a Raw list, MSL (page order)

| page pos | item | topic | decision |
|---|---|---|---|
| 001 | [Playful letterhead](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F4f837650-9a96-434c-839f-bb412db5f497%2FTF4f837650-9a96-434c-839f-bb412db5f497fc7235ca_wac-997307308f9e.docx) | on-topic | coded MSL:001 |
| 002 | [Eighties letterhead](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F4329e40b-b81f-476a-b62c-f739a569a669%2FTF4329e40b-b81f-476a-b62c-f739a569a6698e1e7393_wac-1f4aaebd024f.docx) | on-topic | coded MSL:002 |
| 003 | [Personal letterhead](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F8fbdc6f7-bf7d-4a1b-abb5-5bacb24e19b1%2FTF8fbdc6f7-bf7d-4a1b-abb5-5bacb24e19b1c13c9773_wac-0dc680514001.docx) | on-topic | coded MSL:003 |
| 004 | [Geometric letterhead](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Ffce73ec4-2dcb-47c6-bcef-59a463203574%2FTFfce73ec4-2dcb-47c6-bcef-59a46320357417bd1b5a_wac-cdc2a33f2199.docx) | on-topic | coded MSL:004 |
| 005 | [Letter (origin theme)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F4a052b60-6276-42c3-ab63-1fb296887155%2FTF4a052b60-6276-42c3-ab63-1fb29688715539ff760e_wac-d7cc4ea0967b.docx) | on-topic | coded MSL:005 |
| 006 | [Business letter (sales stripes design)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F0c8d491f-4710-463f-b965-b49a9c0730af%2FTF0c8d491f-4710-463f-b965-b49a9c0730afb9047d19_wac-672549f6beda.docx) | on-topic | coded MSL:006 |
| 007 | [Business letter (simple design)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fb30688e1-3cd6-47b6-b274-8c187e76b335%2FTFb30688e1-3cd6-47b6-b274-8c187e76b335e3a3e965_wac-eb5c722c16a6.docx) | on-topic | coded MSL:007 |
| 008 | [Modern shapes business thank you letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2F21a53c6a-a5dd-4871-9f11-6e6a4af6055f-TF7987fc24-101c-4c58-9f2c-254fb668b0e2_wac.docx) | on-topic | coded MSL:008 |
| 009 | [Formal business letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F9986a0d9-9022-4d2d-b6e2-32852f14bae5%2FTF9986a0d9-9022-4d2d-b6e2-32852f14bae548af8d5d_wac-5f738399055b.docx) | on-topic | coded MSL:009 |
| 010 | [Modern gradient business thank you letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2Fdf31c7fc-02b4-40de-a23e-4453537de87b-TF3a85a46f-724b-4467-9414-5b3133b618a1_wac.docx) | on-topic | coded MSL:010 |
| 011 | [Simple recommendation letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fae06e695-a394-4f8e-be0f-01ffd73cf975%2FTFae06e695-a394-4f8e-be0f-01ffd73cf9750aff8d18_wac-3797a3d684a4.docx) | on-topic | coded MSL:011 |
| 012 | [Recommendation letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F76ad3d87-3b5c-4230-a3bb-5bb73a958874%2FTF76ad3d87-3b5c-4230-a3bb-5bb73a95887405d2bfca_wac-14888d208edf.docx) | on-topic | coded MSL:012 |
| 013 | [Modern purple letter of recommendation](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2F5aa7cc5a-fda8-4421-9dd3-241c69b4a63f-TF3376f8e6-023c-4809-b2c9-0a00f0a6de36_wac.docx) | on-topic | coded MSL:013 |
| 014 | [Corporate recommendation letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fd4d84a9a-6b25-44c1-84c6-3ebbb1899fca%2FTFd4d84a9a-6b25-44c1-84c6-3ebbb1899fca53dfd088_wac-02f0c006bc4c.docx) | on-topic | coded MSL:014 |
| 015 | [Employee recommendation letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Faa0261c5-ea5f-44f5-820e-f69b5820c21a%2FTFaa0261c5-ea5f-44f5-820e-f69b5820c21a63b9a992_wac-343a4f63a0aa.docx) | on-topic | coded MSL:015 |
| 016 | [Modern brown letter of recommendation](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2Fd584d14a-c77e-4e80-8704-5510330817ee-TFbbff9495-fe34-4379-99a5-2d67e9702acb_wac.docx) | on-topic | coded MSL:016 |
| 017 | [Modern purple letter of recommendation](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2F5aa7cc5a-fda8-4421-9dd3-241c69b4a63f-TF3376f8e6-023c-4809-b2c9-0a00f0a6de36_wac.docx) | duplicate | duplicate of pos 13 (same .docx) - not counted |
| 018 | [Simple yellow cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2F37473a38-3b0a-498e-8cf0-cb8135c69d11-TFa74b1134-4885-4939-991e-5608944e55a5_wac.docx) | off-topic | other family: cover letter (Simple yellow cover letter) - corroboration in cover-letter file, not coded here |
| 019 | [General professional thank you letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F65dc06b1-73c4-4193-b259-f24cc2a513cc%2FTF65dc06b1-73c4-4193-b259-f24cc2a513cc31c963dc_wac-cb2e137788fc.docx) | on-topic | coded MSL:019 |
| 020 | [Modern shapes business thank you letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2F21a53c6a-a5dd-4871-9f11-6e6a4af6055f-TF7987fc24-101c-4c58-9f2c-254fb668b0e2_wac.docx) | duplicate | duplicate of pos 8 (same .docx) - not counted |
| 021 | [Corporate newsletter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F371fe1a1-54c3-477c-9fb2-1b14c284b079%2FTF371fe1a1-54c3-477c-9fb2-1b14c284b07930e7914f_wac-5853d426b899.docx) | off-topic | newsletter (excluded per research/82 §10: letters minus newsletters) |
| 022 | [Architecture newsletter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F463abd5c-3d84-43d5-baac-0a41cfac14d3%2FTF463abd5c-3d84-43d5-baac-0a41cfac14d355a1f33c_wac-d3687719b3e8.docx) | off-topic | newsletter (excluded per research/82 §10: letters minus newsletters) |
| 023 | [Landscaping newsletter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fb72b748c-ce40-4de7-8c0b-f2ae9b669eeb%2FTFb72b748c-ce40-4de7-8c0b-f2ae9b669eeb327b8f5e_wac-eded3b46056f.docx) | off-topic | newsletter (excluded per research/82 §10: letters minus newsletters) |
| 024 | [Realtor newsletter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F86e768be-2d8d-49c5-ad69-eb7cdf4a973d%2FTF86e768be-2d8d-49c5-ad69-eb7cdf4a973d5e60430e_wac-280b1d6b304a.docx) | off-topic | newsletter (excluded per research/82 §10: letters minus newsletters) |
| 025 | [School newsletter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Ff5b49e76-2031-4fce-852f-1185a53ea762%2FTFf5b49e76-2031-4fce-852f-1185a53ea762ce18ab24_wac-1c8c9908a65c.docx) | off-topic | newsletter (excluded per research/82 §10: letters minus newsletters) |

## L.2b Raw list, LOL (downloads desc, both pages)

| raw pos | item | downloads | topic | decision |
|---|---|---|---|---|
| 001 | [Briefvorlage DIN lang (DL)](https://extensions.libreoffice.org/en/extensions/show/briefvorlage-din-lang-dl) | 29054 | on-topic | coded LOL:001 |
| 002 | [Rechnungsvorlage DIN lang (DL)](https://extensions.libreoffice.org/en/extensions/show/5131) | 14381 | off-topic | other family: invoice (Rechnungsvorlage); not quote, not cross-listed |
| 003 | [Anschreiben Bewerbung / Bewerbungsschreiben](https://extensions.libreoffice.org/en/extensions/show/5684) | 8270 | off-topic | other family: cover letter (Anschreiben Bewerbung) - corroboration in cover-letter file |
| 004 | [Curriculum Vitae (Resume, CV) filets turquoise](https://extensions.libreoffice.org/en/extensions/show/4042) | 7071 | off-topic | other family: cv |
| 005 | [Newspaper-style (for Draw)](https://extensions.libreoffice.org/en/extensions/show/newspaper-style-newsletter-template-letter-size-two-sided) | 4660 | off-topic | other family: newsletter |
| 006 | [LibreLatex](https://extensions.libreoffice.org/en/extensions/show/librelatex) | 4531 | off-topic | multi-design suite (article/book/letter/report); first design = article; no screenshot either |
| 007 | [Business Document Templates](https://extensions.libreoffice.org/en/extensions/show/3881) | 4524 | on-topic | coded LOL:007 on first screenshot (block letter) |
| 008 | [Briefvorlage Schwarz-Weiss DIN](https://extensions.libreoffice.org/en/extensions/show/briefvorlage-schwar-weiss-din) | 4185 | on-topic | coded LOL:008 |
| 009 | [Cover Letter (Sample)](https://extensions.libreoffice.org/en/extensions/show/cover-letter-sample) | 3942 | off-topic | other family: cover letter - corroboration in cover-letter file |
| 010 | [Fensterbrief](https://extensions.libreoffice.org/en/extensions/show/fenster-brief-dl.ott-1) | 3815 | on-topic | coded LOL:010 |
| 011 | [Basic Personal Letter](https://extensions.libreoffice.org/en/extensions/show/basic-personal-letter-1) | 3450 | on-topic | coded LOL:011 |
| 012 | [MLA Paper](https://extensions.libreoffice.org/en/extensions/show/mla) | 3303 | off-topic | academic paper (MLA) |
| 013 | [Slim CD/DVD Jewel Case](https://extensions.libreoffice.org/en/extensions/show/slim-cd-dvd-jewel-case-cover-templates-letter) | 3224 | off-topic | CD case (Letter paper size) |
| 014 | [Graph papers](https://extensions.libreoffice.org/en/extensions/show/graph-papers) | 2556 | off-topic | graph paper |
| 015 | [Bewerbung](https://extensions.libreoffice.org/en/extensions/show/bewerbung) | 2392 | off-topic | other family: application pack (cover sheet/cover letter/CV) - corroboration in cover-letter file |
| 016 | [Curriculum Vitae (Resume, CV) Frigeri](https://extensions.libreoffice.org/en/extensions/show/4046) | 2275 | off-topic | other family: cv |
| 017 | [Calendar 2014](https://extensions.libreoffice.org/en/extensions/show/2014-libreoffice-themed-calendar-with-some-usa-holidays_7yhHXX5t) | 2073 | off-topic | calendar |
| 018 | [Goal-oriented budget](https://extensions.libreoffice.org/en/extensions/show/betterbudget-goal-oriented-budget-template) | 2010 | off-topic | budget |
| 019 | [Standard Manuscript Format](https://extensions.libreoffice.org/en/extensions/show/standard-manuscript-format) | 1947 | off-topic | manuscript |
| 020 | [Modern Curriculum Vitae (Resume, CV)](https://extensions.libreoffice.org/en/extensions/show/4047) | 1923 | off-topic | other family: cv |
| 021 | [Letter with headers and footer](https://extensions.libreoffice.org/en/extensions/show/575) | 1888 | on-topic | coded LOL:021 |
| 022 | [Company Letter](https://extensions.libreoffice.org/en/extensions/show/company-letter) | 1573 | on-topic | coded LOL:022 |
| 023 | [Anschreiben Bewerbung um einen Ausbildungsplatz](https://extensions.libreoffice.org/en/extensions/show/5687) | 1354 | off-topic | other family: cover letter - corroboration in cover-letter file |
| 024 | [Blank Comic Book - Free printable comic strip template](https://extensions.libreoffice.org/en/extensions/show/70044) | 1302 | off-topic | comic book |
| 025 | [Crossword](https://extensions.libreoffice.org/en/extensions/show/crossword) | 1260 | off-topic | crossword |
| 026 | [Task List Table](https://extensions.libreoffice.org/en/extensions/show/task-list-table) | 1199 | off-topic | task list |
| 027 | [Full Block US Letter Template](https://extensions.libreoffice.org/en/extensions/show/full-block-us-letter-template) | 1162 | on-topic | coded LOL:027 |
| 028 | [Motivationsschreiben Bewerbung](https://extensions.libreoffice.org/en/extensions/show/5165) | 1046 | off-topic | other family: motivation letter for a job application (cover letter) - corroboration in cover-letter file |
| 029 | [Letter Coloured DIN](https://extensions.libreoffice.org/en/extensions/show/briefvorlage-farbig-din) | 1009 | on-topic | coded LOL:029 |
| 030 | [Organizer/Filofax A5](https://extensions.libreoffice.org/en/extensions/show/a5-agenda-organizer-filofax) | 962 | off-topic | organiser refills |
| 031 | [2025](https://extensions.libreoffice.org/en/extensions/show/99274) | 671 | off-topic | greeting card / pattern |
| 032 | [Modified Block US Letter](https://extensions.libreoffice.org/en/extensions/show/modified-block-us-letter) | 531 | on-topic | coded LOL:032 (listing image as preview, 82a C6) |
| 033 | [Professional Business Letterhead Template by InDiFi MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99593) | 447 | on-topic | coded LOL:033 |
| 034 | [Origami CD Envelope](https://extensions.libreoffice.org/en/extensions/show/origami-cd-envelope) | 430 | off-topic | CD envelope |
| 035 | [Covering letter in Phulkari Style by MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99359) | 412 | off-topic | other family: covering letter (job) - corroboration in cover-letter file |
| 036 | [Bible verses sorted in Biblical order with notes!](https://extensions.libreoffice.org/en/extensions/show/bible-verses-sorted-in-a-biblical-with-notes) | 307 | off-topic | bible verse list |
| 037 | [Indian Art Inspired Professional Resume & Cover Letter Template by MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99478) | 262 | off-topic | other family: resume + cover letter pack - corroboration in cover-letter file |
| 038 | [Shipper's letter of instruction](https://extensions.libreoffice.org/en/extensions/show/shippers-letter-of-instruction-generic) | 239 | off-topic | shipping form (other family: form) |
| 039 | [Festive Event Management Letterhead Template by MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99480) | 233 | on-topic | coded LOL:039 |
| 040 | [Indian Art Inspired Professional Letterhead Template by MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99479) | 214 | on-topic | coded LOL:040 |
| 041 | [Scuba Diving Log Template](https://extensions.libreoffice.org/en/extensions/show/scuba-diving-log-template) | 184 | off-topic | dive log |
| 042 | [Letter to Someone](https://extensions.libreoffice.org/en/extensions/show/letter-to-someone) | 104 | on-topic | UNCODEABLE - 82a C3 blank scaffold (three lines: title, salutation, closing; no design content); removed from N |
| 043 | [Moderne brev](https://extensions.libreoffice.org/en/extensions/show/moderne-brev) | 95 | on-topic | coded LOL:043 |
| 044 | [Almindeligt brev](https://extensions.libreoffice.org/en/extensions/show/almindeligt-brev) | 61 | on-topic | coded LOL:044 |
| 045 | [Personal Letter with hyphenation](https://extensions.libreoffice.org/en/extensions/show/privatbrief-mit-sichtfenster-und-automatischer-silbentrennung) | none shown | on-topic | coded LOL:045 |
| 046 | [Optical Store Letterhead Template](https://extensions.libreoffice.org/en/extensions/show/optical-store-letterhead-template) | none shown | on-topic | coded LOL:046 (listing image as preview, 82a C6) |
| 047 | [Slim DVD Movie Jewel Case Cover Templates (Letter)](https://extensions.libreoffice.org/en/extensions/show/slim-dvd-movie-jewel-case-cover-templates-letter) | none shown | off-topic | DVD case (Letter paper size) |

## L.3 Coded table, MSL

| id | columns | head | body | colour | header | rules | dens | letterhead | adm | rule | note | preview |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MSL:001 | 1 | sans | sans | fill-blocks | ruled | rules | airy | top-left | y | - | Confetti illustration strip top + stripe bands at foot: L<=0.90 pixels ~11.6% of page incl. a little text -> fill-blocks (BORDERLINE vs multi). Name left, contact right with icons; full-width multi-segment rule under the header block -> ruled. Confetti = varied shapes (texture), A5 not applied | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/4f837650-9a96-434c-839f-bb412db5f497/thumbnails/400/playful-letterhead-pink-modern-simple-0-1-752282626aa3.webp |
| MSL:002 | 1 | sans | sans | multi | plain-left | none | airy | top-left | y | - | C22 recode (was 2-sidebar): sender name/company/address block in a narrow left column = header zone -> 1. Blue circle #4890e4, teal triangle, orange/red/purple shapes -> multi; shapes each <5% of page | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/4329e40b-b81f-476a-b62c-f739a569a669/thumbnails/400/eighties-letterhead-modern-geometric-0-1-16882fc53299.webp |
| MSL:003 | 1 | sans | sans | mono | plain-left | none | airy | top-left | y | - | Grey page #eae9e5 L=0.908 (>0.90, not a fill; BORDERLINE). Sender contact strip across the top starting at the left margin; sender name large at page foot-left. Date in a row-aligned left gutter -> 1 | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/8fbdc6f7-bf7d-4a1b-abb5-5bacb24e19b1/thumbnails/400/personal-letterhead-modern-simple-0-1-09097007a589.webp |
| MSL:004 | 1 | sans | sans | multi | plain-left | none | airy | top-left | y | - | Magenta/yellow/pink triangle mosaic band at top ~6.5% of page (no header text on it) -> not band, not fill-blocks; sender logo + address only at page foot-left -> C19 (d): top-left, foot noted. Tessellated band treated as pattern, A5 not applied | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/fce73ec4-2dcb-47c6-bcef-59a463203574/thumbnails/400/geometric-letterhead-purple-modern-geometric-0-1-98714187fdf3.webp |
| MSL:005 | 1 | sans | sans | one-accent | ruled | boxes | airy | top-left | y | - | Green line-art logo in a bordered box top-left; frame line along the top directly above the recipient block -> ruled; sender name/address in a bordered footer box -> boxes; script signature. Letterhead = sender logo top-left (sender text only at foot) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/4a052b60-6276-42c3-ab63-1fb296887155/thumbnails/400/letter-%2528origin-theme%2529-modern-simple-0-1-2bacdf5670fb.webp |
| MSL:006 | 1 | serif | sans | fill-blocks | band | rules | airy | top-centered | y | - | Navy #334c6c band with centred white serif caps name (top ~15%) + patterned navy foot band ~8% -> fill-blocks, band; rule above footer contact row | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/0c8d491f-4710-463f-b965-b49a9c0730af/thumbnails/400/business-letter-%2528sales-stripes-design%2529-modern-simple-0-1-608d728a6162.webp |
| MSL:007 | 1 | display | sans | multi | plain-left | none | airy | top-left | y | - | Pink page #fbe9ed L=0.949 not a fill. Rounded heavy display face for the company name; bottom tile strip of different motifs: L<=0.90 pixels 8.9% (cream tile excluded) -> not fill-blocks; blue/orange/yellow/green -> multi. Tiles carry different motifs (not A5) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/b30688e1-3cd6-47b6-b274-8c187e76b335/thumbnails/400/business-letter-%2528simple-design%2529-red-modern-simple-0-1-60bccb3933f3.webp |
| MSL:008 | 1 | serif | serif | one-accent | plain-left | none | airy | top-left | y | - | Green geometric blocks top-right and foot strip: fills with L<=0.90 ~4.8% of page -> not fill-blocks; green only -> one-accent. Green serif 'Thank You' is the largest heading | https://createcatalog.public.onecdn.static.microsoft/uploadedfiles/uploads/d002df76-7710-4e5a-8223-dce434770d68-modern-green-business-thank-you-letter-modern-corporate-shapes-0-1.webp |
| MSL:009 | 1 | sans | sans | mono | plain-left | none | airy | top-left | y | - | Lavender page #e1e3f2 L=0.916 (>0.90, not a fill). Sender name 'RIO BANK' top-left at ~21% height; recipient left / address right in the top strip (no title there) -> plain-left | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/9986a0d9-9022-4d2d-b6e2-32852f14bae5/thumbnails/400/formal-business-letter-green-modern-simple-0-1-04f06b27c292.webp |
| MSL:010 | 1 | sans | sans | fill-blocks | plain-left | none | airy | top-left | y | - | Cyan->blue->indigo gradient bands top (~8%) and foot (~18%) -> fill-blocks (gradient counted as fill, see coder conventions). No text on the gradient (not A3). A7 considered: gradient runs cyan #0098b2 -> blue-violet #2e03fe and is not the sole accent (teal heading) -> not applied, BORDERLINE | https://createcatalog.public.onecdn.static.microsoft/uploadedfiles/uploads/d9a58d87-bb8e-49ef-9c68-c60f4e4c66d1-modern-gradient-business-thank-you-letter-modern-gradient-corporate-0-1.webp |
| MSL:011 | 1 | sans | sans | one-accent | ruled | rules | airy | top-right | y | - | Cream page L=0.951. Olive #35351c caps contact block top-right with a full-width rule directly below -> ruled | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/ae06e695-a394-4f8e-be0f-01ffd73cf975/thumbnails/400/simple-recommendation-letter-green-modern-simple-0-1-43e522881bbb.webp |
| MSL:012 | 1 | sans | sans | one-accent | band | rules | airy | top-centered | y | - | Pale yellow key-pattern band behind the centred company name (pattern stops around the title = flat panel, admissible per 82a C8). Pattern pixels L<=0.90 7.9% -> not fill-blocks; yellow only -> one-accent. C22 recode (was 2-sidebar): recipient block in a narrow left column divided by a vertical rule = header zone -> 1 | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/76ad3d87-3b5c-4230-a3bb-5bb73a958874/thumbnails/400/recommendation-letter-gray-modern-bold-0-1-1b640566ff65.webp |
| MSL:013 | 1 | serif | serif | fill-blocks | split | none | airy | top-right | y | - | Navy/lavender shape band top (9.8%) + foot corners (3.3%) = 13% -> fill-blocks. Logo placeholder left, sender name/address right in the same strip -> split. Letterhead = sender text block (top-right) | https://createcatalog.public.onecdn.static.microsoft/uploadedfiles/uploads/31aa2595-7525-461d-b221-22d0e7919eb0-modern-purple-letter-of-recommendation-modern-shapes-circles-0-1.webp |
| MSL:014 | 1 | sans | sans | one-accent | plain-left | rules | airy | top-left | y | - | Navy #19183a company name top-left; C22 recode (was 2-sidebar): recipient + sender address in a narrow left column = header zone, body indented right -> 1; diagonal line hatch bottom-right (lines) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/d4d84a9a-6b25-44c1-84c6-3ebbb1899fca/thumbnails/400/corporate-recommendation-letter-blue-modern-geometric-linear-0-1-563b0001a32c.webp |
| MSL:015 | 1 | sans | sans | one-accent | plain-left | rules | airy | top-left | y | - | Grey page margin frame L=0.91 not a fill. Medium blue company name and labels (est. ~#3c50b4 from thumbnail; not an A7 hex); rule above a two-column footer; script signature (<=3 families) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/aa0261c5-ea5f-44f5-820e-f69b5820c21a/thumbnails/400/employee-recommendation-letter-blue-modern-simple-0-1-08f4a04d3ed5.webp |
| MSL:016 | 1 | serif | serif | fill-blocks | split | none | airy | top-left | y | - | Dark brown #3c271e surround 33% of page -> fill-blocks; sender block left, serif title right in the same strip -> split | https://createcatalog.public.onecdn.static.microsoft/uploadedfiles/uploads/0cb21d7d-80dd-4aba-b02d-641464bbfacd-modern-brown-letter-of-recommendation-modern-waves-corporate-0-1.webp |
| MSL:019 | 1 | sans | sans | mono | plain-left | none | airy | top-left | y | - | Pale blue logo square #daeff8 L=0.91 (not chromatic). Sender company block top row beside the logo; the large name is the recipient | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/65dc06b1-73c4-4193-b259-f24cc2a513cc/thumbnails/400/general-professional-thank-you-letter-blue-modern-simple-0-1-51d3afdb54fb.webp |

## L.4 Coded table, LOL

| id | columns | head | body | colour | header | rules | dens | letterhead | adm | rule | note | preview |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LOL:001 | 1 | sans | sans | mono | plain-left | rules | airy | address-window | y | - | DIN layout: underlined return-address line above the recipient field; sender block top-right; fold marks. Placeholder content only | https://extensions.libreoffice.org/assets/screenshots/z/briefvorlage-din-lang-dl_a8c53401-70c5-49a5-b579-249dab0efc82.png |
| LOL:007 | 1 | sans | sans | mono | plain-left | none | standard | top-left | y | - | First screenshot = block letter (package also ships memo and modified block; coded on the first). Edit-mode screenshot: grey/cyan field shading is non-printing UI; colour fringes are subpixel text rendering | https://extensions.libreoffice.org/assets/screenshots/948/block-letter-screenshot.png |
| LOL:008 | 1 | serif | sans | mono | plain-left | rules | airy | top-right | y | - | Sender block (blurred by the author) top-right with phone/@ glyph labels, info block with rule; bold serif recipient/subject; no return-address line visible -> not address-window | https://extensions.libreoffice.org/assets/screenshots/z/briefvorlage-schwar-weiss-din_61ef945b-c3b8-4b9b-a73d-33aa12453afc.jpeg |
| LOL:010 | 1 | sans | sans | mono | split | rules | airy | address-window | y | - | Sender name top-left (casual Comic-Sans-like face) with date/contact right in the same strip -> split; underlined return line above the recipient (Courier) -> address-window; bold sans subject is the largest heading. Families: casual + Verdana-like + Courier = 3 (A1 needs >3) | https://extensions.libreoffice.org/assets/screenshots/16/Untitled-2-v4.png |
| LOL:011 | 1 | serif | serif | mono | plain-left | none | standard | top-right | y | - | Sender block right-aligned top-right (Times/Baskerville-like); the hyperlink tint is anti-aliased only (max sample #b3b6df) -> mono | https://extensions.libreoffice.org/assets/screenshots/z/basic-personal-letter-1_bcd0ab55-9f94-4527-808b-2f25f9edd491.jpeg |
| LOL:021 | 1 | sans | sans | one-accent | split | none | airy | top-left | y | - | Low-res edit-mode screenshot (olive text-boundary frames and grey field shading are non-printing UI). Logo placeholder with red lettering + sender name left, slogan right -> split. Red is faint (BORDERLINE one-accent vs mono) | https://extensions.libreoffice.org/assets/screenshots/z/lettre-avec-entetes-et-champs-de-saisie-et-suite-de-lettre_7c4935d0-68e6-4f96-ba7d-bcf6419a8594.jpeg |
| LOL:022 | 1 | sans | sans | one-accent | ruled | boxes | standard | top-left | y | - | Condensed black+cyan logo left, company contact right, full-width blue rule under the header (ruled beats split). Cyan 185 deg and blue 213 deg are <30 deg apart -> one hue. Bordered footer box #dce7f3 (L=0.91, not a fill) -> boxes. Blue #3566a5 is not an A7 hex | https://extensions.libreoffice.org/assets/screenshots/z/company-letter_9a5f6484-449c-4897-af7f-6f8ec6dd1895.png |
| LOL:027 | 1 | sans | sans | mono | plain-left | none | standard | top-left | y | - | Full block, Arial-like throughout | https://extensions.libreoffice.org/assets/screenshots/16/Untitled-1-v11.png |
| LOL:029 | 1 | serif | sans | one-accent | plain-left | rules | airy | top-right | y | - | Colour twin of LOL:008 (same author): blue recipient name, subject, rule, fold marks. Blue sampled ~#3a5a7a-#487098 from a blurred JPEG: A7 (#156082/#4F81BD) NOT established - estimate, flagged for the second coder | https://extensions.libreoffice.org/assets/screenshots/z/briefvorlage-farbig-din_c997d1dd-fc99-4018-a07f-8017b3770e21.jpeg |
| LOL:032 | 1 | sans | sans | mono | plain-left | none | standard | top-right | y | - | Preview = the item's own published listing image (233x300; the detail page has no screenshot; 82a C6, disclosed). Red squiggles = spell-check UI; grey date shading = field UI | https://extensions.libreoffice.org/assets/logos/z/modified-block-us-letter__ScaleMaxHeightWzMwMF0.png |
| LOL:033 | 1 | sans | sans | multi | split | none | airy | top-left | y | - | Letterhead-only (no body text). Slate band top-right + foot band + green strips ~8.7% of page (L<=0.90 total 10.4% incl. text and the logo illustration) -> not fill-blocks (BORDERLINE); green/gold/orange -> multi. Company name+contact left, illustrated logo right -> split | https://extensions.libreoffice.org/assets/screenshots/6516/Professional_Business_Letterhead_Template.jpg |
| LOL:039 | 1 | sans | sans | multi | plain-left | none | airy | top-left | n | A5 | Letterhead-only. Strings of identical pennants (same shape/colour repeated many times) top-right and bottom-left -> A5. C19 recode (was top-centered): sender logo+name only at page foot, centred -> no sender element in the top 25% -> top-left, foot noted. Pale blue panel #e4f0f8 not a fill | https://extensions.libreoffice.org/assets/screenshots/6516/Maharashtra_Event_Management_Letterhead_pataka_design.png |
| LOL:040 | 1 | sans | sans | fill-blocks | split | boxes | airy | top-left | n | A5 | Preview PNG has transparency; composited on white before coding. 9 identical gold flower motifs in header and footer strips -> A5. Gold footer panel + logo box + motifs ~10.5% -> fill-blocks (BORDERLINE). Bordered gold logo box right, sender contact left -> split | https://extensions.libreoffice.org/assets/screenshots/6516/Letterhead_rajasthani_patterns.png |
| LOL:043 | 1 | sans | sans | mono | plain-left | none | airy | top-left | y | - | Yellow #f7f7bd fills the whole screenshot including outside the page boundary -> application background (non-printing UI), not a fill; grey lines around header/recipient frame are LibreOffice text boundaries (UI). Sensitivity: if the yellow were printed, colour=fill-blocks | https://extensions.libreoffice.org/assets/screenshots/z/moderne-brev_ec277545-8d27-4d78-b509-f7caa0e80894.png |
| LOL:044 | 1 | sans | mono | mono | plain-left | none | airy | top-left | y | - | Same author/UI as LOL:043. Bold Arial-like sender name top-left; body in Courier-like monospace; closing indented right | https://extensions.libreoffice.org/assets/screenshots/z/almindeligt-brev_889358a8-c4a3-4750-b7cb-bc7ec31c777a.png |
| LOL:045 | 1 | serif | serif | mono | plain-centered | rules | standard | address-window | y | - | Computer-Modern-like serif; sender name+address centred at the top; underlined return line above the recipient -> address-window; fold marks | https://extensions.libreoffice.org/assets/screenshots/z/privatbrief-mit-sichtfenster-und-automatischer-silbentrennung_d0577361-c3aa-4dcc-a1df-1320a6f4b689.png |
| LOL:046 | 1 | sans | sans | fill-blocks | plain-left | rules | airy | top-left | y | - | Preview = listing image (233x300, carries a third-party site watermark; 82a C6, disclosed). Page tint #d6e6f3 L=0.896 (<=0.90, BORDERLINE) -> fill-blocks; blue bars #2b6596/#408bca (not A7 hexes); eye watermark in the body area but no text over it in the preview (A3 not applied, BORDERLINE); icon-labelled contact lines | https://extensions.libreoffice.org/assets/logos/z/optical-store-letterhead-template__ScaleMaxHeightWzMwMF0.png |

## L.5 Exclusions log (universal A1-A8 only; letter has no family fail constraint in §5)

| id | rule | evidence |
|---|---|---|
| LOL:039 | A5 | Strings of identical pennants, repeated many times, top-right and bottom-left |
| LOL:040 | A5 | 9 identical gold flower motifs across the header and footer strips |

Excluded 2 of 34, leaving **32 admissible**. Checks considered but not applied, all disclosed in the item notes:
- A7 on MSL:010: a cyan→indigo gradient that is not the sole accent.
- A7 on LOL:029: blue sampled from a blurred JPEG, not established as an A7 hex. Flagged for the second coder.
- A3 on LOL:046: eye watermark in the body area, but the preview shows no text over it.
- A5 on MSL:001, MSL:004, MSL:007: pattern bands or differing tiles.
- A1: no item shows more than 3 families.
- A2: no emoji. Contact icons in MSL:001, LOL:008 and LOL:046 are pictograms, not emoji.

## L.6 Frequency table (k per corpus; share = admissible k / N; N includes inadmissible items; combined = unweighted mean over the 2 corpora in this file)

K and shares count **admissible exemplars only** (82a C21). One archetype has a mixed membership: `1|sans|multi|plain-left` has MSL:002 and MSL:004 admitted and LOL:039 excluded under A5, so K=2 (3 counting all exemplars).

| archetype `columns\|heading\|colour\|header` | k MSL all/adm | k LOL all/adm | share MSL = adm/N | share LOL = adm/N | combined | K (adm) | exemplars | admissible modes: body ; rules ; density ; letterhead |
|---|---|---|---|---|---|---|---|---|
| `1\|sans\|mono\|plain-left` | 3/3 | 6/6 | 3/17 = 0.176 | 6/17 = 0.353 | 0.2647 | 9 | LOL:001, LOL:007, LOL:027, LOL:032, LOL:043, LOL:044, MSL:003, MSL:009, MSL:019 | sans:8/mono:1 ; none:8/rules:1 ; airy:6/standard:3 ; top-left:7/address-window:1/top-right:1 |
| `1\|sans\|one-accent\|ruled` | 2/2 | 1/1 | 2/17 = 0.118 | 1/17 = 0.059 | 0.0882 | 3 | LOL:022, MSL:005, MSL:011 | sans:3 ; boxes:2/rules:1 ; airy:2/standard:1 ; top-left:2/top-right:1 |
| `1\|sans\|fill-blocks\|plain-left` | 1/1 | 1/1 | 1/17 = 0.059 | 1/17 = 0.059 | 0.0588 | 2 | LOL:046, MSL:010 | sans:2 ; rules:1/none:1 ; airy:2 ; top-left:2 |
| `1\|sans\|multi\|plain-left` | 2/2 | 1/0 | 2/17 = 0.118 | 0/17 = 0.000 | 0.0588 | 2 | LOL:039 (EXCL A5), MSL:002, MSL:004 | sans:2 ; none:2 ; airy:2 ; top-left:2 |
| `1\|sans\|one-accent\|plain-left` | 2/2 | 0/0 | 2/17 = 0.118 | 0/17 = 0.000 | 0.0588 | 2 | MSL:014, MSL:015 | sans:2 ; rules:2 ; airy:2 ; top-left:2 |
| `1\|serif\|fill-blocks\|split` | 2/2 | 0/0 | 2/17 = 0.118 | 0/17 = 0.000 | 0.0588 | 2 | MSL:013, MSL:016 | serif:2 ; none:2 ; airy:2 ; top-right:1/top-left:1 |
| `1\|serif\|mono\|plain-left` | 0/0 | 2/2 | 0/17 = 0.000 | 2/17 = 0.118 | 0.0588 | 2 | LOL:008, LOL:011 | sans:1/serif:1 ; rules:1/none:1 ; airy:1/standard:1 ; top-right:2 |
| `1\|serif\|one-accent\|plain-left` | 1/1 | 1/1 | 1/17 = 0.059 | 1/17 = 0.059 | 0.0588 | 2 | LOL:029, MSL:008 | sans:1/serif:1 ; rules:1/none:1 ; airy:2 ; top-right:1/top-left:1 |
| `1\|display\|multi\|plain-left` | 1/1 | 0/0 | 1/17 = 0.059 | 0/17 = 0.000 | 0.0294 | 1 | MSL:007 | sans:1 ; none:1 ; airy:1 ; top-left:1 |
| `1\|sans\|fill-blocks\|ruled` | 1/1 | 0/0 | 1/17 = 0.059 | 0/17 = 0.000 | 0.0294 | 1 | MSL:001 | sans:1 ; rules:1 ; airy:1 ; top-left:1 |
| `1\|sans\|mono\|split` | 0/0 | 1/1 | 0/17 = 0.000 | 1/17 = 0.059 | 0.0294 | 1 | LOL:010 | sans:1 ; rules:1 ; airy:1 ; address-window:1 |
| `1\|sans\|multi\|split` | 0/0 | 1/1 | 0/17 = 0.000 | 1/17 = 0.059 | 0.0294 | 1 | LOL:033 | sans:1 ; none:1 ; airy:1 ; top-left:1 |
| `1\|sans\|one-accent\|band` | 1/1 | 0/0 | 1/17 = 0.059 | 0/17 = 0.000 | 0.0294 | 1 | MSL:012 | sans:1 ; rules:1 ; airy:1 ; top-centered:1 |
| `1\|sans\|one-accent\|split` | 0/0 | 1/1 | 0/17 = 0.000 | 1/17 = 0.059 | 0.0294 | 1 | LOL:021 | sans:1 ; none:1 ; airy:1 ; top-left:1 |
| `1\|serif\|fill-blocks\|band` | 1/1 | 0/0 | 1/17 = 0.059 | 0/17 = 0.000 | 0.0294 | 1 | MSL:006 | sans:1 ; rules:1 ; airy:1 ; top-centered:1 |
| `1\|serif\|mono\|plain-centered` | 0/0 | 1/1 | 0/17 = 0.000 | 1/17 = 0.059 | 0.0294 | 1 | LOL:045 | serif:1 ; rules:1 ; standard:1 ; address-window:1 |
| `1\|sans\|fill-blocks\|split` | 0/0 | 1/0 | 0/17 = 0.000 | 0/17 = 0.000 | 0.0000 | 0 | LOL:040 (EXCL A5) | n/a (no admissible exemplar) |


**Coarsening check (§4), after C22:** 32 admissible items (≥15). Singleton admissible items: 8 of 32 = 25% (not >50%). Archetypes with k≥2: 8 (not <5). **Not triggered.**

**C16:** after C22, `columns` = `1` for all 34 letter items. It is non-discriminating, so it is reported and kept; the archetypes are effectively 3-feature for letter.

**Scope caveat.** The combined shares average **two** corpora. research/82 §10 also names `GH("letter template")` as the letter L1 primary. When the orchestrator adds it, combined = mean over 3 corpora and every value changes. The ordering below is provisional and local to this file.

## L.7 Provisional §6 order from these two corpora only, after C22 (orchestrator re-derives after merging GH)

| order | archetype | combined | K | tie-break applied |
|---|---|---|---|---|
| 1 | `1\|sans\|mono\|plain-left` | 0.2647 | 9 | — (+ L3 DIN 5008 authority row merges here, L.8) |
| 2 | `1\|sans\|one-accent\|ruled` | 0.0882 | 3 | — |
| 3 | `1\|serif\|one-accent\|plain-left` | 0.0588 | 2 | 6-way tie at 0.0588: no L1; equal L2 (combined) share; **in 2 corpora**; best native position MSL pos 8 |
| 4 | `1\|sans\|fill-blocks\|plain-left` | 0.0588 | 2 | in 2 corpora; best position MSL pos 10 |
| 5 | `1\|sans\|multi\|plain-left` | 0.0588 | 2 | 1 corpus; best position MSL pos 2 |
| 6 | `1\|serif\|mono\|plain-left` | 0.0588 | 2 | 1 corpus; best position LOL raw 8 (cross-corpus, see note) |
| 7 | `1\|serif\|fill-blocks\|split` | 0.0588 | 2 | 1 corpus; best position MSL pos 13 |
| 8 | `1\|sans\|one-accent\|plain-left` | 0.0588 | 2 | 1 corpus; best position MSL pos 14 |

Step 1 gives 8 ranked archetypes (≤ 10 − n_L3 − n_L4 = 9 with the DIN row merged and one L4 slot kept), so step 3 is not reached. The 8 admissible singletons are listed in L.6.

Note: the "best native position" tie-break compares positions across two different corpora for rows 6 and 7 (LOL raw 8 vs MSL pos 13). If the reviewer rejects a cross-corpus comparison and falls back to archetype code alphabetical, `1|serif|fill-blocks|split` sorts first and rows 6 and 7 swap. **Flag.**

## L.8 L3: DIN 5008 via a fetched secondary (authority; presence plus the geometry it states)

- **Secondary fetched 2026-09-23:** Sematre/typst-letter-pro, via raw files, not the search API.
  - `https://raw.githubusercontent.com/Sematre/typst-letter-pro/main/README.md` (HTTP 200): "A template for creating business letters following the DIN 5008 standard". The README cites Wikipedia DIN 5008, a Deutsche Post DIN 5008 template and edv-lehrgang.de.
  - `typst.toml`: `description = "DIN 5008 letter template for Typst."`, keywords `din5008`.
  - `src/lib.typ` (HTTP 200, 17,122 bytes) states the geometry.
- **Geometry as stated in `src/lib.typ`:**

| DIN 5008 form | header height | fold marks (from top) | address field | information block | other |
|---|---|---|---|---|---|
| Form A (`DIN-5008-A`) | 27 mm | 87 mm and 192 mm (87 + 105) | 85 mm wide × 45 mm tall, starting 20 mm from the left page edge | 75 mm wide, 20 mm gutter after the address field, 5 mm lower | hole mark at 148.5 mm; marks at 5 mm from the left edge |
| Form B (`DIN-5008-B`, the template's default) | 45 mm | 105 mm and 210 mm (105 + 105) | same | same | default margins left 25 mm, right 20 mm, top 20 mm, bottom 20 mm; reference-sign line 45.77 mm × 3 + 25 mm columns (175 mm total) |

- **Preview coded under the same §4 rubric** (for L3 merge only; not in any N): `https://raw.githubusercontent.com/Sematre/typst-letter-pro/main/template/thumbnail.png`. One column. Sender block right-aligned at the top, bold sans name (Source-Sans-like). Underlined return-address line above the recipient. Fold and hole marks. Black only. ~26 text lines.
  → `1|sans|mono|plain-left`. Variants: body sans, rules `rules` (return-line underline), density airy, **letterhead `address-window`**. Admissible (no A-rule applies).
- **Merge (§6 step 2):** the L3 design codes to `1|sans|mono|plain-left`, rank 1. It merges there as an extra provenance row, `authority:DIN 5008 via typst-letter-pro src/lib.typ`; the rank is unchanged and no L3 slot is used. **82a C23 resolves the earlier flag:** filling uses the archetype's modal letterhead (`top-left`, 7 of 9). The DIN 5008 geometry above applies to German-language letter doctypes' page format (address window, fold marks, margins) as an authority provenance row, not to the design's letterhead variant.
- DIN 5008 corroboration inside the corpus: LOL:001, LOL:010 and LOL:045 (`address-window`) plus the LO off-topic invoice raw 002 all name DIN lang or the window layout. For presence only.

## L.9 Bias statement

- **Microsoft Create** is Microsoft's editorial selection: the first static slice of one category page, 17 letters, mostly Word 2023-era "stationery" with decorative fills and pastel page tints. Page order is not a metric. It measures prevalence of curation, not usage.
- **LibreOffice `q=letter`** counts cumulative downloads since 03-2020. It favours pre-2020 items and has a European bias: 7 of 17 coded items are German/Danish/French, 3 use the DIN window layout. Author clustering: LOL:008/029 and LOL:043/044 are same-author pairs; LOL:033/039/040 come from the MKCL-KF batch. The full-text query is noisy (29 of 47 off-topic). Three coded LO previews are edit-mode screenshots (UI ignored) and two are small listing images.
- The two corpora look different: MS letters are colourful and decorated (7 of 17 fill-blocks or multi), while LO letters are mostly plain mono (8 of 17 mono). An equal-weight mean gives each catalogue half the vote whatever its size.
- The GitHub developer/LaTeX corpus is absent from this file (separate worker). Canva, Google and Apple are blocked (§13).
- Popularity is not quality. Singletons carry no information.

## L.10 Second-coder ids (82a C10/C11): the orchestrator draws the family-wide sample

All 34 coded ids, sorted: LOL:001, LOL:007, LOL:008, LOL:010, LOL:011, LOL:021, LOL:022, LOL:027, LOL:029, LOL:032, LOL:033, LOL:039, LOL:040, LOL:043, LOL:044, LOL:045, LOL:046, MSL:001, MSL:002, MSL:003, MSL:004, MSL:005, MSL:006, MSL:007, MSL:008, MSL:009, MSL:010, MSL:011, MSL:012, MSL:013, MSL:014, MSL:015, MSL:016, MSL:019.

Not coded: MSL:017/020 (duplicates), MSL:018 (cover letter), MSL:021-025 (newsletters), LOL raw 042 (C3 blank scaffold) and the 29 off-topic LO raw items. The GH letter ids from the other worker must be added before the seeded sample (`random.Random("82:letter")`) is drawn. The DIN L3 thumbnail is not in the sample (not a corpus item).

## L.11 Ambiguities met (for the second coder and for 82a)

1. ~~Letterhead position has no §4 decision rule~~: resolved by 82a C19 (L.0 #5).
2. **Fill threshold** (ratified by C17). Several page tints sit right at L = 0.90: MSL:001 (0.906, not a fill), MSL:003 (0.908), LOL:046 (0.896, a fill). A second coder judging "non-white" by eye would likely code the MSL:001 mint as a fill.
3. ~~Narrow left column holding the recipient/sender block~~: resolved by 82a C22. MSL:002, MSL:012 and MSL:014 are now `1` (L.13).
4. **Decorative strips at the top without header text** are `plain-left`, not `band` (MSL:004, MSL:010).
5. **Edit-mode LibreOffice screenshots** (LOL:007, LOL:021, LOL:043, LOL:044): UI chrome is ignored. The yellow background on LOL:043/044 is the most consequential call: if it were printed, both would be fill-blocks.
6. **A5 scope**: identical discrete motifs versus pattern bands (L.0 #6).
7. **Cross-corpus position tie-break** (L.7 note).

## L.12 Files written
`research/designs-evidence/letter-corpus-l2.md` (this file) and `research/designs-evidence/letter-items-l2.csv`. No library, designs or provenance CSVs were written: that is F.c, and it needs the GH corpus first. No git, no loaders. Preview images were downloaded to the system temp dir only.

## L.13 Recode under 82a C22 and C19 (2026-09-24)

- **C22** overrules coder rule (h): columns are counted in the body only, and sender, recipient, date and reference blocks never make a column or sidebar.
  - Letters have no C1 constraint, so admissibility is unaffected (32 of 34 admissible before and after).
  - Three items change `columns`: MSL:002 (sender block), MSL:012 (recipient block) and MSL:014 (recipient + sender address), each in a narrow left column.
- **C19** changes the letterhead value of LOL:039 (foot-centred sender → `top-left`, foot noted). MSL:004 changes only in its note text.

| id | columns before | after | letterhead before | after | archetype before | archetype after |
|---|---|---|---|---|---|---|
| LOL:039 | 1 | 1 | top-centered | top-left | `1\|sans\|multi\|plain-left` | `1\|sans\|multi\|plain-left` |
| MSL:002 | 2-sidebar | 1 | top-left | top-left | `2-sidebar\|sans\|multi\|plain-left` | `1\|sans\|multi\|plain-left` |
| MSL:004 | 1 | 1 | top-left | top-left | `1\|sans\|multi\|plain-left` | `1\|sans\|multi\|plain-left` |
| MSL:012 | 2-sidebar | 1 | top-centered | top-centered | `2-sidebar\|sans\|one-accent\|band` | `1\|sans\|one-accent\|band` |
| MSL:014 | 2-sidebar | 1 | top-left | top-left | `2-sidebar\|sans\|one-accent\|plain-left` | `1\|sans\|one-accent\|plain-left` |

**Effect, from the generated tables:**
- Before: 18 admissible archetypes, 6 with k≥2, 12 singleton items.
- After: 16 admissible archetypes, 8 with k≥2, 8 singleton items.
- Two archetypes are new at K=2: `1|sans|multi|plain-left` (MSL:002 + MSL:004) and `1|sans|one-accent|plain-left` (MSL:014 + MSL:015).
- `1|sans|one-accent|band` (MSL:012) is a singleton, replacing `2-sidebar|sans|one-accent|band`.
- Ranks 1-2 are unchanged. The ranked list grows from 6 to 8 (L.7).

**Sensitivity.** C22 says "blocks above the salutation". In MSL:002, MSL:012 and MSL:014 the header-type block sits beside the salutation/body rather than above it. Under a strictly geometric reading those three stay `2-sidebar`, and the ranked list reverts to the 6 archetypes of the first coding: `1|sans|mono|plain-left` 9, `1|sans|one-accent|ruled` 3, then four at K=2. The main coding follows the rule's intent (header-type blocks never make a sidebar). Flagged, together with the cover-letter file CL.11.
