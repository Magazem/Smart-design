# 87 — R3 review: portable pack (commit 84299bb)

Reviewer: Opus Reviewer (adversarial). Date: 2026-09-23. Scope: `portable/AGENTS.md`,
`portable/DDI-LIBRARY.md`, `portable/INSTALL.md`, `research/build-portable.py`,
`scripts/tests/test_portable_sync.py`. Read-only review; the only file written is this one.

## Verdict

The generator works and is deterministic. `test_portable_sync.py` passes (5 passed, 3 subtests).
For all 29 doctypes the "default design" rule in AGENTS.md picks the same design as
`ddi.py`'s Reasoning-Key rule (checked by script, 0 mismatches). Two things are still broken:

1. **The pack drops values that decide whether a document passes.** It leaves out constraint
   thresholds, fold-panel widths, text-safe/fill-only palette roles and the per-format font
   rule. Its one global anti-slop list also marks `multi-column` and `photo` as `fail` for
   every doctype. A model that follows AGENTS.md literally will be told to fail a tri-fold
   brochure for having panels, and to fail a DACH Lebenslauf for having the photo the pack
   calls "customary".
2. **The instructions have gaps and contradictions.** Nothing says how to produce the file
   without code. The trigger list is skewed by alphabetical order: the cv line lists only
   academic keywords, and "report", "brochure" and "pitch deck" don't appear at all. Step 2
   ("design override") contradicts step 4 ("never introduce a font not in the doctype's
   block"). Two of the six CV designs have no style values anywhere in the pack.

Fix findings 1–8 before running the P6.5 proxy trial. Otherwise the trial measures pack
defects, not model compliance.

Severity: **H** = a model following the pack produces a wrong or failing document, or the
pack misstates something. **M** = likely degradation or a misleading claim. **L** = polish.

---

## A. Fidelity (pack vs `ddi.py resolve --doctype <k> --json` + `handoff --format docx|pptx`)

Method: I resolved 6 doctypes (`cv-dach`, `slide-deck-projection`, `invoice-tabular`,
`brochure-trifold-a4`, `quote-devis`, `report-long-toc`). For each one, a script checked
every non-empty cell of every resolved row against that doctype's block in DDI-LIBRARY.md
by substring match. I then read the docx and pptx handoff output side by side with the
block.

**What matches.** Every value that appears in both is identical: trim, 4 margins, bleed,
columns/measure, heading/body family and fallback, each type-scale role (size and leading),
each palette hex, style rule weights, table rules/fills, emphasis, field style, checklist,
and primary headings in en/fr/de. No value differs. Every problem below is an **omission**,
plus one **pptx slide-size divergence** that comes from the code path.

### F1 (H) — Constraint thresholds and Applies-To are dropped
`build-portable.py:288-302` prints `Check (Parameter) -- Severity` only. The data has a
`Threshold` column, and for many checks the limit lives only there. Example: the
`slide-deck-projection` block (DDI-LIBRARY.md:1164-1175) says
`validate-text-density (words_per_slide_body) -- warn` but not the limit (40). The same
block leaves out `validate-contrast-screen` = **7.0**, which is stricter than the 4.5:1
that AGENTS.md:56 advertises; `max_series` = 7; bullets and words per bullet = 6/6; and the
type floors 36/24/18. CV blocks leave out `max_pages` → `cv-regions:Max Pages`. Brochure
blocks leave out the DPI, bleed and safe-margin references (`page-formats:Min DPI Raster`
etc.).
`Applies To` is also dropped, so `format:pdf`-only checks (for example the
professional-print CMYK/output-intent checks) look as if they apply to a docx.
**Fix:** print `Check (Parameter) <op> Threshold -- severity [applies: …]`, and resolve
`table:Column` threshold references to their values inline (e.g. `max pages = 2`).

### F2 (H) — Page-format print geometry is dropped (fold panels, DPI, stock, folio)
`_page_format_lines` (`build-portable.py:160-178`) emits only trim, margins, bleed, columns
and measure. For `brochure-trifold-a4` (DDI-LIBRARY.md:587), the resolved row has
`Panels mm=99.5;99.5;98.0` and `Stock gsm=120`, and the pack shows neither. It shows
`columns: 1; measure: 88mm`, which on its own tells a model "single column". A tri-fold
cannot be built correctly without the panel widths. The `pro-fold-geometry` constraint is
in the block, but it has nothing to check against. `report-long-toc` loses
`Folio Style=roman-front-arabic-body` and `Running Head=centered`. Every doctype loses
`Min DPI Raster/Line Art` and `Print Mode`.
**Fix:** emit every non-empty page-formats column. At minimum: panels, safe margin, DPI,
stock, folio, running head.

### F3 (H) — Palette role semantics are dropped, but AGENTS.md relies on them
AGENTS.md:55-57 and :99-101 promise 4.5:1 contrast "on its own text-safe role pairs".
Neither the doctype blocks (`_palette_lines`, `build-portable.py:212-224`) nor the grand
library (`:372-383`) say which roles are text-safe. Example: `brochure-trifold-a4` resolves
`Fill-Only Roles=muted;accent` and `Text-Safe Roles=foreground;primary;secondary`. The
pack's brochure style says "emphasis: fill", so a model will quite reasonably set text in
Accent #C81E3A or on Muted. The grand library also drops the `On *` roles and rule colours,
which a hand-built brand kit (AGENTS.md §7) needs.
**Fix:** add `text-safe: …; fill-only: …; category-marker: …` to every palette line, and
add On-roles and rules to the grand-library palettes.

### F4 (H) — The per-format font rule (render-targets) is missing
`render-targets.csv` says docx = **safe-stack**, pptx and pdf = **embed**, html =
inline-webfont. The handoff follows that rule: cv-dach docx prints
`python-docx (safe-stack)` and deck pptx prints `python-pptx (embed)`. The pack only says
"use the safe-stack fallback if you cannot embed a font" (AGENTS.md:52-53). So for the
`brochure-trifold-a4` or Harvard CV designs, a pack-following model will name
`Source Sans 3` / `Source Serif 4` in a .docx. The code path would name Arial/Georgia.
That is a real divergence from `handoff --format docx`. The `font-substitutes` table
(metric-identical Liberation/Arimo/… substitutes) is also missing, even though it is the
direct answer to "the design's font isn't installed on the user's machine".
**Fix:** add a short "Font rule by output format" table plus the substitutes table to
DDI-LIBRARY.md, and one sentence to AGENTS.md §3 (see I4).

### F5 (M) — The pptx slide size in handoff disagrees with the pack (code-path defect)
The pack gives `widescreen-16-9` trim **338.67 × 190.5 mm** (13.333 × 7.5 in), which is
PowerPoint's widescreen (DDI-LIBRARY.md:1143). `handoff --format pptx` prints
`LAYOUT_16x9: 10in x 5.625in` (254 × 142.9 mm). The aspect ratio is the same, but the
absolute size is 33% smaller. The 36/24/18 pt sizes therefore look about 1.33× larger on
the handoff's slide than on the pack's slide. The pack is faithful to the data; the handoff
ignores the page-formats row. **Fix (ddi.py):** emit `LAYOUT_WIDE` (13.33 × 7.5) or derive
the size from the page-formats trim. Also flag this in the P6.5 trial scoring (T2).

### F6 (M) — The doctype's own anti-pattern tokens and Doc Conditions are dropped
Each resolved `doc-reasoning` row carries `Anti-Pattern Tokens`, a `Severity`, and
`Doc Conditions` (e.g. cv: `if_ats_target=constraint:ats-strict`; brochure:
`if_professional_print=constraint:professional-print`). The pack flattens the tokens into
one global list (see F9) and leaves out the conditions. As a result, a model can't tell
that professional-print checks apply only when the user is going to a print shop.
**Fix:** print `anti-patterns (severity): …` and `conditional constraints: if … → set` per
doctype.

### F7 (L) — Minor omissions
`Caption Position` / `Cross-Ref Style` (structures), `Has Tabular Figures` (typefaces,
which matters for invoice/quote), and `Education Before Experience` / `Language
Expectation` (cv-regions). All are cheap to add.

---

## B. Instruction quality (AGENTS.md alone, non-Claude model)

### I1 (H) — Trigger words are the first 6 keywords of the alphabetically first doctype
`_family_triggers` (`build-portable.py:508-523`) pools Keywords across doctypes sorted by
`doc_key` and then takes `[:6]`. The first doctype alphabetically fills all six slots:
- **cv** → `cv-academic` wins, so the line reads "academic cv, scientific cv, faculty cv,
  publications list, research cv, grants" (AGENTS.md:15). The words "cv", "resume",
  "curriculum vitae" and "Lebenslauf" never appear.
- **brochure** → `brochure-gatefold`: "gatefold, gate-fold brochure, …" (AGENTS.md:20).
  The words "brochure", "trifold" and "leaflet" are absent.
- **report** → `report-long-toc`: the bare word "report" is absent (AGENTS.md:23).
- **deck** → `slide-deck-document`: "pitch deck", "powerpoint" and "pptx" are absent
  (AGENTS.md:28).
- **flyer** → `brochure-flyer-a4` (a4-only phrasing).

The docstring's claim that this "cannot drift from SKILL.md's own trigger words"
(`:510-513`) is false in practice. **Fix:** round-robin one keyword per doctype until the
list has N items, *or* take each family's generic doctype first (`cv-generic`,
`report-short`, `slide-deck-projection`, `brochure-trifold-*`). Also add an assertion that
the family name itself, or its bare noun, is included.

### I2 (H) — Design override (§2) contradicts "never invent" (§4), and some design values are absent
- AGENTS.md:45 says to apply the chosen design's Style/Palette/Typeface keys. AGENTS.md:68
  says "Never introduce a font, colour, or size that is not in the resolved **doctype's own
  block**". Any override breaks §4 by definition.
- The designs table (e.g. DDI-LIBRARY.md:384-393) gives only **keys**. Palette and typeface
  values can be looked up in the grand library. **Style** values for `cv-dach-tabular` and
  `cv-editorial` exist nowhere in the pack (a script checked all 21 design rows; these 2
  are unresolvable). There is no doc-styles section in the grand library.
- An override changes the typeface, and with it the type scale (`typefaces.Scale Key`,
  e.g. `fraunces-work-sans → cv-editorial-fourth`). AGENTS.md never tells the model to
  follow that link.

**Fix:** (a) reword §4 as "not in the resolved doctype block **or the chosen design's
resolved values**". (b) Emit a fully resolved mini-block per design, with the same
style/palette/typeface/scale lines (one per design, 21 blocks), *or* add a
`### Doc styles` grand-library section and state "design override → type scale =
typeface's Scale Key".

### I3 (H) — "List the family's top 3 ranked designs" diverges from SKILL.md and hides the right answer
SKILL.md step 3 runs `ddi.py designs --doctype <k> --query "<their wording>"`, which is
BM25 over the user's words. AGENTS.md:43 uses fixed rank order. Evidence: for "graphic
designer portfolio creative" on cv-uk, `ddi.py designs` returns **cv-editorial first**
(rank 6 of 6). The AGENTS.md rule offers Harvard, Europass and ATS-restrained, and never
shows the editorial design. In 15 of 16 families there is only 1 design, so "top 3" can't
be satisfied. **Fix:** "list the designs whose *Best for* matches the user's stated style
(up to 3; fewer if the family has fewer), then ask". The Best-for column is already in the
table.

### I4 (H) — No guidance on output format without code execution
AGENTS.md never says what artifact to produce. The honest options, in order: (1) a
complete, styled **HTML** file (single file, CSS `@page` size and margins, font stack with
fallback) that the user prints or saves to PDF; (2) **Markdown or plain text** content in
the resolved section order, plus a **style sheet for the user to apply in Word or
PowerPoint** (named paragraph styles with font, size, leading and colour per role, page
setup, margins); (3) never pretend to have produced a .docx or .pptx.
SKILL.md already says "a plain-text answer in chat is a valid output … with the same
resolved sections and headings". AGENTS.md should say the same.
The `fail`-severity **pptx-font-embedded** (DDI-LIBRARY.md:1175) and all professional-print
checks can't be satisfied or verified without code. As written, AGENTS.md:63 ("fail = must
fix before delivering") means the model must refuse to deliver.
**Fix:** add a §"Delivering without code" that (a) lists the output options and (b) says
that mechanical checks the model cannot verify must be listed to the user as "unverified".
Don't treat them as silently passed or as blocking.

### I5 (H) — Section-order precedence and CV-region fields are unspecified, and the global list contradicts them
A CV block shows two orders. The structure order (cv-dach: 8 sections including
publications and projects) and the regional variant order (`dach-early`: contact,
education, experience, skills). AGENTS.md doesn't say which one wins, or how to pick the
seniority band. The regional rows say `photo=customary` (DDI-LIBRARY.md:68,70, and also
eu-generic and gulf). Meanwhile AGENTS.md:69-70 ("never add … photos"), the cv-restrained
checklist ("Omit photo unless region requires it"), and the global token list
(`photo -- fail`, DDI-LIBRARY.md:1397) all say otherwise.
**Fix:** state the precedence explicitly, in whatever order ddi.py actually applies it
(the handoff printed `source=doctype-default` with the 8-section structure order, and the
region orders only as a side list — that is itself worth confirming in the code path).
Band rule: "early = under ~3 years of experience or a recent graduate". Photo rule:
"include only if the region row says customary AND the user supplies one; ATS-strict
target → omit".

### I6 (M) — Region or language unknown
There is no rule for "CV" with no country given. **Fix:** "If region is unstated: ask one
question (target country), or default to `cv-generic`, and say so." Also: "Language = the
language of the user's request unless they ask otherwise". The doctype `language:` line is
a default, not an override. That is actually *better* than the code path, which resolved a
French devis request to `language: en (source=doctype-default)`.

### I7 (M) — Missing-role sizes
Invoice and quote scales have **no h1/h2** (`body 11pt, legal 8.5pt`, DDI-LIBRARY.md
invoice/quote blocks). cv-dach has no h3, caption or label. AGENTS.md:73 lists
h1/h2/h3/lead/body/caption/label as if they always exist, and §4 forbids inventing a
size. A model must break one rule or the other to title an invoice. **Fix (data):** add
h1 (and label) to `form-print`. **Fix (AGENTS):** "if a role is absent, reuse the nearest
present role with weight emphasis; never create a new size".

### I8 (M) — §6 promises "the SAME data", but the released ZIP is older
The GitHub releases page shows v0.3.0 as latest (11 Sep 2026). The pack was generated from
v0.5-era data at HEAD. INSTALL.md gives no URL. **Fix:** cut a release that matches the
pack, put the tagged URL in INSTALL.md and AGENTS.md §6, and stamp the pack with the data
version (the `VERSION` file) so drift is visible.

### I9 (L) — Brand kit (§7): "the two tables you picked from" should be three
Palette, pairing and scale make three tables (AGENTS.md:110). And "pick the scale grouped
for the right medium" (AGENTS.md:125-126) doesn't point to the pairing's own `scale` link
in the grand library.

---

## C. INSTALL.md accuracy (sources checked 2026-09-23)

### P1 (H) — The Claude.ai section is wrong on two points
INSTALL.md:116-121 says "(no code execution needed, or with it)" and "Settings ->
Capabilities -> Skills, or a Project's file upload". Anthropic's help centre says skills
**require code execution** ("This feature requires code execution to be enabled";
individual plans enable it in Settings > Capabilities). Custom skills are uploaded as a ZIP
via **Customize > Skills → + → Create skill**. Uploading the ZIP to a Project's files does
not install a skill. Sources: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude),
[How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).
**Fix:** state the code-execution prerequisite and the correct path. For Claude with code
execution off, point to the portable pack (Project instructions + knowledge file).

### P2 (M) — Custom GPT
- The 8,000-character Instructions limit is corroborated by the OpenAI community
  ([thread](https://community.openai.com/t/why-is-the-my-gpt-instructions-limited-by-8000-characters/1006936)).
  AGENTS.md is 6,612 chars, so 1,388 chars of headroom for the fixes in section B. Fixes
  I2–I6 will need §6 and §7 trimmed.
- Knowledge: up to 20 files, 512 MB each, 2M tokens per text file, per search snippets of
  [Knowledge in GPTs](https://help.openai.com/en/articles/8843948-knowledge-in-gpts).
  help.openai.com returned 403 to direct fetch, so this is verified only via search-result
  excerpts. A 114 KB file is well within these limits. Knowledge is pulled in "depending on
  relevance", i.e. **retrieved in chunks, not read whole**. That makes section D a real
  risk.
- "The GPT has no code execution by default" (INSTALL.md:132-133) is **unverified**. The
  builder exposes a "Code Interpreter & Data Analysis" capability toggle
  ([Troubleshooting GPTs](https://help.openai.com/en/articles/11325361-troubleshooting-gpts)),
  but I found no official statement of its default. **Fix:** "unless you enable Code
  Interpreter & Data Analysis in Capabilities".
- Projects (INSTALL.md:135-136): Projects do have instructions and files
  ([Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)).
  Per-plan file counts weren't retrievable, so don't state a number.

### P3 (M) — Grok
xAI's official help/docs for Grok **Projects** (instructions + files) could not be fetched.
`grok.com/project` returned an empty shell, and the only corroboration is third-party
(e.g. goodday.work, a YouTube how-to). INSTALL.md:147-152 already says "untested". Also
mark the feature description itself as unverified, and give the fallback: paste AGENTS.md
into Settings → Customize Grok and attach DDI-LIBRARY.md per chat.

### P4 (L) — Gemini Gems
This is accurate: "Under 'Knowledge,' click Add files" and upload from device or Drive
([Use Gems — Computer](https://support.google.com/gemini/answer/15146780?hl=en&co=GENIE.Platform%3DDesktop)).
There's no published instruction-length limit on that page. Keep "untested".

---

## D. Size and format as a retrieval knowledge file

### S1 (M) — About 50% of the bytes are duplicated lines
114,457 bytes over 1,281 non-blank lines, but only 475 of those lines are unique.
Duplicated lines account for **56,856 bytes**: the same palette, style, typography and
section-order lines repeat across the 9 CV doctypes, the 3 deck doctypes, invoice/quote
and so on. The `lib-*-screen` type scales are byte-identical to `lib-*-print`
(DDI-LIBRARY.md:1356 vs its print twin). Chunked retrieval makes this worse: near-identical
chunks from different doctypes compete, and the retriever can return the `cv-us` palette
chunk for a `cv-dach` question. **Fix:** normalise. Doctype blocks keep only a key line
(`style: cv-restrained · palette: mono-ink · typeface: safe-sans-arial · scale: cv-print ·
page: a4-cv-single-col · structure: cv-experienced`), and each component is printed once
in a component section. Alternatively keep the inline values but tag every line with the
doc_key (see S2). Pick one based on the P6.5 trial.

### S2 (M) — Chunks lose their context
- `### Designs (ranked)` appears 16 times with an identical heading (`build-portable.py:351`).
  A retrieved table chunk doesn't say which family it belongs to. **Fix:**
  `### Designs (ranked) — family: cv`.
- A doctype block is about 2–3.5 KB (roughly 700–1,000 tokens), about the size of a typical
  retrieval chunk, so blocks will be split. The constraints half then arrives without the
  `### … (\`cv-dach\`)` heading. **Fix:** repeat `[cv-dach]` on each sub-heading, or split
  each block into `#### cv-dach — page/type/colour` and `#### cv-dach — structure/constraints`.
- The block body lines are indented 2–4 spaces with no list markers. Markdown renders the
  whole block as one run-on paragraph. Raw-text retrieval is unaffected, but use `- ` list
  items anyway for robust splitting.

### S3 (L) — Provenance placeholders
Convention rows render as "(unnamed source)" (designs, palettes) or
"(no provenance recorded)" (type scales, looked up via the first member's
`scale_row_key`). **Fix:** print the Evidence Class (`convention — no external source`).

---

## E. Generator determinism and robustness

### G1 (H) — Brand overlays leak into the pack
The docstring (`build-portable.py:84-87`) says "generic scope only; brand overlays are
… not part of a knowledge pack". But `load_context` loads `SKILL_ROOT/data` via
`datalib.load_all_tables`, which merges **every `data/brand/<slug>/`**
(`scripts/lib/data.py:239-265`). Only the grand-library palettes and typefaces filter on
`Brand Scope == generic` (`:373`, `:387`). Reproduced: I copied the data dir to %TEMP% and
added `brand/acme/{doctypes,designs,palettes}.csv`. `generate_all()` then emitted
`### ACME BRAND ROW (\`acme-cv\`)` as a doctype block and `| 1 | ACME BRAND ROW
(\`acme-design\`) |` in the designs table. The palette was correctly filtered. Brand
doctypes would also feed AGENTS.md triggers (and sort first, per I1). Type scales,
anti-pattern tokens and slop constraints aren't filtered either. Today `data/brand/` holds
only README.md, so the committed pack is clean. But a maintainer with the `ens` kit merged
locally would publish it on the next regeneration, and the sync test would fail everyone
else. **Fix:** filter `Brand Scope == "generic"` right after `load_all_tables` for every
table that has the column, or load base only. Add a test with a fixture brand dir that
asserts the output contains no brand key.

### G2 (H) — The global anti-slop severity folding is wrong for most doctypes
`_anti_slop_checklist` (`:453-458`) takes each doc-reasoning **row's** Severity, applies it
to every token in that row, and keeps the worst value across all rows. So `multi-column`,
`photo` and `text-box` become `fail` for every document (DDI-LIBRARY.md:1396-1397), because
the ATS-CV row is `fail`. AGENTS.md:77-79 then says "check it does not contain any
fail-severity item". That fails every tri-fold brochure (panels), every DACH/Gulf CV with
the customary photo, and every poster that uses a photo. **Fix:** keep tokens per doctype
(F6), and turn the global list into "tokens → the doc categories where they apply, with
severity each".

### G3 (L) — Determinism: OK
Iteration is sorted or in manifest order, there are no timestamps, output is LF + UTF-8,
and the sync test is byte-for-byte with CRLF folding. Minor notes: `int(Rank or 0)`
(`:345`) would crash on a non-integer rank if validation ever let one through, and the
`RuntimeError` text says "data/base fails …" even when the manifest itself is missing.
`main()` enforces the 8,000-char limit (`:722-725`). It's worth also asserting the family
name is present in each trigger line (I1).

---

## F. Data issue surfaced by the pack (same in both paths)

### D1 (M) — A French devis inherits invoice headings
`quote-devis` resolves the structure `invoice-standard`: "Facturé à", "Détails de la
facture", "Invoice Details" (DDI-LIBRARY.md:981-1003). A devis isn't a facture. French
practice expects the word "Devis", a validity date (date de validité), and an acceptance
line ("Bon pour accord", signature). **Fix (data):** a `quote-standard` structure with
`quote-details`, `validity` and `acceptance` sections and fr/de headings. **The P6.5 T3
prompt will hit this, so fix it first or score around it (see below).**

---

## G. PRE-REGISTERED proxy trial for P6.5

This design is written before any run. **It must not be edited after the first model
output is seen.** If it has to change, version it as a new trial.

**Setup.** One fresh session per (platform × prompt), with no chat history.
- Platform A: ChatGPT Custom GPT. AGENTS.md goes in Instructions, DDI-LIBRARY.md in
  Knowledge, Code Interpreter **off**.
- Platform B: Gemini Gem, same two files.
- Platform C: Grok Project, if available.
- Control: the same model with no pack.

Each prompt runs **3 times** per platform. Record the pack commit hash and the model
version. Save the raw transcripts in `research/p65-trial/<platform>/<prompt>-<n>.md`.

**Prompts (verbatim):**

- **T1 — UK graphic-designer CV, inline content.**
  "Make me a CV for UK design agency jobs. I'm a graphic designer with 6 years' experience.
  Name: Sam Okafor, London, sam@okafor.design, 07700 900123, okafor.design. Experience:
  Senior Designer, Northbank Studio (2021–now): led rebrand for 3 FTSE-250 clients, managed
  2 juniors. Designer, Pixel & Pine (2018–2021): packaging and print for retail. Education:
  BA Graphic Design, Falmouth University, 2018. Skills: Adobe CC, Figma, typography,
  art direction. I want it to look like a designer made it."
  → Expected: doctype `cv-uk`. Expected design: because of the stated style, the model
  lists matching designs and **asks**, with cv-editorial among them; or, if it proceeds
  without asking, it must name a pack design. The section order must come from the pack's
  cv-uk block (structure or UK regional row). Language: en.
- **T2 — Investor deck.**
  "I need a 10-slide investor pitch deck for our seed round. We're Loopa, a B2B SaaS that
  automates freight invoice reconciliation; $40k MRR, 22% MoM growth, raising $2M. Give me
  the slides."
  → Expected: `slide-deck-projection`, design "Slide deck, bold minimal". 16:9 at
  338.67 × 190.5 mm, or a stated 13.333 × 7.5 in. (Don't penalise 10 × 5.625 in if the
  output is a pptx recipe; see F5, and record it as a separate note.) Arial, deck-high-
  contrast hexes. At most 6 bullets per slide and at most 6 words per bullet.
- **T3 — French devis.**
  "Fais-moi un devis pour la rénovation d'une salle de bain : dépose de l'existant 850 €,
  plomberie 2 300 €, carrelage 1 900 €, TVA 10 %. Client : Mme Durand, 12 rue des Lilas,
  Lyon. Mon entreprise : Atelier Morel, SIRET 123 456 789 00012."
  → Expected: `quote-devis`, French headings from the pack, Public Sans with Arial
  fallback, print-neutral hexes, form-grid-underline (header and total rules only, no
  zebra, no fills).

**Falsifier. A single run is FAIL if any of these holds:**
1. Any font family, hex colour, or point size appears that is not in the resolved
   doctype's block **or** the named chosen design's resolved values (after fix I2).
   Case-insensitive hex match; a "safe-stack fallback" counts only if that exact fallback
   is listed.
2. No named pack design. The output must name the design (Display Name or key) it applied,
   or explicitly ask the user to choose from designs listed in the pack.
3. The section order does not equal, as an ordered sequence, one order listed in the pack
   for that doctype (structure order or a regional row). Omitting a section the user gave
   no content for is allowed if the omission is disclosed. Adding a section that isn't in
   the pack is FAIL.
4. The wrong doctype for T2 or T3. For T1, the doctype isn't `cv-uk`, and the region isn't
   asked about or disclosed.
5. The output claims to be a .docx/.pptx/.pdf file it cannot have produced (no code
   execution), or claims that a mechanical check passed which it could not run.

**Scoring.**
- Per run: PASS or FAIL. Record which falsifier clause fired, plus secondary counts:
  number of out-of-pack values, number of in-pack values used correctly, and whether it
  asked or disclosed.
- Per platform × prompt: pass rate out of 3.
- Pre-registered success bar for P6.5: at least 7 of 9 runs PASS on Platform A, and each
  prompt passes at least 2 of 3 times. The control must fail clause 1 or 2 in at least
  2 of 3 runs, which shows the pack is doing the work. If the control passes as often as
  the pack, the trial is inconclusive, not a success.
- Scoring is done by a script. It extracts hexes (`#[0-9A-Fa-f]{6}`), font names (matched
  against the typeface table's families plus fallbacks), pt sizes, and heading sequence,
  and compares them against `ddi.py resolve --doctype <k> --json`. A human checks only
  clauses 2 and 5. The scorer must be committed before the first run.
- Known-data caveat: T3 headings will be "Facturé à / Détails de la facture" until D1 is
  fixed. Score the pack as-is, and record D1 as a separate annotated finding rather than a
  model failure.

---

## Fix priority
1. G1 brand leak and G2 severity folding (generator correctness).
2. F1–F4 (dropped decisive values).
3. I1–I5 (instructions: triggers, design override, top-3 rule, output format, CV section
   and photo precedence).
4. P1 Claude.ai install text. Cut a release to match the pack (I8).
5. S1–S2 (retrieval structure), then run the P6.5 trial against the fixed pack.
