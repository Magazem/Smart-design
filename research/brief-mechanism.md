# BRIEF — Mechanism — v0.2: make the degradation message honest again

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT change any threshold, weight or constant in the resolver. If you find
yourself wanting to, stop and tell me instead — that is a standing rule in this project.

## Why
Every one of the 17 structure rows now carries a Section Order (commit aec56f4, gate zero at
414 rows). The "no section-order guidance" path and the comment that justifies it were both
written when 15 of 17 rows were empty by ruling. The behaviour is still right; the reasoning
attached to it is now false, and there is no longer any row in shipping data that exercises it.

## The code
skill/document-design-intelligence/scripts/resolve.py, `_field_value`, docstring at line 528:

    most structure rows ship empty on purpose (headings.csv only holds CV
    sections; the rest is deferred)

Both halves of that parenthesis are now untrue.

## Deliverable (ONE)
1. Rewrite that docstring to state what is actually true: an empty group-FK list column is
   expected data rather than a broken reference, and the function names the gap instead of
   printing nothing. Drop the claim about CV sections and deferral. Keep the ruling citation.
2. Keep the BEHAVIOUR unchanged. The message must still fire when a group-FK list column is
   genuinely empty. Do not delete the path because nothing currently triggers it — it is the
   safety net for the next table that ships a blank.
3. ADD A TEST that proves the path still works, using a SYNTHETIC row with an empty Section
   Order. No row in data/base has one any more, so the test must construct its own fixture
   rather than rely on shipping data. Follow the existing fixture pattern under
   scripts/tests/fixtures/. Assert the exact message text.
4. Add a second test asserting that a POPULATED Section Order returns the real value and NOT
   the guidance message. That is the regression the first test cannot catch alone.

## Then re-run the 12-query set
research/35-resolve-live.md holds a 12-query table (E1-E4, F1-F4, D1-D4) with the verdicts from
before the section data existed. Every query that reached the FK walk ended in REFUSED PATH,
because structures had no section orders. That should now be gone.

Re-run all 12 exactly as written there and record the results in research/43-resolve-live-v2.md
as the same table shape, with a column for what changed since. State plainly:
- how many now produce a full RESOLVED payload end to end;
- whether E3 ("make me a flyer") and D3 ("erstelle eine präsentation") still resolve confidently
  instead of abstaining. Both were known FAILs. Do NOT fix them — they are backlog, and the
  fix is length normalisation which needs real query data. Just report the current state.
- F1's brand pass is still untestable without a brand overlay. Say so rather than inventing a
  verdict.

## Verify
1. `python3 -m pytest scripts -q` from skill/document-design-intelligence. Baseline is 138
   passed plus 8 subtests; expect 140 with your two new tests.
2. `python3 scripts/validate_data.py data/base` — still `OK: validated 14 table(s), 414 row(s)`.
3. No constant in resolve.py changed. Confirm with a diff and say so explicitly.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the new docstring,
the two test names, the 12-query tally with the E3/D3 status, and the confirmation from verify 3.
