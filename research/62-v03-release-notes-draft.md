# v0.3 RELEASE NOTES — DRAFT, not yet applied to RELEASE-NOTES.md

Written 2026-09-11. **Two sections are PLACEHOLDERS pending the infographic work landing**, and
one number must be re-measured at build time. Marked inline. Do not paste this into
RELEASE-NOTES.md until those are resolved.

House style, matched from v0.1.0 and v0.2.0: `# v0.X.0` heading, then `## Added`, `## Fixed`,
`## Known limitations`. Plain sentences. No feature is claimed that was not observed in output.

---

# v0.3.0

## Added

- `infographic` is now a real family. v0.2.0 listed it as a known limitation with no section
  order at all; it resolved layout, typography and colour and nothing else. It now has a
  three-section structure — headline, key points, call to action — with headings already
  present in English, French and German, a palette, a typeface, and a type scale built for a
  1080 by 1350 social canvas: a 108 point lead figure down to 14 point captions, sized to be
  read as a thumbnail rather than at arm's length. Those sizes ship as convention. Nothing in
  the sources this library cites covers screen-thumbnail or statistic-numeral sizing, and we
  would rather say so than credit an authority that does not cover the case.
- A PNG handoff. The infographic family renders to a social-image target, and until now no
  handoff existed for that format at all, so the skill resolved a design and then handed the
  renderer nothing. The block reports the canvas in pixels, the typeface, sizes in pixels and
  the palette, and states plainly that page-based concepts such as bleed and crop marks do not
  apply to a screenshot.
- Heading wording, section by section, now reaches the Word, PowerPoint, PDF and plain-text
  outputs.

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
- The PowerPoint handoff reports a letter-spacing value as not present, because the column it
  reads has not been authored yet. The Word equivalent has been removed rather than carried a
  third time: its mapping was never sourced, so it was both unverifiable and unfillable.
- With the built-in Word and PowerPoint skills present, letters, memos and reports in English
  and French may be routed to those skills or answered in chat without this one; CVs, invoices,
  forms and German prompts fire reliably, and a request that names a file format goes to that
  format's own skill. Add "Use the document-design-intelligence skill." to the request; this
  fired in every test. <!-- The workaround stays in the SAME paragraph as the limitation.
  A limitation without its workaround reads as a broken tool. -->

<!-- v0.2.0's "infographic has no section order at all" is DROPPED: verified fixed, the handoff
     now shows real values on every line. -->

<!-- DO NOT INCLUDE: candidate M's refutation, the description-candidate chain, or any internal
     routing experiment. Six candidates have been tested and none moved named-format routing.
     A user needs the workaround above, not our history. -->

---

## BUILD-TIME CHECKS before this ships
1. ~~Fill both placeholders~~ DONE from research/59.
2. ~~Decide the characterSpacing question~~ DONE, ruled: the Word key is removed, the sourced
   PowerPoint one stays.
3. ~~Confirm the infographic limitation is gone~~ DONE, verified against real handoff output.
3b. ADD to Added once it lands: the description now names infographic in three languages.
4. Re-read every Added and Fixed line against actual handoff output. **The failure this release
   discloses was a notes claim nobody checked against the output.** Do not repeat it in the
   notes that disclose it.
