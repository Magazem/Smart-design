# Release checklist — cutting v0.1.0

Repo: https://github.com/Magazem/Smart-design.git
Workflow: `.github/workflows/release.yml`, triggers on push of a tag matching `v*.*.*`.
That workflow writes `skill/document-design-intelligence/VERSION` from the tag itself
(`GITHUB_REF_NAME`), runs `build_zip.py`, and publishes the ZIP as a release asset with
`RELEASE-NOTES.md` as the release body. Do not hand-edit `VERSION` — it stays
`0.0.1-dev` in the tree; CI overwrites it at build time from the tag you push.

## 1. Pre-flight (local, before tagging)

From `skill/document-design-intelligence`:

```
pytest -q
python3 scripts/validate_data.py data/base
python3 scripts/build_zip.py
```

All three must pass clean (128+ tests passing, 14 tables OK, ZIP built with no
constraint-check failures) before you tag. If any of them fail, stop — do not tag
a red tree.

Confirm the release body the workflow will publish is correct — `RELEASE-NOTES.md`
holds every past version stacked in one file, and the release job extracts only the
`# vX.Y.Z` section matching the tag. From the repo root, with `VERSION` set to the
version you're about to tag:

```
awk -v header="# v$VERSION" '
  $0 == header { printing=1 }
  printing && /^# v/ && $0 != header { exit }
  printing { print }
' RELEASE-NOTES.md
```

The output must start with `# v$VERSION` and must NOT contain any other `# v` section
header. If the output is empty, the workflow will fail the job rather than publish a
blank body — add the section to `RELEASE-NOTES.md` before tagging.

## 2. Commit anything outstanding

Confirm `git status` is clean (everything you want in the release is already
committed to the branch you're about to tag). `skill/dist/` is gitignored — the
local ZIP you just built is a verification artifact only, not something to commit.

## 3. Tag and push

From the repo root:

```
git tag v0.1.0
git push origin v0.1.0
```

Pushing the tag is what triggers the workflow — pushing commits alone does not.
If you tag the wrong commit, see the rollback section before pushing.

## 4. What you should see afterwards

- A new workflow run under the repo's **Actions** tab, named "Release", triggered
  by the `v0.1.0` tag push.
- On success, a new entry under **Releases** tagged `v0.1.0`, with one asset:
  `document-design-intelligence-0.1.0.zip`.
- The release body is the contents of `RELEASE-NOTES.md` (the scope statement and
  known limitation), with the auto-generated commit list appended underneath it
  (`generate_release_notes: true` stays on alongside `body_path`).
- If `validate_data.py` or the ZIP constraint checks fail inside the job, the
  workflow fails and **no asset is published** — this is deliberate fail-closed
  behavior, not a bug. Fix the underlying issue, delete the bad tag (see
  rollback), and re-tag.

## 5. Verify the published asset is the right one

Download the asset from the release page and confirm it matches what you checked
locally before tagging:

```
python3 -c "
import zipfile, hashlib
z = zipfile.ZipFile('document-design-intelligence-0.1.0.zip')
names = z.namelist()
print('members:', len(names))
print('manifest md5:', hashlib.md5(z.read('document-design-intelligence/data/schema-manifest.json')).hexdigest())
print('VERSION:', z.read('document-design-intelligence/VERSION').decode().strip())
"
```

Expected: 39 members, manifest md5 `731d874ff6052d8c3809a3d44a9d4196`, VERSION
`0.1.0` (not `0.0.1-dev` — if VERSION still reads `0.0.1-dev` in the published
asset, the tag-derived version step did not run correctly and the release should
be pulled).

## 6. Roll back a bad tag

If you discover the tagged commit was wrong, or the published asset is bad,
**before** telling anyone to use it:

```
# Delete the GitHub release (via the web UI: Releases -> the bad release -> Delete),
# or with gh:
gh release delete v0.1.0 --yes

# Delete the remote tag (this does NOT retrigger the workflow by itself):
git push origin :refs/tags/v0.1.0

# Delete the local tag:
git tag -d v0.1.0
```

Fix the issue, then restart from step 1. Do not reuse `v0.1.0` for a different
commit without deleting both the release and the tag first — a tag pushed to a
new commit under the same name will not automatically replace a stale asset
that's already been downloaded by someone else.

## What v0.1.0 does and does not contain

- Full section-by-section structure guidance: **CVs only** (`cv-experienced`,
  `cv-academic`).
- Layout, typography, colour, and print guidance: **every document type the
  skill covers**, CV and non-CV alike.
- Section-by-section headings for the non-CV document families: **not in this
  release** — deferred to step 9.
- PDF: PDF/X-4 structurally emitted; conformance not independently verifiable
  with open tooling. Do not claim more than that.
- Known limitation: one ambiguous German deck phrase resolves to the projection
  variant instead of asking which was meant. The three deck rows tie on score
  and the tie is broken by row length. The resolver otherwise resolves when
  confident, asks which of the real candidates you meant when a request is
  ambiguous, and says plainly when nothing matches.

See `RELEASE-NOTES.md` at the repo root for the version of this statement that
ships with the GitHub release itself.
