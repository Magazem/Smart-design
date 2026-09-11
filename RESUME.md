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

## MANIFEST HASHES CHANGED IN v0.2 -- the v0.1.0 pair below is OBSOLETE
The manifest gained `distinct_token_columns`, so its content changed. The CURRENT pair, both
correct, same two-form reason as before:
  c41634d53cd50ebbc3788e1b4e542e72  = the CRLF working copy on disk (768 CRLF pairs)
  e94ff944ac4645edd0871eb9156434b1  = the LF form, which is what git stores and what the ZIP
                                      member carries
A rebuild report quoting e94ff944 is quoting the ARCHIVE and is correct. Do not "fix" either.

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
> **CONFOUNDED — RETIRED AS EVIDENCE, 2026-09-11 (lead ruling). Kept, labelled, not deleted.**
> Every reading in this table is SHAPE-SCORED: "asked about format", "asked for client
> details", "asked the user to upload". The account's custom instructions were ON throughout
> and tell Claude to ask before acting on anything ambiguous, and to keep answers short. So the
> asking these rows scored was plausibly the INSTRUCTION, not the routing. Do not cite these
> PASS/FAIL verdicts as evidence for or against any description candidate.
> Still valid here: the raw observations (what Claude said, what it produced). Only the
> VERDICTS are retired.
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
> **PARTLY CONFOUNDED, 2026-09-11 (lead ruling).** Where a PASS here was scored on the SHAPE of
> a reply, it is RETIRED as evidence -- the account's clarify-first and brevity instructions
> were active. Where it was scored on Claude NAMING the skill it used, it STANDS. Prompt 11's
> pass stands. Prompt 12 was already inconclusive and now has a named cause.
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

## PHASE C PACKAGING MUST CARRY THIS LINE
Ruled by the lead: do NOT amend the published v0.1.0 release notes. When Packaging next touches
RELEASE-NOTES.md, add ONE line under a "Fixed" heading in the v0.2 section, to this effect:
  brochure-flyer-a4 listed one keyword twice in v0.1.0, slightly over-weighting that row;
  now gated.
Bind it into the phase C Packaging brief. It does not get a brief of its own.

## PHASE A IS COMPLETE, and these two decisions are INTENTIONAL -- do not "fix" them
All 17 structure keys are covered: 2 CV rows already had orders, the other 15 are drafted across
research/39 (transactional), research/40 (long-form) and research/41 (marketing). 204 heading
rows across four loader inputs, zero dangling FKs, zero generated-key collisions under a shared
counter, one primary per section per language, and no section order repeats a token.

1. THREE PAIRS of families have IDENTICAL Section Orders, ALL RULED INTENTIONAL:
   - brochure-3panel and brochure-gatefold: panel count is not content; what separates a
     tri-fold from a gate-fold lives in page-formats, panel count and widths.
   - letter-standard and cover-letter-standard: a cover letter IS a letter.
   - flyer-single-sheet and one-pager-standard: same content arc, different format.
   Do not "differentiate" any of them, and do not special-case shared orders in the resolver.
   When two doctypes share an order, the DISCRIMINATING WORK IS DONE BY page-formats and
   doc-styles -- page size, panel count, measure, margins, typography. An identical section
   list does not mean an identical document. All three pairs are flagged in
   research/44-v02-acceptance.md so a user is not surprised by matching answers, and the
   release notes say it in one sentence.
2. The marketing class added only ONE new canonical section, `agenda`. Five of its six families
   are served entirely by sections authored for the earlier classes. That is the reuse rule
   working, not a shortcut.
3. `proposed-solution` was REFUSED for whitepaper-standard in A2 (its German primary carries a
   commercial-bid flavour) and REUSED for deck-standard in A3 (a pitch deck's sales register is
   exactly where that flavour belongs). Both calls stand. The rule cuts both ways.

## PHASE B RESULTS, 2026-09-10
B1 loaded the section model: gate zero at **414 rows** (was 291), headings 81 -> 204, all 17
structure rows carry a Section Order. Commit aec56f4. Only headings.csv, structures.csv and
rationale/headings.md moved; no other table.
Mechanism made the degradation docstring honest and pinned the path with two synthetic-row
tests, since NO row in shipping data has an empty Section Order any more. 140 tests. Commit
47ede8d, a five-line docstring diff, no constant touched.

### E3 VINDICATED THE NO-TUNING RULE
"make me a flyer" was a FAIL in research/35: it resolved confidently instead of abstaining, and
a one-constant margin change would have turned it green. Coverage refused that change at the
time (see the green-tick precedent). E3 NOW PASSES on its own -- it abstains and offers the real
flyer candidates -- repaired by the keyword de-duplication and the tokenizer diacritic fold,
neither of which was aimed at it. The honest fix elsewhere solved the symptom here. Cite this
alongside the green-tick precedent.

### BACKLOG: language signal in ranking
F3 "fais-moi un cv" still passes, but its internals moved: cv-generic dropped out of the top
three entirely and it now abstains among cv-uk, cv-gulf-gcc and cv-france within 0.014 of each
other. Lead's ruling after running it himself: NOT a regression -- a French prompt has no
business matching the generic row, and all three offered are CVs. What it exposes is that
LANGUAGE CARRIES NO RANKING WEIGHT: cv-france should lead on a French query and does not.
Backlog line "language signal in ranking (cv-france on 'fais-moi un cv')". Same family as D3.
Not v0.2.

### D3 STILL FAILS, ON PURPOSE
"erstelle eine präsentation" resolves confidently instead of abstaining. Untouched. The real fix
is BM25 length normalisation, which waits on real query data. Do not lower b.

## BACKLOG: physical layout order for folded and paged formats
The content arc fits a Section Order fine. Panel COUNT, slide COUNT, and the non-linear panel
adjacency of a tri-fold or gate-fold fit NOWHERE in the current model. Flagged as a real gap by
DDR rather than forced into a section list. Not v0.2.

## BACKLOG, added 2026-09-09
- make_brand_kit.py lines 498 and 560: the same single-word duplication, live today but ungated
  because Keywords is declared only on doctypes.
- Doc drift: data/schema-manifest-NOTES.md section 1.4 documents every manifest key and does not
  mention `distinct_token_columns`; build-manifest.py's docstring claims the manifest derives
  from research/09-library-schema.md Revision 4, which does not describe it either.
- Heading variants for non-CV families.

## v0.2.0 IS PUBLISHED AND VERIFIED -- 2026-09-11
Tag v0.2.0 at 31fa967. Release workflow succeeded in 16s.
https://github.com/Magazem/Smart-design/releases/tag/v0.2.0
Asset document-design-intelligence-0.2.0.zip, 143209 bytes, 39 members.

I DOWNLOADED THE PUBLISHED ASSET and verified its bytes, not the local build:
  SKILL.md starts b'---
'; exactly one stamp reading "version: 0.2.0"; VERSION member 0.2.0,
  so CI wrote both from the tag as designed. Zero CR bytes. Description 972 and starting with
  "Creating any document type below", so candidate L shipped. display_columns on 6 tables, so
  the docx handoff fix shipped. Row counts all as built: constraints 47, type-scales 20,
  headings 204, structures 17, doctypes 30. Mirror byte-identical. The plain-text sentence is in
  the body. No .docx members, no brand leak. Manifest md5 070195f13a226c35bf7743c7466ba50d.

THE RELEASE BODY IS ONLY THE v0.2.0 SECTION. Verified on the published release: it starts with
"# v0.2.0", contains NO "# v0.1.0", and exactly one version heading. Ruling O worked in CI on its
first run. The workaround line and the empty-handoff disclosure are both in the published body.

## RULING 2026-09-11 (user, accepted by lead): v0.3 PRIORITY IS INVOKED QUALITY, NOT AUTO-FIRE
100% auto-firing is a later-stage goal. The MVP bar: when the skill runs -- invoked by name
or auto-fired -- the result must be good. v0.3 headline is an INVOKED-QUALITY acceptance pass:
the 15 family prompts with "Use the document-design-intelligence skill." appended, scored on
OUTPUT (sections present and ordered, handoff values applied, zero "not in my library"
refusals). Fix what it exposes first. EN/FR prose-genre auto-fire stays deferred behind the
documented workaround. Ordered list in research/PROJECT-MAP.md section 5.
STANDING RULE for every new format from now on: a format is DONE only when it is fully in the
library (doctype row, structure with headings in all three languages, type scale, page format,
handoff values reaching the renderer) and produces a good result when the skill runs. The
v0.1.0-era symptom "that document type is not in my library" must never recur for a shipped
family; auto-firing is a separate, later concern.

## v0.3 BACKLOG -- everything deferred, in one place
- **TOP ITEM (lead ruling 2026-09-11): CONSIDER REVERTING CANDIDATE L.** Activation 11 fired
  2/2 under H and has now gone docx-only 2/2 under L. L was a pure SALIENCE/ORDERING reorder
  that was NEVER shown to help anything; this is the first evidence it may HURT.
  DECISION PROCEDURE, do not skip steps: (1) one more CLEAN run of activation 11 under L; (2)
  if it still fails, one run with L REVERTED. Decide on that, not on the n=2 alone.
- **TEST THE FILE-ROUTING MECHANISM** (see "THE CLEAN RUN, 2026-09-11" for the evidence).
  Claude's own account says naming a format routes to docx on ITS trigger criteria, and
  implying no file means no document skill is considered at all. If that holds, the lever is
  the deferral sentence's interaction with a NAMED FORMAT, which no candidate has targeted.
  This satisfies the standing rule's requirement for a fresh Claude-sourced mechanism.
- characterSpacing in the docx handoff reads "Letter Spacing pt", a column that exists in NO
  table. Decide: remove the handoff section, or author the column.
- HEADING VARIANTS for non-CV families. The 81 CV heading rows carry 2-3 wordings per language;
  the 123 non-CV rows carry one. Nothing reads Is Primary today, so this is model-facing only.
- LANGUAGE SIGNAL IN RANKING. cv-france does not lead on a French query. Same family as D3.
- D3: "erstelle eine praesentation" resolves confidently instead of abstaining. The real fix is
  BM25 length normalisation and it needs real query data. DO NOT lower b.
- PANEL AND SLIDE LAYOUT ORDER. Panel count, slide count and folded-panel adjacency are modelled
  nowhere. Section Order carries the content arc only.
- FR-REPORT ROUTING, and the whole EN/FR prose-genre routing problem. See the closure ruling
  above: NO further description candidates without a new mechanism hypothesis backed by Claude's
  own account.
- manifest NOTES section 1.4 still claims the four list-FK columns are "not declared twice" and
  that build-manifest asserts it. That assertion was inverted at Revision 4 and list_columns now
  holds 12 columns. Flagged inline with a blockquote, not rewritten.
- test_ddi.py main-guard placement: DONE in the pre-tag commit, drop this line if you see it.
- make_brand_kit.py lines 498 and 560: the same single-word duplication fixed at line 590, live
  today but ungated because Keywords is declared only on doctypes.
- brochure-3panel / brochure-gatefold and the other two identical-order pairs: INTENTIONAL, do
  not "differentiate" them. Listed here only so nobody files it as a bug.

## THE WORKAROUND THAT ACTUALLY WORKS (probes, 2026-09-11)
PROBE 1: English memo with "Use the document-design-intelligence skill." appended -> **FIRED.**
PROBE 2: English memo with the built-in docx skill disabled -> **NOT RUNNABLE.** claude.ai
offers no per-skill toggle for the built-in docx skill. Dropped, not failed -- nobody should
re-attempt it looking for a result.

So the skill works. It is the ROUTING that does not, and naming the skill in the request
bypasses the routing entirely. That is the honest shape of this defect: not "the skill is
unreliable" but "Claude does not always choose it, and you can tell it to."

SHIPPED WORDING, bound by the lead into the v0.2.0 release notes and README:
  Limitation: With the built-in docx/pptx skills present, letters, memos and reports in English
  and French may be routed to docx or answered in chat without this skill; invoices, forms and
  German prompts fire reliably.
  Workaround: Add "Use the document-design-intelligence skill." to the request; this fired in
  every test.
The French report is listed explicitly as a known non-fire.

Both lines go in the SAME paragraph. A limitation without its workaround makes a user think the
tool is broken; the workaround is the more useful half and must not be a footnote.

## DESCRIPTION ITERATION IS CLOSED FOR v0.2. DO NOT OPEN ANOTHER CANDIDATE.
FIVE description changes were applied across 2026-09-09/10 -- F, G, H, lettre, L. Final results
on the L archive:
    FR letter    FAIL      EN memo      FAIL      FR report    FAIL (no trigger)
    activation 10 PASS     activation 13 PASS     activation 11 FAIL (went to docx)
Activation 11 was SAID to have fired 2/2 under H, before L. **That claim has no primary record
and must not be cited** -- see the candidate L ruling above. SETTLED 2026-09-11: L stays.

**FIVE CHANGES HAVE NOT MOVED ENGLISH OR FRENCH PROSE-GENRE ACTIVATION.** Routing against the
built-in docx skill is CLAUDE'S DECISION, not something we can force with description text.
L stays: it states intent, costs nothing, and prompt 13 still passes.

### THE FULL REFUTATION CHAIN -- every theory tried and killed, in order
1. NOUNS. Dead. "memo" and "rapport" were IN the description; both families failed.
2. TRIGGER PHRASES. Dead. invoice and form have NO create-verb phrase and both fire.
3. ARTEFACT vs PROSE GENRE. Dead AS AN EXPLANATION. The German whitepaper and German memo both
   fired -- prose genres in German. Candidate J was built on this and vetoed before application.
   The OBSERVATION survives and may be cited (ruled 2026-09-11): CVs, invoices, forms and German
   prompts fire; EN/FR letters, memos, reports and proposals often do not. The mechanism is
   UNKNOWN -- do not offer artefact-vs-prose as the reason.
4. LANGUAGE AS ROOT CAUSE. Superseded. It is a correlate; Claude's own account gave the
   mechanism instead.
5. SALIENCE / ORDERING. Applied as candidate L. Did NOT fix EN/FR prose genres.
6. TOKEN PARITY WITH THE COMPETING SKILL. **DEAD, 2026-09-11.** Candidate M put the literal
   '.docx'/'.pptx' tokens into our own deferral sentence, at the point the priority claim is
   made, because P6 is Claude naming that exact token as its deciding signal. Activation 11 was
   re-run VERBATIM on a clean, enabled, unconfounded account with the M build verified installed.
   **DOCX-ONLY. Identical to L.** Full record: research/60-candidate-M-refuted.md.
   This was the FIRST candidate built on a mechanism from Claude's own account rather than our
   theorising, and it still failed. That makes it a STRONGER result than the previous five, not
   a weaker one -- the standing rule's bar was met and the lever still does not exist.
   It was killed by its OWN falsification test, written down BEFORE the run. Pre-registering the
   falsifier is what made one browser run decisive. Keep doing that.

### *** THE DESCRIPTION LEVER IS EXHAUSTED FOR THE NAMED-FORMAT CASE (2026-09-11) ***
SIX candidates -- F, G, H, lettre, L, M -- have been applied or tested. **NONE has moved routing
for a prompt that names a format.** Claude's own account (P4, P6) says routing turns on the FILE
and the NAMED FORMAT, decided before our description is weighed. M tested the one remaining
reading of that account and it is refuted. **P6's mechanism statement is SPENT.**
Auto-firing stays deferred behind the documented workaround: add
"Use the document-design-intelligence skill." to the request. That is the v0.3 ruling and this
result confirms it.

### STANDING RULE
**NO FURTHER DESCRIPTION CANDIDATES WITHOUT A NEW MECHANISM HYPOTHESIS BACKED BY CLAUDE'S OWN
ACCOUNT.** Not by our theorising, not by another tally. The one genuinely new fact all day came
from ASKING CLAUDE what it did, and it produced candidate H and then L. If you cannot point at a
fresh statement from Claude explaining a decision, there is nothing to write a candidate against.

### THE HONEST SHAPE OF IT, for the release notes
CVs, invoices, forms and German prompts fire reliably. English and French letters, memos,
reports and proposals may be routed to the built-in docx skill or answered directly in chat.
That is a limitation to STATE, not to hide behind more description text. State it as the
OBSERVED pattern; do not explain it as "artefact vs prose genre" (dead, ruled 2026-09-11).

The user is running two workaround probes: an English memo with "Use the
document-design-intelligence skill." appended, and an English memo with the built-in docx skill
disabled. Their results decide the exact wording of the workaround line.


## PROMPT 1 (ENGLISH CV) FIRES — do not inherit "EN prompts do not fire"
Recorded 2026-09-11 by the sub-manager after a lead correction. The closure ruling at
"FIVE CHANGES HAVE NOT MOVED..." is about EN/FR PROSE GENRES ONLY -- letter, memo, report,
proposal. It is NOT a statement about English as a language.
Activation prompt 1, "Can you make me a CV for a marketing coordinator role?", has PASSED in
every run: see the 2026-09-09 activation table above (row 1, PASS) and every v0.2 round.
When writing a brief or reading a result, the expected outcome for the CV prompt is a FIRE.
Treating a CV non-fire as normal would hide a real regression.
SUPERSEDED IN PART 2026-09-11 -- see "BROWSER ACCEPTANCE TESTING" below: the 2026-09-09 PASS
verified OUTPUT, not INVOCATION. Read this section as "prompt 1 reliably produces a CV", not
"prompt 1 reliably fires the skill". Give it inline content per ruling G before scoring it.
FURTHER, 2026-09-11: the 2026-09-09 row this section rests on is now RETIRED AS CONFOUNDED
(shape-scored, instructions active). What replaces it is BETTER: the 2026-09-11 browser run
showed "Ran 4 commands" and a CV-region picker whose options are rows in our own
cv-regions.csv. That is invocation evidence, not shape. Prompt 1 very probably fires; confirm
it by expanding the commands line on the re-run.
WHY IT FIRES IS UNKNOWN, and that is settled (ruled 2026-09-11): the artefact-vs-prose theory
is dead as an EXPLANATION because German prose genres fired. Cite the OBSERVATION -- CVs,
invoices, forms and German prompts fire; EN/FR letters, memos, reports and proposals often do
not -- and never the theory. The refutation chain and the fire/no-fire section both say this now.


## BROWSER ACCEPTANCE TESTING: WHAT IT COSTS AND WHAT IT IS FOR (ruled 2026-09-11)
Source: research/47-browser-smoke.md, the first live browser run.

**THE QUOTA CONSTRAINT, which decides the whole testing strategy.** The user's claude.ai
account reported "You've used 75% of your weekly limit" after TWO sends. The planned 13
prompts x 3 repeats = 39 sends would exhaust the user's plan several times over. Do not
plan browser runs by prompt count without checking this first.

**RULING (lead, 2026-09-11):**
- The BROWSER tester is for SMALL ROUTING SPOT-CHECKS ONLY. Max ~6 prompts per session.
  Run only after the weekly limit resets, unless the user says otherwise.
- The target set is the previously FAILED cases plus one control: EN memo, FR letter,
  FR report, activation 11, plus a control known to behave.
- The API HARNESS (separate billing) is the scalable path for the invoked-quality pass and
  for ALL regression runs. Anything that needs many runs goes there, not through the browser.

**UI DOUBLE-SUBMIT.** The tester observed one prompt landing as TWO turns. Before reading any
result, verify that exactly ONE send occurred. A double-send silently doubles quota spend and
can produce two differing answers for what looks like one trial.
- **DOUBLE-SUBMIT: WAIT 20 SECONDS.** Two of seven prompts double-submitted on 2026-09-11,
  costing 16 sends instead of 14. Cause: on a fresh /new chat the user message does not render
  for ~10-15 seconds during the /new -> /chat/<id> transition, so the send LOOKS failed and the
  tester retypes -- but the first send already went through server-side. RULE: after clicking
  Send on a fresh chat, WAIT AT LEAST 20 SECONDS and re-check before concluding anything
  failed. Never retype on a blank-looking chat inside that window.

**WHAT THE SMOKE TEST PROVED**
- Login: PASS. Skill listed: PASS -- description shown matches the candidate-L wording
  recorded as shipped in v0.2.0, so the installed build is the expected one.
- The browser harness WORKS, once the panel is opened inside the tester's own conversation.

**WHAT IT DID NOT PROVE, and this is the important part**
- Prompt 1 was INCONCLUSIVE, not a fire and not a regression. Claude asked for real CV content
  instead of producing anything design-framed. With no content in the prompt, asking for it is
  correct generalist behaviour and proves nothing either way -- the same test defect this file
  already names for prompts 3, 4, 5 and 12.
- THE SMOKE TEST WAS NEVER SCORABLE, because the tester did not ask the follow-up question.
  See "THE BROWSER DETECTION METHOD" below: the method is the UI indication PLUS asking "did
  you trigger any skill?" in the same chat. Without the follow-up a trial is UNSCORED, not a
  fail. (This bullet previously claimed no detection method existed. That was my error,
  corrected by the lead 2026-09-11.)
- CONFOUND, spotted by the tester and not yet investigated: one reply said "per your
  clarification rule", which points at an account-level Memory or custom-instruction setting
  forcing Claude to ask before inventing content. If such a setting is active it changes
  behaviour on EVERY browser trial and none of them are clean ground truth. CHECK THE ACCOUNT'S
  MEMORY AND CUSTOM INSTRUCTIONS BEFORE THE NEXT BROWSER RUN.

**CORRECTION TO "PROMPT 1 (ENGLISH CV) FIRES" ABOVE.** That section overstates the evidence and
I wrote it. The 2026-09-09 PASS reads "asked about format, produced an ATS-friendly French CV"
-- output was produced, but invocation was NEVER verified by an indicator. That is the same
ask-before-invoke shape ruled a test defect elsewhere in this file. Ruling G fixed prompt 12 by
giving it inline content; THE SAME FIX WAS NEVER APPLIED TO PROMPT 1. Read that section as
"prompt 1 reliably produces a CV", NOT as "prompt 1 reliably fires the skill". Before prompt 1
is used to judge anything, give it inline content per ruling G.

**GAPS IN THE SMOKE-TEST DELIVERABLE** (brief asked, file does not answer; not worth a re-run,
but fold into the next brief): the verbatim first 300 characters of the reply were paraphrased
rather than quoted; WHERE the tester looked for an invocation indicator was not described; and
whether docx and pptx were enabled in that chat was not recorded. The last one matters -- the
handoff tests are meaningless if those two skills are off.

## THE BROWSER DETECTION METHOD (recorded 2026-09-11 by lead correction)
I wrongly recorded that no detection method exists. One DOES, and it is what produced every
manual result in this file. Two parts, use BOTH:
1. Read claude.ai's own skill-use indication in the reply stream, if it is shown.
2. **ALWAYS ASK THE FOLLOW-UP IN THE SAME CHAT BEFORE SCORING: "did you trigger any skill?"**
   Claude has answered this ACCURATELY every time it was asked -- it named docx when it used
   docx, and named document-design-intelligence when it used DDI.
Step 2 is not optional and is not a fallback. A trial that was never asked the follow-up is
UNSCORED, not a fail. That is exactly what made the 2026-09-11 smoke test inconclusive: the
tester never asked.

**COST CONSEQUENCE, and it halves every browser run.** The follow-up is a SEND. It spends the
user's weekly quota like any other. A six-send ceiling is therefore THREE PROMPTS, not six:
each prompt costs one send for the prompt and one for the follow-up. Plan browser sessions in
PAIRS of sends, never in prompts.

**PARALLEL TESTERS AUTHORISED (user, 2026-09-11).** Two or three copies of the Acceptance
Tester may be spawned to split a large browser run. Not needed below ~7 prompts. Keep it for
the 13x3 run. Spawning is LEAD-ONLY -- ask the lead, do not attempt it yourself. Each copy
needs its browser panel attached in ITS OWN conversation (see the teammate list), so N copies
means N panels the user must open; factor that into whether splitting is actually cheaper.

**USER RULING 2026-09-11, SUPERSEDING THE SIX-SEND CEILING ABOVE.** The quota is NOT a
concern: the 75% came from the user's other work, 25% remained, and it resets in under 18
hours. The spot-check was dispatched at SEVEN prompts x 2 sends = 14 sends. Keep the cost
awareness -- check the remaining limit before a large run -- but do not ration sends against
the six-send figure; that ceiling is withdrawn.
Also ruled: prompt 1 asking for content was EXPECTED, and the fix is to append
" Use placeholder data." to the prompt rather than to treat the ask as a failure.
The follow-up question is now fixed wording: "Which skills did you use for this request,
and why?"

## THE ACCOUNT'S CUSTOM INSTRUCTIONS ARE A PROJECT-WIDE CONFOUND (found 2026-09-11)
Full text quoted in research/48-browser-spotcheck.md Step 0. The user's claude.ai account
carries "Instructions for Claude" including:
  "If anything is unclear or ambiguous, ask me to clarify before doing anything. Never run on
   assumptions."
  "Keep answers short and to the point unless I explicitly ask for detail."
  "stick to it and don't go beyond what's asked"

**CONSEQUENCE, and it reaches backwards.** Every activation result whose FAIL reading was
"Claude asked for details first" -- prompts 2, 3, 4, 5, 12 and the 2026-09-11 smoke test --
may be THIS INSTRUCTION, not a routing failure. The ask-before-invoke pattern this file has
called a "test defect" five separate times now has a named cause, and it is not the skill.
The brevity clauses separately suppress the elaborated design reasoning that several rubrics
use as their PASS signal.

What this does NOT touch: fire/no-fire results established by skill INVOCATION (the follow-up
question, or a "Ran N commands" line). Those stand.
What it DOES undermine: every rubric that scored on the SHAPE of a reply.
BEFORE the next scored run, decide with the user whether to test with these instructions
temporarily off. It is their account and their setting -- ASK, never change it.


### WHICH OLD RESULTS SURVIVE THE CONFOUND (lead ruling, 2026-09-11)
Apply this test to any historical result before citing it.

**RETIRED as evidence** -- anything SCORED ON THE SHAPE of a reply: "asked about format",
"asked for details", "produced X", "gave design reasoning", "answered generically". The
account's clarify-first and brevity instructions were active and produce exactly these shapes
independently of routing. Keep the rows, keep the observations, LABEL them, do not delete them,
do not cite their verdicts.

**STANDS** -- anything established by CLAUDE NAMING THE SKILL IT USED. The custom instructions
change how Claude WRITES; they do not change what it REPORTS having invoked. Specifically:
the v0.1.0 13/13 "did you trigger any skill" answers; the G+H re-run fires; the prompt 11 text
pass; the probe-1 fire. **The description-candidate refutation chain STANDS** for the same
reason -- it was built on invocation, not on prose shape.
### STANDING PRECONDITION FOR EVERY BROWSER RUN (ruled by lead, 2026-09-11)
1. Step 0 of every browser brief READS the account's "Instructions for Claude" and the report
   QUOTES their exact text. No exceptions, no summarising.
2. A run made while a clarify-first or brevity instruction is ACTIVE is labelled **CONFOUNDED**
   and is NOT SCORED. It may still be run and reported; it may not be treated as evidence.
3. RECOMMENDED TO THE USER: switch the custom instructions OFF for test sessions only. The
   skill targets DEFAULT-BEHAVIOUR users, so a default-behaviour account is the correct test
   environment. It is the user's account and the user's setting -- ASK, never change it, and
   never ask the tester to change it.

## "Ran N commands" IS THE UI HALF OF THE DETECTION METHOD (found 2026-09-11)
A collapsed "Ran 4 commands >" line appeared directly above a reply, meaning scripts executed.
Expand it to read the command names and it should identify WHICH skill ran. Use it on every
trial alongside the follow-up question.

## P1 EVIDENCE: THE PICKER OPTIONS ARE OUR OWN DATA (found 2026-09-11)
On the CV prompt, Claude offered "UK style", "France style", "Gulf/GCC style". Those map
one-to-one onto cv-regions.csv's uk-*, france-* and gulf-gcc-* keys. A generalist does not
propose "Gulf/GCC" unprompted as one of three CV regions. Strong evidence the skill fired.
GENERAL LESSON, worth more than the datapoint: when a reply offers options drawn from the
library's own vocabulary, that is invocation evidence. Watch for it.

## OPEN QUESTION: IS THERE A USER-VISIBLE docx/pptx SKILL? (raised 2026-09-11, UNRESOLVED)
The account's skills list shows NO docx or pptx entries. Word/PowerPoint creation appears as
the built-in capability "Cloud code execution and file creation".
IF the deferral target is a capability rather than a listed skill, then (a) SKILL.md's opening
deferral sentence -- about 180 of its 972 characters -- aims at something that may not exist as
a skill, and (b) activation tests 11, 12 and 13 are premised on "docx activates as top-level
skill", which may be impossible on this surface.
DO NOT ACT ON THIS YET. Absent from a settings UI is not absent from the system, earlier
testing recorded activation 11 "went to docx", and research/24-builtin-alignment.md was built
on reading Anthropic's real docx/pptx SKILL.md files. Settle it by expanding a "Ran N commands"
line on a Word-output prompt before touching the description.

## BROWSER OPERATIONAL RULE: NEVER RELOAD THE PAGE (learned 2026-09-11)
The spot-check died because the tester reloaded the chat page to get a cleaner read. The reload
timed out and took the accessibility tree and the JS execution context with it: every
take_snapshot / evaluate_script / press_key call afterwards failed with "Frame with the given
frameId is not found". Screenshots and page listing kept working, so it LOOKS connected, but
nothing can be typed or clicked and there is no coordinate-click fallback. The session is
unrecoverable from the tester's side and needs a fresh panel from the user.
RULE: do not reload, and do not navigate away from a chat mid-trial. If a reply is obscured by
an overlay or a limit banner, scroll or screenshot it. Losing part of one reply is cheap;
losing the session costs a user-side panel reset and everything not yet recorded.

## *** THE CLEAN RUN, 2026-09-11: RESULTS AND THE MECHANISM IT FINALLY GAVE US ***
Full record: research/48-browser-spotcheck.md, "RE-RUN v2". Custom instructions PROVEN empty
(the textbox carried no value attribute while sibling fields did). NOT confounded. All 7 scored
by SKILL.md path in the expanded commands line PLUS Claude's own follow-up answer.

    P1 CV          FIRED          P5 summarise   no fire (correct)
    P2 FR letter   no fire        P6 notes->Word no fire, went docx
    P3 EN memo     FIRED          P7 convert     no fire (correct)
    P4 FR report   no fire

### THREE THINGS THIS SETTLES

**1. THE HANDOFF DESIGN WORKS. First live proof.** P3's command chain is
`/mnt/skills/plugins/document-design-intelligence/SKILL.md` THEN `/mnt/skills/public/docx/SKILL.md`
-- resolve, then build -- exactly what SKILL.md promises. Claude's own account: DDI "resolved
the right structure (To/From/Date/Subject/Body ordering), layout, typography and color palette",
then handed to docx "to write the script that generates the Word file, then followed its
verification step". The two-stage handoff is not theoretical. It ran.

**2. THE docx/pptx OPEN QUESTION IS CLOSED. They ARE skills.** They live at
`/mnt/skills/public/docx/SKILL.md` and `/mnt/skills/public/pdf/SKILL.md`, loaded from inside the
code-execution capability. Absent from the Settings list, present in the filesystem. The
deferral sentence in our description targets something real. DO NOT rewrite it on the
"capability not a skill" reading -- that reading is now DISPROVED.

**3. EN PROSE IS NOT DEAD; FR PROSE STILL IS.** The EN memo FIRED for the first time ever, on a
clean account. So the custom instructions explain at least part of the historical EN failures.
The FR letter and FR report BOTH failed clean -- the French limitation stands on its own and is
not an artefact of the instructions.

### *** THE MECHANISM, FROM CLAUDE'S OWN ACCOUNT -- this is what the standing rule demanded ***
The STANDING RULE above forbids new description candidates without a fresh mechanism statement
from Claude. This run produced two, quoted verbatim from the follow-ups:

- P6 (notes -> Word, went docx): *"Since you asked for a Word doc specifically, it was the clear
  match (its trigger criteria explicitly call out '.docx' requests)."*
- P4 (FR report, no skill at all, emitted Markdown): *"I chose Markdown over Word specifically
  because you didn't ask for a Word file or signal you needed a formal downloadable document."*

**THE HYPOTHESIS THEY SUPPORT.** Routing appears to turn on the FILE, not the genre:
  (a) User NAMES a format ("a Word document") -> docx wins on its own trigger criteria, and our
      "creation is still our job even as Word" clause does NOT beat it. P6, n=2 under L.
  (b) User implies NO file -> Claude answers in chat or emits Markdown and no document skill is
      considered at all. P4.
  (c) A file is implied but no format named, AND there is a design decision to resolve -> we
      fire. P1 (which CV region?) and P3 (memo header structure).
This is a testable mechanism sourced from Claude, not from our theorising. It is the first such
statement since the one that produced candidates H and L.

### CAUTION ON THE DETECTION METHOD, learned this run
P1's follow-up claimed the picker offered "UK, Gulf/GCC and France". THE SCREEN SHOWED
"UK/International, France, US". **Claude's self-report of its own tool output was inexact.**
Trust the SKILL.md PATHS in the expanded commands line as primary evidence of WHICH skill ran;
treat the follow-up prose as corroboration of the same, and do NOT rely on it for DETAILS.
Both were captured this run only because the brief demanded both. Keep demanding both.

### ACTIVATION 11 UNDER CANDIDATE L -- now n=2 docx-only
SUPERSEDED 2026-09-11 -- see the candidate L ruling. The "fired 2/2 under H" baseline has no
primary record and cannot be cited. L is neutral-and-unfalsified and STAYS; the revert was
skipped by ruling. Activation 11 is docx-only under L on a clean, invocation-scored run.
## THE LESSON OF 2026-09-10: A GREEN GATE DOES NOT MEAN THE OUTPUT SAYS ANYTHING
Coverage removed the `report-print-print-h1` row and re-ran everything. **The gate STILL PASSED**
-- `OK: validated 14 table(s)` -- because the remaining rows were perfectly well-formed. Only the
new end-to-end test caught it, by name, showing ['h2','h3'] against the expected
['h1','h2','h3'].

VALIDATION PROVES ROWS ARE WELL-FORMED. ONLY AN END-TO-END TEST PROVES THE OUTPUT SAYS SOMETHING.

Every significant defect found today has this shape -- the data was valid, the code ran, exit 0,
and the answer was empty or wrong:
- the docx handoff block carried no page size, fonts or palette since v0.1.0
- the table-of-contents doctype handed over no heading levels
- a plain-text answer silently dropped the whole section model
- the description coverage test would have passed while checking nothing, twice
None of these were caught by the gate, by validate_data, or by the suite as it stood. All were
caught by looking at what the thing actually PRINTED.

When adding any check, ask what it would say if the feature produced NOTHING AT ALL. If the
answer is "it would pass", it is not a test.

## v0.2 ADDS TWO CONVENTION-TAGGED SETS -- ONE release-notes sentence covers BOTH
Ruled by the lead. Bind into the Packaging tag brief.
1. The five PAGE-FLOW rules (keep-with-next, widows and orphans, table row integrity, repeated
   table headers, figure with caption).
2. The five HEADING SIZES for report-print and cv-print.

Both are CONVENTION, not sourced, and both were checked before authoring rather than assumed:
- Page flow: Bringhurst is cited in this library only for measure and leading, never pagination.
  Butterick and DIN 5008 are cited NOWHERE in it.
- Heading sizes: report 03 gives NO print point-size floor for any role. The rows derive from
  print-office-generic at the same 11pt body -- but THAT set is itself house-authored and
  validated by the leading-ratio formula, NOT a report-03 floor. So the derivation inherits
  convention status; it does not borrow a source that never existed.

TWICE TODAY a ruling named an authority that turned out not to cover the case, and DDR checked
and said so instead of borrowing the name. That is the behaviour to keep.

## cv-print HAS NO h3, DELIBERATELY
h1 and h2 only. A CV's third tier -- job title and dates -- is carried by WEIGHT CONTRAST, not a
distinct size, and a page-budget document should not gain a heading tier without a reason.
Mirroring the report's three tiers would have passed unquestioned. Do not "complete the set".

## RULING K PAGE-FLOW RULES SHIP AS CONVENTION, NOT SOURCED -- say so in the release notes
The ruling that commissioned these rows named Bringhurst, Butterick and DIN 5008. DDR grepped
this library's own citations before authoring and found: Bringhurst is cited repeatedly but ONLY
for measure and leading, never pagination; Butterick and DIN 5008 are cited NOWHERE in this
library at all. It tagged all five rows CONVENTION rather than borrow an authority it could not
verify, and the lead confirmed the naming was a suggestion, not a citation.

BINDING: the v0.2 release notes must state, IN THE SAME SENTENCE that announces the page-flow
rules, that they ship as convention rather than sourced. Bind it into the Packaging brief for
the tag. This project's whole discipline is keeping sourced and conventional apart; announcing
these as if they were cited would spend that credibility for nothing.

The one number, `min_lines_together=2`, is convention-by-ubiquity, flagged the same way the
existing legal-text 8pt floor flags its own unsourced threshold.

TWO SCOPES ARE DELIBERATELY EMPTY, not missing (the other three carry a real scope): `report-heading-keep-with-next` and
`report-figure-caption-keep-together` carry their block type in Parameter via `applies_to_block`
and `binds_to`, following the photocopy-safe precedent of putting roles in Parameter. Do not
"fix" them.

## CLAUDE'S OWN ACCOUNT -- the decisive evidence, verbatim (2026-09-10)
The user asked Claude, in the two FAILED French chats, which skills it considered.

FR LETTER: "I only pulled up the docx skill and didn't check document-design-intelligence. In
hindsight, that was probably the wrong call. You never said Word or .docx -- you just asked for
a formal business letter. Per document-design-intelligence's own trigger rules, letters
(courrier) without a named file format are its job, and it defers to docx only when the user
explicitly names the format for a plain conversion. Since you didn't name a format, it should
have taken priority."

FR REPORT: "I considered the general file-creation guidance (whether this needed a file vs.
inline text, and which format), but I didn't check document-design-intelligence before creating
the file -- I should have. That skill's trigger list explicitly includes reports, so it was
relevant here and I skipped it. I treated this as a short internal markdown summary rather than
a designed document."

### WHAT THIS SETTLES
**THE DESCRIPTION'S CONTENT IS CORRECT.** Claude ENDORSES it once it reads it -- it names
courrier, it recites the deferral condition, it concludes we should have taken priority.
**THE FAILURE IS SALIENCE AT DECISION TIME.** Claude decides "make a file", reaches for docx or
a markdown file, and never opens ours at all.

Candidate H's priority claim is the RIGHT SENTENCE in the WRONG PLACE: it is the seventh of
eight, arriving long after the decision is made. Candidate L reorders it to first.

Note this also reframes the language finding above: the German prompts may simply have been
phrased in ways that made the decision differently, not "German routes better". Keep the tally,
but do not treat language as the root cause now that Claude has told us the mechanism.

## ACTIVATION PROMPT 11 WITH TEXT OUTPUT: PASS -- the plain-text fix is PROVEN
User report: the skill fired, produced well-organised structured text WITHOUT asking for a
format first, and only then offered PDF or docx. That is exactly the behaviour commit 706da0d
was written to produce. It was reported as "addressed, not proven"; it is now proven in
behaviour, which is the only evidence that counts for a prose change.

## ACTIVATION: THE DISCRIMINATOR IS LANGUAGE. THREE THEORIES ARE DEAD. (2026-09-10)
Final tally on the G+H archive, every prompt with its noun present in the description:
    GERMAN  4/4 FIRE   (invoice 2/2, form 1/1, whitepaper, memo)
    ENGLISH 2/5        (memo 0/2, proposal 2/3)
    FRENCH  0/4        (letter 0/2, report 0/2)

### THE REFUTATION CHAIN -- read this before proposing any description change
1. NOUNS. Dead. "memo" and "rapport" are IN the description and both families failed.
2. TRIGGER PHRASES. Dead. invoice and form have NO create-verb phrase and both fire. This is
   what refuted candidate I, and my own premise for it.
3. ARTEFACT vs PROSE GENRE. Dead AS AN EXPLANATION, and it was the best theory we had. It
   predicted that prose genres would not fire. The GERMAN WHITEPAPER FIRED and the GERMAN MEMO
   FIRED -- both prose genres. Candidate J was built on this and was VETOED before application.
   The draft stays in research/38 as history; do not resurrect it without new evidence.
   WHAT SURVIVES (ruled 2026-09-11) is the OBSERVATION, not the mechanism: CVs, invoices, forms
   and German prompts FIRE; EN/FR letters, memos, reports and proposals OFTEN DO NOT. Cite that
   pattern freely. Do NOT cite "it is an artefact" or "it is a prose genre" as the REASON.

### WHAT I CHECKED ABOUT THE FRENCH NOUNS, and it clears them
Asked whether the FR nouns are written in some way that matches worse than the DE ones:
- ACCENTS ARE NOT IT. Only `dépliant`, `présentation` and `Broschüre` carry accents -- one of
  them GERMAN. The failing French prompts used `rapport` and `lettre`, both UNACCENTED.
- FRAMING IS NOT IT. French and German nouns sit in the SAME "also ..." list, same sentence,
  same punctuation. Nothing separates them.
- AND THE DECISIVE ONE, THE CLEANEST COMPARISON IN THE WHOLE FILE:
  **SAME NOUN. SAME FAMILY. SAME CONTENT. ENGLISH 0/2, GERMAN 1/1.**
  The German prompt said "internes Memo", and `memo` IS in the description, so the German memo
  had EXACTLY the same noun match as the English memo that failed twice. Nothing about the
  vocabulary differed. Only the language did.
  (I first recorded this as "there is no German memo noun". That was WRONG -- the lead caught it.
  The corrected version is stronger, not weaker: a controlled comparison beats an absence.)

Whatever drives this sits OUTSIDE the description's vocabulary. Do not spend description budget
on French nouns until we know what it is.

### NEXT STEP IS EVIDENCE, NOT A DRAFT
The lead has asked the user to probe Claude directly in the FAILED English memo and French
report chats: "which skills did you consider, and why not this one?" We act on its own account,
as we did with the "clean Word file" clue that produced candidate H. DO NOT draft a language
hypothesis before that answer arrives.

## THE ACTIVATION FIRE/NO-FIRE PATTERN (2026-09-10 evidence; theory SUPERSEDED 2026-09-11)
**READ THE RULING AT THE TOP OF THIS SECTION FIRST.** The heading below used to read "THE
ACTIVATION DISCRIMINATOR: ARTEFACT vs PROSE GENRE" and the bolded paragraph presented artefact-
versus-prose as the MECHANISM. That explanation is DEAD -- the German whitepaper and the German
memo both fired, and both are prose genres. Ruled 2026-09-11 by the lead: keep the OBSERVATION,
drop the EXPLANATION.

THE OBSERVATION, which is what the evidence supports and what you may cite:
CVs, invoices, forms and German prompts FIRE. English and French letters, memos, reports and
proposals OFTEN DO NOT. No mechanism is known for why.

Measured on the G+H archive, same prompts run twice:
    DE invoice  2/2 FIRE       DE form     1/1 FIRE
    EN proposal 1/2            EN memo     0/2
    FR letter   0/2            FR report   0/2
The three failures were RE-RUN and failed AGAIN. Deterministic non-fires, not routing noise.

~~An invoice and a form are ARTEFACTS Claude cannot produce as prose, so it reaches for a
document tool and finds us. A letter, a memo, a report and a proposal are GENRES CLAUDE WRITES
NATIVELY IN CHAT -- it writes them and never considers a skill.~~ **STRUCK 2026-09-11: refuted
by the German prose genres firing. Retained struck-through so nobody re-derives it.**

The observation above still kills every earlier theory, independently of any mechanism:
- NOUNS ARE NOT THE ISSUE. "memo" and "rapport" are both IN the description and both families
  failed anyway. Adding nouns cannot fix a family Claude never thinks to delegate.
- TRIGGER PHRASES ARE NOT THE ISSUE EITHER. invoice and form have NO create-verb phrase and both
  fire. That is what refuted my candidate-I premise.

The suspect is the LEAD SENTENCE, "Creates and fixes print/office documents", which reads as
FILES. Candidate H reached the case where a format is involved; nothing reaches the case where
Claude intends an ordinary chat reply. Candidate J tests this.

DO NOT go back to adding nouns for a family that fails. Check first whether it is a genre Claude
writes natively -- if it is, the noun is not the lever.

## STANDING RULE, 2026-09-10: "byte-identical" MEANS A BYTE COMPARISON
I reported several times that the fenced "as shipped" block in references/activation.md was
byte-identical to SKILL.md's description. It was not. It was line-WRAPPED, and my check folded
whitespace before comparing -- `" ".join(block.split()) == description`. That is a weaker claim
than the words I used, and nothing in the suite enforced it at all.

From now on: if a report says byte-identical, it means the bytes were compared. If whitespace
was folded, say "equal after whitespace folding". The fenced block is now genuinely one line and
gets a real test in a follow-up brief.

## THE TEST MARKER TRAP -- worth reading before touching the description again
scripts/tests/test_description_coverage.py splits the description into a positive region and a
negative one using a LITERAL string marker. Candidate H deleted the string that was serving as
that marker. Left alone, `find` returns -1, the positive region silently becomes the WHOLE
description, and the test passes forever while checking nothing.

Coverage caught it, moved the marker to H's wording, and added a hard AssertionError if the
marker is ever absent. I verified the guard by altering the phrase in SKILL.md: all six tests
ERROR rather than pass. Any future description edit that touches the marker phrase must move the
marker with it -- the guard will now stop you, loudly.

## APPLIED 2026-09-10, commit f69c6a2: description is now 964 characters
Candidates F, G and H are all live. B remains parked forever. The old deferral sentence
("When a specific file format ... is named") NO LONGER EXISTS -- do not grep for it.

FOLLOW-UP, ruled and not yet done, both AFTER the rebuild, one deliverable each:
1. activation.md stale prose: it still says the description "grew from 667 to 964 with the
   addition of the built-in-skill deferral sentence" (wrong cause now), and the paragraph below
   argues .docx/.pptx stay out of the trigger list while describing a sentence that no longer
   names them.
2. A real test enforcing the fenced "as shipped" block against SKILL.md's description, by BYTE
   comparison.
Neither blocks the user's re-run: activation.md ships in the ZIP but does not affect firing.
They go into a follow-up rebuild before the tag.

## THE PACKAGE AWAITING THE USER, as of 2026-09-10: G-minus-triggers + H = 964 chars
Not G alone. G supplies the missing nouns; H stops the deferral sentence from handing those
documents away. Applying G alone risks a re-run that still fails and unfairly blames G.

H's diagnosis, which is the real find of this round: the shipped deferral sentence says a format
"is named" WITHOUT SAYING BY WHOM, so the model's own choice to render a Word file satisfies it.
Combined with "no design ask" reading at ordinary width, a structural request like an invoice or
a memo is handed to the built-in docx skill by default. That is exactly what Claude told the
user: "a clean Word file, no design skills needed." H says "the USER names it" and keeps the
plain-conversion carve-out word for word.

The trade that makes it fit: G's 76-char trigger-phrase insertion is dropped. I VERIFIED this
costs no coverage -- every noun those phrases carry still appears elsewhere in G. G+H would be
1040, 17 over the cap; G-minus-triggers+H is 964, with 59 to spare.

The application brief is written and HELD at research/brief-coverage.md.

## WHEN CANDIDATE G IS APPLIED -- a condition that must not be forgotten
The description-coverage test is expected to be RED until candidate G lands, so it may ship
marked xfail with a reason naming G. Lead's condition, binding:

**THE XFAIL MARKER MUST BE REMOVED IN THE SAME COMMIT THAT APPLIES G.**

And the sub-manager's verification of that commit MUST include running the test WITHOUT the
marker and seeing it GREEN. Not "the suite passed" -- an xfail test passes the suite while
proving nothing. Run it un-marked, watch it go green, then commit.

If G is applied and the marker is left behind, the project keeps a permanently silent test
covering the exact defect that blocked v0.2 acceptance. That is worse than having no test.

## STANDING RULE, ruled 2026-09-10: widen the description in the SAME release that adds families
WHEN A RELEASE ADDS DOCUMENT FAMILIES, THE DESCRIPTION'S NOUN LIST MUST BE WIDENED IN THE SAME
RELEASE, AND THE COVERAGE MUST BE CHECKED PROGRAMMATICALLY, PER LANGUAGE.

Origin: v0.2 added section guidance for 15 families and shipped a description that never
mentioned them. The user ran acceptance prompts 1-5 and the skill fired on NONE. Claude's own
explanation: "I was doing a clean Word file as per the request, no need for design skills." It
was right -- the description gave it no reason to fire.

Measured by me on 2026-09-10: 8 of the 30 doctypes have NO Keywords token appearing anywhere in
the description -- cv-eu-europass, cv-academic, brochure-gatefold, report-long-toc,
slide-deck-handout, one-pager, infographic, invoice-tabular. The words "invoice", "facture",
"rechnung", "memo", "proposal", "one-pager" and "devis" are all absent.

The per-language part matters: memo-internal is reachable through "note interne" in French and
INVISIBLE in English and German. A single-language check would have called it covered.

The description is the ONLY activation lever. Data can be perfect and unreachable.

## SECOND DEFECT, same blocker: an acceptance prompt must not answer its own question
All 15 v0.2 prompts pre-labelled their sections -- "Rechnungssteller:", "To:", "From:",
"Cover:", "Executive summary:". The structure under test was supplied IN the request, so the
task collapsed to transcription and the docx skill correctly took it.

This is the SAME CLASS as the v0.1.0 round, where four of five failures were prompts referencing
content that was never attached. Both times the test proved nothing and looked like a product
failure. The rule now lives in research/44-v02-acceptance.md's header:
  An acceptance prompt must not pre-supply the structure it is testing.

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

## STANDING RULE, after its SECOND occurrence: IF A FILE HAS A GENERATOR, EDIT THE GENERATOR
First occurrence: data/rationale/headings.md, which says "do not hand-edit" on its own second
line and is written by load-base.py.
SECOND occurrence, 2026-09-10: `display_columns` was added BY HAND to
data/schema-manifest.json, which is written by research/build-manifest.py. I ran the generator
from the skill directory and the key was WIPED. The page-flow render handoff would have stopped
working silently at the next regeneration, with no test failing.

THE MANIFEST IS THE DANGEROUS ONE because it looks like data. It sits in data/, it is JSON, and
nothing in the file says it is generated. Before editing ANY file under data/, check whether
something writes it: `grep -rn "<filename>" research/*.py`.

Generated files known so far: data/schema-manifest.json (build-manifest.py); data/base/*.csv and
data/rationale/*.md (load-base.py). The generator must be run FROM the skill directory -- it
writes a relative path and fails silently-ish from the repo root.

## THE DOCX HANDOFF BLOCK HAS BEEN EMPTY SINCE v0.1.0 (found 2026-09-10)
Running `resolve.py --doctype report-long-toc --json` into `ddi.py handoff --format docx` on
PRODUCTION data gives:
    page / TOC heading levels / characterSpacing / palette -> "(not present in this resolution)"
    fonts -> blank;  font sizes -> ": pt  ->  None half-points"
    page flow -> correct (added 2026-09-10)
The handoff block is WHAT THE DOCX SKILL IS HANDED. It is the only path by which any resolved
decision reaches a rendered file. It has shipped with no page size, no fonts and no palette.

Ruled a v0.2 BLOCKER. RELEASE-NOTES v0.2.0 "Fixed" must carry one honest line saying v0.1.0's
docx handoff shipped without page, font or palette values. Bind that into the Packaging brief.

## GENERATED FILES -- do not hand-edit, change the generator
data/rationale/headings.md, cv-regions.md and doc-reasoning.md are WRITTEN BY load-base.py.
headings.md says so on its own second line. A paragraph typed into any of them is destroyed by
the next load. To change their content, change the write_text block in load-base.py -- for
headings.md that is around line 448.

## PHASE B IS DONE -- all seven truth-pass edits landed 2026-09-10
The reuse rule is in the load-base.py generator, so it is REGENERATED each load. The section
orders are merged. The T10 comment block, both CHANGES strings and the resolve.py docstring no
longer make claims that stopped being true when the data loaded. The manifest NOTES document
`distinct_token_columns` and build-manifest.py's docstring is honest about its provenance.
Every number in the new rationale prose is COMPUTED at load time, not typed.

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

HISTORICAL, and the reason phase A was shaped as it was: at the time, headings.csv held 81 rows
over exactly 11 canonical sections, ALL OF THEM CV-ONLY. **As of 2026-09-10 it holds 204 rows
over 52 sections** and every structure row carries an order. The rule below still governs any
FUTURE family:

CONSEQUENCE: a new family needing brand-new canonical sections must have its **headings rows
authored and loaded BEFORE or WITH its Section Orders, never after.** Load a Section Order
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

## *** RULING 2026-09-11: CANDIDATE L IS NEUTRAL-AND-UNFALSIFIED. THE CASE AGAINST IT HAD NO BASELINE. ***
Full record: research/55-candidate-L-verdict.md. Run: research/49-candidate-L-settle.md.

**THE CLEAN RUN.** Activation 11 under L is DOCX-ONLY, on a run where all three preconditions
were verified read-only first: confound re-proven empty, skill confirmed ENABLED (the USER
enabled it; the tester never touched the toggle), installed build confirmed to be L. The only
SKILL.md path in the trace is /mnt/skills/public/docx/SKILL.md; the follow-up names only "the
docx skill"; a real .docx was produced. Invocation-scored, unconfounded.
**The disabled-skill worry is DEAD for this result.** The skill was on and it still did not fire.

**THE BASELINE DOES NOT EXIST.** The case against L was "fired 2/2 under H, docx-only under L".
Those H runs are NOT RECORDED ANYWHERE in research/. The claim appears only as an assertion --
no chat URL, no commands-line capture, no follow-up quote, no date, no scoring method. The
docx-only results ARE properly recorded (48-browser-spotcheck.md:285, in full).
We cannot apply the confound test to the H runs because **we do not know how they were scored.**
An unscorable baseline cannot carry a verdict -- the same rule that makes us refuse an authority
we cannot grep-verify. **That rule binds our own record too.**

**THEREFORE:** L is NOT shown to have caused anything. It is neutral-and-unfalsified and it
STAYS. The revert was SKIPPED by ruling -- it would not have restored a behaviour we have no
record of. Claude's own account already explains the docx-only outcome without reference to L:
a format was named, docx won on its own literal trigger criteria. **That predicts docx-only
under ANY of our descriptions**, which is exactly what candidate M is built to test.

**DO NOT cite "fired 2/2 under H" again.** If you find the primary record, add it here.

## DESCRIPTION LENGTH -- the one measured number
The SKILL.md frontmatter description measures **972 characters**, as of candidate L applied
2026-09-10 (commit f23fb03). The cap is 1023 (the claude.ai UI enforces "under 1024").
**Headroom: 51 characters.**
Confirmed 2026-09-11 by two independent measurements: the orchestrator decoding the file as
UTF-8 and taking .NET String.Length, and the Mechanism Analyst applying the coverage test's own
regex plus Python len(). Both returned 972. Pre-L (f23fb03^) measures 972 as well -- the only
token difference across the whole string is "above" becoming "below".

**MEASURE CHARACTERS, NOT BYTES. The trap that produced a wrong number on 2026-09-11:** the
description holds three two-byte characters -- the é in dépliant, the é in présentation, the ü
in Broschüre -- so a byte count reads 975 and overstates the length by exactly 3. On this
machine `python` does not run (uv trampoline: "entity not found") and **`wc -m` is not UTF-8
aware in this shell and silently returns the byte count.** Use the coverage test's regex with
Python len(), or PowerShell:
    $raw = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    [regex]::Match($raw, '(?m)^description:\s*"(.*)"\s*$').Groups[1].Value.Length

HISTORY, superseded and kept only so old figures are recognisable: 823 before candidate F, 831
after it, 667 in references/activation.md and 825 in skill/dist/POST-UPLOAD-TESTS.md. Every one
of those predates candidate L. **The "831 characters, headroom 192" that stood here until
2026-09-11 was stale by two candidates and should not be quoted again.**
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

## STEP 9 -- DONE in v0.2, kept for the reasoning. THE COUNTS BELOW ARE HISTORICAL.
All 17 structure rows carry a Section Order as of commit aec56f4. headings.csv is 204 rows over
52 canonical sections. What follows describes the state that MOTIVATED the work, not today's.

### Original ruling, 2026-09-09 (AFTER v0.1.0): headings for the other 14 doc classes
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
- AionUi Butler             01a07a84-e27e-7b92-80e1-ad082022257e — REMOVED FROM THE TEAM by the
  user on 2026-09-09, deliberately. NOT on the team_members roster; messages to it FAIL. No
  replacement is needed or wanted. Do not respawn it. If you need AionUi configuration work,
  raise it with the lead.
- Acceptance Tester         01a08f33-d70b-7d71-b6d8-9c67574e29d8 — BROWSER ACCESS to the
  user's claude.ai account. Runs acceptance prompts in the real harness so routing results
  are ground truth instead of hand-testing. Same rules as every worker: file-first briefs
  (research/brief-tester.md), clear its context after EVERY task, never let it run git.
  BROWSER ATTACHMENT — the gotcha that cost an hour on 2026-09-11: its browser tools fail with
  "The in-app browser is not currently attached" until the user opens the browser panel INSIDE
  THE ACCEPTANCE TESTER'S OWN CONVERSATION. The panel binds PER CONVERSATION. Opening it in the
  main window or the lead's window does NOT attach it, and produces the identical error, which
  reads like a dead capability but is not.
  Corollary, also learned the hard way: team_describe_assistant lists SKILLS, not TOOLS. An empty
  skill list is NOT evidence an assistant lacks browser tools. The error text coming FROM a
  browser tool is proof the tool exists.

## COLD START, 2026-09-11 (evening): WHERE THE PROJECT ACTUALLY IS
**v0.2.0 IS PUBLISHED. NOTHING IS IN FLIGHT. No task is open. All workers idle.**
Two releases shipped: v0.1.0 (CV section guidance only) and v0.2.0 (all 15 families, page flow,
the docx handoff fix). Gate 424 rows over 14 tables, 159 tests plus 32 subtests.

### V0.3 STARTS HERE. Do these three, in this order.
**1. SETTLE CANDIDATE L. -- DONE 2026-09-11. L STAYS.** Clean run: activation 11 is docx-only
   under L, skill confirmed ENABLED, confound proven empty, invocation-scored. The "fired 2/2
   under H" baseline turned out to have NO PRIMARY RECORD, so the case against L never existed.
   L is neutral-and-unfalsified; the revert was SKIPPED by ruling. See the candidate L ruling
   section below and research/55-candidate-L-verdict.md. Do not reopen this.

**2. DRAFT THE FILE-NOT-GENRE CANDIDATE. -- DONE 2026-09-11. This is CANDIDATE M.**
   research/50-candidate-M-draft.md. It edits the DEFERRAL SENTENCE, not the trigger list:
   "even as Word or PowerPoint" -> "even for '.docx'/'.pptx' requests naming Word or PowerPoint".
   1005 chars, cap 1023, headroom 18. Sourced from P6, where Claude named the competing skill's
   literal '.docx' token as the deciding signal. Falsifiable by re-running activation 11 VERBATIM.
   A first draft that inserted a Triggers example was REJECTED as refutation-chain item 2 rebuilt.
   **REFUTED 2026-09-11 -- DOCX-ONLY, identical to L.** Tested clean: build verified installed,
   skill enabled, confound empty, prompt re-run VERBATIM. Killed by its own pre-registered
   falsification test. See refutation chain item 6 and research/60-candidate-M-refuted.md.
   DO NOT APPLY M TO THE REPO.
   If applied to the REPO, it needs a paired NEGATIVE_HEAD_MARKER edit; the shipped ZIP has no
   tests, so the test artefact needed none.
**3. THE INVOKED-QUALITY PASS. -- DONE 2026-09-11.** research/51-invoked-quality.md, 7 defects
   ranked, ZERO "not in my library" refusals across 6 families / 11 prompts. It found the P0
   below, which the lead then put at the TOP of the v0.3 critical path.

### *** THE v0.3 CRITICAL PATH NOW STARTS HERE: THE DROPPED-COLUMNS P0 ***
v0.2.0's headline -- 204 heading rows in three languages -- REACHES NO OUTPUT PATH. Resolved
entries carry the union of keys ["key"] and nothing else; the docx handoff for a UK CV contains
ZERO authored wordings; the plain-text path prints bare ids too. CONFIRMED ON THE PUBLISHED
ASSET, not a dev build (research/53-defect-verification.md). Ruled ahead of ALL description and
activation work. In progress with Packaging; THREE parts, not two -- see that brief, because
ddi.py's HANDOFF_VOCAB has no headings/structures entry at all and parts 1-2 alone would give a
green test and an unchanged Word document.

### WHAT CHANGED ON 2026-09-11 — read before you touch activation
The day's work was browser acceptance testing, and it overturned things.
- **The account's custom instructions were a CONFOUND.** They told Claude to ask before acting
  on anything ambiguous and to keep answers short. Results SCORED ON THE SHAPE of a reply are
  RETIRED (labelled in place, not deleted). Results where CLAUDE NAMED THE SKILL IT USED STAND,
  including the whole description-candidate refutation chain. See "WHICH OLD RESULTS SURVIVE".
  The user switched them off for one clean run and has been asked to restore them.
- **THE HANDOFF DESIGN WORKS.** Observed live: our SKILL.md then /mnt/skills/public/docx/SKILL.md.
- **docx and pdf ARE real skills** at /mnt/skills/public/, loaded inside the code-execution
  capability. Absent from the Settings list is NOT absent from the system.
- **EN prose is not dead.** The EN memo FIRED for the first time on a clean account. FRENCH
  prose still failed 0/2 clean, so the French limitation stands on its own.
- **Detection method:** the SKILL.md paths in the expanded "Ran N commands" line are PRIMARY
  evidence. The follow-up question "Which skills did you use for this request, and why?"
  corroborates WHICH skill, but Claude's prose about DETAILS can be inexact. Capture both.

THE ONE THING A NEWCOMER MUST NOT REDO: the activation/routing problem. Five description
changes were applied and none moved EN/FR prose-genre activation. Nouns, trigger phrases,
artefact-versus-genre and ordering are all dead — see the refutation chain. The workaround
ships in the release notes and README: add "Use the document-design-intelligence skill." to the
request. **The file-not-genre mechanism above is the ONLY live lead. Everything else is closed.**
SCOPE: the problem is PROSE GENRES (letter, report, proposal) in FRENCH. The EN memo now fires
and CV prompts fire reliably.

### *** THE ACCOUNT DOES NOT HOLD THE PUBLISHED BUILD (as of 2026-09-11) ***
The user's claude.ai account has **CANDIDATE M installed, not v0.2.0.** M is refuted and will
not be applied to the repo, so the account carries a build that exists nowhere in the release
history. **Any browser test that reads "the installed description" will read M** unless this is
corrected. Either restore the published asset or re-verify what is installed before scoring
anything. Reference copy: research/test-builds/_published-v0.2.0-reference.zip,
md5 9e9f30fb08c663686bde842c41dd2c42. Only the USER can change the account.

## BROWSER TESTING — the three rules that cost us a session each
1. **NEVER RELOAD or navigate away mid-trial.** A reload destroyed the accessibility tree and
   killed a whole run; screenshots kept working so it still looked connected.
2. **WAIT 20 SECONDS** after Send on a fresh chat before concluding it failed. The message does
   not render for 10-15s and retyping double-submits.
3. **The browser panel binds PER CONVERSATION** — the user must open it inside the tester's own
   conversation. Any other panel gives an identical "not attached" error.

## LEAD RESUME — for a fresh Workflow Orchestrator LEAD context (read this first)
You are the team LEAD. Your context was cleared on purpose. Do NOT rebuild history.
**As of 2026-09-11 (evening) there is NO work in flight.** v0.2.0 is published and verified.
The day was spent on browser acceptance testing; read the COLD START section directly above for
what it overturned and for the three v0.3 starting items. If you have
just woken with no user request, the correct action is to ask the user what they want next, not
to start something from the backlog.
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
