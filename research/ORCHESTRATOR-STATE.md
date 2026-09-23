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
