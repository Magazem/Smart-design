# Brochure corpus — Microsoft Create brochures + LibreOffice brochure, one catalogue pool (L2) + D&AD presence (L3)

Coder: Design Researcher. Counts only (research/82 §1). Retrieved 2026-09-23. Brochure identity archetype = `panel count|heading|colour|header` (§4: panel count replaces columns). Variants: body class, rules/boxes, density. Conventions and resolved ambiguities follow `research/designs-evidence/deck-corpus-lo-ms.md`.

Header-treatment convention used in both files (same as the deck precedent, noted as an ambiguity): §4 says "image/illustration ≥30% of page area" for `image-hero` while inspecting only the top 20% of the page; I read it as **≥30% of the top-20% strip**, since ≥30% of the whole page could never sit in a 20% strip. Panel count / columns / colour use / density follow §4 literally.

## B.1 Sources
- **MS pool part:** `https://create.microsoft.com/en-us/templates/brochures` → `curl -sL` redirected (HTTP 200) to `https://word.cloud.microsoft/create/en/brochure-templates/?source=create_flow`. Order: editorial page order, no metric. 10 cards rendered, **9 distinct templates** (pos 2 and pos 6 are the same .docx "Vivid shapes event brochure"; counted once at the first position). One thumbnail per template (page 1 = outside spread); nothing rendered/opened. research/82 probe found 7; the page now shows 9.
- **LO pool part:** `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&q=brochure&ord=download_d` (Tags=118 Templates + `q=brochure`, sort `ord=download_d`, retrieved 2026-09-23). 5 results, downloads in the raw list below. Full-text `q=` is noisy but returned only brochure items here.
- **Pool:** MS 9 + LO 5 = **N = 14 on-topic, all codeable** (≥10 on-topic → coded as a corpus, §2). Ranking Metric string per §2: `prevalence:ms-create+libreoffice-brochures:k/14`.
- Not counted: LO `q=flyer` item 5049 "Dépliant en trois colonnes" (a three-column leaflet, 1358 downloads) was found only through the flyer query; the pool is defined by the `q=brochure` query, so it is listed here as corroboration, not coded.

## B.2 Raw list (pool order: MS page order, then LO downloads desc)
| id | Item | Metric | Topic | Note |
|---|---|---|---|---|
| MSB:001 | [Builder brochure](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F297974e9-b9f1-4be1-86f8-e553dfc63e31%2FTF297974e9-b9f1-4be1-86f8-e553dfc63e314029b876_wac-dad66241be3d.docx) | page pos 1 | on-topic |  |
| MSB:002 | [Vivid shapes event brochure](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2F235f5dfd-a39b-4959-8326-e0c0315f421b-TFe0c14857-3445-4099-8631-c6b192707317d62f1be5_wac.docx) | page pos 2 | on-topic | same .docx as pos 6, counted once |
| MSB:003 | [Restaurant brochure](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F9fd05068-e911-4e84-ae1b-fe520008b360%2FTF9fd05068-e911-4e84-ae1b-fe520008b360688dc808_wac-00ce4a467f73.docx) | page pos 3 | on-topic |  |
| MSB:004 | [Booklet](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F6aa5002e-71ac-43cc-9433-ce182d56372a%2FTF6aa5002e-71ac-43cc-9433-ce182d56372ab1ea410d_wac-64fd99966f0b.docx) | page pos 4 | on-topic |  |
| MSB:005 | [Architecture brochure](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fe7603f86-38bf-4615-bfef-b7733563dc17%2FTFe7603f86-38bf-4615-bfef-b7733563dc173b1b88ff_wac-80c6047ec3b9.docx) | page pos 5 | on-topic |  |
| MSB:007 | [Travel brochure](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fbd00b536-5615-4700-9a3e-fa0943a369f8%2FTFbd00b536-5615-4700-9a3e-fa0943a369f8e90d5106_wac-7abf8ad0e654.docx) | page pos 7 | on-topic |  |
| MSB:008 | [Color block event brochure](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fc8366172-6db0-48b1-8abb-ede6c98417b8%2FTFc8366172-6db0-48b1-8abb-ede6c98417b8f0afca64_wac-6481f77df973.docx) | page pos 8 | on-topic |  |
| MSB:009 | [Sports event program brochure](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2Fa72a258f-fe8f-424a-8486-73f7aea695ce-TFdaee7e18-6320-4841-b316-eafa9593d3af_wac.docx) | page pos 9 | on-topic |  |
| MSB:010 | [Product launch event brochure](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fuploadedfiles%2Fuploads%2Fd4023b59-ae3a-4c72-b0d7-a7ad672148c4-TF4c68df17-4d14-4f7f-938b-e4ca86cbd681_wac.docx) | page pos 10 | on-topic |  |
| MSB:006 | Vivid shapes event brochure (duplicate listing) | page pos 6 | duplicate of MSB:002 | not counted |
| LOB:001 | [Three Panel Brochure for LibreOffice Draw](https://extensions.libreoffice.org/en/extensions/show/three-panel-brochure) | 3692 downloads | on-topic |  |
| LOB:002 | [3 Column basic Brochure](https://extensions.libreoffice.org/en/extensions/show/3-column-basic-brochure-pamphlet) | 1854 downloads | on-topic |  |
| LOB:003 | [Brochure, 3-fold](https://extensions.libreoffice.org/en/extensions/show/brochure-3-fold-simple-8.5x11-.5-margins-1-gutters) | 1403 downloads | on-topic |  |
| LOB:004 | [Real Estate Brochure/Flyer](https://extensions.libreoffice.org/en/extensions/show/real-estate-brochure-flyer) | 1129 downloads | on-topic | also returned by q=flyer; counted here (title names brochure) |
| LOB:005 | [Brochure 3p](https://extensions.libreoffice.org/en/extensions/show/brochure_3p_drawa4) | 762 downloads | on-topic |  |

On-topic decisions: all 14 are brochure/pamphlet templates (MS category "brochures"; LO title/description names a brochure or fold). No off-topic item in either list. Business cards, newsletters etc. do not occur.

## B.3 Coded table
Panel count values per §4: `2`, `3`, `4+`, `single-sheet`. `dens` = text lines on the outside spread normalised to A4 (≥55 dense, ≤30 airy). Preview column: first preview image used.

| id | panels | head | body | colour | header | rules | dens | adm | reason / note | preview |
|---|---|---|---|---|---|---|---|---|---|---|
| MSB:001 | 3 | sans | sans | fill-blocks | image-hero | rules | airy | y | house photo ~35% of header strip | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/297974e9-b9f1-4be1-86f8-e553dfc63e31/thumbnails/400/builder-brochure-blue-modern-simple-0-1-836c70b1099d.webp |
| MSB:002 | 3 | sans | sans | fill-blocks | image-hero | none | airy | y | blob illustrations ~45% of header strip; blob shapes not treated as A4 paint-swipe (borderline). Listed twice on the page (pos 2 and 6, same .docx) - counted once | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e0c14857-3445-4099-8631-c6b192707317/thumbnails/400/vivid-shapes-event-brochure-blue-modern-color-block-0-1-e1989f71f3e9.webp |
| MSB:003 | 3 | sans | sans | fill-blocks | image-hero | boxes | airy | y | spice photo ~33% of header strip | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/9fd05068-e911-4e84-ae1b-fe520008b360/thumbnails/400/restaurant-brochure-black-modern-simple-0-1-bb68632be08a.webp |
| MSB:004 | 2 | sans | sans | fill-blocks | plain-left | none | airy | n | EXCLUDED A4 yellow brush-stroke scribble behind the title; two-page booklet spread | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/6aa5002e-71ac-43cc-9433-ce182d56372a/thumbnails/400/booklet-yellow-modern-bold-0-1-2995c75fbb63.webp |
| MSB:005 | 3 | sans | sans | fill-blocks | image-hero | rules | airy | y | city photo ~33% of header strip; white on orange sampled 4.51:1 (pull quote) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e7603f86-38bf-4615-bfef-b7733563dc17/thumbnails/400/architecture-brochure-orange-modern-geometric-0-1-2c4b108467e3.webp |
| MSB:007 | 3 | sans | sans | fill-blocks | plain-left | rules | airy | y |  | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/bd00b536-5615-4700-9a3e-fa0943a369f8/thumbnails/400/travel-brochure-purple-modern-simple-0-1-dedbd74445fd.webp |
| MSB:008 | 3 | sans | sans | fill-blocks | band | none | airy | y | yellow band behind title | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/c8366172-6db0-48b1-8abb-ede6c98417b8/thumbnails/400/color-block-event-brochure-yellow-modern-simple-0-1-dc50cd7c4895.webp |
| MSB:009 | 3 | sans | sans | fill-blocks | image-hero | rules | airy | y | duotone swimmer photo; blob shapes not treated as A4 (borderline) | https://createcatalog.public.onecdn.static.microsoft/uploadedfiles/uploads/fabbbeae-2bfd-4349-a67b-25f75106da31-sports-event-program-brochure-red-vintage-retro-0-1.webp |
| MSB:010 | 3 | sans | sans | fill-blocks | image-hero | none | airy | y | sunburst illustrations + circular photos in header strip | https://createcatalog.public.onecdn.static.microsoft/uploadedfiles/uploads/5006494d-666f-4ff9-a2d6-3497e61d2379-product-launch-event-brochure-blue-modern-geometric-linear-0-1.webp |
| LOB:001 | 3 | sans | sans | one-accent | plain-centered | boxes | airy | y | preview is a LibreOffice Draw window showing empty cyan frames labelled inside flap/back/cover (scaffold, no typography) | https://extensions.libreoffice.org/assets/screenshots/z/three-panel-brochure_886352a3-8012-40dc-b57b-6be6368ed772.png |
| LOB:002 | 3 | serif | serif | mono | plain-centered | none | airy | y | preview is a blank scaffold with three tiny serif labels | https://extensions.libreoffice.org/assets/screenshots/16/Screenshot_20200529_010607.png |
| LOB:003 | 3 | sans | serif | mono | plain-centered | none | standard | y | placeholder Latin text in left panel (~45 lines); dashed fold guides treated as non-printing | https://extensions.libreoffice.org/assets/screenshots/z/brochure-3-fold-simple-8.5x11-.5-margins-1-gutters_f3b108e9-85cd-4db3-add1-bca19e546ebf.png |
| LOB:004 | single-sheet | sans | sans | multi | image-hero | rules | standard | n | EXCLUDED A5 4 identical chevron tabs in left strip; A4 real-estate sheet, two pages; cross-listed to flyer | https://extensions.libreoffice.org/assets/screenshots/z/real-estate-brochure-flyer_7980c33f-11a4-43ae-9cfa-9658851cdb57.png |
| LOB:005 | 3 | sans | sans | one-accent | plain-centered | boxes | airy | y | scaffold: empty green frames labelled inside flap/back/cover | https://extensions.libreoffice.org/assets/screenshots/z/brochure_3p_drawa4_41fd33e9-b60f-4a8e-8cea-3eab0b94bf39.png |

## B.4 Exclusions log

| id | rule | evidence |
|---|---|---|
| MSB:004 | A4 | A4 yellow brush-stroke scribble behind the title |
| LOB:004 | A5 | A5 4 identical chevron tabs in left strip |

Excluded 2 of 14 → **12 admissible**. Fail constraints C8 (brochure/flyer/poster: A6 at 3:1 / gradient banding) checked: body-text contrast sampled with `color.py` `contrast_ratio` from 400-px thumbnails for the MS items (lowest 4.5:1 on a white-on-orange pull quote; the yellow-panel sample read 4.28 on an anti-aliased pixel, the real text is near-black) — none excluded. Sampling is from compressed thumbnails, so values are estimates.

## B.5 Frequency table — pool k/14 (denominator includes inadmissible items)

| archetype `panels\|heading\|colour\|header` | k | share | exemplars |
|---|---|---|---|
| `3\|sans\|fill-blocks\|image-hero` | 6 | 6/14 = 0.429 | MSB:001, MSB:002, MSB:003, MSB:005, MSB:009, MSB:010 |
| `3\|sans\|one-accent\|plain-centered` | 2 | 2/14 = 0.143 | LOB:001, LOB:005 |
| `3\|sans\|fill-blocks\|band` | 1 | 1/14 = 0.071 | MSB:008 |
| `3\|sans\|fill-blocks\|plain-left` | 1 | 1/14 = 0.071 | MSB:007 |
| `3\|sans\|mono\|plain-centered` | 1 | 1/14 = 0.071 | LOB:003 |
| `3\|serif\|mono\|plain-centered` | 1 | 1/14 = 0.071 | LOB:002 |

Distinct admissible archetypes: 6; k≥2: 2; singletons 4 (4/12 admissible items). Only one corpus (pool), so combined share = pool share and K(a)=k.
§4 coarsening trigger: needs ≥15 admissible; there are 12 → **not triggered**. (Informational, drop `header`: `3\|sans\|fill-blocks` 8/14, `3\|sans\|one-accent` 2/14, `3\|serif\|mono` 1/14, `3\|sans\|mono` 1/14)

Variant modes over admissible items: body [('sans', 10), ('serif', 2)]; rules/boxes [('none', 5), ('rules', 4), ('boxes', 3)]; density [('airy', 11), ('standard', 1)].

## B.6 L3 — D&AD Catalogues & Brochures (presence only, not coded)
The D&AD category index URLs tried (`/en/d/awards/categories/graphic-design/catalogues-brochures`, `/awards/professional/2025/categories/graphic-design/catalogues-brochures/`, `/en/d/awards/`) returned HTTP 404; `https://www.dandad.org/awards/d-ad-awards/categories-2025/graphic-design` returned 200 but exposes no winner list in static HTML. Individual winner pages resolve (HTTP 200, JS-rendered). One was verified by WebFetch on 2026-09-23; the rest are known from a search-result listing only (search snippets are not rank values; presence only):

| Year | Award | Entry | Level | Source | Verified |
|---|---|---|---|---|---|
| 2017 | D&AD Awards, Catalogues & Brochures / Graphic Design | TypoCircle 40th Anniversary book (The Typographic Circle, UK) | Wood Pencil | https://www.dandad.org/awards/professional/2017/graphic-design/26053/typocircle-40th-anniversary-book/ | WebFetch: award, year, level, entrant confirmed |
| 2011 | D&AD Awards, Catalogues & Brochures | Speaker's School Council Awards: The Year Book (Magpie Studio) | Wood Pencil | https://www.dandad.org/awards/professional/2011/graphic-design/18441/speakers-school-council-awards-the-year-book/ | URL 200; details from search result |
| 2009 | D&AD Awards, Catalogues & Brochures | Paste Catalogue (Build) | Wood Pencil | https://www.dandad.org/awards/professional/2009/graphic-design/17309/paste-catalogue/ | URL 200; details from search result |
| 2005 | D&AD Awards, Brochures and Catalogues | Ballpoint exhibition catalogue (Pentagram Design) | Yellow Pencil | https://www.dandad.org/awards/professional/2005/graphic-design/14599/ballpoint-exhibition-catalogue/ | URL 200; details from search result |
| 1998 | D&AD Awards, Brochures and Catalogues | Minale Tattersfield & Partners | Pencil | https://www.dandad.org/awards/professional/1998/graphic-design/22215/minale-tattersfield-partners/ | URL 200; details from search result |

These are bound catalogues/books, not fold-panel brochures; they have not been coded to an archetype (task: presence only), so they cannot merge into or add a §6 step-2 design here. The orchestrator decides whether an L3 slot is meaningful; the award strings would be `award:D&AD Catalogues & Brochures:<year>`.

## B.7 Bias statement
Microsoft Create = Microsoft's editorial selection, first static slice of one category page (page order is not a metric); 9 templates. LibreOffice = cumulative downloads since 03-2020, European/open-source bias, and three of five items are blank fold scaffolds (their previews contain no typography or colour design, so their `sans/serif/mono` and `one-accent/mono` codes rest on placeholder labels only). MS templates are photo-led and Word-authored; the pool is 64% MS by item count, so MS styling dominates. Prevalence of curation, not usage; popularity is not quality (§13). Brochures are thin (N=14): singletons carry no information.

## B.8 Second-coder ids and seed
Ids: MSB:001, MSB:002, MSB:003, MSB:004, MSB:005, MSB:007, MSB:008, MSB:009, MSB:010, LOB:001, LOB:002, LOB:003, LOB:004, LOB:005 (MSB:006 is the duplicate listing, not coded). Sample per §7: `sample = random.Random("82:brochure").sample(sorted(ids), max(min(10, len(ids)), math.ceil(0.25*len(ids))))` — with N=14 this is 10 ids.

## B.9 Ambiguities met
1. `image-hero` strip interpretation (see top). It decides the largest archetype (6 of 12 admissible are `image-hero`); with a literal page-area reading none could be.
2. Three LO items are wireframe scaffolds without design content; coded as on-topic templates by §3.2 and kept at N (no rule says to drop them).
3. MS brochures show only the outside spread; body/density are from that spread only.
4. A4 vs decorative organic blobs (MSB:002, MSB:009): treated as not paint-swipe; MSB:004's brush scribble is treated as A4.
5. Contrast sampling from compressed thumbnails is noisy (extreme-pixel method).
6. Real Estate Brochure/Flyer appears under both queries; counted in the brochure pool only (title order), listed in the flyer file as corroboration.

