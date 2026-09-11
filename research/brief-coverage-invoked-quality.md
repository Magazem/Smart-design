# BRIEF — Coverage and Gap Analyst — INVOKED-QUALITY PASS on published v0.2.0

ONE deliverable: `research/51-invoked-quality.md`.

## THE QUESTION THIS PASS ANSWERS — read before you start
v0.3's headline, ruled by the user and accepted by the lead: **100% auto-firing is a later-stage
goal. The MVP bar is that when the skill RUNS, the result is GOOD.**

So this pass measures **OUTPUT QUALITY, NOT ACTIVATION.** Every prompt you run gets
`Use the document-design-intelligence skill.` appended, so firing is guaranteed and is not what
you are scoring. Do not report on whether the skill fired. Do not touch routing, description
candidates, or the EN/FR prose-genre problem — all of that is owned elsewhere and is closed to
you.

## WHAT YOU ARE TESTING
The **published v0.2.0 asset**, not a local working copy. Obtain it and exercise it as shipped.
If you must fall back to the local build, say so explicitly and prove the description and row
counts match the published asset before drawing any conclusion from it.
Published asset reference values: description 972 chars starting "Creating any document type
below"; rows — constraints 47, type-scales 20, headings 204, structures 17, doctypes 30;
`display_columns` present on 6 tables.

## THE STANDARD OF EVIDENCE — this project's hardest-won lesson
**VALIDATION PROVES ROWS ARE WELL-FORMED. ONLY AN END-TO-END TEST PROVES THE OUTPUT SAYS
SOMETHING.** Every significant defect found on 2026-09-10 had the same shape: the data was
valid, the code ran, exit 0, and the answer was empty or wrong.
- the docx handoff block carried no page size, fonts or palette since v0.1.0
- the table-of-contents doctype handed over no heading levels
- a plain-text answer silently dropped the whole section model
- the description coverage test would have passed while checking nothing, twice

None were caught by the gate, by `validate_data`, or by the suite. All were caught by looking at
what the thing actually PRINTED. **A green gate is not a result here. Do not report one.**

For every check you write or run, ask: what would this say if the feature produced NOTHING AT
ALL? If the answer is "it would pass", it is not a test and does not go in the report.

## SCORE EACH FAMILY ON THESE, AS SEPARATE FIELDS
1. **No refusal.** Zero occurrences of "that document type is not in my library" or any
   equivalent. A refusal for a shipped family is a P0 defect.
2. **Sections present and in the documented order.** Compare against the structure row for that
   family. Name the expected order and the produced order; do not just say "matches".
3. **Handoff values actually reaching the renderer** — check each of these INDIVIDUALLY and say
   which are present and which are empty: page size, margins, fonts, heading levels and their
   point sizes, colour palette, page-flow rules. An empty handoff block is the exact defect
   shape above; look for it specifically.
4. **The plain-text path.** Where the skill answers without producing a file, confirm the
   section model survives. It silently dropped once before.
5. **Quality of the actual content**, in your judgement: is this a designed document or a
   generic one wearing the skill's name?

## FAMILY SELECTION — spread over OUTPUT PATHS, not breadth
Do NOT run all 15 shallowly, and do not pick arbitrarily. Choose **five to seven** families that
between them cover the DISTINCT output paths, and justify the selection in one paragraph.
The paths that must each be represented at least once:
- a CV family (the best-exercised path, your control — if this is weak, everything is)
- a multi-heading-tier print family (report-print exercises h1/h2/h3; cv-print deliberately has
  NO h3, and that is correct, not a defect — do not file it)
- a slide/deck family (different layout model)
- a short artefact family (invoice, form or quote — different structure model)
- at least one non-English family, to exercise the three-language heading rows
Record which families you did NOT run and why, so the gap is visible.

## HARD RULES
- **No git. Ever.** The orchestrator owns git. Do not commit, do not stash, do not branch.
- **Never hand-edit a generated file.** If a defect lives in generated output, the fix belongs
  in the GENERATOR. Name the generator and the source file.
- **Refuse unverifiable attribution.** If you cite a rule or authority, it must be grep-verifiable
  in this repo. Bringhurst is cited here ONLY for measure and leading, never pagination;
  Butterick and DIN 5008 are cited NOWHERE. If you cannot verify a named source, tag the item
  CONVENTION and say so rather than borrowing the name.
- **Do not fix anything.** This is a diagnostic pass. Record defects; propose fixes in words.
- Do not tune a constant to make a check pass. See "refusing the green tick", 2026-09-09: a
  one-constant change that would have turned four bullets green was refused because it was
  fitting to the test. When a passing number and a working product disagree, this project fixes
  the product.

## DELIVERABLE — `research/51-invoked-quality.md`
- Which asset you exercised and how you proved it was the published one.
- Family selection and its justification; families skipped and why.
- Per family: the five scored fields above, with the ACTUAL OUTPUT quoted, not summarised.
- **DEFECTS RANKED**, worst first. For each: severity, the family or families it hits, what the
  output actually said versus what it should have said, the suspected location (generator and
  source file, not the built artefact), and how you would confirm it.
- What you could not determine, stated plainly.

## Report
Message the orchestrator (slot 01a080c5-2001-78b3-bbbe-afaae15edafa) in a FEW LINES: which
asset, how many families run, count of refusals, the top three ranked defects in one line each,
file path. Then STOP.
