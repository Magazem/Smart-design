# schema-manifest.json — transcription notes

Source: `research/09-library-schema.md` **Revision 4**. 14 tables, 174 columns,
13 foreign keys (5 of them `group`), 8 list columns, 1 reference column.
Generator kept at `research/build-manifest.py` (not shipped inside the skill); run it from
`skill/document-design-intelligence/`, its output path is relative.

> **Only `research/load-base.py` writes `data/base/`. Never hand-edit those files.**
> Every CSV there is generated from the authored drafts in `research/`, and the loader is
> idempotent — a hand-edit survives until the next run and then vanishes without a trace.
> To change a row, change the draft (or the loader's transform) and re-run. `data/base/`
> ships **generic rows only**: the loader skips every draft row whose `Brand Scope` is not
> `generic`, and brand rows reach the library solely through
> `examples/<brand>-brand.md` → `scripts/make_brand_kit.py` → `data/brand/<brand>/`.
> See `data/base/README.md`.

*Revision 3 changed four things here — see §7 for the run. The "172 columns" this file
claimed at Revision 2 was already stale by one: `font-substitutes.Weights Covered` was
added during load pass 1 and the count was not updated. The shipped 0.0.1-dev manifest has
173; this one has 174.*

Gate output with `data/base/` still empty — 14 problems, exactly one per table, all of the
single class the task specified, nothing else:

```
$ python3 scripts/validate_data.py data/base
data/base/doctypes.csv: declared in manifest but file does not exist
data/base/doc-reasoning.csv: declared in manifest but file does not exist
data/base/doc-styles.csv: declared in manifest but file does not exist
data/base/palettes.csv: declared in manifest but file does not exist
data/base/typefaces.csv: declared in manifest but file does not exist
data/base/type-scales.csv: declared in manifest but file does not exist
data/base/page-formats.csv: declared in manifest but file does not exist
data/base/render-targets.csv: declared in manifest but file does not exist
data/base/constraints.csv: declared in manifest but file does not exist
data/base/structures.csv: declared in manifest but file does not exist
data/base/figures.csv: declared in manifest but file does not exist
data/base/cv-regions.csv: declared in manifest but file does not exist
data/base/headings.csv: declared in manifest but file does not exist
data/base/font-substitutes.csv: declared in manifest but file does not exist

14 problem(s) found        (exit 1)
```

`"role": "entry"` is on `doctypes` and on no other table.

---

## 1. Columns the manifest format could not express

These are **format change requests, not silent omissions**. Each one is a fact the schema
states that the manifest cannot carry, so nothing checks it today.

### 1.1 Foreign keys that reference a *group* of rows, not a row — CLOSED at Revision 3

**The request below was granted.** `lib/data.py:82` (`fk_spec`) now accepts
`{"table": …, "column": …, "group": true}`, composing with `"list": true`, and
`validate_data.py:216` checks membership in the target column via `column_values()` instead
of identity with that table's key. All five are declared as of Revision 3 and
`validate-keys` is fully mechanised: **13 of 13**, up from 8 of 13.

*Two counts in the original text below were wrong and are corrected in
`research/09` §0.1.1: it is **five** dropped, not four — `structures.Section Order` and
`cv-regions.Section Order` are two declarations, not one — out of **13** FK relationships
total, not 8.* The original request is kept verbatim below because it is the record of what
was asked for and why.

### 1.1 (original text) — Foreign keys that reference a *group* of rows, not a row

`foreign_keys` resolves against the referenced table's `key_column`, so an FK whose target
column is a non-unique grouping column cannot be declared at all. Four of this schema's FKs
have that shape, and they are dropped from the manifest rather than declared wrongly:

| Table | Column | Intended target | Why it fails |
|---|---|---|---|
| `doctypes` | `Constraint Set Keys` (list) | `constraints.Set Key` | many constraint rows share one Set Key |
| `doctypes` | `Region Key` | `cv-regions.region_key` | one region has two seniority rows |
| `typefaces` | `Scale Key` | `type-scales.scale_key` | one scale has many (medium, role) rows |
| `structures` | `Section Order` (list) | `headings.canonical_section` | one section has many language/variant rows |

This is not four accidents; it is a **recurring shape** in a schema built on long-format
dictionaries — "this value must appear in that column" rather than "this value is that
table's key". **Requested:** a third FK form alongside the string and the `"list": true`
object, e.g. `{"table": …, "column": …, "group": true}` meaning *the value must exist in
that column, which need not be unique*. That one addition would restore all four, and it
composes with `"list": true` for the two that are also lists.

~~Until then, `validate-keys` (§4 entry 1) is only partially mechanised: 4 of its 8 FK
relationships are checked, 4 are not.~~ **Granted and closed — see the header of this
section.**

### 1.2 `constraints.Threshold` — CLOSED at Revision 4 (was BLOCKED)

Revision 2 made `Threshold` either a literal or a typed `<table>:<Column Name>` reference.
Two corrections to the Revision 2 text: the separator is a **colon**, not a dot, and the
column half names the **re-headered** column — `T12:Max Pages`, not `T12:max_pages`
(`research/25-reheader-map.md` §9 correction 3; the shipped `constraints.csv` row was
already right and this file was not).

`validate_data.py` implements a `reference_columns` spec. Revision 3 did not declare it,
because `validate_data.py:249` reads:

```python
ref_table, _sep, ref_column = value.partition(":")
target_spec = tables.get(ref_table)
```

`tables` is keyed by **manifest table name** (`cv-regions`). The canonical form is
`T12:Max Pages`, and `T12` is a label that exists only in `research/09`. So the one shipped
row that uses the form is unresolvable by the code written to resolve it.

**RULED at Revision 4, and declared.** The canonical form is
`<manifest-table-name>:<Column Name>` — `cv-regions:Max Pages` — and the second naming layer
is deleted. The rejected alternative was a per-table `"schema_label": "T12"` with a resolver
accepting either form; it keeps `research/09` prose readable at the cost of reintroducing
exactly the drift this document-plus-manifest pairing exists to prevent. `T#` is a section
number in `research/09`; the data layer has never known it.

```json
"reference_columns": {
  "Threshold": {"pattern": "^[a-z][a-z-]*:[A-Za-z][A-Za-z0-9 -]*$", "must_resolve": true}
}
```

**The `T#:` form was in FIVE shipped rows, not one.** Revision 3 said "the one shipped row",
counting only `cv-page-count`. `constraints.csv` also shipped `pro-bleed-geometry`,
`pro-trim-safe-margin`, `pro-min-dpi-raster` and `pro-min-dpi-line-art`, all `T7:` →
`page-formats:`. Those four enter from `research/21-t9-print-constraints-draft.csv` rather
than from a literal in `load-base.py`, which is why every count taken by *reading* the loader
missed them. The loader now normalises the table half through one `T#` → manifest-name map
(`T_LABEL` + `norm_threshold()`, applied in `write()`), so the three drafts still to be
loaded inherit the rule instead of needing literals edited.

**The pattern fails silently by design** — a `Threshold` that does not match is treated as a
literal with no error — so it is tight on the left and generous on the right. The
lowercase-letter table half keeps the literal `16:9` (`deck-aspect-ratio-default`) out;
digits and hyphens in the column half mean a future `page-formats:Trim W mm` resolves rather
than being swallowed. Both failure modes are proven live: seeding `cv-regions:Maximum Pages`
and `page-formatz:Bleed mm` into a copy of `data/` raises the gate from 13 to 15 with
"unknown column" and "unknown table". Re-run that probe if the pattern is ever changed.

### 1.3 Closed-grammar columns are unvalidated (by design here, but flag it)

`doc-reasoning.Doc Conditions` and `constraints.Parameter` hold `key=value;key=value` under
a closed vocabulary with a hard-fail parser. **`typed_json_columns` is empty on every table,
as required** — these are deliberately *not* JSON, so they neither need the exception nor
trip the no-untyped-JSON check. But nothing in this harness validates their grammar either;
that needs `doc_reasoning_contract.py` and the per-validator parameter declarations, which
are not built.

### 1.4 Non-FK list columns — CLOSED at Revision 4

`"list": true` exists only inside `foreign_keys`, so `;`-separated columns that are not
foreign keys used to be declared as ordinary columns with nothing checking that they parse.
Revision 4 declares **eight** of them via `list_columns`, and the gate rejects any value that
splits into an empty item (leading, trailing or doubled `;`):

| table | columns |
|---|---|
| `doc-reasoning` | `Anti-Pattern Tokens` |
| `doc-styles` | `Checklist` |
| `palettes` | `Text-Safe Roles`, `Fill-Only Roles`, `Category Marker Roles` |
| `page-formats` | `Panels mm` |
| `figures` | `Print Palette Roles` |
| `font-substitutes` | `Weights Covered` |

`Weights Covered` was not on the original list in this section and is a genuine list
(`Regular;Bold;Italic;Bold Italic`). Proven live: a trailing `;` seeded into one
`page-formats.Panels mm` cell raises the gate from 13 to 14.

**Two `;`-bearing columns are deliberately NOT declared, and should stay undeclared.**

- `constraints.Parameter` is a `name=value` **map** (`cpl_min=45;cpl_max=75`), not a list.
  Declaring it would type it as the wrong thing. It stays under §1.3.
- `figures.Anti-Patterns` — `research/09` types it "text list" with the example
  `dual-axis;3d-perspective;truncated-baseline`, but the rows were **authored as prose**: two
  sentences of cited rationale joined by `; `. It would *pass* a list check while meaning
  something else, and declaring it would let the gate certify the drift. Open gap; the same
  shape appears in `figures.{Secondary Options, Static Fallback, When NOT to Use,
  Data Volume Threshold}` and `cv-regions.Language Expectation`. Someone owns choosing:
  retype the column as text, or re-author the rows as tokens with the rationale moved out.

Columns that are list *foreign keys* — `doctypes.Render Target Keys`,
`doctypes.Constraint Set Keys`, `structures.Section Order`, `cv-regions.Section Order` — are
already split by the FK checker and are **not** declared twice. `build-manifest.py` asserts
this, along with "the column exists" and "the pattern compiles", for both new keys.

> **The paragraph immediately above is stale and is left standing as a record, not as a
> ruling.** `build-manifest.py` now asserts the *inverse*: every `list: true` FK must ALSO
> appear in `list_columns`, because the FK loop skips empty tokens and so never sees a
> stray or doubled `;`. All four list FK columns are declared in both places today, and
> `list_columns` holds twelve columns, not eight. Correcting this section is a separate
> edit that has not been made; it is reported as a candidate eighth edit for whoever owns
> the next pass.

### 1.5 `distinct_token_columns` — repeated tokens inside one cell

`list_columns` checks that a delimited cell *parses*. It does not check what the parsed
tokens say, so a cell could name the same token twice and pass. `distinct_token_columns`
closes that: a non-empty value in a declared column is split on that column's delimiter,
stripped, and rejected if any token appears more than once.

The key maps column name → single-character delimiter, exactly as `list_columns` does, and
**twelve** columns are declared across eight tables. The live defect it was added for was the
`brochure-flyer-a4` row of `doctypes`, whose `Keywords` cell carried `flyer a4` twice until
v0.2.

**It is opt-in per column, and deliberately not derived from `list_columns`, in both
directions.**

- It covers a column that is *not* a `;`-list: `doctypes.Keywords` is a `, `-separated
  search-token cell, delimiter `,`. A repeated keyword doubles that term's BM25 frequency
  and biases retrieval toward the row carrying the accidental repeat, so the check matters
  there even though the well-formedness check does not apply.
- It omits a column that *is* a declared list: `page-formats."Panels mm"` is **exempt on
  purpose**. It is a positional sequence of panel widths, and equal panels are the normal
  case — `a4-trifold` is `99.5;99.5;98.0`, `letter-gatefold` is
  `53.175;54.775;54.775;53.175`. A blanket "no repeated token in any list column" rule
  would fail four correct rows.

Repetition is a defect in a *set* and normal in a *sequence*, and nothing in the manifest
says which a given column is. Only the schema author knows, so the declaration is made per
column rather than inferred. `build-manifest.py` therefore guards it only weakly: the column
must exist, and the delimiter must be a single non-empty character. It cannot check the
delimiter against `list_columns`, because agreeing with `list_columns` is not the invariant.

---

## 2. Columns I added that Revision 2 does not have

**Four surrogate key columns.** `key_column` is a single column, and four tables have
composite natural keys. Rather than declare a wrong key, each table gets a surrogate:

| Table | Natural key | Surrogate added |
|---|---|---|
| `type-scales` | (`scale_key`, `Medium`, `Role`) | `scale_row_key` |
| `cv-regions` | (`region_key`, `Seniority Band`) | `cv_region_key` |
| `headings` | (`canonical_section`, `Heading Text`, `Language`) | `heading_key` |
| `font-substitutes` | (`proprietary_family`, `Lineage`) | `substitute_key` |

`font-substitutes` is the one that would surprise a reader: Arial has **two** substitutes
(Liberation Sans under OFL, Arimo under Apache 2.0), so `proprietary_family` is not unique
and the lineage choice is a licence decision — exactly why T14 keeps `Lineage` and `Licence`
as separate columns.

**One key column the schema never named.** `figures` had no stated key. Revision 2 of this
file guessed `figure_key`; the authored `22-t11-figures-draft.csv` names it **`chart_key`**
and the CSV won (`research/09` T11). The manifest has said `chart_key` since load pass 1;
this line was the stale one.

All five are now recorded back into `research/09-library-schema.md` so the document and the
manifest cannot drift. Suggested convention for anything added later: surrogate keys are
`<singular>_key`, declared first in the column list, and the natural key stays as ordinary
columns beside it.

---

## 3. What this proves and what it does not

**Proves:** the manifest parses, `role: entry` is unambiguous, and all 14 tables are
declared with exact ordered headers — the gate reached the file-existence check for every
one and stopped there.

**Does not prove:** any header is *correct*. Header exactness, enum membership, FK
integrity and the contrast rule are all checked against CSVs that do not exist yet. The
first real `data/base/*.csv` is the first test of those. The five `contrast_at_least` rules
on `palettes` (each `On X` against its `X`, plus `Foreground` against `Background`) are the
only derived checks declared, because they are the only build-time computable rule the
schema states — §4 entry 6, re-based onto WCAG at Revision 1 precisely so it needs no
rendered artifact.

---

## 4. Verification run against the schema's own example rows

The five `contrast_at_least` rules were declared at 4.5:1 uniformly. That was an assumption,
so it was checked against `lib/color.py` and both example palettes in `research/09` §T4
before shipping:

| Pair | ENS core | mono-ink |
|---|---|---|
| `On Primary` / `Primary` | 6.15:1 | 17.40:1 |
| `On Secondary` / `Secondary` | 5.58:1 | 8.86:1 |
| `On Accent` / `Accent` | 7.91:1 | — |
| `Foreground` / `Background` | 13.97:1 | 18.88:1 |
| `On Muted` / `Muted` | **4.74:1** | 6.66:1 |

All nine pass at 4.5:1, so the uniform rule stands and no pair is downgraded to the 3:1
large-text threshold. **`On Muted` / `Muted` passes with 5% headroom**, which is the one to
watch: ENS's `#5B665F` on `#DCE8DF` is a secondary-text pair at body size, so 4.5 is the
right threshold for it, but any future darkening of `Muted` or lightening of `On Muted`
breaks the gate. Recorded so the first failure there reads as a real regression rather than
a surprise.

## 5. One blocker for the first real CSV

`research/19-t5-typefaces-draft.csv` (8 authored typeface rows) deliberately leaves
`Embedding Licence` and `Has Tabular Figures` **blank in every row** — both are script-derived
from the `fsType` and GSUB `tnum` reads, and the DDR correctly declined to hand-type them.

Both columns are declared enums here and **neither lists `""`**, so that file fails the gate
the moment it lands in `data/base/`. The fix is not to weaken the enums: both already carry
an **`unknown`** member for exactly this state (`Embedding Licence: unknown`,
`Has Tabular Figures: unknown`). Blank must become `unknown` before the file ships, and
`fonts.py` overwrites `unknown` with a measured value when it runs. Leaving the enums strict
is what makes "nobody has checked this font yet" a visible value rather than an empty cell.

---

## 6. Load pass 1 — 190 rows across 8 tables (see research/25-reheader-map.md §9)

Gate now reports **6 problems, all "declared but file does not exist"** for the six
not-yet-authored tables. All 8 loaded tables pass every check — header exactness, enum
membership, FK integrity, no-BOM, no untyped JSON. `resolve.py` refuses cleanly through the
same loader: `[DATA INVALID] 6 problem(s) — refusing to resolve`.

One manifest change was forced by real data: **`customary` added to T12's field-direction
enum.** My four values (`expected` / `neutral` / `negative-signal` / `contested`) came from
reading a partial sample; the authored file uses a fifth, and `customary` ("commonly
included, not required") is genuinely distinct from `expected` ("its absence is the
anomaly"). Authored data wins over a guessed enum.

### TODO — re-declare the four grouping FKs when the harness gains `"group": true`

§1.1's four dropped foreign keys are still undeclared. Checked by eye at load (§8 of the
re-header map); the values that must exist when the other side of each join lands:

- `typefaces.Scale Key` → 6 `scale_key` values needed in `type-scales.csv`:
  `cv-print, ens-print, form-print, report-print, report-screen, report-technical`
- `doctypes.Constraint Set Keys` → 11 available `Set Key` values in `constraints.csv`:
  `ats-strict, cv-region, font-safety, legal-text, photocopy-safe, print-legibility,
  professional-print, projection, redesign, report-typography, screen`
- `doctypes.Region Key` → 7 available `region_key` values: `dach, eu-europass, eu-generic,
  france, gulf-gcc, uk, us`
- `structures.Section Order` → 11 available `canonical_section` values: `certifications,
  contact, education, experience, languages, projects, publications, references, skills,
  summary, volunteering`

**DONE at Revision 3.** All five are declared (`cv-regions.Section Order` was the one this
list missed). The `typefaces.Scale Key` values above are now enforced rather than checked by
eye — see §7.

---

## 7. Revision 3 regeneration — 174 columns, 13 FKs, and one new class of gate output

`python3 ../../research/build-manifest.py` from this directory:

```
wrote data\schema-manifest.json -- 14 tables, 174 columns, 13 foreign keys (5 group)
```

**Manifest changes, all four forced by the document rather than chosen here:**

1. **Five `group` foreign keys declared** (§1.1 closed): `doctypes.Constraint Set Keys` →
   `constraints.Set Key` (list), `doctypes.Region Key` → `cv-regions.region_key`,
   `typefaces.Scale Key` → `type-scales.scale_key`, `structures.Section Order` →
   `headings.canonical_section` (list), `cv-regions.Section Order` →
   `headings.canonical_section` (list). The generator's final assert was relaxed for these:
   a `group` FK's invariant is *the column exists on the target*, not *the column is the
   target's key*.
2. **`figures.Caption Must State`** added (+1 column). Restores the three per-row facts the
   `Caption Required` yes/no enum could not carry; `research/load-base.py` now splits the
   authored prose across both columns, so this is loader output, not a hand edit, and it
   survives the next re-run.
3. **`cv-regions` field-direction enum** already carried `customary` from load pass 1;
   Revision 3 is where the *document* gained it, so the two now agree.
4. **`doc-reasoning`** is unchanged in shape, but its `Doc Conditions` vocabulary shrank
   from five keys to four: `if_projected` was deleted by the Revision 3 condition-placement
   ruling. Nothing in the manifest expresses that vocabulary (§1.3), so this is recorded
   here and enforced nowhere — worth knowing before someone authors `doc-reasoning.csv`.

### The gate, after regenerating — 14 problems, and 8 of them are new *on purpose*

```
$ python3 scripts/validate_data.py data/base
data\base\doctypes.csv: declared in manifest but file does not exist
data\base\doc-reasoning.csv: declared in manifest but file does not exist
data\base\doc-styles.csv: declared in manifest but file does not exist
data\base\palettes.csv: declared in manifest but file does not exist
data\base\type-scales.csv: declared in manifest but file does not exist
data\base\structures.csv: declared in manifest but file does not exist
data\base\typefaces.csv:2:Scale Key: 'ens-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:3:Scale Key: 'cv-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:4:Scale Key: 'report-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:5:Scale Key: 'report-screen' does not resolve to type-scales.scale_key
data\base\typefaces.csv:6:Scale Key: 'report-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:7:Scale Key: 'report-technical' does not resolve to type-scales.scale_key
data\base\typefaces.csv:8:Scale Key: 'form-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:9:Scale Key: 'report-print' does not resolve to type-scales.scale_key

14 problem(s) found        (exit 1)
```

**Read this correctly: the eight new lines are the declaration working, not a regression.**
`typefaces.csv` is authored and `type-scales.csv` is not, so its `Scale Key` genuinely does
not resolve. Until Revision 3 that FK was undeclared and the failure was invisible — §6's
TODO checked those six values *by eye*. They clear the moment `type-scales.csv` lands with
`cv-print, ens-print, form-print, report-print, report-screen, report-technical`, and the
gate now says exactly which six.

The other four newly-declared FKs produce nothing, correctly: three point out of tables that
are not authored yet, and the fifth — `cv-regions.Section Order` → `headings.canonical_section`
— is the first group FK with **both sides on disk**. All 14 rows × their section lists
resolve against the 11 canonical sections. That is the format's first live pass.

**Suggested harness change, for whoever owns `validate_data.py`:** suppress row-level FK
failures against a target table that failed to load at all. The missing file is already
reported once; re-reporting it per referencing row is a cascade, and it will get much louder
than eight lines when `doctypes.csv` (35 rows × 5 FKs) lands before its targets do. Not
implemented here — it is a validator behaviour decision, not a manifest one.

**Test suite after the change:** `67 passed, 8 subtests passed`.

**Stale artifact:** `skill/dist/document-design-intelligence-0.0.1-dev.zip` ships the
Revision 2 manifest (14 tables, 173 columns, 8 FKs). It needs a rebuild before the next
upload test. *Still true at Revision 4.*

---

## 8. Revision 4 regeneration — two new manifest keys, and the gate drops to 13

`python3 ../../research/build-manifest.py` from this directory:

```
wrote data\schema-manifest.json -- 14 tables, 174 columns, 13 foreign keys (5 group), 8 list columns, 1 reference columns
```

Shape is unchanged — same 14 tables, same 174 columns, same 13 FKs. What is new is that two
manifest keys the harness had always supported are now populated: `list_columns` (§1.4) and
`reference_columns` (§1.2). Plus one enum value: T6 `Role` gains `legal`, inserted as the
size-ordered **floor** below `label`, because T9 already shipped `legal-text-min-size`
(threshold 8) with no T6 role to resolve against.

### The gate — 13 problems, down from 14

```
$ python3 scripts/validate_data.py data/base
data\base\doctypes.csv: declared in manifest but file does not exist
data\base\doc-reasoning.csv: declared in manifest but file does not exist
data\base\doc-styles.csv: declared in manifest but file does not exist
data\base\palettes.csv: declared in manifest but file does not exist
data\base\type-scales.csv: declared in manifest but file does not exist
data\base\structures.csv: declared in manifest but file does not exist
data\base\typefaces.csv:2:Scale Key: 'cv-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:3:Scale Key: 'report-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:4:Scale Key: 'report-screen' does not resolve to type-scales.scale_key
data\base\typefaces.csv:5:Scale Key: 'report-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:6:Scale Key: 'report-technical' does not resolve to type-scales.scale_key
data\base\typefaces.csv:7:Scale Key: 'form-print' does not resolve to type-scales.scale_key
data\base\typefaces.csv:8:Scale Key: 'report-print' does not resolve to type-scales.scale_key

13 problem(s) found        (exit 1)
```

**Composition: 6 unauthored-table + 7 `typefaces.Scale Key`.** Both classes are expected and
neither is a regression — see §7. The Scale Key count fell from 8 to 7 because the loader now
skips brand-scoped rows and `ens-manrope-inter` (the only `ens-print` reference) is gone from
`base/`; the six values still needed from `type-scales.csv` are `cv-print`, `form-print`,
`report-print`, `report-screen`, `report-technical` — five distinct, `ens-print` no longer
among them, since it belongs in `data/brand/ens/`.

**The number is diagnostic. If a later change moves it, read it this way:**

| gate | means |
|---|---|
| **13** | correct |
| 17 | the `Threshold` `T#:` → manifest-name normalisation regressed (4 `T7:` rows) |
| 14 | a brand-scoped row is back in `data/base/` |
| 15 | a `Threshold` reference names a table or column that does not exist |

**`data/base/` is generic-only, and now enforced.** `research/load-base.py` skips every draft
row whose `Brand Scope` is not `generic` and reports what it skipped
(`typefaces: skipped 1 brand-scoped rows: ens x 1`). The invariant is
`grep ",ens," data/base/*.csv` returning nothing. `data/base/README.md` states that only the
loader writes the directory and names the one path a brand row may take
(`examples/<brand>-brand.md` → `make_brand_kit.py` → `data/brand/<brand>/`).

**Loader is still idempotent** — re-verified md5-identical over two consecutive runs *after*
these changes, since the normalisation step is a new place it could have broken.

**Test suite after the change:** `109 passed, 8 subtests passed`
(`python3 -m pytest scripts -q`). Higher than §7's 67 because that figure counted
`scripts/tests` alone at an earlier point; no test was removed or skipped.

---

## Revision 4 erratum, 2026-09-08 — the six prose columns, and why this file's md5 did not move

`figures.{Anti-Patterns, Secondary Options, When NOT to Use, Data Volume Threshold,
Static Fallback}` and `cv-regions.Language Expectation` are retyped `text` in
`research/09-library-schema.md` (§9 erratum) and marked with a new S/V/R letter, `P`
(prose payload: feeds no check). **`schema-manifest.json` is md5-identical across the
change — `0b4a079fbbfd2678cc463a78648dbe86` before and after.** That is not an oversight
to be corrected later; it is the point. The manifest carries no per-column *type* field, so
a retype is a fact about the schema document and about nothing the gate reads. Adding a
`type` key to make the change "real" in the manifest was considered and rejected: it would
introduce a second, unvalidated description of every one of the 174 columns.

**What the retype actually protects.** All six hold `; ` as a *sentence* separator. Declaring
any of them in `list_columns` would make the gate **pass while checking the wrong thing** —
the failure mode the eight real list columns exist to prevent, arriving through the door
marked "more validation is better". Worked example, from `figures.csv` row 1:

> `3D bars (Tufte: adds a perspective-distorted third dimension that misrepresents the
> actual 2D magnitude, pure chartjunk); rainbow/spectral palette across categories …`

Split on `;` that is two "tokens", both well-formed, both meaningless as keys. The citation
is the value — it is the reason a curated row beats the model's own guess — and tokenising
to `3d-perspective;rainbow-palette` would delete it. Rejected alternative: keep tokens and
move the prose to a parallel `*-notes` column; it doubles the width of the most prose-heavy
table to feed a validator nobody has written.

**Three of the six were never typed at all.** Only `Anti-Patterns` was actually typed
"text list". `Static Fallback` and `Language Expectation` were already `text`.
`Secondary Options`, `When NOT to Use` and `Data Volume Threshold` had **no row in any
typed column table** — described in T11's prose survey of upstream `charts.csv` and never
tabled. That is the worse state: an undeclared `;`-bearing column is what the next
contributor declares as a list by guessing right about the delimiter and wrong about the
meaning. `build-manifest.py` now carries a DO-NOT-DECLARE comment at both tables.

**Unchanged and expected after this erratum:** manifest md5 `0b4a079f…`, 14 tables /
174 columns / 13 FKs (5 group) / **8 list columns** / 1 reference column, gate **13**
problems with the same 6 + 7 breakdown, `109 passed, 8 subtests passed`, loader idempotent.
A moved list-column count is the specific regression to look for here: it would mean
somebody declared one of the six.

---

## Erratum 2, 2026-09-09 — the "6 unauthored-table" gate is stale; all 14 now load

The "gate 13 problems, 6 unauthored-table + 7 `typefaces.Scale Key`" figure quoted above
(§7, §8, and the erratum before this one) described a real point-in-time state, but it is no
longer the current one and was being read as ongoing truth, including by
`make_brand_kit.py`'s own docstring, which cited `structures.csv` as one of the tables that
"do not exist yet" to justify leaving `Structure Key` blank on every generated doctype row.
`structures.csv` (17 rows) and the other five then-unauthored tables — `doctypes.csv`,
`doc-reasoning.csv`, `doc-styles.csv`, `palettes.csv`, `type-scales.csv` — are all authored
now, `typefaces.Scale Key` resolves everywhere, and `python3 scripts/validate_data.py
data/base` reports **zero** problems: `OK: validated 14 table(s), 291 row(s)`.
`make_brand_kit.py` now emits a real `structure_key` (from `data/base/structures.csv`) for
every v1 doctype that has an honest generic match, and leaves it blank with a printed NOTE
only for `social`, which has none (a canvas post has no document structure to name) — the
same treatment already used for its `Reasoning Key` and `Page Format Key` gaps.

## 9. `doc-styles.Table Rules` — the four enum values, semantics, A8

`Table Rules` (`build-manifest.py`) has four values. Each states what a renderer draws on a
table, not a vibe:

- `none` — no table-level rule lines at all. No table in the direction, or the table has no
  distinguishing rule treatment.
- `hairline` — a hairline rule on every row boundary AND every column boundary: a full ruled
  grid, but thin (`Rule Hair pt`), not boxed/filled. Used by `report-classic-serif`'s and
  `cv-europass`'s tables, where a full grid is the intended reading (a proficiency grid, a
  running-head rule system).
- `header-and-total` — a rule under the header row and a rule above the total row only, no
  other row or column rules. Used by line-item tables (`form-grid-underline`,
  invoice/quote/form doctypes).
- `row-hairlines` (added A8) — a horizontal hairline between rows ONLY: no vertical rules, no
  cell boxes, no column grid. Distinct from `hairline` specifically because `hairline` alone
  does not rule out a full grid, and a renderer defaulting to "draw table borders" reads
  `hairline` as "box every cell." research/72's blind Opus panel (all three judges, verbatim)
  read `cv-dach-tabular`'s rendered table — authored with `Table Rules=hairline` and a
  Checklist line saying "row padding rather than cell borders" — as a "fully boxed contact
  grid" / "gridded table" (cell-border ratio 1.0, 12/12 cells individually boxed in the
  rendered docx). The Checklist's prose was never wrong; the machine-readable column a
  renderer actually consumes (`ddi.py`'s `_doc_style_lines`, ultimately printed into the
  handoff a renderer reads) carried no signal against boxing. `row-hairlines` closes that
  gap: it is a distinct token from `hairline`, so a renderer cannot conflate "row separators
  only" with "full grid" by reading the same enum value both directions were using.
  `cv-dach-tabular` is the only row using it as of A8; ONE existing row (`cv-dach-tabular`)
  moved from `hairline` to `row-hairlines`, `report-classic-serif` and `cv-europass` keep
  `hairline` because they DO want the full grid.

A renderer building a `docx` handoff sees this explicitly: `_doc_style_lines` (ddi.py) prints
the raw `Table Rules` value AND, for `row-hairlines` specifically, an explicit instruction
line spelling out "horizontal hairlines between rows only; no vertical rules; no cell
borders" — see `ddi.py`'s `TABLE_RULES_INSTRUCTIONS` map — so a renderer does not have to
infer the no-boxes rule from the bare token.

A second, unrelated defect research/72's judges also named — a section heading with no space
after `cv-dach-tabular`'s table ("heading collision") — gets the same explicit-line treatment
via `ddi.py`'s `STYLE_SPACING_INSTRUCTIONS` map, keyed by `style_key` rather than by an enum
value since it is a rule specific to this one style's layout, not a `Table Rules` semantic.
