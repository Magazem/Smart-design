# BRIEF — DDR — Ruling F: prompt 4 tests appearance, plus a scope note

Repo root: C:\Users\ysuliman\Documents\Ai plugin
DO NOT touch git. Do not edit SKILL.md. Do not rebuild the ZIP.

## Why
The rerun passed prompts 2, 3 and 5. Prompt 4 failed for a real reason: Claude said the pasted
paragraph "is not a document, just text", then looked in the skill for rules about correcting
AI-sounding writing and found none. That is correct behaviour. I checked data/base myself —
every table is layout, typography, colour, print or ATS. Nothing covers prose quality. The
"looks like AI" trigger is about how a document LOOKS, not how it reads. Prompt 4 as written
tests a promise the skill never made.

## Deliverable (ONE)
Make prompt 4 test appearance, and state the scope boundary in two places.

### 1. Rewrite prompt 4 in skill/document-design-intelligence/references/activation.md
It currently pastes an AI-sounding paragraph. Replace that with an inline description of how
the document LOOKS. The lead's example, which you may improve on but not weaken:

  "My quarterly report is 6 pages, every heading is centred and bold in a different font, body
  is 10pt Calibri with 1cm margins, there are three colours of bullet points and a clip-art
  chart. It looks like it was thrown together by AI, can you fix it?"

Keep the spirit of the original: no document-type noun beyond "report", no attachment needed.
Rewrite its Pass/Fail lines:
- PASS: the skill fires and reasons about hierarchy, typography, margins or colour, OR asks a
  question framed around those.
- FAIL: generic advice, or it asks for the file.

Change NOTHING else in the 13-prompt section. Prompts 1-3 and 5-13 stay byte-identical.

### 2. Scope note, one line, in two files
- activation.md: put it immediately AFTER the "**Length: 823 characters**" paragraph that
  follows the "## The description as shipped" block, around line 36-40.
  CRITICAL: do NOT edit the fenced description block itself. It is byte-identical to SKILL.md
  and a test depends on that. Also do not touch "Alternate A" or "Alternate B" further down —
  those are retained-for-reference historical text.
- RELEASE-NOTES.md: under the "## Known limitation" heading at line 18, alongside the existing
  German deck note.
Wording, one line, same sense in both: the skill fixes how a document LOOKS, not how its prose
reads; AI-sounding wording is out of scope for v0.1.0.

### 3. Mirror
- TESTS-FOR-USER.md "## Test 11 — 13-prompt activation list": note that prompt 4 now describes
  the document's appearance rather than pasting prose.
- skill/dist/POST-UPLOAD-TESTS.md Test (c): same note. Gitignored, disk-only; do it anyway.

## Verify before you report
1. `git diff skill/document-design-intelligence/references/activation.md` — the only hunks are
   prompt 4, the scope note, and nothing else.
2. The fenced description block still matches SKILL.md exactly. Check it:
   python3 -c "import io,re;s=io.open('skill/document-design-intelligence/SKILL.md',encoding='utf-8').read();d=re.search(r'^description:\s*\"(.*)\"\s*$',s,re.M).group(1);a=io.open('skill/document-design-intelligence/references/activation.md',encoding='utf-8').read();i=a.index('## The description as shipped');q=a[a.index('```',i)+4:a.index('```',a.index('```',i)+4)];print(' '.join(q.split())==d)"
   It must print True.
3. All 13 prompts present and numbered 1-13.

## Report
Message the orchestrator (01a080c5-2001-78b3-bbbe-afaae15edafa), max 8 lines: the new prompt 4
verbatim, the scope-note wording, the files touched, and the True/False from check 2.
