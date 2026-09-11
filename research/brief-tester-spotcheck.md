# BRIEF — Acceptance Tester — ROUTING SPOT-CHECK (browser, claude.ai)

## *** HELD — DO NOT DISPATCH ***
Blocked on all four. The orchestrator releases it; the tester does not self-start.
1. The weekly claude.ai limit has RESET (it stood at 75% after two sends on 2026-09-11).
2. The lead has the user's answer on whether the account carries a custom instruction or
   memory about asking before inventing content (the "clarification rule" confound).
3. Step 0 below has been completed and its findings accepted.
4. The lead has confirmed the run.

ONE deliverable: `research/48-routing-spotcheck.md`.

## THE BUDGET: 6 SENDS = 3 PROMPTS
Every message costs the user's own weekly quota. Two sends consumed 75% of a weekly limit.

**Each trial costs TWO sends: the prompt, then the follow-up question.** So a six-send ceiling
is THREE TRIALS, not six. Count in PAIRS.

If a trial double-submits (observed 2026-09-11: one paste landed as two turns), those extra
sends come out of the same six. You may end with two trials instead of three. That is the
correct outcome — do not exceed six to rescue a third trial.

## THE DETECTION METHOD — this is how you score, do not improvise
Two parts, use BOTH on every trial:
1. Read claude.ai's own skill-use indication in the reply stream, if shown.
2. **ASK THE FOLLOW-UP IN THE SAME CHAT, BEFORE SCORING:** `did you trigger any skill?`
   Claude answers this accurately — it names docx when it used docx, and names
   document-design-intelligence when it used that.

A trial with no follow-up is **UNSCORED**, not a fail. The 2026-09-11 smoke test was wasted
exactly this way. Never skip step 2, even when the answer seems obvious from the reply.

## Hard rules
- Touch nothing else in the account. Change no settings. Delete nothing.
- One FRESH chat per trial. The prompt and its follow-up share that chat; nothing else does.
- VERIFY EXACTLY ONE SEND for the prompt before reading the reply, and one for the follow-up.
- Login screen, 2FA or captcha: STOP and report. Never enter credentials.
- Browser not attached? The panel must be opened inside THIS conversation. Report once and
  stop; do not loop.
- No git. Report to the orchestrator and stop.

## Step 0 — costs no sends, do it first
Open Settings and record:
- Any **Memory**, custom instructions, personal preferences or style settings that are ON,
  quoted verbatim. If a behaviour-changing instruction is active, STOP AND REPORT BEFORE
  SPENDING ANY SENDS. Do not disable it — that is the user's setting and the lead's call.
- **Which skills are enabled** in the chat you will use: document-design-intelligence, docx,
  pptx, UI/UX Pro Max. Name each and whether it is on. A handoff result is meaningless if
  docx and pptx are off.

## Step 1 — the three trials
Fresh chat each. Paste verbatim, then ask the follow-up in that same chat.

Run them IN THIS ORDER, so that if you run out of sends you have lost the least:

1. **CONTROL — German Angebot.** Activation prompt 3, text in
   `skill/document-design-intelligence/references/activation.md`. This project records it as
   firing reliably. It runs FIRST because if the control does not fire, the harness or the
   account is broken and the other trials mean nothing — in that case STOP and report rather
   than spending the remaining sends.
2. **EN memo** — previously did not fire.
3. **FR letter** — previously did not fire.

DEFERRED to a later session, not dropped: FR report, and activation 11 (rough notes -> Word,
which passed 2/2 under H then failed under L, n=1, never re-tested).

Every prompt must carry REAL INLINE CONTENT. A prompt with nothing to work on makes Claude ask
for details, which is correct generalist behaviour and measures NOTHING — that defect wasted
prompts 3, 4, 5, 12 and the whole 2026-09-11 smoke test. If a prompt lacks content, add
plausible inline content and RECORD EXACTLY WHAT YOU ADDED.

Record per trial, as SEPARATE fields, never merged:
- **A. UI indication:** shown / not shown / could-not-tell, and where you looked.
- **B. Follow-up answer:** the reply to "did you trigger any skill?", quoted verbatim,
  including any skill it names.
- **C. First 300 characters of the original reply, VERBATIM** — copied, not summarised. The
  last run paraphrased this; do not.
- **D. Shape:** designed document / design-framed question / generic question / plain chat
  answer.

## Step 2 — write `research/48-routing-spotcheck.md`
A table of trials x fields A/B/C/D, then: Step 0 findings, sends actually spent, any
double-submits, what you added as inline content, and anything you could not determine.
Score a trial ONLY where the follow-up was asked. "Unscored" is a correct entry.

## Report
A few lines: sends spent, control fired yes/no, per-trial follow-up answer in a few words,
Step 0 confounds. Then STOP.
