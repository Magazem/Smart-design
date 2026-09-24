# T9 constraint rows — notes (research/16-t9-constraints-draft.csv)

Scope: report 03 §A (CV/ATS), §B (decks), §D (reports), §E (cross-cutting), plus
research/12's photocopy-colour finding, plus research/06 ENS-review findings that
generalise beyond ENS. §C print production excluded — Print Production Specialist owns
those rows. 38 rows drafted. 7 `fail`, 31 `warn`.

## Row count vs. the 80–120 estimate

38 is well under the schema's 80–120 total — **flagging as a finding, not a failure**, per
the task's own instruction. Three real reasons, not padding to compensate for:
1. A meaningful share of report 03's mechanical rules are correctly owned by other
   tables' validators already, not T9 — see "already covered elsewhere" below (7 rules).
2. Several report 03 rules are genuinely not mechanically checkable at all and were
   excluded rather than forced into a row — see "advisory only" below (10 items).
3. My scope excludes §C entirely (the Print Production Specialist's rows) and excludes
   brand-specific rows (e.g. ENS's own lime/brown choices, which aren't report-03-general).
   The 80–120 total is the sum across all of that, not this file alone.

## Per-row source and mechanical check

| constraint_key | Tag | Source | How a stdlib script checks it |
|---|---|---|---|
| ats-no-multi-column | FACT | report 03 §A | DOCX: `zipfile`+`xml.etree` on `word/document.xml`, flag `w:cols` with `w:num > 1` or sectPr multi-column; PDF: flag if extracted text-run x-coordinates cluster into ≥2 stable bands. |
| ats-no-content-tables | FACT | report 03 §A | DOCX: walk for `w:tbl` elements inside body sections mapped to Experience/Skills. |
| ats-no-textbox | FACT | report 03 §A | DOCX: `w:txbxContent` elements; PDF: text inside an XObject/Form with no direct content-stream placement. |
| ats-contact-in-body | FACT | report 03 §A | DOCX: confirm phone/email regex matches exist in `document.xml` body, not only in `header*.xml`/`footer*.xml`. |
| ats-no-symbol-glyphs | FACT | report 03 §A | Extract bullet-run characters, check codepoints against Private Use Area (U+E000–U+F8FF) / known symbol-font ranges. |
| ats-text-layer | FACT | report 03 §A | **Caveat:** not cleanly stdlib-only. `zlib` (stdlib) decompresses FlateDecode streams, but robustly counting real selectable text needs font-encoding/CMap resolution a minimal parser won't have. A coarse stdlib proxy — count `Tj`/`TJ` text-showing operators in decompressed content streams vs. total page count — is buildable and worth shipping as an approximation; a precise `selectable_ratio` likely needs a PDF library. Flagging honestly rather than overclaiming stdlib-only feasibility, in the same spirit as the fsType finding in research/12. |
| ats-image-only-info | FACT (proxy) | report 03 §A | **Heuristic, not a full check.** DOCX/PDF: flag inline images with no text run in the same paragraph/adjacent cell. Cannot verify true semantic completeness (whether the image's *meaning* has a text equivalent) — that needs judgment, not parsing. Kept as `warn` precisely because it's a proxy. |
| us-cv-length-under10y / -10y-plus | CONVENTION | report 03 §A | Extract Experience section date ranges (regex on date patterns), compute span from earliest start to latest/present; compare page count. Two rows instead of one conditional cell — keeps each row a flat fact per Rule 1, rather than branching logic inside `Parameter`. |
| us-cv-no-photo / uk-cv-no-photo | CONVENTION | report 03 §A | Count embedded raster images in the doc body; threshold 0. |
| us-cv-no-dob | CONVENTION | report 03 §A | Regex scan body text for DOB-pattern labels ("date of birth", "DOB", "né(e) le", "birth date"). |
| us-cv-no-marital-status | CONVENTION | report 03 §A | Regex scan for marital-status labels ("marital status", "married", "single", "situation familiale"). |
| uk-cv-length | CONVENTION | report 03 §A | Page count from render output, threshold 2. (Already an example in `09-library-schema.md:567`; kept as-is.) |
| eu-cv-length | CONVENTION | report 03 §A | Same mechanism, threshold 3 (Europass 2–3pp). |
| gulf-cv-length | CONVENTION | report 03 §A | Same mechanism, threshold 2. |
| gulf-cv-photo-expected | CONVENTION | report 03 §A | Same image-count mechanism as `us-cv-no-photo`, **inverted direction** — flags if `images_of_person < 1`, not `> 0`. First "presence required" row in this set; noted so its inverted polarity isn't missed at implementation time. |
| proj-body-floor | CONVENTION | report 03 §B | Resolved `Size pt` for role=body at medium=projection (T6 join) ≥ 24. |
| proj-body-dense-floor | CONVENTION | report 03 §B | Same join, role=body-dense, ≥ 18 — this is report 03's stated *exception* value, not the default; the exception must not become the default (see `09-library-schema.md` finding #13 in research/06). |
| proj-title-floor | CONVENTION | report 03 §B | Same join, role=h1(title); report 03 gives a 36–44pt range — encoded here as the floor (36), not the ceiling. |
| screen-body-floor | CONVENTION | report 03 §B | Same join, medium=screen (screen-only decks, distinct from projection) ≥ 18. **New row** — this medium/role pair wasn't in the schema draft's own examples. |
| deck-density-bullets / -words | CONVENTION | report 03 §B (6×6 heuristic) | Count bullet paragraphs per slide and words per bullet from slide XML text runs. |
| deck-text-density | CONVENTION | report 03 §B | Word-count of slide body text runs, threshold ~40. |
| deck-chart-series-max | CONVENTION | report 03 §B | Count `c:ser` elements in embedded chart XML (PPTX charts embed an XLSX, itself a zip of XML — still stdlib-walkable). |
| proj-contrast-margin | CONVENTION | report 03 §B | Computed WCAG-style contrast ratio from resolved hex pair (palette table), asserted ≥7:1 rather than the standard screen 4.5:1 — the "projector washout" margin. Reuses `validate-contrast-screen` machinery with a higher threshold, doesn't need a new validator. |
| deck-aspect-ratio-default | CONVENTION | report 03 §B | Page format's width:height ratio from T7, asserted 16:9 unless doctype explicitly opts into a 4:3 legacy override. |
| pptx-font-embedded | FACT | report 03 §B / research/06 finding #14 | `zipfile` open the `.pptx`, assert `ppt/fonts/*` entries exist and `<p:embeddedFont>` appears in `ppt/presentation.xml`. **See overlap note below — this may duplicate T5's `validate-font-embedded`.** |
| report-measure-cpl | CONVENTION (Bringhurst) | report 03 §D | **Computed, not looked up** — resolved body `Size pt` (T6) × average glyph advance width (either a maintained per-typeface constant, or read directly from the font's `hmtx` table using the same fixed-offset stdlib technique proven for `fsType` in research/12) × the width of the **widest body paragraph text frame on the page** → characters-per-line; assert 45–75. **Patched 2026-09-07, ENS field finding:** originally measured against the full page/column text-block width. The ENS acceptance run applied that page-wide width even where a table sat in the flow, which cramped the table into the 130mm body measure and pushed a one-page note to two pages. Scope narrowed to **body paragraphs only** — the check now walks paragraph-level (`w:p`) text frames outside any `w:tbl`, takes the widest one as the measure, and explicitly does **not** apply to table cells, figure/table captions, or multi-column sidebar text (those get their own width from their container, not the page measure, and report 03 never claimed the 45–75 CPL range applies to them — that range comes from long-form *body* reading, §D). Tables may use the full available width. This is the central finding from the Q1 answer (research/12): report 03 gives no static print body-size floor, only this formula — the fix here doesn't change the formula, it fixes what the formula was being asked to measure. |
| report-leading-ratio | CONVENTION (Bringhurst) | report 03 §D | Resolved leading ÷ resolved body size, assert ∈ [1.20, 1.45]. |
| report-running-heads | CONVENTION | report 03 §D | **Structural only.** DOCX: assert `w:evenAndOddHeaders` is set in `sectPr` for multi-page flow docs (distinct verso/recto headers exist). Cannot verify the *content* is correct (verso=doc title, recto=section) — that half is advisory, noted below. |
| report-pagination-frontmatter | CONVENTION | report 03 §D | DOCX: front-matter section's `w:pgNumType w:fmt` = `lowerRoman`; body section's restarts at `w:start="1"` with `fmt="decimal"`. |
| report-table-rules | CONVENTION (Tufte) | report 03 §D | DOCX table XML: count `w:tblBorders`/per-row `w:tcBorders` — assert vertical borders = 0 and horizontal borders present only on header/total rows, not every row. |
| report-table-numeric-align | CONVENTION | report 03 §D | Classify each table column by content (regex digit-majority), cross-reference cell `w:jc` alignment; numeric columns must be `right`, text columns `left`. |
| print-legibility-l-delta | CONVENTION | report 03 §E | Computed CIE Lab L* of resolved text/background hex pair, delta ≥40. **Scoping note below — narrower/broader than the schema's own `print-l-delta` example.** |
| photocopy-safe-color | CONVENTION (my own reasoning) | research/12, extending report 03 §E's L* method + research/06 finding #10 | Computed text-color L* (not delta — absolute lightness) ≤15, for `label`/`legal` roles in doctypes carrying the `photocopy-safe` Set Key. Replaces the size-only `photocopy-body-min` row drafted as an example in `09-library-schema.md:571` — see below, that row should be dropped. |
| legal-text-min-size | CONVENTION (my own recommendation, not report-03-sourced) | research/06 finding #11 | Resolved `Size pt` for role=legal ≥ 8. **No report-03 numeric source exists for this** — I recommended 8–8.5pt during the ENS review as a directional fix over 7.4pt; picked 8 as the defensible round floor. Flagging the provenance plainly since it's weaker than the report-03-sourced rows above. |
| legal-text-no-sustained-uppercase | CONVENTION (general typographic knowledge, not in report 03) | research/06 finding #11 | Regex: longest run of consecutive uppercase words in role=legal text ≤3 (allows short acronyms/labels, flags sustained all-caps paragraphs). **Not sourced from report 03 at all** — report 03 doesn't discuss uppercase legibility; this is typographic convention I introduced during the ENS review (sustained uppercase loses word-shape cues, established readability literature, e.g. Tinker). Weakest-sourced row in this set, tagged accordingly. |

## Two discrepancies with the schema draft's own example rows — flagging, not silently resolving

1. **`proj-body-floor` severity.** The schema draft's own example (`09-library-schema.md:569`)
   sets this `fail`. Report 03 tags the 24pt projection floor **CONVENTION** (Duarte/Reynolds),
   not FACT. Per the severity rule stated in my task assignment — "convention floors = warn
   unless report 03 marks them FACT" — I drafted it `warn`. I did not silently override the
   schema author's example; surfacing the conflict here for reconciliation.
2. **`deck-density` bullet count.** The schema's example (`:573`) uses `5`. Report 03's 6×6
   heuristic is `6`. I used `6` (the report-03-sourced generic default) and split it into two
   rows (bullets, words). ENS's own house rule of 5 bullets (from the ENS rebuild draft) is a
   brand-specific tightening that belongs under `Set Key: ens-house`, not this generic table —
   out of my scope, not authored here.
3. **`photocopy-body-min` (8.5pt) — recommend dropping.** The schema's example row
   (`:571`) sets a photocopy-specific size floor. I have no source for this as a size
   threshold (see research/12's fuller argument): the photocopy risk I actually identified
   is about ink lightness (color), not point size. Replaced by `photocopy-safe-color` above.

## Schema gap surfaced by the patch above — needs a column, not a Parameter hack

`report-measure-cpl`'s new `scope=body-paragraph;exempt=table-cell|caption|sidebar-column`
is stuffed into `Parameter` because **T9's current columns have no way to express "applies
to this element type within the document," only "applies to this doctype/format/artifact-class."**
`Applies To`'s enum (`artifact-class:*|format:*|doctype:*`) scopes at the whole-document
level; it cannot say "this check applies to paragraphs but not table cells within the same
document." Cramming that into `Parameter` works for one validator function that already
knows to look for `scope=`/`exempt=` keys, but it's exactly the kind of implicit,
per-validator convention Rule 2 is supposed to prevent — nothing forces the *next* row that
needs element-level scoping to use the same key names, and nothing validates that the
validator function actually implements them.

**What the schema needs for revision 2:** an `Element Scope` column (or similar) on T9,
enum-like (`body-paragraph` / `table-cell` / `caption` / `sidebar-column` / `heading` /
`all`), so element-level scoping is a first-class, validator-agnostic routing key instead
of parameter text a human has to remember to interpret consistently. This is the same
category of fix as T6 being split out of T5 — a real, recurring dimension (element type)
masquerading as ad hoc parameter text because the table wasn't built with it in mind
originally. Flagging for the Coverage Analyst's revision rather than inventing the column
myself mid-patch, since I don't own T9's shape.

## Overlaps worth reconciling (not resolved unilaterally)

- **`pptx-font-embedded`** (this file) checks the same thing T5's design notes already
  declare as an enabled validator, `validate-font-embedded`
  (`09-library-schema.md:391`). I included the row because the task explicitly asked for
  "PPTX embedding" as a generalised research/06 finding, and reused the same validator
  name rather than inventing a second one — but whether a T9 row *should* exist alongside
  a table-level "Validators enabled" declaration, or whether T9 rows are the only place
  checks should live, is a T9-vs-T5 architecture question I'm not settling myself.
- **`print-legibility-l-delta`** vs. the schema's own `print-l-delta` example
  (`:570`, `Set Key: professional-print`, `format:pdf`). That example is scoped to
  professional print, which reads like §C territory (Print Production Specialist's row,
  possibly). Report 03 §E's L* rule is general — it applies to any printed text, not just
  professionally-printed jobs. I drafted a broader version under a new Set Key
  (`print-legibility`) rather than editing the Print Specialist's row, to avoid collision.
  These may need merging once both passes land.

## Already covered by other tables — not duplicated here

- Canonical section headings → T10 `Canonical Headings` + `validate-canonical-headings`.
- Heading depth cap (H1–H3) → T10 `Heading Depth Max` + `validate-heading-depth`.
- Caption position (below figure / above table) → T10 `Caption Position` + `validate-caption-position`.
- Cross-references numbered, not positional → T10 `Cross-Ref Style` + `validate-cross-refs`
  (this is almost certainly the same grep-for-positional-phrases check I nearly drafted
  as a T9 row — dropped it in favor of the existing T10 validator rather than risk two
  definitions of the same check).
- Tabular figures for numeric table columns → T5 `Has Tabular Figures` + `validate-tabular-figures`.
- Typeface pairing / family count cap → T5 `Family Count` + `validate-family-count`.
- DOCX/PPTX font resolution (safe-stack vs. embed by render target) → T8 `Font Rule` + `validate-font-resolution`.

## Advisory only — not mechanically checkable, listed so nothing is silently dropped

1. Oldstyle vs. lining figure choice for inline-prose numerals vs. tables/headers — no
   reliable stdlib-readable font property distinguishes this (research/12: `tnum` presence
   tells you tabular-*capability*, not figure style).
2. Serif vs. sans in body text — explicitly a contested, genre-signaling convention in
   report 03 §E, no pass/fail condition.
3. True semantic check for "every icon/graphic has a text equivalent" — only a proxy
   (`ats-image-only-info`, included above) is achievable; full verification needs judgment.
4. "Template-looking" visual signals (heavy color panels, stock iconography, alignment-grid
   consistency) — report 03 §A, holistic/qualitative, no threshold exists.
5. CV summary content quality, verb-tense parallelism across bullet entries — content
   craft, not layout/design; also arguably out of a design schema's scope entirely.
6. Running-heads *content* correctness (is verso actually the doc title, is recto actually
   the current section name) — the structural presence check is in the CSV; the content
   match is not mechanically verifiable without deeper semantic parsing.
7. Chart-vs-table editorial judgment ("does this message need a trend or exact values") —
   the >7-series mechanical ceiling is in the CSV; the upstream judgment of whether a chart
   is the right call at all is not.
8. Speaker notes convention (3–5 sentences, must not duplicate slide text) — a crude
   text-overlap check between notes and slide body is conceivable, but report 03 gives no
   overlap threshold to check against; inventing one would be exactly the kind of
   unsourced number this file is trying to avoid.
9. Typeface pairing *harmony* (category-contrast quality beyond the family-count ceiling —
   "looks almost-but-not-quite alike") — qualitative, T5's `Family Count` covers the
   mechanical half only.
10. CV region field-inclusion norms that are additive rather than prohibitive in general
    (e.g., EU sometimes including DOB) — only the *prohibitive* region norms (US/UK: no
    DOB, no marital status) produce a clean mechanical "must be absent" check; norms that
    just permit a field don't have a violation condition to check against.

## New validator names introduced (not yet implemented — will hard-fail `validate-checks-implemented` until built)

`validate-image-text-parity`, `validate-text-safe-fields`, `validate-text-density`,
`validate-chart-series`, `validate-aspect-ratio`, `validate-measure`,
`validate-leading-ratio`, `validate-running-heads`, `validate-pagination-format`,
`validate-table-rules`, `validate-table-alignment`, `validate-text-safe-color`,
`validate-text-case`. Reused existing/declared names: `validate-ats-structure`,
`validate-page-count`, `validate-type-floor`, `validate-density`, `validate-text-layer`,
`validate-contrast-screen`, `validate-contrast-print`, `validate-font-embedded`.

## Proposed row — not added to the CSV, flagging for a decision first

**`content-preservation-on-redesign`** — proposed, net-new validator.

| constraint_key | Set Key | Applies To | Check | Parameter | Threshold | Severity |
|---|---|---|---|---|---|---|
| content-preservation-on-redesign | redesign-job | doctype:* | `validate-content-preservation` (new) | diff_scope=text_nodes;allow=whitespace,typo-corrections-listed | exact_match_excl_allowlist | refuse |

**Source:** the ENS acceptance run itself — not report 03, not an existing research file.
During that run the model shortened three regulatory labels on a `formulaire` redesign to
make them fit the tightened body measure, then had to notice and self-correct. That's a
real, observed failure mode this project's own existing global rule already forbids in
prose (`09-library-schema.md`'s `Global` section: *"content, field numbering, legal text
and figures are preserved verbatim; only obvious typos may be fixed and must be listed to
the user"*) — but nothing in T9 currently checks it. It's a prose promise with no
validator, the exact pattern Rule 2 exists to catch.

**Why `refuse`, not `warn`:** this isn't a legibility judgment call like most of this
file's rows — it's the model silently changing regulatory/legal content to solve a layout
problem, which is a correctness failure, not a style one. It belongs with the ATS
structural `fail` rows in kind, even though its source is a field observation rather than
a report-03 FACT.

**How a script checks it, concretely:** extract all text nodes from the *input* artifact
and the *output* artifact — DOCX: `w:t` runs; PPTX: `a:t` runs; PDF: extracted text stream
(same caveat as `ats-text-layer` above: a coarse `Tj`/`TJ`-based proxy is stdlib-feasible,
a precise extraction likely needs a library) — normalize whitespace on both sides, diff.
Anything outside a maintained allowlist of typo-correction patterns (and the redesign
job's own logged, user-visible list of corrections it made) fails the check.

**Why proposed, not added to the CSV directly:** two open questions that aren't mine to
resolve unilaterally — (1) it needs the `Element Scope` gap above resolved first, or at
minimum a decision on whether "diff the whole document" is an acceptable substitute for
element-level scoping here (arguably yes, since this check wants to catch *any* text
change, not just body-paragraph changes — unlike `report-measure-cpl`, this one plausibly
doesn't need the new column at all, which is itself worth the Coverage Analyst noting as a
counter-example when they design it); (2) "listed set of typo corrections" implies a
redesign job must emit a structured corrections log the validator can read against — that
log doesn't exist as a concept anywhere else in the schema yet, and inventing its shape
wasn't in scope for this patch.

## Severity counts

fail: 7 (all ATS structural FACTs, plus PPTX embedding). warn: 31 (everything CONVENTION-tagged,
including the compounding-risk legal-text rows, which are my own judgment calls layered on
top of report 03 rather than report-03-sourced facts).

## Revision (research/87 F10, research/90 F10) -- `pptx-font-embedded` relaxed

python-pptx cannot embed fonts, so a bare "`ppt/fonts/*` present" check could never pass for the
renderer this project's own pptx handoff targets, while the `fail` severity blocked delivery. The row
is now `Parameter target=ppt/fonts;flag=p:embeddedFont;or=declared-safe-stack`, `Threshold
present-or-declared`, severity still `fail`: it passes when every referenced font is embedded OR the
file declares the safe-stack fallback (core-property keywords `ddi-font-rule=safe-stack`), which the
pptx handoff instructs when the typeface's licence forbids embedding or the renderer cannot embed.
It fails only when neither holds. Verdict: `preflight.py` `pptx-font-embedded`
(`scripts/tests/test_pptx_font_rule.py`).
