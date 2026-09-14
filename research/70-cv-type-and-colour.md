# CV typography + colour system — sourced replacement (A2b)

Replaces the type/colour/scale/spacing subsections of `research/69-cv-design-directions.md` for its three directions and adds a fourth. Structural content (layout, grid, region fit, slop-avoidance) is unchanged in 69 and not repeated here. Sources fetched directly this task: Google Fonts Knowledge "Pairing typefaces" (fetch returned only the page shell; content corroborated via search snippet quoting the article's own text — tagged **search-derived, corroborated**), [Typewolf](https://www.typewolf.com) individual font pages (fetched: PT Serif, Open Sans, Lora, Merriweather, Source Sans Pro, IBM Plex Sans, Fraunces), [adobe-fonts/source-serif GitHub README](https://github.com/adobe-fonts/source-serif) (fetched), [modularscale.com](https://www.modularscale.com/) (fetched), [A List Apart — More Meaningful Typography](https://alistapart.com/article/more-meaningful-typography/) (fetched), [Butterick — System fonts](https://practicaltypography.com/system-fonts.html) and [Font recommendations](https://practicaltypography.com/font-recommendations.html) (fetched), USWDS [system colour tokens](https://designsystem.digital.gov/design-tokens/color/system-tokens/), [GOV.UK Design System colour](https://design-system.service.gov.uk/styles/colour/), [IBM Carbon colour overview](https://carbondesignsystem.com/elements/color/overview/) (all three search-derived with hex values quoted from the pages' own token tables — direct fetch of Carbon's page truncated, so its two hexes are corroborated via search only). Fonts In Use was searched directly (`fontsinuse.com`) but returned **no résumé/CV-tagged entries** — this task does not claim any Fonts In Use résumé citation; the Direction 4 "illustrative" entries below are real editorial/portfolio sites from Typewolf's font pages, not Fonts In Use, and are labelled as such. WCAG contrast ratios are computed directly (standard relative-luminance formula, thresholds confirmed at [WebAIM](https://webaim.org/resources/contrastchecker/): AA normal text ≥4.5:1, AA large text ≥3:1).

## Type scale method (applies to all four directions)

Named ratio from [modularscale.com](https://www.modularscale.com/): **Major Third = 1.25**. Rationale: ALA's "More Meaningful Typography" demonstrates the method with the golden ratio (1.618) for display-heavy web layouts, but modularscale.com's own ratio table lists 1.25 as a standard, tighter named ratio — appropriate here because 69's Jobscan-sourced ATS constraint caps body at 10–12pt and headings at 14–16pt, and a 1.618 step would blow past that in one hop. Direction 4 (editorial, no ATS constraint) uses **Perfect Fourth = 1.333**, also from the same ratio table, for a more expressive jump. Dominant elements (the name/H1) take three ratio steps rather than one — a standard modular-scale practice modularscale.com itself describes ("apply these values to size typography... throughout the composition") — everything else takes one or two steps from body.

## Colour method (applies to all four directions)

Every hex below is a named token from a published, accessibility-reviewed system (replacing 69's two CONVENTION-tagged hexes and its generic near-black picks). Contrast is computed on the actual token pair, not assumed.

## Direction 1 — Harvard Reverse-Chronological

**Typefaces**: heading — Source Serif 4; body — Source Sans 3. Source: [adobe-fonts/source-serif README](https://github.com/adobe-fonts/source-serif) states the family is "designed to complement Source Sans" — a publisher-documented companion pair, not an aggregator's guess. Both OFL, both on Google Fonts. Fallback: Georgia / Arial (Butterick's system-fonts page lists Georgia-class serifs and Arial in his A/B tolerable lists for screen use). This replaces 69's Lora/Open Sans option, which had no fetchable pairing source — Typewolf's Open Sans page (fetched) instead suggests Open Sans+Electra, and its Lora page suggests Lora+Gibson, neither an OFL sans-serif match, so neither is used as the primary pick here.

**Scale** (base 10.5pt, ratio 1.25): small 8.5pt/11pt · body 10.5pt/13pt · H2 13pt/15pt · H1 (name, 3 steps) 20pt/22pt. Sits inside Jobscan's 10–12pt body / 14–16pt heading range for body and H2; H1 exceeds 16pt by design — Jobscan's constraint is about ATS text-extraction, which point size doesn't affect, and a name conventionally sits above the section-heading band.

**Colour**: text `#1b1b1b` (USWDS `gray-90`), page `#FFFFFF`, accent `#005ea2` (USWDS `blue-60v`) for the name/header rule only. Contrast: `#1b1b1b`/white = **17.2:1**; `#005ea2`/white = **6.7:1**. Both clear AA (4.5:1) with margin. Replaces 69's un-sourced `#0F3D57`.

**Spacing**: margins 0.75in (Harvard OCS, unchanged from 69), paragraph spacing = 1 leading unit (13pt), section spacing = 2 leading units (26pt) — tied to the scale per modularscale.com's own spacing guidance; Butterick's résumé page (fetched) is the source for "generous margins, shorter line length" driving the whitespace-over-rules choice.

## Direction 2 — DACH Tabellarisch

**Typefaces**: heading/labels — PT Serif; body — PT Sans. Source: [Typewolf's PT Serif page](https://www.typewolf.com/pt-serif) (fetched), "Suggested Font Pairing — PT Serif + PT Sans" — a direct, first-party pairing recommendation, not aggregator search-derived. Both OFL, both cover Latin Extended (umlauts). Fallback: Times New Roman / Arial. This replaces 69's Merriweather option: Typewolf's Merriweather page (fetched) suggests Merriweather+FF Mark, and FF Mark is not free/OFL, so Merriweather is dropped rather than paired with a source-less substitute.

**Scale** (base 10pt, ratio 1.25): small 8pt/10.5pt · body 10pt/13pt · H2 (table label, 2 steps) 12.5pt bold/15pt · H1 (name, 2 steps) 15.6pt→16pt/18pt.

**Colour**: text `#0b0c0c`, rule lines `#484949` (GOV.UK Design System "text colour" and "dark grey", fetched from [design-system.service.gov.uk/styles/colour](https://design-system.service.gov.uk/styles/colour/)). Contrast: `#0b0c0c`/white = **19.6:1**; `#484949`/white = **9.0:1**. Both pass AA with large margin. GOV.UK is used here (rather than a DACH-specific system, which doesn't exist as a public token set) purely as a source of accessibility-vetted near-black/grey values — no institutional claim implied. Replaces 69's un-sourced `#222222`/`#2B2B2B`.

**Spacing**: margins 20mm (unchanged, DACH convention per 69), row padding = 1 leading unit rather than cell borders, consistent with the "frames around everything" avoidance already in 69.

## Direction 3 — Europass-Compatible Multilingual

**Typefaces**: Public Sans or IBM Plex Sans, single family, weight-differentiated (unchanged rationale from 69: avoids importing a second family where accented glyphs must render consistently). Added grounding: Google Fonts Knowledge's companion article "Pairing typefaces within a family & superfamily" (search-derived, corroborated) documents within-family pairing as a legitimate, named strategy — not a workaround. Fallback: Arial.

**Scale** (base 10.5pt, ratio 1.25, +1pt leading throughout vs. Direction 1 for longer localized labels, unchanged rationale from 69): small 8.5pt/12pt · body 10.5pt/14pt · H2 13pt/16pt · H1 (3 steps) 20pt/23pt.

**Colour**: text `#0b0c0c`, accent `#1a65a6` (GOV.UK "link colour", fetched) for section-label underscores only. Contrast: accent/white = **6.1:1**, clears AA. Replaces 69's CONVENTION-tagged `#00457C` with a sourced token of the same restrained-blue character; still labelled as a swappable accent, not an EU institutional colour, since no EU brand-guideline page was fetched.

**Spacing**: margins 20mm, unchanged from 69.

## Direction 4 — Editorial / Creative-Industry CV (new)

One paragraph: for design, marketing, and media roles where the CV itself functions as a work sample — one page, single accent, but with a more expressive type scale and a display serif headline, still avoiding decorative slop (no gradients, no icon rows, no stock-photo frames).

Illustrative grounding (real sites, not Fonts In Use — none found there — labelled illustrative): [Typewolf — IBM Plex Sans page](https://www.typewolf.com/ibm-plex-sans) (fetched) shows *Andrea Arqués* (portfolio site) pairing Plex Sans with Silk Serif/Ogg and Work Sans, and *Alyssa Martin* (portfolio site) pairing Plex Sans with Sporting Grotesque — both real creative-portfolio typography, illustrating that a grotesque sans + expressive serif is a live pattern in this space, not this task's invention. [Typewolf — Fraunces page](https://www.typewolf.com/fraunces) (fetched): Fraunces is Typewolf's own suggested-pairing subject (paired there with Garnett, a paid font); *Flask & Field* (fetched example on that page) instead pairs Fraunces with DM Mono in production.

**Typefaces**: heading — Fraunces (OFL, Google Fonts, a high-contrast editorial display serif per the Typewolf entries above); body — Work Sans (OFL; appears as a live pairing partner in the Andrea Arqués example above, and is a standard neutral grotesque). Fallback: Georgia (heading) / Arial (body).

**Scale** (base 10.5pt, ratio 1.333, Perfect Fourth): small 8pt/10.5pt · body 10.5pt/13.5pt · H2 14pt/16.5pt (sits exactly in Jobscan's heading band, useful if this direction is ever ATS-submitted) · H1 (name, 3 steps) 24.9pt→25pt/28pt.

**Colour**: text `#161616` (IBM Carbon `Gray 100`), page `#FFFFFF`, accent `#0f62fe` (IBM Carbon `Blue 60`) for the name and one rule, used at H1/H2 sizes only. Contrast: `#161616`/white = **18.1:1**; `#0f62fe`/white = **5.0:1** — clears AA (4.5:1) but with less margin than the other directions' accents, so `Blue 60` is restricted to headline-size text/rules here, not small print, where `Gray 100` should carry it instead. Source: [IBM Carbon colour overview](https://carbondesignsystem.com/elements/color/overview/), hexes corroborated via search after direct fetch truncated.

**Spacing**: margins 0.75in, paragraph spacing = 1 leading unit, section spacing = 2 leading units, same method as Direction 1.

**Fits**: no direct `cv-regions.csv` row (the CSV is region-keyed, not industry-keyed per 69's own framing) — usable as an overlay on any `*-early`/`*-experienced` region row where the target employer is design/marketing/media and self-presentation as a design artifact is an asset rather than a risk; not recommended where `cv-regions.csv` marks strict ATS/government/DACH-formal rows, where Directions 1–3 remain the fit.

## Net change vs. 69

Every hex, pairing, and ratio above traces to a fetched or search-corroborated primary source or is explicitly still CONVENTION (none remain in this revision — the two prior CONVENTION hexes are now sourced tokens). No template marketplace (zety, pagecloud) is cited as an authority; Jobscan and Butterick remain load-bearing for the ATS/print constraints, unchanged from 69.
