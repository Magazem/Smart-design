# proposal -- F.c filling (research/82 sections 6, 8, 9)

Gate: `proposal-agreement.md` -- identity features and admissibility all A_f >= 0.80 (heading 0.80);
variant features `rules_boxes` (0.60) and `density` (0.30) FAILED and are dropped from filling (family
default used); `cover_page` had n=0 shared coded sample, so it is not usable either. `body` passed (1.00).

Inputs: research/82 sections 6/8/9, `proposal-corpus-github.md` (the only ranked corpus; N=40, L1 valid),
`proposal-agreement.md`, `research/designs/proposal.csv` + `research/provenance/seed-designs.csv`
(the one seeded design), the base library as of task start (`typefaces.csv` 34, `palettes.csv` 44,
`doc-styles.csv` 16 + cv fill rows, `doc-reasoning.csv` 20 + cv fill rows), and the generated
`proposal-fill-log.md` (engine ranking beside the decided fill). Generator: `fill_family.py --family
proposal` from `fill-specs/proposal.json`.

`proposal-corpus-ms.md` (7 Word proposals, plus 2 LibreOffice) is corroboration only (7 < 10, not
poolable, section 2) and contributes no share. `proposal-recode-82ag.md` recodes those 7 MS items, not the
GitHub corpus, so no recode applies (`recodes: []`).

## 1. Rank (section 6)

Step 1 (ranked, K>=2, >= 1 admissible exemplar, combined share desc): exactly 5 archetypes qualify;
none tie, so no tie-break was needed. Shares are k/40 over GH only (one corpus, mean = share).

| rank | archetype | k | share | design |
|---|---|---|---|---|
| 1 | `1\|serif\|mono\|plain-centered` | 17 | 0.425 | proposal-serif-centered |
| 2 | `1\|sans\|mono\|plain-centered` | 10 (9 adm) | 0.250 | proposal-sans-centered |
| 3 | `1\|sans\|mono\|plain-left` | 5 | 0.125 | proposal-sans-plain-left |
| 4 | `1\|serif\|mono\|ruled` | 3 | 0.075 | proposal-serif-ruled |
| 5 | `1\|sans\|one-accent\|plain-centered` | 2 | 0.050 | proposal-sans-accent-centered |

Step 2 (L3): none. The family has no fetched authority document (no named award or standard for a
proposal layout in research/82 section 10).
Step 3 (singletons): not used -- steps 1-2 already give 5 = the floor (singletons are allowed only when
they give < 5). The 3 admissible singletons (`1|display|mono|plain-centered` GH:092,
`1|sans|fill-blocks|plain-left` GH:068, `1|serif|mono|plain-left` GH:105) are therefore not shipped.
Step 4 (L4 convention, max 1): the seeded doctype default, below.

Cap: 10 - n_L3 (0) - n_L4 (1) = 9 for step 1; only 5 archetypes exist, so the cap does not bite.

**Shortfall.** The family ships 5 non-convention designs plus 1 convention = 6, below the 8-10 target
and at the floor of 5. Cause: one coded corpus of 40 items in which 8 archetypes appear at all, 5 of
them with k >= 2 (the coarsening trigger -- >= 15 admissible items, > 50% singletons, < 5 archetypes
with k >= 2 -- did not fire: 3 of 39 admissible items are singletons). No second corpus could be
coded: Microsoft Create has 7 proposal documents and LibreOffice 2 (< 10 pooled, section 2).

## 2. Seed disposition (section 9)

The one seed is `proposal-narrative` (a doctype default: the doctype `proposal` and every proposal
brand doctype point at its reasoning row). Coded from its own spec (section 4):
columns 1 (`a4-report-standard`, Columns 1), heading serif (Times New Roman), colour one-accent
(`print-neutral`: Accent #2E5C82 is the only chromatic hex, HSL S 0.48, L 0.35), header plain-left
(`report-classic-serif` Rule Brand pt 0, no rule) -> `1|serif|one-accent|plain-left`. That archetype is
not in the corpus at all (k = 0), so it matches no step-1 archetype and merges nowhere. Per section 9
"an unmatched seed that is a doctype default stays, placed by its own evidence": its rationale cites no
fetched authority, so it stays `convention`, exempt from the L4 cap, and ranks last (6). Its
doc-reasoning row already exists in the base library and is not re-emitted. Its seed provenance row
(`designs:proposal-narrative:1`) moved from `seed-designs.csv` into `provenance/proposal.csv` (duplicate
keys fail the gate). Best For was extended to say what its convention covers: commercial and
consultancy proposals outside the corpus skew. Rank 1 is not the default and the default is not
demoted below its evidence (it has none).

## 3. Section 8 fill -- decisions per rule

Variant features used: `body` only (gate passed). `rules_boxes`, `density`, `cover` -> the family
default (the seed's own style, `report-classic-serif`).

### Style
Mapping (section 8): Table Rules -- the proposal family maps `rules` to `header-and-total`; because
`rules_boxes` is dropped the family default's Table Rules (`header-and-total`) applies to every archetype.
Table Fills `none`. Emphasis: colour mono/one-accent -> `weight`. Header `ruled` -> Rule Brand pt 1,
otherwise 0. Field Style `none`. Checklist lines from columns (`Keep single column`, all five archetypes
are 1-column). Photo/panel/totals/letterhead features do not apply to proposals.

Reuse test (Table Rules, Fills, Emphasis, Field Style, Rule Brand>0 all equal; no contradicting line):
`report-classic-serif` is the only existing row with `header-and-total / none / weight / none / 0`
(`form-grid-underline` has Field Style `underline`).

- Rank 3 (`1|sans|mono|plain-left`): **reuse `report-classic-serif`** (rule applied as written).
- Ranks 1, 2, 5 (`plain-centered`) and rank 4 (`ruled`): **DEVIATION from strict reuse, new rows.**
  Reason: header placement (centred title block, ruled title block) is a coded IDENTITY feature and the
  only place the library can carry it is a Checklist line (the cv fill did the same:
  "Centre the name..."). `report-classic-serif` (shared with the report family) has no placement line, so
  strict reuse would silently drop the coded feature and make ranks 1, 2 and 5 resolve to the same style
  as the plain-left default. New rows: `proposal-plain-centered` (centre the title block; Rule Brand 0)
  and `proposal-ruled` (full-width rule under the title block; Rule Brand 1pt; header `ruled`). Rule
  Hair 0.5 / Strong 1 / Corner 0 are copied from `report-classic-serif`; the headings/tables checklist
  lines are the default's, minus "serif body throughout" (body class is a typeface matter, and ranks 2/3/5
  have a sans heading).

### Typeface
Rule: if the modal declared font is OS/Office-bundled use the `safe-*` row, else candidates = rows
matching heading class and modal body class, lowest Google Fonts popularity of the Heading Family, then
licence, category contrast, key; the row's Scale Key must have the family's medium (print).
Declared fonts are not coded per item in the proposal table (LaTeX templates: Computer Modern / Times /
Palatino mostly), so the safe-stack branch cannot be evaluated and the candidate branch is used.

Modal body class per archetype (admissible exemplars): rank 1 serif 17/17; rank 2 serif 6 / sans 4
(serif); rank 3 serif 4 / sans 1 (serif); rank 4 serif 3/3; rank 5 serif 2/2.

- Ranks 1 and 4 (serif heading + serif body): candidates `safe-serif-georgia`, `safe-serif-times`
  (the library's only serif+serif rows). `safe-serif-georgia`'s Scale Key is `report-screen`
  (medium `screen`), not `print`, so it is rejected by the medium rule; **`safe-serif-times`**
  (`report-print`, print). (Alphabetical tie-break would have chosen Georgia; the medium rule comes first.)
- Ranks 2, 3, 5 (sans heading + serif body): **no library row has a sans heading with a serif body**
  (Category Contrast values are serif-sans, sans-sans, serif-serif, superfamily). Strict rule: log a
  gap and use the family default's typeface (`safe-serif-times`). **DEVIATION:** relax the VARIANT
  (body) and keep the IDENTITY feature (heading): section 4 says variant features never split
  archetypes, and a serif-headed default would make ranks 1 and 2 resolve identically. Candidates =
  sans-heading rows, lowest Google popularity of the Heading Family: Roboto (2), Open Sans (3), Inter (5).
  `lib-roboto` (Scale Key `print-office-generic`, medium print). `lib-inter`'s scale is screen, not
  reached anyway. Result `lib-roboto` (sans/sans, installable) for ranks 2, 3, 5; disclosed here and in
  each design's resolved values (`ddi.py designs` prints them).

### Palette
Class from hexes (section 4 thresholds: chromatic = S >= 0.20, 0.12 <= L <= 0.90, hues >= 30 degrees
apart over Primary, Secondary, Accent, Rule Brand); order: provenance class authority > ranked >
convention -> hue bin (one-accent) -> Foreground/Background and accent >= 4.5:1 -> not an A7 blue ->
key alphabetical. No hex is invented.

- Mono archetypes (ranks 1-4): mono palettes: `cv-dach-formal`, `lib-carbon-mono`, `lib-radix-sand`
  (authority), `lib-cl-r33-neutral` (ranked), `mono-ink` (convention). Strictly the first authority
  key alphabetically is `cv-dach-formal`. **Interpretation applied:** "authority" ordered by evidence
  strength -- `Fetch=fetched` authority before `search-corroborated` authority. `cv-dach-formal`'s
  authority row is a legacy backfill marked `search-corroborated` (source: GOV.UK colour page, not
  fetched); `lib-carbon-mono` and `lib-radix-sand` are `fetched` (IBM Carbon tokens; Radix). Among the
  fetched authority mono palettes the alphabetical first is **`lib-carbon-mono`**, the same palette the cv
  fill used for its mono archetypes (the cv fill got the same answer because the backfill did not exist
  yet). Deviation from the literal reading is limited to this fetched-before-search-corroborated
  ordering; all candidates are listed here.
- One-accent archetype (rank 5): candidates one-accent palettes with Foreground/Background >= 4.5
  and accent >= 4.5 (fetched authority first): `lib-atlassian-ink` (accent #1868DB, 5.2:1, hue 215),
  `lib-carbon-forest`, `lib-carbon-purple`, `lib-carbon-teal`, `lib-fluent-*`, `lib-govuk-*`... The
  hue-bin tie-break needs per-item hex swatches; none are coded (categorical enums only), so it is
  inapplicable as in the cv fill. PR.7 mentions the NSFC blue #006FC0 (hue ~206, bin 4: 180-225) for
  GH:015/084; that is a coder note, but it agrees: `lib-atlassian-ink` (hue 215, bin 4) is also the
  first fetched-authority candidate in bin 4 (`cv-editorial`, `cv-europass`, `cv-harvard` are
  search-corroborated; `lib-carbon-dark-slide` and `lib-fluent-dark-slide` fail 4.5:1 on accent).
  Not an A7 blue (#1868DB is not #4472C4/#4F81BD/#156082/#0563C1). -> **`lib-atlassian-ink`**.

### Reasoning rows (section 8 last paragraph)
`<family>-<archetype>` keys equal the design keys. Style/Palette/Typeface keys as above. Bias terms and
severity (`warn`) are copied from the family default row (`proposal-narrative`); Doc Conditions blank
as there. Anti-Pattern Tokens = the default's (`multi-column;gradient;stock-photo-cliche;emoji`): all five
archetypes are single-column, so none legitimately uses `multi-column`. Note: the copied Typeface Bias
Terms ("safe serif stack") describe the default's typeface, not `lib-roboto`, exactly as section 8
prescribes (cv fill precedent).

## 4. Disclosures

- **Skew.** The corpus is GitHub `proposal template latex` (total_count 196): thesis-proposal, national
  funding (NSFC, DFG, ERC) and application-form templates dominate; commercial proposals are almost
  absent. Every ranked design's Best For / Not For says so; the convention default is the only
  non-academic entry and is labelled convention.
- **Forms.** GH:073, 088, 092, 099, 104 are proposal application forms (form-like), GH:104 excluded (A8).
- **C13 cover page.** `cover` = yes for 24 of 39 admissible items (no for 15). It is a variant feature
  whose second-coder sample was empty (n=0), so it is not fitted; each Best For states the count. Header,
  heading and colour were coded from the cover, columns/body from the first running-text page (C13).
- **Forms/one-page.** One-page proposals (MSP:003, MSP:007) are cross-listed to one-pager, not counted.
- **Duplicated resolved fills.** None: the six designs resolve to six distinct (style, palette,
  typeface) triples.

## 5. Engine notes (for the reviewer and for the next fill)

`fill_family.py`'s `--dry-run` printed style proposals that use `rules/boxes` modal values (`none` ->
Table Rules `none`); it does not yet honour a gate-dropped variant. This fill follows the rules (dropped
variant -> family default) and shows the difference in `proposal-fill-log.md`. The engine's palette
proposal is not implemented (`palette_class` exists but is not wired); palette picks above were made by
the analysis in section 3. Finding for the cv fill: `safe-serif-georgia`'s Scale Key is
`report-screen` (screen), which the section 8 medium rule would have rejected for a print CV, yet three cv
reasoning rows use it (`cv-serif-plain-centered`, `cv-serif-mono-split`, `cv-serif-accent-plain-left`).

## Re-run 2026-09-25 under R7 (research/82a-r7-rulings.md)

Regenerated with the fixed engine from `fill-specs/proposal.json` (0 overrides; the spec keeps only the
authored wording and the one new style row `proposal-ruled`). Generated log: `proposal-fill-log.md`.

Ranks and classes are unchanged (5 ranked designs plus the convention default `proposal-narrative`,
6 total, inside the cap). Corpus GH has 1 inadmissible item in `1|sans|mono|plain-centered`; it is no
longer counted there (k 10 -> 9), so the provenance row of `proposal-sans-centered` changes from
`0.250 (10/40)` to `0.225 (9/40)` (rank 2 either way).

| row | field | old | new |
|---|---|---|---|
| proposal-serif-centered, proposal-sans-centered, proposal-sans-accent-centered | Style Key | proposal-plain-centered (new row) | report-classic-serif (existing row; family default; the engine's reuse rule R7-5 matches it, so the new row is no longer authored and is dropped) |
| proposal-sans-* rows (3) | Typeface Bias Terms | "safe serif stack" | blank (R7-8: heading is sans / typeface is not a safe row) |
| all | Palette Key, Typeface Key | unchanged | unchanged (carbon-mono / atlassian-ink; safe-serif-times / lib-roboto via the draft pairing fallback) |

The pairing fallback (sans heading with a serif body -> keep the heading class) still comes from the
unratified draft 82a-clarifications-6 R2; the log labels it "draft rule R2, unratified". No spec cites it.
