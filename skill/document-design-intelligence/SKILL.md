---
name: document-design-intelligence
description: "Creating any document type below is still this skill's job even as Word or PowerPoint; defer to that format's own skill only when the user names it for a plain conversion or edit with no design ask. Creates and fixes print/office documents: CVs, resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters, quotes, offers, infographic; also note interne, fiche, courrier, lettre, affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht, invoice, memo, proposal, one-pager, facture, devis, rapport, Rechnung, Formular, Broschüre, infographie, Infografik. Triggers: make me a CV, write a note interne, turn this into a brochure, I need slides for Monday, format this report, fais-moi une fiche, erstelle ein Angebot; appearance fixes: looks like AI, looks generic, make it look professional, fix the layout. Applies sourced layout, typography, color, print, and ATS rules. Not for web or app UI/UX design (use UI/UX Pro Max for screens)."
---
<!-- version: 0.0.1-dev (generated at build - do not edit) -->
# Document Design Intelligence

This SKILL.md is a thin router. It sends the model to the right script for the
job; the design rules themselves live in `data/base/*.csv` and are reached through
`scripts/ddi.py`, not restated here.

## Workflow

Run `ddi.py`'s subcommands in this order:

1. `ddi.py check` — validate the data
2. `ddi.py resolve --query "<text>" [--brand <slug>] [--json]` — resolve one request
3. If the user expresses a style, tone, or industry preference (e.g. "make it look
   editorial", "something for a design portfolio", "keep it formal/DACH-style"), run
   `ddi.py designs --doctype <key> [--query "<their wording>"]` and offer the top 3
   designs it lists (Display Name, Best For, Evidence Class) instead of guessing; once
   they pick one, re-run step 2 as `ddi.py resolve --doctype <key> --design <design_key>
   --json` so the rest of the pipeline resolves from that design's own style/palette/
   typeface. Skip this step if the user has no such preference — the doctype's own
   default design (already the fitness choice, e.g. ATS-safe for a CV) applies with no
   extra step. `ddi.py library <palettes|typefaces|type-scales|doc-styles> [--query]` browses
   the grand library the same way when building a brand kit.
4. `ddi.py preflight <file> [--json]` — verify a rendered file
5. `ddi.py handoff --json <resolved.json> --format docx|pptx|pdf|png` — render-handoff block

Do not skip step 2 and go straight to free-form generation — that is the activation
failure this skill exists to prevent.

## Rendering is a handoff, not ours

`handoff` reads a `resolve` result and prints a render-handoff block — resolved
fonts, colors, spacing, page format, and the constraints to check — for `.docx`
and `.pptx` output; a plain-text answer in chat is a valid output too, with no
handoff block and no file. It does not render Office formats itself: hand that block to
the built-in `docx` or `pptx` skill to build the file. PDF is the exception —
this skill renders PDF itself. After rendering, run `ddi.py preflight` on the
artifact; on refuse, fix the specific problem it names and rerun before returning
anything to the user.

For PDF, the tier that is actually delivered is: PDF/X-4 structurally emitted;
conformance not independently verifiable with open tooling.

## Section-order guidance

`resolve` now returns a full section order for every document family this
skill covers, `infographic` included — it resolves `infographic-canvas`
(headline, key-points, call-to-action). Every document type gets layout,
typography, colour, and print guidance alongside its section order.

The output format never changes this order or these headings: a plain-text
reply in chat gets the same resolved sections and headings as a rendered
file. Only the rendering changes.

## Give it your brand

Write one `brand.md`, run `scripts/make_brand_kit.py` on it, get a brand kit
back. See `README.md` in the project repository for the full workflow.

## Attribution

See `NOTICE.md`.
