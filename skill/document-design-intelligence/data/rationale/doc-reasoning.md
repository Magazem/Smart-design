# rationale/doc-reasoning.md

Written by `research/load-base.py`. **Do not hand-edit** -- the source is the
`Reasoning` and `Confidence` columns of `research/29-t2-doc-reasoning-draft.csv`.

Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling
`rationale/<table>.md`, not in a column, so that every row stays a one-line diff.
T2's draft authors two columns the table does not have; the loader strips them here.
`Confidence` is the author's own rating, not a measurement.

One entry per row of `data/base/doc-reasoning.csv`, in file order.

### `cv-ats-strict` -- confidence 0.9

ats-strict Set Key (T1-bound on every regional CV row) reaches 6 fail-severity T9 rows; Style/Palette/Typeface Keys copy the schema's own T2 worked example verbatim (09-library-schema.md:442-444)

### `cv-academic` -- confidence 0.6

T1's cv-academic row carries no Constraint Set Keys (unlike the ats-strict CV rows) so if_ats_target does not apply here -- correcting my own 26-notes.md table, which wrongly grouped cv-academic with cv-ats-strict under if_ats_target

### `cover-letter-professional` -- confidence 0.8

T1's cover-letter row binds Constraint Set Keys=ats-strict directly, so this row reaches the same 6 fail rows as cv-ats-strict

### `letter-formal` -- confidence 0.5

no closed Doc Condition applies; T1 binds no Constraint Set Keys for letter-formal

### `memo-internal` -- confidence 0.5

shares Style/Palette/Typeface intent with letter-formal; this is also the schema's own worked brand two-pass example doc_category (09-library-schema.md Sec.3, note interne / memo query)

### `form-handfilled` -- confidence 0.4

if_photocopied targets a real T9 row (photocopy-safe-color, warn); if_hand_filled targets field-legibility-min, which is PROPOSED -- no such constraint_key exists in data/base/constraints.csv yet, flagged as a T9 gap in 29-notes.md rather than left unwired

### `print-marketing` -- confidence 0.85

T1 binds Constraint Set Keys=professional-print directly on all 6 doctypes sharing this category (5 brochures + poster); professional-print Set Key reaches 5 fail-severity T9 rows (bleed, fold, output-intent, cmyk-guard, font-embed)

### `report-classic` -- confidence 0.7

Style Key copies the schema's own T3 worked example verbatim (09-library-schema.md:525-528); report-typography and print-legibility bind directly via T1, both all-warn in T9 today

### `whitepaper-formal` -- confidence 0.5

shares report-classic-serif's Style Key -- structurally the same grammar as a long report; Plex superfamily's heading/body contrast fits a citation-heavy technical document

### `proposal-narrative` -- confidence 0.5

same report grammar family; no closed Doc Condition applies (T1 binds report-typography only, all-warn)

### `quote-devis` -- confidence 0.5

reuses the form grid grammar (line-item pricing is structurally a form table, not prose)

### `deck-generic` -- confidence 0.5

REVERTED at Revision 3 (09-library-schema.md lines 569-586, 2265-2278): the interim three-Reasoning-Key split (deck-projection/deck-screen/deck-handout) is withdrawn, deck-generic is one key again covering all three slide-deck-* T1 rows, and if_projected is deleted from DOC_CONDITION_SIGNALS outright -- the admission test ruled a condition inadmissible once its truth value is fixed by the resolved T1 row, and the three deck doctypes already carry the discriminator (projection/screen/empty) in T1's own Constraint Set Keys, so slide-deck-projection alone still reaches proj-body-floor etc. through that Set Key, with no Doc Condition needed. Severity=warn here reflects the shared design-language check only; slide-deck-projection's independent fail path (Constraint Set Keys=projection -> pptx-font-embedded) is untouched by this column and does not depend on it. Trade-off of going back to one shared doc_category: deck-handout (print-read, no presenter) now inherits the same bold-minimal/high-contrast/safe-sans-deck design payload as the live-projected and screen-read variants instead of the dense-print/mono-ink treatment the split version gave it -- exactly the economy-vs-context-nuance trade the schema's ruling accepts by design (no new column). Typeface Key was safe-sans-deck, which did not exist as a T5 row at the time; B4 (research/29-notes.md) temporarily repointed it to safe-sans-arial as a stopgap -- the safe-stack sans, chosen over the embeddable ofl-source-sans-serif because deck-generic spans handout/screen/projection contexts including machines the author does not control, where a system font guarantees rendering without relying on correct embedding. That stopgap silently broke Scale Key resolution: safe-sans-arial's own Scale Key is cv-print (the CV's scale, needed there and not to be retargeted), so deck-generic inherited 11pt CV body sizes instead of the deck-projection scale (24/18/36pt) research/30 had already authored and left waiting for this row (research/30-notes.md: 'safe-sans-deck Typeface Key is still PROPOSED... gives it somewhere to resolve once a T5 row exists'). v0.3 D3 (research/51-invoked-quality.md) found the wrong sizes live in the shipped pptx handoff. Fixed by authoring the safe-sans-deck T5 row research/30-notes.md anticipated -- same Arial faces and safe-stack rationale as B4, Scale Key deck-projection -- and repointing Typeface Key here to it; safe-sans-arial itself is untouched, so cv-* doctypes are unaffected.

### `one-pager-restrained` -- confidence 0.5

distinct Style Key from report-classic-serif -- a one-pager's density constraint is a different grammar from a running multi-page report, even though both bind report-typography

### `infographic-scaffold` -- confidence 0.3

no T3/T4/T5 payload authored for this class anywhere in the library yet (02-coverage-gaps.md's unbuilt-scaffold finding, confirmed still true); leaving Style/Palette/Typeface Key blank rather than inventing a resolved row for a class nothing else backs, matching the T1 author's own stated discipline on this doctype

### `invoice-tabular` -- confidence 0.5

same form-grid grammar as quote-devis -- both are line-item tables, not prose documents

---

The draft also carries 4 ENS rows (`ens-formulaire`, `ens-marketing`, `ens-office-document`, `ens-slides`). They are not in `data/base/`
(`BRAND_ROWS`), and `make_brand_kit.py` does not emit a `doc-reasoning.csv`, so
their reasoning reaches no shipped file today and lives in
`research/29-t2-doc-reasoning-draft.csv` alone. Recorded here so the gap is
visible from the table it belongs to.
