# BRIEF — Mechanism — Candidate L: the priority claim must come FIRST

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DRAFT ONLY. DO NOT edit SKILL.md. DO NOT touch git. You append one section to
research/38-description-candidate.md.

## The evidence — Claude's own account, verbatim, from the two failed French chats
FR letter: "I only pulled up the docx skill and didn't check document-design-intelligence. In
hindsight, that was probably the wrong call. You never said Word or .docx — you just asked for a
formal business letter. Per document-design-intelligence's own trigger rules, letters (courrier)
without a named file format are its job, and it defers to docx only when the user explicitly
names the format for a plain conversion. Since you didn't name a format, it should have taken
priority."

FR report: "I considered the general file-creation guidance ... but I didn't check
document-design-intelligence before creating the file — I should have. That skill's trigger list
explicitly includes reports, so it was relevant here and I skipped it. I treated this as a short
internal markdown summary rather than a designed document."

## What that means, and it is different from every theory we have tested
THE DESCRIPTION'S CONTENT IS CORRECT. Claude ENDORSES it once it reads it — it names courrier,
it names the deferral condition, it concludes we should have taken priority. The failure is
SALIENCE AT DECISION TIME: Claude decides "make a file", reaches for docx or a markdown file,
and never opens ours at all.

Candidate H's priority claim is the RIGHT SENTENCE. It is just the SEVENTH of eight, arriving
long after the decision is made.

## Deliverable (ONE) — research/38-description-candidate.md, appended as "Candidate L"
Do NOT overwrite B, F, G, H, I or J. F, G and H are APPLIED and live at 972. J was VETOED.

REORDER so the FIRST sentence is the priority claim over docx and pptx. The lead's sketch:
  "Use this before the docx or pptx skills whenever the user asks for a document to be created,
   drafted, structured or fixed: CVs, ... [noun list] ... appearance fixes ... Applies sourced
   ... Defer to docx/pptx only when the user names the format for a plain conversion or edit
   with no design ask. Not for web/app UI ..."

Rules:
1. MOVE words, do not invent them. This is a reordering, not a rewrite. The more of the current
   972 characters that survive verbatim, the less new risk we take.
2. THE DEFERRAL CONDITION MUST SURVIVE VERBATIM — "only when the user names it for a plain
   conversion or edit with no design ask". Activation prompt 13 depends on it and passes today.
3. Keep "sourced", the UI/UX boundary, "lettre", and every document noun.
4. Measure. Under 1023. Give the exact result on one line, its measured length, and headroom.

## TWO COUPLED CHANGES YOU MUST NAME, or the application breaks
- scripts/tests/test_description_coverage.py uses a LITERAL STRING as its region marker,
  currently "Creating any document type above". If your reorder moves or rewords that sentence,
  the marker must move with it. This exact trap nearly shipped a silent test when candidate H
  deleted the previous marker; there is now a hard AssertionError guarding it. Say in your draft
  what the new marker should be.
- references/activation.md's fenced "as shipped" block must be updated byte for byte. There is
  now a test enforcing that, so a missed update fails the suite rather than drifting silently.

## Risk
State the effect on should-not-fire prompts 8, 9 and 10. Scope does NOT widen here — the same
claims in a different order — so if you find a real risk, that is a finding worth flagging
loudly. Also say whether leading with a claim about OTHER skills' priority could misfire.

## The judgement I want
If you think reordering cannot fix a salience problem — because the platform may show only part
of the description, or because the decision happens before any description is read — SAY SO and
say what would. You refuted the H brief's framing correctly and Coverage refuted I. The same
permission applies.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the new first
sentence verbatim, the measured length and headroom, how much survived verbatim, the new marker
string, and your risk verdict.
