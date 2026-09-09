# BRIEF — DDR — Revise activation prompts 2-5 so each carries its input inline

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe (the repo venv is broken)
DO NOT touch git. The orchestrator commits. Do not run build_zip.py.

## Why
The user ran activation prompts 1-5 against the uploaded ZIP: 1 pass, 4 fail.
Prompts 4 and 5 say "This report..." and "Turn this text..." with NOTHING attached, so
Claude correctly asked for the file/text. Prompt 3 asked for client details, then said it
would "likely use document-design-intelligence" once given them. Those three are a TEST
defect, not a description defect. Prompt 2 ("une fiche") is genuinely too ambiguous in French.
The prompts must supply their own input so the test measures activation, not attachment.

## Read first
- skill/document-design-intelligence/references/activation.md, section
  "## 13-prompt activation test (run after uploading the skill)", starts at line 278.
  Prompts 2-5 are under "### Should fire".
- skill/dist/POST-UPLOAD-TESTS.md, "## Test (c) — the 13-prompt activation list", line 114.
- TESTS-FOR-USER.md (tracked by git; see the mirror instruction below).

## Deliverable (ONE)
Rewrite prompts 2, 3, 4 and 5 in activation.md so each is self-contained, and mirror the
pass/fail rule into the two test docs. Specifically:

2. French only, no English document word anywhere in the prompt. Replace the bare "fiche"
   with a concrete type, e.g. "fiche produit", and add enough French content that Claude has
   something to work with.
3. German. Add 2-3 lines of concrete client and offer facts so no clarification is needed.
4. Paste a short (4-6 line) report paragraph that visibly reads as AI-written, then the
   quality complaint.
5. Paste a short block of plain text, then the brochure ask.

Keep prompts 1 and 6-13 EXACTLY as they are.

Rewrite the **Pass**/**Fail** lines for 2-5 to this rule, in your own wording:
- A clarifying question is a PASS only if it shows document-design framing — it asks about
  format, layout, page count, ATS, branding, or print.
- A generic "what would you like?" with no design framing is a FAIL.
- Producing plain prose with no layout/library reasoning is a FAIL.

Then mirror the change:
- skill/dist/POST-UPLOAD-TESTS.md Test (c): it points at activation.md rather than repeating
  the prompts, so add the same clarifying-question pass rule there and note that prompts 2-5
  now carry their input inline and need no attachment.
- TESTS-FOR-USER.md is TRACKED by git, and it currently has NO 13-prompt activation section
  (its "Test 3 — ENS activation" at line 84 is a different skill's test — leave it alone).
  Add a new short section "## Test 11 — 13-prompt activation list" just before the "## Results"
  heading (line 452), pointing at activation.md, stating the clarifying-question pass rule, and
  saying prompts 2-5 now carry their input inline. Add a matching row `| 11 | 13-prompt
  activation list | | |` to the Results table (the table ends at line 465).
  This matters because skill/dist/ is gitignored: the POST-UPLOAD-TESTS.md edit is NOT under
  version control, so TESTS-FOR-USER.md is the tracked home for the rule.

## Constraints
- ASCII-only except where the language genuinely needs accents (French/German prompts do).
  Check your accented bytes: `python3 -c "print(open('...','rb').read()[a:b])"`.
- Do not edit SKILL.md, the description field, or anything under data/.
- Do not renumber. Prompt 2 stays prompt 2.

## Verify before you report
1. `python3 -c "import io;s=io.open('skill/document-design-intelligence/references/activation.md',encoding='utf-8').read();print(len(s))"` runs clean.
2. Prompt 2 contains no English document noun (grep it yourself).
3. Prompts 4 and 5 contain the pasted content, so a reader needs no attachment.
4. All 13 prompts still present and numbered 1-13.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: the four new
prompts verbatim, the files you touched, and anything you had to rule on yourself.
