# BRIEF — Packaging Analyst — TWO FIXES, IN THIS ORDER

Two tasks, one brief, two deliverables. **Do PART A first and write its file before starting
PART B.** You were paused by delivery limits earlier today; durable partial output beats a
complete report that never lands.

Context you need and nothing more: you just fixed the dropped-columns P0
(`research/54-display-columns-fix.md`). Both fixes below live in the same resolution path and
the same file, `scripts/ddi.py`. Findings D3 and the png gap are in
`research/51-invoked-quality.md`.

## RULES, unchanged and binding
- **No git, ever.** The orchestrator owns git.
- **`data/schema-manifest.json` is GENERATED.** Never hand-edit it; edit `research/build-manifest.py`
  and regenerate.
- **NO ZIP REBUILD.** Ruled by the lead: nothing is rebuilt until the candidate M browser trial
  returns a verdict, so one rebuild bundles everything.
- `python` is broken here. Use **`python3`** (3.12.10).
- Tag CONVENTION for anything you cannot grep-verify in this repo.
- Every test asserts on **resolved JSON and rendered handoff text**, never on rows or the
  manifest. Ask what it would say if the feature produced NOTHING AT ALL; if it would still
  pass, it is not a test.

---

# PART A — TASK 01a0901c: a projector is being handed the CV's print type scale

## The defect
`slide-deck-projection` resolves `cv-print-print-body/h2/h1` at 11/16/24pt, with `Medium: print`.
**A projected deck gets 11pt body text.**

The correct scale EXISTS and is reachable by nothing:

    deck-projection-projection-body,deck-projection,projection,body,24,1.25
    deck-projection-projection-body-dense,deck-projection,projection,body-dense,18,1.25
    deck-projection-projection-h1,deck-projection,projection,h1,36,1.10

## The root cause, already traced — do not re-derive it
The ONLY route to a type scale is `typefaces."Scale Key"`. `doc-reasoning/deck-generic` points at
`safe-sans-arial`, whose `Scale Key` is `cv-print`. No typeface anywhere references
`deck-projection`, so those three rows are unreachable.

## THE CONSTRAINT — binding, and the reason this task is not trivial
**DO NOT fix this by changing `safe-sans-arial`'s `Scale Key`.** Arial is ALSO the CV's face and
the CV needs `cv-print`. The Coverage analyst identified this and refused that one-constant fix;
the lead made the refusal binding. Retargeting Arial would move the deck right and the CV wrong,
and the CV is the best-exercised path in the library.

Cite the 2026-09-09 precedent, refusing the green tick, if you are tempted by a one-constant
change: a passing number and a working product disagreeing means this project fixes the product.

## What to decide
The medium, not just the face, has to reach the scale. A CV and a projected deck can share a
typeface and must not share a type scale. Work out where that selection belongs — a new typeface
row for projection use, a medium-aware lookup, a doctype-level scale override, or something
else — and **justify the choice against the alternatives you rejected.** Say what your fix does
to the CV path, and prove the CV is unchanged.

## Prove it
Paste real before/after for both, because the CV is the regression risk:

    python3 scripts/resolve.py --doctype slide-deck-projection --json > <path>
    python3 scripts/ddi.py handoff --json <path> --format pptx
    python3 scripts/resolve.py --doctype cv-uk --json > <path>
    python3 scripts/ddi.py handoff --json <path> --format docx

Deck must show projection sizes. **CV must be byte-identical to before.** Full pytest green.

**Deliverable: `research/57-deck-projection-fix.md`.** Then report to me before starting PART B.

---

# PART B — TASK 01a0902f: png has no handoff builder at all

## The defect
`_FORMAT_BUILDERS` (`scripts/ddi.py:683`) covers `docx`, `pptx`, `pdf` — that is all.
`infographic`'s ONLY render target is `png-social`, whose `Format` is `png`. So that family has
**no handoff path whatsoever.** Not missing wording: no builder.

Note the CLI too — `ddi.py handoff --format` currently accepts only `{docx,pptx,pdf}`. Extend it.

## The lead's ruling, and why the easy options were refused
**Author a builder.** Retargeting `infographic` to another format HIDES the gap, and shipping a
stated limitation is the v0.2 failure shape again. `infographic` is a SHIPPED family, and
RESUME.md's own v0.3 standing rule says a format is DONE only when it produces a good result
when the skill runs.

## What the builder emits
Pixel dimensions, typefaces, sizes and palette, in **CSS/pixel idiom** — px and `#hex`. Do NOT
copy docx's DXA or half-point conversions, and do not copy pdf's mm `@page`; a png has no page.

**You already have a real source for the dimensions — do not invent them.** `png-social`'s
`Engine Invocation` carries them:

    --headless --no-sandbox --disable-gpu --screenshot=%o --window-size=1080,1350 %i

`Font Rule` is `embed`. `Print Tier Max` is `none` and `Supports Paged Media` is `n/a`, so
bleed, crop marks and paged-media constructs must NOT appear. If you parse `--window-size`, say
so explicitly and say what happens when it is absent or malformed.

## The rule that made this defect invisible for a whole release
Where a concept genuinely does not apply to png, **emit the ruled
`(not present in this resolution)` sentence — do NOT omit the block.** Omission is exactly how
the pdf gap hid. A missing block is invisible; an empty one is a fact.

## Prove it
    python3 scripts/resolve.py --doctype infographic --json > <path>
    python3 scripts/ddi.py handoff --json <path> --format png

Paste the actual output. Same test standard as everything else. Full pytest green.

Also say plainly whether `infographic` now MEETS the v0.3 standing rule, or what still stands
between it and meeting it. That is the question the task exists to answer.

**Deliverable: `research/58-png-handoff.md`.**

---

## Report to me after EACH part, in a few lines
Part A: deck shows projection sizes yes/no, CV unchanged yes/no, pytest green yes/no.
Part B: png builder emits what, infographic meets the standing rule yes/no, pytest green yes/no.
