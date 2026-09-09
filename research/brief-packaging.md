# BRIEF — Packaging — Rebuild the ZIP after ruling F (fourth rebuild)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push.

## Why
Commit c5e2101 rewrote activation prompt 4 to describe a document's APPEARANCE instead of
pasting AI-sounding prose, and added a scope note. activation.md ships in the ZIP.

## Deliverable (ONE)
Run scripts/build_zip.py, then verify:
1. SKILL.md member first bytes are exactly `---\n`.
2. Zero members carry a CR byte.
3. Member count, and schema-manifest.json md5 == 57e886aa8a68665c763904c391ac3836 (LF form).
4. Exactly ONE `<!-- version: ... -->` line, after the frontmatter's closing `---`.
5. No data/brand/<slug>/ members and no active.json; data/brand/README.md expected.
6. NEW: the activation.md member contains "clip-art chart" (new prompt 4) and "not how its
   prose reads" (the scope note), and does NOT contain "fast-paced business landscape" (the
   deleted AI paragraph).
7. Still true: the member contains "Bramwell Logistics", "find_duplicates", "fiche produit",
   "Applies sourced layout", "823-character"; and NOT "Applies validated layout" or
   "825 characters".
8. The SKILL.md member's description still measures 823 characters. Candidate F is drafted but
   NOT applied — if you measure anything other than 823, stop and tell me.
9. `python3 -m pytest scripts -q` from skill/document-design-intelligence.
10. Report whether the build modified the source SKILL.md. It should not.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: archive path and
size, each check with its actual value, and the test tally.
