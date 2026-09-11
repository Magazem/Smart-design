# PREP — reverting candidate L (NOT EXECUTED)

Written 2026-09-11 by the Workflow Orchestrator (sub-manager) while step 1(a) was blocked.
**Nothing here has been applied.** This exists so the revert is not a scramble if the clean
run of activation 11 comes back docx-only.

Lead's ruling, 2026-09-11: 1(b) is a live-account change and is the USER's to perform. If 1(a)
fails, I prepare the reverted ZIP on disk, byte-verify it, and hand the lead the path. I do not
touch the account.

## The commit to revert
`f23fb03` — "Apply candidate L: the priority claim now comes first" (2026-09-10).
It touches THREE files and they must move together:
1. `skill/document-design-intelligence/SKILL.md` — the description reorder
2. `skill/document-design-intelligence/references/activation.md` — the shipped "as shipped" block
3. `skill/document-design-intelligence/scripts/tests/test_description_coverage.py` — the markers

**Do not revert only the description.** The commit raised the test from one marker to two
precisely because the reorder broke it. Reverting file 1 without file 3 leaves
`NEGATIVE_HEAD_MARKER` pointing at a sentence that no longer exists, which now raises
`AssertionError` rather than passing silently. Loud, but still a broken build.

## Measured values — method stated, per the byte-comparison standing rule
Both measured by decoding the file as UTF-8 and regexing the frontmatter, then taking
.NET `String.Length` for characters and `UTF8.GetByteCount` for bytes.

| build | characters | UTF-8 bytes |
|---|---|---|
| current (candidate L, on disk) | 972 | 975 |
| pre-L (`f23fb03^`) | 972 | 975 |

Identical on both counts, as the commit message claims: the only token difference across the
972 characters is `above` becoming `below`. Cap is 1023, so headroom is 51 either way.

**A measurement trap on this machine, recorded so nobody repeats it.** `python` does not run
here (uv trampoline: "entity not found"). `wc -m` in this shell is NOT UTF-8 aware and silently
returns the BYTE count. The description holds three two-byte characters — the é in dépliant,
the é in présentation, the ü in Broschüre — so a byte count overstates the length by exactly 3
and reads as 975. RESUME.md's published figure of 972 characters was correct; only line 1246's
"831 characters, headroom 192" is stale, dating from candidate F and predating L.

## Verification required before handing over any built ZIP
- Extract the built ZIP and compare its SKILL.md description to `f23fb03^`'s **byte for byte**,
  not after whitespace folding. Per the standing rule of 2026-09-10: if a report says
  byte-identical it means the bytes were compared; if whitespace was folded, say "equal after
  whitespace folding".
- Re-run the description coverage test and confirm it PASSES rather than raising on a missing
  marker.
- Confirm the ZIP is otherwise identical to the published v0.2.0 asset, so the run isolates the
  description and nothing else.

## Restore
The revert stays on disk only. Once the trial is done the working tree returns to `main` at
candidate L. The orchestrator owns that, as it owns all git here.
