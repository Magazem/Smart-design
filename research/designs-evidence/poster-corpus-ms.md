# Poster corpus — Microsoft Create posters (L2 attempt); NOT a coded pool (5 < 10 items)

Coder: Design Researcher. Retrieved 2026-09-23. Conventions as `flyer-corpus.md`. Counts only (research/82 §1).

## P.1 Source
- `https://create.microsoft.com/en-us/templates/posters` (curl -sL, UA smart-design-research) → HTTP 200, redirected to `https://powerpoint.cloud.microsoft/create/en/flyers-posters-templates/?source=create_flow` (same vendor catalogue, 82a C5; items are in the static payload). Page is a combined "flyers & posters" PowerPoint page; editorial order, no metric.
- Static payload holds **10 distinct cards = 5 brochure/flyer cards (tri-fold travel brochure ×2, yoga flyer, Holi flyer, daycare flyer; other families) + 5 poster templates**. Alternate `word.cloud.microsoft/create/en/poster-templates/` returned no items. research/82's probe counted "10 items" — that count was the whole page, not posters.
- **On-topic (posters) = 5 < 10 → per §2 not coded as a corpus; corroboration only, not counted, no k/N, no Ranking Metric string.** No L2 `prevalence:` row can be issued for posters from this source.
- The GitHub L1 (`poster template latex`) and D&AD are other workers' tasks.

## P.2 Corroboration list (page order; features listed for information, NOT counted)
All five are portrait, 516-px thumbnails viewed 2026-09-23.

| # | Template | Thumbnail | orient | columns | head | colour | header | note |
|---|---|---|---|---|---|---|---|---|
| 1 | Concert poster (brown modern simple) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/740eba17-f7d6-4fae-88e6-8d9f2c37c034/thumbnails/516/concert-poster-brown-modern-simple-0-1-c82f6c9016e0.webp | portrait | 1 | sans | fill-blocks (full-bleed photo) | image-hero | white text directly on violin photo (would hit A3) |
| 2 | DEI training poster (pink modern bold) | .../93348599-c197-4162-8233-9db18e27e27a/thumbnails/516/dei-training-poster-pink-modern-bold-0-1-629dc867a8eb.webp | portrait | 1 | sans | fill-blocks | plain-left | 12 identical avatar illustrations (A5) |
| 3 | Free therapy support poster (blue whimsical) | .../cada6128-f7d0-4459-81ef-d1c7aec00f9a/thumbnails/516/free-therapy-support-poster-blue-whimsical-color-block-0-1-eeb4cc19f27e.webp | portrait | 1 | display | fill-blocks | plain-centered | repeated tree/raindrop motifs (A5) |
| 4 | Stop bullying awareness poster (red modern bold) | .../ceb71121-6f7a-4685-a213-83ef7413342d/thumbnails/516/stop-bullying-awareness-poster-red-modern-bold-0-1-635b5f4200ae.webp | portrait | 1 | sans | fill-blocks | plain-centered | bordered pills (boxes) |
| 5 | Elementary school food drive poster (black modern bold) | .../e6babdda-d5c0-47ad-9383-4219f87d6b5b/thumbnails/516/elementary-school-food-drive-poster-black-modern-bold-0-1-2cfd2a121f8f.webp | portrait | 1 | sans | fill-blocks (black) | image-hero (illustration strip ≈26% of page — borderline C1, could be plain-left) | mixed sizes |

Observation only: 5/5 portrait, 5/5 single column, 5/5 fill-blocks, 4/5 sans heading. Illustration-heavy; at least 3 of 5 would likely trip A3/A5. Not usable as a rate.

## P.3 Shortfall / handoff
Poster has no L2 evidence (thin 5). Only the GitHub L1/thin-L1 and D&AD L3 can supply ranks. If the GitHub corpus also yields <10, poster is ranked-by-singletons/Shortfall. Second-coder: nothing to sample from this file.


## P.4 Recount under 82b (Design Researcher 3, 2026-09-23; 82b adopted 2026-09-24)

### P.4.1 Sources re-checked (same vendor catalogue, 82a C5)
- `https://powerpoint.cloud.microsoft/create/en/flyers-posters-templates/` re-fetched: same 10 cards as P.1. **5 posters** (pos 1-5: Concert, DEI training, Stop bullying awareness, Elementary school food drive, Free therapy support). The 3 flyers go to flyer (`flyer-corpus.md` F.11) and the 2 tri-fold brochures to brochure (A4, recorded only).
- `https://powerpoint.cloud.microsoft/create/en/infographic-maker/` (82b §1a; HTTP 200). 6 template cards (plus 3 blog cards, which are not templates). All six thumbnail slugs read `…-infographics-poster-…`. By **title**, 3 are posters ("Technology poster", "Gameboard poster", "Education poster") and 3 are infographics. This coder follows 82b §1a's title split: 3 posters.
- `https://word.cloud.microsoft/create/en/poster-templates/` → 307 to the Word home page (0 cards). The slug is absent, so the result is the same as P.1.
- **MS poster total = 5 + 3 = 8 < 10.** It is still corroboration only (§2, 82a C15). No `prevalence:` string, no k/N.

The 3 infographic-maker posters (not coded, not counted):

| # | source (page pos) | template | url | thumbnail |
|---|---|---|---|---|
| PIM:004 | PowerPoint infographic-maker (4) | Technology poster | https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fc9897779-e6ff-4c8a-9b6e-47a3f9f8800e%2FTFc9897779-e6ff-4c8a-9b6e-47a3f9f8800efd2393d2_wac-00615f3c702c.pptx | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/c9897779-e6ff-4c8a-9b6e-47a3f9f8800e/thumbnails/400/technology-infographics-poster-blue-modern-bold-0-1-f4aef10e5d59.webp |
| PIM:005 | PowerPoint infographic-maker (5) | Gameboard poster | https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fef90dccf-e384-4f48-8025-1e3097521601%2FTFef90dccf-e384-4f48-8025-1e30975216012296df21_wac-1c5bbb238ec8.pptx | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/ef90dccf-e384-4f48-8025-1e3097521601/thumbnails/400/gameboard-infographics-poster-blue-modern-geometric-0-1-114488a30414.webp |
| PIM:006 | PowerPoint infographic-maker (6) | Education poster | https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F6797a02e-7d4c-41b3-b4e0-7076369df1a4%2FTF6797a02e-7d4c-41b3-b4e0-7076369df1a4680d1ab4_wac-7b76ace1d85f.pptx | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/6797a02e-7d4c-41b3-b4e0-7076369df1a4/thumbnails/400/education-infographics-poster-red-modern-bold-0-1-69677474da39.webp |

Infographic-titled items on the same page (they belong to the infographic family, corroboration, see `infographic-corpus-iib.md` I.6):

| # | template | thumbnail |
|---|---|---|
| PIM:001 | Illustrate fashion trends | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/ee63bea3-e232-417c-bbb9-774420afc450/thumbnails/400/fashion-infographics-poster-black-modern-bold-0-1-bd3a5e225b11.webp |
| PIM:002 | Provide financial tips | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/7e35941d-51ce-47b1-8aab-bc271e4cfab1/thumbnails/400/financial-infographics-poster-green-modern-simple-0-1-afb75a270533.webp |
| PIM:003 | Display product roadmap | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e91a6422-cb04-4473-9aca-b150e1d949a6/thumbnails/400/product-roadmap-infographics-poster-black-modern-simple-0-1-685d01ef19fa.webp |

### P.4.2 A1 pooling: not applicable to poster
A1 applies only "if every reachable catalogue for a family has fewer than 10 on-topic items". Poster already has a numeric corpus (`poster-corpus-github.md`, `poster-items-github.csv`), and 82b §1e counts Overleaf `tagged/poster` at 27 pages. MS (8) is therefore **not** pooled, and it stays corroboration only. If the orchestrator rules that sub-10 catalogues may pool beside a ≥10 corpus, the candidate members are MS (8) and Typst Universe category `poster` (8 per 82b §1d, not fetched here). Observation only: all 8 MS posters are portrait, and the 3 infographic-maker posters are dense multi-block infographic layouts (Big Data: 2-column fill-blocks; Budget Game: road illustration; College data: stat boxes).


## P.5 A1 pool: MS Create posters (8) + Typst Universe posters (7) - Design Researcher, 2026-09-24 (82b A1 / 82a C27)
C27: a pool of sub-10 catalogues that reaches >=10 on-topic items after dedup IS a corpus and may sit beside the GitHub L1. **Pool N = 15 (>=10): coded as a corpus.** Ranking Metric string: `prevalence:ms-create+typst-universe-posters:k/15`. Combined poster share = unweighted mean of the GitHub L1 (poster-corpus-github.md, k/40) and this pool (k/15), the pool counting once (computed by the orchestrator).

Sources (fetched 2026-09-24): MS = the 5 posters of P.1 + the 3 "poster"-titled infographic-maker templates of P.4.1 = 8 (same vendor catalogue, editorial order, no metric). Typst Universe `https://packages.typst.org/preview/index.json` (1619 packages, 818 templates): category `poster` = 8 templates; **7 on-topic** (isc-hei-poster, pasquino, peace-of-posters, placard, pollux, simple-research-poster, tuhi-course-poster-vuw); **storytiles** is a slide/notes template (off-topic). Preview = the Universe gallery thumbnail `https://packages.typst.org/preview/thumbnails/<name>-<version>.webp` (1356-1920 px), page 1 of the poster. Dedup vs the GitHub L1: none of the Typst packages is among the 40 coded GitHub items (their repos are not in `poster-items-github.csv`; typst-poster-gemini, GitHub rank 60, is beyond the coded walk and is a different package). No MS item duplicates another. Items csv: `poster-items-pool.csv` (15 rows, C11).
Skew: MS = Microsoft editorial pick (event/awareness posters, 3 infographic-maker posters); Typst Universe = scientific/academic posters (Gemini-style clones) plus one course poster. Prevalence of catalogue curation, not usage; all 8 MS posters are portrait.

Coding: 82 section 4 (poster: orientation variant) with header/colour per research/82a-general.md; thumbnails only (400-516 px MS; 1.3-1.9 kpx Typst); contrast values are estimates (C9). A5 counts >=3 identical decorative repeats; A3 counts 3+ text lines set on a gradient/photo.

### P.5.1 Coded table (N = 15)
| id | template | orient | columns | head | body | colour | header | rules | dens | adm | note | thumbnail |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PM:001 | [Concert poster (MS PowerPoint flyers-posters-templates pos 1)](https://powerpoint.cloud.microsoft/create/en/flyers-posters-templates/) | portrait | 1 | sans | sans | mono | image-hero | rules | airy | n | A3 four-line white text block set directly on the full-bleed violin photo (C14 leaves single titles alone; this block is 3+ lines) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/740eba17-f7d6-4fae-88e6-8d9f2c37c034/thumbnails/516/concert-poster-brown-modern-simple-0-1-c82f6c9016e0.webp |
| PM:002 | [DEI training poster (pos 2)](https://powerpoint.cloud.microsoft/create/en/flyers-posters-templates/) | portrait | 1 | sans | sans | one-accent | plain-centered | none | airy | n | A5 twelve identical avatar illustrations in a circle; pale-pink page is background (L 0.93, B1e); navy text (one cluster) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/93348599-c197-4162-8233-9db18e27e27a/thumbnails/516/dei-training-poster-pink-modern-bold-0-1-629dc867a8eb.webp |
| PM:003 | [Stop bullying awareness poster (pos 3)](https://powerpoint.cloud.microsoft/create/en/flyers-posters-templates/) | portrait | 1 | sans | sans | mono | plain-centered | boxes | airy | n | A5 three identical small brain characters (borderline: 1 large + 3 small); red page = background (B1a); white text on #d73a2b 4.64:1 passes A6; two rounded outline boxes | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/ceb71121-6f7a-4685-a213-83ef7413342d/thumbnails/516/stop-bullying-awareness-poster-red-modern-bold-0-1-635b5f4200ae.webp |
| PM:004 | [Elementary school food drive poster (pos 4)](https://powerpoint.cloud.microsoft/create/en/flyers-posters-templates/) | portrait | 1 | sans | sans | mono | plain-left | none | standard | y | black background; top illustration collage ~28% of page (<30%, not image-hero) of varied, not identical, icons; white text | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e6babdda-d5c0-47ad-9383-4219f87d6b5b/thumbnails/516/elementary-school-food-drive-poster-black-modern-bold-0-1-2cfd2a121f8f.webp |
| PM:005 | [Free therapy support poster (pos 5)](https://powerpoint.cloud.microsoft/create/en/flyers-posters-templates/) | portrait | 1 | display | sans | one-accent | plain-centered | none | airy | n | A5 repeated identical tree and raindrop motifs; navy background excluded; cream/yellow lettering (one cluster) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/cada6128-f7d0-4459-81ef-d1c7aec00f9a/thumbnails/516/free-therapy-support-poster-blue-whimsical-color-block-0-1-eeb4cc19f27e.webp |
| PIM:004 | [Technology poster (PowerPoint infographic-maker pos 4)](https://powerpoint.cloud.microsoft/create/en/infographic-maker/) | portrait | grid | sans | sans | fill-blocks | plain-left | boxes | dense | n | A3 blue-violet gradient behind all text; stat tiles (fill-blocks) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/c9897779-e6ff-4c8a-9b6e-47a3f9f8800e/thumbnails/400/technology-infographics-poster-blue-modern-bold-0-1-f4aef10e5d59.webp |
| PIM:005 | [Gameboard poster (infographic-maker pos 5)](https://powerpoint.cloud.microsoft/create/en/infographic-maker/) | portrait | grid | serif | sans | one-accent | plain-centered | none | standard | n | A5 six identical map-pin icon frames along the road; pale-green page = background | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/ef90dccf-e384-4f48-8025-1e3097521601/thumbnails/400/gameboard-infographics-poster-blue-modern-geometric-0-1-114488a30414.webp |
| PIM:006 | [Education poster (infographic-maker pos 6)](https://powerpoint.cloud.microsoft/create/en/infographic-maker/) | portrait | grid | sans | sans | fill-blocks | ruled | boxes | dense | y | blue stat tiles ~15% of page (fill-blocks); full-width blue rules above and below the title block (logo box excluded, gap <4 lines); data glyph repeats are chart marks, not decoration | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/6797a02e-7d4c-41b3-b4e0-7076369df1a4/thumbnails/400/education-infographics-poster-red-modern-bold-0-1-69677474da39.webp |
| PT:isc-hei-poster | [Typst Universe: isc-hei-poster 0.8.1](https://typst.app/universe/package/isc-hei-poster) | portrait | 3+ | sans | sans | one-accent | ruled | boxes | dense | n | A8 every content block is a bordered card; dotted rule under the header block; magenta headings | https://packages.typst.org/preview/thumbnails/isc-hei-poster-0.8.1.webp |
| PT:pasquino | [Typst Universe: pasquino 0.1.0](https://typst.app/universe/package/pasquino) | portrait | 2-equal | serif | serif | mono | plain-left | none | dense | n | A3 soft blue gradient behind the 4-line title/author block ("themed gradients", disclosed borderline: light tint L>0.9 excluded for colour) | https://packages.typst.org/preview/thumbnails/pasquino-0.1.0.webp |
| PT:peace-of-posters | [Typst Universe: peace-of-posters 0.6.0](https://typst.app/universe/package/peace-of-posters) | portrait | 2-equal | sans | sans | fill-blocks | band | none | dense | y | navy title band ~11% of page behind the title; navy section bars; scientific images excluded | https://packages.typst.org/preview/thumbnails/peace-of-posters-0.6.0.webp |
| PT:placard | [Typst Universe: placard 0.1.0](https://typst.app/universe/package/placard) | portrait | 2-equal | serif | serif | mono | plain-centered | boxes | airy | n | A8 both content blocks in rounded bordered boxes (grid demo; mostly empty) | https://packages.typst.org/preview/thumbnails/placard-0.1.0.webp |
| PT:pollux | [Typst Universe: pollux 0.1.0](https://typst.app/universe/package/pollux) | portrait | 2-equal | sans | sans | one-accent | band | none | standard | y | steel-blue title band #4d729a ~8% of page (<10%, so one-accent not fill-blocks); white text on it 5.01:1; blue headings | https://packages.typst.org/preview/thumbnails/pollux-0.1.0.webp |
| PT:simple-research-poster | [Typst Universe: simple-research-poster 0.2.0](https://typst.app/universe/package/simple-research-poster) | landscape | 3+ | serif | serif | fill-blocks | band | rules | dense | y | navy title band ~12% + tinted section boxes; logo excluded; three text columns | https://packages.typst.org/preview/thumbnails/simple-research-poster-0.2.0.webp |
| PT:tuhi-course-poster-vuw | [Typst Universe: tuhi-course-poster-vuw 0.2.0](https://typst.app/universe/package/tuhi-course-poster-vuw) | portrait | 2-sidebar | sans | sans | one-accent | plain-left | none | standard | y | sunset photo ~14% of page (not hero); orange title accent + bullets; narrow right stats column; QR excluded | https://packages.typst.org/preview/thumbnails/tuhi-course-poster-vuw-0.2.0.webp |

### P.5.2 Exclusions log (item stays in N)
| id | rule | evidence |
|---|---|---|
| PM:001 | A3 | A3 four-line white text block set directly on the full-bleed violin photo (C14 leaves single titles alone; this block is 3+ lines) |
| PM:002 | A5 | A5 twelve identical avatar illustrations in a circle; pale-pink page is background (L 0.93, B1e); navy text (one cluster) |
| PM:003 | A5 | A5 three identical small brain characters (borderline: 1 large + 3 small); red page = background (B1a); white text on #d73a2b 4.64:1 passes A6; two rounded outline boxes |
| PM:005 | A5 | A5 repeated identical tree and raindrop motifs; navy background excluded; cream/yellow lettering (one cluster) |
| PIM:004 | A3 | A3 blue-violet gradient behind all text; stat tiles (fill-blocks) |
| PIM:005 | A5 | A5 six identical map-pin icon frames along the road; pale-green page = background |
| PT:isc-hei-poster | A8 | A8 every content block is a bordered card; dotted rule under the header block; magenta headings |
| PT:pasquino | A3 | A3 soft blue gradient behind the 4-line title/author block ("themed gradients", disclosed borderline: light tint L>0.9 excluded for colour) |
| PT:placard | A8 | A8 both content blocks in rounded bordered boxes (grid demo; mostly empty) |

Admissible 6 / 15, excluded 9 (A5 x4: PM:002, PM:003, PM:005, PIM:005; A3 x3: PM:001, PIM:004, pasquino; A8 x2: isc-hei-poster, placard).

### P.5.3 Frequency table k/15 (denominator includes inadmissible; [x] = inadmissible)
| archetype `columns\|heading\|colour\|header` | k | k/15 | admissible k | exemplars |
|---|---|---|---|---|
| `1\|display\|one-accent\|plain-centered` | 1 | 0.067 | 0 | PM:005[x] |
| `1\|sans\|mono\|image-hero` | 1 | 0.067 | 0 | PM:001[x] |
| `1\|sans\|mono\|plain-centered` | 1 | 0.067 | 0 | PM:003[x] |
| `1\|sans\|mono\|plain-left` | 1 | 0.067 | 1 | PM:004 |
| `1\|sans\|one-accent\|plain-centered` | 1 | 0.067 | 0 | PM:002[x] |
| `2-equal\|sans\|fill-blocks\|band` | 1 | 0.067 | 1 | PT:peace-of-posters |
| `2-equal\|sans\|one-accent\|band` | 1 | 0.067 | 1 | PT:pollux |
| `2-equal\|serif\|mono\|plain-centered` | 1 | 0.067 | 0 | PT:placard[x] |
| `2-equal\|serif\|mono\|plain-left` | 1 | 0.067 | 0 | PT:pasquino[x] |
| `2-sidebar\|sans\|one-accent\|plain-left` | 1 | 0.067 | 1 | PT:tuhi-course-poster-vuw |
| `3+\|sans\|one-accent\|ruled` | 1 | 0.067 | 0 | PT:isc-hei-poster[x] |
| `3+\|serif\|fill-blocks\|band` | 1 | 0.067 | 1 | PT:simple-research-poster |
| `grid\|sans\|fill-blocks\|plain-left` | 1 | 0.067 | 0 | PIM:004[x] |
| `grid\|sans\|fill-blocks\|ruled` | 1 | 0.067 | 1 | PIM:006 |
| `grid\|serif\|one-accent\|plain-centered` | 1 | 0.067 | 0 | PIM:005[x] |

15 distinct archetypes; admissible 6 in 6 archetypes; archetypes with k>=2: 0; singleton admissible items 6/6. Coarsening trigger (>=15 admissible, >50% singletons, <5 archetypes k>=2): not triggered (only 6 admissible items).
Variant modes over admissible items: orientation [('portrait', 5), ('landscape', 1)]; body [('sans', 5), ('serif', 1)]; rules/boxes [('band', 3), ('plain-left', 2), ('ruled', 1)]; density [('none', 4), ('boxes', 1), ('rules', 1)]. All 15: orientation [('portrait', 14), ('landscape', 1)].

### P.5.4 Second-coder ids and seed
Ids: PIM:004 PIM:005 PIM:006 PM:001 PM:002 PM:003 PM:004 PM:005 PT:isc-hei-poster PT:pasquino PT:peace-of-posters PT:placard PT:pollux PT:simple-research-poster PT:tuhi-course-poster-vuw
Pool-only sample under `random.Random("82:poster")`: PM:004 PT:placard PT:isc-hei-poster PM:005 PT:peace-of-posters PT:pasquino PT:simple-research-poster PM:002 PIM:006 PM:003 (C10: the orchestrator draws the family-wide sample over GitHub L1 + this pool).

### P.5.5 Ambiguities
1. MS infographic-maker posters are poster-titled but infographic-like (dense tile layouts); counted as posters by title (82b 1a), disclosed. If excluded the pool is 12, still >=10.
2. A5 for PM:003 (3 small identical brains) and PM:005 (many tree/raindrop repeats) is judgement-borderline; PM:002 (12 avatars) is not.
3. Typst thumbnails show demo content; the gradient of pasquino is a soft tint, coded A3 because the 4-line title block sits on it (recode risk).
4. Header for headline-on-photo (PM:001) = image-hero (photo >=30% of page, intersects top 20%); PM:004 illustration <30% -> plain-left.
