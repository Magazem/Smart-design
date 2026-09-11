# VERDICT ON CANDIDATE L — and a provenance problem with the case against it

Written 2026-09-11 by the Workflow Orchestrator (sub-manager) after the clean browser run.
Run record: `research/49-candidate-L-settle.md`. Revert prep: `research/52-revert-L-prep.md`.

## THE CLEAN RUN — activation 11 under candidate L is DOCX-ONLY
All three preconditions were verified read-only before the prompt was sent:
- **Confound empty**, re-verified: the Instructions for Claude textbox carries no value
  attribute while Full name and Display name both carry `value="yazan"`.
- **Skill ENABLED**, confirmed by hover reading "Turn off document-design-intelligence". The
  USER enabled it; the tester did not touch the toggle.
- **Installed build is candidate L**, description matched verbatim.

Result, scored on the primary evidence:
- **A (primary):** the only SKILL.md path anywhere in the expanded trace is
  `/mnt/skills/public/docx/SKILL.md`. No document-design-intelligence path at any point.
- **C (corroboration):** the follow-up names only "the docx skill" and never mentions ours.
- **E:** a real .docx was produced, `Q3_Business_Update.docx`.

**This is a genuine, unconfounded, invocation-scored DOCX-ONLY under L.** It is the third
docx-only result for activation 11 under L and the second that is fully clean. The earlier
worry that a disabled skill explained the result is now DEAD for this run: the skill was
confirmed enabled and it still did not fire.

## THE PROBLEM: THE BASELINE HAS NO PRIMARY RECORD
The entire case against candidate L is the contrast "fired 2/2 under H, docx-only under L". I
went looking for the H runs. **They are not recorded anywhere in `research/`.**

The claim appears only as an assertion, in four places, all of them summary or brief text and
none of them a run record:
- `RESUME.md:487`, `:543`, `:831`, `:1378`
- `research/brief-tester-spotcheck.md:127`

There is no chat URL, no commands-line capture, no follow-up quote, no date, and no scoring
method for either of the two H runs. By contrast the docx-only results ARE properly recorded —
`research/48-browser-spotcheck.md:285` gives P6 in full, with the trace and the verbatim
follow-up.

**This matters because of the project's own ruling.** The 2026-09-11 confound ruling retires any
result SCORED ON THE SHAPE of a reply and keeps only results established by Claude naming the
skill it used. **We cannot apply that test to the H runs, because we do not know how they were
scored.** An unscorable baseline cannot be cited for a verdict, by the same standing rule that
makes us refuse an authority we cannot grep-verify. That rule has to apply to our own record or
it is not a rule.

## WHAT FOLLOWS
1. **L is not shown to have caused anything.** Activation 11 goes docx-only under L. Whether it
   ever behaved differently is unestablished. "L may HURT" rests entirely on the unrecorded
   baseline.
2. **This is also consistent with activation 11 simply never having fired reliably.** Claude's
   own account in the clean run explains the docx-only outcome without reference to L at all:
   the user named a format, and docx won on its own literal trigger criteria. That is the
   file-not-genre mechanism, and it predicts docx-only under ANY of our descriptions.
3. **So the revert trial tests something worth testing, but not what it was commissioned to
   test.** It would not "restore" a behaviour we have no record of. It would ask a fresh
   question: does the pre-L wording fire on activation 11? That is a legitimate n=1 experiment
   and its answer is informative either way. It is NOT a restoration.

## RECOMMENDATION
Put the provenance gap to the user before spending an upload. Either:
- **(a) Drop the revert.** Accept that L is neutral-and-unfalsified, keep it, and spend the
  user's upload on candidate M instead, which targets a Claude-sourced mechanism and is
  falsifiable by this exact prompt. M is the stronger experiment.
- **(b) Run the revert anyway**, relabelled honestly as a fresh test of the pre-L wording rather
  than a restoration, and accept it is n=1 against no baseline.

I recommend **(a)**. The same upload buys a test of a live hypothesis instead of a test of a
recollection. But this is the lead's and the user's call, not mine.

## A TRAP FOR WHOEVER BUILDS ANY TEST ZIP — read before building
The Packaging Analyst is RIGHT NOW modifying `research/build-manifest.py` and the manifest for
the display-columns fix. **A ZIP built from the current working tree would carry BOTH the
description change AND the display-columns fix**, and the trial would move two variables at
once. Any description-test ZIP must isolate the description.

The safe construction: take the PUBLISHED v0.2.0 asset, which is exactly what is installed, and
change ONLY the description (plus `NEGATIVE_HEAD_MARKER`, so the shipped test stays
self-consistent). Do not build from the working tree until the fix has landed and been verified.
