# Brand-kit builder -- procedure for an AI

Goal: turn a person's brand into a `brand.md`, build and merge the kit, and prove it works.
Every choice below comes from a row of the library (`scripts/ddi.py library ...`,
`scripts/ddi.py designs ...`) or from a rule stated here, not from taste. Run everything from the
skill directory. Without code execution, follow the same steps by hand from
`portable/DDI-LIBRARY.md`'s `## Grand library` (the rules are inlined in `portable/AGENTS.md`
step 7) and hand the user the finished `brand.md`.

## 1. Interview (ask, then wait)

Ask only what you cannot infer, in one message:
1. Field / industry, and the brand's name (it becomes the `slug`: lowercase letters, digits, `-`).
2. Three tone adjectives (e.g. formal, precise, warm).
3. Existing brand colours (hex) and logo, if any. Existing fonts, if any.
4. Audiences and **languages** (en/fr/de have authored headings). More than one -> step 6b.
5. Document families needed: cv, cover-letter, letter, memo, form, brochure, flyer, poster,
   report, whitepaper, proposal, quote, invoice, deck, one-pager, infographic.
6. Output formats (Word, PowerPoint, PDF, PNG); this decides how fonts are named (step 3).

## 2. Palette (deterministic)

`python3 scripts/ddi.py library palettes --query "<tone words + industry>" --limit 5` prints every
role (Primary, Secondary, Accent, Background, Foreground, Muted) plus Text-Safe and Fill-Only
roles, so one row is all you need to copy.

- **No brand colour.** Take ONE row, all six roles, never mixing roles from two rows. Selection
  rule: the highest-scoring row whose Evidence names an authority or a fetched ranking (not
  `convention`); ties break by BM25 score, then Evidence class (authority > ranked > convention),
  then palette key alphabetically. State the row you took and why.
- **A brand colour exists.** It becomes the ONE `accent`. Take the other five roles from ONE
  neutral row: `print-neutral`, `lib-govuk-ink`, `lib-uswds-navy` or `lib-atlassian-ink`
  (`--query neutral` returns other things, so name these keys). If the brand colour is dark
  (relative luminance below 0.35) it may be `primary` instead, with the accent taken from the
  neutral row.
- **A brand colour that fails text contrast is kept.** A logo colour is identity: below 4.5:1 on
  the background it is written as a fill-only accent, never changed. `make_brand_kit.py --dry-run`
  prints the pair (`Accent/Background: ... [fill-only ...]`) and a line `accent demoted to
  fill-only (x.xx:1)`; below 3:1 it also warns against thin rules and icons in that colour.
  Tell the user: use it for fills, blocks and large marks; text stays in the text-safe roles.
  Change a colour only if the user wants text in it (then offer the nearest library accent).
- **What stops the build.** Only the body-text pair: foreground on background under 4.5:1
  (`STOP:` line, and the gate refuses). Never invent a hex you have not seen in a library row or
  in the user's own brief.
- **Rules and tints (derived, stated in the dry run).** Rule Hair/Strong come from the library
  palette row when your roles match one; otherwise Rule Hair is the first palette neutral at
  >= 1.5:1 against the background (a convention, printed as such). A tinted light background
  (Material/Radix "surface" colours) is replaced by white for print families, in a `<slug>-print`
  palette; add `print-background: keep` at the top of brand.md to keep the tint.

## 3. Typeface pairing

`python3 scripts/ddi.py library typefaces --query "<tone words>" --limit 5`

- **At most 2 families** (`validate-font-family-count` fails at 3). Take a pairing's heading and
  body names exactly as listed.
- Prefer `Embedding Licence: installable` (SIL OFL) when the output is PDF/PPTX. Fallbacks are
  kept per role and copied from a library pairing row; a family the library has never seen prints a
  WARNING (name a library pairing instead, or tell the user the fallback is a guess).
- **Tell the user what Word will do.** The docx handoff names the safe-stack fallback (docx =
  safe-stack), so in Word the documents use e.g. Times New Roman / Arial unless the user installs
  the brand fonts. The handoff prints `brand fonts X / Y: install them or accept the fallback` in
  every docx and pptx block, including flyers and invoices that have no docx render target. PowerPoint
  embeds only when the typeface's licence allows it (`installable`/`editable`); a kit whose font is
  not a library row has licence `unknown` and gets the safe-stack line with the reason.

## 4. Type scale per medium

`python3 scripts/ddi.py library type-scales --limit 20` (scale keys are `lib-<ratio>-<medium>`;
ratios are minor third 1.2, major third 1.25, perfect fourth 1.333).

- print: the pairing's own `Scale Key` if it has a print row, else `lib-major-third-print`.
- projection: `lib-perfect-fourth-projection` (h1 57pt, body 24, body-dense 18). Every library
  projection scale clears the constraint floors (`proj-title-floor` 36, `proj-body-floor` 24,
  `proj-body-dense-floor` 18); this one is the default because its h1 is the largest.
- screen: `lib-major-third-screen`.
One line per medium under `## Type scales`. The kit adds a `legal` role (= caption) to print scales
so invoice and quote fine print keeps a size (`legal-text-min-size` is 8pt).

## 5. Doctypes and a design per family

List the doctypes under `## Doctypes` (keys such as `cv-uk`, `letter-formal`, `invoice-tabular`,
`report-short`, `slide-deck-projection`). A base doctype keeps its page format, so invoices stay
in their own size.

For each family: `python3 scripts/ddi.py designs --doctype <key> --query "<tone / industry>"`.
Take the **rank-1** design unless a lower one's `Best For` matches the tone; prefer `authority` /
`ranked` / `juried` over `convention`. One line per family: `cv: cv-us-uk-designed`. **Say so
when a family has only a convention design** (most families today): tell the user that no
ranked alternative exists yet. A listed family without a `## Designs` line keeps the generic
palette and typeface, so give every listed family a line.

## 6. Write, build, merge, verify

```
python3 scripts/make_brand_kit.py brand.md --dry-run     # gate + contrast report; fix and repeat until OK
python3 scripts/make_brand_kit.py brand.md               # writes <slug>-brand-kit.zip
python3 scripts/merge_brand_kit.py <slug>-brand-kit.zip  # writes document-design-intelligence-<slug>.zip
```

The dry run also prints, per doctype, the medium's own contrast requirement from the constraint
sets (projection 7:1, print-legibility 4.5:1 body / 3:1 large text) and a `WARN` for any
text-safe role under it (for example a purple accent at 6.1:1 on slides): use such a role for fills
and large marks only in that medium. A `WARN` does not stop the build.

Verify in the merged skill (unzip it, or upload it and run there):

```
python3 scripts/ddi.py check
python3 scripts/ddi.py resolve --brand <slug> --doctype <slug>-<doctype> --json > r.json
python3 scripts/ddi.py resolve --brand <slug> --query "<a request in each language>" --json
python3 scripts/ddi.py handoff --json r.json --format docx     # also pptx | pdf | png
```

Check the resolved palette and typeface are `<slug>-...` rows, the handoff prints the palette's
text-safe and fill-only roles and the fonts, and the second-language query resolves to the brand
doctype. Then give the user the merged ZIP to install as their skill.

### 6b. More than one language

Add `## Languages` (one line: `en, fr`; en/fr/de). The first is the kit's default document
language. Brand doctypes keep the base doctype's own multilingual keywords, so `--query` in
either language finds them, and a detected French or German request gets that language's
headings automatically. `--lang fr` forces it (`--lang de` also steers a CV to the DACH doctype).

## Guardrails that are in the data (cite these, do not paraphrase taste)

- Text contrast >= 4.5:1: the body-text gate, and every palette's `Text-Safe Roles` /
  `Fill-Only Roles`; medium thresholds from the constraint sets (step 6).
- <= 2 font families: `validate-font-family-count`; pairings list exactly two.
- One accent colour: the palette has a single `Accent` role; `validate-accent-colour-palette`
  flags accents outside the resolved palette.
- Anti-slop: no emoji (`validate-no-emoji`, fail), no gradients, no boxed-everything tables
  (`validate-cell-border-ratio`), and each doctype's anti-pattern tokens (multi-column, text-box,
  photo, icon-only-skill-bar, ...) in its `anti-patterns` line.
- Evidence: every library row says where it comes from; `convention` means no external source.

Worked example: `examples/generic-law-firm-brand.md` (library rows only; builds and merges clean).
