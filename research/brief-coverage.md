# BRIEF — Coverage — apply candidates G and H (HOLD until the lead says "user approved")

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT START until the orchestrator tells you the user has approved. If you
are reading this without that go-ahead, stop and say so.

## What is being applied — one package, one commit
The user is deciding on ONE thing: G-minus-triggers plus H, a 964-character description.
- **G nouns**: the missing document nouns, from research/38-description-candidate.md's
  "Candidate G" section.
- **NOT G's trigger phrases.** Drop the 76-character trigger insertion ("draft an invoice",
  "write a memo", "rédige une facture", "erstelle eine Rechnung"). I verified this costs nothing:
  every noun those phrases carry — invoice, memo, facture, Rechnung, one-pager, devis, proposal,
  Angebot — still appears elsewhere in G. It is pure redundancy and it buys the room for H.
- **H**: replace the deferral sentence with the "Candidate H" wording. It keeps the
  plain-conversion carve-out word for word and closes the agentless hole by saying "the USER
  names it".
- **The letter-formal Keywords fix**, which costs zero description characters.

## Deliverable (ONE — four edits, one coherent change)

### 1. SKILL.md description
Apply G's nouns and H's replacement sentence. The result MUST measure exactly **964**
characters. Measure with Python len() on the quoted value. If you get anything else, STOP and
report — do not adjust wording to hit the number.

### 2. The coupled edits that must move with it
These are the same four that bit us when candidate F was applied. Miss one and the build breaks:
- references/activation.md, the fenced block under "## The description as shipped" — it must
  stay BYTE-IDENTICAL to the description. A test depends on it.
- references/activation.md prose: every "831" becomes 964. Leave the historical "grew from 667"
  first number alone.
- Do NOT touch "Alternate A" or "Alternate B" further down. They are retained history.

### 3. letter-formal Keywords
research/26-t1-doctypes-draft.csv line 12: the Keywords cell has "business letter", "formal
letter", "official letter" but no bare "letter" token, although the description carries
"letters". Add the bare token. Then RELOAD via research/load-base.py so it reaches data/base —
only that script may write there. The reload diff must be one row of one file.

### 4. REMOVE THE XFAIL — this is a binding condition, not a cleanup
In scripts/tests/test_description_coverage.py, EMPTY the PENDING_CANDIDATE_G list and remove
the xfail marker. In the SAME commit.
The reason, recorded in RESUME.md: an xfail test passes the suite while proving nothing. If G
lands and the marker stays, the project keeps a permanently silent test covering the exact
defect that blocked v0.2 acceptance — worse than having no test.

## Verify — paste actual output, and note what does NOT count
1. Description measures exactly 964 and contains "the user names it".
2. The fenced block in activation.md equals the description. Must print True.
3. No "831" survives in activation.md.
4. `python3 -m pytest scripts/tests/test_description_coverage.py -q` run WITHOUT the xfail
   marker, GREEN, with PENDING_CANDIDATE_G empty. **"The full suite passed" is NOT acceptable
   evidence** — an xfail test passes the suite while proving nothing. Run this file and show it.
5. Full suite: baseline 146 passed plus 8 subtests.
6. `python3 scripts/validate_data.py data/base` — `OK: validated 14 table(s), 414 row(s)`.
7. The reload diff touches only doctypes.csv, one row.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the measured
length, checks 2-4 verbatim, the reload diff stat, and confirmation the PENDING list is empty.
