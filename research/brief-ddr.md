# BRIEF — DDR — v0.2 phase A1: the transactional-class section model

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT write anything under skill/document-design-intelligence/data/ —
research/ drafts only. Someone else loads them later.

## The thing you must understand first
`Section Order` in T10 structures is a LIST FOREIGN KEY into `headings.canonical_section`,
declared in data/schema-manifest.json with `"group": true, "list": true`. validate_data.py
splits the cell on ";" and checks EVERY token exists in that column. So a Section Order naming
a section that has no headings row is a dangling FK and the gate goes non-zero.

Today headings.csv has 81 rows covering exactly 11 canonical sections, and ALL ELEVEN ARE
CV-ONLY: certifications, contact, education, experience, languages, projects, publications,
references, skills, summary, volunteering. Every non-CV family therefore needs brand-new
canonical sections. That is why this brief asks for the headings rows and the section orders
TOGETHER — they are one model and must be loadable in one go.

## Scope — these five structure keys, verbatim, no others
invoice-standard, letter-standard, memo-standard, form-standard, proposal-standard

These are the transactional class. Bound from data/base/structures.csv, which has 17 keys, of
which only cv-experienced and cv-academic currently carry a Section Order.
Note: T1's `quote-devis` doctype points at `invoice-standard`, NOT at proposal-standard. So
invoice-standard must serve invoices AND quotes/devis/offers. `proposal` points at
proposal-standard. Check that mapping yourself in data/base/doctypes.csv before you design.

## Deliverable (ONE — the transactional section model, two files)
1. research/39-headings-transactional-draft.csv
   Columns exactly as data/base/headings.csv: heading_key, canonical_section, Heading Text,
   Language, Is Primary.
   - One row per (canonical_section, language, wording variant).
   - Languages en, fr, de — all three, matching the existing pattern. The Language enum allows
     only those three.
   - Exactly ONE row per (canonical_section, Language) may have Is Primary = yes.
   - heading_key must be unique across your file AND against the existing 81 keys. Follow the
     existing convention, e.g. `experience-en-1`.
   - Do NOT redefine any of the 11 existing canonical sections. Reuse them by name if a
     transactional family genuinely needs one.
2. research/39-t10-section-orders-transactional.csv
   Two columns only: structure_key, Section Order. Five rows, the five keys above.
   Section Order is ";"-separated canonical_section names, in reading order.

Plus research/39-notes.md, short: your sources, and any family where you had to choose a
convention rather than cite one. Say which is which — a sourced order and an invented one must
not be presented alike.

## Design constraints
- Sections must be the ones these documents actually have. An invoice has issuer, recipient,
  invoice number, dates, line items, totals, tax, payment terms. A memo has to/from/date/subject
  and a body. Do not force CV vocabulary onto them.
- Keep canonical_section names lowercase, ASCII, hyphenated, no spaces — match the existing
  style.
- Heading Text is the human-facing wording and MAY carry accents (Facture, Rechnung).

## Verify before you report
1. Every token in every Section Order cell appears as a canonical_section in either
   data/base/headings.csv or your new file. Write the check in Python and paste its output.
2. No duplicate heading_key, within your file or against the existing 81.
3. Exactly one Is Primary = yes per (canonical_section, Language).
4. Both files parse with csv.DictReader and have the exact column names given above.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the five Section
Order strings, how many new canonical sections and heading rows you added, the output of check
1, and which orders are sourced versus conventional.
