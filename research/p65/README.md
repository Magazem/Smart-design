# P6.5 -- portable-pack proxy trial harness

Implements the trial pre-registered in `research/87-review-r3-portable.md` section G. This
directory is the harness only (prompts, scorer, fixtures); nothing here has been run against a
model. Do not edit `prompts/` or the scorer's clause logic after the first model output has been
seen; if it must change, version it as a new trial (section G's rule).

## Contents

| file | purpose |
|---|---|
| `prompts/T1.txt` `T2.txt` `T3.txt` | the three prompts, extracted from section G by script (only the source's line wraps joined with one space) |
| `wrapper-pack.md`, `wrapper-control.md` | the fixed instruction block put before the prompt (pack arm / control arm) |
| `score.py` | deterministic scorer for the five falsifier clauses |
| `fixtures/`, `make_fixtures.py` | 3 hand-made outputs per trial: `-pass`, `-bad-hex`, `-bad-order` |
| `test_score.py` | `python3 -m pytest research/p65` (10 tests) |

## How a run is done

1. Regenerate the pack (`python3 research/build-portable.py`) and record its commit hash and the
   model name/version.
2. Fresh session per (platform x prompt x repetition), no history. Pack arm: the agent gets ONLY
   `portable/AGENTS.md` (instructions) and `portable/DDI-LIBRARY.md` (knowledge). Control arm: the
   same model, no files. Code execution OFF in every arm.
3. Send `wrapper-pack.md` (control: `wrapper-control.md`) followed by the contents of
   `prompts/T<n>.txt` as one message.
4. Save the raw reply to `research/p65-trial/<platform>/<prompt>-<n>.md` (3 runs each).
5. Score: `python3 research/p65/score.py --trial T1 --output research/p65-trial/<platform>/T1-1.md`
   (JSON; exit 0 = PASS). Score the control arm against the same pack (that is the point: it must
   fail clause 1 or 2 in at least 2 of 3 runs).
6. A human checks clauses 2 and 5 (the JSON lists them under `needs_human`), and records the T3
   `quote-devis` heading wording and the T2 slide-size note (section G) as annotations, not failures.

Success bar (section G): >= 7 of 9 runs PASS on Platform A, every prompt >= 2 of 3; control fails
clause 1 or 2 in >= 2 of 3 runs, else the trial is inconclusive.

## What the scorer checks

Values allowed = every hex, font (heading, body and safe-stack fallbacks) and `pt` size printed in
the expected doctype's block of `DDI-LIBRARY.md` (`cv-uk`, `slide-deck-projection`, `quote-devis`);
plus, if the output names a pack design whose Style/Palette/Typeface keys differ from the doctype's
own, the values the grand library gives for that design (palette line, typeface line, its type
scale, its doc style's rule weights).

1. **Out-of-pack values.** Any `#RRGGBB` (or `#RGB`) not allowed; any font declared with CSS
   `font-family:` or a `Font:`/`Typeface:` line that is not an allowed family; any pack font that is
   not allowed for this doctype appearing anywhere; any `Npt` not allowed; any `font-size` in
   px/em/rem/%.
2. **Named design.** A design key or Display Name from the family's pack table appears, or the
   output asks the user to choose and lists >= 2 pack designs.
3. **Section order.** Headings of the `=== DOCUMENT ===` part (markdown `#` or HTML `<h1-6>`) are
   mapped to canonical sections through the pack's wording (any of en/fr/de). Must equal one pack
   order for the doctype (structure order or a regional-variant order) as an ordered sequence;
   a section not in the pack = FAIL; an omitted section is allowed only if the output contains a
   disclosure phrase.
4. **Doctype.** The expected key is stated and no other doctype key is stated as `doctype: ...`;
   T1 also needs the UK/region mentioned.
5. **Claims.** No claimed .docx/.pptx/.pdf file or link, and no claim that a check/preflight/
   validation passed.

## Interpretation (where section G is ambiguous, the stricter reading was taken)

- **Any non-pt font size is a violation** (px/em/rem/%): section G says "point size" and the pack
  gives pt only.
- **Hexes:** only the doctype block's (or override design's) hexes; `#FFFFFF`/`#000000` are NOT
  free unless the pack lists them. Short `#RGB` is expanded before the check.
- **"Named design" is satisfied by a substring anywhere in the output**, including the style sheet.
  It is heuristic; the human reviewer confirms it (`needs_human`).
- **Section level.** Headings deeper than the level at which most pack headings appear are content
  (job titles, slide titles) and ignored; anything at that level or shallower that is not a pack
  heading is an added section = FAIL, except the very first heading (the title). The wrapper tells
  the agent to structure this way; output without the `=== DOCUMENT ===` marker is scored whole
  (style-sheet headings then count).
- **A run with no headings at all fails clause 3** (a design question with no document is not a
  document); the wrapper tells the agent to list designs AND continue.
- **Omissions** need a disclosure phrase anywhere in the output (`omitted`, `not provided`,
  `left out`, `no content`, ...); the phrase is not tied to the specific section.
- **Clause 5** treats any "preflight/validation/checks ... passed" sentence as a false claim even
  if the same reply also says some other check was unverified.
- The T2 "<= 6 bullets, <= 6 words" and T3 heading-language observations are *secondary* counts,
  recorded but never decide PASS/FAIL (section G lists them under Expected, not under Falsifier).
- Clause 4 for T1 accepts the doctype key in a `Doctype:` line or anywhere in the text.

## Coupling and limits

The scorer parses `DDI-LIBRARY.md` as `research/build-portable.py` writes it (block headings,
`- section order`, `### Designs (ranked) -- family: X` tables, grand-library lines). If the
generator's layout changes, `test_score.py` fails first. Fixtures are hand-made outputs, not model
outputs; passing them shows the scorer's logic, not that a model will behave.
