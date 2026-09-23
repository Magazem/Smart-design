# Cover-letter corpus (L2): Microsoft Create cover-letters. LibreOffice `q=cover letter` is below the corpus floor (listed as corroboration)

Coder: Design Researcher 2 (Phase 4 first coder, research/82 §1: counts, never judges). Retrieved **2026-09-23**. Task F.a, no GitHub search API used: the `GH("cover letter template")` corpus from research/82 §10 is **not** in this file. It belongs to another worker, and the orchestrator merges the corpora. Conventions follow `brochure-corpus.md`, `deck-corpus-lo-ms.md`, and `letter-corpus-l2.md` §L.0, now ratified or overruled by **82a C17-C22** (research/82a-clarifications-4.md):
- a fill counts only if L ≤ 0.90;
- gradients count as fills;
- `band` needs header text on the band;
- UI chrome is ignored.
- **C22:** columns are counted in the body only; sender, recipient, date and reference blocks never make a sidebar.

Cover-letter identity archetype = `columns|heading|colour|header` (§4). Variants: body class, rules/boxes, density, **photo**. Family fail constraints C1-C6 (`ats-strict`) apply in addition to A1-A8 (§5).

Items file for second coders (82a C11): `research/designs-evidence/cover-letter-items-l2.csv` (id, name, url, preview_url only).

## CL.1 Sources

### Corpus MSC: Microsoft Create `cover-letters` (L2, catalogue prevalence)
- URL: `https://create.microsoft.com/en-us/templates/cover-letters`. `curl -sL -A "smart-design-research"` returned HTTP 200 after a redirect to `https://word.cloud.microsoft/create/en/cover-letter-templates/?source=create_flow`, the same vendor catalogue (82a C5). The items are present in the static payload (19 `office-template-grid-card` entries), so the catalogue is **reachable, not an SPA-only page**.
- Order: editorial page order, not a metric. There are 19 cards: 3 duplicate listings (same .docx) and 1 letterhead from another family (the "Playful letterhead", identical to MS letters pos 1). **N_MSC = 15** on-topic, all codeable (400-px webp thumbnail of page 1; 564-px for pos 9). The research/82 probe had seen 16.
- Ranking Metric string: `prevalence:ms-create-cover-letters:k/15`.

### LibreOffice `q=cover letter` (not coded, <10 on-topic, §2)
- URL: `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&q=cover%20letter&ord=download_d` (fetched as `q=cover+letter`), sort downloads, 2026-09-23. **5 items** in total. That is below the 10-item floor, so they are listed as corroboration only and not counted. Further cover-letter items surfaced only through `q=letter` (see letter-corpus-l2.md L.2b raw 028 Motivationsschreiben, raw 035 Covering letter in Phulkari Style). They are not part of this query and are not counted. Even with them the pool would be 7 (<10).

| pos | item | downloads | note |
|---|---|---|---|
| 1 | [Anschreiben Bewerbung / Bewerbungsschreiben](https://extensions.libreoffice.org/en/extensions/show/5684) | 8270 | listed, not coded (<10 on-topic, §2) |
| 2 | [Cover Letter (Sample)](https://extensions.libreoffice.org/en/extensions/show/cover-letter-sample) | 3942 | listed, not coded (<10 on-topic, §2) |
| 3 | [Bewerbung](https://extensions.libreoffice.org/en/extensions/show/bewerbung) | 2392 | listed, not coded (<10 on-topic, §2) |
| 4 | [Anschreiben Bewerbung um einen Ausbildungsplatz](https://extensions.libreoffice.org/en/extensions/show/5687) | 1354 | listed, not coded (<10 on-topic, §2) |
| 5 | [Indian Art Inspired Professional Resume & Cover Letter Template by MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99478) | 262 | listed, not coded (<10 on-topic, §2) |


Cross-family corroboration (not counted): MS **letters** category pos 18 "Simple yellow cover letter" (listed in letter-corpus-l2.md L.2a).

## CL.2 Raw list, MSC (page order)

| page pos | item | topic | decision |
|---|---|---|---|
| 001 | [ATS stylish accounting cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F1907b7c8-c14a-492f-a2d5-9dbf1d4f4b0d%2FTF1907b7c8-c14a-492f-a2d5-9dbf1d4f4b0de8eb85c2_wac-8e26c058836b.docx) | on-topic | coded MSC:001 |
| 002 | [ATS finance cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fe93a3c0c-ed4b-4c33-98b7-73b82ffa6397%2FTFe93a3c0c-ed4b-4c33-98b7-73b82ffa63973be95e49_wac-b09ed4e73b45.docx) | on-topic | coded MSC:002 |
| 003 | [Simple ATS healthcare cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F164be44f-892e-4713-b71c-e27c99934606%2FTF164be44f-892e-4713-b71c-e27c99934606a1e69a83_wac-1ea56f7f6808.docx) | on-topic | coded MSC:003 |
| 004 | [ATS healthcare cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F938d0510-ae51-479a-98d3-6a9fe5ba8c9f%2FTF938d0510-ae51-479a-98d3-6a9fe5ba8c9f2dfc8656_wac-c1d75b3fcf40.docx) | on-topic | coded MSC:004 |
| 005 | [ATS simple classic cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fe5418ab0-a274-4997-b880-24230d938372%2FTFe5418ab0-a274-4997-b880-24230d93837244b4c5ee_wac-b269760ac20c.docx) | on-topic | coded MSC:005 |
| 006 | [Simple UI/UX designer cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F91c3b989-adc7-42c3-99c5-6d8c7f3a5c0a%2FTF91c3b989-adc7-42c3-99c5-6d8c7f3a5c0a96fe9f4d_wac-b743f74833e5.docx) | on-topic | coded MSC:006 |
| 007 | [Geometric cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F1dd4b3a8-9564-4143-813b-da0628316a8c%2FTF1dd4b3a8-9564-4143-813b-da0628316a8cc224a050_wac-21c2e51b8da3.docx) | on-topic | coded MSC:007 |
| 008 | [Bold minimalist professional cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2Fc5c338b9-07e5-4fbb-8756-7ca403b33f5e-TF4c7b2ac9-91c8-45db-bd7a-d74fed2c5be2_wac.docx) | on-topic | coded MSC:008 |
| 009 | [Playful business cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F6158e9a0-e929-469e-b015-c5d218807bf2%2FTF6158e9a0-e929-469e-b015-c5d218807bf207de5c44_wac-e3b3318f230f.docx) | on-topic | coded MSC:009 |
| 010 | [Modern UI/UX designer cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F5c624cb4-bcf0-433e-8d06-329ca778a50b%2FTF5c624cb4-bcf0-433e-8d06-329ca778a50b88d4ca01_wac-15cd582a67a6.docx) | on-topic | coded MSC:010 |
| 011 | [Bold nursing cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fc0651bb6-b39b-4919-91c4-1b031ad4dc0c%2FTFc0651bb6-b39b-4919-91c4-1b031ad4dc0c7b68c311_wac-5b6e6f6f8e7c.docx) | on-topic | coded MSC:011 |
| 012 | [Bold minimalist professional cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2Fc5c338b9-07e5-4fbb-8756-7ca403b33f5e-TF4c7b2ac9-91c8-45db-bd7a-d74fed2c5be2_wac.docx) | duplicate | duplicate of pos 8 (same .docx) - not counted |
| 013 | [Bold food service cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F5559888d-e34b-4ae1-9505-bfe741291f71%2FTF5559888d-e34b-4ae1-9505-bfe741291f7136cca8fd_wac-4cb2b01aaf07.docx) | on-topic | coded MSC:013 |
| 014 | [Modern UI/UX designer cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F5c624cb4-bcf0-433e-8d06-329ca778a50b%2FTF5c624cb4-bcf0-433e-8d06-329ca778a50b88d4ca01_wac-15cd582a67a6.docx) | duplicate | duplicate of pos 10 (same .docx) - not counted |
| 015 | [Bold border professional cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2F9a5fea7e-6f20-4e6f-b4f1-784dc8193e1a-TF368c07a1-6af6-44f1-8c94-82280cb6067d_wac.docx) | on-topic | coded MSC:015 |
| 016 | [Playful business cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F6158e9a0-e929-469e-b015-c5d218807bf2%2FTF6158e9a0-e929-469e-b015-c5d218807bf207de5c44_wac-e3b3318f230f.docx) | duplicate | duplicate of pos 9 (same .docx) - not counted |
| 017 | [Playful letterhead](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F4f837650-9a96-434c-839f-bb412db5f497%2FTF4f837650-9a96-434c-839f-bb412db5f497fc7235ca_wac-997307308f9e.docx) | off-topic | other family: letter ("Playful letterhead", same template as MS letters pos 1 = MSL:001) - not counted here |
| 018 | [Stylish teaching cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fe41daea3-53c8-4ab5-9e9c-c7837b7c95cd%2FTFe41daea3-53c8-4ab5-9e9c-c7837b7c95cd693ce7f6_wac-4560152b6192.docx) | on-topic | coded MSC:018 |
| 019 | [Elegant graphic design cover letter](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F04bbacdc-34ff-4b89-ab9e-e5503f74b32a%2FTF04bbacdc-34ff-4b89-ab9e-e5503f74b32ac0910878_wac-51d285202be6.docx) | on-topic | coded MSC:019 |


## CL.3 Coded table (page 1; photo = variant)

| id | columns | head | body | colour | header | rules | dens | photo | adm | rule | note | preview |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MSC:001 | 1 | sans | sans | one-accent | ruled | rules | airy | no | y | - | Mint page fill #ddf1e8 sampled L=0.906 (>0.90 upper chromatic bound -> not a fill under Â§4 literal); green name + full-width green rule under contact line -> ruled. Sensitivity: if the mint page counted as fill -> fill-blocks | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/1907b7c8-c14a-492f-a2d5-9dbf1d4f4b0d/thumbnails/400/ats-stylish-accounting-cover-letter-green-modern-bold-0-1-5ee4429f9040.webp |
| MSC:002 | 1 | sans | sans | fill-blocks | plain-left | none | airy | no | y | - | Whole page #282828 (L=0.16) behind white text -> fill-blocks; no band distinct from page, no rule -> plain-left; ~29 lines (borderline airy/standard) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e93a3c0c-ed4b-4c33-98b7-73b82ffa6397/thumbnails/400/ats-finance-cover-letter-black-modern-bold-0-1-9c60a1f64423.webp |
| MSC:003 | 1 | sans | sans | fill-blocks | ruled | rules | airy | no | y | - | Navy page #2d2946 + violet right strip (text-free) -> fill-blocks; thin rule across the text area directly under contact line -> ruled | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/164be44f-892e-4713-b71c-e27c99934606/thumbnails/400/simple-ats-healthcare-cover-letter-purple-modern-bold-0-1-f2a48597ecee.webp |
| MSC:004 | 1 | sans | sans | fill-blocks | plain-left | none | standard | no | n | A3 | C22 recode: the left column holds only date, recipient and sender Contact blocks (header-type) -> body is 1 column; C1 withdrawn. Still EXCLUDED: pink-yellow-cyan gradient over the whole page behind body text (A3). Gradient counted as fill (C17) -> fill-blocks. Sparkle dingbats as block markers noted (C4 borderline, not needed) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/938d0510-ae51-479a-98d3-6a9fe5ba8c9f/thumbnails/400/ats-healthcare-cover-letter-modern-bold-0-1-ac2f0055b49b.webp |
| MSC:005 | 1 | serif | sans | one-accent | plain-left | rules | airy | no | y | - | Green serif name; vertical double page rules left and right (lines, not enclosed) -> rules | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e5418ab0-a274-4997-b880-24230d938372/thumbnails/400/ats-simple-classic-cover-letter-white-modern-simple-0-1-7b5cf015dbe5.webp |
| MSC:006 | 1 | sans | sans | one-accent | plain-left | rules | airy | no | y | - | C22 recode (was 2-sidebar, C1): right panel holds sender CONTACT + recipient blocks only -> header zone, body is 1 column. Panel #e9f5fe L=0.955 not a fill (C17). Rule under the name spans the main column only (not full-width) -> plain-left (borderline vs ruled) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/91c3b989-adc7-42c3-99c5-6d8c7f3a5c0a/thumbnails/400/simple-ui%252Fux-designer-cover-letter-blue-modern-simple-0-1-3001edaa3288.webp |
| MSC:007 | 1 | sans | sans | multi | plain-left | rules | airy | no | y | - | C22 recode (was 2-sidebar, C1): recipient address block left of the body -> header zone. Decorative diamond shapes est. ~6% of page -> not fill-blocks; yellow/teal/green -> multi | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/1dd4b3a8-9564-4143-813b-da0628316a8c/thumbnails/400/geometric-cover-letter-green-modern-geometric-0-1-50d18d9741ed.webp |
| MSC:008 | 1 | sans | sans | mono | plain-left | rules | airy | no | y | - | C22 recode (was 2-sidebar, C1): recipient block left of the body -> header zone. Cream page #fbf8f2 L=0.967 not a fill | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/4c7b2ac9-91c8-45db-bd7a-d74fed2c5be2/thumbnails/400/bold-minimalist-professional-cover-letter-modern-bold-0-1-cb03a6a20c06.webp |
| MSC:009 | 1 | sans | sans | fill-blocks | plain-left | none | standard | yes | n | C4 | C22 recode (was 2-equal, C1): the navy panel holds name, photo and sender contact only -> header zone, body 1 column; C1 withdrawn. Still EXCLUDED C4: location/phone/mail/globe icons as contact bullets. Circular photo; organic blobs not A4 | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/6158e9a0-e929-469e-b015-c5d218807bf2/thumbnails/564/playful-business-cover-letter-whimsical-color-block-0-1-89e774d9aa2b.webp |
| MSC:010 | 1 | sans | sans | fill-blocks | split | rules | standard | no | y | - | C22 recode (was 2-sidebar, C1): lavender panel #d3ccf7 (L=0.884, fill) carries sender name/contact only at the top -> header zone; body 1 column. Name right, contact left in the top strip -> split | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/5c624cb4-bcf0-433e-8d06-329ca778a50b/thumbnails/400/modern-ui%252Fux-designer-cover-letter-purple-modern-bold-0-1-b5bbdbd7b762.webp |
| MSC:011 | 1 | sans | sans | one-accent | ruled | rules | airy | yes | y | - | C22 recode (was 2-sidebar, C1): date + recipient block left of the body -> header zone. Circular headshot top right (photo=yes, variant); full-width rust rule under header -> ruled; page #fcfaeb L=0.955 not a fill | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/c0651bb6-b39b-4919-91c4-1b031ad4dc0c/thumbnails/400/bold-nursing-cover-letter-yellow-modern-bold-0-1-94d4535b5fdf.webp |
| MSC:013 | 1 | display | sans | one-accent | plain-left | rules | standard | no | y | - | C22 recode (was 2-sidebar, C1): CONTACT block (sender) left of the body -> header zone. Red stencil-cut name -> display; black top/bottom page bars (~2% each) not directly above the header block -> not ruled | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/5559888d-e34b-4ae1-9505-bfe741291f71/thumbnails/400/bold-food-service-cover-letter-yellow-modern-bold-0-1-0df70525bd5d.webp |
| MSC:015 | 1 | sans | sans | one-accent | plain-centered | boxes | airy | no | n | C6 | Navy page frame + contact in a 3-cell bordered table (layout table visible as a floating block -> C6); centred name; navy sampled ~#18303c (not an A7 hex) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/368c07a1-6af6-44f1-8c94-82280cb6067d/thumbnails/400/bold-border-professional-cover-letter-modern-simple-0-1-0991253dbbbe.webp |
| MSC:018 | 1 | serif | sans | one-accent | plain-left | none | airy | no | y | - | C22 recode (was 2-sidebar, C1): left panel ADDRESS/PHONE/EMAIL/WEBSITE = sender contact -> header zone. Panel #f1f8f6 L=0.96 not a fill; green serif name | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e41daea3-53c8-4ab5-9e9c-c7837b7c95cd/thumbnails/400/stylish-teaching-cover-letter-red-modern-simple-0-1-190240a4e68e.webp |
| MSC:019 | 1 | serif | sans | mono | plain-centered | rules | airy | no | y | - | Centred high-contrast serif caps name + script subtitle + sans body = 3 families (A1 needs >3); line-art flower bottom right (not A4); cream page L=0.967 not a fill | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/04bbacdc-34ff-4b89-ab9e-e5503f74b32a/thumbnails/400/elegant-graphic-design-cover-letter-whimsical-line-0-1-b2c1b2c64a8f.webp |


## CL.4 Exclusions log (A1-A8 + C1-C6), after the 82a C22 recode

| id | rule(s) | evidence |
|---|---|---|
| MSC:004 | A3 | full-page pink-yellow-cyan gradient behind the body text (C1 withdrawn by C22) |
| MSC:009 | C4 | location/phone/mail/globe icons used as contact bullets (C1 withdrawn by C22) |
| MSC:015 | C6 | contact details in a 3-cell bordered layout table (floating block) |

Excluded 3 of 15, leaving **12 admissible**. Before C22 it was 10 excluded and 5 admissible; see CL.11. No A6 pair fell near the threshold: white on #282828 and #2d2946 is evidently far above 4.5:1 (82a C9). No A7 hex was found.

## CL.5 Frequency table: MSC k/15, after C22 (share = admissible k / N; N includes the inadmissible items; C21)

| archetype `columns\|heading\|colour\|header` | k MSC all/adm | share MSC = adm/N | combined | K (adm) | exemplars | admissible modes: body ; rules ; density ; photo |
|---|---|---|---|---|---|---|
| `1\|sans\|one-accent\|ruled` | 2/2 | 2/15 = 0.133 | 0.1333 | 2 | MSC:001, MSC:011 | sans:2 ; rules:2 ; airy:2 ; no:1/yes:1 |
| `1\|serif\|one-accent\|plain-left` | 2/2 | 2/15 = 0.133 | 0.1333 | 2 | MSC:005, MSC:018 | sans:2 ; rules:1/none:1 ; airy:2 ; no:2 |
| `1\|display\|one-accent\|plain-left` | 1/1 | 1/15 = 0.067 | 0.0667 | 1 | MSC:013 | sans:1 ; rules:1 ; standard:1 ; no:1 |
| `1\|sans\|fill-blocks\|plain-left` | 3/1 | 1/15 = 0.067 | 0.0667 | 1 | MSC:002, MSC:004 (EXCL A3), MSC:009 (EXCL C4) | sans:1 ; none:1 ; airy:1 ; no:1 |
| `1\|sans\|fill-blocks\|ruled` | 1/1 | 1/15 = 0.067 | 0.0667 | 1 | MSC:003 | sans:1 ; rules:1 ; airy:1 ; no:1 |
| `1\|sans\|fill-blocks\|split` | 1/1 | 1/15 = 0.067 | 0.0667 | 1 | MSC:010 | sans:1 ; rules:1 ; standard:1 ; no:1 |
| `1\|sans\|mono\|plain-left` | 1/1 | 1/15 = 0.067 | 0.0667 | 1 | MSC:008 | sans:1 ; rules:1 ; airy:1 ; no:1 |
| `1\|sans\|multi\|plain-left` | 1/1 | 1/15 = 0.067 | 0.0667 | 1 | MSC:007 | sans:1 ; rules:1 ; airy:1 ; no:1 |
| `1\|sans\|one-accent\|plain-left` | 1/1 | 1/15 = 0.067 | 0.0667 | 1 | MSC:006 | sans:1 ; rules:1 ; airy:1 ; no:1 |
| `1\|serif\|mono\|plain-centered` | 1/1 | 1/15 = 0.067 | 0.0667 | 1 | MSC:019 | sans:1 ; rules:1 ; airy:1 ; no:1 |
| `1\|sans\|one-accent\|plain-centered` | 1/0 | 0/15 = 0.000 | 0.0000 | 0 | MSC:015 (EXCL C6) | n/a (no admissible exemplar) |


- Admissible: 12 items in 10 distinct archetypes. 2 archetypes have k≥2; 8 are singletons.
- **Coarsening (§4):** needs ≥15 admissible; there are 12, so **not triggered**.
- **C16 (non-discriminating feature):** after C22, `columns` = `1` for all 15 items. It is reported and kept; the archetypes are effectively 3-feature for cover-letter.
- Variant modes over the 12 admissible items are listed per archetype in the table. Photo = yes occurs once among admissible items (MSC:011). The other photo item, MSC:009, is excluded.

## CL.6 Provisional §6 order (this one corpus only; the orchestrator re-derives after merging GH)

There is no L3 source for cover-letter (§10: "—").

| order | step | archetype | share | K | exemplar (page pos) | tie-break |
|---|---|---|---|---|---|---|
| 1 | 1 (K≥2) | `1\|sans\|one-accent\|ruled` | 2/15 = 0.133 | 2 | MSC:001 (1), MSC:011 (11) | tie with row 2 at 0.133, single corpus → best native position 1 < 5 |
| 2 | 1 (K≥2) | `1\|serif\|one-accent\|plain-left` | 2/15 = 0.133 | 2 | MSC:005 (5), MSC:018 (18) | — |
| 3 | 3 (singleton) | `1\|sans\|fill-blocks\|plain-left` | 1/15 | 1 | MSC:002 (2) | native position (MSC:004 and 009 share the archetype but are excluded) |
| 4 | 3 | `1\|sans\|fill-blocks\|ruled` | 1/15 | 1 | MSC:003 (3) | native position |
| 5 | 3 | `1\|sans\|one-accent\|plain-left` | 1/15 | 1 | MSC:006 (6) | native position |
| 6 | 3 | `1\|sans\|multi\|plain-left` | 1/15 | 1 | MSC:007 (7) | native position |
| 7 | 3 | `1\|sans\|mono\|plain-left` | 1/15 | 1 | MSC:008 (8) | native position |
| 8 | 3 | `1\|sans\|fill-blocks\|split` | 1/15 | 1 | MSC:010 (10) | native position |
| 9 | 3 | `1\|display\|one-accent\|plain-left` | 1/15 | 1 | MSC:013 (13) | native position |
| 10 | 3 | `1\|serif\|mono\|plain-centered` | 1/15 | 1 | MSC:019 (19) | native position |

- Step 1 gives 2 (<5), so step 3 (ranked singletons) applies. 8 singletons bring the list to 10, the §6 cap.
- If the orchestrator keeps the single L4 convention slot (step 4), the cap is reached at row 9 and row 10 drops.
- The singleton order carries no popularity information (§13).
- Threshold case: MSC:001's mint page (L=0.906). Counted as a fill, it moves from row 1 to `1|sans|fill-blocks|ruled` (K=2 with MSC:003); MSC:011 then remains alone in row 1's archetype.

## CL.7 Bias statement
- **Microsoft Create** is Microsoft's editorial selection: the first static slice of one category page, 15 templates. It is heavily "designed-résumé" styled (side panels, tinted pages, photos). Page order is not a metric; it measures prevalence of curation, not usage.
- **After C22 the ATS filter removes 3 of 15** (A3, C4, C6). Before C22 it removed 10 via the side-column reading (CL.11).
- LibreOffice is below the corpus floor (5 items, mostly German Anschreiben). The GitHub developer/LaTeX corpus is absent here (another worker). Canva, Google and Apple are blocked (§13).
- Popularity is not quality; singletons are noise (§13).

## CL.8 Second-coder ids (82a C10/C11): the orchestrator draws the family-wide sample
All 15 coded ids, sorted: MSC:001, MSC:002, MSC:003, MSC:004, MSC:005, MSC:006, MSC:007, MSC:008, MSC:009, MSC:010, MSC:011, MSC:013, MSC:015, MSC:018, MSC:019. The ids are unchanged by the recode.

Not coded: MSC:012/014/016 (duplicates of 008/010/009) and MSC:017 (letterhead, another family). The GH cover-letter ids from the other worker must be added before `random.Random("82:cover-letter")` is drawn.

## CL.9 Ambiguities met
1. ~~Recipient/contact block in a narrow side column~~: **resolved by 82a C22** (header-zone blocks never make a sidebar). The interpretation question that remains is in CL.11.
2. **Page tints near L = 0.90**: MSC:001 (0.906, not a fill; C17 ratifies the threshold). MSC:006 (L=0.955) and MSC:018 (L=0.96) have pale panels that are not fills.
3. **Rule spanning only the main column** (MSC:006): coded not full-width, so `plain-left`.
4. **Top/bottom page bars separated from the header by white space** (MSC:013): not "directly above", so not `ruled`.
5. **Gradient page** (MSC:004): a fill (C17) and A3.

## CL.10 Files written
`research/designs-evidence/cover-letter-corpus-l2.md` (this file) and `research/designs-evidence/cover-letter-items-l2.csv` (unchanged by the recode). No library, designs or provenance CSVs were written (F.c, after the GH merge). No git, no loaders. Preview images were downloaded to the system temp dir only.

## CL.11 Recode under 82a C22 (2026-09-24)

C22 overrules coder rule (h). Columns are counted in the body only. Sender, recipient, date and reference blocks never make a column or sidebar. All 9 former C1 exclusions were re-examined. In each one the side column holds only header-type blocks (sender name, photo or contact; recipient address; date), so all 9 recode to `1` and C1 is withdrawn. The feature codes other than `columns` are unchanged.

| id | columns before | after | adm before (rules) | adm after (rules) | archetype before | archetype after |
|---|---|---|---|---|---|---|
| MSC:004 | 2-sidebar | 1 | n (A3; C1) | n (A3) | `2-sidebar\|sans\|fill-blocks\|plain-left` | `1\|sans\|fill-blocks\|plain-left` |
| MSC:006 | 2-sidebar | 1 | n (C1) | y (-) | `2-sidebar\|sans\|one-accent\|plain-left` | `1\|sans\|one-accent\|plain-left` |
| MSC:007 | 2-sidebar | 1 | n (C1) | y (-) | `2-sidebar\|sans\|multi\|plain-left` | `1\|sans\|multi\|plain-left` |
| MSC:008 | 2-sidebar | 1 | n (C1) | y (-) | `2-sidebar\|sans\|mono\|plain-left` | `1\|sans\|mono\|plain-left` |
| MSC:009 | 2-equal | 1 | n (C1; C4) | n (C4) | `2-equal\|sans\|fill-blocks\|plain-left` | `1\|sans\|fill-blocks\|plain-left` |
| MSC:010 | 2-sidebar | 1 | n (C1) | y (-) | `2-sidebar\|sans\|fill-blocks\|split` | `1\|sans\|fill-blocks\|split` |
| MSC:011 | 2-sidebar | 1 | n (C1) | y (-) | `2-sidebar\|sans\|one-accent\|ruled` | `1\|sans\|one-accent\|ruled` |
| MSC:013 | 2-sidebar | 1 | n (C1) | y (-) | `2-sidebar\|display\|one-accent\|plain-left` | `1\|display\|one-accent\|plain-left` |
| MSC:018 | 2-sidebar | 1 | n (C1) | y (-) | `2-sidebar\|serif\|one-accent\|plain-left` | `1\|serif\|one-accent\|plain-left` |

**Effect, from the generated tables:** admissible 5 → **12**. Archetypes with k≥2: 0 → 2 (`1|sans|one-accent|ruled`, `1|serif|one-accent|plain-left`, each 2/15 = 0.133). The §6 list goes from 5 singletons to 2 ranked + 8 singletons (CL.6).

**Interpretation flag (sensitivity).** C22's second sentence says "blocks *above the salutation*". In 8 of the 9 items the side-column block sits beside the salutation and first body lines, not above them. Only MSC:010's sidebar text lies wholly above the salutation. The main coding follows the rule's intent: header-type blocks never make a sidebar, wherever they sit (this matches the task instruction to recode the 9 exclusions). Under a strictly geometric reading, only MSC:010 would recode: admissible = 6, all singletons (`1|sans|one-accent|ruled`, `1|sans|fill-blocks|plain-left`, `1|sans|fill-blocks|ruled`, `1|serif|one-accent|plain-left`, `1|sans|fill-blocks|split`, `1|serif|mono|plain-centered`). Please confirm the reading.
