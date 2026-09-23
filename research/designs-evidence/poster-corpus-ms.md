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
