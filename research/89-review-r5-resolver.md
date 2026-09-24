# 89 — R5 code review: resolver family defaults, query language, named-family narrowing

Reviewer: Opus Reviewer (adversarial). Date: 2026-09-24.

Commits reviewed:
- **f64f4ca**: `_family_default`, `_detect_language` / `_LANG_WORDS`, the `doctypes.Family
  Default` column, the US/letter sibling swap;
- **baa43bb**: `_named_family` narrowing;
- `research/88-generic-request-census.md`.

This is a read-only review. The only file written is this one.

**Method.**
- Queries were run with `python3 scripts/ddi.py resolve --query "<q>" --json` from
  `skill/document-design-intelligence/`. One bash harness printed `doctypes[0].key`,
  `method`, `language` and wall time per query.
- The brand tests used a temp copy of `data/` with the ENS kit extracted into `brand/ens/`,
  built by `make_brand_kit.py examples/ens-brand.md`.
- Tests were run on a clean `git archive baa43bb` snapshot, because the working tree holds
  other workers' uncommitted data edits.

**Verdict.** The mechanism works, and the commits' own test suite passes on the clean
snapshot (281 passed). Plain "CV", "Lebenslauf" and "fais-moi un CV" now resolve instead of
abstaining. But:
- one upgrade path breaks resolution entirely (F1);
- the two text heuristics, language and named family, have false positives on common
  phrasing (F2–F4);
- none of the new assumptions are visible to the caller (F8).

Fix F1–F4 before release.

Severity: **H** = wrong document or total failure on a realistic request; **M** = wrong
variant, inconsistent or invisible behaviour; **L** = polish.

---

### F1 (H) — Brand kits built before f64f4ca make EVERY query refuse

f64f4ca appended the `Family Default` column to `doctypes`. The loader's header check is exact,
and a structural problem refuses the whole dataset, so one old kit disables the skill for all
queries, not just that brand's.

Repro (temp data dir: the current ENS kit plus a copy whose `doctypes.csv` header lacks the new
column, installed as `brand/old/`):
```
python3 scripts/ddi.py resolve --query "slides" --brand old --data-dir <tmp>
  <tmp>\brand\old\doctypes.csv: header mismatch: missing ['Family Default']
  [DATA INVALID] 1 structural problem(s) -- refusing to resolve
python3 scripts/ddi.py check --data-dir <tmp>   -> same, "1 structural problem(s) found -- refusing"
```

**Fix:**
- Make trailing columns added after a kit's build **optional-with-default for brand
  overlays**: `load_table_rows` pads a brand header that is an exact prefix of the manifest
  columns and logs a tier-2 advisory.
- Alternatively, have `merge_brand_kit.py` migrate old kits on install.
- Add a regression test with a prefix-header brand kit.
- Stamp a kit schema version in `brand.md` / the kit zip.

### F2 (H) — "letter" as a paper size counts as naming the letter family

`_named_family` treats every whole-word "letter" as the family name. In "X on letter paper"
two families are then named, narrowing is skipped, and BM25 is split between `letter-formal`
and X. The request abstains.

```
"report on letter paper"     -> abstained
"memo on letter paper"       -> abstained
"a memo on US letter paper"  -> abstained
"invoice on letter paper"    -> abstained
```

"letter size" and "letter paper" are ordinary US phrasing for page size. That is exactly the
cue f64f4ca's `_LETTER_CUE_RE` was written to catch.

**Fix:** before matching families, mask `letter` when it is:
- followed by `size`, `paper`, `format`, `sheet` or `-size`; or
- preceded by `us`, `u.s.` or `american`.

Treat such a match as the page-size cue instead. Add these four queries to the census.

### F3 (H) — Language detection fires on name particles: wrong region CV and wrong headings

`_detect_language` counts `de`, `la`, `du`, `von`, `der` and similar as French/German
stopwords. A name in an English request flips both the doctype and the heading language.

```
"CV for Maria de la Cruz"         -> cv-france  | language fr (source=query)
"CV for Jean-Luc de la Fontaine"  -> cv-france  | language fr
"resume for Anna von der Leyen"   -> cv-dach    | language de (source=query)
```

Control cases that are correct: "CV for a café manager", "resume for a Kindergarten teacher",
"invoice with Rechnung number", "CV for a job at Die Zeit" and "a flyer for le petit café"
all stay English.

**Fix:**
- Skip particles (`de, du, la, le, des, von, van, der, zu, di, da`) when the next original
  token is Capitalised.
- Require at least 2 distinct non-particle stopwords before a language beats English.
- Record `query_language_evidence` (the matched tokens) in the diagnostics.

### F4 (M) — US cue: the pronoun "us" triggers a Letter-size swap, and "U.S." is missed

`_LETTER_CUE_RE` is case-insensitive `\b(us|usa|u\.s\.|letter|american)\b`:
- "us" matches the English pronoun;
- `\b` after the final `.` of `u.s.` never matches before a space.

```
"make a flyer for us"         -> brochure-flyer-letter   (expected a4 default)
"brochure for us"             -> brochure-trifold-letter
"flyer for the U.S. office"   -> brochure-flyer-a4       (expected letter)
"a flyer for the US market"   -> brochure-flyer-letter   (correct)
```

**Fix:** make it case-sensitive for `US|USA`, and handle the rest explicitly:
```
(?:\bUS\b|\bUSA\b|\bU\.S\.(?:A\.)?|(?i:\bamerican\b|\bletter[- ]?(?:size|paper|format)\b|8\.5\s*[x×]\s*11))
```

### F5 (M) — Query language is applied only on the family-default path

`query_language` is set only inside `_family_default`. A French or German request that BM25
resolves outright gets English headings, while the same language on an ambiguous request
gets French.

```
"fais-moi une présentation"             -> slide-deck-projection | language en (doctype-default)
"erstelle eine Präsentation"            -> slide-deck-projection | language en
"rédige un rapport long avec sommaire"  -> report-long-toc       | language en
"fais-moi un flyer"                     -> brochure-flyer-a4     | language fr (source=query)
--brand ens "fais-moi une présentation" -> ens-slides            | language en
```

**Fix:** run `_detect_language` (with the F3 guard) for every `--query` resolution. If it is
confident, not `en`, and there is no `--lang`, set `language = {value, source: "query"}` for
any doctype whose headings exist in that language.

### F6 (M) — Plurals: the named-family regex matches them, but resolution then fails

`_named_family` accepts `s?`, but the narrowed BM25 search has no stemming. It returns
`no-match` (not `ambiguous`), narrowing is abandoned, and the full search also finds nothing.

```
"flyers" -> no_match     "invoices" -> no_match     "posters" -> no_match
"CVs for my team" -> no_match
```

**Fix:** when a family is named and the narrowed search returns `no-match`, go straight to
`_family_default` over that family, or to its single doctype. Better still, fold a trailing
`s` in `BM25` tokenisation for both query and keywords.

### F7 (M) — Multi-family requests silently resolve to one family

When two or more families are named, narrowing is skipped and BM25 or the family default picks
one, with no signal to the caller.

```
"a CV and a cover letter"  -> cover-letter
"slides for the report"    -> report-short       (the artefact is slides)
"deck builder CV"          -> slide-deck-projection
```

**Fix:** when two or more families are named, either:
- (a) abstain with `reason: "multiple-families"` and the list, so SKILL.md's flow asks which
  document to make first; or
- (b) prefer the head noun (the family named before "for/about/on"), and report the other
  families in the diagnostics.

### F8 (M) — The new decisions are invisible in `--json`

The resolved JSON keys are only `status, method, pass, resolved, language, next_step`.
`named_family`, `note` ("query named no variant…"), `query_language` and the candidate list
are dropped. A caller therefore cannot tell the user "I assumed a generic CV" or "I assumed
France". Repro: `ddi.py resolve --query "CV" --json` shows `"method": "family-default"` and
nothing else. **Fix:** emit a `diagnostics` object on resolved output, with
`named_family, note, query_language (+evidence), candidates[:3]`.

### F9 (M) — French maps to France

Step 1 takes the unique `Default Language = fr` doctype, `cv-france`, for any French request.
French-speaking users in Belgium, Switzerland, Québec or Africa get French-market conventions
(photo norms, section order) with no signal. German → `cv-dach` is sound, because DACH covers
DE/AT/CH. **Fix:**
- Take the language-specific regional doctype only when a country cue agrees (`France`,
  `français(e)`, a `.fr` domain). Otherwise use `cv-generic` with `language=fr` headings.
- Or keep the current behaviour but surface it (F8), so Claude asks once, as portable AGENTS.md
  already instructs.

### F10 (L) — The census scores family only, which hides variant errors

`88-census.py` counts a row as right when the family matches. On the clean snapshot:

```
"professional flyer one page A4"      -> brochure-flyer-letter   (explicit A4 ignored)
"make a simple one page CV template"  -> cv-us                   (a plain request gets US conventions)
```

**Fix:**
- Assert the expected doctype for each census row.
- Add an **A4 cue**, symmetric to the letter cue, that swaps a letter-size pick back to its
  `a4-` sibling when the query says A4.

### F11 (L) — `--lang` does not feed doctype choice

`"fais-moi un CV" --lang de` resolves to `cv-france` with German headings. `--lang` overrides
only the heading language (by design), but step 1 of `_family_default` uses the detected
language, not the explicit one. **Fix:** step 1 should use `args.lang` when it is given.
Otherwise, document the current behaviour.

### F12 (L) — Narrowing fallbacks and edge cases

- If the narrowed search abstains for any reason other than `ambiguous`, the full search runs
  and may return a family **other than the one named**. Prefer abstaining with the named family
  in the diagnostics.
- The `whitepaper` family name never matches "white paper". BM25 still resolves it correctly
  today, so this is harmless for now.
- "poster child report" abstains (poster + report named). That's acceptable.

### F13 (info) — Tests, performance, docs

- **Tests:**
  - A clean snapshot of `baa43bb`: **281 passed, 1 xfailed**.
  - `f64f4ca~1`: 268 passed. The commits added 13 tests.
  - The **current working tree fails 67 tests** (test_r2_fixes 10, test_make_brand_kit 8,
    test_ddi 7, test_resolve 1, test_designs 1, …). These come from uncommitted edits by other
    workers (`designs.csv`, `doc-reasoning.csv`, `doc-styles.csv`, `provenance.csv`,
    `SKILL.md`, …), not from these commits. The orchestrator should not commit that tree as-is.
- **Performance:** 0.21–0.41 s per resolve, dominated by data loading. `_named_family` and
  `_detect_language` are O(families + tokens) and negligible.
- **Docs:**
  - SKILL.md and README describe none of family defaults, query-language detection or
    named-family narrowing. SKILL.md step 2 should say: "if `method` is `family-default`, tell
    the user which variant was assumed (country/paper size/language) and offer to switch."
    This needs F8.
  - portable/AGENTS.md ("CV with no country stated: ask once… or use `cv-generic`; write in the
    user's language") matches the code for English, but not for French (F9) or German
    (`cv-dach`).
  - The census document's own claims reproduce: 24/24 in the stray-token census, measured at
    family level only (F10).

## Fix priority
1. F1 (upgrade breaks every brand user)
2. F2, F3 (common phrasing → abstention or wrong country/language)
3. F4, F6, F5 (cue and plural handling, language consistency)
4. F8 (visible diagnostics), then F7 and F9, which rely on it
5. F10–F12
