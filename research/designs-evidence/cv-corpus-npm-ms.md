# cv corpus evidence — L1 NPM(`jsonresume-theme`) + L2 MS(`resumes`)

Phase 4 coding task (F.a, split task 2 of 2). Coder counts; does not judge (R-d). Protocol:
`research/82-design-ranking-protocol.md` §3–§5 (binding), cross-checked against
`research/68-slop-patterns.md` and `skill/document-design-intelligence/data/base/constraints.csv`.
No git, no `load-base.py`/`build-manifest.py` run. No GitHub API call made anywhere in this task
(shared rate limit reserved for the other worker) — every fetch below is `registry.npmjs.org`,
`api.npmjs.org`, `raw.githubusercontent.com` (CDN, not the API), a project's own GitHub Pages site,
or `create.microsoft.com`/`word.cloud.microsoft`.

---

## Corpus A — L1 NPM(`jsonresume-theme`)

**URL:** `https://registry.npmjs.org/-/v1/search?text=jsonresume-theme&size=250`
**Query:** `text=jsonresume-theme`, `size=250` (npm max page size; endpoint is relevance-ranked, not
name-enumerated — see bias statement). **Sort/metric:** search payload's `score` fields are
normalised floats (quality/popularity/maintenance), not counts, so per §3 fallback the metric used
is `downloads.monthly`, fetched per package from `https://api.npmjs.org/downloads/point/last-month/<pkg1,pkg2,...>`
(bulk endpoint, comma-joined, batches of 40 packages/call, `curl -s -A "smart-design-research"`).
**Retrieval date:** 2026-09-23. **Total from search payload:** `total: 87644` (this is npm's whole-index
relevance total for the text query, not a count of on-topic packages — see bias statement).
**Names matching `^jsonresume-theme-`:** 229 of the 250 returned objects.

### Walk

Walked 229 candidates in `downloads.monthly` desc order (native order per §3.1). Stopped at native
position 83 with 40 on-topic codeable items collected (walk cap 200 not reached). 43 items were
excluded before reaching 40; the raw list below covers positions 1–83 (every position touched by
the walk). Positions 84–229 were never evaluated — the walk stops once 40 is reached (§3.1) and is
not extended for extra scrutiny.

**Codeable** per §3.3: a preview had to exist as (a) `https://jsonresume.org/themes/<slug>.png`,
which resolves to a Next.js custom 404 page for every slug tried (confirmed via `curl -I`, identical
19,197-byte body across different slugs, `x-matched-path: /404`) — so this exact path from the
protocol text is **dead as of 2026-09-23** and was not used; (b) the real gallery path discovered
during this task, `https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/<slug>.png`
(GitHub raw CDN, not the API — content-addressed, confirmed distinct file sizes per slug); or
(c) a non-badge image referenced in the package's own npm README (badges/analytics/avatar pixels
excluded — `shields.io`, `travis-ci`, `coveralls`, `ga-beacon`, `nodeico`, `waffle.io`,
`avatars.githubusercontent.com`, `herokuapp` markers filtered out programmatically, then every
remaining candidate image was downloaded and viewed, never rendered/compiled). All images were
downloaded to the OS temp dir and viewed with Read; none were copied into the repo.

**On-topic** per §3.2: excluded 4 packages as tools/generators with no fixed design or scaffolds
(`microdata` → schema.org output; `markdown` → plain-text output; `boilerplate-test`, `polymer` →
literal starter-scaffold repos, `polymer`'s own `package.json` `repository` field points at
`erming/jsonresume-theme-boilerplate`).

**Duplicates** per §3.2 (forks/ports of an already-counted design, highest metric kept): 6 packages
excluded — `codecobra`, `vp`, `ks` all reference the *identical* screenshot URL
`http://i.imgur.com/yktvc8m.png` as `caffeine` (pos 49, 130 dl/mo, highest metric); `eloquent-ru`,
`eloquent-mod` are declared forks of `eloquent` (pos 15, 263 dl/mo) referencing the same relative
screenshot path; `elegant-maksymgendin` is a fork of `elegant` (pos 2, 1937 dl/mo) with an
identical absolute screenshot URL.

**Broken previews** (not anticipated by §3, logged as `uncodeable`): `tan-responsive` — its
gallery slug resolves to a real file, but the rendered page is a blank/illegible grey placeholder
(screenshot capture failure upstream, not a design); `a11y` — its README "screenshot" is a tool
architecture diagram (JSON write/convert/render pipeline boxes A/B/C), not a rendered résumé. Both
were swapped for the next codeable item in native order (berlin-grid pos 80, clinical-precision
pos 83), keeping the walk strictly in metric order.

**Raw list, positions 1–83** (♦ = coded, one row per position; 40 coded + 43 excluded = 83):

| Pos | Package | dl/mo | Status | Reason |
|---|---|---|---|---|
| 1 | jsonresume-theme-even | 3001 | ♦ coded | — |
| 2 | jsonresume-theme-elegant | 1937 | ♦ coded | — |
| 3 | jsonresume-theme-engineering | 1627 | ♦ coded | — |
| 4 | jsonresume-theme-stackoverflow | 1050 | ♦ coded | — |
| 5 | jsonresume-theme-flat | 746 | ♦ coded | — |
| 6 | jsonresume-theme-onepage-plus | 557 | excluded | uncodeable — no non-badge README image, not in gallery |
| 7 | jsonresume-theme-kendall | 505 | ♦ coded | — |
| 8 | jsonresume-theme-modern | 493 | excluded | uncodeable — no non-badge README image, not in gallery |
| 9 | jsonresume-theme-macchiato | 452 | ♦ coded | — |
| 10 | jsonresume-theme-crisp | 414 | excluded | uncodeable — no non-badge README image, not in gallery |
| 11 | jsonresume-theme-material-moon | 373 | excluded | uncodeable — no non-badge README image, not in gallery |
| 12 | jsonresume-theme-randytarampi | 355 | excluded | uncodeable — README images are only a GA-beacon badge and an npm-version badge |
| 13 | jsonresume-theme-two-column | 311 | excluded | uncodeable — no non-badge README image, not in gallery |
| 14 | jsonresume-theme-engineering-leader | 304 | ♦ coded | — |
| 15 | jsonresume-theme-eloquent | 263 | ♦ coded | — |
| 16 | jsonresume-theme-paper | 251 | excluded | uncodeable — no non-badge README image, not in gallery |
| 17 | jsonresume-theme-classy | 242 | excluded | uncodeable — no non-badge README image, not in gallery |
| 18 | jsonresume-theme-tan-responsive | 226 | excluded | uncodeable — gallery image resolves but renders blank/illegible (capture failure) |
| 19 | jsonresume-theme-moon | 215 | excluded | uncodeable — no non-badge README image, not in gallery |
| 20 | jsonresume-theme-microdata | 210 | excluded | off-topic — outputs schema.org microdata, no fixed visual design |
| 21 | jsonresume-theme-lucide | 208 | ♦ coded | — |
| 22 | jsonresume-theme-actual | 203 | excluded | uncodeable — no non-badge README image, not in gallery |
| 23 | jsonresume-theme-sceptile | 195 | excluded | uncodeable — no non-badge README image, not in gallery |
| 24 | jsonresume-theme-paper-plus-plus | 189 | ♦ coded | — |
| 25 | jsonresume-theme-samk | 188 | excluded | uncodeable — no non-badge README image, not in gallery |
| 26 | jsonresume-theme-a11y | 181 | excluded | uncodeable — README image is a workflow diagram, not a résumé render |
| 27 | jsonresume-theme-professional | 178 | ♦ coded | — |
| 28 | jsonresume-theme-minyma | 169 | ♦ coded | — |
| 29 | jsonresume-theme-folio | 163 | excluded | uncodeable — no non-badge README image, not in gallery |
| 30 | jsonresume-theme-mantra | 162 | excluded | uncodeable — no non-badge README image, not in gallery |
| 31 | jsonresume-theme-class | 161 | excluded | uncodeable — no non-badge README image, not in gallery |
| 32 | jsonresume-theme-spartan | 156 | excluded | uncodeable — no non-badge README image, not in gallery |
| 33 | jsonresume-theme-pumpkin | 154 | ♦ coded | — |
| 34 | jsonresume-theme-material | 153 | excluded | uncodeable — no non-badge README image, not in gallery |
| 35 | jsonresume-theme-one | 151 | excluded | uncodeable — no non-badge README image, not in gallery |
| 36 | jsonresume-theme-jacrys | 145 | ♦ coded | — |
| 37 | jsonresume-theme-onepage | 142 | excluded | uncodeable — no non-badge README image, not in gallery |
| 38 | jsonresume-theme-claude | 142 | ♦ coded | — |
| 39 | jsonresume-theme-relaxed | 142 | ♦ coded | — |
| 40 | jsonresume-theme-architects-portfolio | 141 | ♦ coded | — |
| 41 | jsonresume-theme-full | 140 | excluded | uncodeable — no non-badge README image, not in gallery |
| 42 | jsonresume-theme-orbit | 138 | ♦ coded | — |
| 43 | jsonresume-theme-slick | 138 | excluded | uncodeable — no non-badge README image, not in gallery |
| 44 | jsonresume-theme-data-driven | 138 | ♦ coded | — |
| 45 | jsonresume-theme-rickosborne | 137 | ♦ coded | — |
| 46 | jsonresume-theme-tech | 135 | excluded | uncodeable — no non-badge README image, not in gallery |
| 47 | jsonresume-theme-paper_cn | 135 | excluded | uncodeable — no non-badge README image, not in gallery |
| 48 | jsonresume-theme-developer-mono | 133 | ♦ coded | — |
| 49 | jsonresume-theme-caffeine | 130 | ♦ coded | — |
| 50 | jsonresume-theme-spartacus | 128 | excluded | uncodeable — no non-badge README image, not in gallery |
| 51 | jsonresume-theme-kwann-nl | 123 | excluded | uncodeable — no non-badge README image, not in gallery |
| 52 | jsonresume-theme-folio-concise | 121 | excluded | uncodeable — no non-badge README image, not in gallery |
| 53 | jsonresume-theme-jdambron-fr | 116 | excluded | uncodeable — no non-badge README image, not in gallery |
| 54 | jsonresume-theme-sales-hunter | 116 | ♦ coded | — |
| 55 | jsonresume-theme-straightforward | 112 | excluded | uncodeable — no non-badge README image, not in gallery |
| 56 | jsonresume-theme-srt | 112 | excluded | uncodeable — no non-badge README image, not in gallery |
| 57 | jsonresume-theme-simple-red | 112 | ♦ coded | — |
| 58 | jsonresume-theme-colophon | 111 | ♦ coded | — |
| 59 | jsonresume-theme-jdambron | 106 | excluded | uncodeable — no non-badge README image, not in gallery |
| 60 | jsonresume-theme-brutalist | 104 | ♦ coded | — |
| 61 | jsonresume-theme-executive-slate | 103 | ♦ coded | — |
| 62 | jsonresume-theme-eventide | 101 | excluded | uncodeable — no non-badge README image, not in gallery |
| 63 | jsonresume-theme-academic | 101 | ♦ coded | — |
| 64 | jsonresume-theme-standard-resume | 99 | excluded | uncodeable — no non-badge README image, not in gallery |
| 65 | jsonresume-theme-short | 99 | excluded | uncodeable — no non-badge README image, not in gallery |
| 66 | jsonresume-theme-rocketspacer | 91 | ♦ coded | — |
| 67 | jsonresume-theme-kards | 89 | ♦ coded | — |
| 68 | jsonresume-theme-cjean | 87 | ♦ coded | — |
| 69 | jsonresume-theme-modern-classic | 84 | ♦ coded | — |
| 70 | jsonresume-theme-heavypaper | 83 | excluded | uncodeable — no non-badge README image, not in gallery |
| 71 | jsonresume-theme-elite | 82 | ♦ coded | — |
| 72 | jsonresume-theme-react | 82 | ♦ coded | — |
| 73 | jsonresume-theme-academic-cv-lite | 81 | ♦ coded | — |
| 74 | jsonresume-theme-codecobra | 79 | excluded | duplicate — fork/port of caffeine (pos 49), identical screenshot |
| 75 | jsonresume-theme-modern-plain | 78 | ♦ coded | — |
| 76 | jsonresume-theme-cora | 77 | excluded | uncodeable — no non-badge README image, not in gallery |
| 77 | jsonresume-theme-juno-nl | 77 | excluded | uncodeable — no non-badge README image, not in gallery |
| 78 | jsonresume-theme-jjlorenzoelegant | 76 | excluded | uncodeable — no non-badge README image, not in gallery |
| 79 | jsonresume-theme-papirus | 76 | ♦ coded | — |
| 80 | jsonresume-theme-berlin-grid | 76 | ♦ coded | — |
| 81 | jsonresume-theme-stackoverflowed | 75 | excluded | uncodeable — no non-badge README image, not in gallery |
| 82 | jsonresume-theme-straightforward-extra | 73 | excluded | uncodeable — no non-badge README image, not in gallery |
| 83 | jsonresume-theme-clinical-precision | 73 | ♦ coded | — |

(Items also excluded but at positions >83, discovered during the earlier full 1–144 gallery/README
scan before the broken-preview swap was known, listed for transparency though never part of the
final walk: 90 `elegant-pink`, 103 `eloquent-ru` (duplicate), 105 `two-column-modernist`, 106
`sidebar-photo-strip`, 107 `desert-modern`, 113 `pacific-horizon`, 118 `vp` (duplicate), 121
`typewriter-modern`, 124 `elegant-maksymgendin` (duplicate), 125 `community-garden`, 133 `ks`
(duplicate), 136 `art-deco`, 137 `art-school-modern`, 140 `product-manager-canvas`, 141
`eloquent-mod` (duplicate), 144 `mid-century-resume` — these were superseded once berlin-grid/
clinical-precision closed the count at position 83 and were not coded.)

### Coded table (40 items, page 1 only; decks n/a)

Columns: identity = columns, heading, colour, header. Variant = body, rules/boxes, density.
Family-specific variant = photo. Admissible = §5 pass/fail with rule id(s); `C1` = multi-column/
sidebar body text (ats-strict fail, applies to every `2-sidebar`/`3+` row below), `A7` = Office-
default-blue/indigo→purple gradient sole accent, `A8` = >50% of blocks individually bordered
("frames around everything"), `C3` = skill bars/rating dots, `C5` = graphic timeline, `C6` = text
boxes/layout-table blocks read as floating cards.

| Pos | Package | dl/mo | columns | heading | body | colour | header | rules/boxes | density | photo | Admissible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `jsonresume-theme-even` | 3001 | 1 | sans | sans | one-accent | plain-centered | rules | dense | yes | yes |
| 2 | `jsonresume-theme-elegant` | 1937 | 2-sidebar | sans | sans | one-accent | plain-left | rules | standard | yes | no (C1) |
| 3 | `jsonresume-theme-engineering` | 1627 | 1 | serif | serif | mono | plain-centered | rules | dense | no | yes |
| 4 | `jsonresume-theme-stackoverflow` | 1050 | 1 | sans | sans | multi | split | rules | standard | yes | yes |
| 5 | `jsonresume-theme-flat` | 746 | 1 | sans | sans | multi | plain-left | rules | dense | no | yes |
| 7 | `jsonresume-theme-kendall` | 505 | 2-sidebar | sans | sans | one-accent | band | boxes | standard | yes | no (C1,C3,C6) |
| 9 | `jsonresume-theme-macchiato` | 452 | 2-sidebar | display | sans | one-accent | band | rules | standard | no | no (C1) |
| 14 | `jsonresume-theme-engineering-leader` | 304 | 1 | sans | sans | mono | plain-centered | rules | standard | no | yes |
| 15 | `jsonresume-theme-eloquent` | 263 | 2-sidebar | sans | sans | one-accent | plain-left | boxes | standard | yes | no (C1) |
| 21 | `jsonresume-theme-lucide` | 208 | 2-sidebar | sans | sans | fill-blocks | plain-left | boxes | dense | no | no (C1) |
| 24 | `jsonresume-theme-paper-plus-plus` | 189 | 1 | serif | serif | one-accent | plain-centered | rules | standard | no | yes |
| 27 | `jsonresume-theme-professional` | 178 | 1 | serif | serif | mono | plain-centered | rules | dense | no | yes |
| 28 | `jsonresume-theme-minyma` | 169 | 1 | sans | sans | mono | plain-left | boxes | dense | yes | yes |
| 33 | `jsonresume-theme-pumpkin` | 154 | 1 | sans | sans | one-accent | plain-left | none | dense | no | yes |
| 36 | `jsonresume-theme-jacrys` | 145 | 1 | sans | sans | fill-blocks | plain-left | boxes | dense | yes | yes |
| 38 | `jsonresume-theme-claude` | 142 | 1 | sans | sans | one-accent | ruled | boxes | standard | no | no (A7) |
| 39 | `jsonresume-theme-relaxed` | 142 | 1 | sans | sans | multi | plain-left | boxes | dense | no | yes |
| 40 | `jsonresume-theme-architects-portfolio` | 141 | 1 | sans | sans | mono | plain-left | rules | airy | no | yes |
| 42 | `jsonresume-theme-orbit` | 138 | 2-sidebar | sans | sans | fill-blocks | plain-left | none | airy | yes | no (C1) |
| 44 | `jsonresume-theme-data-driven` | 138 | 1 | sans | sans | one-accent | ruled | boxes | dense | no | yes |
| 45 | `jsonresume-theme-rickosborne` | 137 | 2-sidebar | serif | serif | one-accent | plain-left | none | standard | yes | no (C1) |
| 48 | `jsonresume-theme-developer-mono` | 133 | 1 | mono | sans | one-accent | plain-left | rules | standard | no | yes |
| 49 | `jsonresume-theme-caffeine` | 130 | 2-sidebar | sans | sans | one-accent | band | rules | dense | yes | no (C1) |
| 54 | `jsonresume-theme-sales-hunter` | 116 | 1 | sans | sans | one-accent | plain-centered | boxes | standard | no | no (C6) |
| 57 | `jsonresume-theme-simple-red` | 112 | 1 | sans | sans | one-accent | plain-left | none | standard | no | yes |
| 58 | `jsonresume-theme-colophon` | 111 | 1 | serif | serif | one-accent | plain-left | none | airy | no | yes |
| 60 | `jsonresume-theme-brutalist` | 104 | 1 | display | sans | multi | plain-left | boxes | dense | no | no (A8) |
| 61 | `jsonresume-theme-executive-slate` | 103 | 2-sidebar | serif | sans | fill-blocks | plain-left | rules | standard | no | no (C1) |
| 63 | `jsonresume-theme-academic` | 101 | 1 | serif | serif | one-accent | split | rules | dense | no | yes |
| 66 | `jsonresume-theme-rocketspacer` | 91 | 1 | sans | sans | one-accent | plain-left | rules | airy | yes | yes |
| 67 | `jsonresume-theme-kards` | 89 | 1 | sans | sans | one-accent | image-hero | boxes | airy | no | yes |
| 68 | `jsonresume-theme-cjean` | 87 | 1 | sans | sans | one-accent | band | rules | standard | yes | yes |
| 69 | `jsonresume-theme-modern-classic` | 84 | 1 | sans | sans | one-accent | plain-left | rules | standard | no | yes |
| 71 | `jsonresume-theme-elite` | 82 | 3+ | sans | sans | fill-blocks | plain-left | boxes | dense | yes | no (C1,C3,C5) |
| 72 | `jsonresume-theme-react` | 82 | 2-sidebar | sans | sans | one-accent | plain-left | boxes | dense | no | no (C1) |
| 73 | `jsonresume-theme-academic-cv-lite` | 81 | 1 | serif | serif | one-accent | plain-centered | rules | standard | no | yes |
| 75 | `jsonresume-theme-modern-plain` | 78 | 1 | sans | sans | one-accent | split | rules | standard | no | yes |
| 79 | `jsonresume-theme-papirus` | 76 | 2-sidebar | sans | sans | fill-blocks | plain-centered | boxes | dense | yes | no (C1) |
| 80 | `jsonresume-theme-berlin-grid` | 76 | 1 | sans | sans | mono | plain-left | rules | standard | no | yes |
| 83 | `jsonresume-theme-clinical-precision` | 73 | 1 | sans | sans | one-accent | ruled | rules | standard | no | yes |

### Sources (repo + exact preview fetched, per item)

| Pos | Package | Repo | Preview URL |
|---|---|---|---|
| 1 | `jsonresume-theme-even` | https://github.com/rbardini/jsonresume-theme-even | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/even.png |
| 2 | `jsonresume-theme-elegant` | https://github.com/mudassir0909/jsonresume-theme-elegant | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/elegant.png |
| 3 | `jsonresume-theme-engineering` | https://github.com/skoenig/jsonresume-theme-engineering | https://github.com/skoenig/jsonresume-theme-engineering/blob/main/resume.png?raw=true |
| 4 | `jsonresume-theme-stackoverflow` | https://github.com/phoinixi/jsonresume-theme-stackoverflow | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/stackoverflow.png |
| 5 | `jsonresume-theme-flat` | https://github.com/erming/jsonresume-theme-flat | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/flat.png |
| 7 | `jsonresume-theme-kendall` | https://github.com/linuxbozo/jsonresume-theme-kendall | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/kendall.png |
| 9 | `jsonresume-theme-macchiato` | https://github.com/biosan/jsonresume-theme-macchiato | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/macchiato.png |
| 14 | `jsonresume-theme-engineering-leader` | https://github.com/sjw7444/jsonresume-theme-engineering-leader | https://github.com/sjw7444/jsonresume-theme-engineering-leader/blob/main/examples/example-resume.png?raw=true |
| 15 | `jsonresume-theme-eloquent` | https://github.com/thibaudcolas/jsonresume-theme-eloquent | https://raw.githubusercontent.com/thibaudcolas/jsonresume-theme-eloquent/master/raw/theme-screenshot.png |
| 21 | `jsonresume-theme-lucide` | https://github.com/Clement-Cauet/jsonresume-theme-lucide | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/lucide.png |
| 24 | `jsonresume-theme-paper-plus-plus` | https://github.com/lindell/jsonresume-theme-paper | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/paper-plus-plus.png |
| 27 | `jsonresume-theme-professional` | https://www.npmjs.com/package/jsonresume-theme-professional | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/professional.png |
| 28 | `jsonresume-theme-minyma` | https://github.com/godraadam/jsonresume-theme-minyma | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/minyma.png |
| 33 | `jsonresume-theme-pumpkin` | https://github.com/bvosk/jsonresume-theme-pumpkin | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/pumpkin.png |
| 36 | `jsonresume-theme-jacrys` | https://github.com/jacrys/jsonresume-theme-jacrys | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/jacrys.png |
| 38 | `jsonresume-theme-claude` | https://github.com/rolandnsharp/jsonresume-theme-claude | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/claude.png |
| 39 | `jsonresume-theme-relaxed` | https://github.com/ObserverOfTime/jsonresume-theme-relaxed | https://raw.githubusercontent.com/ObserverOfTime/jsonresume-theme-relaxed/master/.github/sample.jpeg |
| 40 | `jsonresume-theme-architects-portfolio` | https://www.npmjs.com/package/jsonresume-theme-architects-portfolio | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/architects-portfolio.png |
| 42 | `jsonresume-theme-orbit` | https://github.com/XuluWarrior/jsonresume-theme-orbit | https://xuluwarrior.github.io/jsonresume-theme-orbit/resume.jpg |
| 44 | `jsonresume-theme-data-driven` | https://www.npmjs.com/package/jsonresume-theme-data-driven | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/data-driven.png |
| 45 | `jsonresume-theme-rickosborne` | https://github.com/rickosborne/jsonresume-theme-rickosborne | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/rickosborne.png |
| 48 | `jsonresume-theme-developer-mono` | https://www.npmjs.com/package/jsonresume-theme-developer-mono | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/developer-mono.png |
| 49 | `jsonresume-theme-caffeine` | https://github.com/kelyvin/jsonresume-theme-caffeine | http://i.imgur.com/yktvc8m.png |
| 54 | `jsonresume-theme-sales-hunter` | https://www.npmjs.com/package/jsonresume-theme-sales-hunter | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/sales-hunter.png |
| 57 | `jsonresume-theme-simple-red` | https://github.com/aandrewww/jsonresume-theme-simple-red | https://raw.githubusercontent.com/aandrewww/jsonresume-theme-simple-red/master/screenshots/screenshot-1.jpg |
| 58 | `jsonresume-theme-colophon` | https://github.com/dmnelson/jsonresume-theme-colophon | https://raw.githubusercontent.com/dmnelson/jsonresume-theme-colophon/main/docs/screenshot.png |
| 60 | `jsonresume-theme-brutalist` | https://www.npmjs.com/package/jsonresume-theme-brutalist | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/brutalist.png |
| 61 | `jsonresume-theme-executive-slate` | https://www.npmjs.com/package/jsonresume-theme-executive-slate | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/executive-slate.png |
| 63 | `jsonresume-theme-academic` | https://github.com/ebenezer-isaac/jsonresume-theme-academic | https://raw.githubusercontent.com/ebenezer-isaac/jsonresume-theme-academic/main/examples/preview.png |
| 66 | `jsonresume-theme-rocketspacer` | https://github.com/rocketspacer/jsonresume-theme-rocketspacer | https://raw.githubusercontent.com/rocketspacer/jsonresume-theme-rocketspacer/master/sample.png |
| 67 | `jsonresume-theme-kards` | https://github.com/XuluWarrior/jsonresume-theme-kards | https://xuluwarrior.github.io/jsonresume-theme-kards/resume-1.png |
| 68 | `jsonresume-theme-cjean` | https://github.com/cjean-fr/atelier | https://i.imgur.com/lWBFRBK.png |
| 69 | `jsonresume-theme-modern-classic` | https://www.npmjs.com/package/jsonresume-theme-modern-classic | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/modern-classic.png |
| 71 | `jsonresume-theme-elite` | https://github.com/nass600/jsonresume-theme-elite | https://raw.githubusercontent.com/nass600/jsonresume-theme-elite/master/docs/img/elite.png |
| 72 | `jsonresume-theme-react` | https://github.com/phoinixi/jsonresume-theme-react | https://raw.githubusercontent.com/phoinixi/jsonresume-theme-react/master/screenshot.png |
| 73 | `jsonresume-theme-academic-cv-lite` | https://www.npmjs.com/package/jsonresume-theme-academic-cv-lite | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/academic-cv-lite.png |
| 75 | `jsonresume-theme-modern-plain` | https://github.com/roman-pinchuk/jsonresume-theme-modern-plain | https://github.com/user-attachments/assets/9e74bc13-415c-471e-abaa-20f81cc29a76 |
| 79 | `jsonresume-theme-papirus` | https://github.com/konalexiou/jsonresume-theme-papirus | https://raw.githubusercontent.com/konalexiou/jsonresume-theme-papirus/master/papirus.png |
| 80 | `jsonresume-theme-berlin-grid` | https://www.npmjs.com/package/jsonresume-theme-berlin-grid | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/berlin-grid.png |
| 83 | `jsonresume-theme-clinical-precision` | https://www.npmjs.com/package/jsonresume-theme-clinical-precision | https://raw.githubusercontent.com/jsonresume/jsonresume.org/master/apps/homepage2/public/img/themes/clinical-precision.png |

### Admissibility summary (§5)

15 of 40 coded items (37.5%) are inadmissible:

- **C1** (multi-column body/sidebar body text — universal for `ats-strict`): every `2-sidebar` and
  `3+` archetype — pos 2, 7, 9, 15, 21, 42, 45, 49, 61, 71, 72, 79 (12 items). This is the dominant
  exclusion reason and removes essentially the entire "photo + narrow sidebar" style family from
  the ATS-admissible pool, consistent with real ATS guidance.
- **A7** (sole accent is an indigo→purple/blue gradient bar, matching the "blue-to-purple gradient
  is the single loudest AI tell" pattern in research/68): pos 38 (`claude`).
- **A8** (>50% of content blocks individually bordered, "frames around everything"): pos 60
  (`brutalist`) — top meta bar, About block and every Experience entry are each boxed in a thick
  black border.
- **C3** (skill bars/rating dots): pos 7 (`kendall`, thin progress bar under each skill category)
  and pos 71 (`elite`, five-dot skill rating rows).
- **C5** (graphic timeline): pos 71 (`elite`, connected timeline dots down the Experience column).
- **C6** (text boxes/layout-table blocks read as floating cards): pos 7 (`kendall`, grey-filled job
  entry), pos 54 (`sales-hunter`, left-border-accented card per job entry).

25 of 40 (62.5%) are admissible. This exceeds the family-wide coarsening trigger check: of the 25
admissible items, 15 sit in singleton archetypes (60% > 50%) **but** 6 archetypes have k≥2 (need
<5 to trigger), so **no coarsening** — the 4th identity feature (header treatment) is kept.

### Frequency table (raw k/40, all coded items; admissible k shown separately)

| Archetype (`columns\|heading\|colour\|header`) | k/40 | share | admissible k | items (pos) |
|---|---|---|---|---|
| `1\|sans\|one-accent\|plain-left` | 4/40 | 0.100 | 4 | pumpkin(33), simple-red(57), rocketspacer(66), modern-classic(69) |
| `2-sidebar\|sans\|one-accent\|plain-left` | 3/40 | 0.075 | 0 | elegant(2), eloquent(15), react(72) |
| `1\|sans\|mono\|plain-left` | 3/40 | 0.075 | 3 | minyma(28), architects-portfolio(40), berlin-grid(80) |
| `1\|sans\|one-accent\|ruled` | 3/40 | 0.075 | 2 | claude(38)[A7], data-driven(44), clinical-precision(83) |
| `1\|sans\|one-accent\|plain-centered` | 2/40 | 0.050 | 1 | even(1), sales-hunter(54)[C6] |
| `1\|serif\|mono\|plain-centered` | 2/40 | 0.050 | 2 | engineering(3), professional(27) |
| `1\|sans\|multi\|plain-left` | 2/40 | 0.050 | 2 | flat(5), relaxed(39) |
| `2-sidebar\|sans\|one-accent\|band` | 2/40 | 0.050 | 0 | kendall(7), caffeine(49) |
| `2-sidebar\|sans\|fill-blocks\|plain-left` | 2/40 | 0.050 | 0 | lucide(21), orbit(42) |
| `1\|serif\|one-accent\|plain-centered` | 2/40 | 0.050 | 2 | paper-plus-plus(24), academic-cv-lite(73) |
| `1\|sans\|multi\|split` | 1/40 | 0.025 | 1 | stackoverflow(4) |
| `2-sidebar\|display\|one-accent\|band` | 1/40 | 0.025 | 0 | macchiato(9) |
| `1\|sans\|mono\|plain-centered` | 1/40 | 0.025 | 1 | engineering-leader(14) |
| `1\|sans\|fill-blocks\|plain-left` | 1/40 | 0.025 | 1 | jacrys(36) |
| `2-sidebar\|serif\|one-accent\|plain-left` | 1/40 | 0.025 | 0 | rickosborne(45) |
| `1\|mono\|one-accent\|plain-left` | 1/40 | 0.025 | 1 | developer-mono(48) |
| `1\|serif\|one-accent\|plain-left` | 1/40 | 0.025 | 1 | colophon(58) |
| `1\|display\|multi\|plain-left` | 1/40 | 0.025 | 0 | brutalist(60)[A8] |
| `2-sidebar\|serif\|fill-blocks\|plain-left` | 1/40 | 0.025 | 0 | executive-slate(61) |
| `1\|serif\|one-accent\|split` | 1/40 | 0.025 | 1 | academic(63) |
| `1\|sans\|one-accent\|image-hero` | 1/40 | 0.025 | 1 | kards(67) |
| `1\|sans\|one-accent\|band` | 1/40 | 0.025 | 1 | cjean(68) |
| `3+\|sans\|fill-blocks\|plain-left` | 1/40 | 0.025 | 0 | elite(71)[C1,C3,C5] |
| `1\|sans\|one-accent\|split` | 1/40 | 0.025 | 1 | modern-plain(75) |
| `2-sidebar\|sans\|fill-blocks\|plain-centered` | 1/40 | 0.025 | 0 | papirus(79) |

25 distinct archetypes over 40 items; Ranking Metric string for every row: `share:NPM:k/40 by
downloads.monthly`.

### Bias statement

- **Search is relevance-ranked, not a name enumeration.** `text=jsonresume-theme&size=250` returned
  250 objects (npm's per-call max) of which 229 matched `^jsonresume-theme-`; the search index's own
  `total` field (87,644) shows the true universe of text-matching packages is far larger than what
  npm's relevance sort surfaces on one page. 18 slugs shown on the maintainers' own
  `jsonresume.org/themes` gallery (e.g. `tailwind`, `consultant-polished`, `government-standard`,
  `investor-brief`) never appeared among the 229 — either published under a different name pattern
  or ranked below page 1 of relevance. The corpus is therefore a **relevance-biased sample of an
  already-narrow ecosystem**, not a full census.
- **Population skew.** npm/JSON Resume theme authors are overwhelmingly individual developers
  writing in JavaScript/Node — the corpus over-represents monospace/sans "developer aesthetic"
  designs (dark backgrounds, code-editor chrome, GitHub-styled cards: `stackoverflow`,
  `developer-mono`, `github`-family) and under-represents non-technical office/admin résumé styles.
  English-only; many entries are explicit regional ports (`-fr`, `-nl`, `-de`, `-ru` suffixes)
  confirming a mostly Western-developer author base.
- **Download counts reward age and defaults, not current quality.** `downloads.monthly` accumulates
  via `jsonresume` CLI's historic default-theme chain and CI/test installs, not necessarily human
  choice; `even` (pos 1, 3001 dl/mo) is very plausibly still the CLI's bundled default rather than
  3001 people actively picking it monthly.
- **The `jsonresume.org/themes` gallery is curated, not exhaustive**, and its preview pipeline
  itself is stale in one place (`/themes/<slug>.png` 404s; the real path is one directory level
  under the site's own repo) — a second, independent bias on top of the search bias above, disclosed
  and worked around rather than silently absorbed.
- **C1 (multi-column) removes proportionally more of the higher-download items** than lower ones —
  6 of the top 15 by downloads are `2-sidebar`/`3+`, vs. 6 of the remaining 25 — so the admissible
  pool's *shape* skews toward mid-tier packages relative to the raw popularity order.

### Second-coder sample (§7)

ids = `NPM:<position zero-padded to 3>`, all 40 coded ids, sorted lexicographically, sampled with
`random.Random("82:cv").sample(ids, max(min(10,len(ids)), math.ceil(0.25*len(ids))))` → n=10:

`NPM:021` (lucide), `NPM:044` (data-driven), `NPM:045` (rickosborne), `NPM:048` (developer-mono),
`NPM:057` (simple-red), `NPM:060` (brutalist), `NPM:061` (executive-slate), `NPM:066`
(rocketspacer), `NPM:068` (cjean), `NPM:080` (berlin-grid).

The second coder should receive only §4–§5 of research/82 and, for these 10 ids, the package name +
repo URL + preview URL from the Sources table above (no codes, no admissibility calls from this
file).

---

## Corpus B — L2 MS(`resumes`)

**Attempted URL (per research/82 §10/§R protocol-author probe):**
`https://create.microsoft.com/en-us/templates/resumes`. **Retrieval date:** 2026-09-23.

**Result: unreachable as of 2026-09-23 — site migrated since the protocol's probe.** `curl -sIL`
shows `create.microsoft.com/en-us/templates/resumes` now **301-redirects** to
`https://word.cloud.microsoft/create/en/resume-templates/?source=create_flow`, a fully
client-rendered Next.js app. The fetched static HTML (299,315 bytes, `curl -sL`) contains only
page chrome, locale-alternate `<link>` tags, and OpenGraph/Twitter meta tags — zero occurrences of
`assetId`, `templateId`, a template `"name"`/`"title"` field, or any thumbnail image URL; the
template catalogue itself loads via a client-side call made only after JS hydration, which is not
present in the server-rendered payload and cannot be enumerated with `curl`. This contradicts
research/82's protocol-author probe text ("Microsoft Create category URLs that resolve with items
in the static payload: resumes (34 items)...") — that finding is now stale; the underlying site
changed between the protocol freeze and this task's retrieval, both dated 2026-09-23.

Two independent fallback attempts were made before concluding unreachable (both honestly reported,
neither fabricated):
1. `https://templates.office.com/en-us/templates-for-resumes` → 301 → `create.microsoft.com/en-us`
   → 301 → `https://m365.cloud.microsoft/create?...` → generic Microsoft 365/Copilot landing page
   (`office_resumes.html`, 278,991 bytes) with **zero** occurrences of the word "resume" in a
   template-name context (5 unrelated hits) and no template data at all.
2. `https://word.cloud.microsoft/sitemap.xml` → sitemap index → `.../create/sitemap.xml` (225,585
   bytes) — this **does** resolve and lists per-locale category pages (`.../en/resume-templates/`,
   `.../en/resume-builder/`, three blog posts) for 16 locales, but **no per-template URLs at all** —
   confirming the individual template gallery is not just unreached by chance but genuinely absent
   from any crawlable/static surface of the new site.

Per research/82 §10 fallback clause ("use only if items and a metric come back; else note
'unreachable 2026-xx-xx'"), this corpus is recorded as: **MS(resumes) unreachable 2026-09-23.** No
items, no metric, no k, no N. This is not a "thin" L2 (§2 threshold for <10 on-topic items) —
it is zero on-topic items because the catalogue could not be retrieved by any means available to a
non-JS-executing worker (WebFetch/curl), consistent with the constraint that GitHub's API could not
be used either as a substitute avenue (out of scope for this task regardless).

**Recommendation for the orchestrator:** either (a) accept cv as single-corpus L1 for this split
(NPM only, disclosed) until a JS-capable fetch path to the new Microsoft site is available, or (b)
substitute one of research/82 §10's other permitted L2 sources for cv if the family's evidence
needs a second corpus (none is currently designated as a fallback for cv specifically — LibreOffice
templates has no "resume"/"CV" *Templates* subcategory distinct from other office docs, per the
protocol author's own LibreOffice probe notes in §R, so this is not a drop-in substitute without a
fresh probe). This file does not choose for the orchestrator; it reports the fetch outcome only.

---

## Report / protocol ambiguities met in practice

- **Counts:** NPM corpus — 40 coded (25 admissible / 15 inadmissible), 43 excluded (33 uncodeable,
  4 off-topic, 6 duplicate), 229 on-topic-by-name candidates from a 250-object relevance page over
  an index of 87,644 text matches. MS corpus — 0 items, corpus unreachable.
- **Frequency table:** 25 distinct archetypes over the 40 NPM items; top archetype
  `1|sans|one-accent|plain-left` at 4/40 (0.100); no archetype reaches K≥2 admissible beyond 4.
- **Exclusions:** 43 total (see raw list); 6 of those are duplicate forks/ports resolved by exact
  screenshot-URL or declared-fork-name match, not by visual judgement.
- **Ambiguities encountered:**
  1. Protocol's literal preview path `jsonresume.org/themes/<slug>.png` is dead (404, confirmed by
     identical byte-for-byte response across slugs); the real path is one directory level into the
     `jsonresume/jsonresume.org` GitHub repo's own public assets, discovered by following an
     absolute image URL used inside several packages' own READMEs. Resolved by using that path for
     every gallery-sourced preview, disclosed here rather than silently substituted.
  2. §3's "Codeable iff a preview exists... README image" doesn't specify how to resolve a
     *relative* image path in a README (e.g. `resume.png`, `screenshots/screenshot.png`) to a
     fetchable URL. Resolved by trying `raw.githubusercontent.com/<owner>/<repo>/main/<path>` then
     `.../master/<path>` against the package's own declared `repository` field — a mechanical,
     disclosed convention, not a judgement call.
  3. §3's duplicate/fork rule ("Forks or ports of an already-counted design are counted once") does
     not state the detection method. Applied narrowly and mechanically here: only excluded as
     duplicate where the *exact same screenshot URL* was referenced by both packages, or where the
     lower-metric package's own name/declared fork relationship made it explicit (`-ru`, `-mod`
     suffixes of `eloquent`). Visually-similar-but-independently-sourced designs (e.g. `elegant`
     vs. `stackoverflow`, which share a similar sidebar+photo layout with a small measured pixel
     diff but different repos/authors) were coded independently, not merged, since R-d forbids
     judging "is this really the same design" beyond mechanical evidence.
  4. The MS(resumes) site migration (create.microsoft.com → word.cloud.microsoft) happening between
     protocol freeze and this task's retrieval, both dated 2026-09-23, is disclosed rather than
     silently worked around with an invented item list.
  5. Two npm README "preview" images turned out on inspection to be non-résumé content (a tool
     workflow diagram, and a broken/blank capture) — codeable-per-metadata but not codeable-per-
     content. Both were swapped for the next native-order item rather than coded from a
     non-representative image.

## Library snapshot

No `research/library/*` or `skill/document-design-intelligence/data/base/*` files were modified by
this task (coding only, per F.a). `skill/document-design-intelligence/data/base/constraints.csv`
was read to confirm the `ats-strict` fail-rule ids (`ats-no-multi-column`, `ats-no-symbol-glyphs`,
etc.) cited above as C1/C3/C4 equivalents.
