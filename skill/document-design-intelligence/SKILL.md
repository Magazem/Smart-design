<!-- version: 0.0.1-dev (generated at build - do not edit) -->
---
name: document-design-intelligence
description: "Creates and fixes print/office documents: CVs, resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht. Triggers: make me a CV, write a note interne, turn this into a brochure, I need slides for Monday, format this report, fais-moi une fiche, erstelle ein Angebot; quality fixes: looks like AI, looks generic, make it professional, fix the layout. Applies sourced layout, typography, color, print, and ATS rules. When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a plain conversion or edit with no design ask, use that format's own skill instead. Not for web or app UI/UX design (use UI/UX Pro Max for screens)."
---

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
and `.pptx` output. It does not render Office formats itself: hand that block to
the built-in `docx` or `pptx` skill to build the file. PDF is the exception —
this skill renders PDF itself. After rendering, run `ddi.py preflight` on the
artifact; on refuse, fix the specific problem it names and rerun before returning
anything to the user.

For PDF, the tier that is actually delivered is: PDF/X-4 structurally emitted;
conformance not independently verifiable with open tooling.

## Section-order guidance is CV-only today

`resolve` returns a full section order only for `cv-experienced` and
`cv-academic`. Every other document type resolves with no section order — the
resolver says so explicitly rather than returning an empty list. In practice:
this skill gives full section-by-section structure guidance for CVs today, and
layout/typography/colour/print guidance for every other document type it covers.

## Give it your brand

Write one `brand.md`, run `scripts/make_brand_kit.py` on it, get a brand kit
back. See `README.md` in the project repository for the full workflow.

## Attribution

See `NOTICE.md`.
