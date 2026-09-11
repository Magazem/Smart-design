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
- The description now names the infographic family in English, French and German. A release
  that adds a family and does not name it leaves the family unreachable however good its data
  is, which is what happened in v0.2.0.

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
  fired in every test.

# v0.2.0

## Added

- Section guidance for all 15 previously uncovered document families: 52
  canonical sections, 204 heading rows in English, French and German. Three
  pairs share an identical section order deliberately — the two brochures,
  letter and cover letter, flyer and one-pager — because what separates each
  pair is page format, not content.
- Page-flow rules: a heading keeps with its first paragraph, no widows or
  orphans, table rows do not split, long tables repeat their header row, a
  figure keeps with its caption. These reach the docx renderer as keepNext,
  widowControl, cantSplit and tblHeader. Slides do not paginate, so pptx says
  so rather than staying silent.
- Heading sizes for report and CV type scales, so a long report hands over
  real heading levels.
- The page-flow rules and the heading sizes both ship as convention, not
  sourced.

## Fixed

- brochure-flyer-a4 listed one keyword twice in v0.1.0, slightly
  over-weighting that row; now gated.
- v0.1.0's docx handoff block shipped with no page size, no font and no
  palette values. The block is what the docx skill is handed. It now carries
  them, and an end-to-end test asserts it.
- A plain-text answer now keeps the resolved section order and headings;
  previously the structure was silently dropped when no file was produced.
- The activation description was corrected across several rounds of this work:
  the trigger promises appearance rather than prose quality; the missing
  document nouns were added, including invoice, memo, one-pager, facture,
  Rechnung, devis and lettre; and the claim that creating a document is this
  skill's job now comes first rather than last. These make the description
  honest and complete. **They did not fix the routing problem below** — five
  description changes were tried and none moved it.

## Known limitations

- `infographic` has no section order at all; it gets layout, typography,
  colour and print only.
- The ambiguous German deck phrase still resolves instead of asking.
- Language carries no ranking weight, so a French query does not favour the
  French CV row.
- Panel count, slide count and folded-panel adjacency are not modelled.
- Non-CV heading sections carry one wording per language, with no variants.
- `characterSpacing` in the docx handoff reads a column that exists in no
  table, so it always reports not present. Removing the section or authoring
  the column is a v0.3 decision.
- With the built-in docx/pptx skills present, letters, memos and reports in
  English and French may be routed to docx or answered in chat without this
  skill; CVs, invoices, forms and German prompts fire reliably. The French report
  is a known non-fire. Add "Use the document-design-intelligence skill." to
  the request; this fired in every test.

# v0.1.0

## Scope — what this release contains

- **Full section-by-section structure guidance for CVs only** (`cv-experienced`
  and `cv-academic`). Every other document type resolves with no section
  order — the resolver says so explicitly rather than returning an empty list.
- **Layout, typography, colour, and print guidance for every document type
  the skill covers** (CVs, resumes, cover letters, brochures, flyers, posters,
  reports, whitepapers, slide decks, presentations, forms, letters, quotes,
  offers), regardless of whether that type gets section-order guidance.
- Section-by-section headings for the non-CV document families are **deferred
  to step 9** — not included in this release.
- PDF output: **PDF/X-4 structurally emitted; conformance not independently
  verifiable with open tooling.** This is the exact tier delivered — no
  stronger claim should be read into it.

## Known limitation

One ambiguous German deck phrase resolves to the projection variant instead
of asking which was meant. The three deck rows tie on score and the tie is
broken by row length.

The skill fixes how a document looks, not how its prose reads; AI-sounding
wording is out of scope for v0.1.0.

What the resolver does do: it resolves when confident, asks which of the
real candidates you meant when a request is ambiguous, and says plainly when
nothing matches.
