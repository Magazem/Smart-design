# BRIEF — DDR — Ruling E: give prompts 6, 8, 10, 11, 13 their input inline

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. The orchestrator commits. Do not edit SKILL.md. Do not rebuild the ZIP.

## Why
You already fixed prompts 2-5 this way. The user spotted the same defect in the should-not-fire
and handoff sets: prompts 6, 8, 10, 11 and 13 say "this dashboard", "this Python function",
"this PDF", "my rough notes", "this .docx file" with nothing attached. A generalist replying
"please upload it" proves nothing about routing. Prompts 7, 9 and 12 are already
self-contained — LEAVE THEM EXACTLY AS THEY ARE.

## Where
skill/document-design-intelligence/references/activation.md
- "### Should not fire" starts at line 338; prompts 6-10 follow.
- "### Handoff tests" starts at line 359; prompts 11-13 follow.

## Deliverable (ONE)
Rewrite prompts 6, 8, 10, 11 and 13 so each carries its own input, then mirror the pass rule.

6. Keep the sidebar-UX ask. Add a short inline description of the dashboard sidebar: a few
   named nav items and a concrete UX complaint. No attachment needed.
8. Paste a real Python function inline, 5-10 lines, obviously slow — nested loops over a list,
   for example. Then the "refactor to run faster" ask.
10. Paste a short abstract-like paragraph inline. KEEP the "PDF research paper" wording and
    keep it a pure summarize ask with no create/fix verb. That wording is the whole point of
    the test: it checks we do not over-trigger on a bare format noun.
11. Paste 5-8 lines of rough bullet notes inline, then keep "Turn my rough notes into a Word
    document." verbatim as the ask.
13. Cannot be pasted — it needs a real file. Keep the prompt text unchanged and add one
    instruction line above it: "Attach any short .docx you have (one page is enough) before
    sending."

Pass/Fail lines: keep each one's INTENT exactly as it is. Add to the should-not-fire prompts
(6, 8, 10) and to 11 and 13 a short note that "asked for the file and named no skill" also
counts as a PASS but is weak evidence, which is why the content is now inline — a test with
content is the stronger signal.

## Mirror
- TESTS-FOR-USER.md, "## Test 11 — 13-prompt activation list" (you added it; it is around
  line 453). Extend the inline-input sentence so it covers 6, 8, 10, 11 and 13 too, and note
  that prompt 13 needs a short .docx attached.
- skill/dist/POST-UPLOAD-TESTS.md, Test (c) around line 114. Same note. This file is gitignored
  so the edit is disk-only; do it anyway.

## Verify before you report
1. All 13 prompts still present, numbered 1-13, in order.
2. Prompts 1-5, 7, 9 and 12 are byte-identical to what is committed. Check with
   `git diff skill/document-design-intelligence/references/activation.md` and read the hunks —
   only 6, 8, 10, 11, 13 and the mirror text should appear.
3. Prompt 10 still contains the words "PDF research paper" and still has no create/fix verb.
4. The file still parses as UTF-8.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: what you put
inline for each of the five, confirmation that 7, 9 and 12 are untouched, and anything you
ruled on yourself.
