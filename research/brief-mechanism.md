# BRIEF — Mechanism Analyst: the zero-score abstain (small, ~8 min)

Context reset by policy; nothing lost. Your abstain pass is verified and closed: 126 passed
+ 8 subtests, "make me a flyer" abstains and offers the two real flyer rows, thresholds
derived and written up in research/35-notes.md. Act from THIS FILE and from disk.

Repo root: C:\Users\ysuliman\Documents\Ai plugin
Skill dir: skill\document-design-intelligence
Python:    C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## The defect (I reproduced it myself)
On a query that matches NOTHING, the abstain path still prints the candidate block and
offers rows scoring 0.0. Running a nonsense query returned:

    [ABSTAIN] no confident match for "<query>"
      top candidates -- ask the user which one they meant:
        'cv-us' "Resume -- US"  score=0.0
        'cv-uk' "CV -- UK"  score=0.0

Asking a user to choose between two irrelevant candidates is worse than saying nothing: it
implies the resolver understood the request and narrowed it down, when in fact it has no
signal at all. Same principle as the named tier-2 refusal — an honest gap beats a
confident-looking answer.

## ONE deliverable: RULED — when top-1 scores 0, say "no match" and list NOTHING.
Distinguish the two cases in the output:
- **Ambiguous**: real competing candidates, margin below threshold -> current behaviour,
  list them and ask which was meant. This is working; do not change it.
- **No match**: top-1 is 0 (nothing matched at all) -> say so plainly and list no
  candidates. Wording is yours; make it obviously different from the ambiguous case, and
  make it useful — a user who typed something the library has no doctype for should be able
  to tell that from the message.
Apply it to both the text and the `--json` output, so a caller parsing JSON can tell the two
apart too.

## Do not
Touch `data/`, `research/load-base.py`, the manifest, or any `research/*.csv` draft — the
DDR is editing research/26 right now and the Coverage analyst reloads after it.

## VERIFY
Real command output pasted for: a no-match query, an ambiguous query (E3 "make me a flyer",
which must still list its two flyer candidates), and a clear-win query (E1 or D1, which must
still resolve). `pytest -q` from the skill dir: >= 126 passed + 8 subtests, plus a test for
the zero-score branch.

## REPORT
Max 8 lines to the Workflow Orchestrator, slot 01a080c5-2001-78b3-bbbe-afaae15edafa:
the three command outputs in brief, the test count, and the JSON shape difference between
"no match" and "ambiguous". If you approach ~10 minutes, checkpoint to
research/handover-mechanism.md and stop.
