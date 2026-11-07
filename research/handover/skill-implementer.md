# Handover -- Skill Implementer (rewritten 2026-09-25, after R7)

## fill_family.py (research/designs-evidence/) -- internals
- ENGINE decides, SPEC only holds wording + ratified overrides (R7-4). Flow: `md_tables` -> `load_corpus` ->
  `apply_recodes` -> `combined_table` (k = ADMISSIBLE only, N unchanged; `inadm` tallied for the log) ->
  `rank_step1` (combined, then shares in `corpus_order` = level, N desc, id) -> `plan_designs` (which spec
  designs ship, rank, class; cap 10 TOTAL; matched default outside cap takes the last ranked slot; unmatched
  default counts inside the cap; identity-duplicate retirement via `own_archetype`; `pending` skipped) ->
  `resolve_family` (section-8 proposals per shipped design, new reasoning rows filled from the engine's
  first candidates, `blank_bias`, `violations`) -> `build` (4 CSVs + `<family>-fill-log.md`).
- Spec fields now: corpora, identity, recodes, date, doc_styles (authored NEW rows only), reasoning.defaults +
  anti_tokens.default, `reasoning.rows` = [] (only override rows), designs (wording, archetype, l3,
  `style_row`, `own_archetype`, `pending`, `override`). No Rank / Evidence Class / fill_rule_provenance.
- `--check`: prints VIOLATION lines then diffs CSVs; `--write` refuses while violations stand.
  `_override_ok`: file under research/ exists, first 20 lines have no "draft"/"not ratified", a line starts
  with the rule id. 82a-clarifications-6.md is still DRAFT -> not citable.
- `Library(family)` hides the family's own previous rows (research/library/doc-styles/<family>.csv), so a
  re-run never reuses its own output. `_lib_rows` dedupes identical rows (base already holds library rows).
- Reuse (`reuse_candidates(proposal, styles, family)`): mapping equal, no column/photo contradiction, no
  region/standard token (`FAMILY_SPECIFIC`), `<family>-` keys first then byte order.
- Typeface: declared-font branch (`font` column, OS_BUNDLED) else class/popularity/medium rule; pairing
  fallback = DRAFT R2 (unratified, logged as such). cv/proposal corpora have no font column: logged "not evaluable".
- Modes: `--check`, `--write`, `--dry-run`, `--borrow-from SRC`.

## Test layout
- Skill: `skill/document-design-intelligence/scripts/tests/` (full run ~65 s, 328 tests).
- Research: `research/designs-evidence/test_fill_family.py` (57, incl. TestR7Rules), `research/p65/` (10).

## Windows / shell quirks
- The Bash tool collapses `\\` in heredocs, so `\b` regexes become 0x08 bytes and `"\x00"` a NUL: write patch
  scripts with the Write tool (research/.tmp_*), or use chr(92). After any patch run
  `grep -c $'\x08' fill_family.py`-style checks (I ran a python count of chr(8)/chr(0)).
- git-bash `/tmp` != python's temp dir. ASCII-only literals in skill scripts/*.py. I run no git.

## Regeneration order (always)
`fill_family.py --family X --write` -> `python3 research/build-manifest.py` -> `research/load-base.py` ->
`research/build-portable.py` -> `ddi.py check` -> skill pytest + test_fill_family.py + research/p65.
New family files go into LIBRARY_INPUTS_ENABLED / PROVENANCE_INPUTS_ENABLED in load-base.py; seed rows of the
family come out of provenance/seed-designs.csv (duplicate keys fail the gate).

## Status
- R7 + ratified 82a-clarifications-6 (R6 cap as fixed point, R7 audience tokens, R2 ratified) applied: cv 10 designs,
  proposal 6. letter 10 designs, cover-letter 9 designs (task 01a0da64 done; letter/cover-letter fill.md + logs written,
  load-base allow-lists + seed-designs.csv rows for letter-formal / cover-letter-professional handled).
- Reuse rules added this session: `OTHER_FAMILY_WORDS` (+ `RELATED_FAMILIES`, family's own doctype styles exempt), photo
  None rejects "photo permitted" rows, `Library` hides EVERY fill-written doc-style row (order independence), design
  `override` on a `style_row` (R4, header placement) lets an authored row win. `dropped_variants` also parses
  paragraph-form agreement text.
- Spec generation for a new family: copy the seed design rows from base designs.csv, `archetype` for merged seeds, new
  designs named `<family>-<heading>-<colour>-<header>` with `style_row` only where the engine finds no reuse (or R4 override).
- Next queued by the orchestrator: whitepaper (01a0da6e, A5 borrow plan), then deck (identity background|heading|title
  layout, colour dropped, 82a-clarifications-7: engine IDENTITY_SLOTS/`_VALID` may need "background"/"title layout" checks).
