# rationale/doc-reasoning.md

Written by `research/load-base.py`. **Do not hand-edit** -- the source is the
`Reasoning` and `Confidence` columns of `research/29-t2-doc-reasoning-draft.csv`.

Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling
`rationale/<table>.md`, not in a column, so that every row stays a one-line diff.
T2's draft authors two columns the table does not have; the loader strips them here.
`Confidence` is the author's own rating, not a measurement.

One entry per row of `data/base/doc-reasoning.csv`, in file order.

### `cv-ats-strict` -- confidence 0.9

ats-strict Set Key (T1-bound on every regional CV row) reaches 6 fail-severity T9 rows; Style/Palette/Typeface Keys copy the schema's own T2 worked example verbatim (09-library-schema.md:442-444). +emoji (A4): research/68-slop-patterns.md flagged this row as missing the emoji token every other ats/professional-register category already carries

### `cv-academic` -- confidence 0.6

T1's cv-academic row carries no Constraint Set Keys (unlike the ats-strict CV rows) so if_ats_target does not apply here -- correcting my own 26-notes.md table, which wrongly grouped cv-academic with cv-ats-strict under if_ats_target. +emoji (A4): research/68-slop-patterns.md emoji-gap census

### `cover-letter-professional` -- confidence 0.8

T1's cover-letter row binds Constraint Set Keys=ats-strict directly, so this row reaches the same 6 fail rows as cv-ats-strict. +emoji (A4): research/68-slop-patterns.md emoji-gap census

### `letter-formal` -- confidence 0.5

no closed Doc Condition applies; T1 binds no Constraint Set Keys for letter-formal

### `memo-internal` -- confidence 0.5

shares Style/Palette/Typeface intent with letter-formal; this is also the schema's own worked brand two-pass example doc_category (09-library-schema.md Sec.3, note interne / memo query)

### `form-handfilled` -- confidence 0.4

if_photocopied targets a real T9 row (photocopy-safe-color, warn); if_hand_filled targets field-legibility-min, which is PROPOSED -- no such constraint_key exists in data/base/constraints.csv yet, flagged as a T9 gap in 29-notes.md rather than left unwired

### `print-marketing` -- confidence 0.85

T1 binds Constraint Set Keys=professional-print directly on all 6 doctypes sharing this category (5 brochures + poster); professional-print Set Key reaches 5 fail-severity T9 rows (bleed, fold, output-intent, cmyk-guard, font-embed). +emoji (A4): research/68-slop-patterns.md emoji-gap census

### `report-classic` -- confidence 0.7

Style Key copies the schema's own T3 worked example verbatim (09-library-schema.md:525-528); report-typography and print-legibility bind directly via T1, both all-warn in T9 today. +emoji (A4): research/68-slop-patterns.md emoji-gap census

### `whitepaper-formal` -- confidence 0.5

shares report-classic-serif's Style Key -- structurally the same grammar as a long report; Plex superfamily's heading/body contrast fits a citation-heavy technical document. +emoji (A4): research/68-slop-patterns.md emoji-gap census

### `proposal-narrative` -- confidence 0.5

same report grammar family; no closed Doc Condition applies (T1 binds report-typography only, all-warn). +emoji (A4): research/68-slop-patterns.md emoji-gap census

### `quote-devis` -- confidence 0.5

reuses the form grid grammar (line-item pricing is structurally a form table, not prose). +boxed-grid (A4): line-item tables are the same Odoo-clone/frames-around-everything risk research/69 Direction 2 names for a tabular personal-data grid -- a line-item table boxed cell-by-cell instead of ruled hairline/header-and-total

### `deck-generic` -- confidence 0.5

+emoji (A4): research/68-slop-patterns.md emoji-gap census. REVERTED at Revision 3 (09-library-schema.md lines 569-586, 2265-2278): the interim three-Reasoning-Key split (deck-projection/deck-screen/deck-handout) is withdrawn, deck-generic is one key again covering all three slide-deck-* T1 rows, and if_projected is deleted from DOC_CONDITION_SIGNALS outright -- the admission test ruled a condition inadmissible once its truth value is fixed by the resolved T1 row, and the three deck doctypes already carry the discriminator (projection/screen/empty) in T1's own Constraint Set Keys, so slide-deck-projection alone still reaches proj-body-floor etc. through that Set Key, with no Doc Condition needed. Severity=warn here reflects the shared design-language check only; slide-deck-projection's independent fail path (Constraint Set Keys=projection -> pptx-font-embedded) is untouched by this column and does not depend on it. Trade-off of going back to one shared doc_category: deck-handout (print-read, no presenter) now inherits the same bold-minimal/high-contrast/safe-sans-deck design payload as the live-projected and screen-read variants instead of the dense-print/mono-ink treatment the split version gave it -- exactly the economy-vs-context-nuance trade the schema's ruling accepts by design (no new column). Typeface Key was safe-sans-deck, which did not exist as a T5 row at the time; B4 (research/29-notes.md) temporarily repointed it to safe-sans-arial as a stopgap -- the safe-stack sans, chosen over the embeddable ofl-source-sans-serif because deck-generic spans handout/screen/projection contexts including machines the author does not control, where a system font guarantees rendering without relying on correct embedding. That stopgap silently broke Scale Key resolution: safe-sans-arial's own Scale Key is cv-print (the CV's scale, needed there and not to be retargeted), so deck-generic inherited 11pt CV body sizes instead of the deck-projection scale (24/18/36pt) research/30 had already authored and left waiting for this row (research/30-notes.md: 'safe-sans-deck Typeface Key is still PROPOSED... gives it somewhere to resolve once a T5 row exists'). v0.3 D3 (research/51-invoked-quality.md) found the wrong sizes live in the shipped pptx handoff. Fixed by authoring the safe-sans-deck T5 row research/30-notes.md anticipated -- same Arial faces and safe-stack rationale as B4, Scale Key deck-projection -- and repointing Typeface Key here to it; safe-sans-arial itself is untouched, so cv-* doctypes are unaffected.

### `one-pager-restrained` -- confidence 0.5

distinct Style Key from report-classic-serif -- a one-pager's density constraint is a different grammar from a running multi-page report, even though both bind report-typography. +emoji (A4): research/68-slop-patterns.md emoji-gap census

### `infographic-scaffold` -- confidence 0.5

+emoji (A4): research/68-slop-patterns.md emoji-gap census. Style/Palette/Typeface Key now authored per research/59-infographic-content.md. Palette REUSED: brand-accent-print is the only T4 row with a Category Marker Roles token and a CTA-framed accent, already the palette behind print-marketing (poster, brochures); infographic's render target (png-social) is a rasterised screen image, not a press job, so brand-accent-print's contrast pairs (already gate-checked >=4.5:1 project-wide) carry over without a print-specific claim. Typeface and type scale NOT reused: the closest screen scale, deck-projection (carried by safe-sans-deck), has no role for an infographic's oversized stat number, so a new typeface row (safe-sans-infographic, Arial/Arial, same shape as the safe-sans-arial/safe-sans-deck pair) and a new scale_key (infographic-screen) were authored, using the Role enum's `lead` value for the stat number -- already used by ens-print at 12pt for standout/lead text, scaled up here to 108pt for an infographic's oversized stat callout; the size itself is CONVENTION, not sourced; Bringhurst covers print measure/leading only, per the standing sourcing rule. Style Key NOT reused from marketing-print-bold: its Checklist hard-codes fold-aware guidance that is wrong for a single canvas, so infographic-bold keeps its Rule/Corner/Table/Emphasis fields identical (same bold-fill family) but replaces the checklist with stat-callout and category-colour guidance tied to this row's own Anti-Pattern Tokens. Section Order (T10 infographic-canvas) reuses headline/key-points/call-to-action verbatim -- all three already carry en/fr/de headings rows, zero new headings authored.

### `invoice-tabular` -- confidence 0.5

same form-grid grammar as quote-devis -- both are line-item tables, not prose documents. +boxed-grid (A4): same Odoo-clone/frames-around-everything risk quote-devis carries, research/69 Direction 2 rationale

### `cv-us-uk-designed` -- confidence 0.85

A4: Direction 1 'Harvard Reverse-Chronological' (research/69 sec 1, research/70 sec 'Direction 1 -- Harvard Reverse-Chronological'). Butterick Practical Typography resumes page (fetched) + Harvard OCS format rules aggregated by cvowl.com/myperfectresume.com (search-derived) + HR Dive's summary of TheLadders 2018 eye-tracking study (fetched) + Jobscan ATS-formatting-mistakes blog (fetched) ground the single-column/no-color-blocks/size-driven-hierarchy structure. adobe-fonts/source-serif README (fetched) grounds Source Serif 4 as a publisher-documented companion to Source Sans, replacing 69's unsourced Lora/Open Sans option. USWDS system colour tokens (search-derived, hex quoted from token tables) ground gray-90 #1b1b1b (17.2:1 on white) and blue-60v #005ea2 (6.7:1 on white), replacing 69's CONVENTION #0F3D57/#1A1A1A. Style/Palette/Typeface Keys are new cv-harvard/cv-harvard/source-serif-sans rows authored for this direction. Doc Conditions/Set-Key reachability copied verbatim from cv-ats-strict -- Direction 1 is explicitly built to remain ATS-safe (single column, no headers/footers/text boxes per Jobscan), so this row reaches the same 6 fail-severity T9 rows cv-ats-strict does. Manager flag: no test pins cv-uk's prior default (cv-ats-strict/safe-sans-arial/Arial) as a required outcome -- grepped scripts/tests for 'safe-sans-arial', 'Source Serif', 'cv-ats-strict', 'doc_category', 'Doc Category': no hits pinning a font/category on cv-uk specifically.

### `cv-dach-tabular` -- confidence 0.75

A4: Direction 2 'DACH Tabellarisch' (research/69 sec 2, research/70 sec 'Direction 2 -- DACH Tabellarisch'). DACH Lebenslauf photo convention aggregated by talentvp.com/cv-creator.co.uk (search-derived) + data/base/cv-regions.csv dach-early/dach-experienced rows (Photo=customary) + Europass official CV page (fetched, photo permitted) ground the two-column table + top-right 4.5x6cm photo structure. Typewolf's PT Serif page (fetched) gives a direct first-party 'Suggested Font Pairing -- PT Serif + PT Sans', replacing 69's Merriweather+FF Mark option (FF Mark is not free/OFL). GOV.UK Design System colour page (fetched) grounds text #0b0c0c (19.6:1 on white) and dark-grey rule lines #484949 (9.0:1 on white), replacing 69's CONVENTION #222222/#2B2B2B; GOV.UK is used only as a source of accessibility-vetted near-black/grey values, no DACH-institutional claim implied (70's own caveat). No Doc Condition bound: this direction is structurally a two-column table, not single-column, so it is deliberately NOT chained to if_ats_target=constraint:ats-strict the way cv-us-uk-designed is -- DACH candidates culturally expect the tabular/photo format over ATS optimisation per 69. Severity=warn, matching the design-language-only checks on the other non-ats-bound CV/form rows (cv-academic, form-handfilled).

### `cv-eu-europass` -- confidence 0.8

A4: Direction 3 'Europass-Compatible Multilingual' (research/69 sec 3, research/70 sec 'Direction 3 -- Europass-Compatible Multilingual'). Europass official CV page (fetched, reverse-chronological, photo permitted not mandatory, clear/simple language) + data/base/cv-regions.csv eu-europass-early/experienced rows (Section Order promotes languages) + Jobscan (fetched, single-column/standard-section-names) ground the structure. GOV.UK Design System 'link colour' token (fetched) grounds accent #1a65a6 (6.1:1 on white), replacing 69's CONVENTION-tagged #00457C with a sourced token of the same restrained-blue character -- still a swappable accent, not a claimed EU institutional colour, since no EU brand-guideline page was fetched (70's own caveat). Google Fonts Knowledge's within-family/superfamily pairing article (search-derived, corroborated) grounds ibm-plex-sans's single-family weight-differentiated choice as a named legitimate strategy, not a workaround. Photo is deliberately NOT in Anti-Pattern Tokens here (unlike cv-us-uk-designed): 69 states photo is made conditional per the target country's cv-regions row, not default-on, so it is neither forced nor flagged. Still single column and standard section names, so if_ats_target=constraint:ats-strict is retained from cv-ats-strict.

### `cv-editorial` -- confidence 0.75

A4: Direction 4 'Editorial / Creative-Industry CV' (research/70 sec 'Direction 4 -- Editorial / Creative-Industry CV'; new direction, not in 69). Typewolf's IBM Plex Sans page (fetched) shows the Andrea Arqués and Alyssa Martin creative-portfolio sites live-pairing Plex-family sans with expressive serifs/grotesques; Typewolf's Fraunces page (fetched) shows Flask & Field pairing Fraunces with DM Mono in production -- both real illustrative sites per 70, explicitly NOT Fonts In Use citations (70 searched fontsinuse.com directly and found no résumé-tagged entries). IBM Carbon colour overview (search-derived, hexes corroborated after a truncated direct fetch) grounds text Gray 100 #161616 (18.1:1 on white) and accent Blue 60 #0f62fe (5.0:1 on white -- clears AA 4.5 but with less margin than the other three directions' accents, per 70's own caveat, so Blue 60 is restricted to headline-size text/rules and Fill-Only Roles in cv-editorial's palette row, not Text-Safe Roles). No Doc Condition/ats-strict binding: 70 explicitly scopes this direction OUT of ats-strict/government/DACH-formal targets, and it carries no cv-regions.csv row of its own (industry overlay, not region-keyed per 70's own 'Fits' note), so it is authored but not wired as any doctype's default per the Manager's decision.

### `cv-serif-plain-centered` -- confidence (none)

(none given)

### `cv-sans-accent-ruled` -- confidence (none)

(none given)

### `cv-sans-mono-split` -- confidence (none)

(none given)

### `cv-serif-accent-plain-left` -- confidence (none)

(none given)

### `cv-sans-accent-plain-centered` -- confidence (none)

(none given)

### `cv-serif-mono-split` -- confidence (none)

(none given)

### `cv-sans-accent-split` -- confidence (none)

(none given)

---

The draft also carries 4 ENS rows (`ens-formulaire`, `ens-marketing`, `ens-office-document`, `ens-slides`). They are not in `data/base/`
(`BRAND_ROWS`), and `make_brand_kit.py` does not emit a `doc-reasoning.csv`, so
their reasoning reaches no shipped file today and lives in
`research/29-t2-doc-reasoning-draft.csv` alone. Recorded here so the gap is
visible from the table it belongs to.
