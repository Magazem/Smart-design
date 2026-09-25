# Handover - Design Researcher (slot 01a0cf5b), 2026-09-25

## Tool quirks (Windows, Git Bash + PowerShell)
- Python default stdout is cp1252: prefix `PYTHONIOENCODING=utf8` or write to files with `encoding='utf8'`; CJK/Persian repo names crash `print`.
- Bash heredocs with an odd number of `'` inside python -c fail silently ("unexpected EOF"): write scripts with the Write tool, then run them. Scratch scripts lived in `%TEMP%\gh\` (prev.py preview finder, tree.py github.com repo-root scraper, dl.py downloader, rp.py PDF page-pair renderer, sheets2.py contact sheets, gen_fam.py corpus generator + `<family>_data.py`). They are not in the repo.
- `rm -rf` on a dir that is the shell cwd fails ("busy"): cd out first or use PowerShell Remove-Item.
- Image `Read` calls sometimes return "media removed: request limit" after long batches; re-read a smaller sheet.
- GitHub search API (unauthenticated, 10/min): 8 s sleep worked; one call per query, per_page 100, page 2 for ranks 101-200. github.com HTML root pages (not the API) list committed PDFs/PNGs when the README has no image; raw.githubusercontent.com is not rate-limited.
- Typst Universe thumbnails: `https://packages.typst.org/preview/thumbnails/<name>-<version>.webp`; index at `/preview/index.json`. Microsoft Create thumbnails are static webp URLs inside the cloud.microsoft payload. LibreOffice extension pages carry `/assets/screenshots/...` images.
- color.py: `skill/document-design-intelligence/scripts/lib/color.py` `contrast_ratio(hex_fg, hex_bg)`; sample from renders only, values are estimates (C9).

## Conventions I settled on (all disclosed in the evidence files)
- Cover-page families (report/proposal/whitepaper): coded from cover + first >=250-word page, `fb` = fallback (contents/sample page) flagged per item.
- Header/colour per 82a-general everywhere after 2026-09-24; header codes on very few items are `ruled`/`band` (mostly plain-left/centred).
- Previews: never copy artwork into the repo; scratch only in temp.

## Independence / exposure status
- I first-coded: cv GitHub+NPM (+ header recode r2/r2a), deck LO/MS, brochure, flyer, memo/form (earlier), poster (MS + GitHub + A1 pool), report (ARC L3 + GitHub), cover-letter GH, letter GH, proposal GH, whitepaper GH, quote GH, memo GH additions. I must NOT second-code any of these.
- I second-coded infographic only (never opened infographic-corpus-iib.md or research/91). I have seen no infographic first-coder codes. I saw only the CV header recode of my own.

## Half-done / caveats
- None open on the board. Known weak spots: poster A5/A3 borderlines (PM:003, pasquino), letter/cover-letter header notes, report `fb` running pages, proposal cover=no items coded from one page.
- Not reconstructed: NISO Z39.18 / APA 7 authority fetches (blocked, Incapsula/404); no `authority:` rows exist for report/whitepaper.
- Possible follow-ups the orchestrator may want: whitepaper merge into whitepaper-corpus.md (I wrote whitepaper-corpus-github.md separately); 82b A5 borrow whitepaper<-report; tuhi-alumni-vuw thumbnail never viewed.
