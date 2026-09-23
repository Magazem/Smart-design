# research/83 — Adversarial audit: grand-library batch 1 (typefaces + palettes)

Auditor: Opus (adversarial). Date: 2026-09-23. Method: independent re-fetch with curl
(no reuse of the researcher's cached payloads), stdlib parsing, `scripts/lib/color.py` for all
contrast. No git run; no file edited except this one.

Scope:
- A. `research/library/typefaces/ranked-pairings.csv` (20 rows) + `-evidence.md` +
  `research/provenance/typefaces-ranked-pairings.csv` (46 rows)
- B. `research/library/palettes/authority-design-systems.csv` (20 rows) + `-evidence.md` +
  `research/provenance/palettes-authority-design-systems.csv` (20 rows)

Both batches are already loaded into `skill/document-design-intelligence/data/base/`
(the typeface and palette rows appear in base `typefaces.csv` / `palettes.csv`).

## Verdicts

| Batch | Verdict | Why |
|---|---|---|
| A. Typefaces (ranked pairings) | **PASS-WITH-FIXES** | All 28 popularity ranks match exactly. All 13 pairing citations say what the provenance claims. All 28 families are OFL. BUT the loaded base **fails `test_provenance.py` (8 failures)**: 7 Typewolf rows are `ranked` with a blank Rank Value, and 13 pairings cite the same (Table, Row Key, URL) triple twice. One row (`lib-dm-serif-display-dm-sans`) breaks the batch's own pre-registered ≥4-weight filter, and the evidence file wrongly says it doesn't. 5 `unknown` tabular-figure cells are demonstrably `yes`. |
| B. Palettes (design-system tokens) | **PASS-WITH-FIXES** | 252 of 256 hex cells trace to a fetched source under the claimed token. All On-X / Foreground-Background pairs are ≥4.5:1. BUT `lib-material3-purple` is `search-corroborated` (breaks R-a) and uses legacy M3 hexes (`#1C1B1F`, surface `#FFFBFE`) that the current fetched token source does not carry. Two dark-slide rows list `accent` as Text-Safe at 3.62:1 and 4.37:1 against their background. |

## Check table

### A. Typefaces

| # | Check | Evidence (URL / method) | Observed | Result |
|---|---|---|---|---|
| A1 | Popularity rank, all 28 families in provenance (not a sample) | `curl https://fonts.google.com/metadata/fonts` → 200, 2,702,073 B, 1,946 families, `familyMetadataList[].popularity` | Roboto 2, Open Sans 3, Inter 5, Montserrat 7, Poppins 8, Lato 9, Noto Sans 20, DM Sans 22, Nunito 24, Nunito Sans 26, Merriweather 33, Source Sans 3 48, Noto Serif 61, Fira Sans 62, Libre Baskerville 67, Libre Franklin 80, EB Garamond 84, Bitter 93, Cabin 106, DM Serif Display 107, Merriweather Sans 136, Archivo Narrow 175, Spectral 180, Roboto Serif 181, Alegreya Sans 187, Vollkorn 212, Alegreya 268, Fira Mono 361 | **PASS: 28/28 exact** |
| A2 | Sort direction | same payload | lowest values = Roboto/Open Sans/Google Sans/Inter; ascending = more popular | PASS |
| A3 | Evidence claim "list is otherwise contiguous" (evidence.md, below Top-60 table) | sorted popularity values | `[2,3,4,5,7,8,9,10,14,16,17,19…]`: values 1, 6, 11, 12, 13, 15, 18 are absent. The field is not a dense rank. | **FAIL (evidence prose only)** |
| A4 | Licence filter | `raw.githubusercontent.com/google/fonts/main/ofl/<dir>/METADATA.pb` for all 28 families; `isOpenSource` in metadata | all 28 return 200 under `ofl/`; all `isOpenSource: true` | PASS |
| A5 | Weight filter (≥4 static weights or `wght` axis) | metadata `fonts` keys + `axes` | All heading/body families pass except **DM Serif Display: 1 weight (400), no axes**, which is the row's *Heading Family*. Fira Mono (3 weights) is only in `Mono Family`, so the auxiliary exception is honest there. | **FAIL: lib-dm-serif-display-dm-sans** |
| A6 | Evidence claim that DM Serif Display is "kept only in an auxiliary role" | ranked-pairings.csv row | `Heading Family = DM Serif Display` | **FAIL: evidence is false** |
| A7 | Typewolf pairing: Libre Baskerville | `curl https://www.typewolf.com/libre-baskerville` (200) | "Suggested Font Pairing Libre Baskerville + Libre Franklin" | PASS |
| A8 | Typewolf: EB Garamond | typewolf.com/eb-garamond (200) | "Suggested Font Pairing EB Garamond + Cabin" | PASS |
| A9 | Typewolf: Bitter | typewolf.com/bitter (200) | "Suggested Font Pairing Bitter + Montserrat" | PASS |
| A10 | Typewolf: Spectral | typewolf.com/spectral (200) | "Suggested Font Pairing Spectral + Source Sans Pro" (the rename to Source Sans 3 is disclosed) | PASS |
| A11 | Typewolf: Vollkorn | typewolf.com/vollkorn (200) | "Suggested Font Pairing Vollkorn + Montserrat" | PASS |
| A12 | Typewolf: Archivo Narrow | typewolf.com/archivo-narrow (200) | "Suggested Font Pairing Archivo Narrow + Merriweather" | PASS |
| A13 | Typewolf: Alegreya | typewolf.com/alegreya (200) | "Suggested Font Pairing Alegreya + Alegreya Sans" | PASS |
| A14 | Roboto Serif companion | fonts.withgoogle.com/roboto-serif (200) | "This latest addition to the Roboto superfamily fills the need for a highly readable serif that pairs well with the sans-serif versions of Roboto." | PASS |
| A15 | Merriweather Sans companion | github.com/SorkinType/Merriweather-Sans + raw README (200) | About: "The Sans companion to the serifed Merriweather"; README: "It is a companion to the serif typeface family Merriweather." | PASS |
| A16 | DM suite | raw googlefonts/dm-fonts README (200) | "This repository contains for DM suite of fonts: Sans, Serif Text and Serif Display." | PASS (but see A5) |
| A17 | Fira Mono companion | en.wikipedia.org/wiki/Fira_(typeface) (200) | "Fira Sans is accompanied by a monospaced variant called Fira Mono, available in the weights of regular, medium, and bold." | PASS |
| A18 | Noto Serif/Sans companion | en.wikipedia.org/wiki/Noto_fonts (200) | "Noto Sans and Noto Serif contain Latin, Greek and Cyrillic glyphs." True, but it states glyph coverage, not a pairing. | WEAK (advisory) |
| A19 | Nunito Sans companion | fontsinuse.com/typefaces/85917/nunito-sans (200) | "A non-rounded version of Vernon Adams' Nunito, added by Jacques Le Bailly in 2017." The quote is real, but Fonts In Use is a third party, not the publisher, so the provenance label "Publisher-documented companion" is wrong. A publisher source exists: `google/fonts/ofl/nunitosans/DESCRIPTION.en_us.html` says "Nunito is a well balanced sans serif typeface superfamily, with 2 versions… an accompanying regular non-rounded terminal version, Nunito Sans." | FIX (label/source) |
| A20 | Provenance business rules (§2C) | `python -m pytest scripts/tests/test_provenance.py` on loaded base | **8 failed, 9 passed.** (a) `test_ranked_rows_require_url_metric_value_and_date`: 7 subtests fail, the `typefaces:*:3` Typewolf rows, which are `ranked` with blank Rank Value. (b) `test_table_row_key_source_url_triples_are_unique`: 13 pairings each carry 2 rows with the same `https://fonts.google.com/metadata/fonts` URL. | **FAIL** |
| A21 | Typewolf evidence class precedent | base `provenance.csv` | `designs:cv-dach-tabular:1` and `designs:cv-editorial:1` already cite Typewolf as `authority` | informs fix |
| A22 | Has Tabular Figures: 9 fonts from `raw.githubusercontent.com/google/fonts/main/ofl/...`, parsed with stdlib GSUB FeatureList and cmap/hmtx, per the research/09 rule "`tnum` present → yes; absent → unknown" | font binaries | tnum present: **Roboto, Lato, Inter, Montserrat, Fira Sans**, Spectral, EB Garamond. tnum absent: Poppins (proportional default digits), Libre Baskerville (proportional). Spectral=`yes` confirmed. | 5 cells should be `yes` (FIX); Poppins/Libre Baskerville correctly `unknown` |
| A23 | Embedding Licence `installable` | OS/2 `fsType` of the same 9 binaries | all `fsType=0` (installable) | PASS |
| A24 | Safe Stack fallbacks match category | row inspection vs research/09 T5 notes | serif heads → Georgia / Times New Roman / Cambria; sans → Arial / Calibri; Archivo Narrow → Arial, Merriweather body → Georgia. Row-level Availability takes the worst case (Cambria/Calibri → `office-bundled`). Category-correct. Advisory: 4 sans rows (Inter, Lato, Poppins, Nunito) pick office-bundled Calibri when os-bundled Arial is available, which triggers the `validate-font-resolution` warning. Base rows all use Arial. | PASS (advisory) |
| A25 | Category Contrast / Family Count / derived body-fallback rule | row inspection | consistent. `superfamily` with Family Count 2 for Fira is valid. | PASS |
| A26 | Scale Key appropriateness | base `type-scales.csv` keys | all keys exist. Mapping is sensible (cv-major-third for the 2 CV rows, form-print for condensed form face, deck-projection for deck-led rows). | PASS |
| A27 | Keywords for BM25 | row inspection | Tone/industry terms are present in every row. Noise tokens: `typewolf-pairing`, `publisher-companion`, `google-companion`, `mozilla-superfamily`, `single-family`, `sans-sans` are provenance/schema meta, not user query vocabulary. | ADVISORY |
| A28 | Duplicate vs base | base typefaces.csv | no key or pairing duplicated | PASS |

### B. Palettes

| # | Check | Evidence (URL / method) | Observed | Result |
|---|---|---|---|---|
| B1 | GOV.UK: 9 hexes, 5 rows | `curl https://design-system.service.gov.uk/styles/colour/` (200) | text #0b0c0c, secondary-text #484949, border #cecece, template-background #f4f8fb, brand #1d70b8, "Green primary #0f7a52", "Red primary #ca3535", "Teal primary #158187", "Brown primary #99704a" | PASS |
| B2 | USWDS: 6 hexes, 2 rows | designsystem.digital.gov/design-tokens/color/theme-tokens/ (200) | base-darkest #1b1b1b, base-dark #565c65, base-lighter #dfe1e2, base-light #a9aeb1, primary 'blue-60v' #005ea2, accent-warm-dark 'orange-50v' #c05600 | PASS |
| B3 | Atlassian: 5 hexes | atlassian.design/DESIGN.md (200) | 'text' #292A2E, 'text-subtle' #505258, 'border-input' #8C8F97, 'background-code-gutter' #F0F1F2 (same hex as 'background-accent-gray-subtlest'), 'text-brand'/'link' #1868DB | PASS (the muted token name is odd, advisory) |
| B4 | IBM Carbon: 9 hexes, 5 rows | raw carbon `packages/colors/src/dtcg/colors.json` (200) | gray 100 #161616, 80 #393939, 70 #525252, 20 #e0e0e0, 10 #f4f4f4; green 60 #198038; teal 60 #007d79; purple 60 #8a3ffc; blue 60 #0f62fe | PASS |
| B5 | Fluent: greys + 3 hues, 3 rows | raw fluentui `packages/tokens/src/global/colors.ts` (200) | grey '4' #0a0a0a, '8' #141414, '14' #242424, '20' #333333, '92' #ebebeb, '94' #f0f0f0; burgundy primary #a4262c; grape primary #881798; blue primary #0078d4 | PASS |
| B6 | Tailwind: 6 hexes | unpkg tailwindcss@3.4.1/lib/public/colors.js (200) | stone 50 #fafaf9, 200 #e7e5e4, 300 #d6d3d1, 700 #44403c, 900 #1c1917; amber 700 #b45309 | PASS |
| B7 | Radix: 11 hexes, 2 rows | cited radix-ui.com/colors/docs/palette-composition/scales (200): hexes present only as swatch `background-color` styles, with no token names in text. Cross-checked against unpkg `@radix-ui/colors@3.0.0/index.js` (200). | red12 #641723, red11 #ce2c31, red6 #fdbdbe, red3 #feebec, red1 #fffcfc, sand12 #21201c, sand11 #63635e, sand6 #dad9d6, sand3 #f1f0ef, sand1 #fdfdfc, bronze11 #7d5e54 | PASS (advisory: add package URL as the name-bearing source) |
| B8 | Material 3 | m3.material.io/styles/color/roles (200, 61,737 B) contains **0** occurrences of `6750a4` (JS-rendered). Static source: raw material-web `tokens/versions/v0_192/_md-sys-color.scss` + `_md-ref-palette.scss` (200). | Light roles: on-surface = neutral10 = **#1d1b20**; surface = neutral98 = **#fef7ff**; on-surface-variant = n-v30 #49454f ✓; surface-variant = n-v90 #e7e0ec ✓; outline-variant = n-v80 #cac4d0 ✓; primary = primary40 #6750a4 ✓. `#1c1b1f` appears **nowhere** in the fetched token files. `#fffbfe` appears only as primary99/secondary99/n-v99, not as surface. | **FAIL** (search-corroborated plus stale hexes) |
| B9 | Mechanical hex trace, all 20 rows | every non-white/black hex in each row grepped against its system's fetched file | 256 cells, 4 untraceable: all `#1C1B1F` in lib-material3-purple (Primary, Foreground, On Muted, Rule Strong) | 252/256 |
| B10 | Contrast: all On-X/X + Fg/Bg, whole file | `color.contrast_ratio` | 98 pairs (2 rows have no accent), min 4.53 (fluent-dark-slide On Accent), all ≥4.5. Every ratio in evidence.md matches to 2 dp. | PASS |
| B11 | Text-Safe / Fill-Only vs contrast (rule from `make_brand_kit.derive_palette_row`: role text-safe iff role/Background ≥4.5) | same | All rows consistent **except**: `lib-carbon-dark-slide` accent #0f62fe on #161616 = **3.62**; `lib-fluent-dark-slide` accent #0078d4 on #0a0a0a = **4.37**. Both list accent as Text-Safe. GOV.UK brown (4.40) is correctly Fill-Only. Tailwind amber on stone-50 = 4.81 OK. | **FAIL: 2 rows** |
| B12 | Category Marker Roles | base precedent | Both dark slides use `accent`. Base `brand-accent-print` also has CM=accent with accent Fill-Only, so a fill marker is accepted precedent. Other rows leave CM blank like the base light rows. | PASS (note inconsistency with `derive_palette_row`'s intersection rule, pre-existing) |
| B13 | Rule Hair visibility | Rule Hair vs Background | `lib-fluent-dark-slide` #141414 on #0a0a0a = **1.07**, effectively invisible. Base deck-high-contrast uses 1.69. Fluent light rows #ebebeb on white = 1.19 (faint; base uses 1.61). | FIX (dark), advisory (light) |
| B14 | Keywords for BM25 | row inspection | Good tone/industry coverage overall. `lib-govuk-burgundy` carries `error`, which draws queries about error states. `lib-govuk-forest` and `lib-govuk-teal` carry `health`, which is not in the source. `lib-uswds-orange` carries `brown` for #c05600. | ADVISORY |
| B15 | Near-duplicates vs base | base palettes | `lib-uswds-navy` shares Primary+Accent with base `cv-harvard`, and `lib-carbon-*` share ink+blue with `cv-editorial`. Secondary, muted and rules differ, so they are distinct rows. | PASS (note) |

## FIX LIST

Priority: **M** = must fix before the batch counts as sourced / tests green; **S** = should fix;
**A** = advisory. The column "Source" is the fetched copy that justifies the correct value.

| # | P | File | Row key | Column | Current value | Correct value | Source |
|---|---|---|---|---|---|---|---|
| 1 | M | research/provenance/typefaces-ranked-pairings.csv | `typefaces:lib-alegreya-alegreya-sans:3`, `…lib-libre-baskerville-libre-franklin:3`, `…lib-eb-garamond-cabin:3`, `…lib-bitter-montserrat:3`, `…lib-spectral-source-sans-3:3`, `…lib-vollkorn-montserrat:3`, `…lib-archivo-narrow-merriweather:3` (7 rows) | Evidence Class | `ranked` (Rank Value blank) | `authority` (Ranking Metric text may stay; Rank Value stays blank) | test_provenance rule 3; base precedent `designs:cv-dach-tabular:1` / `designs:cv-editorial:1` class Typewolf as `authority`; research/80 §2C "ranked rows need … value" |
| 2 | M | research/provenance/typefaces-ranked-pairings.csv | `:1` and `:2` rows of the 13 two-family pairings (`lib-noto-serif-noto-sans` … `lib-archivo-narrow-merriweather`) | whole row pair | two rows per pairing with identical (Table, Row Key, Source URL) | Collapse to ONE `ranked` row per pairing: Rank Value = heading family's rank; Ranking Metric = "Google Fonts popularity (metadata/fonts `popularity`), heading <X>=<n>; body <Y>=<m>". Renumber prov_keys. (Alternative needing an orchestrator ruling: relax test rule 6 for per-family ranks.) | test_provenance rule 6 (`TestNoDuplicateSourceCitations`); ranks as in A1 |
| 3 | M | research/library/typefaces/ranked-pairings.csv (+ its 3 provenance rows) | `lib-dm-serif-display-dm-sans` | row | DM Serif Display as Heading Family (1 static weight, no axis) | **Remove the row.** It fails the batch's pre-registered admissibility filter (b), and R-d rules out ad-hoc exceptions. If the orchestrator rules display heads exempt from (b), keep it and amend the filter text instead. | metadata/fonts: DM Serif Display `fonts` = {400, 400i}, `axes` = [] |
| 4 | M | research/library/typefaces/ranked-pairings-evidence.md | (prose, "Admissibility filter" + "Companion-family ranks" sections) | text | "DM Serif Display … kept only in an auxiliary role" | Delete the claim (with fix 3), or record the orchestrator exception | ranked-pairings.csv: Heading Family = DM Serif Display |
| 5 | S | research/library/typefaces/ranked-pairings-evidence.md | (prose under Top-60 table) | text | "rank 1 and rank 6 are not shown … list is otherwise contiguous" | "The `popularity` field is not dense: values 1, 6, 11, 12, 13, 15, 18 (and others) are absent from the public payload; ranks are reported as returned." | metadata/fonts sorted popularity |
| 6 | S | research/library/typefaces/ranked-pairings.csv | `lib-roboto` | Has Tabular Figures | `unknown` | `yes` | ofl/roboto/Roboto[wdth,wght].ttf: GSUB has `tnum` (and digits are fixed-width 1151) |
| 7 | S | same | `lib-lato` | Has Tabular Figures | `unknown` | `yes` | ofl/lato/Lato-Regular.ttf: GSUB `tnum` present |
| 8 | S | same | `lib-inter` | Has Tabular Figures | `unknown` | `yes` | ofl/inter/Inter[opsz,wght].ttf: GSUB `tnum` present |
| 9 | S | same | `lib-montserrat` | Has Tabular Figures | `unknown` | `yes` | ofl/montserrat/Montserrat[wght].ttf: GSUB `tnum` present |
| 10 | S | same | `lib-fira-sans-fira-mono` | Has Tabular Figures | `unknown` | `yes` | ofl/firasans/FiraSans-Regular.ttf: GSUB `tnum` present |
| 11 | S | research/provenance/typefaces-ranked-pairings.csv | `typefaces:lib-nunito-nunito-sans:3` | Source Name / Source URL / Ranking Metric | "Fonts In Use – Nunito Sans", fontsinuse.com/typefaces/85917/nunito-sans, "Publisher-documented companion (…)" | "Google Fonts – Nunito Sans DESCRIPTION", https://raw.githubusercontent.com/google/fonts/main/ofl/nunitosans/DESCRIPTION.en_us.html, "Publisher-documented companion ("Nunito is a well balanced sans serif typeface superfamily, with 2 versions … an accompanying regular non-rounded terminal version, Nunito Sans")" | fetched 2026-09-23, 200 |
| 12 | M | research/library/palettes/authority-design-systems.csv | `lib-material3-purple` | Primary, Foreground, On Muted, Rule Strong | `#1C1B1F` | `#1d1b20` (md.sys.color.on-surface = neutral10) | raw material-web `tokens/versions/v0_192/_md-sys-color.scss` L102 + `_md-ref-palette.scss` L45 |
| 13 | M | same | `lib-material3-purple` | Background | `#FFFBFE` | `#fef7ff` (md.sys.color.surface = neutral98) | same files, L120 + L66 |
| 14 | M | research/provenance/palettes-authority-design-systems.csv | `palettes:lib-material3-purple:1` | Source Name / Source URL / Fetch | m3.material.io/styles/color/roles, `search-corroborated` | "Material Web tokens v0_192: on-surface neutral10 #1d1b20, on-surface-variant n-v30 #49454f, surface neutral98 #fef7ff, surface-variant n-v90 #e7e0ec, outline-variant n-v80 #cac4d0, primary primary40 #6750a4"; URL https://raw.githubusercontent.com/material-components/material-web/main/tokens/versions/v0_192/_md-sys-color.scss; Fetch `fetched` | R-a (cite only a fetched copy). Recomputed after fixes 12–13: On Primary 17.07, Fg/Bg 16.23, On Muted 13.23, On Secondary 9.34, On Accent 6.44; Text-Safe unchanged (secondary 8.88, accent 6.12 vs #fef7ff) |
| 15 | M | research/library/palettes/authority-design-systems.csv | `lib-carbon-dark-slide` | Text-Safe Roles / Fill-Only Roles | `foreground;primary;secondary;accent` / `muted` | `foreground;primary;secondary` / `muted;accent` (Category Marker `accent` may stay, per base `brand-accent-print` precedent) | color.contrast_ratio(#0f62fe, #161616) = 3.62 < 4.5 |
| 16 | M | same | `lib-fluent-dark-slide` | Text-Safe Roles / Fill-Only Roles | `foreground;primary;secondary;accent` / `muted` | `foreground;primary;secondary` / `muted;accent` | color.contrast_ratio(#0078d4, #0a0a0a) = 4.37 < 4.5 |
| 17 | S | same | `lib-fluent-dark-slide` | Rule Hair | `#141414` (1.07:1 on bg) | `#3d3d3d` (Fluent grey '24'; 1.82:1, comparable to base deck-high-contrast 1.69) | fluentui colors.ts `'24': '#3d3d3d'` |
| 18 | S | research/library/palettes/authority-design-systems-evidence.md | `lib-material3-purple`, `lib-carbon-dark-slide`, `lib-fluent-dark-slide` sections | tables | no role-vs-Background line; stale M3 source | Update the M3 source line and ratios to fixes 12–14. Add "Accent / Background" rows (3.62, 4.37 → Fill-Only) to the two dark sections. | as above |
| 19 | A | research/library/palettes/authority-design-systems.csv | `lib-govuk-burgundy` | Keywords | contains `error` | drop `error` | BM25 hygiene: queries about error states would surface a brand palette |
| 20 | A | same | `lib-govuk-forest`, `lib-govuk-teal` | Keywords | contain `health` | drop, or keep only as a researcher tag (not in source) | GOV.UK colour page makes no health association |
| 21 | A | research/provenance/palettes-authority-design-systems.csv | `palettes:lib-radix-burgundy:1`, `palettes:lib-radix-sand:1` | Source URL | docs page (hexes only as unlabeled swatch styles) | add a `:2` row citing https://unpkg.com/@radix-ui/colors@3.0.0/index.js (carries `red12: "#641723"` etc.) | fetched 2026-09-23, 200 |
| 22 | A | research/library/palettes/authority-design-systems-evidence.md | `lib-atlassian-ink` | Muted token name | `background-code-gutter` | `background-accent-gray-subtlest` (same #F0F1F2, semantically a surface) | atlassian.design/DESIGN.md |
| 23 | A | research/library/typefaces/ranked-pairings.csv | `lib-inter`, `lib-lato`, `lib-poppins`, `lib-nunito-nunito-sans` | Safe Stack Fallback / Body Fallback / Availability | `Calibri` / `Calibri` / `office-bundled` | consider `Arial` / `Arial` / `os-bundled` (base convention; avoids the validate-font-resolution warning) | research/09 T5 notes on office-bundled vs os-bundled |
| 24 | A | research/library/typefaces/ranked-pairings.csv | all `typewolf-pairing`, `publisher-companion`, `google-companion`, `mozilla-superfamily`, `single-family`, `sans-sans` tokens | Keywords | provenance/schema meta tokens | replace with tone/industry/use terms | §2B "Keywords (theme/industry/tone)" |
| 25 | A | research/provenance/typefaces-ranked-pairings.csv | `typefaces:lib-noto-serif-noto-sans:3` | Source | Wikipedia sentence about glyph coverage, not pairing | acceptable; stronger: google/fonts `ofl/notoserif` DESCRIPTION if it names the companion | — |

After fixes 1–4 and 12–16, expected state: `test_provenance.py` green on the typeface rows
(re-run after the orchestrator regenerates base per R-g), 19 typeface rows (or 20 with a
ruling), and 256/256 palette hex cells traced to a fetched token file.

## Fixes applied (2026-09-23)

Orchestrator rulings applied as directed:

- **Item 1 (APPLY):** Reclassified the 7 Typewolf pairing-source provenance rows
  (`lib-alegreya-alegreya-sans:3`, `lib-libre-baskerville-libre-franklin:3`,
  `lib-eb-garamond-cabin:3`, `lib-bitter-montserrat:3`, `lib-spectral-source-sans-3:3`,
  `lib-vollkorn-montserrat:3`, `lib-archivo-narrow-merriweather:3`) from `ranked` to
  `authority` in `research/provenance/typefaces-ranked-pairings.csv`. Rank Value stays
  blank; Ranking Metric prose kept as-is.
- **Item 2 (APPLY, alternative ruling):** Rows NOT merged. Instead
  `test_provenance.py`'s `TestNoDuplicateSourceCitations` now keys on (`Table`,
  `Row Key`, `Source URL`, `Ranking Metric`), with docstring/comment explaining that one
  popularity citation per family of a pairing is legitimate. Verified all 13 pairing rows
  already carry distinct, family-naming Ranking Metric text — no CSV text changes were
  needed for this item.
- **Item 3 (KEEP, orchestrator exemption):** `lib-dm-serif-display-dm-sans` kept. Display
  heading faces are now recorded as exempt from the ≥4-weight admissibility filter in
  `research/library/typefaces/ranked-pairings-evidence.md`.
- **Item 4 (APPLY):** Removed the false "kept only in an auxiliary role" claim about DM
  Serif Display from the evidence file; replaced with an accurate statement distinguishing
  it (Heading Family, exempted) from Fira Mono (genuinely auxiliary).
- **Item 5 (APPLY):** Corrected the "contiguous" prose claim in the evidence file to state
  the `popularity` field is not dense and list the observed gaps.
- **Items 6–10 (APPLY):** `Has Tabular Figures` set to `yes` for lib-roboto, lib-lato,
  lib-inter, lib-montserrat, lib-fira-sans-fira-mono in `ranked-pairings.csv`.
- **Item 11 (APPLY):** Nunito Sans companion citation re-sourced from Fonts In Use to the
  Google Fonts `ofl/nunitosans/DESCRIPTION.en_us.html` publisher description.
- **Items 12–14 (APPLY, re-fetched):** Re-fetched
  `raw.githubusercontent.com/material-components/material-web/main/tokens/versions/v0_192/_md-sys-color.scss`
  and `_md-ref-palette.scss` directly; confirmed on-surface (neutral10) = `#1d1b20` and
  surface (neutral98) = `#fef7ff`. Updated `lib-material3-purple`'s Primary/Foreground/On
  Muted/Rule Strong to `#1d1b20` and Background to `#fef7ff` in
  `authority-design-systems.csv`; reclassified its provenance row from
  `search-corroborated`/m3.material.io to `fetched`/the Material Web token file.
- **Items 15–16 (APPLY):** `lib-carbon-dark-slide` and `lib-fluent-dark-slide` now list
  `accent` under Fill-Only Roles (not Text-Safe Roles); Category Marker Roles unchanged
  (`accent`, per `brand-accent-print` precedent).
- **Item 17 (APPLY):** `lib-fluent-dark-slide` Rule Hair changed from `#141414` (1.07:1,
  invisible) to Fluent grey24 `#3d3d3d` (1.82:1); verified against the live fluentui
  `colors.ts` file.
- **Item 18 (APPLY):** Updated `authority-design-systems-evidence.md`: new M3 source line
  and recomputed ratios; added Accent/Background rows (3.62, 4.37 → Fill-Only) and a
  Rule Hair/Background row for the two dark-slide sections.
- **Items 19–20 (APPLY):** Dropped `error` from `lib-govuk-burgundy` Keywords; dropped
  `health` from `lib-govuk-forest` and `lib-govuk-teal` Keywords.
- **Item 21 (APPLY):** Added `:2` provenance rows for `lib-radix-burgundy` and
  `lib-radix-sand` citing `https://unpkg.com/@radix-ui/colors@3.0.0/index.js`; re-fetched
  and confirmed every cited hex (red/sand/bronze scales) matches exactly.
- **Item 22 (APPLY):** Corrected the Atlassian muted token name in the evidence file from
  `background-code-gutter` to `background-accent-gray-subtlest` (same hex `#F0F1F2`).
- **Item 23 (APPLY):** `lib-inter`, `lib-lato`, `lib-poppins`, `lib-nunito-nunito-sans` now
  use Arial/Arial/`os-bundled` instead of Calibri/Calibri/`office-bundled`.
- **Item 24 (APPLY):** Replaced the six schema/provenance-meta Keyword tokens
  (`typewolf-pairing`, `publisher-companion`, `google-companion`, `mozilla-superfamily`,
  `single-family`, `sans-sans`) across all affected rows with tone/industry/use terms
  drawn from each row's own "Best For" text.
- **Item 25 (SKIP):** Not trivial enough to justify re-sourcing under the time available;
  current Wikipedia citation stands as "acceptable" per the audit's own note.

Verification: `python3 research/load-base.py` (149 provenance rows, no structural
problems); `skill/document-design-intelligence`: `python3 scripts/ddi.py check` →
`OK: validated 16 table(s), 747 row(s)`; `python3 -m pytest -q` → the run collects
`scripts/tests/test_make_brand_kit.py` with a pre-existing `SyntaxError` (unterminated
string literal at line 429, from a concurrent edit unrelated to this batch — this file was
never touched here); excluding that file, `python3 -m pytest -q --ignore=scripts/tests/test_make_brand_kit.py`
→ `223 passed, 1 skipped, 1 xfailed, 935 subtests passed`. `test_provenance.py` and
`test_designs.py` alone: `16 passed, 1 xfailed, 760 subtests passed` (the 1 xfail is the
pre-registered intentional one).
