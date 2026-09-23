# research/library/type-scales/ratio-families-evidence.md — P3.7 ratio-family type scales

Scope: research/80 §4 ("ratio families (minor-third, major-third, perfect-fourth) x
print/projection/screen"). Discipline per research/80 R-d: this document only cites what a
fetched copy of modularscale.com actually shows, plus the base sizes/leading conventions already
established in existing complete `type-scales.csv` rows (report-print / print-office-generic /
deck-projection / report-screen), per research/70's own citation method.

## 1. Ratio source (fetched)

[modularscale.com](https://www.modularscale.com/) — fetched directly this task (2026-09-23; also
fetched previously in research/70 and quoted in research/81's "Type scales" table). The static
markup lists named ratios with numeric values:

> <a href="javascript:rS(1.067)">15:16 – minor second</a>, <a href="javascript:rS(1.2)">5:6 –
> minor third</a>, <a href="javascript:rS(1.25)">4:5 – major third</a>, <a
> href="javascript:rS(1.333)">3:4 – perfect fourth</a>, <a href="javascript:rS(1.5)">2:3 – perfect
> fifth</a>, <a href="javascript:rS(1.618)">1:1.618 – golden section</a>

**Corrected (fix 18)**: the block above quotes the markup as it actually renders (named ratio as
the link text, `rS(...)` supplying the decimal as a click-to-apply argument, not prose). The
previous version of this evidence reformatted it as flowing prose ("minor third 5:6 (1.2)") and
silently omitted named ratios that the live page also lists between/around these entries (e.g.
"aug. fourth", "minor sixth") — this quote is a verbatim excerpt of the entries relevant to this
task's three ratios, not the page's complete named-ratio list.

The three ratios used here — **minor third = 1.2**, **major third = 1.25**, **perfect fourth =
1.333** — are exactly the three named in the task brief and are all present, with these numeric
values, in the fetched page (research/81 row "modularscale.com | named ratio scale", Fetch =
fetched). `cv-major-third` (major third, 1.25) and `cv-editorial-fourth` (perfect fourth, 1.333)
already use two of these same ratios for the CV family only (data/rationale/type-scales.md); this
task extends ratio coverage to three generic mediums (print, projection, screen) with a fuller
role set, independent of the CV-specific rows.

## 2. Mediums

The manifest's `Medium` enum (`skill/.../schema-manifest.json`, `type-scales` table) is exactly
`print`, `projection`, `screen` — these map 1:1 onto the task's "print, projection (slides),
screen" and are used unchanged.

## 3. Base sizes and leading conventions (cited from existing complete rows)

| Medium | Base role | Base size pt | Base Leading Ratio | Cited row (`data/base/type-scales.csv`) |
|---|---|---|---|---|
| print | body | 11 | 1.35 | `print-office-generic-print-body` (also `report-print-print-body`, `report-technical-print-body`, `cv-print-print-body`, `form-print-print-body` — all identical: 11pt/1.35) |
| projection | body | 24 | 1.25 | `deck-projection-projection-body` |
| screen | body | 11 | 1.35 | `report-screen-screen-body` |

Note (screen == print numerically): `report-screen-screen-body` happens to carry the exact same
size (11) and Leading Ratio (1.35) as the print body rows. This is not an error introduced here —
it is the pre-existing value in `data/base/type-scales.csv` line 19 — and it is a deliberate
citation, not an invented number: `report-screen` is a **flow** artifact (a printed/PDF-style
report read on a screen), not a **canvas** artifact, so the `screen-body-floor` constraint
(`constraints.csv`, `Applies To = artifact-class:canvas`, threshold 18) does not apply to it. The
canvas-class screen precedent already in the base data is `infographic-screen-screen-body` (24pt),
which does clear that floor. The new `lib-*-screen` scale rows below follow the `report-screen`
(flow) precedent, since that is the only existing complete "screen" scale with a role structure to
generalise from; see §5 for the floor implication.

**Role set per medium** (per task: "look at report-print / print-office-generic / deck-projection
for role sets"):
- print and screen: `print-office-generic`'s six-role hierarchy — `label`, `caption`, `body`,
  `h3`, `h2`, `h1` (data/base/type-scales.csv rows `print-office-generic-print-*`). Applied
  identically to `screen` since no existing screen scale has more than one role (`report-screen`
  has only `body`) — the print role hierarchy and its per-role Leading Ratio convention (label
  1.20, caption 1.20, body 1.35, h3 1.20, h2 1.20, h1 1.20) is the nearest sourced generalisation.
- projection: `deck-projection`'s three-role set — `body-dense`, `body`, `h1`
  (data/base/type-scales.csv rows `deck-projection-projection-*`), with its Leading Ratio
  convention (body-dense 1.25, body 1.25, h1 1.10) carried over unchanged.

All six roles used (`label, caption, body, h3, h2, h1, body-dense`) are members of the manifest's
`Role` enum (`legal, label, caption, body, body-dense, lead, h3, h2, h1`); no invented role is
used, and `legal`/`lead` are not used (no existing print/screen/projection complete scale uses
them for a body-text hierarchy).

## 4. Step method (modular-scale steps from base body)

**Corrected (fix 16)**: `data/rationale/type-scales.md` and research/70 describe "H1 takes three
ratio steps" as "a standard modular-scale practice modularscale.com itself describes". The fetched
copy of modularscale.com (§1 above) contains no such statement anywhere in its markup; its only
heading-size guidance is "If you know what size you want a heading to be, type the target value @
position on the scale like 36@5" — a UI instruction, not a claim about how many steps a heading
should take. The "H1 = three steps" convention is this project's own derived convention,
inherited from research/70, and is not attributable to modularscale.com; the attribution is
removed here and in `data/rationale/type-scales.md` should be corrected the same way.

**Corrected (fix 17)**: this task applies an integer step map (label/caption/body-dense = -1, h3 =
+1, h2 = +2, h1 = +3) uniformly across all three ratios and three mediums, describing it
previously as "generalising the existing hierarchy shape (sub-body one step down; heading roles
one, two, three steps up)". That is not what the existing ratio scales do: `cv-major-third` steps
h2 = +1 and h1 = +3 (10.5 -> h2 13 -> h1 20, i.e. h2 and h1 are not consecutive steps apart), and
`cv-editorial-fourth` does the same (10.5 -> h2 14 -> h1 25); `print-office-generic` (12/16/24) is
not a modular scale at all (16/12 = 1.333 but 24/16 = 1.5, two different ratios, so it cannot be
read as any consistent step count). The -1/+1/+2/+3 step map used in this batch is therefore this
task's own derived convention, not a generalisation of a precedent that already used it -- it is
declared as such here, not as an extension of existing practice:

| Role | Step (n) from body | Applies to |
|---|---|---|
| label / caption / body-dense | -1 | print, screen (label, caption) / projection (body-dense) |
| body | 0 (= medium base) | all |
| h3 | +1 | print, screen |
| h2 | +2 | print, screen |
| h1 | +3 | print, screen, projection |

Size = `round_to_0.5(base × ratio^n)`. Leading Ratio is **not** derived from the ratio (it is a
line-height convention, independent of the type-size ratio) — it is carried over unchanged from
the cited medium convention in §3, per role.

## 5. Computed tables

### Print (base 11pt, roles from `print-office-generic`)

| Role | n | minor-third (1.2) | major-third (1.25) | perfect-fourth (1.333) | Leading Ratio |
|---|---|---|---|---|---|
| label | -1 | 9 | 9 | 8.5 | 1.20 |
| caption | -1 | 9 | 9 | 8.5 | 1.20 |
| body | 0 | 11 | 11 | 11 | 1.35 |
| h3 | +1 | 13 | 14 | 14.5 | 1.20 |
| h2 | +2 | 16 | 17 | 19.5 | 1.20 |
| h1 | +3 | 19 | 21.5 | 26 | 1.20 |

### Screen (base 11pt, same role set/leading as print — see §3 note)

Identical numbers to the print table above (same base, same steps, same leading convention); only
`Medium` differs (`screen` vs `print`) and therefore `scale_row_key`/`scale_key` differ. Flagged
explicitly, not hidden: this is a direct consequence of `report-screen`'s own base equalling the
print body base in the pre-existing data (§3), not a computation error.

### Projection (base 24pt, roles from `deck-projection`)

| Role | n | minor-third (1.2) | major-third (1.25) | perfect-fourth (1.333) | Leading Ratio |
|---|---|---|---|---|---|
| body-dense | -1 | 20 | 19 | 18 | 1.25 |
| body | 0 | 24 | 24 | 24 | 1.25 |
| h1 | +3 | 41.5 | 47 | 57 | 1.10 |

## 6. Floor / constraint check (constraints.csv)

`validate-type-floor` rows and how the 45 new rows sit against them:

- `proj-body-floor` (medium=projection, role=body, threshold 24, `artifact-class:canvas`): all
  three projection `body` rows = 24 -> **meets the floor exactly**.
- `proj-body-dense-floor` (medium=projection, role=body-dense, threshold 18,
  `artifact-class:canvas`): minor-third 20, major-third 19, perfect-fourth 18 -> **all clear the
  floor** (perfect-fourth meets it exactly).
- `proj-title-floor` (medium=projection, role=h1, threshold 36, `artifact-class:canvas`):
  minor-third 41.5, major-third 47, perfect-fourth 57 -> **all clear the floor** (by a growing
  margin as the ratio steepens, since h1 takes 3 steps).
- `screen-body-floor` (medium=screen, role=body, threshold 18, `artifact-class:canvas`): all three
  screen `body` rows = 11 -> **below the canvas floor**, exactly matching the pre-existing
  `report-screen-screen-body` (11) which is *not* scoped to canvas either. This constraint's
  `Applies To` is `artifact-class:canvas` only, so it does not fire for the intended (flow-style,
  report-like) use of `lib-*-screen`; it would fire if a brand kit tried to apply `lib-*-screen`
  to a canvas-class screen document (e.g. a web slide/infographic), which is outside this scale's
  sourced intent (`infographic-screen`, the existing canvas-class screen precedent, uses body=24,
  not 11). Flagged here rather than silently resolved.
- `legal-text-min-size` (medium=print, role=legal, threshold 8): not applicable — no `legal` role
  row is emitted by any of the 45 new rows.

## 7. Duplicate-scale_key check

Programmatic check (see validation run): no new `scale_key`'s full `(Medium, Role) -> (Size pt,
Leading Ratio)` map is an exact match for any existing `scale_key`'s map in
`data/base/type-scales.csv` — all 45 rows pass.

Nearest existing neighbours, checked by hand per the task's named example:
- `cv-major-third` (ratio 1.25, base 10.5, print, roles `label, body, h2, h1` only) vs.
  `lib-major-third-print` (ratio 1.25, base 11, print, roles `label, caption, body, h3, h2, h1`):
  **different base (10.5 vs 11) and different role coverage** (`cv-major-third` has no `caption`
  or `h3`; `lib-major-third-print` adds both). Per the task's own instruction ("if a combination
  would duplicate ... note it and still include the lib row only if it differs in role
  coverage"), `lib-major-third-print` is included because its role coverage strictly extends
  `cv-major-third`'s (label 9 vs 8.5, body 11 vs 10.5, h2 17 vs 13, h1 21.5 vs 20 — every
  overlapping role also differs numerically, since the base sizes differ).
- `cv-editorial-fourth` (ratio 1.333, base 10.5, print, roles `label, body, h2, h1`) vs.
  `lib-perfect-fourth-print` (ratio 1.333, base 11, print, roles `label, caption, body, h3, h2,
  h1`): same relationship — different base, wider role coverage, no numeric overlap by
  coincidence (label 8.5 vs 8, body 11 vs 10.5, h2 19.5 vs 14, h1 26 vs 25).
- No existing `scale_key` uses ratio 1.2 (minor third) at all, so `lib-minor-third-*` cannot
  duplicate anything by construction.
- No existing `scale_key` covers `projection` at any ratio other than `deck-projection`'s own
  (non-modular, hand-set) values, so `lib-*-projection` rows do not duplicate `deck-projection`
  numerically (deck-projection: body-dense 18/body 24/h1 36; lib rows recompute all three from
  ratio^n and only perfect-fourth's body-dense happens to coincide at 18 — a single-cell
  coincidence, not a full-row duplicate, and body/h1 differ in every case).

## 8. Output summary

- Output A: `research/library/type-scales/ratio-families.csv` — 45 rows (3 ratios x 3 mediums x
  role-set-per-medium: 6 print + 6 screen + 3 projection = 15 rows/ratio x 3 ratios).
- Output B: `research/provenance/type-scales-ratio-families.csv` — 45 rows, one authority row per
  `scale_row_key`, `Table=type-scales`, `Source Name` names the specific named ratio + its
  modularscale.com fraction/decimal, `Source URL=https://www.modularscale.com/`,
  `Retrieved=2026-09-23`, `Fetch=fetched`. `Evidence Class=authority` (not `ranked`): modularscale
  publishes a reference catalog of named ratios, not a popularity/usage metric — per research/81's
  own framing ("named ratio catalog (not popularity — a reference list)"), so `ranked` would
  misrepresent the source; `Ranking Metric`/`Rank Value` are left blank, matching the existing
  convention for non-ranked authority provenance rows (e.g.
  `research/provenance/palettes-authority-design-systems.csv`).
