# BRIEF — Coverage and Gap Analyst: reload T1 + run the D3 acceptance test (~8 min)

Context reset by policy; nothing lost. Load pass 4 is verified and closed — the gate is ZERO
("OK: validated 14 table(s), 291 row(s)"). Act from THIS FILE and from disk.

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Skill dir: skill\document-design-intelligence
Python:    C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## What changed and why you are reloading
The resolver can now abstain on ambiguous queries, but the German one, D3
"erstelle eine <praesentation>", still resolved CONFIDENTLY to `slide-deck-projection`.
That was a DATA asymmetry, not an algorithm fault: projection's Keywords cell carried the
presentation stem five times against its siblings' three and one, including two bare
duplicate tokens with no retrieval value.
The DDR has fixed `research/26-t1-doctypes-draft.csv` (verified by me): projection 5 -> 3,
handout 1 -> 2 (its missing German form added), document unchanged at 3. Projection and
document now have identical structure — one English term, one French phrase, one German
phrase each. No duplicate tokens remain on any deck row.

## ONE deliverable: T1 reloaded and the acceptance test answered.
1. Reload T1 from `research/26-t1-doctypes-draft.csv` via `research/load-base.py`.
2. Run the gate. It MUST still be ZERO — this is a keyword-text change only, so any new line
   means something else moved and that is the story, not the count.
3. Run the acceptance test and report the real output:
   - D3 "erstelle eine <praesentation>" (the German accented form) must now ABSTAIN.
   - The German deck query must still surface the DECK FAMILY as its candidates — if it
     abstains but offers CVs, that is a failure, not a pass.
   - D1 "erstelle einen tabellarischen lebenslauf" must STILL RESOLVE to `cv-dach`. This is
     the binding constraint: D1's margin ratio was the thing that made D3 unfixable by
     thresholds, so it is the row most likely to break.
   - E3 "make me a flyer" must still abstain with its two flyer rows.
   Note the Mechanism Analyst is editing `resolve.py` right now for the zero-score case; if
   its work is mid-flight your query output may shift under you. Report what you see and say
   when you ran it. Do NOT edit resolve.py.

## If D3 still does not abstain
Say so plainly with the numbers. That is a legitimate outcome — it would mean the data fix
was insufficient and the remaining cause is the tokenizer collapsing the accented forms,
which is a post-release item. Do not chase it, and do not tune anything to force a pass.

## Do not
Touch `scripts/`, the manifest generator, or any `research/*.csv` draft.

## VERIFY
Gate output pasted. Loader idempotent over two runs. `assert_no_brand_rows()` clean.
`pytest -q` from the skill dir; note the count and whether any failure is Mechanism's
in-flight work rather than yours.

## REPORT
Max 8 lines to the Workflow Orchestrator, slot 01a080c5-2001-78b3-bbbe-afaae15edafa:
the gate number, the four acceptance results with their candidate lists, idempotency, and
the test count. If you approach ~10 minutes, checkpoint to research/handover-coverage.md
and stop.
