# BRIEF — DDR — v0.2 phase A3: the marketing-class section model (the last six)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT write under skill/document-design-intelligence/. research/ only.

## Scope — these six structure keys, verbatim, and this finishes the fifteen
brochure-3panel, brochure-gatefold, flyer-single-sheet, poster-single-canvas, deck-standard,
cover-letter-standard

Five transactional plus four long-form plus these six is fifteen, which is every structure key
in data/base/structures.csv that has no Section Order. After this, authoring is done and phase B
can load.

## Shape — the loader's input shape, which you now know
research/41-headings-marketing-draft.csv with EXACTLY these columns, from
research/18-ats-headings.csv:
  canonical_section,heading_text,language,is_primary,source
No heading_key — the loader generates it. Every row needs a real `source`.

research/41-t10-section-orders-marketing.csv: structure_key, Section Order. Six rows.
research/41-notes.md: sources, and which orders are SOURCED versus your own CONVENTION.

## Rules, all still binding
- en, fr, de on every section; one row per section per language.
- Exactly one is_primary = yes per (canonical_section, language).
- canonical_section lowercase ASCII hyphenated; heading_text may carry accents.
- THE CROSS-CLASS REUSE RULE, which you have now applied correctly four times: never reuse a
  section across classes when its FR or DE primary reads as a word from the other class. Check
  the actual heading_text in both languages. Your refusals of summary/Profil,
  references/Referenzen and proposed-solution/Losungsvorschlag are the worked examples.
- DO reuse where a section genuinely is the same thing in all three languages. `headline`,
  `key-points`, `call-to-action` and `contact` already exist from research/40 and data/base, and
  several of these six plainly want them.

## PRE-RULING from the lead — read this INSTEAD of guessing
A Section Order lists CONTENT sections in reading order. It does NOT encode physical panels or
slide counts.
- BROCHURES: list the content sections in the order a reader meets them while unfolding —
  cover, hook, body sections, call-to-action, contact. Note in the `source` column that panel
  mapping belongs to page-formats, not structures.
- DECKS: list the content ARC — title, agenda, problem, solution, evidence, ask, close — not
  slides.
- If you still find a family where even that is a stretch, LEAVE THE CELL EMPTY and say why in
  the notes. An honest blank beats a forced list. You will not be asked to justify a blank you
  can explain.

## The hard one, think before you author
These six are not all the same kind of document and the orders should show it.
- A three-panel brochure and a gate-fold have PANELS, read in a physical order, not a linear
  section list. Say in the notes how you are representing that, and whether panel structure is
  really a Section Order at all or is being approximated by one. If you think the model does not
  fit, say so plainly rather than forcing it — that is a finding worth more than a filled cell.
- A poster is a single canvas. If a poster's honest answer is two or three sections, author two
  or three. Do not pad.
- A deck is slides. Decide whether the sections are slide roles (title, agenda, and so on) and
  say why.
- cover-letter-standard is the odd one here: it is transactional in tone and may reuse heavily
  from research/39's letter set. Check before inventing.

## Verify before you report
1. Every token in all six Section Orders resolves against data/base/headings.csv plus
   research/39 plus research/40 plus your new file. Paste the output.
2. Simulate the loader's key generation with a SINGLE shared counter per
   (canonical_section, language) across all four sources; confirm zero collisions.
3. Exactly one primary per (canonical_section, language), in your file and in the union.
4. Zero blank `source` values. Header matches research/18-ats-headings.csv exactly.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the six Section
Order strings, new sections and rows added, what you reused, the output of checks 1 and 2, and
your answer on whether panels and slides genuinely fit a Section Order.
