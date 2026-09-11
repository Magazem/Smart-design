# research/test-builds — ZIPs built for ACCEPTANCE TESTING ONLY

**Nothing here is a release.** These are single-variable test artefacts for browser runs against
the user's claude.ai account. Releases are built by CI from a tag and live in `skill/dist/`.

## Why this directory exists, and the trap it avoids
On 2026-09-11 the Packaging Analyst was modifying `research/build-manifest.py` and the manifest
for the display-columns fix AT THE SAME TIME as a description test was needed. **A ZIP built
from the working tree would have carried both changes**, and the trial would have moved two
variables at once.

So these are built by patching the PUBLISHED release asset, never by running the build from the
working tree. That guarantees exactly one variable moves.

## Contents

### `_published-v0.2.0-reference.zip`
The unmodified published v0.2.0 asset, downloaded from the release:

    gh release download v0.2.0 --repo Magazem/Smart-design --pattern "*.zip"

143209 bytes, md5 `9e9f30fb08c663686bde842c41dd2c42`, 39 members, VERSION `0.2.0`.
This is the baseline every test build is diffed against. It is also exactly what was installed
in the account at the time, confirmed by the tester matching the shown description verbatim.

### `document-design-intelligence-0.2.0-candidateM.zip`
Candidate M, drafted in `research/50-candidate-M-draft.md`. 143230 bytes,
md5 `d1e7f7c3c34f377507f5da9e343cbea7`.

**VERIFIED, by real byte comparison and not by whitespace folding** (standing rule, 2026-09-10):

| check | result |
|---|---|
| member list, names AND order | identical, 39 members |
| members whose md5 differs | exactly one: `document-design-intelligence/SKILL.md` |
| lines differing within SKILL.md | exactly one, line 3 (the `description:` line) |
| CR bytes in SKILL.md | 0 |
| VERSION | `0.2.0`, unchanged |
| description length | 972 -> 1005 characters, cap 1023, headroom 18 |

The single change, the whole of it:

    OLD:  ... still this skill's job even as Word or PowerPoint; defer to ...
    NEW:  ... still this skill's job even for '.docx'/'.pptx' requests naming Word or PowerPoint; defer to ...

Smoke-tested from the extracted tree: `resolve.py --doctype cv-uk --json` runs clean and the
docx handoff renders.

## NO TEST-FILE EDIT WAS NEEDED — worth knowing before the next one
Candidate M breaks `NEGATIVE_HEAD_MARKER`, which is the deferral sentence verbatim, so the
repo's `scripts/tests/test_description_coverage.py` needs a paired edit **if M is ever applied
to the repo**. It did NOT need one here: **the published ZIP ships no tests at all.** Its 39
members include `scripts/` but no `scripts/tests/`. Checked, not assumed.

So a description test build touches exactly one file. The paired marker edit belongs to the
apply-to-repo change, not to the test artefact.

## HOW THE TESTER TELLS THE BUILDS APART
Both descriptions open with the same words, so "first words match" does NOT distinguish them.
**Candidate M is installed if the shown description contains `'.docx'/'.pptx'`.** v0.2.0 as
published does not contain that string anywhere.

---

## `v03-candidate.zip` and `v03-extracted/` — the v0.3 build under test

Built 2026-09-11 by `scripts/build_zip.py` from a green tree. 147016 bytes,
md5 `1cb0b8c9388567708d855b3c6f570fb6`, 39 members, **zero CR bytes across the whole archive**.

`v03-extracted/` is that ZIP unpacked. **The invoked-quality pass runs against the EXTRACTED
ARTEFACT, never the working tree.** That is the lesson of 2026-09-11: six matching reference
values did not prove a dev build matched the release, because none of them would catch a
difference in `resolve.py`, `ddi.py` or the manifest — which is exactly where every defect lived.

### Verified against the published v0.2.0, member by member
Same 39 members, no additions or removals. **Twelve differ, and every one is expected:**

    SKILL.md                      description + png in the workflow line + version stamp
    VERSION                       0.0.1-dev (CI rewrites this from the tag)
    data/base/doc-reasoning.csv   infographic style/palette/typeface pointers
    data/base/doc-styles.csv      infographic-bold
    data/base/doctypes.csv        infographic constraint set + structure key
    data/base/structures.csv      infographic-canvas
    data/base/type-scales.csv     infographic-screen
    data/base/typefaces.csv       safe-sans-deck, safe-sans-infographic
    data/rationale/doc-reasoning.md
    data/schema-manifest.json     display_columns on 8 tables, was 6
    references/activation.md      the mirrored description + its length caption
    scripts/ddi.py                headings/structures handoff, pdf blocks, png builder,
                                  characterSpacing removed

SKILL.md's only three differing lines are the description, the build stamp, and the workflow
line gaining `png`.

### THE ONE DIFFERENCE FROM WHAT WILL SHIP
`VERSION` reads `0.0.1-dev` and SKILL.md's stamp matches it. **CI writes both from the git tag**,
so the released artefact differs from this one in those two places and nowhere else. Anything the
quality pass finds here holds for the release; anything it says about the version string does not.


---

## REBUILD after the ship-blocker fix (2026-09-11)
146987 bytes, md5 `4bc58aaf053b90e6762d59221be490fa`, 39 members, zero CR bytes.
Supersedes the earlier candidate; `v03-extracted/` is this one.

### The gate's own acceptance condition, re-run on the artefact
The v0.3 gate returned DO NOT SHIP on one defect and pre-registered exactly what would clear it:
fix it, then re-run the three pdf-only families asserting `issuer: From` appears in the pdf
block. Run from inside the extracted tree with an absolute `--data-dir`:

    quote-devis          sections block present -> issuer: From / bill-to: Bill To / invoice-details: ...
    invoice-tabular      sections block present -> issuer: From / bill-to: Bill To / invoice-details: ...
    brochure-trifold-a4  sections block present -> headline: Headline / introduction: Introduction / key-points: ...

**Condition met.** Note it was stated BEFORE the fix existed, which is what makes clearing it
mean something -- the pre-registered-falsifier rule applied to an acceptance gate rather than an
experiment.

### Shared-core parity, measured on the artefact rather than in the suite
Every builder emits all four core blocks:

    docx  cv-uk                  sections 1  fonts 1  sizes 1  palette 1
    pptx  slide-deck-projection  sections 1  fonts 1  sizes 1  palette 1
    pdf   quote-devis            sections 1  fonts 1  sizes 1  palette 1
    png   infographic            sections 1  fonts 1  sizes 1  palette 1

The artefact's own source files were not modified by testing. Running the scripts does leave
`__pycache__` directories under `scripts/`; those are removed after each run and are not part of
the archive.
