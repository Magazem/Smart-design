# ORCHESTRATOR STATE — v0.5 "Design Library" phase (started 2026-09-23)

**Cold reader: read THIS file first, then RESUME.md's "*** COLD START" section for standing rules.**
This file is the live checklist. It is updated and committed after every milestone.

## User mandate (2026-09-23, verbatim intent)
- Orchestrator (Opus) plans/reviews; Sonnet workers implement; Opus reviews.
- NEVER fall back to the user. Keep working autonomously inside this repo only.
- Keep committing + pushing to git; keep documenting so a fresh instance can continue.
- End goal: a skill anyone in any field can use with Claude, ChatGPT or Grok to produce
  well-structured, non-slop documents, backed by:
  1. ~10 designs per document type/family, chosen from STRUCTURED ranking sources
     (usage/popularity/juried rankings) — researchers do not judge "best" themselves.
  2. A grand library (palettes, type pairings, scales, styles) plus instructions so an AI
     can build a structured brand kit mixing top designs per modern standards.
- Current activation (manual invocation + some auto triggers) is ENOUGH. Do not reopen routing.

## Working method
- Subagents via the Agent tool with explicit model: haiku = read-only checks,
  sonnet = implementation/research authoring, opus = planning/review.
- Workers do not run git; the orchestrator commits and pushes.
- Plans live in research/80-v05-plan.md (to be written from the planner's output).

## Progress log
- 2026-09-23: Oriented. Launched health check (haiku) + v0.5 planner (opus).
- 2026-09-23: Health check: 199 pass / 6 fail (Windows UTF-8 mojibake in 2 tests, manifest CRLF
  byte-compare), gate OK 477 rows. "make me a CV ..." ABSTAINS (cv-uk vs cv-gulf-gcc) — to fix in Phase 4 cv.
- 2026-09-23: Plan frozen in research/80-v05-plan.md (read §R rulings first). Butterick NOT banned (R-a).
- IN FLIGHT: Windows test fix (sonnet); P1.1 schema in build-manifest.py (sonnet); P2.1
  research/81-ranking-sources.md (sonnet). Next after P1.1: P1.2 loader globs + Family column.
- 2026-09-23: Windows fix committed (8a1b217). research/81 written: typeface (Google Fonts
  metadata popularity, fontsource npm/jsDelivr), palette (GOV.UK/USWDS fetched; Carbon/M3/Fluent
  search-corroborated), modularscale OK. NO fetchable popularity-ranked LAYOUT corpus yet
  (Canva/Behance/Dribbble blocked) -> probe 2 in flight (GitHub stars, Overleaf, Typst, npm themes).
- P1.1 done (uncommitted, gate red until P1.2). IN FLIGHT: P1.2+1.3 loader globs/Family/seed designs;
  P3.1 typeface pairings -> research/library/typefaces/; P3.4 authority palettes -> research/library/palettes/;
  probe 2. Library batches load only when listed in load-base.py's allow-list (orchestrator enables after review).
- COMMITTED 22b5689 (P1.1-1.3: Family, designs, provenance, loader globs, 21 seed designs) and
  7229d7d (library batch 1: 20 typeface pairings + 20 design-system palettes; allow-listed in
  research/load-base.py LIBRARY_INPUTS_ENABLED / PROVENANCE_INPUTS_ENABLED). Gate 625 rows, 200 tests.
- IN FLIGHT: research/82 protocol (opus); P3.5 ranked COLOURlovers palettes; P3.7 ratio type scales;
  R-lib1 audit of batch 1 -> research/83 (opus); P1.4 test_provenance/test_designs; P1.5/1.6 ddi designs/library/--design.
- To enable a new library batch: add its csv filename to the two allow-lists, run
  `python3 research/load-base.py`, then `ddi.py check` + pytest from the skill dir.
- COMMITTED a6b0b81 (9 ratio type scales, gate 715 rows) and research/82 protocol (FROZEN; amendments go in research/82a-*.md).
- PHASE 4 STARTED. Coding outputs per corpus: research/designs-evidence/<family>-corpus-<src>.md, then
  a second-coder task (25% seeded sample, §7) and a fill task (F.c) per family. GitHub search API
  is 10 req/min per IP: only ONE worker may use it at a time.
  IN FLIGHT: cv-corpus-github, cv-corpus-npm-ms, deck-corpus-npm.
- 2026-09-23: User asked for visible hired teammates. Spawned (AionUi team, "Claude Code" assistant):
  Design Researcher (Phase 4 corpus coding), Skill Implementer (code/tests), Opus Reviewer (reviews).
  Slot ids are per-machine; re-derive with team_members. Models are set in the AionUi UI selector
  (intended: Researcher+Implementer = Sonnet, Reviewer = Opus). Background Agent-tool subagents
  are also used in parallel (explicit model per call).
  Board: deck-corpus-lo-ms (Researcher), P5.1 generic brand-kit doctypes (Implementer), R1 review (Reviewer).
- research/83 audit batch 1: PASS-WITH-FIXES; fixes being applied (rulings: keep per-family GF rows,
  test keys on +Ranking Metric; Typewolf rows -> authority; DM Serif Display kept, display faces exempt from weight filter).
- R1 (research/84) no blockers. BACKLOG from it: (a) cv convention ranks above authority -> fix in cv fill;
  (b) cv-dach-tabular/cv-editorial "authority" rests on Typewolf FONT pages, not layout -> re-class in cv fill;
  (c) convention provenance rows carry Fetch=search-corroborated with no source -> make Fetch blank-allowed
  for convention (build-manifest + test) ; (d) legacy provenance backfill for doc-styles/doc-reasoning/
  base palettes/typefaces (LEGACY_UNPROVENANCED in test_provenance.py must shrink); (e) build-manifest cwd
  dependence, stale loader comments, Rank/prov_key format tests.
- Reviewer now on R-lib2 (research/85: ranked palettes + ratio scales).
- COMMITTED: 2ffac1d P5.1, 7577168 P5.2 (brand.md ## Designs), b5b3b4f research/83 fixes + test_provenance/test_designs,
  11e8dca P1.5/1.6 (ddi designs / library / resolve --design / handoff design line; SKILL.md workflow step).
- IN FLIGHT: Implementer = R1 backlog (c)(e) (Fetch blank for convention, build-manifest cwd, format tests);
  Reviewer = R-lib2 audit; Researcher = deck-corpus-lo-ms; bg: cv-corpus-github, cv-corpus-npm-ms,
  deck-corpus-npm, P6.1 portable pack (research/build-portable.py -> portable/).
- NEXT: legacy provenance backfill (d) after Implementer frees test_provenance.py; second-coder + fill for cv
  and deck when their corpora land; remaining families per research/82 §10 (only one GitHub-API user at a time).
- NOTE (user, 2026-09-23): the "Opus Reviewer" teammate started on Sonnet; user switched it to Opus
  manually. Treat R1 (research/84) as possibly Sonnet-authored: the final R4 Opus review must re-cover
  schema/loader. On a new machine, verify teammate models in the AionUi selector after spawning.
- research/85 (R-lib2) PASS-WITH-FIXES; fixes in flight (bg). Rulings: r13 admitted/r137 dropped (pre-registration wins);
  Muted per the pre-registered "lightest tint" rule; new test_palette_roles.py (Text-Safe roles >=4.5 vs Background).
- RULING FIX 19 (lib type scales unreachable): give brand.md a `## Type scales` section (`print|projection|screen: <scale_key>`)
  so make_brand_kit can use lib-* scales per medium instead of its hard-coded print scale -> Implementer task after backfill.
- COMMITTED portable pack (P6.1/P6.2): research/build-portable.py -> portable/{AGENTS.md (6609 chars),
  DDI-LIBRARY.md (~114 KB), INSTALL.md}; test_portable_sync.py fails on ANY data drift.
  RULE: after every load-base.py run, also run `python3 research/build-portable.py` before committing.
- research/82a-clarifications-1.md written (C1-C10; family-wide second-coder sample).
- Committed corpora: cv (github, npm; MS resumes unreachable SPA), deck (npm pending, lo-ms), brochure, flyer.
  IN FLIGHT: cv second coder (bg, independent); invoice corpora (bg, holds GitHub API); deck npm (bg);
  Researcher = brochure recode + memo/form; Implementer = FIX 19 type scales; Reviewer = R2 code review;
  bg palette fixes (research/85).
- 2026-09-23 evening: SESSION LIMIT hit mid-work (resets ~22:30 Europe/Luxembourg); resumed after reset.
  Committed since last log: 0f72892 (FIX 19 ## Type scales + research/86 R2 review).
  Resumed bg agents: palette fixes (research/85, partial edits on disk), invoice corpus, deck npm corpus,
  cv second coder (tmp-cv2/ scratch dir). Teammates were "paused" after the limit; team_interrupt_agent
  re-queues them (plain team_send_message did not wake them).
  Board: Implementer = R2 fixes (Design Key column, brand-aware --design, BM25); Reviewer = R3 portable review;
  Researcher = brochure recode (82a C1/C3) + memo + form.
  RULINGS for R2 (research/86): F1 brand keeps own palette/typeface under --design; F2 nullable
  doc-reasoning.Design Key; F3 blank bias terms in kit rows; F4 drop all-doc query terms, fallback Rank.
- 2026-09-24: WEEKLY + 5h limits hit, user reset both. Committed: 769663d research/85 palette fixes +
  test_palette_roles; 4ff0d4b R2 fixes (Design Key col, brand-aware --design, BM25); research/87 R3 portable
  review; deck-corpus-npm; cv-second-coder (9edd302).
  IN FLIGHT: Implementer = portable fixes per research/87; Reviewer = 82b shortfall-sources plan;
  Researcher = poster MS + report/whitepaper L3; bg: invoice corpus (resumed, GH holder), cv agreement calc
  (research/designs-evidence/agreement.py reusable), deck second coder.
  NEXT: cv agreement verdict -> cv fill (F.c) incl. R1 backlog (a)(b) re-rank; deck agreement -> fill;
  GH families in turn: cover-letter, letter, report, poster, proposal (one GH user at a time).
  Teammate models (seen 2026-09-24): Implementer + Researcher on Fable 5.1 (user told), Reviewer Opus.
- BACKLOG from research/87: quote-devis inherits invoice headings ("Facturé à", "Détails de la facture") —
  data fix in research/39 headings/section orders; pptx handoff slide size 10x5.625in vs page format
  13.33x7.5in (F5, in Implementer's portable task); release a new ZIP so the pack and skill match (I8, at v0.5.0);
  P6.5 proxy trial design is in research/87 §G (run after pack fixes).
- 2026-09-24: cv agreement FAILED on header treatment (0.70) -> 82a-cv.md (opus, bg) sharpens that rule; recode
  header for all cv items + fresh second coder seed "82a:cv" from cv-items.csv. density dropped from cv fill.
- User asked why the orchestrator did so much itself. Response: hired Design Researcher 2 and Repo Keeper
  (the only teammate that runs git: regenerate -> test -> commit -> push -> log line). From now on the
  orchestrator routes commits through Repo Keeper and prefers teammates over background subagents.
- 2026-09-24 Repo Keeper: f00e53c 82a C11 make_items_csv.py + cv-items.csv (80) + deck-items.csv (105 = 40 NPM + 40 LO + 25 MS); 282 passed, 1 skipped, 1 xfailed.
- research/87 fixes landed (Implementer). Remaining from 87: I7 data fix (form-print scale lacks h1), I9, P4 (see 87),
  I8 = cut a release so the pack and the skill ZIP match (at v0.5.0). research/82a-clarifications-3.md (C13-C16) written.
- 2026-09-24 Repo Keeper: b9a1cac poster MS + report L3 + 82a round 3 (docs only; code/data held for job 3).
