# Re-header map — authored drafts → Revision 2 headers

One pass, one person. Every authored CSV below is Rev-1-era or pre-schema; this is what each
needs to become before it loads into `skill/document-design-intelligence/data/base/`.

Authoritative header for every table: `data/schema-manifest.json` (`tables.<name>.columns`,
exact names, exact order). `validate_data.py` fails on any diff, including reordering, so
**column order matters as much as spelling**.

Legend: **+** add · **−** remove · **→** rename · **~** value change

---

## 1. `21-t7-page-formats-draft.csv` → `page-formats.csv`

**No changes. The header already matches Revision 2 exactly, all 21 columns in order.**
Load as-is. (Noted because it is the only one, and because it means T7's Rev 2 column work
and the author's landed on the same answer independently.)

Content note, not a header change: no roll-fold row was authored, because no closed-form
panel formula exists. `roll-fold` stays in the `Fold Type` enum for when one is.

---

## 2. `16-t9-constraints-draft.csv` + `21-t9-print-constraints-draft.csv` → `constraints.csv`

Both files share one header and both merge into one table (38 non-print + 11 print rows).

| | Column | Action |
|---|---|---|
| + | `Element Scope` | **insert between `Check` and `Parameter`.** Allow-list enum; **empty = whole document**. There is no `all` value |

Final order: `constraint_key, Set Key, Applies To, Check, Element Scope, Parameter, Threshold, Severity`

**Value moves, per row:**

| ~ | From | To |
|---|---|---|
| `report-measure-cpl` | `Parameter: cpl_min=45;cpl_max=75;scope=body-paragraph;exempt=table-cell\|caption\|sidebar-column` | `Element Scope: body-paragraph`; `Parameter: cpl_min=45;cpl_max=75` |
| any row using container `caption` | `caption` | `caption-block` — `caption` is already a T6 `Role` and one token must not mean two things |
| print rows | `Threshold: T7:<Column>` | unchanged — Rev 2's polymorphic `Threshold` covers it. **Colon is canonical**; the schema previously wrote `T12.max_pages` with a dot and has been corrected to `T12:max_pages` to match these rows |
| every other row | — | `Element Scope` empty |

**Row-level merges (deletions — confirm before running):**

| − | Rows | Replacement |
|---|---|---|
| 5 rows | `us-cv-length-under10y`, `us-cv-length-10y-plus`, `uk-cv-length`, `eu-cv-length`, `gulf-cv-length` | one row `cv-page-count`, `Applies To: doctype:cv-*`, `Threshold: T12:max_pages`. The `condition=experience_years<10` Parameter disappears — the seniority band *is* the T12 lookup key |
| 4 rows | `us-cv-no-photo`, `us-cv-no-dob`, `us-cv-no-marital-status`, `gulf-cv-photo-expected` | one row `cv-field-norms`, `Check: validate-text-safe-fields`, empty `Threshold`. The validator reads direction from T12, including Gulf's inverted polarity |
| 2 rows → 1 | `print-legibility-l-delta` (16) and any `print-l-delta` (21) | one row `print-contrast-ratio`, `Set Key: print-legibility`, `Applies To: doctype:*`, `Check: validate-contrast-print`, `Threshold: 4.5`, empty `Parameter`. No L\* delta standard exists |
| 1 row | ENS bullet density at 5 | re-key to `ens-deck-density`. A brand slug colliding with a base slug is a refuse-to-run (§0.3); constraint sets **union**, so both 5 and 6 fire |

**Validator renames** (these names must match §4 or `validate-checks-implemented` fails):

| → | From | To |
|---|---|---|
| | `validate-cpl-and-leading` | `validate-measure` + `validate-leading-ratio` (two rows) |
| | `validate-table-style` | `validate-table-rules` + `validate-table-alignment` (two rows) |
| | `validate-series-count` | `validate-chart-series` |

All other validator names in both drafts are adopted into §4 unchanged.

---

## 3. `18-cv-region-rules.csv` → `cv-regions.csv`

| | Column | Action |
|---|---|---|
| + | `cv_region_key` | **first column.** Surrogate key, `<region>-<band>`, e.g. `uk-early` — the manifest allows one key column and this table's natural key is composite |
| → | `region` | `region_key` |
| → | `seniority_band` | `Seniority Band` |
| → | `max_pages` | `Max Pages` |
| → | `photo` | `Photo` |
| → | `date_of_birth` | `Date of Birth` |
| → | `nationality` | `Nationality` |
| → | `marital_status` | `Marital Status` |
| → | `visa_status` | `Visa Status` |
| → | `section_order` | `Section Order` |
| → | `education_before_experience` | `Education Before Experience` |
| → | `format` | `Format` |
| → | `language_expectation` | `Language Expectation` |
| − | `source` | **move to `rationale/cv-regions.md`.** Prose provenance is not a column (Rule 2); `Evidence Class` carries the part a validator needs |
| → | `evidence_class` | `Evidence Class` — values uppercase: `FACT` / `CONVENTION` / `CONTESTED` |

**Row collapse: 28 → 14.** `Seniority Band` is now `early` \| `experienced` only. The `mid`,
`senior` and `executive` rows are identical to each other within every region, so keep
`early` and **one** of the other three per region (they agree), and drop the remaining two.
Where `max_pages` differs between `mid` and `senior` in a region, the `experienced` row
takes the **larger** ceiling — it is a `warn` ceiling, and the narrower one is the
unsourced distinction being collapsed.

**Value change:** `section_order` uses `|` as its separator; the schema's list separator is
`;`. Convert.

---

## 4. `18-ats-headings.csv` → `headings.csv`

| | Column | Action |
|---|---|---|
| + | `heading_key` | **first column.** Surrogate, `<section>-<language>-<n>`, e.g. `experience-en-2` |
| | `canonical_section` | unchanged |
| → | `heading_text` | `Heading Text` |
| → | `language` | `Language` |
| → | `is_primary` | `Is Primary` |
| − | `source` | move to `rationale/headings.md` |

`18-ats-headings-rejected.csv` is **not** a table. It is 15 negative-control fixtures for
`validate-canonical-headings`; it belongs with the validator tests, not in `data/base/`.

---

## 5. `19-t5-typefaces-draft.csv` → `typefaces.csv`

| | Column | Action |
|---|---|---|
| + | `Safe Stack Availability` | **insert between `Safe Stack Fallback` and `Embedding Licence`.** Enum `os-bundled` \| `office-bundled` \| `none` |

**~~Blocker~~ — resolved before the load pass ran.** This section previously warned that
`Embedding Licence` and `Has Tabular Figures` were blank in all 8 rows and would fail the
enum check. **That was stale**: the fill task completed, and both columns now carry real
values (`installable`/`editable`, `yes`/`unknown`). Both loaded clean. The reasoning still
stands for any future draft — a strict enum with an `unknown` member is what makes "nobody
has checked this font yet" a visible value rather than an empty cell.

Also verify `Scale Key` values (`ens-print`, `cv-print`, `report-print`, `report-screen`,
`report-technical`, `form-print`) exist as `scale_key` values in `type-scales.csv` — the
author flagged them as intent, not verified rows, and this FK is one of the four the
manifest cannot mechanise (see §8).

---

## 6. `22-t11-figures-draft.csv` → `figures.csv`

| | Column | Action |
|---|---|---|
| | `chart_key` | unchanged — **this key wins over the schema's `figure_key`**, which was never authored |
| − | `Min Physical Size mm` | **cut.** It cannot be a constant — a legible minimum depends on label count, so it is computed, like CPL |
| | `Caption Required` | keep |
| | `Anti-Patterns` | keep — **not** a duplicate of T2's `Anti-Pattern Tokens`; both bind `validate-anti-patterns` at different `Element Scope` (document vs figure) |

Final order: `chart_key, Data Type, Keywords, Best Chart Type, Secondary Options, When to Use,
When NOT to Use, Data Volume Threshold, Accessibility Grade, A11y Fallback,
Accessibility Notes, Label Strategy, Static Fallback, Print Series Max, Greyscale Safe,
Print Palette Roles, Caption Required, Anti-Patterns`

`Colour Guidance` stays dropped — the author omitted it and that is right: its hexes and
opacity percentages are T4's job, which `Print Palette Roles` already points at.

---

## 7. `27-t14-font-substitutes-draft.csv` → `font-substitutes.csv`

| | Column | Action |
|---|---|---|
| + | `substitute_key` | **first column.** Surrogate, `<family>-<lineage>`, e.g. `arial-liberation`. Natural key is (`proprietary_family`, `Lineage`) — Arial, Times and Courier each have two rows |
| + | `Weights Covered` | `;`-list of weight names, e.g. `Regular;Bold;Italic;Bold Italic`. Carlito and Gelasio are the rows that need it |
| ~ | `Lineage` value `other` | → `independent` (Gelasio: OFL, SorkinType, none of the three big lineages, but a real substitute) |
| ~ | `Metric Identical` blank on 6 rows | **keep blank.** Empty = not applicable. `no` is reserved for "a substitute exists but its metrics differ" — currently an empty set |

15 rows, all load.

---

## 8. What still cannot be checked after re-heading

Four foreign keys in this schema point at a **grouping column**, not a key column, and the
manifest format cannot declare those (`data/schema-manifest-NOTES.md` §1.1). After the
re-header they will still be unverified:

- `doctypes.Constraint Set Keys` → `constraints.Set Key`
- `doctypes.Region Key` → `cv-regions.region_key`
- `typefaces.Scale Key` → `type-scales.scale_key`
- `structures.Section Order` → `headings.canonical_section`

`validate-keys` mechanises 4 of 8 FK relationships until the harness gains a `"group": true`
FK form. **Check these four by eye during the re-header pass** — it is the only pass where
someone has all seven files open at once.

---

## 9. Load pass 1 — what actually happened

Executed by `research/load-base.py` (idempotent; re-runs from the untouched drafts).
190 rows into 8 tables. Gate: 6 problems, all "file does not exist" for the six
not-yet-authored tables; **every loaded table passes every check.**

| Table | Rows | What changed |
|---|---|---|
| `typefaces` | 8 | `+Safe Stack Availability`, all `os-bundled` — none of the 8 rows falls back to an Office-only family |
| `page-formats` | 11 | nothing; header already matched |
| `constraints` | 42 | 10 CV rows → 2; `−print-legibility-l-delta`; `report-measure-cpl` rescoped; `+2` binding rows |
| `figures` | 11 | `−Min Physical Size mm`; `Label Strategy` and `Greyscale Safe` and `Caption Required` prose → enums |
| `cv-regions` | 14 | 28 → 14; 13 renames; `−source`; `true/false` → `yes/no`; `\|` → `;` |
| `headings` | 81 | `+heading_key`; 3 renames; `−source` |
| `font-substitutes` | 15 | `+substitute_key`, `+Weights Covered`; `other` → `independent` |
| `render-targets` | 8 | authored fresh from the schema's own T8 section |

### Six corrections to this map, found by running it

1. **The CV collapse is ten rows, not nine.** `uk-cv-no-photo` is a tenth row of exactly the
   same kind and was collapsed with the other four field-norm rows. 10 → 2.
2. **`print-contrast-ratio` is two rows, not one.** §2 said collapse to one; research/21 had
   already authored the correct pair — `4.5` body and `3.0` large-text — which is what §4 of
   the schema actually specifies. Both kept; only `print-legibility-l-delta` was dropped.
3. **`Threshold` references name the *re-headered* column.** `T12:max_pages` is wrong once
   `max_pages` becomes `Max Pages`. The shipped row reads `T12:Max Pages`. The schema's
   §0.1 example needs the same correction.
4. **No `ens-deck-density` row exists to re-key.** research/16 authored the generic `6`
   only. ENS's `5` is a brand row and belongs in `data/brand/ens/constraints.csv` per §0.3,
   never in `data/base`. The re-key instruction is a no-op for this pass.
5. **`customary` is a fifth field-direction value** in T12, not in my enum. Manifest widened.
6. **Two rows in `18-cv-region-rules.csv` are malformed CSV** — `EU-Europass,mid` and
   `Gulf-GCC,early` have unescaped commas in `source`, so the parser overflows and
   `evidence_class` lands in the overflow list. The loader recovers it (last field) and
   drops `source` anyway, so the load is correct — **but the draft should be fixed at
   source**, because the next person to read that file with a plain `csv.DictReader` gets
   silently wrong values in the last column.

### Information dropped, recorded rather than lost

`research/26-t11-caption-qualifications.md` holds the three `Caption Required` prose
qualifications ("must state bin width", "should state sample size (n)", "captioned ABOVE the
table") that a `yes`/`no` enum cannot carry. They want a `Caption Must State` text column in
Revision 3 — the fact is real, per-row, and currently only in provenance.

`Label Strategy` prose collapsed to the enum on 4 of 11 rows (`comparison-many`,
`correlation`, `geographic` → `either`; the rest → `direct`). The conditions the author
wrote — "direct where category count allows; legend only if colour-encoding a second
dimension" — are exactly what `either` means, so nothing is lost that the enum was ever
meant to carry.
