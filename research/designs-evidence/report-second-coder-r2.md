# report — second coder r2: `header treatment` under C51 (fresh, independent coder, 2026-09-25)

(Saved verbatim by the orchestrator: the subagent harness blocked the coder's own file write.)

**Independence and exposure.** I am a fresh worker and have never coded report. I read only:
- research/82 §4–§5 and §7;
- research/82a-general.md and research/82a-cv.md;
- research/82a-clarifications-1.md to -8.md;
- the report items csvs (report-items.csv, report-items-github.csv, report-items-ms.csv).

I did not open any report-*.md evidence file, research/82a-report-header-failure.md, any *-agreement*.md file, or report-recode-c51.md. I have seen no first-coder, recoder or r1 report codes.

Exposure:
- **GH:104** is a C51 worked example (82a-clarifications-8), so I read its measured value before coding. Per C12, the orchestrator should also report a sensitivity run that excludes GH:104. I re-measured it independently, and my numbers match the example.
- For MSR:004 and MSR:010, I also opened each item's own source .docx (the `src` of the url in report-items-ms.csv). I used it only for element geometry, not for codes.

**Method.**
- Covers follow C13: the page-1 sheet of each preview. The `pages` column gives 1 for the ARC items.
- **PDFs** (GH:079, 104, 123, 084, 009, 058, 022, 103; ARC25:011, 024, 037) were measured with PyMuPDF:
  - span font sizes and bboxes;
  - image bboxes;
  - vector drawings (type, extent, fill or stroke).
- **Rasters** (GH:067, 031, 138; MSR:004, 010) were measured with PIL:
  - ink row bands with extents and centres;
  - white-panel and fill boundaries, found by pixel scans.
- Every cover was tested for image-hero (C51(a)) first. After that the order was band, ruled, split and plain (82a-general §A.2 with C51(b)–(d)).
- All files were downloaded to the system temp directory, never the repo.
- %W, %H and % area are relative to the cover sheet.
- "FLAG" marks any number within 10% of its threshold (C51(e)).

**Sample.** All 64 ids from the three items csvs (64 unique), sorted, then `random.Random("82a-r2:report").sample(ids, 16)`. My result:
GH:079, GH:104, ARC25:011, ARC25:024, GH:123, ARC25:037, GH:084, GH:067, GH:031, GH:009, GH:058, GH:022, GH:138, MSR:004, GH:103, MSR:010.
This is identical to the expected list.

| id | header | header-note |
|---|---|---|
| GH:079 | plain-centered | Image-hero: no image. The two grey "16x9" boxes are image placeholders (never images; their 22.7 pt text is excluded from title). Title "Analysis of Alien Life Forms..." 24.8 pt. Title-centre offset +2.4% W. Rule candidates: none (placeholder box edges 19.0% W only). Largest rejected image: none (placeholders 19.0% W x 7.6% H, top 11.6% H, not images). |
| GH:104 | plain-centered | Image-hero: no image. Title 17.0 pt, y 66.6–86.0 pt. Title-centre offset 0.0% W. Widest rejected rule candidate: grey panel fill 76.2% W (FLAG, within 10% of 80%), 27.4% H &gt; 5%, so never a rule (d1) and not behind the title (no band). Largest rejected image: none. C51 worked example: sensitivity run needed. |
| ARC25:011 | image-hero | Full-bleed photo, top 1.6% H. Visible area about 92.0% (bbox 92.6% of cover, less about 0.6% for the Petronas logo shape; no panels). Title on the photo. |
| ARC25:024 | image-hero | Full-bleed mosaic painting, top 0.0% H, bbox 100% of cover. Visible area at least 93.2% (only the logo image, 6.8% bbox, sits over it). |
| GH:123 | plain-centered | Image-hero: no image. Title "Laboratory Report #X" 25.9 pt. Title-centre offset 0.0% W. Rule candidates: none (no vector drawings). Largest rejected image: none. |
| ARC25:037 | image-hero | Landscape single sheet (1920 x 1080). Office photo, top 13.9% H, visible 80.8% of the cover. Even if the 12.7% overlay image in the lower left is counted as covering, visible is still at least 68.1%. Title "Sustainability" is set on the photo. |
| GH:084 | plain-centered | Image-hero: no image (the university calligraphy is a vector wordmark, a logo). Title 36 pt. Title-centre offset 0.0% W. Widest rejected rule candidate: field underlines, stroked, 32.3% W (fail d2). Largest rejected image: none. |
| GH:067 | plain-centered | Image-hero: only two logos (crests), top 13.5% H, band 22.5% W x 8.8% H (never images). Title "COMP0000J Intro to Temporal Engineering", cap height clearly the largest. Title-centre offset 0.0% W. Widest rejected rule candidate: stroked grey lines directly above and below the title, 76.5% W (FLAG, within 10% of 80%), fail d2; gap 2.1% H. |
| GH:031 | plain-centered | Image-hero: only the UESTC logo on a pale backdrop box, top 8.8% H, 8.7% area (logo, never an image). Title: two lines of equal size (cap about 28 vs 29 px, within 5%), so the higher one, "电子科技大学 XX 学院", is the title. The second line joins (gap 29 px, well under 2 x 28 px). Title-centre offset -0.1% W. Rule candidates: none. Largest rejected image: the logo above. |
| GH:009 | plain-centered | Image-hero: crest image top 8.6% H, 1.4% area (crest, never an image). Title: Persian line, 24.1 pt. Title-centre offset 0.0% W. Rule candidates: none (no vector drawings). |
| GH:058 | plain-centered | Image-hero: university logo image top 8.6% H, 6.9% area (logo). Title "本科生实验报告" 36 pt. Title-centre offset 0.0% W. Widest rejected rule candidate: field underlines, stroked, 61.9% W (fail d2). |
| GH:022 | ruled | Image-hero: logos only (the largest is 1.8% area). Title: "Graduation Project" and "National Engineering Diploma" are both 24.0 pt, so the higher one, "Graduation Project", is the title (y 183.5–207.5 pt). The block is the title alone (gap to "To obtain the" 32.5 pt &gt; 2 x 14.1 pt). Ruled on a thin black fill above the title: 0.5 pt thick (0.06% H), x 49.5–545.9 pt, drawn as 3 abutting segments with 0.4–0.5 pt gaps, read as one line of 83.4% W (FLAG, within 10% of 80%; the middle segment alone is 54.7% W). No text between. Gap 34.1 pt = 4.05% H, within 7%. Not a table line. Offset 0.4% W if ruled is not taken. |
| GH:138 | plain-centered | Image-hero: no image. "同济大学" calligraphy (139 px tall) is a wordmark, so it is excluded from title. Title "XXXX 课程报告" (46 px band). Title-centre offset 0.0% W (0.0% W also if the wordmark were taken as the title). Widest rejected rule candidate: field underlines, stroked, 43.0% W (fail d2); the subtitle underline is 24.5% W. Largest rejected image: none. |
| MSR:004 | image-hero | Street photo from y = 0 (top 0.0% H) down to the teal band at 66.5% H, full width. The white panel (x 28–230 of 400 px, from 9.2% H) covers part of it. Visible area 37.4% (138,000 - 60,291 px of 207,600). |
| GH:103 | plain-centered | Image-hero: no raster image. The gold top-right swoosh is vector decoration, top 0.8% H, bbox 14.9% W x 21.2% H = at most 3.2% area (fails 30%). The Stellenbosch logo is vector, a logo. Title 23.8 pt (2 lines join). Title-centre offset 0.0% W. Widest rejected rule candidate: maroon bottom fill 91.4% W but 10.04% H &gt; 5%, so never a rule (d1); it is not behind the title (no band). |
| MSR:010 | image-hero | The pale wave line-art is a raster picture ("Picture 1", 540 x 720 pt, behind text), top 4.4% H, bbox 80.3% of cover. The white panel (29.9%) and the white BOOK REPORT box (4.9%) cover part of it. Visible area about 45.5%. Judgement: I treat a textural line-art picture as an image under C51(a), which excludes only logos, placeholders and charts. If it is not an image, the fallback would be plain-centered: the title box edges are 68.5% W (fail d2), offset 0.0% W. |
