# BRIEF — Acceptance Tester — SETTLE CANDIDATE L (browser, claude.ai)

ONE deliverable: `research/49-candidate-L-settle.md`. ONE fresh chat. Then STOP.

## Hard rules
- Touch NOTHING else in the account. Change NO settings. Delete nothing. ONE chat only.
- No git, ever. The orchestrator owns git.
- Do not "fix" anything you find. Record it and stop.
- If a login screen, 2FA or captcha appears: STOP and report. NEVER enter credentials.

## THREE BROWSER RULES — each one cost this project a session
1. **NEVER RELOAD or navigate away mid-trial.** A reload destroys the accessibility tree and
   kills the run. Screenshots keep working, so it still looks connected. It is not.
2. **WAIT 20 SECONDS after Send** on a fresh chat before concluding anything failed. The
   message does not render for 10-15s, and retyping double-submits.
3. **The browser panel binds PER CONVERSATION.** If a browser call returns "The in-app browser
   is not currently attached", that is NOT a login problem and NOT a dead capability. The user
   must open the panel inside THIS conversation. You cannot do it yourself. Report it ONCE to
   the orchestrator and STOP. Do not retry in a loop.

## STEP 0 — PROVE THE RUN IS NOT CONFOUNDED. Do this before anything else.
The account's custom instructions were a confound in earlier runs: they told Claude to ask
before acting and to keep answers short. **A run under active custom instructions is
UNSCORABLE BY RULE.** The user says they are off; you must verify it, not assume it.

Recorded method: open the custom-instructions setting and check the textbox. When it is
genuinely empty the textbox carries **no value attribute**, while sibling fields on the same
page do carry one. Record verbatim what you saw.

**If you cannot prove the box is empty, STOP and report. Do not run the prompt.**

## STEP 0b — WHICH BUILD IS INSTALLED
In the account's skills list find `document-design-intelligence`. Record:
- that it is listed, and whether it is ENABLED;
- the **first words of the description exactly as the UI shows them**, verbatim.

Candidate L is installed if the description starts: `Creating any document type below is still
this skill's job even as Word or PowerPoint;`

A mismatch is NOT a failure — record it verbatim and continue. It tells us which build is
actually installed, which we need in order to read the result at all.

Also record in one line: which skills are enabled in the chat you use, specifically whether
`docx` and `pptx` are on.

## STEP 1 — ONE fresh chat, ONE prompt (activation 11)
Open ONE new empty chat. Paste verbatim and send:

```
Here are my rough notes:
- Q3 revenue up 12% vs Q2
- New enterprise client signed: Bramwell Logistics
- Support ticket backlog down from 340 to 190
- Need to hire 2 more support reps by Q4
- Churn rate flat at 4.1%
Turn my rough notes into a Word document.
```

Wait for the reply to finish completely. Do not add the workaround sentence. Do not retry.
Do not open a second chat.

## STEP 2 — THE FOLLOW-UP, in the SAME chat
Send verbatim:

```
Which skills did you use for this request, and why?
```

## RECORD THESE AS SEPARATE FIELDS. Never merge them.
- **A. Commands line (PRIMARY EVIDENCE):** expand the "Ran N commands" line and record its
  contents VERBATIM, including every SKILL.md path. Say explicitly if no such line appeared.
  The SKILL.md paths are the primary and decisive evidence of which skill ran.
- **B. Indicator seen:** yes / no / could-not-tell, plus exactly where you looked.
- **C. Claude's follow-up answer, VERBATIM,** naming any skills it names.
- **D. First 300 characters of the original reply,** verbatim.
- **E. Did a .docx file actually get produced?** yes / no, and how you could tell.

**CAUTION on C, learned the hard way last run:** Claude's self-report of its own tool output was
inexact — it described a picker offering "UK, Gulf/GCC and France" when the screen showed
"UK/International, France, US". Treat the follow-up as corroboration of WHICH skill, never as
evidence about DETAILS. A and C are different evidence. A model can claim skill use without
firing, and fire without mentioning it. Never infer one from the other.

## WHAT COUNTS AS WHICH RESULT
- FIRED = the commands line contains
  `/mnt/skills/plugins/document-design-intelligence/SKILL.md`.
- DOCX-ONLY = the commands line contains `/mnt/skills/public/docx/SKILL.md` and NOT ours.
- Either outcome is a legitimate finding. Record honestly; do not bend it toward an expectation.

## STEP 3 — write the file
Write `research/49-candidate-L-settle.md` containing: the step 0 confound proof verbatim; the
installed-build check; fields A-E in full; anything ambiguous or undetermined; any workaround
you needed and exactly what it was.

## Report
Message the orchestrator (slot 01a080c5-2001-78b3-bbbe-afaae15edafa) in a FEW LINES:
confound proven empty yes/no, installed description matched L yes/no, FIRED or DOCX-ONLY,
the SKILL.md paths seen, file written. Then STOP.
