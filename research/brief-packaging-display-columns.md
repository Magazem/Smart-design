# BRIEF — Packaging Analyst — FIX THE DROPPED COLUMNS (v0.3 critical path, top item)

Deliverable: working code + a real test + `research/54-display-columns-fix.md`.
Ruled by the lead 2026-09-11: this sits AHEAD of all description and activation work.

## THE DEFECT, already verified — do not re-litigate it
v0.2.0's headline feature is 204 heading rows in three languages. **None of them reach any
output path.** Confirmed end-to-end against the PUBLISHED v0.2.0 asset, not a dev build:
resolved `headings` entries carry the union of keys `["key"]` and nothing else; the docx handoff
for a UK CV contains zero of the authored wordings; the plain-text path prints bare ids too.

Full evidence: `research/53-defect-verification.md`, including the ADDENDUM. **Read it first.**
You do not need to reproduce the diagnosis. You need to fix it and prove the fix.

## THE FIX HAS **THREE** PARTS, NOT TWO. This is the whole point of this brief.
The lead's ruling named two. Investigating the generator turned up a third, and without it you
will ship a half-fix that makes the JSON look right while the handoff stays empty — which is
exactly the failure shape this project keeps hitting.

**PART 1 — tables with NO `display_columns` at all.** `headings` and `structures` declare none,
so `resolve.py:_display_columns` falls through to searchable columns plus FK source columns,
which is empty or near-empty. Declare one for each.
- `headings` hides all 4 of its data columns: canonical_section, Heading Text, Language, Is Primary
- `structures` hides 6 of 8: Heading Language, Heading Depth Max, TOC Depth, Front Matter
  Numbering, Caption Position, Cross-Ref Style. **That set IS the section model.**

**PART 2 — tables WITH a `display_columns` that is INCOMPLETE.** Different cause, different fix:
extend the existing list rather than adding one.
- `constraints` declares `["Set Key", "Element Scope", "Parameter"]` and hides **four**: Applies
  To, Check, Threshold, Severity. A rule arrives without what it applies to, what it checks, its
  limit, or whether it fails or warns.
- `type-scales` declares `["Medium", "Role", "Size pt"]` and hides scale_key and Leading Ratio.
  Leading is the one thing this repo genuinely cites Bringhurst for.

**PART 3 — THE ONE THE RULING DOES NOT COVER. `ddi.py`'s `HANDOFF_VOCAB` has no `headings` and
no `structures` entry at all.** I checked: the names it references are page-formats, palettes,
typefaces, type-scales, render-targets and constraints. Exactly six — and the generator's own
comment says the six tables that get `display_columns` "are exactly the six `ddi.py`'s
HANDOFF_VOCAB names."

So `display_columns` alone will put heading wording into the resolved JSON and the plain-text
path, and the **docx/pptx handoff will still print nothing**, because the handoff never looks at
that table. Parts 1 and 2 without part 3 produce a green test and an unchanged Word document.

Decide and justify: does heading wording belong in the handoff block, and in what shape? A
renderer needs the section order AND the wording for the chosen language. Note `headings` rows
carry all three languages (`contact-en-1`, `contact-fr-1`, `contact-de-1`) and an `Is Primary`
flag, so something must select one language and the primary wording. If you conclude the handoff
should NOT carry it, say why and say what should consume it instead — but do not leave the
question unanswered.

## HARD RULES
- **`data/schema-manifest.json` IS GENERATED. NEVER hand-edit it.** The generator is
  `research/build-manifest.py` and its own comment says a hand-added key is wiped on the next
  run. All manifest changes go in the generator, then regenerate.
- **No git, ever.** The orchestrator owns git. Do not commit, branch or stash.
- **NO ZIP REBUILD.** Ruled by the lead: the rebuild waits for step 1's verdict so one rebuild
  bundles everything. Do not run the release build.
- `python` does not work on this machine (uv trampoline error). **Use `python3`** — 3.12.10.
- Tag CONVENTION for anything you cannot grep-verify in this repo.

## THE TEST — this is where the brief is strictest
Ruled: add a test asserting **every authored data column of those four tables reaches the
resolved JSON.** Write it so it fails today and passes after the fix.

**Apply the 2026-09-10 lesson before you write it: ask what your test would say if the feature
produced NOTHING AT ALL. If the answer is "it would pass", it is not a test.** A test that
merely validates rows, or counts them, or checks the manifest declares a key, does not qualify.
It must assert on the RESOLVED OUTPUT.

Do not tune anything to make a check pass. See the 2026-09-09 precedent, refusing the green
tick: when a passing number and a working product disagree, this project fixes the product.

## PROVE IT END TO END
A green test is not the proof. Run and paste the ACTUAL OUTPUT, before and after:

    python3 scripts/resolve.py --doctype cv-uk --json
    python3 scripts/ddi.py handoff --json <that file> --format docx

Show the real heading wordings (Experience, Work Experience, Employment History, Professional
Summary) appearing where bare ids were. If the handoff still shows none after your fix, say so
plainly — that is part 3 unresolved, and it is a finding, not a failure to hide.
Also run the FULL pytest suite and report it green.

## SUB-ITEM, ruled by the lead: the CR loose thread
RESUME.md records the published v0.2.0 asset as having **"Zero CR bytes."** The published
`ddi.py` contains **1209 CR bytes**. I checked one member, not the whole archive, so this is
flagged and NOT asserted. Your job: check the WHOLE archive, correct RESUME.md if the claim is
wrong, and make `build_zip.py` normalise line endings if it does not already. Report what you
find either way.

## DELIVERABLE — `research/54-display-columns-fix.md`
1. What you changed, per part, and why — generator and source file for each.
2. The before/after resolve and handoff output, quoted, not summarised.
3. Your answer on part 3, including the language-and-primary selection question.
4. The test: what it asserts, and your answer to "what would it say if the feature produced
   nothing".
5. Full pytest result.
6. The CR archive finding.
7. A draft RELEASE-NOTES known-limitation entry ONLY if something remains unfixed. If the fix is
   complete, say so and skip it — do not write a limitation for a solved problem.
8. Anything you could not verify.

Report to me in a few lines: parts fixed, handoff carries wording yes/no, pytest green yes/no,
CR finding. Then STOP.
