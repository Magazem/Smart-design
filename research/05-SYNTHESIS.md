# Synthesis — Research Phase Complete
Date: 2026-09-07. Orchestrator-verified claims marked [VERIFIED].

DETAIL LIVES IN THE APPENDICES — this file is the argument, not the evidence:
  01-mechanism.md                 pipeline internals, anti-slop devices, file:line cites
  02-coverage-gaps.md             full coverage matrix, per-row gap causes
  03-document-design-knowledge.md ATS/CV rules, deck+print+report thresholds, FACT vs CONVENTION
  04-packaging.md                 plugin format, claude.ai runtime limits, install path

## Verdict
Worth building. But it is NOT "UI/UX Pro Max for documents." The honest scope is
narrower, sharper, and more defensible than that framing.

## The central finding: canvas vs. flow

One axis explains every gap. Upstream is a CANVAS system — one fixed frame, little text.
Its own source states this outright:
  ui-styling/references/canvas-design-system.md:29  "90% visual design / 10% essential text"
  ui-styling/references/canvas-design-system.md:49  "Never paragraphs"            [VERIFIED verbatim]

Documents are FLOW artifacts — content crosses page boundaries. That single distinction
predicts the entire coverage matrix:
  Works well  (canvas): poster, banner, social image, single slide
  Partial     (hybrid): deck, infographic, letter
  Absent      (flow)  : CV, brochure, long-form report, whitepaper

Repo-wide term counts, independently re-run by the orchestrator:
  @page 0 | page-break 0 | break-inside 0 | @media print 0
  pptx  0 | docx       0 | reportlab   0 | weasyprint   0        [VERIFIED, 0/8 present]

This is not an untuned system. There is no pagination concept anywhere in it.

## What we are actually building
Three missing subsystems, not eight document types:
  1. A PAGINATION / FLOW LAYER   — the hard part; nothing upstream to reuse
  2. A BINARY WRITER             — .docx/.pptx; only needed on one branch
  3. A PRINT GEOMETRY EXECUTOR   — bleed/trim/CMYK exist upstream as prose, never as mechanism
Plus the domain knowledge (report 03), which upstream does not contain at all.

## The output-format fork is premature — do not decide it yet
Counterintuitive and important: print-ready HTML is NOT the cheap branch. Upstream's HTML
is architecturally screen-only (100vw/100vh, position:absolute stacked slides, opacity
toggling, overflow:hidden at four levels). Printing it yields one page.
=> BOTH branches must build pagination. The binary branch merely adds a writer on top.
=> ~70% of the work is shared. Build the flow layer format-agnostically; treat .docx/.pptx
   as a second renderer behind the same content model.

## What we must NOT rebuild (solved upstream, MIT, zero user-visible gain)
Posters, banners, social images, slide visual reasoning, brand-identity generation.
User has confirmed by direct testing that posters + brand adherence already work well.

## Mechanism to clone (and its one flaw)
Anti-slop works via deterministic machinery, not model taste:
  - html-token-validator.py hard-fails on hardcoded hex/rgb/font outside an allow-list
  - contrast-safe "On Primary/Secondary" colors are WCAG-luminance-DERIVED in code, not hand-picked
  - style selection is a closed-form tie-break (BM25 + rerank), not free model choice
  - checklists are baked into generator OUTPUT, not left as instructions to follow
FLAW: the generate-then-inherit loop the user values most is CONVENTION, NOT CODE.
design_system.py writes MASTER.md; SKILL.md merely tells the model to read it next time.
Repo-wide grep: zero hooks, zero automation. Cheap to clone — but it cannot work by file
persistence in claude.ai, whose container is ephemeral. Our inheritance mechanism must be
re-architected (leading hypothesis: generate an installable skill, not a file).

## Delivery surface — settled
Scripts DO execute in claude.ai (bash + filesystem). Only stdout enters context.
=> mechanical validators are viable; the anti-slop premise survives.
Sourced from Anthropic docs fetched 2026-09-07, which gate this on code execution being
enabled (stated there as Pro/Max/Team/Enterprise). Treat the TIER DETAIL as doc-sourced and
liable to change. The CONCLUSION does not rest on it: the user has already run this class of
skill successfully in the app, which is stronger evidence than any doc page.
Loading is 3-tier: description (~100 tok, always) -> SKILL.md body (on activation) ->
bundled files (on demand, free until touched).
Design consequences:
  - Thin router SKILL.md + references/. Upstream's 658-line monolith is ~30% over
    Anthropic's own stated budget. Do not clone it.
  - Ship a PRE-ZIPPED GitHub Release asset. Upstream documents NO claude.ai install path;
    both of theirs are terminal-only. claude.ai install = Settings > Skills > Add > upload zip.
  - No symlinks in our repo (upstream's are broken on this Windows checkout).
  - ONE canonical description. Upstream maintains four, already out of sync.
  - Assume stdlib only; network access in-container is not guaranteed.

## License posture
Upstream MIT (c) 2024 Next Level Builder. Clone SCHEMAS and MECHANISMS (ideas, not
copyrightable); derive all row content independently. Named temptation: the slide-*.csv
decision tables (small enough to paste — do not). Check ui-styling/ separately: it ships
its own LICENSE.txt + 40 OFL fonts.

## Blocking unknowns — all settled by user testing, none by more reading
  T1  import pptx / import docx in the claude.ai container   -> decides binary feasibility
  T2  Does CSS Paged Media (@page, forced breaks) survive the app's PDF export?
      One 3-page test artifact answers it. -> decides the whole flow-layer architecture
  T3  Does a generated design system survive into a FRESH session? (expect NO)
      -> confirms inheritance must be re-architected
  Q1  User's company-voice plugin: was it a file to re-read, or an installable artifact?
      -> if installable, that IS the persistence mechanism and is better than upstream's
  Q2  How does the poster path reach PDF today? No renderer/screenshot/PDF lib found
      under that skill. -> tells us what our export story can assume

## Recommended next phase — RUN THE TESTS, DO NOT PICK A SLICE YET

T2 gates the flow layer's entire architecture and must be answered first:
  - If CSS Paged Media SURVIVES the app's PDF export -> the flow layer is a
    stylesheet + validator problem. Modest build.
  - If it does NOT survive -> it is a compositor problem. A materially different,
    larger build.
Choosing a vertical slice before T2 answers means choosing before we know what we are
building. Run T1/T2/T3 first; they are cheap and none require more reading.

Slice recommendation, CONDITIONAL on T2:
  - T2 passes -> CV. Hardest constraints, sharpest pass/fail test.
  - T2 fails  -> do NOT start with CV. Start on the canvas side we know works.
    Cheapest candidate: INFOGRAPHICS is an abandoned scaffold upstream, not a missing
    feature — html-token-validator.py:29 reserves assets/infographics and :277 reserves
    the --type infographics CLI flag, with no generator behind either. [VERIFIED]
    "Finish it" is a smaller job than "build it."

THE CV CAVEAT, either way: ATS wants plain semantic structure; this system's whole
value-add is token-driven visual richness. Those pull in opposite directions. It needs a
restraint mode and dual output from one content model. That tension is the project's real
design problem — which is also why CV is a poor choice for proving the mechanism works: a
struggling slice would not tell us whether the flow layer is wrong or whether we picked
the one artifact that fights it.

================================================================================
## FIELD EVIDENCE — 2026-09-07, from the user's live ENS-customised instance
Reported by the Claude instance running the modified plugin. This CONFIRMS
report 01's code-level finding from the inside, and REFINES it in one key way.

Q1 IS ANSWERED. The "company-voice plugin" was: one ENS brand-guideline file
(green/brown/lime, Manrope/Inter, voice, imagery) + a paragraph prepended to each
skill saying "read this file first, use ENS as default." It IS an installed
artifact, so it DOES persist. Persistence was never the problem.

THE REAL DIAGNOSIS, in its own words:
  "The identity is an instruction, not data."
The BM25 search still returns GENERIC results (navy palette, Garamond) because
ENS is not IN the searchable database. The brand file then tells the model to
override that afterwards. So the system never generates ENS designs — it
generates generic ones and the model patches them by hand, and every patch is a
judgment call. That is the drift.

=> CORRECTION to this synthesis's earlier framing: the inheritance flaw is NOT
   primarily a persistence problem (ephemeral container). It is a RETRIEVAL
   problem. The brand is installed but sits OUTSIDE the retrieval index, as an
   override instruction layered on top of generic search results.
=> ARCHITECTURAL CONSEQUENCE: our inheritance mechanism must inject brand INTO
   the retrieval path so search returns brand-correct rows natively — not
   alongside it as prose the model is asked to remember to apply.

SECOND FAILURE MODE, unprompted and equally important:
  "I skipped the plugin entirely twice."
On two of three deliverables it read the brand file and built directly, never
invoking any skill or search. The plugin contributed only the color list.
=> This is an ACTIVATION failure, not a content failure. More rules in a file
   the model does not consult change nothing. Fixing it is mechanical: the
   `description` field is the only activation lever (report 04).

THIRD, CONFIRMS CANVAS-VS-FLOW BY EXPERIMENT:
  PDF "fiche intervention" -> good.  Word document -> "wasn't great."
Same brand, same operator, different artifact class. Matches the axis exactly.

WHAT THE IDENTITY DOES AND DOESN'T COVER (its own account):
  Covered   : palette, fonts, French voice — used on every deliverable
  NOT covered: layout, hierarchy, how much color, table style
  "the plugin's generic rules filled the gap inconsistently"
=> That uncovered list IS our product. Per-document-type layout/hierarchy/table
   rules for FLOW documents is precisely the gap reports 02 and 03 identified.

================================================================================
## T2 RESULT — 2026-09-07 — PASS, with a decisive bonus
3-page ENS note, HTML -> PDF, in the user's claude.ai container.
  Page count   3, A4 595x842pt                          PASS
  Forced breaks each SECTION opened its own page          PASS
  Table        header + 6 rows intact on p.2             PASS
  Footers      "Page X / 3" via counter(pages), all 3    PASS

THE BONUS: rendered with WEASYPRINT. wkhtmltopdf also present but its old WebKit
"handles @page margin boxes poorly" (its words). WeasyPrint is a full CSS Paged
Media engine — @page, margin boxes, counter(pages), break-inside all native.
=> The flow layer is a STYLESHEET + VALIDATOR problem, not a compositor. The
   small-build branch. Report 02's fork recommendation now has its answer.
=> Design consequence: target WeasyPrint explicitly; do not write for wkhtmltopdf.
   Verify availability is stable, not incidental (open: is WeasyPrint in the
   default container image, or was it pip-installed on the fly?).

CAVEAT observed in the same run: prompt said "Use the ENS brand"; the model
INVENTED an ENS green (#2E7D32) and guessed the running-header text, then asked
for the real codes afterwards. Third occurrence of the activation/retrieval
failure — it did not consult the installed brand file even when told to.
T1 (import pptx / docx) NOT yet reported.

================================================================================
## T1 RESULT + WEASYPRINT PROVENANCE — 2026-09-07
T1  PASS. python-docx, python-pptx, docx, pptxgenjs all importable in the user's
    claude.ai container. => real editable Office output is on the table. Both
    branches of the fork are now technically open; the flow layer is still built
    format-agnostically first (report 02 recommendation stands).

WEASYPRINT WAS NOT PREINSTALLED. Only wkhtmltopdf was on the image. The model ran
`pip install weasyprint` (got 69.0) during the task because wkhtmltopdf handles
`break-inside: avoid` unreliably. That install is session-scoped.
=> Design consequences for the open-source skill:
   - Network/pip is NOT guaranteed (report 04). Do not hard-depend on WeasyPrint.
   - Need a documented fallback chain: WeasyPrint (pip) -> headless Chrome
     print-to-PDF (same CSS, availability unverified) -> wkhtmltopdf (present,
     but avoid break-inside reliance).
   - OPEN: is headless Chrome present in the container? One-line test.
   - The stylesheet itself is portable across all three; the ENGINE is the
     variable. Keep pagination logic in CSS, not engine-specific code.

================================================================================
## PDF ENGINE — SETTLED 2026-09-07
Headless Chromium IS preinstalled in the claude.ai container: /opt/google/chrome/chrome
(Chromium 141.0.7390.37, Playwright build). Not on PATH — use the absolute path.
Tested on the 3-page note: 3 pages, A4, forced breaks honoured, @page margin boxes
render, counter(pages) footers correct. Output matched WeasyPrint byte-for-purpose.

Working invocation (verified):
  /opt/google/chrome/chrome --headless --no-sandbox --disable-gpu \
    --print-to-pdf=out.pdf --no-pdf-header-footer file:///path/to/doc.html
  --no-pdf-header-footer is REQUIRED or Chrome adds its own date/URL header over ours.
  D-Bus errors on stderr are harmless (no session bus).

=> ENGINE DECISION for the open-source skill:
   PRIMARY   headless Chromium — preinstalled, zero network, full CSS Paged Media
   OPTIONAL  WeasyPrint — only if pip is available; same stylesheet
   AVOID     wkhtmltopdf — present but old WebKit, break-inside unreliable
   Pagination stays in CSS; engine is a one-line swap. No compositor to build.
   Note: Chromium 141 handles @bottom-center + counter(pages); older Chrome did
   not. Pin the expectation, not the version.

## ENS [À valider] DECISIONS — user, 2026-09-07
  #1 Brown   -> A: secondary category marker in documents (two-kind tables, service labels)
  #2 Lime    -> never as text; filled badge only (research)
  #3 Word    -> Arial (research)
  #4 Fields  -> underline
  #5 Social  -> portrait 1080x1350 default; square on request
  #6 Types   -> no additions for now

================================================================================
## THE LIBRARY IS WEB-SHAPED — scope finding, 2026-09-07 (user-prompted, orchestrator-verified)
Column headers, read directly from src/ui-ux-pro-max/data/*.csv:
  products     Landing Page Pattern | Dashboard Style (if applicable)
  styles       Framework Compatibility | CSS/Technical Keywords | Mobile-Friendly |
               Conversion-Focused | Light Mode | Dark Mode
  typography   Google Fonts URL | CSS Import | Tailwind Config
  colors       Card | Ring | Destructive  (shadcn/ui token names)
  ux-guidelines Platform | Code Example Good | Code Example Bad
Rows: 161 product types; 76 mention landing/dashboard/SaaS/app; 13 mention
print/document/brochure/CV/report.

No column exists for: page format, margins, measure, running heads, bleed, paper,
ATS-safety, font-embedding licence, print contrast. These are missing QUESTIONS,
not missing rows. Inserting a brand into this library yields correct colours and
fonts, then every subsequent decision the engine can make is a web decision.

=> ENS pilot proves the MECHANISM (brand-as-data, activation, per-type routing,
   hard-fail validators). It does NOT prove the LIBRARY; ENS's document rules
   live in a prose file outside it — a workaround, not an architecture.
=> Open-source scope is three layers:  their mechanism (clone)
                                       our library   (build — THE product)
                                       our validators (build)
=> Report 03's thresholds are the raw material for the library's columns.
=> NEXT (pending user go): design the document-library schema. Independent of v3.

================================================================================
## VERSION SKEW — 2026-09-07 — MATERIAL CORRECTION TO REPORTS 01, 07, 08
Local checkout analysed by all researchers: v2.5.0, git b7e3af8, 2026-04-03.
User's installed plugin in claude.ai:          v2.13.0 (per rebuild report).
Claims from the rebuild report that are ABSENT in v2.5.0 and therefore could not
have been checked by our reviewers:
  - styles.csv has 29 columns incl. Style ID, Aliases, Status, Parent Style ID
    (v2.5.0: 22 columns; grep for these in local core.py: zero hits)
  - core.py:21 searches "Style ID"/"Aliases"; core.py:740-748 follows Parent/Replacement ID
  - design_system.py:385 parse_decision_rules + apply_decision_rules
  - scripts/reasoning_contract.py CONDITION_SIGNALS — a FIXED dict of evaluated keys
  - scripts/validate_data.py, data-provenance.json, catalog-summary.json
CONSEQUENCES
  - Report 07/08 "Decision_Rules is never evaluated" -> TRUE for v2.5.0, FALSE for
    v2.13.0 where a fixed built-in key set IS evaluated. Custom keys still never
    fire. The fix applied (UI_Category + Style_Priority) is correct either way.
  - Report 07/08 "Style ID/Parent columns do not exist" -> TRUE for v2.5.0 only.
  - Orchestrator's statement to the user that their Claude "confabulated" these
    two items was WRONG. It was reading a newer version. Retracted.
  - The upstream mechanism has evolved materially since April: it now has a data
    validator, provenance, executed decision rules. Report 01 must be refreshed
    against CURRENT upstream before we clone anything. Cloning v2.5.0 would clone
    a mechanism upstream has already superseded.
STATUS: rebuild report items R1/R3 VERIFIED by its own tests (char counts per
skill; wrapper exit 1 demonstrated). Acceptance test NOT yet run.

## MECHANISM REFRESH LANDED — research/10-mechanism-refresh.md
Current upstream v2.13.0, HEAD 4aad0584, 2026-09-06 (shipped YESTERDAY). All six
rebuild-report claims CONFIRMED. Superseded findings listed in its §7. Key deltas:
  - Decision_Rules execute via 32-key CONDITION_SIGNALS allow-list; unknown keys
    RAISE, uncaught at runtime -> a bad key crashes live search. Always run
    validate_data.py before shipping. ENS build used built-in keys only: SAFE.
  - validate_data.py hard-fails WCAG <4.5:1 on On-colours -> supersedes 2.8.
  - _find_reasoning_rule exact-match only -> key identity is now hard, not soft.
  - MASTER.md still never read back -> inherit-is-convention finding STANDS.
  - design.csv gone; Windows symlink issue fixed; version drift across manifests fixed.
Cadence signal: ~8 minor versions in 5 months. Anything we clone goes stale fast;
we clone PATTERNS, not code, and pin the version we studied in our docs.

## VERSION LABEL CORRECTION — from research/11-upstream-releases.md (fetched live via gh api)
The "v2.13.0" label is a STALE MANIFEST FIELD, not the installed code version.
  - Latest tag: v2.15.0 (2026-08-13). main HEAD 4aad058 (2026-09-06) is +24 commits, no new tag.
  - reasoning_contract.py, CONDITION_SIGNALS, data-provenance.json, catalog-summary.json,
    the 29-column styles.csv and Style-ID search all arrived in ONE release: v2.15.0,
    commit a38d04c "feat(search): overhaul relevance and curated design data".
    Confirmed ABSENT at tagged v2.13.0 by direct file diff. validate_data.py is
    older (v2.11.1, commit f8ac5e1) and IS at v2.13.0.
  - Why the label lies: upstream's bump-versions.yml (PR #439) opens a PR per release;
    only ONE was ever merged (#438 -> 2.13.0). skill.json / plugin.json /
    marketplace.json on current main STILL read "2.13.0". Upstream bug.
  => The user's Claude read the manifest honestly and got a wrong number. Its file
     observations were correct: the installed code is v2.15.0-or-main.
  => Our upstream-latest clone is main HEAD 4aad058 — report 10 is against the RIGHT
     code. No rework needed. Only the label in the VERSION SKEW section above is wrong.
  => RULE: never trust a version field from this repo. Identify by commit SHA or by
     presence of reasoning_contract.py.
Other closures:
  - Report 04 open question on colon-namespaced skill names: RESOLVED upstream —
    renamed colon->hyphen in v2.6.x (#383). Use hyphens.
  - No claude.ai install asset at ANY version through v2.15.0 (assets: [] on every
    release). Our pre-zipped Release strategy is still a genuine gap-filler.
  - Cadence: 25 releases in 156 days, ~1 per 6 days, bursty. Shelf-life of any
    cloned reference: days to two weeks. Re-verify against main immediately before
    implementation, not against cached research — including ours.

================================================================================
## PHASE 2 SCHEMA LANDED — research/09-library-schema.md (895 lines, complete)
11 tables. Spine doctypes -> doc-reasoning; payload doc-styles/palettes/typefaces/
type-scales/page-formats; enforcement render-targets/constraints/structures/figures.
Three have NO upstream analog (page-formats, render-targets, constraints) = the
missing questions.
ACCEPTED DEVIATION from brief: explicit foreign keys (Style/Palette/Typeface Key)
with biased BM25 only as fallback. Rationale holds: ENS already pins every value by
hand because the re-search is a heuristic; for documents, same input must give same
margins twice. One fuzzy step (doctype), then key resolution.
THREE DESIGN RULES (each from an observed upstream failure):
  1 no cell contains logic   2 every column is searched / a key / feeds a named
  validator (28 listed)      3 linkage keys are slugs, never display text
BRAND AS DATA: Brand Scope column; two-pass resolution (brand subset -> generic).
Plus validate-brand-resolution: brand active + no brand row resolved => refuse to
emit. Targets the only defect observed in the field (3 skips, invented #2E7D32).
FORK AS DATA: render-targets.csv. Font Rule x typeface DERIVES "Manrope embedded in
PDF/PPTX, Arial in Word" — nothing restated per doc type.
HONEST FLAG: Supports Bleed/CMYK = no on every render row => professional print
mode hard-fails preflight by design. Refusing beats shipping RGB called press-ready.
COST: ~600-900 sourced rows. "The schema is a week. The library is months."
STATUS: analyst paused after delivery (undeliverable queue, likely context limit);
context cleared, work safe on disk.
DISPATCHED: DDR -> type-scale tuples + stdlib fsType (research/12). Butler -> create
Print Production Specialist (Sonnet) for T7/T9 professional-print values + the
press-ready vs shop-submittable ruling.
DECISIONS FOR USER: brand install model (Q4); Chromium stability on fresh container (Q3).

## research/12 LANDED — type-scale tuples + fsType (Document Design Researcher)
- T6 type-scales SHRINKS from ~200 rows to ~4 SOURCED rows. Report 03 has NO
  absolute print point-size floor; its print rules are RATIOS (45-75 CPL, 120-145%
  leading). Print sizes are brand-authored constants validated by the CPL/leading
  FORMULA (T5 x T6 x T7 join), not looked up. Only projection (24pt body, 18pt dense
  callout, 36-44pt title) and screen (18-20pt body) have real numbers.
- Photocopy is NOT a size medium; it is a colour/weight problem (mid-L* ink reads
  grey). CUT photocopy from T6 Medium; move to T9 as a colour constraint.
- fsType IS readable stdlib-only (fixed-offset uint16 in OS/2). Function written and
  run on 6 real fonts, TTF+OTF. Embedding Licence column RETURNS as a real preflight.
- tnum via GSUB: presence => yes; absence => UNKNOWN, never no (Consolas disproof:
  monospaced, no tnum tag, digits already tabular). Has Tabular Figures becomes
  yes/unknown; a true "no" needs glyph-width comparison — not built.
- Tooling note: repo venv python is broken (uv trampoline); use
  %LOCALAPPDATA%\Microsoft\WindowsApps\python3.exe. Explains the earlier heredoc failure.
=> Authoring estimate drops: T6 ~200 -> ~4 sourced + per-brand constants.

## research/13 LANDED — schema vs current mechanism (Mechanism Analyst)
NOTE on its opening flag "there is no v2.15.0": it read the manifest field, which
report 11 proved is stuck at 2.13.0. HEAD 4aad0584 IS v2.15.0+24. Review content is
against the correct code; only the label is wrong. Rule stands: identify by SHA.
1. §0.2 is STALE: current core.py short-circuits to exact-identity dict lookup
   (Style ID / Category / Aliases) BEFORE BM25, and BM25 now ABSTAINS on low
   confidence (score floor / coverage / margin) instead of returning a weak guess.
   "BM25 over search_cols" now describes the fallback, not the primary path.
2. The schema's FK-with-fallback DEVIATION is ALREADY SHIPPING upstream for styles:
   _select_best_match tries _resolve_style() (dict lookup, deprecation-chain walk)
   first, BM25 second. Proven by existence; no hidden cost to MASTER.md or validator.
   Caveat: style-only. Palette Key / Typeface Key EXTEND beyond upstream.
3. RECOMMENDATION (adjudicate in revision): build a closed DOC_CONDITION_SIGNALS
   vocabulary (if_hand_filled, if_photocopied, if_projected, if_ats_target,
   if_professional_print...) with upstream's hard-fail-on-unknown-key parser. This
   CONTRADICTS schema Rule 1 ("no cell contains logic"). Analyst's case: Rule 1's
   real danger is UNTYPED logic; a closed validated vocabulary is the same discipline
   as an enum. Orchestrator leans ACCEPT; Coverage analyst to respond in revision.
4. Validator precedents: ~10 of 28 have upstream precedent (validate-keys,
   contrast math, allow-list greps); 18 are NET-NEW (pagination, bleed, fold, ATS,
   embedding, print contrast, density, section order). Matches report 01 Gaps.
5. FACTUAL ERROR in T2 (lines 231-234) + Rule 1: cites "Decision_Rules is inert"
   from the superseded v2.5.0 finding. Must be corrected in revision. Distinguish
   "custom keys never fire" (true always) from "nothing fires" (old version only).

## research/15 LANDED — distribution model (Packaging Analyst)
RECOMMENDATION (adopted pending user objection): OVERLAY at runtime + SCRIPTED
REGENERATION for distribution. claude.ai's persistence unit is the whole uploaded
ZIP; there is no partial-update path, so SOMETHING must rebuild the package on any
base or brand change. The design question was who — answer: a bundled script.
  - Overlay feasible stdlib-only. ZIP-root rule governs top-level nesting only.
    resolve.py merges base/*.csv + brand/<slug>/*.csv internally, prints ONLY the
    resolved decision (stdout is the only channel into context). Key collision =
    hard fail at load, never silent override.
  - Update story (4 user actions, no local tools): upload base v2 (wipes baked-in
    brand) -> attach saved my-brand-kit.zip in a fresh chat -> bundled
    merge_brand_kit.py re-zips base+brand -> upload that.
  - ONE description (SKILL.md frontmatter). plugin.json/marketplace.json only if a
    Claude Code listing ever happens, GENERATED from SKILL.md at build time.
  - Release pipeline YAML: validate_data.py BEFORE zip, fail-closed; version derived
    from git tag and stamped into VERSION + SKILL.md in the SAME job. No second
    workflow, no PR to forget (upstream's bump-versions.yml failure mode).
  - Security: merge_brand_kit.py unpacks an untrusted ZIP -> zip-slip guard + slug
    sanitisation before any path join. Never bare extractall().
  - Colon-namespace question CLOSED: upstream shipped it and reverted (PR #383).
UNVERIFIED, each with a one-line test in the report (user must run in claude.ai):
  (a) do script writes mid-session survive into a NEW chat? Assumed NO (cf. T3).
      If YES, the re-zip dance is unnecessary — test BEFORE building.
  (b) is a chat-attached file visible to a bundled script's cwd?
  (c) ZIP file-count / size ceiling — none documented.

## research/14 LANDED — print production values (Print Production Specialist)
RULING: three tiers, not two.
  1 print-shop-submittable RGB  — honest, shippable today on EVERY T8 target incl. Chromium
  2 PDF/X-4 with RGB + sRGB output intent — REAL middle tier. WeasyPrint >=67
    (--pdf-variant=pdf/x-4 --output-intent=srgb). Structurally valid PDF/X-4, no CMYK
    conversion, free sRGB profile. Caveat: DeviceRGB transparency groups — fine for
    RGB intent per bug report; untested against a validator in the sandbox.
  3 full CMYK press-ready — still hard-fails on every current row; would need
    WeasyPrint >=67 + a bundled CMYK ICC asset (packaging decision).
  NOTE: tiers 2-3 depend on WeasyPrint = pip = network, which is NOT guaranteed
  (report 04). Chromium (preinstalled) reaches tier 1 only. Promise tier 1 by
  default; offer tier 2 when pip succeeds.
T8 IS STALE for pdf-weasyprint: bleed since v0.41 (2017), CMYK+PDF/X+ICC since
v67.0 (Dec 2025); current pip gives v69.0. Supports Bleed/CMYK = no is wrong on
that row only. Specialist did NOT edit T8; routed to schema revision round 2.
L* FLOOR: report 03's 40-50 confirmed as "convention, no standard" — formal print-
legibility standard confirmed ABSENT. ADA/ANSI signage LRV is wrong domain + wrong
unit. RECOMMENDATION: drop print-l-delta; re-express as WCAG relative-luminance
ratio (4.5:1 / 3:1) computed on T4's RGB hexes at BUILD time — every target is RGB
end-to-end anyway; script-checkable, no PDF inspection.
~55 values: ~40 FACT/named source, ~15 tagged convention / depends-on: shop.
Stdlib-checkable in a Chromium PDF (re+zlib on decompressed objects): font-
embedding presence, raster DPI-at-placed-size (header dims x transform matrix).
Most other pro-print checks: structurally "no" (the boxes/intent don't exist).

## research/16 LANDED — FIRST REAL LIBRARY ROWS (Document Design Researcher)
research/16-t9-constraints-draft.csv: 38 constraint rows (non-print). 7 REFUSE (ATS
structural FACTs + PPTX embedding), 31 WARN (conventions). Versus the 80–120
estimate: 7 rules already owned by T5/T8/T10 validators (not duplicated); 10 rules
genuinely not mechanically checkable, listed advisory-only rather than faked.
=> Estimate drops. The "sourced not plausible" discipline held.
ORCHESTRATOR RULINGS (sent to schema revision):
  - T9 rows BIND validators (defined once in §4) to a scope + severity; they never
    define checks. Font-embedding stays in T9 as a binding of validate-font-embedded.
  - print-l-delta and print-legibility-l-delta both superseded by ONE WCAG-ratio row
    (4.5:1 / 3:1 on T4 hexes, build time). Set Key print-legibility.
  - Sourced CSV beats illustrative examples: proj-body-floor = WARN; deck density
    threshold = 6 (ENS's 5 is a brand row); photocopy-body-min DROPPED ->
    photocopy-safe-color (text L* <= 15, label/legal roles).
Weakest-provenance rows, self-flagged: legal-text-min-size (8pt) and
legal-text-no-sustained-uppercase — judgment calls from the ENS review, tagged so.
Print constraint rows come from research/14 §3 (specialist) — merge in revision.

## SKELETON BUILT — skill/ (Packaging Analyst) — not yet a git repo by design
ZIP root: skill/document-design-intelligence/. release.yml single-job (validate ->
tag-derived version stamp -> zip -> Release asset; fail-closed). merge_brand_kit.py
~250 lines stdlib: 2-layer zip-slip guard, slug ^[a-z0-9-]+$, allow-list
(brand.md, data/*.csv, assets/**), file-level collision refusal, one-line stdout,
exit 1 on refusal. Tested against 5 fixture kits incl. traversal, bad slug,
disallowed file — all refused correctly. Em-dashes stripped from strings (codepage
safety). scripts/README-tests.md = 5 paste-ready claude.ai tests for the user.
OPEN: LICENSE copyright holder is [PROJECT OWNER] placeholder — user must supply.
DISPATCHED: SKILL.md activation description (<1000 chars, triggers in first 200,
EN + FR + DE document nouns, quality-complaint triggers, explicit non-UI boundary)
+ thin-router body structure + 10-prompt activation test -> references/activation.md.

## LANDED TOGETHER — description, CV assets, consolidated test sheet
ACTIVATION DESCRIPTION shipped into skill/.../SKILL.md: 667 chars, EN+FR+DE nouns,
quality-complaint triggers, explicit "not for web/app UI (use UI/UX Pro Max)" boundary.
First 200 chars = all EN nouns + "note interne". HONEST FLAG: a hard 200-char cap
LOSES the UI/UX Pro Max boundary -> over-fire risk on web UI. Three alternates in
references/activation.md (EN-first / multilingual-first / complaints-first). Test 2
(description cap) picks. 10-prompt activation test list included.
CV ASSETS (research/18-*): 28 region x band rows (US EEOC negative-signal vs Gulf
customary = the two cells proving no universal template); 80 headings EN/FR/DE;
15 rejected-heading fixtures. FINDING: DACH "tabellarischer Lebenslauf" two-column
tradition CONFLICTS with ATS no-column rule -> resolver default ATS-safe structure
with DACH content. Seniority collapses to early vs experienced (no source for more).
Placement recs routed to revision: own FK'd tables (cv-regions, headings), not T1/T10 cells.
TESTS-FOR-USER.md at project root: 10 tests, decision-impact order, payloads diffed
verbatim against sources, fresh-conversation grouping, results table.

================================================================================
## USER TEST RESULTS — 2026-09-07 (round 1)
T-persist  FAIL (expected): each session gets a FRESH filesystem; files persist only
           within one conversation unless downloaded. => the scripted re-zip flow
           IS necessary. Distribution design (research/15) CONFIRMED.
T-attach   PARTIAL, decisive: attached files are NOT in a script's cwd; they are at
           /mnt/user-data/uploads/<name> (read-only, fixed mount). A bundled script
           sees them only by absolute path. => merge_brand_kit.py must read from
           that mount and write the merged ZIP somewhere downloadable.
T-chromium PASS: /opt/google/chrome/chrome present on a fresh container.
           => T8 pdf-chromium Availability = preinstalled. Primary engine confirmed.
T-ENS-activation  PASS. « quel skill as-tu utilisé ? » -> "ui-ux-pro-max:brand,
           ui-ux-pro-max/scripts/ens-search.sh, docx" in that order. The skill
           FIRED on an unprompted French request, ran the hard-fail search wrapper,
           and emitted docx. The description-field fix WORKS. The skipping bug is
           closed. ENS pilot: mechanism proven; acceptance re-run of the 3
           deliverables still outstanding.
DECISIONS  Print promise (3 tiers, shop-submittable default): CONFIRMED.
           Brand model (overlay + scripted re-zip): APPROVED.
           Copyright holder: still unanswered.
REMAINING  description cap (200 vs 1024) | pip in fresh chat | bleed fill |
           PDF/X-4 validity | ZIP ceiling | stale brand kit.

## VALIDATOR PRIMITIVES LANDED + VERIFIED — skill/.../scripts/lib/ (Mechanism Analyst)
fonts.py (read_fstype, has_tnum yes/unknown) | color.py (WCAG ported line-for-line
from upstream validate_data.py:148-160) | pdf.py (embedded_fonts via /DescendantFonts,
raster_dpi, page_count, page_boxes). 26/26 tests — RE-RUN BY ORCHESTRATOR: OK.
Per-file stdlib guard (ast + sys.stdlib_module_names), proven to fire.
EMPIRICAL FINDING: Chromium wraps each page in an outer `cm` (device-px->pt scale)
OUTSIDE the image's q..cm..Do..Q block. Naive "last cm before Do" is ~4x wrong
(312.5pt vs correct 75pt for a 100px image). Fixed with full CTM stack composition;
regression test pins 75.0pt. Known limit: no ObjStm decoding (Chromium simple
output uses classic xref; documented).
FYI discrepancy: ENS green/white = 6.15:1 by the ported formula vs 6.4:1 in the ENS
rebuild report. Both pass 4.5:1. Ported formula is authoritative.

## LICENCE AUDIT — research/20 (Packaging Analyst)
Three regimes upstream, not one: root MIT; ui-styling wrapper = APACHE 2.0 (vendored
"ckm:" content); 27 per-family OFL.txt under canvas-fonts/ covering 52 of 54 .ttf.
GAP (upstream's): IBMPlexSerif + InstrumentSerif ship with NO OFL.txt. Our skill/:
nothing derived, grepped per family name — zero matches. We ship zero fonts. If we
ever do: per-family NOTICE block template in the report; fetch fresh from canonical
source, never reuse upstream's copy. NOTICE.md + LICENSE now cite upstream by commit
SHA 4aad0584 / 2026-09-06, not version. [PROJECT OWNER] placeholder remains.

## research/19 LANDED — T5 typefaces draft (Document Design Researcher)
8 rows, header validated against T5. ENS Manrope/Inter as brand example; 3 safe-
stack pairings; 4 OFL pairings (serif-sans, IBM Plex superfamily = report 03's
<=3-with-mono cap, Public Sans humanist, Roboto Slab). Embedding Licence + Has
Tabular Figures LEFT BLANK for script fill. Licences WEB-VERIFIED this session, not
recalled: Roboto re-licensed Apache->OFL (per-variant, verify); JetBrains Mono is
OFL 1.1. KEY MECHANICAL DISTINCTION: OS-bundled on Win+Mac (Arial, Times, Georgia,
Verdana, Trebuchet, Courier New) vs OFFICE-bundled only (Calibri, Cambria, Candara,
Corbel, Constantia, Consolas — absent from bare macOS; safe only if opened in real
Office). Candara/Corbel/Constantia/Consolas have NO metric-compatible substitute:
embed-or-avoid. 20-family OFL catalogue in notes.md (x-height/tnum = unknown).

REVISION-2 BACKLOG (held; round 1 is closed to new inputs):
  - font-substitutes.csv as its own lookup table (per-family fact, not per-pairing):
    Liberation (Arial/Times/Courier metric clones) vs Croscore (Apache 2.0) vs
    Crosextra (OFL 1.1: Carlito=Calibri, Caladea=Cambria). Keep lineages straight.
  - OS-bundled vs Office-bundled as a T5/safe-stack column or the substitutes table.

================================================================================
## ENS PILOT — ACCEPTANCE PASSED — 2026-09-07
All three original deliverables re-run through the rebuilt plugin. Workflow held on
every one: classify -> read rules -> ens-search.sh (exit 0 x3, ENS Document Grid +
ENS palette) -> build -> render + check.
  A note-interne  Arial 11pt / 130mm body measure / black remark numbers / green +
                  brown category roles / 8.5pt labels / page x/y footer. One page.
  B formulaire    black section numbers / labels 8.5 / field labels 9.5 / legal
                  text mixed case 8.5. Model SHORTENED 3 regulatory labels to fit,
                  CAUGHT ITSELF against the verbatim rule, REVERTED, fitted by
                  spacing. All 34 codes + every label unchanged.
  C social        1080x1350 / lime only in kicker badge / bold white emphasis /
                  brown category tags / all four FSE+ figures / QR verified.
=> The mechanism is PROVEN END-TO-END on a real brand: brand-as-data + description
   activation + hard-fail search + per-type rules + Tier-2 thresholds. The drift
   the user originally reported is gone.
RULE REFINEMENT FOUND BY THE TEST (generalises to our library):
  "130mm measure" applied page-wide cramped a table and forced a second page.
  Corrected rule: body-text measure 130mm; TABLES MAY USE FULL WIDTH.
  => T9 report-measure-cpl must SCOPE to body text runs, exempting tables.
DESIGN NOTE: the model self-enforced the verbatim rule. Good — but our design says
validators catch this, not model discipline. NET-NEW VALIDATOR CANDIDATE for
revision 2: content-preservation on redesign jobs (diff extracted text nodes of
input vs output; refuse on any change outside an allow-list of whitespace/typo fixes).

## INCIDENT — rate limit, 2026-09-07 ~13:55
All four workers paused (delivery retry limit) and their queued messages dropped.
Disk audit: schema Revision 1 LANDED (1532 lines) though its report was lost;
merge_brand_kit.py uploads-path fix APPLIED; T5 fill PARTIAL; preflight/harness and
T9 patch NOT started. Resuming each via interrupt with a resume instruction.

## SCHEMA REVISION 1 — REVIEWED BY ORCHESTRATOR — ACCEPTED
research/09-library-schema.md, 1532 lines, changelog §9. Incorporates 12/13/14/15.
Net: +7 columns, -2 columns, +7 validators, -1 medium, -150 est. rows.
Rule 1 -> "no UNTYPED logic in cells"; §0.2 rewritten to current engine (identity
short-circuit + BM25 abstention); FK deviation correctly reframed (Style Key mirrors
upstream, Palette/Typeface Keys extend it). ADOPTED closed DOC_CONDITION_SIGNALS as
T2 "Doc Conditions" with a GOOD deviation of its own: signals tagged context|intent;
intent-sourced conditions may emit only constraint: actions — a missed intent changes
which checks run, never what is emitted. Print tiers on T8 as Print Tier Max (a
property of engine x invocation, not page geometry). print-l-delta -> print-contrast-
ratio. T5 Embedding Licence restored (fails on restricted ONLY — else every MS core
font would fail preflight; editable passes). T6 ~200 -> 50-80 rows.
NOT CONFIRMED in Rev 1: placement of research/18 assets (cv-regions, headings) — my
message may have been dropped. Covered in the Rev 2 brief.
T5 FILL: actually COMPLETE on disk — all 8 rows: installable/editable; tnum yes x7,
unknown x1 (Plex superfamily). Task just wasn't marked done before the pause.

## FIELD EVIDENCE — claude.ai SKILL MOUNT LAYOUT (user session, 2026-09-07)
  /mnt/skills/public/    docx, pdf, pptx, xlsx, frontend-design, file-reading, product-self-knowledge
  /mnt/skills/examples/  import-memory, morning, skill-creator, brand-guidelines
  /mnt/skills/plugins/   ui-ux-pro-max:brand, :design, :design-system, :slides, :banner-design, :ui-styling, :ui-ux-pro-max
  /mnt/user-data/uploads/ = attachments (read-only). Outputs dir: being probed.
=> Anthropic ships BUILT-IN docx / pptx / pdf skills. Ours will coexist with them.
   Read them before writing the resolver; align output conventions, don't invent.
=> A built-in brand-guidelines EXAMPLE skill exists — compare with our overlay design.
=> Plugin skills mount under a colon namespace (plugin:skill). Name-field validation
   rejects colons; mount paths use them. Both true.
=> Our merge script must treat the MOUNTED skill as the base (not an attached ZIP);
   user attaches only the brand kit. Routed to Packaging.
=> The stale-brand-kit test was premature: requires our skill uploaded first.

## T5 FILL CLOSED — research/19 (Document Design Researcher)
13 font files checked (3 system, 10 from github.com/google/fonts canonical paths),
zero parse failures. System fonts fsType=8 editable; all open-licence fonts fsType=0
installable — no licence-vs-bits disagreement (checked, not assumed).
CORRECTION CAUGHT: Roboto Slab is APACHE 2.0 (apache/robotoslab/), not OFL — the
ofl/ path 404'd. Fixed in CSV + catalogue before it propagated. Lesson holds: verify
against the canonical source; do not infer a licence by family analogy.
tnum for mixed-family rows resolved from the BODY family (table digits are body text).
IBM Plex Mono = unknown (same monospace non-finding as Consolas). Temp files deleted.

## T9 PATCH CLOSED + TWO NEW AUTHORING TASKS
report-measure-cpl now scope=body-paragraph; exempt=table-cell|caption|sidebar-column
(38 rows, 7 refuse / 31 warn unchanged). SCHEMA GAP SURFACED: T9 Applies To can only
scope whole documents; element-level scope needs a real "Element Scope" column
(routed to Rev 2). content-preservation validator: implies a corrections-log concept
that doesn't exist; orchestrator leans "zero text changes on redesign; typo fixes are
a separate explicit request + reporting obligation" (routed to Rev 2).
DISPATCHED: Print specialist -> research/21 T7 page-format rows + T9 print rows.
            DDR -> research/22 T11 figures rows, independently sourced (no upstream
            row copying; dataviz local skill citable as a local resource).

## FIELD EVIDENCE — /mnt/user-data LAYOUT + MOUNT WRITABILITY (user session)
  /mnt/user-data/outputs/      = download dir (files produced for the user)  [CONFIRMED]
  /mnt/user-data/uploads/      = attachments, read-only                       [confirmed earlier]
  /mnt/user-data/tool_results/ = internal scratch
  /mnt/skills/public/* , /mnt/skills/examples/*  = READ-ONLY mounts
  /mnt/skills/plugins/                            = writable
  Custom-skill mount tier: not yet observed.
=> merge_brand_kit.py: read mounted base, write to outputs/, never into a skill mount.
=> Anthropic's four built-in SKILL.md files (docx, pptx, pdf, brand-guidelines) exist
   (~39KB); user exporting to research/23-anthropic-builtin-skills.md. Resolver task
   is GATED on reading them: align with house conventions, do not invent.

## TEST RESULT — DESCRIPTION CAP = 1,024 (user, claude.ai upload UI)
UI error text: "Description must be under 1024 characters". The 200-char cap from
report 04's secondary source is NOT real on this surface. Our primary description
(667 chars) ships as-is; the "boundary lost under 200" risk is closed; the three
alternates in references/activation.md are retained only as documentation.
Note the wording "under 1024": treat the hard limit as 1,023.

## HARNESS + PREFLIGHT LANDED + VERIFIED — scripts/ (Mechanism Analyst)
preflight.py (facts only, exit 0): PDF boxes pt+mm, per-font embedded, raster DPI;
DOCX/PPTX real per-font embedding via fontTable.xml.rels / embeddedFontLst rels ->
fonts/ target exists; DOCX ATS structural facts (w:cols>1, w:tbl, txbxContent,
contact-in-header-only). validate_data.py: manifest-driven, 8 failure classes each
with a fixture, key collision base+brand, declared-but-missing file fails, BOM,
untyped-JSON cell, contrast>=4.5:1 derived check; FK accepts "table.col" or
{table,column,list:true} for ;-lists. ORCHESTRATOR RE-RAN: lib 26 OK, scripts 24 OK,
CI gate on empty data/base fails closed exit 1 no traceback, preflight on fixture OK.
DECISIONS ACCEPTED: CLI arg stays data/base (release.yml unchanged); Brand Scope is
SET from directory, overriding CSV (directory is authoritative).
TODO: data/brand/README.md line about key-collision "resolver's job" is now stale.
MANIFEST NEEDS from schema author: per table filename, ordered columns, key column,
enums+values, FKs (+list flag), searchable cols, typed_json_columns (expect empty).

## PACKAGING CLOSE-OUT — merge_brand_kit.py now ONE argument
Base auto-detected from the script's own __file__ (grandparent = live skill root,
correct by construction when mounted), glob fallback across /mnt/skills/*/ and
/mnt/skills/*/*/, -b override, DDI_SKILL_DIR / DDI_UPLOADS_DIR / DDI_OUTPUTS_DIR
test overrides. Reads mount only; writes to outputs/. Bug fixed: output filename
was inheriting a temp stem. README "Updating" = attach ONLY the brand kit. Test
sheets: persistence, attachment, description-cap marked DONE; stale-kit marked NOT
RUNNABLE until our skill is uploaded. Guards re-verified firing.
NEXT UNLOCK: a locally built dev ZIP lets the user upload the scaffolding skill NOW
and answer: custom-skill mount tier, 667-char description acceptance, in-sandbox
merge, and the 10-prompt activation list — all before the library exists.

## research/23 LANDED — Anthropic's built-in document skills (user export, 45KB)
docx / pdf / pptx / xlsx SKILL.md verbatim. Licence: PROPRIETARY — read for
conventions, copy nothing. First-pass facts (orchestrator skim):
  - docx creation uses docx-js (NOT python-docx); editing = unpack -> edit XML in
    place (never pretty-print) -> pack; redlining via --author; comments tooling.
  - "Verify the output" is a first-class section; LibreOffice referenced (render).
  - THE ACTIVATION CLAUSE THAT MATTERS: docx's description says if the user asks for
    a document/report/memo WITHOUT naming a file format "and the session offers a
    dedicated document or page skill... use that instead." pptx says the same for
    decks. => The built-ins DEFER to a dedicated document skill. OUR description
    must position us as exactly that skill, and must name file formats only as
    outputs, not as triggers, to avoid fighting them.
  - brand-guidelines example: presence in dump to be confirmed.
  - brand-guidelines example: ABSENT from the dump (grep count 0). Dump = docx, pdf,
    pptx, xlsx. Asking the user for a separate export.
  - Built-ins' VERIFY convention: render via `python scripts/office/soffice.py
    --headless --convert-to pdf` (a wrapper — bare `soffice` HANGS in the sandbox),
    then `pdftoppm -jpeg -r 100|150` to images, view them. Zero-padded page numbers.
    pptx skill warns: LibreOffice SUBSTITUTES fonts it lacks, so QA renders can show
    overflow the real deck won't — exactly our safe-stack / embedding concern,
    stated by Anthropic. Our preflight (structural) + their render (visual) are
    complementary; the resolver's output should end with both commands.
  - Dependencies declared explicitly: docx npm (preinstalled), pandoc, LibreOffice,
    pdftoppm (Poppler), markitdown, python-pptx. => richer sandbox than "stdlib only"
    assumed; our stdlib rule stays for OUR scripts, but the render handoff may use these.
ROUTED: Mechanism (resolver output vocabulary + verify commands); Packaging
(description deferral clause, structure, dependencies section, render handoff).

## SCHEMA REVISION 2 ON DISK — 2029 lines, 14 tables
New: T12 cv-regions (7 regions x 2 bands), T13 headings (long format), T14 font-
substitutes. T9 Element Scope column added. T9 Threshold now POLYMORPHIC: literal
value OR a column reference (e.g. T7:<Column>) — which already covers the print
specialist's join-marker proposal. Manifest production task is next on the analyst.

## THREE MORE AUTHORED TABLES — research/21 (T7, T9-print) + /22 (T11)
All three CSVs validated by orchestrator: uniform column counts (11x21, 11x7, 11x19).
ORCHESTRATOR RULINGS:
  T11 Min Physical Size mm  -> CUT. Structural: a single mm threshold needs an assumed
                               label count; the real constraint is computed (label pt x
                               count x width). Same class as photocopy/T6 and CPL.
  T11 Anti-Patterns          -> KEEP, scoped to figure-form. Not a duplicate of T2
                               Anti-Pattern Tokens: both BIND validate-anti-patterns
                               with different scope (the T9 rule generalised).
                               [SUPERSEDED 2026-09-08, schema Rev 4 erratum (09 S9):
                                the second sentence is FALSE. T11's column was authored
                                as cited prose and is typed text/P; nothing tokenises it
                                and validate-anti-patterns reads T2 only. "Not a
                                duplicate of T2" still holds -- by KIND, not by scope.]
  T11 Caption Required       -> KEEP (report 03 §D).
  T7 roll-fold               -> DROPPED, correctly: no closed-form panel formula; needs
                               a shop-specific instance row if ever wanted.
  T9-print "T7:<Column>"     -> ACCEPTED; Rev 2's polymorphic Threshold supports it.
  T9-print 3 added rows      -> ACCEPTED (fold geometry, line-art DPI, 3:1 large text).
  business-card default      -> EU 85x55 accepted (Luxembourg pilot); US 3.5x2in as a
                               later second row. Severity enum = fail/warn (schema).
dataviz local skill: not on disk as a directory (plugin-loaded). Irrelevant; primary
sources were used. No action.
NEXT: T1 doctypes (the ENTRY table — resolver stage 1) -> DDR. T14 font-substitutes
-> Print specialist (sourced lineage table). Re-header + load into data/base waits
on the manifest.

## REV 2 REPORT (Coverage analyst) — key points beyond the file
Net: +3 tables, +5 cols, -3 cols, +14 validators, -130 est. rows.
THE FINDING: all three new tables came from AUTHORS hitting restated facts, not
from review. "The reviews found errors; the authoring found structure. What this
schema needs next is more rows, not more review." Orchestrator agrees — that is
the plan from here.
- 18-notes rulings: 1 and 3 adopted; 2 adopted in substance, shape REFUTED: no
  Headings Key column — T13 is keyed (section, language); T10 Section Order already
  names sections; only Language was missing (one enum). Correct.
- Rule 4 in §0: a check is defined once (§4), bound only in T9; T9 rows never define.
- T9 gains Container Scope (all | body-paragraph | table-cell | caption-block |
  sidebar-column | header-footer), orthogonal to T6 Role.
- validate-content-preservation = §4 #13, bound fail on every redesign doctype.
- T9 estimate 85-130 -> 45-70. §4 = 48 validators, 39 net-new (count basis stated).
- COUNTING CORRECTION: my "18 of 28 net-new" was not reproducible; the analyst's
  derivable basis is 7/28 (R0), 9/36 (R1), 9/48 (R2). Use theirs.
- Rename map DELETES 9 authored T9 rows (per-region CV rows -> cv-page-count reading
  T12.max_pages; field norms -> cv-field-norms). RULED: accept; provenance kept in
  notes; ens density re-keyed ens-deck-density. DDR informed directly.
- Two new validators have no CSV binding yet: validate-substitute-available,
  validate-content-preservation -> added at the load pass.

## DEV ZIP BUILT — skill/dist/document-design-intelligence-0.0.0-dev.zip (52,740 B, 15 files)
scripts/build_zip.py = the one shared build path (release.yml now calls it; CI runs
without --allow-empty-data and fails closed; verified it aborts on missing manifest).
Constraint check runs on every build: one root, no backslash paths, SKILL.md present,
description 667 chars, 0 symlinks. Self-containment verified by unzip + run --help.
Bug caught: release asset path was skill/dist/ (local folder name) -> dist/.
skill/dist/POST-UPLOAD-TESTS.md: (a) which tier a custom skill mounts to (+ writable?)
— the most consequential, it decides whether merge_brand_kit's glob matches; (b)
in-sandbox merge with an embedded 3-file brand kit; (c) 10-prompt activation; (d)
preflight on a generated PDF. Disclaimer up top: scaffolding, no library yet.
REV 2 FOLLOW-UP (Coverage): Element Scope — empty means whole document; no "all"
token; DDR's "caption" -> "caption-block" (caption is already a T6 Role). Content
preservation DECIDED: zero text changes on redesign, no allow-list, no corrections
log; typo fixes are a separate explicit request. T9 example row redesign-text-frozen.
Still unwritten (named in §8): per-parameter typing for Parameter/Threshold, so the
numeric-only rule on Threshold references is a convention the parser doesn't check yet.

## TEST RESULT — WEASYPRINT BLEED FILL: PASS (user, fresh chat, WeasyPrint 69.0)
  TrimBox  [0 0 419.53 595.28]            = A5 exact (419.5 x 595.3 pt)
  BleedBox [-8.50 -8.50 428.03 603.78]    = trim + 8.5pt (3mm) per side  <- pass criterion met
  MediaBox == BleedBox                    (no extra room outside bleed)
The MediaBox == BleedBox observation is EXPECTED: `@page { bleed: 3mm }` without
`marks: crop cross` yields no extra media for marks. Requesting marks extends the
MediaBox. => T8 pdf-weasyprint: Supports Bleed = yes (verified: BleedBox/TrimBox
emitted, correct geometry); crop/cross marks require `marks:` in @page.
Not reported: whether the colour block visually extends into the bleed area — the
boxes are correct; fill extension is a stylesheet concern (background on the page
box), not an engine one.
REMAINING USER TESTS: PDF/X-4 validity, ZIP ceiling, POST-UPLOAD-TESTS (4), copyright.

## TEST RESULT — PDF/X-4 + sRGB OUTPUT INTENT: STRUCTURAL PASS, CONFORMANCE UNVERIFIED
WeasyPrint 69.0, --pdf-variant=pdf/x-4 --output-intent=srgb, exit 0, no warnings:
  GTS_PDFXVersion = PDF/X-4
  /OutputIntents [ /S /GTS_PDFX  /OutputConditionIdentifier (IEC 61966-2-1 ... sRGB)
                   /DestOutputProfile 3 0 R ]           <- profile embedded
  DeviceRGB transparency Group count = 0                <- the #2723 caveat did not occur
No validator in-sandbox: veraPDF host + Maven Central BLOCKED; no Ghostscript/Acrobat.
=> NETWORK IS AN ALLOWLIST, not open: PyPI allowed; arbitrary hosts are not. Design
   rule: "pip works" != "network works". Never fetch from non-PyPI hosts in-skill.
=> Tier 2 is structurally real. Conformance check to be done ON THIS MACHINE with
   veraPDF once the user drops pdfx4.pdf into research/ (our network is open).

## T14 FONT-SUBSTITUTES LANDED — research/27 (Print specialist)
15 rows (Arial/Times/Courier x Liberation AND Croscore, per schema precedent).
NO-SUBSTITUTE list (6): Candara, Corbel, Constantia, Consolas, Verdana, Trebuchet MS.
Verdana: the widely-repeated "DejaVu Sans is metric-compatible" claim traces only to
SEO blogs; DejaVu's own site makes no such claim -> REJECTED. Discipline held.
Gelasio (Georgia substitute, OFL, SorkinType) doesn't fit Lineage enum -> RULED: add
`independent`. Metric Identical blank on no-substitute rows -> RULED: blank = n/a.
Weight coverage (Carlito/Gelasio: R/B/I/BI only) -> RULED: new Weights Covered column;
validate-substitute-available must read it. Caveat recorded: Liberation 2.0+ is
Croscore-metric under OFL; 1.x differs (GPL+exception). Key = (family, lineage).
DISPATCHED: Print specialist -> fold live bleed + PDF/X-4 results into research/14;
install veraPDF locally; prepare the offline conformance command for pdfx4-sample.pdf.

## RESOLVER LANDED + VERIFIED — scripts/resolve.py (Mechanism Analyst)
resolve.py 18KB + lib/data.py (shared loader) + tests/test_resolve.py. Orchestrator
re-ran the scripts suite: 40 tests OK (24 harness/preflight + 16 resolver). Abstention
verified live on toy data: "[ABSTAIN] no confident match ... top candidates: ...".
Manifest format gained "role": "entry" (present in the example). CLI: --query
--brand --doctype --data-dir --json. Report message never arrived (dropped); accepted
on disk evidence. Defect: non-ASCII dash in --help renders as a broken byte under
non-UTF-8 consoles -> ASCII-only strings, same fix Packaging applied.
NEXT: single-entry workflow command (validate -> resolve -> handoff -> preflight) so
SKILL.md's mandatory workflow is one call per step; integration against the real
manifest waits on the Coverage analyst.

## SCHEMA MANIFEST DELIVERED — data/schema-manifest.json (Coverage analyst)
14 tables, 172 columns, transcribed from Rev 2 (schema now 2083 lines with new
§0.1.1 recording five surrogate keys: scale_row_key, cv_region_key, heading_key,
substitute_key, figure_key — composite natural keys need a singular key_column;
font-substitutes is the instructive case: Arial has TWO substitutes, choosing is a
licence decision). Generator: research/build-manifest.py (outside the skill, does
not ship). Gate output EXACTLY as required: 14 problems, one per table, one class
("declared but file does not exist"), exit 1. role:entry on doctypes only.
typed_json_columns empty everywhere (Doc Conditions/Parameter are k=v;k=v).
HEADLINE: validate-keys is HALF mechanised. 4 of 8 FKs target GROUPING columns
(Constraint Set Keys -> Set Key; Region Key; Scale Key; Section Order -> section) —
not key_column — so they could not be declared. FORMAT CHANGE REQUEST -> Mechanism:
FK form {"table","column","group":true} = "must exist in that column, need not be
unique"; composes with list:true. Other gaps: Threshold literal-or-reference has no
type (reference form unchecked); non-FK ;-list columns have no delimiter declaration.
VERIFIED, not assumed: all 9 palette pairs pass 4.5:1; ENS On Muted/Muted = 4.74:1
(5% headroom) — first failure there is a regression, not a surprise.
STALE in its report: "T5 blanks in all 8 rows" — research/19 IS filled (verified
earlier). It read an old state.

## ALIGNMENT WITH ANTHROPIC'S BUILT-IN SKILLS — research/24 (Packaging Analyst)
SKILL.md description rewritten to 825 chars: positions us as THE dedicated document
skill the built-ins defer to; file-format nouns are outputs not triggers; explicit
defer-back clause for plain format conversion/edit with no design intent. Render
handoff documented as the observed path (resolve -> built-in docx/pptx renders ->
preflight). brand-guidelines example compared (see §4). Dev ZIP was built before
the rewrite -> REBUILD dispatched as 0.0.1-dev, now shipping the manifest + resolver,
plus a 5th post-upload test (resolve.py in-sandbox must fail with the clean gate
message, not a traceback).
brand-guidelines (research/23b): a SINGLE hardcoded brand (Anthropic's), colours and
fonts as literal markdown in the SKILL.md body — no slug, no data, no overlay. Its
own description calls itself "post-processing": applied AFTER a generic artifact
exists. That is precisely the "identity is an instruction, not data" failure the
ENS pilot diagnosed and our schema exists to avoid. Anthropic's own reference
example for applying a brand is built the way we proved doesn't hold. Nothing to
adopt from it; it independently confirms the diagnosis.
Deferral detail: docx and pptx defer to a dedicated document/slide skill when no
format is named; pdf and xlsx do NOT — PDF is a peer output path for us, not a
handoff target.

## INCIDENT 2 — delivery-limit pause, 2026-09-07 ~14:30 (recovered 2026-09-08)
All five workers paused; queued messages dropped. Disk audit: 0.0.1-dev rebuild,
ddi.py + FK group form, load pass 1, T1 doctypes, veraPDF prep — status per audit
below. Orchestrator produced no-op turns during the pause; resumed via interrupts.
AUDIT RESULT (2026-09-08 resume):
  research/pdfx4.pdf            PRESENT (5,549 B; user kept the original name)
  research/26 T1 doctypes       CSV 11KB + notes 16KB written 14:15-14:16 (unverified)
  skill/dist                    still 0.0.0-dev (70KB, rebuilt with aligned description
                                but not renamed); 0.0.1-dev task not started
  scripts/ddi.py, FK group form NOT started
  data/base/                    EMPTY (load pass 1 not started)
  tools/verapdf-dl/             installer downloaded + extracted; research/28 not written
All five resumed via interrupt; runtimes were "runtime_starting" (new team run).
USER: post-upload tests "passed" (detail pending — mount tier is the key answer).

## OPERATING POLICY — CONTEXT COMPACTION (user directive, 2026-09-08)
Teammate contexts have grown large enough to trigger delivery-limit pauses and to
cost heavily per turn. POLICY: clear each teammate's context (team_clear_agent_
context) as soon as it goes idle after completing a task, BEFORE the next
assignment. Clears are refused mid-turn (all five refused at 14:xx because their
resumed turns had started). Every task brief stays self-contained (paths, what to
read, exact deliverable); all work lives on disk + task board, never in memory.
Saved as a persistent feedback memory.

## T1 DOCTYPES LANDED — research/26 (Document Design Researcher)
35 rows (30 generic + ENS five), 11 cols, Rev 2 header incl. Region Key; zero dupes.
Under the 40-60 target BY DESIGN: every class has a row; sub-variants only where a
sourced structural difference exists (CV x 9 incl. regions + academic; brochure x 5
by fold x paper; deck x 3 by viewing context). No early-career CV row (Seniority
Band is a T12 lookup axis, not routing). Keyword strategy: rare tokens win BM25
("tabellarischer lebenslauf", "europass"). 12-query test list (EN/FR/DE, 3 ambiguous)
for the resolver. Doc Conditions use only the 5 closed keys.
RULINGS:
  ens-web-tool  -> DROP from T1. The schema excludes web tools; the description
                   defers screens to UI/UX Pro Max. ENS's web-tool rules stay in
                   ENS's own plugin. Consistency beats completeness.
  deck x 3 sharing one Reasoning Key -> Doc Conditions collide (if_projected would
                   fire on handout/document decks). INTERIM: three Reasoning Keys
                   (T2 rows differing only in Doc Conditions). REV 3 QUESTION for the
                   Coverage analyst: CONTEXT conditions (if_projected, if_hand_filled,
                   if_photocopied...) are facts about the DOCTYPE and may belong on
                   T1; INTENT conditions stay on T2. Logged, not decided.
POLICY APPLIED: DDR context cleared on idle before next assignment (T2 + T6).

## USER TEST RESULTS — round 3 (2026-09-08)
ZIP ceiling: dev ZIP (15 files, ~70KB) accepted with no issue. No ceiling hit at dev
size; the real test is the full library ZIP (600-900 rows) — re-check at v0.1.
Post-upload (a) mount tier: user answered "document-library" — full path not yet
given; asking for the verbatim /mnt/skills/<tier>/<folder> line. Writable: unknown.
(b)(c)(d): reported as "passed" in aggregate; per-test detail not given.
Copyright holder: user asked what is meant — explaining (MIT line needs a name).

## LOAD PASS 1 — FIRST REAL GATE RUN — 190 ROWS PASS (2026-09-08)
data/base: typefaces 8 · page-formats 11 · constraints 42 · figures 11 · cv-regions
14 · headings 81 · font-substitutes 15 · render-targets 8 (authored from T8 section).
Gate: only the 6 unauthored tables fail ("declared but file does not exist"); every
loaded row passes header/enum/FK/BOM/JSON checks. ORCHESTRATOR RE-RAN: confirmed.
resolve.py refuses through the SAME loader: "[DATA INVALID] 6 problem(s)" exit 1.
Loader research/load-base.py is idempotent from untouched drafts (drafts = provenance).
SIX CORRECTIONS the map needed, found by running it:
  1 CV collapse is 10 rows not 9 (uk-cv-no-photo restated T12)     -> 10 -> 2
  2 print-contrast-ratio is TWO rows (4.5 body, 3.0 large) — the draft was right
  3 Threshold refs must use re-headered names: T12:Max Pages (Rev 3: fix §0.1 example)
  4 ens-deck-density: no such generic row; ENS's 5 belongs in data/brand/ens/ (no-op)
  5 T12 field-direction enum gained `customary` — authored data beat the guessed enum
  6 research/18 has 2 malformed rows (unescaped commas) -> DDR fixing at source
T11: prose in enum columns normalised (Label Strategy -> direct/either; Greyscale
Safe -> yes); 3 Caption Required rows carried real facts ("state bin width", "state
n", "caption ABOVE table") -> normalised to yes, qualifications preserved in
research/26-t11-caption-qualifications.md -> Rev 3: a Caption Note column.
0.0.1-dev ZIP: 26 files, 81,611 B, ships manifest + resolver + the 8 real tables;
.pytest_cache leak caught and excluded; test (e) added (resolver fails closed).
POLICY: Coverage + Packaging contexts cleared on idle.
LOAD PASS — FK EYE-CHECK gives the unauthored tables their required keys:
  type-scales must define: cv-print, ens-print, form-print, report-print,
                            report-screen, report-technical  (typefaces already refs)
  region keys in play:     dach, eu-europass, eu-generic, france, gulf-gcc, uk, us
  Set Keys available: 11 · canonical sections: 11 · headings rows: 81 (not 80)
Routed to DDR (T6 keys verbatim; T2 uses existing keys only) and to Coverage
(T11 column = "Caption Must State", its own name; expected FK sets for the gate).

## USER ANSWERS — 2026-09-08
MOUNT TIER: custom-uploaded skill mounted at /mnt/skills/plugins/document-library
  => tier = plugins/ (the WRITABLE tier observed earlier).
  => FOLDER NAME IS NOT OUR ZIP ROOT ("document-design-intelligence"); the platform
     named it "document-library" (display name or slug chosen at upload). Any glob
     that assumes our folder name would MISS. merge_brand_kit's primary __file__
     heuristic is unaffected (grandparent of the script = skill root regardless of
     name); the fallback glob must search by SKILL.md `name:` content, not folder.
  Routed to Packaging.
COPYRIGHT HOLDER: "Magazem" — applied to LICENSE and NOTICE.md (and README if present).

## CORRECTION — veraPDF DOES NOT VALIDATE PDF/X (Print specialist, research/28)
My task premise was wrong: veraPDF validates PDF/A (ISO 19005) and PDF/UA only;
"--flavour 4" is PDF/A-4, not PDF/X-4 (ISO 15930-7). Verified three ways. No free/
open tool validates PDF/X-4; only commercial preflight (Acrobat, callas, PitStop).
Tool + portable JRE installed anyway at C:\Users\ysuliman\tools\verapdf\ (signature
+ checksum verified); useful later for PDF/A if we ever promise archival output.
research/pdfx4.pdf: structurally clean on every locally checkable point (/Trapped
/False; PDF/X marker in XMP only, no legacy Info duplicate; sRGB intent + profile;
0 DeviceRGB groups; no fonts in file so embedding N/A).
RULING — TIER 2 WORDING, FINAL: "PDF/X-4 structurally emitted (WeasyPrint >=67);
conformance not independently verifiable with open tooling." Never "validated
PDF/X-4" anywhere in SKILL.md, README, or output. research/14 §6 updated by the
specialist to match.

## VERIFIED — ddi.py, FK group form, ASCII clean, 93 TESTS
ddi.py no-arg prints the 4-step workflow (check / resolve / preflight / handoff).
lib/data.py: "group" FK form present; list_columns + reference_columns added.
Zero non-ASCII bytes in any script. Suite: 67 scripts + 26 lib = 93 OK (orchestrator
re-ran). Mechanism report message did not arrive; disk evidence sufficient.
POLICY: Print + Mechanism contexts cleared on idle. Coverage told to re-declare FKs.
MECHANISM REPORT (arrived after disk verification; consistent): group FK fans out to
EVERY matching row in resolve.py's walk (breadth-first, dedup by key); fk_spec now a
4-tuple; new toy schema (tags/items/checks) exercises group, group+list, list_columns,
reference_columns; tests/test_ascii_clean.py walks ast.Constant across all 8 files
(126 em dashes, 10 section signs, 3 middle dots removed); ddi.py handoff refuses non-
resolved JSON (exit 1) and degrades to "(not present in this resolution)" per section
on the toy manifest — honest schema-independence. HANDOFF_VOCAB dict = one rename point.
NEXT for Mechanism (assigned): handoff speaks docx-js / pptxgenjs vocabulary (DXA,
half-points, hex-without-#, LAYOUT_16x9, HeadingLevel, charSpacing) + the PDF @page
block and exact engine commands, tier-2 wording verbatim.

## INCIDENT 3 — CONCURRENT WRITES TO data/base (2026-09-08)
Packaging deleted brand-scoped row ens-manrope-inter from data/base/typefaces.csv
(brand rows never belong in base); Coverage's loader re-created it from the draft.
Also a transient duplicated "Caption Must State" column in figures.csv.
RULINGS (permanent):
  1 ONLY the loader writes data/base. No hand edits. (data/base/README to say so.)
  2 Loader SKIPS all Brand Scope != generic draft rows (logged). Base = generic only.
  3 ENS rows have ONE source of truth: examples/ens-brand.md -> make_brand_kit.py ->
    data/brand/ens/ on merge. Draft ENS rows are provenance only.
  4 build_zip.py excludes data/brand/*/ contents; the base package never ships a brand.
  5 Idempotency check after every loader run: grep ",ens," data/base/*.csv == empty.

## COST CONTROL — CHECKPOINT-AND-RESET (user directive #2, 2026-09-08)
User: teammates are "eating through the session like crazy"; idle-only clearing
is insufficient when turns run 15+ min. ACTION: interrupted Coverage, DDR and
Packaging mid-task with a checkpoint instruction (write research/handover-<name>.md:
done / half-done / not started / 3 key facts; save; task status; end turn). Next:
clear each on idle, resume from its handover with a NARROWER brief. Mechanism left
alone (fresh context, just started). NEW LIMITS: briefs = one deliverable (~10 min);
interrupt-checkpoint any turn past ~10 min; max 2-3 concurrent long tasks.
Saved to persistent memory.

## CHECKPOINT HANDOVERS RECEIVED (research/handover-{coverage,ddr,packaging}.md)
COVERAGE: Rev 3 DONE (schema 2465 lines; manifest 174 cols, 13 FKs incl. 5 group;
  loader splits Caption Must State; idempotent). Gate = 6 unauthored + 8 typefaces.
  Scale Key (target table unauthored) — correct. NOT done: loader brand-row skip.
  RULED by schema owner: if_projected DELETED from the condition vocabulary; the
  three-Reasoning-Key deck split WITHDRAWN (deck-generic one key). Rule: a condition
  is admissible only if the resolved T1 row does not determine its truth value.
  BLOCKER: validate_data resolves Threshold refs against manifest TABLE NAMES, so
  canonical form must be `cv-regions:Max Pages`, not `T12:Max Pages`.
  Stale dev ZIP (Rev 2 manifest). ens-slides references nonexistent render target
  html-export (html-static exists).
DDR: 26 edited (34 rows; deck split applied — to be REVERTED); 29 T2 = 21 rows DONE
  (12 cols; Reasoning/Confidence treated as draft-only — Coverage to adjudicate at
  load); 29-notes NOT written; T6 NOT started (plan: 17 rows); research/18 fix NOT
  done. Its plan leaves 4 of T5's 6 Scale Key refs dangling and proposes repointing
  shipped T5 rows. safe-sans-deck typeface is PROPOSED (no T5 row); ENS slides need a
  projection-medium scale. T3/T4 keys used are all example or invented slugs.
PACKAGING: make_brand_kit.py DONE (16 tests; suite 83 via pytest); ENS kit ZIP not
  yet produced; merge run + gate outputs + README updates + build_zip brand exclusion
  + fallback-by-name NOT done. It hand-patched figures.csv's Caption Must State — the
  same column the loader now writes = the transient duplicate. Rule 1 ends that.
ORCHESTRATOR RULINGS:
  R1 Coverage's condition ruling WINS: revert the deck split to deck-generic; drop
     if_projected. (DDR)
  R2 Threshold canonical form = <manifest-table-name>:<Column>, e.g.
     cv-regions:Max Pages. T-numbers are document labels only. Fix schema §0.1 and the
     shipped constraints row. (Coverage)
  R3 T6 defines ALL six referenced scale keys (cv-print, form-print, report-print,
     report-screen, report-technical, ens-print) + deck-projection + print-office-
     generic. CONVENTION-tagged where unsourced. NO repointing of shipped T5 rows. (DDR)
  R4 Role enum gains `legal` (same precedent as `customary`). (Coverage)
  R5 T5 gets two deck rows: generic safe-sans-deck (Arial/Calibri, Scale Key deck-
     projection) and ENS deck row reusing Manrope/Inter with Scale Key deck-projection —
     authored into the ENS brand kit, not base. (DDR draft; Packaging kit)
  R6 ens-slides Render Target -> html-static (or pptx-office). (DDR)
  R7 T2 Reasoning/Confidence: Coverage decides at load (draft-only strip vs shipped).
CONCURRENCY: Coverage + DDR resume first (critical path); Packaging resumes after
base is confirmed generic-only; Mechanism continues (fresh); Print idle.

## RESUME.md WRITTEN (2026-09-08) — the short state file for a fresh orchestrator
Project root RESUME.md: what exists, standing rules, team operating rules, the 8-step
critical path, handover pointers, slot ids. Recommendation to user: reset all worker
contexts (nothing irreplaceable in them), shut down Print specialist, run 2 workers at
a time with one-deliverable briefs, and start a FRESH orchestrator session from
RESUME.md — this conversation is the largest context in the team.

## RESTRUCTURE — 2026-09-08: SUB-MANAGER ORCHESTRATOR + THIN LEAD
User added a fresh "Workflow Orchestrator" copy as a teammate (slot 01a080c5-2001-
78b3-bbbe-afaae15edafa). Appointed SUB-MANAGER: runs RESUME.md's critical path with
task create/update + messages; asks the lead for context clears ("CLEAR <slot>") after
each task; reports milestones only (<=10 lines). Lead (this session) becomes THIN:
clears, shutdowns, decisions, user relay; no longer reads long worker reports.
All four workers' contexts cleared (Coverage, DDR, Packaging, Mechanism). Print
specialist idle; shutdown pending user decision.

## LEAD HANDOFF — 2026-09-08
Print Production Specialist shut down (scope complete). User directed the lead's
own chat be cleared (or the lead shut down). Chose CLEAR: a lead is required for
clears/shutdowns, which the sub-manager cannot perform. RESUME.md gained a "LEAD
RESUME" section; persistent memory points a fresh session at RESUME.md.
