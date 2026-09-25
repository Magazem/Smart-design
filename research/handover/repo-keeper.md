# Handover — Repo Keeper (2026-09-25)

## Procedure that works (not written down elsewhere)
- Use `python3` (WindowsApps). Plain `python` is broken.
- Docs-only commit: stage exactly the named files, append one line to research/ORCHESTRATOR-STATE.md,
  commit, push, then `git fetch` + `git log -1 origin/main` to confirm. No tests are needed.
- Code/data commit: first check `git status` for OTHER workers' in-progress research sources, then
  `load-base.py` -> `build-portable.py`. Commit locally. Verify in a clean worktree:
  `git worktree add -q ../sd-verify HEAD`, then `ddi.py check`, skill `pytest -q` and
  `pytest -q research/p65`, plus `research/designs-evidence/test_fill_family.py` since 74d9f2f.
  Finish with `git worktree remove --force ../sd-verify`. Push only if green.
- If a requested split leaves an intermediate commit red, squash it (unpushed only, `git reset --soft`)
  and check that the tree hash equals the verified one. Precedent: 0856059, approved by the Orchestrator.
- `ORCHESTRATOR-STATE.md` often carries the Orchestrator's own pending lines. Committing them is expected.
- CRLF->LF warnings are harmless; git normalises the files.
- A push once reported "cannot lock ref" but had actually landed. Always confirm with fetch.

## Tool quirks
- The user REJECTED foreground waits (PowerShell `Start-Sleep 60`). For "stable over N s" checks, use
  mtime age (`stat -c %Y`), or a `run_in_background` bash loop that exits when the files are idle for more
  than N s. That notifies on completion, which works well.
- Race hazard: regenerating while another worker edits research/*.csv pulls their half-done data
  into data/base and portable/. It happened once (b582bad swept in I7 outputs without their sources;
  fixed by fc99531). So check status before regenerating.

## Scripts I own
- research/designs-evidence/make_items_csv.py (C11 items csv: cv, deck, invoice). It recognises tables
  by header only; `CATALOGUE_URL` supplies the url for items without a page of their own (invoice MS).
  make_items_csv_82ag.py is a separate recoder script; it isn't mine.

## Exposure / independence (per family)
- While checking my own parsing I saw first-coder feature codes for a few rows:
  cv (GH:001, NPM:001 row), deck (NPM:002, LO:001, MS:001 rows) and invoice (MS:002 row).
  Treat me as EXPOSED for cv, deck and invoice: do not use me as a second coder for them.
  I saw no codes for any other family.

## Left half-done / open at handover
- Uncommitted, still being written by the bg agreement agent: deck-agreement-r2.md, poster-agreement.md,
  and invoice-r2 agreement (not yet on disk). Commit them once idle for more than 2 min.
- Untracked scratch dirs tmp-rprc/ and tmp-sc7/: never commit them. Delete only when their owners are done.
- 48abd33 was pushed with ONE test excluded:
  test_fill_family.py::TestDryRun::test_family_without_a_parsable_table_is_reported_not_crashed
  (the Implementer is fixing it). Re-include it in the next verification.
