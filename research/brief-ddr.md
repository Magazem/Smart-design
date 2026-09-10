# BRIEF — DDR — RULING N step 1: the missing heading rows in type-scales

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. research/ drafts only — never write under data/.

## Why, and the diagnosis is already done
The docx handoff prints "(not present in this resolution)" for TOC HEADING LEVELS on
report-long-toc — a doctype whose name is "long-form with table of contents". Ruling M fixed the
other empty sections, but not this one, because THIS ONE IS A DATA GAP, not a plumbing gap.

I checked research/30-t6-type-scales-draft.csv myself. It is not a loader drop and not a filter.
The rows were never authored:

    ens-print             label 8.5/1.20  caption 9/1.20  body 11/1.35  lead 12/1.30
                          h3 16/1.15  h1 24/1.10  legal 8.5/1.20
    print-office-generic  label 8.5/1.20  caption 8.5/1.20  body 11/1.35
                          h3 12/1.20  h2 16/1.20  h1 24/1.20
    cv-print              body 11/1.35        <- ONLY ONE ROW
    report-print          body 11/1.35        <- ONLY ONE ROW

Two scale keys carry full heading sets. The two that a report and a CV actually use carry a body
row and nothing else.

## Deliverable (ONE)
Author the missing rows into research/30-t6-type-scales-draft.csv, plus research/46-notes.md.

Columns, exactly as the draft has them:
    scale_row_key,scale_key,Medium,Role,Size pt,Leading Ratio
`scale_row_key` follows the existing pattern `<scale_key>-<medium>-<role>`, e.g.
`report-print-print-h1`.

For report-print: h1, h2, h3 at minimum. Add caption or label ONLY if a report genuinely needs
them; do not pad.
For cv-print: h1, h2, h3 — a CV has a name and section headings, so it needs a hierarchy even if
it is shallower than a report's. Judge honestly whether a CV needs h3 at all; if it does not,
author two and say why.

## SOURCING — the rule that matters here
1. If the library has a source, cite it.
2. If not, you MAY DERIVE from `print-office-generic`, which already carries a sourced set at the
   same body size of 11pt, by keeping the same ratio. If you do, CITE THE DERIVATION explicitly —
   "derived from print-office-generic at the same body size" — rather than presenting the number
   as sourced in its own right. The lead has approved this route.
3. If neither, tag CONVENTION plainly, as you did for the page-flow rules.
Do NOT invent a number and leave its basis unstated. That distinction is the thing this library
is actually for.

Say in the notes whether a report's heading scale should differ from a generic office document's,
and why. If your answer is that it should not, then deriving is not a shortcut but the correct
answer, and say so.

## Verify before you report
1. The new rows parse with csv.DictReader and match the six-column header exactly.
2. No `scale_row_key` collides with the existing 22 rows.
3. Every `Medium` value already appears in the draft — do not introduce a new medium.
4. Leading ratios are plausible against the existing pattern: tighter as size grows.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the rows added
with sizes and ratios, sourced versus derived versus convention for each, and your answer on
whether a report's heading scale should differ from a generic one.
