# T10 `structures.csv` — notes

Scope: the 17 GENERIC `structure_key` values `research/26-t1-doctypes-draft.csv` references
(the 4 ENS-scoped ones — ens-formulaire, ens-note, ens-slides, ens-social — are out of scope,
per brief). 17 data rows, 9 columns, header matches the manifest order.

## The headline finding: `headings.csv` only covers CV sections

`skill/document-design-intelligence/data/base/headings.csv` has 81 rows but only **11**
distinct `canonical_section` values, and every one of them is a CV/resume section:
certifications, contact, education, experience, languages, projects, publications,
references, skills, summary, volunteering. Nothing exists for letters, memos, forms,
invoices, brochures, flyers, posters, decks, one-pagers, reports, proposals, or
whitepapers. `Section Order` is a group-FK list into exactly this column
(`schema-manifest.json` → `structures.foreign_keys."Section Order"` = `{table: headings,
column: canonical_section, group: true, list: true}`), checked token-by-token with no
tolerance for a `?`-suffixed "optional" marker (the schema doc's own worked example,
`contact;summary?;...`, would NOT pass `validate_data.py`'s literal token match — I did not
carry that `?` convention into this draft for that reason).

Result: **only `cv-academic` and `cv-experienced` get an authored `Section Order`.** All
other 15 rows ship `Section Order` empty, on purpose, rather than filled with an invented or
partial token.

## Per-row `Section Order` sourcing

- **`cv-experienced`**: `contact;summary;experience;education;skills;certifications;projects;
  publications`. SOURCED — `research/03-document-design-knowledge.md` line 71-73, "Section
  ordering [CONVENTION, near-universal]": Contact -> Summary -> Experience -> Education ->
  Skills -> optional Certifications/Projects/Publications. I did not add
  languages/references/volunteering; the source doesn't name them, and I'm not extending a
  cited convention past what it says.
- **`cv-academic`**: `contact;summary;education;publications;experience;projects;
  certifications;skills;languages;references`. CONVENTION, UNCITED — no file in this repo
  states an academic-CV order; this is standard academic-CV practice (education and
  publications lead, ahead of a general "experience" block) reproduced from general
  knowledge, not sourced to a project doc. Flagging so Coverage/downstream doesn't mistake it
  for equally-sourced as the row above it.
- **`cover-letter-standard`**: left EMPTY, not filled with the one token that would technically
  pass (`contact`). A cover letter's real skeleton is opening/salutation -> body -> closing ->
  signature; none of those are `canonical_section` values, and `contact` alone doesn't
  represent that skeleton honestly — a single-token "order" isn't an order. Brief's own
  wording called this one "arguable"; I judged it the wrong side of arguable to ship.
- **All other 14 rows** (brochure-3panel, brochure-gatefold, deck-standard,
  flyer-single-sheet, form-standard, invoice-standard, letter-standard, memo-standard,
  one-pager-standard, poster-single-canvas, proposal-standard, report-long-toc, report-short,
  whitepaper-standard): EMPTY. See missing-tokens list below.

## `canonical_section` values T10 needs and headings.csv lacks

By document family (what each genuinely needs, not proposed slugs to add — that's T13/headings
authoring work, out of scope here):

- **Letters** (cover-letter-standard, letter-standard): opening/salutation, body, closing,
  signature-block. (`contact` partially covers a letterhead/address block, nothing else.)
- **Memos** (memo-standard): header-block (to/from/date/re), body, distribution/cc-list.
- **Forms** (form-standard): form-header, field-group, signature-block.
- **Invoices** (invoice-standard): bill-to, line-items, totals, payment-terms.
- **Brochures** (brochure-3panel, brochure-gatefold): cover-panel, inside-panel, back-panel,
  call-to-action.
- **Flyers** (flyer-single-sheet): headline, body, call-to-action.
- **Posters** (poster-single-canvas): headline, visual, call-to-action.
- **Decks** (deck-standard): title-slide, agenda, content-slide, closing-slide.
- **One-pagers** (one-pager-standard): headline, overview, key-points. (`contact` partially
  covers a footer contact line.)
- **Reports** (report-short, report-long-toc): title-page, executive-summary, body, appendix.
  report-long-toc additionally needs: toc, chapter.
- **Proposals** (proposal-standard): title-page, executive-summary, scope, pricing, terms.
- **Whitepapers** (whitepaper-standard): abstract, introduction, body, bibliography.

This list is the scope of the T13 headings-authoring work that has to follow — 29 dangling
`Structure Key` gate lines don't close just because this row exists; they close once T13 gets
these tokens.

## `Heading Depth Max` / `TOC Depth` / `Front Matter Numbering` reasoning

All three are enum/int columns filled for every row (unlike `Section Order`, they aren't FK
columns and the manifest's `enums` block has no empty option for `Front Matter Numbering` or
`Cross-Ref Style` — an empty cell would fail the enum check, not pass silently).

- **`Heading Depth Max`**: 0 for cover-letter-standard/letter-standard (block-format business
  correspondence conventionally carries no internal headings); 1 for the visually flat/
  single-level doctypes (brochure-3panel, brochure-gatefold, deck-standard [slide title =
  H1 only], flyer-single-sheet, form-standard, invoice-standard, memo-standard,
  poster-single-canvas); 2 for cv-academic/cv-experienced (section heading + occasional
  sub-entry level) and report-short/one-pager-standard; 3 for proposal-standard,
  report-long-toc, whitepaper-standard, per `research/03-document-design-knowledge.md`
  §D "Hierarchy depth [CONVENTION] cap reader-facing heading depth at H1-H3."
- **`TOC Depth`**: 0 everywhere except `report-long-toc` (2). Only that doctype's name and
  T1 description ("long-form with table of contents") assert a TOC exists; §D's own TOC
  convention is "include down to H2 (occasionally H3)," so 2 is the sourced default depth.
  I did NOT give `whitepaper-standard` a TOC — T1's whitepaper description
  ("technical paper... citations, bibliography, references") doesn't assert one the way
  report-long-toc's name does, so I treated it as no-TOC by default. This is a judgment call,
  not a sourced fact — flagging it as reversible if someone has a citation either way.
- **`Front Matter Numbering`**: `roman` only for report-long-toc (it's the only row with a
  TOC/front matter to number), `none` everywhere else, per §D "front matter... numbered in
  lowercase roman numerals; body restarts at Arabic 1" — the rule only fires where front
  matter exists.
- **`Caption Position`** (`fig=below;table=above`) and **`Cross-Ref Style`** (`numbered`) are
  uniform across all 17 rows. Both are sourced to §D ("Figure captioning... caption below the
  figure, caption above the table"; "Cross-references... by assigned number, never by
  relative position") and to `09-library-schema.md`'s design note that `Cross-Ref Style:
  positional` "exists only so it can be forbidden." `research/09-library-schema.md:1600`
  treats the Caption Position convention as applying beyond just long reports (it's invoked
  for `invoice-standard`'s tabular captions too), so I applied it uniformly rather than only
  to the report family; rows without figures/tables simply never trigger the rule.
- **`Heading Language`**: `en` for all 17 rows — these are the generic (non-brand,
  non-region) structures; the schema's own worked example for `cv-experienced` uses `en`.

## VERIFY (by script, not by eye)

- csv.reader parses clean at 9 columns on every row; 17 data rows. PASS
- Key set exactly equals the 17 generic keys the brief lists — no ENS rows, none missing. PASS
- Every `Section Order` token exists in `headings.csv`'s `canonical_section` column (checked
  against all 11 values; only cv-academic/cv-experienced rows are non-empty). PASS
- Every enum cell (`Heading Language`, `Front Matter Numbering`, `Cross-Ref Style`) is one of
  the allowed values. PASS
