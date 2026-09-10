# BRIEF — Packaging — rebuild with L and the page-flow work (HOLD)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push. Do not edit VERSION.
DISPATCHED. Candidate L IS applied (f23fb03) and ruling M has landed (5a98f85). Proceed.

## What this bundles
- Candidate L, the description reorder (applied)
- the five page-flow constraints, loaded at gate 419
- K step 3, the page-flow render handoff
- ruling M, the docx handoff block fix and its two new test files

## Deliverable (ONE)
Run scripts/build_zip.py, then verify:
1. SKILL.md member first bytes exactly `---\n`; exactly ONE version stamp, after the frontmatter.
2. Zero members carry a CR byte.
3. The description MEASURES 972 either way — L is a pure reorder and does not change the length.
   So do NOT use length to tell whether L is in: check whether the description STARTS WITH
   "Creating any document type below". Report which you found.
4. It still contains "lettre", "appearance fixes", "the user names it", and the nouns invoice,
   memo, one-pager, facture, Rechnung, devis.
5a. The manifest member must declare display_columns on SIX tables. That is what stops the docx
    handoff from shipping empty; confirm it is in the ARCHIVE, not just on disk.
    (An earlier version of this check also demanded test_schema_manifest.py be present in the
    archive. That was MY ERROR -- build_zip excludes every "tests" directory by design and always
    has. Tests are not shipped and must not be.)
5. The constraints member has 47 rows and contains all five page-flow keys:
   report-heading-keep-with-next, report-widow-orphan-control, report-table-row-no-split,
   report-table-header-repeat, report-figure-caption-keep-together.
6. The SKILL.md body still contains "The output format never changes this order or these
   headings" — the plain-text fix, proven in behaviour and not to be lost in a rebuild.
7. activation.md member: fenced "as shipped" block equals the member's description BYTE for
   byte, on one line.
8. All 14 data/base CSVs present; headings 204 rows; structures 17 rows, zero empty Section
   Order cells.
9. No .docx members. No data/brand/<slug>/ and no active.json; data/brand/README.md expected.
10. `python3 -m pytest scripts -q` — baseline is now 158 passed plus 30 subtests.
11. Archive size, member count, schema-manifest.json md5. Two md5 values are correct, the CRLF
    working copy and the LF form in the archive; report what you measure.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: each check with
its actual value, and state plainly whether L is in the archive.
