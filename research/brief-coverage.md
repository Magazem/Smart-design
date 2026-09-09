# BRIEF — Coverage — v0.2 cleanup 1 of 3: duplicate keyword sweep across T1

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git.

## Why
`brochure-flyer-a4` is known to carry a duplicated token in its Keywords cell. It was found by
eye, which means the same defect may sit in other rows unseen. Duplicated tokens skew BM25 term
frequency and quietly bias retrieval toward the row with the accidental repeat.

## Scope
skill/document-design-intelligence/data/base/doctypes.csv — the `Keywords` column, ALL rows.
Also check the same column in the research draft it was loaded from,
research/26-t1-doctypes-draft.csv, since only research/load-base.py may write data/base and a
fix has to survive a reload.

## Deliverable (ONE)
1. Find every row whose Keywords cell repeats a token. Report them all, not just the first.
2. Fix them in research/26-t1-doctypes-draft.csv by removing the duplicate occurrence, keeping
   the first. Do not reword, do not add tokens, do not rebalance anything — this is a
   de-duplication, not a retrieval tune. If removing a duplicate would leave a row with fewer
   distinct tokens than its siblings, say so and leave it; do not compensate.
3. Add a validator rule to skill/document-design-intelligence/scripts/validate_data.py that
   catches this class permanently: a list column whose cell contains the same token twice is a
   tier 2 problem, tagged with the offending row's own key. `list_columns` is already in the
   spec and `_validate_rows` already iterates it — follow the existing `_add(...)` pattern so
   the message names the column and the repeated token.
4. Add a test for the new rule alongside the existing validator tests.

Do NOT reload data/base in this brief. That is a separate step and a separate brief.

## Verify before you report
1. Your new rule fires on a deliberately duplicated fixture value and does NOT fire on the
   current clean data once you have fixed the drafts.
2. Run the full suite from skill/document-design-intelligence:
   `python3 -m pytest scripts -q`. The baseline is 133 passed plus 8 subtests. Report the new
   number; it should be 133 plus your new test, with nothing broken.
3. Run `python3 scripts/validate_data.py data/base` and report the result. It is expected to
   still be clean, because data/base is untouched and the drafts are what you fixed. If the new
   rule fires against the CURRENT data/base, that is a real finding — report it and do not
   silence the rule.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: every row with a
duplicate and the repeated token, what you changed in the draft, the rule's message text, and
both verification outputs.
