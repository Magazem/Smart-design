# BRIEF — Coverage — v0.2 blocker: the description noun gap

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT edit SKILL.md. Draft only — the user vetoes description changes.

## Why
The user ran v0.2 acceptance prompts 1-5 and the skill fired on NONE. Claude's own explanation:
"I was doing a clean Word file as per the request, no need for design skills."

There are two defects. The other one (the prompts pre-supply their own structure) is DDR's, in
parallel. Yours is the description. v0.2 added section guidance for 15 families but nobody
widened the trigger noun list, so Claude had no reason to fire on an invoice or a memo.

I have already confirmed the gap is real, so do not spend the brief re-proving it exists:
8 of the 30 doctypes have NO keyword token appearing anywhere in the description at all —
cv-eu-europass, cv-academic, brochure-gatefold, report-long-toc, slide-deck-handout, one-pager,
infographic, invoice-tabular. And "invoice", "facture", "rechnung", "memo", "proposal",
"one-pager", "devis" are all absent. My check was crude substring matching in English only.
Yours must be better.

## Deliverable (ONE — two parts, one file)

### Part A: the gap table
For EACH of the 30 doctypes in data/base/doctypes.csv, determine whether the description gives
Claude any reason to fire on it, PER LANGUAGE (en, fr, de). Match on the doctype's Keywords
tokens and its Display Name. Do it properly:
- token-level, not naive substring — "brief" must not count as a hit inside "briefing"
- report per language, because a family can be covered in French and invisible in German.
  memo-internal is exactly this case: "note interne" is in the description, "memo" is not.
State your matching rule in the file. A table that overstates coverage is worse than none.

### Part B: Candidate G
Draft the MINIMAL noun and trigger-phrase additions that close the gap for the 15 v0.2 families,
in all three languages. Append to the existing noun list and trigger list rather than
restructuring the description — F and B are already drafted against its current shape.
The lead's examples: "draft an invoice", "write a memo", "erstelle eine Rechnung",
"rédige une facture".

Append it to research/38-description-candidate.md as "Candidate G". DO NOT overwrite candidates
B or F. B is permanently parked; F is APPLIED and live at 831 characters.

Give, exactly as you did for F:
1. The precise substrings to insert and where.
2. The full resulting description on one line with its MEASURED length.
3. Headroom under the cap. The cap is 1023 — the claude.ai UI enforces "under 1024".
4. Whether G composes with B, should B ever be revived.
5. Risk: which of the 13 activation prompts, especially the should-not-fire set 6-10 and the
   docx handoff 11-13, does G endanger? G WIDENS the trigger, unlike F which narrowed it, so
   this section is the important one. Say plainly if you think any addition is too broad.

## A judgement I want from you, not a fill-in
If the honest answer is that the description cannot carry 15 families' nouns in 3 languages
within the character budget, say so and tell me what you would drop. Do not silently pick the
ones that fit. That is a finding, not a failure.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the gap table's
headline numbers per language, the measured length of G, the headroom, your risk verdict, and
whether everything fit.
