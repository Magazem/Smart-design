# rationale/doc-styles.md

Hand-authored (T3 has no rationale generator). Four rows added at A4 --
`cv-harvard`, `cv-dach-tabular`, `cv-europass`, `cv-editorial` -- one per direction in
`research/69-cv-design-directions.md` (structure/grid) and `research/70-cv-type-and-colour.md`
(spacing). Rule/Corner/Table/Emphasis/Field cells are the structural facts 69 states
directly; Checklist items restate 69's own "slop avoided" bullets as imperative guidance,
the same transform every prior T3 row already applies to its source direction.

### `cv-harvard`

`Table Rules=none`, `Table Fills=none`, `Field Style=none`: 69 Direction 1 has no table or
field grid, only prose sections separated by whitespace ("generous white space between
sections rather than rules/borders" -- Butterick, fetched). `Rule Brand pt=1`: the one
accent-coloured rule under the name/header (69: "used only for the name/header rule").
`Emphasis Mechanism=weight`: 69/70 hierarchy is "type size and whitespace only," no colour
fills. Checklist restates 69's Direction 1 "Slop avoided" bullets (default-blue-everywhere,
mismatched fonts, bloated text, frames around everything) as actions.

### `cv-dach-tabular`

`Table Rules=row-hairlines` (A8, was `hairline` at A4): the two-column label/content table
(69: "margins 20mm, two-column table... photo 4.5x6cm top-right") uses row separation, not a
bordered grid -- but plain `hairline` carried no rule against boxing every cell, and
research/72's blind panel (all three judges, verbatim) read the rendered table as "fully
boxed"/a "gridded table" despite the Checklist already saying "row padding rather than cell
borders": the enum value itself was silent on vertical rules and cell boxes, so a renderer
had nothing to contradict a default all-borders table style. `row-hairlines` states 69's
Whitespace rule directly -- horizontal separators between rows only, no vertical rules, no
cell boxes -- closing the gap between the Checklist text and the machine-readable column a
renderer actually reads. `Table Fills=none` and the Checklist's explicit "no vertical rules,
no cell borders, no boxed grid" line both restate 69's avoidance of the
Odoo-clone/frames-around-everything pattern that same section names for invoice-style grids.
Label column width (~35mm) is now stated directly in the Checklist rather than only in this
rationale, per 69's "two-column table (label column ~35mm, content column remainder)". Row
padding is now stated in pt (13pt) rather than left qualitative, per 70's DACH Scale (body
10pt/13pt) and Spacing ("row padding = 1 leading unit rather than cell borders" -- one
leading unit = the body leading, 13pt). `Rule Brand pt=0`: no accent colour exists in this
direction (70: "No accent colour; formality signalled by structure").

A second Checklist line and handoff instruction were added at A8 by Manager ruling, on top
of the judges' boxed-cell defect: research/72's judges 2 and 3 also named a "heading
collision" -- a section heading crowding the table with no space after it -- a design defect
independent of the table-rules fix. "Space after every table and before every section
heading: one body leading (13pt); headings never touch a table edge" reuses the same 13pt
body-leading value from 70's DACH Scale (not a new, separately-sourced number) applied to the
gap after the table rather than the gap between rows -- a natural reuse of the same rhythm,
not an independent citation.

### `cv-europass`

`Table Rules=hairline`: the language-proficiency self-assessment grid (69: "explicit
language-proficiency table... a real Europass structural element, not a slop pattern, since
it maps to a recognized EU framework"). `Rule Brand pt=1`: the accent underscore under
section labels (70: "accent... for section-label underscores only, never a full-block
fill"), restated verbatim as a Checklist item.

### `cv-editorial`

`Rule Brand pt=1.5`: the one Carbon Blue 60 rule at headline size (70: "restricted to
headline-size text/rules... not small print"), matching the palette rationale's placement of
this same accent in `Fill-Only Roles` rather than `Text-Safe Roles`. `Table Rules=none`,
`Field Style=none`: this direction (69/70's new Direction 4) has no table/field structure,
being a one-page single-column CV. Checklist restates 70's own scope note ("no gradients, no
icon rows, no stock-photo frames") and 69's general slop-avoidance vocabulary reused across
all four directions.
