# v0.2.0

## Scope — what this release contains

- **Section-by-section structure guidance for the 15 previously uncovered
  document families** (brochures, flyers, posters, reports, whitepapers,
  slide decks, presentations, forms, letters, quotes, offers, and the rest of
  the non-CV set): 52 canonical sections, 204 heading rows in English, French,
  and German, gated at 414 rows.
- **Duplicate-token validator rule**, opt-in per column.

## Fixed

- brochure-flyer-a4 listed one keyword twice in v0.1.0, slightly
  over-weighting that row; now gated.
- "make me a flyer" now abstains and offers the real candidates instead of
  resolving wrongly.
- The resolver's empty-list message no longer claims section guidance is
  deferred.

## Known limitations

- The ambiguous German deck phrase still resolves instead of asking.
- Language carries no ranking weight, so a French query does not favour the
  French CV row.
- Panel and slide count and folded-panel adjacency are not modelled at all.
- The non-CV heading sections carry one wording per language, with no
  variants.
- `infographic` is the one document type with no section order at all. It has
  no structure key, so it gets layout, typography, colour, and print guidance
  and nothing else.
- Three pairs of families share an identical section order, deliberately: the
  two brochures, letter and cover letter, and flyer and one-pager. What
  separates each pair is page format, not content.

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
