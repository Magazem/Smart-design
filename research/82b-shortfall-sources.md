# research/82b — Shortfall remedy sources (proposed amendment to research/82 §10)

Author: Opus planner/reviewer, 2026-09-23. **Status: PROPOSAL.** research/82 is frozen. Nothing
here binds a coder until the orchestrator adopts it, and families already coded keep their results.
Adopted parts become `82b` under the 82a convention: dated, and stating which results they affect.

Scope: memo, form, flyer, quote, one-pager, infographic, whitepaper. The goal is still "about 10
designs per family, ranked by a structured system; researchers never judge". Where no such
system exists, the honest result is still a Shortfall. This file finds every source I could reach
today. It does not lower the bar.

Method: every source below was probed today with `curl -s -L -A "smart-design-research"`, or
through WebSearch/WebFetch where marked. Item counts are raw on-page counts from the probe, **not
coded on-topic counts**. Any count marked "est." is my estimate, and an F.a worker must confirm
it. No number here is a Rank Value (research/80 §7).

---

## 1. Probe log (2026-09-23)

### 1a. Microsoft Create: category slugs enumerated from sitemaps, not guessed

The `create.microsoft.com` robots/sitemap routes to the M365 SPA. The per-app sitemaps are
static and list every category slug:
`https://{word,excel,powerpoint}.cloud.microsoft/create/sitemap.xml` (1200 / 676 / 629 URLs).
I counted items as unique `catalog-assets/en-us/<uuid>` in the static payload of
`https://<app>.cloud.microsoft/create/en/<slug>/`.

| App / slug | Resolves | Unique items | Relevant titles (thin families) |
|---|---|---|---|
| word/memo-templates | yes | 9 | 7 memos (already in memo-corpus M.1) |
| word/business-templates | yes | 26 | 4 memos (all already in M.2: Business memo (bold), Logo memo, Memo (simple), Modern memo (simple)); **"Executive summary"**; 5 business proposals; 5 invoices |
| word/papers-and-reports | yes | 10 | 10 reports (business + student). None are whitepapers. *(Bonus for report: a new L2 catalogue, N=10.)* |
| word/pamphlet-templates | yes | 20 | brochures/booklets; "Modern flyer" (= MSF:002, duplicate); "Teacher appreciation flyer" (check against MSF list) |
| word/flyer-templates | yes | 17 | already coded (flyer-corpus F.1) |
| word/minutes-templates, meeting-minutes | yes | 20 / 5 | minutes/agendas. **Not memos** (different doc genre, so not cross-listed) |
| powerpoint/flyers-posters-templates | yes | 10 | **3 flyers** (Yoga flyer, Holi celebration flyer, Daycare flyer); 5 posters; 2 tri-fold brochures |
| powerpoint/infographic-maker | yes | 6 | **3 infographics** (Illustrate fashion trends, Provide financial tips, Display product roadmap); 3 posters |
| powerpoint/business-proposal-templates | yes | 17 | *(bonus for proposal)* |
| excel/invoice-templates | yes | 8 | invoices (already in invoice pool) |
| any app: quote, estimate, fact-sheet, one-page, white-paper, form(s), report (excel/ppt) | **no** | 0 | the slug is absent from all three sitemaps; unknown slugs 307-redirect to the app home |

Conclusion: Microsoft Create has **no** quote, estimate, fact-sheet, one-pager, white-paper or
form category (definitive, because the sitemaps were enumerated). It adds 3 flyers and 3
infographics, and 1 one-pager-like item ("Executive summary").

### 1b. LibreOffice Extensions (tag 118, `q=` full text, `ord=download_d`)

The tag facets are app/type tags only (Impress 43, Writer 44, Business 69, Documents 113,
Presentations 86, …). There are no family tags. Full-text results:

| q | Hits | On-topic (title check) |
|---|---|---|
| devis, kostenvoranschlag, offerte, presupuesto, preventivo, memorandum, fact+sheet | 0 | — |
| quote / quotation / estimate / angebot | 5 / 1 / 1 / 1 | quotation: 1 (id 99480, unverified); the rest are budgets, CVs, a DIN letter |
| memo | 5 | 0 (already in memo-corpus M.1) |
| infographic | 13 | **1** ("Infographic Presentation", 99332). The other 12 are MKCL/InDiFi Impress decks, so noise |
| white+paper | 1 | 0 |
| flyer | 4 | est. 3 (already in flyer-corpus F.7) |
| form / formular | 30 / 3 | noise (CVs, books, letters, SEPA sheet) |
| Tag Business (69) + Templates | ~60 raw | invoices, DIN letters, budgets, Gantt charts. No quotes or memos |

### 1c. GitHub Search API (`sort=stars`, 7–15 s spacing, and several rate-limit retries on a shared IP)

| Query | total_count | On-topic reading of top hits |
|---|---|---|
| `memo+typst` | 15 | est. 6 memo templates: nogula/tufte-memo ★44, tonguetoquill/typst-usaf-memo ★10, christopherkenny/ctk-memo ★1, gael-close/quarto-tech-memo ★1, monaqa/typst-class-memo ★0, jasonelaw/bes-typst-memo ★0. The rest are Spanish "memoria" theses (off-topic) |
| `topic:memo+latex` | 2 | charlesangus/texMemo ★8 |
| `devis+latex` / `quotation+latex` / `angebot+latex` | 3 / 8 / 0 | ≤3 quote generators at ★0–1 |
| `quotation+template+pdf` | 19 | quote generator apps at ★0–1, not templates |
| `topic:quotation` | 75 | trading bots, invoice apps |
| `topic:invoicing` | 1170 | apps: akaunting ★10133, idurar ★8827, Dolibarr ★7651, frappe/books ★4981, bigcapital ★3906, InvoicePlane ★3142, SolidInvoice ★972, itflow ★1007… README mentions quotes for IDURAR, Dolibarr, InvoicePlane, SolidInvoice and itflow. **README images are app-UI screenshots, not quote PDFs**, so codeability is unproven |
| `invoice+typst` | 39 | ad-si/invoice-maker ★174, Sajjon/klirr ★139, erictapen/typst-invoice ★99, … (invoice family; quote support unknown) |
| `whitepaper+latex` / `white-paper+latex` | 76 / 24 | mostly **real project whitepapers** (solana ★110, aeternity, bigchaindb…), which are specimens, not templates. Templates: saboyle/latex-template-whitepaper-basic ★37, mlouhivu/prace-latex-whitepaper ★4, est. <5 in total |
| `topic:whitepaper` | 430 | papers and projects, not templates |
| `one-pager+latex` | 134 | résumés (noise) |
| `factsheet+latex` | 6 | ML-challenge fact sheets (noise) |
| `topic:infographic` | 210 | tools (antvis/Infographic ★6856), CVs. Noise |
| `infographic+latex` | 13 | 2 small templates (★2), the rest CVs. Noise |
| `flyer+typst` | 5 | 5 flyer templates at ★0–2 |
| `form+latex+fillable` | 15 | noise |

### 1d. Typst Universe (`https://packages.typst.org/preview/index.json`)

This covers 1619 packages and 818 templates, with fields `name, description, keywords,
categories, repository, …`. There is **no download or popularity field**. The templates have
categories (office 78, flyer 6, poster 8, report 222, …). Keyword hits among templates: invoice
8, memo 2, flyer 2, one-page 1, whitepaper 0. It's a catalogue with no editorial order, so it
can only support prevalence, and every thin family is under 10 items. It can be used for
corroboration or as a pool member (A1).

### 1e. Overleaf gallery tags (`https://www.overleaf.com/gallery/tagged/<tag>`)

| Tag | Items | Notes |
|---|---|---|
| memo | 11 (2 pages) | est. on-topic 4–5: CAPSL technical memo, Cornell policy memo, SINTEF project memo, SINTEF memo (plus YMCA?). FUCI motions/candidacy are organisational papers (off-topic) |
| invoice | 6 | invoice family |
| newsletter / poster / report / cv / presentation / letter / formal-letter | 3p / 27p / 202p / 83p / 102p / 5p / 18p | report/poster families only |
| white-paper, flyer, form(s), quote, infographic, fact-sheet, one-page, business | none | these tags don't exist; the URL falls back to a default page |

Overleaf shows no metric, so it can only support prevalence.

### 1f. Authorities and juries

| Source | URL | Fetch | Covers |
|---|---|---|---|
| **AR 25-50** Preparing and Managing Correspondence (US Army, 2020) | `https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN42124-AR_25-50-007-WEB-13.pdf` | **fetched** (application/pdf, 4.0 MB; pdftotext) | memorandum format: 8½×11 paper; "Margins. Use standard margins: 1-inch from the left, right, and bottom edges. Do not justify right margins"; "A font with a point size of 12 is recommended"; office symbol at the left margin 1 inch from the top; MEMORANDUM FOR / SUBJECT block (ch. 2 figures) |
| **Purdue OWL**: Memos (format, parts of a memo, sample) | `https://owl.purdue.edu/owl/subject_specific_writing/professional_technical_writing/memos/` (`format.html`, `parts_of_a_memo.html`, `sample_memo.html`) | **fetched** (200) | TO/FROM/DATE/SUBJECT heading segment; opening, context, task, summary, discussion and closing segments |
| SECNAV M-5216.5 DON Correspondence Manual | secnav.navy.mil PDF | **blocked** (returns a PNG bot page) | unverified; don't use |
| DAFH 33-337 *Tongue and Quill* (USAF) | static.e-publishing.af.mil PDF | **403** | unverified. A mirror may work; one retry allowed |
| UNC Writing Center, memos | writingcenter.unc.edu | 404 | none |
| **ABS Forms Design Standards 2023**: *Paper forms design standards: lines and boxes*; *General forms design principles: layout, lines, boxes and typography* (Australian Bureau of Statistics) | `https://abs.gov.au/statistics/standards/abs-forms-design-standards/2023/paper-forms-design-standards-lines-and-boxes` and `…/general-forms-design-principles-layout-lines-boxes-and-typography` | **fetched** (200) | **PRINT forms**: "Use a 0.5-point line for normal answer boxes"; outlined answer boxes; eye-guide lines linking label and box; lines to create columns for split-page forms; full-width instruction boxes |
| **NHS digital service manual**: text input | `https://service-manual.nhs.uk/design-system/components/text-input` | **fetched** (200) | web form fields (same family as GOV.UK) |
| DSFR (France), AGDS/GOLD (Australia) | systeme-de-design.gouv.fr / designsystem.gov.au | 403 / timeout | unverified |
| Center for Civic Design, print + PDF forms | civicdesign.org | 404 | none |
| **Information is Beautiful Awards** (Kantar/IIB) winners | `https://www.informationisbeautifulawards.com/showcase?action=index&award=<YYYY>&controller=showcase&page=<n>&pcategory=winner&type=awards` | **fetched** (200) | juried winners by edition: 2024 ≥30 (2 pages), 2023 29, 2022 30. Editions 2012–2024 are listed. **No format field**: static and interactive entries are mixed, and item pages carry no machine-readable type |
| Malofiej (SND-E, Univ. of Navarra) | `https://www.malofiejgraphics.com/` | homepage 200 | the winners-list structure was not verified |

---

## 2. Proposed amendments (82b), each with its justification

Every amendment below applies an existing metric or rule in a new place. None invents a metric.

**A1. Pooled L2 catalogue.** §10 already pools brochure MS + LO into one catalogue pool
(N≈12). This amendment makes that precedent general. If every reachable catalogue for a
family has fewer than 10 on-topic items (so §2 would make each one corroboration-only), the
F.a worker may pool them into **one** L2 prevalence pool, provided the pool has ≥10 on-topic
codeable items. Conditions: at least 2 distinct sources; each item appears once (cross-source
duplicates collapse to one item); native metrics are recorded but **not used**, because stars
and download counts can't be compared across sources. Ranking Metric:
`prevalence:pool(<src1>+<src2>+…):k/N`. The pool counts as **one corpus** in the §6
unweighted mean. The evidence file must give per-source counts and skews.
*Why this is still "structured":* each member is a curated or published catalogue, and the
statistic (share of archetype a in the pool) is the §2 L2 statistic. It is only computed over a
union.

**A2. Juried pool (L2j).** The winners of a named award edition (or of consecutive editions)
may be coded as a prevalence pool when there are ≥10 on-topic codeable winners. Evidence Class
`juried`; Ranking Metric `prevalence:award:<name>:<years>:k/N`. It counts as one corpus in
§6. Winners at every medal level are pooled, and medal level is **not** used as a weight (no
invented metric). Items that are not a single static composition (interactive-only, video,
physical object, web app) are off-topic under §3.2. That test is decidable from the preview.
*Why:* the user named juried awards as an acceptable ranking system. §2 already treats a jury
as L3 evidence, and prevalence among juried winners is the L2 statistic applied to a juried
population.

**A3. L3 cap when there is no ranked evidence.** §6 step 2 caps L3 at 3 to reserve slots for
ranked designs. If step 1 produces **zero** ranked K≥2 designs for the family, the cap becomes
**5**. Each L3 design must code (§4) to a **distinct** archetype. Same-archetype authorities
still merge (extra provenance row, as today). *Why:* the reservation has no purpose when nothing
ranked exists. Distinctness stops one prescription from being inflated into several "designs".

**A4. Cross-listing generalised.** §3.2 cross-lists quote/estimate/devis/Angebot titles to
`quote`. Under this amendment, any item in any coded corpus that passes **another** family's
on-topic test is recorded in that family's candidate list, with its source corpus and native
position. It enters that family's pool only through A1 (so a cross-listed item never carries the
lending corpus's k/N). *Why:* it's the existing quote rule, applied to every family. Examples:
the PPT tri-fold brochures go to brochure, and the Word "Executive summary" goes to one-pager.

**A5. Structural-twin borrowing.** A family B may borrow up to **3** designs already shipped by
family L only if the shipped data already makes L and B **structural twins**: the defaults
have the **same Style Key, Palette Key and Page Format Key** (a mechanical check against
`doctypes.csv` + `doc-reasoning.csv` at task start). Borrowed designs:
(a) keep the lender's archetype and fill;
(b) are re-checked against **B's** admissibility (§5, e.g. C7 for quote);
(c) take Ranking Metric `borrowed:<L>:<L's own metric string>` and keep L's Evidence Class;
(d) rank **after** all of B's own evidence (steps 1–3) and before L4;
(e) are disclosed in B's evidence file.

Check against the data today:

| B ← L | Style | Palette | Page format | Twin? |
|---|---|---|---|---|
| quote ← invoice | form-grid-underline = | print-neutral = | a4-form-standard = | **yes** |
| whitepaper ← report | report-classic-serif = | print-neutral = | a4-report-standard = | **yes** (the typeface differs; §8 refills it) |
| flyer ← brochure | marketing-print-bold = | brand-accent-print = | a4-flyer ≠ a4-trifold | no |
| flyer ← poster | = | = | a4-flyer ≠ a3-poster | no |
| memo ← letter | memo-plain ≠ letter-formal-grid | = | = | no |
| one-pager ← flyer / report | one-pager-tight ≠ | — | ≠ | no |
| form ← invoice | = | mono-ink ≠ print-neutral | = | no |
| infographic ← poster | infographic-bold ≠ marketing-print-bold | — | ≠ | no |

*Why only twins:* a borrowed rank claims that "this archetype is frequent among L". For a
twin, the product already asserts that L and B render with identical style, palette and page,
so the borrowed design introduces no new visual claim. For non-twins, borrowing would ship
L's popularity as if it were B's, which R-d forbids. **All other borrowing is rejected**, and
in particular memo←letter, one-pager←flyer/report, flyer←poster and infographic←poster.
(Item-level cross-listing under A4 remains the legitimate route between non-twins.)

**Not adopted (considered and rejected):**
- **Specimen corpora** (real published documents ranked by repo stars, e.g. blockchain
  whitepapers): stars measure the project, not the document's design, so this would be an
  invented metric.
- **App-output corpora as L1**: the stars of invoicing software measure the software. At most,
  their default quote PDF could be an A1 pool member (a catalogue of fixed designs, native
  metric unused), and only if a preview is at the source.
- **Typst Universe or Overleaf as L1**: neither has a metric, so they are L2 or pool members
  only.

---

## 3. Per-family source plan (ranked by evidence strength)

"Expected" = shippable non-convention designs after this plan. It is an est. range, not a
promise. The target (8–10) is out of reach for all seven families. The Shortfall sections stay,
and should say so plainly.

### memo (today: 0 ranked, 0 L3, MS 7 corroboration only)
| # | Source | Class | Items (raw → est. on-topic) | Notes |
|---|---|---|---|---|
| 1 | **A1 pool:** MS word/memo-templates (7) + Overleaf `tagged/memo` (11 → 4–5) + GitHub `memo+typst` ∪ `topic:memo latex` (16 → 6–7) + Typst Universe memo (2, overlaps GitHub) | L2 pool | est. 17–19 on-topic before codeability | skew: MS = Office editorial; Overleaf/Typst = LaTeX/Typst, academic/technical. A fork of the same template counts once |
| 2 | **AR 25-50** memorandum format | L3 authority | 1 archetype | fetched; figures show the layout |
| 3 | **Purdue OWL** memo format | L3 authority | 1 archetype (if distinct from #2, else merge) | fetched |
| 4 | Tongue & Quill (USAF), SECNAV M-5216.5 | L3 | — | blocked. One retry via a mirror; else "unreachable 2026-09-23" |

Expected: 2–4 ranked from the pool + 1–2 L3 + seeds, so **4–6**.

### form (today: 2 authorities (USWDS, GOV.UK) → 1 archetype)
| # | Source | Class | Items | Notes |
|---|---|---|---|---|
| 1 | **ABS Paper Forms Design Standards 2023** | L3 authority (print) | 1 archetype, likely distinct: boxed 0.5 pt answer boxes, eye-guide lines, split-page columns | fetched. **The first print-form authority.** It addresses Fm.5's caveat that the existing authorities are screen-only |
| 2 | NHS digital service manual (text input) | L3 authority (web) | likely merges into the USWDS/GOV.UK archetype | fetched; adds a provenance row |
| 3 | DSFR, AGDS/GOLD | L3 | — | 403/timeout. One retry each |
| — | MS forms (SPA), LO `q=form` (noise), Typst "form" (keyword noise), Overleaf (no tag) | — | — | no L1/L2 source exists (verified) |

Expected under A3: **2–3** distinct archetypes + seed. Shortfall stays. Record it honestly:
no public source ranks paper-form designs.

### flyer (today: L2 MS N=16, 5 admissible singletons)
| # | Source | Class | Items | Notes |
|---|---|---|---|---|
| 1 | MS Create flyers **extended** with PowerPoint flyers-posters-templates (3 flyers) + Word pamphlet "Teacher appreciation flyer" (if not a duplicate) | L2 (same vendor catalogue, 82a C5) | N 16 → 19–20 | the recount may cross the §4 coarsening trigger (≥15 admissible, >50% singletons) |
| 2 | **A1 pool:** LO `q=flyer` (est. 3) + Typst Universe category flyer (6) + GitHub `flyer+typst` (5; overlaps Typst) | L2 pool | est. 9–12 on-topic | run it only if ≥10 after dedup; else corroboration |

Expected: **3–6** (the dominant uncertainty is how many are admissible, not source count).
No borrowing (not a twin).

### quote (today: 0; cross-listing only)
| # | Source | Class | Items | Notes |
|---|---|---|---|---|
| 1 | **A5 twin borrowing from invoice** | inherits the invoice class | ≤3 | only after invoice ships; C7 re-check |
| 2 | **A1 pool candidate:** quote PDFs of quote-capable invoicing apps from GitHub `topic:invoicing` (IDURAR, Dolibarr, InvoicePlane, SolidInvoice, itflow, bigcapital, frappe/books …) + LO 99480 + GitHub `devis/quotation latex` generators (≤3) + quote items cross-listed (A4) from the invoice MS/LO/GH corpora | L2 pool | est. 4–12 (**codeability unproven**) | time-box 20 min. The preview must be a quote/estimate PDF published at the source (docs or demo), never generated |
| — | Microsoft Create | — | 0 | no quote/estimate category in any app sitemap (verified) |

Expected: **1–4** (mostly borrowed). The Shortfall stays and must name the borrowing.

### one-pager (today: seeds + 1 convention)
| # | Source | Class | Items | Notes |
|---|---|---|---|---|
| 1 | A4 cross-list: MS Word "Executive summary"; "One-page business proposal" / "Simple one page business proposal" only if they pass the one-pager on-topic test (else proposal) | corroboration (<10) | 1–3 | — |
| — | GitHub `one-pager`/`factsheet`, Overleaf, Typst (1 keyword hit), MS fact-sheet slug | — | 0 | verified noise or absent |

Expected: **seeds + 1 convention**, as §10 already says. No structured source exists
(verified 2026-09-23), and borrowing is rejected because it's not a twin. Recommend stating this
in the product as "convention-based" rather than padding.

### infographic (today: seeds + 1 convention)
| # | Source | Class | Items | Notes |
|---|---|---|---|---|
| 1 | **A2 juried pool: Information is Beautiful Awards winners 2022–2024** (`pcategory=winner`) | L2j (Evidence `juried`) | raw ~90; est. 25–45 static on-topic | the on-topic test is essential ("single static composition"). Skew: data-journalism and NGO work, English-dominant, not template-like. Add 2021 if 2022–2024 yields fewer than 10 on-topic |
| 2 | Malofiej winners (print infographics) | L2j/L3 | unknown | the winners-list structure was not verified. One probe allowed |
| 3 | MS PowerPoint infographic-maker (3), LO 99332 (1) | corroboration | 4 | <10 |

Expected: **3–6** from the juried pool + seeds. This is the only thin family where a genuinely
structured (juried) system reaches ≥10 items. Caveat for §8 filling: award winners are bespoke
editorial graphics. The shipped design is a reconstruction of the identity features (§13) and
doesn't imply template-level reproducibility.

### whitepaper (today: 0)
| # | Source | Class | Items | Notes |
|---|---|---|---|---|
| 1 | **A5 twin borrowing from report** | inherits the report class | ≤3 | report ships first. Typeface is refilled per §8 (the whitepaper default typeface differs) |
| 2 | GitHub whitepaper templates (saboyle ★37, mlouhivu ★4, …) + A4 cross-lists | corroboration or A1 pool if ≥10 | est. <5 | specimens (real project whitepapers) are off-topic |
| — | MS (no slug), Overleaf (no tag), Typst (0) | — | 0 | verified absent |

Expected: **1–4** (mostly borrowed).

---

## 4. Proposed amendment text (to append to research/82 §10 as "82b")

> **82b (adopted <date>) — thin-family sources.** Applies to memo, form, flyer, quote,
> one-pager, infographic, whitepaper. Families already coded are unaffected, except that flyer's
> F.1 corpus gains the PowerPoint `flyers-posters-templates` flyer items (same vendor
> catalogue, 82a C5), and flyer must be **recounted** (§4 coarsening re-evaluated).
> Rules A1 (pooled L2), A2 (juried pool), A3 (L3 cap 5 when no ranked evidence, distinct
> archetypes only), A4 (general cross-listing) and A5 (structural-twin borrowing: same default
> Style, Palette and Page Format keys; ≤3; `borrowed:` metric; ranked after own evidence; B's
> admissibility re-applied) are added as written in research/82b §2.
> Per-family source rows replace the §10 rows for these families as in research/82b §3.
> The expected counts are estimates; F2/F3 (§12) apply to every new corpus unchanged. No
> source added here carries a metric that §2 does not already define.
> Twins as of this date: quote←invoice, whitepaper←report. No other pair qualifies.

Families affected by adoption: flyer (recount only). Nothing already shipped is invalidated.

---

## 5. What stays true after 82b

- Even with every source above, **no thin family reaches 8–10** designs. My estimate is memo
  4–6, form 2–3, flyer 3–6, quote 1–4, one-pager 1–2, infographic 3–6, whitepaper 1–4.
- Two of those ranges depend on borrowing (quote, whitepaper), and the product must disclose
  it.
- One-pager and form have **no ranking system anywhere** reachable today. Their lists are
  authority- or convention-based, and that's the honest result.
- Bonus finds outside scope: Word `papers-and-reports` (10 reports) could serve as a new L2
  catalogue for **report**, and PowerPoint `business-proposal-templates` (17) + Word business
  proposals (5) could serve **proposal**. The orchestrator can decide whether to amend those
  rows too.
