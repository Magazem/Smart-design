# BRIEF — DDR — activation prompt 11's rubric is now wrong, not the skill

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT edit SKILL.md or the description.

## Why
Candidate H is now live. It says creating a listed document type is this skill's job even when
the output is Word or PowerPoint, and defers only when THE USER names a format for a plain
conversion.

Activation prompt 11 is "turn my rough notes into a Word document", and its current pass
criterion is that the docx skill takes it and OURS STAYS SILENT. Under H that criterion is
wrong: turning notes into a document is CREATION, not conversion, so our skill firing is the
intended behaviour. In the user's re-run it fired twice and produced good output the second
time. The rubric would score that a failure.

The plain-conversion deferral is tested by prompt 13 alone — "Just convert this .docx file to a
PDF, don't change anything" — which still passes and must keep its criterion unchanged.

## Deliverable (ONE)
In skill/document-design-intelligence/references/activation.md, rewrite prompt 11's Pass and
Fail lines.
- PASS: this skill fires and renders through the docx handoff. Firing is correct.
- FAIL: docx responds as the top-level skill and ours never engages, or ours engages but
  reimplements OOXML generation itself instead of handing off.
- Add one line recording WHY this changed: it is a consequence of candidate H, which moved
  "create a document that happens to be Word" from the deferral side to ours.

Leave the prompt TEXT itself unchanged — only the criteria move.
Change nothing about prompts 1-10, 12 or 13.

## While you are in that file — two known stale passages, FIX THEM TOO
These are already ruled and are part of this one deliverable:
1. The prose still says the description "grew from 667 to 964 with the addition of the
   built-in-skill deferral sentence". Wrong cause: 964 is the result of candidates F, G and H.
   Make it honest and keep 667 only as the historical starting number.
2. The paragraph below it argues that .docx and .pptx stay out of the trigger list, while
   describing a sentence that no longer names them. H's sentence names neither format as a
   trigger; it names the CONDITION (the user naming a format for plain conversion). Rewrite so
   it describes the sentence that actually ships.

## Do NOT touch
- The fenced block under "## The description as shipped". It is byte-identical to SKILL.md's
  description and that will shortly be enforced by a test. Leave it exactly as it is.
- "Alternate A" and "Alternate B". Retained history.

## Verify before you report
1. `git diff` on activation.md shows ONLY prompt 11's criteria and the two stale passages.
2. The fenced block is untouched — confirm with a byte comparison against SKILL.md's
   description, not a whitespace-folded one.
3. All 13 prompts still present and numbered.
4. Prompt 13's criteria are unchanged.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: prompt 11's new
criteria verbatim, what you changed in the two stale passages, and the result of check 2.
