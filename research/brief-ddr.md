# BRIEF — DDR — Apply Candidate F to the description (USER APPROVED)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not rebuild the ZIP.

## Why
The user approved candidate F. This is the ONLY approved description change; candidate B in the
same file stays unapplied. The current trigger promises "quality fixes", which reads as a
promise about prose. Nothing in data/base covers prose quality. F narrows it to appearance.

## The edit — 8 characters, exact
In skill/document-design-intelligence/SKILL.md, the frontmatter `description:` line.
REPLACE this substring (it occurs exactly once):
  quality fixes: looks like AI, looks generic, make it professional, fix the layout
WITH:
  appearance fixes: looks like AI, looks generic, make it look professional, fix the layout

Change nothing else in the description. Do not reflow the line — it is one long line.
The full drafted result is in research/38-description-candidate.md under "Candidate F".

## Deliverable (ONE)
The edit, plus the three things that MUST move with it or the build breaks:
1. SKILL.md description — after the edit it must measure exactly 831 characters.
2. references/activation.md, the fenced block under "## The description as shipped" — it is
   byte-identical to the description and a check depends on that. Update it to match.
   Do NOT touch "Alternate A" or "Alternate B" below it; those are retained history.
3. references/activation.md prose — "**Length: 823 characters**" becomes 831, and the
   "The 823-character primary description" line near the top becomes 831. Leave the
   "Grew from 667 to ..." historical sentence's 667 alone but update its second number.

Do not touch the version stamp line in SKILL.md. Do not touch any prompt.

## Verify before you report
1. python3 -c "import io,re;s=io.open('skill/document-design-intelligence/SKILL.md',encoding='utf-8').read();print(len(re.search(r'^description:\s*\"(.*)\"\s*$',s,re.M).group(1)))"
   must print 831.
2. The fenced block equals the description. Same check you ran on the last task; it must
   print True.
3. `grep -n "823" skill/document-design-intelligence/references/activation.md` returns nothing.
4. SKILL.md still starts with `---` and the description line is still a single line.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 6 lines: the measured
length, the True/False from check 2, and the output of check 3.
