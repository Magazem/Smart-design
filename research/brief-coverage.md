# BRIEF — Coverage — Ruling F item 3: draft an honest quality-fix trigger

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT edit SKILL.md. Draft only. The user vetoes description changes.

## Why
Activation prompt 4 failed because Claude looked in the skill for rules about fixing
AI-sounding WRITING and found none. It was right: data/base covers layout, typography, colour,
print and ATS, and nothing else. The description currently promises "quality fixes: looks like
AI, looks generic, make it professional, fix the layout", which reads as a promise about prose.
The trigger needs to be honest about being a promise on APPEARANCE.

## Read first
- skill/document-design-intelligence/SKILL.md, the frontmatter description. It measures 823
  characters; re-measure rather than trusting that.
- research/38-description-candidate.md — your own file from task B. APPEND to it, do not
  overwrite it. Candidate B must stay intact and clearly labelled as the still-unapplied
  fallback.

## Deliverable (ONE)
Append a section to research/38-description-candidate.md headed "Candidate F — honest
quality-fix trigger" containing:
1. The minimal rewording of the existing quality-fix clause. The lead's sketch:
   "quality fixes: layout looks like AI, looks generic, make it look professional, fix the
   layout". Minimal means change as few words as you can while removing the prose promise.
2. The exact substring you would replace and the exact substring you would replace it with, so
   the edit is unambiguous.
3. The full resulting description on one line, with its measured character count, and the
   headroom under the 1023 cap.
4. Whether Candidate B and Candidate F can both be applied, and the combined length if so.
5. Risk in 3-4 lines: does narrowing the trigger to "layout" lose real activations? Prompt 4 is
   being rewritten to describe appearance, so say whether the revised prompt 4 still fires under
   Candidate F. Say plainly if you think F is unnecessary.

## Constraints
- ASCII-only prose. Measure with Python len(), not by eye. If the python3 shim is broken, use
  the uv cpython interpreter as before.
- Do not edit SKILL.md, activation.md, the ZIP, or any test doc. Another worker is in
  activation.md right now — stay out of it.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: the replacement
substring, the new length and headroom, whether B and F compose, and your recommendation.
