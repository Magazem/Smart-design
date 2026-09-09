# ENS plugin rebuild — draft for approval

Three parts: **(1)** ENS entries in the plugin's library so its search returns ENS instead of generic results; **(2)** the trigger/instruction block at the top of every skill; **(3)** per-document rules so nothing is improvised. Points marked **[À valider]** are decisions I need from you.

---

## 1. ENS in the library

The plugin's search runs over five CSV tables. I add one ENS row to each, keyed on the same words so a query like `ENS note interne` or `Eng nei Schaff formulaire` resolves to ENS on every table.

**Match keywords (all tables):** `ens, eng nei schaff, engneischaff, bettembourg, luxembourg, recyclage, jardinage, bricolage, transport, asbl, fse`

### products.csv — new row
| Field | Value |
|---|---|
| Product Type | ENS – Eng nei Schaff |
| Keywords | ens, eng nei schaff, engneischaff, bettembourg, recyclage, jardinage, bricolage, transport, asbl, fse, note interne, fiche, formulaire, affiche, facebook |
| Primary Style | ENS Document Grid (see styles row) |
| Secondary Styles | Minimalism & Swiss Style, Flat Design |
| Landing Page Pattern | Trust & Authority (services + contact) |
| Dashboard Style | Data-Dense, light mode only |
| Color Palette Focus | Forest green structure + earth brown secondary, lime accent (marketing only) |
| Key Considerations | Printed documents filled by hand; many readers are non-native French speakers → short words, clear hierarchy; FSE+ co-financing elements are mandatory on funded-project material |

### colors.csv — new row
| Role | Hex | Role | Hex |
|---|---|---|---|
| Primary | #1F6F43 | On Primary | #FFFFFF |
| Secondary | #8B5E3C | On Secondary | #FFFFFF |
| Accent | #9ACD32 | On Accent | #1E2A23 |
| Background | #F7F8F5 | Foreground | #1E2A23 |
| Card | #FFFFFF | Card Foreground | #1E2A23 |
| Muted | #DCE8DF | Muted Foreground | #5B665F |
| Border | #D5DBD6 | Ring | #1F6F43 |
| Destructive | #B4261F | On Destructive | #FFFFFF |

Notes: *Green = structure and primary emphasis. Brown = secondary emphasis and category labels. Lime = marketing accent only, never body text, never in internal documents.*

### typography.csv — new row
| Field | Value |
|---|---|
| Pairing name | ENS Manrope / Inter |
| Heading / Body | Manrope 700–800 / Inter 400–600 |
| Fallback (Word, no embedded fonts) | Arial / Arial |
| Mood | reliable, clear, down-to-earth, functional |
| Notes | Use Manrope/Inter whenever fonts are embedded (PDF, HTML, images). Use Arial in editable Word/Excel files so they open identically on any office PC. Never mix the two in one document. |

### styles.csv — new style "ENS Document Grid"
| Field | Value |
|---|---|
| Style ID | ens-document-grid |
| Parent | minimalism-and-swiss-style |
| Keywords | grid, hairline rules, single accent, no fills, print-friendly, hand-fillable, uppercase tracked labels |
| Effects | none (print) |
| Best For | ENS internal notes, forms, fiches, letters, tables, internal web tools |
| Do Not Use For | Social posts and banners (use ENS Marketing rules instead) |
| Design System Variables | --radius: 0; --shadow: none; --rule-hair: 0.5pt #B9C4BC; --rule-strong: 1pt #1E2A23; --rule-brand: 1.6pt #1F6F43; --space: 4mm grid |
| Checklist | ☐ One green rule under the title ☐ Section labels uppercase 7.5pt tracked ☐ Tables: hairlines only, no zebra, no fills ☐ Fields: underline, 6mm tall ☐ Footer: address line + page x/y ☐ No rounded boxes, no badges, no icons unless functional |

### ui-reasoning.csv — new row
Decision rules encode the per-document routing:
```
{"if_internal_note":["style:ens-document-grid","constraint:no-lime","constraint:arial-if-docx"],
 "if_form":["style:ens-document-grid","constraint:hand-fillable","constraint:keep-all-fields"],
 "if_social":["style:ens-marketing","constraint:lime-accent-ok","constraint:fse-block-if-funded"],
 "if_slides":["style:ens-document-grid","constraint:one-idea-per-slide"],
 "if_web_tool":["style:ens-document-grid","constraint:light-mode-only"]}
```
Anti-patterns: *decorative fills, colored badges, rounded cards in documents, three accent colors on one page, emoji, gradients, navy/blue palettes.*

---

## 2. Trigger block (replaces the current "Company Defaults" paragraph in all 7 skills)

> ### ENS – mandatory workflow
> This plugin is customised for **ENS – Eng nei Schaff a.s.b.l.** (Bettembourg, Luxembourg). Every design task follows these steps in order; do not skip to building.
>
> 1. **Classify the deliverable** into exactly one type: `note-interne`, `formulaire`, `social`, `slides`, `web-tool`. If unclear, ask the user which one.
> 2. **Read the rules for that type** in `brand/references/ens-document-rules.md` — they are fixed decisions, not suggestions.
> 3. **Run the search prefixed with ENS** — e.g. `search.py "ENS formulaire" --design-system`. The library contains ENS entries; if the result is not ENS, the query is wrong — fix the query, do not use a generic palette.
> 4. **Build** using only the ENS palette roles (green structure / brown secondary / lime marketing-only), the font rule for the output format (Manrope+Inter embedded, Arial in Word/Excel), and the type's layout template.
> 5. **Verify** against the type's checklist and render the result before delivering. State which rules file and which search were used.
>
> Never: pick a style from the generic library over the ENS rules; drop a brand color because a generic style says "single accent"; change content, fields or legal text of a document being redesigned; use emoji, gradients, navy/blue.
> Only deviate when the user names another brand or explicitly overrides a rule for this task.

---

## 3. Per-document rules (`ens-document-rules.md`)

### Global (all types)
- **Language:** French, « vous », guillemets « », non-breaking space before : ; ! ?
- **Palette roles:** Green #1F6F43 = titles rule, primary buttons/CTAs, key numbers. Brown #8B5E3C = secondary labels, category markers, second-level emphasis. Lime #9ACD32 = highlight badges/CTAs in marketing only. Text #1E2A23, muted #5B665F, hairline #B9C4BC.
- **Type scale (pt):** 7.5 label · 8 caption · 10 body · 12 lead · 16 H3 · 24 H1 (documents) — social/slides use their own scale below.
- **Logo:** always the original colourful ENS logo, never recoloured; min 15mm high on A4, on white only.
- **Footer on every printed page:** `Eng nei Schaff a.s.b.l. · 144, Z.A.E. Wolser A · L-3225 Bettembourg · Tél. 00352 54 66 70` + `Page x / y`.
- **Redesign jobs:** content, field numbering, legal text and figures are preserved verbatim; only obvious typos may be fixed and must be listed to the user.

### A. `note-interne` (notes, memos, letters, lists) — output: **.docx** (+ PDF copy)
- A4, margins 25 mm sides / 20 mm top-bottom. Font Arial (Word).
- Header line: logo left (17 mm) · document kind centred (« Note interne ») · date right, all 8.5pt muted.
- Title 32pt bold, subtitle 11pt muted, then **one 1.6pt green rule**. Nothing else coloured above the fold.
- Tables: uppercase tracked column labels, 1pt dark rule under header, 0.5pt hairlines between rows, **no fills, no zebra**. Emphasised rows: bold + green text, not background.
- Explanatory remarks in a separate column, never appended in parentheses to the main value.
- Numbered remarks: green number + tab, no bullets, no boxes, no left borders.
- Sign-off: role bold, company muted. No signature image.
- **Brown:** used for a secondary category label if the table has two kinds of rows **[À valider — e.g. brown for "report du …" holidays vs green for "fermeture collective"]**.

### B. `formulaire` (fiches, forms filled by hand) — output: **PDF** (fonts embedded, Manrope/Inter)
- A4, margins 16 mm sides / 12 mm top-bottom, 4 mm vertical grid.
- Header: logo left, company block right (8pt muted), title 24pt Manrope 800, one green rule.
- Section header: number in green (7.5pt bold) + uppercase tracked label, 1pt dark rule under it.
- Fields: label 9pt + **underline field 6 mm high** (no boxes), rows separated by 0.5pt hairlines. Postcode prefix `L-` printed in muted.
- Free-text areas: ruled lines 6.2 mm apart.
- Tables: as in A; numeric code columns use tabular figures, left-aligned; quantity columns separated by hairlines.
- Checkboxes: 3 mm square, 0.7pt dark, no rounding.
- Signatures: label uppercase, 11 mm signing space, underline.
- Everything black/dark except the green rule and section numbers — a form must photocopy cleanly.
- Legal/regulatory text is printed verbatim, 7.4pt uppercase, under its own green rule.

### C. `social` (Facebook/LinkedIn posts, banners, posters) — output: **PNG** 1080×1080 (default), 1080×1350, 1640×624 cover
- Grid: 64 px outer margin, 16 px gaps; safe zone central 80 %.
- Background: green #1F6F43 full-bleed **or** photo with green gradient overlay — never white pages with a coloured table.
- Photo: real ENS work scene in a 20 px-radius card (only place rounded corners are allowed).
- Kicker: lime pill, uppercase Inter 600 18–20 px, text dark. Headline: Manrope 800 56–68 px white, max 2 lines, ≤ 6 words per line. Body: Inter 23–27 px, key words in lime #C9F27A.
- Facts: up to 4 tiles, white 12 % overlay, 1.5 px white 28 % border, value Manrope 800 26–34 px, label 14–16 px.
- One CTA bar, white on green page (or green on light page), email/phone in Inter 600 ≥ 25 px.
- QR: regenerate from the decoded link at ≥ 200 px, white plate, never crop a photo of a QR.
- **FSE+ block** whenever the project is co-financed: EU emblem to spec + « Cofinancé par l'Union européenne », ENS logo, Ministère du Travail logo, on a white footer ≥ 120 px; all agreement figures (dates, rate, budgets) on the image, plus the full sentence in the caption.
- Caption always delivered as a separate text file (French, hashtags at the end).
- **Brown:** used for service category markers (icons/labels for bricolage/transport) **[À valider]**.

### D. `slides` (HTML/PPTX presentations) — output: **PPTX** for the manager, HTML on request
- 16:9, 48 px margins, white slides; title slide and section dividers full green.
- Title Manrope 700 36–40pt, body Inter 18–20pt, one idea per slide, max 5 bullets.
- Charts: green / brown / lime / info-blue in that order; gridlines #D5DBD6; no 3D, no gradients.
- Footer: logo small left, slide number right.

### E. `web-tool` (internal HTML/JS tools, forms, dashboards) — output: HTML
- Light mode only. Background #F7F8F5, cards white with 1px #D5DBD6 border, radius 8 px (screens may use radius; print may not).
- Buttons: primary green, hover #154D2F; secondary outline brown; destructive #B4261F.
- Inputs: visible labels above, 44 px min height, 2px green focus ring.
- Tables: same rules as A; sticky header; zebra allowed on screen (#F3F6F3).
- Icons: Lucide outline 1.5–2 px, green or text colour; SVG only.
- Wording short and concrete (many non-native French readers); primary action verb-first (« Enregistrer », « Envoyer »).

---

## [À valider] — decisions I need from you
1. **Brown's role** — proposal above: secondary emphasis / category markers. Alternative: drop it from documents entirely and keep it for marketing only.
2. **Lime in internal documents** — proposal: never. Alternative: allowed for a single highlight (e.g. deadline).
3. **Word fonts** — proposal: Arial. Alternative: install Manrope + Inter on the office PCs and use them everywhere (needs admin rights).
4. **Fiche fields** — underlines (current) or boxes (original)?
5. **Default social format** — 1080×1080 square (current) or 1080×1350 portrait?
6. Anything in the five types that doesn't match how ENS actually works — e.g. a type I'm missing (devis, courrier client, affiche A3?).

Once you answer, I rebuild the plugin, re-run all three deliverables through it as a test, and send the new `.plugin`.
