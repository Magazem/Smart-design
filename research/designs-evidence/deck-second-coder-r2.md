# research/designs-evidence/deck-second-coder-r2.md — deck, round 2 independent second coder

**Independence.** This file was produced reading ONLY: `research/82a-deck.md` (binding rules),
`research/82-design-ranking-protocol.md` §4 (deck rows) and §5, `research/82a-clarifications-1.md`
through `-5.md`, and `research/designs-evidence/deck-items.csv`. No other file under
`research/designs-evidence/` was opened (no `deck-corpus-*.md`, `deck-recode.md`,
`deck-agreement.md`, `deck-second-coder.md`), and `research/91-family-status.md` was not opened.
Helper scripts (`sample.py`, `gridcolor.py`) were written before any coding and are the only code
used to touch other files; they never printed the contents of an off-limits file.

## Method

1. **Sample.** Ids read from `deck-items.csv`, sorted lexicographically, then
   `random.Random("82a:deck").sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))`.
   `len(ids) = 105` → sample size 27 (`math.ceil(0.25*105) = 27 ≥ min(10,105)`).
2. **Evidence.** For each sampled id, only the preview(s) listed in `deck-items.csv` for that id
   were fetched (`curl -A "smart-design-research"`, downloaded to
   `research/designs-evidence/tmp-deck3/imgs/`, viewed with Read; never rendered/compiled).
   No item's own source files (npm package CSS, `.otp` styles.xml, `.pptx` theme) were fetched —
   all `heading` codes are **glyph-judged** per 82a-deck §1 step 2 (no declared-font check was
   attempted within the time budget; this is disclosed, not a step-1 failure).
3. **Measurement.** Pixel evidence (background-region detection, hue counts, fill/thick tests,
   title-block bounding boxes, WCAG contrast) was produced with two scripts written for this task
   in `tmp-deck3/`: `gridcolor.py` (20×20 grid colour-class sampler implementing 82a-deck §2's
   grouping rule: achromatic classes merge at ΔL≤0.03, chromatic classes merge at hue±15°/ΔL≤0.05)
   and ad hoc PIL pixel scans (bounding boxes of bright/dark text pixels) piped into
   `skill/document-design-intelligence/scripts/lib/color.py`'s `contrast_ratio` for every
   admissibility call that turned on contrast (C9). `gridcolor.py`'s output is mechanical; where a
   background is a **gradient or a photo whose hue drifts across many small classes** (e.g.
   MS:007's rainbow gradient, LO:031's landscape illustration, NPM:002's dark texture), the many
   small hue buckets were manually re-grouped into the one background/illustration region per
   82a-deck §2's explicit instruction ("a gradient background is still the background — it is one
   region") rather than left fragmented by the mechanical clustering.
4. **E4 master sheets.** LO:014 (12-slide grid), LO:016 (3 slides stacked), LO:041 (2×3 layout
   grid) show several miniature slides in one preview; the top-left (or topmost, for a single
   vertical stack) miniature was cropped and measured as if it were the whole slide, per 82a-deck
   E4.
5. **Exposure check.** 82a-deck.md names 17 worked-example items with their correct codes:
   MS:001–003, 010, 013, 023, 024, 025; LO:009, 021, 025, 028, 029; NPM:006, 009, 017, 018, 046,
   049, 139. Of the 27 sampled ids, **6 are worked examples**: LO:021, LO:029, MS:010, MS:013,
   NPM:006, NPM:018. These are coded below exactly as measured (not copied from 82a-deck's table)
   and are flagged in the `exposed` column for the orchestrator's sensitivity run excluding them.

## Sample (n=27, seed `"82a:deck"`)

LO:011, LO:014, LO:015, LO:016, LO:021, LO:029, LO:031, LO:035, LO:041, MS:007, MS:010, MS:013,
MS:014, MS:018, MS:019, MS:020, NPM:002, NPM:006, NPM:018, NPM:025, NPM:026, NPM:031, NPM:032,
NPM:035, NPM:041, NPM:044, NPM:073.

## Coding table

`heading` = heading class (§1). `colour` = colour use (§2). `title layout` = title-slide layout
(§3). `admissible` = y/n + rule id if excluded (§4/§5). `exposed` = worked-example id in
82a-deck.md.

| id | heading | colour | title layout | admissible | rule | deciding measurements |
|---|---|---|---|---|---|---|
| LO:011 | sans (glyph: plain grotesque caps, no serifs) | mono (gradient teal is background, excluded; no other hue ≥0.2% area) | centered (ring/text block ~centred on slide) | yes | — | text `#F2F8F9` vs darker gradient patch `#196D94` = 5.35:1 (≥3:1 large text) |
| LO:014 (E4 top-left of 12) | display (handwriting/script "Émeraude et mimosa", loose joined strokes) | fill-blocks | left | yes | — | background=white 58.0% (gridcolor); green blocks hue166 ≈12.5% + gold blocks hue42 ≈27.3% combined ≈39.8% ≥10%, both thick; heading bbox center 12.1% off tile-centre |
| LO:015 | sans (clean geometric caps, no serifs) | mono (lavender bg is background, excluded; white circle L=1.0 excluded per L>0.90; no chromatic marks) | left (bbox centre 23.4% off slide-centre) | **no** | **A6** | body copy `#FAF2FF` vs bg `#A097CE` = 2.46:1; heading `#FFFFFF` vs `#A097CE` = 2.69:1 (both <4.5:1, body text explicitly fails A6) |
| LO:016 (E4 top of 3 stacked) | sans (clean sans, no serifs, on "Cliquez pour éditer…") | multi (green hue162 ≈3.0%, yellow-green hue83 ≈2.0%, both ≥0.2%, ≥30° apart, combined <10% so hue-count applies) | left (bbox centre 10.4% off tile-centre) | yes | — | background = white/near-white 81.5%+5.0%+2.5% (gridcolor); no busy fill under heading |
| LO:021 | display (handwriting "Title") | mono (pink flat bg excluded as background 79.0%; cream panel L=0.95 >0.90 excluded; text black/achromatic) | centered (panel visually centred) | yes | — | matches 82a-deck worked table (display; admissible) |
| LO:029 | sans (clean sans "Click to add Title", no serifs) | fill-blocks (red diagonal band ≈25% of slide, thick; purple is background) | left (title block sits right of the photo diamond, own text left-aligned) | yes | — | text `#FFFFFF` vs bg `#552D8D` = 9.78:1; photo (headshot) ≈18.7% of area, <30% so not split |
| LO:031 | serif (bracketed/slab terminals on "Lorem Ipsum") | one-accent (background=cream strip 27.2% after dropping illustration hues; olive/khaki strip hue60 ≈5.2%, single chromatic hue, <10% so not fill-blocks) | left (title-block bbox centre 9.9% off slide-centre; illustration ≈67.5% of area, <80% so not full-bleed, and its horizontal extent overlaps the title block so not split) | yes | — | gridcolor: illustration hue clusters (hue 196–228, 328–344) sum ≈67.5%; text on opaque cream ribbon over illustration (C8) |
| LO:035 | sans (bold blocky "Title", no serifs; heavy weight alone is not display) | fill-blocks (tetris-style colour blocks: yellow/red/green/blue pieces, combined ≫10% of slide, each cell ≥8% of slide height so thick; black grid is background) | centered (panel bbox centre ≈2.3% off slide-centre) | yes | — | text `#FFFFFF` vs panel `#333333` = 12.63:1 |
| LO:041 (E4 top-left of 2×3) | sans (clean sans "Cliquez pour éditer…", no serifs) | fill-blocks (achromatic grey/gradient sidebar ≈16–19% of tile area, L 0.28–0.92 (mostly ≤0.90), thick — C17 gradients count as fills) | left (heading bbox centre 7.1% off tile-centre vs 5% threshold, within 10% so recorded) | yes | — | gridcolor: white 74.2% background; grey sidebar classes sum ≈19%; orange "LOGO" tag hue32 1.5% (too small to change the call) |
| MS:007 | sans (bold rounded "bouncy" display-like caps; does not match script/handwriting/blackletter/outline/inline/stencil so defaults to sans per the literal step-2 order — **borderline, disclosed**) | mono (pastel rainbow gradient re-grouped as one background region per §2's gradient rule; white browser-mockup box L=1.0 excluded; 3 window-control dots differ in colour, each <0.2%) | centered (white box bbox centre 0.1% off slide-centre) | yes | — | text black on white box (opaque panel, not on gradient directly); dots not identical so no A5 |
| MS:010 | serif (serif feet on "Master public speaking") | mono | split (flower photo ≈35–40% of right side, thick side-by-side with the ornate frame; extents do not overlap) | yes | — | matches 82a-deck worked table (mono); white serif text on near-black backdrop, high contrast |
| MS:013 | serif (light serif, "presentation title") | fill-blocks | centered (text bbox ≈ slide-centre) | yes | — | matches 82a-deck worked table (fill-blocks: khaki `#C7BFA9` 31.2% + terracotta `#C18E80` 16.8% = 48.0%); text `#372B1F` vs bg `#E6DACD` = 10.0:1 |
| MS:014 | sans (bold caps "PRESENTATION TITLE", no serifs) | mono (olive-brown background 63.5%; sepia colonnade photo excluded; no non-photo chromatic marks ≥0.2%) | left (bbox centre ≈20% off slide-centre; photo occupies top ≈31% of area but is stacked above the title, not side-by-side, so not split) | yes | — | text `#FFFFFA` vs bg `#48403 3`≈`#483F33` = 10.3:1 |
| MS:018 | display (brush-script "Basic Presentation") | mono (beach photo excluded, full-bleed; white text-panel L≈0.98 excluded; dot pattern achromatic) | full-bleed-image (photo covers slide, title block sits on it) | yes | — | text on opaque white panel over photo (C8); no busy-fill contact |
| MS:019 | serif (serif feet on "Pitch deck") | one-accent (dark green background 52%+9%; gold/olive damask pattern hue85 ≈7.2%, single hue, <10% so not fill-blocks; presenter photo excluded) | split (presenter photo ≈43.8% of right side, thick, side-by-side with the text block) | yes | — | text `#FFFFFF` vs bg `#343E2D` = 11.2:1 |
| MS:020 | sans (bold caps "PRESENTATION TITLE", no serifs) | mono (tan background 64.2%; cream footer band L=0.93 >0.90 excluded; horse photo excluded, no other chromatic marks) | centered (bbox centre ≈ slide-centre; photo sits below the title, vertically stacked, so not split) | yes | — | text `#211607` vs bg `#C0B5A7` = 8.80:1 |
| NPM:002 | sans (clean geometric "Slidev - The Unnamed") | fill-blocks (mint highlight box hue166 ≈10.6% of slide, L=0.63≤0.90, thick — dark textured photo is background/photo, excluded) | full-bleed-image (dark 3-D textured photo ≥80% of slide; title sits on the mint panel which sits on the photo) | yes | — | subtitle `#BEC1C5` vs photo patch `#1E2833` = 8.26:1 (≤2-line author line on photo, C14, passes A6) |
| NPM:006 | sans (bold condensed caps "LIGHT ICONS"; heavy weight alone is not display) | one-accent (teal "Slidev Theme" text hue≈166–170, single hue; mountain photo is background, excluded) | full-bleed-image | yes | — | matches 82a-deck worked table (admissible; full-bleed mountain photo behind 2-line title, C14, passes A6) |
| NPM:018 | display (hand-drawn "Drawn, not slided", Excalidraw/Virgil-style letterforms) | one-accent (blue underline squiggle hue≈210, single hue; yellow annotation box and "Andrew/Milon/You" collaborator pill tags treated as collaboration-UI/demo artefacts and ignored, same footing as C20 UI chrome — **disclosed**: if the yellow box were counted instead this would be multi) | centered (heading+subtitle bbox centre ≈0.3% off slide-centre) | yes | — | matches 82a-deck worked table for admissible/display; black text on white, high contrast; pill tags are labelled/functional so exempt from A5 |
| NPM:025 | sans ("Meet" sets the largest/topmost run; "eloc" is an inline monospace product-name badge on the same baseline — **mixed-face heading, disclosed**) | mono (white background; grey badge L≈0.95 excluded; all text achromatic) | centered (heading+subtitle visually centred; hero composition) | yes | — | black text on white, high contrast |
| NPM:026 | sans (bold rounded "Unicorn slidev theme") | mono (purple/magenta gradient is background — hue sampled 265–295° across the slide, excluded; cartoon avatar is an illustration, excluded; no other chromatic marks) | left (bbox centre 23.4% off slide-centre; avatar illustration ≈13.6% of area, <30% so not split) | yes | — | text `#FFFFFF` vs gradient patch `#8A2CB2` = 6.81:1; gradient hue stays within 265–295°, never crosses from 230–255° so **not A7(b)**; 0 hues counted so no "sole accent" for A7(a) |
| NPM:031 | serif (slab/serif feet on "Mokkapps Slidev Theme") | fill-blocks (dark-grey/near-black blobs ≈10.0% + light-grey blob ≈2.5% + teal blob hue154 ≈2.0%, combined ≈14.5% ≥10%, thick organic blobs — blobs are explicitly not illustrations, §2) | centered (bbox centre 0.77% off slide-centre) | yes | — | gridcolor: background white/off-white 85.0%; blob classes as above; dark text on white, high contrast |
| NPM:032 | serif ("Slidev" is the topmost/equal-height line, serif feet visible; "Theme" below is sans) | one-accent (red "Slidev" hue≈355–0, single chromatic hue; black "Theme" achromatic; white background) | centered (stacked lockup visually centred) | yes | — | black/red text on white, high contrast; no busy fill |
| NPM:035 | sans (clean grotesque "WebHH Theme", no serifs) | mono (plain white background, only black achromatic text) | left (bbox centre 22.9% off slide-centre) | yes | — | black text on white, high contrast |
| NPM:041 | sans (bold rounded "Slidev Theme Cobalt", no serifs) | mono (flat cobalt-blue background, excluded; white text achromatic; 0 hues counted so no "sole accent" — flat colour is also not A7 per the explicit "flat indigo/purple is not A7" rule) | centered (text bbox 512–1444 of 1960w, centre 978 vs slide-centre 980 ≈0.1% off) | yes | — | text `#FFFFFF` vs bg `#1C398E` = 10.37:1 |
| NPM:044 | sans (bold "DaoCloud Slidev Theme", no serifs) | one-accent (green hexagon-tunnel + step-bars, hue 120–144 (within 30° so one bucket) ≈7.9% of slide, <10% so hue-count applies, not fill-blocks; near-black is background 90.5%) | left (bbox centre 14.5% off slide-centre; silhouette-in-doorway photo ≈12.5% of area, <30% so not split) | yes | — | white text on near-black, high contrast; concentric hexagons read as one continuous tunnel pattern (C20), not ≥3 identical discrete motifs, so no A5 |
| NPM:073 | sans (bold "Slidev Theme Onecraft", no serifs) | one-accent (OneCraft logo badge + small leaf icon, teal/gear hue≈180–190, single hue bucket, small area; blurred code-screen photo is background/photo, excluded) | full-bleed-image (blurred photo covers 100% of slide; title sits directly on it, no opaque panel) | **no** | **A6** | heading crosses a lighter blurred patch: white text vs local background `#DCA067` = 2.27:1 (<3:1 large-text floor required by C14/A6 for text set directly on a photo); a darker crossing elsewhere gives 15.0:1, so legibility is inconsistent across the glyph run and the low measurement governs |

## Exposure / sensitivity note

Worked-example ids in this sample: **LO:021, LO:029, MS:010, MS:013, NPM:006, NPM:018** (6 of 27).
Each was coded independently from the measurements above, not copied from 82a-deck.md's table
(which in any case gives correct codes for only some of the four features per row, not all). The
orchestrator's sensitivity run should recompute agreement on the remaining 21 non-exposed ids:
LO:011, LO:014, LO:015, LO:016, LO:031, LO:035, LO:041, MS:007, MS:014, MS:018, MS:019, MS:020,
NPM:002, NPM:025, NPM:026, NPM:031, NPM:032, NPM:035, NPM:041, NPM:044, NPM:073.

## Admissibility summary

- Excluded: **LO:015** (A6, body-text contrast 2.46:1), **NPM:073** (A6, title-on-photo contrast
  2.27:1 in a crossing patch).
- All other 25 sampled items: admissible.

## Scratch

Working files (image downloads, `gridcolor.py`, crops, zoom crops) are in
`research/designs-evidence/tmp-deck3/`, deleted at the end of this task.
