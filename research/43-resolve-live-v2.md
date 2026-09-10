# 43 -- resolve.py against live data/base, v2 (Mechanism Analyst, re-run after section model load)

## Gate

```
$ python3 scripts/validate_data.py data/base
OK: validated 14 table(s), 414 row(s)
```

Zero problems (was 31 in `35-resolve-live.md`, 82 before that). `structures.csv` now
exists with a Section Order on all 17 rows (commit aec56f4); no more FK-walk poisoning.

## Per-query results

| # | Query | Entry resolved to | Expected | Verdict | What changed since 35 |
|---|---|---|---|---|---|
| E1 | "build me an academic CV with my publications list" | `cv-academic` | `cv-academic` | **PASS** -- full RESOLVED payload | Was REFUSED PATH (missing structures.csv); now resolves end-to-end |
| E2 | "I need a leave-behind version of this deck for the client" | `slide-deck-handout` | `slide-deck-handout` | **PASS** -- full RESOLVED payload | Was REFUSED PATH; now resolves end-to-end |
| E3 | "make me a flyer" | ABSTAIN (candidates: `brochure-flyer-letter`=4.4916, `brochure-flyer-a4`=4.1957, `brochure-trifold-letter`=2.1005) | ambiguous -> abstain | **PASS (was FAIL)** | Previously resolved confidently to `cv-generic` on accidental keyword overlap ("make me a resume" in its Keywords cell). Now abstains and offers real flyer candidates -- `cv-generic` no longer even in top 3 |
| E4 | "draft an invoice for this order" | `invoice-tabular` | `invoice-tabular` | **PASS** -- full RESOLVED payload | Was REFUSED PATH; now resolves end-to-end |
| F1 no-brand | "fais-moi une note interne sur les congés" | `memo-internal` | `memo-internal` | **PASS** -- full RESOLVED payload | Was REFUSED PATH; now resolves end-to-end |
| F1 `--brand ens` | same | `ens-note-interne` | **still untestable** | `[NO BRAND ROW] brand=ens resolved only generic rows -- refusing to emit`, rc=3. `data/brand/` still has only a README, no `ens` overlay -- unchanged from 35 |
| F2 | "rédige un devis pour ce client" | `quote-devis` | `quote-devis` | **PASS** -- full RESOLVED payload | Was REFUSED PATH; now resolves end-to-end |
| F3 | "fais-moi un cv" | ABSTAIN (candidates: `cv-uk`=2.4771, `cv-gulf-gcc`=2.465, `cv-france`=2.4637) | `cv-generic` ("ideal") or abstain | **PASS** -- abstain is inside 35's recorded expectation | 35 recorded `cv-generic` winning by ~0.09 margin over `cv-france`; that margin is gone -- `cv-generic` isn't even a top-3 candidate now, and the three regional CVs are within 0.013 of each other. Mechanism changed, outcome still within spec |
| F4 | "rédige un rapport avec table des matières" | `report-long-toc` | `report-long-toc` | **PASS** -- full RESOLVED payload | Was REFUSED PATH; now resolves end-to-end |
| D1 | "erstelle einen tabellarischen lebenslauf" | `cv-dach` | `cv-dach` | **PASS** -- full RESOLVED payload | Was REFUSED PATH; now resolves end-to-end |
| D2 | "ich brauche ein anschreiben für diese bewerbung" | `cover-letter` | `cover-letter` | **PASS** -- full RESOLVED payload | Was REFUSED PATH; now resolves end-to-end |
| D3 | "erstelle eine präsentation" | `slide-deck-projection` | ambiguous -> abstain | **still FAIL** -- resolves confidently (score=2.5287, method=bm25), same class as E3 was | Correct entry either way, and now reaches a full RESOLVED payload instead of REFUSED PATH, but it still does not abstain on a one-word doctype-class query. Not investigated further -- out of scope per brief |
| D4 | "erstelle einen europass lebenslauf" | `cv-eu-europass` | `cv-eu-europass` | **PASS** -- full RESOLVED payload | Was REFUSED PATH; now resolves end-to-end |

## Tally

- **10 of 12** now produce a full RESOLVED payload end to end (E1, E2, E4, F1 no-brand,
  F2, F4, D1, D2, D3, D4 -- includes D3, which resolves but should abstain, see below)
  -- the REFUSED PATH wall from 35 is gone, as expected once `structures.csv` landed.
- **E3** ("make me a flyer") no longer resolves confidently: it now abstains and lists
  the real flyer candidates. This is a genuine improvement over 35's FAIL, not something
  this task touched -- consistent with the keyword-balance/no-stopword-filtering work
  landed separately (81bfaeb).
- **D3** ("erstelle eine präsentation") still resolves confidently instead of abstaining
  -- unchanged FAIL class from 35. Per brief: not fixing, reporting only. The fix
  (length normalisation) needs real query data and is backlog.
- **F1's brand pass is still untestable** -- `data/brand/` has no `ens` overlay, only a
  README. Reporting this rather than inventing a verdict, as instructed.
- **F3** ("fais-moi un cv") stays a PASS -- 35 recorded abstain as an accepted outcome
  alongside `cv-generic` -- but the mechanism behind it changed: `cv-generic` dropped
  out of the top 3 entirely (was winning by ~0.09 margin in 35), replaced by three
  regional CVs bunched within 0.013 of each other. Observed, not investigated -- out of
  scope for this brief, which named only E3/D3 as backlog items.

## Section Order guidance message -- live verification

Unlike `35` (which had to fake a `/tmp` fixture because `structures.csv` didn't exist),
every one of the 12 queries above that reached a structures row now shows a populated
`Section Order` in its RESOLVED output (e.g. E1's `structures/cv-academic` ->
`Section Order: contact;summary;education;publications;...`). No row in `data/base`
carries an empty Section Order any more, so the guidance-message path itself cannot be
exercised live -- confirmed by `python3 scripts/validate_data.py data/base` and by a
`csv.DictReader` pass over all 17 `structures.csv` rows and all 14 `cv-regions.csv`
rows, neither of which has a blank Section Order cell. The path is still covered by the
two new synthetic-row unit tests in `test_resolve.py` (see report to orchestrator).
