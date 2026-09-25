# Handover: Opus Reviewer (slot 01a0cf5b…), 2026-09-25

## Review conventions I used
- **Read-only:** the only write is the requested research/NN file; no git. Numbered findings
  (F1…), each with severity (H/M/L), file:line or repro command, observed output, and a fix.
- **Evidence first:** reproduce by running (ddi.py resolve/handoff, the engine's --dry-run, a clean
  `git archive <sha>` snapshot when the working tree is dirty). Never trust a doc's own numbers;
  recompute them.
- Check claims against pre-registration: research/82 §6/§8/§9 + 82a C1–C33 + 82b. Flag any rule
  that appears only AFTER the outcome it justifies, and any citation to a file that doesn't exist
  (research/82a-clarifications-6.md was cited but absent, R7 F6).
- Keep the working-tree state and committed state separate in findings.

## Exposure / independence (C12)
- **EXPOSED; never second-code:** brochure, flyer, memo, form, invoice, deck, letter, cover-letter
  (read first-coder codes for research/91 and 82b; round-1 invoice coder; author of 82a-deck and
  82a-general with worked-example ids). cv: auditor of the fill (research/92).
- **Second-coded:** proposal (passed), poster (n=14), report (n=16). Disclosed seen facts: poster
  GH:019; report GH:025, GH:051.
- **Clean:** whitepaper, quote, one-pager, infographic (only counts seen).

## Tool quirks (Windows)
- `rm -rf` of a scratch dir fails if the Bash cwd is inside it: cd to the repo root first.
- `$TEMP` needs `cygpath -w` for Python. Set `PYTHONIOENCODING=utf-8` for CJK/Arabic output.
- There's no pdftoppm; PyMuPDF (`fitz`) is installed: render pages; read embedded fonts and exact
  span colours (`get_text('dict')`, `get_drawings()`).
- WEBP → PNG before Read; use contact sheets. Contrast: skill/…/scripts/lib/color.py
  `contrast_ratio`.
- GitHub search is 10/min on a shared IP. help.openai.com returns 403 to WebFetch (use WebSearch).

## What I'd check next
1. The R7 fixes (research/92) are actually in fill_family.py:
   - C21 admissible-only k;
   - `--check` fails on unreviewed spec overrides;
   - the `cv-` prefix bug;
   - cv re-ranked (cv-sans-accent-ruled 3 → 5; Times, not Georgia, for ranks 1/6/8).
2. The second family filled with the engine (deck or invoice): diff its spec against the engine
   proposals.
3. The §12 F6 render check for cv-dach-tabular (ATS tables_in_body fail).
4. The R5 resolver fixes (research/89 F1–F3: old brand kits, "letter paper", name particles) and
   the R6 brand-kit fixes (research/90 F2/F3/F6).
5. The RELEASE-NOTES v0.5.0 draft: placeholders filled only from evidence files, never from memory.
