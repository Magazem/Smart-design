# brochure — fresh colour recode under C42 (r2)

Coder: Design Researcher (fresh context, 2026-09-25). Rules used: research/82 §4-§5, 82a-clarifications-1..5 and 7, 82a-general (B1-B6, §C), 82a-gate-failures §10 only (C42 = old C33). I did not open any `*-agreement*`, `*-second-coder*`, `brochure-recode-82ag.md` or `flyer-recode-82ag.md`, and did not read gate-failures §1-§9.

Items: the 11 rows of `brochure-items.csv` (one preview each, 400 px webp / LO png of the outside spread). Only `colour` is recoded; nothing else is touched.

## Method
- **Background (B1a / C42):** 20x20 grid over the whole outside-spread preview. Points on photos/illustrations (hand-set rectangles) and on text (local 7x7 std > 14) are dropped. Classes per 82a-deck §2 (achromatic: ΔL <= 0.03; otherwise hue within 15 deg and ΔL <= 0.05). The class with most points is the background. **Saturation, brand colour or "design intent" never demote it** (MSB:005 and MSB:008 follow this literally). Elements whose core is in the background class are not counted as hues either (the class is excluded from every test).
- **Fill blocks (B3):** non-background, L <= 0.90 area that contains a rectangle with shorter side >= 5% of the spread's shorter side (20 px at 400 px). Measured as connected areas that survive a 9 px opening and then contain a 20 px square. Photos, illustrations, text and L > 0.90 tints excluded. `fill-blocks` if >= 10% of the page.
- **Hues (B4-B6)** for the rest: S >= 0.20, 0.12 <= L <= 0.90, strokes < 2 px achromatic (B2), a hue counts if >= 2 elements or one element >= 0.5% of the page, clusters by single linkage at 30 deg.
- Preview resolution is 400 px: block coverage figures are estimates (+-1.5 points). Items within 2 points of the 10% line are marked BORDERLINE with the alternative.

## Result

| id | colour | colour-note |
|---|---|---|
| MSB:001 | fill-blocks | bg #77a6ad (98/175 valid points; navy #113b53 53, white 24); fill-block coverage 20.3% (navy panel + house panel; photos excluded) |
| MSB:002 | fill-blocks | bg #0e1440 (177/233); fill-block coverage 29.0% (pink/blue/orange blobs, lighter-navy panel #1f2052); non-navy blobs alone 31% raw |
| MSB:003 | one-accent | bg #262626 (113/123); fill-block coverage 7.1% (red #a12934 circle only; 9.8% raw incl. thin stuff) so no fill-blocks; one hue cluster (red ~352 deg, one shape >= 0.5%); logo box and food photos excluded (B1b) |
| MSB:004 | fill-blocks | bg #faf5db (107/224; #fefaf2 is a separate class with 42); fill-block coverage 23.7% (orange #fdbf62 panel ~20% opened); chef photo, title glyphs and pomegranate clip-art excluded |
| MSB:005 | one-accent | bg #c85002 (orange, 86 pts; white 73, so orange is the class, saturation does not demote it); fill-block coverage 3.5% (peach chevron #fddac0, L 0.87); one cluster ~25 deg (chevron >= 0.5%); photos excluded. SENSITIVITY: if white were the background the orange panels would be ~35% = fill-blocks. Literal B1a gives orange |
| MSB:007 | fill-blocks | bg #ffffff (112/166); fill-block coverage 23.4% (purple #4a2986 panel ~20% opened); photos and balloon line-art excluded |
| MSB:008 | mono | bg #e3c220 (yellow, 110/150; white 40); fill-block coverage 0.0% (white L > 0.90 is not a fill; photos excluded); every remaining element is achromatic. The yellow "LOREM IPSUM" heading is in the background class so is excluded; if it were counted it would be one-accent (2 lines) |
| MSB:009 | fill-blocks | bg #fefefc white (194/219); fill-block coverage ~11.5% (blue/lavender blobs #5e73b5 / #a0afda by hue, opened 15 px; red-tinted swimmer photo excluded). BORDERLINE: 8.9% if the photo's whole bounding box is cut out; alternative would be multi (blue + red blob/hatch) |
| MSB:010 | fill-blocks | bg #0b3555 (171/207); fill-block coverage 13.9% (light-teal footer band #8bc8cc ~10%, plus starburst mid-blue); circle photos excluded |
| LOB:003 | mono | bg #ffffff (282/282); fill-block coverage 0.0%; black text, dashed fold guides, red spell-check underlines are editor artefacts (B1d); CC badge achromatic |
| LOB:004 | multi | bg #ffffff (195/203); fill-block coverage 2.1% (arrow tabs); two clusters: orange ~15 deg (title, "for sale", price, feature lines, rules: many elements) and blue 203-240 deg (light-blue + navy tabs, blue/navy text, blue page frame); photos and map excluded |

## Value counts (11 items)
fill-blocks 6 (MSB:001, 002, 004, 007, 009, 010) | one-accent 2 (MSB:003, 005) | multi 1 (LOB:004) | mono 2 (MSB:008, LOB:003).

## Disclosure
- Judgement calls that move a value: MSB:005 (background = orange), MSB:008 (yellow class excluded), MSB:009 (blob area ~11.5% vs 8.9%), MSB:003 (7.1%, under the line).
- No preview art was copied; scratch files were in the system temp dir.
