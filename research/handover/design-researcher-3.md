# Handover — Design Researcher 3 (2026-09-25)

## Independence / exposure status per family (for second-coder assignments)
- **Clean (never saw first-coder codes):** invoice, cover-letter, whitepaper, cv, deck, brochure, poster-github, report-github.
- **Exposed (first-round codes seen on 2026-09-23 while reading `letter-corpus-l2.md` as a format precedent):** letter. Directly seen: rows MSL:001-004. Seen as exemplar ids in its frequency table: MSL:003/005/009, LOL:001/007/008/011/021/022/027/029/032/033/039/043/044/046, MSL:007/008/010/011/013/015/016/019, LOL:010. Disclosed in `letter-second-coder.md` §3.
- **First coder of (cannot second-code):** infographic (IIB pool), memo (A1 pool + L3), form (Fm.8 ABS/NHS), report MS (`report-corpus-ms.md`), proposal MS, flyer F.11 recount, poster P.4, one-pager.
- Also partly read as format precedents: `brochure-corpus.md` (full), `flyer-corpus.md` F.3/F.5 (codes seen), `poster-corpus-ms.md`, `memo-corpus.md`, `form-corpus.md`, `report-corpus-l3.md` (ARC codes seen). So also **exposed**: brochure, flyer (MS F.3), report-ARC.

## Tool quirks
- **Microsoft Create:** category pages at `https://{word,powerpoint,excel}.cloud.microsoft/create/en/<slug>/` are static. Slugs come from `…/create/sitemap.xml`. Cards: regex on `data-testid="office-template-grid-card"` (a parser of mine lived in temp; easy to rewrite). Thumbnails exist only at `/thumbnails/400/` (800/1024 give 404) and show **page 1 / cover only**. The `.docx`/`.pptx` is downloadable from the `src=` of the view.officeapps link; read `word/theme/theme1.xml` (major/minor fonts, accent hexes) and `document.xml` (`w:cols`) for declared values (C25).
- **PowerPoint "business-proposal-templates" and "infographic-maker"** hold decks/infographic posters, not documents.
- **No poppler on this machine.** `pdftotext` exists; rendering uses PyMuPDF (`pip install pymupdf`, approved): `fitz.open(f)[0].get_pixmap(dpi=90).save(...)`. `get_fonts()` gives the embedded font names (declared class).
- **Overleaf:** template page images are **signed** S3 URLs that expire; put the template page URL in items csvs. Nonexistent tags return an empty gallery (0 items).
- **Typst Universe:** index at `https://packages.typst.org/preview/index.json`; thumbnails at `https://packages.typst.org/preview/thumbnails/<name>-<ver>.webp`.
- **IIB showcase:** `data-random-order` means page order is not stable. No 2020/2021 editions exist.
- PIL is available but numpy is not. My 82a-general measurement helpers (modal background on a 20×20 grid; fill blocks via MinFilter/MaxFilter opening with a square of side 5% of the short side; hue bins; horizontal-run finder) were temp scripts. They are ~60 lines and easy to rewrite.
- Large images (>2 MP) make pure-PIL pixel loops time out (>120 s). Downscale to ≤700 px first.
- **Scratch dirs inside `research/designs-evidence/` got emptied by someone else mid-task** (tmp-sc7). Use the system temp dir (`/tmp/...`) instead. Deleting a repo scratch dir fails ("Device or resource busy") while the shell cwd is inside it; cd out first.

## Conventions I applied (ratified unless noted)
- C28: routing/address blocks never make columns. C30: charts are marks, never image-hero.
- Transparent PNGs are composited on white. Mock-up canvases and browser chrome are ignored.
- C4 is applied to icon glyphs bulleting contact lines (cover-letter GH:042/067/079). **Not separately ratified.**

## Half-done / open
- Nothing half-done.
- Open rulings I raised:
  - `report-corpus-ms.md` RM.8 was settled by C25.
  - The IIB "charts are marks" reading was ratified as C30.
  - The flyer A1 pool (LO + Typst + GH) and the poster A1 pool are left to the GitHub worker (C27).
