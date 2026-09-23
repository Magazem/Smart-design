# research/80 — v0.5 "Design Library" plan (frozen 2026-09-23)

Authored by an Opus planner, ruled on by the orchestrator. The orchestrator's rulings are in §R
and OVERRIDE the planner text where they conflict.

## §R Orchestrator rulings (binding)
- R-a **Butterick is NOT banned.** RESUME's line "Butterick and DIN 5008 are cited NOWHERE" was a
  factual observation (2026-09-10) that stopped a ruling from borrowing an unverified authority
  for page-flow rows. Phase A (research/69, /70) FETCHED practicaltypography.com/resumes.html and
  cited it for what it actually says. That is exactly the discipline. Planner task P0.1 is
  CANCELLED. The rule that stands: cite a source only for what a fetched copy says. The same applies
  to DIN 5008 (paywalled; cite only a fetched secondary that quotes it, else CONVENTION).
- R-b A "design" = a `doc-reasoning` row, catalogued by a new `designs` table (§2B). Accepted.
- R-c Provenance lives in a new `provenance` table (§2C). Accepted.
- R-d Researchers COUNT, they do not judge. Rank = frequency in a pre-registered ranked corpus,
  filtered by pre-registered admissibility rules (§3). Accepted.
- R-e Portability via a generated `portable/` pack (§5). Accepted.
- R-f Blind judge panels must be independently spawned judges, never self-judged (research/75).
- R-g Workers never run git and never run load-base.py/build-manifest.py unless the brief says so;
  the orchestrator regenerates and commits.

## §0 Facts found
- A design already exists implicitly: doctypes.Reasoning Key -> doc-reasoning (Style, Palette,
  Typeface keys + anti-patterns); typefaces.Scale Key picks the scale. 19 doc-reasoning rows,
  1-4 per family, 6 CV. cv-editorial is bound to no doctype (unselectable).
- Library: 15 doc-styles, 8 palettes, 13 typefaces, 10 scale keys (32 rows).
- Sources live only in rationale/*.md prose — not queryable, no rank metric.
- make_brand_kit.py DOCTYPE_CATALOG knows only 4 ENS doctypes (note-interne, formulaire, social,
  slides); emits no doc-reasoning row.
- No repo-root README.md although SKILL.md sends users to it.
- CI (release.yml) does not run tests.
- Parity: test_column_parity.py requires every new displayed column to be emitted by all 4
  handoff paths or listed in HANDOFF_EXCLUSIONS (scripts/ddi.py).

## §2 Data model
A. `doctypes.Family` enum (16): cv, cover-letter, letter, memo, form, brochure, flyer, poster,
   report, whitepaper, proposal, quote, invoice, deck, one-pager, infographic. One constant in
   build-manifest.py shared with designs.Family. Filled in research/26. HANDOFF_EXCLUSIONS on all
   4 paths ("catalogue grouping, not a render value").
B. `designs` table (data/base/designs.csv, key design_key): design_key (family-prefixed),
   Display Name, Family (enum), Rank (int, contiguous 1..N per family), Reasoning Key (FK ->
   doc-reasoning.doc_category), Keywords (comma, distinct: theme/industry/tone), Best For,
   Not For, Evidence Class (ranked|juried|authority|convention), Brand Scope (generic).
C. `provenance` table (prov_key `<table>:<row_key>:<n>`): Table (enum), Row Key, Evidence Class,
   Source Name, Source URL (blank only for convention), Ranking Metric, Rank Value, Retrieved
   (ISO date), Fetch (fetched|search-corroborated). Polymorphic FK checked by
   tests/test_provenance.py: Row Key exists; every row of designs/palettes/typefaces/doc-styles/
   doc-reasoning has >=1 provenance row or exactly one convention row; ranked rows need URL,
   metric, value, date; numeric Rank Value only when Fetch=fetched. provenance is deliberately
   not FK-reachable (exclusion recorded here so backlog item 6 does not re-flag it).
D. CLI: `ddi.py designs --doctype <key> [--query "<theme>"] [--json]` lists the family's designs
   in Rank order, marks the doctype default, BM25 re-ranks by query (ties -> Rank), prints the
   evidence line. `ddi.py resolve ... --design <key>` overrides Reasoning Key then normal FK walk;
   refuses (exit 4) on family mismatch. Handoff gains `design: <Name> (rank r of N, <class>)` on
   all 4 paths. Default without --design = doctype default (fitness, e.g. ATS). Agent offers top 3
   by Rank when the user states a style preference. `ddi.py library <palettes|typefaces|
   type-scales|doc-styles> [--query] [--json]` browses the grand library with provenance.
E. Loader: load-base.py gains glob inputs, workers only ADD files:
   research/library/{palettes,typefaces,type-scales,doc-styles,doc-reasoning}/*.csv,
   research/designs/<family>.csv, research/provenance/<batch>.csv. Duplicate keys fail the gate.

## §3 Sourcing (ranked, not judged)
Evidence classes in preference order: ranked (public usage/popularity metric) > juried (named
award + year) > authority (standard / published design system) > convention (tagged, never
cited; counts toward the family target only if <5 non-convention designs; always ranked last).
Sources by artefact (probe fetchability first, research/81):
- Typefaces: Google Fonts popularity (metadata/analytics), jsDelivr/npm @fontsource download
  counts, Typewolf annual most-popular lists.
- Pairings: publisher-documented companions/superfamilies, Google Fonts Knowledge, Typewolf
  suggested pairings; both faces OFL or OS-bundled.
- Palettes: authority = design-system tokens (USWDS, GOV.UK, IBM Carbon, Material 3, Fluent,
  Atlassian); ranked = Coolors/Color Hunt popular like-counts, admissible only after a
  mechanical filter (darkest-on-lightest >= 4.5:1 via lib/color; <=1 saturated hue as text).
  Office default theme excluded (default-blue slop, research/68).
- Type scales: modularscale.com named ratios.
- Layout archetypes (design Rank per family): ranked = Microsoft Create popularity, Envato
  popular, Canva popular, Behance most-appreciated by tag, Google Docs template gallery; juried =
  ARC/Mercury (annual reports), Red Dot Communication, D&AD, European Design Awards, TDC;
  authority = Europass, NISO Z39.18, APA 7, GOV.UK/USWDS, ISO 216 — only where they cover the case.
- Template-marketplace BLOG POSTS are not authorities (zety/pagecloud precedent, research/70).
Family ranking procedure (frozen in research/82 before family work):
1. One primary ranked corpus per family, top 40 in native popularity order; record URL, sort, date.
2. Code each item on a fixed 6-feature rubric (columns, heading type class, colour use
   mono|one-accent|multi|fill-blocks, header treatment, rules/boxes, density) -> archetype.
3. Drop archetypes tripping research/68 slop patterns or the family's fail constraints; log.
4. Rank admissible archetypes by frequency (k/40).
5. Cross-check with one juried/authority source per family.
6. Second independent coder on a 25% sample; FALSIFIER: agreement < 80% -> revise rubric, re-code.
7. Fill each archetype with ranked library parts. No template artwork copied; features only.

## §4 Grand library + brand-kit builder
Targets: ~40 palettes (25 authority, 15 ranked-filtered), ~30 pairings (20 serif/sans, 6
superfamily, 4 display/editorial), ratio families (minor-third, major-third, perfect-fourth) x
print/projection/screen. Logo/lockup rules OUT (no structured source). Voice stays free text.
references/brand-kit-builder.md = interview -> palette (library query; brand accent swap; WCAG
AA via derive_palette_row) -> pairing (<=2 families, OFL if embedded, safe-stack fallback) ->
scale -> per-family design pick -> brand.md -> make_brand_kit.py --dry-run -> build.
Code: DOCTYPE_CATALOG accepts any generic base doctype; brand.md `## Designs` section
(`<family>: <design_key>`) emits `<slug>-<family>` doc-reasoning rows with brand palette/typeface.

## §5 Portability
Tier A (code-capable agents: Claude skill, ChatGPT Code Interpreter, Codex/Cursor): skill ZIP,
`python3 scripts/ddi.py`. Tier B (no code: Grok Projects, Gems, ChatGPT without CI): generated
pack. research/build-portable.py -> repo-root portable/: AGENTS.md (<8000 chars, platform-neutral
workflow + "never invent fonts/colours outside the pack"), DDI-LIBRARY.md (per family designs
in Rank order with fully resolved values + provenance line; then grand library; then
constraints + slop checklist), INSTALL.md (Claude.ai, ChatGPT GPT/Project, Grok Project, generic).
test_portable_sync.py asserts byte-equality (skips if research/ absent). CI publishes
ddi-portable-<ver>.zip as a second asset; portable/ stays out of the skill ZIP.

## §6 Work breakdown (S=Sonnet, O=Opus)
Phase 1 schema+mechanism (serial): P1.1 build-manifest (Family, designs, provenance) ->
P1.2 loader globs + Family in research/26 -> P1.3a/b seed designs from 19 reasoning rows +
backfill provenance from rationale -> P1.4 test_provenance/test_designs -> P1.5 ddi designs,
--design, handoff line -> P1.6 ddi library -> R1 Opus review.
Phase 2 (parallel with 1): P2.1 research/81-ranking-sources.md (probe each source) ->
P2.2 research/82-design-ranking-protocol.md (Opus freezes).
Phase 3 grand library (<=10 rows/task, separate files): typefaces x3, palettes x3, ratios x1.
Phase 4 designs per family, volume order: cv (6->10), cover-letter, deck, letter, memo, report,
whitepaper, proposal, then invoice, quote, brochure, flyer, one-pager, poster, form, infographic.
Per family: F.a code corpus -> research/designs-evidence/<family>.md; F.b 25% second coder;
F.c author rows in research/library/... + research/designs/<family>.csv + provenance. Target 8-10,
floor 5. R3 blind independent Opus panel after cv/cover-letter/deck.
Phase 5 brand kit: P5.1 generic DOCTYPE_CATALOG; P5.2 `## Designs`; P5.3 brand-kit-builder.md +
examples/generic-law-firm-brand.md.
Phase 6 portability: P6.1 build-portable.py + portable/; P6.2 sync test; P6.3 root README.md;
P6.4 release.yml runs pytest + publishes portable ZIP; P6.5 proxy trial (fresh agent given only
portable/; falsifier: any font/hex not in pack, or no named design = FAIL; disclose ChatGPT/Grok
not directly tested).
Phase 7 release: SKILL.md body step `ddi.py designs` (description untouched, 1010/1023);
RELEASE-NOTES v0.5.0 (folds in untagged v0.4 + Phase A); RESUME cold start; R4 final review;
tag v0.5.0, verify downloaded assets.

## §7 Risks
Fetchability of JS-heavy sources (Canva, Behance, Coolors) — use APIs/fallbacks; a rank from a
search snippet never becomes a numeric Rank Value. Popularity != quality — admissibility filter;
ship what evidence supports (floor 5, one convention max as padding). Pack size (<~300 KB).
Parity churn on every new column. Default vs rank: the doctype default stays the fitness choice
(research/72 DACH precedent). ChatGPT/Grok verified by proxy only — disclose.
