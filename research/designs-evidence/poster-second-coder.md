# poster — independent second coder (research/82 §7, seed "82a:poster")

Coder: Opus Reviewer, 2026-09-25.

## 1. Method

**Read:**
- research/82 §4 (rubric; poster variant `orientation`) and §5;
- research/82a-general.md (§A header, §B colour; binding for poster);
- 82a-clarifications-1…5, incl. C8 (poster contrast 3:1 for text ≥ 18 pt), C17 (fill L ≤ 0.90),
  C20, C29 (thresholds literal), C30 (charts are marks);
- `poster-items-github.csv` and `poster-items-pool.csv`.

**Not opened:** any poster `.md` file, research/91.

**Exposure disclosure (C12):** while compiling research/91, the output of a grep over
`poster-corpus-github.md` showed one item-level fact: "#19 body sampled at >= 5.9:1". That
concerns GH:019, which is in this sample. My GH:019 exclusion below rests on its gold headings,
not its body text. A sensitivity line excluding GH:019 is given in §4. No other poster codes
were seen.

**Previews** (the csv's first `preview_url`) went to `tmp-sc5/`, deleted at the end:
- PDFs rendered with PyMuPDF. Declared fonts and exact span colours were read from the PDF; a
  declared font wins (§4).
- Raster previews measured with PIL.
- Contrast with `scripts/lib/color.py contrast_ratio`.

**Page** = the whole poster. Title = the largest non-logo text; the header block is found
wherever it sits (82a-general §A.1).

**Colour** (§B):
- Background = the modal colour class. A full-page gradient is the background (GH:046).
- Excluded: logos, crests and photos.
- Fill blocks: L ≤ 0.90, thickness ≥ 5% of the short side, together ≥ 10% of the area.
  Full-width band heights were measured by a row scan.
- Charts are marks (C30). A hue needs ≥ 2 elements, or 1 element ≥ 0.5% of the area (B5).

**Density** (§4, poster): text blocks > 60% of the area = dense, < 30% = airy (estimated from the
render).

## 2. Sample

Ids from both csvs (55), sorted, then
`random.Random("82a:poster").sample(ids, max(min(10, len(ids)), math.ceil(0.25*len(ids))))`
gives **n = 14**:

`GH:040, GH:046, PT:pollux, GH:051, GH:020, GH:036, GH:022, PT:pasquino, PT:simple-research-poster, PIM:004, GH:008, GH:019, GH:021, GH:003`

## 3. Coding table

| id | columns | heading | body | colour | header | rules/boxes | density | orientation | admissible |
|---|---|---|---|---|---|---|---|---|---|
| GH:003 | 3+ | sans | sans | fill-blocks | band | none | airy | landscape | yes |
| GH:008 | 3+ | serif | serif | multi | ruled | boxes | standard | landscape | yes |
| GH:019 | 3+ | sans | sans | one-accent | plain-centered | boxes | standard | landscape | **no — C8/A6** |
| GH:020 | 3+ | sans | serif | multi | ruled | rules | airy | landscape | yes |
| GH:021 | 3+ | serif | serif | fill-blocks | band | none | standard | landscape | yes |
| GH:022 | 3+ | sans | serif | fill-blocks | band | rules | standard | landscape | yes |
| GH:036 | 3+ | sans | sans | mono | plain-centered | rules | dense | landscape | yes |
| GH:040 | 2-equal | sans | sans | multi | band | rules | dense | landscape | **no — C8/A6** |
| GH:046 | 2-equal | serif | serif | one-accent | plain-centered | boxes | airy | portrait | yes |
| GH:051 | 3+ | sans | sans | fill-blocks | plain-centered | boxes | standard | landscape | yes |
| PIM:004 | grid | sans | sans | fill-blocks | plain-left | boxes | standard | portrait | yes |
| PT:pasquino | 2-equal | serif | sans | multi | plain-left | rules | dense | portrait | yes |
| PT:pollux | 2-equal | sans | sans | one-accent | band | rules | standard | portrait | yes |
| PT:simple-research-poster | 3+ | serif | serif | fill-blocks | band | rules | dense | landscape | yes |

### Per-item measurements

- **GH:003** — Navy band `(12,36,60)` from 0 to 15.1% of H, full width; the title is on it, so
  band. The band plus the navy section bars exceed 10%: fill-blocks. The Oxford crest is a logo.
- **GH:008** — "Stanford University" (the title; the red wordmark top-left is a logo). A red
  full-width rule sits directly below the header block: ruled. The cardinal red headings and
  frames form one cluster, and the green links/emphasis `(0,112,92)` appear across ≥ 4 elements
  (6.05:1), a second cluster: multi. The campus photo and seals are excluded. 2 of about 8
  blocks are bordered (not A8).
- **GH:019** — Gold title and section headings, core `#EAB438`, **1.89:1** on white. That's
  below the poster 3:1 floor for text ≥ 18 pt (C8/A6), so excluded. The image placeholders are
  not colour elements.
- **GH:020** (PDF) — Title "Pitch perception…" in LMSans10-Bold, `#7a0019`; offset about
  +0.07W. A maroon full-width rule sits below the affiliation line: ruled. The bibliography text
  `#667a9a` has S 0.205 (≥ 0.20, C29) and appears in 79 spans, a second hue: multi. Its
  4.36:1 at 29.3 pt passes the 3:1 poster floor. Body is LMRoman (serif).
- **GH:021** — Black band 0–12.4% of H plus a 5.3% footer: fill-blocks. Gold serif title on the
  band. The SJTU crest is a logo.
- **GH:022** — VU blue band 0–14.2% of H plus a 3.3% footer (≈ 17.5%): fill-blocks, band. Orange
  "The Good/Bad/Ugly" headings are 3.2:1 at large size, which passes 3:1.
- **GH:036** — The pale grey header strip has L > 0.90 (C17), so it's not a fill: not a band.
  Title centred. Chart curves in Figure 2 are marks (C30): a red and a blue curve, one element
  each, 0.018% of the area, so neither passes B5. Photo and logos excluded: mono.
- **GH:040** (PDF) — Title CMSSBX10, white on a navy `#273c75` band from 0 to about 8.5% of H.
  The grey and peach blocks are L 0.929 and 0.951, tints and not fills, so the fill total is
  < 10%. Navy headings plus orange `#eb811b` inline emphasis (10 spans) make 2 clusters: multi.
  **The orange body-text emphasis is 2.73:1 at 34.7 pt, below the 3:1 poster floor (C8/A6), so
  excluded.**
- **GH:046** (PDF) — Title SFBX (CM serif), centred between logos, on the full-page
  lavender→blue gradient, which is the background. Green block-header fills are 2 elements, one
  cluster: one-accent. The Manchester and ATLAS logos are excluded. The body text sits in white
  bordered boxes, not on the gradient (A3 does not apply).
- **GH:051** — Light-grey section panels `(228,228,228)` = L 0.894 ≤ 0.90 cover about 16–19% of
  the area, so fill-blocks (a borderline value, at the threshold). Crimson title and bars; the
  Stevens logo is excluded. Title centre ≈ 0.50W.
- **PIM:004** — Indigo background `≈(40,56,248)`, hue 235–246°. That's not an indigo→purple
  shift, so not A7. Periwinkle panels at L 0.88–0.89 give fill-blocks (≈ 18%). "BIG DATA" is on
  the background, not on a band. Stats are laid out as tiles: grid. The 6 icon badges hold
  different icons (C20), so not A5.
- **PT:pasquino** — Serif title flush left on a pale gradient header, L > 0.90. The flowchart
  shapes (blue, green, orange; non-pictorial diagram, counted as marks per C30) give ≥ 2 hue
  clusters: multi. Disclosed: the 3-line author block sits on the pale tint, but that's not a
  busy fill, so admissible.
- **PT:pollux** — Steel-blue band 0–7.8% of H (under 10%) with the white title on it: band. The
  band plus blue headings form one cluster: one-accent.
- **PT:simple-research-poster** — Navy band 0–12.9% of H plus a 4% footer: fill-blocks, band.
  Serif throughout.

## 4. Summary and sensitivity

- 14 coded: 12 admissible, 2 excluded (GH:019, GH:040; both C8/A6).
- Sensitivity excluding GH:019 (exposure): n = 13, 12 admissible, 1 excluded.
