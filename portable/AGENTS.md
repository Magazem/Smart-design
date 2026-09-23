# AGENTS.md -- Document Design Intelligence (portable)

Operating instructions for ANY AI agent producing a print/office document (CV,
cover letter, letter, memo, form, brochure, flyer, poster, report, whitepaper,
proposal, quote, invoice, slide deck, one-pager, infographic) -- Claude,
ChatGPT, Grok, Gemini, or any other assistant, with or without code execution.
Read this file, then open `DDI-LIBRARY.md` for the exact values it references.

## 1. Identify the family and doctype

Match the user's request against a family below by its trigger words (the
request need not use these exact words -- match on intent, e.g. "Lebenslauf"
or "note interne" both count):

- **cv** -- academic cv, scientific cv, faculty cv, publications list, research cv, grants
- **cover-letter** -- cover letter, motivation letter, job application letter, write my cover letter, lettre de motivation, rédige ma lettre de motivation
- **letter** -- letter, business letter, formal letter, official letter, correspondence, write a letter
- **memo** -- internal memo, note, memorandum, staff note, announcement, write a memo
- **form** -- form, fillable form, intake form, application form, registration form, print and fill
- **brochure** -- gatefold, gate-fold brochure, double gate fold, four panel brochure, dépliant portefeuille, brochure porte
- **flyer** -- flyer, single sheet flyer, a4 flyer, promotional sheet a4, poster-sized handout, flyer a4
- **poster** -- poster, wall poster, event poster, a3 poster, large format print, affiche
- **report** -- long report, full report, annual report, report with table of contents, toc, running heads
- **whitepaper** -- whitepaper, white paper, technical paper, position paper, citations, bibliography
- **proposal** -- proposal, project proposal, business proposal, pitch document, write a proposal, proposition
- **quote** -- quote, price quote, quotation, estimate, devis, devis client
- **invoice** -- invoice, bill, line items, invoice document, tabular invoice, facture
- **deck** -- slides, presentation, webinar deck, screen-share deck, deck as document, self-contained deck
- **one-pager** -- one pager, one-page summary, single page brief, fact sheet, one page document, une page
- **infographic** -- infographic, data visual, visual summary, statistics graphic, infographie, visuel de données

Once you have a family, open `DDI-LIBRARY.md`'s `## Family: <family>` section
and pick the specific doctype whose trigger keywords and region/language best
match the request (e.g. family `cv` has separate doctypes for `cv-us`,
`cv-uk`, `cv-dach`, `cv-eu-europass`, `cv-academic`, ...).

## 2. Pick a design

Every doctype has a default design (the first one in that family's "Designs
(ranked)" table whose Style/Palette/Typeface match the doctype's own resolved
values in `DDI-LIBRARY.md`). Use the default UNLESS the user states a style,
tone, or industry preference ("editorial", "formal DACH-style", "for a design
portfolio") -- in that case, list the family's top 3 ranked designs (name,
evidence class, best for) and ask which one they want, then apply THAT
design's own Style/Palette/Typeface keys instead of the default.

## 3. Apply EXACT values from the pack

For the chosen doctype (and design, if overridden), copy from `DDI-LIBRARY.md`
verbatim:
  - page format: trim size + all four margins + bleed
  - fonts: heading and body family, with their safe-stack fallback if you
    cannot embed a font
  - type scale: size and leading per role (h1/h2/h3/lead/body/caption/label)
  - palette: hex value per role (primary/secondary/accent/background/
    foreground/muted) -- every pack palette already meets WCAG 4.5:1 text
    contrast on its own text-safe role pairs
  - section order and headings, in the user's own language (en/fr/de) where
    authored; if a section has no wording in that language, use whichever
    language IS authored and say so
  - the doc style's rule weights, table rules/fills, emphasis mechanism, and
    its checklist items
  - the doctype's key constraints and their severity (fail = must fix before
    delivering; warn = flag it, deliver anyway)

## 4. Never invent

Never introduce a font, colour, or size that is not in the resolved doctype's
own block in `DDI-LIBRARY.md`. Never add multi-column layouts, text boxes,
icon-only skill bars, photos, gradients, emoji, or decorative borders unless
the doctype's own style/checklist explicitly allows them -- see the anti-slop
checklist below.

## 5. Anti-slop checklist (run before returning the document)

`DDI-LIBRARY.md`'s `## Anti-slop checklist` lists every mechanical check and
anti-pattern token this library ships. Before returning a document, check it
does not contain any `fail`-severity item; flag (do not silently ignore)
`warn`-severity items to the user. A resolved doctype's own key-constraints
list (in its `DDI-LIBRARY.md` block) may add doctype-specific fail items on
top of these.

## 6. Prefer code execution when it is available

If you can run python3, prefer the actual skill instead of this pack: fetch
the `document-design-intelligence` skill ZIP (see `INSTALL.md`) and run
`python3 scripts/ddi.py resolve --query "<request>" --json`, then
`ddi.py handoff --json <result> --format docx|pptx|pdf|png`, then render and
run `ddi.py preflight <file>` on the result. That path resolves the SAME data
this pack is generated from, with live per-request search and a mechanical
preflight gate this static pack cannot run for you.

## 7. Building a brand kit from the grand library

If the user wants their own brand's document instead of a generic one, and
you have no code execution (so `make_brand_kit.py` is not available), compose
one by hand from `DDI-LIBRARY.md`'s `## Grand library`:
  - **Palette**: pick one generic palette whose tone matches the brand (e.g.
    restrained/neutral vs. high-contrast/bold); every listed palette already
    satisfies >=4.5:1 text contrast on its text-safe role pairs, so picking
    ANY one keeps that guarantee -- do not hand-mix roles from two palettes.
  - **Typeface pairing**: pick one pairing; keep it to the pairing's own
    families (heading + body -- at most 2 families total; do not add a third
    "just for emphasis", per the anti-slop checklist's font-family-count
    rule).
  - **Type scale**: pick the scale grouped for the right medium (print /
    projection / screen) for the doctype's own artifact class.
  - Apply the picked palette/pairing/scale the same way step 3 above applies
    a doctype's own resolved values -- do not invent a hex, family, or size
    outside the two tables you picked from.
