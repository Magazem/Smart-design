# BRIEF — Packaging Analyst: RELEASE BLOCKER, the ZIP is rejected by claude.ai (~10 min)

Context reset by policy; nothing lost. Step 8 is committed (c26af9f). Act from THIS FILE.

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Skill dir: skill\document-design-intelligence
Python:    C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## The blocker, confirmed in the archive bytes
The user uploaded the ZIP. claude.ai rejected it: "SKILL.md must start with YAML frontmatter
(---)". I read the bytes out of the built archive myself:

    first 80 bytes: b'<!-- version: 0.0.1-dev (generated at build - do not edit) -->\r\n---\r\nname: docum'
    SKILL.md CRLF count: 53
    members containing a CR byte: 9

Two defects in `scripts/build_zip.py`, and the second is wider than SKILL.md:
1. `stamp_version()` PREPENDS the version comment, so the file no longer starts with `---`.
   The stamp must go AFTER the closing `---` of the frontmatter — first line of the body.
2. `stamp_version()` writes with `write_text` and no `newline="\n"`, so Python's Windows
   translation turns every LF into CRLF, and the CRLF file is what gets zipped. NINE members
   carry CR bytes, not just SKILL.md — the working copy is CRLF too
   (`git ls-files --eol` shows w/crlf, i/lf).

## ONE deliverable: a ZIP that claude.ai accepts, and a test that keeps it that way.
1. Move the version stamp to AFTER the frontmatter's closing `---`.
2. Write SKILL.md with `newline="\n"` explicitly.
3. `build()` must add text members as **LF bytes regardless of the working copy's line
   endings** — normalise on the way into the archive, so a Windows checkout cannot produce a
   CRLF release. Apply it to every text member, not only SKILL.md; nine are affected.
4. **Test, opening the BUILT ZIP** (not the source tree): assert SKILL.md starts with
   `b"---\n"`, and that no text member contains a `b"\r"` byte. A test that only checks the
   working copy would have passed while this shipped.

## Do not
Touch `data/`, `research/load-base.py`, the manifest, or any `research/*.csv`.
Do not run ANY git command — the Orchestrator commits. Do not tag. Do not edit VERSION.

## VERIFY
Rebuild, then OPEN the archive and report: SKILL.md's first 40 bytes verbatim, the count of
members containing CR (must be 0), member count, byte size, and the manifest md5
(must stay 731d874ff6052d8c3809a3d44a9d4196). `pytest -q` — was 132 passed + 8 subtests.

## REPORT
Max 8 lines to the Workflow Orchestrator, slot 01a080c5-2001-78b3-bbbe-afaae15edafa:
the first-bytes check, the CR count, the other archive numbers, the test count, and the
paths you changed. If you approach ~10 minutes, checkpoint to
research/handover-packaging.md and stop.
