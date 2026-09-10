---
name: document-design-intelligence
description: "Creates and fixes print/office documents: CVs, resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht, invoice, memo, proposal, one-pager, facture, devis, rapport, Rechnung, Formular, Broschüre. Triggers: make me a CV, write a note interne, turn this into a brochure, I need slides for Monday, format this report, fais-moi une fiche, erstelle ein Angebot; appearance fixes: looks like AI, looks generic, make it look professional, fix the layout. Applies sourced layout, typography, color, print, and ATS rules. Creating any document type above is still this skill's job even as Word or PowerPoint; defer to that format's own skill only when the user names it for a plain conversion or edit with no design ask. Not for web or app UI/UX design (use UI/UX Pro Max for screens)."
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
3. `ddi.py preflight <file> [--json]` — verify a rendered file
4. `ddi.py handoff --json <resolved.json> --format docx|pptx|pdf` — render-handoff block

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
skill covers, with one exception: `infographic`, which has no Structure Key
and so gets no section order — the resolver says so explicitly rather than
returning an empty list. Every document type, infographic included, still
gets layout, typography, colour, and print guidance.

The output format never changes this order or these headings: a plain-text
reply in chat gets the same resolved sections and headings as a rendered
file. Only the rendering changes.

## Give it your brand

Write one `brand.md`, run `scripts/make_brand_kit.py` on it, get a brand kit
back. See `README.md` in the project repository for the full workflow.

## Attribution

See `NOTICE.md`.
