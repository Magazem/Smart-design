# Candidate M draft — file-not-genre mechanism (DRAFT ONLY, not applied)

## 1. The two quotes and the mechanism they support

- P6 (rough notes -> Word, went to docx): *"Since you asked for a Word doc
  specifically, it was the clear match (its trigger criteria explicitly call
  out '.docx' requests)."*
- P4 (FR report, no skill at all, emitted Markdown): *"I chose Markdown over
  Word specifically because you didn't ask for a Word file or signal you
  needed a formal downloadable document."*

Read together: routing is gated on whether a FILE is implied, and if so, on
which FORMAT was named — not on whether a genre noun ("CV", "rapport",
"brochure") appears anywhere. P4 is the harder case: "rapport" is already a
listed noun in our description and it still didn't fire, because Claude
decided no file was needed at all before any noun-matching could happen. P6
shows that even when a file IS implied and named ("Word doc"), the competing
skill's own literal trigger ('.docx') outcompetes our existing carve-out
sentence ("still this skill's job even as Word... unless a plain conversion
with no design ask") — that sentence exists on disk today and did not save
P6.

## 2. Proposed description text (exact, as it would replace the frontmatter value)

```
Creating any document type below is still this skill's job even as Word or PowerPoint; defer to that format's own skill only when the user names it for a plain conversion or edit with no design ask. Creates and fixes print/office documents: CVs, resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, lettre, affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht, invoice, memo, proposal, one-pager, facture, devis, rapport, Rechnung, Formular, Broschüre. Triggers: make me a CV, write a note interne, turn this into a brochure, turn rough notes into a polished Word doc, I need slides for Monday, format this report, fais-moi une fiche, erstelle ein Angebot; appearance fixes: looks like AI, looks generic, make it look professional, fix the layout. Applies sourced layout, typography, color, print, and ATS rules. Not for web or app UI/UX design (use UI/UX Pro Max for screens).
```

Only one clause was inserted: `, turn rough notes into a polished Word doc`
into the existing `Triggers:` list, right after `turn this into a brochure`.

## 3. Character count and method

Method: read `SKILL.md`, apply the same regex the test file uses —
`^description:\s*"(.*)"\s*$` (`re.M`) — take group 1, run Python `len()` on
it. This is codepoint length, matching both claude.ai's upload cap check and
`test_description_coverage.py::test_description_still_fits_the_upload_cap`
(`len(raw) <= 1023`).

- Current on-disk description, measured this way: **972 characters** (not
  975 — the brief's figure was itself an approximation; RESUME.md line 1246's
  831 is confirmed stale, from candidate F, predates L). Re-measure before
  relying on either number; I ran the regex+len() myself against the live
  file rather than trust either upstream figure.
- Candidate M, same method: **1015 characters**.
- Headroom used: 43 of ~51 available characters. 8 characters of headroom
  remain under the 1023 cap.

## 4. Diff-in-words

**Changed:** one insertion, `, turn rough notes into a polished Word doc`,
added to the `Triggers:` example list.

**Unchanged, byte-for-byte:** the deferral sentence, the noun list, the
appearance-fix triggers, the "Applies sourced..." sentence, and the negative
scope sentence. Nothing was deleted or reworded.

**Why this follows from the quotes, not from theory:**

The deferral sentence already states the policy we want ("still this skill's
job even as Word... unless a plain conversion... with no design ask") and it
existed on disk, unmodified, when P6 was run. It did not save P6. So the
defect is not in the *policy statement* — it's that the policy is phrased as
an abstract conditional, and P6 shows Claude resolving the routing decision
by pattern-matching a concrete trigger phrase in the competing skill's own
description ('.docx requests') rather than by reasoning through our
conditional. The skill's own history backs concrete triggers over abstract
policy: the existing `Triggers:` list is itself evidence that this project
already treats literal example phrases as the effective activation lever,
separate from the descriptive sentences around them. Candidate M does not
touch the policy sentence (which is unproven to be the problem) — it adds
one concrete example that combines a named format ("Word doc") with an
explicit design signal ("polished") and a creation verb ("turn... into"),
mirroring P6's own phrasing but with the one addition — an explicit design
word — that P6's actual prompt may have lacked. This is a narrow, targeted
patch to the exact gap the quotes expose, not a rewrite of the surrounding
theory.

## 5. Test-marker check

**Preserved. No test-file edit required.**

- `NEGATIVE_HEAD_MARKER` = the full deferral sentence, unchanged in the
  candidate — verified by substring search against the candidate string
  (`NEGATIVE_HEAD_MARKER in candidate` → `True`).
- `NEGATIVE_SCOPE_MARKER` = `"Not for web or app UI/UX design"`, unchanged —
  same check, `True`.

Both markers sit outside the region I edited (the insertion is inside the
`Triggers:` clause, which is part of the *positive* region between the two
markers, not the markers themselves), so `find()` locates both at the same
relative position. No change to `scripts/tests/test_description_coverage.py`
is needed for this candidate.

## 6. Which cases this draft targets

- **(a) — targeted.** Named format + implied file. The new trigger phrase
  gives Claude a concrete pattern for "named format + design-ask stays with
  us" that P6's actual prompt apparently did not match against.
- **(b) — conceded, explicitly.** The no-file-implied case (P4) is not
  addressed. P4 shows Claude deciding no document output is needed at all,
  before any noun or trigger matching happens — "rapport" was already in the
  description and it didn't help. No amount of description wording can
  intervene in a decision that, per Claude's own account, happens upstream
  of description-matching. Fixing (b) would need a different lever than the
  description string; I have not attempted one here.
- **(c) — unaffected, still works.** No change was made to any text
  supporting the file-implied-no-format case; the insertion is additive and
  scoped to the format-naming trigger only.

## 7. Falsification test

**Prompt to run:** something close to P6 but with an explicit design signal
added, e.g. *"Turn these rough notes into a polished Word document for me"*
or *"I need this cleaned up into a proper-looking Word doc."*

**Expected if M works:** the document-design-intelligence skill fires
(section/typography/ATS rules applied), rather than a plain docx pass-through
with no design reasoning.

**What kills M:** if that same prompt still routes to the docx skill's own
handling with no sign our skill was even considered, that shows a competing
skill's literal extension/format match dominates cross-skill arbitration
regardless of what our own `Triggers:` list contains — i.e., trigger-list
content does not influence routing for the named-format case at all. That
would falsify the mechanism this candidate targets (concrete trigger phrases
beat abstract policy) for this specific interaction, not just this wording
of it.

**Distinguishing M from L:** L touched salience/ordering of the existing
clauses generally and did not add or change any trigger phrase. Re-running
P6 verbatim (no design adjective) is not a fair test of M — M's inserted
trigger requires the design signal to be present, and P6 as quoted may not
have had one. The falsification prompt above must include an explicit design
word to actually exercise M's change.

## 8. Could not verify

- I cannot read docx's actual `SKILL.md` (it lives at
  `/mnt/skills/public/docx/SKILL.md`, outside this repo, loaded inside
  Claude's code-execution capability) to confirm the literal `.docx` trigger
  text Claude paraphrased in P6. That claim is Claude's own account, not
  something I can grep-verify here — tagging it **CONVENTION** per the
  refuse-unverifiable-attribution rule; it's used only as motivation, not as
  a fact this draft depends on being exactly true.
- I have not run this candidate live (draft only, per the brief). The
  falsification test in §7 needs to be executed by whoever runs the next
  activation probe; I cannot confirm M actually changes Claude's routing
  decision from this seat.
- "Polished" as the design-signal word is a judgment call, not something
  derived from the quotes — the quotes establish that a design signal was
  the missing ingredient in principle, not which specific word reads as one
  to Claude. An alternative word choice is untested.
