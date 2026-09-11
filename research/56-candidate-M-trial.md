# 56 — Candidate M trial

## RESULT: DOCX-ONLY

## Build verification — YES

Navigated to Settings → Skills → "Your skills" → "Created by you" (1 skill:
`document-design-intelligence`). Description shown in the UI, verbatim (truncated by the UI at
the same point as before):

> "Creating any document type below is still this skill's job even for '.docx'/'.pptx' requests
> naming Word or PowerPoint; defer to that format's own skill only when the user names it for a
> plain conversion or edit with no design ask. Creates and fixes print/office documents: CVs,
> resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks,
> presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, lettre,
> affiche, dépliant, présentation, formulaire"

The fragment `even for '.docx'/'.pptx' requests naming Word or PowerPoint` is present, matching
Candidate M's proposed text exactly (draft in `research/50-candidate-M-draft.md`). **This is
Candidate M, not the old build — confirmed.**

## Skill enabled — hover only, confirmed

Hovered the `document-design-intelligence` row (no click on the toggle, no click on "View").
The row's accessible control read:

```
button "Turn off document-design-intelligence"
```

"Turn off" implies current state = enabled. No toggle or View click was made.

## Step 0 — confound proof (verbatim)

On `Settings → General` (Profile section) snapshot:

```
uid=1_38 textbox "Full name" value="yazan"
uid=1_40 textbox "Display name" value="yazan"
...
uid=1_50 textbox "Instructions for Claude" multiline
```

`Instructions for Claude` (uid=1_50) carries **no `value` attribute** at all, while the sibling
`Full name` and `Display name` fields on the same page both carry `value="yazan"`. Confound
proof: EMPTY — confirmed.

## Step 1 — test prompt (activation 11), sent verbatim, one fresh chat via navigate_page to claude.ai/new

Sent verbatim, no workaround sentence added:

```
Here are my rough notes:
- Q3 revenue up 12% vs Q2
- New enterprise client signed: Bramwell Logistics
- Support ticket backlog down from 340 to 190
- Need to hire 2 more support reps by Q4
- Churn rate flat at 4.1%
Turn my rough notes into a Word document.
```

Note: the chat composer's rich-text editor auto-converted the `-` bulleted lines into a list on
input (standard markdown-autoformat behavior of this editor, not a deviation I introduced); the
underlying text content sent was unchanged. Waited for completion via `wait_for "Copy"` (well
over 20s elapsed between send and the response being fully rendered).

## Step 2 — follow-up, same chat, sent verbatim: "Which skills did you use for this request, and why?"

Also completed in the same chat, no reload/navigation away at any point after Step 1 was sent.

## Fields A–E

**A. Commands line, VERBATIM (PRIMARY EVIDENCE).** Message showed `"Ran 3 commands, read 2
files, shared files"`. Expanded, the entries were:
1. `button "Checking docx skill before creating Word document SKILL.md"` —
   `description="/mnt/skills/public/docx/SKILL.md"`
2. `"Ran a command"` (not expanded)
3. `"Ran a command"` (not expanded)
4. `button "Visual check of generated document page-1.jpg"` —
   `description="/home/claude/work/page-1.jpg"`
5. `button "Looks clean. Let me get it into the outputs folder."` (not expanded)
6. `"Ran a command"` (not expanded)
7. `"Presented file"` (not expanded — matches "shared files")

**Only one SKILL.md path appeared anywhere in the full trace:
`/mnt/skills/public/docx/SKILL.md`. No `/mnt/skills/plugins/document-design-intelligence/SKILL.md`
path appeared anywhere**, in any expanded or collapsed entry.

**B. Indicator seen:** yes — the single "Checking docx skill... SKILL.md" entry described above,
found by expanding the "Ran 3 commands, read 2 files, shared files" disclosure under the
assistant's message.

**C. Claude's follow-up answer, VERBATIM:**

> "I used one skill: docx (the Word-document creation skill). Here's why and how:
>
> Trigger: You explicitly asked for a Word document, which is exactly what that skill's
> description covers.
>
> What it told me to do:
> Use the docx npm library (already installed) rather than writing raw XML, since I was creating
> a new file from scratch.
> Avoid known pitfalls it documents — e.g., use proper Paragraph/TextRun elements instead of \n
> characters, use HeadingLevel for headings instead of manually bolding text, and set explicit
> page dimensions.
> Render the result to images (soffice → PDF → pdftoppm) and actually look at it before calling
> it done, rather than trusting the code ran without errors.
>
> I didn't need any of the other available skills (pptx, xlsx, pdf, etc.) since the deliverable
> was a single Word document with no images, tables, or existing file to edit."

Per the standing caution: this is corroboration only, not independent evidence — it names only
the docx skill (and explicitly disclaims needing pptx/xlsx/pdf), never mentions
document-design-intelligence, consistent with A.

**D. First 300 characters of the original reply, verbatim** (full reply was shorter than 300
characters): "I organized your notes into sections (Revenue, New Business, Support Operations,
Customer Retention) with a clean heading structure. Let me know if you'd like it in French for
your manager, or want any numbers highlighted differently."

**E. Did a .docx file actually get produced? YES.** The assistant's message included an attached
file card: "Q3 business update" · "Document" · "DOCX" with a "Download" button.

## Verdict

**DOCX-ONLY.** The commands line contains `/mnt/skills/public/docx/SKILL.md` and does NOT
contain `/mnt/skills/plugins/document-design-intelligence/SKILL.md`. Candidate M's literal-token
addition (`'.docx'`/`'.pptx'` in the deferral sentence) did not change the outcome for activation
11 — identical result to Candidate L (`research/49-candidate-L-settle.md`) and to the
pre-L baseline. Per the falsification test defined in `research/50-candidate-M-draft.md` §7:
this result falsifies the token-parity mechanism M targeted (Claude cited the docx skill's own
trigger criteria again and did not engage with ours, the same pattern as P6 under L).

No workaround sentence was added, no retry was performed, only one chat was used throughout (the
same chat opened fresh for Step 1 was reused for Step 2). No reload or navigation away occurred
from the moment the Step 1 prompt was sent through the end of the trial.
