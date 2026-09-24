# Form — colour use recode under research/82a-general.md

Recoder: fresh worker. Retrieved/measured 2026-09-24. Scope: `colour use` ONLY (form has no
`header treatment` row — 82a-general's scope note: "form's header is replaced by `field style`
(§4), which is unchanged"). 2 coded items (`form-items.csv`, 82a C11): FMA:001 (USWDS), FMA:002
(GOV.UK Design System).

**No raster preview exists for either item.** `form-corpus.md` (Fm.1) states plainly that these
are "two web-UI design-system authorities coding to ONE archetype" with values "read from the
authorities' own published CSS/text (fetched raw with curl), not from a model paraphrase" — there
is no rendered mockup screenshot to sample pixels from, only the component doc pages and their
CSS. `form-items.csv`'s `preview_url` therefore points at the component page itself
(`https://designsystem.digital.gov/components/form/` for FMA:001,
`https://design-system.service.gov.uk/patterns/` for FMA:002), not an image.

**Method (disclosed departure from "measure from the preview"):** with no bitmap to sample, the
core colours are taken from the same cited hex values Fm.2 already quotes from each authority's
own CSS, and their HSL is computed with `tmp-bfrc/measure.py`'s `hsl_of` (identical `colorsys`
formula used throughout this recode, same S/L definitions as B2/B4). This is the same numbers,
recomputed independently rather than eyeballed, per the task's "numbers only from script output."

| id | colour (r1) | colour (r2ag) | deciding test + measurement |
|---|---|---|---|
| FMA:001 | mono at rest (red is state-only) | **mono** | USWDS at-rest colours: input border `#5C5C5C` → hue 0°, **S=0.000**, L=0.361 (achromatic, B4: S<0.20); hint text `#757575` → S=0.000, L=0.459 (achromatic). The only chromatic colour anywhere in the spec is the error state, `#B50909` → S=0.905, L=0.373 (clearly chromatic) plus the required-field red asterisk (same hue family) — but both are error/required **state**, not the resting design (Fm.2's own framing, "red only for state"), so under this reading they don't count as a resting-state cluster. With 0 chromatic clusters in the resting design → **mono** (B6: 0 clusters) |
| FMA:002 | mono at rest (red is state-only) | **mono** | GOV.UK at-rest colours: input border `#0B0C0C` → hue 180° (R=11,G=12,B=12, a 1-unit blue tint), **S=0.043**, L=0.045 (achromatic, B4: S<0.20, also near-black L<0.12 — doubly achromatic). The only chromatic colour is the error state, `#CA3535` → S=0.584, L=0.500, again state-only by Fm.2's framing. 0 resting-state chromatic clusters → **mono** |

**Caveat carried over from Fm.5, unaffected by this recode:** treating error-state red as excluded
is an extension of 82a-general by analogy (B1d excludes "editor and UI artefacts"; an error state
is arguably closer to that than to a permanent design colour), not something 82a-general states
for forms explicitly. A reviewer could reasonably count the error red as a genuine chromatic
element (both authorities document it in their own primary CSS, not a transient editor artefact),
which would flip both items to **one-accent**. This exact ambiguity was already flagged in Fm.5
("a reviewer could code that as one-accent") and stands unresolved here — disclosed, not decided
silently.

## Addendum: Fm.8 additions (Design Researcher 3, 2 new authority items)

`form-corpus.md` grew from 52 to 101 lines while this task was in progress: §Fm.8 (82b A3) added
two more L3 authorities, **FMA:003** (ABS Forms Design Standards 2023, Diagram 6) and **FMA:004**
(NHS service manual, text input), plus its own re-check of FMA:001/002 (Fm.8.4, unchanged, "mono").
`form-items.csv` was regenerated (now 4 rows) per the task's re-extract instruction; `FMA:004`'s
`preview_url` resolves to `https://service-manual.nhs.uk/design-system/components/text-input`
after fixing the extraction script's authority-name join (Fm.8.1 spells the source "NHS digital
service manual", Fm.8.3's own `Authority` column spells it "NHS service manual, text input").

Fm.8.3 explicitly labels its colour column "**colour (82a-general §B)**" and shows its own B-series
reasoning already (background L, B1a/B1e exclusions, S/L values with the exact ≥0.20/≤0.90
thresholds spelled out) — like the memo M.6 addition, these two are a fresh coding to
82a-general itself, not a §4 coding needing translation. This addendum is a verification pass, not
a re-derivation.

| id | colour (Fm.8.3) | verification against 82a-general §B |
|---|---|---|
| FMA:003 | mono | `measure.py`: background `#ececec` → L=0.925 (paler than the 0.90 pale-tint ceiling, B1e-adjacent baseline, correctly treated as the neutral base, B1a); ABS logo and barcode correctly excluded (B1b/B1c); fill blocks measured at 0%; the only residual hue pixels are disclosed as anti-alias fringe around black text (B2: "anti-aliasing... around black text are not colour") rather than counted → 0 clusters → mono, correct. Diagrams 7/8 (not the coded specimen, §3.2 "first design shown" rule) are disclosed as an inline sensitivity: Diagram 8's fill blocks measured at 7.45%, correctly under the 10% line, so it stays out of fill-blocks even under that alternate specimen choice |
| FMA:004 | one-accent, BORDERLINE | text `#212B32` → hue≈205°, **S=0.2048**, L=0.163; input border `#4C6272` → hue≈205°, **S=0.2000**, L=0.373 — both computed here independently with `hsl_of` and matching Fm.8.3's own values to 3-4 decimal places. Both clear the B4 chromatic floor (S≥0.20) by a hair (0.0048 and 0.0000 over the line respectively — the border sits exactly ON the 0.20 boundary, "≥0.20" reads it in); same hue (single-linkage cluster, ≤30° apart, trivially — they're the same 205°); 2 elements (text + border) meet B5 presence → 1 cluster → **one-accent**. This is a genuine borderline the exact threshold (S=0.2000 to 4 places) makes it turn on whether "≥" is read as strictly-inclusive, which 82a-general's own wording ("S ≥ 0.20") supports; page `#F0F4F5` correctly excluded at L=0.951 (B1e); red error state again excluded as state-only, consistent with the FMA:001/002 reading above |

## Value counts (4 coded items)

**colour use:** mono 3 (FMA:001, FMA:002, FMA:003), one-accent 1 (FMA:004), multi 0, fill-blocks 0.

No change vs the authority's own r1 call for any of the 4 items; the caveat above (error-state red
possibly countable, flipping FMA:001/002/003 to one-accent too) is the same one already on record
in `form-corpus.md` Fm.5/Fm.8.6, now re-derived with `hsl_of` numbers rather than read off the CSS
by eye, and stands unresolved by design (disclosed, not decided silently).
