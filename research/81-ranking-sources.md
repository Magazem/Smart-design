# research/81 — Ranking-source fetchability probe (P2.1)

Frozen scope: research/80 §3. Discipline per R-d: researchers count, they do not judge. This
document only records what a fetched (or, where marked, search-corroborated) copy of each
candidate source actually exposes — no source is cited as "best," only as "carries metric X with
values Y." Retrieved date for every row below: 2026-09-23, unless noted otherwise.

Legend — Fetchable: **yes** (WebFetch returned the real structured content), **partial** (page
fetched but the specific metric/list was not in the static payload — description/nav only),
**no** (blocked: 403/404/redirect-loop/empty JS shell). Fetch column in the provenance sense:
**fetched** = WebFetch returned the actual numeric/structured payload; **search-corroborated** =
WebFetch failed or returned no metric, and a WebSearch snippet supplied a value instead (never
promoted to a numeric Rank Value per research/80 §2C).

## Typefaces

| Source | Artefact | URL probed | Fetchable? | Metric exposed | Numeric values visible? | Machine endpoint | ToS/robots note | Fetch |
|---|---|---|---|---|---|---|---|---|
| Google Fonts (sort=popularity) | typeface | `https://fonts.google.com/?sort=popularity` | no — Angular SPA, static fetch returns only `<title>Browse Fonts - Google Fonts</title>`, no font list in payload | "popularity order" (intended) | no (client renders it) | — | none observed | search-corroborated only for the concept; no metric captured |
| Google Fonts metadata API | typeface | `https://fonts.google.com/metadata/fonts` | **yes** | `popularity` (int rank) and `trending` (int) fields, plus `defaultSort` | **yes** — numeric `popularity`/`trending` per family entry | this endpoint IS the JSON API | undocumented/unofficial but publicly served, no auth, no robots block found | fetched |
| Google Fonts analytics page | typeface | `https://fonts.google.com/analytics` | no — static fetch returns only page `<title>`, chart data is client-rendered | "usage over time" (intended) | no | none found (analytics numbers appear bundled into the same metadata/webfont delivery pipeline, not a separate open endpoint) | none observed | not usable; superseded by metadata/fonts popularity field |
| jsDelivr package stats API (@fontsource) | typeface | `https://data.jsdelivr.com/v1/stats/packages/npm/@fontsource/inter` | **yes** | CDN "hits" (download-equivalent requests) and bandwidth, with overall/type rank and prior-period comparison | **yes** — total hits 230,702,705 in tracked window; daily 6.9–8.3M; bandwidth 4.68 Tbytes | same URL is the API | public, unauthenticated, documented at jsdelivr.com | fetched |
| npm downloads API | typeface | `https://api.npmjs.org/downloads/point/last-month/@fontsource/inter` | **yes** | last-month download count | **yes** — `{"downloads":10515443,"start":"2026-08-23","end":"2026-09-21"}` | is itself the API | official npm registry API, public | fetched |
| Typewolf "Most Popular Fonts" | typeface | `https://www.typewolf.com/most-popular-fonts` (probed) then `https://www.typewolf.com/recommendations` (worked) | partial — the `/most-popular-fonts` path 404s; `/recommendations` fetched fine | "based on popularity data from over 3,000 sites featured on Typewolf" — ordinal rank only | ordinal rank yes (1–10), no counts/votes | none | no API; scraping not clearly disallowed but no robots check performed | fetched (for `/recommendations`; the exact `/most-popular-fonts` URL is dead — use `/recommendations`) |
| Fontshare | typeface | `https://www.fontshare.com/fonts` | partial — static fetch returned only page `<title>`, no catalog/sort UI in payload | none found; WebSearch corroborates no ranking metric exists site-side (only third-party "most popular Fontshare font" blog opinions naming Satoshi/Clash Display/Boska) | no | none | n/a | search-corroborated, and the search itself found no structured metric — Fontshare is **not admissible** as a ranked source |
| Adobe Fonts (sort=popular) | typeface | `https://fonts.adobe.com/fonts?sort=popular` | no — AngularJS shell, static fetch shows only "Scanning file — please wait" placeholder, no fonts/metric rendered | "popular" order (intended) | no | none found | none observed | not usable without JS execution |

## Pairings

No dedicated ranked API found for pairings; treat as authority/editorial, not ranked:
- Google Fonts Knowledge / publisher "recommended companion" pages and Typewolf's per-post
  pairing suggestions are prose, not a ranked list with a metric. Not separately re-probed here
  (out of scope for a metric fetch — they are cited, if used, as authority/convention, never as
  "ranked").

## Palettes

| Source | Artefact | URL probed | Fetchable? | Metric exposed | Numeric values visible? | Machine endpoint | ToS/robots note | Fetch |
|---|---|---|---|---|---|---|---|---|
| Coolors "Trending" | palette | `https://www.coolors.co/palettes/trending` | partial — static shell present (nav, modals, filters) but the fetch returned "No palettes found," i.e. results themselves are injected client-side/via API not visible to a plain fetch | "trending" (intended) — like-counts described in Coolors' own UI copy, not observed in payload | no | Coolors has an internal API but no public documented one found in this probe | none observed | not usable as-is; would need an authenticated/JS-executing fetch |
| Color Hunt "Popular" | palette | `https://colorhunt.co/palettes/popular` | partial — static shell (nav, filter tags, "Popular"/"New"/"Random" sort control, tagline "The community's favorite color palettes") but no swatches/hex/like-counts in the fetched payload | like-count ("Popular" sort) — intended, not captured | no | none found | none observed | not usable as-is |
| Adobe Color "Explore — Most Popular" | palette | `https://color.adobe.com/explore?filter=most-popular` | no — fetch resolved to the general Adobe Express marketing/FAQ page, not the Color CC explore app; no themes or metrics present | "most popular" (intended) | no | none found | none observed | not usable |
| USWDS color tokens | palette (authority) | `https://designsystem.digital.gov/design-tokens/color/overview/` (overview, partial) then `https://designsystem.digital.gov/design-tokens/color/theme-tokens/` (**worked**) | **yes** on the theme-tokens page | authority (published design-system token table, not a popularity metric) | **yes** — e.g. `primary`→`blue-60v`→`#005ea2`, `secondary`→`red-50`→`#d83933`, `accent-cool`→`cyan-30v`→`#00bde3`, `accent-warm`→`orange-30v`→`#fa9441`, `base-lightest`→`gray-5`→`#f0f0f0` | none needed; static doc site | US federal, public domain doc | fetched |
| GOV.UK Design System colour | palette (authority) | `https://design-system.service.gov.uk/styles/colour/` | **yes** | authority (published system) | **yes** — functional: text `#0b0c0c`, link `#1a65a6`, error `#ca3535`, success `#0f7a52`; web palette: blue primary `#1d70b8`, green primary `#0f7a52`, red primary `#ca3535`, yellow primary `#ffdd00` | none needed | Crown/OGL, reuse permitted | fetched |
| IBM Carbon color tokens | palette (authority) | `https://carbondesignsystem.com/elements/color/overview/` and `.../elements/color/tokens/` | no — both fetches returned truncated/empty payload (page too large or JS-hydrated); metric obtained only via WebSearch synthesis | authority (published tokens) | values reported by search only: e.g. Interactive/Blue 60 `#0f62fe`, Text Primary/Gray 100 `#161616`, Background `#ffffff`, Layer 01/Gray 10 `#f4f4f4`, Border Subtle/Gray 20 `#e0e0e0` | GitHub source `@carbon/themes` package (not fetched directly here) | Apache-2.0 repo | search-corroborated, not fetched |
| Material 3 baseline color | palette (authority) | `https://m3.material.io/styles/color/system/overview` and `.../styles/color/roles` | no — both returned only page `<title>`, tables are client-rendered | authority | values from search only: 13 tonal stops per hue (0–100), e.g. primary tokens `#000000…#21005d…#6750a4…#d0bcff…#ffffff`; 26 color roles across 6 groups | m3.material.io publishes a token-export tool, not probed here | Google, public docs | search-corroborated, not fetched |
| Fluent 2 color tokens | palette (authority) | `https://fluent2.microsoft.design/color` | partial — page fetched, describes the two-layer (global/alias) token model in prose but does not render the actual token table (linked out to Storybook/"Design tokens" page) | authority | no hex values captured in fetch or in follow-up search (search only re-described the token architecture, not values) | `fluent2.microsoft.design/color-tokens`, Storybook (not fetched) | Microsoft, public docs | partial fetch; not usable for values without a further hop |
| Atlassian design tokens (color) | palette (authority) | `https://atlassian.design/foundations/color-new` | no — fetch returned empty content (JS-rendered) | authority | one value found via search: `color.background.information` = `#082145` (dark) / `#E9F2FF` (light); full table lives at `atlassian.design/components/tokens/all-tokens`, not fetched | atlassian.design (not confirmed to expose a JSON export) | Atlassian, public docs | search-corroborated, not fetched |

## Type scales

| Source | Artefact | URL probed | Fetchable? | Metric exposed | Numeric values visible? | Machine endpoint | ToS/robots note | Fetch |
|---|---|---|---|---|---|---|---|---|
| modularscale.com | named ratio scale | `https://www.modularscale.com/` | **yes** | named ratio catalog (not popularity — a reference list) | **yes** — minor second 15:16 (1.067), minor third 5:6 (1.2), major third 4:5 (1.25), perfect fourth 3:4 (1.333), perfect fifth 2:3 (1.5), golden section 1:1.618 (1.618); values are embedded in static markup, not purely JS-computed | none (client-side calculator only) | none observed | fetched |

## Layout archetypes / templates

| Source | Artefact | URL probed | Fetchable? | Metric exposed | Numeric values visible? | Machine endpoint | ToS/robots note | Fetch |
|---|---|---|---|---|---|---|---|---|
| Microsoft Create (resumes) | layout templates | `https://create.microsoft.com/en-us/templates/resumes` → 301 → `https://word.cloud.microsoft/create/en/resume-templates/?source=create_flow` | **yes** (after following the redirect) | none — templates are grouped by job category (nurse, accountant, teacher, attorney, …), **no popularity sort or count visible** in the fetched payload | no | none found | Microsoft, public marketing pages | fetched, but carries no ranking metric — not admissible as "ranked," only as a template inventory |
| Google Docs template gallery | layout templates | `https://docs.google.com/document/u/0/?ftv=1&tgif=d` → redirected to marketing page; `https://docs.google.com/templates?category=resumes` → redirected to a Google login wall | no — both attempts hit redirects (marketing page / `accounts.google.com` sign-in wall), no template list or metric reachable unauthenticated | none reachable | no | none | requires a signed-in Google session; not fetchable anonymously | not usable |
| Canva templates (popular) | layout templates | `https://www.canva.com/templates/?query=resume` | no — HTTP 403 | "popular"/uses count (intended, per Canva marketing copy) | no | none found (no public Canva template API located via search) | 403 suggests bot-blocking | search-corroborated only that Canva markets "hundreds of ... templates," no metric obtained |
| Envato Elements (sort=popular) | layout templates | `https://elements.envato.com/graphic-templates/resume?sort=popular` and `.../resume-cv?sort=popular` | **yes**, page loads | sort control shows "Relevant" as the applied default regardless of the `sort=popular` query param — the popularity sort did not visibly take effect in the static fetch; no sales/favorites counts rendered per item | no | none found | Envato, public marketplace | fetched but the requested metric (popularity) was not actually exposed in the returned list — item titles only |
| Behance (search sort=appreciations) | layout templates / juried-adjacent inspiration | `https://www.behance.net/search/projects?search=resume&sort=appreciations` | no — HTTP 403 | "appreciations" (likes) — intended | no | Official Behance API exists (`api.behance.net/v2/projects?q=...`) and documents an `appreciations` field, but per search results **Behance explicitly excludes sort/category/country filters from crawler/API access** | search-corroborated: metric exists in the API schema but sort-by-appreciations is not obtainable per Behance's own crawler policy |
| Dribbble (popular shots) | layout templates / inspiration | `https://dribbble.com/shots/popular/resume` | no — fetch returned empty content | "likes_count" (via API v2, per search) | no | Dribbble API v2 (`developer.dribbble.com/v2/shots/`) documents `likes_count`, `views_count`, `comments_count`, `rebounds_count`, and a "popular" list mode, but requires OAuth; not fetched here | requires API key/OAuth | search-corroborated: metric exists but needs authenticated API access, not plain WebFetch |

## Juried awards

| Source | Artefact | URL probed | Fetchable? | Metric exposed | Numeric values visible? | Machine endpoint | ToS/robots note | Fetch |
|---|---|---|---|---|---|---|---|---|
| ARC Awards (annual reports) | juried | mercommawards.com/arc category-winner pages (via search; not directly WebFetched) | partial — WebSearch surfaced live category pages (Interactive/Traditional/PDF/Summary Annual Report, Written Text, etc.) | juried award (named winner + category + year) | yes, per search: 2025 Best of Show = Abbott, "2024: Delivering Now, Designing What's Next"; category URLs are real and enumerable | none | mercommawards.com, public awards site | search-corroborated; a direct WebFetch of a specific category-winner page was not attempted in this probe and should be done at protocol-freeze time (research/82) |
| Mercury Excellence Awards | juried | mercommawards.com/mercury category-winner pages (via search) | partial, same pattern as ARC (same publisher, MerComm Inc.) | juried award | yes, per search: 38th Annual Mercury Awards Grand Winners announced 2025-02-25; category pages (Annual Reports – Cover Design, Overall Presentation, Online, Writing) are enumerable | none | mercommawards.com | search-corroborated |
| Red Dot Communication Design winners | juried | `https://red-dot.org/design-refresh/communication-design/winners` | no — HTTP 404 (wrong path guessed) | — | — | — | — | not usable at this URL; needs the correct current path re-probed in research/82 |
| D&AD Awards | juried | dandad.org (Graphic Design category page, via search) | partial | juried award, named subcategories (Integrated, Posters, Catalogues/Brochures/Annual Reports, Direct Mail) | yes, per search: 3,035 Graphic Design category winners in the archive; 2025 example winner "Designing Paris 2024" by W Conran Design | none found | dandad.org, public archive | search-corroborated; direct fetch of `dandad.org/awards/d-ad-awards/categories/graphic-design` not attempted in this pass |
| European Design Awards | juried | europeandesign.org (via search) | partial | juried, 47 categories in 9 groups + Best of Show/Jury Prize/Agency of the Year | yes structurally (category counts, scoring formula for Agency of the Year) but no per-item winner list fetched | `awards.europeandesign.org/winners` exists per search, not directly fetched | europeandesign.org | search-corroborated |
| Type Directors Club (TDC) | juried | oneclub.org/tdcawards, tdc.org (via search) | partial | juried, three disciplines (Communication Design, Lettering, Type Design); TDC Medal for lifetime contribution | yes per search: TDC71 competition, entries from 60+ countries; TDC69 winners from 42 countries; "more than 2,000 entries from over 50 countries" | none found | oneclub.org / tdc.org | search-corroborated |

## Authorities / standards

| Source | Artefact | URL probed | Fetchable? | Note | Fetch |
|---|---|---|---|---|---|
| Europass CV | authority (layout) | `https://europa.eu/europass/en/create-europass-cv` → 301 → `https://europass.europa.eu/en/create-europass-cv` | no — the redirect target itself returned no extractable content in this pass (tool surfaced the redirect but the follow-up fetch was not completed with a body) | Needs a direct re-probe of `europass.europa.eu/en/create-europass-cv` at protocol-freeze time | not usable yet; retry |
| APA 7 paper format | authority | `https://apastyle.apa.org/style-grammar-guidelines/paper-format` | no — fetch returned empty content | APA's paper-format rules (margins, font, spacing, headings) are well documented elsewhere (APA manual itself, paywalled/physical); this specific page did not yield content in this probe | not usable at this URL in this pass; retry or use a library-quoted secondary |
| NISO Z39.18 | authority | not directly fetched; probed via WebSearch | partial | Confirmed current edition ANSI/NISO Z39.18-2005 (R2010); the standard itself is sold by ANSI/NISO (webstore.ansi.org), i.e. **paywalled** — same posture as DIN 5008 per research/80 R-a: cite only a fetched secondary that quotes it, never invent from memory | search-corroborated only; primary text paywalled |
| GOV.UK publishing/content design guidance | authority | `https://www.gov.uk/guidance/content-design/writing-for-gov-uk` → 301 → `https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/tone-of-voice/` | partial — redirect identified but the redirected page's body was not fetched in this pass | Retry at protocol-freeze time with the corrected URL | not usable yet; retry |
| USWDS (as authority, general) | authority | see palette table above (`designsystem.digital.gov`) | **yes** | Already fetched successfully for color tokens; the same site also documents typography/layout guidance not separately re-probed here | fetched (color); layout guidance not yet probed |
| ISO 216 | authority (paper size) | not directly fetched (iso.org sells the standard); probed via WebSearch (Wikipedia/secondary) | partial | A4 = 210mm x 297mm, √2:1 aspect ratio, A(n) = half of A(n-1); ISO 216 itself is paywalled at iso.org — same posture as NISO/DIN: cite the fetched secondary (Wikipedia "International standard paper sizes"), not the primary, and mark authority/paywalled | search-corroborated only; primary paywalled |

## Layout corpora with numeric metrics (probe 2)

Retrieved 2026-09-23. All GitHub rows below were fetched twice — once via WebFetch (whose
underlying small model occasionally paraphrases), then independently re-verified with a direct
`curl` against the raw JSON (`https://api.github.com/search/repositories?...`) — to rule out
model fabrication before any number is cited. Every stargazers_count in this table is the
curl-verified raw value.

**Rate limit note (all GitHub rows):** the unauthenticated Search API caps at
`X-RateLimit-Limit: 10` requests/minute on the `search` resource (confirmed via response headers).
Sequential probing at that pace intermittently returned empty bodies until the window reset —
recorded as "rate-limited, retried" below, not as a dead endpoint.

**Noise-floor warning (GitHub full-text search only):** for families whose family name is a common
English/code word — "quote", "form", "memo", "newsletter" — the query `q="<family> template"`
returns predominantly irrelevant software repositories (e.g. `quote template` top hit is a Solana
trading-bot repo; `form template` top hits are React/Next.js starter kits; `memo template` top hits
are a Zabbix repo list and an AI memory-vault project). GitHub stars are only an admissible metric
for families with a real LaTeX/Typst/web-template ecosystem on GitHub (cv, cover-letter, deck,
report, whitepaper, poster, letter, invoice) — for the others, GitHub search is **not admissible**
without much narrower, hand-curated queries than attempted here.

| Source | Family / query | URL probed | Fetchable? | Metric exposed | Top numeric values (curl-verified) | Fetch |
|---|---|---|---|---|---|---|
| GitHub Search API | cv — `resume+template` | `https://api.github.com/search/repositories?q=resume+template&sort=stars&order=desc` | **yes** | `stargazers_count`, sort honored | total_count 11,352; posquit0/Awesome-CV 28,570; geekcompany/ResumeSample 28,317; billryan/resume 11,452 | fetched + curl-verified |
| GitHub Search API | cv — `topic:cv+topic:resume` | `.../search/repositories?q=topic:cv+topic:resume&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 2,728; posquit0/Awesome-CV 28,570; rendercv/rendercv 17,634; salomonelli/best-resume-ever 16,482 (top 2 hits, career-ops-hq/career-ops 72,510 and MadsLorentzen/ai-job-search 43,744, are real per curl but are AI job-search tools mistagged `cv`/`resume`, not CV templates — exclude by manual filter) | fetched + curl-verified |
| GitHub Search API | cv — `topic:resume-template` | `.../search/repositories?q=topic:resume-template&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 1,588; rendercv/rendercv 17,634; xitanggg/open-resume 8,909; resumejob/awesome-resume 7,431 | fetched (curl) |
| GitHub Search API | cv — `"latex cv"` | `.../search/repositories?q=%22latex+cv%22&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 813; geekplux/cv_resume 544; huajh/awesome-latex-cv 530; opieters/limecv 425 | fetched |
| GitHub Search API | cv — `typst cv` | `.../search/repositories?q=typst%20cv&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 484; rendercv/rendercv 17,634; yunanwg/brilliant-CV 842; skyzh/chicv 727 | fetched |
| GitHub Search API | cover-letter — `"cover letter template"` | `.../search/repositories?q=%22cover+letter+template%22&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 196; ethanhe42/resume-template 137; firefly-cpp/cover-letter-latex 32; FrancesCoronel/cover-letter-templates 29 — thin corpus, low absolute stars | fetched |
| GitHub Search API | deck — `"presentation template"` | `.../search/repositories?q=%22presentation+template%22&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 1,177; ai-ppt-template/free-ppt-template 750; tisho/framer-templates 190; mozilla/mozilla-presentation-templates 144 (deprecated) — low absolute stars, weak corpus | fetched |
| GitHub Search API | poster — `"poster template" latex` | `.../search/repositories?q=%22poster+template%22+latex&sort=stars&order=desc` and `poster%20template%20latex` | **yes** | `stargazers_count` | total_count 133–231 depending on quoting; rafaelbailo/betterposter-latex-template 327; RylanSchaeffer/Stanford-LaTeX-Poster-Template 245; jkjaer/aauLatexTemplates 200 | fetched |
| GitHub Search API | report — `"report template"` | `.../search/repositories?q=%22report+template%22&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 2,812; noraj/OSCP-Exam-Report-Template-Markdown 4,200; whoisflynn/OSCP-Exam-Report-Template 970 — corpus is dominated by pentest/security report templates, not general business reports; usable but needs a narrower query at freeze time | fetched |
| GitHub Search API | whitepaper — `"whitepaper template"` | `.../search/repositories?q=whitepaper%20template&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 45 (very thin); saboyle/latex-template-whitepaper-basic 37; lungetech/proposal-template 11 | fetched, but corpus too small to be a primary ranking source |
| GitHub Search API | proposal — `proposal template` | `.../search/repositories?q=proposal%20template&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 1,156; mohuangrui/ucasproposal 761; tc39/proposal-string-dedent 661 (irrelevant — TC39 language proposal, noise) — mixed relevance | fetched, noisy |
| GitHub Search API | invoice — `"invoice template"` | `.../search/repositories?q=%22invoice+template%22&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 738; sparksuite/simple-html-invoice-template 1,725; tophermade/sprInvoice 224; Invoicebus/html-invoice-generator 173 | fetched |
| GitHub Search API | letter — `"letter template"` | `.../search/repositories?q=%22letter+template%22&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 631; aeris/gdpr 415 (a GDPR request-letter generator, marginal fit); Sematre/typst-letter-pro 217 ("DIN 5008 letter template for Typst" — directly on-family); eddelbuettel/linl 117 | fetched |
| GitHub Search API | brochure — `"brochure template"` | `.../search/repositories?q=%22brochure+template%22&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 29 (extremely thin); top hit only 1 star | fetched, but corpus too small to rank anything |
| GitHub Search API | flyer — `flyer template` | `.../search/repositories?q=flyer%20template&sort=stars&order=desc` | **yes** | `stargazers_count` | total_count 109; open-source-bootcamp/CubeFlyer 19; owncloud-archive/promo 11 — thin, low-star corpus | fetched, weak |
| GitHub Search API | quote / form / memo / one-pager / infographic | various `"<term> template"` | **yes**, page loads | `stargazers_count` present but results are off-topic (see noise-floor warning) | e.g. `quote template` top hit is a 300-star Solana trading bot; `form template` top hit is a 7,049-star Next.js dashboard starter; `memo template` top hit is a 1,032-star Zabbix repo list | fetched but **not admissible** as-is — needs hand-narrowed queries, not attempted here |
| Overleaf template gallery | cv (and by extension all doc families) | `https://www.overleaf.com/latex/templates/tagged/cv` | **yes**, page loads | none — sort control offers only "Recommended," "Last updated," "Last published"; no view/download/star counts anywhere in the fetched payload | no | fetched, confirmed no metric |
| Typst Universe search UI | templates, any family | `https://typst.app/universe/search?kind=templates&q=resume` | **yes**, page loads | none — same "Recommended"/"Last updated" sort, no download counts rendered | no | fetched, confirmed no metric |
| Typst package index (raw JSON) | all Typst packages incl. templates | `https://packages.typst.org/preview/index.json` | **yes** | schema is `name`, `version`, `entrypoint`, `authors`, `license`, `description`, `repository`, `keywords`, `compiler`, `categories`, `updatedAt` — **no downloads/popularity field of any kind** | no | fetched (2,249,267 bytes, 4,796+ package entries); confirmed the index itself carries zero usage metric — would need per-package GitHub star lookup as a proxy, one hop removed |
| CTAN topic/package pages | cv (`moderncv`) | `https://ctan.org/pkg/moderncv` (topic page `ctan.org/topic/resume` 404'd — wrong path) | **yes** for the pkg page | none — version/date/doc links only, no download counts or ranking | no | fetched, confirmed no metric |
| LaTeXTemplates.com | cv category | `https://www.latextemplates.com/cat/curricula-vitae` | **yes** | category size only ("96 templates"), no per-template popularity | no | fetched, confirmed no metric |
| npm registry search API | jsonresume-theme-* (cv, JSON Resume ecosystem) | `https://registry.npmjs.org/-/v1/search?text=jsonresume-theme&size=10` | **yes** | per-package `downloads.monthly` / `downloads.weekly` embedded directly in search results (no second call needed), plus `dependents` count | **yes** — total 87,643 npm packages match the raw substring (mostly noise; real jsonresume-theme-* hits e.g. `jsonresume-theme-modern` monthly 358/weekly 151, `jsonresume-theme-classy`, `jsonresume-theme-waterfall`, etc.) | fetched — note the `text=` search is substring/full-text, not scoped to the exact `jsonresume-theme-` prefix, so `total` is inflated; use the per-package name list, not the total count |
| npm downloads API (point) | jsonresume-theme-elegant (cv) | `https://api.npmjs.org/downloads/point/last-month/jsonresume-theme-elegant` | **yes** | last-month download count | **yes** — `{"downloads":1937,"start":"2026-08-23","end":"2026-09-21"}` | fetched |
| npm registry search API | deck — `reveal.js-theme` | `https://registry.npmjs.org/-/v1/search?text=reveal.js-theme&size=5` | **yes** | per-package `downloads.monthly` | reveal.js core itself 379,944/month (not a theme, the framework); individual themes low (13–31/month for the ones surfaced) — same substring-noise caveat as above | fetched |
| npm registry search API | deck — `marp-theme` | `https://registry.npmjs.org/-/v1/search?text=marp-theme&size=5` | **yes** | per-package `downloads.monthly` | `@marp-team/marpit` 423,052/month, `@marp-team/marp-cli` 278,092/month (core tools, not themes); individual community themes low (65–96/month) | fetched |
| npm registry search API | deck — `slidev-theme` | `https://registry.npmjs.org/-/v1/search?text=slidev-theme&size=5` | **yes** | per-package `downloads.monthly` | `slidev-theme-the-unnamed` 1,880/month, `@echmo/slidev-theme-lidarcar-cz` 1,456/month, `slidev-theme-rockdove` 394/month — this is the cleanest on-topic numeric ecosystem found for the deck family (actual themes, not noise) | fetched |
| Figma Community search | any family | `https://www.figma.com/community/search?resource_type=files&sort_by=popular&query=resume` | no — HTTP 403 | "popular" sort intended, like/duplicate counts described in Figma marketing copy, not observed | no | not usable via plain WebFetch (bot-blocked), consistent with Canva/Behance in probe 1 |
| Slidesgo search | deck | `https://slidesgo.com/search?text=business` | **yes**, page loads | per-category template counts only ("Business: 5,344 templates"); a "Popular themes" section exists but is curated/editorial, not a numeric per-template metric; Like/Download buttons render with no visible counts | no | fetched, confirmed no numeric per-template metric |
| Microsoft Create | cv, invoice, etc. | `https://word.cloud.microsoft/create/en/resume-templates/?source=create_flow&sort=popular` | **yes**, page loads | `sort=popular` param has no observable effect (no evidence it's a real parameter); templates grouped by profession/category only, no counts | no | fetched, confirms probe-1 finding: inventory only, no metric, param does nothing |

## Recommended primary corpus per family

| Family | Best fetchable ranked source | URL | Fallback |
|---|---|---|---|
| cv | Microsoft Create / word.cloud.microsoft resume templates (fetchable inventory, no metric) cross-checked against Europass CV (authority, needs retry-fetch) | `https://word.cloud.microsoft/create/en/resume-templates/?source=create_flow` | Envato Elements resume-cv listing (fetchable, but sort=popular not honored — usable only as an inventory, coded manually) |
| cover-letter | No dedicated ranked corpus found; fall back to Microsoft Create cover-letter category (same domain, same caveats as cv) | `https://word.cloud.microsoft/create/en/` (cover-letter templates) | Envato Elements cover-letter search |
| deck | None of the ranked candidates (Canva, Behance sort, Dribbble popular) were fetchable in this pass | — | Envato Elements presentation-templates listing (fetchable, inventory only, no metric — same limitation as cv) |
| letter | GOV.UK / USWDS style guidance (authority, partially fetched) | `https://design-system.service.gov.uk/` (fetched for color; check for letter/correspondence guidance) | Microsoft Create letter templates |
| memo | No ranked source found; authority only | GOV.UK content design guidance (retry fetch) | Microsoft Create |
| report | ARC Awards / Mercury Excellence Awards category-winner pages (juried, search-corroborated; needs direct fetch at protocol freeze) | `https://mercommawards.com/arc/awardwinners/categoryWinners.htm` | USWDS / NISO Z39.18 (authority, latter paywalled) |
| whitepaper | Same as report (ARC/Mercury do include a written/whitepaper-adjacent category) | as above | D&AD Catalogues/Brochures/Annual Reports category |
| proposal | No ranked or juried corpus found; Envato Elements proposal-template listing is the only fetchable inventory | Envato Elements search "proposal" `sort=popular` (same caveat: sort not honored) | Microsoft Create |
| invoice | Microsoft Create invoice templates (fetchable inventory) | `https://word.cloud.microsoft/create/en/` (invoice) | Envato Elements invoice search |
| quote | No dedicated source; treat as invoice-adjacent | same as invoice | — |
| brochure | D&AD Graphic Design > Catalogues, Brochures & Annual Reports (juried, search-corroborated) | `https://www.dandad.org/awards/d-ad-awards/categories/graphic-design` | Envato Elements brochure search |
| flyer | Envato Elements flyer listing (fetchable inventory) | Envato Elements search "flyer" | Microsoft Create |
| one-pager | No dedicated source; treat as report/brochure-adjacent | — | Envato Elements one-pager search |
| poster | D&AD Graphic Design > Posters (juried, search-corroborated); European Design Awards poster-adjacent categories | `https://www.dandad.org/awards/d-ad-awards/categories/graphic-design` | Envato Elements poster search |
| form | USWDS / GOV.UK form-design guidance (authority) | `https://designsystem.digital.gov/` | — |
| infographic | Behance/Dribbble were both blocked (403/empty) in this pass; no ranked source fetched | — | Envato Elements infographic-template search (inventory only) |

Every family above still needs a **direct, successful WebFetch of the specific ranked/juried page**
before research/82 freezes the protocol — this document flags which URLs are confirmed live
(fetchable) vs. which redirected/blocked/404'd and need a retry with a corrected URL.

## Recommended sources for typefaces, pairings, palettes, scales

- **Typefaces (ranked):** Google Fonts `metadata/fonts` JSON (`popularity`/`trending` fields,
  fetched, numeric) as primary; jsDelivr `@fontsource` package stats (fetched, numeric hits) and
  npm downloads API (fetched, numeric) as corroborating/secondary usage signals for the same face
  where an `@fontsource/<name>` package exists. Typewolf `/recommendations` (fetched, ordinal only)
  as a juried-adjacent secondary opinion, not a numeric rank.
- **Pairings:** no ranked metric exists; treat every pairing as authority/convention (publisher
  "recommended companion" pages, Google Fonts Knowledge, Typewolf editorial suggestions) — never
  cited as "ranked."
- **Palettes:** authority tier is the strongest fetchable tier — GOV.UK Design System colour
  (fetched, full hex table) and USWDS theme-tokens (fetched, full hex table) are the two cleanest
  primary sources. IBM Carbon, Material 3, Fluent 2, and Atlassian tokens exist but were not
  directly fetchable in this pass (JS-hydrated or oversized pages) — usable only as
  search-corroborated until a follow-up fetch succeeds. Ranked tier (Coolors trending, Color Hunt
  popular) failed fetchability in this pass (results are injected client-side); do not treat as
  fetched until an API/JSON path is found.
- **Scales:** modularscale.com is the clean primary — fetched successfully, named ratios with
  numeric values embedded in static markup (minor second 1.067 through golden section 1.618).

## Summary of gaps to resolve before research/82 freezes the protocol

1. Retry with corrected URLs: Europass CV, APA 7 paper-format, GOV.UK content-design guidance,
   Red Dot Communication Design winners (404'd), Google Docs template gallery (needs an
   unauthenticated public gallery URL, not the signed-in editor).
2. Confirm whether Canva/Behance/Dribbble have any anonymously-reachable JSON endpoint at all
   (all three 403'd or returned empty in direct fetch); if not, they are inadmissible as ranked
   sources per research/80 §7 ("a rank from a search snippet never becomes a numeric Rank Value").
3. Carbon/Material 3/Fluent/Atlassian color tokens need a second fetch attempt (smaller page
   slice, e.g. a specific token sub-page) to move them from search-corroborated to fetched.
4. ARC/Mercury/D&AD/European Design Awards/TDC juried sources need at least one direct WebFetch
   of a live category-winner page (not just WebSearch snippets) before they can be cited beyond
   search-corroborated status.

### Recommended primary corpus per family (revised)

Per research/80 R-d, a source only counts as a numeric ranking corpus if it is (a) fetchable and
(b) exposes a real structured count (stars/downloads/likes/uses), not an inventory or a category
size. Applying that bar to everything fetched across both probes:

| Family | Numeric corpus? | Best fetchable numeric-metric corpus | URL | Caveat |
|---|---|---|---|---|
| cv | **yes** | GitHub Search API, `stargazers_count`, best signal-to-noise of any family tested | `https://api.github.com/search/repositories?q=resume+template&sort=stars&order=desc` (cross-check `topic:cv+topic:resume`, `"latex cv"`, `typst cv`) | Manually drop mistagged repos (e.g. AI job-search tools tagged `resume`); combine with `jsonresume-theme-*` npm downloads for the JSON-Resume sub-ecosystem |
| cover-letter | **yes, but thin** | GitHub Search API `"cover letter template"` | `https://api.github.com/search/repositories?q=%22cover+letter+template%22&sort=stars&order=desc` | Only 196 repos total, top result 137 stars — usable but not a deep corpus; fall back to cv corpus (many cv repos bundle a cover-letter template) |
| deck | **yes** | npm registry search `downloads.monthly` for `slidev-theme` (cleanest signal — actual themes, not framework noise) plus GitHub `"presentation template"` stars as a secondary axis | `https://registry.npmjs.org/-/v1/search?text=slidev-theme&size=20` | `reveal.js-theme`/`marp-theme` searches return mostly the core framework packages (very high downloads) drowning out individual themes — filter to packages actually named `*-theme-*`; GitHub deck corpus (1,177 repos) is comparatively weak (top only 750 stars) |
| letter | **yes, but mixed relevance** | GitHub Search API `"letter template"`, filtered to on-topic hits | `https://api.github.com/search/repositories?q=%22letter+template%22&sort=stars&order=desc` | Corpus is small (631 total) and noisy (GDPR request-letter generators, IEEE review-response templates mixed with true correspondence templates); `Sematre/typst-letter-pro` (217 stars, explicitly DIN 5008) is the standout on-family hit |
| memo | **no** | none found | — | GitHub `"memo template"` is dominated by unrelated software (Zabbix repo lists, AI memory-vault projects); no ranked/juried/download corpus located in either probe — flag as gap |
| report | **yes, but domain-skewed** | GitHub Search API `"report template"` | `https://api.github.com/search/repositories?q=%22report+template%22&sort=stars&order=desc` | Corpus (2,812 repos) is dominated by penetration-test/security report templates (OSCP), not general business reports — usable as a numeric corpus for that sub-genre only; needs a narrower query (e.g. add `-OSCP -pentest`) before it represents "report" broadly |
| whitepaper | **no, corpus too thin** | GitHub Search API `whitepaper template` exists but only 45 repos total, top at 37 stars | `https://api.github.com/search/repositories?q=whitepaper%20template&sort=stars&order=desc` | Technically fetchable and numeric, but too small a population to support "counting archetypes" — treat as a weak secondary signal only, flag as a near-gap |
| proposal | **no** | none found | — | GitHub `proposal template` mixes real proposal templates with unrelated hits (e.g. TC39 language proposals); no clean numeric corpus isolated in this probe — flag as gap |
| invoice | **yes** | GitHub Search API `"invoice template"` | `https://api.github.com/search/repositories?q=%22invoice+template%22&sort=stars&order=desc` | Clean, on-topic top results (sparksuite/simple-html-invoice-template 1,725 stars); best invoice signal found in either probe |
| quote | **no** | none found | — | GitHub `"quote template"` returns off-topic code repos (trading bots, string-template libraries); no numeric corpus found — treat as invoice-adjacent for design purposes but do not cite a fabricated metric |
| brochure | **no, corpus too thin** | GitHub Search API `"brochure template"` exists but only 29 repos, top at 1 star | `https://api.github.com/search/repositories?q=%22brochure+template%22&sort=stars&order=desc` | Not usable as a ranking source — population too small; flag as gap |
| flyer | **no, corpus too thin** | GitHub Search API `flyer template` exists but only 109 repos, top at 19 stars | `https://api.github.com/search/repositories?q=flyer%20template&sort=stars&order=desc` | Not usable as a ranking source; flag as gap |
| one-pager | **no** | none found | — | Not separately probed with a clean query in probe 2 (probe 1 found no dedicated source either); flag as gap |
| poster | **yes** | GitHub Search API `"poster template" latex` | `https://api.github.com/search/repositories?q=%22poster+template%22+latex&sort=stars&order=desc` | On-topic academic-poster corpus (rafaelbailo/betterposter-latex-template 327 stars, Stanford/AAU templates); solid numeric signal for the academic-poster sub-genre specifically |
| form | **no** | none found | — | GitHub `"form template"` is dominated by unrelated web-app starter kits (Next.js dashboards); no design-template corpus isolated; flag as gap |
| infographic | **no** | none found | — | GitHub `"infographic template"` corpus (69 repos) is mostly irrelevant (a LaTeX CV repo tops it); Figma Community (403) and Behance/Dribbble (403, per probe 1) remain blocked; flag as gap |

**Families with a real fetchable numeric corpus:** cv, cover-letter (thin), deck, letter (mixed),
invoice, poster (academic-poster sub-genre), report (security-report sub-genre), whitepaper
(borderline — corpus too small to trust alone).

**Families flagged as no numeric corpus found (gap):** memo, proposal, quote, brochure, flyer,
one-pager, form, infographic. For these, per research/80 discipline, no popularity/ranking claim
should be made from any source probed in either pass — only authority/inventory sources (Microsoft
Create, USWDS/GOV.UK, Envato inventories) are admissible, and only as unranked inventories.

## Compact per-family summary (probe 2)

- **cv** — strong numeric corpus (GitHub stars, cross-checked 4 queries + npm downloads for
  JSON-Resume themes).
- **cover-letter** — numeric corpus exists but thin (196 repos, max 137 stars).
- **deck** — strong numeric corpus via npm `slidev-theme` downloads; GitHub stars as secondary.
- **letter** — numeric corpus exists, small and mixed-relevance; one strong on-topic hit
  (`typst-letter-pro`, DIN 5008, 217 stars).
- **memo** — no numeric corpus found.
- **report** — numeric corpus exists but skewed to security/pentest reports specifically.
- **whitepaper** — numeric corpus exists but population too small (45 repos) to trust.
- **proposal** — no clean numeric corpus (query too noisy).
- **invoice** — strong numeric corpus (GitHub stars, clean and on-topic).
- **quote** — no numeric corpus found.
- **brochure** — corpus exists but too small (29 repos) to use.
- **flyer** — corpus exists but too small (109 repos) to use.
- **one-pager** — no numeric corpus found.
- **poster** — strong numeric corpus for the academic-poster sub-genre (LaTeX/Beamer posters).
- **form** — no numeric corpus found.
- **infographic** — no numeric corpus found.

Cross-cutting finding: Overleaf, Typst Universe (both the web UI and the raw
`packages.typst.org/preview/index.json`), CTAN, LaTeXTemplates.com, Slidesgo, and Microsoft Create
were all confirmed fetchable in this pass but **confirmed to expose zero popularity/download
metric** — they remain inventory-only sources regardless of family. Figma Community 403'd, matching
Canva/Behance/Dribbble's blocked status from probe 1. The single clean win of this probe is that
**GitHub's Search API and the npm registry search API both embed the numeric metric directly in the
same JSON response as the inventory** (`stargazers_count`, `downloads.monthly`) — no second
authenticated hop required — which is why they now anchor 8 of 16 families, versus zero
layout-template corpora with a numeric metric in probe 1.
