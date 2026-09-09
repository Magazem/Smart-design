# Coverage & Gap Analysis — Document Types

Source audited: `C:\Users\ysuliman\.claude\plugins\marketplaces\ui-ux-pro-max-skill`
All line numbers refer to that tree. Paths below are relative to it.

---

**Verdict up front.** The gap is real and large, but it is not eight document-type
gaps — it is **three missing subsystems**: a pagination/flow layer, a binary-format
writer, and a print-geometry executor. Everything the existing system does well sits
on one side of a single line, and everything it cannot do sits on the other. The line
is: *the artifact is one fixed-size canvas* vs. *content must flow across pages*.

The honest caveat: the defensible scope is narrower than "document design
intelligence" sounds. Posters, banners, social images and slide *reasoning* are
already solved upstream under MIT — rebuilding those is duplicated effort with no
user-visible gain. The genuinely unserved territory is CVs, long-form
reports/whitepapers, brochures, and any print or binary output. That is roughly 40%
of what the working title implies, and it is the 40% worth building.

---

## 1. Findings

### 1.1 Coverage matrix

Legend: **A** = handles well · **B** = partial · **C** = not at all.
"Gap cause" answers the Orchestrator's question: *deliberate scope choice* vs.
*mechanism cannot reach it* vs. *unbuilt scaffold*.

| Document type | Verdict | Evidence | Gap cause |
|---|---|---|---|
| **Poster** | **A** | `ui-styling/references/canvas-design-system.md:312` lists "Poster designs" as a use case; `:196-203` gives the technical contract — "Single page default", "PDF or PNG output", "Clean margins", "Contained composition". Works because the artifact is one bounded canvas. | — (works) |
| **PowerPoint deck** | **B** | Reasoning layer is genuinely strong: `design-system/data/slide-strategies.csv` (15 deck structures + emotion arcs), `slide-layouts.csv` (25 layouts), `slide-copy.csv` (25 formulas), `slide-charts.csv` (25 chart types). Output layer is screen-only HTML: `slides/references/html-template.md:35` (`width:100vw`), `:46,:52` (all slides `position:absolute`, stacked), `:60` (`opacity:0` toggling). Zero `.pptx` anywhere in the repo. | **Mechanism** for the file; **deliberate** for HTML |
| **Infographic** | **B (scaffold only)** | `design-system/scripts/html-token-validator.py:29` registers an `infographics` output directory, `:271,:277` expose `--type infographics`. There is no infographic generator, no data table, no reference doc. One style line exists at `banner-design/references/banner-sizes-and-styles.md:68`. | **Unbuilt scaffold** |
| **Letter / proposal** | **B (identity only)** | Letterhead exists as brand identity, not as a producible document: `design/data/cip/deliverables.csv:5` (Letterhead), `:39` (Document Template, format field literally "DOCX template"), `brand/references/logo-usage-rules.md:167` (logo placement on letterhead). But `design/scripts/cip/generate.py:6` is a Gemini image generator — the deliverable is a **raster mockup**, not an editable letter. | **Mechanism** |
| **Brochure / flyer** | **C** | Zero occurrences of `brochure`, `flyer`, `leaflet`, `tri-fold`, or `trifold` in `.claude/`. Nearest neighbours are CIP Folder (`design/data/cip/deliverables.csv:7`) and Envelope (`:6`), again image mockups only. | **Mechanism** (multi-panel flow + fold geometry + print) |
| **CV / résumé** | **C** | Zero occurrences of `resume`, `curriculum vitae`, or `ATS` anywhere in `.claude/`. Not a thin section — a total absence. | **Mechanism + adversarial constraint** (see §1.5) |
| **Long-form report** | **C** | Zero `table of contents`, zero `footnote`, zero `running head`, zero `page number` in `.claude/`. The only widow/orphan reference is a manual human checkbox at `brand/references/approval-checklist.md:36`. The closest thing to a body-text spec is `design-system/data/slide-typography.csv:10` (`body-focus,24px`) — still slide-scale, not document-scale. | **Mechanism** (pagination/flow) |
| **Whitepaper** | **C** | Same absences as long-form report, plus zero citation/reference/bibliography apparatus. | **Mechanism** (pagination/flow) |

### 1.2 The single discriminating axis

The matrix is not eight independent judgements. One property predicts every row:

> The system succeeds when the artifact is **one fixed-size canvas with little text**,
> and fails when **content must flow across page boundaries**.

The system states this constraint in its own source. `canvas-design-system.md:29`
specifies "90% visual design / 10% essential text"; `:46-53` is a section headed
"Minimal Text Integration" whose first rule (`:49`) is literally **"Never
paragraphs."** Posters, banners, social photos and each individual slide are fixed
canvases with minimal text. CVs, reports, whitepapers, letters and brochures are
mostly paragraphs distributed across pages.

That makes the gap-cause column mechanical rather than a per-row judgement call, and
it explains why the four hypotheses in the assignment brief collapse into three
subsystems rather than eight features.

`canvas-design-system.md:199` does say "multi-page when requested" — but that is a
sentence, not a mechanism. Nothing downstream implements it.

### 1.3 Print production: knowledge exists, mechanism does not

This is the sharpest finding in the audit. Correct print knowledge **is present**, as
prose:

- `banner-design/SKILL.md:183` — "**Print**: 300 DPI, CMYK, 3-5mm bleed"
- `banner-design/references/banner-sizes-and-styles.md:105-109` — 300 DPI minimum,
  3-5mm bleed all sides, CMYK color mode, 1pt-per-foot viewing distance rule
- `design/SKILL.md:177` — duplicate of the same three specs

And is **never executable anywhere**. Whole-repo counts (`.md`, `.py`, `.cjs`, `.js`,
`.csv`, `.json`, `.ts`; `.git` excluded):

| Mechanism | Hits |
|---|---|
| `pptx` / `python-pptx` | 0 / 0 |
| `.docx` / `python-docx` | 0 / 0 |
| `reportlab` / `weasyprint` / `wkhtmltopdf` | 0 / 0 / 0 |
| `@page` | 0 |
| `page-break` / `break-inside` | 0 |
| `@media print` | 0 |
| `trim mark` | 0 |
| physical units (`mm`) | 0 |

The three print lines are advice to a human designer working in Illustrator. They are
not wired to any renderer. Meanwhile the same sub-skill that carries the advice
declares print out of scope in its own header: `banner-design/SKILL.md:13` — "This
skill handles banner design only. Does NOT handle video editing, full website design,
or **print production**."

### 1.4 Two documented exclusions, and one that isn't

Distinguishing deliberate scope choices from mechanism limits matters because they
need different responses. There are exactly two **explicit** exclusions in the source:

- `design/references/social-photos-design.md:322-329` — a "Security & Scope" section:
  "Does NOT handle: … Print production files (CMYK, bleed) …"
- `banner-design/SKILL.md:13` — quoted above.

Both are deliberate, both are honest, and both concern print. Everything else in the
**C** rows is silent absence, not stated exclusion — which is the signature of
mechanism limit, not scope discipline.

The infographic row is neither. `html-token-validator.py` reserves a path and a CLI
flag for a subsystem that was never written. That is an abandoned scaffold, and it is
the one row where the right response is "finish it" rather than "build it" or "leave
it alone".

The core router confirms the framing. `ui-ux-pro-max/SKILL.md` is 45KB and describes
itself (line 2) as "UI/UX design intelligence **for web and mobile**". A grep of that
file for `poster|print|document|A4|resume|report|brochure|pdf|pptx|docx|paginat`
returns **zero hits**. The system has no document vocabulary at its entry point at all.

### 1.5 Hypothesis test result

The assignment brief's four hypotheses — CVs, true binary output, long-form reports,
print production — **all confirm**. Refinement: they are not four parallel gaps, they
are three subsystems plus one adversarial constraint.

| Missing subsystem | Explains | Hardest part |
|---|---|---|
| **Pagination / flow layer** | CV, report, whitepaper, brochure, letter | Content-aware page breaking, widow/orphan control, running heads, TOC generation |
| **Binary writer** | `.pptx`, `.docx` | Mapping a visual design language onto OOXML's constrained model |
| **Print geometry executor** | Brochure, poster-for-print, any physical output | Bleed/trim boxes, CMYK conversion, physical units |

**The CV is the outlier, and it is not a small gap despite looking like one.** Beyond
the zero data, there is a design tension: ATS parsers reward plain semantic structure
— single column, standard headings, no text-in-graphics, no tables-as-layout — while
this system's entire value proposition is token-driven visual richness. Those pull in
opposite directions. A CV feature is not "add a CSV of résumé layouts"; it is a mode
where the design intelligence must know when to *restrain itself*, and must produce
two divergent artifacts (ATS-safe and human-facing) from one content model. Flagging
this as reasoning, not citation — the evidence here is precisely an absence.

### 1.6 The fork: real `.docx`/`.pptx` vs. print-ready HTML/PDF

**The HTML branch is not the cheap branch.** This is the counterintuitive result and
it changes the cost comparison.

The intuition is that accepting HTML/PDF lets us reuse their pipeline and skip the
hard work. The evidence says otherwise. Their HTML is *architecturally* screen-only,
not merely un-tuned for print:

- `html-template.md:35,44` — sizing in `100vw`/`100vh`, i.e. viewport-relative. There
  is no physical page.
- `html-template.md:46,52` — every slide is `position:absolute`, all stacked at the
  same coordinates.
- `html-template.md:60,67` — only the `.active` slide is visible; the rest are
  `opacity:0`. Printing this yields one page containing one slide.
- `html-template.md:29,37,64,74` — `overflow:hidden` at four levels. Overflowing
  content is silently clipped rather than flowed onward, which is the exact opposite
  of what a paginated document must do.
- Zero `@page`, zero `page-break-*`, zero `break-inside`, zero `@media print`.

So the fork's real shape is:

|  | Print-ready HTML/PDF | Real `.docx`/`.pptx` |
|---|---|---|
| Build a pagination/flow layer | **Required** | **Required** |
| Build print geometry (bleed/trim/CMYK) | Required | Partially (page setup only) |
| Build a binary writer | Not required | **Additionally required** |
| Reuse of upstream output layer | ~None — it must be rewritten | ~None |

Both branches pay for pagination. The binary branch pays for pagination **plus** a
writer. Accepting HTML/PDF saves the writer; it does **not** save the hard part.

Recommendation: **build the pagination layer first and format-agnostically** — a
document model (blocks, flows, page masters, break rules) that renders to paginated
HTML/CSS Paged Media as the first target. Treat `.docx`/`.pptx` as a second renderer
against the same model, not a different project. Deciding the fork now is premature:
the first ~70% of the work is identical either way, and building the model
format-agnostically keeps the fork open at near-zero cost.

Secondary consideration, not decisive but it does lean: a `.docx` is editable by the
recipient and a PDF is not. For CVs, proposals and reports — precisely the unserved
rows — recipients routinely expect to edit. That is a real user-value argument for
eventually reaching binary, and another reason not to architect the pagination layer
around HTML-specific assumptions.

---

## 2. Transferable

Ranked by value, with the reason.

1. **The goal → emotion → layout/color/typography lookup chain.** This is the crown
   jewel and it is a *mechanism*, not content. `slide-layout-logic.csv:1` keys on
   `goal,emotion` and yields `layout_pattern,visual_weight,break_pattern`;
   `slide-color-logic.csv:1` keys on `emotion` and yields
   `background,text_color,accent_usage,gradient,card_style`; `slide-typography.csv:1`
   keys on `content_type` and yields a full type scale. `design-system/SKILL.md:149-166`
   documents the chain end to end. It converts a fuzzy design decision into a
   deterministic table lookup, which is exactly why the output does not read as slop.
   It transfers directly to documents: the key becomes *document section purpose*
   (executive summary, methodology, evidence, appendix) instead of *slide goal*.

2. **Generate-then-inherit persistence.** `ui-ux-pro-max/SKILL.md:380-414` — the
   Master + Overrides pattern. A `MASTER.md` holds global rules, `pages/<name>.md`
   holds per-artifact deviations, and the retrieval prompt at `:402-408` instructs the
   model to prefer the override when present and fall back to Master otherwise. The
   brief identifies this loop as the thing most worth cloning, and the audit agrees —
   but see §3, its file-based half does not survive.

3. **Machine-checkable output discipline.** `design-system/scripts/html-token-validator.py`
   forbids hardcoded values in generated output — hex (`:34`), rgb/rgba (`:35-36`),
   hsl (`:37`), and non-`var()` font families (`:38-39`). A validator that *fails* on
   off-system values is a far stronger anti-slop guarantee than a prose checklist.
   Copy the pattern; see §3 for what is wrong with their implementation.

4. **Explicit anti-patterns alongside recommendations.** `slide-layouts.csv` carries
   an `avoid_for` column (e.g. `:6` Metrics Dashboard → "Early-stage no data").
   `canvas-design-system.md:258` names "Obvious AI generation" as a failure mode to
   design against. Telling the model what *not* to do is doing real work here.

5. **One genuinely document-portable typography rule.**
   `brand/references/typography-specifications.md:111-120` — measure of 65–75
   characters, `.prose { max-width: 65ch }`. Nearly everything else in that file is
   screen typography (see §3), but this one survives intact.

### License note (brief asks for this explicitly)

Upstream is MIT © 2024 Next Level Builder. The temptation is concentrated and easy to
name: **the `slide-*.csv` decision tables**. They are the highest-value artifact in
the repo and small enough to copy in a single paste — `slide-layout-logic.csv` is 997
bytes, `slide-color-logic.csv` 891, `slide-typography.csv` 750. Someone will be
tempted.

Recommendation: clone the **schema and the lookup mechanism** — which is an idea, not
an expression — and derive the row contents independently from document-design
sources. The mechanism is where the value is; the specific mapping of
`frustration → dark-surface` is not defensible IP we need and is in any case wrong for
documents. If any file is adapted rather than derived, retain the MIT notice and
attribute. Note also that `.claude/skills/ui-styling/` ships its own separate
`LICENSE.txt` (11,558 bytes) — check that one independently before reusing anything
under that path, including the 40+ bundled TTF font files, which carry their own OFL
terms.

---

## 3. Breaks

Things that do not survive the move to documents or to the Claude app.

**3.1 Runtime contract (cross-cutting — affects every row equally, cited once).**
The upstream pipeline assumes a project working directory, a Node/Python runtime and
network access:

- `brand/scripts/inject-brand-context.cjs:318` resolves against `process.cwd()`
- `design-system/scripts/generate-slide.py:17,19` resolves `assets/design-tokens.css`
  and an output directory via `Path(__file__).resolve().parents[4]`
- `generate-slide.py:632` emits `<link rel="stylesheet" href="../../../assets/design-tokens.css">`
  — a **multi-file** output, relative-linked
- `ui-ux-pro-max/SKILL.md:308-334` instructs the agent to install Python via
  `brew` / `apt` / `winget` if missing
- `design/scripts/cip/generate.py:30-31` and `design/SKILL.md:295` require
  `GEMINI_API_KEY` and outbound calls to Gemini
- `design/SKILL.md:142,229` delegate export to `chrome-devtools` MCP or Playwright

Stated as fact about the repo. The **consequence for the Claude app is inferred**, not
measured — I have no evidence about that sandbox's network policy or artifact CDN
allowlist, and the user's ground truth (it runs; posters are good) rules out a blanket
"none of this works there" claim. The safest reading consistent with both: the parts
that demonstrably work for the user are the **knowledge-and-prose** parts, and the
poster path (`canvas-design-system.md`) notably requires no script at all. Whatever we
build should assume a **single self-contained artifact with no filesystem and no build
step**, and should not inherit the multi-file token-linking contract.

This has a specific cost: the generate-then-inherit loop (§2 item 2) is half broken.
The *generate* half is prose and survives. The *inherit* half depends on `MASTER.md`
persisting on disk between invocations. In the Claude app that persistence has to be
re-hosted — Project knowledge, an uploaded file, or a block the user pastes back.
Worth naming as a design decision rather than discovering later.

**3.2 Screen typography does not become document typography.**
`brand/references/typography-specifications.md` is web-native throughout: `rem`/`px`
scales (`:33-44`), viewport breakpoints (`:46-59`), a Google Fonts CDN `<link>`
(`:20-24`), and a Tailwind config block (`:159-179`). Documents need points, physical
margins, a baseline grid, and facing-page asymmetry — none of which appear. The type
scale itself is also mis-shaped for documents: it tops out at Display 61px with a 16px
body, tuned for a screen at arm's length, not a page at reading distance.

**3.3 Animation and interaction are dead weight.**
`slide-layouts.csv` carries an `animation_class` column on all 25 rows;
`html-template.md:239-273` defines the animation library; `:170-198` implements
keyboard and click navigation. On paper, all of it is inert. Worse, it is actively
misleading — an emphasis expressed as a stagger animation has no print equivalent, so
the emphasis silently disappears rather than degrading to something visual.

**3.4 The token validator's implementation is not copyable as-is.**
`html-token-validator.py:45-52` hardcodes specific brand hex values
(`rgba(59,130,246`, `rgba(245,158,11`, …) into its allow-list. That is a
brand-specific escape hatch baked into a supposedly generic validator, and it defeats
the purpose the moment the brand changes. Copy the *pattern* (fail on off-system
values); do not copy that allow-list.

**3.5 The validator checks the wrong layer for our purposes.**
It verifies token discipline only — no hardcoded colors or fonts. It does **not**
check overflow, contrast, hierarchy, reading order, or whether text fits its box. For
documents the dominant failure mode is *content overflowing or breaking badly across
pages*, which this class of validator does not see at all.

**3.6 Maintenance smell worth not inheriting.**
The five `slides/references/*.md` files are byte-identical duplicates of
`design/references/slides-*.md` (2,688 / 157 / 9,299 / 3,828 / 2,809 bytes each), and
`banner-sizes-and-styles.md` exists twice (5,111 bytes, under both `banner-design/` and
`design/`). Copy-paste reuse across skills. If our skill routes to sub-skills, resolve
this by reference, not duplication.

---

## 4. Gaps

What is missing entirely and would have to be built. Ordered by how much of the matrix
each unlocks.

**4.1 Pagination / flow layer — unlocks 5 of 8 rows.** The single highest-leverage
item. Needs: a content-flow model that breaks across page boundaries; page masters
(first / left / right / continuation); widow and orphan control (currently a human
checkbox at `approval-checklist.md:36`); keep-with-next for headings; running heads and
folios; auto-generated TOC with real page references; footnote placement. Nothing in
the upstream repo touches any of this — the zero-counts in §1.3 are the proof. This is
the project.

**4.2 Document typography system.** A parallel to `slide-typography.csv` keyed on
document content type rather than slide content type, expressed in physical units:
point sizes, leading in points, measure in characters, margin geometry, a baseline
grid. §2 item 5 (`typography-specifications.md:111-120`) is the only upstream row that
carries over.

**4.3 Print geometry executor.** Turn the prose at `banner-design/SKILL.md:183` and
`banner-sizes-and-styles.md:105-109` into something enforced: page size in physical
units, bleed and trim boxes, safe margins, CMYK-aware color handling, and a resolution
floor. Note the honest risk — CMYK conversion done properly needs ICC profiles, and
there is a real question (see §5) whether a Claude-app skill can do more than *specify*
CMYK intent for a downstream tool.

**4.4 Binary writers (`.docx`, `.pptx`).** Only if the fork resolves that way. §1.6
argues this should be a second renderer against the model from 4.1, not a parallel
effort. The interesting design problem is *lossy mapping*: OOXML cannot express much of
what a rich visual language wants, so the system needs to know which visual decisions
to abandon and which to approximate.

**4.5 CV/résumé mode with dual output.** ATS-safe structure plus a human-facing variant
from one content model, and — the part that is actually novel — rules for *when the
design system should hold back*. See §1.5.

**4.6 A document-appropriate quality validator.** Overflow detection, contrast on paper
(which differs from screen contrast), heading-hierarchy validity, reading order,
orphan/widow detection, TOC/page-reference consistency. This is a different tool from
`html-token-validator.py`, not an extension of it.

**4.7 Long-form content architecture.** Upstream's rhetorical layer is entirely
pitch-shaped: `slide-strategies.csv` covers 15 deck structures, all of them
presentations. There is no equivalent for report structure (executive summary →
methodology → findings → appendix), no citation apparatus, no evidence-hierarchy model.
The *pattern* transfers; every row of content must be built new.

**4.8 Finish the infographics scaffold.** `html-token-validator.py:29,271,277` reserves
the slot. Lowest cost of anything in this list, and the one item where partial upstream
work already exists.

---

## 5. Open questions

1. **What actually executes in the Claude app?** The user's ground truth establishes
   that the skill runs and produces good posters. It does not establish whether Python
   scripts, network calls, or CDN-loaded libraries work there. This matters a lot: if
   code execution is available, a pagination layer can use a real paged-media engine;
   if not, it must be pure CSS + prompt discipline, which is a materially weaker and
   different design. **Settles it:** one empirical test in the Claude app — ask it to
   run `search-slides.py`, and separately ask for an HTML artifact loading Chart.js
   from `cdn.jsdelivr.net` (`html-template.md:14`).

2. **Does CSS Paged Media survive the Claude app's PDF path?** `@page`,
   `page-break-inside`, and named page masters are the cheapest route to pagination —
   *if* whatever converts the artifact to PDF honours them. **Settles it:** produce a
   3-page artifact with `@page { size: A4; margin: 20mm }` and a forced break, then
   export and inspect.

3. **How does the poster path actually reach PDF?** `canvas-design-system.md:200`
   claims "PDF or PNG output" but I found no export mechanism under that skill — no
   renderer, no screenshot call, no PDF library. Either the app supplies it, or the
   user is doing it manually. **Settles it:** ask the user what they physically receive
   from a poster request — a file, an artifact they print, or something they export
   themselves.

4. **Which document types does the user actually need?** This audit ranks by mechanism,
   not demand. A brochure and a whitepaper share almost all their machinery, so row
   ordering barely affects the build — but it strongly affects which demo makes the
   skill look valuable on day one. **Settles it:** ask the user which two documents they
   would use in the first week.

5. **Is CMYK reachable at all, or only specifiable?** Correct CMYK requires ICC profiles
   and a color-managed renderer. It is plausible the honest answer is that a skill can
   only *emit correct intent* (specify profile, warn on out-of-gamut brand colors) and
   must hand off to a real prepress tool. **Settles it:** decide whether "print-ready"
   means press-ready or print-shop-submittable; these are different promises, and
   overpromising here is the fastest way to lose trust with the one audience that would
   notice.

6. **Not determined: whether upstream is still maintained.** If `slides` and `design`
   are diverging copies of the same content (§3.6), a future upstream refactor could
   change what we are cloning. I did not check the git history. Low stakes for a
   mechanism clone; higher if we ever adapt files directly.
