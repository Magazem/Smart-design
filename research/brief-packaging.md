# BRIEF — Packaging — Ruling H: build a badly formatted sample report fixture

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not rebuild the ZIP in this task — that is a separate brief afterwards.

## Why
Activation prompt 4 keeps failing. Describing an ugly document in words is not the same as
handing Claude one. Prompt 4 will become "attach this file", so we need a real, deliberately
badly formatted .docx that lives in the repo but never ships.

## Bound path — use exactly this
research/fixtures/badly-formatted-report.docx

Create research/fixtures/ if it does not exist. This is already safe from the build:
build_zip.py's collect_members() walks only SKILL_DIR (skill/document-design-intelligence), so
anything under research/ is structurally impossible to include. Confirm that yourself rather
than taking my word, and say how you confirmed it.

## Deliverable (ONE)
The .docx file, plus the generator script that made it at research/fixtures/make_bad_report.py
so it is reproducible.

Content: 2-3 pages of harmless placeholder business text. A quarterly-report shape is fine —
invented company, invented numbers, nothing real, nothing that reads as anyone's data.

The formatting defects, all of them deliberate:
- Headings centred and bold, in three DIFFERENT fonts across the document.
- Body text 10pt Calibri.
- Page margins 1cm on all four sides.
- Bulleted lists in three different colours.
- One garish default-styled chart or a clip-art-style image.

It must look genuinely bad, not subtly bad. This is the input to a "fix this" test.

## Tooling
python-docx is NOT installed in the system python3 shim. Options, your choice:
- Install python-docx into a throwaway venv or with uv, as you have done before, or
- Use the officecli skill available in this environment.
Say which you used. Do not add python-docx to any project requirements file — this fixture is
test scaffolding, not a runtime dependency.

## Verify before you report
1. The file opens: reload it with the same library and print the paragraph count and the
   section margins, proving the 1cm margins actually took.
2. Report the page count as rendered, or say honestly that you could not render it and are
   reporting an estimate from content length.
3. Confirm no file was written anywhere under skill/document-design-intelligence/.
4. Run `python3 scripts/build_zip.py` from the skill dir ONLY if you also then confirm no .docx
   member exists in the archive — otherwise skip the build entirely and just show the
   collect_members root.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: the file path and
size, which tool you used, the defects you actually applied, the margin check output, and how
you confirmed the build cannot pick it up.
