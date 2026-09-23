# research/82a-deck — deck heading / colour / title-slide layout / admissibility, sharpened (Opus, 2026-09-24)

**Trigger.** research/82 §7 falsifier fired for deck (`designs-evidence/deck-agreement.md`,
n=27, seed `"82:deck"`). Failing features: `heading` A=0.77, `colour` A=0.67,
`title-slide layout` A=0.73, and `admissible` A=0.78. The admissibility failure is
one-directional: in all 6 mismatches, coder 1 excluded and coder 2 admitted.

This file replaces ONLY the deck decision rules for those four. Everything else is unchanged:
- `background` passed (0.81). It is **not** recoded. §2 below defines a "background region"
  only to say what the colour test excludes; it does not redefine the `background` enum.
- `rules/boxes` passed (0.85).
- Value sets, identity set, §6–§8 and 82a C1–C23 all stay as written, unless restated below.

**Variants `body` (0.78, n=9) and `density` (0.22, n=9).** Per §7 last sentence, these are
**not used in deck filling**; the deck family default applies. They are not recoded.

I viewed these previews via deck-items.csv to write the edge cases: MS:001–003, 010, 013, 023,
024, 025; LO:009, 021, 025, 028, 029; NPM:006, 009, 017, 018, 046, 049, 139. Pixel values were
sampled with PIL on the listed preview files. I did not open any source files.

## 0. Evidence scope (applies to all four rules)

**E1. Code only the previews listed for the item in `deck-items.csv`.** Both coders must see
the same evidence. A slide seen elsewhere (another gallery image, the extension page, a demo
site) is never used, for codes or for admissibility. Round-1 case: LO:021's A3 exclusion cited
a "gradient wave behind body text" that no listed preview shows.

**E2. The title slide** is the first listed preview that is a slide. A preview is **not** a
slide if its aspect ratio is outside 1.2:1–2.4:1 (e.g. NPM:049 `footer.png`, 1715×50) or it
shows UI chrome only (C2). In that case, use the next preview.

**E3. No title slide listed.** If every listed slide carries a body block (≥3 lines of
non-title text), still code the first listed slide. The "title" is its largest text line.
Record `no-title-slide` in the note. Cases: LO:025, LO:028.

**E4. Master-slide sheets.** When one image shows several miniature slides (e.g. LO:009's 3×2
master grid), the title slide is the top-left miniature. It is measured as if it were the
whole slide.

## 1. `heading` (identity), deck only

**Heading text** = the text line on the title slide with the largest cap height. If two lines
are within 10% of each other, take the topmost. Subtitle, author and footer faces are never
the heading. Case: NPM:017's heading is "Classic Academic Blue" (sans), even though its
subtitle and author lines are serif.

Decision order (first match wins):

1. **Declared font.** If the item's own source declares the title face, use it. Sources:
   - npm theme: CSS `font-family` for `h1` / `.slidev-layout h1`, or the theme's `fonts`
     config;
   - LibreOffice `.otp`: `styles.xml` title style `style:font-name`;
   - Microsoft `.pptx`: `ppt/theme/theme1.xml` `<a:majorFont><a:latin typeface=…>`.

   Reading these text files is allowed: it is not rendering (§3.3). Map the family through the
   Google Fonts `category` (SERIF→serif, SANS_SERIF→sans, DISPLAY/HANDWRITING→display,
   MONOSPACE→mono). Non-Google families map by foundry class (§4). Record the family name in
   `heading-note`.
   - If the source cannot be fetched within 2 requests, go to step 2 and record
     `glyph-judged`.
2. **Glyph test**, run only when there is no declared font. Take the first match:
   - a. Script, handwriting, blackletter, outline, inline, stencil or distressed letterforms →
     **display**. LO:021's "Title" in a handwriting face is display, not sans or serif. The
     heading enum has `display`; only body lacks it.
   - b. Equal advance widths (the "i" and "m" boxes are the same width) → **mono**.
   - c. Stem terminals of I, T, E, H or n end in strokes perpendicular to the stem (bracketed,
     hairline or slab) → **serif**.
   - d. Otherwise → **sans**.

**Never display by weight alone.** Heavy weight, condensed width, all caps, colour or
rotation never make a face display on their own. Case: MS:003's "ARTIST PORTFOLIO" is a
condensed heavy sans in neon green. It is **sans** unless its declared family is in the Google
DISPLAY category.

Record the measured cue in `heading-note` whenever step 2 decided.

## 2. `colour use` (identity), deck only

All tests run on the **title slide only** (per E2/E3). The content slide is not used; it is
often absent (C7).

**Background region.** Sample a 20×20 grid of points over the slide. Drop points that land on
photos, illustrations or text. Group the rest into colour classes: two points share a class
if both are achromatic (§4) with ΔL ≤ 0.03, or if hue is within 15° and ΔL ≤ 0.05. The class
holding the most points is the **background**. It is excluded from every test below.
- A colour ground covering most of the slide is the background, even when it doesn't reach
  the edges. MS:023: yellow `#FBE184` covers ~73% of the slide, the white edge strips are not
  fills (L 1.0), so the background is yellow.
- A gradient background is still the background (it is one region). Its hues are recorded in
  the note `bg-hue` for filling, but never count as a hue here.

**Photo / illustration.** A raster scene: photograph, painted or drawn picture, or clip-art
with ≥3 colours. Excluded from fills and hues (§4).
- Decorative vector shapes are **not** illustrations: blobs, bands, diagonals, circles,
  chevrons, frames.
- A photo washed so that every sample lies within ΔL ≤ 0.10 of one flat colour is a **tint**,
  treated as flat colour. NPM:046's faded cover photo samples L 0.92–0.99, so it is a light
  tint.

**Fill block.** A solid non-background area with HSL L ≤ 0.90 (C17; gradients count). It must
also be **thick**: it contains a rectangle whose shorter side is ≥ 8% of slide height. Thin
frames, borders and strokes fail this and are marks, not fills.
- MS:002: the pale-blue frame `#C8DBE2` is 22% of the slide area, but only ~2.5% thick. Not a
  fill.

Decision order (first match wins):

1. **fill-blocks**: the fill blocks together cover ≥ 10% of slide area.
2. Otherwise, count chromatic hues (§4: S ≥ 0.20, 0.12 ≤ L ≤ 0.90, hues ≥ 30° apart) in text,
   rules and **marks**. Marks are non-photo graphics, including thin frames and fills under
   10%. Ignore:
   - marks smaller than 0.2% of slide area;
   - UI chrome (C20);
   - the background;
   - photos and illustrations.

   Result: ≥2 hues → **multi**; 1 → **one-accent**; 0 → **mono**.

## 3. `title-slide layout` (identity), deck only

The **title block** is the heading text plus the lines within 1.5 heading line-heights of it
(subtitle, author). Its horizontal extent is its bounding box.

Decision order (first match wins):

1. **full-bleed-image**: a photo or illustration (not a tint) covers ≥ 80% of slide area, and
   the title block sits on it.
2. **split** (keeps 82a C1's threshold): a photo or illustration covers ≥ 30% of slide area, and
   its horizontal extent does **not** overlap the title block's horizontal extent (they sit side
   by side).
   - An image above or below the title (vertically stacked) is not split.
   - Decorative vector shapes never count as the image.
3. **centered**: the title block's horizontal centre is within ±5% of slide width of the slide
   centre.
4. **left**: everything else. This includes right-aligned titles; record `align=right` in
   `title-note`.

Record the measured quantity for any test decided within 10% of its threshold, in
`title-note`.

## 4. Admissibility on slides: the correct reading of A3, A5, A7

The six round-1 mismatches were all coder-1 exclusions that a literal reading does not
support.

- **A3 (text over a busy fill) on slides follows C14.** A3 excludes an item only for:
  - running text,
  - bullet text, or
  - any text block of ≥ 3 lines

  set **directly** on a gradient, texture or photo.

  A title, subtitle or author line (≤ 2 lines each) on a photo or gradient is **not** A3. It
  must instead pass A6 by C9 sampling: ≥ 4.5:1 below 24 pt, ≥ 3:1 at 24 pt or more. A flat
  opaque panel over a photo is fine (C8).
- **A5 (repeated decoration) follows C20.** It needs ≥ 3 **identical** discrete decorative
  motifs. It does not apply to:
  - motifs that differ in content (different illustrations or icons);
  - functional elements carrying their own text (navigation tabs, labelled pills, numbered
    markers).
- **A7 (Office blue / indigo→purple gradient) concerns the accent.** A7 applies only when:
  - (a) the sole accent (the one hue counted in §2 step 2) is one of the four Office blues; or
  - (b) an indigo→purple gradient is present anywhere, including the background, measured as a
    hue shift of ≥ 20° from the 230–255° range into the 265–295° range across the gradient's
    own samples.

  A **flat** indigo or purple colour is not A7.

## 5. Worked edge cases (all from round-1 disagreements)

| id | Round-1 (c1 / c2) | Measurement | Correct |
|---|---|---|---|
| MS:023 | colour fill-blocks / mono | yellow ground 73% = background; black text and rule, no hue | **mono** |
| MS:013 | colour fill-blocks / multi | beige background `#E6DACE`; khaki `#C7BFA9` (L 0.72) and terracotta `#C28E80` (L 0.63) blobs are 55% of the slide and thick | **fill-blocks** |
| LO:029 | colour fill-blocks / multi | the largest colour class is purple `#55308D` (so background is dark); red `#EC5563` diagonal bands about 25%, thick | **fill-blocks** |
| LO:009 | colour fill-blocks / one-accent | top-left master: blue concentric semicircles about 15–20% of the miniature, thick | **fill-blocks** |
| LO:009 | heading serif / sans | glyph test: serif terminals on "Cliquez pour éditer…" (unless a declared font overrides) | **serif** |
| MS:010 | colour one-accent / mono | dark background; flowers are a photo (excluded); white text; the ornament is under 0.2% of area and near-achromatic | **mono** |
| MS:002 | admissible no / yes | the petri-dish photo sits behind the 1-line title; C14 applies, so this is not A3; black on light passes A6 | **admissible** (if nothing else fires) |
| NPM:006 | admissible no / yes | full-slide mountain photo behind the 2-line title; C14 applies, so not A3; light text on dark photo passes A6 | **admissible** |
| MS:001 | (both excluded, A3) | gradient background behind the 1-line title "Pitch deck"; C14 applies, so not A3 | **admissible** (the reading changes both coders; handled by the recode) |
| LO:021 | admissible no / yes; heading sans / serif | only the title slide is listed (E1); no gradient visible. "Title" is a handwriting face | **admissible; display** |
| LO:025 | admissible no / yes | 8 **different** illustrations, not identical, so not A5 | **admissible** |
| LO:028 | admissible no / yes | background flat `#3F37C9` (H 243° at every sample); no gradient and not an accent, so not A7 | **admissible** |
| NPM:018 | title centered / left | title-block centre at slide centre ±1% | **centered** |
| NPM:139 | title centered / left | title-block centre at slide centre | **centered** |
| NPM:009 | title left / centered | title flush left at about 5% of width | **left** |
| NPM:049 | title left / split | use preview 2 (E2). The avatar illustration is about 13% of the area (under 30%). Title right-aligned | **left** (`align=right`) |
| NPM:017 | heading serif / sans | the largest line "Classic Academic Blue" has no serifs; the serif lines are subtitle and author | **sans** (unless a declared font says otherwise) |
| MS:003 | heading display / sans | condensed heavy caps in neon; no script or decoration | **sans** (unless its declared family is Google DISPLAY) |

These rows illustrate the rules. They are **not** pre-filled codes. The recoder measures every
item again. Where a declared font (§1 step 1) is found, it overrides a glyph call above.

## 6. Recode and re-test

1. **Recode.** A single **fresh worker** (neither round-1 coder, nor the round-1 second coder)
   recodes `heading`, `colour use`, `title-slide layout` and `admissible` with this file. It
   covers **all 105 coded deck items across all three corpora** (NPM 40, LO 40, MS 25):
   - The new value and its note (`heading-note`, `title-note`, `bg-hue`, rule id for
     admissibility) go into `deck-corpus-npm.md` and `deck-corpus-lo-ms.md`.
   - The old values are kept in `(r1)` columns.
   - `background`, `body`, `rules/boxes` and `density` are untouched.
   - `deck-items.csv` is unchanged unless E2 exposes a wrong first preview. In that case the
     orchestrator regenerates it by script (C11) and discloses the change.
2. **Re-test.** A **fresh, independent second coder** reads ONLY:
   - `deck-items.csv`;
   - research/82 §4–§5;
   - the 82a clarification files;
   - this file.

   Evidence .md files are off-limits (C11/C12).
   - Sample: all 105 ids, sorted, then
     `random.Random("82a:deck").sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))`
     (= 27).
   - The second coder codes the four features above for the sample.
   - **Exposure:** this file names 17 items with their correct codes. Any of those that fall in
     the sample are also reported in a **sensitivity run excluding them**. Both numbers are
     published, and the gate uses the full sample.
3. **Gate.** Each recoded identity feature needs A ≥ 0.80, and `admissible` needs A ≥ 0.80.
4. **Second failure.**
   - Each failing identity feature is **removed from deck identity** (e.g. archetype =
     background|heading|colour if title-slide layout fails again). This is disclosed in the deck
     evidence file, per §7.
   - If two or more identity features fail again, deck ships **no ranked archetypes**: seeds
     and convention only, with a Shortfall section. An archetype built on one or two unreliable
     features would not carry ranking information.
   - If `admissible` fails again, it cannot be dropped, because it decides eligibility. Each
     disputed item goes to a per-item Opus adjudication that cites the rule id and the measured
     evidence. The ruling is recorded, and the family is re-ranked. The adjudicator must not
     have coded that item.
