# Document Design Domain Knowledge — CV, Decks, Print, Reports

Scope note: unlike the other research files in this set, this one is not an analysis of
the upstream `ui-ux-pro-max` repo. Per the assignment, this is domain expertise sourced
independently — the rules our skill needs to actually encode and check. I did not need
the upstream repo to produce it, so sections 2/3 are thin; the weight is in 1 and 4, as
instructed.

Every rule below is tagged **[FACT]** (established, checkable, largely vendor/tool
behavior or physical/production constraint) or **[CONVENTION]** (widely followed
practice / house style, not a law of physics or a documented parser behavior). Where a
number exists it is stated as a THRESHOLD. This is written so a model can be held to it —
not design-blog prose.

---

## 1. Findings

### A. CV / Résumé

**ATS parsing constraints — what mechanically breaks extraction**

- **No multi-column body layout.** [FACT] Most ATS text extractors (built on PDF text-stream
  order or DOCX XML document order, not visual/spatial position) read content in the order
  it appears in the underlying file, not the order a human eye scans a rendered column
  layout. A two-column resume (e.g., skills sidebar + experience main column) gets its
  lines interleaved mid-sentence on extraction. THRESHOLD: zero column breaks in any body
  section. WHY: this is the single most commonly cited cause of a resume being read as
  garbled text by an ATS and auto-rejected or mis-parsed into wrong fields.
- **No tables for content that must be parsed.** [FACT] Table cell content is frequently
  extracted out of reading order, or dropped, by extractors not built to walk table
  structure. THRESHOLD: no tables for skills matrices, experience blocks, or any field
  that maps to a structured ATS field (title, dates, company). A simple 2-cell header
  table for name/contact is lower-risk but still avoidable.
- **No content in headers/footers.** [FACT] Many extraction pipelines parse only the body
  stream and skip Word/PDF header and footer regions entirely. Contact info (phone, email)
  placed in a document header can be invisible to those parsers. THRESHOLD: name, phone,
  email, location must appear in the first block of body content, never only in a
  header/footer.
- **No text boxes.** [FACT] Text inside a DOCX text box or a PDF floating text frame is
  often not linearized into the main content stream, or its position in the extracted
  text order is undefined. THRESHOLD: zero text boxes for any content that must remain
  searchable/parseable.
- **No information encoded only in graphics/icons.** [FACT] Text parsers read characters,
  not pixels. A phone icon with no adjacent "Phone:" label, or a skill-level rendered only
  as filled dots/bars, conveys nothing to the ATS. RULE: every piece of information must
  have a plain-text equivalent in the reading stream.
- **Use canonical section headings.** [CONVENTION, but functionally load-bearing] Parsers
  commonly match section headings against a dictionary of expected strings ("Experience",
  "Work Experience", "Employment History", "Education", "Skills", "Certifications").
  Creative headings ("My Journey", "What I Bring to the Table") won't map to the expected
  schema field and that section's content may not be attributed correctly. RULE: use
  canonical headings; save creative framing for the summary/profile paragraph, not the
  heading text.
- **No symbol-font glyphs for bullets/decoration.** [FACT] Bullets or decorative glyphs
  rendered via a symbol font (e.g., Wingdings-style code-point remapping) extract as
  their underlying Unicode code point, not the visual glyph — this produces garbled
  characters in extracted text. RULE: use standard Unicode bullets (•, -, ▪) rendered in
  a normal text font.
- **Export as text-layer PDF or DOCX, never an image/scanned PDF.** [FACT] A PDF that is
  actually a rasterized image (e.g., exported from a design tool without a text layer, or
  a scan) has no extractable text at all without OCR. Verification test: if you cannot
  select and copy the body text out of the PDF, it will not parse. THRESHOLD: 100% of body
  text must be selectable.
- **Font choice is not itself a parsing risk** [FACT] — parsers read the underlying
  character codes, not glyph shapes — but non-standard fonts can cause layout reflow
  issues in DOCX viewers and are a secondary aesthetic risk, not a parsing one. Don't
  conflate "unusual font" with "breaks ATS"; the mechanical breakers are structural
  (columns/tables/text boxes/headers), not typographic.

**Section ordering** [CONVENTION, near-universal]
Contact block → Summary/Profile (2–4 lines, optional) → Experience (reverse-chronological)
→ Education → Skills → optional: Certifications / Projects / Publications. For
early-career candidates (≤2 years experience or new graduates), Education moves above
Experience. Reverse-chronological (not functional/skills-first) is the default expected
format by both recruiters and ATS date-parsing logic; functional resumes are frequently
flagged as evasive by recruiters and parse worse (dates aren't in a predictable per-entry
position).

**Length conventions by seniority and region** [CONVENTION, well established per region]
- **US:** 1 page for <10 years experience; 2 pages acceptable for 10+ years or
  senior/executive roles. No photo, no date of birth, no marital status — this is not
  merely stylistic, it exists to avoid triggering US anti-discrimination (EEOC) concerns
  for the hiring side, so including them is a mild negative signal, not neutral.
- **UK:** "CV," typically 2 pages regardless of seniority level. Photo not customary.
- **EU / Europass:** 2–3 pages, follows the structured Europass template sections; photo
  inclusion varies by country (common in Germany/Austria, decreasingly common in France);
  date of birth sometimes included, unlike US/UK norms.
- **Gulf / Middle East:** photo commonly expected; nationality, visa/residency status, and
  marital status are frequently included fields — a regional norm that directly
  contradicts US/UK practice, so region must gate which fields the skill suggests
  including, not a single universal template.

**What visually distinguishes a strong CV from a "template-looking" one** [CONVENTION,
but with mechanically-describable signals]
- Consistent alignment grid: all dates in one vertical column/tab-stop, not
  individually positioned per entry.
- Hierarchy carried by weight/size (2–3 levels max: name, section head, body), not by
  color blocks or icon rows — heavy color panels and stock iconography are the strongest
  visual tell of an unmodified free template ("Canva-look").
- Consistent bullet punctuation and verb-tense parallelism across all entries (this is a
  content-craft rule, not a layout rule, but it reads as "polish" the same way alignment
  does).

### B. Presentation decks

**Slide typography minimums** [CONVENTION with widely-cited numeric floors, e.g. Duarte /
Garr Reynolds "Presentation Zen"]
- Body/bullet text: 24pt floor for anything viewed via projection at room distance;
  absolute minimum 18pt for dense data callouts, never below that. Title text: 36–44pt.
  WHY: legibility falls off a cliff below these sizes at typical
  room-to-screen viewing distances (rule of thumb: viewing distance in feet ÷ 8 ≈ minimum
  usable point size at the back row).
- For screen-only decks (webinar/shared-screen, no projection, no back-row viewer), an
  18–20pt floor is acceptable since viewing distance is a monitor, not a room.
- **6×6 heuristic** [CONVENTION, frequently debated but a useful mechanical ceiling]: max
  6 bullets per slide, max ~6 words per bullet, as a density ceiling rather than a hard
  rule. A slide needing >~40 words of body text is a signal to split into two slides or
  move detail to a handout/appendix.

**16:9 vs 4:3** [FACT re: current default] 16:9 (1920×1080 export) is the default for any
modern screen or projector; 4:3 is legacy-hardware-only. Default to 16:9 unless the
venue's projector is confirmed 4:3.

**Contrast under projector washout** [CONVENTION, physically grounded] Projectors have a
materially worse black level than an emissive display, and ambient room light further
lifts perceived black — net effect is that on-screen contrast ratios read lower once
projected than the same values would on a monitor. WCAG's 4.5:1 screen-reading minimum is
not sufficient margin for projection. RULE: for anything that will be projected, use
near-maximum contrast pairs (pure/near-white text on a saturated dark background, or
near-black text on white) rather than mid-gray-on-dark or subtle off-white-on-white
combinations that would pass a screen contrast checker but wash out under a projector.

**Chart vs table** [CONVENTION with a checkable line-count threshold]
Use a chart when the message is a trend, comparison, or relationship — the shape of the
data is the point. Use a table when the audience needs to read exact individual values
(e.g., a pricing grid). THRESHOLD: a line chart with more than ~5–7 series becomes a
"spaghetti chart" and stops communicating — past that count, either facet into small
multiples or switch to a table/summary stat.

**Speaker notes convention** [CONVENTION] Full sentences / talking points live in the
notes field, not duplicated on the visible slide; typical density is 3–5 sentences per
slide. Notes are never a copy of the slide's bullet text.

**PPTX-specific failure modes** [FACT — this is the highest-value mechanical content in
this section]
- **Font embedding is opt-in, not automatic.** PowerPoint only embeds fonts in the file
  if the author explicitly enables "Embed fonts in the file" (File → Options → Save)
  *and* the specific font's embedding permission bit (set by the font's license/foundry)
  allows it. Many commercial/licensed fonts disallow embedding outright — the option can
  be on and the font still won't embed, with no obvious warning.
- **Silent substitution is the actual failure mode users experience.** If a font isn't
  embedded and isn't installed on the machine opening the file, PowerPoint silently
  substitutes the nearest installed font. This commonly reflows text, changes line
  breaks, and can overflow text boxes that were sized for the original font's metrics —
  this is the mechanism behind "my deck looked broken on the client's projector."
- **Safe font stack** [CONVENTION, based on default OS/Office font availability]: Arial /
  Calibri / Times New Roman ship on effectively all Windows installs; Helvetica on Mac.
  For a deck that must not rely on embedding, pairing Calibri (or Arial) for both heading
  and body is the lowest-risk cross-platform choice. Anything outside the default Office
  font set should either be embedded (license permitting) or avoided.

### C. Brochures / flyers / posters — print production

This section is intentionally the thinnest of the five per the brief — print production
is a narrower, more mechanical domain than the others and has fewer decision points, not
because it matters less.

- **Bleed:** [FACT, industry-standard] minimum 0.125in (3mm) beyond the trim edge on
  every side for any full-bleed design; some commercial printers require 5mm. WHY:
  accommodates cutting-blade tolerance — without bleed, any trim misalignment reveals a
  thin white edge.
- **Safe margin:** [FACT/CONVENTION hybrid, standard print-shop practice] keep all
  critical text/logos at least 0.125–0.25in (3–6mm) inside the trim line, distinct from
  bleed. WHY: same trim-tolerance risk, opposite direction — protects content from being
  clipped.
- **Artboard size = trim size + bleed on all sides.** [FACT] e.g. a US Letter flyer with
  8.5×11in trim and 0.125in bleed needs an 8.75×11.25in artboard.
- **CMYK vs RGB conversion surprises:** [FACT] CMYK (offset/digital process print) has a
  smaller gamut than RGB; saturated RGB blues, greens, and neons visibly dull/shift on
  conversion. RULE: design and proof in CMYK from the start for anything print-bound;
  converting only at export time produces unpredictable last-minute color shifts.
- **Minimum resolution:** [CONVENTION, industry-standard] 300 DPI at final print size for
  raster images; vector for text/logos wherever possible (resolution-independent). 150
  DPI is an acceptable floor only for large-format pieces (posters/banners) viewed from
  3ft+ away, since viewing distance reduces the eye's effective resolving power.
- **Spot vs process color:** [FACT] spot color (e.g., Pantone/PMS) is a single
  premixed ink giving exact, consistent color — used for brand-critical colors or
  metallics/fluorescents CMYK can't reproduce. Each spot color is a separate press
  plate/cost. Process (CMYK) is the 4-ink mix used for photographic/full-color content.
- **Tri-fold fold geometry:** [FACT] the panel that folds innermost must be narrower
  (~1/8in / 3mm) than the other two so it tucks without binding — a tri-fold is NOT three
  equal panels. For an 11in-wide letter tri-fold: roughly two panels at ~3.7–3.75in and
  one tucking panel at ~3.5–3.58in.
- **Gate-fold:** [FACT] the two outer panels that meet at center must each be very
  slightly narrower than an exact half-split of the remaining spread (~1/16–1/8in
  narrower each) so they don't collide when closed.
- **Paper stock:** [CONVENTION, print-industry practice] coated stock (gloss/matte) holds
  color saturation and fine detail/small type better than uncoated, which absorbs more
  ink and mutes color; heavier cover-weight stock (100lb+) for standalone/handled pieces
  (posters), text-weight (70–100lb) for foldable multi-panel pieces that need to crease
  cleanly without cracking.

### D. Long-form reports / whitepapers

- **Measure (line length):** [FACT, classic typographic convention — Bringhurst,
  *The Elements of Typographic Style*] optimal 45–75 characters per line including
  spaces; ~66 CPL cited as ideal. THRESHOLD: 45–75 CPL acceptable range. WHY: below 45 the
  eye's return-sweep happens too often and breaks reading rhythm; above 75 the eye loses
  its place on the return sweep.
- **Leading:** [CONVENTION, Bringhurst's rule of thumb] body leading conventionally
  120–145% of type size (10pt type → 12–14.5pt leading), increasing with line length
  since a longer measure needs more vertical separation to help the eye track back to the
  correct next line.
- **Hierarchy depth:** [CONVENTION] cap reader-facing heading depth at H1–H3. Beyond
  three levels, headings become visually indistinguishable and hard for a reader to hold
  in working memory — restructure into appendices/sub-documents instead of adding H4/H5.
- **Running heads:** [CONVENTION, publishing-standard] verso (left/even) page carries
  document/chapter title, recto (right/odd) page carries current section heading; page
  number sits outside the running head, in the outer margin or footer center.
- **Pagination:** [CONVENTION, publishing-standard] front matter (title page, TOC,
  executive summary) numbered in lowercase roman numerals (i, ii, iii); body restarts at
  Arabic 1 from the first page of the main content.
- **Table design:** [CONVENTION with mechanically-checkable components] minimize vertical
  rules; use horizontal rules sparingly (header rule + total/bottom rule — avoid a rule
  per row, "prison bars," per Tufte's data-ink-minimization principle); right-align
  numeric columns, left-align text columns. **Mechanically checkable requirement:** any
  column of numbers must use tabular (fixed-width per digit) figures, not proportional,
  so digits align vertically — this is a font-feature-level check (OpenType `tnum`
  feature availability, or use of a monospaced-digit font).
- **Figure captioning:** [CONVENTION, near-universal — e.g. Chicago Manual of Style]
  caption below the figure, caption above the table; captions carry a sequential number
  ("Figure 3", "Table 2") per chapter or per document for cross-referencing.
- **Cross-references:** [CONVENTION, functionally load-bearing] refer to figures/tables/
  sections by their assigned number, never by relative position ("see figure below") —
  position-relative references break the instant pagination reflows.
- **TOC conventions:** [CONVENTION] include down to H2 (occasionally H3), not every
  subheading; page numbers right-aligned, with or without leader dots depending on house
  style; TOC page itself sits in the roman-numeral front matter, not counted in body
  pagination.

### E. Cross-cutting

- **Accessible contrast for print is not WCAG.** [FACT] WCAG 2.x contrast ratios (4.5:1
  body text, 3:1 large text) are defined for self-luminous, additive-light sRGB displays
  and do not have a direct, standardized equivalent for reflective, subtractive CMYK
  print. There is no universally standardized print-contrast-ratio metric. Practical
  substitute [CONVENTION, not a formal standard]: target at least ~40–50 L* units of
  difference (CIE Lab lightness) between text and background as a print-legibility floor,
  and always proof under the expected viewing light — press ink density does not
  reproduce a calibrated monitor's rendering of the same color values.
- **Typeface pairing:** [CONVENTION] pair typefaces with contrast in category (serif
  heading + sans body, or vice versa) rather than two faces from the same category that
  look almost-but-not-quite alike (the classic subtle-mismatch mistake). Alternatively,
  use a single superfamily with matched serif/sans/mono cuts for guaranteed harmony. Cap
  any one document at 2 type families (heading + body), 3 max including a monospace for
  code/data.
- **Numeral styles:** [FACT re: definitions, CONVENTION re: usage rules] lining figures
  (uniform cap-height digits) vs oldstyle figures (varying heights/descenders, blend into
  lowercase text). Oldstyle is the traditionally correct choice for numerals inline
  within body prose; lining is correct for headers, tables, and anywhere digits must look
  uniform/scannable. **Tabular vs proportional** is the mechanically-checkable half of
  this: tabular figures are fixed-width per digit and are REQUIRED for any column of
  numbers that must align vertically (financial tables, statistics); proportional figures
  vary width like normal letters and belong in running prose.
- **When serif beats sans in body text:** [CONVENTION, contested] serif remains the
  traditional default for long-form print (books, reports, whitepapers); the classical
  argument (serifs aid horizontal eye-tracking) is contested by modern legibility research
  showing minimal-to-none measurable difference between well-designed serif and sans
  faces at normal reading sizes. The more defensible framing: serif body text signals
  "formal report / scholarly / book," sans-serif signals "modern / tech / informal" — a
  genre-convention choice, not a legibility mandate. Screen-native documents lean sans
  partly for historical technical reasons (low-res screens rendered serif hairlines
  poorly), a constraint mostly obsolete at modern screen resolutions but the convention
  persists.

---

## 2. Transferable

Thin by design — this file isn't analyzing the upstream repo's mechanism, but two
patterns from the brief's description of that repo are directly applicable to this
domain knowledge:

- The **generate-then-inherit loop** (brand identity generated once, all downstream
  artifacts inherit it) maps cleanly onto documents: a CV, deck, and report for the same
  person/company should inherit one resolved typeface pairing, color pair, and region
  setting rather than each being decided independently.
- Encoding rules as **checkable data (CSV-style rule tables)** rather than prose, per the
  brief's description of `data/*.csv` in the upstream repo, is the right target shape for
  the mechanical rules above (ATS breakers, font-embedding checks, bleed/DPI presets,
  CPL/leading ranges) — they are naturally tabular (rule, threshold, applies-to, source
  type).

## 3. Breaks

Also thin, for the same reason as §2 — I have no upstream mechanism to evaluate against.
One domain-specific break worth flagging: **rules bifurcate hard on output format**, and
this is the one place this file intersects the brief's open question:

- If output is native DOCX/PPTX: the ATS column/table/text-box traps (§A) and the PPTX
  font-embedding failure mode (§B) are the dominant risks, and both require inspecting
  the actual file structure (XML/OOXML), not just the visual result.
- If output is HTML → PDF: the PPTX font-embedding problem *mostly disappears* — a
  correctly generated PDF embeds all fonts by default as part of standard PDF export, so
  "looks broken on another machine" stops being a font issue. But a new problem appears:
  most HTML→PDF pipelines (headless Chrome, wkhtmltopdf, etc.) render in RGB and do not
  natively support CMYK conversion or bleed/trim marks, which breaks the entire §C print
  production section unless the pipeline specifically supports a CMYK-aware print export
  path. **This does not survive the move to an HTML/PDF pipeline without extra tooling.**

## 4. Gaps

This is where the actual build list lives — none of this exists yet and all of it would
need to be built for the rules in §1 to be enforceable rather than advisory text:

- **A DOCX/PPTX structural linter.** Something that opens the OOXML and mechanically
  flags: multi-column body sections, tables in ATS-sensitive zones, text boxes containing
  body content, content placed only in header/footer XML parts, symbol-font glyph usage,
  and (for PPTX) whether font embedding is on and whether referenced fonts are actually
  embedded in the package. This is pure structure-checking, no visual rendering needed —
  cheap to build, high value, directly matches "mechanically checkable" priority from the
  task brief.
- **A canonical section-heading dictionary** (per §A) — the accepted-heading list ATS
  systems are known to key on, so the skill can flag/rewrite non-canonical headings.
- **A region/seniority ruleset as data**, not prose: length ceiling, photo
  yes/no, DOB/marital-status inclusion, section order, keyed by region (US/UK/EU/Gulf)
  and seniority band — this is what lets the skill ask "which region/seniority" once and
  derive every downstream constraint instead of re-deciding per document.
- **A safe-font-stack table** cross-referencing platform (Win/Mac), default Office/Google
  Workspace availability, and embedding-license status — needed to actually answer "will
  this font survive being opened on someone else's machine" per document type.
- **Print production presets as data**: bleed/margin/DPI/color-mode defaults keyed by
  output type (flyer, poster, tri-fold, gate-fold, business card), so the skill doesn't
  re-derive bleed math from prose each time.
- **A CPL/leading calculator** — given a font, point size, and column width, compute
  actual characters-per-line and flag out-of-range (45–75 CPL) — this is a small,
  fully mechanical function, not a rule needing model judgment at all.
- **A tabular-figure / OpenType-feature checker** for numeric table columns (§D, §E) —
  checks whether the font in use has a `tnum` feature and whether it's engaged, or
  whether a monospaced-digit fallback is needed.
- **A print-safe contrast estimator** (§E) — nothing here currently exists that computes
  CIE Lab L* delta between two colors as a print-legibility proxy; this would need to be
  built from scratch since it's explicitly not the same computation as a WCAG screen
  contrast checker.
- **Nothing here addresses image-only/scanned-PDF detection** for CV parsing-safety — a
  "can this PDF's text be selected" check is trivial to build (attempt text extraction,
  check non-empty) but doesn't exist yet either.

## 5. Open questions

- **Which output format is actually in scope — native DOCX/PPTX, or HTML→PDF?** This is
  the single biggest fork for this domain, flagged in the brief as unresolved. It
  determines whether the PPTX font-embedding failure mode (§B) and the DOCX structural
  traps (§A) are even reachable problems, versus whether print-color/bleed handling in a
  browser-print pipeline (§C, §3) becomes the dominant risk instead. Would be settled by
  the same evidence the brief asks all researchers to gather: does the target Claude Skill
  environment support generating/inspecting real OOXML binaries, or only HTML/CSS/PDF?
- **Current, vendor-specific ATS parser behavior is not something I can verify without
  live testing.** The column/table/text-box/header rules in §A are widely reported and
  consistent across resume-writing literature and parser-vendor documentation I'm aware
  of, but exact behavior differs by vendor (Workday, iCIMS, Taleo, Greenhouse, Lever) and
  changes over time as vendors improve extraction. I'm treating these as conservative
  "safe under any parser" rules rather than claiming precise behavior for a named current
  vendor version. Settling this with certainty would require either vendor documentation
  access or empirical round-trip testing (generate a resume, submit it through a real
  ATS, inspect what was extracted) — out of scope for a research pass.
- **Office/Google Workspace default font sets drift over time** (e.g., Microsoft has been
  rotating Calibri's default-font status in newer Office versions) — the "safe font
  stack" in §B should be treated as directionally correct, not a frozen fact, and revisited
  close to build time rather than hardcoded from this research pass.
