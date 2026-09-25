# research/82a-report-header-failure — report `header treatment` gate failure (first failure), diagnosis and C51 (DRAFT)

**Status: DRAFT for orchestrator ratification.** Written 2026-09-25.

**Exposure:** I have never coded report. Writing this file exposed me to both coders' header values on
GH:094, GH:104, GH:129 and MSR:003, so I am excluded from both re-test roles (§5).

**Rules applied:**
- research/82 §7;
- 82a-general §A (header) and §D;
- 82a-cv (ruled/split criteria and Addendum A, which 82a-general §A.2 incorporates);
- 82a-clarifications-1 to -7, especially C1, C13, C16, C17, C18, C29 and C45(d) (the precedent for "call without its number is returned").

**Inputs read:**
- `designs-evidence/report-agreement.md`;
- `designs-evidence/report-recode-82ag.md` (first-coder header values, recoded under 82a-general);
- `designs-evidence/report-second-coder.md`;
- the three items csvs.

**Measurement.** Previews were fetched to the system temp directory and deleted afterwards.
- PDFs: page 1 rendered with PyMuPDF. Text spans and vector drawings were read from the PDF, so the lengths below are exact, in PDF points.
- Rasters: row and column scans with PIL.

**Not done:** no git; no corpus, recode, agreement or second-coder file edited; nothing recoded.

Diagnosis codes follow research/82a-gate-failures.md:
- **ERR-R**: the recoder (first-coder side) departed from the written rule.
- **ERR-S**: the second coder departed from the written rule.
- **AMB**: the written rule admits both readings.

---

## 1. The failure

`header` (identity) A_f = 12/16 = **0.7500** (kappa 0.6384), full sample, seed `"82a:report"`. Every other identity feature passes:
- columns 1.00;
- heading 0.9375;
- colour 0.9375;
- admissible 0.8125.

There is no earlier gate run for report, so this is the **first failure** (§7). The remedy is to clarify the rule, recode and re-test with seed `"82a-r2:report"`.

The agreement file lists exactly **4** header disagreements, and no others.

## 2. Disagreement table

| id | coder 1 (82ag recode) | coder 2 | what the preview shows (my measurement) | diagnosis |
|---|---|---|---|---|
| GH:094 | ruled | plain-centered | **Page:** 612×792 pt.<br>**Title:** the largest span is a 56.7 pt "C" inside the grey crossed image-placeholder frame ("Internship completed at:"). That is a placeholder, so the title is "[Project Title]" at 20.1 pt, centred (offset 0.0% W).<br>**Box around title and subtitle:** x 94.1–517.9 pt = **69.3% W** (shadow included).<br>**Rules framing "END OF STUDIES PROJECT" and "Presented by":** **40.7% W**.<br>**The only 81.5% W lines** are at y = 494.8, 515.4 and 593.8 pt: the jury table's top rule, header rule and bottom rule. The recode's "81.3–81.5%, y=988–1030" is exactly the first two of these at its 2× render. Three text lines lie between the box and the table ("Presented by:", "[Full Name]", "Defended on…"). | **ERR-R.** The recoder attributed the table rules' width to the title box. 82a-general §A.2 step 3 counts a box edge only when "the box spans ≥ 80% of page width"; this box is 69.3%. 82a-cv 3(c) requires "no text lies between it and the header block". The second coder is correct.<br>Latent ambiguity, closed by C51(c)/(d): §A.2 exempts table rules only when the table is the *boundary*, and report has "none". The block's "contiguous … date lines" could arguably chain down to "Defended on DD/MM/YYYY". |
| GH:104 | band | plain-centered | **Page:** 595.3×841.9 pt; page 1 is title plus running text.<br>**Title:** 17 pt, y 67–86 pt, centred (offset 0.0% W).<br>**Grey panel:** declared fill 0.902 grey, x 70.9–524.4, **y 159.0–389.5 pt**, 76.2% W × 27.4% H. It lies behind the "PROJECT ABSTRACT" paragraph only. The title and the 3-column author block sit on white above it. | **ERR-R.** 82a-general §A.2 step 2 (a) and C18: band requires "a fill lies behind the title's glyphs". The recode says the title and authors "all sit on one continuous pale-grey panel … 17.3% of page height", which the drawing extents contradict. The second coder is correct.<br>Latent **AMB**, which neither coder raised: 82a-cv 3 lets "any fill that is not behind the name" act as a rule if it is "≥ 80% of page width **or ≥ 90% of live width**". The panel is 100% of the page's text extent (76.1% W) and sits directly below the author block. A literal reader could code it **ruled**. C51(d) closes this. |
| GH:129 | plain-centered | ruled | **Page:** 2480×3508 px.<br>**Purple field** (60,16,83): full width, y 0–1593 = **45.4% H**. Its only content is the crest and wordmark (logos).<br>**Short black rule:** 23.8% W at 49.9% H.<br>**Title:** top at 55.0% H, centred (offset 0.0% W).<br>**Gap from field to title:** 334 px = **9.5% H**. That is ≈ 3 title line pitches (≈ 110 px), but 4.3–5.1 pitches of the cover's small text (66–78 px). | **AMB (two gaps in the text).** (i) 82a-cv 3 admits "any fill that is not behind the name" with **no thickness limit**, and 82a-general §A.2 adds "a full-width bar at the page edge above the header block". A 45%-high field satisfies both literally (width 100%, above the title, no text between).<br>(ii) Criterion (d) is "gap … ≤ 4 **body lines**", and 82a-cv defines body line as "the line pitch of body text on page 1". A report cover has no body text, so (d) is undefined: it passes on title pitch (the second coder: "about 2 body lines") and fails on small-text pitch.<br>The recoder never tested the field as a rule candidate (an omission), but its value is one literal outcome.<br>C51(d) decides: a fill > 5% H is never a rule, and the gap is ≤ 7% H. The result is **plain-centered**. |
| MSR:003 | band | image-hero | **Page:** 400×519 px.<br>**Photo:** a full-bleed B&W skyscraper photo starting at y = 0 (row 0 is textured; luminance sd 54). Its **visible** area is **66.8%** of the cover.<br>**Yellow panel:** x 0–344 (86.2% W), **y 156–362 = 39.9% H** (the recode says "≈95 px … ≈18%"). The title sits on the panel. | **ERR-R.** 82a-general §A.2 step 1: "image-hero: unchanged (82a C1)", strict priority, first match wins. C1 needs an image "that intersects the top 20% … AND whose own area is ≥ 30% of the page area". Both hold (66.8% visible, 100% including the part behind the panel), so band is never reached. The recoder's MS section never applied C1: it has image-hero 0/10 and no C1 numbers in any MS row. The second coder is correct.<br>C51(a) restates the rule and adds the occlusion convention for borderline cases. |

**Tally:**
- 3 **ERR-R**: GH:094, GH:104, MSR:003.
- 1 **AMB**: GH:129.
- 0 **ERR-S**.

With the three recoder errors corrected and nothing else changed, header would read 15/16 = 0.9375. So the failure is mainly first-coder execution, and it is concentrated in two **method-level** faults, not one-off slips:
1. **MS corpus:** C1 was never measured. Image-hero is 0/10 there, although at least MSR:003 has a top-anchored photo ≥ 30%.
2. **GitHub corpus:** the row-scan script reported "the widest contiguous dark span" on the page, without tying it to the element adjacent to the header block. That is how GH:094 picked up a table rule. The GH section's ruled/not-ruled calls all rest on this script.

**Void or first failure?** The brochure/flyer colour precedent (82a-clarifications-7) voided a re-test whose recode departed from the literal rule. That argument is weaker here:
- the departures are errors, not a disclosed alternative reading;
- GH:129 is a genuine ambiguity.

Both routes prescribe the same work (clarify, full recode, fresh sample). I therefore follow the brief: **count this as report's first failure**. The next failure is then the second failure and drops header.

**Side note (colour, not in scope; colour passed).** GH:104's panel is declared as 0.902 grey, i.e. RGB 230, so L = 0.902. That is above C17's L ≤ 0.90 fill bound, so from the declared colour it is a pale tint (B1e) and not a B3 fill. Both coders coded `fill-blocks`; the second coder sampled (229,230,229) = L 0.900 from the raster. This is a live boundary case under C29. I flag it and propose no action (colour is not re-tested).

A small discrepancy with no effect: the second coder gives GH:129's purple field as 40.5% of the cover, and I measure 45.4%. Both are above every threshold involved.

---

## 3. Draft clarification C51

To be published, once ratified, as `research/82a-clarifications-8.md` **without §1–§2 of this file**, so the recoder and the second coder never see the coders' values.

**C51 (report header treatment; cover per C13). Scope: report only.** C51 supplements 82a-general §A.1–§A.2 and 82a-cv for report. Band's criteria, split, plain-centered (±5% of cover width), plain-left, every colour rule and every other feature are unchanged.

"Cover" means the sheet coded under C13. Where a preview shows a back+front spread, "cover" means the front panel only (as 82a-cv A3). "W", "H" and "area" mean the cover's width, height and area.

**(a) Image-hero first, with numbers.**
- Test 1 (C1) is measured on **every** cover before any other test.
- Record two numbers:
  - the image's top edge, as % H;
  - its **visible area**, as % area. Visible area = the image's pixels not covered by panels, cards, text boxes or other images.
- An image that runs behind a panel qualifies if both hold:
  - it intersects the top 20% of H;
  - its visible area is ≥ 30%.
- These are never images: logos, crests, seals, wordmarks and logo or image placeholders (82a-general §A.1), and charts (C30).

**(b) Title.**
- The title is the largest text on the cover, measured by span font size (PDF) or cap height in px (raster).
- These are excluded from the title: logos, wordmarks, placeholders, and any text inside an image-placeholder frame.
- If two candidates are within 5% of each other in size, the **higher** one on the cover is the title.

**(c) Header block (contiguity).**
- The block starts as the title.
- A line joins the block if both hold:
  - the vertical gap between the line and the nearest block line is ≤ 2 × the bounding-box height of the smaller of the two lines;
  - no drawn line, box edge or fill edge lies between them.
- Chaining stops at the first line, above and below, that fails.
- Table cells never join.

**(d) Ruled on a cover.** This replaces 82a-cv 3(a) and (d) for report; 3(b), 3(c), A2 and 82a-general's boundary-element rule stay. A candidate is ruled only if it meets all of the following:
1. **Type.** It is a stroked line, the top or bottom edge of a stroked box, or a fill whose height is ≤ 5% of H. A fill taller than 5% of H is **never** a rule, whatever its width: it is tested only as band, and, for colour, under B3.
2. **Length.** It is ≥ 80% of W. The "≥ 90% of live width" alternative does not apply to covers.
3. **Position.** It lies above the block's top line or below its bottom line, and **no text line** lies between it and the block. Logos and other drawn elements in between do not block it.
4. **Gap.** The gap to the nearest header-block line is ≤ **7% of H**. This replaces "≤ 4 body lines", which a cover cannot define; 7% H ≈ 4 lines at 14.4 pt leading on A4.
5. **Tables.** It is not a table line. A table is ≥ 2 rows × ≥ 2 columns of text cells. Its top border, header-row rule, internal rules and bottom border never count, whether or not the table is a boundary element.

**(e) Numbers or return.** Every header call records its deciding numbers in `header-note`:

| value | numbers to record |
|---|---|
| image-hero | top % H; visible area % |
| band | fill width % W; top and bottom % H; confirmation that the title's glyphs sit on it (C18) |
| ruled | element type; length % W; thickness % H (fills); gap % H |
| split | the 82a-cv 4 quantities |
| plain-centered, plain-left | title-centre offset % W; the widest rejected rule candidate with its length % W; the image top % H and visible % of the largest rejected image |

A call without its numbers is returned to the coder (as C45(d)). Any number within 10% of its threshold is flagged.

**Worked examples** (measured; they illustrate the rule and are not pre-filled codes):

| id | measurement | value |
|---|---|---|
| MSR:003 | Photo from y = 0, visible 66.8% (yellow panel over it: 86.2% W × 39.9% H). Test 1 decides. | **image-hero** |
| GH:094 | The 56.7 pt "C" is inside an image-placeholder frame, so the title is "[Project Title]" (20.1 pt). Box edges are 69.3% W and the framing rules 40.7% W (both < 80%). The 81.5% W lines are the jury table's rules (d5), with 3 text lines between (d3). Title centre offset 0.0% W. | **plain-centered** |
| GH:104 | The grey panel (y 159–390 pt) is below the title (y 67–86 pt), so band (a) fails. The panel is 27.4% H > 5%, so it is not a rule candidate (d1); 76.2% W would also fail (d2). Offset 0.0% W. | **plain-centered** |
| GH:129 | The purple field is not behind the title (band fails). It is 45.4% H > 5% (d1 fails); the gap to the title, 9.5% H > 7%, would fail (d4) anyway. The short black rule is 23.8% W. Offset 0.0% W. | **plain-centered** |
| GH:086 (not sampled) | "End-of-Studies Project Report" and "[Project Title]" are both 20.7 pt, so the higher one is the title (b). "[Degree Track / Specialization]" joins the block (gap 14 pt ≤ 2 × 18 pt). A stroked line of 81.5% W sits above it with a gap of 49.5 pt = 6.25% H ≤ 7% (flag: within 10%), and no text lies between. | **ruled** |

---

## 4. Effect on the four disputed items under C51

- GH:094 plain-centered (c2 ✓).
- GH:104 plain-centered (c2 ✓).
- GH:129 plain-centered (c1 ✓).
- MSR:003 image-hero (c2 ✓).

These are expectations for the orchestrator's check only. The recode measures every item again.

---

## 5. Recode and re-test instructions

**Who is excluded from both roles below:**
- the report GitHub, MS and ARC first coders;
- the 82ag header/colour recoder;
- the round-1 second coder (Opus Reviewer), who also coded ARC25:011, GH:058 and GH:104, all three in the new sample;
- Design Researcher 2, who ran the report L3 re-check;
- the author of this file.

| step | who | items | reads | does NOT read | writes |
|---|---|---|---|---|---|
| 1. Ratify | orchestrator | — | this file | — | `research/82a-clarifications-8.md` containing C51 (§3 only) |
| 2. Recode | **one fresh worker**, never coded report | **all 64**: GH 40, MS 10, ARC 14. `header treatment` only | the three items csvs (including `pages`), research/82 §4–§5, 82a-general, 82a-cv, 82a-clarifications-1…8 | any `report-*.md` evidence file, `report-agreement.md`, the round-1 second-coder file, this file | `designs-evidence/report-recode-c51.md`: `id \| header \| header-note`, with numbers per C51(e) |
| 3. Re-test | **fresh, independent second coder** | `random.Random("82a-r2:report").sample(sorted(ids), 16)`, `header` only | as the recoder | as the recoder, plus `report-recode-c51.md` | `designs-evidence/report-second-coder-r2.md` |
| 4. Gate | orchestrator | — | — | — | `designs-evidence/report-agreement-r2.md` |

**Why all 64 items, not only the 4 disputed ones:** both faults are method-level (§2). C1 was never run on MS, and the GH ruled calls rest on a whole-page widest-span scan.
- Colour and every other feature are **not** recoded. Colour passed at 0.9375.
- `rules_boxes` stays dropped from filling (non-gating variant, §7).

**New sample (seed `"82a-r2:report"`, 64 sorted ids, n = 16):** `GH:079, GH:104, ARC25:011, ARC25:024, GH:123, ARC25:037, GH:084, GH:067, GH:031, GH:009, GH:058, GH:022, GH:138, MSR:004, GH:103, MSR:010`.
- It overlaps the round-1 sample on ARC25:011, GH:058 and GH:104.
- Worked example GH:104 is in it, so a **sensitivity run excluding GH:104** is reported (82a-general §D.3, C12). The gate uses the full sample.

**Gate invocation** (header from the new recode, colour kept from 82ag):

```
python research/designs-evidence/agreement.py --family report \
  --first GH:research/designs-evidence/report-corpus-github.md \
          MSR:research/designs-evidence/report-corpus-ms.md \
          ARC25:research/designs-evidence/report-corpus-l3.md \
  --override header=research/designs-evidence/report-recode-c51.md \
             colour=research/designs-evidence/report-recode-82ag.md \
  --second research/designs-evidence/report-second-coder-r2.md
```

Run it again with `--exclude GH:104` for the sensitivity run.
- Only `header` is read from the r2 output.
- The other features keep their `report-agreement.md` results.

**Decision:**
- **Pass:** header A_f ≥ 0.80, applied literally (C29): 13/16 = 0.8125 passes, 12/16 fails. Header stays in report identity with the C51 values.
- **Fail (second failure):** header is **dropped** from report identity, and the archetype becomes `columns | heading | colour`. That is disclosed in the report evidence file.
  - Colour has passed, so §D.5's "both fail" clause does not trigger. Ranked archetypes still ship.
  - C16 then no longer matters for report.
