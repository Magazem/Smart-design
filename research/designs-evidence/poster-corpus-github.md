# Poster corpus - GitHub L1 `"poster template" latex` (F.a)

Coder: Design Researcher. Counts only (research/82 section 1). Retrieved 2026-09-23. Identity archetype = `columns|heading|colour|header` (section 4); variant orientation (poster), body class, rules/boxes, density. Rules/measurements are eye-judged at thumbnail size unless stated; contrast values are estimates (82a C9). Conventions follow `flyer-corpus.md`; 82a C1-C16 applied.

## P.1 Corpus
- URL: `https://api.github.com/search/repositories?q=%22poster+template%22+latex&sort=stars&order=desc&per_page=100` (curl -s -A smart-design-research, one call, no rate-limit retry needed)
- Query: `"poster template" latex`, sort stars desc, per_page 100, retrieved 2026-09-23. **total_count = 133** (only page 1 = 100 items fetched; the walk reached N=40 at rank 52, so page 2 was not needed).
- Walk: native star order, ranks 1-52 evaluated. On-topic codeable **N = 40** reached at rank 52 (ranks {1, 2, 3, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 49, 50, 51, 52}). Walk cap 200 not reached.
- Preview = README image, or (when the README has none) a committed example PDF page 1 / image found in the repo root listing on github.com (HTML page, not the API); PDFs rendered at 80 dpi to the temp dir, never into the repo. Ranking Metric string for provenance: `share:GH:k/40 by stars`. **L1 valid: 40 on-topic codeable items (82 F2 satisfied).**
- Skew: academic/conference posters; a large share are university re-themes of a few upstream LaTeX classes (Gemini/beamerposter, baposter, tikzposter). 6+ items reuse the Gemini theme skeleton (same demo text) with different colours. Not de-duplicated because none declares itself a fork/port with identical assets (rule 82 section 3.2 is mechanical); consequence: navy/garnet/red title-band archetypes are over-counted relative to design diversity. The MS(posters) catalogue has only 5 posters (corroboration only, see poster-corpus-ms.md), so poster combined share = this corpus alone.

## P.2 Raw list, ranks 1-52 (status)
| rank | repo | stars | status |
|---|---|---|---|
| 1 | [RylanSchaeffer/Stanford-LaTeX-Poster-Template](https://github.com/RylanSchaeffer/Stanford-LaTeX-Poster-Template) | 245 | coded GH:001 |
| 2 | [LanaSina/better_poster_latex](https://github.com/LanaSina/better_poster_latex) | 111 | coded GH:002 |
| 3 | [gbaydin/oxford-poster](https://github.com/gbaydin/oxford-poster) | 78 | coded GH:003 |
| 4 | [js8544/nyu-latex-templates](https://github.com/js8544/nyu-latex-templates) | 40 | uncodeable: README image jinshang.me/images/demo-poster.png is dead (404); no repo asset found |
| 5 | [zhengkd95/thu_poster_template](https://github.com/zhengkd95/thu_poster_template) | 15 | coded GH:005 |
| 6 | [aeberspaecher/pdfposter](https://github.com/aeberspaecher/pdfposter) | 14 | coded GH:006 |
| 7 | [k4rtik/uchicago-poster](https://github.com/k4rtik/uchicago-poster) | 14 | uncodeable: no README image, no committed PDF/PNG in repo root (only logos/ dir) |
| 8 | [sanhacheong/stanford_beamer_poster](https://github.com/sanhacheong/stanford_beamer_poster) | 12 | coded GH:008 |
| 9 | [yaoshanliang/XJTLU-Poster-Template](https://github.com/yaoshanliang/XJTLU-Poster-Template) | 12 | coded GH:009 |
| 10 | [klb2/scientific-poster-template](https://github.com/klb2/scientific-poster-template) | 11 | coded GH:010 |
| 11 | [keevindoherty/stevens_latex_poster](https://github.com/keevindoherty/stevens_latex_poster) | 10 | uncodeable: README preview keevindoherty.github.io/img/poster_portrait-preview.jpg is dead (404) |
| 12 | [jeongwhanchoi/yonsei-poster](https://github.com/jeongwhanchoi/yonsei-poster) | 7 | coded GH:012 |
| 13 | [Benjamin-Vincent/poster_template](https://github.com/Benjamin-Vincent/poster_template) | 7 | coded GH:013 |
| 14 | [academic-templates/tex-poster-template](https://github.com/academic-templates/tex-poster-template) | 6 | coded GH:014 |
| 15 | [hyoiutu/myPosterTemplate](https://github.com/hyoiutu/myPosterTemplate) | 6 | uncodeable: only placeholder.jpg (a grey Placeholder Image tile), not a poster design |
| 16 | [pskarin/wasp-poster](https://github.com/pskarin/wasp-poster) | 5 | coded GH:016 |
| 17 | [mtekman/MeInBio-LaTex-Poster-Template](https://github.com/mtekman/MeInBio-LaTex-Poster-Template) | 5 | coded GH:017 |
| 18 | [latexstudio/A0-Poster-Template](https://github.com/latexstudio/A0-Poster-Template) | 5 | uncodeable: README previews live on the upstream gemini repo path that now 404s (own preview none) |
| 19 | [suraj-srinivas/latex-poster-template](https://github.com/suraj-srinivas/latex-poster-template) | 5 | coded GH:019 |
| 20 | [guestdaniel/postertemplate](https://github.com/guestdaniel/postertemplate) | 4 | coded GH:020 |
| 21 | [ShuiYidi/sjtu-beamerposter-template](https://github.com/ShuiYidi/sjtu-beamerposter-template) | 4 | coded GH:021 |
| 22 | [esandivi9/VU-latex-poster-template](https://github.com/esandivi9/VU-latex-poster-template) | 3 | coded GH:022 |
| 23 | [uit-cosmo/poster-template](https://github.com/uit-cosmo/poster-template) | 3 | coded GH:023 |
| 24 | [LIKS/horizontal_poster_template_mii](https://github.com/LIKS/horizontal_poster_template_mii) | 3 | coded GH:024 |
| 25 | [yxlao/china3dv-poster-template](https://github.com/yxlao/china3dv-poster-template) | 3 | uncodeable: blank scaffold (title + empty rounded boxes only), 82a C3 |
| 26 | [mg643l/University-of-Liverpool-Unofficial-LaTeX-Poster-Template](https://github.com/mg643l/University-of-Liverpool-Unofficial-LaTeX-Poster-Template) | 3 | coded GH:026 |
| 27 | [Computer-Vision-Group-Siegen/raml-poster-template](https://github.com/Computer-Vision-Group-Siegen/raml-poster-template) | 3 | coded GH:027 |
| 28 | [EliNaig/usc-poster-template](https://github.com/EliNaig/usc-poster-template) | 3 | coded GH:028 |
| 29 | [ojeda-e/Latex-poster-template](https://github.com/ojeda-e/Latex-poster-template) | 2 | coded GH:029 |
| 30 | [iaytutu1/MICCAI-2026-LaTeX-Poster-Template](https://github.com/iaytutu1/MICCAI-2026-LaTeX-Poster-Template) | 2 | uncodeable: no README, no preview file |
| 31 | [R0mb0/Tearable_poster_template_in_LaTeX](https://github.com/R0mb0/Tearable_poster_template_in_LaTeX) | 2 | off-topic: tear-off flyer (other family) |
| 32 | [Franklinwang72/auburn-poster-templates](https://github.com/Franklinwang72/auburn-poster-templates) | 2 | coded GH:032 |
| 33 | [JanserLatex/InfographicPosterTemplate](https://github.com/JanserLatex/InfographicPosterTemplate) | 2 | coded GH:033 |
| 34 | [dronir/NewHYposter](https://github.com/dronir/NewHYposter) | 2 | uncodeable: no README image, no preview file in repo root |
| 35 | [liangzid/PolyU-Poster-Template](https://github.com/liangzid/PolyU-Poster-Template) | 2 | coded GH:035 |
| 36 | [shatz01/Unofficial-Poster-Template-for-Technion-Computer-Science](https://github.com/shatz01/Unofficial-Poster-Template-for-Technion-Computer-Science) | 2 | coded GH:036 |
| 37 | [dham/imposter](https://github.com/dham/imposter) | 1 | coded GH:037 |
| 38 | [MarkTuddenham/soton_poster](https://github.com/MarkTuddenham/soton_poster) | 1 | coded GH:038 |
| 39 | [husk214/poster_template](https://github.com/husk214/poster_template) | 1 | coded GH:039 |
| 40 | [francois-rozet/sleek-poster](https://github.com/francois-rozet/sleek-poster) | 1 | coded GH:040 |
| 41 | [johnlmbui/UMBC-LaTeX-Poster-Template](https://github.com/johnlmbui/UMBC-LaTeX-Poster-Template) | 1 | coded GH:041 |
| 42 | [a2s-institute/poster-template](https://github.com/a2s-institute/poster-template) | 1 | coded GH:042 |
| 43 | [Mygetsy/skoltech-latex-poster-template](https://github.com/Mygetsy/skoltech-latex-poster-template) | 1 | coded GH:043 |
| 44 | [jweede/UC-Latex-Poster-Template](https://github.com/jweede/UC-Latex-Poster-Template) | 1 | coded GH:044 |
| 45 | [fact-project/latex_poster](https://github.com/fact-project/latex_poster) | 1 | uncodeable: no README image, no preview file in repo root |
| 46 | [sdysch/LaTeX_poster_template](https://github.com/sdysch/LaTeX_poster_template) | 1 | coded GH:046 |
| 47 | [while519/baposter](https://github.com/while519/baposter) | 1 | uncodeable: only baposter documentation PDFs (guide/docs figures), no template poster preview |
| 48 | [alejandrogallo/tuwien-poster-template](https://github.com/alejandrogallo/tuwien-poster-template) | 1 | uncodeable: no preview file in repo root |
| 49 | [ChengranAA/UWO_poster_latex_template](https://github.com/ChengranAA/UWO_poster_latex_template) | 1 | coded GH:049 |
| 50 | [harisont/GUnofficial-poster-template](https://github.com/harisont/GUnofficial-poster-template) | 1 | coded GH:050 |
| 51 | [guanqun-yang/StevensTechBeamerPosterTemplate](https://github.com/guanqun-yang/StevensTechBeamerPosterTemplate) | 1 | coded GH:051 |
| 52 | [paulinelemenkova/LaTeX-poster-template-A0-portrait](https://github.com/paulinelemenkova/LaTeX-poster-template-A0-portrait) | 1 | coded GH:052 |

Totals for ranks 1-52: coded 40, uncodeable/off-topic 12 (4,7,11,15,18,25,30,31,34,45,47,48).

## P.3 Coded table (N = 40)
| id | repo | stars | orient | columns | head | body | colour | header | rules | dens | adm | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GH:001 | RylanSchaeffer/Stanford-LaTeX-Poster-Template | 245 | landscape | 3+ | sans | sans | fill-blocks | band | rules | dense | y | dark-red title band + footer ~12% of area; Gemini-style beamerposter |
| GH:002 | LanaSina/better_poster_latex | 111 | portrait | 2-sidebar | sans | sans | fill-blocks | band | rules | airy | y | green title block ~25% of area; narrow right column of extra figures |
| GH:003 | gbaydin/oxford-poster | 78 | landscape | 3+ | sans | sans | fill-blocks | band | boxes | airy | y | navy title band; filled block headers; big logo image |
| GH:005 | zhengkd95/thu_poster_template | 15 | landscape | 3+ | serif | serif | one-accent | plain-centered | boxes | dense | n | A8 every content block is individually bordered (purple frames) |
| GH:006 | aeberspaecher/pdfposter | 14 | portrait | 3+ | serif | serif | multi | plain-centered | boxes | standard | y | green/blue/red coloured boxes on a pale-green page background (about half the blocks boxed, not >50%) |
| GH:008 | sanhacheong/stanford_beamer_poster | 12 | landscape | 3+ | serif | serif | one-accent | ruled | boxes | standard | y | red rule directly under the header; 2 of 6 blocks red-bordered |
| GH:009 | yaoshanliang/XJTLU-Poster-Template | 12 | portrait | 2-equal | sans | sans | one-accent | band | rules | dense | y | purple title band ~8% (<10% so not fill-blocks) |
| GH:010 | klb2/scientific-poster-template | 11 | portrait | 2-equal | sans | sans | one-accent | band | boxes | dense | y | teal title block behind the title; teal block header bars |
| GH:012 | jeongwhanchoi/yonsei-poster | 7 | landscape | 3+ | sans | sans | fill-blocks | band | boxes | airy | y | same layout as #3 (Oxford) re-themed; not a declared fork so counted separately |
| GH:013 | Benjamin-Vincent/poster_template | 7 | portrait | 2-equal | sans | sans | one-accent | plain-centered | boxes | dense | n | A8 every block is a filled/bordered box on a dark page background |
| GH:014 | academic-templates/tex-poster-template | 6 | portrait | 3+ | sans | serif | one-accent | ruled | boxes | dense | y | blue full-width rule under the header; one boxed note |
| GH:016 | pskarin/wasp-poster | 5 | portrait | 2-equal | sans | sans | one-accent | plain-left | boxes | dense | y | teal filled block header bars; dark footer bar with logo |
| GH:017 | mtekman/MeInBio-LaTex-Poster-Template | 5 | portrait | 2-equal | sans | sans | fill-blocks | plain-left | boxes | dense | n | A8 every block boxed with coloured frames; image shows two designs (2018/2021), first = 2018 per C4 |
| GH:019 | suraj-srinivas/latex-poster-template | 5 | landscape | 3+ | sans | sans | one-accent | plain-centered | none | airy | y | gold section headers, grey body; body/heading contrast >=5.9:1 sampled (estimate) |
| GH:020 | guestdaniel/postertemplate | 4 | landscape | 3+ | serif | serif | one-accent | ruled | rules | airy | y | maroon rule under header; file is blank.pdf but renders a filled example poster |
| GH:021 | ShuiYidi/sjtu-beamerposter-template | 4 | landscape | 3+ | serif | sans | fill-blocks | band | boxes | dense | y | black title band ~18% of the sheet; block header bars |
| GH:022 | esandivi9/VU-latex-poster-template | 3 | landscape | 3+ | sans | sans | multi | plain-left | rules | standard | y | blue title with VU logo right; blue/orange/red section accents |
| GH:023 | uit-cosmo/poster-template | 3 | portrait | 2-equal | sans | sans | fill-blocks | band | boxes | dense | y | dark-blue title band; tinted highlight blocks |
| GH:024 | LIKS/horizontal_poster_template_mii | 3 | landscape | 3+ | serif | serif | one-accent | ruled | boxes | dense | y | red rule under the centred header; red boxes for Abstract/Pseudocode |
| GH:026 | mg643l/University-of-Liverpool-Unofficial-LaTeX-Poster-Template | 3 | landscape | 3+ | sans | sans | fill-blocks | band | boxes | standard | y | navy title band ~12%; tinted blocks |
| GH:027 | Computer-Vision-Group-Siegen/raml-poster-template | 3 | portrait | 2-equal | sans | sans | fill-blocks | band | boxes | dense | y | dark-blue header with logos; blue block bars |
| GH:028 | EliNaig/usc-poster-template | 3 | landscape | 3+ | sans | sans | fill-blocks | band | boxes | standard | y | garnet title band + footer; tinted highlighted blocks |
| GH:029 | ojeda-e/Latex-poster-template | 2 | landscape | 3+ | serif | serif | one-accent | plain-centered | none | dense | y | centred serif title, logos both sides, dark-red section headings |
| GH:032 | Franklinwang72/auburn-poster-templates | 2 | landscape | 3+ | sans | sans | multi | plain-left | boxes | dense | y | navy title text + orange accent, dark theorem boxes; 19 themes, first preview coded |
| GH:033 | JanserLatex/InfographicPosterTemplate | 2 | portrait | 1 | sans | sans | mono | plain-left | boxes | airy | y | infographic-style poster; square preview coded as portrait (H>=W); bordered fact boxes |
| GH:035 | liangzid/PolyU-Poster-Template | 2 | landscape | 3+ | sans | sans | fill-blocks | band | boxes | dense | y | red title band ~20% of the sheet; authors blurred in preview |
| GH:036 | shatz01/Unofficial-Poster-Template-for-Technion-Computer-Science | 2 | landscape | 3+ | sans | sans | one-accent | ruled | boxes | standard | y | thin rule under the centred header with logos; tinted block |
| GH:037 | dham/imposter | 1 | portrait | 2-equal | sans | serif | one-accent | plain-left | boxes | dense | n | A8 every block (getting started, positioning...) is bordered; gold-bordered title box |
| GH:038 | MarkTuddenham/soton_poster | 1 | landscape | 3+ | serif | serif | fill-blocks | plain-left | boxes | dense | y | serif title + large Southampton logo; teal block bars with tinted bodies |
| GH:039 | husk214/poster_template | 1 | portrait | 2-sidebar | serif | serif | one-accent | plain-centered | rules | dense | y | centred Japanese/English title; narrow right column; light-blue block bars |
| GH:040 | francois-rozet/sleek-poster | 1 | landscape | 2-equal | sans | sans | multi | band | boxes | standard | y | navy title band ~10%; orange highlight text |
| GH:041 | johnlmbui/UMBC-LaTeX-Poster-Template | 1 | landscape | 3+ | sans | sans | fill-blocks | band | boxes | standard | y | yellow/gold title band with logo; tinted highlighted blocks |
| GH:042 | a2s-institute/poster-template | 1 | portrait | 2-equal | sans | sans | one-accent | plain-left | rules | airy | y | blue rules under section titles; large b-it logos |
| GH:043 | Mygetsy/skoltech-latex-poster-template | 1 | portrait | 2-equal | sans | sans | one-accent | band | boxes | dense | n | A8 every block has a green frame; green title band ~8% |
| GH:044 | jweede/UC-Latex-Poster-Template | 1 | landscape | 3+ | serif | serif | one-accent | ruled | rules | standard | y | thick crimson rule under the centred title block |
| GH:046 | sdysch/LaTeX_poster_template | 1 | portrait | 2-equal | serif | sans | multi | plain-centered | boxes | airy | n | A3 blue-to-lilac gradient page background behind all text; mostly empty example blocks |
| GH:049 | ChengranAA/UWO_poster_latex_template | 1 | landscape | 3+ | serif | serif | fill-blocks | band | boxes | dense | y | purple title band ~15% + section header bars |
| GH:050 | harisont/GUnofficial-poster-template | 1 | portrait | 2-equal | sans | sans | one-accent | plain-left | boxes | airy | y | white cards on grey ground; logo right of title |
| GH:051 | guanqun-yang/StevensTechBeamerPosterTemplate | 1 | landscape | 3+ | serif | sans | one-accent | plain-left | boxes | standard | y | crest left, serif dark-red title; large grey image placeholder |
| GH:052 | paulinelemenkova/LaTeX-poster-template-A0-portrait | 1 | portrait | 3+ | mono | serif | one-accent | plain-centered | boxes | dense | y | monospaced blue title, logos left/right, blue block bars; A0 portrait |

## P.4 Exclusions log (item stays in N)
| id | rule | evidence |
|---|---|---|
| GH:005 | A8 | A8 every content block is individually bordered (purple frames) |
| GH:013 | A8 | A8 every block is a filled/bordered box on a dark page background |
| GH:017 | A8 | A8 every block boxed with coloured frames; image shows two designs (2018/2021), first = 2018 per C4 |
| GH:037 | A8 | A8 every block (getting started, positioning...) is bordered; gold-bordered title box |
| GH:043 | A8 | A8 every block has a green frame; green title band ~8% |
| GH:046 | A3 | A3 blue-to-lilac gradient page background behind all text; mostly empty example blocks |

Admissible 34 / 40, excluded 6 (A8 x5, A3 x1). Contrast: estimates from thumbnails/renders (82a C9); #19 body sampled at >=5.9:1.

## P.5 Frequency table k/40 (denominator includes inadmissible; [x] = inadmissible)
| archetype `columns\|heading\|colour\|header` | k | k/40 | admissible k | exemplars |
|---|---|---|---|---|
| `3+\|sans\|fill-blocks\|band` | 7 | 0.175 | 7 | GH:001, GH:003, GH:012, GH:026, GH:028, GH:035, GH:041 |
| `2-equal\|sans\|one-accent\|plain-left` | 4 | 0.100 | 3 | GH:016, GH:037[x], GH:042, GH:050 |
| `3+\|serif\|one-accent\|ruled` | 4 | 0.100 | 4 | GH:008, GH:020, GH:024, GH:044 |
| `2-equal\|sans\|one-accent\|band` | 3 | 0.075 | 2 | GH:009, GH:010, GH:043[x] |
| `2-equal\|sans\|fill-blocks\|band` | 2 | 0.050 | 2 | GH:023, GH:027 |
| `3+\|sans\|multi\|plain-left` | 2 | 0.050 | 2 | GH:022, GH:032 |
| `3+\|sans\|one-accent\|ruled` | 2 | 0.050 | 2 | GH:014, GH:036 |
| `3+\|serif\|fill-blocks\|band` | 2 | 0.050 | 2 | GH:021, GH:049 |
| `3+\|serif\|one-accent\|plain-centered` | 2 | 0.050 | 1 | GH:005[x], GH:029 |
| `1\|sans\|mono\|plain-left` | 1 | 0.025 | 1 | GH:033 |
| `2-equal\|sans\|fill-blocks\|plain-left` | 1 | 0.025 | 0 | GH:017[x] |
| `2-equal\|sans\|multi\|band` | 1 | 0.025 | 1 | GH:040 |
| `2-equal\|sans\|one-accent\|plain-centered` | 1 | 0.025 | 0 | GH:013[x] |
| `2-equal\|serif\|multi\|plain-centered` | 1 | 0.025 | 0 | GH:046[x] |
| `2-sidebar\|sans\|fill-blocks\|band` | 1 | 0.025 | 1 | GH:002 |
| `2-sidebar\|serif\|one-accent\|plain-centered` | 1 | 0.025 | 1 | GH:039 |
| `3+\|mono\|one-accent\|plain-centered` | 1 | 0.025 | 1 | GH:052 |
| `3+\|sans\|one-accent\|plain-centered` | 1 | 0.025 | 1 | GH:019 |
| `3+\|serif\|fill-blocks\|plain-left` | 1 | 0.025 | 1 | GH:038 |
| `3+\|serif\|multi\|plain-centered` | 1 | 0.025 | 1 | GH:006 |
| `3+\|serif\|one-accent\|plain-left` | 1 | 0.025 | 1 | GH:051 |

21 distinct archetypes; 34 admissible items in 18 admissible archetypes; k>=2 archetypes: 9; singleton admissible items 9/34.
Coarsening trigger (82 section 4: >=15 admissible items, >50% of admissible items singletons, <5 archetypes with k>=2): not triggered.

Variant modes over admissible items: orientation [('landscape', 21), ('portrait', 13)]; body [('sans', 23), ('serif', 11)]; rules/boxes [('boxes', 24), ('rules', 8), ('none', 2)]; density [('dense', 16), ('standard', 10), ('airy', 8)].

## P.7 Second-coder ids and seed
Ids (GH corpus, 40): GH:001 GH:002 GH:003 GH:005 GH:006 GH:008 GH:009 GH:010 GH:012 GH:013 GH:014 GH:016 GH:017 GH:019 GH:020 GH:021 GH:022 GH:023 GH:024 GH:026 GH:027 GH:028 GH:029 GH:032 GH:033 GH:035 GH:036 GH:037 GH:038 GH:039 GH:040 GH:041 GH:042 GH:043 GH:044 GH:046 GH:049 GH:050 GH:051 GH:052
Per-corpus sample under `random.Random("82:poster")` (poster has one coded corpus, so it equals the family-wide sample of C10): GH:033 GH:042 GH:038 GH:039 GH:024 GH:032 GH:035 GH:051 GH:046 GH:029

## P.8 Ambiguities met
1. Repos with no README image were previewed from a committed example PDF/PNG in the repo root (listing scraped from the github.com HTML page, not the API). Choice of file (poster.pdf/main.pdf/example.pdf/...) is by name; #20 `blank.pdf` renders a filled poster.
2. `band` vs `image-hero`/`fill-blocks`: title bands are ~8-25% of the sheet; fill-blocks needs >=10% total solid fill (header + footer + block bars counted where visible). Items at 8-10% (#9, #43) were coded one-accent.
3. `columns` for posters with a wide main column and a narrow right column (#2, #39) coded 2-sidebar; 3 equal columns and multi-column beamer layouts coded 3+.
4. A8 applied where every content block is enclosed (frames or filled boxes): #5, #13, #17, #37, #43; #6/#8 left admissible (about half boxed).
5. #17 shows two designs in one image (2018 | 2021): coded the first (2018) per C4. #33 preview is square; orientation coded portrait (H>=W).
6. Dedup not applied to visually similar Gemini/Oxford re-themes (#3 vs #12; #1, #26, #28, #41 share the Gemini layout) because rule 3.2 needs mechanical evidence of a fork/port; #71 codork/Stanford-CS224N-Poster (beyond rank 52) is a declared fork of #1 with identical images and would be dropped if reached.
7. Body class and heading class are eye-judged at thumbnail size (LaTeX defaults Computer Modern vs sans themes); rules/boxes for "highlighted" tinted blocks coded boxes.
