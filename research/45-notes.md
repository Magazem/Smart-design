# Ruling K step 1 — page-flow constraint rows (research/45-notes.md)

5 rows appended to `research/16-t9-constraints-draft.csv`, all `Set Key: report-typography`,
`Applies To: artifact-class:flow`, `Severity: warn`. Covers the 4 required norms (one norm
split into 2 rows — see below). No `constraint_key` collides: checked against both drafts'
raw 49 rows (38 in `16-`, 11 in `21-`), not the 42-row post-load `data/base/constraints.csv`
count, since collisions can only actually occur at the draft level before `load-base.py`'s CV
collapse/drop logic runs.

## The table binding

Agreed with the brief's reasoning: T9/`constraints.csv` is the only table shaped as
"rule + check + how hard it fails." `doc-reasoning` is per-family style bias, wrong shape.
No better fit found.

## The 5 rows

| constraint_key | Check | Parameter | Threshold |
|---|---|---|---|
| `report-heading-keep-with-next` | `validate-keep-with-next` | `docx_property=keepNext;applies_to_block=heading;binds_to=body-paragraph` | `present` |
| `report-widow-orphan-control` | `validate-widow-orphan` | `docx_property=widowControl;min_lines_together=2` | `2` |
| `report-table-row-no-split` | `validate-table-row-integrity` | `docx_property=cantSplit;applies_to_block=table-row` | `present` |
| `report-table-header-repeat` | `validate-table-header-repeat` | `docx_property=tblHeader;applies_to_block=table-header-row` | `present` |
| `report-figure-caption-keep-together` | `validate-keep-with-next` | `docx_property=keepNext;applies_to_block=figure;binds_to=caption-block` | `present` |

Every `Parameter` names the concrete OOXML property (`keepNext`, `widowControl`, `cantSplit`,
`tblHeader`) so the Mechanism step (K3, which maps loaded constraints to these exact five
properties per its own brief) doesn't have to guess the binding.

**Why 4 norms became 5 rows.** "A short table never splits; a long table splits only with
its header row repeated" is two independently-checkable facts sharing one bullet, not one
fact with a condition. Per Rule 1 (flat fact per row, no branching in `Parameter`) and this
table's own precedent — `us-cv-length-under10y`/`-10y-plus` split one CV-length norm into two
rows rather than a conditional cell — I split it into `report-table-row-no-split` (rows never
break mid-row, relevant whether or not the table ends up spanning a page) and
`report-table-header-repeat` (header row repeats, only matters once a table does span pages).
Both are unconditional presence checks; neither needs a length threshold, since "does this
table span a page" is discovered at render time, not authored as a static number.

`validate-keep-with-next` is reused for both the heading and figure rows (same mechanism,
different anchor block), the same reuse pattern as `pro-min-dpi-raster`/`-line-art` sharing
`validate-dpi` and `proj-contrast-margin` reusing `validate-contrast-screen`.

## Element Scope — the answer, and why

Read `load-base.py:236-239` before authoring, as instructed:

```python
r["Element Scope"] = ""
if k == "report-measure-cpl":
    r["Element Scope"] = "body-paragraph"
```

This is not a general derivation — it is a single hardcoded key comparison. As written, all
five new rows load with `Element Scope = ""`. That's correct for 2 of the 5, and intentional
(not a workaround) for the other 3 — worked through below rather than left as an open flag,
per the brief's "argue it, don't just hand it up" spirit:

- **`report-widow-orphan-control` → `body-paragraph`.** Enum has an exact match.
- **`report-table-row-no-split` and `report-table-header-repeat` → `table-cell`.** Enum has
  an exact match (the table's own cells/rows).
- **`report-heading-keep-with-next` → `""` (empty), deliberately.** The enum
  (`body-paragraph`/`table-cell`/`caption-block`/`sidebar-column`/`header-footer`) has no
  "heading" value, and per `09-library-schema.md`'s own design note, empty is not "unscoped
  guess" — it's the documented allow-list default meaning "no container-type routing," which
  is correct here since a heading isn't any of the five listed containers. The actual
  narrowing happens in `Parameter` (`applies_to_block=heading`), exactly the precedent
  `photocopy-safe-color` already sets: it keeps `roles=label|legal` in `Parameter` with an
  empty `Element Scope`, because `Role` and `Element Scope` are explicitly orthogonal
  vocabularies. Same shape here, one vocabulary over: block-type isn't in the enum, so it
  lives in `Parameter`, not invented as a new enum value.
- **`report-figure-caption-keep-together` → `""` (empty), same reasoning, and the direction
  matters.** `keepNext` binds the block it's set ON to the one that follows — so the property
  goes on the **figure**, not the caption ("figure keeps with its caption" = figure binds
  forward to the caption that follows it, matching Chicago's caption-below-figure
  convention already cited in `03-document-design-knowledge.md:231`). `caption-block` is an
  Element Scope value, but assigning it here would mean "route this check to caption blocks,"
  which asserts the *caption* keeps with whatever follows *it* — the wrong pair. So the row
  stays scope-empty and `Parameter` says both which block carries the property
  (`applies_to_block=figure`) and what it must bind to (`binds_to=caption-block`, reusing the
  existing enum term for clarity even though it isn't the row's own Element Scope).

**For the Coverage step (K2):** the derivation needs the two real container matches
(`body-paragraph` for widow/orphan, `table-cell` for both table rows) added to whatever
data-driven mapping replaces the `if k ==` chain. The two `heading`/`figure` rows need no
Element Scope extension — they're correct at `""` already; don't add a special case for them.

## Sourcing — what's actually verifiable, not what sounds right

Grepped `data/`, `scripts/`, `SKILL.md`, `references/`, and every `research/*.md` rationale
file for `Bringhurst`, `Butterick`, `DIN 5008`, `Tufte`, `Chicago`. Findings, so the next
author doesn't have to re-grep:

- **Bringhurst** is cited repeatedly, but only for measure (45–75 CPL) and leading
  (120–145%) — both computed typographic proportions, not pagination/page-break rules. I
  could not find a passage in this library's own citations that extends Bringhurst's
  authority to widow/orphan control, keep-with-next, or table-header repetition, and I'm not
  willing to attach his name to a claim I can't point at. Per the brief's own standard — "an
  invented threshold presented as a norm is worse than no row" — that applies to invented
  citations too.
- **Butterick** and **DIN 5008** are cited **nowhere** in this library. DIN 5008 specifically
  governs German business-letter layout (address block, margins, date format), not pagination
  — it doesn't cover any of these four norms, so I didn't reach for it just because the brief
  named it as a candidate.
- **Tufte** and **Chicago Manual of Style** are cited for table rules and caption placement
  respectively, but not for page-break behavior.

So all 5 rows are tagged **CONVENTION (general document-production/word-processing
convention — not in report 03, not tied to a specific named authority I can verify)**, using
the same honesty register this file already has precedent for
(`legal-text-no-sustained-uppercase`: "CONVENTION (general typographic knowledge, not in
report 03)"). These four norms are near-universal *default behavior* in Word, LibreOffice,
and InDesign (all four properties — keepNext, keepLines/widowControl, cantSplit, tblHeader —
exist as first-class paragraph/table properties in OOXML itself, which is why the Mechanism
brief can name them directly), not a single author's rule of thumb.

**The one number: `min_lines_together=2`.** Not sourced to a named authority — it's the
long-standing word-processor default (Word's "Widow/Orphan control," on by default since
early versions) for how many lines must stay together at a page boundary. Flagging plainly
that this is convention-by-ubiquity, not a citation, consistent with how `legal-text-min-size`
flagged its own unsourced 8pt floor.

## Families excluded, and why

`Applies To: artifact-class:flow` — matches every sibling row already under `Set Key:
report-typography` (`report-measure-cpl`, `report-leading-ratio`, etc.), and is the correct
cut: per `data/base/doctypes.csv`, `flow` covers CVs, letters, memos, forms, brochures,
reports, whitepapers, proposals, invoices — anything that paginates. Excluded:
`artifact-class:canvas` (`poster`, `slide-deck-projection`, `slide-deck-document`,
`infographic`) — a poster is one physical sheet and a slide is a single canvas; neither
paginates, so "keeps with next page" is meaningless for them, exactly as the brief said. Left
`slide-deck-handout` (`hybrid`) excluded too, matching every other `report-typography` row —
no new exception invented for it.

## Verification (all 4 items from the brief)

1. **Parses, header matches.** `csv.DictReader` on the file after the edit: fieldnames ==
   `['constraint_key','Set Key','Applies To','Check','Parameter','Threshold','Severity']`
   (the seven-column draft header, exact). 43 total rows, no parse error.
2. **No collisions.** Checked the 5 new keys against the union of both drafts' raw keys
   (49 total, 38+11, zero cross-file dupes already) — no match.
3. **Severity enum.** All 5 new rows are `warn`; asserted `Severity in ('fail','warn')` across
   all 43 rows in the file, passes.
4. **Element Scope derivation.** Answered above, quoting `load-base.py:236-239` — 2 rows need
   a real scope added to the derivation (`body-paragraph`, `table-cell`×2), 2 need none (stay
   `""` by design).
