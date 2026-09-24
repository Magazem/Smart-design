# v0.5.0 (draft)

> **DRAFT: not released.** Every `{{placeholder}}` is filled from the evidence files
> (`research/designs-evidence/`, `research/designs/*.csv`) and the test run at release time, never
> from memory. Delete this box when the tag is cut. This release also covers work that was never
> tagged: v0.4 phase 1 (the table census) and Phase A (CV evidence and slop checks).

## Added

- **Designs per document family, chosen by counting, not by taste.** Each family now offers a
  ranked list of designs instead of a single default. A design's rank comes from how often its
  layout signature appears in public template collections that already rank themselves: GitHub
  stars, npm monthly downloads, LibreOffice download counts, prevalence in a vendor's own
  gallery, and juried award lists. Where no such collection exists, published authorities
  (design systems, style manuals) are used. Every design carries its evidence class and the
  source it was counted in. `ddi.py designs --doctype <key> [--query "<style wording>"]` lists
  them; `resolve --design <key>` applies one.

  | Family | Designs | Evidence classes | Counted in | Status |
  |---|---|---|---|---|
  | cv | {{cv_designs}} | {{cv_classes}} | GitHub stars (`resume template`), npm downloads (`jsonresume-theme`); Europass (authority) | {{cv_status}} |
  | deck | {{deck_designs}} | {{deck_classes}} | npm downloads (`slidev-theme`), LibreOffice downloads, Microsoft Create gallery | {{deck_status}} |
  | invoice | {{invoice_designs}} | {{invoice_classes}} | GitHub stars, Microsoft Create gallery | {{invoice_status}} |
  | letter | {{letter_designs}} | {{letter_classes}} | Microsoft Create gallery, LibreOffice; DIN 5008 (authority, via a fetched secondary) | {{letter_status}} |
  | report | {{report_designs}} | {{report_classes}} | GitHub stars, Microsoft Create gallery; ARC Awards 2025 (juried) | {{report_status}} |
  | poster | {{poster_designs}} | {{poster_classes}} | GitHub stars (LaTeX posters) | {{poster_status}} |
  | cover-letter | {{cover_letter_designs}} | {{cover_letter_classes}} | Microsoft Create gallery | {{cover_letter_status}} |
  | memo | {{memo_designs}} | {{memo_classes}} | Microsoft Create + Overleaf (pooled); AR 25-50, Purdue OWL (authorities) | {{memo_status}} |
  | brochure | {{brochure_designs}} | {{brochure_classes}} | Microsoft Create + LibreOffice (pooled) | {{brochure_status}} |
  | flyer | {{flyer_designs}} | {{flyer_classes}} | Microsoft Create gallery | {{flyer_status}} |
  | form | {{form_designs}} | authority only | USWDS, GOV.UK Design System, NHS service manual, ABS paper-forms standard | {{form_status}} |
  | quote | {{quote_designs}} | borrowed from invoice | none of its own | {{quote_status}} |
  | whitepaper | {{whitepaper_designs}} | borrowed from report | none of its own | {{whitepaper_status}} |
  | proposal | {{proposal_designs}} | {{proposal_classes}} | {{proposal_sources}} | {{proposal_status}} |
  | one-pager | {{one_pager_designs}} | convention | none exists | {{one_pager_status}} |
  | infographic | {{infographic_designs}} | {{infographic_classes}} | {{infographic_sources}} | {{infographic_status}} |

  `Status` is one of: *ranked* (passed the agreement gate and filled), *short list* (fewer than
  eight, shortfall stated), or *default only* (the pre-existing design, shortfall stated).
- **A grand library for building a brand.** The palettes, typeface pairings and type scales
  that brands draw from now each carry provenance: where the row came from and, where one
  exists, the ranking that put it there. The library holds:
  - {{n_design_system_palettes}} palettes taken from published design systems (GOV.UK, USWDS,
    IBM Carbon, Material 3, Radix, Tailwind, Atlassian and others);
  - {{n_ranked_palettes}} palettes from the top of COLOURlovers' vote ranking, admitted by a
    mechanical contrast filter written before the palettes were looked at;
  - {{n_pairings}} typeface pairings ranked by Google Fonts' own popularity field;
  - {{n_ratio_scales}} type scales built on named ratios (minor third, major third, perfect
    fourth), one per medium: print, screen and projection.

  Rows with no external source say `convention` rather than borrowing an authority's name.
  `ddi.py library <palettes|typefaces|type-scales|doc-styles> [--query]` browses the library.
- **Brand kits built from the library.** `brand.md` gains two sections:
  - `## Designs` picks one ranked design per family;
  - `## Type scales` picks one library scale per medium.

  A kit can now target any generic document type (`cv-uk`, `invoice-tabular`, `report-short`,
  …), not only the four it launched with. An AI can build a kit by following
  `references/brand-kit-builder.md`; `examples/generic-law-firm-brand.md` is a complete worked
  example made only of library rows.
- **A portable pack for assistants that cannot run code.** Each release now also publishes
  `ddi-portable-<version>.zip`, which contains:
  - `AGENTS.md`: instructions under ChatGPT's 8,000-character limit;
  - `DDI-LIBRARY.md`: every document type's resolved values plus the grand library;
  - `INSTALL.md`: setup for ChatGPT, Grok, Gemini and Claude.

  It is generated from the same data as the skill, and a test fails if the two drift apart.
  Direct testing on those platforms: {{p65_result}}.
- **Plain requests resolve instead of abstaining.**
  - "Make me a CV" used to stop and ask whether you meant a UK or a Gulf CV. A request that
    names a family but none of its variants now resolves to that family's designated default.
  - A German request picks the German-language variant and a French request the French one.
  - A US or Letter-size cue picks the Letter-size page.
  - A request that names exactly one family, such as "flyer", is searched within that family
    only, so a stray word like "paper" can no longer pull a flyer request to the whitepaper.
- **Mechanical anti-slop checks in preflight.** Emoji, more than two typeface families,
  boxed-everything tables, bordered-block ratio and an accent colour outside the palette are now
  measured in the rendered file, not described. The checks come from published slop-pattern
  research, cited in the data. (Phase A.)
- **Section headings follow the document's language.** A French invoice gets French headings
  even when the request was typed in English, and the reverse. (Phase A.)

## How the rankings were made, and where the method failed first

- **Counting, not judging.** The protocol was written and frozen before a single template was
  coded (`research/82-design-ranking-protocol.md`). Coders record four layout features from a
  template's first page and never say which design is better:
  - column structure;
  - heading typeface class;
  - colour use;
  - header treatment.

  A design is the most frequent admissible feature signature, rebuilt from library parts by a
  written rule. Amendments are dated files (`research/82a-*.md`, `research/82b-ADOPTED.md`), each
  stating what it changes and which results it affects.
- **The falsifier fired three times, and each time the work was redone rather than waved
  through.** Every family's codes are checked by a second coder who never sees the first
  coder's answers. The pre-registered bar is 80% agreement on every feature.
  - **cv:** agreement on header treatment was 0.70. The rule was rewritten with measurable
    thresholds, all 80 items were recoded (32 changed), and a fresh second coder reached 0.85.
  - **deck:** heading class (0.77), colour use (0.67), title-slide layout (0.73) and
    admissibility (0.78) all failed. {{deck_gate_outcome}}.
  - **invoice:** header treatment reached 0.33 and colour use 0.50. The failure pattern was
    shared, so one sharpened rule was written for every family not yet checked
    (`research/82a-general.md`) and applied to all of them. {{invoice_gate_outcome}}.
  - Where a feature failed twice, it was removed from that family's rankings and the removal is
    stated: {{second_failures_or_none}}.
- **Features that failed and were not used.** Text density failed in cv, deck and invoice, and
  table-rule style failed in invoice. Those designs take the family default for that feature
  instead of a counted value.
- **Phase A's CV evidence gate also failed, by its own pre-registered letter.** The
  Harvard-style CV ships for US, UK and generic CVs as that gate allowed. The DACH CV reverted
  to its earlier default.

## Known limitations

- **Popularity is not quality.** Rank 1 means "the most frequent admissible layout in these
  collections on this date", not "the best design". A list made only of single occurrences
  carries no ranking information at all; those families are labelled so.
- **Most families fall short of eight to ten designs:** {{shortfall_list}}. No public source
  ranks form or one-pager designs; form ships authorities only and one-pager ships its
  convention default. Quote and whitepaper have no collection of their own. They borrow up to
  three designs from invoice and report, which the data already renders identically, and those
  designs are labelled `borrowed:`.
- **The collections are skewed.** Every design inherits the skew of the collection it was
  counted in:
  - GitHub and npm reflect developers, LaTeX and Typst users, and English. The poster and report
    collections are mostly academic.
  - LibreOffice counts are cumulative since 2020 and lean older and European.
  - The Microsoft gallery is Microsoft's own editorial selection, and only its first static page
    is readable. Its resumes and forms were unreachable.
  - The tools most people actually use (Canva, Google Docs, Behance, Dribbble, Figma) block
    automated access, so they are absent.
- **A shipped design is a reconstruction.** It reproduces four layout features with library
  palettes, typefaces and styles. It does not reproduce a template's artwork, grid or
  typographic finesse, and none were copied.
- **The portable pack is static.** It cannot run the mechanical preflight. {{p65_limitation}}.
- **Resolver edge cases still open:** {{r5_open_items_or_none}}. Candidates from the pre-release
  review: a surname particle ("de la", "von der") can switch the CV to French or German; "on
  letter paper" can make a report or memo request abstain; plural-only requests ("flyers"); and
  query language is detected only when the request is ambiguous.
- **Brand-kit edge cases still open:** {{r6_open_items_or_none}}. Candidates from the pre-release
  review:
  - a brand colour below 4.5:1 is correctly demoted to fill-only, but the report and handoff did
    not say so;
  - a bilingual kit was unreachable in its second language;
  - Word documents use the fallback font rather than the brand font.
- Fold geometry (fold type and panel widths) now reaches the resolved output. The handoff blocks
  do not print it yet.
- Carried from v0.3.0: the PowerPoint handoff still reports letter-spacing as not present,
  because that column is still unauthored. The routing note about the built-in Word and
  PowerPoint skills still applies: {{routing_recheck}}.

## Fixed

- **v0.3.0's notes said panel count and folded-panel adjacency were "not modelled". That was
  false.** Page formats already carried the fold type and the panel widths of a tri-fold
  (99.5, 99.5 and 98 mm). The output never showed them, because 8 of 14 tables declared only
  some of their columns as displayable. The worst case was the CV's own regional table, which
  hid 12 of its 14 columns, the photo and date-of-birth norms among them. Every table now emits
  every column, and a test fails if one is dropped without a declared reason. (v0.4 phase 1.)
- v0.3.0's limitation "language carries no ranking weight" is partly addressed. A plain request
  in French or German now picks that language's variant. Language still does not weight ranking
  among competing matches.
- Quotes and devis used invoice headings ("Facturé à", "Détails de la facture"). A quote now
  has its own structure, with headings in English, French and German.
- The PowerPoint handoff always set a 10 × 5.63 inch slide whatever the page format said. It
  now takes the slide size from the page format.
- The form type scale had no heading size and the technical report scale had no heading levels.
  Both now do. The sizes are convention, not sourced.
- Palettes ranked from COLOURlovers now take their roles and their muted tint by the rule
  written before the palettes were seen. One palette the first pass had wrongly admitted was
  dropped; one it had wrongly excluded was admitted.
- Words that appear in every document type no longer tip the search.
- On Windows, output is now forced to UTF-8, and a manifest test that compared raw bytes now
  compares line-ending-normalised bytes.
- {{r5_fixes}}
- {{r6_fixes}}

## Breaking changes

- **Data columns.**
  - `doctypes` gains `Family` (required) and `Family Default`.
  - `doc-reasoning` gains `Design Key`.
  - Two tables are new: `designs` and `provenance`.
- **Brand kits built before this release.** {{old_kit_behaviour}}. Before the fix, one such kit
  installed anywhere made the whole resolver refuse every request, not only that brand's.
  Rebuild a kit by running `make_brand_kit.py` on its `brand.md`.
- **Default resolution changed.**
  - Plain "CV" now resolves to `cv-generic` instead of abstaining.
  - A French request picks `cv-france` and a German one `cv-dach`.
  - A US or Letter cue picks the Letter-size sibling.

  Pass `--doctype` to pin the old behaviour.
- **Retired designs.** {{retired_designs}}. The only one known today is `cv-editorial`. A
  `brand.md` naming a retired design fails with its line number.

## Sources and credits

Only feature codes and source URLs were recorded. No template artwork, text, logos or images
were copied. Collections counted:
- GitHub (repository stars);
- npm (monthly downloads: `jsonresume-theme-*`, `slidev-theme-*`);
- LibreOffice Extensions (download counts);
- the Microsoft Create gallery;
- Overleaf's gallery;
- the ARC Awards 2025 (MerComm);
- the Information is Beautiful Awards;
- D&AD.

Authorities:
- Europass;
- the GOV.UK Design System;
- USWDS;
- the NHS digital service manual;
- the Australian Bureau of Statistics forms design standards;
- AR 25-50;
- Purdue OWL;
- DIN 5008 (through the typst-letter-pro documentation);
- Butterick's *Practical Typography*.

Library sources:
- Google Fonts (popularity metadata);
- COLOURlovers (through the `nice-color-palettes` package);
- modularscale;
- the design systems named above, plus IBM Carbon, Material 3, Radix, Tailwind and Atlassian.

The work was planned, coded, cross-checked and reviewed by a team of AI agents under a written
protocol; the review files are `research/83`–`research/91`. {{credits}}

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
