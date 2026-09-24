# research/designs-evidence/flyer-second-coder.md — independent second coder (falsifier), 2026-09-24

**Independence.** Coded from `research/82-design-ranking-protocol.md` §4/§5, `research/82a-general.md`
(header treatment + colour use, supersedes §4 for flyer), `research/82a-clarifications-1.md`
through `-5.md`, and `research/designs-evidence/flyer-items.csv` only. No other file under
`research/designs-evidence/` was opened; `research/91-family-status.md` and
`research/82b-shortfall-sources.md` were not opened. First-coder codes were never seen.

**Method.** Ids sorted lexicographically from `flyer-items.csv` (20 ids). Sample:

```python
import math, random
ids = sorted([...])  # the 20 ids
n = max(min(10, len(ids)), math.ceil(0.25 * len(ids)))  # = 10
sample = random.Random("82a:flyer").sample(ids, n)
```

Previews fetched by `curl -s -A "smart-design-research"` (Microsoft Create `.webp` thumbnails,
converted to PNG with Pillow for viewing). Pixel colours sampled directly with Pillow; contrast
computed with `skill/document-design-intelligence/scripts/lib/color.py` `contrast_ratio`
(sampled wherever a call looked plausibly in the 3.5–5.5:1 zone, per clarification C9). Flyer is a
single page (no panel/spread scope questions). Scratch files lived in
`research/designs-evidence/tmp-sc2/flyer/` and are deleted at the end of this task.

**Sample (n=10, sorted):** `MSF:006, MSF:007, MSF:008, MSF:009, MSF:010, MSF:012, MSF:022,
MSFP:007, MSFP:009, MSFP:010`.

## Coding table

| id | columns | heading class | body class | colour use | header treatment | rules/boxes | density | admissible |
|---|---|---|---|---|---|---|---|---|
| MSF:006 | 1 (right-hand venue/date/organiser block is a metadata panel, never a column/sidebar per C28) | sans ("DR. MARTIN LUTHER KING JR.") | sans | mono (red is the page's dominant colour → background, excluded; white text only) | split (name on the left, venue/date/organiser meta on the right of the same header band) | none | standard (title + meta + closing paragraph, moderate area) | yes — contrast borderline disclosed: white body-text on background red sampled `#EB1818`, `contrast_ratio(#FFFFFF,#EB1818)=4.49:1`, ~0.01 below the 4.5:1 body-text line; the display name text (≥24pt) clears 3:1 easily. Estimate from a compressed thumbnail; flagged, not excluded. |
| MSF:007 | 1 | display (rounded "KWANZAA" wordmark) | sans | multi (yellow/orange title cluster, teal cluster, red/pink cluster in the top+bottom dash-pattern border; border is a continuous pattern band so A5 does not apply per C20) | ruled (multicolour dash border sits at the page's top edge directly above the header block, small gap) | rules (same border, top/bottom only, not enclosing) | airy (~7 lines) | yes |
| MSF:008 | 1 | display (rounded "MARDI GRAS" wordmark) | sans | multi (yellow title cluster; pink icon+caption cluster — calendar/clock/location icons counted as B4 "icon" elements, not excluded "illustration"; the feather mask graphic itself is excluded as an illustration) | plain-centered (title centred; mask/paragraph is the boundary, not a fill/rule) | none | airy (~10 lines, icon/mask-dominated) | yes |
| MSF:009 | 1 | sans ("HANUKKAH CELEBRATION") | sans | one-accent (single gold date-line cluster; menorah candle flames excluded as illustration) | plain-centered (title centred; the small "⁂" divider sits inside the header block, between title and the date/meta lines that are still part of the block per the family row, so it does not frame the block's edge) | rules (the divider line) | airy (~6 lines) | yes — contrast checked: white text on background blue sampled `#085898`, `contrast_ratio(#FFFFFF,#085898)=7.34:1`, passes |
| MSF:010 | 1 | sans ("THANKSGIVING") | sans | multi (gold cluster: border frame, "School of Fine Art", "STUDENT POTLUCK", address; red cluster: "NOVEMBER" date badge) | ruled (a gold hairline under the address line spans roughly the header block's width, directly above "School of Fine Art") | boxes (full-page gold border frame encloses the content) | airy (~10 lines against a full-bleed photo) | yes — judgment call disclosed: title/meta and the closing instructional line sit directly on the autumn-leaves photo with only a dark tint (no clearly separate opaque panel); read as within the C8 "flat opaque panel over photo" exception rather than A3, because the tint reads as near-uniform across the text zone. A stricter reading would call this A3. |
| MSF:012 | 1 (the "9/4–9/7 \| 10AM TO 8PM DAILY \| TIME OUT SPORTS OUTLET" row is a meta/table row, not a flowing column) | sans (giant outline "SALE" repeated 3×, the largest text on the page) | sans | one-accent (single dark-red date/price text inside the white info box; the pink-purple-blue background is a gradient, coded as the background per B1a and disclosed) | plain-centered (outline "SALE" watermark is horizontally centred) | boxes (bordered info panel) | airy (~8 lines) | yes — gradient disclosed (colour-note): background is a smooth pink→purple→blue gradient (C17: gradients count as fills, but here it is the dominant/background colour, so excluded from the hue count); small corner captions sit directly on the gradient but are short, high-weight and read at clearly passing contrast by eye, not sampled precisely — disclosed as an eyeballed pass, not a "far from threshold" call |
| MSF:022 | 1 | sans ("THANKS GIVING") | sans | fill-blocks (orange paint-swipe fill, ≥10% of page area combined across 3 strokes) | ruled (gold hairline under the address line, as MSF:010) | boxes (full-page gold border frame) | airy (~10 lines) | **no — A4** (orange paint-swipe/brush-stroke decorative graphic, explicit universal fail) |
| MSFP:007 | 1 | sans ("HATHA VINYASA ASHTANGA") | sans | one-accent (single gold "YOGA CLASSES / Monday–Friday…" cluster; flower logo excluded) | image-hero (full-bleed duotone photo covers the whole page, intersects top 20%, ≫30% area) | none | airy (~12 lines) | **no — A3** (the descriptive paragraph "Our compassionate approach…" sits directly on the pink-duotone photo with no opaque panel behind it; the title itself, being display-size text, would be exempt, but the body paragraph is not) |
| MSFP:009 | 1 | display (outline "HOLI" filled with the same colour-splash texture) | sans | one-accent (navy/dark-blue text cluster only — "YOU ARE INVITED TO A", "CELEBRATION", date, address, paragraph; the colour-powder splash, including the texture masked into the "HOLI" letters, is excluded as a photographic/illustrative texture) | image-hero (the powder-splash graphic covers the page's upper ~60% and intersects the top 20%) | none | airy (~8 lines) | **no — A4** (the colour-powder burst is a splatter decorative graphic, explicit universal fail) |
| MSFP:010 | 1 | display (rounded, whimsical "FABRIKAM KIDS" wordmark) | sans | mono (the sky/sun/sheep/fence/bee scene is a single illustration, excluded in full; remaining text is white, achromatic) | image-hero (the illustrated scene covers the entire page and intersects the top 20%; image-hero counts illustrations, unlike the colour test) | none | airy (~7 lines) | **no — A6** (white title/paragraph text sits directly on light sky-blue; sampled background `#4FCAF5` against white text, `contrast_ratio(#FFFFFF,#4FCAF5)=1.89:1`, far below both the 4.5:1 and 3:1 lines — not a borderline call) |
