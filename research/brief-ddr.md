# BRIEF — DDR — v0.2 phase A2: the long-form-class section model

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT write under skill/document-design-intelligence/data/ — research/
drafts only.

## Same shape as A1, which you just did
`Section Order` is a LIST FOREIGN KEY into `headings.canonical_section`. Every token in a
Section Order must exist as a canonical_section, so the headings rows and the orders are drafted
together and validate together.

## Scope — these four structure keys, verbatim, no others
report-short, report-long-toc, whitepaper-standard, one-pager-standard

Bound from data/base/structures.csv. The transactional five are done; the marketing six come
later. Do not touch either.

## Deliverable (ONE — the long-form section model, two files)
1. research/40-headings-longform-draft.csv — same columns as data/base/headings.csv:
   heading_key, canonical_section, Heading Text, Language, Is Primary.
2. research/40-t10-section-orders-longform.csv — structure_key, Section Order. Four rows.
3. research/40-notes.md — sources, and which orders are SOURCED versus your own CONVENTION.
   Label them separately; do not present an invented order as a cited one.

## Rules carried over from A1, all still binding
- Languages en, fr, de on every section. One row per section per language is sufficient; the
  lead has ruled that wording variants are out of scope for v0.2.
- Exactly one Is Primary = yes per (canonical_section, Language).
- heading_key unique against your file, against the 81 rows in data/base/headings.csv, AND
  against research/39-headings-transactional-draft.csv, which is now committed.
- canonical_section names lowercase ASCII hyphenated. Heading Text may carry accents.

## Reuse rule, now a standing rule — read it before you reuse anything
You were right to refuse the existing CV `summary` for a proposal's executive summary, because
its French and German primaries are "Profil", a CV word. That is now the rule:
NEVER reuse a section across document classes when its FR or DE primary reads as a word from
the other class. Check the actual Heading Text in both languages, not just the English name.
You SHOULD reuse a section when it genuinely is the same thing in all three languages — the
transactional draft correctly shares `date`, `body` and `closing` across letter, memo, form and
proposal. Reuse from research/39 where it fits; a report and a whitepaper plainly share several.

## What these documents actually have
A long report has front matter, a table of contents, an executive summary, an introduction,
a method or approach, findings, a conclusion, recommendations, appendices and references.
report-short is the same family with less of it — the two orders should differ, and the
difference should be defensible, not decorative. A one-pager is a single sheet and its order
should reflect that. Say in the notes why report-short and report-long-toc differ.

## Verify before you report
1. Every token in every Section Order resolves against data/base/headings.csv PLUS
   research/39-headings-transactional-draft.csv PLUS your new file. Write the check in Python
   and paste its output.
2. No duplicate heading_key across all three sources.
3. Exactly one primary per (canonical_section, Language); all three languages present.
4. Both CSVs parse with csv.DictReader and carry the exact column names.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the four Section
Order strings, how many new sections and rows you added, which sections you REUSED from
research/39, the output of check 1, and sourced versus conventional.
