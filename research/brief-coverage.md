# BRIEF — Coverage — RULING N step 2: load the heading rows and pin the TOC section

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git.

## Why
DDR authored five type-scale heading rows (committed 871dc3a). Only research/load-base.py may
write data/base. Until it runs, the docx handoff still prints nothing for TOC heading levels on
report-long-toc — the doctype named for its table of contents.

The five new rows in research/30-t6-type-scales-draft.csv, now 27 rows:
    report-print-print-h3   12pt / 1.20
    report-print-print-h2   16pt / 1.20
    report-print-print-h1   24pt / 1.20
    cv-print-print-h2       16pt / 1.20
    cv-print-print-h1       24pt / 1.20
All five DERIVED from print-office-generic at the same 11pt body size, cited as derivations in
research/46-notes.md. cv-print deliberately has NO h3; a CV's third tier is weight contrast, not
a size. Do not add one.

## Deliverable (ONE)
1. Run research/load-base.py.
2. Extend the end-to-end handoff test you wrote (TestHandoffEndToEndOnRealData in test_ddi.py)
   so TOC HEADING LEVELS must be NON-EMPTY for report-long-toc. That section is the reason this
   ruling exists, and right now nothing would notice if it went blank again.
   Assert the heading levels actually carry the sizes, not merely that the section has text.

## Verify — paste actual output
1. `python3 scripts/validate_data.py data/base` — exit 0. Report the row count; it was 419 and
   type-scales grows by five.
2. `git diff --stat skill/document-design-intelligence/data/` — expect type-scales.csv ONLY.
   Anything else is a finding: report it, do not tidy it.
3. The docx handoff for report-long-toc, in full. TOC heading levels must now show real values.
4. The docx handoff for cv-generic — confirm it shows h1 and h2 and NOT an h3.
5. NEGATIVE CONTROL, and I will repeat it: with your extended test in place, remove the h1 row
   from data/base/type-scales.csv, confirm the test FAILS naming the TOC section, then restore.
   A test not seen failing is not known to work.
6. `python3 -m pytest scripts -q` — baseline 158 passed plus 30 subtests; report your delta.
7. The loader is idempotent: run it twice, confirm the second run changes nothing.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the gate line
with its count, the diff stat, both handoff TOC sections, check 5 verbatim, and the tally.
