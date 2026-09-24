# Document Design Intelligence

A design library that lets an AI assistant make documents that look designed instead of
generic: CVs, cover letters, letters, memos, forms, brochures, flyers, posters, reports,
whitepapers, proposals, quotes, invoices, slide decks, one-pagers and infographics.

It is data plus a small command-line tool. You do not need to be a designer or a programmer
to use it; your AI assistant reads it for you.

## What is in it

- **Designs per document family.** Each family (CV, brochure, invoice, ...) has one or more
  named designs, ranked. A design says which layout, palette and typefaces to use and what it
  is best for. How the ranking is made is described below.
- **A grand library** of colour palettes (43), typeface pairings (33) and type scales (81),
  each with its evidence: an authority such as a design system, a fetched ranking, or
  "convention" when nothing external backs it. Convention rows say so.
- **Exact values.** Page size and margins, font sizes and leading, hex colours, section
  order and headings in English, French and German, per document type (30 doctypes).
- **Anti-slop rules.** Concrete checks for the things that make AI documents look generic
  (emoji, gradients, low-contrast text, too many fonts, boxed-everything tables, ...), some of
  them mechanically checkable on a finished file.

## Install

**Claude (recommended).** Skills need code execution enabled (Settings > Capabilities on
individual plans). Download `document-design-intelligence-<version>.zip` from this
repository's Releases page, then in Claude go to Customize > Skills > + > Create skill and
upload the ZIP. Uploading it to a Project's files does not install a skill.

**Claude Code.** Copy `skill/document-design-intelligence/` into your skills directory.

**ChatGPT, Grok, Gemini and other agents.** These can use the *portable pack* in
[`portable/`](portable/): `AGENTS.md` (instructions), `DDI-LIBRARY.md` (all the values as
plain markdown) and [`INSTALL.md`](portable/INSTALL.md) (per-platform steps). A release also
ships them as `ddi-portable-<version>.zip`. The maintainers have **not tested** ChatGPT,
Grok or Gemini directly; the pack is plain markdown that those platforms accept, and it is
checked against the Claude skill's own data by a test, nothing more.
Without code execution an assistant can hand you HTML or exact styling values, not a finished
.docx or .pptx file.

## Quick usage

Run from `skill/document-design-intelligence/` (Python 3, standard library only). Your
assistant normally runs these; you can too.

```
python3 scripts/ddi.py check                                  # validate the data
python3 scripts/ddi.py resolve --query "make me a cv for uk design agencies" --json > r.json
python3 scripts/ddi.py designs --doctype cv-uk --query "graphic designer portfolio"
python3 scripts/ddi.py library palettes --query "calm" --limit 3    # also: typefaces, type-scales, doc-styles
python3 scripts/ddi.py handoff --json r.json --format docx    # exact values for docx|pptx|pdf|png
python3 scripts/ddi.py preflight my-document.pdf              # check a finished .pdf/.docx/.pptx
```

`resolve` picks the document type and returns every value; `designs` lists the ranked designs
for that type (add `--design <key>` to `resolve` to use one); `handoff` turns the result into
the numbers a renderer needs; `preflight` checks the rendered file against the rules.

## Your own brand

Write one `brand.md` and turn it into a brand kit:

```
# Acme
slug: acme

## Palette
primary: #1F6F43
secondary: #8B5E3C
accent: #9ACD32
background: #F7F8F5
foreground: #1E2A23
muted: #DCE8DF

## Typefaces
heading: Manrope
body: Inter

## Doctypes
cv-uk
invoice-tabular

## Designs
cv: cv-editorial
invoice: invoice-tabular

## Type scales
print: lib-major-third-print
```

`## Palette`, `## Typefaces` and `## Doctypes` are required; `## Designs` (a design per
family), `## Type scales` (a library scale per medium), `## Voice` and `## Document defaults`
are optional. Any unrecognised line is a hard error naming its line number.

```
python3 scripts/make_brand_kit.py brand.md --dry-run     # check without writing
python3 scripts/make_brand_kit.py brand.md               # writes <slug>-brand-kit.zip
python3 scripts/merge_brand_kit.py <slug>-brand-kit.zip  # writes document-design-intelligence-<slug>.zip
```

An AI can build a kit for you by following [`references/brand-kit-builder.md`](skill/document-design-intelligence/references/brand-kit-builder.md); a complete example is [`examples/generic-law-firm-brand.md`](skill/document-design-intelligence/examples/generic-law-firm-brand.md). Upload the merged ZIP as your skill. Text colours are derived and contrast-checked; a kit that fails the gate is not written. See
[`examples/ens-brand.md`](skill/document-design-intelligence/examples/ens-brand.md).

## How designs are ranked, and what that does not mean

The protocol is written down before any coding was done:
[`research/82-design-ranking-protocol.md`](research/82-design-ranking-protocol.md), with
sources in [`research/81-ranking-sources.md`](research/81-ranking-sources.md). In short:
coders count, they do not judge. Where a public corpus with numbers exists (GitHub stars, npm
downloads, template-catalogue download counts) designs are ranked by how many of the top
items use them. Otherwise a design rests on a named authority (a government or design
system) or an award, and otherwise it is labelled `convention`.

Limits, stated plainly:

- **Popularity is not quality.** A design common in a corpus is common, not necessarily
  good; only on-topic items are counted and off-topic ones are dropped by written rule.
- **Some families are thin.** Where no corpus with enough items could be fetched (many
  vendors' galleries need a login or are not public), a family may carry a single
  `convention` design. `ddi.py designs` shows each design's evidence class, so you can see
  which is which.
- Values in the library are sourced where a source was fetched; the rest are marked
  `convention` and no source is claimed for them.

## Repository layout

```
skill/document-design-intelligence/   the skill: SKILL.md, scripts/, data/, tests in scripts/tests
portable/                             generated pack for agents without code execution
research/                             sources, drafts, protocol and review notes; the data loaders
.github/workflows/release.yml         tag vX.Y.Z -> tests -> skill ZIP + portable ZIP
RELEASE-NOTES.md                      what changed per version
```

`data/base/*.csv` and `portable/*` are generated. Edit the sources in `research/`, then run
`python3 research/build-manifest.py`, `python3 research/load-base.py` and
`python3 research/build-portable.py`. Tests: `python3 -m pytest -q` in the skill directory.

## Licence

MIT, see [`LICENSE`](skill/document-design-intelligence/LICENSE). Architecture credit to
UI/UX Pro Max is in [`NOTICE.md`](skill/document-design-intelligence/NOTICE.md); no upstream
code or data is reproduced.
