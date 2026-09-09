# Licence Hygiene Audit — upstream fonts and our NOTICE

Audited against `C:\Users\ysuliman\Documents\Ai plugin\upstream-latest\`, git commit
`4aad0584d92131626b16d4ff4d77f0455385013c`, 2026-09-06T20:29:23+09:00 (confirmed via
`git log -1` in that checkout — this is the same commit identified as current `main` HEAD
in `research/11-upstream-releases.md` §1). Cited by commit, not by the version number in
`skill.json`/`plugin.json`, because `research/11-upstream-releases.md` §5 established that
field has been wrong for over a month.

## 1. Full licence inventory

Found by `find`/`grep`, not assumed. **Correction to the task framing before the results**:
report 02's "LICENSE.txt plus ~40 OFL font files" undersold what's actually there — the
LICENSE.txt is not itself an OFL text, and there are three genuinely separate licence
regimes stacked in this one sub-tree, not one:

| # | File(s) | Licence | Covers |
|---|---|---|---|
| 1 | `LICENSE` (repo root) | MIT, © 2024 Next Level Builder | The `ui-ux-pro-max` skill and its own data/scripts — what reports 04/09/11 already study. |
| 2 | `.claude/skills/ui-styling/LICENSE.txt` (+ byte-identical copy at `cli/assets/skills/ui-styling/LICENSE.txt`) | **Apache License 2.0** — not OFL, and not MIT | The `ui-styling` skill's own code/prose (SKILL.md, canvas-design-system.md, scripts). This is a *different* skill bundled in the *same repo* under a *different licence* than the repo's own root MIT licence — confirms report 02's suspicion that this is vendored-in content from elsewhere (the `ckm:` namespace prefix on this and its sibling skills, per `04-packaging.md` §1.1, is the other tell). No NOTICE file exists anywhere in the repo, so Apache clause 4(d)'s NOTICE-propagation requirement is moot — there is nothing to propagate. |
| 3 | 27 per-family `<Family>-OFL.txt` files under `.claude/skills/ui-styling/canvas-fonts/` | SIL Open Font License 1.1, one distinct copyright holder per family (Google Fonts project authors, IBM Corp., individual type designers — full list below) | 52 of the 54 bundled `.ttf` binaries in that same directory. **Gap found**: `IBMPlexSerif-*.ttf` and `InstrumentSerif-*.ttf` (5 files) have **no accompanying OFL.txt at all** — an upstream compliance gap, not ours, but worth naming: presence of a `.ttf` in that directory does not imply its licence text is actually there; each family had to be checked individually (`comm` against the two file-stem lists, not a glob match). |

**Is anything in our `skill/` folder construable as derived from any of these three?**
Checked file by file against our `data/` and `references/` — both currently near-empty
scaffolding (`data/base/` and `data/brand/` hold only `.gitkeep`/`README.md`;
`references/` holds only `activation.md`, which I wrote and contains zero upstream text,
only path citations). Also checked `scripts/lib/fonts.py` (added by another teammate
since my last pass) directly: it is a generic sfnt-binary parser — reads OS/2.fsType and a
GSUB `tnum` tag from *whatever font path is passed to it* — and neither hardcodes nor
bundles any of upstream's 54 specific font files or their 27 OFL texts. **Confirmed: nothing.**
`grep -il` for every bundled font-family name (WorkSans, Lora, JetBrains, IBM Plex,
Instrument, Bricolage, Tektur, Outfit, Silkscreen, Geist, Crimson) across our own
`scripts/`, `data/`, and `references/` returned zero matches.

## 2. The OFL fonts — do we ship any, and what would OFL require if we did?

**Not currently.** Nothing in `skill/` bundles a font binary, and neither `scripts/lib/fonts.py`
nor the merge/release scripts reference a specific font family by name — `fonts.py` is
introspection tooling, not a font bundle. Report 03/09's T5 typeface table (not yet
authored — `research/19` does not exist as a file yet at time of this audit) is expected to
follow upstream's own `google-fonts.csv` pattern (font family names + Google Fonts CSS
import URLs, per `research/11-upstream-releases.md` §2's v2.15.0 changelog: "1,934 approved
Google Fonts") rather than bundling binaries — that pattern ships zero licensing obligation
because nothing is redistributed, only referenced by name and fetched from Google's own CDN
at render time.

**If we ever do bundle a font file** (e.g. for the ENS example, or for a render path that
needs a local file rather than a CDN import), the correct handling — independent of
whatever copy upstream has, fetched fresh from the font's own canonical source
(fonts.google.com or the font project's own GitHub repo) — is:

1. **Include the font's own OFL license text verbatim, unmodified**, alongside the font
   file(s) it covers, in the same directory (this is what OFL 1.1 §Redistribution term
   actually requires — the licence text travels with the binary, not just with the repo as
   a whole).
2. **Check for a Reserved Font Name (RFN) clause** — of the 27 families surveyed here, at
   least four declare one: `Lora` ("Lora"), `IBM Plex` ("Plex"), `Italiana` ("Italiana"),
   `Libre Baskerville` ("Libre Baskerville"). An RFN only restricts what a *modified*
   version may be named (OFL §1) — verbatim, unmodified redistribution under the original
   name is unaffected. This only becomes load-bearing if we ever subset, hint, or otherwise
   modify a font file before shipping it; plain passthrough bundling is unaffected.
3. **Do not reuse upstream's copy of a font file or its OFL.txt** even though it would be
   legally fine (OFL permits redistribution) — fetch independently from the canonical
   source, consistent with the project's stated preference for independent derivation over
   convenience-copying (`00-BRIEF.md`), and sidesteps inheriting the gap found in item 1
   (upstream itself is missing two families' licence texts — copying from them would silently
   propagate that gap).

**Exact NOTICE text to add if a font is ever bundled** (per-font, appended to our own
`NOTICE.md`, one block per bundled family):

```
This package bundles the "<Family Name>" font, licensed under the SIL Open
Font License, Version 1.1. Copyright <year> <copyright holder>. The full
licence text is included at <path/to/Family-OFL.txt>. This project does not
modify the font; no Reserved Font Name restriction is implicated.
```

(Drop the last sentence, or state the RFN explicitly, if the bundled font's own OFL.txt
declares one and any modification is ever made.)

## 3. NOTICE.md / LICENSE — attribution accuracy fix

**Before**: `document-design-intelligence/NOTICE.md` and `LICENSE` cited upstream generically
("UI/UX Pro Max ... MIT License, Copyright (c) 2024 Next Level Builder") with no version or
commit anchor at all — not wrong, but not falsifiable either, and silent on which exact
snapshot of a fast-moving, 6-day-cadence project (`research/11-upstream-releases.md` §4) the
architecture study actually covered.

**Problem with citing by version number instead**: `research/11-upstream-releases.md` §5
established that `skill.json`/`plugin.json`/`marketplace.json`'s version field has read
`"2.13.0"` since 2026-08-06 regardless of what code is actually present — five releases and
one mechanism overhaul out of date as of the report. A version-number citation would inherit
that lie. **Fixed**: both files now cite the exact commit SHA and date of the checkout this
project's architecture study was actually performed against, which cannot go stale the way a
maintainer-controlled version string can.

Both files have been edited in place (see `skill/document-design-intelligence/NOTICE.md` and
`LICENSE`); the new attribution line in both now reads:

```
UI/UX Pro Max (https://github.com/nextlevelbuilder/ui-ux-pro-max-skill),
MIT License, Copyright (c) 2024 Next Level Builder — architecture studied
against commit 4aad0584d92131626b16d4ff4d77f0455385013c (2026-09-06).
```

`[PROJECT OWNER]` in `LICENSE`'s own copyright line is left as a placeholder, per the task —
that is the user's to fill in, not mine to guess.

## 4. README paragraph — what this project takes and doesn't

Added to `skill/README.md`. Plain language, one paragraph, as requested:

> This project studied how UI/UX Pro Max is built — not what it says. What we took is the
> *architecture*: matching a request against a small, curated table with keyword search
> (BM25), picking the best match with a deterministic tie-break instead of leaving it to
> free-form judgment, resolving the rest of the decision through foreign keys instead of a
> second fuzzy search, and checking the result against hard-coded rules (validators) instead
> of trusting the model's taste. None of that is UI/UX Pro Max's *content* — we wrote our own
> tables, our own rules, and our own thresholds for documents from scratch, sourced from our
> own research into CVs, print production, and ATS behavior. Zero lines of their code and
> zero rows of their data are in this project. Where the two disagree on how something should
> work, ours is the one built for paginated documents, not for a single web screen.

## What I could not fully verify

- **Whether the 4 named Reserved Font Names (Lora, Plex, Italiana, Libre Baskerville) are
  the complete list among the 27** — I checked each file's first line only (the standard
  location for the RFN clause per the OFL template), which is where all four found instances
  appeared, but did not read all 27 files in full for a second, later RFN declaration
  elsewhere in the document body. Low risk (RFN is conventionally stated once, in the
  opening copyright line) but not exhaustively confirmed.
- **Why upstream is missing OFL.txt for exactly IBMPlexSerif and InstrumentSerif** — not
  investigated further (would require upstream's own commit history for that directory);
  irrelevant to us either way since we don't redistribute their copies.
