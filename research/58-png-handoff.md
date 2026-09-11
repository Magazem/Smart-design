# 58 — png handoff builder (task 01a0902f)

## The defect
`_FORMAT_BUILDERS` (`scripts/ddi.py`) covered `docx`, `pptx`, `pdf` only. `infographic`'s
only render target is `png-social` (`Format: png`), and `data/base/doctypes.csv` shows it is
the *only* shipped doctype that references `png-social` at all — so this family had no
handoff path whatsoever. The CLI (`ddi.py handoff --format`) rejected `png` outright
(`choices=("docx", "pptx", "pdf")`).

## What the builder emits
CSS/pixel idiom throughout — px dimensions, `#`-prefixed hex — not docx's DXA/half-points and
not pdf's mm `@page`; the render pipeline is a headless-Chromium **screenshot** of a
fixed-size window, which has no page at all. `_build_png_lines` (new, mirrors the existing
`_build_docx_lines` / `_build_pptx_lines` / `_build_pdf_lines` shape):

- **canvas** — px width/height, parsed from the render target's own `Engine Invocation`
  `--window-size=W,H` flag. This is `png-social`'s only source for its dimensions
  (`--window-size=1080,1350`); nothing is invented. If the flag is absent or its value
  doesn't match `\d+,\d+`, the line says so explicitly (`"--window-size not found or
  unparsable in Engine Invocation (...)"`) instead of silently emitting nothing or a
  fabricated size. Covered by a direct unit test against a synthetic render row with a
  deliberately broken invocation, since no shipped row is malformed on purpose.
- **font-face** — same embed-vs-safe-stack branch as the pdf builder, reading `Font Rule`.
- **font sizes** — px, converted from the resolved `type-scales` rows at 1pt = 96/72px (the
  CSS specification's own fixed ratio; commented `UNSOURCED` from research/23, same tag the
  file already uses for conventions research/23 doesn't cover, since a screenshot pipeline
  isn't one of its exported excerpts). Px, not pt, because the canvas itself is already
  px-native — pt would be the wrong unit for this target, not just an unconverted one.
- **sections** — reused `_sections_lines`, unchanged, same as every other format.
- **palette** — hex with the leading `#` kept (CSS convention; pptx is the one format that
  strips it).
- **paged media** — an explicit `NOT APPLICABLE` line: `png-social`'s `Supports Paged Media`
  is `n/a` and `Print Tier Max` is `none`, so bleed/crop-marks/`@page` constructs never apply
  to this format. Stated, not omitted — the exact rule that made the pdf gap (`research/51`
  D2) and `infographic`'s blank `Structure Key` (D4) invisible before.
- **render command** — engine + path + invocation, same shape as the pdf builder (png, like
  pdf, is rendered by this project's own pipeline rather than handed to a built-in skill).

CLI: `--format` now accepts `png` (`choices=("docx", "pptx", "pdf", "png")`). The workflow
text in three places — `ddi.py`'s module docstring, `WORKFLOW_STEPS` (what `ddi.py` with no
args prints, and what `SKILL.md` quotes verbatim), and `SKILL.md` §Workflow step 4 — all
updated from `docx|pptx|pdf` to `docx|pptx|pdf|png` so they stay in sync (no test enforces
this match, but the module's own comment says they must not drift).

## Real output (`infographic`, the only doctype this can be exercised against)

    python3 scripts/resolve.py --doctype infographic --json > resolved.json
    python3 scripts/ddi.py handoff --json resolved.json --format png

```
HANDOFF (format=png)
  canvas (CSS px -- parsed from the render target's own Engine Invocation --window-size flag; a screenshot has no @page):
    headless-chromium: 1080px x 1350px
  font-face (CSS idiom, embed vs. safe-stack per render target's Font Rule):
    (not present in this resolution)
  font sizes (CSS px -- 1pt = 96/72px; the canvas above is already px-native, so px is the right unit here, not pt):
    (not present in this resolution)
  sections:
    (not present in this resolution)
  palette (CSS hex colour, '#' kept):
    (not present in this resolution)
  paged media (bleed / crop marks / @page): NOT APPLICABLE -- png-social's Supports Paged Media is n/a and Print Tier Max is none; a screenshot has no pages
  render command:
    headless-chromium: /opt/google/chrome/chrome --headless --no-sandbox --disable-gpu --screenshot=%o --window-size=1080,1350 %i
  constraints to preflight: (none found)
next: python3 scripts/preflight.py <rendered-file>.png
```

## Why font-face / font sizes / sections / palette are empty here — and why that's correct
`infographic`'s `doc-reasoning` row, `infographic-scaffold`, has empty `Style Key`,
`Palette Key` and `Typeface Key` (and `infographic`'s `Structure Key` on the doctype row is
also empty) — that's D4 in `research/51-invoked-quality.md`, a separate, already-tracked
defect, out of this task's scope. The builder correctly reads whatever the resolution graph
hands it; there is nothing to read yet for this family's typography, colour or structure.
What matters for THIS task is that the headers still print with `(not present in this
resolution)` rather than the whole block being missing — proven by a test that walks all four
sections and asserts every value line equals `ddi.NOT_PRESENT`, none silently absent.

## Does `infographic` now meet the v0.3 standing rule?
**Not fully.** The render pipeline itself is complete: `infographic` has a doctype row, a
page-format row, a render-target row, and now a handoff builder that speaks that render
target's own vocabulary and never fabricates or silently drops a concept. But the standing
rule requires "a good result when the skill runs," and `infographic` still ships with no
typeface, no palette and no structure/headings reaching the handoff — a model calling this
skill for an infographic gets dimensions and a render command and nothing to actually design
with. What stands between it and meeting the rule is D4: author `infographic-scaffold`'s
`Style Key` / `Palette Key` / `Typeface Key`, and give `infographic` a `Structure Key`. That is
data authoring on `doc-reasoning` / `doctypes` via `research/load-base.py`'s draft inputs, the
same shape of fix as PART A above, not a `ddi.py` change — flagging it rather than expanding
this task's scope.

## Proof
Gate unchanged by this part (no data touched): `python3 scripts/validate_data.py data/base` →
`OK: validated 14 table(s), 425 row(s)`. Full suite: `python3 -m pytest -q` →
**169 passed, 72 subtests passed** (was 164/68 before this part; +5 tests / +4 subtests, all
new, all for the png builder — none of the pre-existing tests changed).

## Files touched
- `scripts/ddi.py` — `PT_TO_PX`, `WINDOW_SIZE_RE`, `_px_from_pt`, `_parse_window_size`,
  `_build_png_lines`; `_FORMAT_BUILDERS["png"]`; `--format` choices; three workflow-text
  strings; module docstring's format-vocabulary sentence.
- `scripts/tests/test_ddi.py` — `TestPngHandoffBuilder` (5 tests: real canvas/render-command
  data, explicit paged-media NOT APPLICABLE, degrade-not-omit on all four empty sections, CLI
  accepts `png`, `_parse_window_size` unit coverage for absent/malformed input).
- `SKILL.md` — step 4's format list (body prose, not the frontmatter `description` field; no
  ZIP rebuild triggered, none taken).

## Report
Png builder emits: canvas (px, from Engine Invocation), font-face, font sizes (px), sections,
palette, paged-media (explicit N/A), render command — CSS/pixel idiom throughout, no
docx/pdf units. Infographic meets the v0.3 standing rule: **NO** — D4 (empty
Style/Palette/Typeface/Structure Key) is the remaining gap, out of this task's scope. Pytest
green: **YES** (169 passed, 72 subtests).
