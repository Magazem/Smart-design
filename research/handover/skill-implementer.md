# Handover -- Skill Implementer (rewritten 2026-09-25)

## fill_family.py (research/designs-evidence/) -- internals
- Two layers. ENGINE (rules): `md_tables` -> `load_corpus`/`discover_corpora` (coded tables in
  `<family>-corpus*.md`, columns aliased via `CANON`) -> `apply_recodes` (last-tagged `header/colour/...`
  column wins, enum-guarded by `_VALID`) -> `combined_table` -> `rank_step1` (combined share, then per-corpus
  shares in config order, corpora count, best pos, key; cap 9). DECISIONS: `fill-specs/<family>.json`
  (corpora cfg, identity, recodes, dropped_*, doc_styles, reasoning rows, designs with archetype/l3,
  fill_rule_provenance). `build()` = spec + engine (ranks, provenance shares) -> 4 CSVs + `<family>-fill-log.md`.
- Section-8 rules in code: `dropped_variants`, `family_default_style`, `propose_style`, `reuse_candidates`,
  `propose_palette` (+`palette_evidence_rank`: fetched authority < search-corroborated < ranked < convention),
  `propose_typeface` (medium rule, then pairing fallback R2), all combined in `section8_proposal(Library)`.
  Rules ratification draft: research/82a-clarifications-6.md (R1-R4).
- Modes: `--check` (diff vs committed, cv must be byte-identical), `--write`, `--dry-run`, `--borrow-from SRC`.
- Palette/typeface picks need per-item hexes/fonts the coded tables lack: hue-bin and safe-stack branches inert.

## Test layout
- Skill: `skill/document-design-intelligence/scripts/tests/` (full run ~75 s): test_resolve_generic (resolver
  R5), test_r2_fixes, test_r6_brandkit + test_make_brand_kit (brand kits), test_pptx_font_rule, test_ddi/
  test_column_parity (handoff), test_portable_sync/test_portable_content (portable pack), test_type_scale_roles.
- Research: `research/designs-evidence/test_fill_family.py` (engine + cv byte regression), `research/p65/`
  (portable-pack trial scorer; needs portable/DDI-LIBRARY.md in current layout).

## Windows / shell quirks
- git-bash `/tmp` != python's temp dir; use repo-relative temp files. Big heredocs with `'''` or `\n` break
  (real newline, `\b` -> 0x08): write patches with the Write tool, run, delete (research/.tmp_*).
- ASCII-only string literals in scripts/*.py (test_ascii_clean): `--`, no em dash. `resolve.BM25` folds
  "ue"->"u" (Quebec->qubec): fold cue lists identically. I run no git; Repo Keeper commits.

## Regeneration order (always)
`python3 research/build-manifest.py` -> `python3 research/load-base.py` -> `python3 research/build-portable.py`
-> `ddi.py check` -> full pytest (skill dir) + test_fill_family.py + research/p65. New family files must be
added to LIBRARY_INPUTS_ENABLED / PROVENANCE_INPUTS_ENABLED in load-base.py and the family's seed rows removed
from provenance/seed-designs.csv (duplicate keys fail the gate).

## Status / left half-done
- cv filled (georgia->times print-scale fix applied); proposal filled. quote<-invoice, whitepaper<-report
  twins confirmed, borrowing never run. Other families: dry-run only, no specs.
- NOT started: 01a0da67 (R7 engine fixes + re-run cv/proposal, per research/92-review-r7-cv-fill.md and
  research/82a-r7-rulings.md) then 01a0da64 (letter + cover-letter fills). Start with R7.
