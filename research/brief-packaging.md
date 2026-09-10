# BRIEF — Packaging — v0.2 phase C: docs, release notes, rebuild

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push. Do not edit VERSION — it stays 0.0.1-dev in tree and
the tag sets it in CI.

## Bindings, all checked on disk — use these, not your memory
- 30 doctypes in data/base/doctypes.csv, 17 distinct structure keys, 17 structure rows, ALL now
  carrying a Section Order.
- **`infographic` has an EMPTY Structure Key.** It is the ONE doctype with no structure guidance.
  Do not write "every document type" without excepting it. This matters more than it looks: the
  v0.1.0 sentence was honest about a limit, and replacing it with a false absolute would be a
  worse lie than the one we are fixing.
- headings.csv: 204 rows, 52 canonical sections. Gate: 414 rows over 14 tables.
- The sentence to REPLACE is skill/document-design-intelligence/SKILL.md lines 38-42, beginning
  "`resolve` returns a full section order only for `cv-experienced`". Replace it, do not append.
- skill/README.md mentions structure only once, at line 12, in a general list. Check whether it
  needs anything; if it does not, say so rather than inventing an edit.

## Deliverable (ONE — three edits and a rebuild)

### 1. SKILL.md
Replace lines 38-42 with the truth: every document family the skill covers now resolves with a
real section order, except infographic. Keep it to the same scale as the sentence it replaces —
this is a router, not a changelog. Do not list all 30 doctypes in SKILL.md; the description
budget and the router's brevity both matter.

### 2. RELEASE-NOTES.md — a v0.2.0 section above the v0.1.0 content
Cover:
- Section guidance for all 15 previously uncovered families: 52 canonical sections, 204 heading
  rows in English, French and German, gate at 414 rows.
- The duplicate-token validator rule, opt-in per column.
- THIS EXACT DISCLOSURE, under a "Fixed" heading, wording bound by the lead:
  brochure-flyer-a4 listed one keyword twice in v0.1.0, slightly over-weighting that row; now
  gated.
- "make me a flyer" now abstains and offers the real candidates instead of resolving wrongly.
- The resolver's empty-list message no longer claims section guidance is deferred.
- KNOWN LIMITATIONS, carried over honestly: the ambiguous German deck phrase still resolves
  instead of asking; language carries no ranking weight, so a French query does not favour the
  French CV row; panel and slide COUNT and folded-panel adjacency are not modelled at all; the
  non-CV heading sections carry one wording per language with no variants.

### 3. Rebuild and verify
Run scripts/build_zip.py, then check ALL of:
1. SKILL.md member first bytes are exactly `---\n`; exactly ONE version stamp, after the
   frontmatter.
2. Zero members carry a CR byte.
3. All 14 data/base CSVs are present as members.
4. The headings.csv member has 204 data rows. Count them, do not assume.
5. The structures.csv member has 17 rows and ZERO empty Section Order cells.
6. The description still measures 831 characters and contains "appearance fixes".
7. NO member ends in .docx.
8. No data/brand/<slug>/ members and no active.json; data/brand/README.md is expected.
9. `python3 -m pytest scripts -q` — baseline 140 passed plus 8 subtests.
10. Report archive size, member count, and the schema-manifest.json md5.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the new SKILL.md
sentence verbatim, whether README needed a change, and each of the ten checks with its value.
