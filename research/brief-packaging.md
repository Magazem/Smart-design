# BRIEF — Packaging — Rebuild the ZIP once more (activation.md changed again)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push. Do not edit any file except by running the build.

## Why
references/activation.md changed again after your last rebuild (commit 785833d: stale
description-length quotes corrected to 823, and the quoted description block updated from
"validated" to "sourced"). That file ships inside the ZIP, so the archive is stale by three
lines. The 13 prompts themselves are unchanged.

## Deliverable (ONE)
Run scripts/build_zip.py and verify the result. Same seven checks as last time:
1. SKILL.md member first bytes are exactly `---\n`.
2. Zero members carry a CR byte.
3. Member count, and schema-manifest.json md5 == 57e886aa8a68665c763904c391ac3836 (the LF
   form; the other documented hash is the CRLF working copy — do not "fix" either).
4. Exactly ONE `<!-- version: ... -->` line, sitting after the frontmatter's closing `---`.
5. No data/brand/<slug>/ members and no active.json. data/brand/README.md is expected.
6. NEW this round: the activation.md member says "Applies sourced layout" and "823-character",
   and does NOT contain "Applies validated layout" or "825 characters". Grep for all four.
7. Run the test suite from skill/document-design-intelligence: `python3 -m pytest scripts -q`.

Note: the build rewrites the SOURCE SKILL.md as a side effect of stamping. That is expected
and the source has already converged, so SKILL.md should come back unchanged. If it does
change, say so — that is a finding.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: archive path and
size, the seven results with actual values, and whether SKILL.md was modified by the build.
