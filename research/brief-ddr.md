# BRIEF — DDR — Correct the three stale description-length quotes

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. The orchestrator commits. Do not edit SKILL.md.

## Why
The description in SKILL.md measures 823 characters. I verified this myself with Python
`len()` on the quoted value. The repo states three different numbers in three places, and two
of them are wrong. It also quotes an out-of-date copy of the description text itself.

## Deliverable (ONE)
Correct the stale numbers and the stale quoted text, nothing else.

1. skill/document-design-intelligence/references/activation.md
   - The block under "## The description as shipped" quotes the description with
     "Applies **validated** layout" — SKILL.md ships "Applies **sourced** layout". Fix that one
     word so the quoted block matches what actually ships.
   - The prose around lines 10-25 calls it "the 667-character primary description". 667 is
     stale. Say 823.
   - Sweep the whole file for any other character-count claim about the description and make it
     823. Do not touch the 1,024 / 1,023 cap discussion — that is correct and separately tested.
2. skill/dist/POST-UPLOAD-TESTS.md, Test (c), around line 128: it says "the 825 character
   description we shipped". Make it 823. (This file is gitignored, so the edit lives on disk
   only. Do it anyway.)

## Verify before you report
Re-measure rather than trusting me:
`python3 -c "import io,re;s=io.open('skill/document-design-intelligence/SKILL.md',encoding='utf-8').read();print(len(re.search(r'^description:\s*\"(.*)\"\s*$',s,re.M).group(1)))"`
If your python3 shim is broken, use the uv cpython interpreter, as you did on the last task.
Then confirm the quoted block in activation.md is character-for-character the SKILL.md value.

## Constraints
Do not change any prompt, any Pass/Fail line, or the 13-prompt section. That work is done and
committed. Do not rebuild the ZIP.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 6 lines: each number you
changed with its old and new value, and whether the quoted block now matches SKILL.md exactly.
