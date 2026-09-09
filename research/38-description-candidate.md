# 38 - Description candidate: activate before the content arrives

Status: PROPOSAL ONLY. SKILL.md was not touched. Nothing here is applied.
Prepared as a fallback in case the revised activation prompts 3, 4 and 5 still fail.

Measured, not quoted: the description now shipping in
`skill/document-design-intelligence/SKILL.md` is **823 characters**.
`references/activation.md` says 825, and quotes a block reading "Applies validated
layout" where SKILL.md actually ships "Applies sourced layout". That single word
(9 chars vs 7) is the whole 825-vs-823 delta. The 667 figure is the pre-deferral-
sentence description and is two revisions stale. Counts in this file were taken
with Python `len()` on the exact string read out of SKILL.md.

## 1. The candidate sentence

```
Handles a request to create or fix a document even when the content, file, or details are not yet provided, activating first and then asking for what is missing.
```

161 characters including the trailing period.

Three changes against the lead's example ("Use this skill first even when the
content or file is not yet provided; it decides what to ask for."):

- **Third person, verb-initial.** The lead's version is second-person imperative
  ("Use this skill"). Every other sentence in this description is third person and
  verb-initial (Creates, Applies, Handles), which activation.md records as a
  deliberate choice following Anthropic's own guidance. Keeping the voice
  consistent costs nothing.
- **"content, file, or details", not "content or file".** Prompt 3 ("Erstelle mir
  ein Angebot fuer diesen Kunden") has no attachment to be missing. What Claude
  asked for there was details about the client. A clause scoped to a missing file
  covers prompts 4 and 5 squarely and prompt 3 only by a stretch, so the missing
  thing is widened to cover all three failures.
- **"a request to create or fix a document" as the scope.** This is the load-
  bearing phrase. It is not decoration: it is what stops the sentence from reading
  as "fire whenever something is missing". See section 5.

## 2. Placement

Immediately after `...quality fixes: looks like AI, looks generic, make it
professional, fix the layout.` and immediately before `Applies sourced layout,
typography, color, print, and ATS rules.`

Two reasons, both about what sits on either side:

- **Adjacent to the trigger list.** "a request to create or fix a document" needs
  the trigger enumeration in front of it to be read as a qualifier rather than a
  new, broader claim. Put it any later and it reads as a standalone rule.
- **Ahead of both boundary sentences.** The format-deferral sentence (Word,
  PowerPoint, .docx, .pptx) and the UI/UX Pro Max exclusion both come after it and
  therefore still read as overriding qualifiers. That ordering is the only thing
  protecting prompts 11 and 13. Moving the new sentence to the end of the
  description would put it after the exclusions and invert that relationship.
  Do not move it.

## 3. Full resulting description, one line

```
Creates and fixes print/office documents: CVs, resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht. Triggers: make me a CV, write a note interne, turn this into a brochure, I need slides for Monday, format this report, fais-moi une fiche, erstelle ein Angebot; quality fixes: looks like AI, looks generic, make it professional, fix the layout. Handles a request to create or fix a document even when the content, file, or details are not yet provided, activating first and then asking for what is missing. Applies sourced layout, typography, color, print, and ATS rules. When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a plain conversion or edit with no design ask, use that format's own skill instead. Not for web or app UI/UX design (use UI/UX Pro Max for screens).
```

**985 characters.** Cap is 1023 (the claude.ai upload UI rejects at 1024;
activation.md lines 10-25). Headroom: 38 characters.

Verified on the resulting string: single line, no double-quote character, no
backslash, so it still fits the existing double-quoted YAML scalar in the
frontmatter unchanged.

## 4. Rationale

Prompts 3, 4 and 5 did not fail on keyword match. In prompt 3 Claude said it would
likely use document-design-intelligence once given the details, so the trigger
words landed; what it did instead was ask a clarifying question first and never
invoke. The description is the only lever that can change that. A skill that never
activates never has its SKILL.md body read, so no instruction placed in the body,
the router, or the reference files can reach this failure. The sentence converts
"I am missing the input, so I will ask" into "I am missing the input, so I will
activate and let the skill decide what to ask for", which is also what prompt 1
already rewards.

## 5. Risk: what this could over-trigger

Blunt version first: the phrase carrying all the safety here is "a request to
create or fix a document". Strip it and this sentence is a general instruction to
fire on incomplete input, which would be a serious over-trigger. Reviewers should
treat that phrase as non-negotiable, not as filler to trim if someone later needs
characters back.

Named risks, ranked:

- **Prompt 11 - "Turn my rough notes into a Word document." HIGHEST RISK.** This
  is genuinely a request to create a document, and the notes are not attached.
  Only the format-deferral sentence keeps this skill silent. Worse, part of what
  may currently be keeping it silent is exactly the hesitation this sentence is
  designed to remove: no notes in hand, so no confident grab. The sentence does
  not touch the format boundary, but it removes a second line of defence that was
  quietly helping. Re-run 11 first after any change.
- **Prompt 10 - "Summarize this PDF research paper in three bullet points."
  MODERATE.** Nothing is attached here either, and "PDF" is a format noun, so a
  loosely worded version of this sentence would land straight on the case
  activation.md itself calls the sharpest over-trigger test. "create or fix"
  excludes "summarize" by construction, which is precisely why that wording was
  chosen over the lead's broader phrasing. Residual risk is real but second-order.
- **Prompt 13 - ".docx to PDF, don't change anything." LOW.** Format named, no
  design ask, explicit no-change instruction. Two independent barriers hold.
- **Prompts 6 and 7 - UI/UX cases. LOW.** Prompt 7 has nothing attached, but
  "document" excludes a landing page hero. The domain boundary is untouched.
- **Prompts 8 and 9 - Python refactor, marketing strategy. NEGLIGIBLE.** Neither
  is a document request under any reading.
- **Prompt 12** is unaffected and mildly helped.

## 6. Verdict and recommendation

Ship this only if the revised prompts 3, 4 and 5 still fail. Do not ship it now.

The reason is a test inconsistency that should be settled before the description
is changed at all. Prompt 1's own pass criterion is "the skill activates **and
asks** about content/format" - it passes by asking. Prompts 3, 4 and 5 were marked
failed for asking. The same behavior is scored both ways in the same test file.
That points at the rubric, not at the description, and the brief already notes
that prompt 3's own transcript shows the description matching correctly.

Spending 161 of the remaining 200 characters, and accepting the prompt 11
regression risk, to correct what may be a scoring artifact is a bad trade while
the cheaper fix is still untested. If the corrected prompts pass, this file can be
closed unused.

If they still fail, take this sentence as written, and re-run prompts 11 and 10
before 1 through 5, since those are the two that can regress.
