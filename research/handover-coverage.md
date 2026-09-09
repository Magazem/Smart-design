# STATUS — load pass 4 is DONE and the gate is 0

Written 2026-09-09. Supersedes the step-3 status block below. Nothing is half-applied;
the loader is re-runnable and idempotent.

**Landed on disk (load pass 4 + the both-empty contrast rule)**
- `research/load-base.py` — new `LOAD PASS 4` section. T10 `structures` loads from
  `research/36-t10-structures-draft.csv`: 17 draft rows -> 17 generic, header already
  equalled the manifest exactly, no ENS rows in the draft so `generic_only()` passed them
  through whole (neither Rule 1 nor Rule 2 applies).
- `data/base/` — **14 of 14 tables, 291 rows** (was 13 / 274). `structures.csv` is the
  last table. `Section Order` blank on 15 of 17 rows BY RULING, left blank; see
  `research/36-notes.md` for the tokens `headings.csv` still lacks. Step 9 work.
- `scripts/validate_data.py` — `contrast_at_least` now skips a pair only when BOTH cells
  are empty; exactly-one-empty still errors. Two-line guard inside the existing `derived`
  loop, contained to that one function. `lib/color.py` and `lib/data.py` untouched.
- `research/09-library-schema.md` — T4 "Design notes" gains a **Blank cells** bullet
  declaring the asymmetry: blank FK skipped per cell, blank contrast pair skipped only
  pairwise, half-filled pair is a hard error. Also requires any future derived check to
  declare its own blank behaviour in its table section before shipping.
- `scripts/validate_data.py` docstring — the CHECKS list's `contrast_at_least` bullet now
  states the same rule, so code and schema doc agree.
- `scripts/tests/fixtures/make_manifest_fixtures.py` — two new builders,
  `manifest_contrast_both_blank_ok` and `manifest_bad_contrast_half_blank`. Only those two
  were generated (the generator was NOT run over the whole tree, so no existing fixture
  moved).

**Gate: 0.** `OK: validated 14 table(s), 291 row(s)`. Was 31 at the start of this pass:
29 `Structure Key` + 1 structures missing-file (both cleared by item 1) + 1 mono-ink
blank-contrast (cleared by item 2). The predicted intermediate of 1 was observed.

**Tests: 124 passed + 8 subtests, 0 failed.** `test_validate_data.py` 27 -> 30; the three
new tests are one per branch — both blank = clean, one blank = fails, both present and
failing = one line. The half-blank fixture carries BOTH orderings (blank `On Primary` on
one row, blank `Primary` on the next) and the test asserts exactly two lines, so the rule
is proven not to be one-sided. My delta is exactly 3. The 2 tests above the brief's 119
baseline are in files I did not touch; I did not trace where they came from.

**Verified**: loader idempotent over two consecutive runs (all 14 base CSVs md5-identical);
`assert_no_brand_rows()` clean; `data/schema-manifest.json` md5 `731d874f` UNCHANGED.

**Gaps found this pass, NOT fixed (out of the brief's two items)**
1. `scripts/make_brand_kit.py` emits `Structure Key` blank on every brand doctypes row,
   and its docstring gives the reason as "`doc-styles.csv` and `structures.csv` do not
   exist yet". `structures.csv` exists as of this pass, so the stated reason is now
   false while the behaviour is unchanged. Gate 0 is NOT at risk (blank FKs are skipped,
   and `data/brand/ens/` does not exist on disk today), but a regenerated ENS kit will
   silently ship doctypes with no structure. `data/schema-manifest-NOTES.md` carries the
   same stale claim in several places, including two pasted gate transcripts.
2. The `contrast_at_least` problem line always anchors to the rule's `column`, so a row
   with a blank `against_column` and a correctly filled `column` tells the author the
   problem is in the cell they got right. My own half-blank test asserts this current
   behaviour. Fix sketch: name the empty column in the message text. Deliberately not
   changed here — it would break `manifest_bad_contrast`'s existing assertion and it is
   outside the brief's one-function containment.
3. `research/36-notes.md` records that the schema doc's own worked example for
   `Section Order` (`contact;summary?;...`) would FAIL `validate_data.py`'s literal
   token match, because there is no tolerance for the `?` optional marker. Either the
   schema drops the `?` convention or the validator learns it. Undecided.

**Open, not mine**: `headings.csv` covers only 11 CV `canonical_section` values, so 15
structures rows cannot get a `Section Order` until T13 is extended (step 9, post-v0.1.0).
`research/36-notes.md` lists what each document family needs. Also note `cv-academic`'s
order is UNCITED convention, flagged in `36-notes.md` — it is not sourced the way
`cv-experienced`'s is.

---

# STATUS — read this first (step 3 is DONE, not mid-flight)

Written 2026-09-09 at the lead's checkpoint request. **Step 3 completed and self-verified
before the request arrived**; nothing is half-applied and the loader is re-runnable. The
detail below this block is the evidence, not pending work.

**Landed on disk**
- `research/load-base.py` — new `LOAD PASS 2` section loads four tables; new `BRAND_ROWS`
  map + `assert_no_brand_rows()`; `write()` now returns its pre-projection rows.
- `data/base/` — **12 of 14 tables, 260 rows** (was 8 / 190). doctypes 30, doc-reasoning 15,
  doc-styles 10, type-scales 15.
- `data/rationale/doc-reasoning.md` — NEW, loader-written. T2's draft-only
  `Reasoning`/`Confidence` stripped here per Rule 2. First `rationale/` file to exist.
- `research/09-library-schema.md` — `figures.Caption Must State` retyped **`V` → `P`**,
  edited in five places (type row, legend, §8 item 11 incl. its stale "five of seven"
  count, the Rev 4 erratum's forward ref, and a new §9 follow-on erratum block).
- `data/schema-manifest.json` — regenerated, **md5 `0b4a079f…` UNCHANGED**.

**Gate: 82** (was 13). The count is not the diagnostic — the line sets are.
- **45 expected**, target table not authored yet: 29 `Structure Key`, 14 `Palette Key`,
  2 missing-file declarations. Clears at step 6.
- **37 real**, target table IS authored: 28 `Page Format Key` (**B1**), 7 CV-region
  `Constraint Set Keys` (**B2**, = RESUME flag (b) confirmed), 1 `png-chromium` (**B3**),
  1 `safe-sans-deck` (**B4**). Left unfixed on purpose — see B1–B4 below.

**Verified**
- Loader idempotent; **all 8 pass-1 tables md5-identical** to a reconstructed pre-change
  loader, so no earlier table moved.
- Tests **105 pass + 8 subtests, 4 fail; 109 still collect.** The 4 are all
  `test_make_brand_kit.py` — see BLOCKER.
- `assert_no_brand_rows()` clean. **The old `grep ",ens," data/base/*.csv` check was broken**
  and is replaced — it only ever matched a whole-field `ens`, so it was blind to
  `doc_category=ens-slides` and `scale_key=ens-print`, the exact seam step 3 had to close.

**Decisions recorded**
- T2 `Reasoning`/`Confidence` → stripped to `data/rationale/doc-reasoning.md`; ships in the
  ZIP (`build_zip.py` is a denylist), decided deliberately.
- `Caption Must State` → **`P`**. Nothing under `scripts/` reads it — not `preflight.py`,
  which the ruling named, nor `resolve.py`/`validate_data.py`/`ddi.py`.

**What remains (not mine, needs the Orchestrator)**
1. **B1 is a ruling, not a fix** — do not let anyone edit `26` or `research/30` on the
   strength of the wording below until it is decided.
2. Step 5 is **BLOCKED**: this pass breaks `make_brand_kit.py` (4 test failures).
3. Step 4 is unblocked — `doctypes.csv` now exists.

---

# Handover — Coverage and Gap Analyst (checkpoint after critical-path step 3)

Supersedes the step-1 checkpoint. Step 1's content is condensed to "Numbers" below; the
step-1 open gaps that are still open are carried forward under OPEN GAPS.

## DONE on disk this pass (load pass 2 + the P-letter seam)

**1. Four tables loaded. `data/base/` is 8 → 12 tables, 190 → 260 rows.**
All four drafts were authored against the manifest header exactly (verified column-by-column
before loading), so there was no re-header step. `research/load-base.py` gained a
`LOAD PASS 2` section:

| table | draft | draft rows | loaded | dropped |
|---|---|---|---|---|
| T1 `doctypes` | `26-t1-doctypes-draft.csv` | 34 | **30** | 4 ENS (`Brand Scope`) |
| T2 `doc-reasoning` | `29-t2-doc-reasoning-draft.csv` | 19 | **15** | 4 ENS (`BRAND_ROWS`) |
| T3 `doc-styles` | `31-t3-doc-styles-draft.csv` | 12 | **10** | 2 ENS (`Brand Scope`) |
| T6 `type-scales` | `30-t6-type-scales-draft.csv` | 22 | **15** | 7 `ens-print` (`BRAND_ROWS`) |

**2. The brand seam in T2/T6 — the part of this step that was not on the brief.**
T1/T3/T5 have a `Brand Scope` column, so `generic_only()` already handled them. **T2 and T6
do not have one and never will** — Revision 4 §0.3 sets `Brand Scope` by the *directory* —
yet their drafts carry 11 brand rows between them. Closed with a declared `BRAND_ROWS` map
in the loader (`{table: (column, {keys})}`), listed by key and never prefix-matched: a
generic key is allowed to begin with a brand's letters. The map errors out if it lists a key
no draft row uses, so a re-authored draft cannot silently reinstate a brand row.

Rejected: adding a draft-only `Brand Scope` column to `29`/`30`. It breaks the loader's own
"drafts are provenance and are never modified" invariant, and it is the `figures.Anti-Patterns`
trap in mirror image — a column that tells the next contributor the table has a column it
does not have. Also rejected: adding `Brand Scope` to the manifest for T2/T6 (contradicts §0.3).

**3. The verification the standing rules relied on was broken, and is replaced.**
`grep ",ens," data/base/*.csv` matches a field whose value is **exactly** `ens` — i.e. a
`Brand Scope` cell. T2's brand rows are `doc_category=ens-slides`; T6's are
`scale_key=ens-print`. **Neither has any field equal to `ens`, so that grep reports clean
even with all 11 rows loaded.** It could not see the seam this step exists to close. Replaced
with `assert_no_brand_rows()`, which runs at the end of every load: every cell of every
written table, split on `;`, each token compared whole against `BRAND_SLUGS` and against
`<slug>-`. Whole-token comparison is why `body-dense` (a real `type-scales.Role`) is not a
false positive. **The rule is now enforced by the loader, not remembered.**

**4. T2's `Reasoning`/`Confidence` disposition — stripped, not lost.**
Both are draft-only. Rule 2 (`09-library-schema.md:70`) puts provenance in a sibling
`rationale/<table>.md`, so `write()` now returns its pre-projection rows and the T2 block
writes **`data/rationale/doc-reasoning.md`** — 15 entries, loader-generated, do-not-hand-edit.
`build_zip.py` is a *denylist* (`rglob` minus `__pycache__`/`tests`/`.gitkeep`), so this
**ships in the ZIP**. Decided deliberately, not by accident: `data/base/README.md` and
`data/brand/README.md` already ship, and the skill directory is the contribution surface.
*First `rationale/` file to exist* — `rationale/cv-regions.md` and `rationale/headings.md`
have been promised by the loader's own CHANGES strings since load pass 1 and were never
written. Not backfilled here (not this brief).

**5. The P-letter seam is closed. `figures.Caption Must State` is `V` → `P`.**
The ruling set the test — *the letter follows whether a script actually reads the column* —
and named `preflight.py` as the candidate. Checked: a recursive grep for the column name
across `skill/` returns `data/base/figures.csv` (header), `data/schema-manifest.json`
(column list) and `data/schema-manifest-NOTES.md` (Revision 3 entry), and **nothing under
`scripts/`** — not `preflight.py`, `resolve.py`, `validate_data.py` or `ddi.py`. Retyped.

Edited in **five** places, because changing the letter alone leaves the document
self-contradictory: the T11 type row; the legend ("exactly six" → seven, and the
deliberately-left-at-`V` paragraph rewritten); §8 item 11 (the count, **and "five of the
seven sit in figures.csv" → six**, which is the number that goes stale silently); the
Revision 4 erratum's forward reference; and a new *"Erratum follow-on — the seventh prose
column"* block in §9. `schema-manifest-NOTES.md:323` needed no edit — it makes no S/V/R claim.

The argument §8 item 11 demands is stated: **this seventh is a correction of a mislabel, not
a widening.** Nothing was enforced and then stopped — the column has been prose since
Revision 3 created it and its `V` claimed a validator that never existed. The count of `P`
columns rose because the count of *truthful* labels rose. Item 11 now watches for an eighth,
with that distinction attached so the warning stays meaningful.

## Numbers to check a future change against

- `data/base/`: **12 of 14 tables, 260 rows.** doctypes 30, doc-reasoning 15, doc-styles 10,
  type-scales 15, typefaces 7, page-formats 11, constraints 42, figures 11, cv-regions 14,
  headings 81, font-substitutes 15, render-targets 8.
- Manifest: **14 tables, 174 columns, 13 FKs (5 group), 8 list, 1 reference.**
  md5 **`0b4a079fbbfd2678cc463a78648dbe86` — UNCHANGED** across both this load and the P
  retype. That is the proof both were scoped right: load pass 2 needed no schema change, and
  a retype is a fact about the document only.
- Loader: **idempotent** — `data/base/*.csv` + `data/rationale/*.md` byte-identical over two
  consecutive runs. 18 brand rows skipped (typefaces 1, doctypes 4, doc-reasoning 4,
  doc-styles 2, type-scales 7). `assert_no_brand_rows()` clean.
- **No load-pass-1 table moved.** Idempotence alone cannot show this — it compares the *new*
  loader to itself, and `generic_only()` was restructured while `write()` gained a return.
  Verified properly: the pre-change loader was reconstructed (original `generic_only`, no
  `write()` return, LOAD PASS 2 removed), run into a temp dir, and all **eight** pass-1 CSVs
  are **md5-identical** to the live ones — typefaces `052be80a`, page-formats `6abdb0e9`,
  constraints `ee16f000`, figures `c183e0f4`, cv-regions `bee01b6f`, headings `912eabfc`,
  font-substitutes `16b17428`, render-targets `a11928ad`. This is what makes 260 a measured
  number and not a sum.
- Gate: **82 problems** (was 13). See the bucket table below — the *line sets*, not the
  count, are the diagnostic. A count alone cannot survive a floor this noisy.
- Tests: **105 passed + 8 subtests, 4 FAILED** (was 109 + 8, 0 failed). **109 still collect**
  (`--collect-only`: 109 total, `test_make_brand_kit.py` 16) — checked, because a collection
  error in that file would drop tests from the total silently and 105 + 4 = 109 only means
  something if nothing disappeared. All four failures are `test_make_brand_kit.py`, same root
  cause — see BLOCKER below.

## The gate, bucketed by whether the FK target table exists

Deliberately **not** "fixed" by teaching `validate_data.py` a pending class. It is the
instrument this change is measured with, and bucket A evaporates on its own at step 6.

**Bucket A — target table not authored yet. Expected; clears at step 6. 45 lines.**

| n | line class |
|---|---|
| 29 | `doctypes.Structure Key` → `structures.structure_key` |
| 14 | `doc-reasoning.Palette Key` → `palettes.palette_key` |
| 2 | `palettes.csv` / `structures.csv` declared in manifest but file does not exist |

**Bucket B — target table IS authored. These are real, and they are the finding. 37 lines.**

| n | line class | verdict |
|---|---|---|
| 28 | `doctypes.Page Format Key` → `page-formats` | **B1**, below — the serious one |
| 7 | `doctypes.Constraint Set Keys` → `constraints.Set Key` | **B2** — RESUME flag (b), confirmed |
| 1 | `doctypes.Render Target Keys`: `png-chromium` | **B3** — one-token typo |
| 1 | `doc-reasoning.Typeface Key`: `safe-sans-deck` | **B4** — one missing key |

`doctypes.Region Key` produced **zero** failures — all 7 region slugs resolve. That was a
predicted risk and it is disproved by the run; do not re-investigate it.

### B1. T7 `page-formats.csv` is the print-production half of a table that needs both halves

**28 of 30 doctype rows cannot resolve a page format** — the single most load-bearing thing a
doctype tells a generator. This is *not* an authoring slip in `26`, and it must not be fixed
by renaming T1's keys:

- **The schema's own examples dangle.** `09:483` gives `a4-cv-single-col` as T1's generic
  `Page Format Key` example; `09:1043` gives `letter-trifold` as T7's own generic
  `page_format_key` example. **Neither is in the shipped table.** T1's author used the
  document's examples; the shipped T7 data diverged from them.
- **All 11 shipped rows are `Print Mode = professional`.** T7 ships zero `office` and zero
  `photocopy` rows, though the enum has all three. The table was authored from
  `14-print-production-values.md` §2, a print-production source, and it faithfully covers
  that domain: `a4/a5/a3/letter/dl-professional`, three folds, a business card, two posters.
- **`Measure mm` is EMPTY on all 11 rows.** The schema types it `number`, marks it `V`, leads
  T7's purpose statement with it ("margins, measure") and shows it in the §3 resolver trace
  (`measure 130mm`). It is **not** marked `nullable`, unlike `Panels mm` and `Stock gsm`
  which are. The gate cannot see this — it has no required/non-null check for non-FK columns.
  A separate, gate-invisible defect in an already-"authored" table.
- **T1 asks for rows that encode document use, not sheet + finish**: `a4-cv-single-col`,
  `a4-report-standard`, `a4-letter-standard`, `a4-form-standard`, `a4-one-pager` are five
  different margin/measure/column setups on one sheet. Collapsing them onto the single
  `a4-professional` row would delete exactly the distinction T7 exists to carry.
- **Three formats are missing outright, not misnamed**: `widescreen-16-9` (no projection
  format at all), `px-infographic-portrait` (no pixel-dimensioned canvas), `a3-poster`
  (T7 has `poster-a1`/`poster-a2` and `a3-professional`, so this one is also a naming clash
  to settle).
- **`make_brand_kit.py` found the same hole independently**, before this pass: its self-check
  emits `NOTE: social: no Page Format Key (... no generic 'Post reseaux sociaux'-shaped
  format in data/base/page-formats.csv yet)` and the same for `slides`.

**This needs an Orchestrator ruling before anyone edits either file. Nobody should start
authoring T7 or renaming T1's keys on the strength of this section alone.**

The ruling I recommend, with the evidence above behind it: **T7 gains ~11 document-use rows
and populates `Measure mm` on all of them; T1's keys stay.** Reasoning — T1's keys match the
schema's own documented examples and carry the layout distinction the resolver needs, while
T7's encode `Print Mode`, a fact that is already its own column. The competing option
(rename T1's keys onto the 11 existing rows) is cheaper by a wide margin but collapses five
distinct A4 setups onto one row and leaves `Measure mm` empty either way, so it buys a clean
gate and loses the data. A third option — leave both and let step 6 absorb it — is what I
would pick *only* if T7 authoring cannot be staffed, since B1 also blocks step 5.

Either way it is a T7 authoring task (~11 rows × 18 columns, needs the print/typography
domain), not a reconciliation, and it is not mine.

### B2. The seven per-region CV `Set Key`s — RESUME open flag (b), now confirmed with evidence

`us-cv-region`, `uk-cv-region`, `dach-cv-region`, `france-cv-region`, `eu-generic-cv-region`,
`eu-europass-cv-region`, `gulf-gcc-cv-region` are in T1's `Constraint Set Keys`. The only CV
set in `constraints.csv` is **`cv-region`** (singular, generic, reached by `Applies To
doctype:cv-*`). T1 tried to encode *which* region through the Set Key; the mechanism that
actually works is `Region Key` — which resolves cleanly on all 7 rows.

**Recommendation: T1's 7 regional CV rows carry `ats-strict;cv-region`, and `Region Key`
does the regional selection.** One-line-per-row edit to `26`, no new T9 rows. Ruling +
draft edit, so it belongs to whoever owns `26`.

### B3 / B4. Two single-token dangling keys

- `doctypes.Render Target Keys: png-chromium` → the only PNG target is **`png-social`**.
  Same class as the step-1 `html-export` gap, which is now moot (its row is ENS and skipped).
- `doc-reasoning.Typeface Key: safe-sans-deck` → no such row. Candidates in the shipped 7:
  `safe-sans-arial` (safe stack) or `ofl-source-sans-serif`. Needs one line of judgement
  from whoever authored `29`, not a guess from here.

**Deliberately not fixed by me, even though B3/B4 are one token each.** Fixing the two cheap
ones while B1 (28 lines) and B2 (7 lines) stand would move the gate to 45+2 and make it
*look* nearly clean while the load-bearing column is still 100% dangling. A number that
flatters the state is the failure mode this project keeps catching.

## BLOCKER — this pass breaks `make_brand_kit.py`, and therefore step 5

Tests went 109 → 105. All 4 failures are `test_make_brand_kit.py`
(`test_dry_run_ok_against_clean_snapshot`, `test_real_run_produces_zip_with_expected_members`,
`test_typescales_omitted_when_no_constants_given`, `test_output_refused_inside_uploads_dir` —
the last is collateral: it asserts on a specific refusal message and gets an earlier refusal).

Root cause, stated in the script's own docstring ("WHY SOME FKS ARE UNCHECKABLE TODAY"): its
self-check treats *"declared in manifest but file does not exist"*, and any FK failure naming
such a table, as an accepted non-blocking gap. **Every other problem blocks emission.** Those
tables now exist, so the exemption stops applying and the 37 bucket-B lines become hard
refusals. Two distinct breaks:

1. **Base bucket-B lines now refuse every brand kit.** B4's `safe-sans-deck` alone is enough.
   Fixing B1–B4 fixes this.
2. **`data/brand/ens/typefaces.csv:2:Scale Key: 'ens-print'` does not resolve.** This one is
   *caused by* the correct decision above: `ens-print` is properly out of `data/base/`, so the
   brand kit must supply it — but `make_brand_kit.py` only emits a `type-scales.csv` when the
   brand.md gives explicit `type-scale <role>:` lines, while emitting `Scale Key=ens-print` on
   the typefaces row **unconditionally**. That is a latent bug the missing table was hiding.
   Fix belongs in `make_brand_kit.py`, not in the loader.

Also stale and now wrong: `REASONING_KEY_HINT` writes a plausible `Reasoning Key`
(e.g. `office-document`) on emitted brand doctype rows. It is **not** among the 15 real
`doc_category` values. It did not surface in the failures above only because earlier refusals
short-circuit; it will surface as soon as they are fixed.

**Step 5 (ENS kit ZIP) is blocked on B1–B4 plus these two `make_brand_kit.py` fixes.**

## OPEN GAPS carried forward (still open, still not mine)

1. `reference_columns` fails silently by design — an unmatched `Threshold` is treated as a
   literal with no error. Pattern deliberately tight-left/generous-right; both halves proven
   by a negative probe. Re-probe if the pattern changes.
2. `skill/dist/…-0.0.1-dev.zip` ships the **Rev 2** manifest. Stale.
3. RESUME flag (a): `ens-manrope-inter`'s Scale Key resolves only to the print-medium
   `ens-print`, so ENS slides still have no projection-medium sizes. T5 authoring.
4. RESUME flag (c): T9 lacks `field-legibility-min`, which `if_hand_filled` points at on two
   T2 rows (`form-handfilled`, `ens-formulaire`). Deliberately wired to the proposed name so
   it flags as unreachable rather than being silently dropped.
5. `rationale/cv-regions.md` and `rationale/headings.md` promised by the loader's CHANGES
   strings since load pass 1, never written. Now that `data/rationale/` exists, cheap.
6. `doc-styles.Checklist` — the step-1 briefing note has **expired cleanly**. T3 is authored
   and the draft honours the declared list shape (short imperative items, `;`-separated). No
   action; recorded so nobody re-opens it.
7. The gate has no required/non-null check for non-FK columns. Found via B1's empty
   `Measure mm`; likely not the only instance. A sweep of every non-`nullable` column against
   its loaded data is a real coverage task nobody has run.

## NOT STARTED
Step 4 (mechanism: `resolve.py` against real data) is unblocked by this pass — the entry
table `doctypes.csv` now exists. Note it will resolve into the B1 hole on `Page Format Key`.

## Coverage checkpoint 2026-09-09 — findings note #01a084e4 (stopped mid-polish)
- DELIVERED: `research/34-untyped-figures-and-blank-fks.md`. NOTE THE NAME — the brief asked
  for `34-gate-invisible-gaps.md`; I did not rename after the lead verified it on disk. Same file.
- Reproducibility script: `research/tmp-sweep/note34.py` (read-only, run from repo root).
  It re-derives every count in the note: the 7 undeclared figures columns, their manifest
  facets, the Accessibility Grade distribution, both doctypes blank-FK sets, and the 4 list FKs.
- INTEGRITY: manifest md5 `0b4a079fbbfd2678cc463a78648dbe86`, gate 82, `data/base/` untouched.
  Gate probes ran on a throwaway copy under Temp, deleted. Only edit outside the note: a 3-line
  SUPERSEDED pointer on `33`'s ranked item 2 (disclosed to the sub-manager).
- MUST-READ before acting: §0. `infographic`'s blanks in BOTH `Structure Key` and
  `Constraint Set Keys` are DELIBERATE (`26-notes.md:222-225`). `33` item 2 is withdrawn.
  4 rows genuinely open, not 6. Also: 5 FKs are nullable and ALL FIVE are `R` — so "R and
  nullable" is already this schema's own established combination, which is the argument for
  exporting `nullable` into the manifest before adding a non-null check.
- UNFINISHED (3 brief items, none blocking): per-column data-shape examples in §1.6; the
  4-step closing ordering the sub-manager dictated ("" enum members -> nullable-label fixes ->
  export nullable -> non-null check); a pointer to `note34.py` inside the note itself.

---

# Load pass 3 — DONE and self-verified, 2026-09-09 (task #01a084f1)

Supersedes every count above. `data/base/` is **13 of 14 tables, 274 rows**; only
`structures.csv` is unauthored.

## Gate: 82 → 31. Bucketed.

| n | line class | verdict |
|---|---|---|
| 29 | `doctypes.Structure Key` → `structures.structure_key` | expected; clears at step 6 |
| 1 | `structures.csv` declared in manifest, file does not exist | expected; same |
| 1 | `palettes.csv:2:On Accent: cannot compute contrast: invalid hex color ''` | **NEW — see below** |

**All 37 bucket-B lines cleared, every one.** 28 `Page Format Key` (B1 — T7 is 11 → 22 rows),
7 CV-region `Constraint Set Keys` (B2), 1 `png-chromium` (B3), 1 `safe-sans-deck` (B4). All
14 `Palette Key` lines cleared with T4 loaded, and `palettes.csv`'s missing-file line with
them. Predicted remainder was 30 (29 + 1); actual is 31, and the extra one is new.

**Regression tripwires from the earlier note: all clear.** Not 17 (T7 normalisation did not
regress — 22 rows, header verbatim). No brand row in base. No `Threshold` line at all.

## The one new line, and why I did not "fix" it

`mono-ink` ships `Accent` and `On Accent` **blank, deliberately**: `32-notes.md:41` records
that the row is `09-library-schema.md:734-748`'s own generic worked example verbatim, and
that example shows `—` for both ("monochrome has no brand colour to mark categories with").
The gate's `contrast_at_least` derived check calls `color.contrast_ratio("", "")` and reports
`cannot compute contrast`. **The brief's "all 25 On-X contrast pairs >= 4.5:1" is 24 — the
author's own table in `32-notes.md:31` prints `—` in that cell.** Nothing is wrong with the
data.

This is the same asymmetry note `34` §2.1 found in the FK checker, one check over: a blank
foreign key is skipped silently, a blank contrast pair is a hard error, and neither is
*declared*. **Recommended ruling: skip a derived contrast rule when BOTH `column` and
`against_column` are empty** — an absent role, not a broken pair — and keep the error when
exactly one is filled, which is a genuinely half-authored pair. That is narrow and it is a
gate change, so it is a ruling, not mine to take unilaterally. The alternative, inventing an
`Accent` for `mono-ink`, contradicts the schema's own example and is worse.

**It does NOT block `make_brand_kit.py`** — checked, not assumed. `make_brand_kit.py` was
repaired while I was out and its self-check now scopes "real" problems to lines whose `file:`
prefix names a file **this run wrote** (`make_brand_kit.py:665`); every base-only line,
including this one and all 30 `structures` lines, is classified expected.
`make_brand_kit.py examples/ens-brand.md --dry-run` reports **DRY-RUN OK** and all 16
`test_make_brand_kit.py` tests pass. The step-5 BLOCKER recorded in the load-pass-2 section
above is therefore **closed** — both halves of it, since `data/brand/ens/typefaces.csv`'s
`ens-print` Scale Key no longer surfaces either.

## The four ruled items — all four done

1. **All four FK list columns are declared** (`doctypes.Render Target Keys`,
   `doctypes.Constraint Set Keys`, `structures.Section Order`, `cv-regions.Section Order`).
   Fixed at the origin in `research/build-manifest.py`, and its guard is **inverted**: the old
   `assert col not in t["foreign_keys"]` is now "every `list: true` FK must appear in
   `list_columns`", so the next list FK cannot be added without one. `list_columns` 8 → 12.
   Zero new gate lines — all four columns are well-formed on the loaded data (checked before
   declaring). `validate_data.py`'s MANIFEST FORMAT comment said "non-FK" in two places and
   would otherwise have contradicted the manifest; corrected.
2. **`figures.{Data Type, Keywords, Best Chart Type}` typed `text`/`S`** in
   `09-library-schema.md`, with the `resolve.py:240` / `searchable_columns` argument stated.
3. **`figures.Accessibility Grade` is an enum**, `high|medium|low-medium`. `tabular-lookup`'s
   96-char sentence is moved by the **loader** (never the draft) into `Accessibility Notes`,
   joined `; `, per the `Caption Required` precedent. The split is recorded in
   `research/26-t11-caption-qualifications.md`, which the loader writes.
   **Three `figures` columns remain untyped, not four** — `Accessibility Grade` left that set
   by being ruled. `When to Use`, `A11y Fallback`, `Accessibility Notes` are **deliberately
   left**, and §9 says why: the legend's "`P` applies to exactly seven columns" and §8 item
   11's whole argument ("an **eighth** `P` column is evidence the schema is losing
   enforcement") are counted prose. Three at once is a rewrite of that entry, not an
   increment. The argument they need is already written down in §9 for whoever takes it.
4. **`research/26` loaded fresh from disk** — B2's `ats-strict;cv-region` on all 7 regional
   rows and the DDR's `print-legibility` on `letter-formal` / `slide-deck-handout` are in.
   `print-legibility` is a real `Set Key` in `constraints.csv`; it produced no gate line.

**Bonus for note 34 §2.4:** `slide-deck-handout` now carries `print-legibility` while
`slide-deck-document` carries `screen`. The two deck rows previously differed only by a
blank. They now differ on real values, so the `if_projected` escape hatch is **stronger**
than §2.4 measured it, not closed.

## The two promised rationale files are written

`data/rationale/cv-regions.md` (14 entries; also records *which* authored seniority band each
collapsed row was taken from, without which the citation cannot be traced) and
`data/rationale/headings.md` (81 rows grouped by citation over 16 distinct sources — 59 carry
the identical `convention (not in report 03)`, which is the shape of the evidence and is
invisible in a per-row list). Both loader-written from the drafts' `source` columns per Rule
2. The loader's CHANGES strings have promised them since load pass 1; that promise is no
longer an untruth.

## Verified

- **Gate 31**, bucketed above.
- **Tests: 119 passed + 8 subtests, 0 failed.** Was 105 + 8 with 4 failures. The 4
  `test_make_brand_kit.py` failures are **gone** — that script was repaired while I was out —
  and 10 tests were added. Nothing in `test_resolve.py` / `test_preflight.py` /
  `test_ddi.py` failed, so the Mechanism Analyst's in-flight per-key work is green as of this
  run. `test_validate_data.py` green.
- **Loader idempotent** — 13 `data/base/*.csv` + 3 `data/rationale/*.md` byte-identical over
  two consecutive runs.
- **`assert_no_brand_rows()` clean.** 19 brand rows skipped (typefaces 1, doctypes 4,
  doc-reasoning 4, doc-styles 2, type-scales 7, **palettes 1** — `ens-core`, caught by
  `Brand Scope`, the column T4's draft does carry).
- **Manifest md5 `0b4a079fbbfd2678cc463a78648dbe86` → `731d874ff6052d8c3809a3d44a9d4196`.**
  It *must* change this time and that is the point: the two earlier errata were facts about
  the document and proved their scope by being md5-identical; this one adds two real checks.
  14 tables / 174 columns / 13 FKs (5 group) / **12** list columns / 1 reference — only the
  list count and one enum moved. Stale references to the old md5 now exist in `33`, `34`,
  `RESUME.md:57` and this file's earlier sections; `schema-manifest-NOTES.md:455,483` are
  correctly scoped to the *previous* erratum and are still true.

## Still open, still not mine

The `mono-ink` contrast ruling above (cosmetic today, real once someone reads the gate count
as a health number), plus every item under OPEN GAPS that
is not `rationale/cv-regions.md` / `rationale/headings.md` — those two are now closed.

## Two additions after the checkpoint above

- **No unintended table moved.** The six tables this pass had no business touching are
  **md5-identical to their pre-pass values**: typefaces `052be80a`, constraints `ee16f000`,
  font-substitutes `16b17428`, render-targets `a11928ad`, **cv-regions `bee01b6f`**,
  **headings `912eabfc`**. The last two are the ones that mattered — their loader blocks were
  edited to collect `source` for the rationale files, and the match proves that collection
  wrote nothing into the rows. Only `page-formats` (`6abdb0e9` → `02e2fd5b`) and `figures`
  (`c183e0f4` → `7d9b149f`) moved, plus the five tables this pass loaded on purpose.
  Idempotence alone cannot show this; it compares the new loader to itself.
- **`figures.Accessibility Notes` is now named in the "DO NOT declare as a list column"
  comment.** The loader appends `; grade rationale: …` to it, which put a `; ` into a column
  §9 leaves untyped — verbatim the "an undeclared column becomes a list column by accident"
  failure the first erratum's own justification describes. It is a fifth sentence-separator
  column, not a list; named beside the other four in `build-manifest.py` and recorded in §9.
  No manifest byte moved (`731d874f…` before and after), no count moved.
- `RESUME.md:57`'s manifest md5 is marked SUPERSEDED in place — it is the designated
  read-first state file, so a stale hash there is a trap rather than a historical note.
