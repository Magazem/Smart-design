# T11 figures draft — sources, gaps, and validation

11 rows, 19 columns, validated with `csv.reader` (header width matches every row, no
mismatches). Row count matches the task's requested list exactly: comparison-few-categories,
comparison-many, part-to-whole, change-over-time-few-series, change-over-time-many,
distribution, correlation, ranking, geographic, flow-process, tabular-lookup.

## Licence posture

Every row was authored from the primary sources below, independently — none of upstream's
`charts.csv` row content was read while drafting these rows (its 25 rows are chart-type ×
web-library recommendations, e.g. "D3.js" / "Recharts," which don't map onto anything this
file needs anyway; see `09-library-schema.md`'s own assessment of that file). Column
*shape* mirrors T11 as already designed by the Coverage Analyst — that mirroring is
explicitly permitted per the task's licence rule, since the schema (not upstream's data)
already made that design call.

## Sources actually used

- **Cleveland & McGill (1984), perceptual-task ranking** — position > length > angle/slope
  > area > volume > colour/shading, roughly. This is the backbone of every
  `Accessibility Grade` value and most `Anti-Patterns` reasoning (pie charts penalised for
  using angle/area, the weakest tasks; bar charts favoured for using length, a strong one;
  choropleth maps flagged low-medium for the same area/colour-value dependency).
- **Tufte** — data-ink ratio and chartjunk (3D bars/pies/flowchart boxes flagged
  throughout as adding visual weight with no information), small multiples (the
  `change-over-time-many` row's entire recommended form), and the "lie factor" /
  data-integrity concern (unlabeled histogram bin width, trend lines shown without
  underlying scatter points, inconsistent y-axis scales across small multiples).
- **Few** — table-vs-chart judgment (`tabular-lookup` row is built directly from this:
  a chart is not always the answer, and forcing one to "look designed" is named as the
  common failure), and the dual-y-axis critique (`change-over-time-few-series`'s
  anti-pattern).
- **report 03 §B** — the 5-7 series spaghetti-chart threshold, cited directly and reused
  as the dividing line between `change-over-time-few-series` (below it) and
  `change-over-time-many` (the small-multiples fix for being at/above it). Also the
  chart-vs-table decision rule itself, which `tabular-lookup`'s `When to Use`/`When NOT to
  Use` cells quote almost verbatim from report 03's own wording.
- **report 03 §D** — table design rules (tabular figures, alignment, sparse rules) reused
  directly in `tabular-lookup`'s `Accessibility Notes`, and the figure/table caption
  convention (`Caption Required`, and the below-vs-above distinction noted in that row).
- **report 03 §E** — "direct labelling is the print default, no hover exists on paper" is
  report 03's own framing (originally about accessible print contrast, but the same
  no-hover logic applies directly to chart labels); every row's `Label Strategy` defaults
  to `direct` unless a specific reason forces a legend (only `geographic`, for a continuous
  colour ramp that can't be direct-labeled per pixel).

## The `dataviz` skill — could not locate its files, did not cite it

Followed the task's instruction and ran `find /c/Users/ysuliman/.claude -maxdepth 6 -type d
-iname "dataviz*"` — no result. Broadened the search significantly beyond what was asked
before giving up: recursive searches (to depth 8-10) under the full user profile, the
`.claude/plugins` marketplaces and cache directories, the project directory itself, and
every AionUi skills-related directory I could find (`aionui/skills/users/*`,
`config/skills`, `session-skills/*`) — the only locally-installed skill I found in any of
those was `slop-review`. The `dataviz` skill is listed as available via the `Skill` tool
in this session (its description mentions a `references/palette.md` with a validated
palette and a form heuristic), so it clearly exists *somewhere* in this environment's
skill-resolution path, but not as a plain discoverable directory under any path I checked.
I did not invoke it live via the `Skill` tool, since that tool is designed to load
instructions for active use (e.g., mid-way through building a chart), not as a
read-only reference lookup, and doing so risked pulling this task off-track for an
optional, explicitly-secondary source. **Net effect: this file cites no `dataviz` content
anywhere** — every source above is a primary academic/professional one, which the task
listed as the actually-required sourcing regardless. Flagging the missing-on-disk finding
in case it's a real environment issue worth someone else's attention, separate from this
task's content.

## `Min Physical Size mm` — left blank in every row, on purpose

The task explicitly warned this column was flagged as an invented threshold and told me to
either source it or leave it blank rather than fill it with a plausible number. I looked
for a real source and didn't find one, for a structural reason rather than a research gap:
**a single "minimum figure size in mm" can't be honestly derived without first assuming a
specific label count and label length for that figure** — a 3-category bar chart and a
20-category sorted bar chart need completely different minimum widths to keep their axis
labels legible at any given type size, even though both are "the same chart type." Any one
number I picked would be exactly the invented-threshold problem this column was already
flagged for.

What I can source, and did note per-row instead: the *actual* constraint is a **computed**
one — resolved axis-label point size (from T6, subject to the same print-legibility
questions research/12/16 already raised for body type) × the number and length of labels
that specific figure needs × available page width (T7) → a derived minimum size for *that*
figure, not a fixed constant for the chart type. This is the same shape of finding as
`report-measure-cpl` in `research/16-t9-constraints-draft.csv`: report 03 gives a formula
where the schema wanted a lookup number, and the honest fix is to make the validator
compute it rather than authoring a wrong constant. Recommend `Min Physical Size mm` either
be cut from T11 entirely (parallel to my `research/12` recommendation to cut the
`photocopy` Medium from T6 rather than invent a number for it) or reframed as a computed
check joining T6's axis-label floor × T7's page width — not authored per-row here either
way, since I don't own T6/T7/T9's validator design.

## Two column additions not in T11's currently-documented shape

`research/09-library-schema.md`'s T11 section (read in full before drafting) lists 9 kept
upstream columns, ~2 reworked, and 6 added (`Label Strategy`, `Static Fallback`,
`Print Series Max`, `Min Physical Size mm`, `Greyscale Safe`, `Print Palette Roles`) — it
does **not** define `Caption Required` or `Anti-Patterns` anywhere. The task explicitly
asked me to fill both, so I added them as real columns in the CSV rather than only noting
the gap, but flagging clearly here since they weren't part of the schema as documented:

- **`Caption Required`** — straightforward addition, sourced directly to report 03 §D's
  captioning convention (every figure/table gets a numbered caption). Low-risk addition;
  every row in this file is `yes` except `tabular-lookup`'s note about above-vs-below
  caption position, which is really a `Caption Position` question T10 already owns
  (`fig=below;table=above`) — worth the Coverage Analyst checking whether `Caption
  Required` on T11 duplicates something T10's join already guarantees, or is genuinely
  needed here because T10's structure rows aren't necessarily joined per-figure.
- **`Anti-Patterns`** — bigger question worth flagging plainly: **T2 `doc-reasoning.csv`
  already has an `Anti-Pattern Tokens` column** (`09-library-schema.md:362`,
  "gradient;emoji;navy;lime-text" etc. — a grep-list the output validator runs). This
  file's new T11 `Anti-Patterns` column is the same *kind* of thing (a checkable
  blocklist with reasons) applied specifically to chart-form choices (3D charts, dual
  y-axes, rainbow ramps, unsorted rank bars). I did not fold these into T2's existing
  column, because T2's tokens read as brand/style-level prohibitions resolved once per
  doctype, while T11's anti-patterns are chart-form-specific and only make sense scoped to
  *which row* is in play (a dual-y-axis warning only matters when a line chart was
  selected). Whether that distinction is worth two columns in two tables, or whether T11's
  anti-patterns should just be additional T2 tokens gated by the resolved `Best Chart
  Type`, is a real design call I'm not making unilaterally — same category of
  T9-vs-T5-validator-ownership question flagged in `research/16-t9-constraints-notes.md`.

## Columns I could not source and left as `n/a` rather than guessing

Several cells read `n/a` rather than a number or `blank` — worth distinguishing from the
`Min Physical Size mm` blanks above, since `n/a` here means "this metric doesn't apply to
this chart form," not "I couldn't find a source":
- `Print Series Max` is `n/a` for `change-over-time-many` (bounded by page layout, not a
  perceptual series-count limit — small multiples don't have the crowding problem a single
  overlaid chart does) and for `flow-process` (the real ceiling is stage/node count,
  already captured in `Data Volume Threshold`, not a "series" in the bar/line sense) and
  for `tabular-lookup` (no chart, no series).
- `Static Fallback` is `n/a` for every chart form that's already static-native (histogram,
  scatter, choropleth, flowchart, small multiples) — the column exists to answer "what
  replaces the interactive/hover behaviour," and forms with no interactive behaviour to
  begin with have nothing to fall back from.

None of these are guesses standing in for missing research — each is a considered
"this dimension doesn't apply to this row" call, stated rather than left silently blank.
