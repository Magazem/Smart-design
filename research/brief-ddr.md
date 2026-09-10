# BRIEF — DDR — RULING K step 1: page-flow constraints (HOLD until dispatched)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. research/ drafts only — never write under data/.
DO NOT START until the orchestrator dispatches this. If you are reading it without a task, stop.

## Why
A user saw a section heading land at the bottom of a page with its body on the next. I grepped
data/, scripts/, SKILL.md and references/ for keep-with-next, keepNext, widow, orphan,
page-break, cantSplit and tblHeader: ZERO HITS. The library has nothing to say about page flow
at all. Every typographic rule we ship is about type, colour, measure and margins; nothing keeps
a heading with its text.

## The table is BOUND: T9 constraints. Here is why, so you can challenge it if you disagree
constraints.csv is `constraint_key, Set Key, Applies To, Check, Element Scope, Parameter,
Threshold, Severity` — a rule, what it applies to, what to check, and how hard it fails. That is
exactly the shape of "a heading keeps with its first paragraph" and "no fewer than two lines
together". The Element Scope enum ALREADY contains `body-paragraph`, `table-cell` and
`caption-block`, which are three of the four scopes these rules need. There is already a
`report-typography` Set Key. doc-reasoning is per-family style bias, which is the wrong shape.
If you think another table fits better, say so before authoring rather than after.

## The loader shape — get this right or the load fails
T9 loads from TWO drafts, `research/16-t9-constraints-draft.csv` and
`research/21-t9-print-constraints-draft.csv`. Both have SEVEN columns, NOT the eight in
data/base:
    constraint_key,Set Key,Applies To,Check,Parameter,Threshold,Severity
`Element Scope` is NOT in the drafts. The loader derives it (load-base.py around line 236).
Read that code before you author, and say in your notes how your rows will get the Element Scope
they need — if the derivation cannot produce it, that is a finding to report, not to work around.

APPEND your rows to research/16-t9-constraints-draft.csv. Do not create a new file; the loader
reads only those two.

## Deliverable (ONE)
The page-flow rows, plus research/45-notes.md.

Cover these norms:
- a heading keeps with its first paragraph (keep-with-next)
- no widows or orphans; a minimum of two lines kept together
- a short table never splits; a long table splits only with its header row repeated
- a figure keeps with its caption

SOURCE THEM. Bringhurst, Butterick, DIN 5008, or whichever authority this library already cites
— check what the existing rationale files cite before reaching for a new one. Mark every row
sourced or convention, as you have done throughout. An invented threshold presented as a norm is
worse than no row.

Think about `Applies To`: page flow is meaningless for a poster or a slide, and central to a
report. Scope the rows honestly rather than applying them everywhere. Say which families you
excluded and why.

## Verify before you report
1. Your rows parse with csv.DictReader and match the SEVEN-column draft header exactly.
2. No constraint_key collides with the 42 existing rows or the other draft.
3. Every Severity is `fail` or `warn` — the enum allows nothing else.
4. If any row needs an Element Scope, confirm the loader's derivation will assign it, quoting
   the code you relied on.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the rows added,
their sources, which families you excluded, and your answer on Element Scope.
