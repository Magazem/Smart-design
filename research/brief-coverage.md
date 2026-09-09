# BRIEF — Coverage — Reload data/base to clear the red gate

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git.

## Why — this is urgent, not routine
Your new duplicate-token rule is correct and it has turned the SHIPPING data gate red:

    data/base/doctypes.csv:19:Keywords: duplicate token 'flyer a4' in ','-delimited list
    1 problem(s) found   (exit 1)

and `resolve.py --doctype brochure-flyer-a4` now prints `[REFUSED PATH]`. I reproduced both.
The data did not change; the rule did, and it is telling the truth about what v0.1.0 shipped.
You fixed research/26-t1-doctypes-draft.csv but were told not to reload, so the fix has not
reached data/base. This brief closes that.

## Deliverable (ONE)
Run `research/load-base.py` so the corrected draft reaches data/base, and confirm the gate is
zero again.

## Scope discipline — read this before you run anything
load-base.py rewrites the WHOLE of data/base from the drafts. The only change that SHOULD
appear is the removed 'flyer a4' token in one row of doctypes.csv.

The heading and structure drafts for v0.2 (research/39, research/40) are NOT wired into the
loader yet and must NOT be wired in here. That is a later brief. If the loader picks them up,
stop and tell me.

## Verify before you report
1. `git diff --stat skill/document-design-intelligence/data/` — report it in full. If anything
   other than doctypes.csv changed, that is a finding: report it and do not "tidy" it.
2. `git diff skill/document-design-intelligence/data/base/doctypes.csv` — the diff must be one
   row, one token removed. Paste it.
3. `python3 scripts/validate_data.py data/base` from skill/document-design-intelligence.
   Expected: `OK: validated 14 table(s), 291 row(s)`, exit 0.
4. `python3 scripts/resolve.py --doctype brochure-flyer-a4` — must now RESOLVE, no
   [REFUSED PATH] and no [DATA WARNING] banner. Paste the first three lines.
5. `python3 scripts/resolve.py --query "a4 flyer"` — must resolve too.
6. `python3 -m pytest scripts -q` — baseline is 138 passed plus 8 subtests.
7. Report whether data/schema-manifest.json changed. It should not; the manifest comes from
   build-manifest.py, not from this loader.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the output of
checks 1, 2, 3 and 6, the resolve lines from 4, and anything the loader changed that you did
not expect.
