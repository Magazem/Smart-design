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
