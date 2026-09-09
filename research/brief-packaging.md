# BRIEF — Packaging — FINAL rebuild: candidate F applied

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push.

## Why
Commit 6b634fa applied candidate F to the SKILL.md description (approved by the user) and
commit 225f1a0 turned prompt 4 into an attachment test. This is the archive the user uploads
before the tag decision.

## Deliverable (ONE)
Run scripts/build_zip.py, then verify:
1. SKILL.md member first bytes are exactly `---\n`.
2. Zero members carry a CR byte.
3. Member count, and schema-manifest.json md5 == 57e886aa8a68665c763904c391ac3836.
4. Exactly ONE `<!-- version: ... -->` line, after the frontmatter's closing `---`.
5. No data/brand/<slug>/ members and no active.json; data/brand/README.md expected.
6. CHANGED THIS ROUND: the SKILL.md member's description measures **831** characters and
   CONTAINS "appearance fixes" and "make it look professional". It must NOT contain
   "quality fixes: looks like AI". This is the inverse of last round's assertion — F is now
   applied on purpose.
7. NEW: NO member anywhere in the archive ends in .docx. Print the count and any names.
   Two .docx files exist in the repo and neither may ship: research/fixtures/ is outside the
   build root, and scripts/tests/fixtures/sample.docx is excluded because build_zip skips any
   directory named "tests". Verify, do not assume.
8. The activation.md member contains "badly-formatted-report.docx" (prompt 4's attach line),
   "Sara Lindqvist", "Bramwell Logistics", "find_duplicates", "fiche produit", "831"; and does
   NOT contain "823", "clip-art chart", "fast-paced business landscape" or "Applies validated
   layout".
9. `python3 -m pytest scripts -q` from skill/document-design-intelligence. If any test asserts
   the old description length, report the failure — do not edit the test.
10. Report whether the build modified the source SKILL.md.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: archive path and
size, each check with its actual value, and the test tally.
