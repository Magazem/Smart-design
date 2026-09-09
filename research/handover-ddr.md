# Handover — Document Design Researcher, context reset

## DONE (verified csv.reader clean)
- **research/26-t1-doctypes-draft.csv**: `ens-web-tool` row dropped (34 rows, was 35).
  Slide-deck Reasoning Keys split: `deck-generic`→`deck-projection`/`deck-screen`/`deck-handout`.
  26-notes.md updated to record both rulings as resolved.
- **research/29-t2-doc-reasoning-draft.csv**: 21 rows, 1:1 match against T1's 21 unique
  `Reasoning Key` values (verified by script). 12 cols = manifest's 10 + draft-only
  `Reasoning`/`Confidence` (advisor-confirmed: draft-only, strip to `rationale/doc-reasoning.md`
  at load per Rule 2 — manifest's shipped header stays 10 cols, task brief's "Rev 2 added
  Reasoning/Confidence" premise is wrong, corrected not obeyed literally).

## HALF-DONE
- **research/29-notes.md**: NOT YET WRITTEN. Must document: Doc Conditions action fixes
  (`field-underline-only`/`print-legibility-l-delta` don't exist in constraints.csv anymore;
  used `photocopy-safe-color`, `ats-strict`(Set Key), `professional-print`(Set Key),
  `proj-body-floor` instead); `if_hand_filled` points at PROPOSED `field-legibility-min`
  constraint that doesn't exist in T9 yet (real gap); T1×T9 Constraint-Set-Keys cross-check
  (done in head, not written) explains every Severity=fail/warn choice.

## NOT STARTED
- **research/30-t6-type-scales-draft.csv + notes** (Deliverable C). Plan already fixed:
  scale_row_key = `<scale_key>-<medium>-<role>`. 17 rows: 4 sourced (`deck-projection`:
  projection/body/24/1.25, projection/body-dense/18/1.25, projection/h1/36/1.10;
  `deck-screen`: screen/body/18/1.25) + 7 ENS (`ens-print`, medium=print: label 8.5, caption 9,
  body 11, lead 12, h3 16, h1 24, **legal 8.5 — needs `Role` enum widened to add `legal`**,
  same precedent as T12's `customary`) + 6 generic CONVENTION (`print-office-generic`: label
  8.5, caption 8.5, body 11, h3 12, h2 16, h1 24, leading 1.20 except body 1.35 — all inside
  T9's [1.20,1.45] check).
- **research/18-cv-region-rules.csv malformed-comma fix** (research/25 finding #6:
  `EU-Europass,mid` / `Gulf-GCC,early` rows have unescaped commas in `source`) — not touched.

## Critical facts for fresh context
1. T5 (`typefaces.csv`, already shipped) references 6 Scale Keys: `ens-print`, `cv-print`,
   `report-print`, `report-screen`, `report-technical`, `form-print`. My planned T6 only
   creates `ens-print` + 2 new deck keys + 1 new generic key — **4 of T5's 6 references stay
   dangling** (cv-print, report-print, report-technical, form-print all resolve to nothing;
   report-screen resolves to nothing and has no print/generic analog at all). Report this as
   the primary FK gap; recommend repointing those 4 to `print-office-generic` unless someone
   has a sourced reason they differ.
2. T2's Typeface Key `safe-sans-deck` (used on `deck-projection`/`deck-screen`) is PROPOSED —
   no such T5 row exists. `ens-slides`' Typeface Key `ens-manrope-inter` has Scale Key=
   `ens-print` (print-medium only) — ENS slides need projection-medium sizes that don't
   resolve yet; ENS's own numbers (title 36-40/body 24/dense 18-20, v2 §3D) coincide with
   generic `deck-projection`'s sourced values, so recommend a new ENS typeface row pointing
   there rather than inventing brand-specific numbers.
3. Style Key/Palette Key (T3/T4) are wholly unauthored — every value in 29 is either the
   schema's own given example (`ens-document-grid`,`ens-core`,`cv-restrained`,`mono-ink`,
   `report-classic-serif`) or my own invented slug, all to be listed as the T3/T4 brief.
