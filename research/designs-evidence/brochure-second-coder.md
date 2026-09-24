# research/designs-evidence/brochure-second-coder.md — independent second coder (falsifier), 2026-09-24

**Independence.** Coded from `research/82-design-ranking-protocol.md` §4 (rubric) and §5
(admissibility), `research/82a-general.md` (header treatment + colour use, supersedes §4 for
brochure per its scope list), `research/82a-clarifications-1.md` through `-5.md`, and
`research/designs-evidence/brochure-items.csv` only. No other file under
`research/designs-evidence/` was opened; `research/91-family-status.md` and
`research/82b-shortfall-sources.md` were not opened. First-coder codes were never seen.

**Method.** Ids sorted lexicographically from `brochure-items.csv` (11 ids: `LOB:003, LOB:004,
MSB:001, MSB:002, MSB:003, MSB:005, MSB:007, MSB:008, MSB:009, MSB:010`). Sample:

```python
import math, random
ids = sorted([...])  # the 11 ids above
n = max(min(10, len(ids)), math.ceil(0.25 * len(ids)))  # = 10
sample = random.Random("82a:brochure").sample(ids, n)
```

Previews fetched by `curl -s -A "smart-design-research"` (LibreOffice screenshot PNGs; Microsoft
Create `.webp` thumbnails, converted to PNG with Pillow for viewing — no non-stdlib dependency in
the scoring itself, only in image I/O). Pixel colours sampled directly from the downloaded raster
with Pillow; contrast computed with `skill/document-design-intelligence/scripts/lib/color.py`
`contrast_ratio`. Brochure "page" = the outside spread (§4); front panel = rightmost panel per
82a-general §A.1's brochure row (MS Create trifold thumbnails are 400×309/800×554, matching an
11″×8.5″ landscape 3-panel spread's aspect ratio, confirming all three panels are present in one
thumbnail even where seams are not visually obvious). Colour use is scored over the **whole**
outside spread per 82a-general §B header note. Scratch files (downloaded previews, crops, pixel
probes) lived in `research/designs-evidence/tmp-sc2/brochure/` and are deleted at the end of this
task.

**Sample (n=10, sorted):** `LOB:003, LOB:004, MSB:001, MSB:002, MSB:003, MSB:005, MSB:007,
MSB:008, MSB:009, MSB:010` (only `MSB:007`... full 11-id set minus `MSB:004` was excluded by the
seeded draw).

## Coding table

| id | panel count | heading class | body class | colour use | header treatment | rules/boxes | density | admissible |
|---|---|---|---|---|---|---|---|---|
| LOB:003 | 3 | sans | sans | multi (red/blue/teal hyperlink-style placeholder words, 3 clusters) | plain-centered ("Cover" centred in front panel; no fill/rule) | none (dashed lines are fold guides, excluded) | standard (~36 lines across spread) | yes |
| LOB:004 | 2 (two pages shown, no further fold panels; "for sale" ad page + map page — not a 3-panel trifold, treated as the closest listed value) | sans ("for sale" is the largest text, blocky sans; front-panel title "Unit X/Y" also sans) | sans | multi (orange title/feature words + blue-grey-navy chevrons, 2 clusters; chevrons individually <10% area so not fill-blocks) | ruled (top border box around the title line spans ~100% of front-panel width, counts as a rule per 82a-general §A.2.3) | boxes (bordered title box; whole-page thin border) | airy (~16 lines) | yes |
| MSB:001 | 3 | sans ("Brochure Title") | sans | fill-blocks (teal band under title + teal address-panel fill, combined ≈ borderline ≥10% of spread — disclosed as borderline) | image-hero (house photo covers >30% of front panel and intersects its top 20%) | rules (underline rule below "Brochure Title") | airy (~19 lines) | yes |
| MSB:002 | 3 | sans ("EVENT SERIES NAME") | sans | fill-blocks ("vivid shapes" cyan/pink/orange blobs, sizeable corner fills across the spread) | plain-left (title left-aligned; blobs intersect the top-20% strip but read as corner accents, estimated <30% of panel area — disclosed as borderline vs. image-hero) | none | airy (~15 lines) | yes |
| MSB:003 | 3 | display (stylised "RESTAURANT" wordmark with star/fork-knife glyphs) | sans | one-accent (single red circular "quote" badge on the middle panel; gold dots/utensil icons on the front panel excluded as part of the logo placeholder) | image-hero (food-photography intersects and covers >30% of the front panel) | boxes (dashed-border logo-placeholder box) | airy (~16 lines) | yes |
| MSB:005 | 3 | sans (no real title on the front panel besides the "Contoso Logo" placeholder box; coded from that wordmark per the fallback rule) | sans | fill-blocks (solid orange rectangle/chevron fill under the skyline photo, ≈>10% of spread) | image-hero (skyline photo covers most of the front panel and intersects its top 20%) | none | airy (~15 lines) | yes |
| MSB:007 | 3 | sans ("MARGIE'S TRAVEL") | sans | fill-blocks (solid purple middle-panel fill, large) | ruled (four thick horizontal purple bars sit at the front panel's top edge directly above the header block, gap ≤ pattern per 82a-general §A.2.3(b)) | rules (same purple bars, no full border box) | airy (~19 lines) | yes |
| MSB:008 | 3 | sans ("BROCHURE NAME") | sans | mono (yellow is the spread's dominant colour → background, excluded by B1a; balloon photo excluded as a photo; only black text remains) | plain-left (title left-aligned on the front panel; photo occupies the panel's bottom, not intersecting the top 20%) | none | airy (~9 lines) | yes |
| MSB:009 | 3 | sans ("Women's Inter-Collegiate Swimming Championship") | sans | fill-blocks (large navy/blue wave shapes over the white base, ≈≥10% of spread) | image-hero (red-duotone swimmer photo covers >30% of the front panel and intersects its top 20%) | rules (short red dashed accent lines beside the photo) | airy (~21 lines) | yes |
| MSB:010 | 3 | plain-left title, sans ("Technology For all") | sans | mono (navy/teal is the dominant spread colour → background, excluded; white text/sunburst achromatic) | plain-left (circular hand photo ≈19-24% of the front panel, estimated below the 30% image-hero threshold — disclosed as borderline; no band since the teal fill is full-panel-height background, no rule) | none | airy (~10 lines) | yes |

Notes on borderline calls (disclosed per protocol): MSB:001 colour (fill-blocks vs one-accent,
teal-fill area near the 10% line), MSB:002 header (plain-left vs image-hero, blob coverage near
30%), MSB:010 header (plain-left vs image-hero, photo coverage near 30%) are all within roughly
10% of their threshold and are recorded here as such; a coder reading the same thumbnails could
plausibly cross these particular lines.
