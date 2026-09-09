# T6 type-scales draft — notes (research/30-t6-type-scales-draft.csv)

22 rows, `csv.reader`-clean, 6 columns matching the manifest's
`scale_row_key,scale_key,Medium,Role,Size pt,Leading Ratio` header exactly (no `Value Basis`
column — per `09-library-schema.md` "Why the floors are T9 rows and not a `Value Basis`
column on T6," floors live in `constraints.csv`, not here). `scale_row_key` = the fixed
`<scale_key>-<medium>-<role>` pattern from the prior handover. 8 `scale_key` values covered,
closing every FK the brief named: `cv-print`, `form-print`, `report-print`, `report-screen`,
`report-technical`, `ens-print` (all 6 that `data/base/typefaces.csv` references — verified
by script, zero dangling), plus `deck-projection` and `print-office-generic` (not referenced
by any shipped T5 row, authored anyway per the brief).

## Sourced rows (4) — report 03 CONVENTION tuples, `09-library-schema.md` lines 894-903

```
deck-projection | projection | body       | 24 | 1.25
deck-projection | projection | body-dense | 18 | 1.25
deck-projection | projection | h1         | 36 | 1.10
```
These three are copied verbatim from the manifest's own "Example rows" block (lines
945-954) — not re-derived, to keep this file traceable to the one place the source tuples
are already transcribed. `body-dense`'s 18 pt is the *dense-callout exception*, not a
default (manifest's own wording) — do not read it as a lower floor for ordinary body text.
`screen`'s sourced 18-20 pt floor (report 03 §B) was deliberately **not** given its own
`scale_key` row here: that convention is scoped to "screen-only decks" (canvas artifacts),
the brief's required-key list does not include a `deck-screen` key, and `deck-generic`'s
Reasoning-Key split that would have consumed it was withdrawn this same pass (see
`26-notes.md` UPDATE 2, `29-t2-doc-reasoning-draft.csv`'s merged `deck-generic` row) — so
there is currently no `scale_key` that convention would attach to. Flagged, not silently
dropped: if a screen-medium deck scale is authored later, 18 pt body is already sourced and
waiting in report 03 §B.

## ENS brand-authored rows (7) — `ens-print`, print medium

```
label   8.5 / 1.20   caption 9   / 1.20   body 11 / 1.35   lead 12 / 1.30
h3      16  / 1.15    h1      24  / 1.10   legal 8.5 / 1.20
```
`label`/`body`/`h1` are the manifest's own given ENS example rows (lines 948-950), copied
verbatim. `caption`, `lead`, `h3`, `legal` are new this pass, sized and given a Leading
Ratio consistent with that example's pattern (small roles tight ~1.20, body/lead ~1.30-1.35,
headings tighten toward `h1`'s 1.10) — **brand-authored constants, not sourced**, exactly
per T6's own rule that print rows have no absolute point-size floor in report 03 (only the
CPL/leading *ratio* formula is sourced). `rationale/type-scales.md` must record all seven as
ENS house decisions, not thresholds, per that same rule.

**`legal` role — the reason it exists at all.** `constraints.csv`'s `legal-text-min-size`
row (`legal-text` Set Key, `medium=print;role=legal`, threshold 8, warn) already expects a
`role=legal` type-scale row on any Scale Key a `legal-text`-bound doctype resolves to. Two
T1 doctypes bind `legal-text`: `form-handfilled` (Typeface Key `ofl-public-sans` → Scale Key
`form-print`) and `ens-formulaire` (Typeface Key `ens-manrope-inter` → Scale Key
`ens-print`). Both therefore need a `legal` row, not just ENS's — see `form-print` below.
8.5 pt on both keeps a hair of headroom above the 8 pt warn floor; picking the same number on
both is a consistency choice, not a second, independent brand decision.

**Role enum — already widened, confirmed on disk, not a gap.** The plan (prior handover)
was to flag `Role`'s enum as needing `legal` added, the same precedent as T12's `customary`
(`09-library-schema.md` lines 1603-1620: a value added because authored data used it and the
enum didn't have it yet). Checked `schema-manifest.json` directly this pass:
`type-scales.enums.Role` already lists `legal` as its first value — someone else's edit
landed concurrently. Nothing left to do here; noted only so nobody re-flags it as open.

## Generic/dangling-FK rows (11) — deliberately minimal, and why

`print-office-generic` (6 roles: `label`/`caption` 8.5, `body` 11, `h3` 12, `h2` 16, `h1`
24; leading 1.20 on every role except `body` at 1.35) is the one fully-fleshed generic scale
this pass authors, per the fixed prior plan — every value stays inside T9's
`report-leading-ratio` check (`[1.20, 1.45]`), unlike the ENS/deck sourced examples where
`h1`'s leading legitimately drops to 1.10.

The other five keys this file closes (`cv-print`, `report-print`, `report-technical`,
`report-screen`, `form-print`) exist only because `typefaces.csv` already commits to their
names — nothing in report 03 or any brand doc gives any of them a reason to differ from
`print-office-generic`'s own authored constants. Rather than inventing five more distinct
label/caption/heading scales with no source and no house decision behind them (the exact
"unsourced-threshold mistake flagged repeatedly across this project" — `26-notes.md`, T11's
`Min Physical Size mm`, T1's gate-fold split), each gets **one row**: the single `body` role
every render path and both T9 formula validators (`validate-measure`, `validate-leading-ratio`
— `S`/`L` are read from `Medium=print, Role=body`) actually consume, reusing
`print-office-generic`'s exact 11 pt / 1.35 constant verbatim. `form-print` gets a second row
(`legal`, 8.5/1.20) for the reason above. `report-screen` gets the same 11/1.35 pair under
`Medium=screen` rather than `print` — there is no sourced or house reason for a report read
on-screen to size differently from one printed (the manifest's own sourced screen convention
is explicitly scoped to canvas decks, not flow reports; see above), so this is a medium-tag
change on a reused constant, not a second unsourced number.

**This is a duplication smell, stated as a finding, not hidden.** Five of eight `scale_key`
values in this file (`cv-print`, `report-print`, `report-technical`, `report-screen`,
`form-print`, arguably `print-office-generic` too) carry identical or near-identical
authored numbers under different names, purely because T5 already named five distinct keys
before any of them had a design reason to differ. Recommend, as the prior handover already
did: collapse `cv-print`/`report-print`/`report-technical`/`report-screen`/`form-print` in
`typefaces.csv` to point at `print-office-generic` directly in a later revision, unless
someone produces an actual sourced or brand reason for one of them to diverge. Not done here
— editing the shipped `typefaces.csv` is outside this task's scope (T6 authoring only), and
the FK direction runs T5 → T6, so leaving five thin T6 rows is the non-destructive way to
close the dangling-FK finding without touching T5.

## Remaining FK / design gaps, not resolved here

- **`ens-slides` has no path to a projection-medium scale, and this pass makes the gap
  worse-defined, not smaller.** `ens-slides`' Typeface Key (`ens-manrope-inter`) resolves to
  `ens-print` — print-medium only. ENS slides are projected. Before this pass, `29`'s own
  `ens-slides` row used `if_projected=constraint:proj-body-floor` as its *only* path to a
  projection floor (its T1 row binds `ens-house;ens-deck-density`, not `projection`, in
  `Constraint Set Keys` — unlike the generic `slide-deck-projection` row, which reaches
  `proj-body-floor` through `Constraint Set Keys` directly and never needed the condition).
  Revision 3 deletes `if_projected` from `DOC_CONDITION_SIGNALS` outright (see `26-notes.md`
  UPDATE 2) with no replacement mechanism for a brand-scoped case like this one. Net effect:
  `ens-slides` currently has **no authored or reachable path** to any projection-scale
  numbers at all — not `ens-print` (print-only), not `deck-projection` (nothing points
  `ens-manrope-inter` there), not a Doc Condition (deleted). This is a real, currently-open
  gap, not something this file's `deck-projection` rows fix by existing — a fix needs either
  a new ENS typeface row pointing at `deck-projection` (the prior handover's recommendation,
  since ENS's own sourced numbers — title 36-40/body 24/dense 18-20, v2 §3D — already
  coincide with `deck-projection`'s sourced values) or a new `Constraint Set Keys` entry on
  `ens-slides`' T1 row containing `projection` alongside `ens-house;ens-deck-density`. Both
  are T1/T5 authoring decisions outside this task's scope; flagging so whoever owns those
  tables sees it before shipping ENS slides.
- **`safe-sans-deck` Typeface Key is still PROPOSED.** No T5 row exists under this name.
  `deck-generic` (the merged T2 row, post-revert) still points at it. This file gives it
  somewhere to resolve *once a T5 row exists* (the `deck-projection` Scale Key), but does not
  create the T5 row itself — not this task's table.
- **The five-key duplication smell above** is flagged, not fixed, per the scope note there.
