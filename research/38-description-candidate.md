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

---

## Candidate F - honest quality-fix trigger

Status: PROPOSAL ONLY, same as Candidate B above. SKILL.md was not touched.
Candidate B (sections 1-6) stands unchanged and remains the unapplied fallback for
the "activate before the content arrives" failure. F is a separate, independent
edit addressing a different defect. Applying one does not require the other.

### F.0 The defect

The clause `quality fixes: looks like AI, looks generic, make it professional, fix
the layout` reads as a promise about prose. Activation prompt 4 failed because
Claude went looking in the skill for rules on fixing AI-sounding WRITING and found
none, which was the correct reading of the description and the correct report of
the skill's contents. `data/base` covers layout, typography, colour, print and ATS.
It holds nothing about wording, tone, or sentence rhythm. The trigger has to stop
promising what the data cannot deliver.

Two words carry the false promise. `quality fixes` is an unbounded scope header:
prose quality is quality. `make it professional` is the one list item that is
unbounded standing alone; the other three (`looks like AI`, `looks generic`, `fix
the layout`) all already lean visual through the verb "looks" or the noun "layout".

### F.1 The minimal rewording

Recommended (Candidate F, +8 characters):

```
appearance fixes: looks like AI, looks generic, make it look professional, fix the layout
```

Two changes: `quality` -> `appearance` in the header, and `make it professional` ->
`make it look professional` in the list. Nothing else moves. All four trigger
utterances survive verbatim or with one word inserted, so no keyword match is lost.

**I am not recommending the lead's sketch, and the reason is substantive.** The
sketch was `quality fixes: layout looks like AI, looks generic, make it look
professional, fix the layout`. It narrows the promise to the word "layout", but
layout is only one of the five things `data/base` actually covers. Typography,
colour, print and ATS are not layout. Narrowing to "layout" swaps a promise that is
too broad for one that is too narrow, and it leaves the unbounded header word
`quality` in place, which is where most of the prose leak comes from. "Appearance"
is the accurate scope: it is close to the union of what the data covers, and it
still excludes wording.

I also considered header-only (`appearance fixes:` with `make it professional`
left alone, +3 characters). It is more minimal and probably sufficient, because the
header scopes the list. It was rejected because that sufficiency is an assumption
about how a model reads a colon-list, and I cannot test it from here. Five extra
characters buy independence from the assumption.

| Variant | Text of the clause | Description length | Headroom |
| --- | --- | --- | --- |
| Current (shipping) | `quality fixes: ... make it professional, ...` | 823 | 200 |
| F-min (header only) | `appearance fixes: ... make it professional, ...` | 826 | 197 |
| **F (recommended)** | `appearance fixes: ... make it look professional, ...` | **831** | **192** |
| Lead's sketch | `quality fixes: layout looks like AI, ... make it look professional, ...` | 835 | 188 |

The lead can drop to F-min for 5 characters if headroom ever gets tight. It should
not; there is 192 characters of it.

### F.2 The exact edit

Replace this substring (81 characters, occurring exactly once in the description
and exactly once in the whole of SKILL.md):

```
quality fixes: looks like AI, looks generic, make it professional, fix the layout
```

with this substring (89 characters):

```
appearance fixes: looks like AI, looks generic, make it look professional, fix the layout
```

Occurrence counts were checked with Python `str.count()`, not by eye. The
replacement contains no double-quote, no backslash and no newline, so the
double-quoted YAML scalar in the frontmatter still parses unchanged.

### F.3 Full resulting description, one line

```
Creates and fixes print/office documents: CVs, resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht. Triggers: make me a CV, write a note interne, turn this into a brochure, I need slides for Monday, format this report, fais-moi une fiche, erstelle ein Angebot; appearance fixes: looks like AI, looks generic, make it look professional, fix the layout. Applies sourced layout, typography, color, print, and ATS rules. When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a plain conversion or edit with no design ask, use that format's own skill instead. Not for web or app UI/UX design (use UI/UX Pro Max for screens).
```

**831 characters.** Cap is 1023. **Headroom: 192 characters.**

Byte note, new and worth recording: the current description is 823 characters but
825 BYTES in UTF-8, the two extra bytes being the accents in "dépliant" and
"présentation". That is a second, simpler explanation for the 825 figure in
activation.md than the validated/sourced word delta given in section 1 above. Both
arrive at 825, so the figure alone cannot tell them apart. It changes nothing here:
under a byte reading F is 833 with 190 headroom, and F plus B is 995 with 28.
Neither reading comes close to the cap.

### F.4 Do B and F compose?

**Yes, and in either order.** They touch disjoint text and neither breaks the
other's anchor.

- F rewrites inside the quality-fix clause and stops before the final `fix the
  layout. `.
- B is inserted immediately AFTER `fix the layout. `, which F leaves byte-identical
  and which still occurs exactly once in the F-modified description (verified with
  `str.count()`).

| Applied | Characters | UTF-8 bytes | Headroom (chars) |
| --- | --- | --- | --- |
| Neither (today) | 823 | 825 | 200 |
| B only | 985 | 987 | 38 |
| F only | 831 | 833 | 192 |
| **B and F** | **993** | **995** | **30** |

B's placement argument in section 2 is unaffected: the new sentence still sits
after the trigger enumeration and ahead of both boundary sentences.

### F.5 Risk

Does narrowing to appearance lose real activations? One class, and losing it is the
point: a user who says "this cover letter sounds like AI, rewrite the wording"
currently fires this skill, which then has nothing to offer them. That is a false
activation, not a lost one. Removing it is the fix, not the cost. Every genuine
appearance request still hits a verbatim trigger utterance.

On revised prompt 4 I have to answer conditionally, because the brief bars me from
`references/activation.md` while another worker is in it, so I have not read the
rewrite. If the revised prompt describes how the document LOOKS, it fires under F:
all four trigger utterances survive, and "appearance" matches it more tightly than
"quality" did. If the revised prompt still names writing, wording or tone, F
correctly does NOT fire. Read that second branch as F working, not as F failing.

Is F unnecessary? No, but it is not what makes prompt 4 pass either, and those are
different questions. If prompt 4 is rewritten to describe appearance it will pass
against the CURRENT description too, so F is not needed for a green test. F is
needed because the shipping description promises prose fixes the skill cannot
perform, and that is a user-facing defect whether or not any test catches it. It
costs 8 characters and it narrows the trigger rather than widening it, so unlike B
it carries no over-trigger risk and needs no regression re-run of prompts 10 and
11. **Recommendation: apply F on its own merits regardless of how the revised
prompt 4 scores. Keep B held back under its existing section 6 verdict.**

---

## Candidate G - the v0.2 trigger-noun gap

Status: PROPOSAL ONLY. SKILL.md was not touched. B remains parked; F is applied
and live at 831 characters, and G is drafted against F, not against the pre-F
823-character text. Applying G does not require B and is incompatible with it
(see G.7).

### G.0 The defect

v0.2 added section guidance for fifteen document families. Nobody widened the
description's noun list, so `invoice`, `memo`, `proposal`, `one-pager`,
`facture`, `devis`, `rapport`, `Rechnung` and `Formular` appear nowhere in the
only string that decides whether this skill ever runs. The acceptance run
failed on prompts 1-5 with no design skill firing at all. F narrowed the
trigger; G is the opposite operation, and section G.8 is the important part of
this candidate.

### G.1 Part A - the matching rule

Everything below was computed, not read off by eye, against the description
read out of `SKILL.md`'s frontmatter at runtime. Five rules, each chosen to
*under*-report coverage rather than over-report it:

1. **Positive region only.** Matching stops at `When a specific file format`.
   The deferral and UI/UX sentences are the boundary that tells the model NOT
   to fire, and `PowerPoint`, `.docx` and `.pptx` occur only there. Counting
   them would have scored `slide-deck-projection` as covered by the sentence
   that silences it. This correction alone moved three doctypes from covered
   to generic.
2. **Token-level, never substring.** `brief` does not match inside `briefing`;
   `gate` does not match inside `gatefold`. A keyword phrase hits only as a
   contiguous run of whole tokens.
3. **Folded, then singularised.** Diacritics stripped (`depliant` matches
   `dépliant`), case dropped, and a conservative English plural rule so the
   description's `brochures` matches the CSV's `brochure`. Acronyms and region
   codes (`ats`, `us`, `uk`, `gcc`) are never singularised.
4. **Whole item versus fragment.** A keyword scores `own` only when it equals a
   whole comma- or semicolon-delimited item, or a whole trigger utterance. A
   phrase found only *inside* a longer item is a fragment and scores `gen`.
   This is what keeps `memo-internal` honest in English: the token `note` is
   present, but only inside the French item `note interne`.
5. **Shared nouns are generic by construction.** A keyword listed by more than
   one doctype cannot tell those doctypes apart, so it scores `gen`, not `own`.
   `brochures` cannot distinguish tri-fold from gate-fold; `reports` cannot
   distinguish short from long-form.

Display names are matched as the head phrase before `--` or `(`, split on `/`,
plus that phrase's final token, so `Formal business letter` is credited to the
description's `letters`. A display-name hit is always `gen` - it is the family
name, not the doctype's own noun.

Language is assigned per keyword phrase, not per doctype. A phrase counts for
French or German only if it contains a token exclusive to that language;
otherwise it counts as English. Thirteen loanwords are credited across
languages by an explicit declared list (`cv`, `flyer` and `brochure` to French,
`poster`, `whitepaper`, `handout` and `deck` to German, and so on) rather than
by guesswork. That list is the softest part of the analysis and is the first
thing to challenge if a number here looks wrong.

### G.2 Part A - the gap table

`own` = the doctype's own noun or trigger utterance is present. `gen` =
reachable only through a broader parent noun. `--` = nothing at all. Each cell
is `en/fr/de`.

| doc_key | structure key | today (F) | under G |
| --- | --- | --- | --- |
| `cv-us` | `cv-experienced` | gen/gen/gen | gen/gen/gen |
| `cv-uk` | `cv-experienced` | own/gen/gen | own/gen/gen |
| `cv-eu-generic` | `cv-experienced` | gen/gen/gen | gen/gen/gen |
| `cv-eu-europass` | `cv-experienced` | gen/--/-- | gen/--/-- |
| `cv-dach` | `cv-experienced` | gen/--/own | gen/--/own |
| `cv-france` | `cv-experienced` | gen/gen/gen | gen/gen/gen |
| `cv-gulf-gcc` | `cv-experienced` | gen/gen/gen | gen/gen/gen |
| `cv-generic` | `cv-experienced` | gen/gen/gen | gen/gen/gen |
| `cv-academic` | `cv-academic` | gen/--/-- | gen/--/-- |
| `cover-letter` | `cover-letter-standard` | own/--/-- | own/--/-- |
| `letter-formal` | `letter-standard` | gen/own/-- | gen/own/-- |
| `memo-internal` | `memo-standard` | gen/own/-- | own/own/own |
| `form-handfilled` | `form-standard` | own/own/-- | own/own/own |
| `brochure-trifold-letter` | `brochure-3panel` | gen/own/gen | gen/own/own |
| `brochure-trifold-a4` | `brochure-3panel` | gen/gen/-- | gen/gen/-- |
| `brochure-gatefold` | `brochure-gatefold` | gen/--/-- | gen/--/-- |
| `brochure-flyer-letter` | `flyer-single-sheet` | gen/gen/gen | gen/gen/gen |
| `brochure-flyer-a4` | `flyer-single-sheet` | gen/gen/gen | gen/gen/gen |
| `poster` | `poster-single-canvas` | own/own/own | own/own/own |
| `report-short` | `report-short` | own/--/own | own/own/own |
| `report-long-toc` | `report-long-toc` | gen/--/-- | gen/--/-- |
| `whitepaper` | `whitepaper-standard` | own/--/own | own/--/own |
| `proposal` | `proposal-standard` | --/--/own | own/--/own |
| `quote-devis` | `invoice-standard` | own/--/-- | own/own/-- |
| `slide-deck-projection` | `deck-standard` | gen/gen/gen | gen/gen/gen |
| `slide-deck-document` | `deck-standard` | gen/--/-- | gen/--/-- |
| `slide-deck-handout` | `deck-standard` | gen/--/-- | gen/--/-- |
| `one-pager` | `one-pager-standard` | --/--/-- | own/--/-- |
| `infographic` | `(none)` | --/--/-- | --/--/-- |
| `invoice-tabular` | `invoice-standard` | --/--/-- | own/own/own |

Headline counts across all thirty doctypes:

| | English | French | German |
| --- | --- | --- | --- |
| own noun today (F) | 7 | 5 | 5 |
| generic only today | 19 | 10 | 10 |
| nothing at all today | 4 | 15 | 15 |
| own noun under G | 11 | 8 | 9 |
| nothing at all under G | 1 | 12 | 12 |

Three doctypes are invisible in all three languages today: `one-pager`,
`invoice-tabular` and `infographic`. G fixes the first two. `infographic` has
no Structure Key, is not one of the fifteen v0.2 families, and is deliberately
left alone.

Two results worth reading before these numbers are quoted anywhere:

- **`letter-formal` is a CSV defect, not a description defect.** The
  description already carries the noun `letters`. That row's Keywords are all
  two-word (`business letter`, `formal letter`, `write a letter`), so a strict
  keyword match scores English as nothing; it is credited `gen` above only
  through the display-name head noun. **Recommendation: add the bare token
  `letter` to `letter-formal`'s Keywords in `doctypes.csv`.** That costs zero
  description characters and is strictly better than spending them.
- **The `gen` column is not a pass.** Fourteen doctypes never score `own` in
  any language. `brochure-gatefold` is reachable only as "a brochure",
  `report-long-toc` only as "a report", all three deck variants only as "slide
  decks". Those families are told apart by page format and structure rather
  than by trigger words, so this is acceptable - but it has to be stated out
  loud, which is what the permanent test in G.9 forces.

### G.3 Part B - the exact edit

Two insertions, no restructuring. Both anchors occur exactly once in the
description and exactly once in the whole of `SKILL.md`, checked with
`str.count()`.

**Insertion 1, the noun list.** After `Lebenslauf, Angebot, Bericht` and before
its full stop, insert this 92-character substring:

```
, invoice, memo, proposal, one-pager, facture, devis, rapport, Rechnung, Formular, Broschüre
```

**Insertion 2, the trigger list.** After `erstelle ein Angebot` and before the
semicolon that follows it, insert this 76-character substring:

```
, draft an invoice, write a memo, rédige une facture, erstelle eine Rechnung
```

Total inserted: 168 characters. Neither insertion contains a double quote, a
backslash or a newline, so the double-quoted YAML scalar in the frontmatter
still parses unchanged.

### G.4 Full resulting description, one line

```
Creates and fixes print/office documents: CVs, resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht, invoice, memo, proposal, one-pager, facture, devis, rapport, Rechnung, Formular, Broschüre. Triggers: make me a CV, write a note interne, turn this into a brochure, I need slides for Monday, format this report, fais-moi une fiche, erstelle ein Angebot, draft an invoice, write a memo, rédige une facture, erstelle eine Rechnung; appearance fixes: looks like AI, looks generic, make it look professional, fix the layout. Applies sourced layout, typography, color, print, and ATS rules. When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a plain conversion or edit with no design ask, use that format's own skill instead. Not for web or app UI/UX design (use UI/UX Pro Max for screens).
```

**999 characters**, 1,003 bytes in UTF-8 - the four accented characters cost
one byte each.

### G.5 Headroom

The cap is 1,023; the claude.ai upload UI enforces "under 1024".

| | characters | UTF-8 bytes | headroom (chars) |
| --- | --- | --- | --- |
| F, live today | 831 | 833 | 192 |
| **G (recommended)** | **999** | **1003** | **24** |
| G plus B | 1161 | 1165 | **-138** |
| G with every noun I wanted (G.6) | 1081 | 1089 | -58 |

Twenty-four characters is thin. It is enough, but it means the description is
now a budgeted resource: the next family added cannot simply append a noun.

### G.6 The judgement: it does not all fit, and here is what I dropped

**The description cannot carry fifteen families' nouns in three languages.**
The full set I would write with no cap comes to 1,081 characters, 58 over. That
is a finding, not a failure, and per the brief I am naming the cuts rather than
silently keeping whatever fit.

Dropped, in the order I would restore them if characters ever come back:

| dropped | family | why it survives without it |
| --- | --- | --- |
| `Präsentation`, `Folien` | deck-standard (de) | German users type the loanword *Deck*, and acceptance prompt 14 itself says "Pitch-Deck". `slide decks` carries it. Cost to restore: 14. |
| `Anschreiben` | cover-letter (de) | Genuinely uncovered in German; acceptance prompt 15 is English. Cost: 13. The weakest of these drops. |
| `lettre de motivation` | cover-letter (fr) | The same gap in French, and the most expensive single noun at 22 characters. |
| `livre blanc` | whitepaper (fr) | French technical writing uses *whitepaper* directly often enough, and that noun is already present. Cost: 13. |
| `proposition` | proposal (fr) | `proposal` and `Angebot` are both present; French is the one hole. Cost: 13. |
| `Brief`, `Geschäftsbrief` | letter-standard (de) | Uncovered in German. See the `letter-formal` CSV note in G.2 - fix the row first, then reconsider. |
| `Plakat` | poster (de) | German uses *Poster* freely and it is present. Low risk. |
| `gatefold`, `Wickelfalz` | brochure-gatefold | Panel count is a page-format dimension. Declared generic-covered instead. |
| `infographie`, `Infografik` | infographic | Out of v0.2 scope - no Structure Key. |

The rule I applied, per Addendum 1: English plus the one non-English noun users
actually type, never three weak ones. `Rechnung`, `facture`, `devis` and
`rapport` are in because those are the words the pilot's users type, and
because four of the fifteen acceptance prompts are French and five are German.
`Präsentation` is out because the German prompt in that family does not use the
word.

**A cheaper alternative to weigh before spending characters.** Several of the
fifteen families would also be reached by editing `doctypes.csv` instead of the
description - adding `letter` to `letter-formal`, adding `deck` to the German
side of the deck rows, and so on. That does not help activation, since the
model never sees the CSV before firing, but it does make this analysis and its
test agree with reality. The description edit is still required; the CSV edit
is free and should happen as well.

### G.7 Does G compose with B?

**No. Shipping G kills B.** They do not conflict textually - B inserts after
`fix the layout. `, which G leaves byte-identical, and both anchors survive -
but G plus B is 1,161 characters against a 1,023 cap, 138 over. No arrangement
of the two fits.

If B is ever revived, one of three things has to give: B's sentence must lose
roughly 140 characters (it is 161, and section 5 of this file argues its
load-bearing phrase cannot be trimmed), or G must fall back to its English-only
core, or the noun list must be restructured - which is what this candidate was
told not to do, and which would invalidate F's and B's placement arguments at
the same time. Treat G and B as mutually exclusive and choose between them
rather than planning to apply both.

### G.8 Risk: G widens the trigger

F narrowed the promise and carried no over-trigger risk. G is the opposite
operation, so this is the section to read carefully. Ranked by how likely each
is to cost a currently-passing activation prompt:

- **`one-pager` against prompt 10. HIGHEST RISK, and the one I would argue
  about.** "Give me a one-pager on X" is, in ordinary usage, a request for a
  *summary*, not for a designed document. Prompt 10 ("Summarize this PDF
  research paper in three bullet points") is the case `references/activation.md`
  itself calls the sharpest over-trigger test. `one-pager` sits in the noun
  list as a bare noun with no create-or-fix verb attached to protect it, unlike
  every trigger phrase G adds. I recommend it anyway, because
  `one-pager-standard` is one of the fifteen v0.2 families and is invisible in
  all three languages without it - but if prompt 10 regresses after G, this is
  the word to remove first, and removing it costs nothing else.
- **The transactional cluster - `invoice`, `Rechnung`, `facture`, `devis`.
  MODERATE, and a different failure mode.** These nouns attract arithmetic and
  pricing questions ("what is the VAT on this invoice", "check these line-item
  totals") where the user wants a calculation, not a layout. The skill would
  fire with nothing relevant to offer. This is a new false-activation class
  that does not exist today, and no current activation prompt tests for it.
  **Recommendation: add a should-not-fire prompt for it**, something like
  "Calculate the VAT on this invoice: three line items at ...", so the class is
  measured rather than assumed.
- **`memo` against prompt 11. LOW-MODERATE.** Prompt 11 turns rough notes into
  a Word document, and rough notes are memo-shaped input. The format-deferral
  sentence is what holds there and G does not touch it, but prompt 11 was
  already flagged as B's highest risk and G nudges the same boundary from the
  other side. Re-run 11 after applying G.
- **`proposal` against prompt 9. LOW.** Prompt 9 asks for a marketing strategy.
  `proposal` is a document noun and `strategy` is not, so the boundary holds.
  Note that I deliberately did not add `pitch document` or `pitch deck`, which
  would have edged into prompt 9's territory for no coverage gain.
- **Prompts 6, 7, 8, 12 and 13. NEGLIGIBLE.** G adds only document nouns and
  create-verb trigger utterances. It does not touch the UI/UX boundary, the
  coding case, or the format-conversion case.

**The four trigger phrases are the safe part of G.** `draft an invoice`,
`write a memo`, `rédige une facture` and `erstelle eine Rechnung` each carry an
explicit create verb, which is precisely what stops them landing on prompt 10.
If characters ever get tight, cut a bare noun before cutting one of these.

**Nothing in G is too broad to ship**, with one qualification: `one-pager` is
the single addition I would call genuinely arguable, for the reason above.
Everything else is a concrete document noun.

**A hypothesis the lead needs, which I cannot verify from here.** None of
acceptance prompts 1-5 names Word, PowerPoint, `.docx` or `.pptx`, yet Claude's
stated reason for not firing was "I was doing a clean Word file as per the
request". Either the run differed from the written prompt, or the deferral
sentence is being read far more broadly than its text says, as "any office
document belongs to the built-ins". If it is the second, **G is necessary but
not sufficient**: adding nouns will not make prompts 1-5 fire, and G will be
scored a failure when the real defect is the deferral sentence's scope. That
sits outside the two defects the brief assigns, so it needs to be visible
before G is judged.

### G.9 The permanent test

`scripts/tests/test_description_coverage.py`, new, six tests. It reads
SKILL.md's frontmatter and `doctypes.csv` at runtime, so it fails the moment
either changes. The rule: every doctype with a non-empty Structure Key must
have one of its Keywords phrases, or its display-name noun, present in the
description's positive region, folded, in at least one language.

`GENERIC_COVERED` is the part that matters. Fifteen doctypes reachable only
through a parent noun are listed there with the noun each rides on, and that
noun's continued presence is itself asserted - so the list is a check, not a
comment. `PENDING_CANDIDATE_G` holds the two doctypes G exists to fix,
`invoice-tabular` and `one-pager`, as an explicit named xfail.

**The suite is green today by design, and that is deliberate.** The honest
statement of the current state is "two known gaps, named, with the fix drafted"
rather than a permanently red suite that everyone learns to ignore. It goes red
on all of these:

| change | test that fails |
| --- | --- |
| add a family with no matching noun | `test_every_structured_doctype_is_reachable` |
| remove `whitepapers` or `quotes` from the description | `test_every_structured_doctype_is_reachable` |
| remove `cover letters` | `test_generic_only_doctypes_are_declared` |
| remove `flyers` | reachability, **and** `test_generic_covered_parents_are_still_present` |
| apply candidate G | `test_pending_list_has_no_stale_entries` |
| push the description past 1023 characters | `test_description_still_fits_the_upload_cap` |

To verify by hand, delete `whitepapers, ` from the description and run
`pytest -q` from the skill directory. Do **not** use `posters` or `reports` for
that check: `poster` stays reachable through the French `affiche`, and `report`
through the trigger `format this report`, so the suite stays green - correctly.

The last row is the self-clearing mechanism. When G is applied,
`test_pending_list_has_no_stale_entries` goes red and names the two doctypes,
forcing whoever applies it to empty the list so the rule guards them for real.

### G.10 Verdict

**Apply G, with `one-pager` flagged for removal if prompt 10 regresses.** It is
the only thing that can make prompts 1-5 fire. No change to `data/base`, the
router, or the reference files can substitute, because a skill that never
activates never has its body read.

Three conditions on that recommendation:

1. **Re-run prompts 10 and 11 before re-running 1-5.** Those are the two that
   can regress, and 10 is the one `one-pager` endangers.
2. **Decide G or B, not both.** They do not fit together (G.7).
3. **Settle the deferral-sentence question first** (G.8, last bullet). If the
   deferral sentence is what silenced prompts 1-5, G will not fix them and will
   be blamed for it.

Confidence: high on the table and the measurements, which are computed and
reproducible; moderate on the loanword language credits in G.1; low on whether
G alone makes prompts 1-5 pass, for the reason in G.8.

---

## Candidate H - is the deferral sentence over-reaching?

Status: PROPOSAL ONLY. SKILL.md was not touched. READ-ONLY analysis.

### H.0 The hypothesis, checked first

Confirmed against `research/44-v02-acceptance.md` prompt 1 (the German
invoice request, "Kannst du mir daraus eine ordentliche Rechnung machen?"):
it names no file format, no ".docx", no "Word", no "PowerPoint" anywhere in
its text. The same holds for prompts 2-5 (French letter, English memo,
German form, English proposal) - none of the fifteen v0.2 prompts names a
file format. If the skill fired on none of them and Claude's own stated
reason was "I was doing a clean Word file as per the request," that reason
cannot be a correct reading of any of these five prompts' actual words. The
hypothesis is **CONFIRMED as stated**: something is producing a "Word file"
belief that the prompts themselves do not support, and the deferral
sentence is the only part of `SKILL.md` that mentions "Word" at all.

### H.1 The sentence, quoted exactly as it ships

```
When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a
plain conversion or edit with no design ask, use that format's own skill
instead.
```

### H.2 Every phrase a model could read as over-reach

Read close, in order, with the specific failure each one enables:

1. **"is named" - passive, agentless.** The sentence never says *who* does
   the naming. Grammatically the condition is satisfied by the format being
   named by anyone, anywhere in the exchange - including the model's own
   silent decision about what format it intends to produce. Nothing in the
   text blocks the reading "a format is named [by me, the model, as my
   output plan]" from satisfying "is named." This is the single most likely
   mechanism behind "I was doing a clean Word file as per the request": the
   request never named Word, but the model's own default assumption about
   how to deliver a business document did, and the passive voice does not
   distinguish the two.
2. **"(Word, PowerPoint, .docx, .pptx)" as a bare parenthetical list.**
   Stated with no framing other than "named," these four nouns are the only
   place in the whole description where "Word" or "PowerPoint" appear. A
   model that has already decided (for any reason) that its output will be
   a Word-shaped document has a ready-made textual anchor to associate that
   decision with this clause, purely by word-overlap, independent of
   whether the *user* said "Word."
3. **"for a plain conversion or edit with no design ask" - a squishy gate
   that structural document families satisfy by default, not by
   exception.** "Design ask" reads naturally as branding, color,
   typography, or print-finish language. None of the fifteen v0.2 families'
   prompts use that vocabulary - they ask for correct *structure*
   (issuer-before-totals, agenda-after-cover, signature-before-date), which
   this skill's actual v0.2 value-add is built entirely around. If "design
   ask" is read at ordinary-language width, turning raw facts into "an
   ordentliche Rechnung" or "a proper internal memo" scores as "no design
   ask" - a plain edit - even though it is exactly the structural work this
   skill exists to do. The gate does not distinguish "no design ask" from
   "no design ask *because this family's design work is structural, not
   decorative*."
4. **"use that format's own skill instead" - "instead" as total
   replacement, not "instead as renderer."** Elsewhere in `SKILL.md` (the
   Workflow section, `references/activation.md` prompt 12) `.docx`/`.pptx`
   are explicitly *renderers this skill calls*, not competitors for the
   whole request. This sentence is the only place that frames the
   relationship as full substitution ("instead"), which - combined with
   item 1's agentless "is named" - is what lets a model conclude "the
   output is Word-shaped, so the *entire task*, not just rendering, belongs
   to the other skill."

Items 1 and 3, compounding, are the load-bearing defect: item 1 lets the
model's own rendering default silently satisfy "named," and item 3 lets a
purely structural request silently satisfy "no design ask." Neither
requires the user to have said "Word" or "PowerPoint" at all, which is
exactly what prompts 1-5 demonstrate.

### H.3 Replacement sentence

```
Creating any document type above is still this skill's job even as Word or
PowerPoint; defer to that format's own skill only when the user names it
for a plain conversion or edit with no design ask.
```

- **Fixes item 1** by making the agent of naming explicit ("the user
  names it," not "is named") - the model's own choice of output format no
  longer has any textual claim to satisfying the condition.
- **Fixes item 3's blast radius, not its wording**, by leading with an
  unconditional positive claim ("creating any document type above is still
  this skill's job") that the deferral clause must now override rather
  than default past. A model no longer reaches "no design ask, so this
  isn't mine" as the path of least resistance - it has to affirmatively
  clear the "user names it" bar first.
- **Keeps the plain-conversion carve-out intact and unweakened.** "Plain
  conversion or edit with no design ask" survives verbatim from the
  original, so prompt 13 ("Just convert this .docx file to a PDF, don't
  change anything") is untouched: format named, plain conversion, no
  design ask, no restructuring - defers exactly as before.
- **Does not weaken item 4** ("instead") by itself - I judged item 4 lower
  priority than 1 and 3 (see H.2) and left "own skill" out of scope for
  this edit to keep the sentence's growth small; if a future review wants
  to also state that the deferral is for rendering specifically, that is a
  separate, additive change, not required to fix prompts 1-5.

### H.4 Measured length, against G's headroom

```
orig  (shipping today): 157 characters
H (replacement)        : 198 characters
delta                  : +41 characters
```

Computed with Python `len()`, not by eye.

- **Against F alone (831, live today, G not yet applied):** F+H = 872
  characters. Headroom under the 1,023 cap: **151 characters.** Fits
  cleanly with no trade needed if G is never applied.
- **Against G (999, drafted, not applied, 24 characters of headroom):**
  G+H = 1,040 characters - **17 characters over the cap.** H does **not**
  fit alongside G as G is currently drafted. Per the brief, here is the
  exact trade, not an assumption that G shrinks on its own:

  **Cut G's insertion 2 in full** - the 76-character trigger-phrase list
  `, draft an invoice, write a memo, rédige une facture, erstelle eine
  Rechnung` - and keep G's insertion 1 (the noun list: `invoice, memo,
  proposal, one-pager, facture, devis, rapport, Rechnung, Formular,
  Broschüre`) untouched.

  **Why this is the right item to cut, not an arbitrary one:** G's own
  matching methodology (G.1, rule 4 - "a keyword scores `own` only when it
  equals a whole comma- or semicolon-delimited item") already credits
  `invoice`, `memo`, `Rechnung`, and `Formular` as `own`-matching the
  moment they appear as bare comma-delimited items in the noun list. The
  trigger phrases in insertion 2 restate those same nouns inside longer
  utterances (`draft an invoice` still contains the whole item `invoice`;
  `erstelle eine Rechnung` still contains `Rechnung`) - by G's own rules
  they add no doctype that the noun list alone does not already cover.
  Checked directly: recomputing G's gap table (G.2) with insertion 2
  removed changes no cell. This is the one 76-character block in G that is
  reinforcement, not coverage, which makes it the correct thing to trade
  for H's 17-character shortfall rather than cutting into insertion 1,
  where every noun (including `Rechnung` and `Formular`, which are the
  exact nouns prompts 1 and 4 of the v0.2 set need) is load-bearing.

  Result: G (minus insertion 2, 923 characters) + H = **964 characters,
  59 characters of headroom.** Verified with `len()` against the exact
  resulting string, not estimated.

### H.5 Risk to activation prompts 11, 12, 13

- **Prompt 11 ("Turn my rough notes into a Word document.") - the one
  genuine new risk, MODERATE.** Walking the sentence: the user's own words
  name "Word document" (clears H's tightened bar), it is a plain edit of
  notes into a document, and no design language appears - so the "only
  when" exception still holds and the sentence still says to defer.
  Outcome should be unchanged. The risk is not in the logic, it is in
  emphasis: H opens with an unconditional affirmative claim ("creating any
  document type above is still this skill's job") in the same sentence a
  model is now reading for a memo-shaped request. A reader would know this
  broke if the model's response shows DDI resolving structure or asking a
  clarifying design question for prompt 11 instead of staying silent while
  `docx` responds - that is the regression signal, not a changed final
  file format.
- **Prompt 12 ("two-page CV, make it look professional...") - unaffected,
  slightly reinforced.** No format is named, so the exception clause never
  engages regardless of wording; the new leading positive claim only makes
  the "this is ours" reading more explicit. No new risk.
- **Prompt 13 (".docx to PDF, don't change anything") - unaffected, LOW.**
  Not a "creating" case (it edits an existing artifact, not one of the
  document types above), format is named, plain conversion, explicit
  no-change instruction. A reader would know this broke only if DDI
  produced any layout/design reasoning at all for a bare format-conversion
  request with an attachment - the same signal as before H.

### H.6 Verdict

Apply H. It targets the actual mechanism (an agentless "is named" plus a
loosely-scoped "no design ask" that structural, non-decorative requests
satisfy by default) rather than the trigger-noun gap G already addresses -
the two are complementary, not competing: G makes the model recognize the
words describing these document families; H stops the model from silently
exempting them once recognized. Confidence: high that prompts 1-5's
literal text supports the hypothesis (checked directly against
`research/44-v02-acceptance.md`); moderate that H alone, without G, is
sufficient to make 1-5 fire, since G still supplies nouns (`Rechnung`,
`Formular`, `invoice`, `memo`, `proposal`, `one-pager`) that are absent
from the description today and that the model must first recognize before
H's fixed deferral logic can even be consulted. **Recommendation: apply
both, with the insertion-2 trade in H.4 if character budget forces a
choice.** Re-run prompts 1-5 and 11 first, since 11 is H's only named risk
and 1-5 are the prompts both candidates jointly target.
