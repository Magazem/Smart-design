# A5 — CV evidence gate: OLD default vs NEW directions (blind Opus panel)

Pre-registered 2026-09-14 in `research/71-cv-gate-content.md`. Content C1 (cv-uk, early),
C2 (cv-dach, experienced), C3 (cv-generic, experienced), rendered literally from the
`ddi.py handoff` docx block via python-docx, converted to PDF via LibreOffice headless,
page 1 to PNG at 150dpi via PyMuPDF. OLD = current `data/` with the three doctypes'
Reasoning Key patched back to `cv-ats-strict` in a temp copy (repo untouched). NEW = repo
`data/` as committed after A4b. Files: `research/evidence/cv/{old,new}/<doctype>.{docx,pdf,png,preflight.json}`,
blind copies for judges at `research/evidence/cv/blind/<doctype>-{X,Y}.png`, mapping in
`research/evidence/cv/manifest.json` (X/Y assigned independently per doctype, not fixed).

Judges never saw the manifest, condition names, or each other's output. 3 Opus judges,
sequential, doctype presentation order randomised per judge.

## Manifest (unblinded here for the record)

| Doctype | X | Y |
|---|---|---|
| cv-uk | old | new |
| cv-dach | new | old |
| cv-generic | old | new |

## Preference results (unblinded)

| Doctype | Judge 1 | Judge 2 | Judge 3 | NEW preferred by |
|---|---|---|---|---|
| cv-uk | Y (NEW) | Y (NEW) | Y (NEW) | 3/3 |
| cv-generic | Y (NEW) | Y (NEW) | Y (NEW) | 3/3 |
| cv-dach | Y (OLD) | Y (OLD) | Y (OLD) | 0/3 |

NEW preferred by ≥2 of 3 judges on 2 of 3 doctypes (cv-uk, cv-generic) — unanimously, in
fact. OLD preferred by all 3 judges on cv-dach.

## Regional correctness (unblinded)

| Doctype | X (condition) | Y (condition) | J1 | J2 | J3 |
|---|---|---|---|---|---|
| cv-uk | old | new | PASS/PASS | — | — |
| cv-dach | new | old | FAIL/FAIL | FAIL/FAIL | FAIL/FAIL |
| cv-generic | old | new | PASS/PASS | — | — |

cv-uk and cv-generic: PASS on both conditions, all 3 judges (order/personal-data fields
correct per `cv-regions.csv`). cv-dach: **FAIL on both X and Y, all 3 judges** — section
order and personal-data fields (DOB, nationality, marital status) correctly matched
`dach-experienced`, but section headings (Contact/Experience/Education/Skills) are English
over German body content, against `cv-regions.csv`'s dach Language Expectation. This fires
identically on OLD and NEW: root cause is `structures.csv`'s "Heading Language" hard-coded
to `en` for every structure (RESUME.md v0.4 backlog item 4 / research/64 D-E), not a
design-direction difference. See A7 (dispatched to fix this) and judges' verbatim reasons
below.

## Preflight fail-severity facts on NEW (all three)

Checked against `slop-mechanical` constraint set (A3): font families >3 fail; emoji >0
fail (all families); cell-border ratio >0.5 fail only for invoice/quote/form (warn
elsewhere); bordered-block ratio >0.5 warn; accent colour outside resolved palette warn;
words-per-slide >36 warn (deck only, n/a here).

| Doctype | font families | emoji | cell-border ratio | bordered-block ratio | accent colours | Fail-severity fires? |
|---|---|---|---|---|---|---|
| cv-uk | 2 (Arial, Georgia) | 0 | n/a (no table) | 0.0 | 1B1B1B, **4F81BD** | No |
| cv-dach | 2 (Arial, Times New Roman) | 0 | **1.0** (12/12 bordered) | 0.0 | 0B0C0C, **4F81BD** | No — cell-border-ratio fail threshold applies only to invoice/quote/form; CV is warn-only, so this is a warn, not a fail |
| cv-generic | 2 (Arial, Georgia) | 0 | n/a (no table) | 0.0 | 1B1B1B, **4F81BD** | No |

**Zero fail-severity facts fire on NEW for any of the three doctypes.** Two warn-severity
notes, both pre-existing and not caused by A4/A4b: (1) `4F81BD` — python-docx's default
Word theme `accent1`, present in the generated docx's theme XML regardless of visible
content, on both OLD and NEW, every doctype; not an A4 regression. (2) cv-dach's
table-cell-border ratio is 1.0 (every contact-block cell individually boxed) — this is the
"Odoo-clone"/"frames around everything" pattern the judges independently flagged; warn, not
fail, for CV family, but a real design defect judges scored down on hierarchy/pairing.

## Judges' verbatim reasons — cv-dach (why the tabular direction lost)

> **Judge 1**: "Y — it drops the fully boxed contact grid and gives the headings proper
> space, so the page reads as composed rather than like a spreadsheet." (Y = OLD)

> **Judge 2**: "Y, because the unboxed contact list and consistent single-family scale
> read cleanly, while X's gridded table and heading collision look like a default
> export." (Y = OLD; X = NEW)

> **Judge 3**: "Y — it presents the same DACH personal-data block as a clean, unboxed
> label/value list with proper spacing, whereas X boxes every cell, misaligns the table
> and crowds the next heading." (Y = OLD; X = NEW)

All three judges independently converged on the same defect in NEW's DACH-Tabellarisch
direction: the fully bordered contact table (table-cell-border ratio 1.0, confirmed above)
reads as a rigid grid/default export, and the "Experience" heading sits with no space
after the table, colliding with it. This is a design defect distinct from the symmetric
language-header issue — judges scored it down on hierarchy (2-3/5, vs 4/5 for OLD) and
pairing (2-3/5, vs 3-4/5 for OLD) independent of the regional FAIL. This is the signal A7's
follow-up research needs: the DACH direction lost primarily on the boxed-table treatment,
not only on the header language it shares with OLD.

## Verdict against the pre-registered condition

**FAIL**, ruled strictly by the letter of the pre-registered condition (Manager ruling,
2026-09-15): the pass condition requires "no regional-correctness fail on NEW" with no
carve-out for a defect symmetric across both conditions. cv-dach's NEW condition fails
regional correctness (all 3 judges), so the gate as a whole does not pass. This is not a
post-hoc reinterpretation of the pre-registration — the KILL SIGNAL condition ("OLD
preferred on ≥2 doctypes") also does not fire (OLD is preferred on only 1 of 3 doctypes),
so the result is a mixed outcome the pre-registration did not anticipate a clean rule for:
neither PASS nor KILL fires as written.

## Scoped decision (Manager, post-hoc, labelled as such — not part of the pre-registered rule)

Because the gate's mixed result was not itself anticipated, the Manager ruled a narrower
default-shipping decision that is a *subset* of what the gate covered, each part of which
individually satisfies every pre-registered clause:

- **cv-us, cv-uk, cv-generic**: keep the Harvard Reverse-Chronological direction
  (`cv-us-uk-designed` → `cv-harvard`/`source-serif-sans`/`cv-harvard` palette) as default.
  NEW preferred 3/3 judges, no regional-correctness fail, zero fail-severity preflight
  facts. Fully satisfies the pre-registered pass clause on its own.
- **cv-dach**: default reverts to `cv-ats-strict` (OLD). OLD was preferred by all 3 judges
  on design grounds independent of the shared language defect (see verbatim reasons
  above) — a real signal, not just the regional FAIL. The DACH-Tabellarisch direction
  (`cv-dach-tabular`) stays authored in the library, available but not default.
- The symmetric defect (English headings over non-English body content) is promoted from
  RESUME.md v0.4 backlog item 4 to **A7**, dispatched before invoice work starts. cv-dach's
  gate is re-run after A7 lands, since the table-treatment defect judges flagged is
  independent of language and may itself need a follow-up fix before DACH becomes a
  serious default candidate again.

No data has been changed as a result of this report. The cv-dach default revert is a
one-line draft-CSV edit the Manager will brief separately once A7's Default Language
column exists on `research/26-t1-doctypes-draft.csv`.
