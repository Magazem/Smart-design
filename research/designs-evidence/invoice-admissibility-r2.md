# Invoice — family-wide admissibility re-run (round 2)

Per `research/82a-clarifications-7.md` (invoice row): "identity passed. Admissibility is
re-run family-wide by the first coder (mechanical A2 emoji scan; A6 per C50). GH:090 and GH:005
are excluded now (both mechanical). MS:004 is decided under C50. Re-test." GH:090 and GH:005 are
recorded as given. All other items in `research/designs-evidence/invoice-items.csv` (48 total: 40
GH + 8 MS) are re-run below.

Rules applied (read per the brief; only 82a-gate-failures.md §10 was opened, nothing in §1–§9):
- research/82 §5 (cited by the brief as §3.4) — universal A1–A7 admissibility, plus the invoice
  family's C7 constraint (table rules = `all-cells`).
- 82a-clarifications-1 C9 — eye judgement is allowed only when evidently far from the threshold;
  any pair plausibly within 3.5–5.5:1 must be sampled with `lib/color.contrast_ratio`. All
  thumbnail-sampled ratios below are estimates, disclosed as such.
- 82a-clarifications-5 C29 — thresholds are applied literally at the boundary (4.5:1 is the A6
  line; a measured value at or above 4.5 passes, below 4.5 excludes).
- 82a-gate-failures.md §10 draft C37 (ratified as **C46**, A3/A5 scope) and draft C41 (ratified as
  **C50**, A6 sampling of thin strokes: text's core colour — darkest-quartile stroke pixels, or a
  declared source colour when available; anti-aliased edge pixels are never the sample; strokes
  < 2 px at the preview's resolution are flagged BORDERLINE and excluded only if the core-pixel
  ratio is below the literal threshold).

## Method (mechanical, per item)

- **A2 (emoji):** the preview render was downloaded (raw GitHub/imgur/Microsoft-Create asset, or
  the PDF's/GIF's first frame for non-raster sources) and inspected for emoji glyphs in the
  specimen itself. A supplementary regex scan of each GitHub repo's `README.md` (raw, `main`/
  `master`) was run to flag candidate repos, then each candidate's rendered preview was checked to
  see whether the emoji is actually part of the invoice design or only README/site decoration
  (repo chrome is not the specimen — 82a-clarifications-6/7 **C47/C38**, unit of coding is the
  prescribed specimen, never site chrome). MS items have no README; their previews were inspected
  directly.
- **A6 (contrast):** for each specimen, visibly dark-on-light or light-on-dark text was judged by
  eye first (C9). Any pair that looked plausibly within 3.5–5.5:1 was cropped and sampled: the
  background is the modal light pixel in the crop, the text colour is the mean of the
  darkest-quartile of pixels that differ from the background by more than an anti-aliasing
  threshold (the C50 "core" pixel method), and the ratio is computed with this repo's
  `skill/document-design-intelligence/scripts/lib/color.py` `contrast_ratio`. All sampled previews
  in this corpus are small (≤ ~1700 px on the long edge, several ≤ 500 px) and body/label text
  renders with visibly thin strokes at that resolution, so every sampled (non-eye-evident) pair is
  flagged BORDERLINE per C50, and excludes only if the measured ratio is literally below 4.5:1
  (C29).
- **A3/A5 (C46):** every item was checked for body/title text set directly on a gradient, texture
  or photo (A3), and for ≥ 3 identical decorative motifs (A5). None of the 48 items have either —
  all are flat white/pastel/solid-panel layouts with tabular line items; the one photographic
  element found (GH:010's kitten logo) sits beside the text, not behind it.
- **C7 (all-cells table rules)** is not part of this re-run's mandate (the clarification names only
  the A2 scan and A6/C50); the 8 exclusions already on record in `invoice-corpus.md` are carried
  forward unchanged: GH:009, GH:016, GH:027, GH:054, GH:060, GH:071, GH:075, GH:106 (each has a
  fully cell-bordered data or giro/remittance table, confirmed still present on re-inspection of
  the same previews used for the A2/A6 pass above).

## Results

| id | admissible | rule | measured | note |
|---|---|---|---|---|
| GH:004 | yes | A2/A6 | n/a (evident) | README has 👋😊 but they are not in the rendered invoice; black text on white, evident pass |
| GH:005 | **no** | A2 | n/a | given: "❤️ Thank you!" printed on the specimen itself |
| GH:007 | yes | A2/A6 | n/a (evident) | no emoji in specimen; black/navy text on white, evident pass |
| GH:009 | **no** | C7 | n/a | carried forward: all-cells data table |
| GH:010 | yes | A2/A6 | n/a (evident) | README 😃 is decoration only, not in specimen; black text on white |
| GH:011 | yes | A2/A6 | n/a (evident) | navy text on light-grey panel, evident pass |
| GH:012 | yes | A2/A6 | n/a (evident) | unit of coding = the Typst preview pane only (C38/C47), editor chrome ignored; black/blue text on white, rules-only table (not all-cells) |
| GH:013 | yes | A2/A6 | ~7.4:1 (est.) | dark plum labels on near-white, sampled since plausibly borderline; passes clearly |
| GH:014 | **no** | A6 (C50) | ~3.41:1 (est., core pixel, BORDERLINE) | "No." / "INVOICE DATE" / "DUE DATE" sidebar labels: muted blue-grey on light-grey panel, below 4.5:1 |
| GH:016 | **no** | C7 | n/a | carried forward: all-cells data table |
| GH:019 | **no** | A6 (C50) | ~3.57:1 (est., core pixel, BORDERLINE) | body address block ("Tampsh, Inc." / NPWP / address) in light grey on white, below 4.5:1; a small monochrome heart glyph in the footer credit line ("Created by ♥ Mohammad Sahrullah") was checked and is not coded as A2 — single-colour icon glyph, not a colour emoji (distinct from GH:005) |
| GH:021 | yes | A2/A6 | n/a (evident) | black on white, evident pass |
| GH:024 | yes | A2/A6 | ~5.06:1 (est., core pixel, BORDERLINE) | "Bill to" / "Invoice Number" tan-grey labels on white, sampled as plausibly borderline; passes just above 4.5:1 |
| GH:027 | **no** | C7 | n/a | carried forward: all-cells data table |
| GH:028 | yes | A2/A6 | n/a (evident) | black text on white, blue IBAN/BIC labels evidently saturated; pass |
| GH:030 | yes | A2/A6 | n/a (evident) | grey item text reads clearly dark enough on white; evident pass |
| GH:035 | yes | A2/A6 | n/a (evident) | black "INVOICE" and item text on white/light-grey boxes; evident pass |
| GH:038 | **no** | A6 (C50) | ~3.38:1 (est., core pixel, BORDERLINE) | "Note number 1/2/3" running text: light grey on white, below 4.5:1 |
| GH:043 | yes | A2/A6 | ~5.78:1 (est., core pixel, BORDERLINE) | "Bill to" / "Invoice number" grey labels on white, sampled as plausibly borderline; passes |
| GH:054 | **no** | C7 | n/a | carried forward: all-cells giro/remittance table |
| GH:057 | yes | A2/A6 | n/a (evident) | black text on white, evident pass |
| GH:058 | yes | A2/A6 | ~4.78:1 (est., core pixel, BORDERLINE) | field-value lines (رقم الجوال / البريد الالكتروني) in blue-grey on lavender, sampled as plausibly borderline; passes just above 4.5:1 |
| GH:060 | **no** | C7 | n/a | carried forward: all-cells tables (bill/client and bank-details grids) |
| GH:061 | yes | A2/A6 | ~7.3:1 (est., core pixel) | "sent Thu Nov 30…" grey subtext on white, sampled as plausibly borderline; passes clearly |
| GH:063 | yes | A2/A6 | n/a (evident) | black text on white, evident pass |
| GH:066 | yes | A2/A6 | n/a (evident) | black monospace text on white, evident pass |
| GH:068 | yes | A2/A6 | ~4.72:1 (est., core pixel, BORDERLINE) | sidebar placeholder labels (Όνομα Επώνυμο, Τίτλος / Επιχείρηση …) in light grey serif on white, sampled as plausibly borderline; passes just above 4.5:1 |
| GH:071 | **no** | C7 | n/a | carried forward: all-cells data table |
| GH:075 | **no** | C7 | n/a | carried forward: all-cells data table |
| GH:080 | yes | A2/A6 | n/a (evident) | README has 🌐👉📄📖 (site-chrome nav decoration) but the specimen itself (blank "Invoice Maker" template) has none; white-on-blue and black-on-white, evident pass |
| GH:082 | yes | A2/A6 | n/a (evident) | black/blue text on white, evident pass (table body is an empty placeholder — nothing to code, no exclusion from that) |
| GH:088 | yes | A2/A6 | n/a (evident) | black text on white; small bold field-name initials read as ordinary dark text, evident pass |
| GH:090 | **no** | A6 (C50) | 3.56:1 | given: excluded per 82a-clarifications-7 |
| GH:096 | yes | A2/A6 | n/a (evident) | unit of coding = the InvoiceApp page only (C38/C47), browser/OS chrome ignored; black text on white/lavender, evident pass |
| GH:097 | yes | A2/A6 | n/a (evident) | dark grey text on white, evident pass |
| GH:099 | yes | A2/A6 | n/a (evident) | black text on white, red heading evidently saturated; evident pass |
| GH:106 | **no** | C7 | n/a | carried forward: all-cells bordered field table |
| GH:119 | yes | A2/A6 | n/a (evident) | black text on white receipt, evident pass |
| GH:128 | yes | A2/A6 | n/a (evident) | unit of coding = the rendered Typst invoice pane only (C38/C47), editor chrome ignored; black text on white, evident pass |
| GH:130 | yes | A2/A6 | n/a (evident) | black serif text on white, evident pass |
| MS:001 | yes | A2/A6 | n/a (evident) | black text on white/lavender, evident pass |
| MS:002 | yes | A2/A6 | n/a (evident) | black text on white/pink zebra rows, white on blue band; evident pass |
| MS:003 | yes | A2/A6 | n/a (evident) | black text on white/light-blue, evident pass |
| MS:004 | yes | A6 (C50) — decided per 82a-clarifications-7 | ~9.7:1 (est., core pixel, BORDERLINE) | "SALESPERSON" / "JOB" / "PAYMENT TERMS" / "DUE DATE" labels: dark grey (~#3e3e3e) core on near-white; small type at thumbnail resolution so flagged BORDERLINE, but well clear of 4.5:1 |
| MS:005 | yes | A2/A6 | n/a (evident) | black text on white, evident pass |
| MS:006 | yes | A2/A6 | n/a (evident) | white text on dark charcoal panel, black on white/peach; evident pass |
| MS:007 | yes | A2/A6 | n/a (evident) | black text on white/pink band, evident pass |
| MS:008 | yes | A2/A6 | n/a (evident) | black text on white/lavender header band, evident pass |

## Counts

- **Total items:** 48 (40 GH + 8 MS)
- **Admissible:** 35 / 48
- **Inadmissible:** 13 / 48
  - **A2 (emoji):** 1 — GH:005 (given)
  - **A6 (C50 contrast):** 4 — GH:090 (given, 3.56:1), GH:014 (~3.41:1), GH:019 (~3.57:1), GH:038
    (~3.38:1)
  - **C7 (all-cells table, carried forward, not re-tested this round):** 8 — GH:009, GH:016,
    GH:027, GH:054, GH:060, GH:071, GH:075, GH:106
- **A3/A5 (C46):** 0 exclusions — no item sets text directly on a gradient/texture/photo, and none
  has ≥ 3 identical decorative motifs.
- **BORDERLINE flags (C50, admissible but thin-stroke sampled):** 6 — GH:013, GH:024, GH:043,
  GH:058, GH:068, MS:004. All measured at or above 4.5:1 and remain admissible.
- **MS:004:** decided admissible under C50 (core-pixel ratio ~9.7:1), as instructed.

The two exclusions given in the brief (GH:090, GH:005) are unchanged; three new A6 exclusions
(GH:014, GH:019, GH:038) were found under the C50 mechanical re-run. No new A2, A3 or A5
exclusions were found. The 8 pre-existing C7 exclusions are unchanged and were not part of this
re-run's scope. The admitted set for filling is the 35 "yes" rows above.
