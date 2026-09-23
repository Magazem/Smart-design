# A8 Part 2 — cv-dach gate re-run, run 2 (supersedes run 1)

Run 1 (`research/75-INVALID-self-judged.md`) is invalid: the worker self-judged the panel
(near-identical verbatim reasoning across all three "judges", not blind, not real
independently-spawned Opus judges) and ran `git status` against the no-git-commands rule.
Its `manifest.json` (X=old/Y=new) also contradicts its own RESULTS section (X=new/Y=old) —
no trustworthy mapping survives from run 1. This file is a full, independent re-run.

Written before any render or judge call (rule: preregister-falsifier). Rubric is A5's
verbatim rubric (board task 01a09fbf-243a-7b03-a58e-0abfffec96c9), same as run 1 reused it.

## PART 1 verification (data + vocabulary, already committed at 7a26588)

- `research/build-manifest.py:127` — Table Rules enum is now
  `["hairline", "header-and-total", "none", "row-hairlines"]`, with rationale at lines
  119–125 explaining why `row-hairlines` is a distinct token from `hairline`.
- `skill/document-design-intelligence/data/schema-manifest-NOTES.md:553-578` documents all
  four Table Rules values, `row-hairlines` explicitly meaning "no cell boxes."
- `doc-styles.csv` row `cv-dach-tabular`: `Table Rules=row-hairlines`; Checklist has explicit
  pt/mm values (35mm label column, 13pt row padding, 13pt space after table) — confirmed by
  direct read.
- `ddi.py` handoff (`scripts/ddi.py:206-207`) prints the instruction line "table rules:
  horizontal hairlines between rows only; no vertical rules; no cell borders" — confirmed in
  a fresh `resolve.py`/`ddi.py handoff` run below.
- Test coverage: `skill/document-design-intelligence/scripts/tests/test_ddi.py` references
  `row-hairlines` (red-then-green test present per brief).

PART 1 is complete and committed. No further data edits made here.

## Closing the field-list confound (flagged, unresolved, in run 1)

Run 1's field list (Name/Ort/E-Mail/Telefon/Geburtsdatum/Staatsangehörigkeit/Familienstand)
was invented by that worker, not sourced. Sourcing it now:

- `research/71-cv-gate-content.md` C2 gives, verbatim: Name, Location (Ort), Email, Phone,
  Geburtsdatum, Staatsangehörigkeit, Familienstand. These are C2's own stated fields — using
  them is not inventing content, it's transcription.
- `skill/document-design-intelligence/data/base/cv-regions.csv` row `dach-experienced`:
  Photo=customary (handled separately as a placed image, not a table row), Date of
  Birth=customary, Nationality=customary, Marital Status=**contested**, Visa Status=customary
  (no data in C2 — omitted, not invented), Evidence Class=CONVENTION.
- **Field list used** (7 rows, no "Name" duplicate row — C2's Name is the page headline, not
  a Kontakt-table field, closing run 1's "redundant Name row" defect at the source): Ort,
  E-Mail, Telefon, Geburtsdatum, Staatsangehörigkeit, Familienstand. Six rows, all directly
  sourced to C2 content plus cv-regions.csv's "customary" marks. Familienstand is CONVENTION/
  contested per cv-regions.csv, not a clean "customary" instruction — included because C2
  supplies the data and dach-experienced does not mark it "not customary," but this is a
  judgment call, declared here before rendering, not after seeing judge reactions.

## Closing the row-padding-doubling defect (flagged, unresolved, in run 1)

Run 1's renderer set `tcMar` top=13pt AND bottom=13pt on every cell (`build_render.py:138-143`),
i.e. ~26pt of padding per row across 7 rows — this is very plausibly what judges meant by "a
blown-out contact table consume[s] two-thirds of the page," a render-instruction-reading bug,
not a property of the design direction. The Checklist text is "row padding to one body
leading unit (13pt)" — plain reading: **13pt total per row**, not 13pt per edge. Declared
interpretation used in this re-render: each cell's `tcMar` top=bottom=6.5pt (130 dxa), summing
to 13pt of padding per row. This is the reading used below, fixed before rendering.

## Conditions (unchanged from run 1's pre-registration)

- **OLD** = `cv-ats-strict` (Reasoning Key `cv-ats-strict`), current committed default for
  `cv-dach`, rendered straight from repo `data/`.
- **NEW** = `cv-dach-tabular`, rendered from a temp copy of `data/` with `doctypes.csv` row
  `cv-dach`'s Reasoning Key changed from `cv-ats-strict` to `cv-dach-tabular`. Repo `data/`
  untouched.
- Both resolve `cv-dach`'s `Default Language`=`de` (A7), so both get German section headings.

## Content

`research/71-cv-gate-content.md` C2 verbatim (Markus Weber, cv-dach, experienced band).

## Pipeline

1. `resolve.py --doctype cv-dach --json` for OLD (repo data/) and NEW (temp copy) →
   resolved JSON.
2. `ddi.py handoff --format docx` on each → handoff text block.
3. A fresh Sonnet Agent (no history of this conversation, no condition names, no mention of
   A5/A8/boxing/judges/run 1) renders both blocks mechanically into docx with python-docx,
   content from C2 only, given: the two handoff blocks (labelled arbitrarily), the sourced
   6-row field list above (with its source cited so the agent doesn't re-invent one), and the
   declared row-padding reading (13pt total per row, split 6.5/6.5).
4. Each docx → PDF via `soffice --headless --convert-to pdf`, page 1 → PNG at 150dpi
   (PyMuPDF).
5. `scripts/preflight.py` on each docx.
6. Files land at `research/evidence/cv-dach-rerun/run2/{old,new}/cv-dach.{docx,pdf,png,preflight.json}`.
7. Blind copies at `research/evidence/cv-dach-rerun/run2/blind/cv-dach-{X,Y}.png`, X/Y by
   fresh coin flip, mapping recorded in `research/evidence/cv-dach-rerun/run2/manifest.json`,
   never shown to a judge.

## Machine-checkable clauses — run BEFORE judges

- (i) cv-dach NEW cell-border ratio < 0.5, from NEW's `preflight.json`.
- (ii) German headings present on NEW.

If either fails: FAIL by the pre-registered letter, panel not run.

## Judge prompt (verbatim, to be pasted into each of 3 fresh Opus Agent calls)

> You are shown two CV page images, X and Y, for the same person (a German CV, "Lebenslauf").
> You have no other information about them and must not read any other files. Score each of
> the following, based only on the two images:
> 1. hierarchy clarity 1–5 (X, Y)
> 2. typographic pairing quality 1–5 (X, Y)
> 3. colour restraint and appropriateness 1–5 (X, Y)
> 4. slop-pattern count (lower better) — count any of: boxed/framed contact grid, emoji,
>    generic clip-art icons, rainbow accent colours, excessive drop shadows, template-look
>    default styling (X, Y)
> 5. regional correctness for a German-market ("DACH") CV, pass/fail for each of X and Y,
>    checked against: Photo=customary, Date of Birth=customary, Nationality=customary,
>    Marital Status=contested/customary, Section Order=contact;experience;education;skills,
>    Language Expectation=German headings over German body content.
> 6. overall preference, X or Y, with one sentence explaining why.
> Answer only using this structure. Do not guess at anything not visible in the images.

3 Opus judges, spawned sequentially, `run_in_background: false`, fresh (no shared context,
no access to this file, this conversation, or run 1), order of image presentation not
varied (single-doctype gate).

## PASS CONDITION (fixed, restated verbatim from the assigning task)

NEW preferred by ≥2 of 3 judges AND no regional-correctness fail on NEW AND zero
fail-severity preflight facts on NEW AND cv-dach NEW cell-border ratio < 0.5.

No separate kill signal. Anything short of the above is FAIL by the letter, and
`cv-dach-tabular` stays non-default, returning to research with the judges' reasons.

---

## RESULTS

Manifest (`research/evidence/cv-dach-rerun/run2/manifest.json`): coin flip `A_is_X` →
**X = old** (`cv-ats-strict`), **Y = new** (`cv-dach-tabular`). A/B were the render-agent's
labels; X/Y was assigned by fresh coin flip after rendering, before any judging.

### Render

A fresh Sonnet Agent (no history, no condition names, no mention of A5/A8/run 1) built both
docx files mechanically from the specs above, using the sourced 6-row field list and the
declared 13pt-total (6.5pt/6.5pt) row-padding reading. Verified in the built XML: Document B
(NEW) table has `insideH` single 0.5pt only, `top/bottom/left/right/insideV` all nil, column
widths 35mm/125mm exact, `tcMar` top=bottom=130dxa (6.5pt). Both converted to 1-page PDFs
(LibreOffice headless) and PNG page 1 at 150dpi (PyMuPDF) — NEW no longer overflows to 2
pages, confirming the padding-doubling in run 1 was a render-instruction-reading bug, not an
inherent property of the direction.

### Machine-checkable clauses — before judges, per pre-registered order

- **(i) cv-dach NEW cell-border ratio**: `research/evidence/cv-dach-rerun/run2/render/B.preflight.json`
  → `table_cell_border_ratio: {bordered: 0, total: 12, ratio: 0.0}`. **PASSES** (0.0 < 0.5).
- **(ii) German headings on NEW**: handoff block and rendered content both show
  Kontakt/Berufserfahrung/Ausbildung/Kenntnisse. **PASSES**.
- Zero fail-severity preflight facts on NEW: 2 font families (≤3, no fail), 0 emoji, 0.0
  cell-border and bordered-block ratios (no fail; CV family is warn-only on cell-border ratio
  regardless). **PASSES**.

Both machine clauses pass — Part 1's row-hairlines fix and the corrected row-padding reading
both hold up under an independent re-render. Panel proceeds.

### Judge panel — 3 fresh Opus judges, sequential, blind, independently spawned

Each judge was given only the two blind PNG paths and the verbatim rubric prompt above, with
an explicit instruction not to read any other file.

| Judge | X (=OLD) pref? | Y (=NEW) pref? | Preferred | X regional | Y regional |
|---|---|---|---|---|---|
| 1 | ✓ | — | X (OLD) | PASS | PASS |
| 2 | ✓ | — | X (OLD) | PASS | PASS |
| 3 | ✓ | — | X (OLD) | PASS | PASS |

**NEW preferred by 0 of 3 judges.** Regional correctness PASSES on both conditions, all three
judges — A7's heading-language fix and this run's field-list/padding fixes removed the two
confounds flagged in run 1.

Reasoning was independently derived, not copy-paste-identical this time (each judge gave
distinct phrasing and distinct secondary observations), but converged on the same primary
defect:

> **Judge 1**: "X — it carries a clearly stronger heading-to-body hierarchy and no slop
> patterns, whereas Y's ruled contact grid, misaligned label/value baselines and
> under-weighted section headings make its structure harder to scan despite both being
> regionally correct."

> **Judge 2**: "X — its section headings clearly outrank the entries below them, whereas Y
> inverts that hierarchy with light serif headings under bolder job titles and adds a ruled
> contact grid that X avoids."

> **Judge 3**: "X — Y's only structural differentiator is a defect, the section headings
> reading lighter than the job titles below them, compounded by six contact rows eating the
> top half of the page and an orphaned gap before Berufserfahrung, whereas X's weakness is
> blandness rather than a broken reading order."

All three independently named the **same defect, and it is not the boxed-table problem this
run fixed**: NEW's section headings (13pt Times New Roman) render visually lighter/smaller
than the bold 10.5pt Arial job titles beneath them, so the heading no longer outranks its own
content in weight — an inversion of the intended hierarchy. Two of three judges also flagged
the now-unboxed contact table itself (hairline rows, no boxes) as still reading as a
structural interruption ("ruled contact grid," "six contact rows eating the top half of the
page") even though the cell-border machine check passes; this is a fresh, distinct signal
from run 1's "fully boxed grid" complaint — the table's *presence and row count*, not its
border style, is now the friction point for 2 of 3 judges.

### Verdict against the pre-registered condition

**FAIL**, by the letter. Pass condition requires NEW preferred by ≥2 of 3 judges; NEW was
preferred by 0 of 3. The other three clauses (no regional-correctness fail on NEW, zero
fail-severity preflight facts on NEW, cell-border ratio < 0.5) all independently PASS — both
Part 1's border fix and this run's field-list/padding fixes worked exactly as intended — but
the preference clause is not met, so the gate as a whole is FAIL.

Per the assigning task: **`cv-dach` stays on `cv-ats-strict`; `cv-dach-tabular` remains
non-default.** No draft-CSV edit made; nothing regenerated or committed (commit authority is
the orchestrator's; workers do not run git).

### What should go back to research

1. **High confidence, data-driven, new signal**: `pt-serif-sans`'s safe-stack fallback prints
   heading text smaller/lighter-looking (13pt Times New Roman) than the bold body job titles
   beneath it (10.5pt Arial bold) — a weight/size hierarchy inversion specific to the
   safe-stack path, independent of the border-treatment issue this run's Part 1 fixed. Worth
   testing either a heavier/larger safe-stack heading size for `cv-dach-tabular`, or
   re-testing with the real PT Serif/PT Sans embedded, before any further gate re-run.
2. **Medium confidence**: 2 of 3 judges still read the unboxed contact table as consuming
   disproportionate page space / interrupting flow, independent of its (now correct)
   border-free rendering. Whether a shorter field list, a different layout (e.g. inline
   label/value pairs instead of a table), or simply accepting this as an inherent property of
   the tabellarisch convention is a research question, not a rendering bug — this run's field
   list and padding are both sourced and applied as declared, so this signal is not confounded
   the way run 1's was.
3. This run corrects two known confounds in `research/75-INVALID-self-judged.md` (invented
   field list; doubled row padding) with fully independent, blind judging. The gate result
   changed from run 1's verdict (still FAIL) but the *reasons* judges give changed
   materially — the border/box complaint from A5 and run 1 is gone; a hierarchy-weight
   complaint has taken its place. That is real signal about what to fix next, not noise.
