# BRIEF — DDR — Ruling G: give prompt 12 inline content

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not edit SKILL.md. Do not rebuild the ZIP.

## Why
Prompts 6-11 and 13 all PASS. Prompt 12 is the last one still bare: "I need a two-page CV, make
it look professional." Claude asked for CV details before any skill fired, the user said to use
placeholders, and only then was a CV produced — so whether the skill fired at creation time is
unknown. That is the same ask-before-invoke pattern that made old prompts 3-5 unreadable, and
the same fix applies: put the content inline.

## Where
skill/document-design-intelligence/references/activation.md, "### Handoff tests" section.
Prompt 12 sits between prompt 11 (the Bramwell Logistics notes) and prompt 13 (the .docx
conversion with its attach instruction).

## Deliverable (ONE)
Rewrite prompt 12 so it carries its own CV content. The lead's example, which you may improve
on but not weaken:

  "I need a two-page CV, make it look professional. I'm Sara Lindqvist, 8 years as a
  supply-chain analyst at Nordica Freight, before that 3 years as a logistics coordinator at
  Baltic Rail; MSc Logistics, Gothenburg; fluent Swedish, English, German; Excel, SAP,
  Power BI."

Two hard constraints on the wording:
- Keep the design intent ("two-page", "make it look professional"). That is what the test
  measures.
- Name NO file format. No Word, no .docx, no PowerPoint. Prompt 12 tests that we fire and hand
  off internally; naming a format would turn it into prompt 11.

Its Pass/Fail lines keep their intent exactly: PASS is this skill firing and rendering via the
docx handoff with docx not acting as the top-level responder; FAIL is docx responding directly,
or this skill reimplementing OOXML itself. You may add the same weak-evidence note the other
prompts carry, if it reads naturally.

Change NOTHING else. Prompts 1-11 and 13 stay byte-identical.

## Mirror
- TESTS-FOR-USER.md, "## Test 11 — 13-prompt activation list": extend the inline-input sentence
  to cover prompt 12.
- skill/dist/POST-UPLOAD-TESTS.md Test (c): same. Gitignored, disk-only; do it anyway.

## Verify before you report
1. `git diff skill/document-design-intelligence/references/activation.md` — only prompt 12 and
   the mirror text appear.
2. Prompt 12 contains no file-format word. Grep it for Word, docx, pptx, PowerPoint, PDF.
3. All 13 prompts present and numbered 1-13.
4. The fenced block under "## The description as shipped" is untouched — it is byte-identical
   to SKILL.md and a check depends on that. Do not touch Alternate A or Alternate B either.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 6 lines: the new prompt 12
verbatim, the files touched, and the result of check 2.
