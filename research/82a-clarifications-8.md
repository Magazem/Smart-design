# research/82a — Clarifications round 8: C51 report header (orchestrator, 2026-09-25)

RATIFIED. Source: research/82a-report-header-failure.md §3 (drafted by an independent Opus diagnostician). Report's header failure (A_f 0.75) is a FIRST failure. Recode header for all 64 report items under C51 with a fresh recoder, then re-test with seed `random.Random("82a-r2:report")`. GH:104 is both a worked example and in the new sample, so the gate also runs a sensitivity run excluding GH:104. The full run binds. A second failure drops header, and report identity becomes columns | heading | colour.

Recoders and second coders must NOT open research/82a-report-header-failure.md or any report evidence file other than the items csv(s).

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
