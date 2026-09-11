# BRIEF — Acceptance Tester — SMOKE TEST (browser, claude.ai)

ONE deliverable: `research/47-browser-smoke.md`. Expect ~10 minutes. Then stop.

## Hard rules
- Touch nothing else in the account. Change no settings. Delete nothing. ONE chat only.
- If a login screen, 2FA, or captcha appears: STOP immediately and report. NEVER enter
  credentials.
- No git. Ever. The orchestrator owns git.
- Do not "fix" anything you find. Record it and stop.

## WHAT "SUCCESS" MEANS HERE — read this before you start
Success = each step below **completed and was recorded**. Record what you observe; do not
bend it toward any expectation.

**The expected result on the step-3 prompt is that the skill FIRES.** Prompt 1 (the English
CV request) has passed in every run this project has: 2026-09-09 on the rebuilt ZIP
(RESUME.md's activation table, row 1: "PASS — asked about format, produced an ATS-friendly
French CV") and again in every v0.2 round. CV requests fire reliably.

There IS a known routing limitation on this skill, but it does **not** apply here: English
and French PROSE genres (letter, memo, report, proposal) may fail to fire and get answered
directly in chat or routed to the built-in docx skill. That is a closed, documented issue
about a different prompt family. It says nothing about the CV prompt.

So: if the skill fires, that is the expected result. If it does NOT fire, that is a genuine
and important finding — record it in full detail and report it, but do not retry, do not add
the workaround sentence, and do not open a second chat. One observation, recorded honestly.

## Steps

### 1. Logged in
Open claude.ai. Confirm the session is already logged in. Record what you saw that proved
it (e.g. the chat list, the account avatar). If not logged in -> STOP and report.

### 2. Skill present and its shown description
In the account's skills list, find `document-design-intelligence`.
Record:
- that it is listed, and whether it is ENABLED;
- the **first words of the description exactly as the UI shows them**, verbatim.

For reference, the on-disk description starts: `Creating any document type below is still
this skill's job even as Word or PowerPoint;`

**If the shown text differs, that is not a failure — do not stop.** Record the difference
verbatim and continue. A mismatch just tells us which build is actually installed, which
we need in order to read step 3's result correctly.

Also record, in one line: **which skills are enabled in the chat you use for step 3** —
specifically whether `docx` and `pptx` are on. (Later handoff tests depend on this.)

### 3. One fresh chat, one prompt
Open ONE new, empty chat. Paste this prompt verbatim and send it:

```
Can you make me a CV for a marketing coordinator role?
```

Wait for the reply to finish completely. Then record these as **three separate fields** —
do not merge them:

- **A. UI skill-use indicator (PRIMARY evidence):** did the interface itself show that a
  skill was used (badge, "used skill" row, tool/skill chip, expandable block)? Answer
  yes / no / could-not-tell, and describe exactly what you did or did not see and where
  you looked.
- **B. The reply's own claim (SECONDARY, separate):** did the reply text itself state or
  imply it used the skill? Quote the words if so.
- **C. First 300 characters of the reply**, verbatim, character-for-character.

A and B are different evidence. A model can claim skill use without firing, and can fire
without mentioning it. Never infer one from the other.

### 4. Write the file
Write `research/47-browser-smoke.md` containing:
- what worked, step by step;
- **what the UI actually looked like at each step** — enough detail that someone who has
  never seen it can navigate it next time (where the skills list lives, where the
  skill-use indicator appears or does not, how you opened a fresh chat);
- the three separate fields A, B, C from step 3;
- any step that needed a workaround, and exactly what the workaround was;
- anything ambiguous or that you could not determine.

## Report
Message the orchestrator in a FEW LINES: logged in yes/no, skill listed yes/no + enabled,
shown-description first words (and whether they matched), A / B one word each, file
written. Then STOP.
