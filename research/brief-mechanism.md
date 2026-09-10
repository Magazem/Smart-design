# BRIEF — Mechanism — Candidate J: the lead sentence reads as "files"

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DRAFT ONLY. DO NOT edit SKILL.md. DO NOT touch git. You append one section to
research/38-description-candidate.md.

## The data, which is now good enough to reason from
Same archive, same prompts, run twice:
  DE invoice  2/2 FIRE      DE form     1/1 FIRE
  EN proposal 1/2           EN memo     0/2
  FR letter   0/2           FR report   0/2
The three that failed were re-run and failed AGAIN. These are deterministic non-fires, not
routing noise.

## The hypothesis you are testing — the lead's, and it fits every point
An invoice and a form are ARTEFACTS. Claude cannot produce them as prose, so it reaches for a
document tool and finds us. A letter, a memo, a report and a proposal are GENRES CLAUDE WRITES
NATIVELY IN CHAT. It writes them and never considers a skill at all.

If that is right, nouns were never the issue — which explains the thing that broke the previous
theory, that "memo" and "rapport" are both present in the description and both families failed
anyway.

The suspect is the LEAD SENTENCE: "Creates and fixes print/office documents". That reads as
FILES. Candidate H helped the case where a format is involved — "even as Word or PowerPoint" —
but says nothing to the case where Claude intends an ordinary chat reply.

## Deliverable (ONE) — research/38-description-candidate.md, appended as "Candidate J"
Do NOT overwrite B, F, G, H or I. F, G and H are APPLIED and live at 964.

1. Rewrite the LEAD so it is format-agnostic and USE-WHEN framed. The lead's sketch, which you
   may improve but not weaken: "Use whenever the user asks for any of these documents to be
   written, drafted, made, structured or fixed, whether the answer is a chat reply or a file:"
   followed by the existing noun list.
2. KEEP candidate H's deferral sentence intact. It is doing real work and prompt 13 depends on
   it.
3. INCLUDE the bare noun "lettre". It is genuinely missing.
4. FUND IT by trimming the TRIGGER-EXAMPLE list. The data says those examples are not the
   discriminator — invoice and form have no trigger phrase and both fire. Do NOT pay for it out
   of "sourced" or the UI/UX boundary sentence; both were fought for and both are load-bearing.
5. Measure. Under 1023. Give the exact substrings, the full result on one line, the measured
   length and the headroom.

## The risk section is the important part of this brief
A use-when lead WIDENS scope, where every recent change narrowed it. Say explicitly what it does
to the should-not-fire prompts:
- 8, the Python refactor
- 9, the marketing strategy question
- 10, "summarize this PDF research paper" — the sharpest one, because a use-when lead plus a
  noun list is close to "any mention of a document type"
Say how a reader would TELL if you broke them, and say plainly if you think the risk is not
worth taking.

## And the judgement I want
If, having read the shipped description, you think the lead sentence is NOT the cause, say so
and say what is. You refuted a brief premise correctly on candidate H and Coverage did the same
on I. A well-argued "this hypothesis is wrong" remains a valid deliverable here.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the new lead
verbatim, what you trimmed, the measured length and headroom, your risk verdict on 8, 9 and 10,
and whether you back the hypothesis.
