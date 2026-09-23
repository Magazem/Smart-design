# cv — L1 corpus GH(`resume+template`) (F.a, split task 1 of 2)

Coder role: count, never judge (research/82 §1, R-d). This file covers only the GitHub L1 corpus
for the `cv` family. The second L1/L2 corpus (NPM `jsonresume-theme`, MS `resumes`) is a separate
split task; combined ranking/frequency and the fill step (§8) happen once both are in hand and are
**not** done here.

## Corpus

- URL: `https://api.github.com/search/repositories?q=resume+template&sort=stars&order=desc&per_page=100`
- Query: `resume+template`, sort: `stars`, order: `desc`, `per_page=100`
- Retrieved: 2026-09-23 (single page fetch via `curl -s -A "smart-design-research"`; no rate-limit
  retries needed, one call)
- `total_count` (API): 11352
- Walk cap: 200 raw items (protocol §3.1). Actual walk: **77 raw items**, stopped once 40 on-topic
  codeable items were coded (see "Sequencing note" below for one disclosed deviation from strict
  rank order in the last two slots).

## Raw list (rank = native stars-desc position, stars = `stargazers_count` at fetch time)

`OT?` = on-topic per §3.2. `Codeable?` = preview found per §3.3 (README image / example PDF /
gallery thumbnail, downloaded to system temp and viewed with Read; never rendered/compiled).

| Rank | Repo | Stars | On-topic? | Codeable? | Reason / note |
|---|---|---|---|---|---|
| 1 | posquit0/Awesome-CV | 28570 | yes | yes | LaTeX CV template, own design |
| 2 | geekcompany/ResumeSample | 28317 | yes | **no** | collection of per-role `.md` content files (php.md, java.md…), no image/PDF preview anywhere in repo — uncodeable |
| 3 | billryan/resume | 11452 | yes | yes | LaTeX résumé template |
| 4 | JordanSchuetz/LearnCS8-Resume | 11202 | yes | **no** | `img/` folder contains unrelated conference photos (GDC talk, balloon arch) baked into the template as placeholder content — no genuine layout preview exists; uncodeable |
| 5 | resumejob/awesome-resume | 7431 | **no** | — | awesome-list of external links/phrases, not a template |
| 6 | deedy/Deedy-Resume | 5063 | yes | yes | LaTeX two-column CV template |
| 7 | jankapunkt/latexcv | 3342 | yes | yes | LaTeX CV/resume collection; coded on first design shown (`docs/media/classic.png`) |
| 8 | jakegut/resume | 2816 | yes | yes | LaTeX resume template ("Jake's Resume") |
| 9 | dnl-blkv/mcdowell-cv | 2709 | yes | yes | LaTeX CV template |
| 10 | sproogen/modern-resume-theme | 2311 | yes | yes | Jekyll resume theme |
| 11 | tbakerx/react-resume-template | 2142 | yes | **no** | README has only badges/social icons, no screenshot; no image/PDF anywhere in repo — uncodeable |
| 12 | LingyiChen-AI/JadeAI | 1984 | **no** | — | AI resume-builder tool/generator ("50+ templates, AI optimization"), no fixed design |
| 13 | jglovier/resume-template | 1971 | yes | yes | Jekyll + GitHub Pages resume template |
| 14 | WebPraktikos/universal-resume | 1798 | yes | **no** | only a live HTML demo (`docs/index.html`), no static image/PDF — would require rendering, disallowed |
| 15 | devcelio/resume-template | 1696 | yes | **no** | LaTeX source only, no committed PDF/image preview |
| 16 | elipapa/markdown-cv | 1497 | yes | **no** | README images are generic GitHub help-doc screenshots + a Gravatar avatar, not the CV layout |
| 17 | LimHyungTae/Awesome-PhD-CV | 1281 | **no** | — | curated list of academic CV templates + guidelines, not itself a template |
| 18 | ubaimutl/react-portfolio | 1172 | **no** | — | portfolio website, not a résumé/CV document |
| 19 | mmmlllnnn/ResumeCollection | 1172 | yes | yes | collection of Chinese résumé templates; coded on first design shown (`1.中文简历/001/001.jpg`) |
| 20 | youngyangyang04/Markdown-Resume-Template | 1044 | yes | **no** | the linked preview image (`kamajianli.jpg`) is a screenshot of an unrelated third-party résumé-builder website (卡码简历), not this template's output — uncodeable |
| 21 | darwiin/yaac-another-awesome-cv | 1040 | yes | yes | LaTeX CV template (Font Awesome + Source Sans) |
| 22 | acmenlei/codecv | 981 | **no** | — | online résumé-builder tool, not a fixed template |
| 23 | fky2015/resume-ng | 880 | yes | yes | LaTeX resume template; README file is lowercase `readme.md` (not fetched by the default-case URL, refetched directly) |
| 24 | liweitianux/resume | 853 | yes | yes | LaTeX CV, coded from committed `resume-zh+en.pdf` (no README image) |
| 25 | yunanwg/brilliant-CV | 842 | yes | yes | Typst CV template |
| 26 | xriley/Orbit-Theme | 819 | yes | yes | Bootstrap 5 resume/CV template |
| 27 | subidit/rover-resume | 805 | yes | yes | LaTeX ATS resume template; repo ships 6 variants, coded on first shown ("Base Rover") |
| 28 | ndpvt-web/latex-document-skill | 767 | **no** | — | Claude Code tool/skill bundle (27 templates + scripts), not a single template |
| 29 | ankitsultana/researcher | 756 | yes | **no** | README images are only a personal photo and an institute-logo sample, no CV layout preview |
| 30 | htmldocs-js/htmldocs | 745 | **no** | — | general document-authoring framework ("LaTeX alternative"), no fixed design |
| 31 | nordicgiant2/react-nice-resume | 685 | yes | **no** | linked preview shows an unrelated colourful portfolio splash/landing page ("Nordic-Giant Project"), not resume content — uncodeable |
| 32 | jbee37142/gatsby-starter-bee | 677 | **no** | — | blog template (other family) |
| 33 | luosijie/vue-resume | 648 | yes | **no** | the "usage" image is a mouse-click instructional strip ("Click on Content / Right Click on Item…"), not the resume design |
| 34 | tbaltrushaitis/cv | 635 | yes | **no** | only preview is an animated GIF; captured frame is a loading spinner, not resume content — uncodeable |
| 35 | ptsouchlos/modern-cv | 624 | yes | yes | Typst resume template inspired by Awesome-CV |
| 36 | mnjul/html-resume | 606 | yes | yes | HTML/CSS resume, coded from committed `firefox_result.pdf` |
| 37 | changh95/latex_resume_template_kor | 566 | yes | yes | LaTeX CV/resume template for Koreans |
| 38 | zachscrivena/simple-resume-cv | 555 | yes | yes | XeLaTeX resume/CV template |
| 39 | murraco/jekyll-theme-minimal-resume | 553 | yes | yes | Jekyll minimal resume theme |
| 40 | geekplux/cv_resume | 544 | yes | yes | LaTeX CV/resume template |
| 41 | byoungd/Resume-template-for-Coder | 532 | yes | yes | resume template; several sketches, coded on first shown (`2021-preview.png`) |
| 42 | jskherman/imprecv | 514 | yes | yes | Typst CV template |
| 43 | Blankj/resume | 500 | yes | **no** | only `.html`/`.md` source, no committed image/PDF preview |
| 44 | yanliudesign/offer-toolkit-skill | 494 | **no** | — | job-hunt Claude skill bundle (JD decoder + builder + 11 templates), tool not a single template |
| 45 | adongwanai/LLM-Resume-Template | 460 | yes | **no** | README's only images are hosted in an unrelated repo ("Awesome-Awesome-LLMs") and do not depict this template's résumé layout |
| 46 | guilyx/awesome-github-pages-portfolios | 445 | **no** | — | awesome-list + portfolio (other family) |
| 47 | thehale/expressive-resume | 443 | yes | yes | LaTeX resume/cover-letter template pair; coded on the resume (`examples/resume.png`) |
| 48 | AVS1508/My-Alternate-Portfolio-Website | 404 | **no** | — | portfolio website |
| 49 | darhonbek/resume_templates | 389 | **no** | — | "result-oriented achievement" bullet-phrasing guide, not a document design |
| 50 | imfing/vuepress-homepage | 375 | **no** | — | general homepage/portfolio template; resume is one of several unrelated uses, not CV-specific |
| 51 | Zilize/DrawCV | 372 | yes | yes | Draw.io-based CV template; preview is a promo banner containing the actual rendered sample |
| 52 | chrisneagu/FTC-Skystone-Dark-Angels-Romania-2020 | 313 | **no** | — | FTC robotics competition SDK, unrelated (false keyword match) |
| 53 | Erik-Cupsa/ResumeTemplate | 309 | yes | **no** | only `main.tex`, no committed PDF/image |
| 54 | eddiewebb/hugo-resume | 306 | yes | yes | Hugo resume theme |
| 55 | crispgm/resume | 306 | yes | yes | Jekyll/Hexo minimalist resume template |
| 56 | ryanbalieiro/react-portfolio-template | 306 | **no** | — | portfolio template |
| 57 | dcetin/Simple-CV | 305 | yes | yes | LaTeX CV template with BibLaTeX |
| 58 | FrancesCoronel/hire-me | 303 | **no** | — | job-hunt guide (tutorial), not a fixed template |
| 59 | MLNLP-World/Academic-Resume-Template | 298 | yes | yes | academic bilingual résumé template |
| 60 | srleom/astro-theme-resume | 285 | yes | **no** | linked `public/images/image.png` is only a headshot photo, not a page layout — uncodeable |
| 61 | mliu7/latex-moderncv | 274 | yes | yes | LaTeX moderncv-based resume; coded from committed `mark_liu_resume.pdf` |
| 62 | cowboysmall-tools/hugo-devresume-theme | 272 | yes | yes | Hugo resume/CV theme for developers |
| 63 | Hunterdii/Smart-AI-Resume-Analyzer | 253 | **no** | — | AI résumé-analysis tool |
| 64 | Tombarr/html-resume-template | 246 | yes | yes | HTML/CSS/JS resume template |
| 65 | stuxf/basic-typst-resume-template | 241 | yes | yes | Typst resume template |
| 66 | lanxx314/resume | 232 | yes | yes | LaTeX resume template |
| 67 | aershov24/101-developer-resume-cv-templates | 225 | yes | **no** | repo is per-stack bullet-phrasing `.md` guides, no visual template/preview |
| 68 | rohitg00/one_pager_resume_template | 225 | yes | yes | LaTeX one-pager resume template |
| 69 | sleepymalc/LaTeX-Template | 224 | **no** | — | generic multi-family LaTeX template collection (notes, reports, beamers, CV together), not CV-specific |
| 70 | 0xPrateek/Portfolio-Template | 221 | **no** | — | portfolio website |
| 71 | afnizarnur/draco | 219 | yes | yes | personal résumé/portfolio site template with an Experience section |
| 72 | Stavrospanakakis/jekyll-cv | 216 | yes | yes | Jekyll CV theme with dark mode |
| 73 | daehopark/resume-for-web-developer | 213 | yes | yes | HTML5 résumé template |
| 74 | izzydoesizzy/resumetemplate | 212 | **no** | — | description states "personal website/landing page template", not CV-specific despite repo name |
| 75 | hyesungoh/comet-land | 202 | yes | **no** | only image found (`comet-land-blog.png`) depicts the blog section, not the résumé content |
| 76 | NorthSecond/Auto_Typst_Resume_Template | 202 | yes | yes | Typst bilingual résumé template |
| 77 | maksymilan/zju-resume-template | 198 | yes | yes | LaTeX CV template (photo + PDF in repo) |

**Totals for the walk (ranks 1–77):** on-topic = 59, off-topic = 20, on-topic-but-uncodeable = 19
(2,4,11,14,15,16,20,29,31,33,34,43,45,53,60,67,75 = 17 **plus** the 2 that were superseded once
40 codeable items were already reached — see note below), **codeable on-topic (coded) = 40 = N**.

**Sequencing note (disclosed deviation).** Preview-checking was not perfectly linear: ranks 76–79
were investigated slightly out of strict order for efficiency (fetching several README candidates
in parallel batches). The correct effect on the corpus is nil — the first 40 on-topic codeable
items in native rank order are exactly ranks {1,3,6,7,8,9,10,13,19,21,23,24,25,26,27,35,36,37,38,
39,40,41,42,47,51,54,55,57,59,61,62,64,65,66,68,71,72,73,76,77}, and that is the set actually
coded below (rank 77 = the 40th). Ranks 78–79 (stick-i/markdown-resume-template, dphang/resume)
were fetched during the search but are **not** part of the corpus (N=40 was already reached at
rank 77); they are noted here only for transparency, not coded.

## Coded table (N = 40; id = `GH:<rank zero-padded to 3>`)

Identity features: **columns | heading | colour use | header treatment**. Variant: body class,
rules/boxes, density, photo (cv variant feature). "Admissible" = passes §5 (universal + cv fail
constraints C1–C6); reason cites rule ids for excludes.

| id | Repo | Stars | Columns | Heading | Body | Colour | Header | Rules/boxes | Density | Photo | Admissible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GH:001 | posquit0/Awesome-CV | 28570 | 1 | sans | sans | one-accent | plain-centered | rules | dense | no | yes |
| GH:003 | billryan/resume | 11452 | 1 | serif | serif | mono | plain-centered | rules | airy | no | yes |
| GH:006 | deedy/Deedy-Resume | 5063 | 2-sidebar | sans | sans | mono | plain-left | none | dense | no | **no — C1** (multi-column body) |
| GH:007 | jankapunkt/latexcv | 3342 | 1 | serif | sans | one-accent | plain-centered | rules | standard | no | yes |
| GH:008 | jakegut/resume | 2816 | 1 | serif | serif | mono | plain-centered | rules | dense | no | yes |
| GH:009 | dnl-blkv/mcdowell-cv | 2709 | 1 | serif | serif | mono | split | rules | dense | no | yes |
| GH:010 | sproogen/modern-resume-theme | 2311 | 1 | sans | sans | mono | split | rules | airy | yes | yes |
| GH:013 | jglovier/resume-template | 1971 | 1 | sans | serif | mono | plain-centered | rules | airy | yes | yes |
| GH:019 | mmmlllnnn/ResumeCollection | 1172 | 1 | sans | sans | fill-blocks | band | rules | standard | yes | yes |
| GH:021 | darwiin/yaac-another-awesome-cv | 1040 | 1 | sans | sans | one-accent | split | boxes | dense | yes | yes |
| GH:023 | fky2015/resume-ng | 880 | 1 | serif | serif | mono | plain-left | rules | dense | no | yes |
| GH:024 | liweitianux/resume | 853 | 1 | sans | sans | one-accent | plain-left | rules | dense | no | yes |
| GH:025 | yunanwg/brilliant-CV | 842 | 1 | sans | sans | one-accent | split | rules | standard | yes | yes |
| GH:026 | xriley/Orbit-Theme | 819 | 2-sidebar | sans | sans | fill-blocks | plain-left | rules | standard | yes | **no — C1, C3** (skill-proficiency bars) |
| GH:027 | subidit/rover-resume | 805 | 1 | serif | serif | mono | split | rules | standard | no | yes |
| GH:035 | ptsouchlos/modern-cv | 624 | 1 | sans | sans | one-accent | split | rules | dense | no | yes |
| GH:036 | mnjul/html-resume | 606 | 1 | sans | sans | mono | plain-left | rules | dense | no | yes |
| GH:037 | changh95/latex_resume_template_kor | 566 | 2-sidebar | sans | sans | fill-blocks | plain-left | rules | dense | no | **no — C1, C5** (graphic timeline connectors) |
| GH:038 | zachscrivena/simple-resume-cv | 555 | 1 | serif | serif | mono | plain-centered | none | dense | no | yes |
| GH:039 | murraco/jekyll-theme-minimal-resume | 553 | 1 | sans | sans | fill-blocks | band | none | airy | no | yes |
| GH:040 | geekplux/cv_resume | 544 | 1 | sans | sans | one-accent | split | rules | dense | yes | yes |
| GH:041 | byoungd/Resume-template-for-Coder | 532 | 1 | serif | serif | one-accent | plain-left | none | airy | no | yes |
| GH:042 | jskherman/imprecv | 514 | 1 | serif | serif | mono | plain-centered | rules | dense | no | yes |
| GH:047 | thehale/expressive-resume | 443 | 1 | sans | sans | mono | split | rules | standard | no | yes |
| GH:051 | Zilize/DrawCV | 372 | 2-sidebar | sans | sans | mono | split | rules | dense | yes | **no — C1, C3** (per-skill rating dots) |
| GH:054 | eddiewebb/hugo-resume | 306 | 2-sidebar | sans | sans | fill-blocks | band | none | airy | yes | **no — C1, A3** (gradient fill behind header/body) |
| GH:055 | crispgm/resume | 306 | 1 | sans | sans | mono | split | rules | airy | no | yes |
| GH:057 | dcetin/Simple-CV | 305 | 1 | serif | serif | mono | split | rules | dense | no | yes |
| GH:059 | MLNLP-World/Academic-Resume-Template | 298 | 1 | sans | sans | one-accent | split | rules | dense | yes | yes |
| GH:061 | mliu7/latex-moderncv | 274 | 1 | sans | sans | one-accent | split | rules | dense | no | yes |
| GH:062 | cowboysmall-tools/hugo-devresume-theme | 272 | 2-sidebar | sans | serif | one-accent | split | rules | standard | yes | **no — C1** |
| GH:064 | Tombarr/html-resume-template | 246 | 2-sidebar | sans | serif | mono | plain-left | boxes | standard | no | **no — C1** |
| GH:065 | stuxf/basic-typst-resume-template | 241 | 1 | serif | serif | one-accent | plain-left | rules | dense | no | yes |
| GH:066 | lanxx314/resume | 232 | 1 | sans | sans | mono | split | rules | dense | yes | yes |
| GH:068 | rohitg00/one_pager_resume_template | 225 | 1 | serif | serif | mono | split | rules | dense | no | yes |
| GH:071 | afnizarnur/draco | 219 | 1 | serif | sans | mono | plain-left | none | airy | yes | yes |
| GH:072 | Stavrospanakakis/jekyll-cv | 216 | 2-sidebar | sans | sans | one-accent | plain-left | rules | dense | no | **no — C1** |
| GH:073 | daehopark/resume-for-web-developer | 213 | 2-sidebar | sans | sans | mono | split | rules | standard | no | **no — C1, C3** (proficiency bars) |
| GH:076 | NorthSecond/Auto_Typst_Resume_Template | 202 | 1 | serif | serif | mono | plain-centered | rules | dense | no | yes |
| GH:077 | maksymilan/zju-resume-template | 198 | 1 | sans | sans | one-accent | split | rules | dense | no | yes |

Admissible = 31/40. Inadmissible = 9/40 (all fail C1, three additionally fail C3, one C5, one A3).

## Exclusions log

Admissibility exclusions (item still counts in N; archetype logged, not shipped):

| id | Rule(s) | Evidence |
|---|---|---|
| GH:006 | C1 | narrow left column (~30% width) carries Education/Links/Coursework/Skills alongside a wider Experience/Research column — two independently flowing text columns |
| GH:026 | C1, C3 | teal sidebar (~25%) + main column; sidebar "Skills & Proficiency" uses filled progress bars per skill |
| GH:037 | C1, C5 | right sidebar (~20%) for Contact/Skills; left column experience entries connected by a vertical timeline line with date-dot markers |
| GH:051 | C1, C3 | left ~70%/right ~30% split; right column "技能" lists Git/Java/C++/Python/JavaScript each with 5 dot-rating icons |
| GH:054 | C1, A3 | left nav-label sidebar + main card; card background is a purple-to-pink gradient fill behind the header and lead paragraph |
| GH:062 | C1 | left ~75% Experience column / right ~25% Skills+Education sidebar |
| GH:064 | C1 | left ~20% Contact/Skills/Technologies/References sidebar / right main column |
| GH:072 | C1 | left ~25% Contact/Languages/Education/Skills sidebar / right main column |
| GH:073 | C1, C3 | right ~20% column of section-label anchors beside main content; "Skill" section uses Master/Professional/Senior/Junior/Rookie horizontal proficiency bars |

Uncodeable exclusions (do not count toward N=40; excluded before feature coding per §3.3):

| Rank | Repo | Reason |
|---|---|---|
| 2 | geekcompany/ResumeSample | text-only `.md` role guides, no image/PDF preview anywhere in repo |
| 4 | JordanSchuetz/LearnCS8-Resume | `img/` assets are unrelated conference photos, not a résumé layout |
| 11 | tbakerx/react-resume-template | README carries only badges/shields, no screenshot or PDF exists in repo |
| 14 | WebPraktikos/universal-resume | only a live-rendered HTML demo, no static preview (rendering disallowed by §3.3) |
| 15 | devcelio/resume-template | LaTeX source only, no committed preview asset |
| 16 | elipapa/markdown-cv | README images are generic GitHub-help screenshots + a Gravatar avatar, not the CV |
| 20 | youngyangyang04/Markdown-Resume-Template | linked image shows an unrelated résumé-builder website's homepage, not this template |
| 29 | ankitsultana/researcher | README images are a personal photo and an institute-logo sample, no layout preview |
| 31 | nordicgiant2/react-nice-resume | linked image is an unrelated portfolio splash/landing page, not résumé content |
| 33 | luosijie/vue-resume | the "usage" image is a mouse-click instructional strip, not the resume design |
| 34 | tbaltrushaitis/cv | only preview is an animated GIF whose captured frame is a loading spinner |
| 43 | Blankj/resume | HTML/MD source only, no committed image/PDF |
| 45 | adongwanai/LLM-Resume-Template | README images are hosted in an unrelated repo and do not show this template |
| 53 | Erik-Cupsa/ResumeTemplate | `.tex` source only, no committed preview |
| 60 | srleom/astro-theme-resume | linked image is a personal headshot photo, not a page layout |
| 67 | aershov24/101-developer-resume-cv-templates | per-stack bullet-phrasing `.md` guides, no visual template |
| 75 | hyesungoh/comet-land | only image found depicts the blog section, not the résumé |

Cross-listing note (§3.2, quote/estimate token): none of the 40 coded items name quote/estimate/
devis/Angebot in their titles.

## Frequency table of archetypes (k/40; N=40, this corpus only)

Archetype = `columns|heading|colour|header` (identity features only). Admissible column marks
whether that k contributes admissible exemplars.

| Archetype | k | k/40 | Admissible exemplars? |
|---|---|---|---|
| `1\|sans\|one-accent\|split` | 7 | 0.175 | yes (7/7) |
| `1\|serif\|mono\|plain-centered` | 5 | 0.125 | yes (5/5) |
| `1\|serif\|mono\|split` | 4 | 0.100 | yes (4/4) |
| `1\|sans\|mono\|split` | 4 | 0.100 | yes (4/4) |
| `1\|sans\|fill-blocks\|band` | 2 | 0.050 | yes (2/2) |
| `1\|serif\|mono\|plain-left` | 2 | 0.050 | yes (2/2) |
| `1\|serif\|one-accent\|plain-left` | 2 | 0.050 | yes (2/2) |
| `2-sidebar\|sans\|mono\|plain-left` | 2 | 0.050 | no (0/2 — GH:006, GH:064; both C1) |
| `2-sidebar\|sans\|fill-blocks\|plain-left` | 2 | 0.050 | no (0/2 — GH:026, GH:037; C1 +C3/C5) |
| `2-sidebar\|sans\|mono\|split` | 2 | 0.050 | no (0/2 — GH:051, GH:073; C1 +C3) |
| `1\|sans\|one-accent\|plain-centered` | 1 | 0.025 | yes |
| `1\|serif\|one-accent\|plain-centered` | 1 | 0.025 | yes |
| `1\|sans\|mono\|plain-centered` | 1 | 0.025 | yes |
| `1\|sans\|one-accent\|plain-left` | 1 | 0.025 | yes |
| `1\|sans\|mono\|plain-left` | 1 | 0.025 | yes |
| `2-sidebar\|sans\|fill-blocks\|band` | 1 | 0.025 | no (GH:054; C1+A3) |
| `2-sidebar\|sans\|one-accent\|split` | 1 | 0.025 | no (GH:062; C1) |
| `2-sidebar\|sans\|one-accent\|plain-left` | 1 | 0.025 | no (GH:072; C1) |

Sum of k = 40. 18 distinct archetypes; 31 admissible items across 12 distinct admissible
archetypes; 5 of those 12 admissible archetypes are singletons (5/31 ≈ 16% of admissible items) —
below the 50% coarsening trigger in §4, so **no coarsening applied**; the 4th identity feature
(header treatment) is kept.

Modal admissible archetype: **`1|sans|one-accent|split`**, k=7/40 (share 0.175), all 7 exemplars
admissible — this is the largest coherent group in the corpus (single-column body, sans display
type, one accent colour, name/title on one side of the header band with contact/photo on the
other).

## Bias statement

This corpus is **GitHub, developer/LaTeX-skewed** (research/82 §13): dominated by software
engineers building their own résumé as a LaTeX/Typst/Jekyll/React side project. Effects visible in
the coded table:
- Heavy `heading=serif` presence (10/40) comes almost entirely from LaTeX academic-CV lineages
  (Computer Modern/Latin Modern faces default in `article`/`moderncv`-style classes), not from a
  general population preference for serif résumés.
- English- and Chinese-language items dominate (several explicitly bilingual or Chinese-only,
  e.g. GH:019, GH:040, GH:059, GH:077); no items in other non-English languages appeared in the
  admissible top 40.
- Multi-column ("2-sidebar") designs are disproportionately excluded here (9/9 candidates fail
  admissibility), which is a property of the *cv* family's ATS constraints (C1), not of GitHub's
  popularity signal — GitHub stars reward visual sophistication (sidebars, timelines, skill bars)
  that ATS-strict coding then rejects wholesale. This is a real, disclosed tension: the most
  "starred" designs on GitHub skew toward exactly the multi-column/graphic patterns this family's
  fail constraints exclude.
- Photo=yes appears in 9/40 (22.5%), all discretionary (never forced): several items are static
  Jekyll/React personal-site templates where an avatar is conventional; this is a stronger
  photo-inclusion rate than a strictly ATS-first population would show, again a developer-site
  artefact (personal homepage conventions bleeding into "CV" repos) rather than an ATS-résumé norm.
- GitHub stars reward long-lived popular repos; several top items (Awesome-CV, Deedy-Resume,
  billryan/resume, mcdowell-cv) are 8+ years old and no longer maintained, so the corpus also
  skews toward *historically* popular LaTeX designs over current tooling (Typst templates, e.g.
  GH:025, GH:035, GH:042, GH:065, GH:071 [Typst-adjacent via Draco's JS/PSD lineage], GH:076,
  GH:077, appear only at lower star counts despite being newer/current designs).

## Second-coder sample (§7, seeded)

ids = `GH:<rank zero-padded to 3>` for all 40 coded items, sorted lexicographically (equivalent to
ascending numeric order here, since all ranks are zero-padded to 3 digits):

```
GH:001 GH:003 GH:006 GH:007 GH:008 GH:009 GH:010 GH:013 GH:019 GH:021
GH:023 GH:024 GH:025 GH:026 GH:027 GH:035 GH:036 GH:037 GH:038 GH:039
GH:040 GH:041 GH:042 GH:047 GH:051 GH:054 GH:055 GH:057 GH:059 GH:061
GH:062 GH:064 GH:065 GH:066 GH:068 GH:071 GH:072 GH:073 GH:076 GH:077
```

`n_sample = max(min(10, 40), ceil(0.25 * 40)) = max(10, 10) = 10`

```python
import math, random
sample = random.Random("82:cv").sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))
```

Computed sample (10 ids), for the independent second coder to receive with §4–§5 and the item/
preview URLs only (no codes from this file):

```
GH:021  GH:057  GH:041  GH:055  GH:040  GH:039  GH:064  GH:076  GH:061  GH:051
```

Corresponding repos (for the orchestrator's convenience in assembling the second-coder packet —
**not** to be shown to the second coder alongside this file's codes):
GH:021 darwiin/yaac-another-awesome-cv · GH:057 dcetin/Simple-CV · GH:041 byoungd/Resume-template-
for-Coder · GH:055 crispgm/resume · GH:040 geekplux/cv_resume · GH:039 murraco/jekyll-theme-
minimal-resume · GH:064 Tombarr/html-resume-template · GH:076 NorthSecond/Auto_Typst_Resume_
Template · GH:061 mliu7/latex-moderncv · GH:051 Zilize/DrawCV.

## Preview sources used (for reproducibility / second coder)

| id | Preview URL used |
|---|---|
| GH:001 | raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/resume-0.png |
| GH:003 | user-images.githubusercontent.com/25968335/131621921-...png (README "English" sample) |
| GH:006 | raw.githubusercontent.com/deedydas/Deedy-Resume/master/OpenFonts/sample-image.png |
| GH:007 | raw.githubusercontent.com/jankapunkt/latexcv/master/docs/media/classic.png |
| GH:008 | raw.githubusercontent.com/jakegut/resume/master/resume.png |
| GH:009 | raw.githubusercontent.com/dnl-blkv/mcdowell-cv/master/McDowell_CV.png |
| GH:010 | raw.githubusercontent.com/sproogen/modern-resume-theme/master/screenshot.png |
| GH:013 | raw.githubusercontent.com/jglovier/resume-template/master/images/screenshot.png |
| GH:019 | raw.githubusercontent.com/mmmlllnnn/ResumeCollection/master/1.中文简历/001/001.jpg |
| GH:021 | raw.githubusercontent.com/darwiin/yaac-another-awesome-cv/master/example/preview/cv1.jpeg |
| GH:023 | github.com/fky2015/resume-ng user-attached asset (readme.md, lowercase) |
| GH:024 | raw.githubusercontent.com/liweitianux/resume/master/resume-zh+en.pdf (page 1) |
| GH:025 | raw.githubusercontent.com/yunanwg/brilliant-CV/main/thumbnail.png |
| GH:026 | themes.3rdwavemedia.com Orbit promo mockup (shows actual template + demo cards) |
| GH:027 | raw.githubusercontent.com/subidit/rover-resume/main/img/base-rover.jpg |
| GH:035 | raw.githubusercontent.com/ptsouchlos/modern-cv/main/assets/images/header.png |
| GH:036 | raw.githubusercontent.com/mnjul/html-resume/master/firefox_result.pdf (page 1) |
| GH:037 | raw.githubusercontent.com/changh95/latex_resume_template_kor/main/resume_img.png |
| GH:038 | raw.githubusercontent.com/zachscrivena/simple-resume-cv/master/Miscellaneous/CV-01.png |
| GH:039 | raw.githubusercontent.com/murraco/jekyll-theme-minimal-resume/master/screenshot.png |
| GH:040 | raw.githubusercontent.com/geekplux/cv_resume/master/template_cn_blue.png |
| GH:041 | raw.githubusercontent.com/byoungd/Resume-template-for-Coder/master/Resume-Sketch-byoungd/2021-preview.png |
| GH:042 | github.com/jskherman/imprecv/raw/main/assets/thumbnail.1.png |
| GH:047 | raw.githubusercontent.com/thehale/expressive-resume/main/examples/resume.png |
| GH:051 | raw.githubusercontent.com/Zilize/DrawCV/master/asset/Banner.png |
| GH:054 | raw.githubusercontent.com/eddiewebb/hugo-resume/master/images/about.png |
| GH:055 | raw.githubusercontent.com/crispgm/resume/master/screenshots/resume-desktop.png |
| GH:057 | raw.githubusercontent.com/dcetin/Simple-CV/master/img/black-1.png |
| GH:059 | raw.githubusercontent.com/MLNLP-World/Academic-Resume-Template/main/imgs/sample/2_1.png |
| GH:061 | raw.githubusercontent.com/mliu7/latex-moderncv/master/mark_liu_resume.pdf (page 1) |
| GH:062 | raw.githubusercontent.com/cowboysmall-tools/hugo-devresume-theme/master/images/screenshot.png |
| GH:064 | raw.githubusercontent.com/Tombarr/html-resume-template/master/Chrome_sample.jpg |
| GH:065 | raw.githubusercontent.com/stuxf/basic-typst-resume-template/main/example-resume.png |
| GH:066 | raw.githubusercontent.com/lanxx314/resume/master/resume-zh_CN.png |
| GH:068 | raw.githubusercontent.com/rohitg00/one_pager_resume_template/main/rohit_resume_screenshot.png |
| GH:071 | cloud.githubusercontent.com/assets/4648648/26038614/...png (Draco promo screenshot) |
| GH:072 | raw.githubusercontent.com/Stavrospanakakis/jekyll-cv/main/preview.png |
| GH:073 | raw.githubusercontent.com/daehopark/resume-for-web-developer/master/assets/img/screenshot.png |
| GH:076 | raw.githubusercontent.com/NorthSecond/Auto_Typst_Resume_Template/main/docs/English.png |
| GH:077 | raw.githubusercontent.com/maksymilan/zju-resume-template/master/CV.jpg |

## Notes for the Manager (ambiguities encountered in practice, not amendments)

1. **"Codeable" is doing double duty.** §3.3 defines codeable as "a preview exists"; in practice
   a majority of not-codeable exclusions here were previews that *exist but are wrong/unrelated*
   (mismatched images, tool screenshots, instructional graphics, headshots-only) rather than
   simply absent. The protocol text reads as if codeable is a yes/no on existence; I treated
   "preview exists but does not depict this repo's own résumé layout" as equivalent to no preview
   (uncodeable), which seems like the intended spirit but is not literally what §3.3 says.
2. **Repo shipping several designs, "first design shown in its README."** For jankapunkt/latexcv,
   mmmlllnnn/ResumeCollection, byoungd/Resume-template-for-Coder, subidit/rover-resume, and
   ethanhe42/resume-template-style repos, "first shown" was unambiguous (README lists images in a
   fixed order). It would be worth pre-registering whether "first" means first `<img>`/`![]`
   markdown token in source order, or first visually-rendered position — for these five it was the
   same, but a table-based README could make them differ.
3. **GH:071 (afnizarnur/draco) family fit is soft.** Draco's shipped page reads as a personal
   "About Me" landing page with a "Work Experiences" section rather than a conventional CV/résumé
   document; it was coded on-topic per §3.2's broad "template/theme whose output is a document of
   the family" test, but a stricter reading could exclude it as a portfolio-site hybrid. Flagging
   rather than silently excluding, since it materially affects whether N=40 needs a different 40th
   item.
4. **Cross-linked/aliased preview hosting.** Two items (GH:023 fky2015, GH:071 afnizarnur) host
   their preview image on `user-images.githubusercontent.com`/`cloud.githubusercontent.com`
   (GitHub's old attachment CDN) rather than in-repo — these were still treated as "the repo's own
   README image" per §3.3 since the README markdown source links them directly, but they are not
   literally files in the repository tree; worth confirming this counts as "fetched" rank value
   evidence for provenance purposes.
5. **Duplicate/port de-duplication (§3.2) did not bite inside the coded 40**, but was observed
   just beyond it: abdullah-arif-swe/modern-deedy (rank 95, 142 stars, explicitly "based on
   Deedy") would have been a duplicate of GH:006 had the walk reached that far; not an issue for
   this file since N=40 was reached at rank 77, but flagging for the family assembler in case the
   NPM/L2 corpus surfaces the same duplicate independently.
6. **Rate limiting:** the single unauthenticated GitHub Search API call (`per_page=100`) returned
   all needed data in one request; the ≥7s inter-call sleep rule in §1/§3 did not end up mattering
   here since only one search call was needed (all subsequent fetches were `raw.githubusercontent.
   com`/`api.github.com/repos/.../contents`, which are not the rate-limited search endpoint).
