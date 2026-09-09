# BRIEF — Packaging — Rebuild the distribution ZIP after the activation-prompt change

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe (the repo venv is broken)
DO NOT touch git. The orchestrator commits. Do not tag. Do not push.

## Why
Prompts 2-5 in skill/document-design-intelligence/references/activation.md were rewritten so
each carries its input inline (committed as 8699c9b). That file ships inside the ZIP, so the
archive the user has is stale. The user re-uploads and re-runs prompts 2-5, then 6-13.

## Deliverable (ONE)
Rebuild the archive with scripts/build_zip.py, then VERIFY it. Nothing else changes.

## Verification — all of it, no shortcuts
A previous release was rejected by claude.ai because the ZIP was checked for membership and
never for validity. Check the bytes:
1. The first bytes of the SKILL.md member are exactly `---\n`. Print them.
2. Zero members contain a CR byte. Print the count and the offending names if any.
3. Member count, and the data/schema-manifest.json md5. Two md5s are legitimate and documented
   in RESUME.md under "TWO MANIFEST HASHES": 731d874ff6052d8c3809a3d44a9d4196 is the CRLF
   working copy, 57e886aa8a68665c763904c391ac3836 is the LF form the ZIP must carry. Do not
   "fix" either. The ZIP must show the LF one.
4. Exactly ONE `<!-- version: ... -->` line in the SKILL.md member, and it sits AFTER the
   frontmatter's closing `---`.
5. No user brand data: no data/brand/<slug>/ members and no active.json. data/brand/README.md
   is expected and fine.
6. The activation.md member contains the new prompt 2 text (grep for the French fiche produit
   line) — proof the rebuild actually picked up the change.
7. Run the test suite and report the counts.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the archive
path, the seven verification results with their actual numbers, and the test tally.
