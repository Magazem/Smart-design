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
