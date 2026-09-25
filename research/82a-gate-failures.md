# research/82a-gate-failures — §7 gate failures: brochure, flyer, memo, form, deck r2, poster, invoice r2, infographic (DRAFT rulings)

**Status: DRAFT for orchestrator ratification.** Author: Design Researcher 2, 2026-09-25.

**Exposure:** none for brochure, flyer, memo, form, poster, invoice or infographic (never coded). **Exposed on deck:** I am the round-2 deck recoder (`deck-recode.md`), so §7 is marked for the orchestrator's independent check. Also exposed on report (L3 re-check), which is not in this file.

**Rules applied:**
- research/82 §7;
- 82a-clarifications-1 to -5 (C29: thresholds literal);
- 82a-general §A, §B, §C, §D;
- 82a-cv (ruled/split criteria and Addendum A, which 82a-general §A.2 incorporates);
- 82a-deck §4 and §6.4 (admissibility precedents).

**Inputs read:**
- `designs-evidence/{brochure,flyer,memo,form}-agreement.md`;
- `-recode-82ag.md` and `-second-coder.md` for each family;
- the exclusions logs in `flyer-corpus.md` (F.4) and `form-corpus.md` (colour caveat).

**Not done:** no git; no corpus file edited; nothing recoded. Every count below comes from a script over the agreement files' "Disagreements" tables (60 rows in total, all features). My diagnosis labels are my judgement and are marked as such.

Diagnosis codes used in the tables:
- **AMB-x**: rubric ambiguity (the written rule admits both readings).
- **ERR-R**: the recoder/first-coder side departed from the written rule.
- **ERR-S**: the second coder departed from the written rule.
- **MEAS**: measurement near a threshold, with no numbers recorded by at least one side.
- **OLD**: first coder applied a reading superseded by a later clarification.
- **SCOPE**: the two coders coded different objects.

---

## 0. Which failure is this? (history per feature)

§7 is per family:
- first failure → `82a-<family>` sharpens the failing rule, recode, fresh second sample;
- second failure → the feature is dropped from that family's identity.

82a-general §D adds a family-general layer:
- §D.1 names the families whose existing codes were **recoded** under it: invoice, cover-letter, letter, brochure, flyer, poster, report-ARC, memo and form "where coded".
- §D.5 calls failing the §D.3–§D.4 re-test a **"Second failure"**: the feature is dropped, and "if both header and colour fail again, the family ships no ranked archetypes".
- §D.6 says families **not yet coded** "code with this file from the start. The ordinary §7 gate applies" (i.e. a first failure).

The re-tests used seed `"82a:<family>"`, the seed §7 reserves for the re-test *after* a first failure. So the text treats the 82a-general re-test as the second test of header/colour for every family recoded under §D.1.

| Family | Feature | A_f | Coded under | Failure # (literal) | Basis |
|---|---|---|---|---|---|
| brochure | colour | 0.60 | recode under 82a-general (§D.1) | **second** | §D.5 |
| brochure | header | 0.40 | recode under 82a-general (§D.1) | **second** | §D.5 |
| flyer | colour | 0.30 | recode under 82a-general (§D.1) | **second** | §D.5 |
| flyer | header | 0.50 | recode under 82a-general (§D.1) | **second** | §D.5 |
| flyer | admissible | 0.40 | first coder, §5 (pre-C14/C20 readings) | **first** | §7; 82a-general does not cover admissibility |
| memo | header | 0.33 | coded fresh under 82a-general (M.6, after it landed; `memo-recode-82ag.md`: nothing was coded when the ruling was issued) | **first** | §D.6 |
| form | columns | 0.00 | first coder, §4 | **first** | not an 82a-general feature |
| form | heading | 0.50 | first coder, §4 | **first** | not an 82a-general feature |
| form | colour | 0.00 (**0.25 corrected**, §4.1) | recode under 82a-general (§D.1, "form where coded") | **second** (literal) | §D.5 |

Passing features, unaffected:
- brochure: panel count 0.90, heading 0.80, admissible 0.90;
- flyer: columns 0.90, heading 0.90;
- memo: columns 1.00, heading 0.89, colour 0.89, admissible 1.00;
- form: field style 1.00, admissible 1.00.

**Parser artifacts in the agreement files** (they don't change any verdict):
- brochure MSB:010 heading: coder 2's cell reads "plain-left title, sans" and coder 1's "sans". A real agreement, so heading = 0.90, not 0.80.
- form FMA:004 colour: coder 1's cell reads "one-accent, BORDERLINE" and coder 2's "one-accent". A real agreement, so colour = 0.25, not 0.00.

Recommend `agreement.py` strip parenthetical and after-comma notes before comparing.

---

## 1. Brochure

### 1.1 Disagreements on the failing features (script tally: colour 4, header 6)

| id | feature | coder 1 (recode) | coder 2 | diagnosis |
|---|---|---|---|---|
| MSB:003 | colour | fill-blocks | one-accent | **ERR-R.** The recoder's disclosed reading R2 counts a saturated majority panel (black, share 0.425) as a B3 fill. 82a-general B1a makes the most common grid class the background, excluded from every test. §C's own worked example contradicts R2 (cover-letter MSC:002: "the full-page dark grey … is the background (B1a), so not a fill") |
| MSB:008 | colour | fill-blocks | mono | **ERR-R** (R2; yellow is the most common class) |
| MSB:010 | colour | fill-blocks | mono | **ERR-R** (R2; navy is the most common class) |
| LOB:003 | colour | mono | multi | **AMB-B5.** Red/blue placeholder words: is each word one element (B4 "a text run in one colour (a word or line)"), giving ≥ 2 elements per hue, or is each hue one "run"? The recoder excluded them by area; coder 2 counted 3 clusters |
| MSB:001, 003, 005, 009 | header | plain-left | image-hero | **AMB-panel.** 82a-general §A.1 scopes brochure to the front panel ("every 'page width' below means panel width"), but C1's image-hero test says "≥ 30% of the PAGE area". The recoder measured photos against the whole spread (MSB:001 ≈ 16%, MSB:009 ≈ 26%); coder 2 measured against the front panel (> 30%) |
| MSB:007 | header | image-hero | ruled | **ERR-S.** The hiker photo fills the entire front panel (≈ 100% of the panel, ≈ 33% of the spread), so it is image-hero under **either** scope. Image-hero outranks ruled by strict priority (§A.2 step 1) |
| LOB:004 | header | plain-left | ruled | **MEAS.** Box edge / underline width against the 80% line; neither side recorded the width |

Causes (script tally over the 10 failing-feature disagreements):
- **colour:** 3 ERR-R, 1 AMB-B5;
- **header:** 4 AMB-panel, 1 ERR-S, 1 MEAS.

### 1.2 Literal §7 / §D.5 outcome
Header and colour are both second failures, so both are dropped. §D.5 then applies: **brochure ships no ranked archetypes** (L3 D&AD presence, L4 and seeds only, with a Shortfall section).

### 1.3 Draft ruling (recommended)

- **Header: DROP** (literal §D.5). The disagreement is mostly a genuine ambiguity (panel vs spread), which is exactly what a second failure is meant to remove. C34 below fixes the ambiguity for future brochure-like families; it does not rescue this test.
- **Colour: VOID the re-test and re-run it; do not drop.** The recode did not apply the written rule. It applied R2, a disclosed departure from B1a that is contradicted by 82a-general's own worked example (§C, MSC:002). A gate failure produced by a recode that substituted a different rule is not evidence that B1a is unreproducible.
  - Order a **fresh recode of colour only**, by a worker who has not coded brochure, applying B1a/B3 as written plus C33 below.
  - Order a **fresh second-coder sample** with seed `"82a-r2:brochure"`.
  - If colour then fails, it is dropped (this is its second valid test), and §D.5 applies.
- **Upper bound** (analysis, not a code): if the three ERR-R items were recoded to coder 2's values, colour agreement would be at most 9/10 = 0.90. Whether the fresh recode reaches that is for the re-test to show.
- **Consequence if both rulings are ratified:** brochure identity = `panel count | heading | colour` (header dropped, §7). If the colour re-run also fails → no ranked archetypes (§D.5).

**Alternative (strict) ruling, if the orchestrator does not accept voiding:** drop colour too, so brochure ships no ranked archetypes (as §1.2).

---

## 2. Flyer

### 2.1 Disagreements on the failing features (script tally: colour 7, header 5, admissible 6)

| id | feature | coder 1 (recode / first coder) | coder 2 | diagnosis |
|---|---|---|---|---|
| MSF:006, 007, 008, 009, 012, MSFP:010 | colour | fill-blocks | mono / multi / multi / one-accent / one-accent / mono | **ERR-R ×6.** The flyer recode applies the same R2 reading ("a saturated colour covering most of the page is a design fill, not the background"). In every one of these items the full-page colour (red, black, dark purple, blue, pink-purple gradient, sky blue) is the most common grid class, i.e. the B1a background. Coder 2 excluded it as B1a requires |
| MSF:010 | colour | one-accent | multi | **AMB-B5.** Is the gold frame line an element alongside the gold text runs; does the red "NOVEMBER" badge count? Element counting |
| MSF:006 | header | band | split | **AMB-texture.** A halftone stripe patch behind the name: is a texture patch a band "fill"? Its height was estimated at ≈ 40%, exactly the (d) ceiling (recoder flagged it low-confidence) |
| MSF:007 | header | plain-left | ruled | **AMB-bar.** Does a multicolour dot/dash pattern strip at the page edge count as the "full-width bar at the page edge" of §A.2 step 3? |
| MSF:010 | header | image-hero | ruled | **ERR-S.** A full-bleed photograph behind the title meets C1 (≈ 100% of the page, intersects the top 20%), and image-hero outranks ruled. Coder 2 coded MSFP:007 (also a full-bleed photo) image-hero, so the call is internally inconsistent |
| MSF:022 | header | plain-centered | ruled | **MEAS / ERR-R.** A gold hairline under the address line; the recoder did not test it (only the page frame); no width recorded |
| MSFP:010 | header | plain-centered | image-hero | **AMB-scene.** A full-page drawn scene (sky, sun, sheep, fence): one illustration (image-hero), or a flat sky fill plus separate clip-art (sun ≈ 10%)? The colour test already excludes it whole (B1b), so the header test should read it the same way (see C35) |
| MSF:007, 008 | admissible | no (A5; A3 + A5) | yes | **OLD.** The first coder's A5 on a continuous border pattern and on 3 *different* icons, and A3 on texture behind body text, predate C20 (A5 = identical discrete motifs only; continuous pattern bands excluded) |
| MSF:006 | admissible | no (A4) | yes | **OLD / AMB.** A4 on a halftone brush texture behind the title. Also **C29:** coder 2 sampled white body text on `#EB1818` at **4.49:1** and still admitted. Under C29's literal threshold, 4.49 < 4.5 is an **A6 fail** (thumbnail estimate, C9) → ERR-S on the A6 leg |
| MSF:009, 010, 012 | admissible | no (A3) | yes | **AMB-A3.** Text over a star pattern, a tinted photo, and a gradient behind short captions. C14 (covers) and 82a-deck §4 (slides) narrowed A3 to running text and ≥ 3-line blocks, but **no clarification extends that to flyer/poster/brochure**. The first coder read A3 strictly ("any text"), coder 2 read it the narrow way |

Causes (script tally over the 18 failing-feature disagreements):
- **colour:** 6 ERR-R, 1 AMB-B5;
- **header:** 3 AMB (texture, bar, scene), 1 ERR-S, 1 MEAS/ERR-R;
- **admissible:** 3 OLD, 3 AMB-A3.

### 2.2 Literal outcome
- Header and colour are second failures → dropped → §D.5 → **flyer ships no ranked archetypes**.
- Admissible is a first failure. Admissibility cannot be dropped (82a-deck §6.4 logic): it decides eligibility.

### 2.3 Draft ruling (recommended)
- **Header: DROP** (literal §D.5).
- **Colour: VOID and re-run**, for the same reason as brochure: 6 of 7 disagreements come from R2, not from B1a as written.
  - Fresh colour recode under B1a + C33 by a worker new to flyer.
  - Fresh second sample, seed `"82a-r2:flyer"`.
  - Upper bound if the 6 ERR-R items matched coder 2: 9/10 = 0.90.
- **Admissible (first failure):**
  - Ratify **C37** (A3/A5 scope for every family, below).
  - A fresh worker recodes **admissibility only** for all 20 flyer items under C37 + C20 + C29.
  - Fresh second sample, seed `"82a-r2:flyer"` (the same draw as colour).
  - If admissible fails again: per-item adjudication by a non-coder (82a-deck §6.4 precedent), citing rule id and measurement.
- **Resulting identity if ratified:** `columns | heading | colour` (header dropped). If the colour re-run fails → no ranked archetypes (§D.5).

**Alternative (strict):** drop colour as well → no ranked archetypes. The admissibility recode still runs, because it decides which seeds and L3 items may ship.

---

## 3. Memo

### 3.1 Disagreements on the failing feature (script tally: header 6)

| id | coder 1 | coder 2 | diagnosis |
|---|---|---|---|
| MSM:002 | ruled | plain-left | **AMB-boundary.** A full-width hairline (85% of page width, per M.6.2) sits between the TO/FROM block and the body label "COMMENTS:". Coder 1: the header block's closing rule → ruled. Coder 2: the rule "belongs to the boundary element" (82a-general §A.2 step 3, which generalises 82a-cv A2). §A.2 only exempts rules of a line-item table or a **section heading**; a single body label is not clearly either |
| MSM:004 | ruled | plain-left | **AMB-boundary** (same pattern: an orange double rule at the header/body boundary) |
| MSM:005 | ruled | plain-left | **AMB-title.** No "MEMO" or organisation title exists. Coder 1 took the largest non-logo text ("DATE") as the title and a mosaic bar at the page edge as ruled. Coder 2 found no title "distinct enough" and fell through. §A.1 already says "largest text in the top 30%", so the ambiguity is only whether a routing label qualifies |
| MSM:006 | plain-left | split | **MEAS.** Coder 1 measured the title centre at 39% of page width (not flush to a side, so split (a) fails). Coder 2 read "date left, title right" without numbers |
| OLM:009 | plain-left | split | **AMB-meta.** A SINTEF organisation contact block opposite the title. 82a-general split: "Meta = the header block's own contact or document-meta text". Memo's header block is defined as title + TO/FROM/CC/DATE/SUBJECT, so it is unclear whether an **organisation** address/contact block is "the header block's own contact" |
| OLM:010 | plain-left | split | **AMB-meta** (same; coder 1 also applied split (c) and found that the block ends above the title baseline) |

Causes (script tally): 2 AMB-boundary, 2 AMB-meta, 1 AMB-title, 1 MEAS. **No ERR.** Coder 1 recorded numbers; the ambiguities are real.

### 3.2 Literal outcome
**First failure** (§D.6: memo was coded fresh under 82a-general).
- The remedy is to sharpen the failing rule (**C36**), have the first coder (Design Researcher 3) recode header for the whole family, and run a fresh second-coder sample with seed `"82a-r2:memo"`.
- Do not drop yet.

### 3.3 Draft ruling
Ratify **C36**; recode header; re-test. If header fails again → dropped (second failure); memo identity becomes `columns | heading | colour`.

---

## 4. Form

### 4.1 Disagreements (script tally: columns 4, heading 2, colour 4, of which 1 is a parser artifact)

| id | feature | coder 1 | coder 2 | diagnosis |
|---|---|---|---|---|
| FMA:001-004 | columns | 1 | 2-sidebar | **SCOPE.** Coder 1 coded the **prescribed form specimen** (the field/pattern the authority prescribes). Coder 2 coded the **documentation web page** that shows it, whose left navigation / "On this page" aside became a sidebar |
| FMA:001 | heading | sans | serif | **SCOPE.** Coder 2 took the USWDS *site's* `<h1>` (Merriweather); coder 1 took the form text face |
| FMA:003 | heading | serif | sans | **SCOPE / source.** ABS page CSS (Open Sans) vs the diagram's own lettering |
| FMA:001, 002 | colour | mono | one-accent | **SCOPE + AMB-state.** Coder 2 counted the documentation site's **link colour** (`#005ea2`, `#1a65a6`). Coder 1 counted only the at-rest specimen and excluded the error-state red as a "state" (a disclosed extension of B1d, not a rule) |
| FMA:003 | colour | mono | one-accent | **SCOPE.** Coder 2 sampled the answer-box stroke (`#00A8E8`) in the page's embedded diagrams; coder 1 measured the page |
| FMA:004 | colour | one-accent, BORDERLINE | one-accent | **no disagreement** (parser artifact; C29 literal: S = 0.2000 is chromatic, and both coders applied it) |

Causes (script tally over 10 rows): 9 SCOPE-related, 1 parser artifact. The two coders were not coding the same object, so the gate compared two different populations.

Form has only **4 items, all L3 authorities** (presence only, no ranking; 82b A3 allows up to 5 distinct authority archetypes). The archetype code matters only for the **distinctness** test between authorities and for filling.

### 4.2 Literal outcome
- Columns and heading are first failures (not 82a-general features).
- Colour is a second failure by §D.1/§D.5, so literally it is dropped.
- With columns and heading still to re-test, dropping colour would leave form's identity as `columns | heading | field style`.

### 4.3 Draft ruling (recommended)
- **VOID all three form comparisons as SCOPE failures** (the coders coded different objects) and treat them as untested.
- Ratify **C38** (the unit of coding for authority web pages).
- A fresh worker codes all 4 items under C38.
- A fresh second coder codes all 4, with seed `"82a-r2:form"` (n = all 4).
- A form item is a single unit, so a disagreement cannot be averaged away; with n = 4 the gate is extremely sensitive. I recommend the orchestrator either keep the gate as written, with the small-n caveat disclosed, or, since form has no ranked designs, replace the gate for authority-only families by **per-item adjudication** of every disagreement (82a-deck §6.4 style). **Orchestrator's call.**

**Alternative (strict):** drop colour now (literal §D.5) and re-test columns/heading under C38.

---

## 5. Deck, round 2 (after 82a-deck) — **EXPOSED: I am the recoder; ruling marked for the orchestrator's independent check**

| Feature | Full (n = 27) | Sensitivity, 6 worked-example ids excluded (n = 21) | Failure # |
|---|---|---|---|
| background | 0.81 (round 1, carried) | — | passed round 1 |
| heading | 0.81 | 0.76 | second test (round 1 failed at 0.77) |
| colour | **0.70** | 0.67 | **second failure** (round 1 failed at 0.67) |
| title layout | 0.93 | 0.90 | passes |
| admissible | 0.89 | 0.86 | passes |

**Which run binds.** 82a-deck §6 step 2 is explicit about the worked-example exposure: "Both numbers are published, and **the gate uses the full sample**." The full run therefore binds. `deck-agreement-r2.md`'s "net statement" (the sensitivity reading should govern, so no ranked archetypes) contradicts that ratified text and should be corrected.

**Literal outcome (full run):**
- colour failed a second time → **dropped** from deck identity (82a-deck §6 step 4);
- heading passes (0.81) and title layout passes;
- one identity feature failing twice is not "two or more", so deck **still ships ranked archetypes** on `background | heading | title layout`.
- The sensitivity result (heading 0.76) is published as a caveat on heading's stability. It does not decide the gate.

**Disagreement mechanisms** (from the table; the recoder's own reading, not a verdict):
- **Heading, 5 of 5:** LO:014, LO:031, MS:007, MS:014, NPM:032 are all items where the recode used 82a-deck §1 **step 1 (declared face** from the item's source files) and coder 2's value matches a glyph reading. Examples: MS:007 declared Jumble → display, coder 2 sans; MS:014 declared Felix Titling → serif, coder 2 sans; LO:031 declared Liberation Sans with a slab-looking render, flagged in `deck-recode.md`. The agreement rests on whether the second coder fetches source files; 82a-deck §1 permits it but does not require it.
- **Colour, 8 in the full run:**
  - 3 are fill/background calls near the 10% or background-class threshold (NPM:002, NPM:031, LO:041); NPM:002 and NPM:031 were disclosed BORDERLINE in the recode.
  - 5 are hue-presence calls (LO:031, MS:007, NPM:018, NPM:026, NPM:073). 82a-deck §2 uses a 0.2% mark-area floor, while 82a-general B5 uses "≥ 2 elements or ≥ 0.5%"; deck's rule is looser and element-free.

**Draft ruling:** apply the full run, so colour is dropped and deck identity = `background | heading | title layout`. Correct the net-statement paragraph in `deck-agreement-r2.md`.

**Optional hardening, not required by the gate:** make the step-1 font lookup mandatory for future deck coders.

---

## 6. Poster

**History:**
- Colour **was** recoded under 82a-general: `poster-recode-82ag.md` (fresh worker, 39 GH items, B1a applied as written, no R2-type departure).
- The MS + Typst pool (P.5, 15 items) was coded fresh under 82a-general by its own worker.
- Poster is in the §D.1 list, and the gate is family-wide, so colour's failure is a **second failure** (§D.5), even though one of its 4 disagreements comes from the fresh-coded pool.

| Feature | Full (n = 14) | Sensitivity, GH:019 excluded (n = 13) | Failure # |
|---|---|---|---|
| columns / heading / header | 1.00 / 0.86 / 0.86 | 1.00 / 0.85 / 0.85 | pass |
| colour | **0.71** | 0.69 | **second** (§D.5) |
| admissible | **0.64** | 0.69 | **first** (82a-general does not cover admissibility) |
| body / rules-boxes / density (variants) | 0.71 / 0.50 / 0.64 | similar | variant failures → not used in filling (§7) |

Poster uses the ordinary §7 gate, not 82a-deck's worked-example rule. The GH:019 exclusion is a C12 exposure sensitivity, so both numbers are published. Neither changes any gate outcome.

**Colour disagreements (4):**
- **GH:036** (fill-blocks vs mono): a grey header panel `#E0E0E0` at L = 0.88 (≤ 0.90, so a fill under C17, literal per C29), 17.6% of the page. Coder 2 read it as near-white → **ERR-S** under C29. The same call drives the band vs plain-centered header split.
- **GH:051** (one-accent vs fill-blocks): **MEAS**, fill share contested.
- **GH:008** (one-accent vs multi) and **PT:pasquino** (mono vs multi): **AMB-B5** (clustering of the brand cardinal/maroon plus other hues; a light gradient read as a tint vs as hues).

**Admissible disagreements (5):** GH:019 and GH:040 (coder 1 yes, coder 2 no); GH:046, PIM:004 and PT:pasquino (coder 1 no, coder 2 yes). They run both ways, and PT:pasquino is an A3 case (gradient behind a 4-line title/author block), i.e. the C37 scope question.

**Draft ruling:**
- Colour → **drop** (second failure). Poster identity = `columns | heading | header`.
- Admissible → first failure: ratify **C37**; a fresh worker recodes admissibility for all 55 poster items; fresh second sample with seed `"82a-r2:poster"`. If it fails again → per-item adjudication (§7 rule).

---

## 7. Invoice, round 2: how to handle an admissibility-only failure

**History:**
- Round 1 (`invoice-agreement.md`): admissible **1.00** (pass); header and colour failed (0.33 / 0.50), which triggered 82a-general.
- Round 2 (fresh sample, n = 12): header **0.83** (0.82 sensitivity) and colour **0.83** (0.82) now pass, so the recode is vindicated. Columns and heading pass at 1.00.
- **Admissible fails at 0.75 (0.73 sensitivity): its first failure.**
- Density (variant) fails 0.50 → not used in filling (§7).

**Disputed items (3):**

| id | coder 1 | coder 2 | evidence | diagnosis |
|---|---|---|---|---|
| GH:090 | yes | **no, A6** | coder 2: white contact text (< 24 pt) on `#4285F4` = **3.56:1** via `contrast_ratio` | **coder-1 error:** the pair lies in C9's 3.5–5.5 "must sample" band and was not sampled; C29: 3.56 < 4.5 → A6 |
| GH:005 | **no, A2** | yes | coder 1: heart emoji "❤️ Thank you!" | **coder-2 error:** A2 is literal and the emoji is present |
| MS:004 | yes | **no, A6** | coder 2: light-grey text ≈ `#898989`–`#979797` on white ≈ **3.36:1**, but strokes < 2 px on a 400-px thumbnail (disclosed BORDERLINE) | **AMB-sampling:** 82a-general B2 says elements < 2 px are "too thin to sample" for colour, while C9 demands sampling for contrast. Anti-aliasing lightens thin strokes, so a thumbnail understates contrast. Needs **C41** |

**What §7 and §6 say:**
- §7: "Agreement per feature f, **including admissibility** (admit/exclude only, reason ignored) … Gate: every A_f ≥ 0.80. On failure: … sharpening only the failing rule; the first coder recodes the whole family; the second coder codes a fresh sample … A second failure removes that feature from the family's identity."
- Admissibility is not an identity feature, so "removes … from identity" cannot apply to it.
- §3.4: "The denominator N includes inadmissible items — admissibility removes archetypes from shipping, not items from N."
- §6 step 1 ranks only "**admissible**" designs, and C21 counts admissible exemplars in K.
- Admissibility therefore decides **which archetypes may ship and their K**; it cannot be dropped.

**Draft ruling (admissibility failures, all families):**
1. **First failure** → the §7 procedure:
   - sharpen the failing rule (for invoice: **C41** + a mechanical A2 scan);
   - **the first coder re-runs admissibility over the whole family**: A2 by emoji detection on extracted text (or a visual pass where no text layer exists); A6 by `contrast_ratio` for every text-on-colour or grey pair < 24 pt, sampled per C41;
   - a fresh second sample (`"82a-r2:<family>"`) is compared.
2. **Disputed sampled items are adjudicated immediately**, with rule id and measurement, by a worker who coded neither side (82a-deck §6 step 4 precedent). Invoice's three: GH:090 → exclude (A6, 3.56 sampled); GH:005 → exclude (A2); MS:004 → decide under C41 (the declared text colour from the `.docx` styles decides if available, per C25-style declared evidence; otherwise core-pixel sampling).
3. **Second failure** → no dropping is possible. **Every** item on which the two coders' admissibility differs, in any sample, goes to per-item adjudication. Items outside any sample keep the first coder's (re-run) call.
4. **Rejected alternatives:**
   - "Fill only from items both coders admit": only 12 of 48 items were second-coded, so the rule would silently apply the first coder's call to the other 36 anyway, and bias toward items that happened to be sampled.
   - "Apply the first coder's exclusions log as is": the round-2 sample shows that log misses at least one sampled A6 (GH:090), so it cannot be treated as complete.
5. **Invoice filling may proceed on header/colour.** Identity passed, and admissibility only changes which archetypes' exemplars count. Final ranks wait for step 1 (re-run) and the step 2 adjudications.

---

## 8. Infographic, round 1

**History:** coded fresh under 82a-general (IIB pool, N = 12, `infographic-corpus-iib.md` I.8.4). Per §D.6 this is the ordinary §7 gate, so these are **first failures**.

| Feature | A_f (n = 10) | Note |
|---|---|---|
| columns | **0.70** | first failure |
| colour | **0.70** | first failure |
| heading / header / admissible | 0.80 / 1.00 / 0.90 | pass (header: coder 2 coded plain-left on all 10; coder 1 agreed on all 10) |
| rules/boxes, density (variants) | 0.30 / 0.40 | variant failures → not used in filling (§7); a re-test is optional (below) |

**Disagreements on the failing features:**
- **columns (3):** IIB:116 and IIB:142 (1 vs 2-sidebar), IIB:139 (1 vs grid). **AMB-tiles:** §4 says "card/tile layouts = grid", and "columns" counts independently flowing **text** columns. Coder 1 read the dashboard / small-multiple panels as one flow; coder 2 read them as tiles or a sidebar.
- **colour (3):** IIB:075 (fill-blocks vs one-accent), IIB:116 (fill-blocks vs multi), IIB:125 (fill-blocks vs mono). **AMB-C30:** C30 makes charts "MARKS … §B elements/shapes", but does not say whether a large data fill (bars, areas, map regions) can be a B3 fill block. Coder 1 counted chart fills ≥ 10% as fill-blocks; coder 2 treated them as marks.
- **rules/boxes (7 of 10 disagree):** mostly chart axes, gridlines and panel frames read as rules/boxes by one coder only. The same C30 gap.

**Draft ruling:** clarify with **C39 + C40**; the first coder recodes columns, colour and rules/boxes (and density, optionally) for all 12 IIB items; fresh second sample `"82a-r2:infographic"`; if they fail again → drop (second failure).

**Recode instructions (for the first coder):**
1. Re-open each IIB preview at the resolution used before. Apply C39 and C40 only to `columns`, `colour use` and `rules/boxes` (and `density` if the orchestrator wants the variant re-tested).
2. Record per item:
   - `columns-note`: number and type of text-bearing panels and whether they carry their own heading;
   - `colour-note`: background hex, non-data fill area %, and counted clusters listing which are data-mark elements;
   - `rules-note`: which lines are chart parts (ignored) vs layout rules.
3. Leave heading, header and admissibility untouched.

---

## 9. Spot-check of `agreement.py --override` (hand check)

I checked invoice round 2 (`--recode invoice-recode-82ag.md`) by reading 4 sampled items' raw rows from `invoice-recode-82ag.md`, `invoice-second-coder-r2.md` and `invoice-corpus.md`:

| id | corpus (r1) header / colour | recode header / colour | coder 2 header / colour | script's disagreement list | correct? |
|---|---|---|---|---|---|
| GH:058 | split / fill-blocks | plain-left (`align=right`) / one-accent | split / one-accent | header plain-left vs split only | **yes**: recode used (not corpus); the note "(`align=right`)" is normalised away; colour agreement correctly not listed |
| GH:011 | split / fill-blocks | band / mono | plain-left / mono | header band vs plain-left only | **yes** |
| MS:004 | band / mono | split / mono | split / fill-blocks | colour mono vs fill-blocks only | **yes**: header agreement (split = split) correctly not listed, although the corpus said band |
| GH:035 | split / one-accent | split / mono | split / mono | none | **yes**: colour override (one-accent → mono) applied |

The override logic behaves as documented on these 4 items. Two **parser artifacts** remain in other families' outputs: brochure MSB:010 heading and form FMA:004 colour (§0). Both are trailing annotations inside a value cell. Suggested fix: strip `(...)`, and text after a comma, from a cell before comparing, as the override path evidently already does for "(`align=right`)".

---

## 10. Draft clarification texts (to become `82a-clarifications-6.md` if ratified)

**C33 (colour background, all families under 82a-general; voids reading R2).**
- The background is **exactly** 82a-general B1a: the most common colour class on the 20×20 sample grid, after dropping points on photos, illustrations and text, using 82a-deck §2's class tolerances.
- Saturation, brand colour or "design intent" never demote the most common class to a fill. A colour that is the background is never a B3 fill block.
- For brochure, the grid covers the whole outside spread (§B page scope).
- B5 elements: each separately set word or line in one colour is one element. Placeholder text counts. A single hyperlink still fails B5 (§C GH:030).

**C34 (brochure header scope).**
- Every header test for brochure, **including C1's image-hero area**, is measured against the **front panel**: "page area" = front-panel area, "page width" = panel width, "page height" = panel height.
- Image-hero keeps strict priority over band/ruled/split.
- *Effect on the failed test: none (header is dropped for brochure). The text is recorded for poster/infographic spreads and for any future brochure corpus.*

**C35 (full-page illustrated scenes and patterned strips; header).**
- A full-page drawn scene (sky/ground/background drawn as part of one picture) is **one illustration**, for the header test (image-hero if ≥ 30%) as well as the colour test (B1b). A flat colour field with separate clip-art laid on top is a fill plus illustrations.
- A patterned strip (dots, dashes, pennants) spanning ≥ 80% of page width at the page edge counts as the "full-width bar" of §A.2 step 3.
- A halftone/texture patch is a band fill only if criteria (a)–(d) are met by its L ≤ 0.90 extent.
- *Effect on the failed test: none (header dropped for flyer); recorded for poster/infographic.*

**C36 (memo header).**
- (a) **Boundary.** For memo the boundary is the first body paragraph or a single body label that introduces it ("COMMENTS:", "MESSAGE", "Notes"). A rule directly above that label, with no text between, is the header block's closing rule and is tested under 82a-cv ruled (a)–(d). 82a-cv A2's section-heading exemption applies only when the body contains **≥ 2** headed sections.
- (b) **Meta for split.** Memo meta = the header block's document-meta lines only: TO / FROM / CC / DATE / SUBJECT / RE / reference or memo number. Organisation identity blocks (sender or organisation address, contact, certification text, logo, crest) are **never** meta and **never** create split in memo.
- (c) **Title.** If no "MEMO"/"Memorandum"/organisation-name text exists, the title is the largest text in the top 30% excluding logos and placeholders (§A.1), even if it is a routing label. Record this in `header-note`.
- (d) **Numbers.** Ruled (a)/(d) and split (a)–(c) calls must record the measured width, edge or offset in `header-note`. A call without its number is returned to the coder.

**C37 (A3 and A5 scope, every family).**
- A3 excludes an item only for running text, bullet text, or any text block of **≥ 3 lines** set **directly** on a gradient, texture or photo (C14 and 82a-deck §4, generalised).
- Titles, subtitles, labels and captions of ≤ 2 lines on such a fill are not A3. They must pass A6 by C9 sampling at C14's size thresholds (≥ 4.5:1 below 24 pt, ≥ 3:1 at 24 pt or more), with C29 literal thresholds.
- A photo counts as a flat panel only if it is a tint: every sample behind the text lies within ΔL ≤ 0.10 (82a-deck §2).
- A5 = ≥ 3 **identical** discrete motifs (C20). Never continuous pattern bands, never differing icons.
- A4 (paint-swipe/splatter) is unchanged.

**C38 (unit of coding for authority web pages, form and any family whose items are design-system pages).**
- The item is the **prescribed specimen** (the form field/pattern exactly as the authority prescribes it), never the documentation website that presents it.
- Site navigation, side "On this page" TOCs, site headers/footers, breadcrumbs, code samples, site link colours and the site's own `<h1>` styling are page chrome (as 82a-cv A3's "page is the document sheet only") and are ignored.
- Heading/body class = the typeface the authority prescribes for form text (from its own component CSS or type guidance).
- Columns = the specimen's own question-flow layout.
- Colour = the specimen's **at-rest** colours. Error, focus and hover states are UI states (B1d) and are excluded. Where the authority publishes only diagrams (ABS), the diagram is the specimen and its own strokes and fills are coded.
- **Record** which of these sources was used per item.

**C39 (charts vs fills; infographic and any family with data graphics; extends C30).**
- Data marks (bars, areas, lines, dots, map regions, pie/donut slices, heat cells) are **never** B3 fill blocks and never make `fill-blocks`, whatever their size.
- Each distinctly coloured data series is one B4 element for hue counting (B5: a series drawn in ≥ 2 marks counts as ≥ 2 elements).
- Chart axes, gridlines, tick marks and a chart's own frame are part of the chart: they are neither `rules` nor `boxes` in rules/boxes.
- Non-data panels, bands and cards remain B3 candidates as usual.

**C40 (columns with panels and tiles).**
- `columns` counts independently flowing **text**. A chart or data panel is not a column.
- **grid** = ≥ 3 text-bearing tiles/cards of similar size arranged in ≥ 2 rows and ≥ 2 columns, each with its own heading or label.
- **2-sidebar** = one narrow (≤ 40% of text width) column of running text beside the main flow.
- A single stacked sequence of full-width sections is **1**, even if each section contains side-by-side charts.
- Record the count of text-bearing tiles and rows/columns in `columns-note`.

**C41 (A6 sampling of thin strokes).**
- A6 is decided on the text's **core** colour: the darkest-quartile pixels of strokes, or the declared text colour from the source file (C25-style declared evidence), which wins when available.
- Where strokes are < 2 px at the preview's resolution and no source colour is available, the pair is coded from the core pixels and flagged BORDERLINE. It excludes only if the core-pixel ratio is below the threshold (C29 literal).
- Anti-aliased edge pixels are never the sample.

**Seed rule for these re-tests:** `random.Random("82a-r2:<family>")`, so no sample repeats the `"82a:<family>"` draw.

---

## 11. Summary of draft rulings

| Family | Feature | Literal §7/§D | Recommended draft ruling | Next step |
|---|---|---|---|---|
| brochure | header | 2nd failure → drop | **drop** | — (C34 recorded for later families) |
| brochure | colour | 2nd failure → drop (→ no ranked) | **void + re-run** (recode departed from B1a, R2) | fresh colour recode (C33) + second sample `82a-r2:brochure`; fail again → drop → §D.5 no ranked |
| flyer | header | 2nd failure → drop | **drop** | — (C35 recorded) |
| flyer | colour | 2nd failure → drop (→ no ranked) | **void + re-run** (6/7 disagreements = R2) | fresh colour recode (C33) + second sample `82a-r2:flyer` |
| flyer | admissible | 1st failure | **clarify + recode** | C37; fresh admissibility recode of all 20; same second sample; fail again → per-item adjudication |
| memo | header | 1st failure | **clarify + recode** | C36; first coder recodes header; second sample `82a-r2:memo`; fail again → drop |
| form | columns, heading | 1st failure | **void (SCOPE) + recode** | C38; fresh coding of all 4 + second coder all 4 (`82a-r2:form`); small-n gate vs per-item adjudication = orchestrator's call |
| form | colour | 2nd failure (literal) → drop | **void (SCOPE) + recode** with the above | as above |
| deck r2 (**exposed: recoder**) | colour | 2nd failure (full run binds, 82a-deck §6.2) | **drop** colour; heading passes 0.81 → identity `background \| heading \| title layout`; ranked archetypes ship | correct `deck-agreement-r2.md` net statement; orchestrator to verify independently |
| poster | colour | 2nd failure (§D.1/§D.5) | **drop** → identity `columns \| heading \| header` | — |
| poster | admissible | 1st failure | **clarify (C37) + recode** all 55 | second sample `82a-r2:poster`; fail again → per-item adjudication |
| invoice r2 | admissible | 1st failure (round 1 was 1.00) | **re-run admissibility (C41 + A2 scan) + adjudicate 3 disputed** | fresh sample `82a-r2:invoice`; identity passed, so filling may proceed |
| infographic | columns, colour | 1st failure (§D.6) | **clarify (C39, C40) + recode** columns/colour/rules-boxes | second sample `82a-r2:infographic`; fail again → drop |


**Strict alternative** (no voiding):
- brochure and flyer: header and colour dropped → no ranked archetypes (§D.5); seeds, L3/L4 and a Shortfall.
- form: colour dropped; columns/heading re-tested under C38.
- memo is unaffected: it is a first failure either way.

**Why I recommend voiding for colour but not for header:** the header failures come mainly from genuine ambiguities in the written rule, which a second failure is designed to remove. The colour failures come from a recode that openly substituted a different rule (R2), contradicted by 82a-general's own worked example. That did not test the rule at all.

**Process note for the orchestrator:** both R2 recodes (brochure, flyer) disclosed their departure from B1a in their own "Readings applied" sections and were still fed into the gate. A pre-gate check that a recode's disclosed readings do not contradict a ratified rule or worked example would have caught this.
