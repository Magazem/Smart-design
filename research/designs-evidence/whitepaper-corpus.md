# Whitepaper family: evidence sweep, A1 pool with the GitHub whitepaper items (pooled N = 10) + 82b A5 twin check (whitepaper ← report)

Coder: Design Researcher 2. Retrieved **2026-09-25**. I count; I do not judge (research/82 §1).

**Binding rules:** research/82, 82a-clarifications-1 to -5, 82a-general (header treatment, colour use) and 82b-ADOPTED (A1, A4, A5). The method follows `quote-corpus.md`.

**Scope limits:**
- No git and no GitHub search API. GitHub was used only for raw fetches of two repositories named in research/82b §1c.
- From the report and proposal corpora I read ONLY the items csv titles/urls, never their codes.
- Exposure: I am the report-L3 re-checker (report-corpus-l3.md R.8). I must not second-code report later.

Items file (C11 + C24 `pages`): `research/designs-evidence/whitepaper-items.csv`.

## W.0 Result in one paragraph

My non-GitHub sweep yields 4 on-topic codeable items (W.1). Two of them (saboyle, mlouhivu) are also among the 8 GitHub whitepaper templates coded by Design Researcher (`whitepaper-items-github.csv`). **After dedup by repo/url the A1 pool has N = 10** on-topic codeable items (W.8), which meets the floor. Under 82a C27 / 82b A1 it is therefore a **coded corpus**: one pool, counted once in §6.
- My contribution to the pool: **WPL:001** (LibreOffice) and **WPO:001** (Overleaf).
- The 2 duplicates count once, under the GitHub worker's ids (WP:001 saboyle, WP:003 mlouhivu). My codes for them (W.3, `WPG-dup(...)`) are an independent coding, blind to theirs, and are not counted.
- I did not read the GitHub worker's codes. The pooled k/N and frequency table must be computed by the orchestrator from both files.

The **A5 twin check passes** (W.5): whitepaper and report share Style, Palette and Page Format keys. Whitepaper may borrow up to 3 report designs once report ships, with the typeface refilled per §8.

## W.1 Sources walked (2026-09-25, `curl -sL -A "smart-design-research"`)

| Source | Query / method | Raw hits | On-topic whitepaper | Codeable |
|---|---|---|---|---|
| **Microsoft Create sitemaps** | `{word,excel,powerpoint}.cloud.microsoft/create/sitemap.xml` (1200 / 677 / 629 URLs), English slugs grepped for `white|paper|report|technical|research|brief` | slugs: technical-documentation, papers-and-reports, expense-report-templates (+3 blog posts) | no whitepaper slug | — |
| **Microsoft Create, all English category pages** | 168 `/create/en/` pages, static payload parsed: **1,168 cards**; titles grepped for `white ?paper|livre blanc|position paper|technical (paper|brief)|policy (paper|brief)|brief` | 1: "Whitepaper proposal presentation" (powerpoint/business-proposal-templates). The technical-documentation page carries 0 static cards | 0: a PowerPoint deck is the deck family, not a whitepaper document (§3.2) | — |
| **LibreOffice Extensions** | tag 118 + `q=` white+paper, whitepaper, white-paper, livre+blanc, weissbuch, libro+blanco, position+paper, policy+brief, technical+paper | 1 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | 1: 5083 "Conference White Paper" (Writer .ott, 532 downloads) | 1 (screenshot 181x256 px) |
| **Overleaf tags** | `/gallery/tagged/{white-paper, whitepaper, white-papers, technical-report, technical-reports, policy-brief}` | none exist: every one falls back to "Journal articles" | — | — |
| **Overleaf search** | `/latex/templates?q=white+paper` | ignored: identical output to `q=zzqqxx_nonsense` | — | — |
| **Overleaf `report` tag, full walk** | all **202** pages of `/gallery/tagged/report` (403 throttling on 169 pages first; retried until every page returned); **1,518** unique templates; titles grepped as above | 1: "Astro2020 Decadal Science White Paper" (page 115) | 1 | 1 (template PDF at source) |
| **Typst Universe** | `packages.typst.org/preview/index.json` (1,619 packages, 818 templates); name/description/keywords/categories grepped | 0 | 0 | — |
| **A4 cross-lists from report / proposal corpora** | titles and urls in `report-items-github.csv` (40), `report-items-ms.csv` (10), `report-items.csv` (14), `proposal-items-github.csv` (40), `proposal-items-ms.csv` (7) | 0 titles mention white paper / whitepaper / position paper / policy brief (report-corpus-ms.md also states "None is a whitepaper") | 0 | — |
| **GitHub repositories named in 82b §1c** (raw fetch, no search) | saboyle/latex-template-whitepaper-basic (★37 per 82b); mlouhivu/prace-latex-whitepaper (★4) | 2 | 2 (both are whitepaper templates by README) | 2 (example PDFs published at source: `out/whitepaper.pdf`, `example.pdf`) |
| GitHub `whitepaper+latex` beyond those two | needs the search API | — | not walked | GitHub worker's scope (disclosed). 82b §1c: the remainder are real project whitepapers (specimens, off-topic) |

My sweep alone: **4 codeable on-topic items from 3 sources** (LibreOffice, Overleaf, GitHub), which is < 10. Pooled with the GitHub worker's 8 items after dedup: **N = 10** (W.8).

## W.2 On-topic decisions

- **WPL:001 LO 5083 "Conference White Paper".** A Writer template labelled white paper: project title, organisation and photo box, then abstract/keyword sections in two languages. On-topic by title; closest in form to a conference submission sheet (disclosed).
- **WPO:001 Overleaf Astro2020 Decadal Science White Paper.** Template for white papers submitted to the Astro2020 survey. On-topic. Its PDF is a title/metadata sheet plus near-empty pages (words per page 55 / 13 / 2), so there is **no C13 running-text page** (no page has ≥250 words). Body features other than those visible on page 1 are `unknown` (C7 / C25 analogue). Not a blank scaffold (C3): typography and labels are present.
- **WPG-dup(saboyle) saboyle.** README: "Basic latex template for formal research or business whitepapers"; sample `out/whitepaper.pdf`. Page 1 = title + abstract + running text (505 words): no separate cover, so all features come from page 1 (C13).
- **WPG-dup(mlouhivu) mlouhivu.** README (plain-text file `README`): "LaTeX package for a PRACE-RI whitepaper"; sample `example.pdf`. Page 1 = title + abstract + running text (550 words): no separate cover.
- **Off-topic:** MS "Whitepaper proposal presentation" (a deck).
- **Not walked:** real project whitepapers (specimens; 82b "not adopted").

## W.3 Coded items (§4 + 82a-general A/B; C13 page scope; variant `cover page`)

| id | columns | heading | body | colour | header | rules/boxes | density | cover | adm | measurements / notes |
|---|---|---|---|---|---|---|---|---|---|---|
| WPL:001 | 1 | sans | sans | mono | ruled | boxes | standard | no | y | 181x256 px screenshot, viewed x4: low resolution, BORDERLINE on every glyph call. The title block sits in a bordered box spanning ≥ 80% of page width; its edge counts as a line (82a-general A.2 step 3) → ruled. Section heads carry full-width rules. Photo placeholder excluded (B1b); black/grey only → mono. ~40 text lines. Heading/body glyph-judged sans (the `.ott` was not opened) |
| WPO:001 | 1 | serif | serif | mono | plain-left | unknown | unknown | yes | y | PDF page 1, fonts from the PDF: title NimbusRomNo9L 25 pt (Times clone → serif), labels NimbusRomNo9L-Medi 12 pt. Title left-aligned, no band or rule → plain-left. All text #000000 → mono. ☐ checkboxes are text glyphs (MSAM10), not boxes. No running-text page (C13) → rules/boxes and density `unknown`. 18 text lines on page 1. Page 1 is a title/metadata sheet → cover yes |
| WPG-dup(saboyle) | 1 | sans | sans | mono | plain-centered | none | dense | no | y | PDF fonts: NimbusSanL (Helvetica clone → sans) for title (16 pt) and body (9 pt). All spans #000000 ("custom colours for section titles" are black in the sample) → mono. Title/author/date centred, no rule → plain-centered. Margin line numbers are marks, not rules. **74** text lines on page 1 (≥ 55) → dense |
| WPG-dup(mlouhivu) | 1 | serif | serif | mono | ruled | rules | dense | no | y | PDF fonts: CMR17 title, CMR10 body (Computer Modern → serif). PRACE star logo excluded (B1b); all text #000000 → mono. Title block (title, authors, affiliations) is centred; a full-width hairline sits directly below it, above the abstract (gap < 4 body lines) → ruled (ruled precedes plain-centered). **55** text lines (≥ 55) → dense |

Admissibility:
- **A1-A8:** none fire.
- **C-rules:** whitepaper has no family fail constraint in §5.
- **Codes:** 4 of 4 admissible.

## W.4 Descriptive tally of my coded items (presence only; the pooled frequency is computed by the orchestrator, W.8)
- `1|sans|mono|ruled`: WPL:001
- `1|serif|mono|plain-left`: WPO:001
- `1|sans|mono|plain-centered`: WPG-dup(saboyle)
- `1|serif|mono|ruled`: WPG-dup(mlouhivu)

Skew:
- 3 of the 4 are LaTeX academic/technical templates (developer and research users).
- 1 is a LibreOffice conference sheet.
- There is no office-suite business whitepaper template in any reachable catalogue.
- All 4 are mono and single-column.

## W.5 82b A5 structural-twin check (whitepaper ← report)

Mechanical check against the shipped data, `skill/document-design-intelligence/data/base/doctypes.csv` → `Reasoning Key` → `doc-reasoning.csv` (script output, 2026-09-25):

| Key | whitepaper | report-short (report family default) | report-long-toc | Equal (A5 keys) |
|---|---|---|---|---|
| Reasoning Key | whitepaper-formal | report-classic | report-classic | — |
| **Style Key** | report-classic-serif | report-classic-serif | report-classic-serif | **yes** |
| **Palette Key** | print-neutral | print-neutral | print-neutral | **yes** |
| **Page Format Key** | a4-report-standard | a4-report-standard | a4-report-standard | **yes** |
| Typeface Key (not an A5 key) | ofl-plex-superfamily | safe-serif-times | safe-serif-times | no |
| Render Target / Constraint Set | pdf-chromium;docx-office / report-typography;print-legibility | same | same | yes |
| Structure Key (informational) | whitepaper-standard | report-short | report-long-toc | no |

**Result: structural twins (A5 satisfied)** against both report doctypes. This confirms 82b's table.

The typeface differs. Per 82b A5, a borrowed design keeps report's archetype and fill, but its **typeface is re-selected by §8** for whitepaper (82b: "the typeface differs; §8 refills it"). The whitepaper default row `ofl-plex-superfamily` is the fallback on `scale-gap`.

**Borrowing plan** (to run after report is filled and shipped; 82b A5 (a)-(e)):
1. Take up to **3** of report's shipped designs, in report's rank order. They keep report's archetype and fill, except the typeface (refilled per §8 with whitepaper's heading/body classes).
2. Re-check each against **whitepaper** admissibility: §5 universal A1-A8; no family constraint. Also apply the whitepaper default Anti-Pattern Tokens (multi-column, icon-only-skill-bar, gradient, emoji…) when authoring the reasoning row. A report design with `columns ≠ 1` conflicts with the whitepaper `multi-column` anti-pattern; that is flagged for the filler, and §8 copies anti-pattern tokens from the family default.
3. Ranking Metric `borrowed:report:<report's own metric string>`, keeping report's Evidence Class (ranked/juried).
4. Rank them after whitepaper's own evidence. Whitepaper has none ranked, so they take ranks 1-3, before any L4 convention.
5. Disclose here and in the whitepaper designs table.
6. Re-run the key comparison at borrowing time.

The W.4 codes are presence notes only; they never reorder borrowed designs.

## W.6 Second-coder ids
The family-wide sample (C10) draws from the pooled ids: the GitHub worker's 8 (`whitepaper-items-github.csv`) plus **WPL:001, WPO:001** (`whitepaper-items.csv`, with a C24 `pages` column). The duplicates are not listed twice. Sample size for N = 10: `max(min(10, 10), ceil(2.5)) = 10`, i.e. all 10 items.

**Id clash:** the GitHub file uses `WP:NNN`. My items were therefore renamed to `WPL:` (LibreOffice) and `WPO:` (Overleaf) so the two files can be merged without collisions.

## W.7 Shortfall (honesty rule)
The pooled corpus (N = 10) ranks only archetypes with K ≥ 2 in the orchestrator's merge. Whitepaper then ships its own ranked archetypes first (§6 steps 1-3). Up to **3 borrowed report designs** (A5, W.5) follow, then L4. Any remaining gap to 8-10 is stated in the designs table and release notes.

## W.8 A1 pool with the GitHub whitepaper items (dedup, 82a C27)

| Source | Items (on-topic, codeable) | ids |
|---|---|---|
| GitHub (Design Researcher; `whitepaper-items-github.csv`) | 8 | WP:001 saboyle, WP:002 lungetech, WP:003 mlouhivu, WP:005 Iki-Software, WP:006 orelyx, WP:012 dominiek/moonfish, WP:013 browric2/Metrasens, WP:017 taryune |
| LibreOffice (this file) | 1 | WPL:001 |
| Overleaf (this file) | 1 | WPO:001 |
| GitHub, found via the 82b-named repos (this file) | 2 | duplicates of WP:001 and WP:003; dropped (C27: first by corpus order; both are GitHub-sourced, so the GitHub worker's entry is kept) |

Script dedup by normalised repo URL: 8 GitHub + 4 mine, 2 duplicates → **N = 10 unique**.

- Ranking Metric: `prevalence:pool(github+libreoffice+overleaf):k/10`.
- Native metrics (stars, downloads) are recorded but not used (A1).
- Skew: 8 of 10 are LaTeX/GitHub developer templates; 1 is an Overleaf academic template; 1 is a LibreOffice conference sheet. There is no office-suite business whitepaper template.
- WPO:001 carries `unknown` for rules/boxes and density (no running-text page); these are variants, so the identity is unaffected.
