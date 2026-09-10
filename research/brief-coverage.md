# BRIEF — Coverage — apply candidate L (HOLD until the lead says "user approved")

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT START without the go-ahead. If you are reading this without it, stop
and say so.

## What is being applied
Candidate L, from research/38-description-candidate.md. It is a PURE REORDER: the priority
claim moves from seventh position to FIRST. I rebuilt it from the live description and diffed at
token level — the only change across all 972 characters is `above` becoming `below`.

New first sentence:
  Creating any document type below is still this skill's job even as Word or PowerPoint; defer
  to that format's own skill only when the user names it for a plain conversion or edit with no
  design ask.

Length stays 972. If you measure anything else, STOP and report.

## THE TEST CHANGE IS PART OF THIS, NOT A FOLLOW-UP
Mechanism proved this by running the real test, and it is the reason L cannot ship alone:
- Moving that sentence to the front puts NEGATIVE_SCOPE_MARKER at INDEX 0. The positive region
  collapses to an empty string and ALL THIRTY doctypes read as unreachable.
- Renaming the marker alone does NOT fix it. It leaks "PowerPoint" into the positive region and
  falsely credits slide-deck-projection — the exact bug that test exists to catch.
The fix is a genuine two-marker change to scripts/tests/test_description_coverage.py:
NEGATIVE_HEAD_MARKER plus NEGATIVE_SCOPE_MARKER. Mechanism wrote and verified it; its working
version is in research/38-description-candidate.md under Candidate L, section L.2, and
research/38-verify-candidate-l.py reproduces all four scenarios.

Take that fix, do not reinvent it. Keep the hard AssertionError guard on BOTH markers — a marker
that silently fails to match is how this test nearly went quiet twice.

## Also coupled
references/activation.md's fenced "as shipped" block: copy the new description in verbatim, one
line. test_description_mirror.py enforces it, so a miss fails the suite rather than drifting.
The "972" prose figures do NOT change — the length is identical.

## Verify — paste actual output
1. Description measures exactly 972 and STARTS with "Creating any document type below".
2. Token-level diff against the previous description: the ONLY difference is above/below.
3. `python3 -m pytest scripts/tests/test_description_coverage.py -q` — 6 passed, run on its own.
4. `python3 -m pytest scripts/tests/test_description_mirror.py -q` — 2 passed, on its own.
5. NEGATIVE CONTROL, and I will repeat it: with L applied and your two-marker fix in place,
   confirm the coverage test still FAILS when a noun is removed from the description. A test
   that passes because its region is wrong is exactly what we are guarding against. Paste it.
6. Full suite: baseline 148 passed plus 8 subtests.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the measured
length, checks 2 and 5 verbatim, and the four test results.
