# Memo — header treatment recode r2 under 82a-clarifications-7 C45 (memo header)

Recoder: Design Researcher 3, 2026-09-25. I am the memo first coder (M.6/M.7; the M.8 GitHub rows were coded by
another worker in the same corpus file). Scope: `header treatment` ONLY, for **every memo item** in
`memo-items-pool.csv` (25: MSM 7, OLM 4, OLH 1, GM 13), under 82a-general §A as amended by **C45** (ratified draft
C36 in `82a-gate-failures.md` §10). Colour and every other feature are untouched.
Independence: I did not open `memo-agreement.md`, `memo-second-coder.md` or §1–§9 of `82a-gate-failures.md`. I read only §10
(the rule texts) and `82a-clarifications-7.md`.

**Method.** Previews were fetched into the system temp dir (not the repo). MS: 400×519 thumbnails. Overleaf: current signed
page-1 images, re-read from each template page (OLM:002/008 794×1028, others 794×1123). GitHub: PNG as published, and PDF
page 1 rendered at 90 dpi with PyMuPDF. Measurements come from script output only:
- `hl.py`: horizontal runs ≥ 30–40% of width, with the length as % of page width;
- `lines.py`: text-line y/x extents, used for title position, live width and body pitch;
- for the PDFs, `pdfgeo.py`: exact span sizes, bboxes and baselines (`get_text('dict')`), plus vector rules (`get_drawings()`),
  in pt. Page width is 612 pt (Letter) or 595.3 pt (A4).

Readings applied throughout, stated once:
- **C45(a) boundary**: the first body paragraph, or the single body label that introduces it (COMMENTS:, Comments:, Abstract).
  A rule directly above it with no text between is the header block's closing rule. The A2 section-heading exemption is not
  triggered for any closing rule below (no memo has ≥ 2 headed sections *and* a rule attached to a heading).
- **C45(b)**: sender/organisation address blocks, logos and crests never create split.
- **C45(c)**: every title that was chosen by the fallback is named in the note.
- **C45(d)**: every ruled (a)/(d) call and every split (a)–(c) call carries its number.
- **Live width** (82a-cv) = the leftmost to the rightmost body-size text on page 1, logos excluded.
- **Body pitch** = the modal line pitch of running body text. Where a page has no or only one body line, the note says which
  pitch was used.
- Ruled (a) passes at ≥ 80% of page width **or** ≥ 90% of live width. (d) passes at a gap ≤ 4 body lines.

| id | header | header-note |
|---|---|---|
| MSM:001 | plain-left | title "Memo" (x 36–77 of 400, centre 14.1%). Header block Memo + To/From/CC; boundary = first body paragraph (y 170). The only line ≥ 40% W near the block is the purple top-right bar, x 209–399 = **47.8% W**, 58% of live width (x 35–363). Ruled (a) fails; the footer bar is at the page foot. Band: title on white. No meta on the opposite side → split (a) fails |
| MSM:002 | ruled | title "MEMO" (x 56–197, centre 31.6%) on the white strip, not on the yellow panel → not band. Hairline y 241, x 4–343 = **85.0% W** (a ✓), directly above the body label "COMMENTS:" (y 272), no text between (C45a closing rule). Gap from the last meta line (Re:, bottom y 209) = 32 px = **2.4 body lines** (pitch 13.5 px), so (d) ✓ |
| MSM:003 | plain-left | title "Memorandum" (x 36–129, centre 20.6%); the LOGO placeholder box is excluded. No horizontal line ≥ 40% W on the page (`hl.py` found none). The corner square art is not behind the title. No right-side meta |
| MSM:004 | ruled | title "memo" (x 61–294, centre 44.4%). Orange rule y 243–246, x 53–351 = **74.8% W** (< 80%), but live width x 59–340 = 281 px, so the rule is **106% of live width** (a ✓). Directly above the body label "Comments:" (y 275), no text between. Gap from Re: (bottom y 217) = 26 px = **1.9 body lines** (pitch 14 px) |
| MSM:005 | ruled | **C45(c)**: no MEMO/Memorandum/organisation text, and "replace with LOGO" is excluded, so the title = the largest text in the top 30% = the routing label **"DATE"** (8 px caps, x 346–370, top-right; the TO:/FROM: labels are 6 px). Header block DATE + TO/FROM/SUBJECT/CC; boundary = body paragraph (y 220). Rule y 200, x 28–371 = **86.0% W**, directly above the boundary, no text between. Gap from CC (bottom y 189) = 10 px = **0.4 lines** (header pitch 26 px; only one body line exists). The multicolour triangle bar at the page top (x 11–387 = 94.2% W) would also pass |
| MSM:006 | plain-left | title "Memo" (x 117–191, centre 38.5%). The black rule under it is the closing rule directly above "COMMENTS:" (C45a), but it is y 65–67, x 115–377 = 263 px = **65.8% W** and **74.5% of live width** (x 24–377), so ruled (a) fails. The short rule under the date (x 24–92) is separate. Split (a): the title's left edge is 93 px (26% of live width) from the left margin and its right edge is 186 px from the right margin, so it is not flush → split fails. Centre is 11.5% off → not centred |
| MSM:007 | plain-left | title "Memo" (x 36–76, centre 14.0%). The navy bar at the page top (y 11–25, x 12–357 = **86.5% W**) passes (a). **(d) fails**: the gap from the bar to the header block (title top y 87) = 61 px = **5.3 body lines** at the running-body pitch of 11.5 px (body lines y 254/266/277, 297/308). **BORDERLINE**: at the pitch of the larger blue lead paragraph (15.5 px) the gap is 3.9 lines, which would give ruled. The spheres are an illustration; no other line ≥ 40% W lies near the block. **Changed from r1 (ruled)** |
| OLM:002 | ruled | title = the organisation name "University of Delaware" (A.1 memo row; 17 px, tied with "Title goes here", 17 px; C45(c) takes the org name). Header block = the three organisation lines (y 79–136). Rule y 146–148, x 104–689 = **73.8% W**, **110% of live width** (x 160–694), so (a) ✓. It lies directly below the block, no text between. Gap 10 px = **< 1 line** at any pitch on the page (org lines 20.5 px). Crest excluded. Alternative title "Title goes here" (centre 49.9%): the rule lies above it, and the gap is 63 px ≈ 4.0 lines, borderline |
| OLM:008 | ruled | **C45(c)**: no MEMO/Memorandum/organisation heading; all five header lines have the same size (12–13 px), so the title = the first line, the routing label **"To:"** (x 93–571). Rule y 207–208, x 93–700 = **76.6% W**, **103% of live width** (x 93–681), so (a) ✓. It lies directly below "Section:" and directly above the first body paragraph. Gap 184→207 = 22 px = **1.2 body lines** (pitch 18.7 px) |
| OLM:009 | plain-left | title "Project Memo" (31 px, x 230–411, centre 40.4%). Header block = title + meta rows (VERSION … PROJECT NUMBER); boundary = the body label "Abstract". The only closing line is the hairline under the PROJECT NUMBER row: y 484, x 232–703 = **59.4% W** and **73.8% of live width** (x 68–708, including the sender-address column). Ruled (a) fails. The hairline is #f8f8f8 (ΔL 0.027 from white). The sender-address column is organisation identity (C45b) → no split. Alternative: excluding the address column from live width (x 241–708) the hairline is 101% → ruled |
| OLM:010 | plain-left | title "Memo" (24 px, x 89–166, centre 16.1%). The top-right sender address is organisation identity (C45b) → never split. The hairlines at y 286 (77.6% W) and y 489 (77.8% W) lie **inside** the header block (above the meta rows, and between DISTRIBUTION and PROJECT NUMBER). Nothing lies between the last meta row (bottom y 536) and the first body paragraph (y 558) → no closing rule. Zebra rows L 0.91–0.92 are not fills (C17) |
| OLH:001 | ruled | **C45(c)**: Overleaf logo excluded; no MEMO/organisation text; all header lines have the same font size, so the title = the first line, the routing label **"To:"** (x 96–195). Rule y 316, x 96–697 = **75.8% W**, **100% of live width** (x 96–697). It lies below "Date:" (bottom y 289) and above the first body paragraph (y 343), no text between. Gap 27 px = **1.5 body lines** (pitch 18.5 px) |
| GM:001 | plain-left | title "TUFTE INSPIRED TYPST TEMPLATE" (x 93–485 of 801, centre 36.1%). No horizontal line ≥ 40% W on page 1. The second author block starts at x 408, far from the right edge of the live width (≈ 715), so split (a) fails |
| GM:002 | plain-centered | title = the organisation name "DEPARTMENT OF THE AIR FORCE" (largest text in the top 30%; seal excluded), x 411–812 of 1224, **centre 50.0%** (offset 0.0%). No rule. The title is centred, not flush → split (a) fails |
| GM:003 | ruled | title "RESEARCH MEMO" (x 229–381, centre 49.8%). Running-head rule y 50, x 72–539 = **76.5% W**, **100% of live width** (x 73–541). It lies above the title, no text between. Gap 20 px = **1.3 body lines** (pitch 15.5 px) |
| GM:005 | ruled | title "Memorandum" (14.3 pt, x 259.4–352.6 pt, centre 50.0%); crest excluded. Rule y 236.8 pt, x 72–540 = **76.5% W**, **100% of live width** (x 72–540). It lies between "Date:" (bottom 215.5 pt) and the first body paragraph (257.4 pt), no text between. Gap 21.3 pt = **1.5 body lines** (pitch 14.5 pt). Ruled precedes plain-centered |
| GM:006 | plain-left | title "MEMORANDUM" (14.3 pt, x 72–189 pt, centre 21.3%); logo excluded; no rule. Split: the date "April 25, 2014" (meta) is flush right (right edge 521.2 pt, 23.7 pt = **5.0% of live width** x 72–544.9), but it ends **35.3 pt above** the title (y 134.3 vs 169.6), so (c) fails. The address lines are organisation identity (C45b) |
| GM:007 | ruled | **Title per A.1 top-30% rule**: the top 30% (y < 237.6 pt) holds "CBMM Memo No. 00" and the date (12 pt bold). "Memo Title" (20.7 pt) starts at 34.9% of H, outside it. So the title = "CBMM Memo No. 00" (the memo-number line, containing "Memo"). Rule y 184.6 pt, x 57.6–554.4 = **81.2% W** (a ✓). It lies above the title, no text between (the logo sits above the rule). Gap 36.8 pt = **3.1 body lines** (abstract pitch 12 pt), so (d) ✓. Split would also hold (date flush right on the same line), but ruled comes first |
| GM:011 | plain-centered | title "Document's title" (20.7 pt, x 228.9–366.3 pt, **centre 50.0%**). The running-head rule (y 65.3 pt, x 70.9–524.4 = 76.2% W, 100% of live width) lies above the title with no text between, but **(d) fails**: gap = 75 px = **59.9 pt = 4.1 body lines** (12 pt body, baselineskip 14.5 pt; only one body line exists, so the pitch is the class default). **BORDERLINE** (within 10%) |
| GM:012 | ruled | title "EEEE 381 - Electronics 1 Techical Memorandum" (24.8 pt, 2 lines, left); the missing-image box is a logo placeholder, excluded. Rule y 340.4 pt, x 72–540 = **76.5% W**, ≥ 100% of live width (body/meta text x 72–423). It lies below "Subject:" (bottom 327.4 pt) and above the first body element ("Abstract", 403 pt), no text between. Gap 13.0 pt = **0.9 lines** (meta pitch 14.4 pt). The rule is 63 pt above "Abstract" and belongs to the header block, not to that heading |
| GM:013 | plain-left | **C45(c)**: no title, no MEMO/organisation text; all header lines are 10.9 pt, so the title = the first line, the routing label **"To: Professor Art Vandelay"** (x 162.6–313.4 pt, centre 38.9%, 11.1% off centre). No rule on page 1. No opposite-side meta → no split |
| GM:015 | ruled | title "NOAA Technical Memorandum NOS CS XX" (17.2 pt; tied in size with "Tech Memo Template", and the Memorandum line is taken, A.1). "Tech Memo Template" is not a TO/FROM/CC/DATE/SUBJECT line (A.1 memo row), so it is the first element after the header block. Rule y 114.7 pt, x 72–540 = **76.5% W**, **111% of live width** (x 72–494.5). It lies between the two, no text between. Gap 17.1 pt = **0.95 body lines** (pitch 17.9 pt). Alternative, if the subtitle is read as part of the block: the rule is internal → plain-left |
| GM:017 | plain-centered | the top 30% (y < 252.6 pt) holds only the uk\|SRC logo lock-up (excluded). The largest text on page 1, "Example UKSRC Memo" (25.9 pt, starts at 32.5% of H), is taken as the title and recorded here: x 154.6–440.7 pt, **centre 50.0%**. The metadata table's top border (x 70.9–495.1 = 71.3% W) is < 80% and lies inside the block → not ruled |
| GM:021 | ruled | title "Memorando Nº 02/2017 - DACOM" (10 pt bold; "Memorando" = memorandum; the letterhead lines are 9 pt and are organisation identity, C45b). Letterhead rule (black + yellow) y 93.6–96.4 pt, x 72–523.3 = **75.8% W**, **100% of live width** (x 72–523.3). It lies above the title, no text between. Gap 24.6 pt = **1.3 body lines** (pitch 19.1 pt). Split would also hold (date flush right on the title line), but ruled comes first. **Changed from r1 (plain-centered)**: r1 took the centred organisation line as the title |
| GM:023 | image-hero | the page is the sheet only (macOS window chrome ignored). A starfield photo covers **100%** of the sheet, including the top 20% → C1 image-hero (strict priority). Alternative, if the photo were not a hero: the rule under DATE (x 239–1249 of the 1242-px sheet = **81.4%**, above the salutation, no text between) → ruled. Item is inadmissible (A3) either way. **Changed from r1 (plain-centered)** |

## Value counts (25 items)

- **ruled 12**: MSM:002, MSM:004, MSM:005, OLM:002, OLM:008, OLH:001, GM:003, GM:005, GM:007, GM:012, GM:015, GM:021
- **plain-left 9**: MSM:001, MSM:003, MSM:006, MSM:007, OLM:009, OLM:010, GM:001, GM:006, GM:013
- **plain-centered 3**: GM:002, GM:011, GM:017
- **image-hero 1**: GM:023
- band 0, split 0

Changes vs the corpus-file values (r1), 3 of 25:
- MSM:007 ruled → plain-left ((d) 5.3 body lines);
- GM:021 plain-centered → ruled (title = the "Memorando" line, C45);
- GM:023 plain-centered → image-hero (C1).

Borderlines (C45(d) numbers are above):
- MSM:007: pitch reading;
- GM:011: 4.1 lines;
- OLM:009: live-width reading;
- GM:015: subtitle in or out of the block;
- OLM:002: tie between title candidates, with the same outcome under the first reading.

The corpus file's archetype table is **not** updated here. The re-test decides whether these values stand.
