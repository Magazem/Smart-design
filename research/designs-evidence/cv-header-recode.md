# cv header-treatment recode under research/82a-cv.md (r2)

Recoder: Design Researcher (fresh worker, not a round-1 coder). Retrieved/viewed 2026-09-23. Scope: `header treatment` ONLY for all 80 coded cv items (GH 40 + NPM 40). Original corpus files untouched; every other code (columns, heading, colour, admissibility) is copied from them. Previews re-fetched from the URLs listed in those files (GH:003/023/071/026 exact URLs resolved from the repos READMEs; GH:019 path percent-encoded). Contact sheets rendered to the system temp dir, never into the repo.

Tests: T1 image-hero (82a C1, unchanged) - T2 band - T3 ruled - T4 split - T5 plain-centered - T6 plain-left, strict priority, exactly as 82a-cv. "Sheet" = physical page 1; for web screenshots the document card/viewport, excluding browser chrome and canvas. Tall NPM scroll screenshots were cropped to A4 ratio for viewing; where 82a-cv itself gives a percentage of "sheet height" (NPM:001) its value is used.

## Result: 32 of 80 header codes changed (GH 18/40, NPM 14/40)

Header value counts (all 80): plain-centered r1 16, r2 16, r2a 16, plain-left r1 32, r2 35, r2a 35, split r1 21, r2 10, r2a 10, band r1 7, r2 2, r2a 2, ruled r1 3, r2 15, r2a 15, image-hero r1 1, r2 2, r2a 2

## Addendum A changes (82a-cv Addendum A: A1 summary not in header block; A2 section-heading rules never count; A3 document sheet only, sheets <300 px low-confidence)

4 of 80 header codes change vs r2 (r2 vs r1: 32): GH:055 ruled -> split, NPM:039 ruled -> plain-left, NPM:048 plain-left -> ruled, NPM:063 split -> ruled.

- NPM:048: A1 - summary is not part of the header block: grey rule 100% live width sits ~2.1 body lines under the title, before the summary (T3 a-d pass)
- NPM:063: A1 - gold rule 100% live width ~3.3 body lines under the title/contact block, before the summary; T3 passes (gap within 20% of the 4-line limit) so T3 precedes T4
- GH:055: A2 - the rule above Education is the same section-separator style repeated above Skills and Experience, so it belongs to the section headings and never counts; T4 passes (name flush left, contact block flush right)
- NPM:039: A2 - the rule above Personal Info is the overline pattern repeated above every section heading (Work Experience, ...), so it never counts; no T4, not centred
- GH:013: A1+A2 - decided now by the rule between the title row and the summary (A1); the overline above Experience is excluded (A2). Unchanged call
- NPM:080: unchanged (plain-left): its rule is BELOW the summary, so text lies between it and the header block (T3c fails); the rule above EXPERIENCE is a section overline (A2).
- Conflict flagged: the 82a-cv worked example NPM:044 and my NPM:054, NPM:069, NPM:073 have a rule BELOW the un-headed summary. Read literally, A1 (summary is not part of the header block) puts text between that rule and the header block (T3c fails), which would turn them to plain-left (NPM:044/054/069) and plain-centered (NPM:073). I KEPT them ruled because the binding worked example says ruled. Orchestrator to decide; r2a keeps ruled.
- A3: no other call changes (canvas outside the sheet was already ignored: NPM:007, GH:035, GH:054). Low-confidence (sheet <300 px, my estimate): GH:026, GH:051, GH:054, GH:055; GH:010 borderline.

## Per-item table

| id | item | header (r1) | header (r2) | header (r2a) | test that decided | note |
|---|---|---|---|---|---|---|
| GH:001 | posquit0/Awesome-CV | plain-centered | plain-centered | plain-centered | T5 | name centre on page centre; underline on Summary is a section-heading rule |
| GH:003 | billryan/resume | plain-centered | plain-centered | plain-centered | T5 | centred name; rules only under section headings |
| GH:006 | deedy/Deedy-Resume | plain-left | ruled (chg vs r1) | ruled | T3 | grey rule spans 100% page width between contact line and EDUCATION; gap ~1 body line; no text between (name centre ~50%, would be plain-centered) |
| GH:007 | jankapunkt/latexcv | plain-centered | plain-centered | plain-centered | T5 | name centred; meta block below name, no rule |
| GH:008 | jakegut/resume | plain-centered | plain-centered | plain-centered | T5 | centred name; heading rules only |
| GH:009 | dnl-blkv/mcdowell-cv | split | plain-centered (chg vs r1) | plain-centered | T5 | T4a fails: name is centred between address (left) and contact (right); T5 passes |
| GH:010 | sproogen/modern-resume-theme | split | split | split | T4 | name flush left, Email/Web text block flush right, vertical overlap; dotted line is under "About Me" (section rule) |
| GH:013 | jglovier/resume-template | plain-centered | ruled (chg vs r1) | ruled | A1+A2 / T3 | decided now by the rule between the title row and the summary (A1); the overline above Experience is excluded (A2). Unchanged call |
| GH:019 | mmmlllnnn/ResumeCollection | band | plain-left (chg vs r1) | plain-left | T6 | T2c fails: rounded band max width 0.599 of page (951/1587 px) < 0.60 - BORDERLINE (within 10%); height ok, ends at 10% of page |
| GH:021 | darwiin/yaac-another-awesome-cv | split | plain-left (chg vs r1) | plain-left | T6 | T4 fails: no meta TEXT block opposite the name (avatar image on right never creates split); name centre far from page centre |
| GH:023 | fky2015/resume-ng | plain-left | plain-centered (chg vs r1) | plain-centered | T5 | name and contact line centred in the rendered PDF (promo mockup around it ignored) |
| GH:024 | liweitianux/resume | plain-left | plain-left | plain-left | T6 | name flush left, contact rows below it; no opposite meta text; no rule |
| GH:025 | yunanwg/brilliant-CV | split | plain-left (chg vs r1) | plain-left | T6 | T4 fails: avatar is an image, contacts sit under the name; underline is on Education heading |
| GH:026 | xriley/Orbit-Theme | plain-left | plain-left | plain-left | T6 | promo shows real template: name is inside a full-height coloured sidebar (band d fails); no split, not centred LOW-CONF (sheet <300 px) |
| GH:027 | subidit/rover-resume | split | split | split | T4 | name flush left, contact text block flush right, vertical overlap |
| GH:035 | ptsouchlos/modern-cv | split | plain-left (chg vs r1) | plain-left | T6 | name centre -9.3% of sheet width from sheet centre (logo image on right shifts the block) >5% so not plain-centered; logo image never creates split |
| GH:036 | mnjul/html-resume | plain-left | plain-left | plain-left | T6 | name left; contact info is a grey full-height sidebar starting ~1.5 name-heights below the baseline (fails T4c) |
| GH:037 | changh95/latex_resume_template_kor | plain-left | split (chg vs r1) | split | T4 | name flush left, Github/Email/Mobile block flush right, vertical overlap |
| GH:038 | zachscrivena/simple-resume-cv | plain-centered | plain-centered | plain-centered | T5 | centred name; no rule |
| GH:039 | murraco/jekyll-theme-minimal-resume | band | plain-centered (chg vs r1) | plain-centered | T5 | band fails (d): dark hero fill runs the whole visible page height; name centred |
| GH:040 | geekplux/cv_resume | split | split | split | T4 | name flush left, contact/date text block flush right (photo far right), vertical overlap |
| GH:041 | byoungd/Resume-template-for-Coder | plain-left | plain-left | plain-left | T6 | large left "About" heading; no meta/rule |
| GH:042 | jskherman/imprecv | plain-centered | plain-centered | plain-centered | T5 | centred name block |
| GH:047 | thehale/expressive-resume | split | split | split | T4 | name flush left, contact block flush right, vertical overlap; rule under Work Experience is a section underline |
| GH:051 | Zilize/DrawCV | split | plain-left (chg vs r1) | plain-left | T6 | sample sheet inside promo banner: name left, contacts under it, avatar image right; rule under the section heading is an underline LOW-CONF (sheet <300 px) |
| GH:054 | eddiewebb/hugo-resume | band | plain-left (chg vs r1) | plain-left | T6 | name sits on white main area beside a full-height terracotta sidebar; no fill behind glyphs; name centre ~35% of width LOW-CONF (sheet <300 px) |
| GH:055 | crispgm/resume | split | ruled (chg vs r1) | split **(A-change)** | A2 / T3 | the rule above Education is the same section-separator style repeated above Skills and Experience, so it belongs to the section headings and never counts; T4 passes (name flush left, contact block flush right) LOW-CONF (sheet <300 px) |
| GH:057 | dcetin/Simple-CV | split | split | split | T4 | name flush left, Website/Email/GitHub block flush right; rules are under section headings |
| GH:059 | MLNLP-World/Academic-Resume-Template | split | plain-left (chg vs r1) | plain-left | T6 | T4 fails: contacts are left under the name, photo is an image; rules are under section headings |
| GH:061 | mliu7/latex-moderncv | split | split | split | T4 | name flush left, contact text block flush right, vertical overlap; short blue rule is beside the Education heading |
| GH:062 | cowboysmall-tools/hugo-devresume-theme | split | split | split | T4 | name flush left, contact text block flush right, vertical overlap (card) |
| GH:064 | Tombarr/html-resume-template | plain-left | plain-left | plain-left | T6 | T3a fails: rule is 57% of page and 73% of live width (<80% / <90%); name not flush to margin (sidebar) |
| GH:065 | stuxf/basic-typst-resume-template | plain-left | plain-left | plain-left | T6 | name left, contacts under it; rules are under section headings |
| GH:066 | lanxx314/resume | split | split | split | T4 | name flush left, Email/Mobile block flush right, vertical overlap |
| GH:068 | rohitg00/one_pager_resume_template | split | plain-left (chg vs r1) | plain-left | T6 | T4 fails: contacts under name, photo is an image; rules under section headings |
| GH:071 | afnizarnur/draco | plain-left | plain-centered (chg vs r1) | plain-centered | T5 | largest heading = DRACO watermark centred on sheet (BORDERLINE: read as the small left "I live in far northern sky" it would be plain-left) |
| GH:072 | Stavrospanakakis/jekyll-cv | plain-left | plain-left | plain-left | T6 | name in left column; moon icon is an image; lines beside section headings |
| GH:073 | daehopark/resume-for-web-developer | split | plain-left (chg vs r1) | plain-left | T6 | name "Resume" sits right of centre but 12% short of the right text edge (T4a fails); rule passes through the header (T3b fails) |
| GH:076 | NorthSecond/Auto_Typst_Resume_Template | plain-centered | plain-centered | plain-centered | T5 | centred name; heading rules only |
| GH:077 | maksymilan/zju-resume-template | split | plain-centered (chg vs r1) | plain-centered | T5 | 82a worked example: logos never create split; blue rule is under the section heading |
| NPM:001 | jsonresume-theme-even | plain-centered | band (chg vs r1) | band | T2 | 82a worked example: #F3F4F5 tint behind photo/name, full width, ends ~7% of sheet height |
| NPM:002 | jsonresume-theme-elegant | plain-left | plain-left | plain-left | T6 | name centred inside left sidebar column only; no fill behind glyphs different from page |
| NPM:003 | jsonresume-theme-engineering | plain-centered | plain-centered | plain-centered | T5 | centred name; heading rules only |
| NPM:004 | jsonresume-theme-stackoverflow | split | plain-left (chg vs r1) | plain-left | T6 | T4 fails: contacts sit under the name (left), photo is an image |
| NPM:005 | jsonresume-theme-flat | plain-left | band (chg vs r1) | band | T2 | full-width light-grey tint behind name+title, dL~0.045, ends ~17% of page height |
| NPM:007 | jsonresume-theme-kendall | band | ruled (chg vs r1) | ruled | T3 | sheet = white card; dark navy is canvas outside the sheet. Grey rule spans 100% of card under name/title, gap ~1.5 lines, no text between |
| NPM:009 | jsonresume-theme-macchiato | band | ruled (chg vs r1) | ruled | T3 | thin green stripe at card top, 100% width, gap to name ~2 body lines, name not on it (cf. 82a caffeine example) |
| NPM:014 | jsonresume-theme-engineering-leader | plain-centered | plain-centered | plain-centered | T5 | centred name; rule under Experience heading is a section underline |
| NPM:015 | jsonresume-theme-eloquent | plain-left | plain-left | plain-left | T6 | name centred inside left column only; full-height sidebar |
| NPM:021 | jsonresume-theme-lucide | plain-left | plain-left | plain-left | T6 | T3a fails: rule spans main column only (66% of live width); name flush left of main column |
| NPM:024 | jsonresume-theme-paper-plus-plus | plain-centered | plain-centered | plain-centered | T5 | centred name in card |
| NPM:027 | jsonresume-theme-professional | plain-centered | plain-centered | plain-centered | T5 | centred name; heading rules only |
| NPM:028 | jsonresume-theme-minyma | plain-left | plain-left | plain-left | T6 | name centre +6.1% of sheet width from centre (photo left of name) >5%; contacts are below, not beside (T4c fails) |
| NPM:033 | jsonresume-theme-pumpkin | plain-left | plain-left | plain-left | T6 | name at left of main column beside label rail |
| NPM:036 | jsonresume-theme-jacrys | plain-left | plain-left | plain-left | T6 | name left under photo; no rule/meta opposite |
| NPM:038 | jsonresume-theme-claude | ruled | ruled | ruled | T3 | gradient bar across top of card (>=90% live width), gap to name ~1.5 lines |
| NPM:039 | jsonresume-theme-relaxed | plain-left | ruled (chg vs r1) | plain-left **(A-change)** | A2 / T3 | the rule above Personal Info is the overline pattern repeated above every section heading (Work Experience, ...), so it never counts; no T4, not centred |
| NPM:040 | jsonresume-theme-architects-portfolio | plain-left | plain-left | plain-left | T6 | name left; no rule |
| NPM:042 | jsonresume-theme-orbit | plain-left | plain-left | plain-left | T6 | name inside full-height teal sidebar on the right (band d fails); not centred |
| NPM:044 | jsonresume-theme-data-driven | ruled | ruled | ruled | T3 | 82a: heavy blue line below un-headed summary, ~100% live width |
| NPM:045 | jsonresume-theme-rickosborne | plain-left | plain-left | plain-left | T6 | name left; contact list is on the right but starts >=3 name-heights below the name (T4c fails) |
| NPM:048 | jsonresume-theme-developer-mono | plain-left | plain-left | ruled **(A-change)** | A1 / T6 | summary is not part of the header block: grey rule 100% live width sits ~2.1 body lines under the title, before the summary (T3 a-d pass) |
| NPM:049 | jsonresume-theme-caffeine | band | ruled (chg vs r1) | ruled | T3 | 82a worked example: full-width teal stripe at top edge, name not on it, gap ~2.8 lines |
| NPM:054 | jsonresume-theme-sales-hunter | plain-centered | ruled (chg vs r1) | ruled | T3 | green rule 100% of live width under the summary, gap ~1.2 lines |
| NPM:057 | jsonresume-theme-simple-red | plain-left | plain-left | plain-left | T6 | name left; wavy divider is far below the header block |
| NPM:058 | jsonresume-theme-colophon | plain-left | plain-left | plain-left | T6 | name left; page tint is the background (full page), not a band |
| NPM:060 | jsonresume-theme-brutalist | plain-left | ruled (chg vs r1) | ruled | T3 | heavy black rule (100% of boxed sheet width) directly under the top meta bar above the name; gap ~1 line, no text between |
| NPM:061 | jsonresume-theme-executive-slate | plain-left | plain-left | plain-left | T6 | 82a worked example: sidebar (full height) so not band; rule <90% live width so not ruled |
| NPM:063 | jsonresume-theme-academic | split | split | ruled **(A-change)** | A1 / T4 | gold rule 100% live width ~3.3 body lines under the title/contact block, before the summary; T3 passes (gap within 20% of the 4-line limit) so T3 precedes T4 |
| NPM:066 | jsonresume-theme-rocketspacer | plain-left | plain-left | plain-left | T6 | photo left, name left-aligned beside it; no opposite meta |
| NPM:067 | jsonresume-theme-kards | image-hero | image-hero | image-hero | T1 | full-bleed dark hero image with title (unchanged from r1; kept image-hero) |
| NPM:068 | jsonresume-theme-cjean | band | image-hero (chg vs r1) | image-hero | T1 | low-poly image band spans 100% width x 44% of page height (own area >=30%, intersects top 20%); card occludes part of it (visible ~18%) - BORDERLINE |
| NPM:069 | jsonresume-theme-modern-classic | plain-left | ruled (chg vs r1) | ruled | T3 | grey rule spans 100% live width directly under the summary, gap ~1.4 lines |
| NPM:071 | jsonresume-theme-elite | plain-left | plain-left | plain-left | T6 | name inside full-height dark sidebar (band d fails) |
| NPM:072 | jsonresume-theme-react | plain-left | plain-left | plain-left | T6 | name left, contacts beneath; rule is beside the ABOUT heading |
| NPM:073 | jsonresume-theme-academic-cv-lite | plain-centered | ruled (chg vs r1) | ruled | T3 | grey rule 100% live width under the summary, gap ~0.7 line, before EDUCATION (name centred but T3 precedes T5) |
| NPM:075 | jsonresume-theme-modern-plain | split | ruled (chg vs r1) | ruled | T3 | blue rule 100% live width under name/title/contact block (also would be split); gap ~1 line |
| NPM:079 | jsonresume-theme-papirus | plain-centered | plain-left (chg vs r1) | plain-left | T6 | name centred in main column, 16% right of sheet centre (T5 fails); dark sidebar full height |
| NPM:080 | jsonresume-theme-berlin-grid | plain-left | plain-left | plain-left | T6 | T3d fails: black rule is ~5.2 body lines below the summary (>4); no split |
| NPM:083 | jsonresume-theme-clinical-precision | ruled | ruled | ruled | T3 | thick green bar above name across card (100%), gap ~1.5 lines |

## Borderline / measured decisions (82a-cv: record any test within 10% of its threshold)

- GH:019 band width 0.599 vs 0.60 threshold (951/1587 px, widest row of the rounded band) - fails; band would be the answer at 0.60. Second coder should measure it.
- GH:035 name centre offset -9.3% (threshold 5%); NPM:028 +6.1%; NPM:079 +16%; GH:073 right-edge gap 12% of live width (T4a threshold 5%).
- NPM:080 rule gap ~5.2 body lines (threshold 4); GH:013 gap ~1.9; GH:006 ~1.
- NPM:068 image own area 44% of page (threshold 30%) but only ~18% visible around the card; kept image-hero under the literal "own area".
- GH:071 largest-heading choice (DRACO watermark vs the small left text).
- GH:039 / NPM:067: a dark starfield hero fills the visible page; GH:039 read as fill (band d fails -> plain-centered), NPM:067 as image (kept image-hero from r1). Not the same call on visually similar heroes - flag for the second coder.
- Mockup/promo previews (GH:010, 023, 026, 035, 051, 055, 071; NPM:068): the document sheet inside the mockup was coded. GH:026/051 sheets are tiny (approx 150-250 px).

## Frequency tables (r2a headers = r2 plus Addendum A; denominators include inadmissible items; [x] = inadmissible)

### GH L1 (share:GH:k/40 by stars) - 19 archetypes

| archetype | k | k/40 | admissible k | exemplars |
|---|---|---|---|---|
| `1\|serif\|mono\|plain-centered` | 8 | 0.200 | 8 | GH:003, GH:008, GH:009, GH:023, GH:038, GH:042, GH:071, GH:076 |
| `1\|sans\|one-accent\|plain-left` | 5 | 0.125 | 5 | GH:021, GH:024, GH:025, GH:035, GH:059 |
| `1\|sans\|mono\|split` | 4 | 0.100 | 4 | GH:010, GH:047, GH:055, GH:066 |
| `2-sidebar\|sans\|mono\|plain-left` | 3 | 0.075 | 0 | GH:051[x], GH:064[x], GH:073[x] |
| `1\|sans\|one-accent\|plain-centered` | 2 | 0.050 | 2 | GH:001, GH:077 |
| `1\|sans\|one-accent\|split` | 2 | 0.050 | 2 | GH:040, GH:061 |
| `1\|serif\|mono\|split` | 2 | 0.050 | 2 | GH:027, GH:057 |
| `1\|serif\|one-accent\|plain-left` | 2 | 0.050 | 2 | GH:041, GH:065 |
| `2-sidebar\|sans\|fill-blocks\|plain-left` | 2 | 0.050 | 0 | GH:026[x], GH:054[x] |
| `1\|sans\|fill-blocks\|plain-centered` | 1 | 0.025 | 1 | GH:039 |
| `1\|sans\|fill-blocks\|plain-left` | 1 | 0.025 | 1 | GH:019 |
| `1\|sans\|mono\|plain-left` | 1 | 0.025 | 1 | GH:036 |
| `1\|sans\|mono\|ruled` | 1 | 0.025 | 1 | GH:013 |
| `1\|serif\|mono\|plain-left` | 1 | 0.025 | 1 | GH:068 |
| `1\|serif\|one-accent\|plain-centered` | 1 | 0.025 | 1 | GH:007 |
| `2-sidebar\|sans\|fill-blocks\|split` | 1 | 0.025 | 0 | GH:037[x] |
| `2-sidebar\|sans\|mono\|ruled` | 1 | 0.025 | 0 | GH:006[x] |
| `2-sidebar\|sans\|one-accent\|plain-left` | 1 | 0.025 | 0 | GH:072[x] |
| `2-sidebar\|sans\|one-accent\|split` | 1 | 0.025 | 0 | GH:062[x] |

### NPM L1 (share:NPM:k/40 by downloads.monthly) - 22 archetypes

| archetype | k | k/40 | admissible k | exemplars |
|---|---|---|---|---|
| `1\|sans\|one-accent\|ruled` | 6 | 0.150 | 4 | NPM:038[x], NPM:044, NPM:054[x], NPM:069, NPM:075, NPM:083 |
| `1\|sans\|mono\|plain-left` | 3 | 0.075 | 3 | NPM:028, NPM:040, NPM:080 |
| `1\|sans\|one-accent\|plain-left` | 3 | 0.075 | 3 | NPM:033, NPM:057, NPM:066 |
| `2-sidebar\|sans\|fill-blocks\|plain-left` | 3 | 0.075 | 0 | NPM:021[x], NPM:042[x], NPM:079[x] |
| `2-sidebar\|sans\|one-accent\|plain-left` | 3 | 0.075 | 0 | NPM:002[x], NPM:015[x], NPM:072[x] |
| `1\|sans\|multi\|plain-left` | 2 | 0.050 | 2 | NPM:004, NPM:039 |
| `1\|sans\|one-accent\|image-hero` | 2 | 0.050 | 2 | NPM:067, NPM:068 |
| `1\|serif\|mono\|plain-centered` | 2 | 0.050 | 2 | NPM:003, NPM:027 |
| `1\|serif\|one-accent\|ruled` | 2 | 0.050 | 2 | NPM:063, NPM:073 |
| `2-sidebar\|sans\|one-accent\|ruled` | 2 | 0.050 | 0 | NPM:007[x], NPM:049[x] |
| `1\|display\|multi\|ruled` | 1 | 0.025 | 0 | NPM:060[x] |
| `1\|mono\|one-accent\|ruled` | 1 | 0.025 | 1 | NPM:048 |
| `1\|sans\|fill-blocks\|plain-left` | 1 | 0.025 | 1 | NPM:036 |
| `1\|sans\|mono\|plain-centered` | 1 | 0.025 | 1 | NPM:014 |
| `1\|sans\|multi\|band` | 1 | 0.025 | 1 | NPM:005 |
| `1\|sans\|one-accent\|band` | 1 | 0.025 | 1 | NPM:001 |
| `1\|serif\|one-accent\|plain-centered` | 1 | 0.025 | 1 | NPM:024 |
| `1\|serif\|one-accent\|plain-left` | 1 | 0.025 | 1 | NPM:058 |
| `2-sidebar\|display\|one-accent\|ruled` | 1 | 0.025 | 0 | NPM:009[x] |
| `2-sidebar\|serif\|fill-blocks\|plain-left` | 1 | 0.025 | 0 | NPM:061[x] |
| `2-sidebar\|serif\|one-accent\|plain-left` | 1 | 0.025 | 0 | NPM:045[x] |
| `3+\|sans\|fill-blocks\|plain-left` | 1 | 0.025 | 0 | NPM:071[x] |

MS(resumes) was unreachable in the original task (see cv-corpus-npm-ms.md), so the combined share below is the unweighted mean over the TWO coded corpora only (82 section 6 says over all coded corpora).

### Combined (r2a)

| archetype | k GH | k NPM | share GH | share NPM | combined (mean) | K | admissible K |
|---|---|---|---|---|---|---|---|
| `1\|serif\|mono\|plain-centered` | 8 | 2 | 0.200 | 0.050 | 0.1250 | 10 | 10 |
| `1\|sans\|one-accent\|plain-left` | 5 | 3 | 0.125 | 0.075 | 0.1000 | 8 | 8 |
| `1\|sans\|one-accent\|ruled` | 0 | 6 | 0.000 | 0.150 | 0.0750 | 6 | 4 |
| `2-sidebar\|sans\|fill-blocks\|plain-left` | 2 | 3 | 0.050 | 0.075 | 0.0625 | 5 | 0 |
| `1\|sans\|mono\|plain-left` | 1 | 3 | 0.025 | 0.075 | 0.0500 | 4 | 4 |
| `1\|sans\|mono\|split` | 4 | 0 | 0.100 | 0.000 | 0.0500 | 4 | 4 |
| `2-sidebar\|sans\|one-accent\|plain-left` | 1 | 3 | 0.025 | 0.075 | 0.0500 | 4 | 0 |
| `1\|serif\|one-accent\|plain-left` | 2 | 1 | 0.050 | 0.025 | 0.0375 | 3 | 3 |
| `2-sidebar\|sans\|mono\|plain-left` | 3 | 0 | 0.075 | 0.000 | 0.0375 | 3 | 0 |
| `1\|sans\|fill-blocks\|plain-left` | 1 | 1 | 0.025 | 0.025 | 0.0250 | 2 | 2 |
| `1\|sans\|multi\|plain-left` | 0 | 2 | 0.000 | 0.050 | 0.0250 | 2 | 2 |
| `1\|sans\|one-accent\|image-hero` | 0 | 2 | 0.000 | 0.050 | 0.0250 | 2 | 2 |
| `1\|sans\|one-accent\|plain-centered` | 2 | 0 | 0.050 | 0.000 | 0.0250 | 2 | 2 |
| `1\|sans\|one-accent\|split` | 2 | 0 | 0.050 | 0.000 | 0.0250 | 2 | 2 |
| `1\|serif\|mono\|split` | 2 | 0 | 0.050 | 0.000 | 0.0250 | 2 | 2 |
| `1\|serif\|one-accent\|plain-centered` | 1 | 1 | 0.025 | 0.025 | 0.0250 | 2 | 2 |
| `1\|serif\|one-accent\|ruled` | 0 | 2 | 0.000 | 0.050 | 0.0250 | 2 | 2 |
| `2-sidebar\|sans\|one-accent\|ruled` | 0 | 2 | 0.000 | 0.050 | 0.0250 | 2 | 0 |
| `1\|display\|multi\|ruled` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 0 |
| `1\|mono\|one-accent\|ruled` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 1 |
| `1\|sans\|fill-blocks\|plain-centered` | 1 | 0 | 0.025 | 0.000 | 0.0125 | 1 | 1 |
| `1\|sans\|mono\|plain-centered` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 1 |
| `1\|sans\|mono\|ruled` | 1 | 0 | 0.025 | 0.000 | 0.0125 | 1 | 1 |
| `1\|sans\|multi\|band` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 1 |
| `1\|sans\|one-accent\|band` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 1 |
| `1\|serif\|mono\|plain-left` | 1 | 0 | 0.025 | 0.000 | 0.0125 | 1 | 1 |
| `2-sidebar\|display\|one-accent\|ruled` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 0 |
| `2-sidebar\|sans\|fill-blocks\|split` | 1 | 0 | 0.025 | 0.000 | 0.0125 | 1 | 0 |
| `2-sidebar\|sans\|mono\|ruled` | 1 | 0 | 0.025 | 0.000 | 0.0125 | 1 | 0 |
| `2-sidebar\|sans\|one-accent\|split` | 1 | 0 | 0.025 | 0.000 | 0.0125 | 1 | 0 |
| `2-sidebar\|serif\|fill-blocks\|plain-left` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 0 |
| `2-sidebar\|serif\|one-accent\|plain-left` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 0 |
| `3+\|sans\|fill-blocks\|plain-left` | 0 | 1 | 0.000 | 0.025 | 0.0125 | 1 | 0 |

Distinct archetypes r2: 33 (r1: 33). Archetypes with all exemplars inadmissible (C1/C3/C5/C6/A7/A8) cannot ship; admissible-only ranking order by combined share, K>=2 and >=1 admissible exemplar:

- `1|serif|mono|plain-centered`  combined 0.1250  K=10 (GH 8, NPM 2)  admissible exemplars 10
- `1|sans|one-accent|plain-left`  combined 0.1000  K=8 (GH 5, NPM 3)  admissible exemplars 8
- `1|sans|one-accent|ruled`  combined 0.0750  K=6 (GH 0, NPM 6)  admissible exemplars 4
- `1|sans|mono|plain-left`  combined 0.0500  K=4 (GH 1, NPM 3)  admissible exemplars 4
- `1|sans|mono|split`  combined 0.0500  K=4 (GH 4, NPM 0)  admissible exemplars 4
- `1|serif|one-accent|plain-left`  combined 0.0375  K=3 (GH 2, NPM 1)  admissible exemplars 3
- `1|sans|fill-blocks|plain-left`  combined 0.0250  K=2 (GH 1, NPM 1)  admissible exemplars 2
- `1|sans|multi|plain-left`  combined 0.0250  K=2 (GH 0, NPM 2)  admissible exemplars 2
- `1|sans|one-accent|image-hero`  combined 0.0250  K=2 (GH 0, NPM 2)  admissible exemplars 2
- `1|sans|one-accent|plain-centered`  combined 0.0250  K=2 (GH 2, NPM 0)  admissible exemplars 2
- `1|sans|one-accent|split`  combined 0.0250  K=2 (GH 2, NPM 0)  admissible exemplars 2
- `1|serif|mono|split`  combined 0.0250  K=2 (GH 2, NPM 0)  admissible exemplars 2
- `1|serif|one-accent|plain-centered`  combined 0.0250  K=2 (GH 1, NPM 1)  admissible exemplars 2
- `1|serif|one-accent|ruled`  combined 0.0250  K=2 (GH 0, NPM 2)  admissible exemplars 2

Note: this counts every item of the archetype (inadmissible included) in k, as 82 section 6 does (denominator N includes inadmissible items); "admissible K" is for shipping only. Admissibility of an archetype = at least one admissible exemplar; the exclusion rules are per item.
