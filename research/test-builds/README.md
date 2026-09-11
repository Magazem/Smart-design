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
