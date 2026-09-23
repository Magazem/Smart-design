# research/82a-general — header treatment and colour use for every remaining family (Opus, 2026-09-24)

**Trigger.** `header treatment` and `colour use` have now failed the §7 gate three times:
- cv header 0.70 (fixed by 82a-cv);
- deck colour 0.67 (fixed by 82a-deck);
- invoice header 0.33 and colour 0.50 (`designs-evidence/invoice-agreement.md`).

The failures share one cause: §4 does not say what "the header" is outside a CV, or what counts
as a coloured element. This file gives one measurable rule for each feature.

**Scope.** It **supersedes §4's `header treatment` and `colour use` rows** for invoice, quote,
cover-letter, letter, memo, report, whitepaper, proposal, brochure, flyer, poster, infographic
and one-pager. `colour use` also applies to form; form's header is replaced by `field style`
(§4), which is unchanged.
- cv keeps 82a-cv; deck keeps 82a-deck.
- Every other feature, all thresholds not restated here, §5–§8 and 82a C1–C23 stay as they are.

**Disclosure.** I was the round-1 invoice second coder, so I am excluded from both invoice
re-test roles. Worked examples were measured with PIL on the listed previews
(`invoice-items.csv`, `letter-items-l2.csv`, `cover-letter-items-l2.csv`), downloaded to the
system temp directory and deleted afterwards.

---

## A. Header treatment

### A.1 What is measured, per family

The **title** is the element that plays the role the person's name plays in 82a-cv.

The **header block** is the title plus the contiguous lines that belong to it. It is defined by
content, not position: the tests run wherever the block lies. (82a-cv's "top 20%" scope is
dropped for these families. Poster, flyer and cover titles are often mid-page.)

The **boundary** is the first element after the header block. It replaces 82a-cv's "first
section heading".

| Family | Page | Title | Header block | Boundary |
|---|---|---|---|---|
| invoice, quote | page 1 | largest text in the top 30% of the page (issuer name or "INVOICE / QUOTE / DEVIS / ANGEBOT") | title + issuer identity (name, tagline, address, contact) + document meta (number, dates) lying above the boundary | first recipient block (Bill to / Ship to / Client / À / An) or the line-item table, whichever comes first |
| letter | page 1 | sender name: the first line of the sender block | letterhead = sender name + sender address, contact and slogan lines | date, recipient block, reference line or salutation, whichever comes first |
| cover-letter | page 1 | the applicant's name | name + role line + contact lines | as for letter |
| memo | page 1 | largest text in the top 30% ("MEMO", "Memorandum" or the organisation name) | title + TO / FROM / CC / DATE / SUBJECT lines | first body paragraph |
| report, whitepaper, proposal | cover (C13) | largest text on the cover | title + contiguous subtitle / author / organisation / date lines | none (the tests use the block's own extent) |
| poster, flyer, infographic, one-pager | page 1 | largest text on the page | title + contiguous subtitle / date / venue lines | first following text block |
| brochure | the **front panel** of the outside spread | largest text on the front panel | as for poster | as for poster; every "page width" below means **panel width** |

Rules common to every family:
- Logos, logo placeholders ("CompanyLogo", "Votre logo", "<Logo>"), crests and photos are never
  the title and never meta text.
- If the largest text is a logo placeholder, take the next largest text.

### A.2 Decision procedure

This is 82a-cv's procedure and thresholds, with "name" read as **title** and "first section
heading" read as **boundary**. Strict priority; first match wins.

1. **image-hero**: unchanged (82a C1).
2. **band**: criteria (a)–(c) of 82a-cv, plus a generalised (d):
   - (a)–(c): a fill lies behind the title's glyphs (C18), with height ≥ the title's cap height
     and width ≥ 60% of page width.
   - (d) **The fill's height is ≤ 40% of page height.** A full-page tint or background is not a
     band.
3. **ruled**: criteria (a)–(d) of 82a-cv, including Addendum A1, A2 and A4.
   - A **box edge** counts as a line when the box spans ≥ 80% of page width.
   - A **full-width bar at the page edge** above the header block counts, subject to (d),
     gap ≤ 4 body lines (as 82a-cv NPM:049).
   - Lines that belong to the **boundary element** never count: the top border or header rule
     of a line-item table, or the rule of a section heading. This generalises A2.
4. **split**: 82a-cv step 4.
   - Meta = the header block's own contact or document-meta text.
   - Recipient blocks are not meta.
   - Logos and images never create split.
5. **plain-centered**: the title's centre is within ±5% of page width of the page centre.
6. **plain-left**: everything else, including right-aligned titles. Record `align=right` in
   `header-note`.

Record the measured value in `header-note` for any test decided within 10% of its threshold.

---

## B. Colour use

Page scope is the same as §A.1. Brochures use the whole outside spread, as §4 already says.

**B1. Excluded from every test:**
- (a) the **background**: the most common colour class on a 20×20 sample grid, excluding
  points on photos, illustrations and text (82a-deck §2 method);
- (b) photos, illustrations, logos and logo placeholders, with any shape that only frames a
  logo (the shape's box is ≤ 2× the logo's box);
- (c) QR codes and barcodes;
- (d) editor and UI artefacts (C20): field shading, text-boundary frames, rulers, buttons,
  browser chrome;
- (e) any colour with L > 0.90: pale tints are neither fills nor hues.

**B2. Sample the core colour, never the edge.**
- Text: the median of pixels inside strokes ≥ 2 px wide at the preview's resolution.
- Rules and shapes: the interior.
- Anti-aliasing and sub-pixel fringes around black text are **not colour**.
- An element too thin to sample (< 2 px) is achromatic, unless its source declares a hex.

**B3. Fill block.** A non-background area with L ≤ 0.90 (C17) that contains a rectangle whose
shorter side is **≥ 5% of the page's shorter side** (A4 ≈ 10.5 mm). Thinner areas are
elements, not blocks.
- **fill-blocks** if the blocks together cover **≥ 10% of page area**. Otherwise continue.

**B4. Chromatic element.** An element whose core has S ≥ 0.20 and 0.12 ≤ L ≤ 0.90 (§4).
- An **element** is one of: a text run in one colour (a word or line), one rule, one icon, one
  shape, or one sub-threshold fill.
- Near-greys (S < 0.20) and near-blacks (L < 0.12) are achromatic.

**B5. Presence.** A hue counts only if it appears in **≥ 2 separate elements**, or in **one
element covering ≥ 0.5% of page area**. A single hyperlink or a one-off coloured glyph does
not make an accent.

**B6. Clustering.**
- Place each counted element's hue on the circle.
- Hues ≤ 30° apart join one cluster (single linkage). A cluster wider than 60° is split at its
  largest internal gap.
- Clusters meeting B5: ≥ 2 → **multi**; 1 → **one-accent**; 0 → **mono**.

**Recording.** Put these in `colour-note`: background hex, block area %, and each counted
cluster with its element count.

---

## C. Worked examples (from the round-1 disagreements and new letter / cover-letter items)

These illustrate the rules; they are not pre-filled codes. The recoder measures every item again.

| id | Feature | Round-1 (c1 / c2) | Measurement | Correct |
|---|---|---|---|---|
| invoice GH:004 | header | split / ruled | a full-width rule sits directly below the header block (logo left; name + contact right, one side). Ruled comes before split by priority, and the logo cannot make split | **ruled** |
| invoice GH:004 | colour | one-accent / mono | the only colour is the "{.js}" logo, excluded by B1b | **mono** |
| invoice GH:097 | header, colour | split / plain-left; multi / mono | meta left, React logo right (a logo never makes split). Cyan logo (B1b) and green button (B1d) excluded | **plain-left; mono** |
| invoice MS:005 | colour | mono / one-accent | label core `#4D2C33` (S 0.27, L 0.24) is chromatic; 3 labels (DATE, INVOICE #, BILL TO) meet B5 | **one-accent** |
| invoice MS:005 | header | split / plain-left | the right-hand meta starts about 3 title line-heights below the "INVOICE" baseline (more than 1), so not split | **plain-left** |
| invoice MS:006 | header | split / ruled | purple top bar is 21 px of 518 (4.1% of H), full width, directly above the header block, no text between. Ruled comes before split | **ruled** |
| invoice MS:006 | colour | — | bars are 21 px ≥ 20 px (5% of the 400 px short side), so they are blocks. Purple + lavender fills 11.3% + black wedges ≥ 10% | **fill-blocks** |
| invoice GH:030 | colour | one-accent / mono | the chromatic pixel share of 0.9% is spread over 3 hue bins: that's anti-alias fringe (B2). The single blue "View in browser" link fails B5 | **mono** |
| invoice GH:075 | colour | multi / one-accent | the multicolour logo is excluded; the blue company name + blue signature line are 2 elements in one cluster | **one-accent** |
| letter LOL:011 | colour, header | — | one blue "@" link, 45 px, fails B5. Sender name is right-aligned with no rule | **mono; plain-left** (`align=right`) |
| letter LOL:022 | colour | — | footer panel L 0.91 fails B1e; the single vertical blue rule fails B5; "CompanyLogo" excluded | **mono** |
| letter LOL:007 | colour | — | teal highlight on placeholder fields is editor shading (B1d) | **mono** |
| cover-letter MSC:006 | colour, header | — | right panel (H 206°, L 0.95) is a tint, so not a fill. Navy headings (hue 190–215°) across ≥ 6 elements form one cluster. The rule under the role line spans about 55% of page width, under 80%, so not ruled | **one-accent; plain-left** |
| cover-letter MSC:007 | colour | — | geometric fills cover 6.6% (under 10%). Yellow (~45°), green (~90°) and teal (~190°) are 3 clusters | **multi** |
| cover-letter MSC:002 | colour, header | — | the full-page dark grey (L 0.16, S 0) is the background (B1a), so not a fill, and not a band (d fails) | **mono; plain-left** |

---

## D. Recode, re-test and consequences

1. **Recode.** For each family with a coded table (invoice, cover-letter, letter, brochure, flyer,
   poster, report-ARC, memo and form where coded), one **fresh worker per family** recodes ONLY
   `header treatment` and `colour use` (form: colour only) for all coded items, using this file.
   - It records `header-note` and `colour-note`, and keeps the old values in `(r1)` columns.
   - Admissibility and every other feature are untouched.
   - The worker must not have coded that family before.
   - Invoice additionally excludes its round-1 first and second coders.
2. **Items csv.** The orchestrator makes sure `<family>-items.csv` exists (C11) before re-test.
3. **Re-test.** A **fresh, independent second coder** per family reads only:
   - the items csv;
   - §4–§5;
   - the 82a clarification files;
   - this file.

   Sample:
   `random.Random("82a:<family>").sample(ids, max(min(10, len(ids)), math.ceil(0.25 * len(ids))))`.

   Any item named in §C that falls in a sample is also reported in a **sensitivity run excluding
   it** (C12). The gate uses the full sample.
4. **Gate.** A ≥ 0.80 per feature.
5. **Second failure.**
   - A failing feature is **dropped from that family's identity**, and the archetype becomes the
     remaining features. This is disclosed in the family's evidence file (§7).
   - If **both** header and colour fail again, the family ships **no ranked archetypes**: L3/L4
     and seeds only, with a Shortfall section, as in 82a-deck §6.
6. **Families not yet coded** (quote, proposal, whitepaper, infographic, one-pager, and report
   beyond ARC) code with this file from the start. The ordinary §7 gate applies.
7. **Failed variants.** Invoice's failed variants (`density`, `table rules`) stay dropped from
   filling per §7. They are not re-tested here.
