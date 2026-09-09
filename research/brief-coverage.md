# BRIEF — Coverage — Draft ONE description sentence (draft only, do not apply)

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. DO NOT edit SKILL.md. The user personally vetoes description changes;
this is a proposal that goes in front of the lead, nothing more.

## Why
Activation prompts 3, 4 and 5 failed because Claude asked for the missing file/text before
invoking anything. In prompt 3 it then said it would "likely use document-design-intelligence"
once given the details — so the description matched, it just clarified first. We are fixing the
test (another worker, in parallel). This brief prepares a fallback in case the revised prompts
still fail: a sentence that tells Claude to invoke the skill BEFORE asking for missing content.

## Read first
- skill/document-design-intelligence/SKILL.md — the frontmatter `description:` field, one long
  line. MEASURE its current length yourself from SKILL.md -- the repo quotes 667, 823 and 825
  in three different places and at most one is current. The hard cap is 1023 (tested against the claude.ai
  upload UI; see references/activation.md lines 10-25).
- skill/document-design-intelligence/references/activation.md, "## The description as shipped".

## Deliverable (ONE)
Write research/38-description-candidate.md containing:
1. ONE candidate sentence, verbatim and quoted, to be inserted into the description. The
   lead's example of the intent: "Use this skill first even when the content or file is not
   yet provided; it decides what to ask for." Improve on it if you can; keep it one sentence.
2. Exactly where in the current description it would go, and why there.
3. The full resulting description as a single line, with its exact character count, proving
   it stays under 1023.
4. Rationale: why this addresses the observed failure, in 3-4 lines.
5. Risk: what this sentence could over-trigger. Prompts 6-13 are the "should not fire" and
   handoff cases in activation.md — name which of them this sentence puts at risk and why.
   Be blunt. If you think the sentence is a bad idea, say so and say what you would do instead.

## Constraints
- ASCII-only in your prose. The description itself may keep its existing accented words.
- Count characters with Python, not by eye:
  `python3 -c "print(len(open('f','r',encoding='utf-8').read().strip()))"`.
- Do not modify SKILL.md, the ZIP, or the test docs.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: the sentence,
the new character count, and your risk verdict.
