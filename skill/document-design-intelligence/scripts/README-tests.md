# Tests to run in claude.ai before trusting the distribution design

These settle the five unverified items from `research/15-distribution-model.md`.
Tests 1 and 2 below are **DONE** — see their results inline; do not re-run
them. Tests 3-5 are still open; each is a prompt you paste into a claude.ai
chat with this skill installed and Code Execution enabled.

See also `TESTS-FOR-USER.md` at the project root, which consolidates these
with tests from other reports under its own numbering (this file's Test 1 =
its Test 1; this file's Test 2 = its Test 6).

---

## Test 1 — does a script's write survive into a new chat? — **DONE: FAIL (confirmed by direct user test)**

**Result**: confirmed **no persistence**. Every chat gets a fresh filesystem;
nothing a script writes into the skill's own bundled directory survives past
that conversation. This was the expected outcome (by analogy to
`05-SYNTHESIS.md`'s T3 finding) and is now directly confirmed, not inferred.

**Consequence, already applied**: the re-zip-and-reupload flow in
`README.md`'s "Updating to a new version" is necessary as designed, not just
cautious — `merge_brand_kit.py` and the README were built around this result
holding, and it does.

<details>
<summary>Original test prompt (for reference — do not re-run)</summary>

**In chat A**, with the skill enabled, paste:

> Run `python3 document-design-intelligence/scripts/merge_brand_kit.py` on any
> test base zip and brand kit zip you can construct in this session (they
> don't need to be real — just valid zips matching the formats described in
> the script's docstring), so that `data/brand/<slug>/` ends up written
> somewhere inside this skill's own directory. Then tell me the exact
> directory you wrote it to.

**Then close that chat and start chat B** (same skill enabled), and paste:

> Without me telling you anything about a previous session, look inside this
> skill's own directory for a `data/brand/` folder. List what's in it, if
> anything.

</details>

---

## Test 2 — can a bundled script see a file you attach to the chat? — **DONE: attachments are NOT in the script's cwd (confirmed by direct user test)**

**Result**: confirmed. Attached files land at a **fixed, read-only mount**,
`/mnt/user-data/uploads/<filename>` — not the script's working directory, and
not somewhere a script discovers by searching. A bundled script only sees an
attachment via that absolute path (or its bare filename, if the script knows
to look there itself).

**Consequence, already applied**: `merge_brand_kit.py` now resolves both its
`base_zip` and `brand_kit_zip` arguments by trying the given path directly
first, then falling back to `<uploads-dir>/<basename>` — so a non-technical
user's Claude can pass just the attachment's filename and it resolves
correctly. Output defaults to `/mnt/user-data/outputs/`, the documented
downloadable-output location, and the script refuses outright if asked to
write into the uploads mount. See the script's own docstring (UPLOADS
DIRECTORY / OUTPUTS DIRECTORY sections) for the full contract, and
`README.md`'s "Updating to a new version" for the resulting attach-both-files
flow.

<details>
<summary>Original test prompt (for reference — do not re-run)</summary>

**In one chat**, with the skill enabled, attach any small `.zip` file (it
doesn't need valid contents) and paste:

> I've attached a zip file to this message. Without me telling you where it
> is, run a script (or a plain shell command) that locates it on disk and
> prints its exact path.

</details>

---

## Test 3 — is there a file-count or size ceiling on a Skill ZIP upload?

This one isn't a chat prompt — it's a real upload attempt.

1. Build (or ask Claude to build, using `zipfile`) a skill ZIP sized close to
   the document-library schema's own estimate: roughly a dozen CSV files
   totalling ~600–900 rows (`research/09-library-schema.md` §6), plus this
   scaffolding's scripts and references.
2. Go to **Settings → Customize → Skills → Add** and upload it.

- **Pass**: it uploads and activates normally — no ceiling in practice at this
  size.
- **Fail**: upload is rejected or silently truncated. Note the exact error
  message and the file's size/entry count at the point of failure — that
  tells us whether the limit is on total size, entry count, or something else.

---

## Test 4 — description field length limit: 200 or 1,024 characters? — DONE: RESOLVED, limit is 1,024 (confirmed)

**Result: confirmed.** The claude.ai upload UI enforces "Description must be
under 1024 characters" — note "under," so 1,023 is the practical maximum. The
200-character figure (from a support-article summary, `research/04-packaging.md`
§5) does not hold on this surface. Our shipped 667-character description
ships as-is with no truncation risk. See `references/activation.md` for the
full resolution note — the three alternates built for the truncation
contingency are retained there for reference only, not needed.

<details>
<summary>Original test prompt (for reference — do not re-run)</summary>

Edit `SKILL.md`'s frontmatter `description` field so it's a real sentence
around 600 characters long (comfortably between the two numbers reported in
`research/04-packaging.md` §1.2), re-zip the skill, and upload it via
**Settings → Customize → Skills → Add**.

</details>

---

## Test 5 — does `merge_brand_kit.py`'s `validate_data.py` call actually catch a stale brand kit?

**NOT RUNNABLE YET — requires our skill to be uploaded and installed first.**
This test exercises the live brand-merge workflow inside claude.ai, which
means our own skill zip has to actually exist as an uploaded, installed Skill
before there's anything to run this prompt against — it isn't runnable during
local scaffolding work, only after the first real release. It further depends
on `data/base/` holding the real document-design tables (still not authored —
`research/09-library-schema.md`'s schema, ~600-900 rows, is design-only so
far). `validate_data.py` itself is no longer a stub as of this writing, but
that's necessary, not sufficient — come back to this test once both
conditions hold:

> I have a brand kit built against an older version of this skill's base
> library, where one of the tables it references has since changed shape
> (a renamed or removed column). Run the brand-merge workflow with it and
> tell me whether the merge is refused with a clear reason, or silently
> succeeds and produces a broken package.

- **Pass**: the merge is refused with a message naming the specific
  incompatibility.
- **Fail**: the merge succeeds silently. That means `merge_brand_kit.py` needs
  to actually invoke `validate_data.py` on the merged result before writing
  the output zip, not just assume compatibility.
