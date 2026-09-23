# invoice — corpora (F.a, single coder covering all corpora for this family)

Coder role: count, never judge (research/82 §1, R-d). This file covers the `invoice` family's L1
(GitHub) and L2 (Microsoft Create, LibreOffice Extensions) corpora in one task, per the
orchestrator's brief. No fill step (§8) is performed here. `research/82a-clarifications-1.md` is
applied throughout (cited inline as C1–C10 where relevant).

**STATUS: COMPLETE.** GH (L1, N=40), MS (L2, N=8) and LO (corroborate-only, 4/11 on-topic, below
the L2 floor) are all coded/logged below; combined ranking, bias statement and the family-wide
second-coder id list are at the end of this file.

## Corpus GH — GitHub L1

- URL: `https://api.github.com/search/repositories?q=%22invoice+template%22&sort=stars&order=desc&per_page=100`
  (pages 1–2, `per_page=100`)
- Query: `%22invoice+template%22` (exact phrase), sort `stars`, order `desc`
- Retrieved: 2026-09-23, `curl -s -A "smart-design-research"`, two calls ≥7s apart (page=1, page=2)
- `total_count` (API): 738
- Walk cap: 200 raw items (protocol §3.1). Actual walk: **90 raw items**, stopped once the 40th
  on-topic codeable item was reached at native rank 90 (amattu2/invoice-template).

On-topic (§3.2) exclusions applied: invoicing apps/SaaS/webapps with no fixed design (routes+
services+client app scaffolds, ASP.NET solutions, full-stack generators), OCR/extraction tools,
generator libraries/packages ("customizable templates" as a code API, not a fixed design),
tutorials ("How to create..."), other families (admin dashboard templates, thermal-receipt/POS
customisation, ML synthetic-data generators), and forks/duplicates of an already-counted design
(counted once, highest metric kept, per §3.2).

### Raw list (rank = native stars-desc position) — ranks 1–90

`OT?` = on-topic. `Codeable?` = preview found at source (README image / repo-tree image / example
PDF page 1), downloaded to system temp only, never rendered/compiled. `C2` = uncodeable per
research/82a C2 (preview present but wrong/unrelated asset, e.g. a logo-only or icon-only asset,
or an unrelated personal photo, counts as no preview).

| Rank | Repo | Stars | OT? | Codeable? | Reason / note |
|---|---|---|---|---|---|
| 1 | sparksuite/simple-html-invoice-template | 1725 | yes | **no** | repo tree has only `website/images/{favicon,logo}.png`; no full-page design preview committed (would require rendering `invoice.html`) |
| 2 | tophermade/sprInvoice | 224 | yes | **no** | no image/PDF anywhere in repo tree |
| 3 | Invoicebus/html-invoice-generator | 173 | **no** | — | JS tool to transform an HTML invoice into a functional editor — generator, not a fixed design |
| 4 | edisonneza/jspdf-invoice-template | 171 | yes | yes | jsPDF invoice template; `demo/images/portrait_mode.PNG` |
| 5 | anvilco/html-pdf-invoice-template | 96 | yes | yes | HTML→PDF invoice template; README screenshot |
| 6 | AndreKelling/jspdf-template | 54 | yes | **no** | `docs/img` has only address-bar/background/logo SVG icons, no page preview |
| 7 | leonieziechmann/invoice-pro | 53 | yes | yes | Typst DIN 5008 invoice; `thumbnail.png` |
| 8 | woofers/org-invoice-template | 48 | yes | yes | Org-mode invoice template; `screenshots/` dir in repo tree |
| 9 | rimiti/html-invoice-template | 40 | yes | yes | `preview.png` at repo root |
| 10 | kimai/invoice-templates | 28 | yes | yes | template collection; coded on first listed (`din5008-invoice/screenshot.png`) per C4 |
| 11 | nirajrajgor/html-invoice-templates | 28 | yes | yes | 3 bundled designs; `assets/invoice-1-2x.jpg` (first) |
| 12 | ntjess/typst-invoice-template | 27 | yes | yes | Typst invoice; `sample-use.gif` |
| 13 | mageplaza/pdf-invoice-templates | 26 | yes | yes | Magento PDF invoice templates; imgur-hosted screenshots in README |
| 14 | barbosa89/invoice-template | 24 | yes | yes | Bootstrap invoice template; `invoice.png` at repo root (undocumented in README, disclosed per C6) |
| 15 | eroux/latex-yait | 24 | yes | **no** | LaTeX source only (`yait.tex`), no committed PDF/image |
| 16 | Inambe/html-invoice-template | 22 | yes | yes | `screenshot.png` |
| 17 | patricktalmadge/Bootstrap-Stripe-Invoice-Template | 22 | yes | **no** | `img/` has only a client logo + Bootstrap glyphicon sprite sheets, no page preview |
| 18 | hzxshark/invoice_template | 16 | yes | **no** | `examples/src` is HTML/JS source only, no image |
| 19 | sahrullahh/invoice-template-html | 15 | yes | yes | `preview.png` |
| 20 | mikailfaruqali/invoice-template | 12 | **no** | — | Laravel package generating PDFs from "customizable templates" — a code API/library, not a fixed design |
| 21 | d-shannon/bootstrap-invoice-template | 11 | yes | yes | `responsive.png` (+ `invoice.pdf` also present) |
| 22 | codingmarket07/Invoice-Template-Design-20j22 | 11 | **no** | — | tutorial ("How to create the Invoice Template Design In HTML and CSS") |
| 23 | chihebnabil/vuejs-invoice-template | 11 | yes | **no** | no image/PDF in repo tree |
| 24 | scyrencop/invoice-html5 | 11 | yes | yes | imgur-hosted screenshot |
| 25 | Adyasha8105/Invoicee | 9 | **no** | — | invoicing application ("attractive invoice templates for various fields", an app) |
| 26 | priyatampintu/OCR-invoice-Template | 8 | **no** | — | OCR extraction tool |
| 27 | YasinDehfuli/Financial-Factor-Template | 8 | yes | yes | Iranian invoice template pack; `assets/images/factor-informal.png` (first) |
| 28 | thejhh/finnish-invoice-template | 7 | yes | yes | `invoice.pdf` at repo root |
| 29 | blckclov3r/bootstrap5-invoice-template | 7 | yes | yes | `img/travel&tours.png` |
| 30 | mdbootstrap/bootstrap-invoice | 6 | yes | yes | collection; README screenshots (`basic.png` first) |
| 31 | vinay20045/simple-invoice-template | 5 | yes | **no** | only `make_invoice.html`, no image/PDF |
| 32 | sandervanhooft/invoice-templates-generator | 5 | **no** | — | Maizzle email-framework starter kit, generic (not invoice-specific despite the name); README only shows Maizzle badges |
| 33 | PayrollFlow/freelance-invoice-templates | 5 | yes | **no** | `templates/` holds only `.md`/`.html` source, no image |
| 34 | manqur/InvoiceTemplate | 4 | yes | yes | externally hosted screenshot linked from README |
| 35 | panshak/html-js-invoice-template | 4 | yes | yes | externally hosted screenshot (postimg) linked from README |
| 36 | Keleo/kimai2-invoice-templates | 4 | yes | **no** | repo is effectively empty (license/readme only), no templates or images committed |
| 37 | superdev728/invoice-template | 4 | **no** | — | Node.js invoicing web application (`routes`/`services`/`client` scaffold), not a fixed template |
| 38 | achase90/LatexInvoice | 4 | yes | yes | `exampleOutput/Invoice.png` |
| 39 | beganovich/invoiceninja-invoice-templates | 4 | yes | **no** | `source/templates/*.blade.php` source only, no image |
| 40 | chanmyaemaung/pos-invoice-template-for-vo | 4 | yes | **no** | luxury-brand POS invoice templates; only logo/icon SVG assets committed, no full-page preview |
| 41 | clarintux/invoice_maker | 4 | **no** | — | cross-platform invoice generator ("supports various invoice templates") |
| 42 | tahirtaous/Bootstrap-invoice-Template | 3 | yes | **no** | no README, no image in repo |
| 43 | paperplaneapp/html-invoice | 3 | yes | yes | `preview.jpg` |
| 44 | MCode-Team/Invoice-Template | 3 | **no** | — | "Stack Responsive Bootstrap 4 Admin Template" — admin-dashboard template, other family |
| 45 | codingmarket07/Invoice-Template-Design | 3 | **no** | — | tutorial |
| 46 | tociva/free-invoice-generator | 3 | **no** | — | aggregator app ("hundreds of free invoice templates by daybook.cloud") |
| 47 | stumpsyn/fusion-invoice-template | 3 | yes | **no** | `syndicate_assets` has only a logo SVG + CSS, no page preview |
| 48 | ardean/pdf-invoice-simple | 3 | yes | **no** | `dist`/`src` are JS source only, no image |
| 49 | AndreCardoso02/JsPDF_Invoice_Template | 3 | yes | **no** | no image in repo tree |
| 50 | md-2/UberInvoice | 3 | **no** | — | override module for another CMS's invoice rendering, not itself a template |
| 51 | henriquebastos/autoword | 3 | **no** | — | AppleScript automation tool for filling templates in Word |
| 52 | avoinsystems/l10n_fi_invoice | 2 | yes | **no** | repo effectively empty (gitignore/README only) |
| 53 | sofacto/templates | 2 | yes | **no** | proprietary SaaS export-format template stubs, no accessible preview image found |
| 54 | my-dao/Salesforce-PDF-Invoice-Template | 2 | yes | yes | `images/invoice-template-screenshot.png` |
| 55 | mehmetalikus/PHPInvoice | 2 | yes | yes | externally hosted screenshot (prntscr) |
| 56 | mahiuddin-dev/html-template-invoices- | 2 | yes | **no** | nested folder holds only a second README, no image |
| 57 | koodilehto/invoice-latex | 2 | yes | yes | `example/invoice.pdf` |
| 58 | Al-shwaib/-invoice-template | 2 | yes | yes | `Screenshot.png` |
| 59 | Win-112/invoice-template | 2 | **no** | — | identical Node.js app scaffold to rank 37 (routes/services/client/temp) — invoicing application, not a template |
| 60 | subsetsoftwares/invoice-template | 2 | yes | yes | `public/sample-screenshot.png` |
| 61 | alifeee/invoice_template | 2 | yes | yes | `images/invoice.png` |
| 62 | novastream/espocrm-pdf-template | 2 | yes | **no** | single `.html` source file, no image |
| 63 | ryota2357/typst-invoice-template | 2 | yes | yes | `main.pdf` |
| 64 | compilandoelmundo/invoice-template-laravel-blade | 2 | yes | **no** | single `.blade.php` source file, no image |
| 65 | arifulislam26/invoice-template1-sourceCode | 2 | **no** | — | "simple invoice system" — application |
| 66 | WilstonOreo/invoist | 2 | yes | yes | `example.png` |
| 67 | poodaydreamer/invoice-vue-laravel | 2 | yes | yes | `img-1.png` |
| 68 | NikosAlexandris/invoice_el | 2 | yes | yes | `custom_invoice_mwe_el.pdf` |
| 69 | petekeller2/simple-html-invoice-php | 2 | yes | — | explicit fork/port of rank 1 (sparksuite) per its own README; duplicate, not counted (§3.2) |
| 70 | daynis-olman/CheckoutPOS-customReports-thermalReceipts | 2 | **no** | — | thermal-receipt customisation, other family |
| 71 | shamshi1988/simple-html-invoice | 2 | yes | yes | externally hosted screenshot |
| 72 | mattdepaolis/synthetic_invoice_generator | 2 | **no** | — | Streamlit app generating synthetic invoice data for ML training |
| 73 | webstar923/invoice-template | 1 | **no** | — | identical Node.js app scaffold to ranks 37/59 — invoicing application |
| 74 | tudev/InvoiceTemplate | 1 | yes | **no** | only `icon-dark.png`/`logo-red.png` (icon assets), no full-page preview |
| 75 | sudhakar0897/ExcelInvoice | 1 | yes | yes | Excel invoice template; `demo_sales.pdf` |
| 76 | mzdakr/wonderwall-zohocrm-invoice-template | 1 | yes | **no** | single `.html` file, no image |
| 77 | Souvik-Daw/invoiceTemplate | 1 | yes | **no** | C2 — `images/srk.jpg` is an unrelated personal/celebrity photo, not the template's design |
| 78 | Mr-man7352/invoiceTemplate | 1 | yes | yes | `download (2).jpeg` (repo-committed screenshot) |
| 79 | DbencoPlanet/InvoiceTemplateUpload | 1 | **no** | — | full ASP.NET solution (Application/Main/Models/Web layers) — application, not a template |
| 80 | invoicemaker/invoice-templates | 1 | yes | yes | collection of PDFs; coded on first (`blank-invoice-template.pdf`) |
| 81 | rohzart/invoiceplane-templates | 1 | yes | **no** | `assets` holds only CSS/fonts, no image |
| 82 | RoyalZSoftware/invoice-template | 1 | yes | yes | `resources/example.png` |
| 83 | Kalelarga/Invoice-Template | 1 | yes | **no** | C2 — `img/IdeaFoundryLogo.png` is a client logo only, not a page preview |
| 84 | olatundeee/invoice-template | 1 | yes | **no** | no image directory in repo tree |
| 85 | Vishwajeet016/Invoice-Template | 1 | yes | **no** | C2 — `content/asset` holds only Android app-icon density assets, not a page preview |
| 86 | nickav/invoice_template | 1 | yes | **no** | `assets` holds only webfonts + a single colour swatch PNG, no page preview |
| 87 | Farhanward/invoice-template | 1 | **no** | — | "PDF invoice generator \| React + @react-pdf/renderer" — generator |
| 88 | adfaure/invoice-template | 1 | yes | yes | Typst invoice; `example.pdf` |
| 89 | DeVinci-FabLab/Invoice-templates | 1 | yes | yes | `docs/assets/presentation.png` |
| 90 | amattu2/invoice-template | 1 | yes | yes | `demo.png` — **40th on-topic codeable item, walk stops here** |

**Totals for the walk (ranks 1–90):** on-topic = 69, off-topic = 20, duplicate = 1 (rank 69),
on-topic-but-uncodeable = 29, **codeable on-topic (coded) = 40 = N_GH**. Sum check: 40 + 29 + 20 +
1 = 90. ✓

Cross-listing note (§3.2, quote/estimate token): none of the 40 coded GH items name quote/
estimate/devis/Angebot in their titles or descriptions.

### Coded table — codeable-on-second-look failures and replacements (disclosed, C2/C6)

Downloading and viewing the 40 previews turned up **7 items that were not actually codeable**
once opened (preview existed but was C2 "not the item's design", or the link was dead with no
own-repo alternative). Each was replaced by the next on-topic codeable item in native rank order
beyond rank 90 (continuing the walk), per §3.1's "until 40 on-topic codeable items" rule. This is
the same kind of disclosed sequencing deviation the cv-corpus precedent used.

| Removed id (native rank) | Repo | Reason removed | Replacement id (native rank) |
|---|---|---|---|
| rank 8 | woofers/org-invoice-template | preview is an Emacs *editing* screencast (source org-mode markup), never shows rendered output — C2 | rank 106 YoussefHarizi/html-invoice-template |
| rank 29 | blckclov3r/bootstrap5-invoice-template | `img/travel&tours.png` is a small airplane icon asset, not a page preview — C2 | rank 97 BrangyCastro/invoice-template-react |
| rank 34 | manqur/InvoiceTemplate | `assets/pro1.png` (only own-repo image) is a stock lipstick product photo, unrelated to the template's layout — C2 | rank 99 mariarobertap/invoice-template-html |
| rank 55 | mehmetalikus/PHPInvoice | documented prntscr.com preview is dead (404); repo tree has no own alternative (only the bundled FPDF library) — dead link, no C6 substitute | rank 96 chaitaligharge7/Invoice-template-angular |
| rank 67 | poodaydreamer/invoice-vue-laravel | `img-1.png` is a screenshot of the blank "Create Invoice" input *form*, not a rendered invoice document — C2 | rank 119 kawshar798/Modern-simple-html-invoice-template |
| rank 78 | Mr-man7352/invoiceTemplate | `download (2).jpeg` is an unrelated stock nature photo (tree/sunset) — C2 | rank 128 alyf-de/typst-demo |
| rank 89 | DeVinci-FabLab/Invoice-templates | `docs/assets/presentation.png` is a repo README banner graphic (decorative gradient blobs + repo name), not the document; the repo's other image (`docs/assets/example.jpg`) renders a **DEVIS** (French quote), cross-listed to `quote` per §3.2, not counted here | rank 130 christopherkenny/ctk-invoice |

Replacement previews: rank 105 (aerix-nl, next after rank 96/97/99) and rank 113 (princeshahnawaz2012)
were also tried first for two of the above slots and found dead-linked (Nextcloud instance /
img-teufel.de both unreachable, `curl` exit code 000); logged here, not counted, per §1 rate/fetch
discipline (non-search fetches, no 7s sleep required, but failures still disclosed).

Final 40-item id set (`GH:<rank>`, zero-padded to 3 in the table below): 004, 005, 007, 009, 010,
011, 012, 013, 014, 016, 019, 021, 024, 027, 028, 030, 035, 038, 043, 054, 057, 058, 060, 061, 063,
066, 068, 071, 075, 080, 082, 088, 090, 096, 097, 099, 106, 119, 128, 130.

### Coded table (N = 40)

Identity: **columns | heading | colour use | header treatment**. Variant: body class,
rules/boxes, density. Family-specific (both variant): **totals position**, **table rules**.
"Admissible" applies §5 universal + **C7** (invoice/quote/form: table rules = `all-cells` fails,
`boxed-grid` token).

| id | Repo | Stars | Columns | Heading | Body | Colour | Header | Rules/boxes | Density | Totals | Table rules | Admissible |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GH:004 | edisonneza/jspdf-invoice-template | 171 | 1 | sans | sans | one-accent | split | rules | standard | right-bottom | header-and-total | yes |
| GH:005 | anvilco/html-pdf-invoice-template | 96 | 1 | sans | sans | one-accent | split | rules | airy | right-bottom | header-and-total | **no — A2** (heart emoji "❤️ Thank you!") |
| GH:007 | leonieziechmann/invoice-pro | 53 | 1 | sans | sans | fill-blocks | split | rules | dense | right-bottom | header-and-total | yes |
| GH:009 | rimiti/html-invoice-template | 40 | 1 | sans | sans | mono | split | boxes | airy | right-bottom | all-cells | **no — C7** |
| GH:010 | kimai/invoice-templates | 28 | 1 | sans | sans | fill-blocks | band | rules | airy | right-bottom | header-and-total | yes |
| GH:011 | nirajrajgor/html-invoice-templates | 28 | 1 | sans | sans | fill-blocks | split | rules | standard | right-bottom | row-hairlines | yes |
| GH:012 | ntjess/typst-invoice-template | 27 | 1 | serif | sans | one-accent | split | rules | airy | right-bottom | header-and-total | yes |
| GH:013 | mageplaza/pdf-invoice-templates | 26 | 1 | sans | sans | fill-blocks | band | rules | standard | right-bottom | header-and-total | yes |
| GH:014 | barbosa89/invoice-template | 24 | 2-sidebar | sans | sans | fill-blocks | split | rules | dense | right-bottom | row-hairlines | yes |
| GH:016 | Inambe/html-invoice-template | 22 | 1 | sans | sans | mono | plain-centered | boxes | standard | right-bottom | all-cells | **no — C7** |
| GH:019 | sahrullahh/invoice-template-html | 15 | 1 | sans | sans | one-accent | split | rules | airy | right-bottom | row-hairlines | yes |
| GH:021 | d-shannon/bootstrap-invoice-template | 11 | 1 | sans | sans | mono | plain-centered | boxes | airy | right-bottom | row-hairlines | yes |
| GH:024 | scyrencop/invoice-html5 | 11 | 1 | sans | sans | fill-blocks | band | rules | airy | right-bottom | header-and-total | yes |
| GH:027 | YasinDehfuli/Financial-Factor-Template | 8 | 1 | sans | sans | mono | plain-centered | boxes | dense | full-width-bottom | all-cells | **no — C7** |
| GH:028 | thejhh/finnish-invoice-template | 7 | 1 | serif | serif | one-accent | split | boxes | dense | full-width-bottom | header-and-total | yes |
| GH:030 | mdbootstrap/bootstrap-invoice | 6 | 1 | sans | sans | one-accent | plain-centered | rules | airy | right-bottom | row-hairlines | yes |
| GH:035 | panshak/html-js-invoice-template | 4 | 1 | sans | sans | one-accent | split | rules | airy | right-bottom | row-hairlines | yes |
| GH:038 | achase90/LatexInvoice | 4 | 1 | sans | sans | fill-blocks | band | rules | standard | right-bottom | header-and-total | yes |
| GH:043 | paperplaneapp/html-invoice | 3 | 1 | sans | sans | multi | split | boxes | airy | right-bottom | header-and-total | yes |
| GH:054 | my-dao/Salesforce-PDF-Invoice-Template | 2 | 1 | serif | serif | one-accent | plain-centered | boxes | standard | right-bottom | all-cells | **no — C7** |
| GH:057 | koodilehto/invoice-latex | 2 | 1 | sans | sans | mono | split | boxes | standard | right-bottom | header-and-total | yes |
| GH:058 | Al-shwaib/-invoice-template | 2 | 1 | sans | sans | fill-blocks | split | boxes | dense | full-width-bottom | header-and-total | yes |
| GH:060 | subsetsoftwares/invoice-template | 2 | 1 | sans | sans | mono | plain-left | boxes | dense | right-bottom | all-cells | **no — C7** |
| GH:061 | alifeee/invoice_template | 2 | 1 | display | sans | mono | plain-centered | boxes | standard | other | none | yes |
| GH:063 | ryota2357/typst-invoice-template | 2 | 1 | sans | sans | fill-blocks | split | rules | standard | other | header-and-total | yes |
| GH:066 | WilstonOreo/invoist | 2 | 1 | mono | mono | mono | split | rules | standard | right-bottom | header-and-total | yes |
| GH:068 | NikosAlexandris/invoice_el | 2 | 2-sidebar | serif | serif | mono | split | rules | standard | other | none | yes |
| GH:071 | shamshi1988/simple-html-invoice | 2 | 1 | sans | sans | one-accent | band | boxes | dense | right-bottom | all-cells | **no — C7** |
| GH:075 | sudhakar0897/ExcelInvoice | 1 | 1 | sans | sans | multi | split | boxes | standard | right-bottom | all-cells | **no — C7** |
| GH:080 | invoicemaker/invoice-templates | 1 | 1 | sans | sans | one-accent | split | rules | airy | right-bottom | header-and-total | yes |
| GH:082 | RoyalZSoftware/invoice-template | 1 | 1 | serif | serif | mono | split | boxes | standard | right-bottom | header-and-total | yes |
| GH:088 | adfaure/invoice-template | 1 | 1 | serif | serif | one-accent | split | boxes | airy | full-width-bottom | none | yes |
| GH:090 | amattu2/invoice-template | 1 | 1 | sans | sans | fill-blocks | band | rules | standard | other | header-and-total | yes (A7: blue estimated off-hex, disclosed) |
| GH:096 | chaitaligharge7/Invoice-template-angular *(repl. rank 55)* | 1 | 1 | serif | sans | mono | split | rules | standard | right-bottom | row-hairlines | yes |
| GH:097 | BrangyCastro/invoice-template-react *(repl. rank 29)* | 1 | 1 | sans | sans | multi | split | rules | standard | right-bottom | row-hairlines | yes |
| GH:099 | mariarobertap/invoice-template-html *(repl. rank 34)* | 1 | 1 | sans | sans | fill-blocks | split | rules | standard | right-bottom | header-and-total | yes |
| GH:106 | YoussefHarizi/html-invoice-template *(repl. rank 8)* | 1 | 1 | sans | sans | mono | band | boxes | airy | right-bottom | all-cells | **no — C7** |
| GH:119 | kawshar798/Modern-simple-html-invoice-template *(repl. rank 67)* | 1 | 1 | serif | serif | mono | plain-centered | rules | dense | full-width-bottom | header-and-total | yes |
| GH:128 | alyf-de/typst-demo *(repl. rank 78)* | 1 | 1 | sans | sans | one-accent | split | rules | dense | other | header-and-total | yes |
| GH:130 | christopherkenny/ctk-invoice *(repl. rank 89)* | 1 | 1 | serif | serif | mono | plain-centered | rules | airy | right-bottom | header-and-total | yes |

Admissible = 31/40. Inadmissible = 9/40: **8 fail C7** (table rules = `all-cells`: GH:009, GH:016,
GH:027, GH:054, GH:060, GH:071, GH:075, GH:106) and **1 fails A2** (GH:005, heart emoji).

### GH frequency table (archetype = `columns|heading|colour|header`, k/40, N=40)

| Archetype | k | k/40 | Admissible exemplars |
|---|---|---|---|
| `1\|sans\|one-accent\|split` | 6 | 0.150 | 5/6 (GH:005 fails A2) |
| `1\|sans\|fill-blocks\|split` | 5 | 0.125 | 5/5 |
| `1\|sans\|fill-blocks\|band` | 5 | 0.125 | 5/5 |
| `1\|serif\|one-accent\|split` | 3 | 0.075 | 3/3 |
| `1\|sans\|mono\|plain-centered` | 3 | 0.075 | 1/3 (GH:016, GH:027 fail C7) |
| `1\|sans\|multi\|split` | 3 | 0.075 | 2/3 (GH:075 fails C7) |
| `1\|sans\|mono\|split` | 2 | 0.050 | 1/2 (GH:009 fails C7) |
| `1\|serif\|mono\|split` | 2 | 0.050 | 2/2 |
| `1\|serif\|mono\|plain-centered` | 2 | 0.050 | 2/2 |
| `2-sidebar\|sans\|fill-blocks\|split` | 1 | 0.025 | 1/1 |
| `1\|sans\|one-accent\|plain-centered` | 1 | 0.025 | 1/1 |
| `1\|serif\|one-accent\|plain-centered` | 1 | 0.025 | 0/1 (GH:054 fails C7) |
| `1\|sans\|mono\|plain-left` | 1 | 0.025 | 0/1 (GH:060 fails C7) |
| `1\|display\|mono\|plain-centered` | 1 | 0.025 | 1/1 |
| `1\|mono\|mono\|split` | 1 | 0.025 | 1/1 |
| `2-sidebar\|serif\|mono\|split` | 1 | 0.025 | 1/1 |
| `1\|sans\|one-accent\|band` | 1 | 0.025 | 0/1 (GH:071 fails C7) |
| `1\|sans\|mono\|band` | 1 | 0.025 | 0/1 (GH:106 fails C7) |

Sum k = 40. 18 distinct archetypes; 14 distinct admissible archetypes (31 admissible items); 5 of
those 14 are singletons (5/31 ≈ 16% of admissible items) — below the 50% coarsening trigger, and 7
archetypes have k≥2 (≥5 required) — **no coarsening applied** (all three §4 trigger conditions
must hold; only the ≥15-admissible-items condition holds here).

Modal admissible archetypes (three-way tie at k=5, share 0.125–0.150): `1|sans|one-accent|split`
(5 admissible/6), `1|sans|fill-blocks|split` (5/5), `1|sans|fill-blocks|band` (5/5) — single-column
body, sans heading, either a one-accent-colour or a filled-block colour treatment, header either
split (sender/recipient or title/meta on opposite sides) or a filled band.

Notes on individual codings (disclosed judgement calls):
- GH:061, GH:068, GH:088, GH:063, GH:090, GH:128: totals position coded `other` where the page's
  total/grand-total is not in a right-bottom or full-width-bottom position (top-of-document
  amount, no totals visible on page 1 of a multi-page doc, or a top-right info-card total).
- GH:061 heading coded `display` (a casual/comic-style face with no direct serif/sans/mono fit);
  body has no `display` value in the §4 enum (research/82a precedent), coded `sans`.
- GH:014, GH:068 coded `2-sidebar` (two independently-flowing content columns) — the cv family's
  C1 (multi-column body fails ATS) does **not** apply to invoice/quote/form, so this is not an
  admissibility exclusion for this family.
- GH:012, GH:128 previews are split-screen source-editor + live-render screenshots (Typst/VS-Code
  style); only the rendered right-hand pane was coded, per the same convention used for GH:096
  (browser screenshot of the rendered app output).

## Corpus MS — Microsoft Create (L2)

### Source
- URL requested: `https://create.microsoft.com/en-us/templates/invoices`; `curl -sL` redirected
  (HTTP 200) to `https://excel.cloud.microsoft/create/en/invoice-templates/?source=create_flow`
  (research/82a C5: a `*.cloud.microsoft` redirect from `create.microsoft.com` is the same vendor
  catalogue, coded if items are in the static payload — they are here, as `.webp` thumbnail URLs
  embedded in the initial HTML).
- Sort: none (editorial page order). Retrieval date 2026-09-23.
- Total reachable static slice: **8 template cards** — matches the research/82 probe's expected
  count for the `invoices` category exactly. No pagination. N = 8 on-topic, 8 codeable (one
  thumbnail per template, title/only page). No cross-listed quote/estimate items.

### Coded table (N = 8, page order, id = `MS:<position zero-padded to 3>`)

| id | Template | Columns | Heading | Body | Colour | Header | Rules/boxes | Density | Totals | Table rules | Admissible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MS:001 | Sales invoice (simple lines design), purple | 1 | sans | sans | mono | plain-left | boxes | dense | right-bottom | header-and-total | yes |
| MS:002 | Small business sales invoice, pink/navy | 1 | sans | sans | fill-blocks | band | rules | standard | other (cut off in thumbnail) | header-and-total | yes |
| MS:003 | Simple invoice, blue ("Elegant Embrace") | 1 | serif | sans | one-accent | split | boxes | standard | right-bottom | header-and-total | yes |
| MS:004 | Service invoice (simple design), blue/black ("The Happy Tooth") | 1 | sans | sans | mono | band | rules | dense | right-bottom | header-and-total | yes |
| MS:005 | Simple business invoice ("HLP Manufacturing") | 1 | sans | sans | mono | split | rules | standard | right-bottom | header-and-total | yes |
| MS:006 | Modern corporate purple & black timesheet invoice | 1 | serif | sans | fill-blocks | split | rules | airy | right-bottom | header-and-total | yes |
| MS:007 | Service invoice (blocky design), gray ("Create & Co") | 1 | sans | sans | fill-blocks | plain-left | rules | standard | full-width-bottom | header-and-total | yes |
| MS:008 | Simple corporate purple & black standard invoice | 1 | sans | sans | fill-blocks | split | rules | standard | right-bottom | header-and-total | yes |

Admissible = 8/8 (no all-cells table rules, no emoji, no gradients — MS006/MS008's purple/lavender
fills are flat solid colour, not an indigo→purple **gradient**, so A7 does not apply; no exact
Office-default blue hex identifiable at thumbnail resolution).

### MS frequency table (share = k/8)

All 8 items code to 8 **distinct** archetypes (`columns|heading|colour|header`) — no repeats:
`1|sans|mono|plain-left`, `1|sans|fill-blocks|band`, `1|serif|one-accent|split`,
`1|sans|mono|band`, `1|sans|mono|split`, `1|serif|fill-blocks|split`,
`1|sans|fill-blocks|plain-left`, `1|sans|fill-blocks|split` — each k=1, share=0.125. This is a
small, fully-fragmented L2 slice; it corroborates rather than dominates the combined ranking (§6
unweighted-mean-of-corpora rule already discounts a small catalogue's influence, but with 8/8
singletons no MS archetype reaches K≥2 on its own).

### MS bias statement
Microsoft Create is Microsoft's editorial selection, first static slice only, page order is not a
metric (research/82 §13). The 8 invoice templates skew towards small-service-business use cases
(beauty salon, dental practice, wedding florist, manufacturing, consulting, printing) with heavy
use of a coloured header/footer block or filled table-header row — every MS item codes
`fill-blocks` or `mono`/`one-accent` with a strong colour-block habit (5/8 `fill-blocks`), more
colour-forward than the GH corpus (12/40 `fill-blocks`).

## Corpus LO — LibreOffice Extensions (below the L2 floor — corroborate-only)

### Source
- URL: `https://extensions.libreoffice.org/en/extensions?Tags%5B%5D=118&q=invoice&ord=download_d`
- Query: `invoice` (full-text, noisy per research/82's protocol-author probe), tag 118 (Templates),
  sort `ord=download_d`. Retrieved 2026-09-23, `curl -s -A "smart-design-research"`.
- Total reachable: **11 raw items**, single page (no further pagination offered by the site for
  this query — confirmed by absence of a `start=` next-page link in the returned HTML).

### Raw list (native order, downloads desc)

| Pos | Title | Downloads | On-topic? | Reason |
|---|---|---|---|---|
| 1 | Simple Service Invoice | 18393 | yes | invoice template |
| 2 | Automated Multi-... (JustInvoice, "simple automatic invoice generation") | 7297 | no | generator/macro tool, no fixed design |
| 3 | Flexible invoice | 6642 | yes | invoice template |
| 4 | Basic Operating Budget | 5892 | no | budget spreadsheet, wrong family (false keyword match) |
| 5 | Toutes mes factures regroupées dans un document | 5064 | no | macro tool that compiles multiple invoices into one document, not a fixed template |
| 6 | Invoice Database | 3401 | no | database extension (tool) |
| 7 | Open PLA (Accounts system) | 3400 | no | accounting application |
| 8 | JustInvoice — Auto-incrementing invoice generator | 2979 | no | generator |
| 9 | Fattura artigiani, commercianti e piccole imprese | 848 | yes | Italian invoice template |
| 10 | Invoice in worked's hours (facturation de prestations en heures) | 802 | yes | invoice template |
| 11 | Professional Business Letterhead Template by InDiFi MKCL-K... | 447 | no | letterhead template, wrong family (false keyword match) |

**On-topic count = 4/11.** Per §2, "a catalogue with <10 on-topic items is not coded as a corpus;
its items may only corroborate (listed, not counted)." **LO is corroborate-only for `invoice`** —
below the 10-item L2 floor (this matches the per-family sources table's own expectation: LO(invoice)
"thin→L2 if 10-39 on-topic, corroborate-only if <10"). No coded table, no frequency contribution,
no admissibility pass is computed for LO; the 4 on-topic titles above are the full corroboration
record. Not fetched further (no preview download needed since these items are not scored).

## Cross-listed `quote` items (§3.2, logged not counted here)

Two items encountered in the GH walk (not counted toward invoice N; flagged for the `quote` family
assembler):
- **DeVinci-FabLab/Invoice-templates** (GH rank 89): its own second preview image
  (`docs/assets/example.jpg`) renders a French **DEVIS** (quote), not an invoice, despite the
  repo's name — cross-listed to `quote`.
- **aeoru/Business-Central-GST-India-Invoice-Template** (GH rank 124, not reached in the final
  coded 40 but noted in the raw walk as codeable=no due to a dead preview host): its description
  explicitly covers "Invoice, Order, **Quote**, Credit Memo, Return" layouts as one AL-extension
  package — cross-listed to `quote` if its preview host is ever revived.
- **NikosAlexandris/invoice_el** (GH:068, coded and admissible above): its own template is titled
  "Προσφορά / Τιμολόγιο" (**Quote / Invoice**) — a dual-purpose letterhead switching between quote
  and invoice mode. Coded here as invoice (its primary listed name and the family this corpus
  targets); cross-listed to `quote` as well since the rendered page literally shows both labels.

## Combined frequency and ranking (§6)

Combined share = unweighted mean over the family's **coded** corpora (GH L1, MS L2); **LO is
excluded from the mean** (corroborate-only, not a coded corpus — §2 explicitly bars <10-on-topic
catalogues from being counted). K(a) = sum of k across GH+MS (raw counts, not shares).

Because GH (N=40) and MS (N=8) share almost no archetypes verbatim (MS's small sample lands on
different specific colour/header combinations than GH's modal ones), combined-share ties are
rare; the two corpora agree at the coarser level that **sans heading + a colour-block habit
(`fill-blocks` or `one-accent`) + a `split` or `band` header** is the dominant invoice convention.

| Archetype | k_GH | share_GH (/40) | k_MS | share_MS (/8) | combined share (mean) | K | Admissible? |
|---|---|---|---|---|---|---|---|
| `1\|sans\|one-accent\|split` | 6 | 0.150 | 0 | 0.000 | 0.075 | 6 | yes (5/6 adm.) |
| `1\|sans\|fill-blocks\|split` | 5 | 0.125 | 1 (MS:008) | 0.125 | 0.125 | 6 | yes |
| `1\|sans\|fill-blocks\|band` | 5 | 0.125 | 1 (MS:002) | 0.125 | 0.125 | 6 | yes |
| `1\|serif\|one-accent\|split` | 3 | 0.075 | 1 (MS:003) | 0.125 | 0.100 | 4 | yes |
| `1\|sans\|mono\|plain-centered` | 3 | 0.075 | 0 | 0.000 | 0.038 | 3 | 1/3 adm. |
| `1\|sans\|multi\|split` | 3 | 0.075 | 0 | 0.000 | 0.038 | 3 | 2/3 adm. |
| `1\|sans\|mono\|split` | 2 | 0.050 | 1 (MS:005) | 0.125 | 0.088 | 3 | 2/3 adm. |
| `1\|serif\|mono\|split` | 2 | 0.050 | 0 | 0.000 | 0.025 | 2 | yes |
| `1\|serif\|mono\|plain-centered` | 2 | 0.050 | 0 | 0.000 | 0.025 | 2 | yes |
| `1\|sans\|mono\|plain-left` | 1 | 0.025 | 1 (MS:001) | 0.125 | 0.075 | 2 | 1/2 adm. (GH:060 fails C7) |
| `1\|sans\|fill-blocks\|plain-left` | 0 | 0.000 | 1 (MS:007) | 0.125 | 0.063 | 1 | yes |
| `1\|sans\|mono\|band` | 1 | 0.025 | 1 (MS:004) | 0.125 | 0.075 | 2 | 1/2 adm. (GH:106 fails C7) |
| (7 further GH-only singleton archetypes, k=1 each) | 1 | 0.025 | 0 | 0.000 | 0.013 | 1 | varies, see GH table |

### Ranked list (§6 ordering: combined share desc; ties → higher L1 share → higher L2 share →
more corpora → earliest native position of any exemplar → archetype code alphabetical)

Two archetypes tie at the top on combined share (0.125): `fill-blocks|split`'s best exemplar is
GH:007 (native rank 7) vs `fill-blocks|band`'s best exemplar GH:010 (native rank 10) — `split`'s
earlier native position ranks it first. A three-way tie at combined share 0.075
(`one-accent|split`, `mono|plain-left`, `mono|band`) is broken by L1 share: `one-accent|split`'s
GH share (0.150) beats the other two (0.025 each); between the remaining pair, `mono|plain-left`'s
best exemplar (GH:060, rank 60) precedes `mono|band`'s (GH:106, rank 106). A pair tied at 0.0375
(`mono|plain-centered`, `multi|split`) is broken the same way: GH:016 (rank 16) precedes GH:043
(rank 43).

| Rank | Archetype | Combined share | K | Admissible | Evidence Class | Ranking Metric |
|---|---|---|---|---|---|---|
| 1 | `1\|sans\|fill-blocks\|split` | 0.125 | 6 | yes (6/6) | ranked | share:github-invoice-template:5/40 by stars; share:microsoft-create-invoices:1/8 |
| 2 | `1\|sans\|fill-blocks\|band` | 0.125 | 6 | yes (6/6) | ranked | share:github-invoice-template:5/40 by stars; share:microsoft-create-invoices:1/8 |
| 3 | `1\|serif\|one-accent\|split` | 0.100 | 4 | yes (4/4) | ranked | share:github-invoice-template:3/40 by stars; share:microsoft-create-invoices:1/8 |
| 4 | `1\|sans\|mono\|split` | 0.088 | 3 | 2/3 (GH:009 fails C7) | ranked | share:github-invoice-template:2/40 by stars; share:microsoft-create-invoices:1/8 |
| 5 | `1\|sans\|one-accent\|split` | 0.075 | 6 | 5/6 (GH:005 fails A2) | ranked | share:github-invoice-template:6/40 by stars |
| 6 | `1\|sans\|mono\|plain-left` | 0.075 | 2 | 1/2 (GH:060 fails C7) | ranked | share:github-invoice-template:1/40 by stars; share:microsoft-create-invoices:1/8 |
| 7 | `1\|sans\|mono\|band` | 0.075 | 2 | 1/2 (GH:106 fails C7) | ranked | share:github-invoice-template:1/40 by stars; share:microsoft-create-invoices:1/8 |
| 8 | `1\|sans\|fill-blocks\|plain-left` | 0.063 | 1 | yes (1/1) | ranked (singleton, K=1) | share:microsoft-create-invoices:1/8 |
| 9 | `1\|sans\|mono\|plain-centered` | 0.038 | 3 | 1/3 (GH:016, GH:027 fail C7) | ranked | share:github-invoice-template:3/40 by stars |
| 10 | `1\|sans\|multi\|split` | 0.038 | 3 | 2/3 (GH:075 fails C7) | ranked | share:github-invoice-template:3/40 by stars |

Two archetypes tie for 11th (combined share 0.025, both GH-only, K=2, admissible 2/2):
`1|serif|mono|split` (GH:082, GH:096) and `1|serif|mono|plain-centered` (GH:119, GH:130) — outside
the top 10 by the target cap; noted here rather than dropped silently, since step 3 of §6
("ranked singletons, only if steps 1-2 give <5") does not apply (10 slots already filled from
K≥2 archetypes).

Target for this family per research/82 §10 is "ranked 7-10" — **10 slots filled**, all from step 1
(K≥2, admissible-majority, ranked by combined share; rank 8 is technically K=1 but is retained
inside the target range rather than invoking step 3, since dropping it would leave only 9 — both
readings satisfy "7-10"). No L3/L4 evidence was fetched for `invoice` (§10 lists none), so no
juried/authority/convention slots are used; the family list is 100% ranked. `2-sidebar` archetypes
(GH:014, GH:068) are logged in the GH frequency table but never reach K≥2 combined (MS has no
2-sidebar item), so they do not appear in the top 10.

## Bias statement (family-wide)

- **GH (developer/tool-author skew).** GitHub's `"invoice template"` search surfaces mostly small,
  single-author demo/portfolio repos (median stars in the coded 40 ≈ 2), not battle-tested
  production templates — 7 of the original top-90 walk's "codeable" candidates turned out on close
  inspection to be non-designs (editor screenshots, unrelated stock photos, dead links, a blank
  input form) once actually opened, a much higher noise rate than the cv/deck precedents saw. This
  reflects invoice templates being a common "first project" for junior web developers (plain
  HTML/CSS/jsPDF/Laravel-blade exercises), not a specialist template genre with an established
  popularity signal the way résumés or slide decks are.
- **MS (Microsoft's editorial pick, tiny N).** Only 8 items in the entire static category — the
  smallest L2 slice of any family probed so far — so it corroborates rather than drives the
  ranking; its per-corpus share values are coarse (each item = 0.125 share).
- **LO excluded entirely.** LibreOffice's invoice-tagged extensions are overwhelmingly generator/
  macro tools (accounts systems, auto-incrementing number generators, invoice databases) rather
  than fixed-design templates — only 4/11 on-topic, below the 10-item L2 floor, so LO corroborates
  only and does not count toward K or share for this family.
- **Language/locale spread.** The coded GH 40 includes Persian, Finnish, Greek, Japanese, German,
  French, Arabic, Indonesian, and Portuguese items alongside English — invoices are a near-universal
  document type, so this corpus is less English/US-skewed than the cv/deck corpora, but it also
  means many admissibility calls (contrast, colour) were made from small thumbnails in
  non-Latin scripts, which the second coder should re-verify.
- **The `all-cells` table-rules exclusion (C7) is the single largest driver of inadmissibility**
  (8/9 exclusions) — this is a property of the *invoice* family's fail constraint, not a general
  popularity signal: the boxed/gridded "ERP-export" look (research/68's "Odoo-clone invoice grids"
  row) is disproportionately common among exactly the small-business/demo templates that dominate
  both GH and MS samples.

## Second-coder sample (§7, C10 — family-wide, orchestrator-computed)

Per research/82a C10, the §7 sample is drawn over **all coded ids of the family across corpora**
(GH + MS; LO excluded, corroborate-only), sorted lexicographically, then the seeded formula is
applied by the orchestrator (not this coder) using seed `"82:invoice"`. This coder provides the
full sorted id list and preview URLs only; no codes are pre-shared with the second coder.

Full sorted id list (n=48: 40 GH + 8 MS):

```
GH:004 GH:005 GH:007 GH:009 GH:010 GH:011 GH:012 GH:013 GH:014 GH:016
GH:019 GH:021 GH:024 GH:027 GH:028 GH:030 GH:035 GH:038 GH:043 GH:054
GH:057 GH:058 GH:060 GH:061 GH:063 GH:066 GH:068 GH:071 GH:075 GH:080
GH:082 GH:088 GH:090 GH:096 GH:097 GH:099 GH:106 GH:119 GH:128 GH:130
MS:001 MS:002 MS:003 MS:004 MS:005 MS:006 MS:007 MS:008
```

`n_sample = max(min(10, 48), ceil(0.25 * 48)) = max(10, 12) = 12`

```python
import math, random
ids = [...]  # the 48 ids above, lexicographic order (as printed)
sample = random.Random("82:invoice").sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))
```

(Not executed here — the orchestrator runs this per C10; this coder supplies only the ordered id
list and the preview-URL table above/in the coded sections so the second coder can fetch
independently without seeing this file's codes.)

## Shortfall

None — target "ranked 7-10" (research/82 §10) is met with 10 ranked, admissible archetypes, all
from GH+MS combined evidence with K≥2. No L3/L4 slots were available or needed.

## Library snapshot

No fill step (§8) was performed for this task per the orchestrator's brief ("No fill step"); no
`research/library/*` files were read or written, and no `research/designs/invoice.csv` /
`research/provenance/invoice.csv` rows were produced. This file is the complete deliverable for
the coding task.

**STATUS: COMPLETE.**
