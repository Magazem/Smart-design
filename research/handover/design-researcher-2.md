# Handover — Design Researcher 2 (2026-09-25)

## Exposure / independence per family (do not second-code these)
- **Coded or recoded by me:** cover-letter + letter (L2 first coder; C22/C19 recodes), deck (round-2 recoder, `deck-recode.md`), quote (all 3 items), whitepaper (WPL:001, WPO:001, plus blind codes of saboyle/mlouhivu).
- **Re-checked:** report L3 (ARC, R.8).
- **Read codes of (analysis only, never coded):** brochure, flyer, memo, form, poster, invoice, infographic. I read their agreement / recode / second-coder files for `82a-gate-failures.md`, so I am NOT a clean second coder for them either.
- **Clean:** cv, proposal, one-pager, and the GitHub corpora of any family.

## Tool quirks (Windows + Git Bash)
- **Bash heredocs break** on some content (apostrophes / long `python3 - <<'EOF'` blocks give "unexpected EOF"). For long scripts or markdown, write a file with the Write tool, then run `python3 file.py`.
- `/tmp` in Git Bash = `C:\Users\yazan\AppData\Local\Temp`. Python is Windows-native: use relative or `C:/...` paths, never `/tmp/...`, inside Python. `cygpath -w` converts.
- Set `PYTHONIOENCODING=utf-8` when printing non-ASCII (cp1252 crashes).
- numpy had to be pip-installed; PyMuPDF (`fitz`) and PIL are available; no pdftoppm.
- Long regexes over minified JS hang (catastrophic backtracking): restrict to css/vue/json and split on `}`.
- Overleaf gallery: `q=` is ignored; tags that don't exist fall back to "Journal articles"; paging throttles (403), so retry slowly. S3 preview links are signed per page (fetch the template page, extract `writelatex.s3...published_ver` jpeg) or use the template `.pdf` URL.
- MS Create: the per-app sitemaps `{word,excel,powerpoint}.cloud.microsoft/create/sitemap.xml` list every category; the static payload holds cards (regex on `office-template-grid-card`). Microsoft `.pptx` parts can have non-standard names: resolve via `presentation.xml` rels (targets may be absolute `/ppt/...`).
- LibreOffice `.otp` title font: first `*-title` style → `style:font-name` → `style:font-face svg:font-family` (`fo:font-family` there is the bullet font).
- Contrast on published PDFs: redact the text layer (`apply_redactions`, images kept), re-render, sample under each span, compare with the span's exact fill colour.

## Conventions I relied on (now ratified)
- C17–C22, C24 (items csv `pages` column), C28 (routing blocks never columns), C29 (thresholds literal), C32 (faint watermark).
- Deck: 82a-deck §6.2 says the gate uses the FULL sample, not the sensitivity run.

## Half-done / open
- `82a-gate-failures.md` is a **DRAFT** awaiting orchestrator ratification. Its deck section needs an independent check (I am the deck recoder).
- The rulings propose C33–C41 → `82a-clarifications-6.md` if ratified, with re-test seeds `"82a-r2:<family>"`.
- Whitepaper pooled N = 10 (the GitHub worker's 8 + WPL:001 + WPO:001). The pooled frequency table is not computed: the orchestrator must merge (I never read the GitHub codes).
- Quote / whitepaper A5 borrowing is planned, not done: it runs after invoice / report ship. Re-run the key comparison then.
- `deck-agreement-r2.md`'s "net statement" (sensitivity governs) contradicts 82a-deck §6.2 and still needs correcting by whoever owns that file.
