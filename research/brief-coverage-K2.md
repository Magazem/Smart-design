# BRIEF — Coverage — RULING K step 2: load the page-flow constraints (HOLD)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DISPATCHED. DDR step 1 is committed as 21de2b3 and verified. Proceed.

## Why
DDR has authored page-flow rows into research/16-t9-constraints-draft.csv. Only
research/load-base.py may write data/base.

## A loader change you will almost certainly need — I checked this before writing the brief
T9's `Element Scope` is NOT in either draft. The loader derives it, and the derivation is
hardcoded to a SINGLE key (load-base.py around line 236):
    r["Element Scope"] = ""
    if k == "report-measure-cpl":
        r["Element Scope"] = "body-paragraph"
So every new row lands with an EMPTY Element Scope unless you extend that logic. Page-flow rules
need real scopes — `body-paragraph` for widows and orphans, `table-cell` for table splitting,
`caption-block` for figure-and-caption. All three are already in the enum.

DDR HAS ALREADY TOLD YOU WHICH ROWS NEED WHAT, so do not re-derive it:
- `report-widow-orphan-control` needs `body-paragraph`.
- `report-table-row-no-split` and `report-table-header-repeat` need `table-cell`.
- `report-heading-keep-with-next` and `report-figure-caption-keep-together` stay scope-EMPTY
  BY DESIGN. Their block type is carried in Parameter via `applies_to_block` and `binds_to`,
  following the photocopy-safe precedent of putting roles in Parameter. That is NOT a gap and
  must not be "fixed".
Its full reasoning is in research/45-notes.md; read it before changing anything.

Extend the derivation to carry the scopes those rows need. Prefer a data-driven mapping over
another hardcoded key comparison; a chain of `if k ==` lines is how this became a special case
in the first place. If DDR's notes say the rows cannot get their scope, say so and stop.

## Deliverable (ONE)
Load, to gate zero.
1. Extend the Element Scope derivation as above.
2. Run research/load-base.py.
3. Update the T9 CHANGES string if it states a row count that your load changes.

## Verify — paste actual output
1. `python3 scripts/validate_data.py data/base` — exit 0. Report the table and ROW COUNT; it was
   414, and constraints grows by however many rows DDR added.
2. `git diff --stat skill/document-design-intelligence/data/` — expect constraints.csv only. If
   any OTHER table moved, that is a finding: report it, do not tidy it.
3. Every new row has the Element Scope DDR intended. Print the new rows with their scopes.
4. `python3 -m pytest scripts -q` — baseline 148 passed plus 8 subtests.
5. The loader is idempotent: run it twice and confirm the second run changes nothing.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the gate line
with its row count, the diff stat, the new rows with scopes, and the idempotency result.
