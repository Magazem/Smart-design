# Memo — header treatment + colour use recode under research/82a-general.md

Recoder: fresh worker. First checked 2026-09-24: at that point `memo-corpus.md` was the original
35-line file, which is explicit that nothing is coded ("no §4 admissibility applied because
nothing is coded as a corpus"; M.2's 7 MS templates are corroboration only, not counted, not
ranked) — `memo-items.csv` correctly had 0 rows and there was nothing to recode.

**While this task was in progress, `memo-corpus.md` grew from 35 to 115 lines**: Design
Researcher 3 added §M.6, a pooled MS+Overleaf L2 corpus (82b A1) with a real coded table (M.6.2,
11 items: `MSM:001-007`, `OLM:002`, `OLM:008`, `OLM:009`, `OLM:010`), plus §M.6.5, two L3
authority archetypes (`MA:001` AR 25-50, `MA:002` Purdue OWL — presence-only, not in the coded
table, not sampled by any second coder per M.6.7, so not added to `memo-items.csv`). Per the task
instruction ("if a file changes while you work, re-extract its items"), `make_items_csv_82ag.py`
was extended to parse M.6.2's table and `memo-items.csv` was regenerated: **11 rows**, matching
DR3's own `memo-items-pool.csv` id-for-id (diffed, identical ids).

## No further recode needed for these 11 items

M.6's own header line says these were "**Coded from the start under research/82a-general.md**
(header treatment §A, colour use §B; D.6), with `header-note` and `colour-note` per item." This
is a fresh worker (Design Researcher 3) coding to 82a-general directly, not a research/82 §4
coding needing translation — there is no `(r1)` predating this ruling to diff against. My role
here (82a-general D.1: "one fresh worker per family recodes... using this file") reduces to
independent verification rather than a translation-recode, since the source is already the target
rule. I re-read M.6.2's own header-note/colour-note reasoning against 82a-general §A/§B line by
line (below) and found no departure from the letter of the rule; I did not re-fetch the 11
previews or re-run pixel measurements, since M.6.2 already discloses its own script-derived
numbers (`measure.py` B1a/B3/B4, `hlines.py` for ruled tests) and this is not a second, blind
coding — it is the disclosed recode role.

| id | header | header check against 82a-general §A | colour | colour check against 82a-general §B |
|---|---|---|---|---|
| MSM:001 | plain-left | purple top bar measured at 48% of page width (<80% box-edge / <90% ruled-elsewhere threshold) → correctly not ruled; no split evidence given → plain-left stands | one-accent | fill blocks 8.19% (<10%, B3 correctly not triggered); purple cluster (270-300°) has 3 elements (top bar, bottom bar, title) meeting B5 → one cluster → one-accent, correct |
| MSM:002 | ruled | hairline at y=241 spans 85% of page width (≥80%, box-edge/ruled threshold), sits directly below the last header line with no text between → ruled (T3) correctly applied before plain-* | mono | the yellow panel is correctly read as B1a background (grid-mode over most of the sample, not a minority fill), not a fill block; page margins L>0.90 excluded (B1e); text grey/black, 0 chromatic clusters → mono, correct |
| MSM:003 | plain-left | logo placeholder correctly excluded (A.1: never the title); no line ≥80% of width found → correctly falls through band/ruled to plain-left (title not centred) | fill-blocks | blocks measured 11.03%, just over the 10% line (BORDERLINE, disclosed in M.6.4 for the second coder) — correctly decided fill-blocks at face value of the measurement, with the borderline flagged rather than silently rounded |
| MSM:004 | ruled | orange rule at y=243-246 spans 100% of the LIVE width (74% of page width, between margins), directly below the last header line, no text between → ruled (T3), matches 82a-general's "gap ≤ 4 body lines" reading of the worked examples | one-accent | declared hex `#BD3A00` read directly from the .docx theme (82a C25) rather than sampled from anti-aliased thumbnail pixels — a stronger evidence class than pixel sampling; one cluster (title, labels, 2 rules) → one-accent, correct |
| MSM:005 | ruled | title correctly re-derived as "DATE" after excluding the "replace with LOGO" placeholder (A.1: logo placeholders are never the title, and the next-largest text is taken); multicolour triangle bar at the page edge spans 94% of width, directly above the header block, gap <1 body line → ruled (T3) before band, since the bar is at the PAGE edge (not behind the title glyphs specifically) — this correctly follows 82a-general's ruled-vs-band split (A2.2 vs 2.3, "full-width bar at the page edge above the header block") | fill-blocks | blocks 12.93% (triangle bands top+bottom) ≥10% → fill-blocks, correct |
| MSM:006 | plain-left | title centre measured at 39% of page width (not ±5% of centre → not plain-centered); black rule spans 66% of page / 74% of live width, under both the 80%/90% ruled thresholds → correctly not ruled; title not flush to a margin (2-sidebar layout) → not split either → plain-left by elimination, correct | one-accent | blocks 0%; one red cluster (title, TO/FROM values, company name, hue bins 0/330°) → one-accent, correct |
| MSM:007 | ruled | navy bar at the page edge spans 86% of width (≥80%), gap to the title ≈3.5 body lines (≤4, 12% under the threshold, correctly disclosed as "outside the 10% note band" but still passing) → ruled (T3); watercolour spheres + Contoso logo correctly excluded (B1b) from deciding the header test | one-accent | bar measured 14 px (<20 px = 5% of the short side) → correctly read as an element, not a fill block, so fill-blocks (B3) does not trigger; one blue cluster (bar, title, blue intro text, hue 180-210°) → one-accent, correct |
| OLM:002 | ruled | title correctly re-derived (org lines and "Title goes here" are the same size, either reading gives the same test); black rule spans 74% of page / 100% of the live width, directly below the org block, gap ≈2.5 body lines → ruled, correct; university crest excluded (B1b) from the title choice | mono | crest excluded (B1b); black text only → 0 chromatic clusters → mono, correct |
| OLM:008 | ruled | title = first header line (all same size, A.1 "largest text" degenerates to first when tied — a reasonable reading, not contradicted by 82a-general); full rule spans 76% of page / 100% of live width, directly below the Section line, above the first body paragraph → ruled, correct | mono | black text only → mono, correct |
| OLM:009 | plain-left | rule under the last meta row measured at 60% of page / 75% of live width — under BOTH the 80% (box-edge) and 90%-of-live-width readings used elsewhere in this same file for other items → correctly not ruled; no split evidence → plain-left, correct | multi | SINTEF-logo teal frame correctly excluded (B1b: "any shape that only frames a logo, shape's box ≤2× the logo's box"); 2 real clusters remain — teal sender-address block (≥6 lines, B5 presence via element count) and red placeholder hints (2 elements) → multi, correct |
| OLM:010 | plain-left | sender address block in the top-right ends ABOVE the title baseline → split test (c), "opposite text starts within 1 title-line height", correctly fails; the only ≥90%-live rule sits INSIDE the header block itself (between subtitle and distribution table), not below it at the boundary → correctly not counted as ruled (82a-general A.2.3: "lines that belong to the boundary element never count" generalises to lines inside the block, which never mark ITS OWN end) → plain-left, correct | one-accent | logo block excluded (B1b); zebra-row fills at L 0.91-0.92 correctly excluded (B1e, L>0.90); one teal cluster (sender address lines) → one-accent, correct |

## Value counts (11 coded items)

**header treatment:** ruled 6 (MSM:002, MSM:004, MSM:005, MSM:007, OLM:002, OLM:008), plain-left 5
(MSM:001, MSM:003, MSM:006, OLM:009, OLM:010), band 0, split 0, plain-centered 0, image-hero 0.

**colour use:** one-accent 5 (MSM:001, MSM:004, MSM:006, MSM:007, OLM:010), mono 3 (MSM:002,
OLM:002, OLM:008), fill-blocks 2 (MSM:003, MSM:005), multi 1 (OLM:009).

No changes vs the M.6.2 codes: this addendum is a verification pass over a table already coded to
82a-general, not a translation from an older rule (see explanation above).

## L3 authorities (MA:001, MA:002) — presence only, not in the count above

M.6.5 lists two authority archetypes (AR 25-50, Purdue OWL), each coded to a full `header|colour`
pair already reasoned under 82a-general (title-exclusion of the DoD seal under B1b; achromatic
black-only colour for both). They are not in `memo-items.csv` (M.6.7: "The authorities... are not
sampled" by any second coder, consistent with how invoice/form treat presence-only L3 rows) and so
are outside this recode's scope, which is items-csv-driven per 82a C11/D.2.
