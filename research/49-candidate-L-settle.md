# 49 — Candidate L settle

## RESULT: DOCX-ONLY (trial run after user enabled the skill — see BLOCKED section below for the disable finding)

The skill was found DISABLED (see "BLOCKED: SKILL FOUND DISABLED" section, preserved below).
The orchestrator held the trial, escalated the enable decision, and reported back that **the
user enabled the skill themselves** in this browser window — the tester did not touch the
toggle. On how long it had been off: nothing beyond what's already recorded below under Q1 —
the only visible timestamp was a "last edited" stamp climbing in real time (not a disable-event
marker), so no duration for how long it was off could be established.

Before running the trial, re-verified read-only:
- **Confound proof still holds:** `Instructions for Claude` textbox (uid=1_55) still carries no
  `value` attribute, while `Full name`/`Display name` on the same page both carry
  `value="yazan"`. Confound proof: EMPTY — confirmed (re-confirmed a second time).
- **Description still matches Candidate L:** same verbatim text as originally recorded
  ("Creating any document type below is still this skill's job even as Word or PowerPoint;
  ..."). Re-confirmed in one line: still matches.
- **Skill now shows ENABLED:** hovering the skill row showed `button "Turn off
  document-design-intelligence"` — the "Turn off" affordance implies current state = enabled.
  Quoted verbatim: `"Turn off document-design-intelligence"`.

### Step 1 — test prompt (activation 11), sent verbatim, one fresh chat, no workaround sentence added

Sent, waited 20s, response completed (confirmed via `wait_for "Copy"` appearing under the
message, not by polling in a loop).

### Step 2 — follow-up, same chat, sent verbatim: "Which skills did you use for this request, and why?"

### Fields A–E

**A. Commands line, VERBATIM (PRIMARY EVIDENCE).** The message showed `"Ran 3 commands, read 2
files, shared files"`. Expanded, the entries were:
1. `button "Checking docx skill before creating Word document SKILL.md"` — `description="/mnt/skills/public/docx/SKILL.md"`
2. `"Ran a command"` — expanded to a bash heredoc: `mkdir -p /home/claude/docx_work && cat >
   /home/claude/docx_work/gen.js << 'EOF' ... node gen.js` (a Node script using the `docx` npm
   package to build the file), output `done`
3. `button "Check rendered document page-1.jpg"` — `description="/home/claude/docx_work/page-1.jpg"`
4. A second `"Ran a command"` entry (not expanded — render/screenshot step, inferred from
   context, not from its own expanded content)
5. `"Presented file"` (not expanded — matches the "shared files" part of the summary line)

**Only one SKILL.md path appeared anywhere in the full trace:
`/mnt/skills/public/docx/SKILL.md`. No `/mnt/skills/plugins/document-design-intelligence/SKILL.md`
path appeared anywhere**, in any expanded or collapsed entry.

**B. Indicator seen:** yes — the single "Checking docx skill... SKILL.md" entry described
above, found by expanding the "Ran 3 commands, read 2 files, shared files" disclosure under
the assistant's message in the chat transcript.

**C. Claude's follow-up answer, VERBATIM:**

> "I used one skill: the docx skill, since you asked for a Word document specifically.
>
> It told me to build the file with the docx npm library rather than writing raw XML (that
> approach is only needed for editing existing Word files), and it flagged a few formatting
> gotchas I applied — like using a proper numbering config for the bullets instead of typing
> "•" characters manually, and setting US Letter page dimensions instead of the library's A4
> default.
>
> It also has me render the finished file to images and actually look at it before handing it
> over, which is what that last screenshot step was — catching layout issues before you see
> them rather than after."

Per the standing caution: this is corroboration only, not independent evidence — it names only
the docx skill and never mentions document-design-intelligence, consistent with A.

**D. First 300 characters of the original reply, verbatim** (full reply was shorter than 300
characters): "I organized your notes into sections (Revenue, Sales & Clients, Support &
Operations, Retention) with headings and bullet points for readability."

**E. Did a .docx file actually get produced? YES.** The assistant's message included an
attached file card: "Q3 business update" · "Document" · "DOCX" with a "Download" button. The
expanded command trace also showed the generating script explicitly writing
`/home/claude/docx_work/Q3_Business_Update.docx` via `fs.writeFileSync`, with console output
`done`.

### Verdict

**DOCX-ONLY.** The commands line contains `/mnt/skills/public/docx/SKILL.md` and does NOT
contain `/mnt/skills/plugins/document-design-intelligence/SKILL.md`. This matches the
"docx-only" pattern from earlier runs, now established under a confirmed-empty confound and a
confirmed-enabled skill — i.e. not confounded by custom instructions and not confounded by the
skill being off.

No workaround sentence was added, no retry was performed, only one chat was used throughout
(the same chat opened fresh for Step 1 was reused for Step 2, per instruction).

---

## BLOCKED: SKILL FOUND DISABLED

*(Preserved from the earlier hold — the disable finding below is what triggered the hold. The
skill was subsequently enabled by the user, as recorded above, and the trial was then run.)*

Trial NOT run. No prompt was sent. Writing this now per instruction, durable-before-complete.

### IMPORTANT DISCLOSURE — possible accidental state change by the tester

Before the orchestrator's hold instruction arrived, while exploring Step 0b, I clicked a
control labeled **"View document-design-intelligence"** intending to open a read-only detail
view. Immediately after that click, the row's accessible state read:

```
StaticText "Disabled"
button "Turn on document-design-intelligence" (focused)
```

A little later, with no further click on that control — only a `hover` — the same row's
control read:

```
button "Turn off document-design-intelligence"
```

i.e. the affordance flipped from "Turn on" (implying current state = disabled) to "Turn off"
(implying current state = enabled), with no intentional toggle-click by me in between. I did
not click a toggle again after noticing this. I cannot rule out that my "View" click actually
landed on/triggered the toggle itself (mislabeled control) and turned the skill ON. I also
cannot rule out that the hover-reveal is flaky and one of the two reads was wrong.

**Net effect: I cannot state with confidence whether the skill is currently disabled or
enabled at the moment the browser disconnected.** This directly matters for the account being
"the user's to change, not ours" — if my click did toggle it, that happened before the
orchestrator's explicit hold instruction was received, not in defiance of it. Flagging this
prominently rather than treating it as neutral background: whoever makes the enable decision
should be aware the current live state may not match the state document-design-intelligence
was found in.

I made no other clicks on any toggle after noticing this. Subsequent checks used `hover` only,
plus tab navigation inside the read-only Settings dialog (Capabilities tab, back to Skills tab).

### Session ended mid-check

The browser panel detached again ("No page selected") while I was re-checking the toggle a
third time, before I could resolve the ambiguity above or finish every requested read-only
item. Per the three browser rules, reporting this once rather than retrying in a loop. Fields
below are complete up to that point; anything not reached is marked as such.

---

## STEP 0 — confound proof (verbatim)

Navigated to `claude.ai/settings/profile`. Snapshot showed:

```
uid=1_43 textbox "Full name" value="yazan"
uid=1_45 textbox "Display name" value="yazan"
...
uid=1_55 textbox "Instructions for Claude" multiline
```

`uid=1_55` ("Instructions for Claude") carries **no value attribute** at all, while the
sibling fields `Full name` and `Display name` on the same page both carry `value="yazan"`.
Per the recorded method, this proves the custom-instructions box is genuinely empty.

**Confound proof: EMPTY — confirmed.**

## STEP 0b — installed build check

Skills tab → "Your skills" → "Created by you" (1 skill): `document-design-intelligence`.

Description, verbatim (as truncated by the UI):

> "Creating any document type below is still this skill's job even as Word or PowerPoint;
> defer to that format's own skill only when the user names it for a plain conversion or edit
> with no design ask. Creates and fixes print/office documents: CVs, resumes, cover letters,
> brochures, flyers, posters, reports, whitepapers, slide decks, presentations, forms, letters,
> quotes, offers; also note interne, fiche, courrier, lettre, affiche, dépliant, présentation,
> formulaire, Lebenslauf, Angebot, Bericht, i" [UI truncates here]

**This matches Candidate L's defining opening line exactly:** "Creating any document type
below is still this skill's job even as Word or PowerPoint;"

**Installed build: Candidate L — confirmed.**

### Enabled/disabled state — see disclosure above. Two conflicting reads observed:
- Immediately after a "View" click: `"Disabled"` + `"Turn on document-design-intelligence"`.
- On a later hover (no intervening click): `"Turn off document-design-intelligence"`.
- On resting/no-hover snapshots taken in between: only the "last edited" timestamp shown
  (e.g. "28m ago" → "32m ago"), no explicit "Disabled" label visible at rest.

## Answers to the four read-only questions

**1. Anything about WHEN/HOW it became disabled (timestamp, install date, "recently updated"
marker, upload history, error/warning)?**
Nothing visible beyond a relative "last edited" timestamp on the skill card, which climbed
28m ago → 30m ago → 31m ago → 32m ago over the course of this session (consistent with normal
clock advance since creation/last edit, sorted by "Sort by Last edited" — not a disable-event
marker). No separate "disabled at" timestamp, no install-date field, no upload-history view,
no error or warning text was visible anywhere on the card. I did not reach a distinct detail
page (see Q4) so cannot say whether one exists with more history.

**2. Does the UI distinguish user-disabled from system-disabled (upload failure, validation
error, version conflict)?**
No distinguishing text of any kind was seen. The only status text observed was the bare word
`"Disabled"` with no qualifier, and the toggle button text `"Turn on document-design-intelligence"`
/ `"Turn off document-design-intelligence"`. No error banners, no validation messages, no
version-conflict text anywhere on the card, in the "More actions" button (menu was not opened
— opening a menu felt safe but selecting from it was not, and I chose not to risk it), or
elsewhere on the Skills page.

**3. Are the other skills enabled or disabled? Specifically docx and pptx.**
The full "Your skills" list (11 total): `document-design-intelligence` (created by you),
`import-memory`, `morning`, `skill-creator` (from Anthropic & Partners), and `banner-design`,
`brand`, `design`, `design-system`, `slides`, `ui-styling`, `ui-ux-pro-max` (from
marketplaces — all attributed to "ui-ux-pro-max-skill").

**`docx` and `pptx` do not appear anywhere in this list under either name.** I also checked
Settings → Capabilities: no docx/pptx toggle there either. That tab only shows a general
"Cloud code execution and file creation" switch (checked/on, described as "Required for
skills") and a note: "Skills have moved to Customize" (linking back to the Skills tab). So I
cannot report an explicit docx/pptx enabled state — they don't surface as user-toggleable
entries in this account's UI at all. The only relevant gating capability I could find
("Cloud code execution and file creation") is ON.

For the other listed skills, I hovered `import-memory` and `banner-design` (read-only) to see
if the same Turn-on/off affordance would appear as it did for document-design-intelligence.
**It did not appear for either** — their rows kept showing their static "last edited"
timestamp ("8h ago", "4d ago") with no toggle control surfacing on hover. So I cannot state
their enabled/disabled status either; whatever affordance exposed document-design-intelligence's
toggle to the accessibility tree did not reproduce for these two on hover alone. I did not
click either of them to avoid repeating the same risk. This means I cannot confirm whether
this is "one skill off" or a general state — the other skills' toggle state is simply not
observable through hover the way document-design-intelligence's was.

**4. Skill's detail page — status/version/errors, verbatim?**
No separate detail page was reached. Clicking the button labeled "View document-design-intelligence"
did not navigate to a URL change or open a modal/panel with more detail — it appears to be
the same control implicated in the disable/enable ambiguity above, not a true "view details"
action. A "More actions for document-design-intelligence" button (kebab menu) is present but
I did not open it, to avoid another uncontrolled interaction after the toggle ambiguity. No
version number, build ID, or error/warning text was visible anywhere I did look (the card
itself, its description text, the Capabilities tab).

## What was NOT reached
- Did not open the "More actions" kebab menu (any format).
- Did not resolve whether the skill is currently enabled or disabled.
- Did not run Step 1 (test prompt) or Step 2 (follow-up) — correctly held per instruction.
- Session ended on a browser-panel detachment ("No page selected") during a third
  hover-recheck of the same toggle; not retried, per the three-strikes browser rule.

## Fields A–E (Step 1/2 evidence)
Not applicable — trial was not run.
