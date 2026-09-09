# Notes — 40: long-form-class section model (v0.2 phase A2)

## Column shape correction
research/40-headings-longform-draft.csv uses research/18-ats-headings.csv's five lowercase
columns (canonical_section, heading_text, language, is_primary, source), NOT the
data/base/headings.csv five. research/load-base.py generates `heading_key` itself as
`<section>-<lang>-<n>` and writes the `source` column out to
data/rationale/headings.md — it is not dropped, it feeds the rationale file. Every row
here carries a `source` citation (all `convention (...)`, matching the style in
research/18 — no row from this file traces to "report 03", which is CV/ATS-specific).
research/40-t10-section-orders-longform.csv is unchanged (structure_key, Section Order —
already the manifest shape, per the brief).

## Scope
report-short, report-long-toc, whitepaper-standard, one-pager-standard — bound from
skill/document-design-intelligence/data/base/structures.csv. No doctype mapping needed;
these are the structure_keys directly.

## 12 new canonical sections
table-of-contents, introduction, methodology, findings, conclusion, recommendations,
appendices, bibliography, solution-approach, headline, key-points, call-to-action
(36 rows: 12 sections × en/fr/de, one row each, Is Primary=yes on all — single row per
language per rule carried from A1).

## Reused sections (4)
- From research/39 (transactional draft): `cover`, `executive-summary`, `problem-statement`.
- From data/base/headings.csv (CV set): `contact` (one-pager-standard only).

## Reuse rule applied — two rejections, with the DE/FR primary as the test
- **`references` (CV canonical_section) — rejected**, same shape as A1's `summary` rejection.
  Its DE primary `Referenzen` reads as the CV/testimonial sense (people who vouch for you),
  not a source list. A German report's bibliography heading is `Literaturverzeichnis`, not
  `Referenzen` — those are different words for different things, not a translation of the
  same concept. Created `bibliography` instead (en References / fr Bibliographie /
  de Literaturverzeichnis) for report-long-toc, report-short, whitepaper-standard.
- **`proposed-solution` (from research/39, built for proposal-standard) — rejected for
  whitepaper-standard.** Its DE primary `Lösungsvorschlag` ("solution proposal") carries
  commercial bid/tender flavor from its proposal origin; a whitepaper argues a position, it
  doesn't pitch a deliverable. Created `solution-approach` instead (en Solution Approach /
  fr Approche proposée / de Lösungsansatz — "approach", not "proposal").
- `cover`, `executive-summary`, `problem-statement`, `contact` all passed the check: their
  FR/DE primaries are generic in both source and target context, no other-class reading.

## Why report-short and report-long-toc differ (grounded in structures.csv, not taste)
- report-long-toc: Front Matter Numbering=roman, TOC Depth=2, Heading Depth Max=3 →
  keeps `cover` and `table-of-contents` (the table's own fields call for both), plus
  `methodology` and `appendices`, which need the extra depth level (3) report-short doesn't
  have — a standalone methodology section and nested appendix material both want depth-3
  headings, not depth-2.
- report-short: Front Matter Numbering=none, TOC Depth=0, Heading Depth Max=2 → drops
  `cover`/`table-of-contents` (no front matter numbering or TOC to anchor them) and drops
  `methodology`/`appendices` (both want depth 3). Kept `bibliography`: a short report can
  still cite sources at depth 1, dropping it would be a scope cut with no support in the
  structures.csv fields, unlike the other four.
- whitepaper-standard sits in between: argues a position (`problem-statement` →
  `solution-approach`) rather than reporting neutral method+findings, so it also skips
  `recommendations` and `appendices` — a whitepaper's evidence lives in `findings`, not a
  separate recommendations section, which is a report-genre convention.

## Sourced vs. conventional
- **Sourced**: DIN 5008-adjacent German report vocabulary (`Einleitung`, `Zusammenfassung`
  already sourced in A1, `Literaturverzeichnis` for bibliography — standard German academic/
  business report term, distinct from `Referenzen`); French report vocabulary
  (`Table des matières`, `Bibliographie`, `Méthodologie`) — standard francophone report
  headings, not invented.
- **Conventional / my own choice**: the report-long-toc ten-section skeleton (cover → toc →
  executive-summary → introduction → methodology → findings → conclusion →
  recommendations → appendices → bibliography) is a common long-report shape but not the
  only valid one. The whitepaper's argumentative order (problem-statement →
  solution-approach → findings → conclusion) is likewise a common but not standardized
  whitepaper pattern. The one-pager's four-section order (headline → key-points →
  call-to-action → contact) has no external standard — one-pagers vary by purpose; this is
  a reasonable generic marketing/business one-pager shape, not a cited convention.
  `headline`/`key-points`/`call-to-action` German and French terms (`Kernbotschaft`,
  `Kernpunkte`, `Handlungsaufruf`, `Accroche`, `Points clés`, `Appel à l'action`) are
  standard marketing-collateral vocabulary in each language, not invented, even though the
  four-section skeleton they sit in is my own construction.

## Verification (research/40-verify.py, run via the given python3.exe)
All five checks pass — see full stdout in the orchestrator report. Check 2/3 generate
t40's heading_key exactly the way load-base.py will (`<section>-<lang>-<n>`) before
comparing, since the draft file itself no longer carries that column. Union check (base +
research/39 + generated t40 keys) also passes for the one-primary-per-(section,language)
rule, so no pre-existing irregularity in data/base/headings.csv needed to be worked around.
Check 5 confirms no row was left with a blank `source` (which the loader would otherwise
file under "(none given)" in data/rationale/headings.md).
