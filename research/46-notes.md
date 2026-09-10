# Ruling N step 1 — missing type-scale heading rows (research/30-t6-type-scales-draft.csv)

## Diagnosis, unchanged
`report-print` and `cv-print` each had one row (`body`, 11/1.35). `_heading_roles()`
(`ruling-m-diagnosis.md` Finding 3) matches `h[0-9]+` against resolved `Role` values —
with none present, the docx/pptx TOC heading-levels section stays empty on
`report-long-toc`. This is the authoring gap, not a plumbing bug.

## Sourcing check, done before writing anything
`12-typescale-and-fstype.md` already answered this: report 03 gives **no** print
point-size floor for any role, headings included — only ratios (leading 1.20-1.45x body,
Bringhurst's 45-75 CPL for measure). So neither `report-print` nor `cv-print` headings
can be tagged sourced-from-report-03. `print-office-generic`'s own h1/h2/h3
(12/1.20, 16/1.20, 24/1.20) are themselves brand/house-authored constants validated by
the leading-ratio formula, not a report-03 floor (`30-notes.md`, `12-typescale-and-fstype.md`
Q1 table) — they are the "already carries a set" the brief points at, not a sourced set
in their own right. That leaves route 2 of the brief's sourcing rule: derive.

## Rows added (5)
```
report-print-print-h3   12pt / 1.20   DERIVED — print-office-generic h3, same body size (11pt)
report-print-print-h2   16pt / 1.20   DERIVED — print-office-generic h2, same body size
report-print-print-h1   24pt / 1.20   DERIVED — print-office-generic h1, same body size
cv-print-print-h2       16pt / 1.20   DERIVED — print-office-generic h2, same body size
cv-print-print-h1       24pt / 1.20   DERIVED — print-office-generic h1, same body size
```
No CONVENTION tags needed here — route 2 (derivation) applied cleanly since
`print-office-generic` already has a full, same-body-size set to copy the ratio from.
`rationale/type-scales.md` must record all five as derived-from-`print-office-generic`,
not as independently sourced or independently house-decided numbers.

## report-print: h1/h2/h3 only, no caption or label
`_heading_roles()` only needs `h[0-9]+` roles to stop printing NOT_PRESENT — that is the
entire defect. Nothing in report 03, in `30-notes.md`, or in the figures draft
(`22-t11-figures-draft.csv`) gives a report a caption or label role distinct from what a
generic print document already has. Adding them here would be exactly the padding the
brief warns against, so three rows, not five.

## cv-print: h1 and h2 only, no h3 — judged, not defaulted
A CV's actual hierarchy is name (h1) and section headers — Experience, Education, Skills
(h2). Individual entries within a section (job title, dates, school) are conventionally
carried by weight/style contrast on the body role, not a third distinct point size — CVs
are printed to a strict 1-2 page budget and a third heading tier works against that
constraint rather than for it. So two rows, not three, and the shallower hierarchy is a
judgment about what a CV needs, not a shortcut taken to save a row.

## Should a report's heading scale differ from a generic office document's? No.
Report 03 gives no reason for a printed report to size headings differently from any
other print document — the only sourced facts are the leading-ratio and CPL formulas,
which apply uniformly across print media, not a report-specific number. `30-notes.md`
already flagged `report-print` as one of five scale_keys that exist only because
`typefaces.csv` names them, with a standing recommendation to collapse them into
`print-office-generic`. Deriving report-print's headings from print-office-generic at
identical values is not a workaround for missing data — it is the correct answer, and
matches the same five-key duplication finding already on record. If a report brand or
report 03 revision ever gives reports their own sourced or house-decided heading sizes,
these three rows should be revisited then, not before.

## Verification
- `csv.DictReader` over the file: 27 rows, header matches the six-column pattern exactly.
- No `scale_row_key` collision with the prior 22 rows (checked programmatically).
- `Medium` values used (`print`) already existed in the draft; no new medium introduced.
- Leading ratios: all five new rows sit at 1.20, tighter than body's 1.35 — same relation
  every existing heading row in the file already has to its own body row.
