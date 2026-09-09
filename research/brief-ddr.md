# BRIEF — Document Design Researcher: the D3 keyword asymmetry (small, ~8 min)

Context reset by policy; nothing lost. Your T10 structures pass is verified, loaded, and the
gate is now ZERO (14 tables, 291 rows). Act from THIS FILE and from disk — not from chat.

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Python:    C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## HARD CONSTRAINT
Edit ONLY `research/26-t1-doctypes-draft.csv` and `research/26-notes.md`. Nothing under
`data/`, no loader. The Coverage analyst reloads afterwards; the Packaging analyst is
rebuilding the ZIP right now.

## The problem, measured
The resolver can now ABSTAIN on ambiguous queries. Two of the three ambiguous test queries
work: "make me a flyer" and "fais-moi un cv" both abstain and offer candidates. The German
one, D3 "erstelle eine praesentation", still resolves CONFIDENTLY to
`slide-deck-projection`, which is wrong — it is ambiguous between projection, document and
handout.
It is NOT fixable by tuning: D3's margin ratio (0.315) is LARGER than D1's (0.249), and D1
"erstelle einen tabellarischen lebenslauf" must keep resolving. The cause is in YOUR file.
`slide-deck-projection`'s Keywords cell contains the word presentation FOUR times
(term frequency 4) where its siblings have 2 and 1:
  - `presentation` (English)
  - `praesentation` (accented form) — appears TWICE, an exact duplicate
  - `fais-moi une praesentation` (French phrase)
  - `erstelle eine praesentation` (German phrase)
Its siblings: `slide-deck-document` has 2 occurrences, `slide-deck-handout` has 1.

## ONE deliverable: the asymmetry removed without losing language coverage.
1. Remove the EXACT DUPLICATE bare accented token — it appears twice in the same cell and
   one copy is pure term-frequency inflation with no retrieval value.
2. Then judge the remaining imbalance. THE GUARD, ruled by the lead: the German and French
   forms must STAY, or the German and French queries lose their match. Fix this by removing
   duplicate repeats, or by EQUALISING the siblings' multilingual coverage (giving
   `slide-deck-document` and `slide-deck-handout` the German and French forms they lack is
   as legitimate as trimming projection, and is probably the better answer — those rows are
   thin in French and German, which is a real coverage gap in its own right).
3. While you are in there: `erstelle eine praesentation` currently uses the FRENCH accented
   form inside a German phrase. German is "Praesentation" with the German umlaut. Check the
   actual bytes and fix it if it is wrong — a German user's phrase should match the German
   spelling. Note it in 26-notes.md either way.

## You cannot verify the acceptance test yourself
The change only takes effect after Coverage reloads `data/base`, which happens after you.
So: verify the FILE (below), state clearly in your report what you changed and why, and the
acceptance test — D3 abstains AND the German deck query still surfaces the deck family as
candidates — is run by Coverage after the reload. Do not run the loader to test it.

## VERIFY by script
- `research/26-t1-doctypes-draft.csv` parses clean at 11 columns x 34 rows.
- Count occurrences of the presentation stem per deck row and report the before/after
  numbers for all three rows.
- No Keywords cell has an exact duplicate token any more (check all 34 rows, not just decks
  — if others have duplicates, report them but do not fix them in this brief).

## REPORT
Max 8 lines to the Workflow Orchestrator, slot 01a080c5-2001-78b3-bbbe-afaae15edafa:
the before/after term counts per deck row, what you removed versus what you added, the
German-spelling finding, and any other duplicate-token rows you spotted.
If you approach ~10 minutes, checkpoint to research/handover-ddr.md and stop.
