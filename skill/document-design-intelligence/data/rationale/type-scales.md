# rationale/type-scales.md

Hand-authored (T6 has no rationale generator). Two new `scale_key`s added at A4,
`cv-major-third` and `cv-editorial-fourth`, four rows each -- `label`, `body`, `h2`, `h1` --
matching the existing row shape (e.g. `cv-print`'s three rows, `report-print`'s four).
`research/70-cv-type-and-colour.md`'s "small" role (its own prose term) is mapped onto the
schema's `Role` enum value `label`, since the enum has no `small`/`caption`-for-CV token
closer in size to what 70 describes (a role below `body`).

### Why two scale keys, not four

`research/70` authors slightly different base sizes and leading per direction (Harvard base
10.5pt, DACH base 10pt, Europass base 10.5pt +1pt leading, Editorial base 10.5pt). The A4
brief (Manager decision) collapses this to exactly two scale keys: `cv-major-third` (ratio
1.25, Major Third, shared by Directions 1/2/3 -- Harvard, DACH, Europass) and
`cv-editorial-fourth` (ratio 1.333, Perfect Fourth, Direction 4 only). This is the same
economy-vs-context-nuance trade the schema's own `deck-generic` ruling already accepts by
design (`data/rationale`/doc-reasoning history, `deck-generic` entry): one shared design
language costs some per-direction nuance and is chosen deliberately rather than authoring a
fourth near-duplicate scale for a few tenths of a point of difference research/70 itself
frames as variation within one method, not a different method. `cv-major-third`'s four rows
below use Direction 1 (Harvard)'s own numbers as the representative values, since Harvard is
the most heavily sourced of the three directions sharing the key.

### `cv-major-third` (ratio 1.25, base 10.5pt) -- research/70 Direction 1 numbers

| Role | Size pt | Leading pt | Leading Ratio | research/70 citation |
|---|---|---|---|---|
| `label` | 8.5 | 11 | 1.29 (11/8.5) | "small 8.5pt/11pt" |
| `body` | 10.5 | 13 | 1.24 (13/10.5) | "body 10.5pt/13pt" |
| `h2` | 13 | 15 | 1.15 (15/13) | "H2 13pt/15pt" |
| `h1` | 20 | 22 | 1.10 (22/20) | "H1 (name, 3 steps) 20pt/22pt" |

Modular-scale method: [modularscale.com](https://www.modularscale.com/) (fetched, research/70),
Major Third = 1.25 as a standard named ratio; H1 takes three ratio steps per
modularscale.com's own worked practice. Sits inside Jobscan's 10-12pt body / 14-16pt heading
ATS range for `body`/`h2`; H1 exceeds 16pt by design, since a name conventionally sits above
the section-heading band and ATS text-extraction is unaffected by point size (research/70's
own caveat, restated from research/69).

### `cv-editorial-fourth` (ratio 1.333, base 10.5pt) -- research/70 Direction 4 numbers

| Role | Size pt | Leading pt | Leading Ratio | research/70 citation |
|---|---|---|---|---|
| `label` | 8 | 10.5 | 1.31 (10.5/8) | "small 8pt/10.5pt" |
| `body` | 10.5 | 13.5 | 1.29 (13.5/10.5) | "body 10.5pt/13.5pt" |
| `h2` | 14 | 16.5 | 1.18 (16.5/14) | "H2 14pt/16.5pt (sits exactly in Jobscan's heading band)" |
| `h1` | 25 | 28 | 1.12 (28/25) | "H1 (name, 3 steps) 24.9pt->25pt/28pt" |

Perfect Fourth = 1.333, also from modularscale.com's ratio table, chosen for Direction 4
because it carries no ATS point-size ceiling (research/70: "a more expressive jump").
