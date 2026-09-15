# rationale/font-substitutes.md

Hand-authored (T14 has no rationale generator; `research/load-base.py` only derives
`substitute_key` and `Weights Covered`). Four rows added at A4, one per new CV typeface row
authored in `research/19-t5-typefaces-draft.csv` (`source-serif-sans`, `pt-serif-sans`,
`ibm-plex-sans`, `fraunces-work-sans`), reusing this table's existing shape
(`proprietary_family -> Substitute Family`) to record each new family's own safe-stack
fallback -- the same fallback already declared on the T5 row's `Safe Stack Fallback` column,
restated here at font-family grain because T14 is where a per-family substitute lookup
belongs (the constraint `font-substitute-available` reads this table, not T5, per
`research/load-base.py`'s T9 block).

Interpretation note: every prior T14 row maps a **proprietary** family (Arial, Calibri...)
to a **metric-identical open** substitute (Liberation Sans, Carlito...), with
`Metric Identical=yes` and a real OFL/Apache licence on the substitute. The four rows below
run the other direction -- an **open** family (Source Serif 4, PT Serif, IBM Plex Sans,
Fraunces) falling back to a **proprietary, OS-bundled** family (Georgia, Times New Roman,
Arial) when the open family cannot be embedded. That is not a metric clone relationship, so
`Metric Identical=no` on all four, and `Licence=none` is used deliberately -- the manifest's
`Licence` enum (`OFL-1.1`/`Apache-2.0`/`none`) has no "proprietary" value, and Georgia/Times
New Roman/Arial are proprietary Microsoft-class fonts, not OFL or Apache-licensed. Tagged
**CONVENTION**: no schema revision defines a licence token for this reversed direction; the
same `none` value the table already uses for "no known substitute" rows (Candara, Corbel...)
is reused here for "known substitute, but it isn't an open licence."

| `proprietary_family` (= new family) | `Substitute Family` (= its fallback) | matches T5 row |
|---|---|---|
| Source Serif 4 | Georgia | `source-serif-sans` |
| PT Serif | Times New Roman | `pt-serif-sans` |
| IBM Plex Sans | Arial | `ibm-plex-sans` |
| Fraunces | Georgia | `fraunces-work-sans` |

Sources: research/70 Directions 1, 2, 3 and 4 (Georgia/Arial, Times New Roman/Arial,
Arial, Georgia/Arial fallbacks respectively), citing Butterick's
[system-fonts page](https://practicaltypography.com/system-fonts.html) for the OS-bundled
tolerable-fallback lists.

Body-family rows (Source Sans 3, PT Sans, Work Sans) were deliberately NOT given their own
T14 row: each new T5 typeface row is a heading+body pair sharing one
`Safe Stack Fallback` cell (the same one-fallback-per-row shape every prior T5 row with a
Family Count > 1 already uses, e.g. `ofl-source-sans-serif`'s single `Arial` fallback for its
Source Sans 3 + Source Serif 4 pair) -- one T14 row per new T5 row keeps that 1:1
correspondence rather than inventing a second, unneeded fallback fact per pair.
