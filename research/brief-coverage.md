# BRIEF — Coverage — apply "lettre", and pin the mirror with a test

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git.

## What was decided
Your refutation was accepted. The lead's ruling (d) was wrong on the mechanism and you were
right to say so. THE PHRASE BLOCK IS NOT BEING APPLIED. Only the one-word addition you
recommended is, plus the test you identified as missing.

## Deliverable (ONE — two parts, one coherent change)

### Part 1: add the bare noun "lettre"
In skill/document-design-intelligence/SKILL.md's frontmatter description, add "lettre" to the
non-English noun list. It currently reads:
  ... also note interne, fiche, courrier, affiche, dépliant, présentation, formulaire,
  Lebenslauf, Angebot, Bericht, invoice, memo, proposal, one-pager, facture, devis, rapport,
  Rechnung, Formular, Broschüre.
Result MUST measure exactly **972** characters. If you get anything else, STOP and report. Do
not adjust other wording to reach the number.

THE COUPLED EDITS, which have now bitten twice:
- references/activation.md line 23, the fenced "as shipped" block: must be updated to match,
  BYTE for byte, on one line.
- references/activation.md lines 15, 26 and 28: "964" becomes 972 in all three. Leave the
  historical 667 alone.

### Part 2: the test that would have caught this
Add a test asserting the fenced block equals SKILL.md's description BY BYTES. Requirements:
- Read BOTH files at runtime. Do not embed either string in the test.
- Compare bytes. NOT `" ".join(x.split())` — that is the whitespace-folded comparison I used in
  my own verification and reported as "byte-identical", which is how this drifted unnoticed.
- Locate the block by a marker, and raise a clear AssertionError if the marker is missing —
  same guard you added to the coverage test after candidate H deleted its marker. A test that
  silently finds nothing is worse than no test.
- The failure message must say which file to edit and that the two must move together.
Put it wherever it best belongs — beside the description coverage test is the obvious home.

## Verify — paste actual output
1. Description measures exactly 972 and contains "lettre".
2. Your new test passes.
3. NEGATIVE CONTROL, and I will repeat it myself: break the mirror by changing one character in
   activation.md's fenced block, confirm the new test FAILS and names the problem, then restore.
   Paste both results. A test not seen failing is not known to work.
4. No "964" survives in activation.md.
5. `python3 -m pytest scripts/tests/test_description_coverage.py -q` green on its own.
6. Full suite: baseline was 146 passed plus 8 subtests; expect 147 with your new test.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the measured
length, checks 3 and 4 verbatim, and the test tally.
