# BRIEF — Mechanism Analyst: fold diacritics in the tokenizer (pre-release, ~10 min)

Context reset by policy; nothing lost. Your zero-score fix is verified, committed (81bfaeb)
and closed: 128 passed + 8 subtests, "[NO MATCH]" for a query that matches nothing.
Act from THIS FILE and from disk.

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Skill dir: skill\document-design-intelligence
Python:    C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## The defect, reproduced directly (not inferred)
`BM25.tokenize` splits on `[^a-z0-9]+`, so one word has THREE tokenizations:
    accented form  -> ['pr', 'sentation']
    ae-spelling    -> ['praesentation']
    plain form     -> ['presentation']
Consequences measured on live data:
- D3, the German deck query in its accented spelling, still RESOLVES confidently to
  `slide-deck-projection` when it should abstain. All three deck rows tie at pr=2,
  sentation=2, and projection wins only on length normalisation (18 tokens vs 34).
- The same query in its ASCII spelling scores **0.0 on all 30 rows** — no candidates at all.
- Every accented French and German term in the library is effectively unsearchable.
The skill's activation description advertises French and German triggers, so this is a
claim the product does not honour. RULED pre-release by the lead.

## ONE deliverable: accented and plain spellings score identically.
1. **Fold diacritics in `tokenize`**: NFKD normalise, strip combining marks, then the
   existing split. Apply it SYMMETRICALLY to the query and to the keyword/searchable text —
   asymmetry here is its own bug.
2. **German transliteration equivalence**: ae/oe/ue/ss must match the umlaut and eszett
   forms, so both spellings of a German word converge on one token.
3. **NO THRESHOLD CHANGE.** A margin in (0.1862, 0.2492] would turn all four acceptance
   bullets green with one constant, and the Coverage analyst deliberately refused it: a
   0.063-wide window fitted to two queries is tuning to the test, and it leaves every
   accented term unsearchable. Do not take that shortcut. If your change alone does not
   satisfy a bullet, report that honestly.
4. **The ASCII-clean test still applies** to your source: write the transliteration map with
   `\x` escapes or `unicodedata` lookups, not literal accented characters.

## Acceptance — report each explicitly
- The accented and plain spellings of the German deck word produce IDENTICAL scores.
- D3 (accented) ABSTAINS, with the deck family as candidates.
- D1 "erstelle einen tabellarischen lebenslauf" still RESOLVES to `cv-dach`.
- E3 "make me a flyer" still ABSTAINS with its two flyer rows.
- The ASCII spelling no longer scores 0.0 on every row.
- The existing 128 tests stay green; add tests for the folding itself.

## Do not
Touch `data/`, `research/load-base.py`, the manifest, or any `research/*.csv` draft.
Do not run ANY git command — the Orchestrator commits, path-scoped, after verifying.

## REPORT
Max 8 lines to the Workflow Orchestrator, slot 01a080c5-2001-78b3-bbbe-afaae15edafa:
the six acceptance results with numbers, the test count, and the paths you changed.
If you approach ~10 minutes, checkpoint to research/handover-mechanism.md and stop.
