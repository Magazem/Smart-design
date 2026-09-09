# Print Production Values — T7/T9 and the Print-Ready Promise

Scope: sourced values for `page-formats.csv` (T7) print columns and `constraints.csv`
(T9) professional-print rows, plus a ruling on §7 open question 2
(`09-library-schema.md:848-851`). Read against `03-document-design-knowledge.md` §C
(:163-204) and §E (:242-279), which this supersedes for print-specific values —
§E's typography/numeral-style material outside print production is untouched.

---

## 1. The ruling

Two terms, precisely, then a ruling on all three candidates the task named (trim+bleed geometry alone / PDF/X-4 with RGB + output intent / neither).

**Press-ready** = an imposition-ready PDF/X file a shop RIPs and imposes with no intervention: embedded fonts, a `/OutputIntents` dictionary carrying a real ICC profile, and correct `TrimBox`/`BleedBox` geometry (ISO 15930 family; pdfa.org/technical-side-and-requirements-of-pdfx). **Print-shop-submittable** = a PDF whose trim size is correct, whose full-bleed art physically extends past the intended trim line, whose fonts are embedded, and whose images clear the DPI floor, but which carries none of PDF/X's structural machinery — the shop's own prepress does the rest (color conversion, box interpretation, marks).

**Candidate 1 — trim+bleed geometry present in the page box, nothing else: this alone is not press-ready, and is exactly what "print-shop-submittable" already covers.** A page box sized to trim+bleed with no `/OutputIntents` and no `/GTS_PDFX` version key is a plain PDF, not a PDF/X file by any ISO 15930 part — it's the honest ceiling for Chromium's output (§2 below), not a third tier.

**Candidate 2 — PDF/X-4 with RGB content and an RGB output intent: this is real, and it is not the same thing as candidate 1.** PDF/X-1a forbids RGB outright (CMYK/spot only). PDF/X-4 (ISO 15930-7) does not — it permits a document to use a single device-independent color space with a matching output intent, and if that color space is RGB the output intent must itself be an RGB profile, e.g. sRGB (confirmed against duon-portal's PDF/X-4 RGB-output-intent guidance and pdfa.org). Concretely: WeasyPrint ≥67 exposes exactly this via `--pdf-variant=pdf/x-4 --output-intent=srgb` (doc.courtbouillon.org/weasyprint/stable/api_reference.html) — a structurally valid PDF/X-4 file whose content never leaves RGB. This dissolves the licensing caveat a CMYK output intent would carry: an sRGB (IEC 61966-2-1) profile is the same one bundled with essentially every OS, browser and imaging library, unlike GRACoL/SWOP profiles which Adobe distributes under its own restricted terms. **Caveat, sourced not assumed:** WeasyPrint sets `/Group << /CS /DeviceRGB >>` on every page/Form XObject unconditionally; Kozea/WeasyPrint#2723 documents this as a PDF/X-4 violation specifically *when the output intent is CMYK* (DeviceRGB transparency group vs. a CMYK output intent mismatch). With an **RGB** output intent the group colorspace and the output intent agree, so the failure mode as described should not trigger — but that's read off the bug report's stated trigger condition, not independently tested against a real validator, and belongs with the other unverified items in §5.

**Candidate 3 (implicit) — full CMYK press-ready:** still correctly a hard-fail on every current T8 row, per the original analysis below.

So the honest three-tier picture is: **plain print-shop-submittable RGB** (works today on Chromium, no new dependency) < **PDF/X-4 RGB — structurally emitted, live-confirmed (§6); conformance validated offline, not in-sandbox** < **full CMYK press-ready** (needs WeasyPrint ≥67 + a bundled CMYK ICC profile, and still hard-fails on Chromium). T8's current `Supports Bleed=no`/`Supports CMYK=no` on *every* row is stale for `pdf-weasyprint` on both the bleed axis (confirmed live, §6) and, via the PDF/X-4-RGB path, the "structurally press-ready" axis — CMYK specifically is a separate, still-unmet bar.

**A stdlib-only route to any of this does not exist** — Python's standard library has no color-management or PDF-authoring capability at all. **A pip route exists for the RGB and PDF/X-4-RGB tiers today, and for full CMYK conditional on shipping a licensed ICC asset.** WeasyPrint ≥67.0 (current PyPI release: 69.0, 2026‑06‑02) added `device-cmyk()`, `@color-profile` (external ICC binding), `--output-intent`, and `--pdf-variant` spanning PDF/X-1a through PDF/X-5g (doc.courtbouillon.org/weasyprint/stable/common_use_cases.html; changelog v67.0, 2025‑12‑02). It has independently supported CSS Paged Media `@page { bleed: …; marks: crop cross }` — a real `TrimBox`/`BleedBox` — since v0.41 (Oct 2017). **This is a genuine capability gap between the two `pip`/`preinstalled` engines T8 treats identically, and I'm flagging it back to the team rather than editing T8 myself.** Remaining caveats:

1. Full CMYK press-ready needs a redistributable ICC file shipped as a binary asset alongside the skill. ECI's CMYK profiles (e.g. `ISOcoated_v2_eci.icc`) are stated to be freely distributable; Adobe-hosted GRACoL/SWOP profiles are not (eci.org/en_colorstandards_offset; Adobe ICC EULA). This caveat does **not** apply to the PDF/X-4-RGB tier, which needs only the near-universally-bundled sRGB profile.
2. **Verified live, resolved.** WeasyPrint's bleed-area geometry has open and recently-open GitHub issues (Kozea/WeasyPrint #934, #1446) about backgrounds not extending correctly into the declared bleed. Live-tested in the user's claude.ai sandbox (WeasyPrint 69.0, `17-print-live-tests.md` Test 1): `TrimBox [0 0 419.527559 595.275591]`, `BleedBox [-8.503937 -8.503937 428.031496 603.779528]`, `MediaBox == BleedBox` — exactly 8.503937pt (3mm) larger than TrimBox on every side, PASS confirmed against this report's own pass criterion. The box geometry is no longer a documentation-only claim. **Still open:** whether the painted background actually reaches the BleedBox edge (box-correct is not the same as paint-correct) — see `17-print-live-tests.md` Test 1 for the one-line PNG-render check that would close this out.
3. ~~The PDF/X-4-RGB transparency-group caveat above is inferred from a bug report's stated trigger condition, not independently tested.~~ **Live-tested, see §6: the failure mode did not occur** (DeviceRGB transparency Group count = 0 on the emitted file). What remains open is full third-party conformance validation (veraPDF/Acrobat), not this specific bug.

**Verdict:** don't claim plain "press-ready" for any current `preinstalled` render target (Chromium never qualifies). Do treat "print-shop-submittable RGB" as honest and shippable today on every current target. Do treat "PDF/X-4, RGB output intent" as a real, stronger, likely-shippable middle tier via WeasyPrint ≥67 — pending items 2 and 3 above — that needs no CMYK asset and no licensing decision, and is worth a T8 row of its own rather than folding into either existing bucket. Full CMYK press-ready is real but gated on a packaging decision (which ICC profile to bundle) that this report surfaces but doesn't make.

---

## 2. T7 page-formats — sourced values

### 2.1 Trim sizes

| Item | Value | Unit | source-or-tag | depends-on |
|---|---|---|---|---|
| A4 | 210 × 297 | mm | FACT — ISO 216 (en.wikipedia.org/wiki/International_standard_paper_sizes) | — |
| A5 | 148 × 210 | mm | FACT — ISO 216 | — |
| A3 | 297 × 420 | mm | FACT — ISO 216 | — |
| A2 (poster) | 420 × 594 | mm | FACT — ISO 216 | — |
| A1 (poster) | 594 × 841 | mm | FACT — ISO 216 | — |
| US Letter | 215.9 × 279.4 (8.5 × 11 in) | mm | convention, US/Canada — no ISO analog, ANSI/ASME Y14.1 customary series (colorcopiesusa.com) | region: US/Canada |
| DL envelope | 110 × 220 | mm | FACT — ISO 269 (blog.printleaf.com/paper-sizes/international-envelopes/dl) | — |
| DL leaflet (⅓ A4, "1/3 A4") | 99 × 210 | mm | convention — derived from A4 tri-fold panel width, not itself an ISO size | — |
| Business card, EU | 85 × 55 | mm | convention, regional (papersizes.io/business-card) | region: EU |
| Business card, US/Canada | 88.9 × 50.8 (3.5 × 2 in) | mm | convention, regional (papersizes.io/business-card) | region: US/CA |
| Business card, ISO/A8-based | 74 × 52 | mm | FACT — ISO 216 A8, used where a single ISO-derived card size is wanted | region: uncommon in practice |

### 2.2 Bleed, safe margin, trim tolerance

| Item | Value | Unit | source-or-tag | depends-on |
|---|---|---|---|---|
| Bleed, small/standard format (A4/A5/DL/business card/office print) | 3 (0.125 in) | mm | convention, near-universal shop minimum (Solopress, solopress.com/blog/knowledge-base/how-big-should-bleed-be-for-printing; Mixam, mixam.com/support/bleed) | depends on: shop; treat 3mm as floor, not ceiling |
| Bleed, large format (poster/banner/signage) | 5–10 | mm | convention (beautiful.co.uk large-format bleed guide; foamboardprintshop.com) | depends on: shop and substrate — canvas/wrap products need more |
| Safe margin, business card | 5 (some shops cite 1/8in=3.175mm as a floor) | mm | convention (apexworkwear.ca/safe-margin-for-print-design; apexworkwear.ca/business-card-bleed-and-safe-area) — larger near rounded corners: a 4mm corner radius + 3mm bleed needs ≈7mm clear | depends on: shop; add clearance if corners are rounded |
| Safe margin, standard poster/flyer (≤24×36in / ≤A2) | 6 (0.25in) | mm | convention (apexworkwear.ca/safe-margin-for-print-design) | depends on: shop |
| Safe margin, large-format poster (≥36×48in, banners, signage) | 12.7 (0.5in), or 6–10 for banners/yard signs | mm | convention — cutting tolerance widens on large sheets (apexworkwear.ca/safe-margin-for-print-design) | depends on: shop, sheet size |
| Safe margin, other mid-size formats (A4/A5/DL not otherwise listed) | 3–6 | mm | convention, standard shop practice (same source cluster as bleed) — sources do not differentiate this range by format the way they do for business cards and large-format posters | depends on: shop |
| Trim/cutting tolerance (guillotine mechanical variance) | 0.5–1.5, up to ~2 on multi-sheet stacks | mm | convention/shop-spec — smartpress.com "Cutting Tolerance for Print"; guillotine blade tolerance ≈±0.2mm per maxtormetal.com, but stack-shift dominates real-world variance | depends on: shop, stack height, blade condition |

### 2.3 Fold panel geometry

All panel sets below sum to the finished trim dimension they fold *across* — `validate-fold-geometry` per `09-library-schema.md:472-474` checks this sum, so it is stated explicitly per row.

| Item | Value | Unit | Sums to (Trim W/H) | source-or-tag | depends-on |
|---|---|---|---|---|---|
| Z-fold, US Letter (3 equal panels) | 93.13 / 93.13 / 93.14 | mm | 279.40mm (11in edge) | FACT — no panel tucks inside another, so no thickness compensation applies; 279.4/3=93.133̄ (printingpartners.net/folding-guide) | — |
| Tri-fold, US Letter (2 outer + 1 tuck panel) | 93.66 / 93.66 / 92.08 (3 11/16in / 3 11/16in / 3 5/8in) | mm | 279.40mm (11in edge) | convention, shop spec — 2×93.6625+92.075=279.40 exactly (stocklayouts.com; printingpartners.net) | depends on: stock weight, see fold-allowance row below |
| Tri-fold, A4 (2 outer + 1 tuck panel) | 99.5 / 99.5 / 98.0 | mm | 297mm (long edge) — finished folded footprint is 210×99mm, i.e. the "DL leaflet" row in §2.1 | convention — tuck panel ≈1.5mm narrower than the outer panels, same ratio pattern as the sourced Letter row; no single authoritative A4-specific source, figures cluster around this split | depends on: shop, stock thickness |
| Gate-fold, 4-panel, finished width W | wide panel = W/4 + 0.8 (1/32in); narrow/tuck panel = wide − 1.6 (1/16in) | mm, formula | W (2×wide + 2×narrow = W by construction) | shop formula (thempxgroup.com/pages/panel-size-calculator) | depends on: finished width, stock |
| Roll-fold, 4+ nested panels | each inward panel narrower than the one outside it by 1.5 (text stock) or 3 (cover stock) per nest, cumulative | mm | should sum to Trim W, but no closed-form guarantees it | convention (printingpartners.net/folding-guide) — source states this is "the most complex panel sizing of any common fold type" with no fixed closed-form | depends on: panel count, stock weight — **no fixed formula exists**, see §5 |
| Fold-in allowance ("creep"), text weight (80–120gsm) | ≈0.8 (1/32 in) per fold | mm | shop convention (printingpartners.net) | depends on: shop |
| Fold-in allowance ("creep"), cover weight (200–300gsm) | 1.5–3 (1/16–1/8 in) per fold | mm | shop convention (printingpartners.net) | depends on: shop |
| Scoring required above | 170 | gsm | convention, general bindery practice (printingpartners.net) | depends on: stock, fold direction relative to grain |

**Why the tucking panel is always narrower:** the panel that folds innermost must clear the thickness the other folded layers add outside it, or the fold binds and the piece won't close flat — this is the mechanical reason behind every non-Z fold's asymmetric panels, not a stylistic choice (matches 03's existing note at :191-194; sourced above rather than asserted).

### 2.4 Recommended stock by fold count / use

| Item | Value | Unit | source-or-tag | depends-on |
|---|---|---|---|---|
| Any multi-panel fold (tri-fold/roll-fold/Z-fold/gate-fold) body stock | 80–100 lb text (≈120–150 gsm) | lb / gsm | convention (printingpartners.net: "80lb text is the standard… avoid cover stock entirely for tri-folds") | depends on: shop; heavier stock needs scoring (§2.3) |
| Single-panel flyer/poster (no fold, handled or displayed) | cover-weight or coated photo stock, ~200gsm+ | gsm | convention, general print-shop practice | **cannot be sourced to a specific figure** — no authoritative citation found beyond generic "heavier for standalone pieces" (see §5) |
| Business card | 14–18pt (≈350–450gsm) cover/card stock | pt / gsm | convention, standard paper-weight conversion charts (qinprinting.com; centexprinting.com) | depends on: shop, region — pt is a US caliper measure, gsm the metric-region equivalent, not a strict 1:1 |

Paper-weight conversion facts used above (FACT, arithmetic conversion, not shop-specific): text/book stock ≈ lb × 1.48 = gsm; cover stock ≈ lb × 2.708 = gsm (qinprinting.com/paper-weight-conversion-gsm-to-lbs). 80lb text ≈ 120gsm; 100lb text ≈ 150gsm; 80lb cover ≈ 215gsm; 100lb cover ≈ 270gsm.

### 2.5 Minimum raster DPI at final size

| Item | Value | Unit | source-or-tag | depends-on |
|---|---|---|---|---|
| Continuous-tone (photos), normal handheld viewing (<1m) | 300 | dpi | convention, industry-wide — tied to 2× the halftone screen ruling (2×150lpi=300dpi) (4over4.com; letsenhance.io) | depends on: the press's actual halftone screen ruling, typically 133–175 lpi |
| Line art / 1-bit (logos, barcodes, hairline rules, micro-text) | 600–1200 | dpi | convention (jotamachinery.com; scantips.com) | depends on: final reproduction size, plate/press type |
| Large-format, viewed 1–2m (posters held or near-wall) | 150 | dpi | convention, "halve DPI per doubling of viewing distance" rule (posterprintshop.com) | depends on: actual viewing distance |
| Large-format, viewed 3m+ (banners, signage) | 100 or less | dpi | convention, same source cluster | depends on: actual viewing distance |
| Office/photocopy print mode | 150 | dpi | consistent with T7's own existing example row (`a4-ens-note` = 150, `09-library-schema.md:451`) — not independently re-sourced here | matches schema's existing internal convention |

### 2.6 Colour space by print mode

| Item | Value | Unit | source-or-tag | depends-on |
|---|---|---|---|---|
| `professional` print mode | CMYK, output-intent-tagged (e.g. Fogra39/51, GRACoL2013, SWOP) | enum | FACT — required by PDF/X-1a (ISO 15930-1) and PDF/X-4 (ISO 15930-7); pdfa.org/technical-side-and-requirements-of-pdfx | — |
| `office` / `photocopy` print mode | sRGB | enum | consistent with T8's RGB-only render targets — not an independent print-industry fact, a pipeline consequence | tied to T8 engine capability, not a print standard |

---

## 3. T9 — professional-print constraint set

Evaluated against a **Chromium-emitted PDF** as the task specifies. Chromium's output has no `TrimBox`/`BleedBox`, no `/OutputIntents`, and RGB content only, so several checks are trivially "always fails" on that engine — that's `validate-print-mode-coherence` at the T8 level (§1), not a per-document defect. Where WeasyPrint's newer output differs, it's noted; the checks themselves are the same either way.

A structural note behind every "partial": PDF is largely a plain-text object-dictionary format with `FlateDecode` (zlib) compressed content streams — both `re` and `zlib` are Python stdlib. That makes presence/dictionary checks and content-stream token scans genuinely stdlib-feasible; it does **not** make full PDF semantics (indirect object graphs, compressed cross-reference/object streams some writers use in PDF 1.5+, embedded image color modes) stdlib-feasible — there is no PDF object model in the standard library.

| id | what is checked | threshold | severity | stdlib-checkable in a Chromium PDF |
|---|---|---|---|---|
| `pro-bleed-geometry` | page box = trim + 2×bleed on every side | bleed ≥3mm (≥5mm large-format), per §2.2 | fail | **no** — Chromium has no TrimBox/BleedBox at all; the box simply doesn't exist to measure. On a WeasyPrint `@page{bleed;marks}` output: partial/yes, box presence is a regex-scannable dictionary entry once decompressed |
| `pro-output-intent-present` | `/OutputIntents` array with `/S /GTS_PDFX` and `/DestOutputProfile` | presence + named condition matches an approved list (Fogra39/51, GRACoL2013, SWOP) | fail | **no** on Chromium (never present). **Partial** in general: dictionary presence is regex-scannable; validating the embedded ICC binary is a real, matching profile needs ICC parsing stdlib doesn't provide |
| `pro-color-space-cmyk` | no RGB color operators (`rg`/`RG`, `/DeviceRGB`) in content streams | 0 occurrences | fail | **no** on Chromium (100% RGB by construction). **Partial** in general — regex over decompressed content streams reliably catches vector/text RGB operators; embedded raster images' internal color mode (JPEG/PNG) is not decodable without an image-format parser, which stdlib doesn't provide beyond raw zlib inflate |
| `pro-fonts-embedded` | every referenced `/Font` has an embedded program (`/FontFile`, `/FontFile2`, `/FontFile3`) | 100% of fonts | fail | **partial/yes** — dictionary presence scan over decompressed objects; same caveat if a writer uses compressed object streams for the font dict itself |
| `pro-trim-safe-margin` | no text/logo bounding box within the safe margin (§2.2) of the TrimBox edge | ≥3mm (format-dependent) | warn | **no** — needs live content geometry (glyph/image placement from `Tm`/`Td`/`cm` operators resolved against a real TrimBox), which is a layout problem, not a dictionary scan |
| `pro-min-dpi-raster` | every raster XObject's effective DPI at placed size clears T7's `Min DPI` | 150 / 300 / 600 per §2.5 | warn | **yes** — `/Width`/`/Height` pixel dimensions are plain dictionary entries, and placement size is derivable from the content-stream transform matrix; this needs no image decoding at all, just arithmetic |
| `pro-spot-color-declared` | if a brand row specifies a Pantone spot, content stream contains a matching `/Separation` colorspace naming it | exact name match | warn | **partial** — regex over decompressed streams for `/Separation` entries; same object-stream caveat as above |
| `print-l-delta` (existing T9 example row, `09-library-schema.md:570`) | contrast between text and background | see §4 — recommend re-deriving from RGB, not Lab | warn | **yes**, and the strongest check in this table — it can be computed from the T4 palette RGB values at build time, before any PDF exists at all |

---

## 4. The L\* contrast floor — confirmed as convention, replacement recommended

Report 03's claim that **no standardized print-contrast-ratio metric exists** is correct and I could not find one — confirmed, not refuted. WCAG 2.x's 4.5:1/3:1 ratios are defined for self-luminous sRGB displays and have no formally adopted print equivalent.

The closest *real* published standard is **not** ISO 12647 — I checked; ISO 12647-2 governs offset press calibration (dot gain / tone-value curves for CMYK process control), which is about matching ink density to a target, not about text-to-background legibility, and doesn't apply here. The closest real analog is **ADA/ANSI A117.1 accessible signage contrast**: a formally published requirement that sign text and background differ by **≥70% Light Reflectance Value (LRV) contrast**, formula `Contrast = [(B1−B2)/B1] × 100` where B1/B2 are the lighter/darker surface's LRV (International Sign Association, signs.org/codes-regulations/technical-codes-and-standards/ada-accessible-signage/sign-contrast; current ADA guidance treats 65% as the enforced floor and 70% as the safer rule of thumb). This is a real, sourced, mechanically-checkable standard — but two honest caveats stop it from being a drop-in replacement for report 03's number: (1) it's scoped to accessible signage viewed at a distance, not brochures/reports read up close — a domain mismatch; (2) LRV-percentage contrast and CIE L\* delta are **not the same quantity** — LRV is approximately linear reflectance (≈Y in CIE XYZ, as a % of perfect white), while L\* is Y put through a cube-root compression (`L* = 116×(Y/Yn)^(1/3) − 16`), so a "70% LRV" figure cannot be substituted 1:1 for an "L\* delta" figure; converting one to the other requires doing the actual math per color pair, not a unit swap.

**Recommendation:** keep report 03's 40–50 L\* figure tagged exactly as it already is — `convention, no standard` — don't upgrade its evidence class, and don't replace it with the ADA number (wrong domain, wrong unit). Instead, re-express T9's `print-l-delta` constraint as a **WCAG relative-luminance contrast ratio** (reusing WCAG's own 4.5:1 body / 3:1 large-text thresholds as the convention, since they are at least a real, rigorously published formula) computed directly against the sRGB values the design actually uses. This isn't a compromise for its own sake: every current T8 render target is RGB-only end to end (§1), so the sRGB values in T4's palette rows *are* what gets rasterized — there's no separate "print RGB" for a print-specific metric to diverge from. A script can compute this at build time from T4 without touching a rendered PDF at all, which is exactly the kind of check Rule 2 (`09-library-schema.md:29`) asks for.

**Verdict:** confirmed absent as a formal standard; do not invent print-specific numbers; recommend swapping the constraint's basis from an unverifiable Lab delta to the already-real, already-checkable WCAG contrast-ratio formula applied to actual RGB values.

---

## 5. Cannot be sourced

- **A single-panel flyer/poster stock recommendation as a specific gsm/lb figure.** Every source found gives directional guidance ("heavier for standalone pieces") without a number I'd stand behind as industry-standard; tagged `convention, no specific figure` in §2.4.
- **A fixed formula for roll-fold panel widths.** Sources explicitly describe it as the most complex fold to size and give a per-nest adjustment rule, not a closed-form; §2.3 reports the rule, not a formula, and flags this.
- **A formal print-legibility contrast standard for body text (L\* or otherwise).** Confirmed not to exist — see §4. This is a "does not exist," not a "couldn't find."
- **Whether WeasyPrint's PDF/X-4-with-RGB-output-intent output actually passes a real prepress validator.** Narrowed by §6: the specific DeviceRGB-transparency-group failure mode named in Kozea/WeasyPrint#2723 did not occur (Group count = 0, live-checked), and the file is structurally PDF/X-4-tagged with a correct sRGB output intent. **Still open:** full conformance against a real validator (veraPDF, Acrobat preflight) — the sandbox's network allowlist blocks `software.verapdf.org` and Maven Central and has no Ghostscript/Acrobat, so this specific check cannot run inside the sandbox at all. See `28-verapdf-ready.md` for the offline check prepared to close this out.
- ~~WeasyPrint's current behavior on bleed-area background fill~~ — **resolved, see §1.** Live-verified in the user's sandbox (WeasyPrint 69.0): BleedBox geometry is exactly correct. Narrowed, not fully closed: whether the *painted* fill (not just the box) reaches the bleed edge is still unconfirmed — one PNG-render check away, detailed in `17-print-live-tests.md` Test 1.
- **`fsType` / font-embedding-permission stdlib readability.** Explicitly out of scope — routed to the Document Design Researcher per open question 1 (`09-library-schema.md:845-846`).
- **Exact per-shop bleed/margin/tolerance numbers.** Physically real but shop-dependent by nature; every relevant row in §2.2 is tagged `depends on: shop` with a typical range rather than a single number, per the domain rules.

---

## 6. Verified live, 2026-09-07

Two of §1's documentation-only claims are now live-tested results, run in the user's
claude.ai sandbox per `17-print-live-tests.md`. Recorded here as the authoritative
result; §1 and §5 above point back to this section rather than restating it.

**Bleed geometry — PASS, confirmed.** WeasyPrint 69.0, A5 page, 3mm bleed declared:

```
TrimBox  [0 0 419.53 595.28]
BleedBox = MediaBox = trim + 8.5pt/side
```

`BleedBox − TrimBox` is exactly 8.5pt (3mm) on every side — this report's own pass
criterion, met exactly. **Caveat:** `MediaBox == BleedBox` with no extra room beyond
it is *expected*, not a defect — the test HTML did not set `marks: crop cross` in
`@page`, and crop marks are what would extend the `MediaBox` further; their absence
here is a test-input fact, not an engine limitation. **T8 consequence: `pdf-weasyprint`
row, `Supports Bleed = yes`,** sourced to this run.

**PDF/X-4 + sRGB output intent — structural PASS, confirmed.**
`--pdf-variant=pdf/x-4 --output-intent=srgb`, exit 0, no warnings from WeasyPrint
itself.

- `/GTS_PDFXVersion` = `PDF/X-4`
- `/OutputIntents` present, `/S /GTS_PDFX`, `/OutputConditionIdentifier` =
  `"IEC 61966-2-1 Default RGB Colour Space - sRGB"`, `/DestOutputProfile` embedded
- DeviceRGB transparency `Group` count = **0** — the Kozea/WeasyPrint#2723 failure
  mode (§1 caveat 3) **did not occur**

This closes the specific bug-report-inferred caveat from §1: the file is structurally
correct PDF/X-4 by every marker this project's stdlib inspection script can check
(`17-print-live-tests.md` Test 2). It does **not** close full third-party conformance
— see the sandbox constraint below.

**Sandbox constraint, newly discovered: network is an allowlist, not open access.**
PyPI is reachable (WeasyPrint installs fine via `pip`), but `software.verapdf.org` and
Maven Central are blocked, and there is no Ghostscript or Acrobat available either.
**Consequence: real PDF/X-4 conformance validation (veraPDF, Acrobat preflight)
cannot run inside the claude.ai sandbox at all**, regardless of WeasyPrint version or
network timing — this is a permanent constraint of that environment, not a
transient one Test 4 (pip availability) would catch. The offline check prepared on
this machine (`28-verapdf-ready.md`) exists specifically to close this gap outside
the sandbox.

**Tier ruling, updated.** Tier 2 is no longer "reachable, pending an untested caveat"
— it is **"PDF/X-4 structurally emitted and live-confirmed; conformance validated
offline, not in-sandbox."** That is a permanent shape for tier 2, not a temporary
gap: this project's own render pipeline will never be able to run veraPDF against its
own output at generation time, so "conformance-checked" is necessarily a
build-time/offline property of the *template*, not a per-document runtime guarantee
the way tier 1's box-geometry checks (§3, T9) can be.
