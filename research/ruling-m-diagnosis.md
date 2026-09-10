# RULING M — diagnosis, per section, written BEFORE any code changed

Doctype probed: `report-long-toc` (and `cv-generic` as the second case).
Method: `resolve.py --doctype <d> --json`, then inspect which tables were attached and
which COLUMNS each surfaced, then `ddi.py handoff --format docx`.

## Finding 0 — every table ddi.py reads WAS attached

The resolve path is not the problem anywhere. All six HANDOFF_VOCAB tables came back
with rows for both doctypes:

    page-formats 1   typefaces 1   type-scales 1   palettes 1   render-targets 4   constraints 13

So the brief's second candidate ("the resolve path never attaches that table at all")
is ruled out for all six sections. What came back was rows with almost no columns:
`resolve._display_columns()` defaults to *searchable columns + this table's own FK
source columns*, and five of the six tables declared no `display_columns` override.

## Per section

| section | cause | verdict |
|---|---|---|
| page | no `display_columns` on `page-formats` | brief's candidate 1 |
| fonts | no `display_columns` on `typefaces` (+ a display bug, see Finding 2) | candidate 1 |
| font sizes | no `display_columns` on `type-scales` | candidate 1 |
| TOC heading levels | DATA GAP, not display — see Finding 3 | NOT one of the three |
| characterSpacing | reads a column that exists in NO table — see Finding 4 | candidate 3 |
| palette | no `display_columns` on `palettes` | candidate 1 |

Evidence for candidate 1, per table (columns actually surfaced before the fix):

    page-formats  key, Display Name, Keywords                 <- no Trim/Margin mm at all
    typefaces     key, Display Name, Keywords, Best For, Scale Key   <- no Heading/Body Family
    type-scales   key                                          <- no Role, no Size pt
    palettes      key, Display Name, Keywords                  <- no Primary/Secondary/...

That is why `font sizes` printed `: pt  ->  None half-points`: the row was there, `Role`
and `Size pt` were not, so `_pt_to_half_points("")` returned None.

## Finding 1 — a SEVENTH broken line the brief's reproduction did not show

`constraints to preflight (Set Keys): ` rendered with nothing after the colon.
`constraints` was the one table that DID have `display_columns` — the hand edit — and it
listed only `Element Scope` and `Parameter`. `ddi.py` also reads `Set Key`
(`HANDOFF_VOCAB["constraints_id_column"]`). The hand edit fixed page flow and broke this
line in the same stroke.

## Finding 2 — `fonts:` printed BLANK, not `(not present in this resolution)`

`page` and `palette` both carry a `shown` flag and fall back to NOT_PRESENT when the row
surfaces none of their columns. The `fonts` block, in BOTH the docx and pptx builders, had
no such flag: it printed its header and then nothing. A blank section reads as "no fonts
needed"; NOT_PRESENT reads as "not resolved". Same defect class as the blocker itself.

## Finding 3 — TOC heading levels stays empty AFTER the fix. Out of scope, needs its own brief.

`data/base/type-scales.csv` holds 15 rows. `report-print` has exactly ONE (`body`) and
`cv-print` has exactly ONE (`body`). `_heading_roles()` matches `h[0-9]+` against the
resolved `Role` values, finds none, and the section stays empty — on a doctype named for
its table of contents.

This is an authoring gap in `data/base/`, not a display or resolve bug. The fuller draft
already exists at `research/30-t6-type-scales-draft.csv` (22 rows, all 8 scale keys). The
standing rule is that only `research/load-base.py` writes `data/base/`, so this task did
not touch it. Recommend a separate brief.

## Finding 4 — characterSpacing is CORRECT as it stands

`ddi.py` reads `Letter Spacing pt`. That column name appears in NO table in the manifest
and in no CSV. `ddi.py`'s own module comment already says so and says it should degrade.
NOT_PRESENT is the honest answer here, not a bug, and no `display_columns` entry can fix
it. Adding the column would be a schema change, which this task was not asked to make.
