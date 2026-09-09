# BRIEF — Packaging — Rebuild the ZIP after ruling E (third rebuild)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push.

## Why
Commit 6f98d84 gave activation prompts 6, 8, 10, 11 and 13 inline input. That file ships in
the ZIP, so the archive is stale again.

## Deliverable (ONE)
Run scripts/build_zip.py, then verify:
1. SKILL.md member first bytes are exactly `---\n`.
2. Zero members carry a CR byte.
3. Member count, and schema-manifest.json md5 == 57e886aa8a68665c763904c391ac3836 (LF form).
4. Exactly ONE `<!-- version: ... -->` line, after the frontmatter's closing `---`.
5. No data/brand/<slug>/ members and no active.json; data/brand/README.md expected.
6. NEW: the activation.md member contains "Bramwell Logistics" (prompt 11's new inline notes)
   and "find_duplicates" (prompt 8's function). Both must be present.
7. Still true from before: the member contains "Applies sourced layout", "823-character",
   "fiche produit", and does NOT contain "Applies validated layout" or "825 characters".
8. `python3 -m pytest scripts -q` from skill/document-design-intelligence.
9. Report whether the build modified the source SKILL.md. It should not.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: archive path and
size, each check with its actual value, and the test tally.
