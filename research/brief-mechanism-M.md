# BRIEF — Mechanism Analyst — DRAFT CANDIDATE M (file-not-genre mechanism)

ONE deliverable: `research/50-candidate-M-draft.md`.

## THIS IS A DRAFT ONLY
**DO NOT apply the candidate. DO NOT edit SKILL.md. DO NOT rebuild the ZIP. DO NOT run git.**
You produce a proposed description text and the argument for it. Nothing is applied.

## WHY A NEW CANDIDATE IS PERMITTED AT ALL
The standing rule forbids new description candidates without a fresh mechanism hypothesis
backed by **Claude's own account**, not our theorising and not another tally. Five candidates
(F, G, H, lettre, L) were applied and none moved EN/FR prose-genre activation. The refutation
chain is closed: nouns dead, trigger phrases dead, artefact-vs-prose-genre dead as an
explanation, language-as-root-cause superseded, salience/ordering applied as L and did not fix
it. **Do not revisit any of those.**

The clean run of 2026-09-11 produced two verbatim statements from Claude. These, and only
these, are what you write the candidate against. Quote both in your deliverable:

- P6 (rough notes -> Word, went to docx): *"Since you asked for a Word doc specifically, it was
  the clear match (its trigger criteria explicitly call out '.docx' requests)."*
- P4 (FR report, no skill at all, emitted Markdown): *"I chose Markdown over Word specifically
  because you didn't ask for a Word file or signal you needed a formal downloadable document."*

## THE MECHANISM TO TARGET
Routing appears to turn on the FILE, not the genre:
  (a) User NAMES a format ("a Word document") -> docx wins on its OWN trigger criteria, and our
      "creation is still our job even as Word" clause does NOT beat it.
  (b) User implies NO file -> Claude answers in chat or emits Markdown, and no document skill is
      considered at all.
  (c) A file is implied but no format named, AND there is a design decision to resolve -> we
      fire (the CV and the EN memo both did).

No candidate so far has targeted the deferral sentence's interaction with a NAMED FORMAT. That
is the lever. Case (b) — the no-file-implied case — is the harder one; say explicitly whether
your draft addresses it or concedes it.

## HARD CONSTRAINTS ON THE DRAFT

**1. LENGTH.** The claude.ai UI enforces under 1024 characters. The description currently on
disk measures **975 characters** (RESUME.md line 1246 still says 831; that figure is STALE,
from candidate F, and predates L — do not trust it). Re-measure the current value yourself with
a real character count of the quoted string and state your method. **Headroom is roughly 48
characters.** Your draft must fit under 1023. State your draft's exact measured count. If you
need room, say precisely what you would remove and what that costs.

**2. THE TEST MARKER TRAP — check this or the draft is unusable.**
`scripts/tests/test_description_coverage.py` splits the description into a positive region and
a negative one using a LITERAL string marker. Candidate H deleted the string that was serving
as that marker; left alone, `find` returns -1, the positive region silently becomes the WHOLE
description, and the test passes forever while checking nothing. **Read that test, identify the
exact marker string, and state in your deliverable whether your draft preserves it.** If it
does not, say so loudly and propose the generator-side fix.

**3. DO NOT rewrite the deferral sentence on the "docx is a capability, not a skill" reading.**
That reading is DISPROVED. docx and pdf are real skills at `/mnt/skills/public/docx/SKILL.md`
and `/mnt/skills/public/pdf/SKILL.md`, loaded inside the code-execution capability. Absent from
the Settings list is not absent from the filesystem. The deferral sentence targets something
real.

**4. Generated files are edited via their generator, never by hand.** Since you are not applying
anything, this means: if your draft would require a change, name the GENERATOR and the source
file, not the built artefact.

**5. Refuse unverifiable attribution.** If you cite a rule or authority, it must be grep-
verifiable in this repo. If it is not, tag it CONVENTION and say so.

## DELIVERABLE — `research/50-candidate-M-draft.md`
1. Both verbatim Claude quotes, and the mechanism they support.
2. The proposed description text in a single fenced block, exactly as it would be applied.
3. Its exact measured character count and the measurement method.
4. A diff-in-words against the current description: what changed, what stayed, and WHY each
   change follows from the quotes rather than from theory.
5. The test-marker check result.
6. Which of cases (a), (b), (c) the draft targets, and which it concedes.
7. The falsification test: which activation prompt(s) would distinguish M from L, and what
   result would kill M. A candidate you cannot falsify is not a candidate.
8. Anything you could not verify.

## Report
Message the orchestrator (slot 01a080c5-2001-78b3-bbbe-afaae15edafa) in a FEW LINES: draft
written yes/no, its character count, marker preserved yes/no, which cases it targets, file
path. Then STOP.
