# Activation design

Supports the `description` field now live in `SKILL.md`'s frontmatter. Per
`research/04-packaging.md`, that field is the only activation lever — this
file documents why it's shaped the way it is, records the now-resolved
200-vs-1,024-character cap question, sketches the router body's structure for
whoever writes it once the schema lands, and gives a test list to run after
upload.

**RESOLVED (tested directly against the claude.ai upload UI): the limit is
1,024 characters, not 200.** The UI's own validation message reads
"Description must be under 1024 characters" — note "under," so the practical
maximum is 1,023, not 1,024 itself. The 200-character figure came from a
support-article summary (`research/04-packaging.md` §5) and does not hold on
this surface. The 831-character primary description below ships as-is, with
no truncation risk. The three alternates further down were built against the
truncation contingency and are **retained for reference only — not needed**
now that the cap is confirmed at 1,024.

## The description as shipped

```
Creates and fixes print/office documents: CVs, resumes, cover letters,
brochures, flyers, posters, reports, whitepapers, slide decks, presentations,
forms, letters, quotes, offers; also note interne, fiche, courrier, affiche,
dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht. Triggers:
make me a CV, write a note interne, turn this into a brochure, I need slides
for Monday, format this report, fais-moi une fiche, erstelle ein Angebot;
appearance fixes: looks like AI, looks generic, make it look professional,
fix the layout. Applies sourced layout, typography, color, print, and ATS
rules.
When a specific file format (Word, PowerPoint, .docx, .pptx) is named for a
plain conversion or edit with no design ask, use that format's own skill
instead. Not for web or app UI/UX design (use UI/UX Pro Max for screens).
```

**Length: 831 characters** (well under the confirmed 1,024-character ceiling —
resolved above; no truncation risk in practice). Grew from 667 to 831 with
the addition of the built-in-skill deferral sentence — see
`research/24-builtin-alignment.md` item 1 for why: Anthropic's own `docx` and
`pptx` skills each carry a clause deferring to "a dedicated document/slide
skill" when the user doesn't name a file format — that dedicated skill is
supposed to be us, and the boundary needs to hold in both directions. Neither
".docx" nor ".pptx" appears anywhere in our own trigger list, by design —
those filename mentions belong to the built-ins, not to us; naming them here
would blur the exact boundary this sentence exists to draw.

**Scope note**: the skill fixes how a document looks, not how its prose
reads; AI-sounding wording is out of scope for v0.1.0.

**First 200 characters** (kept below for reference — this analysis drove the
alternates while the cap was still disputed, but no longer gates a real risk
now that 1,024 is confirmed):

```
Creates and fixes print/office documents: CVs, resumes, cover letters,
brochures, flyers, posters, reports, whitepapers, slide decks, presentations,
forms, letters, quotes, offers; also note interne,
```

**What survives a 200-char cut**: every English document-type noun (CVs,
resumes, cover letters, brochures, flyers, posters, reports, whitepapers,
slide decks, presentations, forms, letters, quotes, offers) and one complete
French trigger (`note interne`) — the cut lands cleanly after a comma, not
mid-word.

**What would have been lost if cut at 200**: `fiche`, `courrier`, `affiche`,
`dépliant`, `présentation`, `formulaire`, `Lebenslauf`, `Angebot`, `Bericht`,
every quoted example trigger phrase, both quality-complaint keywords, the
built-in-skill deferral sentence (added later, see above), and the UI/UX Pro
Max boundary statement. Moot now that the cap is confirmed at 1,024 —
recorded here only so the reasoning isn't lost if a future UI change ever
reintroduces a shorter cap.

Design choices, stated so they can be revisited: third person throughout, no
first/second person voice (per Anthropic's own guidance — quoted trigger
phrases are the *user's* words, not the skill's); comma-dense keyword-list
style copying upstream's pattern (`research/04-packaging.md` §2) rather than
full prose, to maximize triggers per character; document nouns ordered
highest-frequency-English first, then the pilot's French/German nouns, then
example phrases, then the exclusion boundary last (accepting that the
boundary is what's most at risk under truncation — see the three alternates
below, one of which reorders specifically to protect it).

## Three alternates (~500 characters) — retained for reference, not needed

The 200-char cap these were built against does not exist on claude.ai
(confirmed 1,024-char limit, see the RESOLVED note above). None of these are
needed for the current description. Kept here in case a future platform
change reintroduces a shorter cap, or a different surface (Claude Code,
API-uploaded custom Skills) turns out to enforce one.

Each reorders priority differently. Test 4 (below) has since run and found no
200-char cutoff, so none of these are in play — kept as-is for the "if a cap
ever comes back" case described above.

### Alternate A — English document nouns first

```
Creates and fixes print/office documents: CVs, resumes, cover letters,
brochures, flyers, posters, reports, whitepapers, slide decks, presentations,
forms, letters, quotes, offers. Also: note interne, fiche, courrier, affiche,
dépliant, présentation, formulaire, Lebenslauf, Angebot, Bericht. Fires on
'make me a CV', 'I need slides for Monday', 'format this report', and quality
complaints such as 'this looks like AI', 'looks generic', 'make it
professional'. Not for web or app UI/UX design (use UI/UX Pro Max for
screens).
```

Length: 526. First 200: identical English noun list as the primary, cut
mid-way through "brochures, flyers, posters, reports, whitepapers, slide
decks, presentations, forms, letters, quotes, offers. Also: note int—" — loses
the French/German cluster and everything after. **Use this alternate only if
English-only document requests are confirmed as the overwhelming majority of
real traffic** and the pilot's French/German need turns out smaller than
assumed — otherwise it's strictly worse than the primary for this project.

### Alternate B — multilingual nouns first

```
Handles CVs, note interne, fiche, courrier, affiche, dépliant, présentation,
formulaire, Lebenslauf, Angebot, Bericht, and other print/office documents:
resumes, cover letters, brochures, flyers, posters, reports, whitepapers,
slide decks, presentations, forms, letters, quotes. Fires on 'fais-moi une
fiche', 'erstelle ein Angebot', 'make me a CV', 'write a note interne', and
quality complaints ('looks like AI', 'make it professional', 'fix the
layout'). Not for web/app UI design (use UI/UX Pro Max).
```

Length: 504. First 200: covers CVs plus **all ten** required multilingual
nouns (note interne, fiche, courrier, affiche, dépliant, présentation,
formulaire, Lebenslauf, Angebot, Bericht) intact, cutting off partway into the
English "and other print/office documents: resumes, cover letters, brochures,
flyers, post—" list. **Use this alternate if the ENS pilot (French-first) is
the dominant near-term user and English coverage can lean on the model's own
general document knowledge** — the tradeoff this alternate makes explicitly.

### Alternate C — quality complaints and UI/UX boundary first

```
Fixes documents that look AI-generated, generic, or unprofessional (bad
layout, typography, color, or print-readiness) and creates new ones on
request: CVs, resumes, cover letters, brochures, flyers, posters, reports,
whitepapers, slide decks, presentations, forms, letters, quotes; also note
interne, fiche, courrier, affiche, dépliant, présentation, formulaire,
Lebenslauf, Angebot, Bericht. Applies a validated document-design library, not
free-form styling. Not for web or app UI/UX design, use UI/UX Pro Max for
screens.
```

Length: 528. First 200: covers the quality-complaint framing ("look
AI-generated, generic, or unprofessional — bad layout, typography, color, or
print-readiness") and the opening of the document-type list (CVs, resumes,
cover letters, brochures, flyers), cutting before French/German and before
the boundary statement (which, despite being this variant's namesake
priority, still doesn't survive a 200-char cut — there simply isn't room for
everything). **Use this alternate if activation testing shows the model
already infers document-type triggers reliably from general knowledge, but
under-fires specifically on vague quality complaints** ("this looks bad",
"fix this") — the actual gap this ordering is built to close.

**Historical note**: no ordering fit document nouns in three languages, four
complaint phrases, and an exclusion boundary into 200 characters as readable
prose — that was a real trade-off at the time, not a solved problem. Test 4
has since confirmed the 200-char cap doesn't exist on claude.ai, so this
trade-off no longer applies to the shipped description; recorded here in case
it becomes relevant again on a different surface.

## SKILL.md body structure (headings + one-line intent — not the prose)

The body content waits on `research/09-library-schema.md`'s tables landing in
`data/base/`. This is the structure whoever writes it should follow, per
Anthropic's progressive-disclosure guidance (`research/04-packaging.md` §1.2:
body loads only on activation, keep it under ~500 lines, link to
`references/` one level deep, scripts run via bash with only stdout entering
context):

```
# Document Design Intelligence

## When to Apply
  Must Use / Recommended / Skip triad (mirrors upstream's own structure,
  research/04-packaging.md §1.1), naming real doctype categories once
  data/base/doctypes.csv exists instead of the generic list in the
  frontmatter description.

## Mandatory Workflow
  States the six-step pipeline as non-skippable — this section exists
  specifically because the ENS pilot skipped the plugin entirely on two of
  three deliverables (research/05-SYNTHESIS.md field evidence). Low-freedom,
  "run exactly this" phrasing per Anthropic's authoring guidance, not a
  suggestion.

  ### 1. Classify the doctype
    One line: how the user's request maps to a doc_key (research/09-library-
    schema.md T1) — the only fuzzy step in the chain.

  ### 2. Resolve
    One line: run scripts/resolve.py with the classified doctype (and active
    brand, if any); it prints the resolved key set, never raw table rows.

  ### 3. Validate (preflight)
    One line: the resolver's own preflight validators (brand resolution,
    render-engine availability, print-mode coherence, font resolution — 09-
    library-schema.md §4 items 5-8) must pass before rendering starts.

  ### 4. Render by handoff
    One line: for .docx/.pptx targets, hand the resolved decision to the
    docx/pptx built-in skills as renderers (docx-js / pptxgenjs respectively)
    rather than reimplementing OOXML generation — adopted from studying
    Anthropic's own docx/pptx SKILL.md files, research/24-builtin-alignment.md
    item 3. PDF is the one target NOT handed off: this skill's own HTML to
    Chromium/WeasyPrint pipeline is the native, primary path there.

  ### 5. Preflight
    One line: scripts/preflight.py runs against the actual rendered artifact
    (post-render validators, §4 items 9-28); on refuse, fix the specific
    problem named and rerun step 4 — do not return a refused artifact.

  ### 6. Report
    One line: pass/fail state from preflight is what gets reported back to
    the user — not a claim the model makes unchecked.

## Dependencies
  New section, adopted directly from Anthropic's own docx/pdf/pptx/xlsx
  SKILL.md files, each of which declares one (research/24-builtin-alignment.md
  item 2) — ours: Python stdlib only for resolution/validation/merge;
  Chromium at /opt/google/chrome/chrome (preinstalled, primary PDF renderer,
  research/05-SYNTHESIS.md's PDF-engine finding); optional `pip install
  "weasyprint>=67"` as a secondary PDF renderer (network-dependent, never a
  hard dependency); the docx and pptx built-in skills as renderers for those
  two output formats specifically (see Render Handoff above) — not a Python
  package, a co-installed skill this one calls into.

## Brand Rule
  One line: if data/brand/active.json names a brand, resolution failing to
  return a brand-scoped row is a hard refusal, not a silent fallback to
  generic with a note to "remember to apply the brand" — that pattern is
  exactly the ENS failure mode (research/09-library-schema.md §0.3).

## Output Tiers
  One line, stated as three honest promise levels, not one: shop-submittable
  RGB PDF is the default and always available; PDF/X-4 only when a real CMYK
  path (e.g. WeasyPrint) is actually installed in the current session; press-
  ready output is never promised (research/09-library-schema.md §7 Q2 — no
  sourced CMYK+bleed path exists yet).

## Setting Up Your Brand
  One line: pointer to the brand-kit workflow, linked one level deep to
  references/brand-workflow.md (build_brand_kit.py / merge_brand_kit.py) —
  not inlined, per the "keep references one level deep" anti-pattern rule.
  That reference file must state the confirmed reality, not the original
  assumption: nothing written during a chat persists to a new chat (confirmed
  by direct test, not the T3-by-analogy guess this design started from), and
  chat attachments live at a fixed path outside this script's working
  directory, not wherever Claude happens to be running from (confirmed by
  direct test). It must also state the further field evidence that arrived
  after the above: the base skill itself is already live-mounted wherever
  claude.ai puts an active skill's files, so merge_brand_kit.py auto-detects
  and zips that live directory as the base — the user attaches only their
  saved `my-brand-kit.zip`, not the base skill zip too. Attaching a base zip
  explicitly (via -b/--base) is the fallback path, only needed if
  auto-detection ever fails. See README.md, "Updating to a new version," for
  the resulting single-attachment flow this drives, and the script's own
  docstring (BASE AUTO-DETECTION section) for exactly how detection works and
  what it falls back to.

## References
  One-line index of what lives in references/ instead of inline, each a
  direct link from here (never nested further): resolution-flow.md,
  print-production.md, ats-rules.md, brand-workflow.md, and (new, once
  resolve.py's output shape is known) render-handoff.md — the unit/vocabulary
  conversions the resolved-decision block needs for docx/pptx handoff
  (DXA vs. mm, hex-without-# for pptxgenjs, etc. — see
  research/24-builtin-alignment.md item 3 for the full list as change
  requests against the not-yet-built resolver).

## Attribution
  One line: pointer to NOTICE.md.
```

## 13-prompt activation test (run after uploading the skill)

Five should fire the skill; five should not, including two that belong to
UI/UX Pro Max specifically (both skills co-installed, per the task). A
further three (added after studying Anthropic's own docx/pptx SKILL.md files,
research/24-builtin-alignment.md item 1) specifically test the deferral
boundary in both directions against the built-in docx/pptx skills. For each:
paste the prompt into a fresh chat with this skill, docx, and pptx all
enabled, and check which skill (if any) responds using its specialized
behavior versus answering as a generalist.

### Should fire

1. "Can you make me a CV for a marketing coordinator role?"
   **Pass**: the skill activates and asks about content/format instead of
   just writing generic CV prose. **Fail**: a plain-prose CV comes back with
   no layout/library reasoning visible.
2. "J'ai besoin d'une fiche produit pour lundi : nouveau vélo électrique
   "Modèle X500", autonomie 80 km, moteur 250W, prix 1490 euros, disponible
   en trois coloris. Tu peux me la faire ?"
   **Pass**: activates on the French content alone, no English document word
   present, and either produces a designed fiche or asks a clarifying
   question framed around format, layout, page count, or branding. **Fail**:
   Claude treats this as a generic writing request, or asks a clarifying
   question with no document-design framing.
3. "Erstelle mir ein Angebot für diesen Kunden: Kunde ist die Müller GmbH,
   Ansprechpartner Herr Weber. Es geht um 50 Bürostühle und 10
   Schreibtische, Lieferung bis Ende Oktober, Gesamtpreis 12500 Euro netto."
   **Pass**: activates on the German content alone and either produces a
   structured Angebot or asks a clarifying question framed around format,
   layout, page count, or branding. **Fail**: generic response with no
   document-structure reasoning, or a clarifying question that isn't framed
   around document design.
4. Attach research/fixtures/badly-formatted-report.docx before sending.
   "This report looks like it was thrown together by AI, can you fix it?"
   **Pass**: the skill fires and reasons about hierarchy, typography,
   margins or colour. **Fail**: generic advice. **Fail** also if it asks
   for the file — the file is attached, so asking for it is exactly the
   failure this revision tests for.
5. "Sunrise Yoga Studio offers classes for all levels, from beginner to
   advanced. We have five instructors with over ten years of combined
   experience. Classes run Monday through Saturday, morning and evening
   sessions. We also offer private sessions and a monthly membership plan.
   New members get their first class free. Our studio is located downtown,
   two blocks from the train station. Turn this text into a two-page
   brochure."
   **Pass**: activates and asks about brand, layout, page count, or print,
   or produces a two-page design with visible layout reasoning. **Fail**:
   produces a plain reformatted text block with no design reasoning, or
   asks a clarifying question with no document-design framing.

### Should not fire

6. "My dashboard sidebar has Home, Reports, Settings, and Billing as nav
   items, but users keep missing Billing because it's buried below a
   scroll. Redesign this dashboard's sidebar navigation for better UX."
   **Pass** (correct boundary): UI/UX Pro Max activates instead, or neither
   activates generically. Asking for the file with no skill named also
   counts as a pass, but it's weak evidence — that's why the complaint is
   now inline; a test with content is the stronger signal. **Fail**: this
   skill activates on a screen-UI request — the boundary statement didn't
   hold.
7. "What color palette should I use for my SaaS landing page hero section?"
   **Pass**: same boundary check as #6, web UI territory.
   **Fail**: this skill answers instead of UI/UX Pro Max.
8. "Can you refactor this Python function to run faster?
   ```python
   def find_duplicates(items):
       duplicates = []
       for i in range(len(items)):
           for j in range(len(items)):
               if i != j and items[i] == items[j] and items[i] not in duplicates:
                   duplicates.append(items[i])
       return duplicates
   ```"
   **Pass**: neither skill activates — unrelated to either domain. Asking
   for the file with no skill named also counts as a pass, but it's weak
   evidence — that's why the function is now inline; a test with content is
   the stronger signal. **Fail**: this skill activates on an unrelated
   coding task.
9. "What's a good marketing strategy for launching my app next quarter?"
   **Pass**: neither skill activates — strategy, not document or UI design.
   **Fail**: either skill claims this request.
10. "Summarize this PDF research paper for me in three bullet points:
    'Prior work on sidebar navigation has focused on discoverability
    metrics in isolation, without accounting for task frequency. We
    present a longitudinal study of 40 enterprise dashboards showing that
    reordering nav items by usage frequency reduces mis-clicks by 23%
    on average, with the largest gains in sidebars exceeding six items.'"
    **Pass**: neither skill activates — this is summarization, not document
    creation or a quality complaint, despite mentioning "PDF". Asking for
    the file with no skill named also counts as a pass, but it's weak
    evidence — that's why the abstract is now inline; a test with content
    is the stronger signal. **Fail**: this skill activates on the
    file-format mention alone, with no create/fix verb attached — the
    sharpest test of over-triggering on a bare noun.

### Handoff tests (built-in docx/pptx boundary, both directions)

11. "Here are my rough notes:
    - Q3 revenue up 12% vs Q2
    - New enterprise client signed: Bramwell Logistics
    - Support ticket backlog down from 340 to 190
    - Need to hire 2 more support reps by Q4
    - Churn rate flat at 4.1%
    Turn my rough notes into a Word document."
    **Pass**: the `docx` skill activates (file format named explicitly,
    matches its own trigger list) — this skill stays silent. Asking for
    the file with no skill named also counts as a pass, but it's weak
    evidence — that's why the notes are now inline; a test with content is
    the stronger signal. **Fail**: this skill activates instead of, or
    alongside, `docx` — the boundary sentence didn't hold in the direction
    that protects the built-ins from us.
12. "I need a two-page CV, make it look professional. I'm Sara Lindqvist, 8 years as a
    supply-chain analyst at Nordica Freight, before that 3 years as a logistics coordinator at
    Baltic Rail; MSc Logistics, Gothenburg; fluent Swedish, English, German; Excel, SAP,
    Power BI."
    **Pass**: this skill activates (no file format named, explicit design/
    quality intent) and, per the Render Handoff workflow step, produces its
    output *by calling* the `docx` skill's approach internally — `docx` does
    not activate on its own as the top-level responder. Asking for the CV
    with no skill named also counts as a pass, but it's weak evidence —
    that's why the content is now inline; a test with content is the
    stronger signal. **Fail**: `docx` activates directly and this skill
    never engages, or this skill engages but reimplements OOXML generation
    itself instead of handing off.
13. Attach any short .docx you have (one page is enough) before sending.
    "Just convert this .docx file to a PDF, don't change anything."
    **Pass**: `docx`/`pdf` handle this directly (file format named, purely
    mechanical conversion, no design ask) — this skill stays silent. Asking
    for the file with no skill named also counts as a pass, but it's weak
    evidence — that's why this test now needs a real attachment; a test
    with content is the stronger signal. **Fail**: this skill activates on
    a plain format-conversion request it has no reason to touch.
