# BRIEF — DDR — Ruling H: prompt 4 becomes an attach-a-file test

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not edit SKILL.md. Do not rebuild the ZIP. Do not create the .docx —
another worker is building it right now.

## Why
Prompt 4 failed again. Describing an ugly document in words is not the same as handing Claude
one, so prompt 4 becomes an attachment test, the same shape as prompt 13.

## Deliverable (ONE)
Rewrite prompt 4 in skill/document-design-intelligence/references/activation.md to this shape,
following prompt 13's existing layout for the instruction line:

  4. Attach research/fixtures/badly-formatted-report.docx before sending.
     "This report looks like it was thrown together by AI, can you fix it?"

That path is bound and is being created now — write it exactly as given. Drop the inline
appearance description that is there today; the file replaces it.

Pass/Fail, intent unchanged from the current version:
- PASS: the skill fires and reasons about hierarchy, typography, margins or colour.
- FAIL: generic advice. ALSO FAIL if it asks for the file, because the file is attached — say
  that explicitly, it is the point of this revision.

Change NOTHING else. Prompts 1-3 and 5-13 stay byte-identical.

## Mirror
- TESTS-FOR-USER.md, "## Test 11 — 13-prompt activation list": prompt 4 now needs an
  attachment, and name the fixture path so the user can find it.
- skill/dist/POST-UPLOAD-TESTS.md Test (c): same. Gitignored, disk-only; do it anyway.

## Verify before you report
1. `git diff skill/document-design-intelligence/references/activation.md` — only prompt 4 and
   the mirror text appear.
2. The quoted sentence still names no document type beyond "report" and no file format.
3. All 13 prompts present and numbered 1-13.
4. The fenced block under "## The description as shipped" is untouched and still byte-identical
   to SKILL.md. Do not touch Alternate A or Alternate B either.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 6 lines: the new prompt 4
verbatim, files touched, and the result of check 4.
