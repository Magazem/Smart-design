# One-pager corpus — cross-listed items (82b A4) across every reachable catalogue: **4 on-topic < 10 → corroboration only**

Coder: Design Researcher 3 (Phase 4 first coder; counts, never judges; research/82 §1). Retrieved **2026-09-24**. Binding: research/82 §4, 82a C1-C30, 82a-general (header §A, colour §B), 82b A1/A4.

**Plain result.** Every catalogue reachable today was swept for one-pager items. It yields **4 on-topic items** across 3 sources: 3 in Microsoft Create and 1 in Typst Universe. The A1 pool would be 4, below the floor of ≥10, so **no corpus is formed**: no k/N and no Ranking Metric string. One-pager ships **seed + ≤1 convention**, as research/91 says. The 4 items are listed as corroboration, with codes for information only.

## OP.1 On-topic test (pre-set before any preview was viewed)
An item is **on-topic** iff (a) its own title or description names a one-page purpose: *one-page / one pager, fact sheet, executive summary, one-page brief/proposal, at-a-glance*, or a product *datasheet*; and (b) its preview is a **single page** of that document. Off-topic: CVs "on one page" (cv family), presentations (deck), ML "datasheets for datasets" (multi-section documentation questionnaires), and letters/briefs in the German sense ("Brief" = letter).

## OP.2 Sweep (all `curl -s -L -A "smart-design-research"`, HTTP 200 unless noted)
| Source | Query / method | Raw | On-topic | Notes |
|---|---|---|---|---|
| Microsoft Create, Word + PowerPoint | **All 79 English category pages** listed in the static sitemaps `https://{word,powerpoint}.cloud.microsoft/create/sitemap.xml` (82b §1a method; blog URLs excluded). Every card title was grepped for one-page / fact / summary / brief / glance / sheet / datasheet | 7 matching titles | **3** | Executive summary (business-templates); One-page business proposal and Simple one page business proposal (business-templates + business-proposals, = MSP:003/007 in `proposal-corpus-ms.md`). Off: Product summary presentation (.pptx deck); Fax cover sheet ×2; Meeting sign-in sheet |
| Microsoft Create, Excel | slugs in `https://excel.cloud.microsoft/create/sitemap.xml` | 0 relevant slugs | 0 | balance sheets, timesheets, attendance sheets only |
| LibreOffice Extensions (Templates tag 118, `ord=download_d`) | `q=` fact+sheet, factsheet, one+page, onepage, one-pager, datasheet, executive+summary, brief | 0 / 0 / 12 / 0 / 0 / 0 / 1 / 12 | 0 | "one page" = a calendar + CVs; "executive summary" = 99219, an Impress presentation; "brief" = German letters (Briefvorlage) |
| Overleaf gallery | `tagged/` fact-sheet, factsheet, one-page, one-pager, onepager, data-sheet, brief, policy-brief, executive-summary, summary | 0 each | 0 | tags empty (82b §1e: these tags do not exist) |
| Overleaf gallery | `tagged/datasheet` (5), `tagged/handout` (3) | 8 | 0 | datasheet = "Datasheet for dataset" ×2, MT datasheet, model card (ML documentation), an archaeological site form; handout = landscape brochure, linguistics handout, **"memo-template"** (A4 cross-list → memo, see OP.5) |
| Typst Universe | `https://packages.typst.org/preview/index.json` (1619 packages), latest version, regex over name/description/keywords/categories | 4 | **1** | `isc-hei-exec-summary` 0.8.1 ("Official executive summary for the bachelor thesis", HES-SO); off: `briefs` (letters), `habaneraa-one-page-resume-zh` (cv), `ohdsi-symposium-submission` (paper) |
| GitHub | — | — | — | not run: the GitHub search API belongs to the Design Researcher. 82b §1c already logs `one-pager+latex` (134) and `factsheet+latex` (6) as noise |

**Total on-topic: 4** (MS 3 + Typst 1). A1 needs ≥10 after dedup, so the pool is **not formed**.

## OP.3 Corroboration list (codes for information only, NOT counted; 82a-general applied)
Previews: MS 400×519 webp thumbnails; Typst `…/thumbnails/isc-hei-exec-summary-0.8.1.webp` (992×1403). Colour measured with `measure.py` (temp), rules with `hlines.py`, and declared theme fonts from the .docx (82a C25). Items file: `one-pager-items.csv` (C11).

| id | item | columns | head | body | colour | header | rules | dens | header-note | colour-note | preview |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OPX:001 | [Executive summary](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fcreatecatalog.public.onecdn.static.microsoft%2Fcatalog-assets%2Fen-us%2F1b4c752f-b419-4ae7-850a-9bb757ac1b75%2FTF1b4c752f-b419-4ae7-850a-9bb757ac1b75024a8109-ae47179cf116.docx) (Word business-templates pos 5) | 1 | sans | sans | one-accent | band | none | airy | grey fill behind the title "Executive Summary": width ≈79% of page (≥60%), height ≈ one title line (≤40%) → band | bg #fefefe; blocks 2.34% (<10%); green section headings (hue ≈150°, 5 elements) = one cluster. Declared Candara / Candara | https://createcatalog.public.onecdn.static.microsoft/catalog-assets/en-us/1b4c752f-b419-4ae7-850a-9bb757ac1b75/thumbnails/400/executive-summary-modern-simple-0-1-c7e1e7ac1413.webp |
| OPX:002 | One-page business proposal (= MSP:003) | 1 | sans | sans | fill-blocks | plain-left | none | standard | dark-teal title with a vertical bar, left; no full-width rule | bg #f2ede8; pale-teal left panel = blocks 23.53%. The panel holds only the prepared-for/by contact blocks, so under 82a C28 it makes no column | see `proposal-corpus-ms.md` MSP:003 |
| OPX:003 | Simple one page business proposal (= MSP:007) | 2-equal | serif | serif | mono | ruled | rules | standard | rule at y=200 spans 88% of page width. It lies directly below a 3-line un-headed intro (82a-cv A4, applied via 82a-general §A.2 step 3) → ruled | bg #f9f6f2; blocks 0%; no chromatic cluster meets B5 | see MSP:007 |
| OPX:004 | [isc-hei-exec-summary](https://typst.app/universe/package/isc-hei-exec-summary) 0.8.1 (Typst Universe) | 2-equal | sans | sans | one-accent | plain-left | none | dense | bold sans title top-left; no rule or band | bg white; QR code excluded (B1c) and portrait photo excluded (B1b); magenta-red cluster (300-330°): subtitle, author line, intro paragraph, headings | https://packages.typst.org/preview/thumbnails/isc-hei-exec-summary-0.8.1.webp |

Observation only: 4 items, 4 different archetypes. OPX:002 and OPX:003 are also counted as proposal corroboration (`proposal-corpus-ms.md`). A4 allows an item to be listed for several families, but it only ever counts through a pool.

## OP.4 Consequences for shipping
- **No ranked one-pager design** (no pool, no L1/L2 corpus). No authority for one-pager layout was found or proposed (82b §3). The seeded doctype default stays and at most 1 convention ships (research/82 §10, research/91 row "one-pager").
- These 4 items may corroborate a convention in the release notes. They are not a rate.

## OP.5 Handoffs found during the sweep (A4)
- **Memo:** Overleaf `tagged/handout` contains `https://www.overleaf.com/latex/templates/memo-template/xfgfwnxzcgkf` ("memo-template"). It is not tagged `memo`, so it was not in the memo pool (M.6). Adding it would give N=12 **if** it passes the memo on-topic test (not checked here). The orchestrator decides whether pool membership is by tag query (as run) or by A4 cross-listing.
- **Deck:** MS PowerPoint "Product summary presentation" and LibreOffice 99219 "Consulting Blue - IBM Plex Sans" are presentations, recorded only.

## OP.6 Bias statement
Microsoft = editorial Word selection. The two one-page proposals share the Microsoft cloud-font house style noted in `proposal-corpus-ms.md` P.5. Typst = one university's thesis executive summary. There are no usage metrics. The one-pager genre (fact sheets, product sheets, policy briefs) is almost absent from every public template catalogue reachable on 2026-09-24. Canva, Adobe Express and Google are not reachable (research/82 §13).

## OP.7 Second coder
Nothing is coded as a corpus, so there is nothing to sample (§7).
