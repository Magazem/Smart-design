# Deck corpus 2 — LibreOffice Impress + Microsoft Create (Phase 4 coder output, research/82)

Coder: Design Researcher. Counts only; no judgement of quality (research/82 §1). Retrieved 2026-09-23. Second-coder ids use the corpus id + native raw list position (zero-padded); see §LO.7.

Deck identity archetype = `background|heading|colour|title-slide-layout` (§4 family table). Variants: body class, rules/boxes, density.

## Corpus LO — LibreOffice Extensions, tag Templates + Impress (L1 attempt)

### LO.1 Source
- URL (page 1): `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&Tags%5B%5D=43&ord=download_d`; pages `&start=30`, `60`, `90` (each fetched with `curl -s -A "smart-design-research"`).
- Sort: `ord=download_d` (downloads, cumulative since the 03-2020 site migration, read from `<span data-value=… class="intl-number">`). Retrieval date 2026-09-23.
- Total reachable: **114 raw items** (30+30+30+24); the last item (raw #114, "Fundo Vermelho 1") shows no download count. Walk stopped at raw position 45, where the 40th on-topic codeable item was reached (walk cap 200 not hit).
- Screenshots: per-item detail page `/en/extensions/show/<id>`, the un-scaled `/assets/screenshots/…` images (first = title slide where the author supplied one, second = next). Downloaded to the system temp dir only.

### LO.2 Raw list (native order, downloads desc) with on-topic decision
| Raw pos | Item | Downloads | Topic | Reason / note |
|---|---|---|---|---|
| 001 | [Modern template](https://extensions.libreoffice.org/en/extensions/show/5139) | 7017 | on-topic |  |
| 002 | [Template LibreOffice Presentations MMA v1](https://extensions.libreoffice.org/en/extensions/show/34149) | 4296 | on-topic |  |
| 003 | [Line Impression](https://extensions.libreoffice.org/en/extensions/show/5073) | 2435 | on-topic |  |
| 004 | [Profesional Impress Template](https://extensions.libreoffice.org/en/extensions/show/645) | 1858 | on-topic |  |
| 005 | [ZamZam](https://extensions.libreoffice.org/en/extensions/show/5075) | 1715 | on-topic |  |
| 006 | [Tokyo Style Template](https://extensions.libreoffice.org/en/extensions/show/tokyo-style-template) | 1576 | on-topic |  |
| 007 | [Free Business Card Designs By MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99421) | 1559 | off-topic | other family: business card |
| 008 | [Présentation Symphonie en noir](https://extensions.libreoffice.org/en/extensions/show/99229) | 1521 | on-topic |  |
| 009 | [Chocolat & variantes](https://extensions.libreoffice.org/en/extensions/show/41979) | 1334 | on-topic |  |
| 010 | [Birthday Greeting Card presentation template for all age groups created By MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99418) | 1204 | off-topic | other family: greeting card |
| 011 | [Bumi Samudra](https://extensions.libreoffice.org/en/extensions/show/5076) | 1162 | on-topic |  |
| 012 | [Presentation Framboise écrasée](https://extensions.libreoffice.org/en/extensions/show/99225) | 1133 | on-topic |  |
| 013 | [The Oriental by bajinra](https://extensions.libreoffice.org/en/extensions/show/99243) | 1107 | on-topic |  |
| 014 | [Émeraude et mimosa (présentation)](https://extensions.libreoffice.org/en/extensions/show/27501) | 1059 | on-topic |  |
| 015 | [Corporate Business Strategy Presentation Template by MKCL](https://extensions.libreoffice.org/en/extensions/show/99297) | 1053 | on-topic |  |
| 016 | [Presentation Sapins et tilleuls](https://extensions.libreoffice.org/en/extensions/show/99226) | 1029 | on-topic |  |
| 017 | [Consulting Blue - IBM Plex Sans](https://extensions.libreoffice.org/en/extensions/show/99219) | 1013 | on-topic |  |
| 018 | [Geometric Lotus by bajinra](https://extensions.libreoffice.org/en/extensions/show/99456) | 1010 | on-topic |  |
| 019 | [Pack of 6 beautiful Presentation templates inspired by Indian arts, designs by MKCL](https://extensions.libreoffice.org/en/extensions/show/99255) | 981 | on-topic | pack of 6; coded once, on the design shown first |
| 020 | [Alizarin](https://extensions.libreoffice.org/en/extensions/show/5144) | 943 | on-topic |  |
| 021 | [Strawberry Milk Template by Natalie Chmura](https://extensions.libreoffice.org/en/extensions/show/99337) | 912 | on-topic |  |
| 022 | [Impress Modèle de présentation Bleus et gris](https://extensions.libreoffice.org/en/extensions/show/4066) | 903 | on-topic |  |
| 023 | [RedBlack Lines](https://extensions.libreoffice.org/en/extensions/show/42002) | 866 | on-topic |  |
| 024 | [Hazard! Game Template (Jeopardy Clone)](https://extensions.libreoffice.org/en/extensions/show/99270) | 844 | off-topic | game board (Jeopardy), not a presentation deck |
| 025 | [Tiles](https://extensions.libreoffice.org/en/extensions/show/5089) | 765 | on-topic |  |
| 026 | [Love OpenSource](https://extensions.libreoffice.org/en/extensions/show/5086) | 763 | on-topic |  |
| 027 | [Sunny Gradient](https://extensions.libreoffice.org/en/extensions/show/5072) | 761 | on-topic |  |
| 028 | [We Care](https://extensions.libreoffice.org/en/extensions/show/5090) | 754 | on-topic |  |
| 029 | [About Me](https://extensions.libreoffice.org/en/extensions/show/5098) | 742 | on-topic |  |
| 030 | [Signs](https://extensions.libreoffice.org/en/extensions/show/5065) | 741 | on-topic |  |
| 031 | [Sandwich Future Template by Pavan Rauch](https://extensions.libreoffice.org/en/extensions/show/99335) | 730 | on-topic |  |
| 032 | [Impress Modèle de présentation Fée bleue](https://extensions.libreoffice.org/en/extensions/show/4067) | 712 | on-topic |  |
| 033 | [Presentation Template for Social Media Posts by MKCL-KF](https://extensions.libreoffice.org/en/extensions/show/99422) | 682 | off-topic | other family: social-media post |
| 034 | [Golden Hour - Template](https://extensions.libreoffice.org/en/extensions/show/27485) | 677 | on-topic |  |
| 035 | [Block Game Template by Natalie Chmura](https://extensions.libreoffice.org/en/extensions/show/99336) | 667 | on-topic |  |
| 036 | [Présentation Grain de café](https://extensions.libreoffice.org/en/extensions/show/41976) | 639 | on-topic |  |
| 037 | [Vaux](https://extensions.libreoffice.org/en/extensions/show/5093) | 630 | on-topic |  |
| 038 | [Pin Collage Template for Pinterest Promotions by MKCL](https://extensions.libreoffice.org/en/extensions/show/99345) | 624 | off-topic | other family: Pinterest collage |
| 039 | [Retro style Template](https://extensions.libreoffice.org/en/extensions/show/99330) | 617 | on-topic |  |
| 040 | [Blue White Template](https://extensions.libreoffice.org/en/extensions/show/99328) | 611 | on-topic |  |
| 041 | [Ambiance Halloween ou estivale](https://extensions.libreoffice.org/en/extensions/show/5047) | 594 | on-topic |  |
| 042 | [Elegant Embroidery in a Presentation Template for all, by MKCL.](https://extensions.libreoffice.org/en/extensions/show/99266) | 578 | on-topic |  |
| 043 | [Strategic Growth and Innovation Presentation Template by MKCL](https://extensions.libreoffice.org/en/extensions/show/99296) | 561 | on-topic |  |
| 044 | [Professional Presentation Template for Monthly work By MKCL](https://extensions.libreoffice.org/en/extensions/show/99339) | 560 | on-topic |  |
| 045 | [SuperGreta!](https://extensions.libreoffice.org/en/extensions/show/1086) | 506 | on-topic |  |
| 046–114 | not walked (target of 40 reached at 045) | 497…37 | — | raw list retained in the fetched pages |


Off-topic exclusions (not counted in N; §3.2 "other families"): raw 007 business cards, 010 greeting card, 024 Jeopardy game board, 033 social-media posts, 038 Pinterest collage, 055 party invitation, 056 syllabus document. Raw 049 is on-topic but uncodeable (§3.3). Raw 019 is a pack of six, coded once on the design shown first. MKCL/InDiFi variants are distinct designs by one author and are counted separately (ambiguity noted at the end).

### LO.3 Coded table (40 on-topic codeable items, native order)
Codes per §4: bg = background; head/body = heading/body class; colour; title = title-slide layout; rules = rules/boxes; dens = density (from the first content slide when a preview shows one, else from the title slide); adm = admissible. Id `LO:<raw position>`.

| id | Item (downloads) | Preview URL (first) | bg | head | body | colour | title | rules | dens | adm | reason / note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LO:001 | [Modern template](https://extensions.libreoffice.org/en/extensions/show/5139) (7017) | https://extensions.libreoffice.org/assets/screenshots/1447/modern-blue-show-1.png | dark | sans | sans | mono | centered | boxes | airy | y | title slide only (colour variants) |
| LO:002 | [Template LibreOffice Presentations MMA v1](https://extensions.libreoffice.org/en/extensions/show/34149) (4296) | https://extensions.libreoffice.org/assets/screenshots/5011/template-LibreOffice-Praesentation-MMA-01.jpg | light | sans | sans | one-accent | left | none | airy | y |  |
| LO:003 | [Line Impression](https://extensions.libreoffice.org/en/extensions/show/5073) (2435) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v7.png | dark | sans | sans | multi | centered | none | airy | y | title slide only, blurry |
| LO:004 | [Profesional Impress Template](https://extensions.libreoffice.org/en/extensions/show/645) (1858) | https://extensions.libreoffice.org/assets/screenshots/z/professionnel-et-sobre-modele-impress-profesional-y-sob_QvPVa6dA_0c8f98c6-fd47-41e1-a97f-7e2e439a28a9.png | light | serif | sans | fill-blocks | split | rules | airy | y | low-res, master pages |
| LO:005 | [ZamZam](https://extensions.libreoffice.org/en/extensions/show/5075) (1715) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v9.png | dark | sans | sans | multi | split | none | airy | y | title slide only |
| LO:006 | [Tokyo Style Template](https://extensions.libreoffice.org/en/extensions/show/tokyo-style-template) (1576) | https://extensions.libreoffice.org/assets/screenshots/z/tokyo-style-template_3778dced-2f81-4141-b019-f7a63d226021.png | image | sans | sans | mono | left | none | airy | n | EXCLUDED A3 gradient over photo behind title/subtitle; title slide only |
| LO:008 | [Présentation Symphonie en noir](https://extensions.libreoffice.org/en/extensions/show/99229) (1521) | https://extensions.libreoffice.org/assets/screenshots/1011/dm-pres-symphonie-en-noirs.png | dark | sans | sans | mono | split | boxes | standard | y | master-slide previews |
| LO:009 | [Chocolat & variantes](https://extensions.libreoffice.org/en/extensions/show/41979) (1334) | https://extensions.libreoffice.org/assets/screenshots/1011/pres-bleu-gris-pm.png | light | serif | serif | fill-blocks | left | boxes | standard | n | EXCLUDED A5 5 identical progress ovals; master-slide previews |
| LO:011 | [Bumi Samudra](https://extensions.libreoffice.org/en/extensions/show/5076) (1162) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v10.png | dark | sans | sans | mono | centered | none | airy | n | EXCLUDED A3 gradient bg behind text; title slide only |
| LO:012 | [Presentation Framboise écrasée](https://extensions.libreoffice.org/en/extensions/show/99225) (1133) | https://extensions.libreoffice.org/assets/screenshots/1011/pres-framboise-dm.png | light | sans | sans | fill-blocks | left | boxes | standard | y | master-slide previews |
| LO:013 | [The Oriental by bajinra](https://extensions.libreoffice.org/en/extensions/show/99243) (1107) | https://extensions.libreoffice.org/assets/screenshots/6515/preview-v1.2.0.png | light | sans | sans | fill-blocks | centered | none | standard | n | EXCLUDED A5 6 identical flower icons on content slide |
| LO:014 | [Émeraude et mimosa (présentation)](https://extensions.libreoffice.org/en/extensions/show/27501) (1059) | https://extensions.libreoffice.org/assets/screenshots/1011/mimosa-expl-v3.png | light | sans | sans | fill-blocks | left | none | standard | y | master-slide previews |
| LO:015 | [Corporate Business Strategy Presentation Template by MKCL](https://extensions.libreoffice.org/en/extensions/show/99297) (1053) | https://extensions.libreoffice.org/assets/screenshots/6516/Slide1-v20.JPG | light | sans | sans | fill-blocks | left | boxes | standard | n | EXCLUDED A5 3 identical purple cards; A6 white on lavender |
| LO:016 | [Presentation Sapins et tilleuls](https://extensions.libreoffice.org/en/extensions/show/99226) (1029) | https://extensions.libreoffice.org/assets/screenshots/1011/dm-verts-forets.png | light | sans | sans | fill-blocks | left | rules | standard | y | master-slide previews |
| LO:017 | [Consulting Blue - IBM Plex Sans](https://extensions.libreoffice.org/en/extensions/show/99219) (1013) | https://extensions.libreoffice.org/assets/screenshots/6297/screenshot-001.png | dark | sans | sans | multi | left | boxes | dense | y | title dark, content light; bg coded from title slide |
| LO:018 | [Geometric Lotus by bajinra](https://extensions.libreoffice.org/en/extensions/show/99456) (1010) | https://extensions.libreoffice.org/assets/screenshots/6515/lotus-prev-1.0-1.png | light | sans | sans | multi | left | none | airy | n | EXCLUDED A5 6 identical flower icons on content slide |
| LO:019 | [Pack of 6 beautiful Presentation templates inspired by Indian arts, designs by MKCL](https://extensions.libreoffice.org/en/extensions/show/99255) (981) | https://extensions.libreoffice.org/assets/screenshots/6516/Education_Madhubani.JPG | light | sans | sans | multi | centered | boxes | airy | n | EXCLUDED A5 repeated identical border motif; cartoon figure; title slide + section slide |
| LO:020 | [Alizarin](https://extensions.libreoffice.org/en/extensions/show/5144) (943) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v32.png | light | sans | sans | one-accent | left | none | airy | y | single blurry content slide, no title slide shown; title layout coded from it |
| LO:021 | [Strawberry Milk Template by Natalie Chmura](https://extensions.libreoffice.org/en/extensions/show/99337) (912) | https://extensions.libreoffice.org/assets/screenshots/6857/StrawberryMilk_1.png | light | sans | sans | fill-blocks | centered | boxes | airy | n | EXCLUDED A3 gradient wave behind body text; heading is handwriting face (display), body enum has no display value -> sans |
| LO:022 | [Impress Modèle de présentation Bleus et gris](https://extensions.libreoffice.org/en/extensions/show/4066) (903) | https://extensions.libreoffice.org/assets/screenshots/1011/impres-visu-bleus-et-gris.png | light | sans | sans | one-accent | left | rules | standard | y | thumbnail overview only, very low res |
| LO:023 | [RedBlack Lines](https://extensions.libreoffice.org/en/extensions/show/42002) (866) | https://extensions.libreoffice.org/assets/screenshots/4015/Screenshot-2023-11-03-at-18.20.10.png | light | sans | sans | one-accent | centered | rules | airy | y | content slide is dark full-bleed; bg coded from title slide |
| LO:025 | [Tiles](https://extensions.libreoffice.org/en/extensions/show/5089) (765) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v22.png | light | sans | sans | multi | left | boxes | airy | n | EXCLUDED A5 8 identical circular illustrations; single slide |
| LO:026 | [Love OpenSource](https://extensions.libreoffice.org/en/extensions/show/5086) (763) | https://extensions.libreoffice.org/assets/screenshots/1150/LoveOpenSource.png | dark | sans | sans | mono | centered | none | standard | n | EXCLUDED A3 gradient bg behind body text (both slides); no title slide shown; title layout coded from content slide |
| LO:027 | [Sunny Gradient](https://extensions.libreoffice.org/en/extensions/show/5072) (761) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v6.png | dark | display | sans | multi | centered | boxes | airy | n | EXCLUDED A3 gradient pill fill behind subtitle text; title slide only, low res |
| LO:028 | [We Care](https://extensions.libreoffice.org/en/extensions/show/5090) (754) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v23.png | dark | sans | sans | fill-blocks | split | none | standard | n | EXCLUDED A7 indigo-to-purple gradient background; single content slide, low res |
| LO:029 | [About Me](https://extensions.libreoffice.org/en/extensions/show/5098) (742) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v31.png | dark | sans | sans | fill-blocks | split | none | airy | y | title slide only, low res |
| LO:030 | [Signs](https://extensions.libreoffice.org/en/extensions/show/5065) (741) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v2.png | dark | sans | sans | one-accent | centered | none | airy | y | title slide only |
| LO:031 | [Sandwich Future Template by Pavan Rauch](https://extensions.libreoffice.org/en/extensions/show/99335) (730) | https://extensions.libreoffice.org/assets/screenshots/6857/Sandwich_1.png | image | display | sans | multi | full-bleed-image | rules | airy | y | title slide over gradient/illustrated bg with flat cream panels behind text |
| LO:032 | [Impress Modèle de présentation Fée bleue](https://extensions.libreoffice.org/en/extensions/show/4067) (712) | https://extensions.libreoffice.org/assets/screenshots/1011/impres-visu-fee-bleue.png | light | sans | sans | one-accent | left | rules | standard | y | thumbnail overview only, very low res |
| LO:034 | [Golden Hour - Template](https://extensions.libreoffice.org/en/extensions/show/27485) (677) | https://extensions.libreoffice.org/assets/screenshots/4015/Screenshot-2023-03-31-at-14-v2.58.43.png | dark | serif | serif | fill-blocks | centered | none | standard | y | bg coded dark from title slide (L=0.47 <0.5); content slide is mostly white |
| LO:035 | [Block Game Template by Natalie Chmura](https://extensions.libreoffice.org/en/extensions/show/99336) (667) | https://extensions.libreoffice.org/assets/screenshots/6857/BlockGameTheme_1.png | dark | sans | sans | multi | centered | boxes | airy | n | EXCLUDED A3 tetromino/grid texture bg behind text |
| LO:036 | [Présentation Grain de café](https://extensions.libreoffice.org/en/extensions/show/41976) (639) | https://extensions.libreoffice.org/assets/screenshots/1011/grains-de-cafe-3-pages.png | light | sans | sans | one-accent | centered | none | standard | y | two variants (photo/gradient); first coded |
| LO:037 | [Vaux](https://extensions.libreoffice.org/en/extensions/show/5093) (630) | https://extensions.libreoffice.org/assets/screenshots/4/thumbnail-v26.png | image | sans | sans | mono | full-bleed-image | boxes | airy | n | EXCLUDED A3 photo fill behind text; title slide only |
| LO:039 | [Retro style Template](https://extensions.libreoffice.org/en/extensions/show/99330) (617) | https://extensions.libreoffice.org/assets/screenshots/35/btssg2021.png | light | sans | sans | fill-blocks | centered | boxes | airy | y | Japanese text; Noto Sans JP class by glyphs |
| LO:040 | [Blue White Template](https://extensions.libreoffice.org/en/extensions/show/99328) (611) | https://extensions.libreoffice.org/assets/screenshots/35/all.png | light | sans | sans | one-accent | left | rules | airy | y | accent sampled #5174b7 (not an exact A7 hex; near Office blue) |
| LO:041 | [Ambiance Halloween ou estivale](https://extensions.libreoffice.org/en/extensions/show/5047) (594) | https://extensions.libreoffice.org/assets/screenshots/1011/dm-pres-halloween-v2.png | light | sans | sans | multi | left | rules | standard | n | EXCLUDED A5 5 identical tree icons in footer strip (master); master-slide previews |
| LO:042 | [Elegant Embroidery in a Presentation Template for all, by MKCL.](https://extensions.libreoffice.org/en/extensions/show/99266) (578) | https://extensions.libreoffice.org/assets/screenshots/6516/1.jpg | image | sans | sans | multi | full-bleed-image | boxes | airy | n | EXCLUDED A5 repeated identical flower motifs (content-slide header strip) |
| LO:043 | [Strategic Growth and Innovation Presentation Template by MKCL](https://extensions.libreoffice.org/en/extensions/show/99296) (561) | https://extensions.libreoffice.org/assets/screenshots/6516/Slide1-v19.JPG | dark | sans | sans | one-accent | left | none | airy | n | EXCLUDED A3 pattern texture behind body text on content slide; title slide black; content slide pale |
| LO:044 | [Professional Presentation Template for Monthly work By MKCL](https://extensions.libreoffice.org/en/extensions/show/99339) (560) | https://extensions.libreoffice.org/assets/screenshots/6516/Slide10-v19.JPG | light | sans | sans | mono | left | none | airy | y | content slides only (chart + photo); chart series colours are content, not decoration; title layout coded from content slide |
| LO:045 | [SuperGreta!](https://extensions.libreoffice.org/en/extensions/show/1086) (506) | https://extensions.libreoffice.org/assets/screenshots/471/1.png | light | sans | sans | fill-blocks | split | none | standard | y |  |

### LO.4 Exclusions log (admissible = n)

| id | rule | evidence |
|---|---|---|
| LO:006 | A3 | A3 gradient over photo behind title/subtitle |
| LO:009 | A5 | A5 5 identical progress ovals |
| LO:011 | A3 | A3 gradient bg behind text |
| LO:013 | A5 | A5 6 identical flower icons on content slide |
| LO:015 | A5 | A5 3 identical purple cards; A6 white on lavender |
| LO:018 | A5 | A5 6 identical flower icons on content slide |
| LO:019 | A5 | A5 repeated identical border motif |
| LO:021 | A3 | A3 gradient wave behind body text |
| LO:025 | A5 | A5 8 identical circular illustrations |
| LO:026 | A3 | A3 gradient bg behind body text (both slides) |
| LO:027 | A3 | A3 gradient pill fill behind subtitle text |
| LO:028 | A7 | A7 indigo-to-purple gradient background |
| LO:035 | A3 | A3 tetromino/grid texture bg behind text |
| LO:037 | A3 | A3 photo fill behind text |
| LO:041 | A5 | A5 5 identical tree icons in footer strip (master) |
| LO:042 | A5 | A5 repeated identical flower motifs (content-slide header strip) |
| LO:043 | A3 | A3 pattern texture behind body text on content slide |

Excluded 17 of 40 → **23 admissible**. Rule counts (first-cited rule): A3=8, A5=8, A7=1.

### LO.5 Frequency table — 4 identity features `bg|heading|colour|title`, share = k/40 (denominator includes inadmissible items, §3.4)

| archetype | k | share | exemplars (raw pos) |
|---|---|---|---|
| `light\|sans\|one-accent\|left` | 5 | 5/40 = 0.125 | 2, 20, 22, 32, 40 |
| `light\|sans\|fill-blocks\|left` | 3 | 3/40 = 0.075 | 12, 14, 16 |
| `light\|sans\|one-accent\|centered` | 2 | 2/40 = 0.050 | 23, 36 |
| `dark\|sans\|fill-blocks\|split` | 1 | 1/40 = 0.025 | 29 |
| `dark\|sans\|mono\|centered` | 1 | 1/40 = 0.025 | 1 |
| `dark\|sans\|mono\|split` | 1 | 1/40 = 0.025 | 8 |
| `dark\|sans\|multi\|centered` | 1 | 1/40 = 0.025 | 3 |
| `dark\|sans\|multi\|left` | 1 | 1/40 = 0.025 | 17 |
| `dark\|sans\|multi\|split` | 1 | 1/40 = 0.025 | 5 |
| `dark\|sans\|one-accent\|centered` | 1 | 1/40 = 0.025 | 30 |
| `dark\|serif\|fill-blocks\|centered` | 1 | 1/40 = 0.025 | 34 |
| `image\|display\|multi\|full-bleed-image` | 1 | 1/40 = 0.025 | 31 |
| `light\|sans\|fill-blocks\|centered` | 1 | 1/40 = 0.025 | 39 |
| `light\|sans\|fill-blocks\|split` | 1 | 1/40 = 0.025 | 45 |
| `light\|sans\|mono\|left` | 1 | 1/40 = 0.025 | 44 |
| `light\|serif\|fill-blocks\|split` | 1 | 1/40 = 0.025 | 4 |

Distinct admissible archetypes: 16; with k≥2: 3; singletons: 13 (13/23 = 57% of admissible items).

**§4 coarsening trigger (family-wide; the orchestrator decides, not this coder):** ≥15 admissible (23), singleton items >50% (57%), <5 archetypes with k≥2 (3) — all three conditions hold for LO alone. Recount with the 4th identity feature (title layout) dropped, for the orchestrator's use:

| archetype `bg\|heading\|colour` | k | share | exemplars |
|---|---|---|---|
| `light\|sans\|one-accent` | 7 | 7/40 = 0.175 | 2, 20, 22, 23, 32, 36, 40 |
| `light\|sans\|fill-blocks` | 5 | 5/40 = 0.125 | 12, 14, 16, 39, 45 |
| `dark\|sans\|multi` | 3 | 3/40 = 0.075 | 3, 5, 17 |
| `dark\|sans\|mono` | 2 | 2/40 = 0.050 | 1, 8 |
| `dark\|sans\|fill-blocks` | 1 | 1/40 = 0.025 | 29 |
| `dark\|sans\|one-accent` | 1 | 1/40 = 0.025 | 30 |
| `dark\|serif\|fill-blocks` | 1 | 1/40 = 0.025 | 34 |
| `image\|display\|multi` | 1 | 1/40 = 0.025 | 31 |
| `light\|sans\|mono` | 1 | 1/40 = 0.025 | 44 |
| `light\|serif\|fill-blocks` | 1 | 1/40 = 0.025 | 4 |

Variant modes over admissible LO items: body [('sans', 22), ('serif', 1)]; rules/boxes [('none', 11), ('rules', 7), ('boxes', 5)]; density [('airy', 13), ('standard', 9), ('dense', 1)].

### LO.6 Bias statement
LibreOffice Extensions downloads are cumulative since the 03-2020 site migration, so older templates had longer to accumulate; the community is European (French/Spanish/Japanese-language items) and skews to open-source, education and public-sector use; the top slice includes authors who publish batches (MKCL/InDiFi series, a French master-slide series), each variant counting as one design. Previews are often master-slide placeholder screenshots or thumbnail overviews rather than filled slides, so density and body-class codes are low-confidence. Popularity is not quality (§13).

### LO.7 Second-coder ids
Ids are `LO:<raw position, zero-padded>`. The §7 sample is drawn over the whole deck family (all corpora, including the npm corpus this coder does not hold), so the orchestrator computes it: `random.Random("82:deck").sample(ids, max(min(10,len(ids)),ceil(0.25*len(ids))))`. Ids from this file: LO:001, LO:002, LO:003, LO:004, LO:005, LO:006, LO:008, LO:009, LO:011, LO:012, LO:013, LO:014, LO:015, LO:016, LO:017, LO:018, LO:019, LO:020, LO:021, LO:022, LO:023, LO:025, LO:026, LO:027, LO:028, LO:029, LO:030, LO:031, LO:032, LO:034, LO:035, LO:036, LO:037, LO:039, LO:040, LO:041, LO:042, LO:043, LO:044, LO:045, MS:001, MS:002, MS:003, MS:004, MS:005, MS:006, MS:007, MS:008, MS:009, MS:010, MS:011, MS:012, MS:013, MS:014, MS:015, MS:016, MS:017, MS:018, MS:019, MS:020, MS:021, MS:022, MS:023, MS:024, MS:025.

## Corpus MS — Microsoft Create presentation templates (L2)

### MS.1 Source
- URL requested: `https://create.microsoft.com/en-us/templates/presentations`; `curl -sL` redirected (HTTP 200) to `https://powerpoint.cloud.microsoft/create/en/presentation-templates/?source=create_flow`. Sort: none (editorial page order, not a metric). Retrieval date 2026-09-23.
- Total reachable static slice: **25 template cards** (the research/82 probe found 23). No pagination in the static HTML. Each card gives a title, a `.pptx` viewer link and one 400×225 thumbnail (title slide, index `-0-1`); other slide indices return 404. Nothing was rendered or opened.
- N = 25 on-topic, 25 codeable. No cross-listed quote/estimate items.

### MS.2–3 Raw list and coded table (page order)
Only the title slide is visible: `dens` is coded from it (all ≤15 words → `airy`) and `body` is `-` where no secondary text is visible (excluded from variant modes).

| id | Template | Thumbnail URL | bg | head | body | colour | title | rules | dens | adm | reason / note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MS:001 | Abstract airbrush presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/34efa91b-fbff-4df4-8911-13715ceb5bc7/thumbnails/400/abstract-airbrush-presentation-pink-modern-bold-0-1-109440f4fc91.webp | image | serif | sans | multi | centered | rules | airy | n | EXCLUDED A3 gradient (airbrush) bg behind text |
| MS:002 | Scientific discovery | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/51de1e5f-e0e8-4dd0-99f3-5b7584f7abdc/thumbnails/400/scientific-discovery-blue-modern-simple-0-1-d2b293ea3a82.webp | light | sans | sans | one-accent | centered | boxes | airy | n | EXCLUDED A3 photo (petri dish) behind title text |
| MS:003 | Music design | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/eb6d7fe8-c564-4d2c-86b0-33e200bb59b7/thumbnails/400/music-design-purple-modern-bold-0-1-0c2b88738642.webp | dark | display | sans | multi | split | none | airy | n | EXCLUDED A3 neon gradient/photo bg behind text |
| MS:004 | Geometric color block | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/8a9b5915-b8c7-461e-8cdd-693d48b5e323/thumbnails/400/geometric-color-block-modern-simple-0-1-46989181611e.webp | light | sans | - | fill-blocks | centered | none | airy | y |  |
| MS:005 | Pacific presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/20f81ff3-d0ce-4141-a1ab-c870ef16c9ba/thumbnails/400/pacific-presentation-blue-modern-bold-0-1-8b317bfd7dac.webp | light | serif | - | one-accent | split | none | airy | y |  |
| MS:006 | Dark modernist presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/37fc29f0-e32c-4aaa-a823-4be66e668925/thumbnails/400/dark-modernist-presentation-blue-modern-bold-0-1-80994fe225e5.webp | light | sans | sans | fill-blocks | split | none | airy | y |  |
| MS:007 | Fluorescent presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/a8a03304-e6de-4010-a628-924515496220/thumbnails/400/fluorescent-presentation-whimsical-color-block-0-1-a6e72adf5028.webp | image | display | - | multi | centered | boxes | airy | n | EXCLUDED A3 gradient bg; text sits on white window panel; gradient behind the panel, not the text itself: rule applied literally on visible bg |
| MS:008 | Hexagon presentation dark | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/63aebcec-8e39-4664-940a-dd6c2f00c54d/thumbnails/400/hexagon-presentation-dark-blue-modern-simple-0-1-7a290173f4e0.webp | dark | sans | sans | multi | left | rules | airy | y |  |
| MS:009 | Headlines design | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/acfcb60d-139a-4252-a187-2268deb0703b/thumbnails/400/headlines-design-brown-modern-simple-0-1-2490d66d19fc.webp | light | serif | sans | mono | left | rules | airy | y |  |
| MS:010 | Floral flourish | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/6ca04e33-feaa-4cf5-9b27-d56362f12ac0/thumbnails/400/floral-flourish-modern-color-block-0-1-a949d8f2a7d9.webp | dark | serif | serif | one-accent | split | boxes | airy | y |  |
| MS:011 | Feathered design | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/8527a7e3-9e8b-40b7-811a-0420cf63f5c2/thumbnails/400/feathered-design-pink-vintage-retro-0-1-cf01f5eff951.webp | image | sans | - | mono | full-bleed-image | boxes | airy | y | text on flat cream pill, photo around it |
| MS:012 | Droplet design | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e682b736-fb6a-49aa-b412-06b803d1c9a7/thumbnails/400/droplet-design-purple-modern-simple-0-1-d33ff5545e76.webp | image | sans | sans | multi | left | none | airy | n | EXCLUDED A3 holographic gradient behind text |
| MS:013 | Organic presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/1ed9553b-00c4-4092-846a-c8f7f2908f3b/thumbnails/400/organic-presentation-green-modern-bold-0-1-f26132fc1060.webp | light | serif | - | fill-blocks | centered | none | airy | y |  |
| MS:014 | City design | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/2ac7d8b4-20d7-432a-b571-8da6e509fd56/thumbnails/400/city-design-green-organic-simple-0-1-bc26ff9b6a28.webp | dark | serif | sans | mono | left | rules | airy | y |  |
| MS:015 | Shapes presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/ab1f0ecd-b87c-476f-be30-2c815ce1b1f8/thumbnails/400/shapes-presentation-blue-modern-geometric-0-1-3a403f62b530.webp | light | sans | - | fill-blocks | left | none | airy | y | title sits right-of-centre inside the circle; enum has no `right`, coded non-centered = left |
| MS:016 | Nostalgic business presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/0003c3ad-25c9-410c-ad89-28dcccb59551/thumbnails/400/nostalgic-business-presentation-black-modern-color-block-0-1-8128790c38ed.webp | image | sans | - | mono | full-bleed-image | boxes | airy | n | EXCLUDED A3 photo visible through translucent panel behind text |
| MS:017 | Minimalist color presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/29f5a614-3b3c-40fd-ae6a-7f5696624aed/thumbnails/400/minimalist-color-presentation-green-organic-simple-0-1-08d2dd091824.webp | light | sans | sans | mono | split | rules | airy | y |  |
| MS:018 | Bohemian design | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/aa287773-cb03-4ae5-b3b5-21e16eb0bb47/thumbnails/400/bohemian-design-blue-organic-boho-0-1-34a0b590325f.webp | image | display | - | mono | full-bleed-image | boxes | airy | y | script face; text on flat white panel over photo |
| MS:019 | Elegant damask pitch deck | https://createcatalog.public.onecdn.static.microsoft/uploadedfiles/uploads/20585aea-d5ba-4bfb-be2b-260d5f619cbc-elegant-damask-pitch-deck-modern-elegant-0-1.webp | dark | serif | serif | one-accent | left | boxes | airy | n | EXCLUDED A3 damask pattern texture behind text |
| MS:020 | Heartland dreamer | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/74227c3b-7f69-4d66-9366-3f192364d22b/thumbnails/400/heartland-dreamer-brown-minimal-clean-uncluttered-stylish-modern-chic-neutral-understated-balanced-0-1-d7599c042ee4.webp | light | sans | sans | mono | centered | none | airy | y |  |
| MS:021 | Muted macchiato | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/5643a32c-56b7-4f91-a2f5-12d1d8123bae/thumbnails/400/muted-macchiato-brown-bold-sophisticated-refined-contemporary-stylish-elegant-clean-minimal-formal-professional-0-1-eab32842a092.webp | dark | sans | sans | mono | left | none | airy | y |  |
| MS:022 | Modular maximalism keynote presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/740e6461-9b93-4a8d-8a06-e12b6b090328/thumbnails/400/modular-maximalism-keynote-presentation-pink-rectangular-modern-0-1-352db363e819.webp | light | sans | sans | fill-blocks | split | none | airy | n | EXCLUDED A4 painted-brush image occupying lower 60% |
| MS:023 | Impact annual presentation | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/24989aa7-1514-4bdf-90c2-cc59dc3dfec1/thumbnails/400/impact-annual-presentation-yellow-modern-simple-0-1-11547e6b4136.webp | light | sans | sans | fill-blocks | left | rules | airy | y |  |
| MS:024 | Sanguine and pearl | https://createcatalog.public.onecdn.static.microsoft/uploadedfiles/uploads/c4623bba-067b-440c-932d-bb543ee2491d-sanguine-and-pearl-gray-minimal-clean-restrained-contemporary-stylish-sophisticated-elegant-editorial-geometric-linear-formal-refined-monochromatic-architectural-professional-0-1.webp | light | sans | sans | one-accent | split | none | airy | y |  |
| MS:025 | Solace | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/3f93ee17-7713-4d90-9f1f-df2b9572b929/thumbnails/400/solace-blue-vintage-botanical-floral-damask-elegant-romantic-nostalgia-old-fashioned-antique-bygone-quaint-0-1-bddcee9daacc.webp | light | serif | sans | mono | split | none | airy | y |  |

### MS.4 Exclusions log

| id | rule | evidence |
|---|---|---|
| MS:001 | A3 | A3 gradient (airbrush) bg behind text |
| MS:002 | A3 | A3 photo (petri dish) behind title text |
| MS:003 | A3 | A3 neon gradient/photo bg behind text |
| MS:007 | A3 | A3 gradient bg; text sits on white window panel |
| MS:012 | A3 | A3 holographic gradient behind text |
| MS:016 | A3 | A3 photo visible through translucent panel behind text |
| MS:019 | A3 | A3 damask pattern texture behind text |
| MS:022 | A4 | A4 painted-brush image occupying lower 60% |

Excluded 8 of 25 → **17 admissible**. Rule counts (first-cited): A3=7, A4=1.

### MS.5 Frequency table — 4 identity features, share = k/25

| archetype | k | share | exemplars |
|---|---|---|---|
| `light\|sans\|fill-blocks\|left` | 2 | 2/25 = 0.080 | 15, 23 |
| `dark\|sans\|mono\|left` | 1 | 1/25 = 0.040 | 21 |
| `dark\|sans\|multi\|left` | 1 | 1/25 = 0.040 | 8 |
| `dark\|serif\|mono\|left` | 1 | 1/25 = 0.040 | 14 |
| `dark\|serif\|one-accent\|split` | 1 | 1/25 = 0.040 | 10 |
| `image\|display\|mono\|full-bleed-image` | 1 | 1/25 = 0.040 | 18 |
| `image\|sans\|mono\|full-bleed-image` | 1 | 1/25 = 0.040 | 11 |
| `light\|sans\|fill-blocks\|centered` | 1 | 1/25 = 0.040 | 4 |
| `light\|sans\|fill-blocks\|split` | 1 | 1/25 = 0.040 | 6 |
| `light\|sans\|mono\|centered` | 1 | 1/25 = 0.040 | 20 |
| `light\|sans\|mono\|split` | 1 | 1/25 = 0.040 | 17 |
| `light\|sans\|one-accent\|split` | 1 | 1/25 = 0.040 | 24 |
| `light\|serif\|fill-blocks\|centered` | 1 | 1/25 = 0.040 | 13 |
| `light\|serif\|mono\|left` | 1 | 1/25 = 0.040 | 9 |
| `light\|serif\|mono\|split` | 1 | 1/25 = 0.040 | 25 |
| `light\|serif\|one-accent\|split` | 1 | 1/25 = 0.040 | 5 |

Distinct admissible archetypes: 16; k≥2: 1; singletons 15/17 admissible items.

Coarsened (title layout dropped), for the orchestrator:

| archetype `bg\|heading\|colour` | k | share | exemplars |
|---|---|---|---|
| `light\|sans\|fill-blocks` | 4 | 4/25 = 0.160 | 4, 6, 15, 23 |
| `light\|sans\|mono` | 2 | 2/25 = 0.080 | 17, 20 |
| `light\|serif\|mono` | 2 | 2/25 = 0.080 | 9, 25 |
| `dark\|sans\|mono` | 1 | 1/25 = 0.040 | 21 |
| `dark\|sans\|multi` | 1 | 1/25 = 0.040 | 8 |
| `dark\|serif\|mono` | 1 | 1/25 = 0.040 | 14 |
| `dark\|serif\|one-accent` | 1 | 1/25 = 0.040 | 10 |
| `image\|display\|mono` | 1 | 1/25 = 0.040 | 18 |
| `image\|sans\|mono` | 1 | 1/25 = 0.040 | 11 |
| `light\|sans\|one-accent` | 1 | 1/25 = 0.040 | 24 |
| `light\|serif\|fill-blocks` | 1 | 1/25 = 0.040 | 13 |
| `light\|serif\|one-accent` | 1 | 1/25 = 0.040 | 5 |

Variant modes over admissible MS items: rules/boxes [('none', 9), ('rules', 5), ('boxes', 3)]; density [('airy', 17)]; body [('sans', 10), ('-', 6), ('serif', 1)].

### MS.6 Bias statement
Microsoft Create is Microsoft's editorial selection and this is only the first static slice of one category page; page order is not a metric. One thumbnail per template (title slide), so the result is the prevalence of title-slide styling in a curated catalogue, not usage. Templates lean photo/gradient/paint-heavy, which A3/A4 exclude.

## Protocol ambiguities met (for the orchestrator)
1. **A3 scope for decks.** A3 says "behind body text"; title slides often have no body text. Coded literally-strict: any visible gradient/texture/photo directly behind title, subtitle or body text excludes; text on a flat panel over a photo/gradient (LO:031, LO:051, MS:011, MS:018) is admitted. MS:007 is excluded on the gradient behind its white window panel, which is inconsistent with that admission rule — flag for the second coder.
2. **Title-slide-only previews.** MS gives only slide 1; 12+ LO items show only a title slide or master-slide thumbnails. Density, body class and rules are therefore low-confidence; deck density rule (words on first content slide) is unavailable for all of MS.
3. **Title layout `split` vs `left`.** No threshold in §4. Applied: image ≥30% of slide area beside the text → `split`, else `left` (or `centered`). Text right-of-centre (MS:015) has no enum value; coded `left`.
4. **Background when title and content slides differ.** Coded from the title slide (LO:017, LO:023, LO:034, LO:043). LO:034's golden title slide has L=0.47, so `dark` by the L<0.5 rule although the deck reads light.
5. **Handwriting/display body faces.** §4 body enum lacks `display` (LO:021); coded `sans`.
6. **A6 contrast** was assessed by eye, not with `color.py` on sampled hexes, for every item except LO:040 (accent sampled). A7: LO:040's blue (#5174b7) is near but not equal to any listed Office default, so not excluded.
7. **Colour-use with photographic decks.** Deck background is excluded from `fill-blocks`, and photos are excluded; a slide whose only large fill is the background codes `mono`/`one-accent`. This makes `fill-blocks` mean "an additional large panel".
8. **Thin corpus counts.** LO reached 40 on-topic codeable items at raw #45 (23 admissible); the 4-feature archetype space fragments (coarsening trigger met for LO alone; MS: see MS.5).
9. **MS count.** The page delivered 25 cards vs 23 in the research/82 probe; the corpus is time-varying.
10. **Ranking Metric strings** (for the orchestrator): `share:libreoffice-impress:k/40 by downloads`, `prevalence:microsoft-create-presentations:k/25`.

