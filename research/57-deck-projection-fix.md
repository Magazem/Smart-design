# 57 — deck-projection type scale fix (v0.3 D3 / task 01a0901c)

## The defect
`slide-deck-projection` resolved `cv-print` (11pt body, 16pt h2, 24pt h1, `Medium: print`)
instead of `deck-projection` (24pt body, 18pt body-dense, 36pt h1, `Medium: projection`).
`type-scales.csv` already carried the correct `deck-projection` rows — they were reachable
by no typeface. Root cause: the only route to a type scale is `typefaces."Scale Key"`, and
`doc-reasoning/deck-generic`'s `Typeface Key` pointed at `safe-sans-arial`, whose `Scale Key`
is `cv-print` (the CV's scale).

## The constraint honoured
Did NOT touch `safe-sans-arial`'s `Scale Key`. Arial is also the CV's face; the CV needs
`cv-print`; retargeting it would have moved the deck right and the CV wrong (the 2026-09-09
"refusing the green tick" precedent — a passing number and a working product disagreeing
means fix the product, not the constant).

## Where the fix lives, and why
**A new typeface row, `safe-sans-deck`** (`research/19-t5-typefaces-draft.csv`), Arial faces,
`Scale Key: deck-projection`. `doc-reasoning/deck-generic`'s `Typeface Key` (`research/29-t2-
doc-reasoning-draft.csv`) now points at it instead of `safe-sans-arial`. Both files are loader
inputs; `research/load-base.py` was run to regenerate `data/base/typefaces.csv` and
`data/base/doc-reasoning.csv` — nothing under `data/base/` was hand-edited, per the standing
rule ("only the loader writes there").

This is not a new mechanism; it completes one the project already specified and shelved.
`research/29-t2-doc-reasoning-draft.csv`'s own Reasoning cell for `deck-generic` said the
`Typeface Key` "was `safe-sans-deck`, which does not exist as a T5 row" and had been
temporarily repointed to `safe-sans-arial` as a stopgap (ruling B4). `research/30-notes.md`
(T6 authoring pass) says the same thing from the other side: "`safe-sans-deck` Typeface Key
is still PROPOSED. No T5 row exists under this name... This file gives it somewhere to
resolve once a T5 row exists (the `deck-projection` Scale Key), but does not create the T5
row itself." The `deck-projection` scale rows have been sitting there, sourced and unreachable,
since that pass. Authoring the row it was waiting for closes the gap with zero new
architecture: no manifest column, no code change to `resolve.py` or `ddi.py` — the existing
`typefaces.Scale Key -> type-scales.scale_key` FK walk just now has a second, correctly-scoped
place to land.

### Alternatives considered and rejected
- **Medium-aware lookup in `resolve.py`.** Would need a new signal per doctype (a render
  medium) independent of `Typeface Key`, a manifest change, and code in the FK walker that
  every other table's resolution doesn't need. Bigger surface for a fix that data alone
  already solves, and it duplicates the routing implied by `render-targets.Format` /
  `doctypes."Constraint Set Keys"` for the projection/screen/print split.
- **Doctype-level scale override column.** Same shape of cost (schema + loader + resolver
  change) for one family. The FK-only fix generalises for free: `slide-deck-document` and
  `slide-deck-handout` also now resolve `safe-sans-deck` / `deck-projection`, whereas an
  override keyed to `slide-deck-projection` alone would have left the other two decks on the
  CV's scale.

### What this does to the CV path
Nothing. `safe-sans-arial` is byte-identical; `cv-*` doctypes never referenced `safe-sans-deck`.
Proven below.

## Proof

Gate: `python3 scripts/validate_data.py data/base` → `OK: validated 14 table(s), 425 row(s)`
(was 424; +1 row is the new typeface). Full suite: `python3 -m pytest -q` →
**164 passed, 68 subtests passed** (unchanged from before the change).

CV, before vs after (`resolve.py --doctype cv-uk --json`, then `ddi.py handoff --format docx`):
**byte-identical** — `diff` on both the resolved JSON and the rendered handoff text produced
no output.

Deck, before:
```
type-scales/cv-print-print-body   Medium: print   Role: body   Size pt: 11
font sizes (pptxgenjs pt): body: 11pt   h2: 16pt   h1: 24pt
```

Deck, after (`resolve.py --doctype slide-deck-projection --json`, then
`ddi.py handoff --format pptx`):
```
resolved.typefaces[0] = {key: safe-sans-deck, Scale Key: deck-projection, ...}
resolved.type-scales  = [
  {key: deck-projection-projection-body,       Medium: projection, Role: body,       Size pt: 24},
  {key: deck-projection-projection-body-dense, Medium: projection, Role: body-dense, Size pt: 18},
  {key: deck-projection-projection-h1,         Medium: projection, Role: h1,         Size pt: 36},
]
font sizes (pptxgenjs pt): body: 24pt   body-dense: 18pt   h1: 36pt
```

`slide-deck-document` and `slide-deck-handout` (siblings sharing `deck-generic`) were also
checked and now resolve `safe-sans-deck` / `deck-projection` — consistent with the existing,
already-documented trade-off that the merged `deck-generic` key gives all three decks the same
design payload (Revision 3 revert; see `29-t2-doc-reasoning-draft.csv`'s Reasoning cell). Before
this fix all three got the CV's print scale; now all three get the projection scale, which is
strictly correct for the projection case and no worse than before for the handout case.

## Files touched
- `research/19-t5-typefaces-draft.csv` — +1 row, `safe-sans-deck`.
- `research/29-t2-doc-reasoning-draft.csv` — `deck-generic.Typeface Key` `safe-sans-arial` ->
  `safe-sans-deck`; Reasoning cell updated to record the fix and its sourcing.
- `research/load-base.py` — T5's `CHANGES` log line was hardcoded to "8 rows" from the pass
  that wrote it; parameterised, plus a new entry documenting this change. No behavioural change.
- `data/base/typefaces.csv`, `data/base/doc-reasoning.csv` — regenerated by
  `research/load-base.py` (not hand-edited).

## Report
Deck shows projection sizes: **yes**. CV byte-identical: **yes**. Pytest green: **yes**
(164 passed, 68 subtests).
