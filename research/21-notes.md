# Notes for 21-t7-page-formats-draft.csv / 21-t9-print-constraints-draft.csv

Both CSVs parse cleanly with `csv.reader`: T7 = 21 columns × 11 data rows, T9 = 7
columns × 11 data rows, no malformed rows (verified by script, not by eye).

---

## Flags for the schema author (read before merging)

1. **T7 has no provenance column** (confirmed against `09-library-schema.md:762-780`
   — the table's own "Sourced values" summary at :788-816 is explicitly *not* a
   column, "provenance that does not change validator behaviour belongs in
   `rationale/page-formats.md`"). Every numeric cell's source tag is in §1 below
   instead, keyed by row, as instructed.
2. **`Threshold` as a `T7:<Column>` join marker is a proposal, not an established
   convention.** No existing T9 row (16-t9-constraints-draft.csv) does this — every
   existing threshold is a literal number or word. I introduced it for the four rows
   where the real limit is per-format (bleed, safe margin, both DPI floors) rather
   than a fixed constant, because a hardcoded number here would be a second source
   of truth for a value T7 already stores — the same reasoning the schema itself
   used to justify *not* storing a CPL range on T7 (`09-library-schema.md:823-826`).
   It's licensed by the schema's own prose at `09-library-schema.md:1012`, which
   states `pro-trim-safe-margin`'s threshold as "≥ T7 `Safe Margin mm`" rather than
   a number — I made that prose machine-readable. `Parameter` stays a bare metric
   token (`bleed_mm`, `safe_margin_mm`, `dpi_raster`, `dpi_line_art`) matching
   existing rows like `selectable_ratio`, `columns` — no key the four validators
   don't already declare. Confirm or reject this convention before merge; if
   rejected, these four rows need real per-row numbers instead, which reintroduces
   the duplication.
3. **`pro-fold-geometry` is an addition beyond the schema's own 7-row professional-print
   summary table** (`09-library-schema.md:1006-1014` lists bleed / output-intent /
   color-space / fonts / safe-margin / dpi-raster / spot-color, not fold-geometry).
   `validate-fold-geometry` is a real, already-named validator (§4 entry 27) that had
   no T9 activation row anywhere — without one, `Fold Type`/`Panels mm`/`Stock gsm`
   on T7's fold rows are unenforced. Added it; flagging the addition rather than
   silently expanding the set.
4. **`pro-min-dpi-line-art` is likewise an addition** — the summary table only names
   `pro-min-dpi-raster`, but T7 carries two DPI columns (`Min DPI Raster`, `Min DPI
   Line Art`) and only one was bound. Added the second for the same reason as #3.
5. **Severity vocabulary normalized to `fail`/`warn`.** The assignment message said
   "refuse / warn"; T9's actual `Severity` enum (`09-library-schema.md:982`) and
   every row in `16-t9-constraints-draft.csv` use `fail`/`warn` — "refuse" appears in
   the schema only as prose describing what `fail` *does* at runtime
   (`09-library-schema.md:256,933`), never as a literal column value. Used the
   schema's actual enum.
6. **Constraint IDs are exactly the schema's own**, not invented: `pro-bleed-geometry`,
   `pro-trim-safe-margin`, `pro-output-intent-present`, `pro-color-space-cmyk`,
   `pro-fonts-embedded`, `pro-min-dpi-raster`, `pro-spot-color-declared` are copied
   verbatim from `09-library-schema.md:1006-1014`. `print-contrast-ratio` and its
   `scope=` parameter grammar are copied from the schema's own worked example at
   `09-library-schema.md:997`. Only `pro-fold-geometry`, `pro-min-dpi-line-art`, and
   `print-contrast-ratio-large` (the 3:1 large-text counterpart the schema's example
   only implies) are new — all three bind an already-named validator, none invents one.

---

## §1 — T7 row sources (no provenance column exists; tags live here)

| Row | Field | Value | Source |
|---|---|---|---|
| all rows | Trim sizes | — | FACT — ISO 216 (A4/A5/A3/A2/A1), ISO 269 (DL), convention for US Letter/business card — see `14-print-production-values.md` §2.1, reproduced at `09-library-schema.md:790-794` |
| all rows | Bleed mm = 3 (standard), 5 (poster-a2/a1) | convention, near-universal shop minimum / large-format bucket | `14-print-production-values.md` §2.2 |
| all rows | Safe Margin mm = 5 (business-card, standard), 6 (A3, poster-a2/a1) | convention | `14-print-production-values.md` §2.2. **Judgment call, not directly sourced**: A3 and posters A2/A1 were bucketed under the "poster/flyer ≤A2" 6mm figure by size proximity, not because report 14 named A3/A1 specifically — flagging so the author can re-bucket if they disagree |
| a4-trifold | Panels mm = 99.5;99.5;98.0 | convention, no single authoritative A4-specific source, figures cluster here | `14-print-production-values.md` §2.3 |
| letter-gatefold | Panels mm = 53.175;54.775;54.775;53.175 | shop formula (wide=W/4+0.8mm, narrow=wide−1.6mm), W=215.9mm US Letter width | `14-print-production-values.md` §2.3; verified sums to 215.9 |
| letter-zfold | Panels mm = 93.13;93.13;93.14 | FACT — no panel tucks, no compensation; sums to 279.40mm exactly | `14-print-production-values.md` §2.3 |
| a4-trifold, letter-gatefold, letter-zfold | Stock gsm = 120 | convention, text-weight bucket (80–100lb ≈ 120–150gsm); matches the schema's own generic example row already using 120 | `14-print-production-values.md` §2.4 |
| business-card-eu | Trim = 85×55mm | convention, regional (EU) — **defaulted to EU over US (88.9×50.8mm) and ISO/A8 (74×52mm) because no default was specified; this is my choice, not a sourced preference** | `14-print-production-values.md` §2.1 |
| business-card-eu | Stock gsm = 400 | convention, 14–18pt ≈ 350–450gsm bucket, midpoint | `14-print-production-values.md` §2.4 |
| poster-a2, poster-a1 | Stock gsm = blank | **cannot be sourced to a figure** — carried forward, see §2 below | `14-print-production-values.md` §2.4 / §5 |
| all rows | Min DPI Raster = 300 (standard), 150 (poster-a2/a1) | convention — 2× a 150lpi halftone screen / halve-per-doubling-of-viewing-distance rule | `14-print-production-values.md` §2.5 |
| all rows | Min DPI Line Art = 600 | convention | `14-print-production-values.md` §2.5. Not distance-adjusted for large format — only one line-art figure was sourced, applied uniformly |
| all rows | Fold Type = none / tri-fold / gate-fold / z-fold | derived from which row this is, not independently sourced beyond the panel geometry itself | — |
| all rows | Print Mode = professional | **not a report-14 value — my own choice.** Every row here carries bleed/stock/DPI data sourced specifically for print-shop production, which is what `professional` gates; the schema's existing `office`/`photocopy` example rows (e.g. `a4-ens-note`) are separate and untouched | — |
| all rows | Columns = 1, Running Head = none, Folio Style = none | **structural default, not a sourced print value.** Every row here is a single physical sheet/panel (flyer, card, poster, brochure panel) — a single sheet definitionally has no running head or folio, and 1 column is the simplest default a doctype-specific row can override | — |
| all rows | Margin Top/Bottom/Inside/Outside mm, Measure mm | **left blank — out of scope.** These are text-layout/typography decisions (report 03 §D domain: line length, page furniture), not print-production physical facts. Populating them was not part of this task and I didn't want to invent generic numbers dressed as sourced ones | — |

---

## §2 — Cannot be sourced (carried over from `14-print-production-values.md` §5, plus this round's additions)

- **Single-panel flyer/poster stock as a specific gsm figure.** No authoritative
  citation found beyond "heavier for standalone pieces" — `Stock gsm` left blank on
  `poster-a2`/`poster-a1`.
- **A closed-form roll-fold panel formula.** Sources state this explicitly (source
  cited in report 14: "the most complex panel sizing of any common fold type," no
  fixed formula). **Dropped the `letter-rollfold` T7 row entirely rather than ship it
  with an empty `Panels mm`** — a `roll-fold` row with no panels would pass
  `validate-fold-geometry` vacuously or hard-fail outright depending on how the
  validator treats an empty list, and either way it's a guaranteed failure state, not
  a genuinely-sourced row. Author one concrete instance (tagged as one shop's
  numbers, not a general formula) if a roll-fold row is needed before this ships.
- **A formal print-legibility contrast standard.** Confirmed absent, not unfound —
  `print-contrast-ratio` uses the WCAG relative-luminance formula as the least-bad
  real substitute (severity `warn`, per the schema's own reasoning at
  `09-library-schema.md:1030-1034`).
- **fsType / font-embedding stdlib readability.** Out of scope for this specialist,
  routed elsewhere per the schema (`09-library-schema.md` §7 Q1) — not represented in
  either CSV.
- **Live verification of WeasyPrint's bleed-fill and PDF/X-4 validity in the actual
  sandbox.** Not a CSV-row question — tracked in `17-print-live-tests.md` /
  `TESTS-FOR-USER.md`, results not yet in.

---

## §3 — Severity count (T9, this file only)

`fail`: 5 — `pro-bleed-geometry`, `pro-fold-geometry`, `pro-output-intent-present`,
`pro-color-space-cmyk`, `pro-fonts-embedded`.

`warn`: 6 — `pro-trim-safe-margin`, `pro-min-dpi-raster`, `pro-min-dpi-line-art`,
`pro-spot-color-declared`, `print-contrast-ratio`, `print-contrast-ratio-large`.

`pro-color-space-cmyk` is `fail` **by design and stays that way until an ICC asset
ships** — it is scoped to fire only when `print_tier=cmyk-press` (tier 3) via its
`Parameter`'s `condition=` clause, and tier 3 is unreachable on every current T8 row
per `09-library-schema.md:909-914`. That is the schema's own intentional hard-fail,
not a defect in this row — restated here per the task's explicit instruction to flag
it.
