# 90 — R6 review: brand-kit builder guide, law-firm example, brand.md pipeline

Reviewer: Opus Reviewer (adversarial). Date: 2026-09-24. Read-only; this file is the only
output.

**Scope:**
- `references/brand-kit-builder.md`
- `examples/generic-law-firm-brand.md`
- README "Your own brand"
- `portable/AGENTS.md` step 7
- the `make_brand_kit.py` brand.md grammar and derivations
- `merge_brand_kit.py`

**Goal tested:** "a grand library a smart AI can be instructed to use to build a brand kit…
top designs mixed in good manners according to modern best standards."

**Method: the guide followed cold, twice, end to end.** Both briefs were built, merged into a
temp copy, and resolved plus handed off (docx and pptx) for 2 doctypes each. All temp outputs
were removed afterwards.

- **B1, children's charity "little-steps".** Brief: existing logo orange `#F28C28`, bilingual
  EN/FR, letter + flyer + report.
  - Palette: `lib-govuk-ink` roles with the orange as accent.
  - Typeface: `lib-nunito-nunito-sans` (top hit for "warm friendly approachable rounded").
  - Scale: `print: lib-major-third-print`.
  - Designs: letter-formal, flyer-print-marketing, report-classic.
- **B2, fintech "ledgerline".** Brief: no colours; deck + invoice + one-pager.
  - Palette: `lib-material3-purple`, the rank-1 authority hit for "modern trustworthy confident
    fintech technology", copied whole.
  - Typeface: `lib-inter`.
  - Scales: print major-third, projection minor-third.
  - Designs: deck-generic, invoice-tabular, one-pager-restrained.

**Verdict.** The pipeline is sound as plumbing:
- the brand.md grammar is strict with line-numbered errors;
- dry-run → build → merge → `check` → resolve → handoff all worked first time for both briefs;
- On-colours are derived; a failing brand colour is correctly demoted to fill-only; ≤ 2
  families holds; scales are per medium.

It does **not yet deliver the goal**:
- (a) The data offers no "top designs" to mix: every family used here has exactly one
  `convention` design (F1).
- (b) The failing brand colour, correctly marked fill-only in the data, is invisible to both
  the user and the renderer (F2, F3).
- (c) Several derivations degrade the library rows they copy (F4, F5).
- (d) The guide has contradictions and taste steps a cold AI cannot resolve from data (F7–F10).
- (e) A bilingual brand is unreachable in its second language (F6).

Severity: **H** = the built kit produces a document that breaks the library's own rules, or
the goal is not met; **M** = wrong or ambiguous guidance, or silent degradation; **L** = polish.

---

### F1 (H) — There are no ranked designs to choose from

In both briefs, `ddi.py designs --doctype <k> --query …` printed exactly one design per family,
each `convention` class:
- letter-formal, flyer-print-marketing, report-classic;
- deck-generic, invoice-tabular, one-pager-restrained ("rank 1 of 1, convention").

Guide step 5 ("take the rank-1 design unless a lower one's Best For matches the tone; prefer
authority/ranked/juried") is therefore vacuous outside `cv`. The goal's "top designs mixed" is
not met until Phase 4 ships the ranked lists.

**Fix:**
- Nothing to fix in the guide.
- Gate the goal claim in the README on Phase 4.
- Have the guide say so to the user when a family has only a convention design. It already
  asks for this; make it mandatory in the handoff to the user.

### F2 (H) — A brand colour that fails contrast is demoted silently, and the report never shows the failing pair

For B1, `#F28C28` on `#ffffff` is **2.45:1** (on muted, 2.30:1). The kit correctly writes
`Fill-Only Roles: accent`, `Text-Safe Roles: primary;secondary`. But the dry-run contrast report
prints only On-colour pairs and Foreground/Background:

```
On Accent/Accent: #000000 on #F28C28 = 8.56:1 [OK, threshold 4.5:1]
Foreground/Background: #0b0c0c on #ffffff = 19.59:1 [OK ...]
DRY-RUN OK
```

**Accent/Background is never printed**, and no line says "accent demoted to fill-only". The
guide's instruction ("treat any FAIL as a stop") can never fire for the one pair that matters.
It also contradicts the correct behaviour: a logo colour must be **kept** as a fill, not changed.

**Fix:**
- Print `Accent/Background` and `Secondary/Background` pairs.
- Print an explicit `NOTE accent #F28C28 = 2.45:1 on background -> fill-only (never set text in
  it); non-text contrast 2.45 < 3:1 (WCAG 1.4.11), so avoid it for thin rules/icons too`.
- Rewrite guide step 2: "a brand colour below 4.5:1 is kept as a fill-only accent. Only change
  it if the user wants text in brand colour; then offer the nearest library accent in the same
  45° hue bin that passes."

### F3 (H) — The handoff tells the renderer nothing about fill-only roles

For both B1 handoffs (flyer docx/pptx, report docx/pptx), the palette block is just:

```
Primary: #0b0c0c  Secondary: #484949  Accent: #F28C28  Background: #ffffff  Foreground: #0b0c0c
```

There is no `Text-Safe Roles` or `Fill-Only Roles`. A renderer, or Claude, will naturally set
headings or links in the accent, which fails `low-contrast-text` (Severity **fail** for the flyer
design) and the 4.5:1 floor. The data knows; the handoff drops it.

**Fix:** print `text-safe: primary, secondary, foreground` and `fill-only: accent (2.45:1)` in
every handoff palette block, for docx, pptx, pdf and png alike. This is the same gap noted in R3
F3 for the portable pack.

### F4 (M) — The derived Rule Hair uses Muted, so hairlines become invisible

`make_brand_kit.py:715` sets `"Rule Hair": p["muted"]`. With a library neutral, muted is a
near-white fill colour:
- B1 and the **law-firm example**: Rule Hair `#f4f8fb` on white = **1.07:1**, used for letter
  and report hairlines (Rule Hair pt 0.5).
- The source palette row `lib-govuk-ink` has its own `Rule Hair #cecece`, which the kit throws
  away.

**Fix:** when the palette roles were copied from a library row, copy that row's Rule
Hair/Strong/Brand. Otherwise, derive Rule Hair as the first grey ≥ 3:1 against background (WCAG
1.4.11 non-text).

### F5 (M) — Other derivations lose library information

- **Text-Safe Roles omits `foreground`.** It is computed only over {primary, secondary, accent};
  base palettes list `foreground;primary;secondary;accent`. Add foreground (it's the body text
  colour).
- **Rule Brand = primary, never accent.** The law-firm example's Voice says "Accent red only for
  the firm name rule", but the data puts black there. Either derive Rule Brand = accent when
  accent ≥ 3:1 on background, or drop that sentence from the example.
- **Invoice loses the `legal` role.** The base `form-print` scale has `legal 8.5pt`; the brand
  `print` scale (a `lib-*-print` row) has caption/label but no legal. Invoice/quote fine print
  then has no size. Fix: map legal → caption, or add legal to `lib-*-print`.
- **Material/Radix palettes carry tinted "surface" backgrounds** (B2 `#fef7ff`). The brand
  background becomes the page colour of printed invoices and one-pagers: a lavender page on
  office printers, with a white unprintable margin. The library palettes have no medium tag.
  Fix: the guide should say "print doctypes use `#FFFFFF` background unless the user insists";
  or the kit should emit a print variant with white background.

### F6 (H for bilingual briefs) — A bilingual brand cannot be reached in its second language

Brand doctype Keywords are derived as `<doc_key tokens>, <slug>`. B1's report row has
`Keywords: report-short, report short, little-steps`. The base doctype's multilingual keywords
("rapport", "Bericht", …) are dropped.

```
resolve --brand little-steps --query "fais-moi un rapport"   -> [NO BRAND ROW] … refusing to emit
resolve --brand little-steps --query "a report for our donors in French" -> little-steps-report-short, language en
```

The interview asks for languages (step 1.4), but `brand.md` has no field for them. The guide
never says French headings need `--lang fr`, and verification (step 6) uses only `--doctype`,
which hides the problem.

**Fix:**
- Copy the base doctype's Keywords into the brand row (plus the slug).
- Add a `languages: en, fr` top-level key that sets the brand doctypes' Default Language, or
  emits one row per language.
- Add a `--query` in the user's second language to step 6's verification.

### F7 (M) — The guide contradicts itself on type-scale ratio

Step 4: "tighter for dense documents, **wider for slides**". The guide's own example lines, and
the law-firm example, use `projection: lib-minor-third-projection` (ratio **1.2**, the tightest)
and `print: lib-major-third-print` (1.25). That is the opposite. A cold AI cannot tell which to
follow, and "tighter/wider" is taste.

**Fix:** state a data rule, for example:
- print = the pairing's own `Scale Key` medium row if it exists, else `lib-major-third-print`;
- projection = `lib-perfect-fourth-projection`: its h1 57 pt clears the 36 pt `proj-title-floor`
  with margin; the minor third's 41.5 pt does too, but with a smaller ratio.

Then fix the example to match.

### F8 (M) — Selection steps are not deterministic

- **Palette** (step 2): "`--query "<tone words + industry>"`, prefer authority". The tone words
  are the AI's own. Which of the top 5 to take on a tie is unspecified. In B2 the rule yields
  Material baseline **purple** `#6750A4` for a fintech: authority-backed, but the stereotypical
  AI-generated look the slop research warns about.
- **"If the brand colour is dark, it may be primary instead"**: "dark" is undefined.
- **"Neutral library palette whose tone fits"**: `library palettes --query "neutral"` returns
  COLOURlovers rows named "…neutral", not the guide's own examples (`print-neutral`,
  `lib-govuk-ink`, `lib-uswds-navy`).

**Fix:**
- Rule: take the highest-scoring row whose evidence is authority/ranked. On ties, prefer the
  palette whose accent hue bin matches the user's stated industry colour, if any, else the
  lowest key.
- Define dark as L < 0.35 (then it becomes primary, and the accent comes from the neutral).
- Add `--query neutral` aliases, or tag neutrals with `neutral` in Keywords.

### F9 (M) — The CLI cannot show a full palette row

Guide step 2 says to copy all six roles from one palette. `library palettes` (text and `--json`)
shows only `Primary / Accent / Background` (`key_values`). A cold AI must open
`data/base/palettes.csv` to get Secondary, Foreground and Muted. The guide doesn't say so.

**Fix:** have `library palettes` print all six roles plus Text-Safe/Fill-Only, or add
`--key <palette_key>` to dump the row.

### F10 (M) — The brand's fonts vanish in Word, and some handoffs name no font

- B1 report, docx: `python-docx (safe-stack): headings Arial / body Arial`. Nunito and Nunito
  Sans never reach Word, which is correct per the docx safe-stack rule but silent. The user
  believes they have a Nunito brand.
- B1 flyer docx and B2 invoice docx: `fonts: (not present in this resolution)`. Those doctypes
  have no docx render target, so a Word flyer or invoice gets **no font instruction at all**.
- B2 deck: `python-pptx (embed): Inter / Inter`, while `pptx-font-embedded` is a **fail**
  constraint that python-pptx cannot satisfy (R3 finding, still open).

**Fix:**
- The guide should tell the user: "in Word your documents will use <fallback>; install
  <fonts> or accept the fallback."
- Handoff should print the brand family + fallback for every format, even without a matching
  render target.
- Resolve the pptx embedding contradiction (mark it warn, or document a manual embed step).

### F11 (M) — Medium-specific contrast is not checked for brand palettes

The kit gate checks 4.5:1 only. B2's deck accent `#6750A4` on `#fef7ff` = **6.12:1**. That
passes the gate but is below the library's own projection threshold (`proj-contrast-margin`
**7.0**). The deck will warn at preflight after the kit was declared OK.

**Fix:** for each brand doctype, check the palette against its constraint set's contrast
thresholds (projection 7:1; print-marketing 3:1 for display). Report per doctype in the dry-run.

### F12 (L) — Example and docs

- The law-firm example is 100% library rows. It builds (`DRY-RUN OK … typefaces=2 doctypes=5
  type-scales=9`) and inherits F4 (invisible hairline) and F7 (scale ratio contradiction).
- README's Acme sample uses accent `#9ACD32` on `#F7F8F5` (about 1.8:1, so fill-only). That's
  fine, but the README should say that is what happens.
- `portable/AGENTS.md` step 7 points no-code users to `references/brand-kit-builder.md "in the
  skill"`, a file they don't have. Inline the 6 rules instead.
- Guide step 6 verifies only with `--doctype`. Add `--query` checks (see F6).

**What works (verified):**
- brand.md grammar with line-numbered errors;
- On-colour derivation;
- fill-only demotion in data;
- ≤ 2 families (Inter = 1, Nunito pair = 2);
- per-medium typeface rows (`typefaces=2` for print + projection);
- `<slug>-<family>` doc-reasoning rows swapping palette/typeface while keeping the design's style;
- merge + `check` clean.

## Fix priority

1. F2 + F3: a failing brand colour must be visible to the user and the renderer.
2. F6: bilingual brands.
3. F4: invisible hairlines.
4. F10 + F11: fonts and contrast per format/medium.
5. F7–F9: make the guide deterministic from data.
6. F5, F12.
7. F1 resolves with Phase 4.
