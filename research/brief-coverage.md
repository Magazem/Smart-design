# BRIEF — Coverage — v0.2 phase B2: the truth pass

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT run git stash — that is what wiped your first B1 pass.

## Why
B1 changed the numbers. Several comments and generated strings now describe the world as it was
before the load. Every one of them reads as authoritative and is now false. This brief makes
them true. No behaviour changes.

## Deliverable (ONE — seven edits, all in research/load-base.py unless stated)

1. **The rationale/headings.md generator prose, line ~467.** It hardcodes the literal string
   `convention (not in report 03)` and claims that distinction "governs every row". With 49
   citation groups over 204 rows that is false. Rewrite the paragraph so it describes the real
   shape: the CV rows split sourced-versus-convention against report 03; the transactional,
   long-form and marketing rows carry their own citations. Compute any number you state.
   Do NOT hand-edit data/rationale/headings.md itself — it is generated, and it says so.

2. **The T10 CHANGES string, line ~621.** It still justifies blanks with "by ruling --
   headings.csv covers CV sections only". There are no blanks now. Say what is true: all 17
   rows carry a section order, fifteen loaded from the phase A drafts.

3. **The comment block above the T10 loader, around line 595.** It asserts Section Order is
   empty on 15 of 17 rows BY RULING and points at research/36-notes.md. Rewrite it to record
   what the column IS — a group-FK list into headings.canonical_section — and that it is now
   fully populated. Keep the warning that only this loader may write data/base.

4. **The reuse rule, into the headings.md generator paragraph.** Add it so it is REGENERATED
   each load rather than hand-typed. The rule: never reuse a canonical_section across document
   classes when its FR or DE primary heading text reads as a word from the other class; check
   the actual heading text in all three languages, not just the English name. Give the three
   worked examples:
   - `summary` refused for a proposal's executive summary; its FR/DE primary is "Profil", a CV
     word. `executive-summary` authored instead.
   - `references` refused for a report's bibliography; the DE primary "Referenzen" reads as
     testimonials. `bibliography` authored instead.
   - `proposed-solution` refused for a whitepaper over its commercial-bid flavour, then REUSED
     for a pitch deck, where that flavour is correct. The rule cuts both ways.

5. **data/schema-manifest-NOTES.md section 1.4** documents every manifest key and does not
   mention `distinct_token_columns`, which you added. Document it: what it declares, why it is
   opt-in per column rather than derived from list_columns, and that page-formats."Panels mm" is
   deliberately exempt because repeated panel widths are correct.

6. **research/build-manifest.py's docstring** claims the manifest derives from
   research/09-library-schema.md Revision 4, which does not describe `distinct_token_columns`.
   Make the docstring honest about that key's provenance.

7. Re-run the loader afterwards and confirm the regenerated rationale/headings.md contains your
   new prose and the reuse rule.

## Verify — paste the actual output
1. `python3 scripts/validate_data.py data/base` — must still be `OK: validated 14 table(s),
   414 row(s)`, exit 0.
2. `python3 -m pytest scripts -q` — 138 passed plus 8 subtests.
3. The loader is idempotent: run it twice, and confirm the second run changes nothing.
4. Confirm data/base/*.csv are byte-identical to before this brief. This brief must change
   PROSE only. If a CSV moves, that is a finding — report it, do not tidy it.
5. Grep the repo for the strings you removed. None of "81 rows", "covers CV sections only", or
   "governs every row" should survive anywhere.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: each of the seven
done or not, the gate line, the test tally, the idempotency result, and the grep from check 5.
