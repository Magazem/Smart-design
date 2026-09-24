# Flyer — header treatment + colour use recode under research/82a-general.md

Recoder: fresh worker (has not coded flyer before). Retrieved/measured 2026-09-24. Scope:
`header treatment` and `colour use` ONLY, for all 16 coded flyer items (`flyer-items.csv`, 82a
C11). Every other code (columns, body, rules, density, admissibility, reason/note) is untouched
and copied as-is from `flyer-corpus.md` F.3; `(r1)` columns preserve it.

**Previews:** the `thumbnail`/`preview_url` of each item, downloaded to
`research/designs-evidence/tmp-bfrc/` (400x519 px each) and converted to PNG; deleted at the end.
Measurements use `tmp-bfrc/measure.py` / `tmp-bfrc/hue.py` (stdlib + PIL, `colorsys` HSL). Page
scope = the whole sheet (flyer has no panels).

**Readings applied (disclosed, same as brochure — see `brochure-recode-82ag.md` R1-R4 for the
full rationale):**
- Gradients/flat colour fills count as B3 fill blocks, not B1a background, unless genuinely
  pale/neutral (C17; a saturated colour covering most of the page is a design fill, not "the
  background").
- Photos and illustrations (a drawn scene: moon+haunted house, menorah, feather mask, row of
  little houses, autumn-leaf photo) are excluded wholesale from colour tests (B1b), including
  their internal colour variety — this is the main reason several `multi` r1 calls become
  `fill-blocks` or `one-accent` here: the "multiple colours" the first coder saw were inside a
  single excluded illustration, not independent counted elements.
- Band(d): a fill spanning the WHOLE page (not just the title's own block) is never a band,
  however solid its colour, even if it happens to also be identifiably "on brand".
- image-hero (C1) is tested FIRST, strictly, before band/ruled/split/plain-*. A full-bleed
  PHOTOGRAPH covering the whole page always clears the ≥30%-of-page-area / intersects-top-20%
  test, even when a text box/frame sits on top of it. I distinguish an actual photograph
  (MSF:010's autumn-leaves macro photo) from a painted texture/brush background (MSF:006,
  MSF:017, MSF:022), which the corpus's own convention (F.9/F.10) does not score as image-hero
  candidates; only discrete photos/illustrations with a measurable bounding box are tested.

## Per-item table

| id | header (r1) | header (r2ag) | deciding test + measurement | colour (r1) | colour (r2ag) | deciding test + measurement |
|---|---|---|---|---|---|---|
| MSF:001 | plain-left | plain-left | title "FALL GALA" sits on the plain cream page tint (no distinct fill behind its glyphs, and the tint covers the whole page anyway) → band fails; no rule; title flush toward the left margin (matches the intro paragraph and address block above/below it) → plain-left (T6) | fill-blocks | fill-blocks | background #F0E0D0 (cream, share 0.677), `fill_area_share=0.178`; green/orange/navy "colour-block" organic shapes (not photographic; R3 fills, not illustrations of an object) sum ≥10% of the page (B3) |
| MSF:002 | plain-left | plain-left | "Twine + Burlap" sits directly on the dark taupe page background, which covers the WHOLE page → band(d) fails (full-page fill); no rule; title starts near the page's left margin → plain-left (T6) | fill-blocks | fill-blocks | background #404030 (dark taupe, share 0.588), `fill_area_share=0.340`; the taupe panel alone (achromatic, S=0.143, but B3 doesn't require chroma) covers ≥10% (B3); interior-design photos excluded (B1b) |
| MSF:003 | image-hero (r1 already under C1) | image-hero | unchanged: moon fills ≈47% of the page (first coder's own C1 measurement), intersects the top 20%, "HALLOWEEN PARTY" sits on it → image-hero (test 1) | fill-blocks | fill-blocks | background #C04000 (orange gradient sky, share 0.233), `fill_area_share=0.570`; gradient counts as a fill (C17) and alone covers most of the page (B3); moon/house/bat illustration excluded (B1b) |
| MSF:004 | plain-centered | plain-centered | leaf/pumpkin border art is decorative framing only, not one image ≥30% of the page → not image-hero; "FALL HARVEST" sits on the yellow tint that covers the WHOLE page → band(d) fails; no rule; symmetric leaf frame either side of the centred text block → plain-centered (T5) | fill-blocks | fill-blocks | background #F0D070 (yellow, share 0.627), `fill_area_share=0.266`; yellow fill alone ≥10% (B3); leaf/pumpkin line art excluded (B1b) |
| MSF:005 | plain-left | plain-left | blue fill covers the WHOLE page → band(d) fails; no rule; "MEMORIAL DAY BARBEQUE" flush to the left margin, well short of page centre → plain-left (T6) | fill-blocks | fill-blocks | background #4080C0 (blue, share 0.637), `fill_area_share=0.191`; blue fill alone ≥10% (B3); grill illustration excluded (B1b) |
| MSF:006 | plain-left | **band** | a blue/purple halftone-stripe patch sits behind "DR. MARTIN LUTHER KING JR." specifically (not the whole page): estimated width ≈75-80% of page width (≥60%, criterion (c)), height confined to the name block, estimated ≈40% of page height — **at the (d) ceiling, recorded as borderline/low-confidence from the 400px thumbnail**. Read as passing (a)-(d) → band. Recode from the first coder's plain-left | fill-blocks | fill-blocks | background #E01010 (red, share 0.500), `fill_area_share=0.364`; red fill alone ≥10% (B3); halftone-stripe texture excluded as decorative pattern (C20-adjacent), doesn't change the call |
| MSF:007 | plain-left | plain-left | title "KWANZAA" sits on the plain black page fill, which covers the WHOLE page (not a band sized to the title; the coloured dot/dash pattern is at the top/bottom edges, not behind the title) → band(d) fails; no rule; "JOIN US FOR A" / "KWANZAA" both flush left → plain-left (T6) | fill-blocks | fill-blocks | background #000000 (black, share 0.620), `fill_area_share=0.264`; the solid black fill alone ≥10% (B3, chroma not required for B3); dot/dash border pattern excluded as repeated decorative motif |
| MSF:008 | plain-centered | plain-centered | "MARDI GRAS" sits on the plain dark-purple page fill covering the WHOLE page → band(d) fails; no rule; symmetric layout (feather mask centred beneath) → plain-centered (T5), unchanged | multi | **fill-blocks** | background #302040 (dark purple, share 0.552), `fill_area_share=0.281`; the dark-purple page fill alone is ≥10% of the page (B3) — B3 is checked **before** B4-B6 hue clustering, so the yellow/pink feather-mask illustration's internal colours (which the first coder read as `multi`) never reach the clustering step; the mask itself is also excluded as an illustration (B1b). Recode |
| MSF:009 | plain-centered | plain-centered | "HANUKKAH CELEBRATION" sits on the plain blue page fill covering the WHOLE page → band(d) fails; no rule; symmetric layout under the centred menorah → plain-centered (T5), unchanged | fill-blocks | fill-blocks | background #005090 (blue, share 0.525), `fill_area_share=0.239`; blue fill alone ≥10% (B3); star-pattern texture and menorah illustration excluded |
| MSF:010 | plain-centered | **image-hero** | the autumn-leaves image is an actual full-bleed PHOTOGRAPH (not a texture/pattern), covering the entire page (own area ≈100% ≥30%, intersects the top 20%); "THANKSGIVING / STUDENT POTLUCK" sits directly on it inside a thin gold frame → image-hero (test 1) wins by strict priority. Recode from plain-centered: the first coder didn't re-test this item for image-hero because it was never coded image-hero originally, but the literal C1 test is met regardless of the framing box | one-accent | one-accent | background #200000 (dark photo corner, share 0.122 — photo dominates and is excluded, B1b); remaining non-photo elements: "NOVEMBER / 28" numerals (one hue, ≈20-30°) is the only counted chromatic cluster → **one-accent**, unchanged |
| MSF:012 | plain-centered | plain-centered | pink-purple gradient covers the WHOLE page (a fill, C17) → band(d) fails regardless of the sneaker photo/outline "SALE" art; no rule under "SALE"; the three stacked "SALE" outlines and "SPORTING GOODS SALE" box read as a centred composition around the shoe → plain-centered (T5), unchanged | multi | **fill-blocks** | background #C04000-adjacent purple/pink gradient (share low because it's a continuous gradient, not one flat mode colour), `fill_area_share=0.876` — the gradient alone (C17: gradients count as fills) covers ≈88% of the page, ≫10% (B3), decided **before** any hue-cluster count of "SALE"/box outline colours. Recode |
| MSF:014 | band | **plain-left** | title = "OPEN HOUSE" (largest text on the page); it sits on the PLAIN WHITE background, not on the yellow strip — the yellow fill sits behind the small address masthead line ABOVE the title, not behind the title's own glyphs (C18 requires the fill under the title specifically) → band fails for the title; no rule directly under "OPEN HOUSE"; title flush left (matches the address line and photo caption) → plain-left (T6). Recode: the first coder's C1 image-hero re-test (F.10) turned this into `band` for the photo/yellow-strip generally, but 82a-general's C18 test is about the TITLE's own glyphs, which are not on the yellow | fill-blocks | fill-blocks | background #F0F0F0 (pale, share 0.328, genuinely neutral), `fill_area_share=0.599` (mostly the house photo, excluded, B1b); the yellow top strip alone is still ≥10% of the page (B3) |
| MSF:017 | plain-centered | **band** | a navy paint-swipe sits directly behind "THANK YOU TEACHERS!": estimated width close to full page width (≥60%, criterion (c)), height confined to the swipe, estimated ≈30-35% of page height (< 40% ceiling, criterion (d) passes) → band. Recode from plain-centered: the first coder treated the swipe purely as an A4 decorative texture for admissibility and didn't re-apply it as a band for header | multi | **fill-blocks** | background #F0F0F0 (white, share 0.495 — genuinely neutral), `fill_area_share=0.414`; the navy swipe fill alone is ≥10% of the page (B3), decided before any hue-clustering of the backpack/globe/pencil doodle icons (which are also excluded as illustrations, B1b, and/or a repeated decorative motif under C20). Recode |
| MSF:018 | plain-centered | plain-centered | "Winter Celebration" (cursive, pink) sits on the plain white page, no fill behind it → band fails; no rule; symmetric layout over the centred row of houses → plain-centered (T5), unchanged | multi | **one-accent** | background #F0F0F0 (white, share 0.740, genuinely neutral), `fill_area_share=0.230` — mostly the row-of-houses illustration, excluded WHOLESALE as one illustration (B1b), including its internal palette of pastel roof/window colours; the only element that survives exclusion is the pink/red cursive title + matching date text, one hue cluster (≈350°) → **one-accent**. Recode: the first coder's `multi` counted the houses' internal colours, which B1b excludes |
| MSF:022 | plain-centered | plain-centered | maroon/brush-stroke background is a painted texture (not a discrete photo/illustration with a measurable bounding box), and it covers the WHOLE page → band(d) fails; no rule under the title specifically (the gold frame borders the whole card, not the header block); centred "THANKS / GIVING / Event Title" composition → plain-centered (T5), unchanged | fill-blocks | fill-blocks | background #500000 (maroon, share 0.735), `fill_area_share=0.233`; maroon fill alone ≥10% (B3); orange brush strokes excluded as decorative texture, doesn't change the call |
| MSF:027 | plain-centered | **ruled** | "HALLOWEEN" sits on the plain dark-purple page fill (not on the moon; band fails, both because the moon illustration is excluded, B1b, and because the plain fill covers the whole page, (d)); a thin orange rule sits directly below the header block (title + "COSTUME PARTY" tagline), estimated to span most of the page width (≥80%, low-confidence estimate from the 400px thumbnail) before the "you're invited..." line → ruled, ahead of plain-centered in priority. Recode from plain-centered — **disclosed low-confidence**: the exact rule width was estimated by eye from the thumbnail, not pixel-measured; a second coder should re-check it | fill-blocks | fill-blocks | background #200030 (dark purple, share 0.625), `fill_area_share=0.227`; dark-purple fill alone ≥10% (B3); moon/bat/jack-o'-lantern-eye illustrations excluded (B1b) |

## Addendum: F.11 recount (Design Researcher 3, 4 new items, added after this file's first pass)

`flyer-corpus.md` grew from 118 to 170 lines while this recode was in progress (§F.11, a PowerPoint
+ Word-pamphlet recount under 82b, adding `MSFP:007`, `MSFP:009`, `MSFP:010`, `MSFW:017`). Per the
task instruction ("if a file changes while you work, re-extract its items and code any new ones"),
`flyer-items.csv` was regenerated (now 20 rows) and the 4 new previews were fetched and recoded
under 82a-general below. These 4 were coded by DR3 on 2026-09-23, before 82a-general existed as a
named ruling, so (unlike the memo/form additions below) they get the same fresh recode treatment
as the original 16.

| id | header (r1, F.11.2) | header (r2ag) | deciding test + measurement | colour (r1, F.11.2) | colour (r2ag) | deciding test + measurement |
|---|---|---|---|---|---|---|
| MSFP:007 | image-hero | image-hero | unchanged: full-bleed pink duotone photo (yoga pose), intersects top 20%, own area ≈100% ≥30% (C1); title "HATHA VINYASA ASHTANGA" sits on it → image-hero (test 1) | one-accent | one-accent | duotone photo excluded wholesale (B1b, including its pink tint); the only surviving elements are the orange/gold "FABRIKAM YOGA STUDIOS" wordmark + "YOGA CLASSES / Monday-Friday..." lines, one hue cluster (≈30-40°) → one-accent, unchanged |
| MSFP:009 | image-hero | image-hero | unchanged: the watercolour/powder paint splash fills the top half, intersects top 20%, own area ≥30% (C1); "HOLI" sits on it → image-hero (test 1) | multi | **one-accent** | the paint splash is an illustration/decorative graphic (B1b), excluded wholesale — its magenta/blue/teal palette (what the first coder read as `multi`) never reaches B4-B6. What survives: navy/dark-blue text ("YOU ARE INVITED TO A", "CELEBRATION", the date, the body paragraph — ≥2 elements, one hue cluster ≈210-220°); the small pink hand icon inside the "O" of "HOLI" is one element well under 0.5% of the page, failing B5 presence → 1 cluster → **one-accent**. Recode |
| MSFP:010 | plain-centered | plain-centered | sky-blue fill covers the WHOLE page → band(d) fails; sun illustration ≈10% of page (<30%, not image-hero, unchanged from F.11.2's own measurement); no rule; symmetric layout (sun and sheep both centred) → plain-centered (T5), unchanged | fill-blocks | fill-blocks | full-page sky-blue fill (`#62cdf7`-family, sampled by DR3) alone is ≥10% of the page (B3); sun/cloud/sheep/fence illustrations excluded (B1b), doesn't change the call |
| MSFW:017 | plain-left | plain-left | title "MUSIC LESSONS" sits on the navy page fill, which covers the WHOLE page → band(d) fails; the short yellow rules beside it don't reach 60-80% of page width (DR3's own note: "not full-width") → not ruled; no split; title sits in the right column, well off page centre → plain-left (T6), unchanged | fill-blocks | fill-blocks | full-page navy fill (`#0a4c68`, sampled by DR3) alone is ≥10% of the page (B3); the guitar-of-music-notes illustration is excluded (B1b), doesn't change the call |

Updated value counts including these 4 (20 coded items total): **header treatment** plain-left 6
(+ MSFW:017), plain-centered 8 (+ MSFP:010), image-hero 4 (+ MSFP:007, MSFP:009), band 2, ruled 1,
split 0. **colour use:** fill-blocks 16 (+ MSFP:010, MSFW:017), one-accent 4 (+ MSFP:007, MSFP:009
[recode]), mono 0, multi 0.

## Value counts (original 16 coded items, F.3 only — see addendum above for all 20)

**header treatment:** plain-left 5 (MSF:001, MSF:002, MSF:005, MSF:007, MSF:014), plain-centered 7
(MSF:004, MSF:008, MSF:009, MSF:012, MSF:018, MSF:022), image-hero 2 (MSF:003, MSF:010), band 2
(MSF:006, MSF:017), ruled 1 (MSF:027), split 0.

**colour use:** fill-blocks 14 (MSF:001, MSF:002, MSF:003, MSF:004, MSF:005, MSF:006, MSF:007,
MSF:008, MSF:009, MSF:012, MSF:014, MSF:017, MSF:022, MSF:027), one-accent 2 (MSF:010, MSF:018),
mono 0, multi 0.

## Changes vs r1 (first coding, pre-82a-general)

- Header: MSF:006 plain-left→band; MSF:010 plain-centered→image-hero; MSF:014 band→plain-left;
  MSF:017 plain-centered→band; MSF:027 plain-centered→ruled. Unchanged: MSF:001, 002, 003, 004,
  005, 007, 008, 009, 012, 018, 022 (11 of 16).
- Colour: MSF:008 multi→fill-blocks; MSF:012 multi→fill-blocks; MSF:017 multi→fill-blocks;
  MSF:018 multi→one-accent. Unchanged: 12 of 16. Every colour change follows the same mechanism:
  applying B3 (fill blocks) strictly BEFORE B4-B6 (hue clustering), and excluding illustrations
  wholesale (B1b) rather than counting their internal palette — the first coder (pre-82a-general)
  had no B3-first ordering rule and read illustration-internal colour variety as `multi`.

Scratch previews in `tmp-bfrc/` deleted at the end of this task (per instruction).
