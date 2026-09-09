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
