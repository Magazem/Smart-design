# research/designs-evidence/deck-second-coder.md — Second coder (falsifier), deck family

Per research/82 §7 and research/82a-clarifications-1.md. This worker read ONLY
research/82-design-ranking-protocol.md §4 (coding rubric) and §5 (admissibility), and
research/82a-clarifications-1.md (all of it), before touching any corpus content. The two
corpus files (`deck-corpus-npm.md`, `deck-corpus-lo-ms.md`) were never opened, read, grepped
or catted directly — they were only ever passed through the extraction script below, which
prints exclusively item id / name / source URL / preview URL(s). No feature/code column,
admissibility verdict, exclusion reason or frequency table from either corpus file was ever
seen by this worker. This file records only this worker's own coding of the rubric applied
to each sampled item's preview image(s); it contains no comparison to, or knowledge of, any
first coder's values (none were available to compare against).

## 1. Extraction method

A standalone python3 script (`tmp-deck2/extract.py`, logic summarized below; deleted with the
rest of `tmp-deck2/` at the end of this task) was run against both corpus files:

1. Parse each file as generic markdown pipe-tables (header row + separator row + data rows),
   locating tables purely by matching **header cell names** — never by reading row content.
2. A first calibration pass (`peek_headers.py`) printed only the raw header lines of every
   table in both files (column names such as `Pos | Package | dl/mo | background | ...`), so
   the layout of each file could be learned without reading any data row. That calibration
   output is what told this worker which table in `deck-corpus-npm.md` is the coded-item
   feature table (header includes `background`, `title-layout`, `heading`, `colour`,
   `rules/boxes`, `body`, `density`, `Admissible` — all forbidden) and which is the
   companion URL table (header `Pos | Package | Repo | Preview URL(s) fetched` — allowed).
3. From the npm file: the feature table is used **only** to read its `Pos` and `Package`
   columns (never the feature/Admissible columns) to know which positions are coded items;
   the companion URL table's `Pos`, `Repo`, `Preview URL(s) fetched` columns supply the
   source URL and preview URL(s), joined on position.
4. From the lo-ms file: the coded-item tables already place `id`, `Item (downloads)` /
   `Template`, and `Preview URL (first)` / `Thumbnail URL` columns alongside the (forbidden)
   feature columns in the same table; the script reads **only** the `id`, name and URL
   columns by header name and ignores every other column in that same row (`bg`, `head`,
   `body`, `colour`, `title`, `rules`, `dens`, `adm`, `reason / note` are never touched).
   Markdown links embedded in the name cell (`[name](url)`) are split into name/source-URL.
5. For Microsoft Create (`MS:*`) items the per-item table has no distinct source-URL column
   (only a thumbnail URL), so the script fills `source_url` with the one corpus-level catalogue
   URL it read from a **non-table prose line** of the same file (`https://create.microsoft.com/
   en-us/templates/presentations`, redirected to `https://powerpoint.cloud.microsoft/create/en/
   presentation-templates/?source=create_flow`, retrieved 2026-09-23) — this line is the
   corpus's own recorded fetch URL, not a per-item feature.
6. Output: one line per coded item, `id | name | source_url | preview_urls`, nothing else.
   npm yielded 39 coded ids, LO yielded 39 coded ids, MS yielded 27 coded ids — **105 coded
   ids total** across both files.

## 2. Sample

All 105 coded ids, sorted lexicographically, then per research/82a C10 (family-wide sample)
and research/82 §7:

```python
import math, random
ids = sorted([...])  # 105 ids: LO:001..LO:045 (39 present), MS:001..MS:025 (27 present, incl.
                      # per protocol id gaps at excluded/uncodeable positions), NPM:002..NPM:143
                      # (39 present)
sample = random.Random("82:deck").sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))
```

`len(ids) = 105` → `max(min(10,105), ceil(0.25*105)) = max(10, 27) = 27`.

Exact sample produced (27 ids, in the order `Random.sample` returned them):

```
MS:010, MS:001, NPM:018, LO:021, LO:030, NPM:054, NPM:017, NPM:046, LO:040, NPM:139,
NPM:032, LO:029, MS:013, MS:002, NPM:049, NPM:006, LO:028, LO:025, NPM:009, NPM:069,
NPM:041, MS:024, LO:009, MS:011, MS:003, MS:023, MS:025
```

n_sample = **27**.

## 3. Coding table

Notes on method: page 1 = title slide + first content slide where a genuine one exists. Per
82a **C7**, several sampled items ship only a title slide, or a second image that is itself
another title/section-divider variant with no real body prose (Takahashi-style single-word
decks, "section divider" slides, alternate colour-theme covers). In those cases `body class`,
`rules/boxes` and/or `density` are recorded `unknown` rather than guessed, and this is called
out per row. Colour/contrast judged from thumbnails per **C9** are eyeball estimates,
disclosed; several LibreOffice thumbnails are very small (256×144) which limits confidence.
`background`/`title-slide layout` use the literal **C1** test (image ≥30% of slide area) to
decide `image`/`full-bleed-image`/`split` vs `light`/`dark`/`centered`/`left`.

| id | name | source URL | background | title-layout | heading | colour | body | rules/boxes | density | Admissible |
|---|---|---|---|---|---|---|---|---|---|---|
| MS:010 | Floral flourish | create.microsoft.com/en-us/templates/presentations (catalogue URL; no per-item URL in corpus) | dark | split | serif | mono | unknown | boxes | unknown | yes |
| MS:001 | Abstract airbrush presentation | create.microsoft.com/en-us/templates/presentations (catalogue URL) | light | centered | serif | multi | unknown | rules | unknown | **no — A3** (title text set directly on the pink/teal gradient fill) |
| NPM:018 | slidev-theme-excalidraw | github.com/milon/slidev-theme-excalidraw | light | left | display (handwriting-style "Excalifont"/Virgil glyphs) | multi (cursor labels: green, red, blue) | sans (nearest bucket for the handwriting body font) | boxes (bordered rectangle/ellipse/dashed-box examples on content slide) | standard (~30 words on content slide) | yes |
| LO:021 | Strawberry Milk Template by Natalie Chmura | extensions.libreoffice.org/en/extensions/show/99337 | light | centered | serif | one-accent | unknown | boxes | unknown | yes |
| LO:030 | Signs | extensions.libreoffice.org/en/extensions/show/5065 | dark | centered | sans | one-accent (gold) | unknown | none | unknown | yes |
| NPM:054 | slidev-theme-touying | github.com/kermanx/slidev-theme-touying | light | centered | serif | one-accent (teal) | serif | boxes (filled band behind heading) | standard (~22 words, TOC list) | yes |
| NPM:017 | slidev-theme-scholarly | github.com/jxpeng98/slidev-theme-scholarly | light | centered | sans | one-accent | unknown (2nd image is an alternate colour-theme cover, not body content) | none | unknown | yes |
| NPM:046 | slidev-theme-hep | github.com/AvencastF/slidev-theme-hep | image (full-bleed cover photo) | full-bleed-image | sans | one-accent (teal) — **also carries an emoji** | sans | boxes (bordered box around bullet list) | dense (>40 words: two prose paragraphs + 5 bullets) | **no — A2** (🥳 emoji on title slide) |
| LO:040 | Blue White Template | extensions.libreoffice.org/en/extensions/show/99328 | light | left | sans | one-accent (blue) | sans | rules (underline below heading) | standard (5 body lines; Japanese has no word-spacing, word count is an estimate) | yes |
| NPM:139 | slidev-theme-spezi | github.com/zzzFelix/slidev-theme-spezi (repo URL unresolved in corpus, recorded as "(unresolved)") | dark | left | sans | one-accent (orange) | sans | none | standard (~19 words on content slide) | yes |
| NPM:032 | slidev-theme-takahashi | github:kecrily/slidev-theme-takahashi | light | centered | sans | one-accent (red) | unknown (Takahashi-method: 2nd slide is a single giant word, no body prose — C7) | none | unknown (C7) | yes |
| LO:029 | About Me | extensions.libreoffice.org/en/extensions/show/5098 | light | centered | serif (best-effort at 256×144) | multi (sage-green + terracotta) | unknown | none | unknown | yes |
| MS:013 | Organic presentation | create.microsoft.com/en-us/templates/presentations (catalogue URL) | light | centered | serif | multi (sage-green + terracotta) | unknown | none | unknown | yes |
| MS:002 | Scientific discovery | create.microsoft.com/en-us/templates/presentations (catalogue URL) | light | centered | sans | one-accent (pale blue frame) | unknown | rules (thin frame line) | unknown | yes |
| NPM:049 | slidev-theme-ksick-dynatrace | github.com/KatharinaSick/slidev-theme-ksick-dynatrace | dark | split | sans | multi (gradient text/avatar ring) — **also carries emoji** | unknown | none | unknown | **no — A2** (🚀 and 🔗 emoji on the only real slide); note: first preview URL ("footer.png") is a thin UI-chrome banner crop, not a slide, so it was not used as page 1 |
| NPM:006 | slidev-theme-light-icons | github.com/lightvue/slidev-theme-light-icons | image (full-bleed mountain photo) | full-bleed-image | sans | one-accent (teal) | sans | boxes (bordered "LIGHT" label) | airy (~11 words) | yes |
| LO:028 | We Care | extensions.libreoffice.org/en/extensions/show/5090 | dark | unknown — single preview shows no title text, only icon+caption rows and a photo, so title-slide layout could not be read (see disclosure below) | unknown | mono | sans | none | dense (~45-54 words across 3 caption blocks) | yes |
| LO:025 | Tiles | extensions.libreoffice.org/en/extensions/show/5089 | light | split | sans (best-effort at 256×144) | mono | sans | boxes (white rounded text card) | standard (~25-30 words) | yes |
| NPM:009 | slidev-theme-purplin | github.com/moudev/slidev-theme-purplin | light | centered | sans | one-accent (purple) | sans | boxes (rounded-card image frame) | airy (~6 words) | yes |
| NPM:069 | @ricoapon/slidev-theme-technical | github.com/ricoapon/slidev-theme-technical | dark | left | mono (declared monospace theme) | one-accent (purple) | mono | rules (underline) | unknown (2nd image is a section-divider slide, no body prose — C7) | yes |
| NPM:041 | slidev-theme-cobalt | github.com/minagishl/slidev-theme-cobalt | dark | centered | sans | one-accent (blue) | unknown (2nd image is an alternate "title-center" cover, not body content — C7) | boxes (bordered white card) | unknown (C7) | yes |
| MS:024 | Sanguine and pearl | create.microsoft.com/en-us/templates/presentations (catalogue URL) | image (~55% grayscale photo) | split | serif | one-accent (maroon) | unknown | none | unknown | yes |
| LO:009 | Chocolat & variantes | extensions.libreoffice.org/en/extensions/show/41979 | light | left | sans | one-accent (blue, multiple tints of one hue) | sans | boxes (pill-shaped sidebar nav labels) | dense (7-line bulleted outline, ~50+ words) | yes |
| MS:011 | Feathered design | create.microsoft.com/en-us/templates/presentations (catalogue URL) | image (full-bleed feather photo) | full-bleed-image | sans | mono (photo + near-white pill excluded/near-white; no chromatic text/marks) | unknown | boxes (cream pill holding the title) | unknown | yes |
| MS:003 | Music design | create.microsoft.com/en-us/templates/presentations (catalogue URL) | image (~40% portrait photo + synthwave grid) | split | sans | multi (neon green + neon pink/purple grid) | unknown | rules (perspective grid lines) | unknown | **no — A3** (tagline text set directly on the textured neon-grid background, not an opaque panel) |
| MS:023 | Impact annual presentation | create.microsoft.com/en-us/templates/presentations (catalogue URL) | light | left | sans | mono | unknown | rules (rule under heading) | unknown | yes |
| MS:025 | Solace | create.microsoft.com/en-us/templates/presentations (catalogue URL) | image (~45% photo, split) | split | serif | mono (pale sage panel judged below S≥0.20 chromatic threshold from thumbnail) | unknown | none | unknown | yes |

Disclosures on individual rows:
- **LO:028** ("We Care"): the single available preview shows no title-slide content at all
  (only an icon-caption content layout and a photo). Per the spirit of 82a C7 (which covers
  the reverse case — content-only when a title is expected), `title-slide layout` and
  `heading class` are recorded `unknown` rather than guessed from a slide that is evidently
  not the title slide.
- **NPM:049**: the corpus's first listed preview URL for this item is a ~1715×50 px crop of
  UI chrome (a footer bar), not a slide; the second URL is a genuine full title slide. Only
  the genuine slide was coded as page 1.
- Several LibreOffice thumbnails (`LO:029`, `LO:025`, `LO:028`) are natively only 256×144 px;
  heading-class and fine hue calls on these are lower-confidence, disclosed here per C9.
- Word counts for density on non-English/CJK slides (`LO:040`, Japanese) are estimates, since
  the rubric's word-count test presumes space-delimited text; disclosed per the same spirit
  as C9's contrast-estimate disclosure.

## 4. Admissibility summary

23 of 27 admitted, 4 excluded:
- **MS:001** — A3 (gradient fill directly behind title text).
- **NPM:046** — A2 (emoji 🥳 on the title slide).
- **NPM:049** — A2 (emoji 🚀 and 🔗 on the only codeable slide).
- **MS:003** — A3 (tagline text set directly on a textured/gridded background, not an opaque
  panel; distinguished from the admissible "flat panel over photo" case per 82a C8).

No comparison to a first coder's admissibility calls is made or implied anywhere in this
file — none were seen.

## 5. Cleanup

`research/designs-evidence/tmp-deck2/` (calibration script, extraction script, downloaded
preview images) is deleted at the end of this task, per instructions.
