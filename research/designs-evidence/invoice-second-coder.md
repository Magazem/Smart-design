# invoice — independent second coder (research/82 §7)

Coder: Opus Reviewer, 2026-09-24.

## 1. Method

**Inputs read:**
- research/82 §4 (rubric, including the invoice features `totals position` and
  `table rules`) and §5 (admissibility);
- 82a-clarifications-1…4;
- `research/designs-evidence/invoice-items.csv` (id, name, url, preview_url).

**Not read:** `invoice-corpus.md` or any other invoice evidence.
- Exposure disclosure (C12): during an earlier, unrelated task (research/82b) I ran one
  `grep` for section headings over `designs-evidence/invoice*.md`. It printed no lines from the
  invoice file, so no first-coder codes were seen.
- I also authored research/82a-deck.md. It is deck-only and was not applied here. 82a-cv.md
  is cv-only and was not applied either; header treatment follows §4 as written.

**Previews:** the first `preview_url` of each sampled item, downloaded to `tmp-inv2/` and viewed
there. That folder is deleted at the end.
- GH:075's preview is an example PDF. Page 1 was rasterised with PyMuPDF to view it (viewing a
  published preview, per §3.3; nothing was compiled). Its embedded fonts are Calibri and
  Calibri-Bold; the letterhead is a raster image.
- Hues were checked with PIL pixel sampling (§4 chromatic test: S ≥ 0.20, 0.12 ≤ L ≤ 0.90).
- One contrast value was computed with `scripts/lib/color.py contrast_ratio` (C9).

**Readings applied (disclosed):**
- **R1. Logos are excluded from `colour use`.** This covers placeholder brand logos: GH:004,
  GH:054, GH:075, GH:097. They are brand art, not text, rules or marks. Counting them would
  turn GH:054 and GH:097 into one-accent.
- **R2. The page is the document sheet.** Browser chrome, the web canvas and the card shadow
  are ignored (GH:030, GH:097, GH:119).
- **R3. Editor/UI elements are ignored (C20).** This covers "Print" and "Imprimir" buttons and
  editable input shading (GH:090, GH:097, GH:119).
- **R4. Fills are L ≤ 0.90 (C17).** Page tints and pale greys above that are not fills
  (MS:001 page `#F3F3F7`; GH:027 grey bars).
- **R5. The heading is the largest text on page 1.** For invoices that is usually "INVOICE"
  or the business name.
- **R6. Admissibility:** C7 (`table rules = all-cells`) is a fail for invoice.

## 2. Sample

Ids from `invoice-items.csv` (48 coded ids), sorted, then
`random.Random("82:invoice").sample(ids, max(min(10, len(ids)), math.ceil(0.25*len(ids))))`
gives n = 12:

`GH:075, GH:004, GH:054, GH:027, GH:119, GH:030, GH:090, MS:001, MS:005, MS:007, MS:006, GH:097`

## 3. Coding table

| id | name | columns | heading | body | colour | header | rules/boxes | density | totals position | table rules | admissible |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GH:004 | edisonneza/jspdf-invoice-template | 1 | sans | sans | mono | ruled | rules | dense | right-bottom | row-hairlines | yes |
| GH:027 | YasinDehfuli/Financial-Factor-Template | 1 | sans | sans | mono | plain-centered | boxes | standard | full-width-bottom | all-cells | no — C7 |
| GH:030 | mdbootstrap/bootstrap-invoice | 1 | sans | sans | mono | plain-centered | rules | airy | right-bottom | row-hairlines | yes |
| GH:054 | my-dao/Salesforce-PDF-Invoice-Template | 1 | serif | serif | mono | ruled | boxes | standard | right-bottom | all-cells | no — C7 |
| GH:075 | sudhakar0897/ExcelInvoice | 1 | sans | sans | one-accent | ruled | boxes | standard | right-bottom | all-cells | no — C7 |
| GH:090 | amattu2/invoice-template | 1 | sans | sans | fill-blocks | band | rules | standard | other | header-and-total | yes |
| GH:097 | BrangyCastro/invoice-template-react | 1 | sans | sans | mono | plain-left | rules | airy | right-bottom | row-hairlines | yes |
| GH:119 | kawshar798/Modern-simple-html-invoice-template | 1 | serif | serif | mono | ruled | rules | standard | right-bottom | row-hairlines | yes |
| MS:001 | Sales invoice (simple lines design), purple | 1 | serif | sans | mono | ruled | boxes | standard | right-bottom | header-and-total | yes |
| MS:005 | Simple business invoice ("HLP Manufacturing") | 1 | sans | sans | one-accent | plain-left | rules | standard | right-bottom | row-hairlines | yes |
| MS:006 | Modern corporate purple & black timesheet invoice | 1 | serif | serif | fill-blocks | ruled | none | airy | right-bottom | none | yes |
| MS:007 | Service invoice (blocky design), gray ("Create & Co") | 2-sidebar | sans | sans | fill-blocks | plain-left | rules | standard | full-width-bottom | row-hairlines | yes |

### Per-item notes

- **GH:004** — "Business Name" (Helvetica), right-aligned opposite the logo. A full-width rule
  sits directly below the header block, so `ruled` wins over `split` by priority. 15 two-line
  rows put it at ≥ 55 lines. Logo excluded (R1).
- **GH:027** — Persian RTL pro-forma invoice; the face has no stroke contrast (sans). Title
  centred; the X logo is not a title. The grey section bars are L ≈ 0.94, so not fills (R4) and
  not rules. Every table cell is a rounded bordered box: all-cells, so C7. The only total is
  the "sum in words" row spanning the table.
- **GH:030** — The card is the sheet (R2). Centred "Thank for your purchase". Row hairlines,
  plus a heavier rule above and below the total.
- **GH:054** — Serif "INVOICE" centred, with a full-width rule below the date line (ruled).
  Fully bordered table: all-cells, so C7. The sun logo is excluded (R1).
- **GH:075** — The letterhead is raster: a heavy sans company name in blue (hue bin 180°; the
  only chromatic hue outside the logo). The page is framed, and the header block's frame bottom
  is a full-width line (ruled). The goods table has every cell bordered: all-cells, so C7.
  Families visible: Calibri, a Times-like face in the raster address lines and a heavy sans, so
  3 in total, which does not trip A1.
- **GH:090** — `#4285F4` band is 18.7% of page height at full width (band, fill-blocks). It is
  not an A7 Office blue. White contact lines on the band measure **3.56:1**. A6 is written for
  body text; these are header meta lines, so they are not excluded here, but the value is
  disclosed. "Total Due" sits top-right above the table, so totals position is `other`.
  Grey section fills plus a blue rule over the header row and rules above subtotals give
  header-and-total.
- **GH:097** — No title text; the largest text is the bold labels (sans). Meta is left and the
  React logo right; a logo never makes `split`, so plain-left. The green button is UI (R3).
- **GH:119** — POS receipt layout. "Store logo / Store Name" in bold Times, centred, with a
  full-width rule below the address block (ruled). The red "Print" button is UI (R3).
- **MS:001** — Page tint `#F3F3F7` (R4), so mono. Serif "INVOICE". The bordered company box
  starts directly below the title, which gives ruled (a full-width line directly below the
  header). Header row and TOTAL are boxed; item rows are unruled with a closing rule, so
  header-and-total. Bordered blocks are ≤ 50%, so not A8.
- **MS:005** — Heavy sans "INVOICE". Crimson labels (hue bin 330°) are the only chromatic hue:
  one-accent.
- **MS:006** — Purple top and bottom bands plus lavender header and total rows exceed 10% of the
  area together, so fill-blocks. The top band runs full width directly above the header block
  with no text between: `ruled` comes before `split` in §4 priority (company left, "INVOICE"
  right). Zebra fills only, no lines, so table rules `none` and rules/boxes `none`.
- **MS:007** — Dark "CC" monogram block, dark description column, orange totals band and a
  grey left panel: fill-blocks. The left panel (Salesperson/Job/Payment/Due Date, about 22% of
  width) is secondary content in a narrow column, so 2-sidebar (C1 is cv-only and does not
  apply). No fill behind the name, and no rule or split, so plain-left. The totals band spans
  the table width (full-width-bottom).

Summary: 12 coded, 3 inadmissible (all C7: GH:027, GH:054, GH:075), 9 admissible.
