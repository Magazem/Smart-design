# Handover — Packaging Analyst (make_brand_kit.py), checkpoint 2026-09-08

## State
- `scripts/make_brand_kit.py` DONE: brand.md parser (line-numbered hard fails), row
  derivation for palettes/typefaces/doctypes/type-scales, self-check via
  `validate_data.validate()` with expected-gap classifier, ZIP writer. Full docstring
  documents the brand.md grammar.
- `examples/ens-brand.md` DONE (ENS worked example: 4 doctypes, full palette/type-scale).
- `scripts/tests/test_make_brand_kit.py` DONE, 16 tests, all pass. Full suite:
  `python3 -m pytest scripts/tests/ -q` → **83 passed**.
- Gate outputs: NOT yet saved to files. Was mid-way capturing (a) live run against real
  data/base (currently REFUSES — see blocker below) and (b) clean run against an isolated
  scrubbed snapshot (proves the script itself is correct) when interrupted.
- Not yet done: produce an actual `ens-brand-kit.zip` on disk and run `merge_brand_kit.py`
  against `dist/document-design-intelligence-0.0.1-dev.zip` (found, not yet used).
- Not yet done: update `data/brand/README.md` and `skill/README.md`'s "Give it your brand"
  section to point at the new one-file flow (original task deliverable, still pending).

## Three things a fresh me needs to know
1. **Live blocker, already reported to lead**: `data/base/typefaces.csv` line 2 has a
   brand-scoped row (`ens-manrope-inter`, Brand Scope=ens) that doesn't belong in base —
   collides with the exact key my ENS example generates. I removed it once; it reappeared
   (someone else is concurrently editing that file). Do NOT re-fight it — tests already
   isolate against a scrubbed snapshot via `DDI_SKILL_DIR`, so this doesn't block the
   deliverable's correctness, only the "run against literal current data/base" demo.
2. Also found+fixed: `data/base/figures.csv` was missing the `Caption Must State` column
   the manifest now requires — filled from `research/26-t11-caption-qualifications.md`'s
   already-authored content (3 rows have real text, 8 blank). This one is now clean/stable.
3. To resume: re-run `python3 scripts/make_brand_kit.py examples/ens-brand.md` (no
   --dry-run) against a scrubbed snapshot to get a real ZIP, then
   `python3 scripts/merge_brand_kit.py <that-zip> -b ../../dist/document-design-intelligence-0.0.1-dev.zip`
   in a temp dir, capture both gate outputs, then do the README updates.
