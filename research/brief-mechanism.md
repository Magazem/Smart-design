# BRIEF — Mechanism — plain-text output must keep the section order

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT change the description in SKILL.md's frontmatter — that is settled and
under test. You are editing the SKILL.md BODY prose only. No script changes.

## Why — this is a v0.2 blocker, not polish
The user ran activation prompt 11 twice on the new archive. Both times this skill fired, which
is now correct. Run one asked "PDF or text?", the user chose TEXT, and the output was
unstructured AI-looking prose. Run two did not ask and produced something the user called very
neat and professional.

So on the plain-text path the skill dropped the section order entirely. That means the ENTIRE
structure model added in v0.2 — 52 canonical sections, 204 heading rows, section orders for all
17 families — is silently absent whenever the user asks for text rather than a file. The data is
loaded, the resolver returns it, and the body prose never tells the model it still applies.

## The body as it stands
skill/document-design-intelligence/SKILL.md, 52 lines. Two sections matter:
- "## Rendering is a handoff, not ours" at line 24, which frames output as docx, pptx or PDF.
  Plain text is not mentioned anywhere, so a model reasonably reads text as outside the flow.
- "## Section-order guidance" at line 37, which says resolve returns a section order but never
  says what to DO with it when there is no file to render.

## Deliverable (ONE)
Body prose that makes this unambiguous. The rule to state:

  THE OUTPUT FORMAT NEVER CHANGES THE SECTION ORDER OR THE HEADINGS. Plain text in the chat
  still gets the resolved structure — the same sections, in the same order, with the same
  headings. Only the RENDERING changes.

Put it where a model reading top to bottom will hit it before it starts generating. Decide
yourself whether that is inside the section-order section, the handoff section, or the numbered
step list near the top, and say why you chose that place.

Keep it SHORT. This file is a router, and every line competes for attention with the four-step
flow that is the point of it. Two or three sentences. If you find yourself writing a paragraph,
you are explaining rather than instructing.

Also make sure the handoff section no longer implies output is only ever a file. One clause is
probably enough.

## What NOT to do
- Do not touch the frontmatter. Not one character. There is a test that reads it.
- Do not add a fifth step to the four-step flow.
- Do not restate the section list or name families.

## Verify before you report
1. `git diff` on SKILL.md shows body changes only, and the description line is untouched.
2. `python3 -m pytest scripts -q` — baseline 146 passed plus 8 subtests. The description
   coverage test must still pass, which is your proof the frontmatter is intact.
3. Report the file's new line count. It was 52. If it grew by more than about 5, you wrote too
   much.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: the new prose
verbatim, where you put it and why, the line count, and the test tally.
