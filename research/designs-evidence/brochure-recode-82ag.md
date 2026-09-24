# Brochure — header treatment + colour use recode under research/82a-general.md

Recoder: fresh worker (has not coded brochure before). Retrieved/measured 2026-09-24. Scope:
`header treatment` and `colour use` ONLY, for all 11 coded brochure items (`brochure-items.csv`,
82a C11). Every other code (panels, body, rules, density, admissibility, reason/note) is
untouched and is copied as-is from `brochure-corpus.md` B.3; the `(r1)` columns below preserve it.

**Previews:** the `preview_url` of each item (brochure-items.csv), downloaded to
`research/designs-evidence/tmp-bfrc/` and converted to PNG for viewing; deleted at the end (82a
task instruction). Pixel measurements use `tmp-bfrc/measure.py` and `tmp-bfrc/hue.py` (stdlib +
PIL, `colorsys` HSL, same S/L definitions as `skill/.../lib/color.py`'s WCAG-adjacent module).
Page scope = the whole outside spread (400x309 px for the 9 MS thumbnails; LOB:003/004 differ).

**Readings applied (disclosed):**
- R1. Front panel = the rightmost panel of the outside spread (confirmed by LOB:003's own
  fold-guide labels: "Front / Cover" is printed on the rightmost panel, "Back" on the narrow
  panel just before it). "Page width" in 82a-general's table = panel width, per §4 as the task
  restates.
- R2. Gradients and flat colour fills count as B3 fill blocks (C17), never as B1a "background",
  unless they are a genuinely neutral/pale base tone (L>0.90, or a near-white/cream margin). A
  saturated colour that happens to cover most of a panel (e.g. a brand-colour panel) is a fill
  block, not "the background" excluded by B1a — B1a's grid-mode background is for the page's
  neutral base surface, not a deliberate majority-colour design choice; §B3's own worked example
  (invoice MS:006, "black wedges" counted toward fill-blocks) already treats large solid areas
  this way.
- R3. Photos and illustrations (drawings of a recognisable object: a moon+haunted-house scene,
  a swimmer photo, a hiker photo, leaf/pumpkin line art) are excluded wholesale from every colour
  test (B1b), including their internal colour variety. Abstract organic "colour-block" shapes
  (MSB:002, MSB:009's swim-team wave graphic) are treated as fills, not illustrations of an
  object, consistent with these MS asset file names ("...color-block...").
- R4. Band(d): a fill spanning the panel's full height (i.e. ≥40% of page/panel height) is never
  a band, however solid or on-brand its colour (82a-general A.2.2(d)).

## Per-item table

| id | header (r1) | header (r2ag) | deciding test + measurement | colour (r1) | colour (r2ag) | deciding test + measurement |
|---|---|---|---|---|---|---|
| MSB:001 | plain-left | plain-left | front = right navy panel ("Brochure Title/Subtitle"); navy fill spans the full panel height (309/309 px = 100% > 40%) → band(d) fails; no rule under the title; title flush to the panel's left margin, not centred → plain-left (T6) | fill-blocks | fill-blocks | `measure.py`: background #70A0A0 (teal panel, share 0.273), `fill_area_share(<=0.90 excl bg)=0.572` — teal + navy panels alone are ≥40% combined, ≫10% of page area (B3) |
| MSB:002 | plain-left | plain-left | front = right navy/blob panel ("EVENT SUBTITLE / EVENT SERIES NAME"); navy fill is full-panel-height (>40%) → band(d) fails; no rule; title starts near the panel's left edge, not centred → plain-left (T6) | fill-blocks | fill-blocks | background #001030 (navy, share 0.440), `fill_area_share=0.364`; navy alone covers ≈44% ≥10% (B3); colour-block blobs (R3) don't change the call |
| MSB:003 | plain-left | plain-left | front = right photo-collage panel; title = "RESTAURANT" wordmark (largest non-photo, non-logo text on the panel), right-aligned within the panel, not on a distinct fill rectangle behind its glyphs → band fails; not centred → plain-left (T6), `align=right` (A.2.6) | fill-blocks | fill-blocks | background #202020 (black panel, share 0.425), `fill_area_share=0.345`; black panel + red quote-circle fill alone exceed 10% (B3); food photos excluded (B1b/R3) |
| MSB:004 | plain-left | plain-left | front = right page, "YOUR PREMIER CATERING SOLUTION" on the cream page tint; the cream covers the WHOLE page (full-page tint) → band(d) fails explicitly ("a full-page tint... is not a band"); no rule; title flush left → plain-left (T6) | fill-blocks | fill-blocks | background #F0F0D0 (cream, share 0.282), `fill_area_share=0.448`; yellow accent panel + orange/green pumpkin-catering icon fills ≥10% (B3) |
| MSB:005 | plain-left | plain-left | **front-panel reading disclosed low-confidence:** right panel (orange, address+logo block) carries no headline-weight text at all, only equal-size contact lines beside a logo placeholder (excluded, A.1 "logos never the title"); the only true headline in the spread is "JOIN OUR TEAM" on the LEFT panel, so I read that as the title (self-mailer-style spread, address panel facing out). It sits on plain white, no fill behind it → band fails; no rule; flush left → plain-left (T6) | fill-blocks | fill-blocks | `fill_area_share=0.641` (grey photo panel + orange diagonal fill + orange contact panel, all ≫10%, B3) |
| MSB:007 | plain-left | **image-hero** | front = right panel: a full-bleed photo (hiker seated on a mountain edge) fills the ENTIRE panel top-to-bottom — panel width 133/400 px ≈ 33.3% of the page, full page height, so own area ≈33% ≥30% (82a C1), and it intersects the top 20% of the page (full-height photo). "MARGIE'S TRAVEL" (the title) sits directly on that photo → **image-hero** wins by strict priority (test 1), ahead of band/ruled/plain. This is a genuine recode: the first coder had this as `plain-left` | fill-blocks | fill-blocks | background not dominant (photo-heavy); `fill_area_share=0.553` — purple accent panel (balloon icon, contact block) alone is a fill ≥10% (B3); the hiker/collage photos are excluded (B1b) |
| MSB:008 | band | **plain-left** | front/middle = yellow panel, "BROCHURE NAME / SUBTITLE"; the yellow fill runs from the top of the panel down to where the balloon photo begins — estimated ≈60% of page/panel height, **> the 40% band(d) ceiling**, so it is not a band (a full/near-full-panel tint, not a band sized to the title). No rule under the title. Title flush to the panel's left margin → plain-left (T6). Recode: the first coder read this fill as a band; measured against 82a-general's explicit (d) it is too tall | fill-blocks | fill-blocks | background #E0C020 (yellow, share 0.285, hue 50°), `fill_area_share=0.456` — yellow panel alone ≥10% (B3); balloon-photo and puzzle/lightbulb photos excluded (B1b) |
| MSB:009 | plain-left | plain-left | front = right panel, "Women's Inter-Collegiate Swimming Championship" on white with red/blue wave graphics; the swimmer photo was already measured by the first coder at ≈26% of the spread (< 30%, sub-threshold for image-hero, unchanged under 82a since the literal test is the same C1 test); no fill behind the title glyphs → band fails; no rule; title flush left → plain-left (T6) | fill-blocks | fill-blocks | background #F0F0F0 (pale page, share 0.552, excluded as neutral base, B1e-adjacent), `fill_area_share=0.387` — red/blue wave-graphic fills (R3, not photo) ≥10% (B3) |
| MSB:010 | plain-left | plain-left | front = right panel, "Technology For all" on navy with a white starburst accent; the starburst sits partly behind "Technology" but is a narrow decorative shape, not a rectangle ≥60% of panel width behind the full title → band fails (criterion (c)); no rule; title flush left → plain-left (T6) | fill-blocks | fill-blocks | background #003050 (navy, share 0.557, hue 204°), `fill_area_share=0.399` — navy fill alone ≥10% (B3) |
| LOB:003 | plain-centered | plain-centered | this item IS the fold-guide template: the rightmost panel is labelled "Front / Cover" by the template itself, with "Cover" set in large type centred in that panel, "Put a bird on it kale chips ethnic pickled" centred beneath it; no fill, no rule → plain-centered (T5) | mono | mono | background #F0F0F0 (share 0.897 — genuinely the page's neutral base, most of the spread is blank/placeholder), `fill_area_share=0.097` (< 10%, B3 fails) → B4-B6: only near-black/grey placeholder text and red/blue link-coloured placeholder words remain, individually < 0.5% of page area each and not forming a ≥2-element cluster → **mono** |
| LOB:004 | plain-centered | **plain-left** | front = page 1 (left page of the 2-page spread; this item is `single-sheet`, not folded, so front = page 1 per 82a-general's table). Title = "Unit X / Y Some Street"; on plain white, no fill behind it → band fails; the underline beneath it is sized to the text only, well under 80% of page width → not ruled; the heading sits flush to the page's left margin (the vertical "for sale" strip occupies the left edge, and the heading itself starts at the left edge of the content column, well left of page centre) → plain-left (T6), not plain-centered. Recode: re-read on this pass as left-aligned, not centred | multi | multi | background #F0F0F0 (share 0.535 — the two interior/exterior photos and the map graphic are excluded, B1b/R3), `fill_area_share=0.448` mostly photo/map (excluded); blue+navy chevrons single-linkage-cluster within 30° (one cluster, ≈210-220°); orange/red "for sale" + heading text is a separate cluster (≈10-20°) → 2 clusters meeting B5 → **multi** (unchanged) |

## Value counts (11 coded items)

**header treatment:** plain-left 8 (MSB:001, MSB:002, MSB:003, MSB:004, MSB:005, MSB:009, MSB:010, LOB:004), image-hero 1 (MSB:007), plain-centered 1 (LOB:003), band 0, ruled 0, split 0.

**colour use:** fill-blocks 9 (MSB:001, MSB:002, MSB:003, MSB:004, MSB:005, MSB:007, MSB:008, MSB:009, MSB:010), mono 1 (LOB:003), multi 1 (LOB:004), one-accent 0.

## Changes vs r1 (first coding, pre-82a-general)

- MSB:007: `plain-left` → `image-hero` (full-bleed photo panel, own area ≈33% ≥30%, C1 literal test).
- MSB:008: `band` → `plain-left` (fill height ≈60% of panel/page, over the 40% band(d) ceiling).
- LOB:004: `plain-centered` → `plain-left` (re-read: title flush left, not centred, once the
  page-1/page-2 spread and the left "for sale" strip are taken into account).
- Colour: unchanged for all 11 items; the fill-blocks/mono/multi calls made by the first coder
  already match a strict B3-then-B4-B6 read once photos/illustrations are excluded (R3) and
  gradients/majority fills are treated as B3 blocks rather than B1a background (R2).

Scratch previews in `tmp-bfrc/` deleted at the end of this task (per instruction).
