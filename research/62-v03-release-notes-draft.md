# v0.3 RELEASE NOTES — DRAFT, not yet applied to RELEASE-NOTES.md

Written 2026-09-11. **Two sections are PLACEHOLDERS pending the infographic work landing**, and
one number must be re-measured at build time. Marked inline. Do not paste this into
RELEASE-NOTES.md until those are resolved.

House style, matched from v0.1.0 and v0.2.0: `# v0.X.0` heading, then `## Added`, `## Fixed`,
`## Known limitations`. Plain sentences. No feature is claimed that was not observed in output.

---

# v0.3.0

## Added

- `infographic` is now a real family. <!-- PLACEHOLDER: fill from research/59 once DDR lands.
  Must state the structure, the three-language headings, the type scale for the 1080x1350
  social canvas, the palette and the typeface, and which values ship as convention. -->
- A PNG handoff. The infographic family renders to a social-image target, and until now no
  handoff existed for that format at all, so the skill resolved a design and then handed the
  renderer nothing. The block reports the canvas in pixels, the typeface, sizes in pixels and
  the palette, and states plainly that page-based concepts such as bleed and crop marks do not
  apply to a screenshot.
- Heading wording, section by section, now reaches the Word, PowerPoint, PDF and plain-text
  outputs. <!-- see the first Fixed entry; this is the other half of that disclosure -->

## Fixed

- **v0.2.0 announced something it did not deliver, and this release says so.** Those notes
  listed "204 heading rows in English, French and German" as a feature, and said a plain-text
  answer kept the section order and headings. Neither reached the output. Every path emitted
  bare row identifiers and no wording at all: a Word handoff for a CV contained none of the
  authored headings, and the plain-text answer printed identifiers where headings were
  promised. The rows themselves were correct and complete throughout; nothing could reach them.
  They now reach every output path, and a test asserts the wording is present rather than
  asserting the rows exist.

- The same cause was hiding other values. A constraint arrived without what it applies to, what
  it checks, its threshold or its severity. A document structure arrived without its heading
  depth, table-of-contents depth, caption position or cross-reference style — which is the
  section model itself. A type scale arrived without its leading ratio.

- The PDF handoff carried no type sizes, no heading levels and no palette. Not empty values:
  those sections were absent entirely, which is why this survived a release unnoticed. It hit
  invoices and quotes hardest, since an invoice has no output format other than PDF and nothing
  else could supply them.

- A projected slide deck was handed the CV's print type scale — eleven point body text aimed at
  a projector. The projection scale existed and nothing in the library could reach it. Decks now
  resolve their own scale; the CV is unchanged.

- Where a value genuinely does not apply to a format, every handoff now says so on its own line
  instead of omitting the section. Two of the defects above hid for a whole release precisely
  because an absent section looks like nothing at all, while an empty one is a visible fact.

## Known limitations

<!-- CARRIED FORWARD from v0.2.0, minus what this release fixed. Re-check each before shipping. -->
- The ambiguous German deck phrase still resolves instead of asking.
- Language carries no ranking weight, so a French query does not favour the French CV row.
- Panel count, slide count and folded-panel adjacency are not modelled.
- Non-CV heading sections carry one wording per language, with no variants.
- `characterSpacing` in the Word handoff reads a column that exists in no table, so it always
  reports not present. <!-- DECIDE BEFORE SHIP: v0.2.0 called this "a v0.3 decision" and it is
  still open. Either remove the section, author the column, or restate the limitation. Do not
  carry the same sentence a second time without a decision. -->
- With the built-in Word and PowerPoint skills present, letters, memos and reports in English
  and French may be routed to those skills or answered in chat without this one; CVs, invoices,
  forms and German prompts fire reliably, and a request that names a file format goes to that
  format's own skill. Add "Use the document-design-intelligence skill." to the request; this
  fired in every test. <!-- The workaround stays in the SAME paragraph as the limitation.
  A limitation without its workaround reads as a broken tool. -->

<!-- DROPPED from the v0.2.0 list because this release fixes it:
     "`infographic` has no section order at all; it gets layout, typography, colour and print
     only." Confirm it is genuinely fixed before removing. -->

<!-- DO NOT INCLUDE: candidate M's refutation, the description-candidate chain, or any internal
     routing experiment. Six candidates have been tested and none moved named-format routing.
     A user needs the workaround above, not our history. -->

---

## BUILD-TIME CHECKS before this ships
1. Fill both placeholders from `research/59-infographic-content.md`.
2. Decide the `characterSpacing` question rather than carrying v0.2.0's sentence again.
3. Confirm the infographic limitation is genuinely gone before deleting it from the list.
4. Re-read every Added and Fixed line against actual handoff output. **The failure this release
   discloses was a notes claim nobody checked against the output.** Do not repeat it in the
   notes that disclose it.
