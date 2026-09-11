# BRIEF — Packaging Analyst — REMOVE characterSpacing FROM THE docx HANDOFF

Small, surgical. Ruled by the lead 2026-09-11. Deliverable: the change plus a few lines in
`research/63-characterspacing-removal.md`.

## WHY
The docx handoff emits a `characterSpacing` key sourced from a `Letter Spacing pt` column that
**exists in no table**, so it always reports not present. The mapping is itself tagged UNSOURCED
in `ddi.py`'s own module note. A key that is both unsourced and permanently empty is noise in the
one block the renderer actually reads.

## SCOPE — EXACTLY THIS, AND NOTHING ELSE
1. Drop the `characterSpacing` line from the **docx** handoff (`ddi.py`, around line 523, using
   `docx_letter_spacing_key` at line 231).
2. Remove its test reference (`scripts/tests/test_ddi.py`, around line 230).
3. Remove any now-dead vocabulary entry or helper **only if nothing else uses it.** Check first.

**DO NOT touch anything else.** This must not ride along with other changes.

## *** LEAVE THE pptx `charSpacing` ALONE — read this before you start ***
`ddi.py:591` emits `charSpacing` for **pptx**, and that one **IS SOURCED** (research/23 pptx:458).
The ruling is docx-only. Do not remove it, and do not "tidy" it.

**But note the asymmetry and report it, do not act on it:** both paths read the same missing
`Letter Spacing pt` column via `_letter_spacing_pt` (line 317), so pptx's `charSpacing` is ALSO
permanently empty — just with a sourced mapping rather than an unsourced one. So
`_letter_spacing_pt` stays; pptx still needs it.

**Say in your deliverable whether you think pptx should keep emitting a sourced key that can
never carry a value.** That is a question for the lead, not a change for you to make. I want your
opinion on the record, not your edit.

## RULES
- **No git, ever.** The orchestrator owns git.
- Use `python3`, not `python`.
- Full pytest green afterwards. Report the count.
- Run the docx handoff for `cv-uk` and paste the output showing the line is gone and **nothing
  else changed**.

## ALSO
Confirm the docx handoff still emits every other block, each with its not-present line where
applicable. **We are removing a line, not learning to omit blocks again** — omission is the exact
failure mode that hid the pdf gap for a whole release.

Report to me in a few lines: removed yes/no, pptx untouched yes/no, pytest count, your opinion on
the pptx asymmetry.
