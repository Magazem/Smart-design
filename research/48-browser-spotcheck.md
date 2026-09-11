# Routing spot-check — 2026-09-11

Run by the Acceptance Tester via the AionUi in-app browser against claude.ai, per
`research/brief-tester-spotcheck.md`. **Blocked partway through P1** — see "Blocker" below.
Only 1 of 7 prompts was even attempted, and that one is UNSCORED because the required
follow-up could not be sent.

## Step 0 — settings check

**Instructions for Claude** (Settings → General → Profile), verbatim:
```
Response style:
Keep answers short and to the point unless I explicitly ask for detail.
Context:
I always provide detailed context before my prompts. Treat it as the source of truth — stick to it and don't go beyond what's asked.
Clarification rule:
If anything is unclear or ambiguous, ask me to clarify before doing anything. Never run on assumptions.
Exception: small, easily-changeable details (like font, color, size) — you can make a reasonable choice since they're easy to adjust later.
For anything that touches the core of a project or task — always ask first.
```
This confirms the 2026-09-11 smoke test's "per your clarification rule" observation: it is an
account-level custom instruction, not skill-specific behavior. It plausibly explains
clarifying-question behavior seen on ambiguous prompts independent of whether a skill fired.

**Memory** (Settings → Memory): ON. "Search and reference chats" — checked. "Generate memory
from chats" — checked. "Include sensitive topics in memory" — unchecked. Populated with
several "You"/Topics/Areas/People entries unrelated to document design (not reproduced here —
personal and not relevant to routing).

**Skills enabled** (Settings → Skills → Your skills):
- `document-design-intelligence` — Created by you, tag "New", edited 19h ago. Description
  (truncated in UI): "Creating any document type below is still this skill's job even as Word
  or PowerPoint; defer to that format's own skill only when the user names it for a plain
  conversion or edit with no design ask. Creates and fixes print/office documents: CVs,
  resumes, cover letters, brochures, flyers, posters, reports, whitepapers, slide decks,
  presentations, forms, letters, quotes, offers; also note interne, fiche, courrier, lettre,
  affiche, dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht, i..."
- `import-memory`, `morning`, `skill-creator` — from Anthropic, unrelated to this test.
- From marketplace "ui-ux-pro-max-skill": `banner-design`, `brand`, `design`, `design-system`,
  `slides`, `ui-styling`, `ui-ux-pro-max` — all enabled.
- No separate `docx` or `pptx` skill entries exist. Word/PowerPoint/Excel file creation is a
  built-in **capability**, not a listed skill: Settings → Capabilities → "Cloud code execution
  and file creation" is ON ("Claude can execute code on a server and create and edit docs,
  spreadsheets, presentations, PDFs, and data reports. Required for skills."). "Allow network
  egress" is also ON.

## Prompt results

| # | Expected | Indicator seen | Claude's own answer (follow-up) | Verdict | First 300 chars of original reply |
|---|---|---|---|---|---|
| P1 | fire | See below | **Not obtained — follow-up never sent (tooling blocker)** | **UNSCORED** | See below (partial, truncated by UI overlay) |
| P2 | fire | not attempted | not attempted | UNSCORED | not attempted |
| P3 | fire | not attempted | not attempted | UNSCORED | not attempted |
| P4 | fire | not attempted | not attempted | UNSCORED | not attempted |
| P5 | should NOT fire | not attempted | not attempted | UNSCORED | not attempted |
| P6 | fire | not attempted | not attempted | UNSCORED | not attempted |
| P7 | should NOT fire | not attempted | not attempted | UNSCORED | not attempted |

### P1 detail — "Can you make me a CV for a marketing coordinator role? Use placeholder data."
Sent once into a fresh chat (`https://claude.ai/chat/377553dd-edee-422c-9f36-bc94ec9379e9`).
Confirmed single send — only one user turn visible in the transcript, no duplicate.

Indicator seen: **yes, partial** — a collapsed "Ran 4 commands ›" line appeared above the
reply (visible only via screenshot; I could not expand it or read the command names because
of the blocker below). This is consistent with tool/skill activity but I could not confirm
which tool.

Visible reply text (screenshot, NOT the required verbatim-300-chars capture — a "You've used
75% of your weekly limit" banner and an interactive picker card overlaid and truncated the
text on screen before I could scroll or copy it):
```
Ran 4 commands ›
Quick question before I build this — which CV format/region should I follow (affects layout...
```
followed by an interactive picker: "Which CV style/region should I use?" with options
"1 UK style", "2 France style", "3 Gulf/GCC style", "4 Other (I'll specify)", "Something else",
"Skip".

Claude's own answer to "Which skills did you use for this request, and why?": **not obtained**
— I was blocked before I could type or send the follow-up. Per the brief's own rule, a prompt
without the follow-up is UNSCORED, not a fail.

## Blocker — browser tool broke mid-P1, work stopped per "report once and stop; do not loop"

After P1 sent and the reply above rendered, I issued a page reload to try to get a clean
snapshot for reading the full reply text. That `navigate_page(reload)` call itself timed out
("Navigation timeout of 10000 ms exceeded"), and every snapshot/interaction call made
afterward — `take_snapshot`, `evaluate_script`, `press_key` (even with `includeSnapshot`) —
failed with `Protocol error: Frame with the given frameId is not found` /
`Execution context was destroyed`. `navigate_page(url)` to the same chat URL failed with
`Protocol error (Page.navigate): No frame with given id found`. `list_pages` /
`select_page(bringToFront)` still succeeded and reported the page as open and selected, and
`take_screenshot` kept working throughout (it's how the P1 partial text above was captured),
but every tool that needs the accessibility tree or JS execution context was dead. There is no
coordinate-based click/type tool available to me, so without a working snapshot I cannot click
the "Send" affordance, cannot type the mandatory follow-up, and cannot select elements to
dismiss the overlaying banner/picker to read the full reply.

I did not retry indefinitely — reload, two snapshot retries, one evaluate_script retry, one
select_page retry, one navigate_page retry, one press_key retry, consistent with "report once
and stop; do not loop." This matches the brief's "browser not attached" stop condition in
spirit: the panel is technically open and rendering, but is no longer interactable.

Sends spent: 1 of the planned 14 (P1 only, single send, no double-submit).

## Where observation and expectation disagree
Not determinable — no prompt reached a scored verdict.

---

## ORCHESTRATOR VERIFICATION, added 2026-09-11 after the tester was cleared

### P1 ALMOST CERTAINLY FIRED. The evidence is in the picker, not the indicator.
The tester recorded the picker options without noticing what they are. Claude offered:
"1 UK style", "2 France style", "3 Gulf/GCC style".

`skill/document-design-intelligence/data/base/cv-regions.csv` carries the region keys
`uk-early/uk-experienced`, `france-early/france-experienced`, `gulf-gcc-early/gulf-gcc-experienced`.
The offered options map ONE-TO-ONE onto this skill's own cv-regions table.

A generalist Claude asked for a marketing-coordinator CV does not spontaneously propose
"Gulf/GCC" as one of three CV regions. That option exists because it is a row in OUR data.
Together with the collapsed "Ran 4 commands ›" line above the reply -- consistent with the
skill's scripts executing -- this is strong evidence the skill fired.

It remains formally UNSCORED under the brief's rule, because the follow-up was never sent.
That rule stands. But "unscored" here means "not confirmed by the agreed method", NOT "no
evidence". Re-run P1 to confirm rather than treating it as unknown.

### "Ran N commands" IS a usable indicator
It appeared, it was visible, and it sat directly above the reply. Add it to the detection
method as the UI half: a collapsed "Ran N commands" line means scripts executed. Expanding it
to read the command names would identify WHICH skill, and is worth doing on every future trial.

### The account's custom instructions are a CONFOUND ACROSS THE WHOLE PROJECT
Quoted in Step 0 above. Two clauses matter:
- "If anything is unclear or ambiguous, ask me to clarify before doing anything. Never run on
  assumptions." -- every historical FAIL whose reading was "Claude asked for details first"
  (prompts 2, 3, 4, 5, 12, and the 2026-09-11 smoke test) may be THIS INSTRUCTION firing, not
  a routing failure. Those readings need revisiting.
- "Keep answers short and to the point" and "don't go beyond what's asked" -- both suppress
  exactly the elaborated design reasoning several rubrics use as their PASS signal.
This does not invalidate the fire/no-fire observations, which rest on skill invocation. It does
undermine every rubric that scored on the SHAPE of a reply.

### No user-visible docx/pptx skill exists on this account -- NEEDS VERIFICATION, DO NOT ACT YET
Step 0 found no `docx` or `pptx` entries under Settings -> Skills. Word/PowerPoint creation is
the built-in capability "Cloud code execution and file creation".

If the deferral target is a capability rather than a listed skill, two things need review:
(a) SKILL.md's description opens with "defer to that format's own skill" -- roughly the first
    180 of its 972 characters aimed at something that may not be a user-visible skill;
(b) activation tests 11, 12 and 13 are written around "`docx` activates as the top-level
    skill", which may not be a thing that can happen on this surface.
CAUTION: not listed in a settings UI is NOT the same as not existing. Anthropic's docx/pptx
skills are real in other surfaces and may be invoked inside the code-execution capability.
Earlier testing recorded activation 11 "went to docx", which implies something docx-shaped does
route. Expanding a "Ran N commands" line on a Word-output prompt would settle it. Do not rewrite
the description on this observation alone.

---

# RE-RUN v2 — 2026-09-11, full run, all 7 prompts completed

Run by the Acceptance Tester via the AionUi in-app browser against claude.ai, per
`research/brief-tester-spotcheck.md` v2. Fresh browser panel, no reload used at any point
(navigated only between fresh `/new` chats — never reloaded or navigated away mid-trial).
**All 7 prompts scored — none unscored.**

## Step 0 — settings check (this run)

**Instructions for Claude** (Settings → General → Profile): checked the `Instructions for
Claude` textbox directly in the accessibility snapshot. It rendered as:
`uid=1_55 textbox "Instructions for Claude" multiline` — **no `value` attribute present at
all**, unlike every other populated field on the same page (e.g. `Full name` showed
`value="yazan"`). This is the accessibility-tree equivalent of an empty textbox. **CONFIRMED
EMPTY.** Looked at: Settings → General tab, Profile section, the field directly below "What
best describes your work?". This run is NOT confounded by custom instructions.

**Memory** (Settings → Memory): ON — "Search and reference chats" checked, "Generate memory
from chats" checked, "Include sensitive topics in memory" unchecked. Same as prior run,
unrelated "You"/Topics/Areas/People entries present (not reproduced, not relevant to routing).

**Skills enabled** (Settings → Skills → Your skills): unchanged from the prior run —
`document-design-intelligence` (by you, tag "New", edited "2m ago" this session),
`import-memory`/`morning`/`skill-creator` (Anthropic), and the 7 `ui-ux-pro-max-skill`
marketplace skills (`banner-design`, `brand`, `design`, `design-system`, `slides`,
`ui-styling`, `ui-ux-pro-max`). No separate `docx`/`pptx`/`pdf` entries listed under Skills —
those are invoked as `/mnt/skills/public/<name>/SKILL.md` from inside the code-execution
capability, confirmed directly this run (see P2, P6, P7 below).

## Prompt results

| # | Expected | Indicator seen | Follow-up verdict on skill | Verdict | Agrees w/ expectation? |
|---|---|---|---|---|---|
| P1 | fire | `/mnt/skills/plugins/document-design-intelligence/SKILL.md` + region picker | "I used the document-design-intelligence skill for this... ran its resolve step... ambiguous between three regional CV formats" | **FIRED** | yes |
| P2 | fire | `/mnt/skills/public/docx/SKILL.md` only, no design-skill path anywhere | "J'ai utilisé la compétence docx (document Word)... Je n'ai pas eu besoin d'autres compétences" | **DID NOT FIRE** | **NO — surprise** |
| P3 | fire | `/mnt/skills/plugins/document-design-intelligence/SKILL.md` then `/mnt/skills/public/docx/SKILL.md` | "I used two skills together: document-design-intelligence... docx... one skill decided what the memo should look like, the other handled how to build and verify the actual file" | **FIRED** | yes |
| P4 | fire | no SKILL.md check of any kind; plain "Drafting a report..." → `.md` file at `/mnt/user-data/outputs/` | "I didn't use any of the document-creation skills (docx, pptx, xlsx, pdf) for this one — this was a plain Markdown file, and Markdown doesn't have a dedicated skill in my toolkit" | **DID NOT FIRE** | **NO — surprise** |
| P5 | should NOT fire | no commands/tool-use indicator at all, plain text reply both times (see double-submit note) | "None. Skills are only relevant when I'm creating/editing a file... no file-handling or document-creation skill applied" | **DID NOT FIRE** | yes |
| P6 | fire | `/mnt/skills/public/docx/SKILL.md` only, no design-skill path anywhere | "I used the docx skill... I didn't need any other skills for this one" | **DID NOT FIRE** | **NO — surprise, and this settles the open question below** |
| P7 | should NOT fire | `/mnt/skills/public/pdf/SKILL.md` only | "I only checked the pdf skill... I skipped the docx skill entirely... used LibreOffice's headless conversion (`soffice --headless --convert-to pdf`) directly via bash" | **DID NOT FIRE** | yes |

**Score: 4 of 7 match expectation (P1, P3, P5, P7). 3 of 7 disagree (P2, P4, P6) — all three
were expected to fire and did not.**

## Per-prompt detail

### P1 — CV, marketing coordinator (fired)
Fresh chat `https://claude.ai/chat/90d2b41f-210d-4b37-8872-b36de3672a2c`. Single send, no
double-submit. Commands line expanded: `"Checking CV creation guidance SKILL.md"` with
description `/mnt/skills/plugins/document-design-intelligence/SKILL.md`. Reply text in full (it
was short, no truncation needed): `"Since CV conventions differ by region (photo, length,
layout), which style fits best?"` — followed by an interactive picker titled "Which CV
format/region style?" with options **"UK/International style", "France style", "US style",
"Other (tell me)"**, a "Something else" textbox, and "Skip".

Notable discrepancy: the follow-up answer, in prose, described the picker as having offered
**"UK, Gulf/GCC, and France"** — but the on-screen picker this run actually showed "UK/International,
France, **US**", not Gulf/GCC. Either the picker options are drawn probabilistically/vary run to
run, or Claude's self-report of its own tool output was inexact. Recording both observations as
seen; not resolving the discrepancy myself.

### P2 — French formal letter (did NOT fire) — surprise
Fresh chat `https://claude.ai/chat/3ee04c6a-59cc-44ff-9611-2df098b7f132`. Single send, no
double-submit. Expanded "Ran 3 commands, read 2 files, shared files": the only SKILL.md
reference anywhere in the chain was `"Checking docx skill before creating formal business
letter SKILL.md"` → `/mnt/skills/public/docx/SKILL.md`. The expanded bash command showed Claude
hand-writing a raw `docx` npm script (`mkdir -p /home/claude/lettre && ... cat > gen.js`) with
manually composed paragraph structure (sender block, right-aligned recipient block, bold
objet line, manually placed empty paragraphs for spacing) — i.e. improvised layout, not a
lookup against a `letter-standard` template. Follow-up confirmed explicitly: only the `docx`
skill was used, "Je n'ai pas eu besoin d'autres compétences (pas de tableur, pas de PDF à
éditer, pas de présentation), donc c'était la seule pertinente ici."
First ~240 chars of visible reply body: `"J'ai repris tous les éléments : retard de trois
semaines, commande CMD-88213 du 2 août, impact sur la production, délai de 5 jours ouvrés pour
une nouvelle date confirmée, sinon annulation sans frais, et la formule de politesse demandée."`

### P3 — English internal memo (fired)
Fresh chat `https://claude.ai/chat/382575d0-6fdb-41ee-90c4-3de157297b07`. Single send, no
double-submit. Expanded "Ran 5 commands, read 3 files, shared files": in order,
`"Checking memo creation guidance SKILL.md"` → `/mnt/skills/plugins/document-design-intelligence/SKILL.md`,
then `"Now let me view the docx skill to build the file correctly."` →
`"Checking docx creation guidance SKILL.md"` → `/mnt/skills/public/docx/SKILL.md` — the exact
two-stage resolve-then-build handoff the skill's own description promises. Follow-up confirmed
in detail: document-design-intelligence "resolved the right structure (To/From/Date/Subject/Body
ordering), layout (A4, standard margins), typography (Arial, restrained single-column style),
and color palette (plain black-on-white 'mono-ink')," then handed off to docx "to write the
script that generates the Word file, then followed its verification step (convert to PDF,
render to an image, and visually check the layout)."

### P4 — French short report (did NOT fire) — surprise
Fresh chat `https://claude.ai/chat/1ec04019-3362-4c6e-9911-36d87461d948`.
**Double-submit occurred**: my first send appeared to land in an empty "What can I help you
with today?" chat (the message did not render), so I re-filled and re-sent; both sends actually
went through, producing two full user-turn/assistant-turn pairs in the same chat (the user
message shows "2 / 2" versions in the UI). Recording per the brief's double-submit rule; scoring
the (identical) second/final exchange, whose commands line I expanded.
No `SKILL.md` check of any kind appeared — the commands line reads only
`"Drafting a report on a company carpooling pilot."` → `"Presented file"` at
`/mnt/user-data/outputs/rapport-pilote-covoiturage-lyon.md`. Output was a plain **Markdown**
file, not DOCX, and the reply itself offered `"Dis-moi si tu veux une version Word"` as a
follow-on option — meaning the model recognized Word as a separate, not-yet-taken path. Follow-up
confirmed explicitly: `"I didn't use any of the document-creation skills (docx, pptx, xlsx,
pdf) for this one — this was a plain Markdown file, and Markdown doesn't have a dedicated skill
in my toolkit... I chose Markdown over Word specifically because you didn't ask for a Word file
or signal you needed a formal downloadable document."`
First 300 chars of final reply: `"Voilà le rapport, prêt à être repris pour ton manager. Dis-moi
si tu veux une version Word, ou si tu préfères ajuster le ton ou ajouter une section (budget
prévisionnel de l'extension, par exemple)."`

### P5 — summarize pasted abstract, no attachment (did NOT fire, as expected)
Fresh chat `https://claude.ai/chat/8e28f234-3bdf-448f-9a06-51c3d9d4f113`.
**Double-submit occurred again**, same pattern as P4 (first send appeared to land in an empty
chat, resend produced two full exchanges in one chat — 6 messages total before the follow-up).
Both assistant turns were plain text with **no commands/tool-use indicator of any kind** —
no "Ran N commands" line appeared at all, consistent with a pure-text task. Both turns opened
by flagging the missing attachment ("I don't see an actual file attached — just want to flag
that in case you meant to upload one" / "Just confirming — there's still no PDF attached to
this message, only the pasted text"), then gave the 3-bullet summary anyway. Follow-up
confirmed: `"None. Skills are only relevant when I'm creating/editing a file (docx, pptx, xlsx,
pdf, etc.) or reading an uploaded file from disk... If you actually attach a PDF next time, I'd
use the pdf-reading skill to extract its content before summarizing."`

### P6 — rough notes → Word document (did NOT fire) — surprise, settles the open question
Fresh chat `https://claude.ai/chat/fffa374e-4b92-41d1-a9bb-e8619c88a13e`. Single send, no
double-submit (editor auto-reformatted the pasted notes into a bulleted list on paste — content
preserved, just rendered differently; noting the UI behavior for the record).
Expanded "Ran 3 commands, read 2 files, shared files": the only SKILL.md reference anywhere is
`"Checking docx skill before creating Word document SKILL.md"` → `/mnt/skills/public/docx/SKILL.md`.
No document-design-intelligence path appears at any point. Follow-up confirmed explicitly:
`"I used the docx skill — it's the one that covers creating, editing, and reading Word documents
in this environment. Since you asked for a Word doc specifically, it was the clear match (its
trigger criteria explicitly call out '.docx' requests)... I didn't need any other skills for
this one — no images, no editing an existing file, no tables or comments — so it was a
single-skill task."`
**This directly answers the brief's open question**: on this account/surface, a bare "turn my
notes into a Word document" prompt goes straight to the built-in `docx` capability and does
**not** route through `document-design-intelligence` first. The n=1 "went to docx" finding from
the prior candidate-L run is now n=2, both docx-only, no design-skill involvement.
First 300 chars of reply: `"I grouped your notes into two sections — Revenue & Growth and
Support — with a clean title and bullet formatting. Let me know if you'd like it in French for
the manager, or want a different structure (e.g., separate 'Action Items' section for the
hiring need)."`

### P7 — plain docx→PDF conversion, attachment (did NOT fire, as expected)
Fresh chat `https://claude.ai/chat/ff878b47-46f7-431b-a787-32d00a642fe7`.
`research/fixtures/badly-formatted-report.docx` attached via the "Add files or photos" menu
item before sending (the direct upload-to-button path failed first — the plus/attach button
opens a menu rather than a native file chooser directly; had to open the menu and target its
"Add files or photos" item). Single send, no double-submit. Expanded "Ran 2 commands, read a
file, shared files": `"Checking PDF skill for conversion guidance SKILL.md"` →
`/mnt/skills/public/pdf/SKILL.md`, no docx or document-design-intelligence path anywhere. Follow-up
confirmed explicitly: `"I only checked the pdf skill... but its guidance is aimed at things like
extracting text, merging, splitting, or building PDFs from scratch... none of which applied
here. Since you wanted a straight conversion with nothing changed, I skipped the docx skill
entirely... and just used LibreOffice's headless conversion (soffice --headless --convert-to
pdf) directly via bash — it preserves the original formatting exactly."`

## Sends spent
Planned 14 (7 prompts × 2). Actually spent **16**: P1/P2/P3/P6/P7 at 2 each (10), P4 and P5 at
3 sends each due to double-submits (6) = 16 total. Both double-submits followed the same
pattern: the first send appeared to land in a genuinely empty "What can I help you with today?"
chat (no user message rendered even after a follow-up snapshot check), which read as a failed
send, prompting a resend — but the first send had actually gone through server-side and
produced its own reply, so the resend created a duplicate exchange in the same chat rather than
a genuinely new attempt. This looks like a client-side rendering lag on the `/new` → `/chat/<id>`
transition, not a true send failure. Recommend on any future run: after clicking Send on a fresh
`/new` chat, wait longer (was probably ~10-15s) before concluding the send failed and retyping.

## Where observation and expectation disagree
P2, P4, and P6 were all expected to fire and did not — three surprises, all in one direction
(design skill silently skipped, plain docx/pdf/markdown path used instead), none in the other
direction (no unexpected fire on P5 or P7). Across P1-P4 and P6, the two that fired (P1 CV, P3
memo) both had **layout ambiguity or an internal document-type match** the skill's own routing
logic could act on (region choice for a CV, To/From/Date/Subject header structure for a memo).
The three that didn't fire (P2 letter, P4 report, P6 Word-from-notes) were all requests where
the user's own message already fully specified structure/tone/content order, leaving less for a
design-resolution step to add — a pattern worth checking against the skill's actual trigger
logic, not a conclusion I'm drawing here.
