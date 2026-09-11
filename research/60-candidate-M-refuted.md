# CANDIDATE M IS REFUTED — and it was killed by its own pre-registered test

Run record: `research/56-candidate-M-trial.md`. Draft: `research/50-candidate-M-draft.md`.
Test artefact: `research/test-builds/document-design-intelligence-0.2.0-candidateM.zip`.

## THE RESULT
**DOCX-ONLY.** Identical to candidate L. Activation 11 did not fire under M.

Every control held, and each was verified read-only BEFORE the prompt was sent:
- **Build verified installed**, not assumed: the shown description contains
  `even for '.docx'/'.pptx' requests naming Word or PowerPoint`. This mattered — both
  descriptions open with identical words, so first-words matching would have proved nothing and
  the old build could have been tested under the new name.
- **Skill ENABLED**, confirmed hover-only. No toggle click, no "View" click.
- **Confound empty**, re-proven: the Instructions for Claude textbox carries no value attribute
  while Full name and Display name both carry `value="yazan"`.
- **One chat, one send, no reload or navigation from send through trial end.**

Evidence, scored on the primary signal:
- The only SKILL.md path in the trace is `/mnt/skills/public/docx/SKILL.md`. Ours appears
  nowhere.
- Follow-up corroborates: *"I used one skill: docx... I didn't need any of the other available
  skills (pptx, xlsx, pdf, etc.)"* — document-design-intelligence is never mentioned.

## WHY THIS IS A CLEAN REFUTATION AND NOT A DISAPPOINTMENT
M's falsification test was **written down before the run**, in `50-candidate-M-draft.md` §7:
re-run activation 11 VERBATIM; if it still routes to docx with Claude citing the competing
skill's own criteria, the token-parity mechanism is dead. That is exactly what happened, on
exactly that prompt, with no rewording.

Contrast the FIRST M draft, which was rejected partly because its test required a friendlier
prompt. Had that version shipped, this run would have been unscorable and we would have learned
nothing. **Pre-registering the falsifier is what made one browser run decisive.**

## WHAT IS NOW DEAD — refutation chain item 6
**6. TOKEN PARITY WITH THE COMPETING SKILL. Dead.** Putting the literal `'.docx'/'.pptx'` tokens
into our own deferral sentence, at the point the priority claim is made, does not win the
arbitration. Claude named that token as its deciding signal in P6; matching it changes nothing.

This is the first candidate built on a mechanism from Claude's own account rather than our
theorising, and it still failed. That is a stronger result than the previous five, not a weaker
one: the standing rule's bar was met and the lever still does not exist.

## THE CONCLUSION THIS SUPPORTS
Six description candidates — F, G, H, lettre, L, M — have now been applied or tested. **None has
moved routing for a prompt that names a format.** Claude's own account in P4 and P6 says routing
turns on the file and the named format, decided before our description is weighed. M tested the
one remaining reading of that account and it is refuted.

**The description lever should be treated as exhausted for the named-format case.** The standing
rule still stands and now binds harder: no further candidate without a NEW mechanism statement
from Claude. We do not have one. P6's statement has been spent.

This is why the 2026-09-11 user ruling is right: v0.3's headline is that the output is GOOD when
the skill runs. Auto-firing for EN/FR prose genres and named-format prompts stays deferred behind
the documented workaround — add "Use the document-design-intelligence skill." to the request.

## ACTION REQUIRED — THE ACCOUNT NO LONGER HOLDS THE PUBLISHED BUILD
The user's claude.ai account now has **candidate M installed, not v0.2.0.** M is refuted and is
not going to be applied to the repo, so the account is carrying a build that exists nowhere in
the release history.

Any future browser test reading "the installed description" will read M unless this is corrected.
**Either restore the published v0.2.0 asset to the account, or record prominently that the
account holds M.** The reference copy is at
`research/test-builds/_published-v0.2.0-reference.zip`, md5 `9e9f30fb08c663686bde842c41dd2c42`.
This is the user's account and only the user can change it. Raised, not acted on.
