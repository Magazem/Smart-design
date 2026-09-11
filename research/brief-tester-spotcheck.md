# BRIEF — Acceptance Tester — ROUTING SPOT-CHECK (browser, claude.ai)

## *** HELD — DO NOT DISPATCH ***
Blocked on all three of these. The orchestrator releases it; the tester does not self-start.
1. The weekly claude.ai limit has RESET. It stood at 75% after two sends on 2026-09-11.
2. The account's Memory / custom instructions have been checked (see Step 0).
3. The lead has confirmed the run.

ONE deliverable: `research/48-routing-spotcheck.md`.
HARD CEILING: **6 sends.** Not 6 prompts plus retries. SIX SENDS TOTAL. If you spend a send by
accident, that is one of the six. Stop at six whatever happens.

## Why this is small
The user's own claude.ai plan pays for every send. Two sends cost 75% of a weekly limit. The
13x3 run once planned would exhaust their plan many times over. Scaled regression runs go to
the API harness (separate billing), not here. This brief exists only to spot-check ROUTING on
the cases that previously failed.

## Hard rules
- Touch nothing else in the account. Change no settings. Delete nothing.
- One FRESH chat per prompt. Never two prompts in one chat.
- **VERIFY EXACTLY ONE SEND PER PROMPT BEFORE READING THE REPLY.** A UI double-submit was
  observed on 2026-09-11: one paste landed as two turns. A double-send doubles the cost and
  can give two different answers for what looks like one trial. If a prompt double-sends,
  record it, count BOTH sends against the ceiling of six, and do not treat it as two trials.
- If a login screen, 2FA or captcha appears: STOP and report. Never enter credentials.
- No git. Report to the orchestrator and stop.
- Browser not attached? The panel must be opened inside THIS conversation. Report once, stop,
  do not loop.

## Step 0 — FIRST, and it costs no sends
Before any prompt, open the account's Settings and record:
- Any **Memory**, custom instructions, personal preferences or style settings that are ON,
  quoting them. A 2026-09-11 reply cited "per your clarification rule", which suggests an
  account-level instruction forcing Claude to ask before inventing content. If such a setting
  exists it changes behaviour on EVERY trial below and the results are not clean ground truth.
- **Which skills are enabled** in the chat you will use: document-design-intelligence, docx,
  pptx, UI/UX Pro Max. Name each and whether it is on.

If a behaviour-changing instruction IS active, STOP AND REPORT BEFORE SPENDING ANY SENDS.
Do not disable it yourself. That is the user's setting and the lead's call.

## Step 1 — find out whether a skill-use indicator exists at all
**This is the most valuable thing in this brief.** Read it before you send anything.

No skill-invocation indicator has EVER been observed in this project's browser testing. Every
recorded PASS was inferred from the SHAPE of the reply. Until we know what a fire LOOKS LIKE,
no browser result can separate "the skill fired" from "Claude answered well as a generalist".

So on your FIRST prompt, before judging anything, hunt for the indicator and describe the
hunt: look at the message header and footer, any badge, chip, pill, disclosure triangle,
"thinking"/"tools"/"used" row, any expandable block, and the chat's own sidebar or info panel.
Say exactly WHERE YOU LOOKED, not only what you found. "I saw none" is a useful answer ONLY if
it comes with the list of places checked.

If you find one: describe it precisely enough to recognise on sight, and say so immediately in
your report — it changes how every future run is scored.

## Step 2 — the prompts (5 sends, leaving 1 spare)
Fresh chat each. Paste verbatim. These are the previously FAILED routing cases plus a control.
Record for each, as SEPARATE fields, never merged:
- **A. UI indicator** (primary evidence): yes / no / could-not-tell, plus where you looked.
- **B. The reply's own claim** (secondary): did the text say it used the skill? Quote it.
- **C. First 300 characters of the reply, VERBATIM** — copied exactly, not summarised. The
  last run paraphrased this; do not.
- **D. Shape**: did it produce a designed document, ask a design-framed question, ask a
  generic question, or just answer in chat?

1. EN memo — previously did not fire.
2. FR letter — previously did not fire.
3. FR report — previously did not fire.
4. Activation 11 (rough notes -> Word document) — passed 2/2 under H, FAILED under L by going
   to docx. n=1 flip, never re-tested. Take prompt 11's exact text from
   `skill/document-design-intelligence/references/activation.md`.
5. CONTROL — a case expected to behave, to prove the harness discriminates at all. Use the
   German invoice/Angebot prompt (activation prompt 3 in the same file), which this project
   records as firing reliably.

Each prompt must carry REAL INLINE CONTENT. A prompt with nothing to work on makes Claude ask
for details, which is correct generalist behaviour and measures NOTHING — that defect has now
wasted prompts 3, 4, 5, 12 and the 2026-09-11 smoke test. If a prompt above lacks content,
add plausible inline content and RECORD WHAT YOU ADDED.

## Step 3 — write `research/48-routing-spotcheck.md`
A table of the five prompts x fields A/B/C/D, then: the Step 0 settings findings, the Step 1
indicator hunt (where you looked, what you found), sends actually spent, any double-submits,
and anything you could not determine. Do not score PASS/FAIL if no indicator exists — report
the shape and say scoring is not possible. Saying "I could not tell" is correct and expected.

## Report
A few lines to the orchestrator: sends spent, indicator found yes/no, per-prompt shape in one
word each, Step 0 confounds. Then STOP.
