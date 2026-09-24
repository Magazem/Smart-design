# Memo corpus — Microsoft Create memos (L2, below the 10-item floor → corroborate only); LibreOffice memo (corroborate only); GOV.UK (no memo guidance found)

Coder: Design Researcher. Counts only (research/82 §1). Retrieved 2026-09-23. **Plain statement: there is no rankable memo evidence. This is a Shortfall family; nothing below enters a frequency table or a Rank Value.**

## M.1 Sources
- **MS(memos):** `https://create.microsoft.com/en-us/templates/memos` → `curl -sL` redirected (HTTP 200) to `https://word.cloud.microsoft/create/en/memo-templates/?source=create_flow` (same vendor catalogue, items are in the static payload → codeable under 82a C5). Page order, no metric. **10 cards; on-topic memos = 7** (pos 1-7). Off-topic: pos 8 "Modern celebration of life program", pos 9 "Thank you card", pos 10 "Hats off graduation card". 7 < 10 → per §2 "a catalogue with <10 on-topic items is not coded as a corpus; its items may only corroborate (listed, not counted)". The research/82 probe found 9 cards; the page now shows 10.
- **LO(memo):** `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&q=memo&ord=download_d` (HTTP 200) returned 5 items (ids 3881, 5049, 99351, 20655, fattura-artigiani-commercianti-e-piccole-imprese). Titles seen: 3881 "Business Document Templates", 20655 "E-learning Course Authoring Methodology", 99351 a meeting-invitation template; 5049 is the three-column leaflet; the invoice item is another family. **0 memos** (full-text `q=` noise). Corroboration count: 0.
- **L3 GOV.UK content guidance:** fetched `https://www.gov.uk/guidance/content-design/writing-for-gov-uk` (301 → `https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/tone-of-voice/`); WebFetch of the redirected page reports "no mention of memo found". No GOV.UK page prescribing a memo format was located → **no L3 memo source**. (One retry done, as §10 says "retry".)

## M.2 MS memos listed for corroboration (NOT counted, NOT ranked)
Descriptive notes only, from the 400-px thumbnails (one look each; no §4 admissibility applied because nothing is coded as a corpus).

| pos | Item | Notes (not a rank input) |
|---|---|---|
| 1 | Logo memo | logo box top-left; purple diagonal bands top-right and bottom; To/From/CC block stacked; sans heading |
| 2 | Memo (simple design) | large grey serif "MEMO"; pale-yellow full-page fill; To/From/CC/Date/Re in a label-left column; hairline rule |
| 3 | Angles and curves memo | serif "Memorandum"; logo box; orange/mauve square blocks top-right and bottom-left; stacked To/From/CC |
| 4 | Modern memo (simple design) | large orange lowercase display "memo"; cream fill; label-left To/From/CC/Date/Re; orange rules top/bottom |
| 5 | Prism memo | multicolour triangle strips top and bottom; date top-right; To/From/Subject/CC caps labels |
| 6 | Business memo (bold design) | red "Memo" over a heavy black rule; date top-left; label-left TO/FROM/CC/RE column; COMMENTS body; company footer with rule |
| 7 | Blue spheres memo | round logo art top-right; blue "Memo"; stacked To/From/CC; blue body text |

Observation only: all 7 put a To/From/(CC/Date/Subject|Re) block at the head; 3 of 7 use a label-left column, 4 of 7 stack the labels; 5 of 7 carry decorative header/footer art. With 7 items no share is quoted as evidence.

## M.3 Consequences for shipping
- No ranked memo design, no L3 design. The seeded doctype default keeps its place as the doctype default (evidence class convention, disclosed). Filling has nothing to fill from.
- Expected Shortfall (§10: "2-5, Shortfall") is not met even at its floor: **0 ranked, 0 juried/authority, ≥1 convention.** The floor of 5 non-convention designs cannot be reached from the public sources reachable on 2026-09-23.

## M.4 Bias statement
Only Microsoft's editorial selection (7 memo templates, Word-authored, decoration-heavy) was reachable. No juried award category exists for memos, GOV.UK has no memo format, LibreOffice returned no memo. Prevalence of curation, not usage; popularity is not quality (§13).

## M.5 Ambiguities met
1. Card count moved from 9 (research/82 probe) to 10; three cards are other families and were not counted.
2. 82a C5 applies: the redirect target is static and reachable, but holds only 7 on-topic items.
3. No second-coder list: nothing is coded (82 §7 has nothing to sample).


## M.6 Pooled L2 corpus under 82b A1 (Design Researcher 3, 2026-09-24): MS memos + Overleaf `tagged/memo`

**This section supersedes M.3's "no rankable memo evidence".** 82b A1 (adopted 2026-09-24) pools sub-10 catalogues into one L2 prevalence corpus once the union reaches ≥10 on-topic codeable items. 82a C27 lets such a pool sit beside other corpora. The GitHub Typst/LaTeX memos (82b §3 memo row 1) are **not** in this section. The GitHub worker adds them and deduplicates against this pool, so N below is the non-GitHub part only.

Coded from the start under **research/82a-general.md** (header treatment §A, colour use §B; D.6), with `header-note` and `colour-note` per item. Other features follow research/82 §4, and 82a C1-C27 apply. Ranking Metric string: `prevalence:pool(ms-create-memos+overleaf-memo):k/11` (the pool counts as one corpus in §6). Items file (C11): `memo-items-pool.csv`.

### M.6.1 Sources (retrieved 2026-09-23/24, `curl -s -L -A "smart-design-research"`)
- **MS**: `https://word.cloud.microsoft/create/en/memo-templates/`, the static target of `create.microsoft.com/en-us/templates/memos` (82a C5). HTTP 200, 10 cards, 10 distinct. On-topic memos are pos 1-7, the same 7 as M.2. Pos 8-10 (celebration-of-life program, two cards) are off-topic. `word/business-templates` repeats 4 of these memos (same .docx), so they are not re-counted. Skew: Microsoft editorial, Word-authored, decorative.
- **Overleaf**: `https://www.overleaf.com/gallery/tagged/memo` and `…/tagged/memo/page/2`. HTTP 200, **10 templates** (82b §1e estimated 11). Gallery order, no metric. On-topic test, pre-set before viewing: the template's own title or description names a **memo/memorandum**, and page 1 is that document.

| gallery pos | Overleaf template | decision |
|---|---|---|
| 1 | ETA-Motionsmall (motions to society meetings) | off: motion/proposition (organisational paper) |
| 2 | CAPSL Technical Memo Template | **on-topic → OLM:002** |
| 3 | ymca ("notice template"; tagged formal-letter + memo) | off: a letter (salutation, "Sincerely"), letter family |
| 4 | FUCI National Presidency Communication | off: no memo named (official communication) |
| 5 | FUCI AF Mandate | off: mandate form |
| 6 | FUCI Motion | off: motion |
| 7 | FUCI RAF Candidacy | off: candidacy letter |
| 8 | Sample Policy Memo for Cornell INFO 1200 | **on-topic → OLM:008** |
| 9 | SINTEF Project Memo | **on-topic → OLM:009** |
| 10 | SINTEF Memo | **on-topic → OLM:010** |

  Preview: the page-1 image published on each template page (`writelatex.s3.amazonaws.com/published_ver/<id>.jpeg`, a signed URL that is re-issued on every visit). Nothing was compiled. Skew: LaTeX users, academic/technical (a university lab, a course, a Norwegian research institute). OLM:009 and OLM:010 are two layouts of one class family (`sintefdoc`). They are different designs, not forks, so both are counted (disclosed).
- **Pool:** MS 7 + Overleaf 4 = **N = 11 ≥ 10**, 2 distinct sources, 0 cross-source duplicates. Native metrics: none exist on either source. LibreOffice `q=memo` still returns 0 memos (M.1), and Typst Universe memo (2) overlaps GitHub, so it is left to the GitHub worker.

### M.6.2 Coded table
MS: 400×519 webp thumbnails. Overleaf: 794-px page-1 images. Measurements use the temp scripts `measure.py` (82a-general B1a background on a 20×20 grid; B3 fill blocks by morphological opening with a square of side 5% of the short side = 21 px; B4 hue bins) and `hlines.py` (horizontal runs ≥50% of width, for ruled tests). Previews are kept in the system temp dir, never in the repo. Declared-hex checks for MSM:004 and MSM:007 read the .docx theme (82a C25).

| id | source (pos) | template | columns | head | body | colour | header | rules | dens | adm | header-note | colour-note | preview |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MSM:001 | MS memo-templates (1) | [Logo memo](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fc5871878-ab3d-4671-adf7-af65b58cf429%2FTFc5871878-ab3d-4671-adf7-af65b58cf4296ece7a1d_wac-b86ca461e44d.docx) | 1 | sans | sans | one-accent | plain-left | boxes | airy | y | title "Memo" left; the purple top-right bar is 48% of page width (<80%, not a line); bottom bar is at the page foot, not near the header block | bg #fefefe; blocks 8.19% (<10%); purple cluster (270-300°): top bar, bottom bar, title = 3 elements | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/c5871878-ab3d-4671-adf7-af65b58cf429/thumbnails/400/logo-memo-purple-modern-simple-0-1-8d0111887029.webp |
| MSM:002 | MS memo-templates (2) | [Memo (simple design)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F19515b70-926d-4891-b273-352b9380b022%2FTF19515b70-926d-4891-b273-352b9380b02266453782_wac-ee0822eb6af3.docx) | 1 | serif | sans | mono | ruled | rules | airy | y | title "MEMO" (serif, grey) above the panel; hairline y=241 spans 85% of page width, between the last header line (Re:) and the COMMENTS body, no text between | bg = the yellow panel #f0efcb (modal on the 20x20 grid, B1a), so the panel is background, not a fill; white page margins L>0.90 (B1e); text grey/black → 0 clusters | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/19515b70-926d-4891-b273-352b9380b022/thumbnails/400/memo-%2528simple-design%2529-red-modern-bold-0-1-fe65d809ea35.webp |
| MSM:003 | MS memo-templates (3) | [Angles and curves memo](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fa51be22f-3a4f-44f4-98e1-210cf11b05d2%2FTFa51be22f-3a4f-44f4-98e1-210cf11b05d2358aa362_wac-5673fdc9442f.docx) | 1 | serif | serif | fill-blocks | plain-left | boxes | airy | y | title "Memorandum" left; logo placeholder box excluded; no line ≥80% | bg #fefefd; blocks 11.03% (≥10%, BORDERLINE within 10% of threshold); mauve/orange/peach square clusters | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/a51be22f-3a4f-44f4-98e1-210cf11b05d2/thumbnails/400/angles-and-curves-memo-brown-modern-simple-0-1-c7bfdb3043ad.webp |
| MSM:004 | MS memo-templates (4) | [Modern memo (simple design)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Fe45d4108-33de-4f0d-9f44-6a65bc04a92a%2FTFe45d4108-33de-4f0d-9f44-6a65bc04a92a1936b019_wac-56d20b5fac76.docx) | 1 | sans | sans | one-accent | ruled | rules | airy | y | title "memo" left; orange rule y=243-246 spans 74% of page width = 100% of live width (x 53-351), between the Re line and Comments, no text between | bg #f9f2e0 (L 0.927); blocks 0%; one red-orange cluster (declared #BD3A00; hue bins 0-30°): title, labels, 2 rules | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/e45d4108-33de-4f0d-9f44-6a65bc04a92a/thumbnails/400/modern-memo-%2528simple-design%2529-green-modern-simple-0-1-1c5bcb9d0968.webp |
| MSM:005 | MS memo-templates (5) | [Prism memo](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2Ff0454c06-2989-44fd-b80a-524a55c3e9ee%2FTFf0454c06-2989-44fd-b80a-524a55c3e9ee35ba21c7_wac-931b7f437b74.docx) | 1 | sans | sans | fill-blocks | ruled | rules | airy | y | largest text in top 30% after excluding the "replace with LOGO" placeholder = "DATE" (right); multicolour triangle bar at the page edge spans 94% of width (y 11-60), directly above the header block, gap < 1 body line | bg #fefefe; blocks 12.93% (triangle bands top and bottom) | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/f0454c06-2989-44fd-b80a-524a55c3e9ee/thumbnails/400/prism-memo-modern-color-block-0-1-ac32f11d3001.webp |
| MSM:006 | MS memo-templates (6) | [Business memo (bold design)](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F114ed224-91a8-4b7e-bcf3-2248d12bffd7%2FTF114ed224-91a8-4b7e-bcf3-2248d12bffd727e5da3e_wac-c7c9025d9bdf.docx) | 1 | sans | sans | one-accent | plain-left | rules | airy | y | title "Memo" centre at 39% of width; black rule under it spans 66% of page / 74% of live width (<80% / <90%) → not ruled; title not flush to a margin → not split. Columns: the TO/FROM/CC/RE routing block sits in a narrow left column; under 82a C28 a routing block never makes a column → 1 (was 2-sidebar) | bg #fefefe; blocks 0%; one red cluster (0/330° bins): title, TO/FROM values, company name | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/114ed224-91a8-4b7e-bcf3-2248d12bffd7/thumbnails/400/business-memo-%2528bold-design%2529-red-modern-bold-0-1-6dabfb5624da.webp |
| MSM:007 | MS memo-templates (7) | [Blue spheres memo](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F7182945c-4bb3-4d8c-9666-c1c73ebc2271%2FTF7182945c-4bb3-4d8c-9666-c1c73ebc227118958c6c_wac-04bc9cda5882.docx) | 1 | sans | sans | one-accent | ruled | rules | airy | y | navy bar at page edge (y 11-24) spans 86% of width; gap to the title "Memo" ≈ 60 px = 3.5 body lines (pitch 17 px) ≤ 4 (12% under the threshold; recorded although outside the 10% note band); watercolour spheres + Contoso logo excluded (B1b) | bg #fdfefe; spheres illustration excluded (B1b); blocks 0% (bar 14 px < 20 px = element); one blue cluster (180-210°): bar, title, blue intro text | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/7182945c-4bb3-4d8c-9666-c1c73ebc2271/thumbnails/400/blue-spheres-memo-blue-modern-simple-0-1-10cc38ce3ea4.webp |
| OLM:002 | Overleaf tagged/memo (2) | [CAPSL Technical Memo Template](https://www.overleaf.com/latex/templates/capsl-technical-memo-template/hsdjggvnghyz) | 1 | serif | serif | mono | ruled | rules | airy | y | largest text in the top 30%: the org lines and "Title goes here" are the same size; either reading gives ruled: the black rule (74% of page, 100% of live width) sits directly below the org block and above the centred title (gap ≈ 2.5 body lines) | bg white; university crest excluded (B1b); black text only | https://writelatex.s3.amazonaws.com/published_ver/10101.jpeg (signed; open via the template page) |
| OLM:008 | Overleaf tagged/memo (8) | [Sample Policy Memo for Cornell INFO 1200](https://www.overleaf.com/latex/templates/sample-policy-memo-for-cornell-info-1200/kybzqhsxjgjk) | 1 | serif | serif | mono | ruled | rules | standard | y | all header lines are the same size, so title = first line (To:); full rule (76% of page, 100% of live width) directly below the Section line, above the first body paragraph | bg white; black text only | https://writelatex.s3.amazonaws.com/published_ver/9643.jpeg (signed; open via the template page) |
| OLM:009 | Overleaf tagged/memo (9) | [SINTEF Project Memo](https://www.overleaf.com/latex/templates/sintef-project-memo/ttnmmkyprcdf) | 1 | sans | sans | multi | plain-left | rules | airy | y | title "Project Memo" in the right column; rule under the last meta row spans 60% of page / 75% of live width → not ruled; no split. Columns: the left column holds only the sender address block → 1 under 82a C28 (was 2-sidebar) | bg white; the teal block framing the SINTEF logo is excluded (B1b, ≤2× logo box); clusters: teal (sender address, ≥6 lines) and red (2 placeholder hints "Set with \clientref{}", "Set with \approved{}") → multi | https://writelatex.s3.amazonaws.com/published_ver/51414.jpeg (signed; open via the template page) |
| OLM:010 | Overleaf tagged/memo (10) | [SINTEF Memo](https://www.overleaf.com/latex/templates/sintef-memo/yzjhpwzywbwm) | 1 | sans | sans | one-accent | plain-left | rules | airy | y | title "Memo" left; sender address top-right ends above the title (split (c) fails); the only ≥90%-live rule sits between the subtitle and the distribution table, inside the header block → not ruled | bg white; logo block excluded (B1b); zebra rows L 0.91-0.92 (B1e); one teal cluster (sender address lines) | https://writelatex.s3.amazonaws.com/published_ver/51419.jpeg (signed; open via the template page) |

### M.6.3 Exclusions log
None: 11 of 11 are admissible. Checks: A1 (≤2 families each); A2 none; A3 no text on a gradient, texture or photo; A4 none; A5 the MSM:003 square clusters and MSM:005 triangle bands are pattern blocks, not ≥3 identical discrete motifs (C20); A6 the lowest pairs are MSM:004 #BD3A00 on #F8F3E0 = **5.01:1** and MSM:007 blue intro text #0072C7 on white = **4.96:1** (declared hexes, `color.contrast_ratio`; both ≥4.5, within the C9 band, so they were sampled); A7 no Office default blue (MSM:007 accents #2C567A/#0072C7 are not A7 hexes); A8 not hit. Memo has no family fail constraint (§5).

### M.6.4 Frequency (k counts admissible exemplars, C21; N includes inadmissible items; this pool is one corpus)
Script output (`memo_codes.py`):

| archetype `columns\|heading\|colour\|header` | k | share = k/11 | exemplars | sources | modes: body ; rules ; density |
|---|---|---|---|---|---|
| `1\|sans\|one-accent\|plain-left` | 3 | 3/11 = 0.273 | MSM:001, MSM:006, OLM:010 | MSM+OLM | sans:3 ; rules:2/boxes:1 ; airy:3 |
| `1\|serif\|mono\|ruled` | 3 | 3/11 = 0.273 | MSM:002, OLM:002, OLM:008 | MSM+OLM | serif:2/sans:1 ; rules:3 ; airy:2/standard:1 |
| `1\|sans\|one-accent\|ruled` | 2 | 2/11 = 0.182 | MSM:004, MSM:007 | MSM | sans:2 ; rules:2 ; airy:2 |
| `1\|serif\|fill-blocks\|plain-left` | 1 | 1/11 = 0.091 | MSM:003 | MSM | serif:1 ; boxes:1 ; airy:1 |
| `1\|sans\|fill-blocks\|ruled` | 1 | 1/11 = 0.091 | MSM:005 | MSM | sans:1 ; rules:1 ; airy:1 |
| `1\|sans\|multi\|plain-left` | 1 | 1/11 = 0.091 | OLM:009 | OLM | sans:1 ; rules:1 ; airy:1 |

N=11 admissible=11 distinct=6 k>=2=3 singletons=3. Marginals: columns 1:11 (after C28); heading sans 7 / serif 4; body sans 8 / serif 3; colour one-accent 5 / mono 3 / fill-blocks 2 / multi 1; header ruled 6 / plain-left 5. §4 coarsening needs ≥15 admissible; there are 11 → **not triggered**. Three archetypes have K≥2 (two tie at 3/11), so memo now has ranked evidence (§6 step 1). The order is provisional until the GitHub memos are merged. Two archetypes are drawn from both sources (`1|serif|mono|ruled`: MS 1 + Overleaf 2; `1|sans|one-accent|plain-left`: MS 2 + Overleaf 1).

Columns (82a C28, ruled 2026-09-24): routing/address/metadata blocks never make a column. MSM:006 (TO/FROM/CC/RE block in a narrow left column) and OLM:009 (sender-address column) were first coded `2-sidebar`, and they are recoded to `1` with a note in the table. Before C28 the table read `1|sans|one-accent|plain-left` k=2, plus two 2-sidebar singletons.

Borderlines recorded for the second coder: MSM:003 blocks 11.03% (fill-blocks vs one-accent/multi); MSM:007 bar gap 3.5 body lines (ruled vs plain-left); MSM:001 blocks 8.19%.

### M.6.5 L3 authorities (presence; coded to an archetype from the authority's own specimen)
| id | Authority | Fetched | What it prescribes | Specimen coded | Archetype | Ranking Metric |
|---|---|---|---|---|---|---|
| MA:001 | **AR 25-50**, *Preparing and Managing Correspondence* (US Army, 10 Oct 2020) | `https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN42124-AR_25-50-007-WEB-13.pdf`: HTTP 200, application/pdf, 4,005,232 B; text via pdftotext; figure page rendered at 80 dpi with PyMuPDF into the temp dir | 1-18: 8½×11 paper; 1-16: computer-generated letterhead bearing the DoD seal, **black ink**, "do not print … decorative devices"; 1-19: "A font with a point size of 12 is recommended", no script faces; 2-3c: "1-inch from the left, right, and bottom edges. Do not justify right margins"; 2-4: block style flush left (heading, body, closing); office symbol at the left margin with the date flush right on the same line; "MEMORANDUM FOR" on the third line below; "SUBJECT:" in caps | **Figure 2-1** (PDF p. 20, "Using and preparing a memorandum with digital signature"). Embedded fonts ArialMT / Arial-BoldMT. Title = the centred letterhead "DEPARTMENT OF THE ARMY" (seal excluded, B1b) → plain-centered; black only → mono; one column; no rules in the memo body | `1\|sans\|mono\|plain-centered` (body sans; rules none; density standard) | `authority:AR 25-50 (2020) fig 2-1` |
| MA:002 | **Purdue OWL**, Memos: Format, Parts of a Memo, Sample Memo | `https://owl.purdue.edu/owl/subject_specific_writing/professional_technical_writing/memos/` + `format.html`, `parts_of_a_memo.html`, `sample_memo.html` (HTTP 200 each); linked sample `…/memos/documents/sample-business-memo-09192025.pdf` (HTTP 200, 87,629 B, 2 pp) | "single spaced and left justified … skip a line between" paragraphs; headings and lists; heading segment "TO: / FROM: / DATE: / SUBJECT:"; header ≈ 1/8 of the memo | The OWL **sample memo PDF, page 1** (fonts TimesNewRomanPSMT / -BoldMT). Title = first header line (all header lines the same size), flush left; no rule, band or colour | `1\|serif\|mono\|plain-left` (body serif; rules none; density standard) | `authority:Purdue OWL Memos (sample memo)` |

The two authority archetypes are **distinct from each other and from every pool archetype**, so neither merges (§6 step 2). Pool archetypes with K≥2 exist, so the ordinary L3 cap of 3 applies (82b A3's cap of 5 does not). SECNAV M-5216.5 and USAF *Tongue and Quill* (82b §1f) were not retried: they are outside this task's list.

### M.6.6 Bias statement (pool)
MS = Microsoft's editorial Word selection, decorative (5 of 7 carry header/footer art). Overleaf = LaTeX users, academic and institutional; 6 of the 10 tagged items are off-topic organisational papers. The pool is 64% MS by item count. There are no usage metrics, only curation. Authorities: one US military regulation and one US university writing guide, both English. Popularity is not quality (§13).

### M.6.7 Second coder (82a C10/C11; 82a-general D.6: ordinary §7 gate)
Ids (11): MSM:001-007, OLM:002, OLM:008, OLM:009, OLM:010, in `memo-items-pool.csv`. For Overleaf, the csv preview_url is the template page, because the image URL is signed and expires. The family-wide sample is drawn by the orchestrator after the GitHub memos are merged. The authorities (MA:001-002) are not sampled.
