# Alignment with Anthropic's Built-in Document Skills

Source: `research/23-anthropic-builtin-skills.md` — Anthropic's own `docx`, `pdf`,
`pptx`, `xlsx` `SKILL.md` files, exported verbatim from `/mnt/skills/public/` in
the user's claude.ai session. **License: Proprietary** (each file's own
frontmatter: "Proprietary. LICENSE.txt has complete terms"). Everything quoted
below is for internal citation and engineering reference only — nothing from
that file is copied into our own skill; it structurally cannot leak into the
shipped product either, since `research/` sits outside `skill/document-design-intelligence/`
and `scripts/build_zip.py` only ever zips the latter.

## 1. The deferral clause — the single most important finding

Two of the four built-ins carry an explicit deferral clause; two don't:

- **`docx`** (`research/23-anthropic-builtin-skills.md:5`): "...if they ask for
  a document, page, report, memo, or notes WITHOUT naming a file format and the
  session offers a dedicated document or page skill or connector, use that
  instead."
- **`pptx`** (`:422`, restated in the body at `:428`): "...when the user asks
  for a deck, slides, a slide deck, or a presentation without naming a file
  format, default to using a dedicated slide-deck artifact type or a separate
  slides skill if this session offers one; otherwise, use this skill."
- **`pdf`** (`:102`) and **`xlsx`** (`:669`): no equivalent clause. Neither
  describes deferring to a competing skill — there's no generic "spreadsheet
  artifact type" or "PDF artifact type" concept their own text gestures at the
  way `docx`/`pptx` gesture at "a dedicated document/slide skill." This matters
  for §3 below: PDF isn't a handoff target for us, it's a peer output path.

**This is our skill's own activation contract, written by someone else, before
we existed.** `docx` and `pptx` already yield to "a dedicated document/slide
skill" whenever the user doesn't pin a file format — that dedicated skill is
supposed to be us. The boundary has to hold in both directions: we must be
recognizable as that skill (so their deferral actually routes to us and
doesn't just fall through to nothing), and we must yield back when the user
*does* name their format for a mechanical task with no design intent (so we
don't steal traffic that should mechanically go to them).

### (a) Rewritten description — now IS the dedicated skill

No change was needed to remove filename mentions — the shipped description
never mentioned ".docx"/".pptx"/"Word"/"PowerPoint" as our own triggers, and
that was already correct: those belong to the built-ins, not to us, and
including them would blur exactly the boundary this section is about.

### (b) New boundary sentence added

```
When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a
plain conversion or edit with no design ask, use that format's own skill
instead.
```

Mirrors their phrasing pattern (name the condition, name the alternative)
rather than copying their wording. Deliberately **excludes PDF and XLSX** from
this sentence: PDF generation is inside our own scope (§3), and spreadsheets
were never our domain to begin with (report 03/09 never covered tabular
financial artifacts) — including either would misstate the actual boundary.

### (c) Full new description, character count, activation re-check

```
Creates and fixes print/office documents: CVs, resumes, cover letters,
brochures, flyers, posters, reports, whitepapers, slide decks, presentations,
forms, letters, quotes, offers; also note interne, fiche, courrier, affiche,
dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht. Triggers:
make me a CV, write a note interne, turn this into a brochure, I need slides
for Monday, format this report, fais-moi une fiche, erstelle ein Angebot;
quality fixes: looks like AI, looks generic, make it professional, fix the
layout. Applies validated layout, typography, color, print, and ATS rules.
When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a
plain conversion or edit with no design ask, use that format's own skill
instead. Not for web or app UI/UX design (use UI/UX Pro Max for screens).
```

**825 characters** (verified against the live `SKILL.md` file, not just the
draft — up from 667, still comfortably under the confirmed 1,023-character
practical maximum, see `references/activation.md`).

The original 10-prompt activation list (`references/activation.md`) was
re-walked on paper against this change: none of the original 10 needed
rewording, since the new sentence only adds a boundary condition, it doesn't
touch any existing trigger. **3 new prompts added** (now 13 total), testing
the handoff explicitly in both directions:

11. "Turn my rough notes into a Word document." → `docx` should fire (format
    named), we should not.
12. "I need a two-page CV, make it look professional." → we should fire (no
    format named, design intent), and internally hand off to `docx` as a
    renderer rather than `docx` firing as the top-level responder.
13. "Just convert this .docx file to a PDF, don't change anything." → `docx`/
    `pdf` should fire (format named, purely mechanical, no design ask), we
    should not.

Full pass/fail criteria for all 13 are in `references/activation.md`'s
"13-prompt activation test" section (renamed from "10-prompt" to match).

## 2. Structure comparison — what we adopt from their idiom

| Their convention | Where | Adopted? |
|---|---|---|
| A **Dependencies** section, last, one line per dependency, naming exactly what's preinstalled vs. optional-install | `docx:91-93`, `pptx:658-660`, `xlsx:763-765` | **Yes** — added to our body-structure outline (`references/activation.md`). Ours: stdlib Python, Chromium (preinstalled), optional `pip install "weasyprint>=67"`, and the `docx`/`pptx` built-ins themselves as renderer dependencies — a co-installed skill, not a package, which none of their own Dependencies sections have an example of (a genuinely new case for this convention). |
| "Script paths below are relative to this skill's directory" stated once, up front | `docx:19`, `pptx:440` | **Yes**, worth adopting verbatim as a convention once our own `scripts/` grows past the two files it has today — noted for whoever writes the real body. |
| A **Verify the output** / **QA (Required)** step after generation, re-rendering and inspecting the artifact before returning it | `docx:37-47` ("Verify the output"), `pptx:588-656` ("QA (Required)", far more elaborate — content QA, file QA, visual QA, three sub-passes) | **Yes, this is our existing Preflight step, confirmed as the right shape by comparison, not newly copied.** We already had `scripts/preflight.py` and a mandatory post-render validation step before this task started (`09-library-schema.md` §4 items 9-28, `scripts/preflight.py` already built). Seeing pptx's three-tier QA (content/file/visual) suggests our own preflight should eventually grow a similar tiering — noted as a forward-looking observation, not an action taken now (preflight.py's real check set isn't this task's scope). |
| Their **License field** in frontmatter (`license: Proprietary. LICENSE.txt has complete terms`) | all four | **Not adopted as a required field** — Anthropic's own general Agent Skills spec (`research/04-packaging.md` §1.2) lists only `name`/`description` as required frontmatter keys; `license` is optional. We already carry MIT attribution via `LICENSE`/`NOTICE.md` inside the package instead of a frontmatter field, which is the right place for a human-readable license, not a one-line frontmatter tag. No change. |
| Length: `docx` ~95 lines, `pdf` ~415, `pptx` ~300, `xlsx` ~100 | all four | Informative, not adopted directly — confirms our own <500-line target (`research/04-packaging.md` §2) is in the right range; `pdf`'s length is mostly a large flat code-snippet reference section (Quick Reference table + many short examples), a pattern our own `references/*.md` split already anticipates rather than needing to inline everything in `SKILL.md` itself. |
| **A single flat file** for `docx`/`pdf`/`xlsx` (no linked reference files in what was exported) vs. `pptx` explicitly pointing to `REFERENCE.md`/`FORMS.md`-equivalent sub-files (`pdf:110`, `"see REFERENCE.md"`) | `pdf` | Confirms progressive disclosure via linked files is Anthropic's own idiom too, not something we invented — no change, just corroboration of the design already in `references/activation.md`. |

## 3. Render handoff — confirmed field behavior, not a proposal

**This is not a new design decision — it is what already happened.** In the
ENS acceptance run, the model loaded `ui-ux-pro-max:brand` for the brand
rules, resolved the design via `ens-search.sh`, and then used the **public
`docx` skill** (docx-js build, rendered to PDF/JPEG for verification) to
produce the actual file — before this workflow step existed anywhere in our
own documentation. What follows states that confirmed pattern explicitly, in
`SKILL.md`'s placeholder Workflow section, so it's written down as the
intended path rather than left to be independently rediscovered each time.

This skill does not own OOXML generation. After `scripts/resolve.py` returns
the resolved design decision, rendering is a handoff for two of three
targets:

- **`.docx` → hand off to the `docx` skill**, which builds via `docx`
  (npm/docx-js) for new documents or unpack/edit/repack for existing ones
  (`docx:11-16`).
- **`.pptx` → hand off to the `pptx` skill**, which builds via `pptxgenjs`
  (`pptx:430-437`).
- **PDF is NOT a handoff.** This skill's own HTML → headless-Chromium (primary)
  / WeasyPrint (optional fallback) pipeline is the native path
  (`05-SYNTHESIS.md`'s PDF-engine finding — Chromium at
  `/opt/google/chrome/chrome`, confirmed preinstalled). The built-in `pdf`
  skill is a different tool for a different job: it manipulates existing PDFs
  (merge, split, OCR, watermark, forms — `pdf:102`) rather than producing a
  polished, designed document from scratch. Its own description never claims
  the latter, and it carries no deferral clause the way `docx`/`pptx` do
  (§1) — there's nothing to hand off to or receive from on the PDF path; the
  two skills simply don't overlap.

After rendering (by either path), `scripts/preflight.py` runs against the
actual artifact; on refuse, fix the named problem and rerun rendering before
returning anything — this loop was already the design (§4 items 9-28), now
stated explicitly as the last two steps of the workflow.

### Resolver vocabulary mismatches — change requests for `resolve.py` (not yet built)

Checked their skills' stated input expectations against what our schema
(`research/09-library-schema.md`) will need to hand them. None of these block
anything today (the resolver doesn't exist yet), but whoever builds it needs
to know the resolved-decision block has to speak the target renderer's
vocabulary, not just our own:

1. **Units**: `docx`-js page size is DXA (twips; 1440 = 1 inch — `docx:25`).
   Our `T7 page-formats.csv` (schema §T7) is expected to store physical page
   dimensions in mm, matching print-domain convention. **Change request**: the
   handoff step needs a mm→DXA conversion before calling `docx`, or `resolve.py`
   should emit both units.
2. **Slide dimensions are a separate physical format from print pages**:
   `pptxgenjs` defaults to `LAYOUT_16x9` = 10″×5.625″, not 13.3″ wide
   (`pptx:454`) — `pres.layout` must be set explicitly before adding slides.
   Our `T7` table's rows are page-format-shaped (trim/margins for print); a
   presentation target needs its own slide-dimension rows, not a repurposed
   print page format. **Change request**: `T7` (or a new small table) needs a
   `Slide Layout` value (`LAYOUT_16x9` / `LAYOUT_WIDE` / custom) distinct from
   print trim sizes.
3. **Color format differs per renderer**: `pptxgenjs` wants hex **without**
   `#` and never an 8-digit (alpha) hex — `"FF0000"`, not `"#FF0000"`
   (`pptx:455`, explicitly: both forms "corrupt the file"). Our `T4
   palettes.csv` (schema §T4) is expected to store standard `#RRGGBB`.
   **Change request**: the `.pptx` handoff path must strip the leading `#`
   before calling `pptxgenjs`; the `.docx` path's own color format needs the
   same check (not yet verified against docx-js's expectations, since the
   exported `docx` SKILL.md doesn't specify a color-argument format the way
   `pptx`'s does — flag as unverified, not assumed safe).
4. **Heading structure for `.docx` TOC**: `docx`'s TOC requires built-in
   `HeadingLevel.*` styles; custom heading styles need `outlineLevel` set or
   they won't appear in the TOC (`docx:33`). Our `T10 structures.csv`'s
   `Heading Depth` column needs a documented mapping onto `HeadingLevel`
   specifically when the render target is `.docx` — **change request**: note
   this mapping requirement against `T10` once `resolve.py` exists.
5. **Naming, not units**: `pptxgenjs`'s `letterSpacing` option is silently
   ignored; the real option is `charSpacing` (`pptx:458`). If our schema ever
   emits a letter-spacing value for slide decks (not currently planned per
   `T3`/`T6`), the handoff step must translate the property name, not just
   pass it through.

These five are genuine, sourced mismatches — not speculation — but none of
them can be resolved until `resolve.py`'s actual output shape exists. Recorded
here so the resolver's author doesn't have to re-derive them from these two
proprietary files again.

## 4. `brand-guidelines` example skill — found separately, compared

Not in `research/23`; the user exported it separately to
`research/23b-brand-guidelines-skill.md` (88 lines: `SKILL.md` verbatim + a
directory listing showing only `LICENSE.txt` and `SKILL.md` — no data files,
no scripts). Read in full. The comparison against our own overlay design is
short because the architectures aren't close:

**What it is**: a single, hardcoded, single-brand skill. Its own description
(`23b:6`) — "Applies Anthropic's official brand colors and typography to any
sort of artifact that may benefit from having Anthropic's look-and-feel" —
names exactly one brand (Anthropic's), with the four main colors, three
accent colors, and two font choices written directly into the SKILL.md body
as literal markdown values (`23b:22-38`). There is no brand slug, no
multi-brand concept, no data table, no merge mechanism, no equivalent of our
`data/brand/<slug>/` overlay at all — it is architecturally "one skill = one
brand," not "one skill, many brand overlays," which was never going to
transfer to a product meant to serve users with their own distinct brands
(ENS being the proof case).

**The one finding worth keeping — it independently confirms our own
diagnosis.** The skill's own description calls itself a **"post-processing"**
step (`23b:6`) — applied to "any sort of artifact," implying it runs *after*
a document/deck already exists, adjusting colors and fonts on top of
whatever was already generated with generic defaults. That is precisely the
failure mode `research/09-library-schema.md` §0.3 diagnosed from the ENS field
evidence and built the schema specifically to avoid: *"The identity is an
instruction, not data"* — generation happens first against generic rows, and
brand is patched on as an afterthought, where every patch is a judgment call
that can drift or be skipped. **Anthropic's own official reference example
for "how to apply a brand" is built exactly that way.** This isn't a
hypothetical anti-pattern we're guarding against — it's the pattern their own
example ships. Our design (brand rows inside the searched tables,
resolved *during* generation, not patched after) remains the right call,
now with a second independent data point supporting it.

**One minor idiom, considered and rejected**: the skill lists a `**Keywords**:`
line in its body (`23b:16`) in addition to its frontmatter `description` —
a second, separate copy of trigger terms. Not adopted: this is exactly the
"more than one place describing what a skill does" pattern `research/04-packaging.md`
§1.1 and `research/11-upstream-releases.md` §5 both flag as upstream's
own drift bug (four descriptions, one of them silently stale for a month).
One canonical description stays the rule here.

## 5. Edits applied (summary — see each file for the actual diffs)

- **`skill/document-design-intelligence/SKILL.md`**: description replaced
  (825 chars, verified against the live file); Workflow section's render step
  rewritten to state the handoff as confirmed field behavior (the ENS
  acceptance run already did this), not a new proposal (§3).
- **`skill/document-design-intelligence/references/activation.md`**: shipped-
  description block updated with new text/length/rationale; body-structure
  outline gained a "Render by handoff" workflow step, a new "Dependencies"
  section, and a forward pointer to a future `render-handoff.md` reference
  file; activation test list extended from 10 to 13 prompts (§1c) and
  retitled accordingly.
- **`skill/README.md`**: new paragraph in the intro stating plainly that
  `.docx`/`.pptx` generation is handed off to Anthropic's built-in skills and
  PDF is rendered natively, with a pointer to this report.
