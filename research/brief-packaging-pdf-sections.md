# BRIEF — Packaging Analyst — SHIP-BLOCKER: the pdf handoff emits no sections

Deliverable: the fix, a test, and `research/65-pdf-sections-fix.md`.
**This blocks the v0.3 tag.** The acceptance gate returned DO NOT SHIP on this alone.

## THE DEFECT — confirmed independently, do not re-diagnose
`_sections_lines` is called at three of four sites:

    ddi.py:513   _build_docx_lines
    ddi.py:576   _build_pptx_lines
    ddi.py:766   _build_png_lines
    _build_pdf_lines (603-706)  -- NOT CALLED

So the pdf handoff has **no sections block at all.** Not empty: absent. The decisive control,
which I ran myself on the built artefact — the SAME resolved payload:

    handoff --format docx  ->  sections: issuer: From / bill-to: Bill To / invoice-details: ... (6 more)
    handoff --format pdf   ->  nothing. No block.

## WHY THIS IS SHIP-BLOCKING
**9 of 30 doctypes have a pdf render target and NO docx or pptx target** — five brochures, the
poster, `quote-devis`, `invoice-tabular`, `form-handfilled`. For every one of those families the
headline P0 of this release, heading wording reaching the output, **is simply unfixed.** The
handoff block is the sole specification a renderer receives.

The analyst closed the one escape hatch before filing: SKILL.md's "renders PDF itself" does NOT
mean a second route. `lib/pdf.py` is a stdlib PDF *reader*, imported only by `preflight.py`, and
there is no renderer or HTML emitter anywhere in `scripts/`. Do not go looking for one.

**THIS IS MY MISS, NOT YOURS.** When I briefed the handoff work I named docx and pptx. png was
added later and correctly picked it up. pdf was never named and nobody noticed. That is exactly
the half-fix shape this project keeps hitting, and it is why the gate exists.

## THE FIX
One line, matching the three existing call sites. Put it where the other builders put it, so the
block lands in a consistent position in the output.

**Then look at the rest of `_build_pdf_lines` with the same eye.** The gate also filed D-J: the
pdf path silently omits page flow where five constraints had resolved. **If you can see that it
is the same one-line omission, fix it in this task and say so. If it is anything more than that,
STOP and report it — do not let a ship-blocker fix grow.**

## THE TEST — this is the part that must not be weak
Assert on the **rendered handoff text for a pdf-only family**, not on rows and not on the
manifest. The gate named the exact assertion: `issuer: From` appears in the pdf block for
`quote-devis`.

Ask what your test would say if the feature produced NOTHING AT ALL. If it would still pass, it
is not a test. A test that merely checks the string "sections" appears is weak — assert a real
wording.

Add it so it fails before your fix and passes after. Say that you checked both.

## ALSO IN SCOPE — one documentation correction
SKILL.md still says `infographic` "has no Structure Key and so gets no section order". **That is
now false** — it resolves `infographic-canvas` with three sections. Fix it in the **SKILL.md
source**, not in the extracted artefact.

**Careful: SKILL.md's frontmatter description is at 1010 of 1023 characters, 13 to spare.** This
correction is in the BODY, not the description, so it costs no budget — but do not touch the
description, and do not disturb either test marker.

## RULES
- **No git, ever.** The orchestrator owns git.
- Never hand-edit a generated file, and **never edit the extracted artefact** in
  `research/test-builds/` — that is the thing under test. Fix the source; I rebuild.
- `python` is broken here; use **`python3`**.
- Full pytest green, report the count.

## PROVE IT
Paste the pdf handoff for `quote-devis` before and after, showing the sections block with real
wordings where there was none. Then do the same for one more pdf-only family.

Report: sections in pdf yes/no, page-flow question answered, test added and failing-before
confirmed, SKILL.md corrected, pytest count.
