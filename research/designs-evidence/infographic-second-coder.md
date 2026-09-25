# Infographic - independent second coder (seed `82a:infographic`)

Coder: Design Researcher (second coder; never opened `infographic-corpus-iib.md` or research/91). Date 2026-09-25.

## Method
Read only research/82 sections 4-5, 82a-general.md, 82a-clarifications-1..5 (incl. C30: charts are marks) and `infographic-items-iib.csv` (12 ids; C11). Page = the preview image (a mockup or canvas around a sheet is ignored). Previews downloaded to a scratch dir (deleted after use) and viewed. Measurements with PIL: background = most common colour class on a 20x20 grid (82a-general B1a), chromatic hue histogram in 30-degree bins (B4-B6), and `lib/color.contrast_ratio` on sampled text/background pairs (C9: thumbnail samples are estimates). Title = the heading block (largest text unless it is a chart label); header tests per 82a-general A.2; density per 82 section 4 (text-block share of the sheet). Only the seven section 4 features plus admissibility (A1-A8) were coded; infographic has no family-specific feature and no family fail constraint.

## Sample
Sorted ids (12): IIB:029 IIB:049 IIB:050 IIB:075 IIB:116 IIB:125 IIB:135 IIB:139 IIB:142 IIB:148 IIB:163 IIB:171

`random.Random("82a:infographic").sample(ids, max(min(10, len(ids)), math.ceil(0.25*len(ids))))` gives n = 10 in this draw order: IIB:148 IIB:171 IIB:142 IIB:139 IIB:135 IIB:075 IIB:049 IIB:116 IIB:125 IIB:163.

## Coded table (n = 10; rows in sorted order)

| id | columns | head | body | colour | header | rules/boxes | density | adm | measurements / notes |
|---|---|---|---|---|---|---|---|---|---|
| IIB:049 | grid | serif | serif | multi | plain-left | rules | airy | y | columns: small-multiples grid of 50 state glyphs (tiles) + intro column; colour: bg #fbfbe1 excluded, green marks (~150 deg) + pink dots (~330 deg) = 2 clusters, each in many elements; header: title top-left, legend panels to its right are not meta text, no qualifying rule; rules: dotted vertical dividers + rule under legend heading; body #58585a on #fbfbe1 = 6.76 (sampled) |
| IIB:075 | 1 | display | sans | one-accent | plain-left | rules | airy | n | A3: maroon-to-orange gradient behind all text incl. the 5-line "path of totality" block and ring lyrics (bg samples #3d0002 / #54001d / #701a0e); title right-aligned in upper right (align=right); colour: orange/red glow marks 330-30 deg join into one cluster; thin frame line -> rules |
| IIB:116 | 2-sidebar | sans | sans | multi | plain-left | rules | standard | n | A3: radial banded grey gradient behind the left text column (bg samples L 40-84 of 255, text over it est. ~4:1) and the right lists; title "all the ways of winning in sports" left-aligned inside a black hemisphere (not top); rainbow line marks = multi; coloured rules above the lists -> rules |
| IIB:125 | 3+ | serif | sans | mono | plain-left | rules | airy | y | colour: yellow #ffcb05 panel covers ~88% of the sheet so it is the background (B1a) -> mono (sensitivity: fill-blocks under section 4(a)); body black on yellow 13.8; white heading/legend text on yellow = 1.52 recorded, not body text so A6 not applied (borderline); heading slab serif heavy condensed (glyph judgement); many text columns around the chart -> 3+; axis/arrow lines -> rules |
| IIB:135 | 1 | sans | sans | multi | plain-left | rules | airy | y | title centre ~42% of page width (>5% from centre) -> plain-left; underline under title is 21% of page (<80%); tube marks in navy/yellow/teal/light-blue/red/pink = multi; map is data (C30); 3D gloss on marks only; body #110d0e on white 19.3 |
| IIB:139 | grid | serif | serif | multi | plain-left | boxes | airy | y | dashboard: KPI cards + bar/scatter panels + callout notes -> grid; bg cream excluded; orange and blue marks + pink/teal = multi; intro text #666467 on white panel 5.86, callout #232323 on #fdfbef 15.1; title top-left, legend at right is not meta |
| IIB:142 | 2-sidebar | sans | serif | fill-blocks | plain-left | boxes | airy | n | A3: 3+ line description blocks set directly on the painted, textured treemap fills (e.g. PORTRAIT 1,013 WORKS, GUITAR 517) and white-on-yellow/orange labels est. <4.5:1 (A6 estimate); treemap = chart marks (C30) but fills >10%; narrow right column holds title + body; condensed caps sans title |
| IIB:148 | 3+ | serif | serif | fill-blocks | plain-left | boxes | standard | y | two-page newspaper spread on a blue-grey mockup canvas (canvas ignored, A3 of 82a-cv); blue/red/yellow stream charts are marks (C30) but cover ~12% of the sheet -> fill-blocks; title on a flat pale-blue chart fill that runs the full page height (band d fails); body #22180f on #ebebeb 14.6; portrait sketches are 4 different drawings; callout boxes -> boxes |
| IIB:163 | 1 | sans | sans | multi | plain-left | none | airy | y | single ring chart of multicolour strokes (marks, C30); only text is a small legend at lower right ("Immigration to the U.S. 1830-2016") = title (align right/bottom, not top) and 1850-2000 tick labels; no body text |
| IIB:171 | 1 | serif | serif | multi | plain-left | none | airy | y | four circular charts = marks; bg #e9e5e4 excluded; yellow/red/purple/blue/green marks = multi; title block centre ~41% (>5% from centre); body #646363 on #e9e5e4 = 4.79 (sampled, near threshold); slab serif heading/body (Google SERIF incl. slabs) |

Admissible 7 / 10; excluded IIB:075 (A3), IIB:116 (A3), IIB:142 (A3 + A6 estimate).
