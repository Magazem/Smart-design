# BRIEF — DDR — v0.2 blocker: the acceptance prompts answer their own question

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Rewrite research/44-v02-acceptance.md in place.

## Why — read this carefully, it is the whole brief
The user ran prompts 1-5. The skill fired on NONE. Claude said: "I was doing a clean Word file
as per the request, no need for design skills." It was right to.

Every prompt pre-labels its own sections. Prompt 1 supplies "Rechnungssteller:", prompt 3
supplies "To:", "From:", prompt 5 supplies "Cover:", "Executive summary:". The section
structure the skill exists to supply is ALREADY IN THE REQUEST, and the ask is effectively
"write this up". That is a transcription job, and the docx skill correctly takes it.

This is the SAME CLASS OF DEFECT as the v0.1.0 activation round, where four of five failures
were prompts referencing content that was never attached. The test answered its own question.
There is a separate description defect being fixed in parallel — not your concern.

## Deliverable (ONE)
Rewrite all 15 prompts in research/44-v02-acceptance.md so each is a genuine test.

### Rules for the new prompts
1. RAW CONTENT ONLY. No section labels. No colon-prefixed field names. Give the facts the way a
   real person dumps them: a paragraph, a jumble, a list of details in no particular order.
   If a reader can reconstruct your expected section order by reading the prompt, it is wrong.
2. THE ASK MUST CARRY DESIGN OR STRUCTURE INTENT, in natural words a person would use. "make me
   a proper invoice", "I need this as a professional memo", "turn these notes into a business
   proposal", "erstelle daraus ein ordentliches Angebot". Not "write this up".
3. Keep the content INLINE. That lesson stands.
4. Keep the language mix. It is currently 6 English, 5 German, 4 French — keep roughly that, and
   keep each family in the language it has now so the expected orders stay comparable.
5. The expected section orders DO NOT CHANGE. They are correct and verified against
   structures.csv. You are changing the stimulus, not the answer.
6. Keep the three trap notes about families that share an identical order.

### Add a rule to the file header
State it so nobody reintroduces the defect:
  An acceptance prompt must not pre-supply the structure it is testing. If the prompt names the
  sections, the model only has to transcribe them, and the test proves nothing.

## Verify before you report
1. Grep your own prompts for colon-prefixed labels at line starts. There should be none inside
   the quoted prompt blocks.
2. For each prompt, ask yourself the reconstruction test in rule 1 and say which was hardest.
3. All 15 keys still present exactly once; expected orders still match data/base/structures.csv
   verbatim — re-run the check, do not assume, since you are editing the file around them.
4. Language counts still roughly 6/5/4.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: two rewritten
prompts verbatim as samples, the output of check 3, and which family was hardest to write
without leaking its structure.
