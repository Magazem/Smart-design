# Notes for Task B1 — extending `21-t7-page-formats-draft.csv`

File is now 21 columns x 22 data rows (11 original + 11 new), csv-clean (verified
with `csv.DictReader`, no malformed rows, no duplicate keys). T1's Page Format Keys
(`26-t1-doctypes-draft.csv`) reference 16 distinct T7 keys; 3 are ENS-scoped
(`a4-ens-note`, `a4-ens-formulaire`, `px-ens-social-1080`) and are intentionally
**not** added here — base ships generic rows only (`RESUME.md` standing rule); ENS
rows have one source, `examples/ens-brand.md -> make_brand_kit.py`. The remaining
13 generic keys minus the 2 already shipped (`a4-trifold`, `letter-gatefold`) are
exactly the 11 rows added: `a3-poster`, `a4-cv-single-col`, `a4-flyer`,
`a4-form-standard`, `a4-letter-standard`, `a4-one-pager`, `a4-report-standard`,
`letter-flyer`, `letter-trifold`, `px-infographic-portrait`, `widescreen-16-9`.

---

## §1 — Measure mm formula (the task's other half)

Two different formulas, because the two row classes have different populated
inputs, per `09-library-schema.md:1059`'s own worked example
(`Measure mm = Trim W mm - Margin Inside mm - Margin Outside mm`, verified against
the schema's `a4-ens-note` example: 210 - 25 - 55 = 130):

- **The 11 original print-shop rows** (`Print Mode=professional`): `Measure mm =
  Trim W mm - 2 x Safe Margin mm` for flat single-panel formats, or `narrowest
  Panels mm entry - 2 x Safe Margin mm` for folded formats (the tuck panel is the
  binding width constraint, same reasoning the schema already uses for fold-in
  allowance). `Safe Margin mm` is the only populated inset available on these rows
  at the time Measure mm was authored, and its own definition
  (`09-library-schema.md:1115-1120`, "how far content must stay inside the trim")
  makes it a legitimate stand-in when no dedicated Margin columns exist.
  **Judgment call**: this reproduces the schema's own `letter-trifold` = 89
  Measure example only approximately (99.5-2x5=89.5, or per-row precision below)
  — that number in the schema table looks illustrative, not reverse-derivable
  exactly; flagging rather than force-fitting.
  **Task B1b (2026-09-09)** filled the four `Margin Top/Bottom/Inside/Outside mm`
  columns on these rows (plus the 4 new `professional`-mode rows below) — see
  the new §4. Every one of these 15 rows now has `Margin Inside mm = Margin
  Outside mm = Safe Margin mm`, which makes the `Measure mm = Trim W mm -
  Margin Inside mm - Margin Outside mm` formula from `09:1059` compute to the
  exact Measure mm value already shipped here, on flat rows against `Trim W mm`
  and on the four fold rows against the narrowest `Panels mm` entry (verified
  for all 15, see §4) — so the two derivations above and the schema's general
  formula are one formula, not two.
- **The 11 new rows**: authored real `Margin Top/Bottom/Inside/Outside mm` values
  (see §2), then `Measure mm = Trim W mm - Margin Inside mm - Margin Outside mm`
  directly — except the 4 new `professional`-mode rows (`letter-trifold`,
  `letter-flyer`, `a4-flyer`, `a3-poster`), which follow the *existing-row* rule
  above instead (blank margins, Safe-Margin-derived Measure) to stay consistent
  with the other print-shop rows they sit beside.

Why new rows couldn't reuse the Safe-Margin fallback: the 7 non-print-shop new
rows all carry `Safe Margin mm = 0` (office/photocopy convention, matching the
schema's own `a4-ens-note` example), so the fallback formula would collapse to
`Measure = Trim W` — clearly wrong for a body-text document. Real margins were
authored instead.

---

## §2 — New-row sourcing and judgment calls

| Row(s) | Value | Source / reasoning |
|---|---|---|
| `a4-cv-single-col`, `a4-letter-standard` | Margins 25mm all sides | convention — 1in "safe" margin widely cited for ATS-parseable resumes and standard business letters; **judgment call**, no single citation |
| `a4-form-standard` | Print Mode = `photocopy` | sourced from T1: `form-handfilled` (the doctype that names this key) carries the `photocopy-safe` constraint |
| `a4-form-standard` | Margins 15/20mm | tighter than the letter/CV rows — judgment call, to leave more field-writing space on a fillable form |
| `a4-report-standard` | Folio Style = `roman-front-arabic-body`, Running Head = `centered`, Inside 30mm/Outside 20mm | this one key is shared by `report-short`, `report-long-toc`, `whitepaper`, `proposal` in T1 — `report-long-toc`'s TOC is the reason for the front/body split folio; the extra 10mm on Inside is a binding-margin judgment call, not sourced |
| `a4-one-pager` | Margins 18mm | judgment call — tighter than the letter/CV rows since "one-pager" implies fitting more on the single page |
| `letter-trifold` | Trim 215.9x279.4mm (portrait, unrotated), Panels mm = 93.66;93.66;92.08 | Panels are **FACT**, `14-print-production-values.md` §2.3 / `09-library-schema.md:1091` ("Tri-fold, US Letter"); orientation and the "panels sum to Trim H" convention mirrored from the existing `a4-trifold` row (not from `letter-gatefold`, which sums panels to Trim W instead — the two existing fold rows already disagree on this axis; reproduced rather than resolved, out of this task's scope) |
| `letter-trifold`, `letter-flyer`, `a4-flyer`, `a3-poster` | Bleed/Safe Margin/DPI | copied bucket-for-bucket from the existing sibling rows of the same trim size (`letter-gatefold`/`letter-zfold` for Letter, `a4-trifold` for A4, `a3-professional` for A3) rather than re-deriving from `14-print-production-values.md` |
| `letter-flyer`, `a4-flyer`, `a3-poster` | Stock gsm blank | **cannot be sourced** — same finding as `21-notes.md` §2 ("Single-panel flyer/poster stock as a specific gsm figure... left blank on `poster-a2`/`poster-a1`"); applies identically here, carried forward rather than invented |
| `widescreen-16-9` | Trim 338.67x190.5mm | **FACT** — Microsoft PowerPoint's default "Widescreen" slide preset, 13.333in x 7.5in |
| `widescreen-16-9`, `px-infographic-portrait` | Margins = ~5% inset, rounded | convention — presentation/screen design's usual title-safe inset; **judgment call**, not print-sourced (these aren't trimmed physical sheets, so `Bleed`/`Safe Margin mm` = 0, matching the `a4-ens-note` office/photocopy convention) |
| `px-infographic-portrait` | Trim 285.75x357.19mm (= 1080x1350px @ 96 CSS px/in) | 1080x1350px is the pixel canvas `render-targets.csv`'s `png-social` row already hard-codes (`--window-size=1080,1350`), and `infographic` (T1) is the only other doctype pointing at that render target today — reused rather than invented, to avoid a second source of truth for a canvas size the pipeline already fixes. **Flag**: if a dedicated infographic render target is ever split out from `png-social` with a different window size, this row goes stale — check `render-targets.csv` before trusting it later. 96 px/in is the W3C CSS reference-pixel definition, not print-sourced |
| all 7 non-print-shop new rows | Print Mode = `office` (except `a4-form-standard` = `photocopy`) | none of `office`/`photocopy`/`professional` cleanly fits a projected deck or a screen-native PNG, but `Print Mode` is schema-required (`R V`, `09-library-schema.md:1066`); `office` picked as the "everyday, not press" bucket, consistent with `docx-office`/`pdf-chromium`/`pptx-office` render targets used by these doctypes rather than `pdf-weasyprint-pdfx4` |
| all 11 new rows | Columns=1, Running Head/Folio Style=none (except `a4-report-standard`), Fold Type=none | structural default, same reasoning as `21-notes.md` line 75 — not independently sourced |

---

## §3 — New gap this doesn't close (as of Task B1)

Margins remain blank on all 11 *original* print-shop rows (task scope was Measure
mm, not full margin authoring for those). The `RESUME.md` "NEW GAP" entry about no
required/non-null gate check on non-FK columns is still open — Measure mm being
filled here doesn't add that check, it just satisfies it for T7. **Closed by
Task B1b, see §4** — all four Margin columns are now non-blank on every row.

---

## §4 — Task B1b: filling the 15 blank-margin rows (2026-09-09)

B1 ruling amendment: `Margin Top/Bottom/Inside/Outside mm` are non-nullable `V`
columns (schema `09:1058`, one shared type row for all four), so leaving them
blank on any row — including the 11 `professional`-mode print-shop rows and the
4 new `professional`-mode rows added by B1 (`letter-trifold`, `letter-flyer`,
`a4-flyer`, `a3-poster`) — was never actually in scope; §1 above undersold it as
"out of scope." This task fills all 15.

**Value chosen: `Margin Top mm = Margin Bottom mm = Margin Inside mm = Margin
Outside mm = Safe Margin mm`**, per row (5mm on the 11 rows with `Safe Margin
mm=5`, 6mm on the 4 with `Safe Margin mm=6`: `poster-a2`, `poster-a1`,
`a3-poster`, and `a3-professional`).

Why this value and not another:

- **Forced, not chosen, on Inside/Outside.** Measure mm was already shipped by
  B1 using the formula in §1 (`Trim W - 2xSafe Margin`, or narrowest panel for
  fold rows). The schema's own general formula (`09:1059`) is `Measure mm = Trim
  W mm - Margin Inside mm - Margin Outside mm`. The only `Margin Inside`/`Margin
  Outside` values that keep the already-shipped Measure mm column arithmetically
  true against that formula are `Inside = Outside = Safe Margin mm` — verified
  by direct computation for all 15 rows (11 flat rows against `Trim W mm`, the 4
  fold rows — `a4-trifold`, `letter-gatefold`, `letter-zfold`, `letter-trifold`
  — against the *narrowest* `Panels mm` entry instead, since `Columns` is
  documented as "1 (per panel)" for fold formats, i.e. the four margins are
  per-panel insets on these rows, not flat-sheet insets against the full
  pre-fold `Trim W mm`). Any other Inside/Outside pair makes the shipped
  Measure mm column internally false against `09:1059`.
- **Top/Bottom is an actual judgment call**, unlike Inside/Outside — nothing in
  the file cross-checks it. Set equal to `Safe Margin mm` for uniformity and
  because these are unbound, single-panel-per-side pieces (no running text
  column, no binding edge) with no other sourced inset to draw on; not
  independently verifiable the way Inside/Outside is.
- Reuses an already-sourced column (`Safe Margin mm`, itself sourced from
  `09-library-schema.md`'s worked table, §1 above) rather than inventing a
  second, unsourced inset figure.

**Verification:** `csv.DictReader` — 21 columns x 22 data rows unchanged, no
duplicate keys, zero rows now have any blank Margin cell. Formula cross-check
(`calc = trimw_or_narrowest_panel - inside - outside` vs. shipped `Measure mm`)
matches to <=0.02mm on all 15 rows (the 0.02 tolerance absorbs `letter-gatefold`'s
43.175 vs. shipped 43.18 rounding, already present pre-B1b).

**Scope:** draft file only (`research/21-t7-page-formats-draft.csv` and this
notes file). `data/base/page-formats.csv` untouched — only `research/load-base.py`
writes there per `RESUME.md`'s standing rule.
