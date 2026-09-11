# Browser smoke test — 2026-09-11

Run by the Acceptance Tester via the AionUi in-app browser against claude.ai.

## 1. Login
CONFIRMED. claude.ai/new greeted "What's cooking, yazan?" — logged in as the project user.

## 2. Skill listed
CONFIRMED. claude.ai/customize/skills -> Skills -> Yours -> "Created by you · 1":
- `document-design-intelligence`, tag "New", edited "19h ago", categories Jobs & career /
  Files & documents / Designs & media.
- Description shown starts "Creating any document type below is still this skill's job even
  as Word or PowerPoint; defer to that format's own skill only when the user names it for a
  plain conversion or edit with no design ask. Creates and fixes print/office documents: CVs,
  resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks,
  presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, lettre,
  affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht, i..." — matches
  the candidate-L wording RESUME.md records as shipped in v0.2.0.

## 3. Activation prompt
Prompt used (RESUME.md's "Prompt 1", recorded there as firing reliably): "Can you make me a
CV for a marketing coordinator role?" New chat, pasted verbatim, sent.

RESULT: did NOT visibly fire. Two turns (a UI double-send landed both), same shape each time:
Claude asked for real CV content instead of producing anything design-framed, e.g. "I still
need the actual content before I can build this — I don't want to invent a work history for
you," listing name/experience/education/target-posting as needed inputs. No skill-invocation
indicator, no mention of document-design-intelligence, no file or formatted output, in either
turn. One response also said "per your clarification rule," which points at a generic
no-fabrication behaviour (possibly the account's Memory/preference settings) rather than
anything skill-specific.

This is inconclusive by the same defect RESUME.md already names for prompts 3/4/5/12 in the
2026-09-09 run: a prompt with no real content attached is legitimately ambiguous, and asking
for details is correct generalist behaviour, not proof the skill was or wasn't considered. It
does NOT reproduce the RESUME.md claim that this exact prompt "has PASSED in every run" — that
history used inline placeholder content or accepted the offer of placeholders; this run did
neither, so it measured the same thing prompt 12 originally failed to measure, not a
regression.

## Other observations
- Session shows "You've used 75% of your weekly limit" after these two sends.
- No errors, refusals, or broken UI encountered otherwise.

## Verdict
Login: PASS. Skill listed: PASS. Activation prompt: INCONCLUSIVE (test defect — no inline
content given), not a scored PASS/FAIL under the rubric in RESUME.md's own activation
methodology.
