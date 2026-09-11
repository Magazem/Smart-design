# BRIEF — Mechanism — RULING O: the release body would carry both versions

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push.

## Why — a real pre-tag blocker, found by the lead
.github/workflows/release.yml line 46 sets `body_path: RELEASE-NOTES.md`. That file now holds:

    line  1:  # v0.2.0
    line 55:  # v0.1.0

So the GitHub release body for v0.2.0 would include the ENTIRE v0.1.0 section underneath it.
This worked by accident in v0.1.0, when the file held exactly one version.

## Deliverable (ONE)
### 1. release.yml
After the existing "Set version from tag" step at line 26 — which already computes
`VERSION="${GITHUB_REF_NAME#v}"` and writes it to `$GITHUB_OUTPUT` — add a step that extracts
ONLY the section for that version into a temp file, and point `body_path` at it.

Extraction rule: from the line `# v$VERSION` up to, but NOT including, the next line beginning
`# v`, or end of file if there is none.

**FAIL THE JOB LOUDLY IF THE SECTION IS MISSING.** An empty or absent section must stop the
release, not publish a blank body. That is the whole point: a silent empty body is exactly the
class of defect we spent yesterday finding — the command succeeds and says nothing.

`generate_release_notes: true` stays as it is; it appends the commit list underneath.

The job runs in bash on ubuntu-latest. No Windows quoting, no PowerShell.

### 2. research/37-release-checklist.md
Add the check to the pre-flight section: confirm the extracted body contains the version being
tagged and does NOT contain the previous one. Someone reading the checklist before a tag should
be able to run it by hand.

## Verify — paste BOTH outputs in your report
Run your extraction locally over the real RELEASE-NOTES.md, twice:
1. For 0.2.0 — must start at "# v0.2.0" and STOP before "# v0.1.0".
2. For 0.1.0 — must start at "# v0.1.0" and run to EOF.
Paste both. I want to see the boundary behave in both directions, because an off-by-one that
drops the last line of the final section would be invisible in the first test alone.
3. Show what happens for a version that does NOT exist, e.g. 9.9.9 — it must fail loudly.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe
(for any local checking; the workflow itself must be shell)

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the new workflow
step verbatim, the three outputs, and the checklist line you added.
