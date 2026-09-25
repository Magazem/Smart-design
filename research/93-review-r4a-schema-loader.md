# research/93 — R4-early: independent Opus re-review of schema / loader / manifest

Reviewer: Opus Reviewer (claude-opus-5-5). The review was read-only; this file is the only write, and I ran no git.
Scope: research/load-base.py, research/build-manifest.py, data/schema-manifest.json,
scripts/lib/data.py, research/build-portable.py, tests test_provenance / test_designs /
test_portable_sync / test_schema_manifest. Checked against research/80 §R/§2 and research/82 §9.
fill_family.py and the fill outputs were not reviewed. I only grepped fill_family.py to see where it writes.

## Method
- **Snapshot.** I copied the working tree (excluding .git and `__pycache__`) to `%TEMP%\r4a`. There I ran `load-base.py`, then
  `validate_data.py ../data/base`, then the four in-scope tests. Result: loader exit 0, validator
  `OK: validated 16 table(s), 894 row(s)`, tests `27 passed, 1453 subtests passed`.
- **Working-tree state, not a finding.** The regenerated `doc-reasoning.csv` differs from the working-tree copy on the 3
  `proposal-sans-*` rows (`Typeface Bias Terms`). The library input was edited after base was last
  written, which is consistent with the in-flight fill. The full suite on the snapshot also shows 6
  pre-existing failures: test_ddi ×5 and test_resolve ×1, all "twelve cv designs" (base holds 10). Both belong to
  the in-flight cv work.
- **Mutation probes.** Each probe ran on a fresh copy of the snapshot: mutate one input, then run the loader,
  validator, tests and (where relevant) build-portable. Probe ids (P1…P5) are cited below.
- **Data sweep (clean today).** No design's `Evidence Class` is missing from its provenance classes. No non-convention
  provenance row has a blank URL or Source Name. No row mixes convention with other classes. No row has more than one
  convention row. `designs.Family` and `doctypes.Family` are the identical 16-value list. `make_brand_kit.FAMILY_HINT`
  and `resolve._FAMILY_ALIASES` map only into that list.

## R1 (research/84) status
Six R1 findings are fixed:
- F1: convention ranks last (test_designs rule 6).
- F3: ranked rows need a Rank Value (tested).
- F4: convention rows have a blank Fetch (tested).
- F6: Rank contiguity and the prov_key format are tested.
- F8: build-manifest anchors on `__file__`.
- F7: the allow-list comments are no longer stale.

**F5 is only partly fixed.** `LEGACY_UNPROVENANCED` is now empty, but type-scales still sits outside the coverage test (F5 below).

## Findings (severity-ranked)

### H

**F1 — H: the review gate pins filenames, not reviewed content. Designs have no gate at all.**
- **Where:** `load-base.py:190` and `:853` (allow-lists), `:202-204` (name-only match, applied to all five library folders),
  `:832-841` (every `research/designs/*.csv` loads, "no other agent writes here in this phase").
- **The comment's premise is now false.** `fill_family.py:41` sets `DESIGNS = RES / "designs"`, and `--write` writes the
  §9 outputs there and into the gated folders.
- **Failure scenarios:**
  1. **Re-fill after enabling (P5).** `cv.csv`/`proposal.csv` are enabled once. Any later
     `fill_family --family proposal --write`, or a hand edit, reloads with no re-review. P5 changed the enabled
     `research/provenance/proposal.csv` row `designs:proposal-serif-centered:1` to Source URL
     `https://example.invalid/never-reviewed` and `Fetch=search-corroborated`, keeping Rank Value
     `0.425 (17/40)`. Result: loader exit 0, validator OK, in-scope tests 24 passed, full suite adds zero
     failures over baseline, and build-portable writes the pack.
  2. **Cross-table name collision (P1).** Enabling `cv.csv` for doc-reasoning/doc-styles also enables any future
     `research/library/{palettes,typefaces,type-scales}/cv.csv`. P1 dropped an unreviewed
     `palettes/cv.csv` in. It loaded (palettes 43→44), and validate reported OK. Only test_provenance coverage caught it,
     and that check would be satisfied by a matching row in the already-enabled `provenance/cv.csv`, which
     the same engine writes.
  3. **Unreviewed family designs load immediately.** A family designs file lands before its provenance and library
     batch are enabled. Its designs load immediately and feed `doc-reasoning."Design Key"` derivation
     (`:724-732`).
- **Fix:** make each allow-list entry `(<table-folder>/<file>, sha256)`. Fail with `sys.exit` on a hash mismatch or on a
  listed file that is missing. Put `research/designs/` under the same gate.

### M

**F2 — M: build-portable ships a pack from data with tier-2 errors (FK holes, enum drift).**
- **Where:** `build-portable.py:102-107`. It refuses only when `tier1_ok` is false. Its own docstring says a pack
  "built from invalid data would ship silently wrong values".
- **Probe P3:** set `whitepaper-formal`'s Reasoning Key to `no-such-reasoning-row`. The validator names the problem, but
  `build-portable.py` exits 0 and writes `DDI-LIBRARY.md:1189`:
  `| 1 | Whitepaper, formal serif (…) | convention | … | (not present) / (not present) / (not present) |`.
- **Enum drift is also silent here.** A doctype whose Family falls outside the enum is simply skipped, because the family loop at
  `:614` iterates the enum.
- **Why it matters:** portable/ is consumed straight from the repo, not from the release ZIP. So only a pytest run before
  commit stops it. CI runs pytest only on release (`release.yml:62`).
- **Fix:** also refuse on any tier-2 line, or at least on tier-2 lines in doctypes/designs/doc-reasoning/provenance.

**F3 — M: provenance rule 4 ("numeric Rank Value only when fetched") never fires on the §9 canonical format.**
- **Where:** `test_provenance.py:86` (`_is_numeric` uses `float()`) and `:204`.
- **The problem:** research/82 §9 mandates `0.225 (9/40)`, which `float()` rejects. Today 35 of 83 non-blank Rank Values
  are not float-parseable, so the rule cannot see them.
- **Failure scenario:** shown by P5 — a `search-corroborated` row carrying `0.425 (17/40)` passes.
- **Fix:** parse the leading number (`^\d+(\.\d+)?`) or any digit, not the whole cell.

**F4 — M: plan §2C "Source URL blank only for convention" is only half-enforced.**
- **Where:** `test_provenance.py:176` checks that convention rows have a blank URL, and that non-convention rows have a Fetch value.
- **What is not checked:** it never checks that `authority`/`juried` rows have a Source URL or Source Name. Only `ranked` is covered (`:192`).
- **Failure scenario:** an authority row with blank URL and blank Source Name passes. build-portable then prints
  `(unnamed source)` as that design's evidence (`build-portable.py:427`).
- **Status:** clean today (sweep).
- **Fix:** require URL and Source Name for every non-convention class, and a Retrieved date for juried/authority rows.

**F5 — M: polymorphic-FK coverage excludes type-scales, and 32 of 81 rows have no provenance.**
- **Where:** `PROVENANCED_TABLES` (`test_provenance.py:67`) follows the plan's five tables.
- **The gap:** `LEGACY_UNPROVENANCED = set()` (`:102`) reads as "fully covered", and the Table enum and build-portable's grand library both
  treat type-scales as provenanced. On the snapshot, 32/81 type-scales rows lack a row: every row of
  `cv-print, cv-major-third, cv-editorial-fourth, deck-projection, form-print, infographic-screen,
  print-office-generic, report-print, report-screen, report-technical`. These are the scales the
  shipped doctypes actually resolve through.
- **Other omissions:**
  - "Exactly one convention row" (§2C) is not asserted. It is clean today.
  - The Row Key check resolves against base+brand keys, so a provenance row can cite a brand-overlay row.
- **Fix:** either rule type-scales out explicitly (and have build-portable stop printing "(no provenance recorded)"
  for it), or add it to `PROVENANCED_TABLES` with the 32 rows as a named LEGACY list that may only shrink.

**F6 — M: nothing ties a design's `Evidence Class` or family to its evidence.**
- **The gap:**
  - test_designs checks rank order by class, and test_provenance checks provenance rows independently.
  - No test asserts that `designs."Evidence Class"` is among that design's provenance classes (e.g. `ranked` ⇒ ≥1 ranked
    provenance row).
  - No test checks that a design's Reasoning Key is not another family's doctype default.
- **Failure scenarios:**
  - A fill that labels a design `ranked` while shipping only a convention provenance row passes every test. Rule 6 then
    ranks it as non-convention.
  - A `cv-*` design pointing at `report-classic` passes too.
- **Status:** clean today (sweep).
- **Fix:** add both assertions to test_designs.

**F7 — M: `lib/data.py:171` parses CSV via `text.splitlines()`, which splits records inside valid quoted cells.**
- **What `splitlines()` does:** it breaks on `\n` inside quotes, and also on U+2028, U+0085, `\x0b`, `\x0c` and `\x1c-\x1e`.
- **Probe P4:** a U+2028 in `whitepaper-formal."Best For"`. The loader wrote a correct CSV; test_designs (which uses
  `csv`) passed. data.py split the record, so the validator reported a phantom row 32 (`Family: 'convention' not in allowed enum`,
  `Evidence Class: ''`), and resolve/portable read a truncated whitepaper row.
- **Why it's likely to happen:** web-scraped Source Name or Best For text is the likeliest carrier.
- **A related silent problem:** `dict(zip(columns, row))` (`:227`, `:265`) drops extra cells and leaves short rows' columns absent,
  and there is no row-length check.
- **Fix:** `csv.reader(io.StringIO(text, newline=""))`, plus a tier-1 "row has N cells, header has M" problem.

**F8 — M: silent batch drop through `generic_only`.**
- **Where:** `load-base.py:108-115`. Brand Scope is compared case-sensitively and whitespace-stripped, and the
  column's presence is decided from `rows[0]` only.
- **Probe P2:** `Generic` in the enabled `ranked-colourlovers.csv` dropped all 15 palettes. The loader
  only printed `skipped 16 brand-scoped rows: Generic x 15` and exited 0; validate reported OK.
- **What caught it:** only test_provenance, through dangling Row Keys.
- **Blind spots:**
  - A batch with no provenance vanishes unseen.
  - A second file missing the column is also dropped as `(blank)` whenever the first file has it.
  - Separately, a blank-scoped duplicate of a draft key is dropped before the duplicate check, so it cannot trip it.
- **Fix:** exit on any Rule-1 scope value that is not `generic` and not a known brand slug (`BRAND_SLUGS`).

### L

**F9 — L: `designs.Rank` is untyped in the manifest.** P3's first attempt put `no-such-reasoning-row` into Rank, and the
validator reported OK. Only test_designs caught it. build-portable crashes on it with an `int()` ValueError at `:442`, which is
at least loud. Fix: add a manifest `integer_columns` (or pattern) check so the validator owns it.

**F10 — L: Windows newline and case fragility.**
- **CRLF on Windows:** `build-manifest.py:559` and every rationale/`26-t11` write in load-base
  (`write_text`) emit CRLF on Windows. Measured: `write_text('a\nb\n')` → `b'a\r\nb\r\n'` on this Python 3.14 win32.
  This contradicts the LF promise in the loader docstring.
  - It is harmless in git (`* text=auto eol=lf`) and in the byte tests (they fold CRLF).
  - But `build_zip.py` zips working-tree bytes, so a Windows local build ships CRLF rationale files.
  - Fix: `write_text(..., newline="\n")` or `write_bytes`.
- **Case-sensitive allow-list match:** it is exact (`path.name in …`), so on NTFS `CV.csv` silently does not load.

**F11 — L: no non-empty-key check.** Neither the loader's duplicate check nor `data.py`/validate rejects a blank key
cell. It is caught indirectly for the provenanced tables (prov_key regex), but not for type-scales, headings or constraints.

**F12 — L: stale hard-coded CHANGES strings in load-base.** Three examples:
- "T7: 11 rows" — it wrote 22.
- "T14: 15 rows" — it wrote 22.
- "os-bundled for every row … none resolve to an Office-only fallback" (`:251`) — 2 rows are `office-bundled` (Cambria).

Also, a blank `Safe Stack Fallback` would be derived as `office-bundled`, not `none` (`:249`). Fix: count them, as T13 already does.

**F13 — L: the manifest's `provenance.Table` enum accepts all 15 tables.** That includes headings, constraints and render-targets.
It is `sorted(tables.keys())` taken at the provenance declaration (`build-manifest.py:476`), so it also silently
excludes any table later declared after provenance. Scoping it to the provenanced set would make F5's decision
explicit. Separately, `_provenance_line` shows only `matches[0]` (`build-portable.py:423`). A design ranked in two corpora
displays one, in file order.

## What is sound
- **Duplicate keys** (draft+glob, glob+glob, across family files) exit loudly.
- **Brand guard:** `assert_no_brand_rows` runs over all tables after load.
- **Group/list FK declaration guard:** build-manifest asserts every list FK is also in `list_columns`.
- **Manifest and portable sync tests** compare bytes after a CRLF-only fold and include guard-the-guard tests.
- **Family enum** is a single constant shared by both tables. Downstream literal maps agree with it.

## Recommended order
1. F1: hash-pinned allow-lists, with designs gated too.
2. F2: build-portable refuses on tier-2 errors.
3. F3, F4, F6: three small test additions.
4. F7: the parser fix, which is a one-line change plus a length check.
5. F5 needs a ruling from the orchestrator. The rest are cleanups.
