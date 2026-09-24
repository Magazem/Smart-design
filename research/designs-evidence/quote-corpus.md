# Quote family: A4 cross-listed items + fresh search (corroboration only) + 82b A5 twin check

Coder: Design Researcher 2. Retrieved **2026-09-25**. I count; I do not judge (research/82 §1).

**Binding rules:**
- research/82 and 82a-clarifications-1 to -5;
- 82a-general for header treatment and colour use;
- 82b-ADOPTED: A1 pool, A4 cross-listing, A5 structural-twin borrowing.

**Scope limits:**
- No git.
- No GitHub search API (another worker holds it). GitHub was used only for raw README/image fetches of named repositories.
- From `invoice-corpus.md` I read only the "Cross-listed `quote` items" section and the item list (`invoice-items.csv`), not the invoice codes.

Items file (C11): `research/designs-evidence/quote-items.csv`.

## Q.0 Result in one paragraph

Across every reachable source, **3 on-topic codeable quote items** exist. That is below the A1 pool floor of 10, so **quote has no corpus**:
- the items are coded below for the record (**corroboration only**);
- no k/N or share is computed;
- quote ships nothing ranked from its own evidence.

The **A5 twin check passes**: `quote-devis` and `invoice-tabular` share Style, Palette and Page Format keys (Q.5). Quote may therefore borrow up to 3 designs from invoice once invoice ships. Each borrowed design must be re-checked against quote admissibility (C7) and labelled `borrowed:invoice:<invoice metric>`.

## Q.1 Sources walked (all 2026-09-25, `curl -sL -A "smart-design-research"`)

| Source | Query / method | Raw hits | On-topic quote items | Codeable |
|---|---|---|---|---|
| **A4 cross-lists from invoice** | `invoice-corpus.md` § "Cross-listed `quote` items" | 3 | 3 | 2 (DeVinci-FabLab, invoice_el); aeoru = dead preview host, uncodeable |
| **Microsoft Create sitemaps** | `https://{word,excel,powerpoint}.cloud.microsoft/create/sitemap.xml` (1200 / 677 / 629 URLs) grepped for `quot|estimat|devis|angebot|offer|bid|tender` | 0 category slugs (only `business-proposals` / `business-proposal-templates`, which belong to the proposal family) | 0 | — |
| **Microsoft Create, all English category pages** | 168 `/create/en/` pages, static payload parsed: **1,168 cards**, titles grepped with the same pattern | 3 titles: "Educational quotes posters", "FIRE estimator", "Savings estimator" | 0 (a poster and two calculators) | — |
| **LibreOffice Extensions** | tag 118 + `q=` quote, quotation, estimate, devis, angebot, offerte, offer, presupuesto, preventivo, kostenvoranschlag, cotizacion, orcamento, proforma, tender; `ord=download_d` | 5 / 1 / 1 / 0 / 1 / 0 / 28 / 0 / 0 / 0 / 0 / 1 / 1 / 1 | 0 (budgets, calculators, CVs, decks, a DIN 676 business letter, a balance sheet). `q=quotation` → 99480 "Festive Event Management Letterhead" is a letterhead (letter family; coded there as LOL:039), not a quote | — |
| **Overleaf gallery tags** | `/gallery/tagged/{quote, quotation, quotations, estimate, offer, devis, angebot, invoice, invoices, business}` | tags `quote`…`angebot`, `invoices`, `business` do **not exist**: each falls back to the default "Journal articles" page. `invoice` = 6 templates | 0 (all 6 invoice-tag titles are invoices) | — |
| **Typst Universe** | `https://packages.typst.org/preview/index.json` (1,619 packages, 818 templates); name/description/keywords/categories grepped for `quot|estimat|devis|angebot|offert|offer|kostenvoranschlag|presupuesto|preventivo|proforma|cotiza|orçamento` | 3 (notionly, pannotyp = "quotes" as punctuation; **tiefletter** = "Invoice and offer template") | 1 (tiefletter's `offer` class) | 1: source README publishes `examples/offer.jpg` |
| **Typst Universe invoice templates** (quote mode?) | the 8 invoice templates' tarballs; README grepped for quote/offer/Angebot/estimate | 8 | 0 new (laskutys "quotes" = string quoting; ledger-rail "Quote INV-…" = sample text; tiefletter already counted) | — |
| **Invoicing apps named in 82b** | raw README of idurar-erp-crm, Dolibarr, InvoicePlane, SolidInvoice, itflow, bigcapital, frappe/books, akaunting | quote support stated by 5 | 0 codeable | 0: READMEs show only app-UI screenshots or no images; no quote/estimate PDF is published at the source (82b: "codeability unproven" is now **confirmed negative**). Time-boxed |
| GitHub `devis/quotation latex` generators (82b est. ≤3) | needs the GitHub search API | — | not walked | out of scope for this worker (disclosed; the GitHub worker may add them) |

Pool size (A1): **3 codeable on-topic items from 2 sources** (GitHub-hosted templates via A4 cross-listing; Typst Universe). That is **< 10**, so the pool is not formed: corroboration only (§2, 82b A1).

## Q.2 On-topic decisions

- **QP:001 tiefletter `offer`.** The class renders an "Angebot" (offer/quote) with its number, date, validity and a priced item table. On-topic. The package's default template/thumbnail is the **invoice** class, so only the README's `examples/offer.jpg` is the quote preview, and that image is what was coded.
- **QP:002 DeVinci-FabLab `templates/devis`.** The source README calls it "Quote template" / "an example of an quote template"; the page is titled **DEVIS**. On-topic. It carries a leftover "Numéro de facture" label (disclosed; the title and the README decide).
- **QP:003 invoice_el.** The rendered page is titled "Προσφορά / Τιμολόγιο" (Quote / Invoice), a dual-purpose scrlttr2 letter. It passes the quote on-topic test (A4). It is also coded in the invoice corpus as GH:068. The families differ, so there is no dedup issue.
- **Not codeable:** aeoru/Business-Central-GST-India-Invoice-Template (dead preview host, per the invoice cross-list note).

## Q.3 Coded items (§4 + 82a-general A/B + C28; quote family features)

Features:
- identity: `columns|heading|colour|header`;
- variants: body, rules/boxes, density, totals position, table rules.

Previews were downloaded to the system temp dir only.

| id | columns | heading | body | colour | header | rules/boxes | density | totals | table rules | adm | measurements / notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| QP:001 | 1 | serif | serif | mono | plain-left | rules | standard | right-bottom | header-and-total | y | **Declared font:** Cormorant Garamond (`document_preset.typ` `set text(font:)`), Google SERIF.<br>**Title:** the banner "Tiefseetauchner" lockup (purple icon + wordmark) is a logo (never the title, B1b), so the title is the largest remaining top-30% text: the right-aligned sender address. No band or full-width rule within the header block; the rule under "Angebot 2024-023" belongs to the meta line after the recipient boundary. → plain-left (`align=right`).<br>**Colour:** purple logo excluded; black text only → mono.<br>**Body:** 1 column; routing blocks don't count (C28). ~33 text lines. Net total right-aligned under the table; rules above and below the table header plus a closing rule. |
| QP:002 | 1 | serif | serif | mono | plain-left | boxes | standard | right-bottom | header-and-total | y | **Title:** "DEVIS" (Times-like bold serif; multicolour FabLab logo excluded).<br>**Header:** the meta block (numbers/dates) sits top-right, ~8 title line-heights above DEVIS, so not split. No band. No full-width rule in the header block (the table's top rule is the boundary) → plain-left.<br>**Colour:** black text; the diagonal "SPECIMEN" watermark is #F2F2F2. **C32:** (a) watermark vs page 1.119:1 (≤ 1.3) and (b) black text vs watermark 18.76:1 (≥ 4.5), both via `contrast_ratio`, so the watermark is ignored → mono.<br>**Rules/boxes:** recipient and signature boxes are bordered → boxes.<br>**Table:** header rule + subtotal/total rules; the items have no row lines → header-and-total (not C7). ~53 text lines. |
| QP:003 | 1 | serif | serif | one-accent | plain-left | rules | standard | other | none | y | LaTeX scrlttr2, Computer Modern (foundry serif).<br>**Columns:** the right sender column (name, activities, address, contacts, tax id, bank) is issuer/routing → never a column (C28) → 1.<br>**Colour:** blue link text in 2 separate elements (e-mail, LinkedIn URL) meets B5 (≥ 2 elements) → one cluster → one-accent. QR code excluded (B1c); grey labels achromatic.<br>**Header:** the DIN-style return-address underline belongs to the recipient block (boundary, A.2 step 3), no band → plain-left.<br>**Table:** no price table on page 1 → totals `other`, table rules `none`. |

Admissibility:
- **A1-A8:** none fire.
- **C7** (all-cells table): none.
- **Codes:** 3 of 3 admissible.

## Q.4 Descriptive tally (presence only; not a share, not a rank; the pool was not formed)

- `1|serif|mono|plain-left`: QP:001, QP:002
- `1|serif|one-accent|plain-left`: QP:003

Skew:
- All 3 are developer-made templates: Typst and LaTeX on GitHub.
- 2 are German/Austrian or French freelancer/association quotes.
- 1 is a Greek dual-purpose letter.
- No office-suite (Microsoft, LibreOffice) quote template exists in any reachable catalogue.

## Q.5 82b A5 structural-twin check (quote ← invoice)

Mechanical check against the shipped data, `skill/document-design-intelligence/data/base/doctypes.csv` → `Reasoning Key` → `doc-reasoning.csv`, read 2026-09-25:

| Key | quote-devis | invoice-tabular | Equal |
|---|---|---|---|
| Style Key (doc-reasoning) | form-grid-underline | form-grid-underline | **yes** |
| Palette Key (doc-reasoning) | print-neutral | print-neutral | **yes** |
| Page Format Key (doctypes) | a4-form-standard | a4-form-standard | **yes** |
| Typeface Key (doc-reasoning; not required by A5) | ofl-public-sans | ofl-public-sans | yes |
| Render Target / Constraint Set (doctypes; informational) | pdf-chromium / report-typography | pdf-chromium / report-typography | yes |
| Structure Key (doctypes; informational, not an A5 key) | quote-standard | invoice-standard | no |

**Result: structural twins (A5 satisfied).** This confirms 82b's table. The only difference is the Structure Key (content outline). A5 does not test it, and borrowing does not touch it.

Consequences for filling (82b A5 (a)-(e)), to be done **after invoice is filled and shipped**:
- (a) Up to **3** invoice designs keep invoice's archetype and fill.
- (b) Each is **re-checked against quote admissibility**. C7 applies to quote exactly as to invoice (all-cells tables fail), so an admissible invoice design stays admissible unless its evidence item was admitted under an invoice-only reading. None is known today.
- (c) Ranking Metric `borrowed:invoice:<invoice's own metric string>`, keeping invoice's Evidence Class.
- (d) Borrowed designs rank after quote's own evidence. Quote has no own ranked evidence, so they occupy ranks 1-3, before any L4 convention.
- (e) Disclosure in this file and in the quote designs table: "borrowed from invoice (structural twin); quote's own catalogue evidence = 3 corroborating items (Q.3), no pool".

The corroborating codes in Q.4 (serif, mono/one-accent, plain-left) are a presence note only; they do not reorder borrowed invoice designs (§6, R-d).

Re-run the key comparison at borrowing time, in case either default row changes before then.

## Q.6 Second-coder ids (C10/C11)
QP:001, QP:002, QP:003 (all coded items; `quote-items.csv`). The family-wide sample formula yields all 3 items (`max(min(10, 3), ceil(0.75)) = 3`).

## Q.7 Shortfall (honesty rule, 82b-ADOPTED)
Quote's own evidence cannot rank anything: 3 items against a floor of 10. The family ships at most **3 borrowed invoice designs + L4 convention**, with the shortfall stated in the designs table and release notes.
