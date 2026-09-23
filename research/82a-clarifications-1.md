# research/82a — Clarifications round 1 (orchestrator, 2026-09-23)

These are CLARIFICATIONS of research/82 text as written, raised by the first coders of cv, deck,
brochure and flyer. None changes a pre-registered rule; where a coder's reading departed from the
literal text, the literal text wins and the affected items are recoded. Binding on all coders
and second coders from now on.

C1 **image-hero (§4 header treatment).** Literal reading: an image/illustration that intersects the
   top 20% of page 1 AND whose own area is ≥30% of the PAGE area. Not "30% of the strip".
   → brochure first coder recodes header treatment for every brochure item (affects the modal
   archetype). Deck `title-slide layout = split` uses the same test: image ≥30% of slide area.
C2 **Uncodeable (§3.3)** covers both "no preview" and "preview present but not the item's design"
   (wrong/unrelated asset, spinner, headshot). Such items are skipped, not counted in N.
C3 **Blank scaffolds.** A template whose preview shows no design content (empty fold guides,
   placeholder boxes only) has nothing to code → uncodeable, removed from N (brochure LO blanks).
C4 **Multi-design repos/packages:** code the first design in RENDERED README order.
C5 **Redirected catalogues.** create.microsoft.com redirecting to *.cloud.microsoft is the same
   vendor catalogue; code it if items are in the static payload. If the target is an SPA with no
   static item data, the catalogue is "unreachable <date>", disclosed, never reconstructed.
C6 **Dead documented preview paths** may be replaced by the item's own published preview (repo
   raw image, npm README image) if disclosed per item.
C7 **Title-slide-only previews (deck):** variant features that need body content (density, rules)
   are coded `unknown`; filling then uses the family default for that variant (§7 last sentence).
   Deck background is coded from the title slide.
C8 **A3 (text over busy fill):** applies to any text set directly on a gradient, texture or photo.
   Text on a flat opaque panel placed over a photo is admissible.
C9 **Contrast (A6) from thumbnails:** eye judgement is allowed only when evidently far from the
   threshold; any pair plausibly within 3.5–5.5:1 must be sampled with lib/color.contrast_ratio.
   All thumbnail-sampled ratios are estimates and are disclosed as such.
C10 **Second-coder sample is FAMILY-WIDE** (§7): all coded ids of the family across corpora,
   sorted, then the seeded formula. Per-corpus samples computed by first coders are superseded.
