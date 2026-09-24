# Brand-kit builder -- procedure for an AI

Goal: turn a person's brand into a `brand.md`, build and merge the kit, and prove it works.
Every choice below comes from a row of the library (`scripts/ddi.py library ...`,
`scripts/ddi.py designs ...`), not from taste. Run everything from the skill directory.
Without code execution, follow the same steps by hand from `portable/DDI-LIBRARY.md`'s
`## Grand library` (see `portable/AGENTS.md` step 7) and hand the user the finished `brand.md`.

## 1. Interview (ask, then wait)

Ask only what you cannot infer, in one message:
1. Field / industry, and the brand's name (it becomes the `slug`: lowercase letters, digits, `-`).
2. Three tone adjectives (e.g. formal, precise, warm).
3. Existing brand colours (hex) and logo, if any. Existing fonts, if any.
4. Audiences (clients, regulators, candidates) and languages (en/fr/de have authored headings).
5. Document families needed: cv, cover-letter, letter, memo, form, brochure, flyer, poster,
   report, whitepaper, proposal, quote, invoice, deck, one-pager, infographic.
6. Output formats (Word, PowerPoint, PDF, PNG); this decides how fonts are named (step 3).

## 2. Palette

`python3 scripts/ddi.py library palettes --query "<tone words + industry>" --limit 5`

- **No brand colour:** take one library palette whole. `brand.md` needs six roles -- primary,
  secondary, accent, background, foreground, muted -- copy all six hexes from ONE palette; do not
  mix roles from two. Pick rows with an authority in the Evidence line over `convention` rows.
- **A brand colour exists:** make it the `accent` (one accent only), and take the other five roles
  from a neutral library palette whose tone fits (`print-neutral`, `lib-govuk-ink`,
  `lib-uswds-navy`, ...). If the brand colour is dark, it may be `primary` instead.
- **Contrast is checked for you, but check first:** `make_brand_kit.py` derives On-colours
  (white or black) and prints every pair against the **4.5:1** WCAG text-contrast threshold
  (`contrast pairs ... [OK|FAIL, threshold 4.5:1]`); treat any FAIL as a stop and change the colour. The accent becomes fill-only if it fails 4.5:1
  against the background (the library's `Fill-Only Roles`): then never set text in it.
  Never invent a hex you have not seen pass that report.

## 3. Typeface pairing

`python3 scripts/ddi.py library typefaces --query "<tone words>" --limit 5`

- **At most 2 families** (the library's `validate-font-family-count` check fails at 3). Take a
  pairing's heading and body names exactly as listed (`Heading Family`, `Body Family`).
- Prefer rows with `Embedding Licence: installable` (SIL OFL) when the output is PDF/PPTX and
  fonts will be embedded; for Word, the recipient's machine may lack the font, so the docx handoff
  names the safe-stack fallback (`font rule by output format`: docx = safe-stack).
- Fallbacks are kept separately for heading and body. If the pair you name is a library pairing
  row, `make_brand_kit.py` copies that row's `Safe Stack Fallback` / `Safe Stack Body Fallback`
  (and its licence, availability and tabular-figures flags). A family that is not a library
  pairing gets a fallback from the font-substitutes table, else the fallback the library gives
  that family elsewhere, else its category default (serif -> Georgia, sans -> Arial). A family
  the library has never seen prints a WARNING: then name a library pairing instead, or tell
  the user the fallback is a guess.

## 4. Type scale per medium

`python3 scripts/ddi.py library type-scales --limit 20` (scales are `lib-<ratio>-<medium>`).

Use one line per medium the brand needs under `## Type scales`, medium matching the scale:
`print: lib-major-third-print`, `projection: lib-minor-third-projection`,
`screen: lib-major-third-screen`. Ratios are named ratios (minor third 1.2, major third 1.25,
perfect fourth 1.333): tighter for dense documents, wider for slides. Projection scales are large
by design; do not reuse a print scale for slides. No line = the doctypes keep their generic scale.

## 5. Doctypes and a design per family

List the doctypes needed under `## Doctypes` (`ddi.py resolve --query` or the table in
`portable/DDI-LIBRARY.md` gives keys such as `cv-uk`, `letter-formal`, `invoice-tabular`,
`report-short`, `slide-deck-projection`).

For each family: `python3 scripts/ddi.py designs --doctype <key> --query "<tone / industry>"`.
Take the **rank-1** design unless a lower one's `Best For` matches the tone (for example
`cv-editorial` for a creative studio). Read its Evidence Class: prefer `authority` / `ranked` /
`juried` over `convention`, and say so to the user when only a convention design exists.
One line per family: `cv: cv-us-uk-designed`. A family with no line keeps the generic
palette and typeface -- listed doctypes without a `## Designs` line will NOT show the brand's
colours, so give every listed family a line.

## 6. Write, build, merge, verify

```
python3 scripts/make_brand_kit.py brand.md --dry-run     # gate + contrast report; fix and repeat until OK
python3 scripts/make_brand_kit.py brand.md               # writes <slug>-brand-kit.zip
python3 scripts/merge_brand_kit.py <slug>-brand-kit.zip  # writes document-design-intelligence-<slug>.zip
```

Any bad line in `brand.md` is a hard error with its line number; the error lists the valid keys.
Verify in the merged skill (unzip it, or upload it and run there):

```
python3 scripts/ddi.py check
python3 scripts/ddi.py resolve --brand <slug> --doctype <slug>-<doctype> --json > r.json
python3 scripts/ddi.py handoff --json r.json --format docx     # also pptx | pdf | png
```

Check the resolved palette / typeface are `<slug>-...` rows and the handoff prints the brand's
hexes and sizes. Then give the user the merged ZIP to install as their skill.

## Guardrails that are in the data (cite these, do not paraphrase taste)

- Text contrast >= 4.5:1: the kit gate and every palette's `Text-Safe Roles` / `Fill-Only Roles`.
- <= 2 font families: `validate-font-family-count`; pairings list exactly two.
- One accent colour: the palette has a single `Accent` role; the `validate-accent-colour-palette`
  check flags accents outside the resolved palette.
- Anti-slop: no emoji (`validate-no-emoji`, fail), no gradients, no boxed-everything tables
  (`validate-cell-border-ratio`), and the per-doctype anti-pattern tokens (multi-column, text-box,
  photo, icon-only-skill-bar, ...) listed in each doctype's `anti-patterns` line.
- Evidence: every library row says where it comes from; `convention` means no external source.

Worked example: `examples/generic-law-firm-brand.md` (library rows only; builds and merges clean).
