# research/74-heading-language.md -- A7: heading language follows the document, not the structure

## What changed

`structures.csv."Heading Language"` was a per-structure constant of `en` on every row, so
every doctype handed over English section headings even though `headings.csv` authors 63 fr
and 63 de rows (research/64 D-E, confirmed by the A5 judges on cv-dach).

1. **`doctypes.csv` gained a `Default Language` column** (`en`|`fr`|`de`), authored in
   `research/26-t1-doctypes-draft.csv` and declared in `research/build-manifest.py`
   (`language_column`, mirroring `resolve.py`'s existing `description_column` idiom).
   `cv-dach`→`de`, `cv-france`→`fr`, the four `ens-*` doctypes→`fr` (French Display Names,
   Brand Scope `ens`), the other 28 doctypes→`en`. Criterion and full table:
   `skill/document-design-intelligence/data/rationale/doctypes.md` (CONVENTION, no external
   authority -- keyword presence cannot discriminate, since almost every CV doctype's
   `Keywords` cell carries all three languages' request phrasing).
2. **`resolve.py` gained `--lang en|fr|de`.** The resolved JSON always carries a top-level
   `"language": {"value": ..., "source": "override"|"doctype-default"}` block.
3. **`ddi.py`'s `_section_headings`** now picks each section's primary heading in the
   *resolved* language, not the structure's `Heading Language` column. That column is now
   only the FALLBACK: a section missing a primary heading in the resolved language falls back
   to it and prints `(no <lang> wording authored; <fallback-lang> used)` on that line -- never
   silently. The `sections` header states the language actually used and its source
   (`sections (Section Order, language=de, source=doctype-default):`). This required
   threading a `language` argument through all four `_FORMAT_BUILDERS` and
   `_build_handoff_lines` (the largest structural edit -- the language block lives one level
   above the per-table `resolved` dict those builders previously took as their only argument).
4. **`HANDOFF_EXCLUSIONS` updated, two entries:**
   - `doctypes."Default Language"` (new, all 4 formats): excluded as
     "not applicable: consumed by resolve.py to build the top-level `language` block
     ... no handoff builder reads it as a doctypes table cell" -- the value reaches the
     handoff via the payload's `language` argument, not via the resolved `doctypes` row.
   - `cv-regions."Language Expectation"`: reason corrected from the generic bundled
     "not yet wired: backlog cv-regions design columns" to
     "not applicable: free-text regional advisory prose ..., not a discrete renderable
     value", distinguishing it explicitly from the new `doctypes."Default Language"` (the
     *rendered document's* language) -- this column is about the *CV content's* expected
     language (e.g. "English standard for multinational/private-sector roles; Arabic for
     government/local-market roles"), unstructured prose the schema already refuses to treat
     as a list (`build-manifest.py`'s own comment on this column).
   - `structures."Heading Language"` needed **no change**: it already had no
     `HANDOFF_EXCLUSIONS` entry (it's named in `HANDOFF_VOCAB` and was already read) --
     the task's premise that it needed updating from "excluded" to "fallback that IS read"
     did not hold; it was already read, just for the wrong purpose (selection, now fallback).
5. **`make_brand_kit.py` regression found and fixed.** Regenerating `data/base/doctypes.csv`
   surfaced that the brand-kit generator (used to build `data/brand/ens/doctypes.csv`) emits
   no `Default Language` at all -- the new enum then failed 4 rows. Fixed by defaulting brand
   doctype rows to `en` (documented as this tool's parse-nothing stopgap; adding brand-markdown
   language parsing is out of this fix's scope).

## Census (research/heading_reach.py, run against the regenerated data)

| | reachable | unreachable |
|---|---|---|
| BEFORE (Heading Language hard-coded `en`) | 74 (en=74, fr=0, de=0) | 121 (fr=60, de=61) |
| AFTER (Default Language + `--lang` override) | 195 (en=74, fr=60, de=61) | **0** |

9 rows (`volunteering-{en,fr,de}-*`) are excluded from both counts as **orphans** -- their
`canonical_section` ("volunteering") appears in no structure's or cv-region's `Section Order`
that any doctype resolves, a pre-existing defect unrelated to language selection, not folded
into either count.

## Tests (red-then-green, `scripts/tests/test_heading_language.py`)

Before the fix: 7 failed (`KeyError: 'language'`, `unrecognized arguments: --lang`, missing
German/French wording in the docx handoff, missing fallback text), 1 trivially passed.
After: all 8 pass, plus the existing suite is unaffected --
**197 passed / 174 subtests passed** (baseline 189/162 + this task's 8 new tests / 12 new
subtests), from `skill/document-design-intelligence`. `python3 scripts/validate_data.py
data/base` -> `OK: validated 14 table(s), 477 row(s)`. `research/load-base.py` run twice in a
row produces no further diff (only `data/base/doctypes.csv`, `data/schema-manifest.json`, and
the new `data/rationale/doctypes.md` changed on the first run).

## Addendum: cv-dach Reasoning Key revert (landed in this same regeneration, orchestrator-confirmed)

Per the Orchestrator (research/72 §scoped decision), `cv-dach`'s `Reasoning Key` was reverted
from the A4 default `cv-dach-tabular` back to `cv-ats-strict` in the same
`research/26-t1-doctypes-draft.csv` edit; `cv-us`/`cv-uk`/`cv-generic` stay on
`cv-us-uk-designed`, unchanged. This is unrelated to A7's heading-language fix but landed in
the same final regeneration at the Orchestrator's instruction. Effect: cv-dach now resolves
`safe-sans-arial` (single-family) instead of `pt-serif-sans` (heading/body pair), which makes
`pt-serif-sans` unreachable from any doctype's docx-office path. This broke
`TestDocxSafeStackFallbackIsAHeadingBodyPair`'s premise (it named cv-dach as one of "the two
doctypes that hit docx-office with a two-family pairing") -- fixed by dropping cv-dach from
that test's `EXPECTED` table, since only cv-uk exercises a two-family docx pairing now.
Final suite after both changes, from `skill/document-design-intelligence`:
**197 passed / 173 subtests passed** (one fewer subtest than the interim heading-language-only
run, from removing cv-dach's now-invalid case there). Second `research/load-base.py` run
confirmed a no-op (`diff -rq` clean) after the revert; `validate_data.py data/base` -> OK, 14
tables/477 rows. Heading-language census unaffected by this revert (74/121 before,
195 reachable / 0 unreachable non-orphan after -- unchanged, since cv-dach's language and
section order didn't change, only its typeface).

## The fallback rule

`_section_headings(resolved, language)`: target language = `language["value"]` (override or
doctype-default), fallback language = the resolved structure's own `Heading Language` column
(today always `en`, but the enum permits `fr`/`de`, so the code reads the actual value rather
than hardcoding `"en"`). For each section in `Section Order`: look up the primary (`Is
Primary=yes`) heading in the target language; if absent AND target != fallback, look it up in
the fallback language instead and append `(no <lang> wording authored; <fallback-lang>
used)` to that line. If absent in *both*, the line degrades to `(not present in this
resolution)` with no fallback note -- that is an unrelated data gap (or, with today's fully
covered data, unreachable), not a language failure, and must not be misreported as one.
