# Corrections to ENS-plugin-rebuild-draft.md — apply BEFORE rebuilding

Reviewed 2026-09-07 by two specialists against (a) the plugin's actual source code
and (b) document-design research. Full detail: research/06-review-ens-rules.md and
research/07-review-ens-mechanism.md. This file is the action list.

Two tiers. Tier 1 items mean the rebuild WILL NOT WORK as drafted. Tier 2 items are
quality fixes. Apply all of Tier 1; apply Tier 2 unless you have a reason not to.

======================================================================
## TIER 1 — the draft will not work without these
======================================================================

### 1.1  The plugin will keep getting skipped — the trigger is in the wrong place
The draft puts the "ENS mandatory workflow" block INSIDE each skill's body.
But the plugin decides whether to activate BEFORE it opens that file, using only
the `description:` line in the YAML frontmatter at the top. The body loads only
AFTER activation. The draft never changes `description:`. So the skipping bug
(2 of 3 documents, plus the invented green on the pagination test) has no reason
to stop.

FIX: rewrite the frontmatter `description:` of every skill to name the concrete
triggers. It must contain, at minimum:
  - the organisation: "ENS", "Eng nei Schaff", "a.s.b.l.", "Bettembourg"
  - every document type: "note interne", "formulaire", "fiche", "affiche",
    "dépliant", "présentation", "post Facebook", "courrier"
  - the framing: "all documents for this organisation must use the ENS brand,
    never generic or default styling"
Keep the body trigger block too — it is good — but it only helps once activation
has already happened.

TEST: ask for a document WITHOUT naming the plugin or saying "ENS brand" —
e.g. just "fais-moi une note interne sur les congés". Check whether the skill fired.

### 1.2  The per-document routing in ui-reasoning.csv is decorative — it never runs
The draft puts all five document-type rules in the `Decision_Rules` JSON column.
Confirmed in source: design_system.py:244 stores that column into the output and
NOTHING ever reads it back or branches on it. It is inert.

FIX: do not rely on it. The real routing is Steps 1–2 of the trigger block (classify
the type, then read ens-document-rules.md). Keep the JSON only as documentation,
and label it as such. Instead fill the columns the code DOES read:
  UI_Category      = exactly the same text as products.csv "Product Type"
  Style_Priority   = "ENS Document Grid + Minimalism & Swiss Style"
Without Style_Priority the style selector falls back to a generic default that
actively biases AWAY from ENS.

### 1.3  Three of the five CSV rows use column names that don't exist
The code looks columns up by exact header text; a wrong name returns blank silently.

  products.csv    "Primary Style"    -> must be "Primary Style Recommendation"
                  "Dashboard Style"  -> must be "Dashboard Style (if applicable)"
  colors.csv      the draft row has NO "Product Type" and NO "Notes" column —
                  and those are the ONLY two columns the colour search reads.
                  As written the ENS colour row is unfindable.
                  -> add Product Type (identical text to products.csv) and a Notes
                     value containing "ENS Eng nei Schaff Bettembourg Luxembourg"
  styles.csv      no "Style ID" or "Parent" column exists; there is no inheritance
                  concept in the data at all.
                  -> put "ENS Document Grid" in "Style Category" (the field that is
                     string-matched); restate anything you wanted to inherit from
                     Swiss Style directly in this row's Keywords / Best For
  typography.csv  "Heading / Body" is two columns: "Heading Font" and "Body Font"
                  "Mood" -> "Mood/Style Keywords"; also fill "Category" (e.g.
                  "Sans + Sans") and "Best For" — both are searched, both blank now

### 1.4  The linking text must be byte-identical across files
products.csv "Product Type", ui-reasoning.csv "UI_Category" and colors.csv
"Product Type" are matched by exact string first. The draft uses an EN DASH in
"ENS – Eng nei Schaff". If any file gets a plain hyphen or different spacing, the
match fails and falls through to the generic default (see 1.2).
FIX: pick one exact string, e.g.  ENS - Eng nei Schaff  (plain hyphen), and paste
it identically into all three files.

### 1.5  "If the result is not ENS, fix the query" is a sentence, not a check
Nothing verifies the search actually returned ENS. The search matches exact
tokens only — no synonyms, no fuzzy match. A query without the literal token
"ens" can return a generic row and the model will proceed with it.
FIX (cheap, worth doing): wrap the search in a tiny script that greps its own
output for "ENS" and prints a loud  [NO ENS MATCH]  marker if absent. This is the
same hard-fail pattern the plugin's own html-token-validator.py already uses.

### 1.6  Output formats that are not yet confirmed
The draft targets .docx for note-interne and .pptx for slides. Whether the
python-docx / python-pptx libraries exist in this environment has NOT been
tested yet. Run:  import docx; import pptx  — and report. If either is missing,
that type's output format changes to PDF (which is confirmed working via WeasyPrint).

======================================================================
## TIER 2 — quality fixes from the design review
======================================================================

### 2.1  Legal text on forms: 7.4pt UPPERCASE — most severe design finding
Smallest size in the scale + sustained all-caps (loses word shape) + must survive
photocopying, on the one text that legally must not be misread.
FIX: mixed case, and 8–8.5pt minimum.

### 2.2  Note-interne body lines are too long
10pt Arial across a 160mm text block (A4 minus 25mm margins) = roughly 85–95
characters per line. Readable range is 45–75.
FIX: either narrow the text measure to about 130mm (e.g. a wider right margin or
a side column), or raise body to 12pt. Pick one and state it in the rules.

### 2.3  Section numbers on forms should be black, not green
Green #1F6F43 photocopies as mid-grey. At 7.5pt that degrades fast across copy
generations — directly against the draft's own "must photocopy cleanly" rule.
FIX: black section numbers; keep green for the rule lines only.

### 2.4  Slides: 18–20pt body is the floor, not the default
24pt is the general floor for projected body text; 18pt is for dense data
callouts only.
FIX: default body 24pt+; allow 18–20pt only on explicitly data-dense slides.

### 2.5  PPTX font embedding is not mentioned anywhere
The font rule covers PDF/HTML (embed) and Word/Excel (Arial) but PPTX is in
neither bucket — and PPTX is the format where missing embedding causes silent
font substitution on the recipient's machine. Manrope and Inter are OFL-licensed,
so embedding is permitted.
FIX: add to type D: "font embedding ON for every PPTX export, verified not assumed."

### 2.6  Lime as text fails contrast everywhere
Computed L* for #9ACD32: fails against white AND against the dark green. The
draft's "never body text" is right; extend it to "never as text at all".
If a highlight is wanted, use a FILLED lime badge with dark text on top (as the
social kicker already does).

### 2.7  Small labels at 7.5pt
Not a hard violation, but the draft's own products row says many readers are
non-native French speakers. 7.5pt labels raise reading effort exactly where it
should be lowest. Consider 8.5pt.

### 2.8  Hand-typed "On Primary / On Accent" colours are unchecked
Normally these are derived by code for guaranteed contrast. Hand-typed, nobody
checks them. Verify Accent-on-background and On-Accent manually (WCAG 4.5:1
body / 3:1 large). Also: if _sync_all.py is ever re-run, the ENS colour row can
be silently discarded unless its Product Type text is byte-identical.

======================================================================
## [À valider] — answered by the reviews where research applies
======================================================================
  #2  Lime in internal docs   -> NEVER as text (fails contrast). Filled badge only.
  #3  Word fonts              -> Arial. Confirmed lower-risk; installing fonts
                                 fleet-wide is a permanent IT dependency.
  #6  Affiche A3              -> adding it pulls in a whole print-production
                                 section (3mm bleed, safe trim, CMYK, 300 DPI)
                                 that none of the current five types need.
                                 Decide it deliberately, not as an afterthought.
  #1 brown, #4 underlines vs boxes, #5 square vs portrait -> ENS preference; no
     research basis either way. Yours to answer.
