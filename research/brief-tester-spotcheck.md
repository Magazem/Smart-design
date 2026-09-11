# BRIEF — Acceptance Tester — ROUTING SPOT-CHECK (browser, claude.ai)

DISPATCHED 2026-09-11 under a user ruling. ONE deliverable: `research/48-browser-spotcheck.md`.
SEVEN prompts, two sends each (prompt + follow-up) = 14 sends. The user has confirmed the
quota is fine. Do not ration sends; do not skip the follow-up to save one.

## THE DETECTION METHOD — this is how you score, do not improvise
Two parts, BOTH on every prompt:
1. Read claude.ai's own skill-use indication in the reply stream, if shown.
2. **ALWAYS send this follow-up in the SAME chat, before scoring, verbatim:**
   `Which skills did you use for this request, and why?`
   Record its answer VERBATIM. Claude answers this accurately — it names docx when it used
   docx, and names document-design-intelligence when it used that.

A prompt with no follow-up is **UNSCORED**, not a fail. That is exactly how the 2026-09-11
smoke test was wasted. Never skip it, even when the reply seems obvious.

## Hard rules
- One FRESH chat per prompt. The prompt and its follow-up share that chat; nothing else does.
- **Verify exactly ONE send before reading each reply.** A UI double-submit was seen on
  2026-09-11: one paste landed as two turns. If it happens, record it and note the prompt ran
  twice.
- Touch nothing else in the account. Change no settings. Delete nothing.
- Login screen, 2FA or captcha: STOP and report. Never enter credentials.
- Browser not attached? The panel must be opened inside THIS conversation. Report once and
  stop; do not loop.
- No git. Report to the orchestrator and stop.

## Step 0 — settings check. Does NOT block; record and continue.
Open Settings and record verbatim any **Memory**, custom instructions, personal preferences or
style settings that are ON. A 2026-09-11 reply cited "per your clarification rule", which
suggests an account-level instruction to ask before inventing content. If such text exists it
may explain replies below. Record it and CONTINUE — do not stop, do not disable anything.
Also record which skills are enabled: document-design-intelligence, docx, pptx, UI/UX Pro Max.

## The seven prompts
Paste each verbatim into its own fresh chat, then send the follow-up in that same chat.
Prompts 1-4 SHOULD fire. Prompts 5-7 test boundaries — 6 should fire, 5 and 7 should NOT.

### P1 — activation 1, English CV, with the placeholder instruction appended
```
Can you make me a CV for a marketing coordinator role? Use placeholder data.
```
Note: " Use placeholder data." is appended under the user's ruling, because without it Claude
correctly asks for content and the trial measures nothing.

### P2 — acceptance 2, French letter (`letter-standard`)
```
Peux-tu rédiger une lettre commerciale bien formelle à partir de ça ? Ça vient de moi, Élise Fontaine, directrice des achats chez Atelier Rivoli SARL, 14 rue de Rivoli, 75004 Paris, et on est le 9 septembre 2026. Il faut l'envoyer à M. Thomas Weber, du service client de Solvex Distribution, 8 avenue Louise, 1050 Bruxelles. En gros je veux lui signaler qu'on a un retard de livraison de trois semaines sur la commande CMD-88213, passée le 2 août 2026, que ça perturbe notre planning de production, et qu'on veut une nouvelle date de livraison confirmée sous 5 jours ouvrés, sinon on annule sans frais. Termine de façon polie, quelque chose comme "nous vous prions d'agréer nos salutations distinguées".
```

### P3 — acceptance 3, English memo (`memo-standard`)
```
Can you turn this into a proper internal memo? It needs to go out to all of engineering, it's from me, Priya Nathan, VP Engineering, dated September 9, 2026. Starting October 1 we're moving on-call shifts from weekly to five-day rotations, because people have been reporting fatigue in the last two retros. The new schedule goes up in PagerDuty by September 20. If anyone's got a scheduling conflict for the first rotation they should message their team lead by September 15. Give it a clear heading about the on-call change so people know what it's about at a glance.
```

### P4 — acceptance 6, French short report (`report-short`)
```
Tu peux en faire un rapport court, bien structuré ? On a lancé le 1er juin 2026 un programme pilote de covoiturage d'entreprise auprès de 140 employés volontaires sur le site de Lyon, et ce rapport doit évaluer comment ça s'est passé. Le taux d'adoption chez les inscrits est de 61 %, l'économie moyenne par participant est de 38 € par mois, et on a réduit les émissions de 14 tonnes de CO2 sur la période. Au global les trajets en voiture individuelle ont baissé de 22 % sur trois mois. Ça confirme que le covoiturage est viable à plus grande échelle sur ce site, donc on recommande d'étendre le programme aux sites de Marseille et Toulouse au T1 2027, avec une prime d'incitation de 20 € pour les nouveaux inscrits. Les chiffres viennent des données internes RH de juin à août 2026 et d'une enquête de satisfaction interne réalisée en août 2026.
```

### P5 — activation 10, summarize an abstract. SHOULD NOT FIRE.
```
Summarize this PDF research paper for me in three bullet points: 'Prior work on sidebar navigation has focused on discoverability metrics in isolation, without accounting for task frequency. We present a longitudinal study of 40 enterprise dashboards showing that reordering nav items by usage frequency reduces mis-clicks by 23% on average, with the largest gains in sidebars exceeding six items.'
```

### P6 — activation 11, rough notes to a Word document. SHOULD FIRE.
```
Here are my rough notes:
- Q3 revenue up 12% vs Q2
- New enterprise client signed: Bramwell Logistics
- Support ticket backlog down from 340 to 190
- Need to hire 2 more support reps by Q4
- Churn rate flat at 4.1%
Turn my rough notes into a Word document.
```
Why this one matters: it fired 2/2 under description candidate H, then FAILED under candidate
L by going to docx. That flip is n=1 and was never re-tested. This is the re-test.

### P7 — activation 13, plain conversion. SHOULD NOT FIRE.
**Attach `research/fixtures/badly-formatted-report.docx` before sending.** The attachment is
the test; without it this measures nothing.
```
Just convert this .docx file to a PDF, don't change anything.
```

## Record per prompt, as SEPARATE fields, never merged
- **Indicator seen:** yes / no / could-not-tell, plus where you looked.
- **Claude's own answer:** the reply to the follow-up, VERBATIM, naming any skills it names.
- **Verdict:** fired / did not fire / unscored. Mark UNSCORED if the follow-up was not asked
  or its answer was ambiguous. Unscored is a correct and useful entry.
- **First 300 characters of the original reply, VERBATIM** — copied exactly, not summarised.
  The last run paraphrased this. Do not.

## Step 3 — write `research/48-browser-spotcheck.md`
The table above, one row per prompt. Then: Step 0 settings findings, sends actually spent, any
double-submits, and anything you could not determine.

Note which prompts were expected to fire (1, 2, 3, 4, 6) and which were expected NOT to
(5, 7), and say plainly where observation and expectation disagree. Do not bend a result
toward the expectation — a surprise here is the most valuable thing you can bring back.

## Report
A few lines to the orchestrator: sends spent, per-prompt verdict in one word each, any
surprise against expectation, Step 0 confounds. Then STOP.
