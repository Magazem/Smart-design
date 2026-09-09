# 33 — Non-nullable column sweep (Gap 7)

Coverage and Gap Analyst, 2026-09-09. **Report only. Nothing on disk was changed** —
manifest md5 `0b4a079fbbfd2678cc463a78648dbe86` unchanged, gate still **82**, `data/base/`
mtimes untouched (Sep 8 14:09). No edit to `validate_data.py`, no edit to
`handover-coverage.md`. Throwaway scripts in `research/tmp-sweep/`, deletable.

Closes RESUME's "NEW GAP" and `handover-coverage.md` OPEN GAP 7: *a sweep of every
non-`nullable` column against its loaded data is unrun*. It is now run.

## Headline

**B1 under-counted its own evidence by a factor of five.** `page-formats.Measure mm` is not
the only 100%-empty column in T7 — **`Margin Top mm`, `Margin Bottom mm`, `Margin Inside mm`
and `Margin Outside mm` are empty on all 11 rows too.** T7 ships sheet size (`Trim W/H mm`),
`Bleed mm` and `Safe Margin mm`, and **zero interior page geometry**. A resolver can tell you
what sheet to print on and cannot lay out a single line of text on it.

Why B1 missed it: the schema gives all four margins **one shared type row**
(`09:1058` — `` `Margin Top/Bottom/Inside/Outside mm` | number ×4 ``). A reader scanning T7's
type table sees one line and one empty-looking column; the shipped CSV has four. `Measure mm`
sits on the next line and was the one that got noticed.

## What was swept, and the denominator

The manifest carries **no nullability at all** (`grep -c nullable data/schema-manifest.json`
= 0). The only place `nullable` exists is `research/09-library-schema.md`'s per-table type
rows, so that is the source of truth, and the sweep is a three-way join of schema type rows ×
manifest columns × loaded CSV cells.

| | n |
|---|---|
| manifest columns | 174 |
| declared by a schema type row | 162 |
| — of those, marked `nullable` | 12 |
| — non-nullable | 150 |
| no type row: surrogate keys (§0.1.1, non-null by construction) | 5 |
| no type row: **nullability undeterminable** | 7 |
| **total treated as non-nullable** (150 declared + 5 surrogate) | **155** |
| — of those, **swept** | **126** |
| — of those, **unsweepable** (`palettes`, `structures` files do not exist) | **29** |

Every step reconciles, and each number is measured rather than summed: 174 = 162 declared + 12
undeclared; 162 = 150 non-nullable + 12 nullable; the 7 undeterminable are excluded and the 5
surrogates included, giving 155; and 155 = 126 swept + 29 unsweepable. Every type row maps to a
manifest column (zero orphans). Four documented one-row-covers-many shorthands were expanded, each cited in
its own section's design note: T3 `Rule Weights` → 3, T4 `Primary`/`On Primary`-style pairs →
13, T7 `Trim W/H` → 2 and `Margin …` → 4, T12 `Photo`/`Date of Birth`/… → 5.

**Say "unsweepable", not zero, for `palettes` (20 columns) and `structures` (9).** They clear
at critical-path step 6, along with the gate's bucket A.

### How the counts were produced (reproducible)

Counts come from a script over `data/base/`, not from reading. `research/tmp-sweep/` holds
both steps; neither writes anything outside that directory.

1. `parse_types.py` reads `research/09-library-schema.md`. It finds each `## T<n>.` heading that names a table file,
   bounds the section at the **next `##` of any kind**, and inside it accepts rows only
   from a markdown table whose header is literally `| Column | Type | …`. Two bounding rules
   matter: without the section bound, §2's dropped-upstream table and T9's example-row table
   are read as columns (they add 19 phantom "columns"); without the header rule, any backticked
   first cell qualifies. A cell is a column declaration only if it is entirely backticked names
   joined by `/`, which is what expands the four shared type rows. Escaped pipes (`\|`) inside
   enum type cells are protected before splitting on `|`, otherwise the type string truncates
   at the first enum member and a trailing `nullable` would be lost.
2. `nullable` = the substring `nullable` in the type cell. `S/V/R` = the last cell.
3. `sweep.py` joins that to `data/schema-manifest.json`'s `columns` and to the CSV, and counts
   a cell as blank when `value.strip() == ""`. Placeholders are counted separately and only
   when the value is **not** a declared member of that column's manifest enum.

Two checks guard the parse: every type row must map to a manifest column (zero orphans), and
declared + undeclared must equal 174. Both hold.

## Class 1 — non-nullable columns holding blank cells

Fourteen columns across five tables. The right-hand column is the verdict the Orchestrator
needs: **DATA** = author the values, **SCHEMA** = the label is wrong and the data is right.

| table.column | S/V/R | blank | verdict |
|---|---|---|---|
| `page-formats.Margin Top mm` | V | **11/11** | **DATA** |
| `page-formats.Margin Bottom mm` | V | **11/11** | **DATA** |
| `page-formats.Margin Inside mm` | V | **11/11** | **DATA** |
| `page-formats.Margin Outside mm` | V | **11/11** | **DATA** |
| `page-formats.Measure mm` | V | **11/11** | **DATA** (B1's original) |
| `constraints.Element Scope` | R V | 41/42 | **SCHEMA — doc only** |
| `render-targets.Engine Invocation` | V | 5/8 | **SPLIT: 3 SCHEMA, 2 DATA** |
| `font-substitutes.Metric Identical` | V | 6/15 | **SCHEMA — doc only** |
| `font-substitutes.Weights Covered` | V | 6/15 | **SCHEMA** |
| `doctypes.Constraint Set Keys` | R | 5/30 | **DATA (needs ruling)** |
| `doctypes.Structure Key` | R | 1/30 | **DATA** |
| `doc-reasoning.Palette Bias Terms` | S | 1/15 | DATA, minor |
| `doc-reasoning.Typeface Bias Terms` | S | 1/15 | DATA, minor |
| `constraints.Threshold` | V | 1/42 | **SCHEMA** |

### The two that look worst and are not defects at all

`constraints.Element Scope` is the largest line count in the sweep (41/42) and **is correct
data**. Its own type cell says *"empty = whole document"* (`09:1269`), its examples are both
`*(empty)*`, and `09:1812` names the principle: *"empty is a real state, not a missing
value."* Decisively: **the manifest already lists `""` as the first legal member of the
enum**, so the gate sanctions it deliberately. Same for `font-substitutes.Metric Identical`
(`""` in the manifest enum; `09:1810` licenses it explicitly as *not applicable*).

So for these two the machine-readable layer is right and only the **schema document** is
inconsistent — it says `nullable` on twelve columns and expresses the same idea as prose
inside a type cell on two others. That is the finding: **the schema has two ways to license
an empty cell and only one of them is machine-readable.** A future doc-driven sweep will
re-flag these two every time until they are reconciled. Cheapest fix is to add `nullable` to
those two type rows; the manifest needs no change.

### The clean structural cluster

`font-substitutes` blanks in `Metric Identical` and `Weights Covered` fall on **exactly the
same six rows** — 10 Candara, 11 Corbel, 12 Constantia, 13 Consolas, 15 Verdana,
16 Trebuchet MS — which are precisely the rows with `Lineage = none`, `Licence = none` and an
empty `Substitute Family`. There is no substitute to describe, so both blanks are correct.
`Substitute Family` is already marked `nullable`; **`Weights Covered` should be too**, and it
has no design note covering it the way `Metric Identical` does.

`render-targets.Engine Invocation` splits and the split matters. Blank on rows 3, 5, 6, 7, 9:

- **3 are SCHEMA** — `docx-office` (python-docx), `pptx-office` (python-pptx) and
  `html-static` (stdlib-template) are **library APIs with no command line**. An invocation
  string is not a missing value, it is a category error. Mark nullable.
- **2 are DATA** — `pdf-weasyprint` and `pdf-wkhtmltopdf` **are** command-line tools, and the
  sibling row `pdf-weasyprint-pdfx4` carries a real invocation. Those two blanks are gaps.

`constraints.Threshold` blank on row 10 `cv-field-norms`: its check
`validate-text-safe-fields` is parameterised by a field list in `Parameter`
(`fields=photo|date_of_birth|…`) and has no scalar threshold. **SCHEMA** — mark nullable.

### The three that are real data gaps beyond T7

`doctypes.Structure Key` blank on row 30 `infographic`. **Not structural.** All four other
non-`flow` doctypes carry one — `poster` → `poster-single-canvas`, and the three deck rows →
`deck-standard`. `infographic` is the only `canvas` row without a structure. Note this is a
**second** dangling-vs-blank problem in the same column that already contributes 29 bucket-A
gate lines; it will not surface when `structures.csv` is authored, because a blank FK is
skipped, not resolved.

`doctypes.Constraint Set Keys` blank on rows 10 `cv-academic`, 12 `letter-formal`,
13 `memo-internal`, 28 `slide-deck-handout`, 30 `infographic`. Marked **`R`** — required for
resolution. `cv-academic` is the conspicuous one: every other CV row carries constraint sets,
and B2 is a separate finding about seven CV rows carrying the *wrong* ones. **These five carry
none.** An empty list is a defensible "no constraints apply", so this needs a ruling rather
than a silent backfill, but I would not ship a CV doctype with no `ats-strict`.

`doc-reasoning` row 15 `infographic-scaffold` is blank in `Palette Bias Terms` and
`Typeface Bias Terms` (both `S`, searchable only, so the cost is degraded search, not a broken
resolve). Its `Style Key`/`Palette Key`/`Typeface Key` are also blank but those three **are**
`nullable`, so they are legitimate. Same doctype family as the two `doctypes` gaps above —
**`infographic` is the least-finished row in the loaded data**, and it is the one row that
appears in three separate findings here.

## Class 2 — placeholder strings where a value is expected

Only three cells in all of `data/base/`, and all three are in `figures.csv` row 12
`tabular-lookup` — the deliberate "the right answer is no chart" row.

| column | type | S/V/R | value |
|---|---|---|---|
| `Print Series Max` | `int` | **V** | `n/a` |
| `Secondary Options` | `text` | P | `n/a` |
| `Static Fallback` | `text` | P | `n/a` |

**`Print Series Max` is a genuine type violation** — a column typed `int` holding the string
`n/a`, with no enum and no check to catch it. Any numeric consumer breaks or silently
coerces. Recommend it be marked `nullable` and left **blank**, not `n/a`. The two `P` prose
columns holding `n/a` are stylistically inconsistent with the blank-means-absent convention
used everywhere else, but they are prose and nothing parses them; low priority.

Worth recording as a negative result: a scan for `—`, `-`, `TBD`, `null`, `?` as whole field
values across all 12 loaded tables found **none**, and every other `none`/`n/a` in the data
(72 and 14 occurrences) is a **declared member of that column's enum** — `Fold Type=none`,
`Supports Bleed=n/a` and so on. The placeholder problem is three cells, not a pattern.

## Class 3 — the seven columns whose nullability cannot be determined

`figures.csv` ships seven columns with **no type row anywhere in the schema**:
`Data Type`, `Keywords`, `Best Chart Type`, `When to Use`, `Accessibility Grade`,
`A11y Fallback`, `Accessibility Notes`.

This is the exact defect class the **Revision 4 erratum said it was closing**. Its own words
(`09:1525`): these columns *"arrive from `charts.csv` and this document had described them in
prose without ever giving them a row in a typed table — which is how an undeclared column
becomes a list column by accident. Typed now, so it cannot."* The erratum then typed
**three** — `Secondary Options`, `When NOT to Use`, `Data Volume Threshold`. **Seven were
left.** The erratum is incomplete, not wrong, and T11 is the only table in the schema with
undeclared columns. **All seven are populated on all 11 rows** — checked directly, not inferred from the
sweep, which skips undeclared columns before it counts blanks. So nothing is broken today and
the risk is exactly the one the erratum names, no more.

This is the same shape as the P-letter work: a label that claims something the document does
not actually establish. Recommend it be recorded as a **second Revision 4 erratum follow-on**
and the seven typed, ideally by whoever wrote the first one.

## Scope: base data only, and why that is the whole of it

The sweep covers `data/base/` alone. That is not a narrowing — **`data/brand/` currently holds
only `README.md`**, no CSVs. The `data/brand/ens/typefaces.csv:2` line in
`handover-coverage.md`'s step-5 blocker refers to a file `make_brand_kit.py` *emits at run
time*, not one on disk. There is no brand data to sweep, and when there is, it will be
generated rather than authored, so the check belongs in that script's self-check.

## Class 4 — negative results, so nobody re-runs them

- **No dead `nullable` markings.** All 12 nullable columns are blank on at least one loaded
  row, so none is a label with no purpose. Range: `doc-reasoning.Style Key` 1/15 to
  `doctypes.Region Key` 23/30.
- **No CSV header disagrees with the manifest** on any of the 12 loaded tables.
- **No type row exists that is not a manifest column.**
- The five surrogate keys are non-null on every row, as their construction requires.
- The seven undeclared `figures` columns are non-null on every row (see Class 3).
- `constraints.Applies To` is typed `enum` in the schema doc with no manifest enum. **Not a
  defect** — its values are glob patterns (`doctype:cv-*`), which an enum list cannot express.
  Recorded so it is not re-raised.

## Why the gate cannot see any of this, stated precisely

`validate_data.py` has no required/non-null check, and two specific mechanisms make the
blanks invisible rather than merely unchecked:

1. **Every FK is treated as nullable.** `scripts/validate_data.py:214` — `if not value:
   continue  # nullable FK, no reference to check`, documented at lines 114–115. This is
   correct for the four genuinely-nullable FKs, and it is why `doctypes.Constraint Set Keys`
   (5 blank, `R`) and `doctypes.Structure Key` (1 blank, `R`) produce **zero** gate lines
   despite both being required.
2. **Non-FK, non-enum columns are unconstrained entirely.** Nothing looks at
   `page-formats.Measure mm` or the four margins at all. Twelve of the fourteen Class 1
   columns are in this state; the other two are enums that deliberately permit `""`.

**I am not recommending the gate be taught a non-null check in this pass.** The gate is the
instrument the current change set is measured with, its floor is already noisy at 82, and
buckets A and B must resolve before a new check class is added — otherwise the next worker
cannot tell which lines are new. It is a real follow-up, after step 6, and it needs the
schema's two ways of licensing an empty cell reconciled first, or it will emit 41 false
positives on `Element Scope` alone on its first run.

## Recommended disposition, ranked

1. **Amend the B1 ruling — it is already made, and it names one column too few.** RESUME
   records B1 as *"T7 gains ~11 document-use rows AND populates the empty `Measure mm` on all
   rows"*. **It must say `Measure mm` and all four `Margin … mm` columns.** The direction of the
   ruling is unchanged and this is not a re-litigation: an author working to the ruling as
   written would populate one column of five, ship 44 still-empty cells, and the gate would
   stay silent exactly as it does today. This is the only place the sweep changes an existing
   decision, and it is a one-line amendment.
2. **SUPERSEDED by `34-untyped-figures-and-blank-fks.md` §0 — do not act on this item as written.**
   `infographic`'s blanks in BOTH columns are deliberate and documented at `26-notes.md:222-225`;
   four rows remain genuinely open, not six. Original text follows.
   ~~Author `doctypes.Structure Key` for `infographic`~~ and rule on the five blank
   `Constraint Set Keys`. Both are `R`, both gate-invisible, both cheap. Belongs with B2 —
   same file, same author, one edit to `research/26`.
3. **Type the seven undeclared `figures` columns** as a Revision 4 erratum follow-on.
4. **Mark seven columns `nullable`** in the schema document: `Element Scope`,
   `Metric Identical` (doc-only, manifest already correct), `Weights Covered`,
   `Threshold`, `Print Series Max`, and `Engine Invocation` *if* the ruling accepts that
   library-API engines have no invocation string.
5. **Fill two `Engine Invocation` values** (`pdf-weasyprint`, `pdf-wkhtmltopdf`) and blank
   `figures.Print Series Max` on row 12 instead of `n/a`.
6. **After step 6**, add a non-null check to the gate — but not before the label fixes, and
   the reason is measurable. See below.

## Should `validate_data.py` gain a non-null check, and what would it cost?

**Yes, but fourth in order, not first.** The cost is a false-positive rate that the label fixes
in item 4 collapse almost to nothing, and the numbers say so rather than the intuition:

| non-null check, added… | lines emitted | real defects | false positives | rate |
|---|---|---|---|---|
| naively today, against schema-doc `nullable` | 122 | 65 | 57 | **47%** |
| today, but honouring the manifest's `""` enum members | 75 | 65 | 10 | **13%** |
| after item 4's label fixes | 65 | 65 | 0 | **0%** |

The 47% is what makes a naive check unshippable on top of a gate already sitting at 82 — it
would nearly double the floor with noise and destroy the property this project keeps
protecting, that the line sets are the diagnostic. The drop to 13% is **free**: the gate
already reads manifest enums, and `""` is already a declared member for `Element Scope` and
`Metric Identical`, so a check that consults the enum before the null rule suppresses 47 lines
without any new judgement. The last 10 are `Weights Covered` (6), `Engine Invocation`'s three
library-engine rows, and `Threshold` (1) — all three of which item 4 fixes with a `nullable`
on a type row.

Two design requirements fall out. **The check must read nullability from the manifest, not the
schema document** — the manifest has none today, so building the check means first exporting
`nullable` into `schema-manifest.json`, which is a manifest-format change and will move the
md5. And **it must honour a declared enum containing `""` as sanctioning the blank**, or the
`Element Scope` principle becomes 41 false positives on the first run.

Note what the check would *not* have caught: `figures.Print Series Max` holding the string
`n/a` in an `int` column. That is a type violation, not a null, and it needs the type checker
the manifest also does not have. Worth knowing before the non-null check is sold as closing
this class.

None of this blocks step 4. Item 1 is inside step 5's existing B1 blocker and adds no new
blocker of its own.

## Confidence and open questions

**High confidence** on the counts, the reconciliation (162 + 12 = 174, exact) and the
manifest-enum evidence for `Element Scope`/`Metric Identical` — those are read directly off
the shipped files. **High** on the T7 margins, which are visible in the first data row of
`page-formats.csv`.

**Medium** on two verdicts, both flagged above as needing a ruling rather than a fix:
whether the five blank `Constraint Set Keys` are authoring gaps or deliberate "no
constraints", and whether `Engine Invocation` should be nullable or whether the three
library-engine rows should carry a synthetic descriptor instead.

**Assumption stated:** blank means missing unless the schema, a design note, or the manifest
enum says otherwise. Where a design note contradicted the type row I followed the note and
said so. **The 29 unsweepable columns are not a clean bill of health** — `palettes` in
particular has 13 hex columns that a contrast validator will read, and this sweep says
nothing about them.
