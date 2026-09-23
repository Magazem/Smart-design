# deck corpus evidence — L1 NPM(`slidev-theme`)

Phase 4 coding task (F.a, deck, split task 1 of 2). Coder counts; does not judge (R-d). Protocol:
`research/82-design-ranking-protocol.md` §3–§5 (binding) as amended by
`research/82a-clarifications-1.md` (binding, applied throughout this file — every place a
clarification changed a call from a first pass is disclosed inline), cross-checked against
`research/68-slop-patterns.md` and `skill/document-design-intelligence/data/base/constraints.csv`.
No git, no `load-base.py`/`build-manifest.py` run, no GitHub *search* API call anywhere in this task
(shared rate limit reserved for the other worker). Every fetch below is `registry.npmjs.org`,
`api.npmjs.org`, `raw.githubusercontent.com` / `media.githubusercontent.com` / `cdn.jsdelivr.net`
(CDN mirrors, not the API), a project's own GitHub Pages site, `github.com/<owner>/<repo>` HTML
pages (repo pages, not search), or the GitHub *contents* API (`api.github.com/repos/<owner>/<repo>/
contents/<path>`, a per-repo read, not search) used a handful of times to list a directory when a
declared image path 404'd.

**Corpus URL:** `https://registry.npmjs.org/-/v1/search?text=slidev-theme&size=250`
**Query:** `text=slidev-theme`, `size=250` (npm's max page size for one call; no pagination beyond
this per research/82 §10's exact `NPM(t)` URL). **Sort/metric:** `downloads.monthly`, present
directly in each returned object's `downloads` field (no separate bulk-downloads call was needed —
the search payload already carries it). **Retrieval date:** 2026-09-23. **Total from search
payload:** `total: 87769` (npm's whole-index relevance total for the text query, not a count of
on-topic packages — see bias statement). **Names matching `slidev-theme-*` or
`@scope/slidev-theme-*`:** 225 of the 250 returned objects.

## Walk

Walked 225 candidates in `downloads.monthly` desc order (native order per §3.1). The walk needed to
go to native position 143 to collect 40 on-topic codeable admissible-to-attempt items (one
uncodeable item at position 59, `improving-25`, was discovered only after coding had begun and was
swapped out per 82a C2/C6 — see note on that row); positions beyond 143 were never evaluated. Walk
cap (200) was not reached.

**On-topic** per §3.2: every position examined below is a genuine `slidev-theme-*`/
`@scope/slidev-theme-*` npm package (all matched the exact name filter); no off-topic tool/generator/
framework-core package was encountered in the walked range (no `awesome-list`, no bare `reveal.js`/
`marp-cli` core, etc. — `slidev-theme-reveal` and `slidev-theme-excalidraw` are themes skinning
Slidev to *look like* those tools, not the tools themselves, so they are on-topic). No cross-listing
to `quote` applied (no item title referenced quote/estimate/devis/Angebot).

**Codeable** per §3.3, as clarified by 82a **C2** and **C6**: a preview had to exist as (a) a
non-badge image in the package's own npm README (npm mirrors the GitHub README at publish time);
(b) a non-badge image in the GitHub repo's own current README (fetched separately when the npm copy
had none, since npm's mirrored copy can be stale — badge/CI/license/analytics images filtered by a
domain/keyword blocklist: `shields.io`, `badgen.net`, `netlify` deploy-status badges, `opencollective`,
GitHub Actions workflow badges, `stargazers`/`network/members` count badges); or (c) a thumbnail in
the official Slidev theme gallery (`https://raw.githubusercontent.com/slidevjs/slidev/main/docs/
.vitepress/themes.ts`, the data file backing `sli.dev/resources/theme-gallery` — the gallery page
itself is a client-rendered VitePress SPA with no static item data, so this underlying data file was
fetched instead, itself a raw GitHub file, not the API). Per 82a C6, several items whose npm-README-
declared preview path 404'd were coded from the item's own published preview found by another route
(GitHub README, gallery) instead — disclosed per item in the Notes table. Every candidate image was
downloaded to the OS temp dir and viewed with Read; none were copied into the repo, none were
rendered/compiled from source.

**Uncodeable** per §3.3 and 82a **C2** (broadened: "no preview" *or* "preview present but not the
item's design" — wrong/unrelated asset, logo-only, broken path): the dominant exclusion reason in
this corpus by far. Concretely: `slidev-theme-tulip-lab` (only image is a wordmark logo, not a slide
render); `slidev-theme-academic` (its README-declared preview screenshots have been deleted from the
repo — 404 both at the declared path and inside the published npm tarball; the only bundled image is
an unrelated stock audience photo used as example content, not a design render); `slidev-theme-tud`
(only available format is SVG with an embedded base64 raster plus vector-outlined text — no
rendering tool was available in this environment to view it as a raster image, so it could not be
coded from); `slidev-theme-hka`, `slidev-theme-ycs77`, `slidev-theme-prussianblue` (no GitHub repo
link resolvable from npm metadata, README, or maintainer-username guesses); `slidev-theme-
architectural-console`, `slidev-theme-supa11y`, `slidev-theme-nxyz` (README-declared image paths
404 at the repo's current default branch — path renamed/removed since the README was written, and
82a C6's "replace with the item's own published preview" turned up nothing else usable);
`slidev-theme-rich` (its only image host, `images.jieyu.ai`, fails DNS resolution entirely). Every
other excluded position (the large majority) is the plain case: no non-badge image found anywhere.
`slidev-theme-improving-25` (walked position 59) was initially coded but is now **excluded and
replaced** per 82a **C2**: its only fetchable image is a colour-palette content slide, and no title
slide could be found anywhere for it (README/gallery) — since deck identity features (background,
title-slide layout) are read from the title slide (82a **C7**), an item with no title-slide preview
cannot be coded on those features even though *a* preview file exists. It is replaced in the coded
40 by `slidev-theme-renuo` (walked position 143, downloads.monthly = 20, tied with several others at
that count — taken as the next on-topic codeable item after 139 in the walk).

**Duplicates** per §3.2: none excluded as duplicate. Two pairs of independently-authored,
independent-repo items turned out to share the same underlying visual archetype after coding
(`bestony2026`/`noninsurance`, `frankfurt`/`takahashi` incidentally, etc. — see frequency table) —
these are **not** forks or ports of one another (different owners, different repos, no declared
fork relationship, no shared screenshot URL), so per §3.2's literal test (exact-asset or declared-
fork match only) they were coded independently, not merged. Their shared archetype is exactly what
the frequency count is for.

**Raw list, positions 1–143** (♦ = coded; 40 coded + 103 excluded = 143 positions touched):

| Pos | Package | dl/mo | Status | Reason |
|---|---|---|---|---|
| 1 | `slidev-theme-ehl2022` | 8652 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 2 | `slidev-theme-the-unnamed` | 1880 | ♦ coded | - |
| 3 | `slidev-theme-penguin` | 1650 | ♦ coded | - |
| 4 | `@echmo/slidev-theme-lidarcar-cz` | 1456 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 5 | `slidev-theme-tulip-lab` | 1385 | excluded | uncodeable - only image found is a wordmark logo, not a slide/design screenshot |
| 6 | `slidev-theme-light-icons` | 1372 | ♦ coded | - |
| 7 | `slidev-theme-dracula` | 1358 | ♦ coded | - |
| 8 | `slidev-theme-tud` | 1348 | excluded | uncodeable - only preview format is SVG with embedded base64 raster + vector text; no rendering tool available |
| 9 | `slidev-theme-purplin` | 1096 | ♦ coded | - |
| 10 | `slidev-theme-geist` | 767 | ♦ coded | - |
| 11 | `slidev-theme-academic` | 764 | excluded | uncodeable - README-referenced screenshots removed from repo (404 at declared path and in npm tarball); no rendered slide preview found |
| 12 | `slidev-theme-giornata` | 725 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 13 | `slidev-theme-alchemmist` | 681 | ♦ coded | - |
| 14 | `slidev-theme-kotlin` | 634 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 15 | `slidev-theme-lilas` | 589 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 16 | `slidev-theme-neversink` | 516 | ♦ coded | - |
| 17 | `slidev-theme-scholarly` | 503 | ♦ coded | - |
| 18 | `slidev-theme-excalidraw` | 490 | ♦ coded | - |
| 19 | `slidev-theme-tahta` | 456 | ♦ coded | - |
| 20 | `slidev-theme-nearform` | 433 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 21 | `@troshab/slidev-theme-troshab` | 399 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 22 | `slidev-theme-rockdove` | 394 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 23 | `slidev-theme-meetup` | 313 | ♦ coded | - |
| 24 | `@sp-days-framework/slidev-theme-sykehuspartner` | 282 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 25 | `slidev-theme-eloc` | 281 | ♦ coded | - |
| 26 | `slidev-theme-unicorn` | 273 | ♦ coded | - |
| 27 | `slidev-theme-supa11y` | 259 | excluded | uncodeable - README-referenced img.png 404s at guessed monorepo subpath |
| 28 | `slidev-theme-frankfurt` | 243 | ♦ coded | - |
| 29 | `slidev-theme-bestony2026` | 229 | ♦ coded | - |
| 30 | `@gepardec/slidev-theme-gepardec` | 226 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 31 | `slidev-theme-mokkapps` | 222 | ♦ coded | - |
| 32 | `slidev-theme-takahashi` | 206 | ♦ coded | - |
| 33 | `slidev-theme-gtlabo` | 204 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 34 | `slidev-theme-architectural-console` | 201 | excluded | uncodeable - README-referenced ./screenshots/1.png 404s at repo root on default branch |
| 35 | `slidev-theme-webhh` | 170 | ♦ coded | - |
| 36 | `slidev-theme-nord` | 155 | ♦ coded | - |
| 37 | `slidev-theme-vuetiful` | 150 | ♦ coded | - |
| 38 | `slidev-theme-pku` | 149 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 39 | `@aotoki/slidev-theme-terraforming` | 136 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 40 | `slidev-theme-dataerai` | 127 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 41 | `slidev-theme-cobalt` | 124 | ♦ coded | - |
| 42 | `slidev-theme-excali-slide` | 123 | ♦ coded | - |
| 43 | `slidev-theme-practicum` | 117 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 44 | `@carlory/slidev-theme-daocloud` | 111 | ♦ coded | - |
| 45 | `@politecnicoopenunixlabs/slidev-theme-poul` | 107 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 46 | `slidev-theme-hep` | 102 | ♦ coded | - |
| 47 | `slidev-theme-hka` | 100 | excluded | uncodeable - no GitHub repo link resolvable from npm metadata/README/maintainer |
| 48 | `slidev-theme-field-manual` | 98 | ♦ coded | - |
| 49 | `slidev-theme-ksick-dynatrace` | 86 | ♦ coded | - |
| 50 | `@luocfprime/slidev-theme-ustc` | 80 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 51 | `@zlict/slidev-theme-zli` | 79 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 52 | `slidev-theme-noninsurance` | 79 | ♦ coded | - |
| 53 | `slidev-theme-rainforest` | 77 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 54 | `slidev-theme-touying` | 72 | ♦ coded | - |
| 55 | `slidev-theme-enolive` | 71 | ♦ coded | - |
| 56 | `slidev-theme-ycs77` | 70 | excluded | uncodeable - no GitHub repo link resolvable from npm metadata |
| 57 | `slidev-theme-viplay` | 68 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 58 | `slidev-theme-mumbo` | 62 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 59 | `slidev-theme-improving-25` | 61 | excluded | uncodeable (82a C2) — only fetchable image is a colour-palette content slide, no title slide found anywhere (README/gallery); cannot code the deck identity features (background, title-slide layout) which are read from the title slide, so the item is not usable even though a preview file exists |
| 60 | `slidev-theme-greycat` | 59 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 61 | `@jungsap/slidev-theme-sap` | 58 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 62 | `slidev-theme-prussianblue` | 57 | excluded | uncodeable - no GitHub repo link resolvable; only image reference is a Netlify badge |
| 63 | `slidev-theme-diapositiv` | 55 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 64 | `slidev-theme-datev-scc` | 55 | ♦ coded | - |
| 65 | `slidev-theme-abicom` | 54 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 66 | `slidev-theme-soba` | 53 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 67 | `@yettoapp/slidev-theme-yetto` | 50 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 68 | `slidev-theme-tud-db` | 49 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 69 | `@ricoapon/slidev-theme-technical` | 48 | ♦ coded | - |
| 70 | `slidev-theme-foamscience` | 48 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 71 | `slidev-theme-dmml` | 47 | ♦ coded | - |
| 72 | `@insight-services-apac/slidev-theme-insight` | 47 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 73 | `slidev-theme-onecraft` | 47 | ♦ coded | - |
| 74 | `slidev-theme-envek` | 46 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 75 | `@puzzleitc/slidev-theme-puzzle` | 45 | excluded | codeable but walk already reached 40 before this position was needed |
| 76 | `slidev-theme-hexlet` | 44 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 77 | `slidev-theme-miracle` | 44 | excluded | codeable but walk already reached 40 before this position was needed |
| 78 | `slidev-theme-raft` | 44 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 79 | `slidev-theme-mint` | 42 | ♦ coded | - |
| 80 | `slidev-theme-nxyz` | 42 | excluded | uncodeable - README-referenced img/cover.png 404s on both main and master branches |
| 81 | `slidev-theme-reveal` | 42 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 82 | `slidev-theme-mistica` | 40 | excluded | codeable but walk already reached 40 before this position was needed |
| 83 | `slidev-theme-capgemini` | 39 | excluded | codeable but walk already reached 40 before this position was needed |
| 84 | `slidev-theme-penguin-ht` | 39 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 85 | `slidev-theme-pixel` | 39 | ♦ coded | - |
| 86 | `@timdaik/slidev-theme-nutmeg` | 38 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 87 | `slidev-theme-wordman` | 38 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 88 | `slidev-theme-doctolib` | 38 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 89 | `@open-xchange/slidev-theme-ox` | 38 | excluded | codeable but walk already reached 40 before this position was needed |
| 90 | `slidev-theme-rich` | 38 | excluded | uncodeable - all README image hosts (images.jieyu.ai) fail DNS resolution |
| 91 | `slidev-theme-oqtopus` | 37 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 92 | `@ricoapon/slidev-theme-narrative` | 37 | ♦ coded | - |
| 93 | `@cxphoenix/slidev-theme-fhsh-isiphs-universal` | 37 | excluded | codeable but walk already reached 40 before this position was needed |
| 94 | `slidev-theme-4obsidian` | 35 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 95 | `slidev-theme-modern-tech` | 34 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 96 | `slidev-theme-cyberpunk-ide` | 33 | excluded | codeable but walk already reached 40 before this position was needed |
| 97 | `@mudssky/slidev-theme-default` | 32 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 98 | `slidev-theme-whu-landing` | 32 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 99 | `slidev-theme-bestony` | 31 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 100 | `slidev-theme-vatis` | 31 | excluded | codeable but walk already reached 40 before this position was needed |
| 101 | `@cxphoenix/slidev-theme-fhsh-aisp` | 31 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 102 | `slidev-theme-dfhi-isfates` | 30 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 103 | `slidev-theme-vibe` | 30 | excluded | codeable but walk already reached 40 before this position was needed |
| 104 | `slidev-theme-neat` | 29 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 105 | `slidev-theme-antfu-vite-conf-2023` | 29 | excluded | codeable but walk already reached 40 before this position was needed |
| 106 | `slidev-theme-penjj` | 28 | excluded | codeable but walk already reached 40 before this position was needed |
| 107 | `slidev-theme-kolaente-basic` | 28 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 108 | `slidev-theme-vuetiful-uno` | 28 | excluded | codeable but walk already reached 40 before this position was needed |
| 109 | `slidev-theme-swiss-ai-hub` | 28 | excluded | codeable but walk already reached 40 before this position was needed |
| 110 | `slidev-theme-hydra-conf` | 27 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 111 | `slidev-theme-bitnate` | 26 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 112 | `slidev-theme-generic` | 26 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 113 | `@openfeature/slidev-theme-open-feature` | 26 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 114 | `slidev-theme-arthistory` | 26 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 115 | `slidev-theme-underglow` | 25 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 116 | `slidev-theme-vatisbh` | 24 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 117 | `slidev-theme-ucas` | 24 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 118 | `slidev-theme-anny-theme` | 24 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 119 | `@inloopstudio/slidev-theme-inloopstudio` | 24 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 120 | `slidev-theme-watabegg` | 23 | ♦ coded | - |
| 121 | `slidev-theme-aneo` | 23 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 122 | `slidev-theme-ninja` | 23 | excluded | codeable but walk already reached 40 before this position was needed |
| 123 | `slidev-theme-shopee` | 23 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 124 | `slidev-theme-squircle` | 23 | excluded | codeable but walk already reached 40 before this position was needed |
| 125 | `slidev-theme-hatch-corporate` | 23 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 126 | `slidev-theme-hal` | 22 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 127 | `slidev-theme-bawue` | 22 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 128 | `slidev-theme-easy` | 22 | excluded | codeable but walk already reached 40 before this position was needed |
| 129 | `slidev-theme-storyblok` | 22 | excluded | codeable but walk already reached 40 before this position was needed |
| 130 | `slidev-theme-audioshake` | 22 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 131 | `slidev-theme-stordahl` | 21 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 132 | `slidev-theme-beta` | 21 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 133 | `slidev-theme-ventus` | 21 | excluded | codeable but walk already reached 40 before this position was needed |
| 134 | `slidev-theme-poli-usp` | 21 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 135 | `slidev-theme-vue-i23` | 21 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 136 | `@captainsafia/slidev-theme-sketchdeck` | 21 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 137 | `slidev-theme-monomi` | 20 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 138 | `slidev-theme-nisl` | 20 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 139 | `slidev-theme-spezi` | 20 | ♦ coded | - || 140 | `slidev-theme-dimsam` | 20 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 141 | `slidev-theme-andyjjrt` | 20 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 142 | `slidev-theme-orlando` | 20 | excluded | uncodeable - no non-badge preview image found in npm README, GitHub README, or sli.dev theme gallery |
| 143 | `slidev-theme-renuo` | 20 | ♦ coded | replaces improving-25 (82a C2/C6) |


### Coded table (40 items, deck page 1 = title slide (+ first content slide where a genuine one
was found and fetched))

Columns: identity = background, title-slide layout, heading, colour. Variant = rules/boxes, body,
density. Per 82a **C7**, when only a title-slide preview (or two title-slide colour/palette
variants) could be found — no genuine distinct content slide — `body` and/or `density` are recorded
as `unknown` rather than guessed; filling then falls back to the family default for that variant
(disclosed per row in the Notes table below). Admissible = §5 pass/fail with rule id(s); `A2` =
emoji; `A3` = gradient/texture/photo fill directly behind body text (82a **C8**: a flat opaque panel
placed over a photo is fine — only text set *directly* on the busy fill fails); `A5` = ≥3 identical
decorative icon/shape repeats. No item in this corpus triggered A1 (>3 typefaces), A4 (paint-swipe/
splatter), A6 (contrast — all sampled pairs were evidently far from the 3.5–5.5:1 sampling band per
82a **C9**, so eye judgement was used and disclosed as such, no `lib/color.contrast_ratio` sampling
was needed), A7 (Office-default-blue/indigo-purple-gradient sole accent), or the deck-specific C9
(dark/light body contrast) constraint.

| Pos | Package | dl/mo | background | title-layout | heading | colour | rules/boxes | body | density | Admissible |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | `slidev-theme-the-unnamed` | 1880 | image | full-bleed-image | sans | fill-blocks | none | sans | standard | no (A3) |
| 3 | `slidev-theme-penguin` | 1650 | dark | centered | sans | one-accent | rules | sans | airy | yes |
| 6 | `slidev-theme-light-icons` | 1372 | image | full-bleed-image | sans | one-accent | boxes | sans | airy | no (A3) |
| 7 | `slidev-theme-dracula` | 1358 | dark | left | sans | one-accent | boxes | sans | standard | yes |
| 9 | `slidev-theme-purplin` | 1096 | light | left | sans | one-accent | boxes | sans | airy | yes |
| 10 | `slidev-theme-geist` | 767 | light | left | sans | mono | boxes | sans | dense | no (A2) |
| 13 | `slidev-theme-alchemmist` | 681 | light | centered | serif | multi | boxes | serif | dense | yes |
| 16 | `slidev-theme-neversink` | 516 | light | left | sans | one-accent | boxes | sans | standard | yes |
| 17 | `slidev-theme-scholarly` | 503 | light | centered | serif | one-accent | none | unknown | unknown | yes |
| 18 | `slidev-theme-excalidraw` | 490 | light | centered | display | multi | boxes | display | airy | yes |
| 19 | `slidev-theme-tahta` | 456 | dark | left | serif | one-accent | boxes | sans | standard | yes |
| 23 | `slidev-theme-meetup` | 313 | light | left | sans | one-accent | none | sans | airy | yes |
| 25 | `slidev-theme-eloc` | 281 | light | centered | sans | mono | boxes | sans | airy | yes |
| 26 | `slidev-theme-unicorn` | 273 | dark | split | sans | one-accent | none | sans | dense | no (A2,A3) |
| 28 | `slidev-theme-frankfurt` | 243 | light | centered | sans | one-accent | boxes | sans | standard | yes |
| 29 | `slidev-theme-bestony2026` | 229 | dark | left | display | one-accent | none | sans | unknown | yes |
| 31 | `slidev-theme-mokkapps` | 222 | light | left | serif | one-accent | none | sans | standard | no (A2) |
| 32 | `slidev-theme-takahashi` | 206 | light | centered | sans | one-accent | none | unknown | unknown | yes |
| 35 | `slidev-theme-webhh` | 170 | light | left | sans | mono | none | sans | airy | yes |
| 36 | `slidev-theme-nord` | 155 | dark | centered | sans | multi | rules | unknown | unknown | yes |
| 37 | `slidev-theme-vuetiful` | 150 | dark | centered | sans | one-accent | rules | unknown | unknown | no (A5) |
| 41 | `slidev-theme-cobalt` | 124 | dark | centered | sans | mono | none | unknown | unknown | yes |
| 42 | `slidev-theme-excali-slide` | 123 | light | left | display | multi | boxes | display | dense | yes |
| 44 | `@carlory/slidev-theme-daocloud` | 111 | dark | split | sans | one-accent | none | unknown | unknown | no (A5) |
| 46 | `slidev-theme-hep` | 102 | image | left | sans | one-accent | none | sans | standard | no (A2,A3) |
| 48 | `slidev-theme-field-manual` | 98 | light | left | display | one-accent | boxes | unknown | unknown | no (A3) |
| 49 | `slidev-theme-ksick-dynatrace` | 86 | dark | left | sans | multi | none | sans | airy | no (A2) |
| 52 | `slidev-theme-noninsurance` | 79 | dark | left | display | one-accent | none | unknown | unknown | yes |
| 54 | `slidev-theme-touying` | 72 | light | centered | serif | one-accent | boxes | unknown | unknown | yes |
| 55 | `slidev-theme-enolive` | 71 | image | split | sans | one-accent | none | unknown | unknown | yes |
| 64 | `slidev-theme-datev-scc` | 55 | dark | centered | serif | multi | none | unknown | unknown | yes |
| 69 | `@ricoapon/slidev-theme-technical` | 48 | dark | left | mono | one-accent | rules | unknown | unknown | yes |
| 71 | `slidev-theme-dmml` | 47 | light | left | sans | multi | rules | unknown | unknown | yes |
| 73 | `slidev-theme-onecraft` | 47 | image | left | sans | multi | none | unknown | unknown | no (A3) |
| 79 | `slidev-theme-mint` | 42 | image | split | sans | mono | boxes | unknown | unknown | no (A3) |
| 85 | `slidev-theme-pixel` | 39 | image | centered | sans | one-accent | rules | unknown | unknown | no (A3) |
| 92 | `@ricoapon/slidev-theme-narrative` | 37 | light | left | mono | mono | rules | unknown | unknown | yes |
| 120 | `slidev-theme-watabegg` | 23 | light | centered | sans | mono | none | unknown | unknown | no (A3) |
| 139 | `slidev-theme-spezi` | 20 | dark | centered | sans | one-accent | none | sans | airy | yes |
| 143 | `slidev-theme-renuo` | 20 | light | left | sans | mono | none | sans | airy | no (A3) |

### Sources (repo + exact preview URL(s) fetched, per coded item)

| Pos | Package | Repo | Preview URL(s) fetched |
|---|---|---|---|
| 2 | `slidev-theme-the-unnamed` | https://github.com/estruyf/slidev-theme-the-unnamed | https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/cover.png; https://cdn.jsdelivr.net/gh/estruyf/slidev-theme-the-unnamed@main/assets/about-me.png |
| 3 | `slidev-theme-penguin` | https://github.com/alvarosaburido/slidev-theme-penguin | https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/dark/01.png; https://cdn.jsdelivr.net/gh/alvarosaburido/slidev-theme-penguin@master/screenshots/light/02.png |
| 6 | `slidev-theme-light-icons` | https://github.com/lightvue/slidev-theme-light-icons | https://cdn.jsdelivr.net/gh/lightvue/slidev-theme-light-icons@master/screenshot/1-layout-intro.png; https://cdn.jsdelivr.net/gh/lightvue/slidev-theme-light-icons@master/screenshot/2-layout-image-header-intro-light.png |
| 7 | `slidev-theme-dracula` | https://github.com/jd-solanki/slidev-theme-dracula | https://cdn.jsdelivr.net/gh/jd-solanki/slidev-theme-dracula/screenshots/screenshot-1.png; https://cdn.jsdelivr.net/gh/jd-solanki/slidev-theme-dracula/screenshots/screenshot-2.png |
| 9 | `slidev-theme-purplin` | https://github.com/moudev/slidev-theme-purplin | https://i.imgur.com/BX3TpEc.png; https://i.imgur.com/mqqRi1F.png |
| 10 | `slidev-theme-geist` | https://github.com/nico-bachner/slidev-theme-geist | https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/01.png; https://cdn.jsdelivr.net/gh/nico-bachner/slidev-theme-geist@main/example-export/02.png |
| 13 | `slidev-theme-alchemmist` | https://github.com/alchemmist/slidev-theme-alchemmist | https://github.com/user-attachments/assets/762bf0ba-5a52-4c59-ab52-1c37cf6edacd |
| 16 | `slidev-theme-neversink` | https://github.com/gureckis/slidev-theme-neversink | https://gureckis.github.io/slidev-theme-neversink/screenshots/2.png; https://gureckis.github.io/slidev-theme-neversink/screenshots/6.png |
| 17 | `slidev-theme-scholarly` | https://github.com/jxpeng98/slidev-theme-scholarly | https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/classic-blue/1.png; https://raw.githubusercontent.com/jxpeng98/slidev-theme-scholarly/HEAD/images/themes/oxford/1.png |
| 18 | `slidev-theme-excalidraw` | https://github.com/milon/slidev-theme-excalidraw | https://raw.githubusercontent.com/milon/slidev-theme-excalidraw/master/screenshots/cover.png; https://raw.githubusercontent.com/milon/slidev-theme-excalidraw/master/screenshots/sketchy-boxes.png |
| 19 | `slidev-theme-tahta` | https://github.com/zcag/tahta | https://cdn.jsdelivr.net/gh/zcag/tahta@1dd8357/docs/screenshots/01.png; https://cdn.jsdelivr.net/gh/zcag/tahta@1dd8357/docs/screenshots/02.png |
| 23 | `slidev-theme-meetup` | https://github.com/tboerger/slidev-theme-meetup | https://raw.githubusercontent.com/tboerger/slidev-theme-meetup/master/example-export/1.png; https://raw.githubusercontent.com/tboerger/slidev-theme-meetup/master/example-export/2.png |
| 25 | `slidev-theme-eloc` | https://github.com/zthxxx/slides/blob/master/packages/slidev-theme-eloc | https://media.githubusercontent.com/media/zthxxx/slides/refs/heads/master/packages/slidev-theme-eloc/screenshot/01.png; https://media.githubusercontent.com/media/zthxxx/slides/refs/heads/master/packages/slidev-theme-eloc/screenshot/02.png |
| 26 | `slidev-theme-unicorn` | https://github.com/Dawntraoz/slidev-theme-unicorn | https://cdn.jsdelivr.net/gh/Dawntraoz/slidev-theme-unicorn@master/screenshots/dark-theme-intro.png; https://cdn.jsdelivr.net/gh/Dawntraoz/slidev-theme-unicorn@master/screenshots/light-theme-cover.png |
| 28 | `slidev-theme-frankfurt` | https://github.com/MuTsunTsai/slidev-theme-frankfurt | https://cdn.jsdelivr.net/gh/MuTsunTsai/slidev-theme-frankfurt/screenshots/01.png; https://cdn.jsdelivr.net/gh/MuTsunTsai/slidev-theme-frankfurt/screenshots/04.png |
| 29 | `slidev-theme-bestony2026` | https://github.com/bestony/slidev-theme-bestony2026 | https://raw.githubusercontent.com/bestony/slidev-theme-bestony2026/main/assets/layouts/cover.png; https://raw.githubusercontent.com/bestony/slidev-theme-bestony2026/main/assets/layouts/intro.png |
| 31 | `slidev-theme-mokkapps` | https://github.com/mokkapps/slidev-theme-mokkapps | https://cdn.jsdelivr.net/gh/mokkapps/slidev-theme-mokkapps@master/screenshots/dark/001.png; https://cdn.jsdelivr.net/gh/mokkapps/slidev-theme-mokkapps@master/screenshots/dark/002.png |
| 32 | `slidev-theme-takahashi` | github:kecrily/slidev-theme-takahashi | https://cdn.jsdelivr.net/gh/kecrily/slidev-theme-takahashi@master/screenshots/01.png; https://cdn.jsdelivr.net/gh/kecrily/slidev-theme-takahashi@master/screenshots/02.png |
| 35 | `slidev-theme-webhh` | https://github.com/hoverbaum/slidev-theme-webhh | https://raw.githubusercontent.com/hoverbaum/slidev-theme-webhh/main/assets/layouts/title.png; https://raw.githubusercontent.com/hoverbaum/slidev-theme-webhh/main/assets/layouts/speaker.png |
| 36 | `slidev-theme-nord` | https://github.com/oller/slidev-theme-nord | https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/1.png; https://raw.githubusercontent.com/oller/slidev-theme-nord/HEAD/example-export/2.png |
| 37 | `slidev-theme-vuetiful` | https://github.com/linusborg/slidev-theme-vuetiful | https://cdn.jsdelivr.net/gh/LinusBorg/slidev-theme-vuetiful@main/screenshots/cover-alt.png; https://cdn.jsdelivr.net/gh/LinusBorg/slidev-theme-vuetiful@main/screenshots/section.png |
| 41 | `slidev-theme-cobalt` | https://github.com/minagishl/slidev-theme-cobalt | https://raw.githubusercontent.com/minagishl/slidev-theme-cobalt/main/screenshots/cover.png; https://raw.githubusercontent.com/minagishl/slidev-theme-cobalt/main/screenshots/title-center.png |
| 42 | `slidev-theme-excali-slide` | https://github.com/filiphric/slidev-theme-excali-slide | https://raw.githubusercontent.com/filiphric/excali-slide/main/images/default_slide.png; https://raw.githubusercontent.com/filiphric/excali-slide/main/images/intro_slide.png |
| 44 | `@carlory/slidev-theme-daocloud` | https://github.com/carlory/slidev-theme-daocloud | https://raw.githubusercontent.com/carlory/slidev-theme-daocloud/main/docs/previews/cover.png; https://raw.githubusercontent.com/carlory/slidev-theme-daocloud/main/docs/previews/intro.png |
| 46 | `slidev-theme-hep` | https://github.com/AvencastF/slidev-theme-hep | https://cdn.jsdelivr.net/gh/avencastf/slidev-theme-hep/screenshot/001.png; https://cdn.jsdelivr.net/gh/avencastf/slidev-theme-hep/screenshot/004.png |
| 48 | `slidev-theme-field-manual` | https://github.com/pjdoland/slidev-theme-field-manual | https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/1.jpg; https://raw.githubusercontent.com/pjdoland/slidev-theme-field-manual/main/screenshots/2.jpg |
| 49 | `slidev-theme-ksick-dynatrace` | https://github.com/KatharinaSick/slidev-theme-ksick-dynatrace | https://raw.githubusercontent.com/KatharinaSick/slidev-theme-ksick-dynatrace/main/screenshots/footer.png; https://raw.githubusercontent.com/KatharinaSick/slidev-theme-ksick-dynatrace/main/screenshots/about.png |
| 52 | `slidev-theme-noninsurance` | https://github.com/alili/slidev-theme-noninsurance | https://raw.githubusercontent.com/alili/slidev-theme-noninsurance/main/assets/layouts/cover.png; https://raw.githubusercontent.com/alili/slidev-theme-noninsurance/main/assets/layouts/intro.png |
| 54 | `slidev-theme-touying` | https://github.com/kermanx/slidev-theme-touying | https://github.com/user-attachments/assets/a075a45c-7ee7-4ede-b3e7-90f29edf3845; https://github.com/user-attachments/assets/5ddea6cb-e604-41f9-a857-9f43b439c91b |
| 55 | `slidev-theme-enolive` | https://github.com/enolive/slidev-theme-enolive | https://raw.githubusercontent.com/enolive/slidev-theme-enolive/main/demo/0.png; https://raw.githubusercontent.com/enolive/slidev-theme-enolive/main/demo/3.png |
| 64 | `slidev-theme-datev-scc` | https://github.com/enolive/slidev-theme-datev-scc | https://raw.githubusercontent.com/enolive/slidev-theme-datev-scc/main/screenshots/intro.png; https://raw.githubusercontent.com/enolive/slidev-theme-datev-scc/main/screenshots/code.png |
| 69 | `@ricoapon/slidev-theme-technical` | https://github.com/ricoapon/slidev-theme-technical | https://raw.githubusercontent.com/ricoapon/slidev-theme-technical/main/screenshots/cover.png; https://raw.githubusercontent.com/ricoapon/slidev-theme-technical/main/screenshots/section.png |
| 71 | `slidev-theme-dmml` | https://github.com/Shu-Wan/slidev-theme-dmml | https://raw.githubusercontent.com/Shu-Wan/slidev-theme-dmml/main/screenshots/01-cover.png; https://raw.githubusercontent.com/Shu-Wan/slidev-theme-dmml/main/screenshots/02-intro.png |
| 73 | `slidev-theme-onecraft` | https://github.com/spawnrider/slidev-theme-onecraft | https://raw.githubusercontent.com/spawnrider/slidev-theme-onecraft/master/example-export/1.png; https://raw.githubusercontent.com/spawnrider/slidev-theme-onecraft/master/example-export/20.png |
| 79 | `slidev-theme-mint` | https://github.com/alfatta/slidev-theme-mint | https://raw.githubusercontent.com/alfatta/slidev-theme-mint/main/screenshot/1.png; https://raw.githubusercontent.com/alfatta/slidev-theme-mint/main/screenshot/2.png |
| 85 | `slidev-theme-pixel` | https://github.com/romanoe/slidev-theme-pixel | https://raw.githubusercontent.com/romanoe/slidev-theme-pixel/main/screenshots/cover.png; https://raw.githubusercontent.com/romanoe/slidev-theme-pixel/main/screenshots/cover-dark.png |
| 92 | `@ricoapon/slidev-theme-narrative` | https://github.com/ricoapon/slidev-theme-narrative | https://raw.githubusercontent.com/ricoapon/slidev-theme-narrative/main/screenshots/cover.png; https://raw.githubusercontent.com/ricoapon/slidev-theme-narrative/main/screenshots/statement.png |
| 120 | `slidev-theme-watabegg` | https://github.com/watabegg/slidev-theme-watabegg | https://raw.githubusercontent.com/watabegg/slidev-theme-watabegg/refs/heads/main/example/0.png; https://raw.githubusercontent.com/watabegg/slidev-theme-watabegg/refs/heads/main/example/1.png |
| 139 | `slidev-theme-spezi` | (unresolved) | https://raw.githubusercontent.com/zzzFelix/slidev-theme-spezi/main/example-slides/001.png; https://raw.githubusercontent.com/zzzFelix/slidev-theme-spezi/main/example-slides/002.png |
| 143 | `slidev-theme-renuo` | https://github.com/renuo/slidev-theme-renuo | https://raw.githubusercontent.com/renuo/renuo-slidev-theme/main/screenshots/cover.png; https://raw.githubusercontent.com/renuo/renuo-slidev-theme/main/screenshots/intro.png |
### Per-item disclosures (Notes)

Rows not listed here had no special disclosure (a genuine title + content slide pair was found and
fetched, coded normally).

| Pos | Package | Note |
|---|---|---|
| 2 | `slidev-theme-the-unnamed` | textured photo fill directly behind title text (title slide itself) |
| 6 | `slidev-theme-light-icons` | mountain photo fill directly behind 'LIGHT ICONS' title text |
| 10 | `slidev-theme-geist` | emoji bullets on content slide (paper/palette/robot/etc icons) |
| 13 | `slidev-theme-alchemmist` | single compiled montage image (multiple slides overlapping); identity/variant read off the clearest visible slides, disclosed low-confidence |
| 17 | `slidev-theme-scholarly` | both available images are title-slide palette variants (Classic Academic Blue / Oxford Burgundy); no content slide found -> body/density unknown per 82a C7 |
| 26 | `slidev-theme-unicorn` | emoji bullets on content slide; solid purple gradient fill directly behind title/subtitle text |
| 29 | `slidev-theme-bestony2026` | only title-slide-style image verified for content (Chinese-text deck); density unknown per C7 - second image is a similarly title-styled intro slide, not distinct body content |
| 31 | `slidev-theme-mokkapps` | flag/twitter emoji in content-slide bio bullets |
| 32 | `slidev-theme-takahashi` | only the single-word title-style slide was verified (Takahashi method: giant word-only slides); second gallery image not fetched -> density/body unknown per C7 |
| 36 | `slidev-theme-nord` | only the title slide was fetched/verified; no content slide -> body/density unknown per C7 |
| 37 | `slidev-theme-vuetiful` | Vue logo icon repeated 9x as decorative pattern (>=3 identical decorative icon repeats); body/density unknown, only title slide verified |
| 41 | `slidev-theme-cobalt` | only title slide verified; body/density unknown per C7 |
| 42 | `slidev-theme-excali-slide` | title slide = 'Slidev Theme Starter' (yellow-highlighter hand-drawn heading); colour/rules/density read from combined title+content evidence per §4 |
| 44 | `@carlory/slidev-theme-daocloud` | nested hexagon-outline tunnel graphic repeats the same outline shape >=3 times as decoration; body/density unknown, only title slide verified |
| 46 | `slidev-theme-hep` | emoji present ('Don't explicitly put title on cover page' with emoji); faint industrial-photo fill directly behind title/body text |
| 48 | `slidev-theme-field-manual` | visible paper-grain texture fill directly behind title text; only title slide verified, body/density unknown per C7 |
| 49 | `slidev-theme-ksick-dynatrace` | rocket/link emoji in content-slide bio line |
| 52 | `slidev-theme-noninsurance` | only title slide verified (near-identical layout to bestony2026, independent repo/author); body/density unknown per C7 |
| 54 | `slidev-theme-touying` | only title slide (name-card style) verified; body/density unknown per C7 |
| 55 | `slidev-theme-enolive` | photo occupies right half of title slide but text sits on the solid dark left half (not over the photo, admissible per C8); only title slide verified, body/density unknown per C7 |
| 64 | `slidev-theme-datev-scc` | only title slide verified; body/density unknown per C7 |
| 69 | `@ricoapon/slidev-theme-technical` | only title slide verified; body/density unknown per C7 |
| 71 | `slidev-theme-dmml` | only title slide verified; body/density unknown per C7 |
| 73 | `slidev-theme-onecraft` | blurred code-on-screen photo fill directly behind title/subtitle text; only title slide verified |
| 79 | `slidev-theme-mint` | gradient fill directly behind title/subtitle text (right side, away from the framed photo); only title slide verified |
| 85 | `slidev-theme-pixel` | night-mountain photo fill directly behind bold heading text; both fetched images are title-slide colour variants (light/dark), no content slide -> body/density unknown per C7 |
| 92 | `@ricoapon/slidev-theme-narrative` | only a placeholder title slide ('Title'/'Subtitle', ORG A/ORG B labels) verified; body/density unknown per C7 |
| 120 | `slidev-theme-watabegg` | blue gradient fill directly behind heading/subtitle text; only title slide verified |
| 143 | `slidev-theme-renuo` | faint repeating dash-pattern texture fill directly behind title text (replaces improving-25, which had only a non-title content slide with no usable identity evidence) |

### Admissibility summary (§5, as clarified by 82a C8)

15 of 40 coded items (37.5%) are inadmissible:

- **A3** (gradient/texture/photo fill directly behind body text, per 82a C8's literal "text set
  directly on a gradient, texture, or photo" — not merely a busy background somewhere on the slide):
  `the-unnamed`(2, textured photo), `light-icons`(6, mountain photo), `unicorn`(26, purple gradient),
  `hep`(46, faint industrial photo), `field-manual`(48, paper-grain texture), `onecraft`(73, blurred
  code photo), `mint`(79, gradient), `pixel`(85, night-mountain photo), `watabegg`(120, blue
  gradient), `renuo`(143, dash-pattern texture) — 10 items. This is the dominant fail reason, and it
  falls almost entirely on "hero photo/gradient behind the headline" title-slide designs — a very
  common convention-deck pattern that this rubric treats as a slop tell regardless of execution
  quality (per research/68's "gradient/texture" and "photo-behind-text" patterns).
- **A2** (emoji): `geist`(10, palette/robot/etc. emoji bullets), `unicorn`(26, emoji bullets — also
  A3), `mokkapps`(31, flag/twitter emoji in bio line), `hep`(46, emoji in body text — also A3),
  `ksick-dynatrace`(49, rocket/link emoji in bio line) — 5 items, found only on the *content* slide
  in 4 of 5 cases (the title slide alone would have looked admissible), consistent with 82a's
  reminder that page 1 covers both slides.
- **A5** (≥3 identical decorative icon/shape repeats): `vuetiful`(37, the Vue.js triangle logo
  repeated 9 times as a scattered decorative pattern top and bottom of the title slide), `daocloud`
  (44, the same hexagon-ring outline repeated ~8 times as a nested "tunnel" decorative graphic).

25 of 40 (62.5%) are admissible. **Coarsening check (§4):** of the 25 admissible items, 14 sit in
singleton archetypes (56% > 50%) but exactly **5** archetypes have k≥2 — the trigger requires
*fewer than* 5, so at 5 exactly **no coarsening** is applied; the 4th identity feature (title-slide
layout) is kept.

### Frequency table (k/40, admissible items only; inadmissible items' archetypes are not counted
per §6 but are listed in the coded table above with their rule id)

| Archetype (`background|heading|colour|title-layout`) | k/40 | share | items (pos) |
|---|---|---|---|
| `light|sans|one-accent|left` | 3/40 | 0.075 | purplin(9), neversink(16), meetup(23) |
| `dark|sans|one-accent|centered` | 2/40 | 0.050 | penguin(3), spezi(139) |
| `light|serif|one-accent|centered` | 2/40 | 0.050 | scholarly(17), touying(54) |
| `light|sans|one-accent|centered` | 2/40 | 0.050 | frankfurt(28), takahashi(32) |
| `dark|display|one-accent|left` | 2/40 | 0.050 | bestony2026(29), noninsurance(52) |
| `dark|sans|one-accent|left` | 1/40 | 0.025 | dracula(7) |
| `light|serif|multi|centered` | 1/40 | 0.025 | alchemmist(13) |
| `light|display|multi|centered` | 1/40 | 0.025 | excalidraw(18) |
| `dark|serif|one-accent|left` | 1/40 | 0.025 | tahta(19) |
| `light|sans|mono|centered` | 1/40 | 0.025 | eloc(25) |
| `light|sans|mono|left` | 1/40 | 0.025 | webhh(35) |
| `dark|sans|multi|centered` | 1/40 | 0.025 | nord(36) |
| `dark|sans|mono|centered` | 1/40 | 0.025 | cobalt(41) |
| `light|display|multi|left` | 1/40 | 0.025 | excali-slide(42) |
| `image|sans|one-accent|split` | 1/40 | 0.025 | enolive(55) |
| `dark|serif|multi|centered` | 1/40 | 0.025 | datev-scc(64) |
| `dark|mono|one-accent|left` | 1/40 | 0.025 | technical(69) |
| `light|sans|multi|left` | 1/40 | 0.025 | dmml(71) |
| `light|mono|mono|left` | 1/40 | 0.025 | narrative(92) |

19 distinct archetypes over the 25 admissible items (25 total admissible, 15 inadmissible, 40 coded
overall). Ranking Metric string for every admissible row: `share:NPM:k/40 by downloads.monthly`.
Top archetype `light|sans|one-accent|left` at 3/40 (0.075) — a light background, sans-serif heading,
single accent colour, left-aligned title, no other decoration: the plain "developer default" look.

### Bias statement

- **Search is relevance-ranked, not a name enumeration**, same caveat as the cv corpus: `size=250`
  is npm's per-call max; the index's own `total` (87,769) is the whole text-match universe, of which
  only 225 objects on this one page matched the exact `slidev-theme-*` name filter. Slidev's own
  official theme gallery (`@slidev/theme-default`, `theme-seriph`, `theme-apple-basic`, etc., scoped
  under `@slidev/` not `slidev-theme-`) is entirely absent from this corpus by construction — the
  name filter is the one research/82 §10 specifies (`slidev-theme-*`), so official first-party themes
  are out of scope for this corpus, not merely under-ranked.
- **Population skew.** Slidev itself is a developer-only tool (Markdown + Vue + Vite); every author
  in this corpus is a developer writing for other developers or for their own conference/meetup/
  lab/employer talk. The corpus is saturated with "insider" themes built once for a specific talk or
  employer and published to npm mostly so the author's own CI/build could `npm i` it — many of the
  highest-download items (`ehl2022`, `hep`, `dmml`, `noninsurance`, `bestony2026`) are named after a
  specific event, lab, or company, not designed as general-purpose products. English is not
  universal: Chinese (`bestony2026`, `noninsurance`, both walked at similar downloads with a shared
  visual archetype), German (`webhh`, `datev-scc`, `spezi`), and Japanese (`watabegg`) titles/UI text
  all appear in the top 40.
- **Download counts reward CI/test installs and one popular monorepo, not human choice at scale.**
  The single highest-download item in the entire 225-name list, `ehl2022` (8,652/mo — nearly 5×
  the #2 item), turned out to be **uncodeable**: its README is a Chinese-language step-by-step
  install tutorial with no design preview at all, strongly suggesting its download count is driven
  by a course/cohort repeatedly running `npm install` rather than by design popularity — exactly the
  kind of number research/82 §13 warns "popularity is not quality" about, now with a concrete
  example.
- **A3 (gradient/texture/photo-behind-text) removes a disproportionate share of the highest-
  download items.** 5 of the top 10 by downloads (`the-unnamed`#2, `light-icons`#6, `geist`#10 via
  A2, `unicorn`#15 via A2+A3) are inadmissible, vs. a lower rate further down the list — so the
  admissible pool's *shape* skews toward mid-tier packages relative to raw popularity, same pattern
  observed in the cv corpus with C1.
- **Every walked item this session is a solo/community theme; none is a corporate design-system
  export** in the sense of a governed brand system — even the company-named ones (`onecraft`/
  Capgemini, `daocloud`, `mistica`/Telefonica, seen further down the walk) are individual employees'
  side-project themes referencing their employer's brand loosely, not an official design-system
  package maintained by a design team.

### Second-coder sample

Per 82a **C10**, the second-coder sample must be **family-wide** (all coded ids of the deck family
across *both* corpora — this NPM corpus and the sibling LO-Impress/MS-presentations corpus coded by
the other split-task worker — sorted together, then the seeded draw). This file's worker does not
have the sibling corpus's id list, so the sample below is **informational/per-corpus only** and is
**superseded** by the orchestrator's family-wide draw once both corpora's id lists are combined:

ids = `NPM:<position zero-padded to 3>` for this corpus's 40 coded ids, sorted lexicographically,
sampled with `random.Random("82:deck").sample(ids, max(min(10,len(ids)), math.ceil(0.25*len(ids))))`
→ n=10 (informational only, not the binding sample):

`NPM:018` (excalidraw), `NPM:019` (tahta), `NPM:025` (eloc), `NPM:026` (unicorn), `NPM:032`
(takahashi), `NPM:037` (vuetiful), `NPM:046` (hep), `NPM:049` (ksick-dynatrace), `NPM:092`
(narrative), `NPM:120` (watabegg).

The orchestrator should recompute with `random.Random("82:deck")` over the *combined* sorted id list
from both deck corpora before dispatching to the second coder; per §7 the second coder receives only
§4–§5 of research/82 plus, for the sampled ids, the package name + repo URL + preview URL(s) from the
Sources table above (no codes, no admissibility calls from this file).


## Report / protocol ambiguities met in practice

- **Counts:** 40 coded (25 admissible / 15 inadmissible), 103 excluded (102 uncodeable across a
  mechanically-applied blocklist + individually-diagnosed dead-path/DNS/format cases, 1 swapped out
  post-hoc as uncodeable-for-identity per 82a C2/C7), 225 on-topic-by-exact-name candidates from a
  250-object relevance page over an index of 87,769 text matches. Walk reached native position 143.
- **Frequency table:** 19 distinct archetypes over 25 admissible items; top archetype
  `light|sans|one-accent|left` at 3/40 (0.075); exactly 5 archetypes reach k≥2 (coarsening not
  triggered, see admissibility summary).
- **Exclusions:** 103 total (see raw list); the top-ranked item overall (`ehl2022`, 8,652 dl/mo) is
  among them (uncodeable — no design preview, only an install tutorial).
- **Ambiguities encountered, beyond what 82a already resolved:**
  1. The protocol's `NPM(t)` URL (`size=250`) returns npm's *relevance* ranking, not a
     `downloads.monthly` ranking — the walk re-sorts the 250 returned objects by the
     `downloads.monthly` field already present in each object (no separate bulk-downloads call was
     needed, unlike the cv-corpus task's `api.npmjs.org/downloads/point/...` fallback — this
     endpoint's search payload already had the metric). Disclosed since research/82 §10 only gives
     the URL, not which field to sort by when the payload carries more than one.
  2. §3's "Codeable iff a preview exists... README image" doesn't say what to do when npm's own
     mirrored README is stale (older than the GitHub repo's current README) or absent entirely for a
     scoped/monorepo package (`@sp-days-framework/...`, `zthxxx/slides` monorepo). Resolved by always
     also checking the live GitHub README/gallery before ruling an item uncodeable, per 82a C6's
     "replace a dead documented path with the item's own published preview" — applied even before an
     item's *declared* path had 404'd, since for several packages npm's README simply had 0 images
     while GitHub's had several.
  3. Two independently-run themes (`bestony2026`, `noninsurance`) coded to visually near-identical
     archetypes despite being different repos/owners with no declared relationship and no shared
     asset URL — per §3.2's literal fork/duplicate test (exact-asset-URL or declared-fork-name match
     only) these do **not** qualify as duplicates and were coded independently; their shared
     archetype is legitimate popularity signal, not double-counting, and is disclosed rather than
     silently merged or silently left unremarked.
  4. Two items had a *second* npm README image that was itself a title-slide colour/palette variant
     rather than a distinct content slide (`scholarly`'s "Classic Academic Blue" vs. "Oxford
     Burgundy" variants; `pixel`'s light vs. dark cover). Per 82a **C7** these are treated the same
     as a single-title-slide-only preview: `body`/`density` recorded as `unknown`, not guessed from
     a second title-style image.
  5. One item (`hep`) needed the GitHub *contents* API (`api.github.com/repos/<owner>/<repo>/
     contents/<path>`) to confirm a declared screenshot directory no longer existed at the current
     default branch before it could be logged as uncodeable-by-dead-path — this is a per-repo content
     read, not the GitHub *search* API, so it does not touch the reserved rate limit; used sparingly
     (a handful of times across the whole task) and disclosed here for transparency.
  6. A6 (contrast) was never mechanically sampled: every admissible item's text/background pairing
     was evidently far outside the 3.5–5.5:1 ambiguous band by eye (either near-black-on-white/pale
     or near-white-on-near-black), so per 82a **C9** no `lib/color.contrast_ratio` run was triggered;
     disclosed as an eye-judgement pass with nothing found, not a skipped check.

## Library snapshot

No `research/library/*` or `skill/document-design-intelligence/data/base/*` files were modified by
this task (coding only, per F.a). `skill/document-design-intelligence/data/base/constraints.csv` was
read to confirm this family has no deck-specific constraint rows beyond the `projection`/
`slop-mechanical` sets already covered by the universal A1–A8 admissibility rules cited above (no
deck-only constraint id was needed beyond the C9 dark/light-contrast-margin note, which did not
trigger for any item in this corpus).
