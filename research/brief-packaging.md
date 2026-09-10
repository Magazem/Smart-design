# BRIEF — Packaging — the v0.2.0 pre-tag brief (HOLD)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not tag. Do not push. Do not edit VERSION — it stays 0.0.1-dev and CI
writes it from the tag.
DO NOT START without the go-ahead from the orchestrator.

## Counts, taken from disk by me — use these, not your memory
    constraints   47 rows      type-scales   20 rows
    headings     204 rows      structures    17 rows
    doctypes      30 rows      description  972 chars
    manifest: display_columns declared on 6 tables
    gate: OK: validated 14 table(s), 424 row(s)
    suite: 159 passed plus 32 subtests

## Deliverable (ONE) — four parts

### 1. One-line code fix
scripts/tests/test_ddi.py line 218 has `if __name__ == "__main__": unittest.main()` ABOVE
TestHandoffEndToEndOnRealData, so running that file directly never defines the class. Move the
guard to the END of the file. Harmless under pytest, wrong as written.

### 2. RELEASE-NOTES.md — a v0.2.0 section above v0.1.0
Cover, in this order:

**Added**
- Section guidance for all 15 previously uncovered document families: 52 canonical sections,
  204 heading rows in English, French and German. Note that THREE PAIRS share an identical
  section order deliberately — the two brochures, letter and cover letter, flyer and one-pager —
  because what separates each pair is page format, not content.
- Page-flow rules: a heading keeps with its first paragraph, no widows or orphans, table rows do
  not split, long tables repeat their header row, a figure keeps with its caption. These reach
  the docx renderer as keepNext, widowControl, cantSplit and tblHeader. Slides do not paginate,
  so pptx says so rather than staying silent.
- Heading sizes for report and CV type scales, so a long report hands over real heading levels.

**ONE SENTENCE, both convention.** The page-flow rules AND the heading sizes ship as convention,
not sourced. Say it plainly and in the same sentence that announces them. This library's whole
discipline is keeping sourced and conventional apart.

**Fixed**
- brochure-flyer-a4 listed one keyword twice in v0.1.0, slightly over-weighting that row; now
  gated.
- **v0.1.0's docx handoff block shipped with no page size, no font and no palette values.** The
  block is what the docx skill is handed. It now carries them, and an end-to-end test asserts it.
- A plain-text answer now keeps the resolved section order and headings; previously the structure
  was silently dropped when no file was produced.
- The activation description was corrected across several releases of this work: the trigger
  promises appearance rather than prose quality; the missing document nouns were added, including
  invoice, memo, one-pager, facture, Rechnung, devis and lettre; and the claim that creating a
  document is this skill's job now comes FIRST rather than last.

**Known limitations** — carry these honestly:
- `infographic` has no section order at all; it gets layout, typography, colour and print only.
- The ambiguous German deck phrase still resolves instead of asking.
- Language carries no ranking weight, so a French query does not favour the French CV row.
- Panel count, slide count and folded-panel adjacency are not modelled.
- Non-CV heading sections carry one wording per language, with no variants.
- characterSpacing in the docx handoff reads a column that exists in no table, so it always
  reports not present. Removing the section or authoring the column is a v0.3 decision.
- IF the user's final run still shows the French report not firing, say so: a request Claude can
  answer as a chat-native markdown summary may not reach this skill.
  ASK THE ORCHESTRATOR for that result before writing this line. Do not guess it either way.

### 3. SKILL.md and README
Check whether either still says anything untrue after all of this. Report "no change needed" if
that is the answer — do not invent an edit.

### 4. Final rebuild, with every byte check
1. SKILL.md member first bytes exactly `---\n`; exactly ONE version stamp, after the frontmatter.
2. Zero members carry a CR byte.
3. Description measures 972 and STARTS WITH "Creating any document type below". Length alone
   proves nothing — candidate L was a pure reorder.
4. The manifest member declares display_columns on 6 tables.
5. Member row counts match the table above: constraints 47, type-scales 20, headings 204,
   structures 17 with zero empty Section Order cells, doctypes 30.
6. activation.md member's fenced block equals the member's description BYTE for byte, one line.
7. SKILL.md body still contains "The output format never changes this order or these headings".
8. No .docx members; no data/brand/<slug>/ and no active.json; data/brand/README.md expected.
9. SMOKE RUN, and paste both: resolve then handoff for report-long-toc AND cv-generic, docx
   format. Page, fonts, font sizes, palette, TOC heading levels and page flow must all carry
   real values for report-long-toc. This is the check that would have caught the empty block.
10. `python3 -m pytest scripts -q` — 159 passed plus 32 subtests, plus your delta.
11. Archive size, member count, schema-manifest.json md5 in both forms.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 12 lines: the release-notes
headings you wrote, whether SKILL.md or README needed changing, both smoke-run blocks, and each
byte check with its value.
