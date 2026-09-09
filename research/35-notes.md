# 35-notes — abstain thresholds, derived (Mechanism Analyst, research/brief-mechanism.md)

## What changed in resolve.py

1. **Stopword filtering**, applied inside `BM25.tokenize` itself -- the one
   function `fit()` (documents) and `scores()` (query) both call, so the
   query and the keyword text are filtered identically by construction, not
   by two call sites that could drift. `_STOPWORDS` is closed-class words
   only (articles, pronouns, prepositions, conjunctions) plus the generic
   request-verbs that appear as filler across almost every doctypes.csv
   Keywords cell (`make`/`build`/`draft`/`write`/`create`, `erstelle`,
   `fais`/`rédige`) -- never a content word, even a frequent one (`cv`,
   `présentation` stay unfiltered). en + de covered per the brief (E3/D3).
   fr checked against the real Keywords text (`fais-moi`, `rédige mon`,
   `un cv`, `pour ce client`, ...) and included for the same reason -- French
   queries (F1/F2/F3/F4) hit the same filler-word pattern.
   Accented forms (`für`, `rédige`, `rédiger`) are deliberately **not** in
   the literal set: the tokenizer already splits on any non-`[a-z0-9]`
   character, so an accented source word never survives as one token in the
   first place (`für` -> `f`, `r`; `rédige` -> `r`, `dige`) -- adding the
   accented spelling would be dead code, and this project requires
   ASCII-only source (`scripts/tests/test_ascii_clean.py`).

2. **Abstain rule**, floor + a **relative** margin:
   `abstain = top_score <= _SCORE_FLOOR or (top - runner_up) / top < _MIN_MARGIN_RATIO`
   (only the second clause applies once there's more than one nonzero
   candidate). Relative, not absolute, because a fixed absolute gap tuned on
   the ~30-row `doctypes.csv` corpus does not port to a smaller corpus with
   different score magnitudes -- this project's own `tests/fixtures/manifest_ok`
   (2-3 rows) is exactly that case, and `pytest -q` is the proof: an
   absolute-margin version of this same derivation abstains on the fixture's
   `"hammer tool"` case, which must resolve.

## The 12-query score distribution (data-derived)

Ran `bm25.scores(query)` against the real `data/base/doctypes.csv` entry
rows (`Display Name` + `Keywords`, the manifest's `searchable_columns` for
`doctypes`) for all 12 queries, before and after stopword filtering.

**Before** (no stopword filtering -- the pre-fix baseline):

| # | top pick | top score | margin (abs) |
|---|---|---:|---:|
| E3 | cv-generic (WRONG) | 5.8756 | 0.7996 |
| D3 | slide-deck-projection (WRONG*) | 12.0324 | 6.1865 |
| F3 | cv-generic | 5.6909 | 0.0877 |

*D3's pick is the "expected" doctype by content, but the brief rules the
query itself ambiguous (projection vs. document vs. handout deck) -- see below.

**After stopword filtering, ratio = (top - runner_up) / top:**

| # | expected | top pick | top score | ratio |
|---|---|---|---:|---:|
| E1 | cv-academic | cv-academic | 12.7252 | 0.8046 |
| E2 | slide-deck-handout | slide-deck-handout | 11.8781 | 0.6401 |
| **E3** | **abstain** | brochure-flyer-letter | 4.5297 | **0.0393** |
| E4 | invoice-tabular | invoice-tabular | 5.7753 | 1.0000 |
| F1 | memo-internal | memo-internal | 9.3123 | 0.6107 |
| F2 | quote-devis | quote-devis | 9.9659 | 0.7185 |
| **F3** | cv-generic *or* abstain | cv-uk | 2.4867 | **0.0054** |
| F4 | report-long-toc | report-long-toc | 13.2021 | 0.5788 |
| **D1** | cv-dach | cv-dach | 2.2680 | **0.2492** |
| D2 | cover-letter | cover-letter | 5.1407 | 0.3920 |
| **D3** | **abstain** | slide-deck-projection | 8.1070 | **0.3154** |
| D4 | cv-eu-europass | cv-eu-europass | 8.0972 | 0.7199 |

## The threshold: `_MIN_MARGIN_RATIO = 0.15`

The must-abstain ratios (E3=0.0393, F3=0.0054) and the smallest
must-resolve ratio (**D1=0.2492**, the binding constraint -- `cv-dach`
narrowly beats `cv-eu-europass`/`cv-eu-generic` because seven of the nine CV
rows all carry the token `lebenslauf`) leave a band of
**0.0393 -> 0.2492**, a 6.3x separation. `0.15` sits in that band with
margin on both sides (3.8x above the highest must-abstain ratio, 1.7x below
the lowest must-resolve one). `_SCORE_FLOOR = 0.0` is unchanged and does no
work in any of the 12 cases -- every query that should resolve produces a
nonzero top score, and E3's pre-fix failure scored 5.8756, well above zero,
so floor was never the lever; margin (now ratio) is what abstention runs on.

**What would break `0.15`:** D1 at 0.2492 is only ~1.7x the threshold, and
it's thin specifically because `lebenslauf` (German for "CV") is repeated
across seven of the nine CV-family rows -- one more German synonym added to
any regional CV row's Keywords narrows this further and risks pushing D1
into the abstain band. `cv-dach` (`doctypes.csv` row) is the name to check
first if a future regression report says a German CV query now abstains
that used to resolve.

## Acceptance: 3 of 4 bullets met, D3 not met -- and cannot be by this mechanism

- **E3 "make me a flyer" ABSTAINS** -- yes. No longer scores `cv-generic` at
  all (stopword filtering removed `make`/`me`/`a` from both the query and
  `cv-generic`'s `"make me a resume"` keyword phrase); top two candidates
  are now the two real flyer rows, in a genuine near-tie (ratio 0.039).
- **The nine other correct queries (E1, E2, E4, F1, F2, F4, D1, D2, D4)
  still resolve correctly** -- yes, verified via the live CLI (`resolve.py
  --query ... --json`), not just the internal scorer.
- **F3 gains no new confident wrong pick** -- yes: F3 now abstains (ratio
  0.0054, effectively a 4-way tie among `cv-uk`/`cv-gulf-gcc`/`cv-academic`/
  others) rather than resolving at all. Per the brief's own bullet 4, this
  is an accepted outcome, not a regression.
- **D3 "erstelle eine präsentation" ABSTAINS** -- **not met.** Traced why:
  after stopword filtering, D3's ratio (0.3154) is *larger* than D1's
  (0.2492) -- D3 is measurably *more* confident by this metric than a query
  that must stay resolved. No single margin/floor threshold (absolute or
  relative) can abstain D3 while resolving D1: any cutoff high enough to
  catch D3 also catches D1 (and, checked separately, D2 at 0.392 stays
  clear either way, so D1 is the actual binding case, not D2).

  Root cause, separate from the stopword fix: `slide-deck-projection`'s
  Keywords cell contains the phrase for "presentation" in three scripts
  (`presentation`, `présentation`, `präsentation`) with the German and
  French forms *each appearing twice* (once standalone, once inside a
  longer phrase) -- tf=4 for the query's dominant token. Its siblings
  (`slide-deck-document`, `slide-deck-handout`) each carry the phrase only
  once or not at all (tf=2, tf=1). Compounding this: the tokenizer splits
  on any non-`[a-z0-9]` character, so accented `präsentation` and
  `présentation` both collapse to the identical fragment pair `pr`+
  `sentation` -- German and French mentions of "presentation" count as the
  *same* token, further inflating `slide-deck-projection`'s score relative
  to a design where they'd be distinct tokens. Confirmed this isn't a
  tokenizer-only artifact: re-ran with an accent-preserving tokenizer
  (kept `à-ö`, `ø-ÿ` as word characters, so German/French forms no longer
  collide) as a diagnostic only, not shipped -- D3's top score and absolute
  margin both fell (top 8.107 -> 3.8562, margin 2.5566 -> 1.7621), but its
  *ratio* actually widened (0.3154 -> 0.4571) while D1's stayed about the
  same (0.2492 -> 0.2477). The D1/D3 inversion survived either way -- the
  diacritic collision inflates D3's raw score, but isn't the reason
  margin/ratio can't separate it from D1. This is a genuine Keywords-cell asymmetry
  in the data (`data/` is out of scope for this task) combined with a
  tokenizer limitation (also out of scope -- the brief's ONE deliverable is
  stopwords + floor/margin abstention, not a tokenizer rewrite), not
  something a smarter constant fixes. Flagged to the lead in the report.

## Test count

`pytest -q` from the skill dir: **126 passed, 8 subtests passed** (baseline
was 121 + 8; brief's floor was >= that). New: `TestMarginRatioBoundary`
(`scripts/tests/test_resolve.py`) -- `test_clear_win_resolves` and
`test_weak_top_abstains`, both hand-verified against `resolve.BM25` directly
(same standard as the module docstring's hammer/dice tie), plus the
pre-existing tie test (`test_margin_tie_abstains_not_a_coin_flip`) covers
the third named branch.
