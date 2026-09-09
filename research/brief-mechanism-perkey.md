# BRIEF — Mechanism Analyst: per-key degradation (one deliverable, ~10 min)

Context reset by policy; nothing lost. Your step 4a report (research/35-resolve-live.md) is
what produced this ruling. Act from THIS FILE and from disk, not from chat.

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Skill dir: skill\document-design-intelligence
Python:    C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## The ruling (approved by the lead — implement, do not relitigate)
`resolve.py` currently calls `validate_data.validate()` over the WHOLE dataset before
stage 1, so any single unauthored table makes every query refuse. Replace that with
**per-key degradation, two tiers**:

- **Tier 1 — still a hard refusal, whole dataset.** Structural problems: a declared file
  missing, manifest/header mismatch, malformed CSV, duplicate keys. These mean the dataset
  cannot be trusted at all.
- **Tier 2 — refuse only the resolution paths that touch the broken key.** Row-level
  problems: dangling FK, bad enum value, bad threshold reference, blank non-nullable cell.
  Everything not touching that key answers normally.
- The whole-dataset gate summary prints as a **warning header**, not a refusal.
- **Every refused path is named in the output**, with the key and the reason, so the user
  can see what was skipped and why rather than getting a silent partial answer.
- The same rule applies to `preflight.py` and to `ddi.py check`.

## ONE deliverable: the three scripts implement the two tiers, with tests.
Tests must cover, at minimum: a tier-1 problem still refuses everything; a tier-2 problem
refuses only the touching path; an untouched path answers with the warning header present;
the refused-path message names the key. Keep the existing suite green — it is
**109 passed + 8 subtests** from the skill dir. Stdlib only, same guard as the rest.

## Do not
Touch `data/`, `research/load-base.py`, the manifest, or any `research/*.csv` draft.

## VERIFY
`pytest -q` from the skill dir. Then run the 12-query list in `research/26-notes.md`
(~line 200) against live `data/base` and report how many now resolve. `structures` is still
unauthored, so any path through `Structure Key` should be a NAMED tier-2 refusal — that is
the headline case this ruling exists for.

## REPORT
Max 8 lines to the Workflow Orchestrator, slot 01a080c5-2001-78b3-bbbe-afaae15edafa:
test count, how many of the 12 queries resolve now, what a tier-2 refusal looks like
verbatim (one example), and anything the ruling did not anticipate.
If you approach ~10 minutes, checkpoint to research/handover-mechanism.md and stop.

## ADDED BY RULING (do this in the same pass if you have not finished; otherwise it is your next task)
`structures.Section Order` will ship EMPTY on most rows — `headings.csv` only has CV
sections, so most document classes have no honest section order yet, and authoring the rest
is deferred to after v0.1.0. Therefore: when `Section Order` is empty, resolve.py must say
**"no section-order guidance for <doctype>"**. It must NEVER present an empty list as if it
were an answer. This is the same principle as the named tier-2 refusal: a visible gap, not a
silent one.
