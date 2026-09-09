# BRIEF — Packaging Analyst: step 7b, rebuild the distribution ZIP (~10 min)

Context reset by policy; nothing lost. Your 7a pass is verified and closed: SKILL.md's body
is 53 lines, zero hits for render_pdf/render_docx/scaffolding/placeholder/validated, tier
wording verbatim. Act from THIS FILE and from disk — not from chat.

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Skill dir: skill\document-design-intelligence
Python:    C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## State you are building on
The gate is ZERO: "OK: validated 14 table(s), 291 row(s)" — all 14 tables loaded, 291 rows.
The shipped `skill/dist/document-design-intelligence-0.0.1-dev.zip` is STALE: it carries the
Rev 2 manifest (173 cols, 8 FKs) and a stray `ens-manrope-inter` typeface row that is long
gone from live data. That staleness is what this brief ends.

## ONE deliverable: a fresh, correct distribution ZIP.
1. **One-word description change, RULED.** In `SKILL.md`'s YAML frontmatter, change
   "Applies **validated** layout, typography, color, print, and ATS rules" to
   "Applies **sourced** layout, typography, color, print, and ATS rules". Nothing else in
   the description. Much of the library is sourced convention rather than validated rule,
   and this is the first sentence a user sees. Keep the description under 1024 characters
   and report its new length.
2. **Fix the stale justification in make_brand_kit.py (gap (a) from load pass 4).** It still
   emits a blank `Structure Key` and justifies it in a comment with "structures.csv does not
   exist yet". That is now FALSE — structures.csv exists with 17 rows. A regenerated ENS kit
   currently ships doctypes with NO structure. Emit a real `structure_key` that exists in
   `data/base/structures.csv`, or if a brand's doctype genuinely has no match, leave it blank
   with a printed NOTE naming the table and key, per the pattern you already established.
   `schema-manifest-NOTES.md` repeats the same stale claim — fix it there too.
3. **Regenerate the ENS kit** with the corrected script so the artefact matches the code.
4. **Rebuild the ZIP** with `build_zip.py`. Then verify the built archive, by listing its
   members, contains: the current manifest (14 tables — check the md5 is 731d874f, not the
   Rev 2 one), all 14 base CSVs, `data/rationale/`, and NO `data/brand/<slug>/` path and no
   `active.json`. Your own build_zip test covers the last part; confirm it on the real
   artefact too, not only in the test.

## Do not
Touch `data/base`, `research/load-base.py`, the manifest generator, or any `research/*.csv`.
Do not touch `scripts/resolve.py` — Mechanism may still be in it.

## VERIFY
`pytest -q` from the skill dir: >= 124 passed. Note that
`scripts/tests/test_ascii_clean.py` may fail on `resolve.py` from Mechanism's in-flight
stopword work — that is NOT yours; report it and carry on.
State the new ZIP's filename, size, member count, and the manifest md5 inside it.

## REPORT
Max 8 lines to the Workflow Orchestrator, slot 01a080c5-2001-78b3-bbbe-afaae15edafa:
the description's new length, what you did for the Structure Key, the ZIP's identity and
the four archive checks, and the test count. If you approach ~10 minutes, checkpoint to
research/handover-packaging.md and stop.
