# BRIEF — DDR — Retrofit research/39 into the loader's shape (40 is already done)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT write under skill/document-design-intelligence/. research/ only.

## Why
Your A1 and A2 content is verified and correct — this is not a rework of the sections. Both
heading CSVs were authored against data/base/headings.csv, which is the loader's OUTPUT shape.
research/load-base.py reads a different, lowercase INPUT shape, generates heading_key itself,
and needs a `source` column that neither draft has. Without it every new row lands under
"(none given)" in data/rationale/headings.md, which the loader writes.

## The target shape — from research/18-ats-headings.csv, verbatim
canonical_section,heading_text,language,is_primary,source

## Deliverable (ONE — one file converted)
You already converted research/40 and I verified it is lossless. Only this one is left:
- research/39-headings-transactional-draft.csv

Use your own converted research/40-headings-longform-draft.csv as the worked example of the
target shape and of how to write the `source` column.

For each row:
1. DROP the heading_key column entirely. The loader generates the key as
   `<canonical_section>-<language>-<n>`. Yours would be ignored.
2. Rename the columns to the five lowercase names above, in that order.
3. ADD a `source` value on EVERY row. This is the real work of this brief, not a formality.
   - Where you cited something in 39-notes.md or 40-notes.md, put that citation here. The DIN
     5008 letter terms, the francophone report vocabulary, the German invoicing wording.
   - Where the wording is your own convention, say so in the existing house style, which you can
     read in data/rationale/headings.md — for example `convention (not in report 03)`, or a
     short parenthetical naming what kind of convention it is.
   - Do not write a vague source to fill the cell. A row whose wording you invented must say so.
     The whole point of this column is that a reader can tell sourced from conventional.

The two section-order CSVs are already correct. Do not touch them, and do not touch the notes
files except to keep them honest if a source string differs from what the notes claim.

## Do not renumber or re-author
No section may be added, removed or renamed. No heading text may change. If converting reveals a
content problem, report it, do not fix it here.

## Verify before you report
1. Both files' headers equal research/18-ats-headings.csv's header exactly, in the same order.
2. Row count unchanged: 84.
3. The multiset of (canonical_section, heading_text, language, is_primary) is IDENTICAL before
   and after. Read the committed version with
   `git show HEAD:research/39-headings-transactional-draft.csv` and diff the tuples in Python.
   Paste the output. This is the check that proves you converted rather than rewrote. Note the
   committed file's columns are the OLD names -- Heading Text, Language, Is Primary.
4. Zero rows with a blank `source`.
5. Simulate the loader's key generation across data/base plus both files with a SINGLE shared
   counter per (canonical_section, language), and confirm no generated key collides.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: the output of
checks 3, 4 and 5, and how many distinct source strings you ended up with.
