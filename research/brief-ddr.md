# BRIEF — DDR — v0.2 phase C: the acceptance prompt set

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Write ONE file: research/44-v02-acceptance.md.
(43 is taken — research/43-resolve-live-v2.md is Mechanism's query re-run.)

## Why
v0.2 claims every document family now has section guidance. That claim is currently proved only
by our own gate. It needs the same treatment the 13-prompt activation list got: real prompts a
human runs against the uploaded skill, where a wrong answer is visible.

## Deliverable (ONE)
research/44-v02-acceptance.md: FIFTEEN prompts, one per newly covered family, for the user to
run after uploading the v0.2 ZIP.

The fifteen structure keys, bound from data/base/structures.csv:
invoice-standard, letter-standard, memo-standard, form-standard, proposal-standard,
report-short, report-long-toc, whitepaper-standard, one-pager-standard, brochure-3panel,
brochure-gatefold, flyer-single-sheet, poster-single-canvas, deck-standard,
cover-letter-standard

## Every prompt must
1. CARRY ITS CONTENT INLINE. This is the hardest-won lesson in the project: prompts referencing
   a file or text that is not attached measure attachment handling, not the skill. Four of the
   five original activation failures were this defect. Give each prompt enough real material to
   work with.
2. Name the EXPECTED SECTION ORDER in the pass criteria — read it from the section-order drafts
   (research/39, 40, 41) or from data/base/structures.csv. The reader must be able to tell
   whether the skill reasoned with the right sections without knowing the library.
3. Have explicit Pass and Fail lines. A clarifying question is a PASS only if it shows
   document-design framing: format, layout, page count, sections, branding, print. A generic
   "what would you like?" is a FAIL. Producing content with no structural reasoning is a FAIL.
4. Vary the language. The library carries English, French and German headings for every section,
   so some prompts must be in French and some in German. A section model that only works in
   English is a finding worth catching here.

## Two traps to handle explicitly
- brochure-3panel and brochure-gatefold have IDENTICAL section orders, ruled intentional: panel
  count is not content, and what separates them lives in page-formats. Write the two prompts so
  a reader is not confused into thinking one of them is wrong.
- A poster has only two sections, headline;call-to-action. That is deliberate, not an omission.
  Say so in that prompt's notes so nobody "fixes" it.

## Verify before you report
1. Fifteen prompts, one per key, every key present exactly once.
2. Every expected section order you quote matches data/base/structures.csv EXACTLY. Check
   programmatically and paste the output — a typo here makes the whole set untrustworthy.
3. At least three prompts in French and at least three in German.
4. No prompt references content that is not inline.

Python: C:\Users\ysuliman\AppData\Local\Microsoft\WindowsApps\python3.exe

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 10 lines: the language
split, the output of check 2, and any family where writing an honest prompt was hard — that is a
signal about the section model itself and I want to hear it.
