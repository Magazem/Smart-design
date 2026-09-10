# BRIEF — Mechanism — Candidate H: is the deferral sentence over-reaching?

Repo root: C:\Users\ysuliman\Documents\Ai plugin
READ-ONLY TASK. Do not edit SKILL.md. Do not edit any script. Do not touch git.
The ONLY file you write is research/38-description-candidate.md, appending a section.

## Why — a hypothesis worth testing before the re-run, not after
The user ran the v0.2 acceptance prompts. The skill fired on NONE. Claude explained itself:

    "I was doing a clean Word file as per the request, no need for design skills."

NONE of those prompts names Word, .docx, PowerPoint or any file format. Read prompt 1 in
research/44-v02-acceptance.md and confirm that yourself before going further — if I am wrong
about that, say so and stop.

So where did "Word file" come from? The leading hypothesis: our own deferral sentence is being
read as "any office document belongs to the built-in docx/pptx skills". If that is what is
happening, then candidate G — which adds the missing nouns — is NECESSARY BUT NOT SUFFICIENT,
and it will be blamed unfairly when the re-run still fails.

## The sentence
In skill/document-design-intelligence/SKILL.md's frontmatter description:

    When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a plain
    conversion or edit with no design ask, use that format's own skill instead.

Its history is in references/activation.md and research/24-builtin-alignment.md item 1: it was
added to align with Anthropic's own docx and pptx skills, which each carry a clause deferring to
a dedicated document skill. It exists for a real reason. Activation prompts 11 and 13 test it,
and both PASS today. Do not propose throwing it away.

## Deliverable (ONE) — research/38-description-candidate.md, appended as "Candidate H"
Do NOT overwrite candidates B, F or G. F is applied and live. G is drafted and with the user now.

1. QUOTE the sentence exactly as it ships.
2. List EVERY phrase in it a model could read as "office documents are not this skill's job".
   Be specific about which words carry the over-reach — naming the four formats first, the bare
   "use that format's own skill instead", whatever you find. This analysis is the real value of
   the brief; the sentence is only worth replacing if you can say precisely what goes wrong.
3. Draft ONE replacement sentence that:
   - KEEPS the plain-conversion carve-out. "Convert this .docx to PDF, change nothing" must
     still defer. That is activation prompt 13 and it passes today.
   - States POSITIVELY that creating or designing any of the listed document types is THIS
     skill's job, even when the output happens to be Word or PowerPoint.
4. MEASURE it. G leaves 24 characters of headroom under the 1023 cap. If H does not fit
   alongside G, say exactly what in G you would trade for it and why that trade is right. Do
   not quietly assume G shrinks.
5. Say which of activation prompts 11, 12 and 13 your sentence puts at risk, and how a reader
   would tell if it broke them. 11 and 13 must still defer; 12 must still fire.

## The judgement I actually want
If, having read the sentence closely, you conclude it is NOT the cause and the "Word file"
explanation came from somewhere else, SAY SO and say what you think the real cause is. A
well-argued "this hypothesis is wrong" is a better outcome than a sentence nobody needed. Do
not manufacture a candidate to fill the brief.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: your verdict on
the hypothesis, the offending phrases, the replacement sentence, its measured length against
G's headroom, and the prompt-11/12/13 risk.
