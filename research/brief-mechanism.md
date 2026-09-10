# BRIEF — Mechanism — RULING K step 3: page flow must reach the renderer (HOLD)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DISPATCHED. The constraints are loaded and committed as 0076fff. Proceed.

## Why
Page-flow rules in the library are useless if the render handoff never mentions them. The
`handoff` command prints resolved fonts, colours, spacing, page format and constraints for the
built-in docx and pptx skills to act on. Unless the page-flow constraints arrive there in words
docx understands, a heading will still land alone at the foot of a page.

## Deliverable (ONE)
Make the render-handoff block carry page flow.
1. Find where `handoff` builds its block — scripts/ddi.py and whatever it calls.
2. Emit the page-flow constraints in terms the docx skill can act on directly:
   keepNext, keepLines, widowControl, cantSplit, tblHeader.
   Map each loaded constraint to its property rather than inventing a parallel vocabulary.
3. STATE PLAINLY IN THE OUTPUT THAT PPTX HAS NO EQUIVALENT. Slides do not paginate, so these
   properties do not apply. Say it in the block rather than silently omitting it — a silent
   omission reads as an oversight to anyone comparing the two paths.
4. Add a test that the docx handoff block contains the properties and the pptx one carries the
   not-applicable statement.

## Constraints
- Do NOT change any threshold, weight or constant in the resolver. If you want to, stop and tell
  me — that is a standing rule here.
- Do NOT edit SKILL.md's frontmatter description. It is under test.
- If the body needs a sentence pointing at this, keep it to one line; the file is a router.

## Verify
1. Run `handoff` on a resolved report and paste the block, so the page-flow lines are visible.
2. Run it for pptx and paste the not-applicable statement.
3. `python3 -m pytest scripts -q` — baseline will be whatever step 2 left it at; report the
   number and your delta.
4. `python3 scripts/validate_data.py data/base` unchanged.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the two blocks,
the test names, and the tally.

## The five rows are already in data/base -- here they are
Loaded 2026-09-10, gate 419 rows. Every Parameter already NAMES the OOXML property, so you are
mapping, not inventing:
  report-heading-keep-with-next        docx_property=keepNext;applies_to_block=heading;binds_to=body-paragraph
  report-widow-orphan-control          docx_property=widowControl;min_lines_together=2
  report-table-row-no-split            docx_property=cantSplit;applies_to_block=table-row
  report-table-header-repeat           docx_property=tblHeader;applies_to_block=table-header-row
  report-figure-caption-keep-together  docx_property=keepNext;applies_to_block=figure;binds_to=caption-block
All five are Set Key , Applies To , Severity .
Two carry an empty Element Scope BY DESIGN -- their block type lives in Parameter. Do not treat
that as missing data.

READ THE PARAMETER, do not hardcode a second copy of this mapping in the handoff code. If the
Parameter says , emit keepNext. A hardcoded parallel table is how the
two copies drift apart.

THESE RULES ARE CONVENTION, NOT SOURCED. DDR checked and could not attribute them to any
authority this library cites. If the handoff block labels provenance anywhere, label them
honestly.
