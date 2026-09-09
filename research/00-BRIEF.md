# Project Brief — Document Design Intelligence (working title)

## Goal
Build a free, open-source Claude Skill that does for **documents** what UI/UX Pro Max
does for web UI: raise output quality and eliminate "AI slop" in PowerPoint decks, CVs,
brochures, reports and similar artifacts. A later V2 should generate a reusable brand /
design system that all downstream documents inherit.

## Target surface
The **Claude app** (claude.ai / desktop), NOT Claude Code. Skills are confirmed working
there — the user has UI/UX Pro Max installed and running in the Claude app today.
ChatGPT parity is a secondary consideration.

## Prior art (READ IT, don't guess)
Full UI/UX Pro Max source is on this machine:
  C:\Users\ysuliman\.claude\plugins\marketplaces\ui-ux-pro-max-skill
326 files. Key locations:
  - .claude/skills/ui-ux-pro-max/SKILL.md      (45KB, the core router)
  - src/ui-ux-pro-max/data/*.csv               (styles, colors, typography, ux-guidelines)
  - src/ui-ux-pro-max/scripts/design_system.py (48KB)
  - .claude/skills/slides/                     (HTML presentations)
  - .claude/skills/design-system/data/slide-*.csv
  - .claude/skills/brand/references/*.md       (the V2 brand-identity layer)
  - .claude/skills/design/, .claude/skills/banner-design/

## LICENSE — binding constraint
Upstream is **MIT (c) 2024 Next Level Builder**. Studying the architecture and
re-implementing is fine. Copying data files or text verbatim requires retaining the
MIT notice and attribution. Prefer independent derivation. Flag anything you think
we'd be tempted to lift.

## Known ground truth from the user (primary evidence, do not contradict without cause)
- The skill DOES run in the Claude app.
- It already produces good posters that adhere to a generated brand identity.
- Its V2 brand-identity generator built the user a company-voice plugin they rate highly.
  That generate-then-inherit loop is the mechanism most worth cloning.
- Therefore the value of this project lives in the GAPS, not in rebuilding what works.

## Open question (unresolved — cover both branches)
Must output be real .docx/.pptx files, or is print-ready HTML/PDF acceptable?
Their pipeline terminates in HTML. Do not assume; treat as a fork.

## Deliverable format (ALL researchers)
Write ONE markdown file to:
  C:\Users\ysuliman\Documents\Ai plugin\research\<your assigned filename>
Use exactly this skeleton:

  # <Scope name>
  ## 1. Findings          — what you actually observed, with file:line citations
  ## 2. Transferable      — what we should reuse or copy the pattern of, and why
  ## 3. Breaks            — what does NOT survive the move to documents / the Claude app
  ## 4. Gaps              — what is missing entirely and would have to be built
  ## 5. Open questions    — what you could not determine, and what would settle it

Cite real paths and line numbers. Do not summarize the README — read the source.
Do not pad. If a section is empty, say so and move on.
