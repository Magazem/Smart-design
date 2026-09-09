# Schema §0.2 / T1–T2 vs. current upstream mechanism

**Version correction first.** The task cites a "v2.15.0 overhaul." I re-fetched `upstream-latest/` (`git fetch --depth 1 origin main`) — HEAD is still `4aad0584`, `2026-09-06`, `plugin.json` version `2.13.0`. Upstream has not moved since `research/10-mechanism-refresh.md` was written. Everything below is checked against **2.13.0**, the actual current upstream, not 2.15.0. The mechanism changes the task describes (relevance overhaul, deprecation redirects, Style-ID search) are real — they're just already the subject of report 10, not a newer version on top of it.

## 1. Is §0.2's engine description still accurate?

**No — it undersells how far upstream has already moved toward the schema's own proposed deviation.**

§0.2 keeps three claims. Checked against `upstream-latest/src/ui-ux-pro-max/scripts/`:

- *"BM25 over designated search_cols... from-scratch, k1=1.5/b=0.75, no embeddings."* — Still true as far as it goes (`core.py:285`, `k1=1.5, b=0.75`, unchanged formula). But it's no longer a complete description of the retrieval step. Current `search()` (`core.py:755-845`) runs an **exact-identity short-circuit before BM25 ever executes**: `_style_identity()` and `_exact_row_identity()` try to resolve the query directly against `Style ID`/`Style Category`/`Aliases` (style) or `Pattern ID`/`Pattern Name`/`Aliases` (landing) identity fields; only if that misses does BM25 run, and even then it runs against a **calibrated, abstaining** scorer — per-domain score floors, coverage thresholds, and margin checks (`_SEARCH_THRESHOLDS`, `core.py:203-213`) that make it return **zero results + suggestions** rather than a weak top-1 guess when confidence is low. "BM25 over search_cols" describes the fallback path now, not the primary one.
- *"The chain: doctype → reasoning → biased style/palette/typeface lookups."* — Still architecturally correct; `generate()` still does product-search → `_apply_reasoning()` → `_multi_domain_search()` in that order (`design_system.py:461-476`).
- *"Closed-form rerank (`_select_best_match`, exact-name-wins then weighted score)."* — This is the one that changed materially. See §2 below — it's no longer just a rerank of BM25 candidates.

**What the schema should know about:** upstream now has an exact-identity index (`_style_identity`, `core.py:664-692`; a plain dict lookup, `_build_style_lookup`, `design_system.py:296-305`) that resolves a known name/alias/ID with zero fuzziness before BM25 is consulted at all. Recommend the schema's own T1 fuzzy step adopt the same shape: try an exact `doc_key`/alias hit first, fall back to BM25 only on a miss. This is a small, low-risk addition (it's what upstream's own evolution converged on) and it strengthens exactly the reproducibility argument §0.2 already makes for T2.

## 2. Is the explicit-FK deviation implementable on stdlib, and what's the hidden cost?

**Implementable, and lower-risk than the schema assumes — because upstream has already partially built it.**

`_select_best_match()` (`design_system.py:408-443`) no longer does what §0.2 describes upstream as doing. Read in full, it now does:

```python
for priority in priority_keywords:
    resolved = self._resolve_style(priority)
    if resolved and resolved.get("Status", "active") != "deprecated":
        return dict(resolved)
# only then: score by keyword match in all fields  (the old behavior)
```

`_resolve_style()` (`design_system.py:307-317`) is a **direct dict lookup** against `self.style_lookup`, built once from `Style ID` + `Style Category` (`_build_style_lookup`, lines 296-305), with deprecation-chain walking via `Parent Style ID`. That is a foreign-key resolution stage — the exact pattern the schema calls a "deviation" — already living inside upstream's own `_select_best_match`, for the **style** stage specifically, with BM25 keyword-scoring kept only as the fallback when the name doesn't resolve. This is proof by existence that a direct-lookup stage does not break upstream's output contract, `MASTER.md` formatting, or `validate_data.py`: it's already shipping in the version those things validate against.

One caveat the schema should record precisely: **this convergence is style-only.** `Color_Mood`/`Typography_Mood` (`_apply_reasoning`, `design_system.py:393-406`) are still plain text folded into the biased BM25 query in `_multi_domain_search` — there is no `_resolve_palette`/`_resolve_typeface` equivalent yet. So the schema's `Palette Key`/`Typeface Key` foreign keys are not mirroring an existing upstream mechanism the way `Style Key` would be — they're extending the pattern to two stages upstream hasn't gotten to yet. Still fully implementable with stdlib (it's one more `dict` built at load time, same shape as `style_lookup`), just worth being honest that it's "upstream's own next step, taken early," not "already proven for all three."

**No hidden cost found** against the output contract: `search()`'s return shape (`{"domain", "query", "file", "count", "results", ...}`, `core.py:821-845`) is unaffected by whether a hit came from BM25 or from the identity dict — both paths produce the same row shape via `_project_row`. `MASTER.md` formatting (`format_master_md`) consumes the resolved dict, not the resolution method. A direct-lookup stage is invisible downstream.

**Recommendation:** keep the schema's FK design as-is; cite `_resolve_style`/`_build_style_lookup` as upstream precedent for `Style Key` specifically, and note `Palette Key`/`Typeface Key` as a deliberate extension beyond current upstream, not a mirror of it.

## 3. T2's decision-rule handling — recommendation

**T2's factual premise is wrong (see §5), but its instinct — no free-text JSON blob — is right for the wrong stated reason. Recommendation: build the same closed-grammar mechanism upstream now ships, don't leave conditional behavior out of the table entirely.**

Upstream did not solve this by deleting `Decision_Rules`; it solved it by validating it. `reasoning_contract.py` is a ~120-line, stdlib-only module: a fixed `CONDITION_SIGNALS` dict (32 keys, report 10 §4 has the full list), a hard-fail parser (`parse_decision_rules`, unknown condition or malformed action → `ValueError`, not silent drop), and an `apply_decision_rules` that only ever produces `constraint:`/`style:`/`pattern:`/`mode:` actions matching a token regex. That is exactly what Rule 1 should be reaching for: the danger Rule 1 correctly names is *untyped, uncheckable* logic in a cell, not *any* conditional expression in a cell. A closed, enumerated vocabulary with a validator that rejects anything outside it is not the same risk — it's the same discipline the schema already applies to `Artifact Class` (an enum) and `Table Rules`/`Field Style` (enums), just applied to a condition→action mapping instead of a single value.

Build `doc_reasoning_contract.py` on the same shape: a closed `DOC_CONDITION_SIGNALS` dict seeded with the five doctype-relevant conditions named in the task (`if_hand_filled`, `if_photocopied`, `if_projected`, `if_ats_target`, `if_professional_print`) plus whatever else the document corpus needs, each mapped to matching substrings the same way upstream maps `if_data_heavy` to `("data heavy", "data-heavy", "analytics", "large dataset")`. Actions restricted to prefixes T2 already has columns for (`constraint:`, `style:` if a doctype-level override is ever needed) so the grammar has nowhere to smuggle in real branching. Validate it exactly like upstream: a build-time check that rejects unknown keys/actions (mirrors `validate_data.py`'s `_check_reasoning_contract`), and — since `Severity` already exists on T2 — extend `validate-severity-map` to also confirm every activated condition reaches a real constraint, the same closed-loop check upstream's validator does for style/pattern actions (`validate_data.py:366-372`).

This gets T2 real per-document conditional behavior (a hand-filled form and a photocopied internal note can now diverge from one `doc_category` row instead of requiring two rows) without reopening the actual defect Rule 1 was written against.

## 4. §4 validator manifest — upstream precedent map

| Direct or partial precedent in upstream | Net-new (no upstream analog) |
|---|---|
| 1 `validate-keys` — precedent: `validate_data.py`'s cross-file `Product Type`/`UI_Category` set-equality + duplicate-key checks (`validate_data.py:337-358`) | 2 `validate-checks-implemented` |
| 11 `validate-contrast-screen` — direct precedent: `_check_color_contract`'s WCAG ratio math (`validate_data.py:387-414`), same 4.5:1/3:1 thresholds | 3 `validate-severity-map` |
| 15 `validate-palette-only` — direct precedent: `html-token-validator.py`'s `FORBIDDEN_PATTERNS` hex/rgb/rgba-outside-allow-list check | 4 `validate-artifact-class` |
| 16 `validate-anti-patterns` — direct precedent: `html-token-validator.py`'s whole grep-against-pattern-list mechanism, generalized to a token list | 5 `validate-brand-resolution` |
| 8 `validate-font-resolution` — partial precedent: `_check_typography_contract`/`_check_font_catalog` validate CSS-import/font-weight/Google-Fonts shape, but not an embed-vs-safe-stack fork | 6 `validate-engine-available` |
| 26 `validate-checklist-emitted` — loose precedent, different mechanism: upstream *bakes* a fixed checklist into generator output (`format_master_md`, confirmed report 01 §1.5) rather than validating it post-hoc on a rendered artifact | 7 `validate-print-mode-coherence` |
| 27 `validate-figure-size`/`validate-series-count`/`validate-label-strategy` — partial precedent: `_check_chart_contract` validates the chart *data catalog* (accessibility grade, text fallback), not rendered figure geometry | 9 `validate-cpl`, 10 `validate-type-floor` (threshold exists as prose in `ux-guidelines.csv`, never enforced by a script) |
| | 12 `validate-contrast-print`, 13 `validate-greyscale`, 14 `validate-text-safe-roles` |
| | 17 `validate-font-embedded` (no OOXML handling anywhere upstream) |
| | 18 `validate-ats-structure`, 19 `validate-text-layer` |
| | 20 `validate-pagination`, 21 `validate-bleed`, 22 `validate-fold-geometry` |
| | 23 `validate-tabular-figures` |
| | 24 `validate-density` (threshold exists as prose in `design-system/SKILL.md`, "max 5 bullets," never enforced by a script) |
| | 25 `validate-section-order`/`validate-canonical-headings`/`validate-heading-depth`/`validate-caption-position`/`validate-cross-refs` |
| | 28 `validate-emphasis-mechanism`/`validate-table-style`/`validate-family-count`/`validate-dpi` |

**Recommendation:** for the "direct precedent" rows, port the actual upstream function shape (same threshold constants, same hard/soft-fail split) rather than re-deriving it — `_check_color_contract`'s contrast math and `html-token-validator.py`'s allow-list pattern are already correct and tested. Everything in "net-new" is new because upstream has no flow/print/OOXML concept at all (matches report 01's Gaps finding exactly) — budget these as real build work, not adaptation work.

## 5. Factually wrong about upstream — quote and correct

**T2, lines 231-234** (and the same claim restated in §0.2 Rule 1, lines 20-27):
> *"`Decision_Rules` is not carried forward. It is inert upstream (Rule 1) and there is no honest way to keep it without building the evaluator `01-mechanism.md` §4 says does not exist."*

**Wrong for current upstream.** The evaluator exists: `src/ui-ux-pro-max/scripts/reasoning_contract.py`, imported at `design_system.py:28` and called at `design_system.py:385-386`:
```python
decision_rules = parse_decision_rules(rule.get("Decision_Rules", "{}"))
applied = apply_decision_rules(decision_rules, query)
```
`CONDITION_SIGNALS` (`reasoning_contract.py:7-43`) is a real, executing, 32-key closed vocabulary (`if_booking` … `if_video_ready`, plus `must_have`). `01-mechanism.md` §4's "no evaluator exists" finding is correct for the v2.5.0 checkout that report was written against, not for current upstream — this is precisely the version-skew correction `research/10-mechanism-refresh.md` §7 already made in writing. T2 is citing a superseded finding as if it were still current.

**Correction:** *"`Decision_Rules` upstream now executes against a closed, validated 32-key condition vocabulary (`reasoning_contract.py`); only conditions outside that fixed set are inert. Keeping our own version of `Decision_Rules` is possible and upstream-precedented (see §3) — the reason to still not carry the column forward unchanged is that upstream's specific 32 keys are all web/product vocabulary (`if_booking`, `if_checkout`, `if_luxury`...) and none apply to documents, not that the mechanism doesn't work."*

**§0.2's Rule 1 text is additionally self-contradictory as written**, independent of the version question: *"It is inert: design_system.py:385 reads it but only a fixed set of built-in condition keys can ever fire..."* — a fixed set of keys that "can ever fire" is the definition of *not* inert. The sentence describes a working, closed evaluator and then calls it inert in the same breath. Recommend rewording regardless of which upstream version is cited, to distinguish "unknown/custom keys never fire" (true in both versions) from "nothing fires" (only true in the old one).

**No other factual errors found in §0.2/T1/T2 beyond this one** — T1's design notes (canvas-vs-flow, region-as-doctype-variant) make no claims about upstream's current code that need checking; they're original schema design decisions, not mechanism descriptions.
