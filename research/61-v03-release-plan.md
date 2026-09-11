# v0.3 RELEASE PLAN — sequence, gates, and one honesty problem

Written 2026-09-11 by the Workflow Orchestrator at the lead's request.
**NOTHING IS REBUILT until the infographic content is authored AND verified.** Ruled by the lead.

## *** THE THING TO SETTLE FIRST: v0.2.0's RELEASE NOTES OVERCLAIMED ***
This is not a style point. Two claims in the shipped v0.2.0 notes were false as shipped, and both
are fixed by the very work v0.3 is about to ship.

**Claim 1, under "Added":**
> "Section guidance for all 15 previously uncovered document families: 52 canonical sections,
> **204 heading rows in English, French and German.**"

The rows existed and were gated. **Their wording reached no output path.** Resolved entries
carried the union of keys `["key"]`; the docx handoff contained zero authored wordings. A user
reading that line was promised something the product did not do.

**Claim 2, under "Fixed":**
> "A plain-text answer now keeps the resolved section order and **headings**; previously the
> structure was silently dropped when no file was produced."

The plain-text path printed `headings/contact-en-1` — bare ids. It kept the section ORDER and
the heading IDS. It did not keep headings in any sense a reader would recognise.

### THE RECOMMENDATION
**Say so plainly in the v0.3 notes, under Fixed, naming v0.2.0.** Something of this shape:

> v0.2.0 announced 204 heading rows in three languages and said the plain-text answer kept
> headings. Neither reached the output: every path emitted bare row ids and no wording. The rows
> were correct and unreachable. They now reach the Word, PowerPoint, PDF and plain-text paths,
> and a test asserts the wording is present rather than asserting the rows exist.

**Do NOT quietly fix this.** A silent correction leaves anyone who read v0.2.0's notes believing
they had a feature they never had. This project already refuses unverifiable attribution and
retires its own confounded results in place; the same standard applies to its release notes.
That is a call for the lead and the user, but the default should be disclosure.

## SEQUENCE — each step gated on the one before

**1. INFOGRAPHIC CONTENT — in progress, DDR (task 01a0903d).**
   Gate: png handoff shows ZERO not-present lines for font-face, sizes, sections, palette;
   pytest green; `validate_data.py data/base` clean.

**2. PACKAGING REVIEWS THE LOADED RESULT.** Ruled by the lead. Independent of the author.
   Gate: Packaging confirms the loaded rows match the drafts and the loader was the only path
   into `data/base`.

**3. FULL LOCAL VERIFICATION BEFORE ANY BUILD.**
   - full pytest, gate clean, row count stated
   - regenerate the manifest and diff — an EMPTY diff proves no hand-edit
   - run the handoff for one family per format: docx, pptx, pdf, png

**4. RELEASE NOTES DRAFT.** Must cover, at minimum:
   - the dropped-columns P0, and the honesty item above
   - the pdf handoff gaining sizes, heading levels and palette
   - deck-projection: a projected deck no longer gets the CV's print scale
   - the png builder and the infographic family becoming real
   - **the routing workaround, unchanged and in the SAME paragraph as the limitation.**
     A limitation without its workaround makes a user think the tool is broken.
   - **candidate M's refutation is INTERNAL. It does not belong in user-facing notes.**
     Users do not care which of our descriptions we tested. The workaround is what they need.

**5. ONE REBUILD, bundling everything.** No partial rebuilds — that is why nothing has been
   rebuilt all day.

**6. FRESH INVOKED-QUALITY PASS ON THE BUILT ZIP.** Ruled by the lead, and the gate before any
   tag. **Run it against the extracted BUILT artefact, not the working tree.** The lesson from
   today: six matching reference values did not prove the dev build matched the release, because
   none of them would catch a difference in the resolver, the handoff or the manifest — which is
   exactly where the defects live. **Match the behaviour files, or run the artefact itself.**

**7. TAG AND PUSH — USER CONFIRMS FIRST.** Standing rule. CI writes VERSION and the stamp from
   the tag, and ruling O already limits the release body to the current version's section.

## RISKS TO CARRY
- **The account holds candidate M, not the published build.** Any browser check during release
  verification reads M. Either the user restores v0.2.0 first, or no browser step is part of the
  release gate. Reference copy: `research/test-builds/_published-v0.2.0-reference.zip`.
- **`research/test-builds/` must never be confused with `skill/dist/`.** Test artefacts are not
  releases. The README there says so.
- **The infographic type scale is the one place a value could be invented.** DDR has been told
  to justify it rather than copy the 11pt screen row. Check that reasoning at step 2, not later.
