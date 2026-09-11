# Candidate M draft — file-not-genre mechanism (DRAFT ONLY, not applied)

Supersedes an earlier version of this file that inserted a `Triggers:` example
instead of touching the deferral sentence. The orchestrator's follow-up
correctly pointed out the brief names the deferral sentence itself as the
lever, and gave me the current (two-marker) state of the coverage test, which
changes what this draft can safely propose. This version replaces that one.

## 1. The two quotes and the mechanism they support

- P6 (rough notes -> Word, went to docx): *"Since you asked for a Word doc
  specifically, it was the clear match (its trigger criteria explicitly call
  out '.docx' requests)."*
- P4 (FR report, no skill at all, emitted Markdown): *"I chose Markdown over
  Word specifically because you didn't ask for a Word file or signal you
  needed a formal downloadable document."*

Read together: routing is gated on whether a FILE is implied, and if so, on
which FORMAT was named — not on whether a genre noun ("CV", "rapport",
"brochure") appears anywhere. P4 is the harder case (see §6). For P6, the
load-bearing detail is *how* Claude describes the loss: it names the
competing skill's own literal token, `'.docx'`, as the deciding signal. Our
deferral sentence already says "still this skill's job even as Word" — a
genre-level claim — but contains no literal `.docx`/`.pptx` token to compete
with the string Claude says actually won.

## 2. Proposed description text (exact, as it would replace the frontmatter value)

```
Creating any document type below is still this skill's job even for '.docx'/'.pptx' requests naming Word or PowerPoint; defer to that format's own skill only when the user names it for a plain conversion or edit with no design ask. Creates and fixes print/office documents: CVs, resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, lettre, affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht, invoice, memo, proposal, one-pager, facture, devis, rapport, Rechnung, Formular, Broschüre. Triggers: make me a CV, write a note interne, turn this into a brochure, I need slides for Monday, format this report, fais-moi une fiche, erstelle ein Angebot; appearance fixes: looks like AI, looks generic, make it look professional, fix the layout. Applies sourced layout, typography, color, print, and ATS rules. Not for web or app UI/UX design (use UI/UX Pro Max for screens).
```

Only the opening clause of the deferral sentence changed: `even as Word or
PowerPoint` becomes `even for '.docx'/'.pptx' requests naming Word or
PowerPoint`. Everything else, including the rest of that same sentence (the
`defer... no design ask` half), is untouched.

## 3. Character count and method

Method: read `SKILL.md` as UTF-8, apply the frontmatter regex
`^description:\s*"(.*)"\s*$` (`re.M`), take group 1, measure with Python
`len()` — codepoint count, not bytes. This is the same quantity
`test_description_coverage.py::test_description_still_fits_the_upload_cap`
checks (`len(raw) <= 1023`) and the same quantity the orchestrator's
PowerShell `$d.Length` computes; I cross-checked the current on-disk figure
against both and they agree.

- Current on-disk description: **972 characters** (975 UTF-8 *bytes* — the
  3-byte gap is exactly the three two-byte characters: é in `dépliant`, é in
  `présentation`, ü in `Broschüre`). Confirmed against the orchestrator's
  correction.
- Candidate M, same method: **1005 characters**.
- Delta: +33 characters. Headroom remaining under the 1023 cap: **18
  characters**.

## 4. Diff-in-words

**Changed:** `even as Word or PowerPoint` → `even for '.docx'/'.pptx'
requests naming Word or PowerPoint`, inside the deferral sentence only.

**Unchanged, byte-for-byte:** the entire `defer to that format's own skill
only when the user names it for a plain conversion or edit with no design
ask` half of the same sentence, the noun list, the `Triggers:` list, the
appearance-fix triggers, the "Applies sourced..." sentence, and
`NEGATIVE_SCOPE_MARKER`'s text.

**Why this follows from the quotes, not from theory:** P6 is Claude
explaining a loss in its own words, and the word it reaches for is the
competing skill's literal token, `'.docx'`, not a genre or intent word. Our
sentence asserts the same priority claim ("still this skill's job") but only
at the genre level ("even as Word"). This edit puts the same literal token
class into our own sentence, at the same point the priority claim is made,
so the two skills are competing on the same kind of signal Claude says it
actually used.

**Two alternatives considered and rejected**, both worth naming so they are
not silently re-tried later:

1. *Insert a `Triggers:` example instead of touching the deferral sentence*
   (my first draft, superseded). Rejected because the brief and the
   orchestrator both identify the deferral sentence itself, not the trigger
   list, as the untried lever — an example phrase sidesteps the sentence the
   brief says to target.
2. *Rewrite the defer condition from "no design ask" to "names no document
   type below" instead of adding the literal tokens.* I drafted this too
   (997 characters, also fits) and rejected it: replacing "no design ask"
   with "no document type below" would make the plain-conversion carve-out
   almost never trigger, since nearly any real request already names a
   document-type noun — "convert my CV to PDF" would stop deferring under
   that wording, which is a real regression on exactly the plain-conversion
   case the sentence exists to protect. Nothing in P6 or P4 argues for
   removing that carve-out, so I did not ship it. Flagging this so a future
   candidate doesn't reach for it without seeing this note.

## 5. Test-marker check

**NOT preserved — this candidate requires a paired edit to
`scripts/tests/test_description_coverage.py`.**

`NEGATIVE_HEAD_MARKER` (currently line 57) is defined as the deferral
sentence verbatim:

    NEGATIVE_HEAD_MARKER = "Creating any document type below is still this skill's job even as Word or PowerPoint; defer to that format's own skill only when the user names it for a plain conversion or edit with no design ask."

Candidate M changes that sentence, so `raw.find(NEGATIVE_HEAD_MARKER)` would
return `-1` and the test would raise `AssertionError("NEGATIVE_HEAD_MARKER
not found")` — loudly, not silently; this is the closed failure mode the
orchestrator described, not the open one from candidate H. The required
paired edit is a literal replacement of that constant's value with:

    NEGATIVE_HEAD_MARKER = "Creating any document type below is still this skill's job even for '.docx'/'.pptx' requests naming Word or PowerPoint; defer to that format's own skill only when the user names it for a plain conversion or edit with no design ask."

This constant is hand-maintained, not generated — I checked
`scripts/build_zip.py`, and the only thing it generates or stamps is the
`<!-- version: ... -->` comment line; it never touches the description or
the test file. So the correct fix is a direct hand-edit of the constant in
`scripts/tests/test_description_coverage.py`, made in the same change as the
`SKILL.md` edit, the same way candidate L's commit (f23fb03) moved its
`SKILL.md` and marker edits together. I have not made either edit; this is
the proposal only.

`NEGATIVE_SCOPE_MARKER` (`"Not for web or app UI/UX design"`) is untouched
by this candidate and needs no change.

## 6. Which cases this draft targets

- **(a) — targeted.** Named format + implied file. The literal-token addition
  is aimed directly at the mechanism P6 exposes.
- **(b) — conceded, explicitly.** The no-file-implied case (P4) is not
  addressed. P4 shows Claude deciding no document output is needed at all,
  before any noun or token matching happens — "rapport" was already in the
  description and it did not help. No wording change to the deferral
  sentence can intervene in a decision that, per Claude's own account,
  happens upstream of it. Fixing (b) needs a different lever; none is
  proposed here.
- **(c) — unaffected, still works.** No change touches the file-implied,
  no-format-named path.

## 7. Falsification test

**Prompt to run:** the same or an equivalent prompt to P6 — rough/unstructured
notes, with the user naming Word specifically (e.g. *"turn these rough notes
into a Word doc"*). P6 was run on the clean 2026-09-11 run, after candidate L
was already applied, and still lost to docx — so this prompt already
falsifies L. It is the direct re-test for M because M's only change is the
literal-token addition; nothing else about the sentence moved.

**Expected if M works:** our skill is at least weighed against docx for this
prompt — evidenced by section/typography/ATS handling appearing, or by a
visible acknowledgment that the deferral clause applied — rather than an
unexamined pass to the docx skill.

**What kills M:** if the identical (or equivalent) prompt still routes to
docx with the same reasoning pattern as P6 — Claude citing the competing
skill's own trigger criteria and not engaging with ours — that shows adding
the literal `.docx`/`.pptx` tokens to our own sentence did not change which
signal the router weighs. That would falsify the specific mechanism this
candidate targets (token-parity with the competing skill), distinct from L's
already-falsified mechanism (clause ordering/salience).

## 8. Could not verify

- I cannot read docx's actual `SKILL.md` (`/mnt/skills/public/docx/SKILL.md`,
  outside this repo, loaded inside Claude's code-execution capability) to
  confirm the literal `.docx` trigger text Claude paraphrased in P6. That
  claim is Claude's own account, not something I can grep-verify here —
  tagging it **CONVENTION** per the refuse-unverifiable-attribution rule.
  This draft's edit is motivated by that account but does not depend on its
  exact wording being correct, only on Claude having named a literal token
  as the deciding factor.
- I have not run this candidate live (draft only, per the brief). §7's test
  needs to be executed by whoever runs the next activation probe.
- Whether adding these two literal tokens actually shifts router behavior,
  versus being cosmetically present but still outweighed by the competing
  skill's own description, is exactly what §7 tests and is not something I
  can establish from this seat.
