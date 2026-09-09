# RESUME — Document Design Intelligence (open-source Claude skill)
Written 2026-09-08 by the Workflow Orchestrator after two session-limit incidents.
Purpose: let a FRESH orchestrator (or the user) continue with a small context.
Full history: research/05-SYNTHESIS.md (long). This file is the short version.

## What exists (all on disk, all verified)
- research/00..30 — research, schema (09, Revision 4), authored tables, reviews.
- skill/document-design-intelligence/ — the skill:
  - SKILL.md (825-char description, aligned with Anthropic's built-in docx/pptx skills)
  - scripts/: resolve.py, validate_data.py (manifest-driven gate), preflight.py,
    ddi.py (4-step entry: check/resolve/preflight/handoff), merge_brand_kit.py,
    make_brand_kit.py (brand.md -> kit ZIP), build_zip.py, lib/{data,color,fonts,pdf}.py
  - data/schema-manifest.json (14 tables, 174 cols, 13 FKs) ; data/base/ = 8 of 14
    tables loaded, 190 rows, gate-clean except unauthored tables
  - tests: 109 pass + 8 subtests (run `pytest -q` from the skill dir). Run with WindowsApps python3.exe
    (repo venv python is broken).
- skill/dist/document-design-intelligence-0.0.1-dev.zip — uploaded to claude.ai and
  tested: mounts at /mnt/skills/plugins/<name>, scripts run in-sandbox, activation
  fires, preflight runs. ZIP is STALE (Rev 2 manifest) — rebuild before next upload.
- ENS pilot: PASSED acceptance (3 real deliverables, drift gone).
- LICENSE: Copyright (c) 2026 Magazem. Upstream cited by commit SHA (version field lies).

## Standing rules (do not relitigate)
- Only research/load-base.py writes data/base/. Nobody hand-edits base files.
- Base ships GENERIC rows only. Loader must SKIP Brand Scope != generic (NOT YET DONE).
- ENS rows have one source: examples/ens-brand.md -> make_brand_kit.py -> data/brand/ens/.
- Threshold reference form: <manifest-table-name>:<Column Name> (cv-regions:Max Pages).
- Condition vocabulary = 4 keys; if_projected DELETED; deck-generic is ONE Reasoning Key
  (the DDR's three-key split must be reverted in research/26 and /29).
- Role enum gains `legal`; T12 field-direction has `customary`; T11 has Caption Must State.
- Tier-2 print wording: "PDF/X-4 structurally emitted; conformance not independently
  verifiable with open tooling." Never "validated".
- Sandbox: network is a PyPI-only allowlist; Chromium preinstalled; outputs -> /mnt/user-data/outputs.

## Team operating rules (the session-burn fix)
- ONE deliverable per brief, ~10 minutes. No multi-part briefs.
- At most 2 workers running at once. Others idle.
- Clear a worker's context (team_clear_agent_context) after EVERY task, before the next.
- If a turn passes ~10 min: interrupt with "checkpoint to research/handover-<name>.md
  and stop", then clear, then resume from the note.
- Keep orchestrator messages short; every message enlarges the worker's context.
- Do not let dropped/redelivered messages be re-read — act from disk instead.

## Progress (updated 2026-09-08 by the sub-manager orchestrator)
- STEP 1 DONE + verified on disk: schema Rev 4; gate = 13 problems (6 unauthored tables
  + 7 typefaces.Scale Key); 109 tests + 8 subtests; manifest 14 tables / 8 list cols /
  1 reference col; data/base/README.md; grep ",ens," data/base/*.csv EMPTY; the T#:
  threshold form (FIVE shipped rows, not one) normalised by a map in load-base.py write().
  Gate diagnostics: 17 = T7 normalisation regressed; 14 = a brand row is back in base/;
  15 = a Threshold names a missing table/column.
- STEP 2 DONE + verified: 26 back to deck-generic (34 rows); 29 = 19 rows x 12 cols;
  research/30-t6-type-scales-draft.csv = 22 rows x 6 cols, all 8 scale_keys, zero dangling.
- STEP 2b DONE + verified: ens-slides now carries `projection` in its T1 Constraint Set
  Keys and a blank Doc Conditions; 29's condition vocabulary is exactly the 4 ruled keys;
  29-notes.md written; research/18 = 28 rows x 14 cols, csv-clean.
- STEP 3a DONE + verified: six columns typed `text` (only ONE was actually typed
  "text list"; three had no type row at all). Manifest md5 0b4a079fbbfd2678cc463a78648dbe86 (SUPERSEDED at load pass 3 -> 731d874ff6052d8c3809a3d44a9d4196: +4 list-FK declarations, +figures.Accessibility Grade enum; see 09 S9 and handover-coverage.md)
  UNCHANGED -- a retype is schema-doc only; data/base byte-identical; gate 13; 109 tests.
  Rev 2's Rule 4 claim about T11 Anti-Patterns disproved and rewritten; 05-SYNTHESIS
  annotated SUPERSEDED. New legend letter `P` (prose payload) ACCEPTED by ruling; the letter follows whether a
  script actually reads the column, so T11.Caption Must State becomes P unless preflight
  reads it (check, then set).
- STEP 6 DONE + verified (drafts only, not yet loaded): research/31-t3-doc-styles-draft.csv
  12x15 and research/32-t4-palettes-draft.csv 5x20, both headers exact, both key sets 1:1
  with T2, T4's 25 On-X pairs all >=4.5:1 re-checked with lib.color.contrast_ratio.
  Latent flag: print-neutral Primary L*~15.8 vs T4's l_star_max=15 photocopy floor
  (not reachable by if_photocopied today).
- SKILL.md DESCRIPTION CHANGED BY ONE WORD 2026-09-09 (ruled): "Applies validated ... rules"
  -> "Applies sourced ... rules". Much of the library is sourced convention, not validated
  rule, and the description is the first sentence a user sees. Recorded here so that if
  activation regresses after the ZIP rebuild, the cause is known and the revert is one word.
  Activation triggers are the document nouns, not this adjective; the user's 13-prompt run
  is the test. Keep the description under 1024 chars.
- RESOLVER, post-abstain (2026-09-09): stopword filtering + RELATIVE margin abstain
  (floor=0.0, ratio=0.15, derived in research/35-notes.md). "make me a flyer" abstains with
  the two real flyer rows as candidates. 126 tests + 8 subtests.
  KNOWN, not fixed: (i) D3 "erstelle eine praesentation" does not abstain -- its margin ratio
  0.315 EXCEEDS D1's 0.249 and D1 must stay resolved, so no threshold separates them; the
  cause is data (slide-deck-projection repeats "presentation" in 3 scripts, tf=4 vs 2/1).
  One-line fix in research/26 + reload, not an algorithm change.
  (ii) a query scoring ZERO everywhere still prints "top candidates" and lists arbitrary
  0.0-scoring rows; it should say "no match" instead.
  (iii) BM25's tokenizer splits on any non-[a-z0-9] char, so accented words fragment
  (fuer -> f,r). Symmetric on query and keywords so matching still works, but it is why the
  German and French forms of "presentation" collapse together. Relevant to step 9/10.
- *** GATE ZERO, 2026-09-09 *** load pass 4 landed: "OK: validated 14 table(s), 291 row(s)".
  All 14 tables loaded, structures included. Contrast both-empty rule in (one function,
  3 tests). Blank-handling asymmetry now DECLARED in the schema and in validate_data's
  docstring, with a standing rule that any future derived check declares its blank behaviour
  before shipping. Manifest md5 731d874f unchanged; loader idempotent.
- THREE GAPS open after gate zero (detail in research/handover-coverage.md):
  (a) make_brand_kit.py still emits a blank Structure Key justified by "structures.csv does
      not exist yet", which is now FALSE -- a regenerated ENS kit ships doctypes with no
      structure. schema-manifest-NOTES.md repeats the stale claim.
  (b) the contrast error line anchors to the rule's `column`, so a blank against_column
      points the author at the cell they got RIGHT.
  (c) RULED: FIX THE EXAMPLE, no `?` marker. The schema's Section Order example
      `contact;summary?;...` would fail the validator; optional sections, if ever wanted,
      get a schema revision first rather than a late-invented marker.
  Owners: (a) Packaging at step 7b -- the regenerated ENS kit's Structure Key must reference
  real structures keys. (b) Coverage, small, not urgent. (c) whoever edits 09 next.
  ASCII rule stands: German stopwords go in as \x escapes, or the normaliser strips
  diacritics before matching -- Mechanism's choice, documented in research/35-notes.md.
- LOAD PASS 3 DONE + verified 2026-09-09: base = 13 of 14 tables, 274 rows (only structures
  left, its draft is research/36). GATE 82 -> 31 = 29 doctypes.Structure Key + 1 structures
  missing-file + 1 NEW blank-contrast line. Tests 119 + 8 subtests, zero failures. All four
  FK list columns declared and build-manifest.py's guard INVERTED so a list FK cannot be
  added without one (8 -> 12 list columns). Manifest md5 is now 731d874f -- it MUST move,
  this erratum added two real checks. rationale/cv-regions.md and headings.md written.
- RULED (blank contrast): skip a derived contrast rule only when BOTH cells are empty; keep
  the error when exactly one is. mono-ink ships Accent/On Accent blank deliberately (09:734-748's
  own worked example). Owner: Coverage, next brief.
- (superseded) STEP 3 DONE + verified: data/base = 12 of 14 tables, 259 rows (doctypes 30,
  doc-reasoning 15, doc-styles 10, type-scales 15); data/rationale/doc-reasoning.md written
  (T2's draft-only Reasoning/Confidence stripped there); manifest md5 unchanged;
  figures.Caption Must State retyped V -> P (nothing under scripts/ reads it).
  GATE 82 = 45 expected (29 Structure Key, 14 Palette Key, 2 missing files; clear at step 6)
  + 37 REAL: 28 Page Format Key (B1), 7 CV-region Set Keys (B2), png-chromium (B3),
  safe-sans-deck (B4). Tests 105 pass / 4 FAIL, all test_make_brand_kit.py.
- SUPERSEDED CHECK: `grep ",ens," data/base/*.csv` was BROKEN — it only matched a whole
  field equal to `ens`, so it never saw doc_category=ens-slides or scale_key=ens-print.
  The loader's assert_no_brand_rows() enforces this now. Do not use the grep again.
- STEP 5 UNBLOCKED 2026-09-09 + verified: make_brand_kit.py's self-check now blocks only on
  problems under the run's own data/brand/<slug>/; pre-existing base defects print as NOTEs
  naming their base file. Scale Key blank unless type-scale lines given; reasoning hints
  mapped to real doc_categories (social left blank + NOTE). Suite back to 109 + 8 subtests;
  a real ens-brand-kit.zip builds against live data/base.
- B1/B1b/B2/B3/B4 ALL DONE + verified (drafts): T7 is 22x21 with Measure mm and the four
  Margin mm columns filled on every row; the 7 regional CV rows carry `ats-strict;cv-region`;
  png-chromium -> png-social; deck-generic's Typeface Key -> safe-sans-arial.
- RULED 2026-09-09 (resolve.py / preflight / ddi.py check): PER-KEY DEGRADATION, two tiers.
  Tier 1, still a hard refusal: structural problems -- missing files, manifest/header
  mismatch, malformed CSV, duplicate keys. Tier 2, refuse only the paths that touch the
  broken key: dangling FK, bad enum, bad threshold, blank non-nullable. The whole-dataset
  gate summary prints as a warning header and every refused path is named in the output.
  WHY: resolve.py today validates the whole dataset before stage 1, so with the gate at 82
  all 12 test queries refused identically and nothing reached search or the FK walk -- one
  unauthored table makes the entire skill unusable, and structures is scheduled last.
- NEXT, in order: B2/B3/B4 one-line draft fixes -> load pass 3 (T4 palettes + reloaded T7)
  -> step 4 Mechanism -> step 5 ENS kit + merge -> T10 structures -> step 7 SKILL.md + ZIP
  -> step 8 tag v0.1.0. Non-null gate check lands FOURTH in the sweep's own sequence.
- RULED (B1, AMENDED 2026-09-09): T7 page-formats gains the 11 document-use rows AND
  populates `Measure mm` AND the four `Margin Top/Bottom/Inside/Outside mm` columns on all
  rows -- all five are non-nullable V columns that were 100% empty; the schema gives the
  four margins ONE shared type row (09:1058), which is why only Measure was first seen; T1's keys STAY. T7 currently ships 11 print-professional rows
  only, zero office/photocopy, and the schema's own examples (a4-cv-single-col,
  letter-trifold) are not in it. widescreen-16-9, px-infographic-portrait and a3-poster are
  missing outright.
- RULED (B2): T1's 7 regional CV rows carry `ats-strict;cv-region`; Region Key does the
  regional selection (it already resolves on all 7). B3: png-chromium -> png-social.
  B4: safe-sans-deck -> pick safe-sans-arial or ofl-source-sans-serif, one line of judgement.
- NEW GAP: the gate has no required/non-null check for non-FK columns (found via T7's empty
  Measure mm). A sweep of every non-nullable column against loaded data is unrun.
- Also unwritten since pass 1: data/rationale/cv-regions.md and headings.md.
  NOTE for T3/T4 authors: doc-styles.Checklist is a DECLARED list column -- short
  imperative items separated by ";", never prose.
- NEW OPEN FLAGS (not fixed): (a) ens-manrope-inter's Scale Key resolves only to the
  print-medium ens-print, so ENS slides still have no projection-medium sizes -- T5
  authoring; (b) T1's per-region CV Set Keys (us-cv-region etc.) match no Set Key in
  constraints.csv, and only work today via the doctype:cv-* attach pattern; (c) T9 lacks
  the `field-legibility-min` constraint that if_hand_filled points at.
- RULED 2026-09-08: figures.{Anti-Patterns, Secondary Options, Static Fallback, When NOT
  to Use, Data Volume Threshold} and cv-regions.Language Expectation are RETYPED "text list"
  -> "text" (cited prose beats tokens); record as a Rev 4 schema erratum. Step 3a.
- NOTE: the `sticky-board` skill is disabled for model invocation; findings go to
  research/handover-*.md instead.

## TWO MANIFEST HASHES -- both correct, do not "fix" either
`data/schema-manifest.json` has TWO valid md5s and they differ only by line endings:
  731d874ff6052d8c3809a3d44a9d4196 = the WORKING COPY on Windows (CRLF, 740 pairs)
  57e886aa8a68665c763904c391ac3836 = the LF form: what git stores (i/lf per .gitattributes)
                                     and what the built ZIP now contains
Since the release blocker fix, build_zip normalises every text member to LF, so the in-ZIP
manifest hashes as 57e886aa. A Linux checkout will show 57e886aa on disk too. Quote the
right one for the context you are checking; a mismatch between them is not a defect.

## VERIFICATION RULE, added 2026-09-09 after a release blocker
"Opened and checked the ZIP" MUST include the FIRST BYTES of SKILL.md and a CR-byte scan of
every text member. The 7b/step-8 archive checks passed on member list, manifest md5, brand
exclusion and description text -- and the ZIP was still rejected by claude.ai, because
SKILL.md began with the build stamp instead of `---` and 9 members carried CRLF. Checking
that a file is PRESENT is not checking that it is VALID.

## ACTIVATION TEST, run 2026-09-09 by the user on the rebuilt ZIP -- prompts 1-5 only
Result 1 pass, 4 fail. The tag is BLOCKED until the revised prompts are re-run.

| # | Prompt intent | Outcome | Reading |
|---|---|---|---|
| 1 | CV, marketing coordinator | PASS | asked about format, produced an ATS-friendly French CV |
| 2 | "une fiche" (FR) | FAIL | Claude asked what the user wanted first; "fiche" alone is genuinely ambiguous in French |
| 3 | "Angebot" (DE) | FAIL (test defect) | Claude asked for client details, then said it would "likely use document-design-intelligence" once given them -- the description DID match |
| 4 | "this report" | FAIL (test defect) | asked the user to upload the file; nothing was attached |
| 5 | "this text" | FAIL (test defect) | asked for the text; nothing was attached |

The lead's reading, adopted: 3-5 are a TEST defect, not a description defect. The prompts say
"this report" / "this text" / "diesen Kunden" with nothing attached, so a generalist
clarification is the correct behaviour and proves nothing either way. #3 is positive evidence
the description matches. #2 is partly genuine.

RULINGS 2026-09-09 (lead):
A. Revise activation.md prompts 2-5 so each carries its input INLINE. #2 -> French-only with a
   concrete fiche type (e.g. "fiche produit"), still no English document word. #3 -> 2-3 lines of
   client/offer facts in German. #4 -> a short pasted "AI-looking" report paragraph. #5 -> a short
   pasted text. Pass/fail lines stay honest: "asks a clarifying question" is a PASS only if the
   question shows document-design framing (format, layout, ATS, brand); a generic "what do you
   want" is a FAIL. Mirror in skill/dist/POST-UPLOAD-TESTS.md Test (c) and TESTS-FOR-USER.md.
B. DO NOT change the description yet. Draft ONE candidate sentence in research/ (not in
   SKILL.md) telling Claude to invoke the skill before asking for missing content. Applied only
   if the re-run of the revised prompts still fails. The user vetoes description changes.
C. Commit the uncommitted SKILL.md diff. NEW RULE: the build stamp must never precede `---` in
   the SOURCE file either, not just in the built ZIP. The committed source carried the same
   defect that was fixed in build_zip.py; the source is now stamp-after-frontmatter.
D. Rebuild the ZIP only after A lands. The user then re-runs 2-5, then 6-13.

NOTE: skill/dist/ is gitignored (.gitignore line 12). Edits to
skill/dist/POST-UPLOAD-TESTS.md live on disk only and are NOT under version control.

## PRECEDENT, 2026-09-09: refusing the green tick
The Coverage analyst had a one-constant change in hand that would have turned all four
resolver acceptance bullets green (any margin ratio in (0.1862, 0.2492]). It refused, on the
grounds that a 0.063-wide window fitted to two queries is tuning to the test and leaves every
accented term in the library unsearchable either way. The real cause -- BM25.tokenize
splitting on [^a-z0-9]+ -- was fixed instead. When a passing number and a working product
disagree, this project fixes the product. Cite this the next time a threshold is tempting.

## STEP 9 BACKLOG (all AFTER v0.1.0)
- BM25 LENGTH NORMALISATION: after diacritic folding, D3's three deck rows TIE on score and
  projection wins only because its row is 18 tokens against its siblings' 34 (b=0.75).
  Do NOT just lower b -- that is the same tuning-to-the-test trap in a different variable
  (see "refusing the green tick" above). Shipped as a stated limitation in RELEASE-NOTES.md.
- `brochure-flyer-a4` has a duplicate Keywords token ("flyer a4" listed twice). Found while
  fixing the deck rows; left alone deliberately so the D3 brief stayed one deliverable.
  Worth a sweep for duplicate tokens across all 34 T1 rows, not just this one.
- The contrast error line anchors to the rule's own `column`, so a blank `against_column`
  points the author at the cell they got RIGHT. (Coverage, small.)
- The schema's Section Order example `contact;summary?;...` must be FIXED (no `?` marker).
- BM25 tokenizer splits on any non-[a-z0-9] char, so accented words fragment; that is why
  the German and French forms of "presentation" collapse together.
- (RESOLVED 2026-09-09) Version control is LIVE. Repo at the PROJECT ROOT, initial commit
  0bdb838 (204 files), pushed to https://github.com/Magazem/Smart-design.git.
  release.yml MOVED to ./.github/workflows/ with paths prefixed `skill/` (VERSION write,
  build_zip.py call, dist/ asset). .gitignore excludes upstream-latest/, skill/dist/, caches,
  data/brand/*/ except README and .gitkeep, active.json, .claude/. .gitattributes pins LF so
  the manifest md5 survives a Windows checkout.
  WORKING RULE (ruled 2026-09-09): THE ORCHESTRATOR COMMITS, NOT THE WORKERS. Workers do
  not touch git at all. The orchestrator already verifies every milestone on disk, so the
  commit is the last step of that verification, and a single committer removes the risk of
  one worker's `git add` sweeping up another's half-finished edits. Path-scoped
  `git add <paths>` only, NEVER -A; the commit message names the task.
  Nobody pushes. Tag and push are the lead's, after the user confirms.
  Step 8 = final ZIP check, commit the remainder, hand the tag command over.

## STEP 9, ruled 2026-09-09 (AFTER v0.1.0): headings for the other 14 doc classes
`structures.Section Order` is a list FK into `headings.canonical_section`. `headings.csv`
has 81 rows but only ELEVEN distinct canonical_section values, all CV sections:
certifications, contact, education, experience, languages, projects, publications,
references, skills, summary, volunteering. Nothing exists for letters, memos, invoices,
reports, decks, posters or brochures, so of T10's 17 generic rows only the two CV ones and
arguably cover-letter-standard can be authored honestly. T10 therefore ships with
Section Order EMPTY on most rows -- deliberately, with the missing values listed in
research/36-notes.md. Authoring them is a full table of research and waits until after the
first release, which already has honest value for CVs and cover letters.
TWO CONDITIONS so the gap is visible rather than silent:
  1. resolve.py must say "no section-order guidance for <doctype>" when Section Order is
     empty. It must never present an empty list as an answer. (Mechanism, per-key/handoff.)
  2. SKILL.md and README (step 7) must list which doctypes carry structure guidance.

## Critical path, in order (each is one small brief)
1. Coverage: loader skips brand rows + data/base/README ("only the loader writes here")
   + Threshold form fix (schema §0.1 + shipped constraints row) + `legal` in Role enum
   + declare list_columns/reference_columns + regenerate + gate; grep ",ens," base == empty.
2. DDR: revert deck split in 26/29; author research/30 T6 with ALL of: cv-print,
   form-print, report-print, report-screen, report-technical, ens-print, deck-projection,
   print-office-generic (17-25 rows); write 29-notes; fix research/18's two malformed rows.
3. Coverage: load pass 2 (T1 26, T2 29, T6 30) -> gate: only doc-styles/palettes/
   structures should remain unauthored; decide T2 Reasoning/Confidence disposition.
4. Mechanism: resolve.py against real data + the 12-query test from research/26-notes;
   then the pending handoff-vocabulary task (docx-js DXA/half-points, pptxgenjs hex/LAYOUT).
5. Packaging: produce ENS kit ZIP, merge against dev ZIP, gate outputs; build_zip excludes
   data/brand/*/; merge_brand_kit fallback finds skill by SKILL.md name, not folder;
   README "give it your brand" one-file flow.
6. DDR or Coverage: T3 doc-styles (~20) and T4 palettes (~10 generic) from the keys
   research/29 references; T10 structures last (least confident table).
7. Packaging: SKILL.md body prose (thin router; quote ddi.py's 4-step text; render
   handoff to built-in docx/pptx; tier wording); rebuild ZIP; user re-uploads and runs
   the 13-prompt activation list + one end-to-end document.
8. First release: tag v0.1.0 -> release.yml builds the asset.

## Handover notes from the last checkpoint
research/handover-coverage.md, research/handover-ddr.md, research/handover-packaging.md
(each <=50 lines; read the one for the worker you are resuming).

## Teammates (slot ids) and what to do with them
- Coverage and Gap Analyst  01a07ade-8092-7ee0-9b55-768db8e39586  (Opus) — keep; clear; step 1
- Document Design Researcher 01a07ade-92a9-7bb3-98aa-8285eb3c6176 (Sonnet) — keep; clear; step 2
- Mechanism Analyst         01a07ade-7e18-76c3-8fdc-a17bcc956541  (Sonnet) — keep; clear; step 4
- Packaging Analyst         01a07ade-92de-7d22-a88a-f878d878610a  (Sonnet) — keep; clear; step 5
- Print Production Specialist 01a07b9d-086a-7851-8272-9275344e264d — domain exhausted; shut down
- AionUi Butler             01a07a84-e27e-7b92-80e1-ad082022257e — idle; keep

## LEAD RESUME — for a fresh Workflow Orchestrator LEAD context (read this first)
You are the team LEAD. Your context was cleared on purpose. Do NOT rebuild history.
- The execution loop is run by a SUB-MANAGER teammate: "Workflow Orchestrator",
  slot 01a080c5-2001-78b3-bbbe-afaae15edafa. It creates tasks, briefs workers, verifies
  deliverables, and reports milestones to you (<=10 lines).
- YOUR job is thin: (1) when the sub-manager messages "CLEAR <slot_id>", call
  team_clear_agent_context on that slot and reply "cleared"; (2) shutdowns and spawns
  (lead-only); (3) decisions the sub-manager escalates; (4) relay milestones to the user
  in a few sentences. Do not read long worker reports; the sub-manager does.
- Print Production Specialist was SHUT DOWN 2026-09-08 (scope complete).
- Standing rules and the critical path are above in this file. Rulings live in
  research/05-SYNTHESIS.md (long; consult only for a specific question).
- If the sub-manager goes quiet for >30 min, message it "status?" — nothing more.
