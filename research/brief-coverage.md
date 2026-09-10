# BRIEF — Coverage — apply candidate J (HOLD until the lead says "user approved")

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT START without the go-ahead. If you are reading this without it, stop
and say so.

## What is being applied
Candidate J, from research/38-description-candidate.md. It replaces the LEAD sentence and trims
the trigger examples. Everything else in the description stays.

Live description today: 972. After J: **986**. I measured that myself against disk; do not
trust the number, reproduce it.

What J changes, and nothing else:
- The lead "Creates and fixes print/office documents:" becomes the use-when wording.
- The trigger examples drop from seven to three, one per language.
- KEPT, verify each survives: "sourced", the UI/UX boundary sentence, "lettre", candidate H's
  deferral sentence (must appear EXACTLY ONCE and byte-intact), and every document noun. Note
  "report" leaves only as part of the deleted example "format this report" — the noun "reports"
  must remain in the list.

## Deliverable (ONE)
1. Apply J to SKILL.md's frontmatter description. Result MUST measure exactly 986. If it does
   not, STOP and report. Do not adjust wording to reach the number.
2. The coupled edits, which now have a test behind them:
   - references/activation.md's fenced "as shipped" block, updated to match BYTE for byte, on
     ONE line.
   - "972" becomes 986 on the three prose lines that carry it. Leave the historical 667 alone.

## Verify — paste actual output
1. Description measures exactly 986 and contains "whether the answer is a chat reply or a file".
2. H's sentence: `description.count(<H sentence>) == 1`.
3. `python3 -m pytest scripts/tests/test_description_mirror.py -q` — both tests green. These are
   the tests you wrote; they are now the ones protecting this edit.
4. `python3 -m pytest scripts/tests/test_description_coverage.py -q` — green on its own, not as
   part of the suite.
5. No "972" survives in activation.md.
6. Full suite: baseline 148 passed plus 8 subtests.
7. Confirm no document noun was lost: diff the noun list before and after and paste it.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the measured
length, checks 2, 5 and 7 verbatim, and the two test results.
