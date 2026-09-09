# T11 `Caption Required` qualifications -- RESTORED at Revision 3

`Caption Required` is a yes/no enum; research/22 authored prose in it, because it was
answering a second question the column did not ask. Revision 3 added
`Caption Must State`, and this loader now splits the prose across both columns, so
these three facts are **in the library**, not only here. This file stays as
provenance: it records the authored cell verbatim beside what the split produced.

| `chart_key` | authored `Caption Required` | loaded `Caption Must State` |
|---|---|---|
| `distribution` | yes -- must state bin width for histograms specifically | must state bin width for histograms specifically |
| `correlation` | yes -- should state sample size (n) and, where relevant, the correlation coefficient | should state sample size (n) and, where relevant, the correlation coefficient |
| `tabular-lookup` | yes -- and captioned ABOVE the table, not below, per report 03 Section D and T10's Caption Position convention -- the one row in this file where that differs from figures | and captioned ABOVE the table, not below, per report 03 Section D and T10's Caption Position convention |

`tabular-lookup`'s value is a *position*, not a statement. T10's `Caption Position`
stays authoritative for that (schema T11 design note, Revision 3); the cell records
the fact where the row that carries it can be read, and does not drive the check.

## `Accessibility Grade` -- the same split, one column over

`Accessibility Grade` became an enum at the Revision 4 erratum follow-on. The T11
author wrote prose into it on the same row and for the same reason, so the loader
applies the same rule: the enum token stays, the sentence moves to the prose column
beside it (`Accessibility Notes`), joined with `; ` -- the sentence separator those
columns already use. Nothing is lost, and the draft is not hand-edited.

| `chart_key` | authored `Accessibility Grade` | loaded | moved to `Accessibility Notes` |
|---|---|---|---|
| `tabular-lookup` | high by construction -- a table is the ground-truth data, no perceptual-encoding step to fail at | `high` | a table is the ground-truth data, no perceptual-encoding step to fail at |
