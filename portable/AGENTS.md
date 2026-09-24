# AGENTS.md -- Document Design Intelligence (portable)

Operating instructions for ANY AI agent producing a print/office document (CV,
letter, memo, form, brochure, flyer, poster, report, whitepaper, proposal, quote,
invoice, slide deck, one-pager, infographic), with or without code execution.
Read this file, then use `DDI-LIBRARY.md` for the exact values it references.

## 1. Identify the family and doctype

Match the request to a family by intent (e.g. "Lebenslauf", "note interne"):

- **cv** -- academic cv, lebenslauf, europass, cv, resume, scientific cv
- **cover-letter** -- cover letter, motivation letter, job application letter, write my cover letter, lettre de motivation, anschreiben
- **letter** -- letter, business letter, formal letter, official letter, correspondence, write a letter
- **memo** -- memo, internal memo, note, memorandum, staff note, announcement
- **form** -- form, fillable form, intake form, application form, registration form, print and fill
- **brochure** -- gatefold, brochure, gate-fold brochure, trifold, double gate fold, tri-fold
- **flyer** -- flyer, single sheet flyer, a4 flyer, handout, promotional sheet a4, promotional sheet
- **poster** -- poster, wall poster, event poster, a3 poster, large format print, affiche
- **report** -- long report, report, full report, short report, annual report, summary report
- **whitepaper** -- whitepaper, white paper, technical paper, position paper, citations, bibliography
- **proposal** -- proposal, project proposal, business proposal, pitch document, write a proposal, proposition
- **quote** -- quote, price quote, quotation, estimate, devis, devis client
- **invoice** -- invoice, bill, line items, invoice document, tabular invoice, facture
- **deck** -- deck, slides, handout deck, presentation, leave-behind, webinar deck
- **one-pager** -- one pager, one-page summary, single page brief, fact sheet, one page document, une page
- **infographic** -- infographic, data visual, visual summary, statistics graphic, infographie, visuel de données

Open `DDI-LIBRARY.md` `## Family: <family>` and pick the doctype whose keywords
and region/language fit (family `cv`: `cv-us`, `cv-uk`, `cv-dach`, ...). CV with
no country stated: ask once for the target country, or use `cv-generic` and say
so. A French CV with no country cue is `cv-france`; with Belgium/Switzerland/
Quebec use `cv-eu-generic` in French; German is `cv-dach`. Name particles
("de la", "von der") are not language cues. Plain "brochure"/"flyer" means A4 unless
the user says US/Letter; a request naming two documents (a CV and a cover letter):
ask which first. Write in the user's language; a doctype's `language:` is only a default.

## 2. Pick a design

The default design is the family design whose Style/Palette/Typeface equal the
doctype's own. Use it UNLESS the user states a style, tone or industry
("editorial", "for a design portfolio"): then list up to 3 designs from the
family's "Designs (ranked)" table whose Best-for fits their wording (fewer if
the family has fewer) and ask. An override replaces Style/Palette/Typeface with
the design's: look them up under `## Grand library` (Doc styles, Palettes,
Typeface pairings) and use the typeface's own type scale. Page format, section
order and constraints stay the doctype's.

## 3. Apply EXACT values

Copy verbatim from the doctype block (and chosen design): page format (trim,
margins, bleed, print geometry: panels, DPI, folio), fonts, type scale, palette
hexes, the doc style's rules/tables/emphasis/checklist, section order with
headings, the doctype's anti-patterns and constraints WITH their limits.
- Fonts: obey the block's `font rule by output format`: `safe-stack` (docx)
  means name the fallback fonts, not the design's own; `embed` may use the
  design's fonts.
- Colour: text only in text-safe roles; fill-only roles are fills, never text.
- Missing role size (e.g. no h1): reuse the nearest listed role with weight
  emphasis; never create a size.
- CV: the regional variant for the user's country and seniority band (early =
  under ~3 years or a recent graduate) sets section order and limits over the
  structure order. Photo only if the variant says `customary` AND the user
  supplies one; ATS-strict target: never.
- `conditional constraints` apply only when their condition holds (e.g.
  professional-print only if going to a print shop).

## 4. Never invent

No font, colour or size outside the doctype block or the chosen design's
resolved values. Add no layout or decoration the doctype's own anti-patterns,
style and checklist forbid; an anti-pattern listed for another category does
not bind this one.

## 5. Check before returning

Check the document against its doctype's `anti-patterns` and `key constraints`
and the `## Anti-slop checklist`. `fail` = fix before delivering; `warn` = flag
it. Checks you cannot verify without tools (embedded fonts, PDF/X, DPI): list
them as "unverified", never as passed.

## 6. Delivering without code execution

Never claim to have produced a .docx/.pptx/.pdf you did not create. Deliver
either (1) one self-contained HTML file (CSS `@page` size and margins, font stack
with fallback, exact hex and pt values) to print or save as PDF, or (2) the
content in section order plus an exact style sheet (named styles: font, size,
leading, colour per role; page setup and margins) to apply in Word/PowerPoint.
With code: install the skill ZIP (see `INSTALL.md`) and run `python3
scripts/ddi.py resolve --query "<request>" --json`, then `ddi.py handoff`, render,
`ddi.py preflight` -- same data, plus live search and a mechanical gate.

## 7. Brand kit from the grand library (no code)

Interview first (field, three tone adjectives, colours/logo, families, languages, formats).
1. Palette: ONE row, all six roles (highest-scoring row with a cited source; never mix rows). A
brand colour becomes the single accent over one neutral row (`print-neutral`, `lib-govuk-ink`);
if it fails 4.5:1 keep it as a fill-only accent, never for text. Body text must pass 4.5:1.
2. Typefaces: ONE pairing, max 2 families, its fallbacks as listed; tell the user Word uses the
fallback. 3. Type scale per medium: print = the pairing's scale, projection =
`lib-perfect-fourth-projection`. 4. A design per family (rank 1 unless Best-for fits the tone;
say when only a convention design exists). 5. Write `brand.md` (slug, palette, typefaces,
doctypes, designs, scales, languages). Invent no hex, family or size outside those rows.
