# research/designs-evidence/memo-second-coder.md — independent second coder (falsifier), 2026-09-24

**Independence.** Coded from `research/82-design-ranking-protocol.md` §4/§5, `research/82a-general.md`
(header treatment + colour use, supersedes §4 for memo), `research/82a-clarifications-1.md`
through `-5.md`, and `research/designs-evidence/memo-items.csv` only. No other file under
`research/designs-evidence/` was opened; `research/91-family-status.md` and
`research/82b-shortfall-sources.md` were not opened. First-coder codes were never seen.

**Item list used.** `research/designs-evidence/memo-items.csv` was read fresh for this task and,
at read time, held **11** rows: `MSM:001…MSM:007`, `OLM:002, OLM:008, OLM:009, OLM:010`. (The
orchestrator flagged that `memo-items-pool.csv` now carries a 12th id, `OLH:001`, an added
Overleaf template — `memo-items.csv` itself did not yet contain that row when it was read for
this task, so the seeded sample below was drawn from the 11 ids actually present in
`memo-items.csv`. `OLH:001` was not coded.)

**Method.** Ids sorted lexicographically from the 11-row `memo-items.csv`. Sample:

```python
import math, random
ids = sorted(['MSM:001','MSM:002','MSM:003','MSM:004','MSM:005','MSM:006','MSM:007',
              'OLM:002','OLM:008','OLM:009','OLM:010'])
n = max(min(10, len(ids)), math.ceil(0.25 * len(ids)))  # = 10
sample = random.Random("82a:memo").sample(ids, n)
```

Previews fetched by `curl -s -A "smart-design-research"`. Microsoft Create `.webp` thumbnails
converted to PNG with Pillow. The Overleaf preview URLs in the csv are S3 links signed for the
template-gallery page only (`AccessDenied` on direct fetch); each template's own page
(`overleaf.com/latex/templates/...`) was fetched instead and its embedded, freshly-signed
`writelatex.s3.amazonaws.com/published_ver/<id>.jpeg` URL extracted and fetched — this is the
item's own published preview per clarification C6 (dead documented path replaced by the item's
own published preview, disclosed). Pixel colours sampled with Pillow; contrast computed with
`skill/document-design-intelligence/scripts/lib/color.py`. Scratch files lived in
`research/designs-evidence/tmp-sc2/memo/` and are deleted at the end of this task.

**Sample (n=10, sorted):** `MSM:001, MSM:002, MSM:004, MSM:005, MSM:006, MSM:007, OLM:002,
OLM:008, OLM:009, OLM:010` (drawn from the 11 ids listed above; `MSM:003` was not selected).

## Coding table

| id | columns | heading class | body class | colour use | header treatment | rules/boxes | density | admissible |
|---|---|---|---|---|---|---|---|---|
| MSM:001 | 1 | serif ("Memo") | sans | fill-blocks (magenta/purple diagonal triangle bands top-right and bottom-right, combined ≈≥10% of the page) | plain-left ("Memo" left-aligned; the decorative band sits in the corner, not behind the title glyphs, so no band; "LOGO" is a bordered placeholder, excluded) | boxes (bordered "LOGO" placeholder) | airy (~15-18 lines) | yes |
| MSM:002 | 1 | serif ("MEMO") | sans | mono (the pale cream/yellow panel measures L≈0.9+ on inspection, excluded as a pale tint per B1e/B1a background; all text is grey/black) | plain-left ("MEMO" left-aligned; the faint rule before "COMMENTS:" belongs to the boundary, excluded per the generalised A2) | rules (the boundary hairline; no bordered box — the cream panel has no visible stroke) | airy (~10 lines) | yes |
| MSM:004 | 1 | sans (bold lowercase "memo") | sans | one-accent (single rust/orange cluster: title, "Comments" label, rule) | plain-left (title left-aligned; the orange double rule sits at the header/body boundary, excluded from the header test) | rules (same rule, no border box) | airy (~9 lines) | yes |
| MSM:005 | 1 | sans (routing labels; no distinct "Memo"/org-name title exists on this template — the largest non-logo text is the "DATE" label / TO-FROM-SUBJECT-CC labels, coded from their font) | sans (instructional line) | fill-blocks ("Prism" low-poly mosaic bands top and bottom, ≥10% combined page area — colour-note: multiple hues present, but the block-area test is met first per §4(a), so the fill-blocks code, not multi, applies) | plain-left (no title text distinct enough to anchor split/centred; "replace with LOGO" is excluded as a logo placeholder and cannot create split) | rules (hairline before the instructional line) | airy (~6 lines) | yes |
| MSM:006 | 1 | sans (bold "Memo") | sans | one-accent (single red cluster: title, TO/FROM/CC/RE labels, "CANEIRO GROUP" footer, contact lines) | split (date "05.26.2023" left and title "Memo" right, opposite sides of the same top line/band; the hairline immediately below sits inside the header block — between the title row and the TO/FROM rows, which are still part of the header per the family row — so it does not qualify as a framing rule ahead of split) | rules (hairline under the title row, hairline above the footer; no bordered box seen) | airy (~15 lines) | yes |
| OLM:002 | 1 | serif (Computer-Modern-style LaTeX default throughout) | unknown (no running body paragraph appears on page 1 — the page is a title/cover block; per the spirit of C7/C25, coded `unknown`, falls back to the family default) | mono (university shield is a logo, excluded; all remaining text is black) | ruled (a full-width black rule sits directly below the "University of Delaware / Department… / Laboratory" header block) | rules (that rule, plus a second rule near the footer; no border box) | unknown (no running text to normalise; falls back to family default) | yes |
| OLM:008 | 1 | serif (Computer-Modern-style LaTeX default) | serif | mono (no colour anywhere; pure black on white) | ruled (a full-width rule sits directly below the To/From/Re/Date/Section block, above the first paragraph) | rules (that rule; no border box) | standard (≈45+ lines of running prose and bullets on the page — close to, but not confidently over, the 55-line dense line; disclosed as borderline-dense) | yes |
| OLM:009 | 1 (the Version/Date/Author(s)/Client(s)/Project-number meta table is a 2-column label/value panel, never a column per C28) | sans ("Project Memo", the larger of the two top lines, matching the family row's "Memo" pattern) | sans (Abstract text) | multi (teal cluster: SINTEF contact block + ISO-certification footer text, several elements; red cluster: the placeholder "Set with \clientref{}" text — 2 clusters ≥30° apart) | split (SINTEF logo + teal contact block occupy the left ~30% of the header band; title + subtitle + meta fields occupy the right ~70% of the same band — logo itself cannot create split, but the teal contact text is not a logo and sits opposite the title) | rules (hairlines between meta-table rows; no full cell borders) | airy (only the one-line Abstract as running text) | yes |
| OLM:010 | 1 (the Person-Responsible/Distribution/Project-number rows are meta-table content, never a column per C28; the vertically-set Attention/Comments/Information/As-Agreed matrix is a small table, not a flowing column) | sans ("Memo") | sans (closing paragraphs) | one-accent (single teal cluster: SINTEF contact block, rotated column headers; no second hue visible on this item, unlike OLM:009's red placeholder) | split (logo top-left, SINTEF contact block top-right opposite the title "Memo", within the same header zone, consistent with OLM:009's layout) | rules (hairlines under each meta/table row and the zebra-striped distribution table; no full cell borders) | standard (meta table + ~4 closing paragraphs, more running text than OLM:009) | yes |

Note on borderline calls (disclosed): OLM:008 density (standard vs. dense, ~45+ counted lines
against the 55-line dense threshold) is close enough that a stricter line count could tip it to
dense.
