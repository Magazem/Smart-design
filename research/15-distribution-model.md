# Distribution Model — Brand Overlay, Package Layout, Release Pipeline

Answers `09-library-schema.md` §7 Q4. Builds on `04-packaging.md` (ZIP mechanics, 3-tier
loading, claude.ai limits) and `11-upstream-releases.md` §3/§5 (no claude.ai asset has ever
shipped upstream; upstream's own version-manifest automation broke and nobody noticed for a
month — the release pipeline in §4 below is designed specifically so that class of bug is
structurally impossible, not just avoided by discipline).

## Recommendation, stated first

The schema's Q4 names three options: edit shipped CSVs (breaks updates), a `brand/` overlay
merged at load (unverified assumption), regenerate the whole package (what ENS did by hand).
**The answer is not one of the three — it is the overlay for runtime resolution, combined with
option (c) automated rather than manual for distribution.** A `data/brand/<slug>/` overlay
directory is real and necessary: it is what makes brand rows searchable (`09-library-schema.md`
§0.3), and nothing about the claude.ai ZIP format forbids it (§1 below). But claude.ai's
persistence unit is **the whole uploaded ZIP, not a patchable directory** — there is no
"upload just this one file into my existing skill" operation (confirmed: `04-packaging.md`
§1.3, "Custom Skills are individual to each user," uploaded as a complete ZIP via
Settings → Skills → Add; there is no partial-update API on that surface). So every time base
or brand changes, *some* full package has to be rebuilt and re-uploaded. The design question is
not whether to regenerate — it is **who does the regenerating**: ENS's answer was a human,
by hand, once. Ours is a bundled stdlib script the user runs *inside a claude.ai chat*, so the
"regenerate" step costs the user an attach-and-ask, not a local unzip/edit/rezip workflow they
may not have the tools or confidence for. §2 gives the exact steps.

---

## 1. Overlay feasibility

**Yes, a stdlib-only resolver can merge `data/base/*.csv` with `data/brand/<slug>/*.csv` at
load time, with no constraint from the ZIP mechanism that rules it out.**

- **ZIP-root rule**: per `04-packaging.md` §1.3, the constraint is that the archive contains
  exactly one top-level directory (the skill's own folder, matching its `name`) with `SKILL.md`
  directly inside it — it says nothing about internal nesting depth. `data/base/` and
  `data/brand/<slug>/` as subdirectories inside that one top-level folder are ordinary internal
  structure, no different from upstream's own `data/stacks/` (`04-packaging.md` §1.1). Not a
  constraint.
- **File count**: no documented ceiling was found anywhere in Anthropic's docs (`04-packaging.md`
  §1.2 — "no practical limit on bundled content, files don't consume context until accessed").
  At the schema's own estimate of ~600–900 rows across 11 CSVs (`09-library-schema.md` §6), plus
  a handful of reference `.md` files and 5–6 scripts, plus one small directory per installed
  brand (a handful of CSV files each, since a brand overlay only needs to supply rows for the
  tables it actually overrides — see worked example below), total file count stays in the low
  dozens to low hundreds. This is far below anything likely to hit an undocumented limit, but
  **it is genuinely unverified — no ceiling is stated anywhere I could find.** Test: build a
  full-size skill ZIP (11 base CSVs at the §6 row estimates, one populated brand overlay) and
  upload it in Settings → Skills; if it's rejected, the limit is on file count, entry count, or
  total ZIP size, and only that test tells you which.
- **Stdout-only consequence**: because only a script's stdout enters context (`04-packaging.md`
  §1.2), the merge must happen *inside* a script that prints the final resolved decision, not by
  having Claude read both CSVs into context and reconcile them itself. This is a design
  constraint on `scripts/resolve.py`, not a blocker: it should behave like upstream's
  `search.py` (`04-packaging.md` §1.1) — read every CSV it needs, do the two-pass brand
  resolution in Python, and print one compact result (the resolved key set + emitted values),
  never the raw table contents.

### Directory layout

```
data/
  base/
    doctypes.csv
    doc-reasoning.csv
    doc-styles.csv
    palettes.csv
    typefaces.csv
    type-scales.csv
    page-formats.csv
    render-targets.csv
    constraints.csv
    structures.csv
    figures.csv
  brand/
    active.json                 <- {"active": "ens"} or {"active": null}
    ens/                         <- present only once a brand is installed
      doctypes.csv               <- brand rows only, e.g. ens-note-interne
      doc-reasoning.csv
      palettes.csv
      typefaces.csv
      (any subset of the 11 table filenames — a brand overlay
       need not touch every table, only the ones it customises)
```

### Merge rule

`scripts/resolve.py`, on startup:

1. Read `data/brand/active.json`. If `active` is set and `data/brand/<active>/` exists, that
   is the active brand for this resolution; otherwise resolution is generic-only.
2. For each of the 11 table names, load `data/base/<table>.csv` unconditionally. If
   `data/brand/<active>/<table>.csv` exists, load it too and **append** its rows to the
   in-memory table (this is where each brand row's `Brand Scope` column, already set to the
   brand's slug per `09-library-schema.md` §0.3, comes from — the file lives under a
   brand-named directory, so the loader stamps or verifies that column rather than trusting
   free text).
3. **Key-collision rule, hard fail**: before any row is used, check every table's primary slug
   column (`doc_key`, `doc_category`, `style_key`, …) for duplicates *within the merged table*.
   A brand CSV is expected to introduce **new** slugs (`ens-note-interne`, `ens-office-document`,
   …); if a brand row's slug collides with an existing base slug, that is not a valid override —
   it is silent shadowing of a differently-authored row — and the resolver refuses to run,
   printing which file and which slug collided. This is the schema's own instinct (§0.3's
   `validate-brand-resolution` is a preflight hard-fail already; this is the same posture applied
   one step earlier, at load rather than at resolution).
4. Resolution then proceeds exactly as `09-library-schema.md` §0.3 specifies: try
   `Brand Scope == <active>` first, fall back to `Brand Scope == generic`. Because only one
   brand can be active at a time (`active.json` names one slug), cross-brand collisions between
   two *different* installed-but-inactive brand directories are inert by construction — the
   resolver never loads a non-active brand's files. Multi-brand-simultaneous merge was not
   something the ENS evidence asked for (one org, one identity) and is out of scope.

**Security note for the scripts that populate this directory** (relevant because two of the
scripts in §3 unpack ZIPs the user attaches, which is untrusted input by definition): use a
safe-extract helper that resolves every archive member's path and rejects any that escape the
target directory (`../`-style zip-slip), rather than calling `ZipFile.extractall()` directly.
Also validate the brand slug itself against `^[a-z0-9-]+$` before it is ever joined into a
filesystem path — an attacker-controlled or fat-fingered slug like `../../etc` must be rejected
before it reaches `os.path.join`, not sanitized after.

---

## 2. The update story

**The constraint that decides this whole section, restated plainly**: a claude.ai custom Skill
is one uploaded ZIP per account, with no partial-update path (§ recommendation, above). Whatever
isn't inside the ZIP the user uploads is not there next session. Two consequences follow
immediately, and both are currently **unverified assumptions** flagged for a direct test rather
than asserted as fact:

- It is unconfirmed whether files a bundled script *writes* into the skill's own directory
  during one chat (e.g., unpacking an attached brand-kit ZIP into `data/brand/ens/`) survive
  into a **new, separate** chat with the same skill active. `05-SYNTHESIS.md`'s T3 finding
  ("does a generated design system survive into a fresh session? expect NO") was about a
  different mechanism (a design-system file written by upstream's `design_system.py`) but the
  underlying claim — the code-execution container is ephemeral per conversation — would apply
  identically here if true. **Assume NO** until tested. Test: in chat A, run the brand-merge
  script (unpacks a brand kit into the skill's live directory); in a brand-new chat B with the
  same skill enabled, ask the resolver to list installed brands; if `ens` is missing in chat B,
  the assumption is confirmed and the design below (which does not depend on in-session
  persistence) is the only correct one.
- It is unconfirmed whether a file the user attaches to a chat (their saved brand-kit ZIP) is
  visible to a bundled script in the same working directory as the skill's own files, or lives
  in a separate uploads path the script would need to search for. Test: attach a small ZIP in a
  chat with the skill enabled and ask Claude to run `ls -la .` (and, if that doesn't surface it,
  a broader but still-safe listing of likely upload locations) before assuming a fixed path.

**Given those two unknowns, the design below is deliberately built to not depend on either
resolving favorably** — it treats every chat as starting from exactly what was last uploaded in
Settings → Skills, and nothing else.

### Concrete steps: base v1 + brand installed → base v2 ships

1. **We publish** `document-design-intelligence-v2.0.0.zip` (base only — no brand folders; see
   §3, brand directories are never part of our release artifact).
2. **User downloads** that file from our GitHub Release page (one link, one file).
3. **User goes to claude.ai → Settings → Customize → Skills**, finds their existing skill entry,
   and replaces it — uploads the new ZIP over the old one. **What survives**: nothing brand-
   specific. This upload is base v2 only; any `data/brand/ens/` content that was baked into the
   *previous* upload is gone, because the previous upload — brand folder and all — has just been
   discarded wholesale. This is expected and is why step 4 exists.
4. **User starts a new chat** with the (now base-v2-only) skill enabled, and **attaches the
   `my-brand-kit.zip` file we gave them the first time they set up their brand** (see the
   first-install flow below — this is the one artifact the user is responsible for keeping,
   and it is deliberately tiny: a handful of brand-only CSVs, not the whole skill).
5. **User asks**: "Install my brand from the attached kit." `scripts/merge_brand_kit.py`
   (bundled in the skill, stdlib-only): safely extracts the attachment, writes its contents
   into `data/brand/<slug>/` inside the *current session's* copy of the skill directory, runs
   `validate_data.py` against the merged result (catching a stale brand kit that references a
   base table column which changed shape between releases — a real risk of decoupling brand
   from base release cycles, worth surfacing immediately rather than at generation time), then
   immediately **re-zips the entire current skill directory** (base v2 + the newly-merged brand
   folder) into one file and returns it to the user as a chat download. This is the "regenerate
   the package" step from the schema's Q4 — automated, not hand-done — and it exists *precisely
   because* nothing written mid-session is assumed to persist.
6. **User downloads that returned ZIP and uploads it in Settings → Skills**, replacing the
   base-v2-only upload from step 3. This final upload is the one that persists: base v2 rows +
   the user's brand overlay, baked together, as the one artifact claude.ai actually keeps.

### First-time brand install (no prior kit)

Same mechanism, run once: user describes their brand (colors, fonts, voice — or attaches
existing brand assets) in a chat with the skill enabled, asks the skill to set it up.
`scripts/build_brand_kit.py` turns the answers into rows across whichever of the 11 tables the
brand needs to override (typically `doctypes.csv`, `doc-reasoning.csv`, `palettes.csv`,
`typefaces.csv` per the ENS evidence — `05-SYNTHESIS.md`'s "WHAT THE IDENTITY DOES AND DOESN'T
COVER" list), writes `data/brand/<slug>/` and sets `active.json`, then returns **two** files:
a small standalone `my-brand-kit.zip` (just the brand folder — this is what the user saves
permanently and re-attaches after every future base update, per step 4 above) and the full
merged skill ZIP (what they upload right now, to start using it today).

### Why not a runtime-only overlay with no re-zip step

Considered and rejected for the reason stated at the top of §2: it requires in-session writes to
survive to future sessions, which the best current evidence (T3, by analogy) says they do not.
If that assumption turns out to be *wrong* — i.e., if claude.ai's custom-skill storage for a
given account really is a persistent, script-writable volume across conversations, not a
frozen upload — the re-zip-and-reupload dance in steps 5–6 becomes unnecessary and step 5's
script could instead just write the merge in place and be done. **That would be a strictly
better outcome and is worth testing directly** (see the test above) before committing engineering
effort to the reupload flow as permanent UX; it's the safe default, not a confirmed requirement.

---

## 3. Package layout

One canonical folder, no symlinks (per `04-packaging.md` §3 — the Windows-broken-symlink finding
applies to us too if any contributor ever zips this repo directly on Windows).

```
document-design-intelligence/            <- ZIP root IS this folder (matches `name:` in frontmatter)
  SKILL.md                                <- thin router, target <500 lines (04-packaging.md §2)
  VERSION                                  <- single line, e.g. "2.0.0" — CI-generated, never hand-edited (§4)
  LICENSE                                  <- our MIT license
  NOTICE.md                                <- attribution line, see below
  references/                              <- linked ONE level deep from SKILL.md only (04-packaging.md §2)
    resolution-flow.md
    print-production.md
    ats-rules.md
    brand-workflow.md
  scripts/
    resolve.py                             <- BM25 + FK resolution + brand two-pass merge (§1); stdout-only output
    validate_data.py                       <- build-time table integrity checks (§4); also run by merge_brand_kit.py
    render_pdf.py                          <- headless Chromium primary, WeasyPrint-if-available fallback (per T2 result, 05-SYNTHESIS.md)
    render_docx.py                         <- python-docx / python-pptx paths (per T1 result, 05-SYNTHESIS.md)
    build_brand_kit.py                     <- interview → data/brand/<slug>/ rows + standalone brand-kit.zip
    merge_brand_kit.py                     <- safe-extract an attached brand-kit.zip, re-zip whole skill (§2)
  data/
    base/         (11 CSVs, §1)
    brand/        (active.json + per-brand subfolders, §1 — empty/absent until first install)
```

### Manifests: claude.ai needs none of upstream's four

Confirmed in `04-packaging.md` §1.1 and §3: `skill.json`, `.claude-plugin/plugin.json`, and
`.claude-plugin/marketplace.json` are Claude-Code/marketplace concepts. claude.ai's Settings →
Skills → Add flow reads nothing but the ZIP's `SKILL.md` frontmatter. **For claude.ai, the only
manifest is `SKILL.md`'s own two required frontmatter keys — `name` and `description` — and we
maintain exactly one copy of each, full stop.** This directly avoids upstream's observed
four-copies-drift bug (`04-packaging.md` §1.1: skill.json/plugin.json/marketplace.json/SKILL.md
all describing the package differently, and — per `11-upstream-releases.md` §5 — silently going
stale relative to each other for over a month once their own sync automation broke).

`name`: lowercase/digits/hyphens only, ≤64 chars, no "claude"/"anthropic" (`04-packaging.md`
§1.2). Suggest `document-design-intelligence` or the shorter `designing-documents` (gerund form
per Anthropic's naming convention, `04-packaging.md` §1.2) — a naming choice, not load-bearing.
**Do not use a colon-namespaced name** (`ckm:something`) — this was an open question in
`04-packaging.md` §5 and is now resolved: upstream shipped that exact convention and had to
revert it (`11-upstream-releases.md` §2, PR #383, "replace colon with hyphen in skill names").

**If a Claude Code marketplace listing is ever added (secondary, per the task)**: it lives
*outside* the zipped skill folder, at the repo root (`.claude-plugin/plugin.json` +
`.claude-plugin/marketplace.json`, pointing at `./document-design-intelligence` as the skill
path — mirroring `04-packaging.md` §1.1's structure). Its `name`/`description` fields should be
**generated from `SKILL.md`'s frontmatter by the same release script that stamps `VERSION`**
(§4), never hand-maintained in parallel — that is the specific discipline upstream lacked. Do
not build this until there is an actual reason to list on that surface; it adds no value to the
claude.ai-only distribution path this project is scoped to.

### Attribution (`NOTICE.md`)

```
This project's routing/validation architecture (BM25 retrieval, closed-form
rerank, foreign-key resolution chain, deterministic anti-slop validators) was
independently studied from UI/UX Pro Max (https://github.com/nextlevelbuilder/ui-ux-pro-max-skill),
MIT License, Copyright (c) 2024 Next Level Builder. No upstream source code,
CSV rows, or text content is reproduced in this project; all data tables and
prose were authored independently for the document domain. See LICENSE for
this project's own MIT terms.
```

---

## 4. Release pipeline

Design goal, stated against `11-upstream-releases.md` §5's specific failure: upstream's version
sync depended on a *second*, separately-triggered workflow (`bump-versions.yml`) opening a PR
that a human had to notice and merge — and after one successful run, nobody did, for a month,
across five releases and a mechanism overhaul. **Ours must have no second step and no PR to
forget.** The tag push *is* the release; the same job that validates the data also stamps the
version and produces the artifact, in one run, with nothing left for a human to remember.

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*.*.*"

permissions:
  contents: write

jobs:
  build-and-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      # Build-time validators from 09-library-schema.md §4 (1-4): validate-keys,
      # validate-checks-implemented, validate-severity-map, validate-artifact-class.
      # Hard fail here means no tag ever produces a broken artifact.
      - name: Validate library data
        run: python document-design-intelligence/scripts/validate_data.py document-design-intelligence/data/base

      # Version is derived from the tag, never hand-typed, never a separate PR.
      - name: Stamp version
        id: version
        run: |
          VERSION="${GITHUB_REF_NAME#v}"
          echo "version=$VERSION" >> "$GITHUB_OUTPUT"
          echo "$VERSION" > document-design-intelligence/VERSION
          sed -i "1i<!-- version: ${VERSION} (generated at build — do not edit) -->" \
            document-design-intelligence/SKILL.md

      # SKILL.md frontmatter itself is untouched: it stays exactly the two required
      # keys (name, description) per 04-packaging.md's spec constraints. The version
      # comment is a human-visible marker one line above the frontmatter, not inside it.

      - name: Build ZIP with correct root
        run: |
          cd "$(dirname document-design-intelligence)"
          zip -r "document-design-intelligence-v${{ steps.version.outputs.version }}.zip" \
            document-design-intelligence \
            -x "*.pyc" -x "__pycache__/*"
        working-directory: .

      - name: Publish release
        uses: softprops/action-gh-release@v2
        with:
          files: document-design-intelligence-v${{ steps.version.outputs.version }}.zip
          generate_release_notes: true
```

Notes on this design:

- **`validate_data.py` runs before the zip step and the job fails closed** — a tag that fails
  data validation never produces a Release asset at all. This is the single biggest structural
  difference from upstream's pipeline (`11-upstream-releases.md` §5: their `bump-versions.yml`
  ran *after* a release already existed and could be — and was — silently ignored).
  `validate_data.py` should exit non-zero on any of: a slug collision, a foreign key that
  doesn't resolve, a `fail`-severity reasoning row with no reachable hard constraint, or an
  `Artifact Class` row referencing an incoherent page format/structure pairing
  (`09-library-schema.md` §4, items 1–4).
- **`sed -i "1i..."` runs in the same job, same step sequence, no PR, no second workflow.**
  There is nothing to forget because there is nothing asynchronous.
- **The zip step excludes `__pycache__`** (a small hygiene item; upstream's own repo shows no
  equivalent — worth doing since we're building this from scratch).
- **`generate_release_notes: true`** uses GitHub's own auto-generated notes (commit list since
  last tag) rather than semantic-release's conventional-commit parsing, which upstream's own
  data shows produces empty-looking release bodies for a large fraction of releases
  (`11-upstream-releases.md` §2 — v2.9.0 through v2.14.2 all had empty bodies). A plain commit
  list is less polished but never silently empty.
- **No `bump-versions.yml` equivalent exists, on purpose** — there is nothing left to bump. The
  only version-bearing files are `VERSION` and the one-line SKILL.md comment, both written in
  this same job, both derived from `GITHUB_REF_NAME`, never from a hand-maintained field.

---

## 5. README — "How do I install this?" (for a non-technical claude.ai user)

```markdown
## Install

**You'll need**: a Claude Pro, Max, Team, or Enterprise plan, with Code Execution
turned on. (Free plans and Code Execution being off will make this skill unable
to run its scripts — Anthropic's help center article "Create and edit files with
Claude" explains where to turn it on if you're not sure.)

1. **Download** the latest `document-design-intelligence-vX.Y.Z.zip` from this
   project's [Releases page](../../releases) — click the `.zip` file under the
   newest release, no need to unzip it yourself.
2. In claude.ai, go to **Settings → Customize → Skills → Add**, and choose the
   file you just downloaded. That's it — the skill is installed and Claude will
   use it automatically whenever you ask for a document, deck, CV, brochure, or
   report.

## Give it your brand (optional, one-time)

Start a new chat with the skill on and tell Claude about your brand — your
colors, fonts, and voice, or just attach your existing brand guidelines. Ask it
to set your brand up by name. It will hand you back **two files**:

- `my-brand-kit.zip` — small, just your brand's own data. **Save this somewhere
  you'll find it again** — you'll reuse it every time this skill gets updated.
- an updated skill `.zip` — upload this one in Settings → Skills, replacing the
  base-only version from step 2 above. From now on, every document it makes
  will default to your brand.

## Updating to a new version

Every update replaces the whole skill, which means your brand isn't carried
over automatically — here's how to bring it back in two extra minutes:

1. Download the new `.zip` from Releases and upload it in Settings → Skills,
   same as a first install. (Your brand is temporarily gone at this point —
   that's expected, keep going.)
2. Start a new chat with the skill on, **attach the `my-brand-kit.zip` you
   saved earlier**, and ask Claude to install your brand from it.
3. It will hand you back one merged `.zip`. Upload *that* in Settings → Skills,
   replacing what you uploaded in step 1. Your brand and the new version are
   now both in place, together.

## License

This project is MIT licensed (see `LICENSE`). Its retrieval/validation
architecture was independently studied from UI/UX Pro Max (MIT, © 2024 Next
Level Builder) — see `NOTICE.md` for the full attribution. No code, data rows,
or text from that project are reused here.
```

---

## What I could not verify, and the test that settles each

1. **Whether files a bundled script writes mid-session persist into a fresh chat with the same
   skill.** Assumed NO (by analogy to `05-SYNTHESIS.md` T3). Test: §2's step-by-step, run in
   two separate chats, check whether `data/brand/<slug>/` survives.
2. **Whether a chat-attached file is visible to a bundled script in the skill's own working
   directory, or requires searching a separate uploads path.** Assumed visible via a simple
   `ls`/`find` from the script, not confirmed. Test: attach a file, ask the skill to locate it.
3. **Whether claude.ai's Skill ZIP upload enforces a file-count or total-size ceiling.** Not
   documented anywhere found. Test: upload a full-size ZIP built at the schema's §6 row
   estimates and see if it's accepted.
4. **Whether `description` is capped at 200 or 1,024 characters in the actual upload UI**
   (already flagged in `04-packaging.md` §5, restated here because it constrains how much of
   this skill's activation triggers — CV, brochure, report, deck, "looks like AI slop" — can fit
   in one field). Test: upload with a ~600-character description and see what happens.
5. **Whether re-running `validate_data.py` inside `merge_brand_kit.py` (step 5 of §2) actually
   catches a brand kit built against an older base schema** — this is a real design intent, not
   yet a tested one, since it depends on the merge script and the validator both existing first.
   Settled by writing both and testing with a deliberately stale brand kit once the schema's
   authoring phase (`09-library-schema.md` §6) produces a real base to test against.
