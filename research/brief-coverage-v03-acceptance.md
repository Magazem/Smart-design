# BRIEF — Coverage and Gap Analyst — v0.3 INVOKED-QUALITY PASS ON THE BUILT ARTEFACT

Deliverable: `research/64-v03-acceptance.md`. This is **the gate before tagging v0.3.**

## WHAT YOU ARE TESTING — and this is the whole point of the brief
**The EXTRACTED BUILT ARTEFACT, not the working tree:**

    research/test-builds/v03-extracted/document-design-intelligence/

Run everything from inside that directory. **Do not run anything from `skill/`.** If you find
yourself resolving against the working tree, stop and start again from the extracted path.

WHY, because you hit this yourself earlier today: you exercised a local build and argued it
matched the release on six reference values. It did — but those six were five row counts and a
description, and **none of them could have detected a difference in `resolve.py`, `ddi.py` or the
manifest**, which is exactly where every defect of this release lived. The orchestrator had to
download the published asset and re-run your checks to establish the P0 was real in the shipped
product. That round trip is what this brief exists to avoid. **Test the artefact.**

Provenance, already verified, so you do not need to redo it:
- 147016 bytes, md5 `1cb0b8c9388567708d855b3c6f570fb6`, 39 members, zero CR bytes
- same member list as published v0.2.0; 12 members differ, all expected, itemised in
  `research/test-builds/README.md`
- **`VERSION` reads `0.0.1-dev` and CI rewrites it and the SKILL.md stamp from the git tag.**
  That is the ONLY difference from what ships. Findings about behaviour carry to the release;
  anything about the version string does not. Say so if you mention it.

## WHAT CHANGED SINCE YOUR LAST PASS — verify each, do not take it on trust
Your v0.2.0 pass (`research/51-invoked-quality.md`) ranked seven defects. Five were fixed:
1. **D1, the P0.** Heading wording reaches Word, PowerPoint, PDF and plain text. The hidden
   columns on constraints, structures and type-scales are surfaced.
2. **D2.** The PDF handoff gained sizes, heading levels and palette.
3. **D3.** A projected deck gets its own type scale instead of the CV's print scale.
4. The png handoff builder exists; `--format png` is accepted.
5. `infographic` is a real family, and the description now names it in three languages.

**Confirm each independently. A fix you cannot demonstrate from the artefact is not fixed.**

## THE STANDARD, unchanged and non-negotiable
**Validation proves rows are well-formed. Only an end-to-end test proves the output SAYS
something.** Every defect this release fixed had the same shape: valid data, exit 0, green gate,
empty answer. **A green gate is not a result. Do not report one.**
For every check ask what it would say if the feature produced NOTHING AT ALL. If the answer is
"it would pass", it is not a test.

## SCOPE
Same frame as before: append `Use the document-design-intelligence skill.` so firing is
guaranteed. **Score OUTPUT QUALITY, not activation.** Routing is closed to you — six description
candidates have now been refuted and the workaround is documented.

Cover the distinct output paths, **including every format**: docx, pptx, pdf AND png. At least
one non-English family. Include `infographic` and `slide-deck-projection`, which are new or
changed. Re-check `cv-uk` as your control — it must be unchanged, and a regression there is the
most serious thing you could find.

Per family, as separate fields: zero "not in my library" refusals; sections present and in
documented order; **each handoff value INDIVIDUALLY** — page/canvas, margins, fonts, heading
levels and sizes, palette, page flow; the plain-text path; and your judgement on whether this
is a designed document or a generic one wearing the skill's name.

## HARD RULES
- **No git, ever.** The orchestrator owns git.
- Never hand-edit a generated file; name the generator.
- Tag CONVENTION for anything not grep-verifiable in the artefact.
- `python` is broken here; use **`python3`**.
- **Write `research/64-v03-acceptance.md` incrementally as you go.** You were paused twice today.

## THE QUESTION THIS PASS ANSWERS
**Is v0.3 good enough to tag?** Give a plain verdict: SHIP or DO NOT SHIP, with the defects that
justify it ranked worst first. A "do not ship" with a real defect behind it is a good outcome and
is the reason this gate exists. Do not soften it.

Report to me in a few lines: formats covered, refusal count, verdict, top three findings.
