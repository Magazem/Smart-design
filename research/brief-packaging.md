# BRIEF — Packaging Analyst: step 8, prepare the v0.1.0 release (~10 min)

Context reset by policy; nothing lost. Your 7b pass is verified and closed — I opened the
rebuilt ZIP myself: 39 members, 14 base CSVs, rationale present, manifest md5 731d874f, no
brand overlay, no active.json, description 823 chars saying "sourced".
Act from THIS FILE and from disk.

Repo root: C:\Users\ysuliman\Documents\Ai plugin  (this IS now a git repo — see below)
Skill dir: skill\document-design-intelligence
Python:    C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## What changed: the project is under version control as of today
Repo at the PROJECT ROOT, initial commit 0bdb838, remote
https://github.com/Magazem/Smart-design.git. `release.yml` now lives at
`./.github/workflows/release.yml` and derives the version FROM THE TAG: it writes
`skill/document-design-intelligence/VERSION` from `GITHUB_REF_NAME`, then runs
`build_zip.py`, then attaches the dist asset. So VERSION is CI's to write, not yours.

## ONE deliverable: the tree is release-ready and the tag command is handed over.
1. **Do NOT bump VERSION by hand** — it still reads `0.0.1-dev` and that is correct; the
   workflow overwrites it from the tag. If you think that is wrong, say so rather than
   editing it.
2. **Final artefact check.** Rebuild the ZIP locally and OPEN it. Confirm, by listing
   members: all 14 base CSVs, `data/rationale/`, the manifest with md5 731d874f, SKILL.md
   whose description says "sourced" and not "validated", NO `data/brand/<slug>/` path and no
   `active.json`. Report the member count and byte size. Note `skill/dist/` is gitignored,
   so the local artefact is a check, not a commit.
3. **Do NOT touch git.** The Orchestrator commits, path-scoped, after verifying your work. Just report what you changed and where.
   worker may have edits in flight in the same tree. Commit locally. DO NOT PUSH and DO NOT
   TAG: pushing and tagging are the lead's, after the user confirms.
4. **Write `research/37-release-checklist.md`**: the exact command sequence for the user to
   cut v0.1.0 — the tag command, the push that triggers the workflow, and what they should
   see afterwards (workflow run, asset name, where it lands). Include how to verify the
   published asset is the right one, and how to roll back a bad tag. Be precise; this is the
   file someone follows at the moment they are least able to improvise.
5. State plainly in the checklist what this release DOES and DOES NOT contain: full section
   guidance for CVs only, layout/typography/colour/print guidance for everything else,
   headings for the other document families deferred to step 9, and the PDF/X-4 wording
   exactly as it stands. A release note that overstates is the same defect as a data cell
   that overstates. Include this known limitation VERBATIM in substance:
   "One ambiguous German deck phrase resolves to the projection variant instead of asking
   which was meant. The three deck rows tie on score and the tie is broken by row length."
   Also state what the resolver DOES do: it resolves when confident, asks which of the real
   candidates you meant when a request is ambiguous, and says plainly when nothing matches.

6. **The scope statement must reach the USER, not just research/.** `release.yml`'s publish
   step sets `generate_release_notes: true`, which builds the GitHub release body from
   commit titles — so everything you write in item 5 would never be seen by anyone
   downloading the skill. Fix that: write `RELEASE-NOTES.md` at the repo root (committed,
   not gitignored) carrying the scope statement, and add `body_path: RELEASE-NOTES.md` to
   the `softprops/action-gh-release@v2` step in `.github/workflows/release.yml`. Keep
   `generate_release_notes: true` if you want the commit list appended underneath; the
   action supports both. This is the ONE workflow edit you are authorised to make in this
   brief — do not change the build or version steps.

## Do not
Touch `data/base`, `research/load-base.py`, the manifest, or any `research/*.csv` draft.
Do not run ANY git command. Do not push, tag, commit, or stage. Do not edit VERSION.

## VERIFY
`pytest -q` from the skill dir — report the count (128 passed + 8 subtests at last check).
`python3 scripts/validate_data.py data/base` must print OK for 14 tables.
Do not run git. Just list the paths you created or changed, so the Orchestrator can stage
exactly those.

## REPORT
Max 8 lines to the Workflow Orchestrator, slot 01a080c5-2001-78b3-bbbe-afaae15edafa:
gate result, test count, the ZIP's identity and the six archive checks, the exact paths you
created or changed, and confirmation the checklist is written. If you approach ~10 minutes,
checkpoint to research/handover-packaging.md and stop.
