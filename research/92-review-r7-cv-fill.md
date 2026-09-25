# 92 — R7 audit: cv fill (12 designs) and the generic fill engine

Reviewer: Opus Reviewer (adversarial), 2026-09-25. Read-only; this file is the only output.

**Scope:**
- commit 0856059 (cv fill: `cv-fill.md`, `generate_cv_fill.py`, `research/designs/cv.csv`,
  `research/library/{doc-styles,doc-reasoning}/cv.csv`, `research/provenance/cv.csv`);
- commit 74d9f2f (`fill_family.py` + `fill-specs/cv.json`);
- the **uncommitted** working-tree edit of `fill_family.py` (+251/−44 lines at review time, being
  changed by another worker). Findings say which version they apply to.

**Method:**
- Recomputed the combined table from `cv-header-recode.md` (r2a) and the two corpus files.
- Ran `fill_family.py --family cv --check` (committed CSVs reproduce: `same` ×4) and
  `--dry-run`.
- Ran `ddi.py designs --doctype cv-uk`, plus `resolve --doctype cv-uk --design <k>` and
  `handoff --format docx` for three designs (rendered nothing).
- Classified every generic palette with the engine's own functions.

**Verdict.** The plumbing is sound. The 12 rows load, resolve and hand off, and the committed CSVs
are reproducible from the spec. But **the ranking and the fill each break a pre-registered rule in
ways that change what ships**:
- rank 3 is wrong under C21;
- three designs carry a screen type scale with no heading sizes;
- the palette tie-breaks don't follow §8 as written.

The engine, which will be reused for 15 families, **does not enforce §6/§8**. Rank order,
palette, typeface and style are free decisions in the spec file, and one tie-break cites a ruling
that does not exist. Fix the H items before any other family is filled with this engine.

Severity: **H** = changes what ships or will propagate to every family; **M** = a protocol
deviation or an unbounded judgment; **L** = hygiene.

---

## A. Ranking (§6)

### F1 (H) — Shares count inadmissible exemplars, against C21, so rank 3 is wrong

`cv-header-recode.md` §Combined, which the fill uses, says: "this counts every item of the
archetype (inadmissible included) in k". 82a **C21** was ratified before the fill:
**"shares count ADMISSIBLE exemplars (k); inadmissible items stay in N"**.

Recomputed:
- `1|sans|one-accent|ruled` = NPM 6 items, of which **NPM:038 and NPM:054 are inadmissible**.
- Admissible k = 4, so share_NPM = 4/40 = 0.100 and **combined = 0.0500, not 0.0750**.
- It then ties at 0.050 with `1|sans|mono|split` (GH 0.100) and `1|sans|mono|plain-left`
  (GH 0.025 / NPM 0.075).

Under the engine's own tie order (GH share first), the order becomes:
1. split
2. plain-left (`cv-ats-strict`)
3. ruled

So `cv-sans-accent-ruled` moves from rank 3 to rank 5. Under "max L1 share" it's split, then
ruled (NPM:044 vs GH:010, position), then plain-left. Either way, rank 3 is wrong. No other
step-1 archetype has an inadmissible exemplar. The provenance row
`designs:cv-sans-accent-ruled:1` also records `0.150 (6/40)`; it should be `0.100 (4/40)`.

**Fix:**
- `combined_table()` counts `k` over admissible items only; N unchanged.
- Re-rank cv and correct the provenance row.
- Add a unit test with a mixed-admissibility archetype.

This is **still present in the working-tree engine** (`combined_table`, dry-run shows `0.0750 K=6
adm=4`).

### F2 (M) — The "higher L1 share" tie-break depends on corpus order in the spec

§6 says "higher L1 share → higher L2 share". cv has **two** L1 corpora. `rank_step1()` compares
shares lexicographically in the order the spec lists the corpora (GH first, "primary"). That is a
spec decision, not a rule, and it decided the 8-way 0.025 tie and the 0.050 tie in F1. The code
also never sorts corpora by `level`: an L2 corpus listed first would outrank L1.

**Fix:** a 82a ruling: for ≥ 2 L1 corpora, compare the **max** L1 share, then the next, and so
on (order-free). Sort by level before comparing. Record it in the spec as a rule, not a choice.

### F3 (M) — 12 designs ship against a cap of 10, and the one-per-archetype rule is applied unevenly

§6: "Rank contiguous 1..N, **cap 10**". The fill ships 12, arguing that defaults are never
omitted. That's a real protocol gap: §9 exempts only *unmatched* defaults from the L4 cap and is
silent when a *matched* default's archetype ranks below the cap (`cv-us-uk-designed`, 10th).
But the two exemptions were applied inconsistently:
- `cv-editorial` was **retired** because its archetype (`1|serif|one-accent|ruled`) was
  already taken by a default ("§9 gives one design_key per archetype").
- `cv-dach-tabular` codes to `1|serif|mono|plain-left`, **the same archetype as the default
  `cv-academic`** (cv-fill.md §3 says so). By the same rule it should also have been retired.
  Instead it took the L4 slot.
- The L4 tie-break between `cv-dach-tabular` and `cv-editorial` ("names a real, independently
  documented cultural convention") is taste. §9 has no such criterion.

**Fix:** a 82a ruling, before the next family, that states:
- (a) whether matched defaults may exceed the cap, and by how many;
- (b) that the one-design-per-archetype rule applies to every seed, so `cv-dach-tabular` is
  retired, or the rule is dropped and `cv-editorial` is reinstated;
- (c) a mechanical L4 tie-break (e.g. seed rank order).

### F4 (M) — An inadmissible exemplar decides a variant tie, and positions are compared across corpora

For rank 3, the rules/boxes tie (3 boxes / 3 rules) was broken by NPM:038 ("highest
downloads"), which is **inadmissible**. `modal_variant()` also uses `pos` as the proxy for
"highest-metric exemplar". Position 10 in GH (stars) and position 10 in NPM (downloads) are not
comparable. With admissible exemplars only (044/069/075/083), the tie must be recomputed.

**Fix:** compute modal variants over admissible exemplars only. For a tie, use the native metric
where the corpora share one, else a per-corpus normalised position (pos / N). Log it.

## B. Filling (§8)

### F5 (H) — Ranks 1, 6 and 8 carry a screen type scale with no heading sizes

These ranks use `safe-serif-georgia`, whose `Scale Key` is `report-screen` (Medium **screen**,
body only). §8: "the chosen row's Scale Key must have that Medium [print for cv]; if not, take the
next candidate". The next candidate is `safe-serif-times` (`report-print`).

Observed: the `handoff --format docx` for `cv-serif-plain-centered` (**rank 1**) prints only
`body: 11pt`, with **no h1, h2 or h3**. The renderer gets no heading sizes for the family's
top-ranked design. The working-tree engine already says so in its dry-run: "`safe-serif-georgia`
rejected: Scale Key `report-screen` is medium ['screen'], not print (medium rule)". The committed
decision contradicts it.

**Fix:** use `safe-serif-times` for ranks 1, 6 and 8 (it's also the only serif/serif print row).

### F6 (H) — The palette picks were justified by false statements, then by a ruling that doesn't exist

cv-fill.md §5 says `lib-carbon-mono` is "the only AUTHORITY mono palette". That's false:
`cv-dach-formal` (GOV.UK, authority) and `lib-radix-sand` (Radix, authority; its accent
`#7d5e54` has S < 0.20) are also authority/mono, and `cv-dach-formal` sorts first. It also says
`lib-atlassian-ink` is "the alphabetically-first AUTHORITY one-accent palette". Also false:
`cv-editorial`, `cv-europass` and `cv-harvard` are authority, one-accent, pass 4.5:1 on text and
accent, aren't A7, and sort first.

The working-tree engine now reaches the committed picks through a new evidence order, "fetched
authority outranks search-corroborated authority … (fill engine rule R1,
**research/82a-clarifications-6.md**)". **That file does not exist** (only clarifications-1…5
are present). The rule may be reasonable. But it is **unratified and was written after the
outcome it justifies**, which the pre-registration discipline forbids.

**Fix:** either:
- ratify R1 in a dated 82a file that states it affects cv, and correct cv-fill.md's text; or
- apply §8 as written: mono → `cv-dach-formal`; one-accent → `cv-editorial` (or, if cv-specific
  palettes are to be excluded, **say so in a rule**).

### F7 (M) — Reusing the Europass style makes rank 3 inherit Europass-only instructions

`cv-sans-accent-ruled` reuses the `cv-europass` style row. §8 checks only Table Rules, Fills,
Emphasis, Field Style, Rule Brand and checklist contradictions on columns and photo, so the reuse
is legal. The handoff checklist for this generic ruled CV now says "**Follow the Europass section
order** … **Include a language-proficiency table using the recognised EU framework**".

**Fix:** a 82a rule. Reuse requires that the reused row's checklist contain no
family-variant-specific instruction (anything naming a region, standard or programme). Otherwise
author a new row. In the engine, flag checklist lines that name a doctype, region or standard.

### F8 (M) — Doc-reasoning bias terms contradict the design

§8 copies bias terms from the family default (`cv-ats-strict`: "monochrome, ink on white, no
color-coded meaning"). They are copied verbatim into the one-accent designs (ranks 3, 6, 7, 9),
which resolve to an accent palette. cv-fill.md discloses this as a mechanical artefact. The BM25
search and `designs --query` read these terms, though, so an accent design advertises
"monochrome". **Fix:** amend §8. Copy Doc Conditions and Severity only, and derive bias terms from
the archetype's own features.

### F9 (M) — The first typeface branch of §8 was never evaluated

§8's first branch: "if the modal declared font across the archetype's items is OS/Office-bundled
… pick the `safe-*` row". Neither cv-fill.md nor the engine checks declared fonts. The engine
docstring admits "that branch stays a decision". For CV corpora full of LaTeX (Computer Modern)
and HTML (system stacks), the outcome could differ, e.g. `safe-sans-arial` instead of
`lib-roboto`. **Fix:** record per-item declared fonts where the corpus file has them (C25 already
reads theme fonts for MS). Otherwise log "branch not evaluable" per archetype.

### F10 (L) — Evidence class of merged designs

`cv-eu-europass` (rank 2) and `cv-us-uk-designed` (rank 10) ship as `authority`, although their
rank comes from counted shares. §6 says an L3 design that merges "rank unchanged, extra provenance
row". The honest class is `ranked`, with the authority as an extra provenance row. Minor, but the
designs table's class column is what users read.

### F11 (risk, not verified) — `cv-dach-tabular` vs the family's own ATS fail constraint

The DACH style is a label/content **table**. cv doctypes carry `ats-strict`
(`validate-ats-structure (tables_in_body) — fail`). §12 F6 withdraws any shipped design whose
rendered handoff trips a fail-severity preflight. I rendered nothing (task scope).
**Run F6 for `cv-dach-tabular` before release.**

**ATS checks on the other 11:** every checklist has "Keep single column"; there are no skill-bar,
icon or multi-column tokens; photo is permitted only in ranks 4 and 9 (the `photo` token was
removed; cv-regions' photo=warn then applies). No violation found.

## C. Provenance (§9)

- URLs, metric strings and dates match the corpus headers. `Rank Value`s match the r2a table,
  **except `cv-sans-accent-ruled` (F1)**.
- Every non-convention row has `Fetch = fetched` (checked programmatically).
- The fill-rule rows cite a corpus URL with `fill-rule:research/82§8`, `n/a`. That's acceptable.

## D. The engine (`fill_family.py`) as the tool for 15 more families

### F12 (H) — The engine proposes; the spec decides everything, and nothing checks the gap

`build()` takes **Rank from the order of `spec["designs"]`** ("Rank = position in the decided
list"). Palette, typeface and style keys also come from the spec. `--check` only verifies that
the spec reproduces the committed CSVs. It never checks that the spec agrees with the engine's
§6 ranking or §8 proposals. So every rule deviation above would pass CI silently. The decisions
log shows the differences, but no one is required to read it.

**Fix:**
- `--check` fails when a ranked design's position, or a fill key, differs from the engine's
  proposal, unless the spec carries an `override` entry with a rule citation (an 82a id).
- Report the override count per family in the log and the release notes.

### F13 (H) — Hard-coded `cv-` in style reuse

`reuse_candidates()` sorts `not k.startswith("cv-")`, i.e. "family-prefixed first", but for
every family, not just cv. For invoice or deck, cv rows would lose priority to nothing, and the
family's own rows would not be preferred. **Fix:** pass `family` and use `f"{family}-"`.

### F14 (M) — The reuse check ignores photo contradictions

§8 says reuse requires "no Checklist line contradicts it (column count, **photo**)". The engine
checks only multi-column. A `photo = yes` archetype could reuse a row whose checklist says "Omit
photo". **Fix:** add the photo check (and C28-style routing rules if they become checklist lines).

### F15 (M) — The engine's typeface proposal ignores body class and excludes `safe-*` rows

`propose_typeface()` filters on heading class only, but §8 says "heading class **and body class**
match". It also drops every `safe-*` row, which is exactly what cv's serif/serif archetypes need.
The committed engine therefore proposes serif/**sans** pairings (Merriweather/Merriweather Sans,
Source Sans/Serif) for serif/serif archetypes. The working tree now reaches `safe-serif-times`
through the medium rule. That's better, but verify the body-class filter.

### F16 (fixed in the working tree, confirm when committed) — `palette_class`

In committed 74d9f2f, `palette_class()` returned `fill-blocks` for any palette with non-empty
`Fill-Only Roles`. That's **all 78 generic palettes**, so the engine proposed no mono or
one-accent palette at all. The working tree fixes it (`palette_serves`). Add a regression test.

### F17 (L) — `_lib_rows` double-reads library rows

Base palettes already contain the `research/library/palettes/*.csv` rows, so the engine sees each
of those palettes twice (visible in the dry-run's duplicated notes). This is harmless for
ordering, but noisy. **Fix:** de-duplicate by key.

## Fix priority

1. **F1** (C21 count): re-rank cv.
2. **F5**: switch Georgia to Times for ranks 1, 6 and 8.
3. **F6**: ratify R1 in a real 82a file, or re-pick the palettes.
4. **F12** + **F13** before the engine fills another family.
5. A ruling for **F2/F3** (tie order; cap and one-per-archetype; L4 tie-break).
6. F7, F8, F14, F15, F9.
7. Before release: F6-render check of `cv-dach-tabular` (F11).
