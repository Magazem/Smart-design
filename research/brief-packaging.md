# BRIEF — Packaging — rebuild after candidates G and H

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push. Do not edit VERSION.

## Why
Commit f69c6a2 applied the user-approved description package: the missing document nouns, and a
rewritten deferral sentence. The archive is stale.

## Deliverable (ONE)
Run scripts/build_zip.py, then verify ALL of:
1. SKILL.md member first bytes are exactly `---\n`; exactly ONE version stamp, after the
   frontmatter.
2. Zero members carry a CR byte.
3. The description in the SKILL.md member measures exactly **964** characters and CONTAINS the
   phrase "the user names it". It must NOT contain "When a specific file format" — that is the
   old sentence H replaced.
4. It still contains "appearance fixes" (candidate F, applied earlier) and the nouns "invoice",
   "memo", "one-pager", "facture", "Rechnung", "devis".
5. All 14 data/base CSVs present. headings member 204 data rows. structures member 17 rows with
   ZERO empty Section Order cells.
6. The doctypes member's letter-formal row carries a bare `letter` token in Keywords.
7. NO member ends in .docx. No data/brand/<slug>/ members and no active.json;
   data/brand/README.md expected.
8. The activation.md member's fenced "as shipped" block equals the description exactly.
9. `python3 -m pytest scripts -q` — baseline 146 passed plus 8 subtests.
10. Report archive size, member count, schema-manifest.json md5. Note: the md5 has TWO correct
    values, the CRLF working copy and the LF form the ZIP carries. Report what you measure; I
    will reconcile.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: each check with
its actual value.
