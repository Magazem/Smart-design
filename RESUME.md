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

## ACTIVATION RERUN, 2026-09-09, on the ZIP rebuilt after ruling E
Prompts 2, 3 and 5 PASS. Prompt 4 FAIL. The inline-content fix worked, so candidate B (the
"activate before asking for missing content" sentence) stays UNAPPLIED.

Prompt 4 failed for a real reason, and it is a SCOPE finding, not a bug. Claude said the pasted
paragraph "is not a document, just text", then searched the skill for rules about correcting
AI-sounding writing and found none. That is correct. data/base was checked by the lead and again
by me: every table is layout, typography, colour, print or ATS. The word "prose" appears only as
a use-case descriptor in doc-styles.csv and typefaces.csv, never as prose-quality guidance.

**THE SKILL FIXES HOW A DOCUMENT LOOKS, NOT HOW ITS PROSE READS.** AI-sounding wording is out of
scope for v0.1.0. The description's "looks like AI / looks generic" trigger is a promise about
APPEARANCE. Prompt 4 as originally written tested a promise the skill never made.

RULING F (lead):
1. Prompt 4 is rewritten so the complaint describes the document's APPEARANCE inline -- centred
   bold headings in mixed fonts, 10pt body, 1cm margins, three bullet colours, clip-art chart.
   Pass = fires and reasons about hierarchy/typography/margins/colour, or asks a design-framed
   question. Fail = generic advice, or asks for the file.
2. A one-line scope note goes in activation.md after the "Length: 823 characters" paragraph and
   in RELEASE-NOTES.md under "## Known limitation".
3. A second description candidate ("Candidate F") is DRAFTED in research/38-description-candidate.md
   making the quality-fix trigger honest about layout. NOT applied. The user vetoes description
   changes.
4. The change mirrors to TESTS-FOR-USER.md Test 11 and the dist test doc.

BINDING NOTE for whoever edits activation.md: the fenced block under "## The description as
shipped" is byte-identical to SKILL.md's description and must stay that way. The "Alternate A"
and "Alternate B" blocks further down are retained-for-reference history -- do not update them
to match current wording.

## ACTIVATION RUN, prompts 6-13, on the ruling F ZIP
6 PASS, 7 PASS, 8 PASS, 9 PASS, 10 PASS, 11 PASS, 13 PASS. Prompt 4 not yet re-reported.
Prompt 12 INCONCLUSIVE, and that is a test defect of the same family as the others.

Prompt 12 observation: given "I need a two-page CV, make it look professional", Claude asked for
CV details with no skill triggered. The user said to use placeholders, and a CV was then
produced. Whether the skill fired at creation time is unknown, so the prompt measured nothing.
Same ask-before-invoke pattern that made old prompts 3-5 unreadable.

RULING G (lead): prompt 12 gets inline CV content -- a named person, two employers with years,
a degree, languages and tools -- while KEEPING the design intent ("two-page", "make it look
professional") and naming NO file format. Naming a format would turn it into prompt 11 and
destroy what prompt 12 tests, which is that this skill fires and renders through the docx
handoff without docx becoming the top-level responder. Pass/Fail intent unchanged. Mirrors to
TESTS-FOR-USER.md Test 11 and the dist test doc.

Candidate F remains ON HOLD pending the user's veto decision. Do not apply it.

## ACTIVATION RUN, prompt 12 and prompt 4, on the ruling G ZIP
Prompt 12 PASS -- the skill fired on the inline CV, so ruling G worked and the handoff test is
now readable. Prompt 4 FAIL again, on the appearance-described text.

RULING H (lead): describing an ugly document in words is not the same as handing Claude one.
Prompt 4 becomes an ATTACHMENT test, the same shape as prompt 13.
- A deliberately badly formatted sample report is built as a TRACKED fixture at
  research/fixtures/badly-formatted-report.docx, with its generator at
  research/fixtures/make_bad_report.py. It is NOT shipped.
- Why that path is safe: build_zip.py's collect_members() walks only SKILL_DIR
  (skill/document-design-intelligence), so anything under research/ is structurally impossible
  to include. This is a stronger guarantee than an exclusion rule and should not be traded for
  one.
- Prompt 4 becomes an attach instruction plus the unchanged quote "This report looks like it
  was thrown together by AI, can you fix it?" Asking for the file is now an explicit FAIL,
  because the file is attached.
- The rebuild asserts no .docx member exists in the archive.

CANDIDATE F: **APPROVED BY THE USER** (2026-09-09). Apply after ruling H lands, in its OWN
commit. The 8-character edit exactly as drafted in research/38-description-candidate.md:
  "quality fixes: looks like AI, looks generic, make it professional, fix the layout"
  -> "appearance fixes: looks like AI, looks generic, make it look professional, fix the layout"
Four things move together or the build breaks:
1. SKILL.md description -> must measure 831.
2. The fenced "as shipped" block in references/activation.md -> must stay byte-identical to it.
3. The "823-character" prose in activation.md -> 831.
4. The DESCRIPTION LENGTH section below -> 831, headroom 192.
Because F NARROWS the trigger, no should-not-fire prompts need re-running. The user re-uploads
and runs prompt 4 only. If 4 passes, the tag is next and is the user's call.

Prompt 4 detail confirming ruling H: Claude asked for the file. The appearance description in
words was not enough; it wanted the document.

## ACTIVATION TEST COMPLETE, 2026-09-09 -- ALL 13 PROMPTS PASS
Prompt 4 PASS on the attached fixture: the skill fired and produced a corrected document. That
was the last outstanding prompt. The full 13-prompt activation list now passes on the release
candidate with candidate F applied.

What made it pass, in order: giving prompts 2-5 their input inline (ruling A), giving 6, 8, 10,
11, 13 theirs (ruling E), stating that the skill fixes appearance and not prose (ruling F),
giving prompt 12 inline CV content (ruling G), and finally attaching a real badly formatted
.docx instead of describing one in words (ruling H). Four of the five original failures were
test defects, not skill defects.

RELEASE STATE: v0.1.0 is ready. Gate 0, 14 tables, 291 rows. 133 tests + 8 subtests. ZIP
verified from its bytes. Nothing pushed, nothing tagged -- the remote still has only the
initial import 0bdb838. Push then tag per research/37-release-checklist.md.

## v0.1.0 IS PUBLISHED -- 2026-09-09
Tag v0.1.0 points at d2885b9. The Release workflow run succeeded in 13s. The asset
document-design-intelligence-0.1.0.zip (135566 bytes) is live at
https://github.com/Magazem/Smart-design/releases/tag/v0.1.0

I downloaded the PUBLISHED asset and verified it, not the local build:
39 members; SKILL.md starts b'---
'; exactly one stamp reading
"<!-- version: 0.1.0 (generated at build - do not edit) -->"; VERSION member reads 0.1.0, so CI
overwrote the 0.0.1-dev tree value from the tag as designed; zero CR bytes; manifest md5
57e886aa8a68665c763904c391ac3836; description 831 chars with "appearance fixes"; zero .docx
members; no brand leak beyond data/brand/README.md; activation.md carries all 13 prompts and the
fixture reference.

The release is DONE. Anything further is step 9 work against a new version.

## THE GATE IS RED ON MAIN RIGHT NOW -- DO NOT PUSH UNTIL THE RELOAD LANDS
State as of commit 9060c77: `validate_data.py data/base` exits 1 with ONE line,
`doctypes.csv:19:Keywords: duplicate token 'flyer a4'`, and `resolve.py --doctype
brochure-flyer-a4` prints [REFUSED PATH]. Every other key resolves; tier 1 is clean.

THE DATA DID NOT CHANGE. The RULE changed, and it is telling the truth about data that shipped
in v0.1.0. The fix exists in research/26-t1-doctypes-draft.csv but has not reached data/base,
because only research/load-base.py may write there and the sweep brief forbade a reload.
The reload brief is dispatched. Local red is acceptable; PUSHING is not, until it lands.

Note for honesty: the PUBLISHED v0.1.0 archive contains the duplicate token. It is not a
correctness bug for users -- a repeated keyword slightly skews BM25 term frequency for one
flyer row -- but the lead has been asked whether to disclose it.

## HOW THE DUPLICATE RULE WAS BUILT, and why not the way I specified
My brief said to iterate `list_columns`. Coverage REFUSED, correctly, and this is the third such
refusal in the project. Two reasons, both verified by me:
- doctypes.Keywords is COMMA-separated. `list_columns` is semicolon-only and the generator
  asserts `delim == ";"`. A rule over list_columns could never have seen the motivating bug.
- page-formats.`Panels mm` IS a semicolon list where repeats are CORRECT: a4-trifold is
  `99.5;99.5;98.0`. A blanket rule would have raised four false positives on right data.
So the check is OPT-IN per column via a new manifest key `distinct_token_columns:
{column: delimiter}`, declared on 12 columns across 8 tables, with Panels mm deliberately exempt.
Scoping a rule to where it is true is not silencing it.

The rule immediately found a SECOND bug no file sweep could see: make_brand_kit.py:590 built
Keywords as `f"{doctype}, {doctype.replace('-',' ')}, {slug}"`, so EVERY single-word doctype
emitted a duplicate into EVERY brand kit ever generated. Fixed with order-preserving
dict.fromkeys. That fix is load-bearing for the suite, which is why it is in the same commit.

## BACKLOG, added 2026-09-09
- make_brand_kit.py lines 498 and 560: the same single-word duplication, live today but ungated
  because Keywords is declared only on doctypes.
- Doc drift: data/schema-manifest-NOTES.md section 1.4 documents every manifest key and does not
  mention `distinct_token_columns`; build-manifest.py's docstring claims the manifest derives
  from research/09-library-schema.md Revision 4, which does not describe it either.
- Heading variants for non-CV families.

## STANDING RULE, ruled 2026-09-09: draft in the loader's shape, verified against the loader
ANY new data draft MUST be authored in the EXACT shape research/load-base.py reads, and the
sub-manager MUST check load-base.py BEFORE writing the brief. Do not infer the shape from
data/base -- the loader renames columns, generates surrogate keys and drops columns on the way
in, so data/base is the OUTPUT shape, not the input shape.

Origin: the A1 and A2 heading drafts were authored against data/base/headings.csv
(heading_key, canonical_section, Heading Text, Language, Is Primary). The loader actually reads
research/18-ats-headings.csv:
    canonical_section,heading_text,language,is_primary,source
It GENERATES heading_key itself as <section>-<lang>-<n>, so the drafts' painstakingly unique
keys are ignored, and it needs a `source` column the drafts did not have. Without it every new
row lands under "(none given)" in data/rationale/headings.md, stripping provenance from 28-plus
sections in a project whose entire discipline is separating sourced from conventional.
Caught before phase B; A2 corrected mid-flight, research/39 retrofitted after.

The same single-source shape applies elsewhere: T10 structures loads only from
research/36-t10-structures-draft.csv.

## GENERATED FILES -- do not hand-edit, change the generator
data/rationale/headings.md, cv-regions.md and doc-reasoning.md are WRITTEN BY load-base.py.
headings.md says so on its own second line. A paragraph typed into any of them is destroyed by
the next load. To change their content, change the write_text block in load-base.py -- for
headings.md that is around line 448.

## PHASE B MUST ALSO DO THESE
1. Put the cross-class reuse rule into the load-base.py generator for rationale/headings.md.
2. Merge the section orders into research/36-t10-structures-draft.csv, the loader's only
   structures source.
3. Rewrite the comment block above the T10 loader (around line 595) which asserts the fifteen
   blanks are correct BY RULING and points at research/36-notes.md.
4. Fix the T13 CHANGES string, which hardcodes "81 rows", and the T10 CHANGES string, which
   says "headings.csv covers CV sections only".
5. Fix the scripts/resolve.py _field_value docstring around line 528, same stale claim.

## STANDING RULE, ruled 2026-09-09: cross-class section reuse
NEVER reuse a canonical_section across document classes when its FR or DE primary Heading Text
reads as a word from the OTHER class. Check the actual Heading Text in all three languages, not
just the English name.

Origin: DDR refused to reuse the CV section `summary` for a proposal's executive summary,
because its French and German primaries are "Profil" -- a CV word that would render a proposal
wrongly. It authored `executive-summary` instead. The lead endorsed this.

The converse also holds: DO reuse when a section genuinely is the same thing in all three
languages. The transactional draft correctly shares `date`, `body` and `closing` across letter,
memo, form and proposal.

## HEADING VARIANTS -- backlog, not a task
The 81 existing CV heading rows carry WORDING VARIANTS, roughly two or three phrasings per
section per language with one marked primary. The new non-CV sections have exactly one row per
section per language.

Lead's ruling after grepping scripts/: NOTHING reads `Is Primary` or the non-primary rows. The
only reference is a resolve.py comment. So variants are model-facing alternatives, not
code-consumed, and one row per section per language is sufficient for v0.2 loading.
Backlog line: "heading variants for non-CV families". No brief now.

## PHASE B MUST FIX THIS COMMENT
scripts/resolve.py, _field_value docstring around line 528, states "headings.csv only holds CV
sections; the rest is deferred". That stops being true the moment the transactional and
long-form rows load. Update it in the same brief that changes the degradation behaviour.

## A FILE THE LEAD NAMED THAT DOES NOT EXIST
The ruling said to write the reuse rule into `rationale/headings.md`. There is no such file, and
references/ contains only activation.md. The rule is recorded above instead. If it should ship
to users rather than live here, the natural home is a new references file written in phase C,
when Packaging documents which doctypes carry structure guidance.

## v0.2 IS OPEN -- scope and the one structural fact that shapes it, 2026-09-09

### CANDIDATE B IS PERMANENTLY ON HOLD. DO NOT REVIVE IT.
The "invoke first, ask later" sentence drafted in research/38-description-candidate.md stays
unapplied until REAL USERS report the skill staying silent when it should have fired. It is not
a pending task, it is a parked option. Its own risk analysis says it endangers the docx deferral
(activation prompt 11). Every failure it was meant to fix turned out to be a test defect. If you
find yourself about to apply it because activation testing looks weak, stop: fix the test.

### THE FACT THAT SHAPES ALL HEADINGS WORK
`Section Order` in T10 structures is a LIST FOREIGN KEY into `headings.canonical_section`
(schema-manifest: "group": true, "list": true). validate_data.py splits the cell on ";" and
validates EVERY token. I read the code path at scripts/validate_data.py around line 236 to
confirm it splits rather than validating the joined string.

headings.csv has 81 rows covering exactly 11 canonical sections, and ALL ELEVEN ARE CV-ONLY:
certifications, contact, education, experience, languages, projects, publications, references,
skills, summary, volunteering.

CONSEQUENCE: every non-CV family needs brand-new canonical sections, so **headings rows must be
authored and loaded BEFORE or WITH their Section Orders, never after.** Load a Section Order
first and every section name without a headings row is a dangling FK and the gate goes non-zero.
This is how gate 82 happened last time. The drafts are therefore authored in pairs.

### THE FAMILY COUNT IS 15 KEYS, NOT 14
data/base/structures.csv has 17 structure keys. cv-experienced and cv-academic carry a Section
Order; the other FIFTEEN are empty:
brochure-3panel, brochure-gatefold, cover-letter-standard, deck-standard, flyer-single-sheet,
form-standard, invoice-standard, letter-standard, memo-standard, one-pager-standard,
poster-single-canvas, proposal-standard, report-long-toc, report-short, whitepaper-standard.

Two mappings that are easy to get wrong, both bound from data/base/doctypes.csv:
- T1 `quote-devis` points at `invoice-standard`, NOT proposal-standard. invoice-standard must
  serve invoices AND quotes/devis/offers.
- T1 `infographic` has an EMPTY Structure Key. It is not in the 15 and gets no section order.

### PHASE PLAN
A. In parallel: DDR drafts section models class by class (transactional first: invoice, letter,
   memo, form, proposal), each draft being a headings CSV plus a section-orders CSV that
   validate together. Coverage takes three sequential cleanup briefs: duplicate-keyword sweep
   plus a permanent validator rule, contrast error line anchoring, and the schema's Section
   Order example that wrongly carries a "?" marker.
B. Coverage loads the headings rows FIRST, then the section orders, to gate zero. Mechanism
   updates resolve.py so "no section-order guidance for <doctype>" fires only for families still
   empty, with the 133-test baseline holding.
C. DDR fills the remaining families. Packaging updates the SKILL.md and README list of doctypes
   that carry structure guidance, and rebuilds.

DEFERRED, waiting on real query data, not on us: BM25 length normalisation and the tokenizer
split behaviour.

## DESCRIPTION LENGTH -- the one measured number
The SKILL.md frontmatter description measures **831 characters**, as of the candidate F edit
applied 2026-09-09. Verified with Python len() on the quoted value. The cap is 1023 (the
claude.ai UI enforces "under 1024"). Headroom: 192 characters.
It measured 823 before candidate F. Candidate B, if it is ever applied, would take it to 993.

The repo previously quoted 667 (references/activation.md) and 825 (skill/dist/POST-UPLOAD-TESTS.md).
Both are stale and are being corrected to 823. The 825 figure differs by exactly the 2-character
"validated" -> "sourced" edit, which the activation.md quoted block had not picked up.
If you change the description, re-measure and update this line. Do not quote it anywhere else.

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
