# BRIEF — Packaging — rebuild (HOLD until the orchestrator says go)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push. Do not edit VERSION.
DO NOT START without the go-ahead — the description change this depends on may not be applied.

## Why
The archive is four commits stale. This rebuild bundles:
- d3219d0 activation prompt 11's criteria, changed under candidate H
- 706da0d SKILL.md body: plain-text answers keep the section order
- 5ac9d4a the "lettre" noun and the description mirror tests
- and candidate J, IF it has been applied — check the description length to find out.

## Deliverable (ONE)
Run scripts/build_zip.py, then verify:
1. SKILL.md member first bytes exactly `---\n`; exactly ONE version stamp, after the frontmatter.
2. Zero members carry a CR byte.
3. **The description length. Report what you MEASURE — do not assume.** It is 972 if J was not
   applied, 986 if it was. Say which, and say whether the member contains "whether the answer is
   a chat reply or a file".
4. It still contains "lettre", "appearance fixes", "the user names it", and the nouns invoice,
   memo, one-pager, facture, Rechnung, devis.
5. The SKILL.md member's BODY contains "The output format never changes this order or these
   headings" — that is the plain-text fix, and it is the one thing in this bundle a user can see
   fail.
6. The activation.md member: its fenced "as shipped" block equals the member's description BYTE
   for byte and is on one line. Prompt 11's Pass line says this skill firing is correct.
7. All 14 data/base CSVs present; headings member 204 rows; structures member 17 rows with zero
   empty Section Order cells.
8. No .docx members. No data/brand/<slug>/ and no active.json; data/brand/README.md expected.
9. `python3 -m pytest scripts -q` — baseline 148 passed plus 8 subtests.
10. Archive size, member count, schema-manifest.json md5. The md5 has two correct values, the
    CRLF working copy and the LF form in the archive; report what you measure.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: each check with
its actual value, and state plainly whether J is in the archive.
