# Letter corpus - GitHub L1 `"letter template"` (F.a)

Coder: Design Researcher. Conventions as `flyer-corpus.md`; header treatment and colour use per **research/82a-general.md** (title = sender name, the first line of the sender block; logos never the title; boundary = date/recipient/salutation; band d <=40% page height; colour B1-B6, background/logos/watermarks excluded). Letter variant: letterhead position. Contrast values are estimates (C9).

## LT.1 Corpus
- URL: `https://api.github.com/search/repositories?q=%22letter+template%22&sort=stars&order=desc&per_page=100 (+ &page=2 fetched)`, sort stars desc, per_page 100. **total_count = 631**. Retrieved 2026-09-24.
- Walk: native order, ranks 1-83 evaluated; **N = 40 on-topic codeable** items reached at rank 83 (walk cap 200 not reached). **L1 valid** (>=40 on-topic codeable, F2 satisfied). Ranking Metric string: `share:GH:k/40 by stars`.
- Preview: README image, else a committed example PDF page 1 (from the github.com repo root page). Page 1 of the letter is coded.
- On-topic (82 section 3.2): letter templates; **cover-letter / CV repos are other-family and are excluded and cross-listed** to cover-letter. Journal *response/rebuttal* letters (GH:002, 010, 016, 021, 025, 028, 064; 7 items) are on-topic by name and by the query, but are structurally reports (comment/response lists); disclosed.
- Skew: ~45% are Chinese-university recommendation/application letter templates sharing one upstream skeleton (logo + address block + faint seal watermark); German DIN 5008 letters (Sematre, jgehrcke, black-snake, klingtnet, smartmic x2, mariuskiessling, corrupt/ckiri beyond the walk) form the second cluster. Watermark items are admissible under C32 when faint (LT.8).

## LT.2 Raw list, ranks 1-83 (status)
| rank | repo | stars | status |
|---|---|---|---|
| 1 | [aeris/gdpr](https://github.com/aeris/gdpr) | 415 | uncodeable/off-topic: no preview (GDPR letter text template) |
| 2 | [shellywhen/Journal-Response-Letter-Template-LaTeX](https://github.com/shellywhen/Journal-Response-Letter-Template-LaTeX) | 358 | coded GH:002 |
| 3 | [Sematre/typst-letter-pro](https://github.com/Sematre/typst-letter-pro) | 217 | coded GH:003 |
| 4 | [ethanhe42/resume-template](https://github.com/ethanhe42/resume-template) | 137 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 5 | [eddelbuettel/linl](https://github.com/eddelbuettel/linl) | 117 | coded GH:005 |
| 6 | [nycdsa/tech-rejection-letters](https://github.com/nycdsa/tech-rejection-letters) | 90 | uncodeable/off-topic: off-topic: rejection-letter wording repository |
| 7 | [mcanouil/quarto-letter](https://github.com/mcanouil/quarto-letter) | 80 | uncodeable/off-topic: no preview |
| 8 | [pascal-huber/typst-letter-template](https://github.com/pascal-huber/typst-letter-template) | 48 | coded GH:008 |
| 9 | [jgehrcke/latex-briefvorlage](https://github.com/jgehrcke/latex-briefvorlage) | 44 | coded GH:009 |
| 10 | [faicaiwawa/Response_Letter_Template](https://github.com/faicaiwawa/Response_Letter_Template) | 41 | coded GH:010 |
| 11 | [firefly-cpp/cover-letter-latex](https://github.com/firefly-cpp/cover-letter-latex) | 32 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 12 | [ustctug/ustcletter](https://github.com/ustctug/ustcletter) | 30 | uncodeable/off-topic: README PDF is documentation, not a letter |
| 13 | [FrancesCoronel/cover-letter-templates](https://github.com/FrancesCoronel/cover-letter-templates) | 29 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 14 | [dvdvgt/typst-letter](https://github.com/dvdvgt/typst-letter) | 28 | coded GH:014 |
| 15 | [anthonyattard/Deedy-Resume-Cover-Letter](https://github.com/anthonyattard/Deedy-Resume-Cover-Letter) | 24 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 16 | [JohannaXie/Response-Letter-Template](https://github.com/JohannaXie/Response-Letter-Template) | 24 | coded GH:016 |
| 17 | [leungll/ByteDance-Letter-Template](https://github.com/leungll/ByteDance-Letter-Template) | 19 | coded GH:017 |
| 18 | [arubertoson/latex-resume](https://github.com/arubertoson/latex-resume) | 15 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 19 | [TimmyChan/data-science-tech-cover-letter-template](https://github.com/TimmyChan/data-science-tech-cover-letter-template) | 15 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 20 | [ocamp020/JMP_Cover_Letter](https://github.com/ocamp020/JMP_Cover_Letter) | 15 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 21 | [cqylunlun/journal-response-letter-template](https://github.com/cqylunlun/journal-response-letter-template) | 13 | coded GH:021 |
| 22 | [ZhonghaoJiang/Response_Letter_Template](https://github.com/ZhonghaoJiang/Response_Letter_Template) | 12 | uncodeable/off-topic: no preview |
| 23 | [leungll/NENU-Letter-Template](https://github.com/leungll/NENU-Letter-Template) | 12 | coded GH:023 |
| 24 | [HovChen/HDU-Letter-Template](https://github.com/HovChen/HDU-Letter-Template) | 12 | coded GH:024 |
| 25 | [alxvth/Revision-Rebuttal-Letter-Template](https://github.com/alxvth/Revision-Rebuttal-Letter-Template) | 12 | coded GH:025 |
| 26 | [UCL/ucl-letter](https://github.com/UCL/ucl-letter) | 11 | uncodeable/off-topic: only a banner asset |
| 27 | [juliantao/qletter](https://github.com/juliantao/qletter) | 11 | coded GH:027 |
| 28 | [cherise215/Journal-Response-Letter-Template](https://github.com/cherise215/Journal-Response-Letter-Template) | 11 | coded GH:028 |
| 29 | [yosgi/Typing_Love_Letter](https://github.com/yosgi/Typing_Love_Letter) | 11 | uncodeable/off-topic: no preview |
| 30 | [JmlrOrg/jmlr-coverletter](https://github.com/JmlrOrg/jmlr-coverletter) | 10 | coded GH:030 |
| 31 | [lagerfeuer/office-resume](https://github.com/lagerfeuer/office-resume) | 10 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 32 | [Tanglumy/NKU-Recommendation-Letter-Template](https://github.com/Tanglumy/NKU-Recommendation-Letter-Template) | 10 | coded GH:032 |
| 33 | [xhghhh/UESTC-Recommendation-Letter-Template](https://github.com/xhghhh/UESTC-Recommendation-Letter-Template) | 10 | coded GH:033 |
| 34 | [thatfloflo/typst-pc-letter](https://github.com/thatfloflo/typst-pc-letter) | 9 | coded GH:034 |
| 35 | [Hai-Jun-Yan/Response_Letter_Template](https://github.com/Hai-Jun-Yan/Response_Letter_Template) | 9 | uncodeable/off-topic: no preview |
| 36 | [black-snake/LaTeX-letter](https://github.com/black-snake/LaTeX-letter) | 9 | coded GH:036 |
| 37 | [suretrust/cover-letter-editor](https://github.com/suretrust/cover-letter-editor) | 9 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 38 | [avonmoll/bamdone-rebuttal](https://github.com/avonmoll/bamdone-rebuttal) | 8 | uncodeable/off-topic: thumbnail only shows rebuttal tool |
| 39 | [CFC87/Fudan-Recommendation-Letter-Template](https://github.com/CFC87/Fudan-Recommendation-Letter-Template) | 7 | coded GH:039 |
| 40 | [the-au-forml-lab/au_ccs_letterhead_template](https://github.com/the-au-forml-lab/au_ccs_letterhead_template) | 7 | coded GH:040 |
| 41 | [npujol/chuli-cv](https://github.com/npujol/chuli-cv) | 7 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 42 | [HarshitKumar9030/Letteran](https://github.com/HarshitKumar9030/Letteran) | 7 | uncodeable/off-topic: off-topic: Python script |
| 43 | [klingtnet/DIN-letter-template](https://github.com/klingtnet/DIN-letter-template) | 6 | coded GH:043 |
| 44 | [bast/quarto-letter-template](https://github.com/bast/quarto-letter-template) | 6 | coded GH:044 |
| 45 | [hpzhan66/Journal_Response_Letter_Template](https://github.com/hpzhan66/Journal_Response_Letter_Template) | 6 | uncodeable/off-topic: no preview |
| 46 | [xjasonlyu/HDU-letter-template](https://github.com/xjasonlyu/HDU-letter-template) | 5 | coded GH:046 |
| 47 | [cjdet/unl-letter-template](https://github.com/cjdet/unl-letter-template) | 4 | coded GH:047 |
| 48 | [smartmic/letter-template-lout](https://github.com/smartmic/letter-template-lout) | 4 | coded GH:048 |
| 49 | [smartmic/letter-template-latex](https://github.com/smartmic/letter-template-latex) | 4 | coded GH:049 |
| 50 | [kamisatoayakaaaa/Ahu-Letter-Template](https://github.com/kamisatoayakaaaa/Ahu-Letter-Template) | 4 | uncodeable/off-topic: preview is the university logo, not a letter (C2) |
| 51 | [YimianDai/NUAAletter](https://github.com/YimianDai/NUAAletter) | 4 | coded GH:051 |
| 52 | [YanMing-lxb/GUET_Cover_Letter_Template](https://github.com/YanMing-lxb/GUET_Cover_Letter_Template) | 4 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 53 | [yy/uva-sds-letter-template](https://github.com/yy/uva-sds-letter-template) | 4 | coded GH:053 |
| 54 | [xinhjBrant/SYSU-Recommendation-Letter-Template](https://github.com/xinhjBrant/SYSU-Recommendation-Letter-Template) | 4 | coded GH:054 |
| 55 | [Jaaaahan/SWJTU-Recommendation-Letter-Template](https://github.com/Jaaaahan/SWJTU-Recommendation-Letter-Template) | 4 | coded GH:055 |
| 56 | [Nova-chen151/Tongji-cover_letter-latex](https://github.com/Nova-chen151/Tongji-cover_letter-latex) | 4 | coded GH:056 |
| 57 | [iphysresearch/UCAS_ICTP_AP-cover_letter-template](https://github.com/iphysresearch/UCAS_ICTP_AP-cover_letter-template) | 4 | coded GH:057 |
| 58 | [da-luce/cv](https://github.com/da-luce/cv) | 4 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 59 | [nouaim/sirati](https://github.com/nouaim/sirati) | 4 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 60 | [mayank1014/Endorsify](https://github.com/mayank1014/Endorsify) | 4 | uncodeable/off-topic: off-topic: web app |
| 61 | [timerring/SDU-letter-template](https://github.com/timerring/SDU-letter-template) | 3 | coded GH:061 |
| 62 | [juliandwain/cover-letter-template](https://github.com/juliandwain/cover-letter-template) | 3 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 63 | [nikita-parkhomenko/email-letter-template](https://github.com/nikita-parkhomenko/email-letter-template) | 3 | uncodeable/off-topic: off-topic: e-mail boilerplate |
| 64 | [holmescao/Response-letter-template-latex-](https://github.com/holmescao/Response-letter-template-latex-) | 3 | coded GH:064 |
| 65 | [yingjinghuang/PKU-Cover-Letter-template](https://github.com/yingjinghuang/PKU-Cover-Letter-template) | 3 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 66 | [ivowang/UESTC-RecommendationLetter-Template](https://github.com/ivowang/UESTC-RecommendationLetter-Template) | 3 | coded GH:066 |
| 67 | [nucontreras/cover-letter-template-english-french-spanish](https://github.com/nucontreras/cover-letter-template-english-french-spanish) | 3 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 68 | [HFUTTUG/HFUT_Letter](https://github.com/HFUTTUG/HFUT_Letter) | 3 | uncodeable/off-topic: no preview (background asset only) |
| 69 | [markusos/cv](https://github.com/markusos/cv) | 3 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 70 | [MEschenbacher/latex-letter](https://github.com/MEschenbacher/latex-letter) | 3 | uncodeable/off-topic: no preview |
| 71 | [Himel-Sarder/Personalized-Letter-Generator](https://github.com/Himel-Sarder/Personalized-Letter-Generator) | 3 | uncodeable/off-topic: off-topic: Python generator |
| 72 | [zanoptics/SZTU-recommendation-template](https://github.com/zanoptics/SZTU-recommendation-template) | 3 | uncodeable/off-topic: preview is a source-code screenshot (C2) |
| 73 | [wilbowma/ubc-letter-template](https://github.com/wilbowma/ubc-letter-template) | 2 | uncodeable/off-topic: signature asset only |
| 74 | [ila/cover-letter-template](https://github.com/ila/cover-letter-template) | 2 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 75 | [WeAreMahsaAmini/LetterTemplates](https://github.com/WeAreMahsaAmini/LetterTemplates) | 2 | uncodeable/off-topic: no preview |
| 76 | [gkArvindr/Letter_Template](https://github.com/gkArvindr/Letter_Template) | 2 | uncodeable/off-topic: no preview |
| 77 | [iamcsr/cover-letter-template](https://github.com/iamcsr/cover-letter-template) | 2 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 78 | [chunkitlau/BUPTRecommendationLetterTemplate](https://github.com/chunkitlau/BUPTRecommendationLetterTemplate) | 2 | uncodeable/off-topic: no example letter |
| 79 | [lessiYin/HUST-Letter-Template](https://github.com/lessiYin/HUST-Letter-Template) | 2 | coded GH:079 |
| 80 | [punchelvis/open-letter-template](https://github.com/punchelvis/open-letter-template) | 2 | uncodeable/off-topic: no preview |
| 81 | [kidozh/nwpu_invitation_letter_template](https://github.com/kidozh/nwpu_invitation_letter_template) | 2 | coded GH:081 |
| 82 | [lahirsti/LaTeX_Templates_CoverLetter](https://github.com/lahirsti/LaTeX_Templates_CoverLetter) | 2 | uncodeable/off-topic: off-topic: cover-letter / CV repo (other family; cross-listed to cover-letter) |
| 83 | [Anna-Yanamii/UESTC-Recommendation-Letter-Template](https://github.com/Anna-Yanamii/UESTC-Recommendation-Letter-Template) | 2 | coded GH:083 |

Totals ranks 1-83: coded 40, uncodeable/off-topic 43.

## LT.3 Coded table (N = 40)
| id | repo | stars | columns | head | body | colour | header | rules | dens | letterhead | adm | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GH:002 | shellywhen/Journal-Response-Letter-Template-LaTeX | 358 | 1 | serif | serif | mono | plain-centered | none | airy | top-centered | y | journal reviewer-response TITLE page (paper title, journal, authors centred); response letter is on-topic by name only |
| GH:003 | Sematre/typst-letter-pro | 217 | 1 | sans | sans | mono | plain-left | none | standard | address-window | y | DIN 5008: sender block top right, bold sender name; align=right; small return-address line above recipient |
| GH:005 | eddelbuettel/linl | 117 | 1 | serif | serif | mono | plain-left | none | standard | top-right | y | LOW-CONFIDENCE: letter is ~300 px tall inside an Emacs screenshot (A3: mockup ignored); return address top right; align=right |
| GH:008 | pascal-huber/typst-letter-template | 48 | 1 | display | serif | mono | plain-left | none | standard | address-window | y | monospaced "Bananas Ltd." title in a right-hand block with a banana photo (excluded); coloured layout-guide boxes are editor artefacts (B1d); align=right |
| GH:009 | jgehrcke/latex-briefvorlage | 44 | 1 | serif | serif | mono | plain-left | none | standard | address-window | y | sender name bold top right, small italic lines; align=right; return-address line under sender |
| GH:010 | faicaiwawa/Response_Letter_Template | 41 | 1 | serif | serif | one-accent | plain-centered | boxes | standard | top-centered | y | journal response letter: centred bold title; grey bordered reply boxes; blue "Reply:" labels x2 (one cluster) |
| GH:014 | dvdvgt/typst-letter | 28 | 1 | serif | serif | one-accent | ruled | rules | standard | address-window | y | blue name + full-width blue rule directly under header block (gap 0.3 line); blue subject line; DIN return-address line |
| GH:016 | JohannaXie/Response-Letter-Template | 24 | 1 | serif | serif | mono | plain-left | boxes | standard | top-left | y | response-to-editor page: salutation first, grey bordered comment box; no letterhead |
| GH:017 | leungll/ByteDance-Letter-Template | 19 | 1 | serif | serif | mono | plain-left | none | standard | top-right | y | C32-recheck: faint logo watermark behind the body text; logo left (excluded), address block right; script signature [wm/page 1.04:1, text/wm 13.8:1] |
| GH:021 | cqylunlun/journal-response-letter-template | 13 | 1 | serif | serif | mono | plain-centered | none | standard | top-centered | y | page 1 of the mosaic preview: centred title "Response Letter" then salutation; page 2 red link boxes not coded |
| GH:023 | leungll/NENU-Letter-Template | 12 | 1 | serif | serif | mono | plain-left | none | standard | top-right | y | C32-recheck: university seal watermark behind the body text; logo left, address right [wm/page 1.21:1, text/wm 11.6:1] |
| GH:024 | HovChen/HDU-Letter-Template | 12 | 1 | sans | serif | mono | plain-left | none | standard | top-right | y | logo left, address block right, no rule; Chinese body; date left |
| GH:025 | alxvth/Revision-Rebuttal-Letter-Template | 12 | 1 | serif | serif | one-accent | plain-centered | boxes | standard | top-centered | y | centred title "Revision Letter"; grey quote bars (L 0.90 tint, fills under threshold); red link boxes x3 (one hue) |
| GH:027 | juliantao/qletter | 11 | 1 | sans | sans | one-accent | plain-left | none | standard | top-right | y | logo placeholder left, sender name/contact right; blue email links x2; align=right |
| GH:028 | cherise215/Journal-Response-Letter-Template | 11 | 1 | serif | serif | multi | plain-centered | boxes | standard | top-centered | y | centred title; dark-green filled box header + pale-green box; blue text/links (2 clusters) |
| GH:030 | JmlrOrg/jmlr-coverletter | 10 | 1 | serif | serif | one-accent | plain-left | none | airy | top-right | y | JMLR journal cover letter (cross-listed from cover-letter, C31): no letterhead, right-aligned date; red bold placeholder text (one cluster, many elements) |
| GH:032 | Tanglumy/NKU-Recommendation-Letter-Template | 10 | 1 | serif | serif | one-accent | plain-left | none | standard | top-left | y | C32-recheck: faint university-seal watermark behind body text; logo left, purple address block right with vertical rule [wm/page 1.11:1, text/wm 12.5:1] |
| GH:033 | xhghhh/UESTC-Recommendation-Letter-Template | 10 | 1 | serif | serif | one-accent | plain-left | none | standard | top-left | y | C32-recheck: crest watermark behind body text; blue address block right [wm/page 1.17:1, text/wm 16.6:1] |
| GH:034 | thatfloflo/typst-pc-letter | 9 | 1 | serif | serif | mono | plain-centered | none | standard | address-window | y | cream page tint is the background (B1a); centred red small-caps sender name (1 element only, fails B5); return-address line; signature in script |
| GH:036 | black-snake/LaTeX-letter | 9 | 1 | serif | serif | mono | ruled | rules | standard | address-window | y | large sender name top right with a full-width rule directly under it; footer rule and bank block; QR margin code |
| GH:039 | CFC87/Fudan-Recommendation-Letter-Template | 7 | 1 | serif | serif | one-accent | plain-left | none | standard | top-left | y | C32-recheck: seal watermark behind body text; blue letterhead block [wm/page 1.14:1, text/wm 12.6:1] |
| GH:040 | the-au-forml-lab/au_ccs_letterhead_template | 7 | 1 | serif | serif | mono | plain-centered | none | standard | top-centered | y | C32-recheck: diagonal "Draft" watermark behind body text (template option shown in the preview); centred logo excluded [wm/page 1.16:1, text/wm 17.6:1] |
| GH:043 | klingtnet/DIN-letter-template | 6 | 1 | serif | serif | multi | split | rules | standard | address-window | y | name small caps left, contact block right (vertical overlap); lilac rule ~56% of page (<80%) so not ruled; red "MAHNUNG" title + blue subject |
| GH:044 | bast/quarto-letter-template | 6 | 1 | sans | sans | one-accent | plain-left | none | standard | top-left | y | logo top-left (excluded); sender block at page foot; blue link + blue URL (2 elements); Markdown-set letter |
| GH:046 | xjasonlyu/HDU-letter-template | 5 | 1 | serif | serif | one-accent | plain-left | none | standard | top-left | y | C32-recheck: faint seal watermark behind body text; blue address block right [wm/page 1.08:1, text/wm 19.4:1] |
| GH:047 | cjdet/unl-letter-template | 4 | 1 | serif | serif | mono | plain-left | none | standard | top-centered | y | centred red logo (excluded) and footer logo; no sender-name title; plain-left by default |
| GH:048 | smartmic/letter-template-lout | 4 | 1 | sans | sans | mono | plain-left | none | standard | address-window | y | sender name top right; footer contact grid; diagonal README overlay text is an artefact (B1d), not coded; align=right |
| GH:049 | smartmic/letter-template-latex | 4 | 1 | serif | serif | mono | plain-left | rules | standard | address-window | y | sender name top right, footer rule; grey page tint = background; diagonal README overlay ignored; align=right |
| GH:051 | YimianDai/NUAAletter | 4 | 1 | sans | serif | one-accent | plain-left | none | standard | top-left | y | logo left + blue bold name/title/contact block right (vertical rule); blue text x5 elements |
| GH:053 | yy/uva-sds-letter-template | 4 | 1 | sans | sans | mono | plain-left | none | standard | top-left | y | logo top-left, address block right; orange URL = 1 element; footer page number |
| GH:054 | xinhjBrant/SYSU-Recommendation-Letter-Template | 4 | 1 | serif | serif | one-accent | plain-left | none | standard | top-left | y | C32-recheck: seal watermark behind body text; green letterhead text [wm/page 1.10:1, text/wm 12.5:1] |
| GH:055 | Jaaaahan/SWJTU-Recommendation-Letter-Template | 4 | 1 | serif | serif | one-accent | plain-left | none | standard | top-left | y | C32-recheck: faint seal watermark behind body text; blue letterhead [wm/page 1.10:1, text/wm 19.1:1] |
| GH:056 | Nova-chen151/Tongji-cover_letter-latex | 4 | 1 | serif | serif | mono | plain-left | rules | airy | top-left | y | Tongji journal cover letter (cross-listed, C31): logo top-left, right-aligned author block, single rule at foot; align=right |
| GH:057 | iphysresearch/UCAS_ICTP_AP-cover_letter-template | 4 | 1 | serif | serif | mono | plain-left | rules | airy | top-left | y | UCAS journal cover letter (cross-listed, C31): logo + rule then date, then right-aligned name block (date between rule and name, so not ruled); logo blue excluded |
| GH:061 | timerring/SDU-letter-template | 3 | 1 | serif | serif | one-accent | plain-left | none | dense | top-left | y | C32-recheck: mountain-seal watermark behind body text; preview is a 2-page landscape mockup [wm/page 1.15:1, text/wm 7.7:1] |
| GH:064 | holmescao/Response-letter-template-latex- | 3 | 1 | serif | serif | mono | plain-left | none | standard | top-left | y | response-letter first page: numbered list; red "首页" annotation is a README artefact (B1d); green bold words in the source not visible on preview |
| GH:066 | ivowang/UESTC-RecommendationLetter-Template | 3 | 1 | serif | serif | one-accent | plain-left | rules | standard | top-left | y | C32-recheck: crest watermark behind body text; logo left with vertical rule [wm/page 1.18:1, text/wm 13.8:1] |
| GH:079 | lessiYin/HUST-Letter-Template | 2 | 1 | serif | serif | mono | ruled | rules | airy | top-left | y | logo left + Date/Name/Phone/Email right; full-width rule (~81% of page) directly below the header block; footer rule and page number |
| GH:081 | kidozh/nwpu_invitation_letter_template | 2 | 1 | serif | serif | mono | ruled | rules | standard | top-left | y | logo + serif wordmark; rule under it is ~72% of page but ~100% of live width (a via live width); italic date right |
| GH:083 | Anna-Yanamii/UESTC-Recommendation-Letter-Template | 2 | 1 | serif | serif | mono | plain-left | none | airy | top-left | y | minimal one-line letter: logo top-left, name block left; no rule |

## LT.4 Exclusions log (item stays in N)
| id | rule | evidence |
|---|---|---|

Admissible 40 / 40, excluded 0. No exclusions remain after the C32 re-check: the 11 former A3 items in N are admissible (measured, LT.8) and GH:088 (the one measured exclusion, 1.48:1) left N after the C31 cross-listing (LT.9). GH:005 is low-confidence (mockup).

## LT.5 Frequency table k/40 (denominator includes inadmissible; [x] = inadmissible)
| archetype `columns\|heading\|colour\|header` | k | k/40 | admissible k | exemplars |
|---|---|---|---|---|
| `1\|serif\|mono\|plain-left` | 11 | 0.275 | 11 | GH:005, GH:009, GH:016, GH:017, GH:023, GH:047, GH:049, GH:056, GH:057, GH:064, GH:083 |
| `1\|serif\|one-accent\|plain-left` | 9 | 0.225 | 9 | GH:030, GH:032, GH:033, GH:039, GH:046, GH:054, GH:055, GH:061, GH:066 |
| `1\|sans\|mono\|plain-left` | 4 | 0.100 | 4 | GH:003, GH:024, GH:048, GH:053 |
| `1\|serif\|mono\|plain-centered` | 4 | 0.100 | 4 | GH:002, GH:021, GH:034, GH:040 |
| `1\|sans\|one-accent\|plain-left` | 3 | 0.075 | 3 | GH:027, GH:044, GH:051 |
| `1\|serif\|mono\|ruled` | 3 | 0.075 | 3 | GH:036, GH:079, GH:081 |
| `1\|serif\|one-accent\|plain-centered` | 2 | 0.050 | 2 | GH:010, GH:025 |
| `1\|display\|mono\|plain-left` | 1 | 0.025 | 1 | GH:008 |
| `1\|serif\|multi\|plain-centered` | 1 | 0.025 | 1 | GH:028 |
| `1\|serif\|multi\|split` | 1 | 0.025 | 1 | GH:043 |
| `1\|serif\|one-accent\|ruled` | 1 | 0.025 | 1 | GH:014 |

11 distinct archetypes; 40 admissible items in 11 admissible archetypes; archetypes with k>=2: 7; singleton admissible items 4/40. Coarsening trigger (>=15 admissible, >50% of admissible items singletons, <5 archetypes with k>=2): not triggered.
Variant modes over admissible items: letterhead [('top-left', 18), ('address-window', 9), ('top-centered', 7), ('top-right', 6)]; body [('serif', 35), ('sans', 5)]; rules/boxes [('none', 27), ('rules', 9), ('boxes', 4)]; density [('standard', 33), ('airy', 6), ('dense', 1)].
Distribution over all 40: header [('plain-left', 28), ('plain-centered', 7), ('ruled', 4), ('split', 1)]; colour [('mono', 23), ('one-accent', 15), ('multi', 2)]; letterhead [('top-left', 18), ('address-window', 9), ('top-centered', 7), ('top-right', 6)].

## LT.6 Second-coder ids and seed
Ids (40): GH:002 GH:003 GH:005 GH:008 GH:009 GH:010 GH:014 GH:016 GH:017 GH:021 GH:023 GH:024 GH:025 GH:027 GH:028 GH:030 GH:032 GH:033 GH:034 GH:036 GH:039 GH:040 GH:043 GH:044 GH:046 GH:047 GH:048 GH:049 GH:051 GH:053 GH:054 GH:055 GH:056 GH:057 GH:061 GH:064 GH:066 GH:079 GH:081 GH:083
Sample `random.Random("82:letter")` (single coded corpus here; other corpora of the family join under C10): GH:053 GH:083 GH:002 GH:016 GH:009 GH:025 GH:047 GH:028 GH:024 GH:027

## LT.7 Ambiguities met
1. (SUPERSEDED by C32 - see Re-check section) A3 was first applied to faint watermarks behind running text (12 items); a faint watermark is arguably decorative rather than a "texture fill". If the orchestrator rules faint (<10% contrast) watermarks admissible, all 12 come back and the archetype table changes: the `1|serif|one-accent|plain-left` and `1|serif|mono|plain-left` groups grow.
2. Header for institution letterheads: the title is the largest text of the sender block; logos and seals never count, so many Chinese templates code plain-left with no sender name (GH:047, 053, 083).
3. GH:008, GH:049, GH:048: coloured layout guides and diagonal README overlay text are treated as editor artefacts (B1d), not colour.
4. GH:005 and GH:101: mockup-size and near-blank previews respectively; kept in N under C2/C3 borderline, second coder should confirm.
5. GH:081 rule: 72% of page width but ~100% of the live width of the text block (82a-general A.2 step 3a uses live width via 82a-cv).
6. Cross-list: 30+ cover-letter/CV repos in the walk (see raw list) belong to the cover-letter corpus; Deedy/others already appear there.

## LT.8 Re-check under C32 (research/82a-clarifications-5.md, 2026-09-24)
Rule: a single faint watermark is admissible iff watermark-vs-page <= 1.3:1 AND body text over it >= 4.5:1 (lib/color.contrast_ratio); ignored for colour use; "DRAFT" stamps are editor artefacts. Measured on the item's own preview (letter body area: page = most common colour, watermark = most common non-page light colour, text = darkest pixel; PDF renders 80 dpi, PNGs at source size; estimates per C9).

| id | page | watermark | watermark/page | darkest text / watermark | wm pixel share | verdict |
|---|---|---|---|---|---|---|
| GH:017 | #ffffff | #f3fcfc | 1.04 | 13.8 | 1.9% | admissible |
| GH:023 | #ffffff | #e5eaf2 | 1.21 | 11.6 | 0.8% | admissible |
| GH:032 | #ffffff | #f7f2f6 | 1.11 | 12.5 | 2.4% | admissible |
| GH:033 | #ffffff | #e9eef6 | 1.17 | 16.6 | 6.3% | admissible |
| GH:039 | #ffffff | #f0f0f0 | 1.14 | 12.6 | 8.5% | admissible |
| GH:040 | #ffffff | #edeeef | 1.16 | 17.6 | 8.2% | admissible (also a DRAFT stamp = editor artefact) |
| GH:046 | #ffffff | #f2f6ff | 1.08 | 19.4 | 2.1% | admissible |
| GH:054 | #ffffff | #f1f5f0 | 1.10 | 12.5 | 4.6% | admissible |
| GH:055 | #ffffff | #eff5f8 | 1.10 | 19.1 | 4.8% | admissible |
| GH:061 | #ffffff | #f0efef | 1.15 | 7.7 | 3.1% | admissible (landscape 2-page mockup) |
| GH:066 | #ffffff | #e7edf5 | 1.18 | 13.8 | 12.1% | admissible |
| GH:088 | #ffffff | #ebcdcf | 1.48 | 9.6 | 1.6% | **stays excluded** (watermark/page 1.48 > 1.3) |

Effect: 11 of 12 items return to the admissible pool; GH:088 stays excluded by measurement but is dropped from N after the C31 cross-listing (see LT.9), so the final family has no A3 exclusions. Watermarks are ignored for colour use: none of the 11 items' colour codes used the watermark (colour came from letterhead text). Tables above are recomputed. Reviewer-response letters (GH:002, 010, 016, 021, 025, 028, 064) stay on-topic, disclosed (ambiguity list).

## LT.9 Cross-listed from cover-letter (C31 / 82b A4)
Journal / manuscript-submission cover letters, off-topic for cover-letter (C31), are on-topic here as letters. Those inside this walk (letter ranks 30, 56, 57) are coded above: **GH:030** JMLR (JmlrOrg/jmlr-coverletter), **GH:056** Tongji, **GH:057** UCAS. The rest are not coded: letter rank 11 (firefly-cpp) has only a logo image; rank 52 (GUET) and 65 (PKU logo asset) have no preview; WHU (rank 127) and AllenYolk PKU (rank 156) fall beyond the walk stop.
Because 3 cross-listed items entered at ranks 30-57, N=40 is now reached earlier: the previous tail items at ranks 88 (A3-excluded), 97 and 101 were dropped from N (walk stops at rank 83). The C32 re-check above still reports GH:088 as the measured exclusion (it is now outside N; kept in the log for audit).

