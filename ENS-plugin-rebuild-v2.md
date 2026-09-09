# ENS plugin rebuild — v2 (corrections applied, not yet built)

Changes versus v1 are marked **[T1.x]** / **[T2.x]** referring to the corrections file. Where I verified a claim against the plugin source, I say so.

## Verification notes (what I checked before revising)
- **[T1.1] confirmed** — activation is decided from the frontmatter `description:` only; the body block never influenced it.
- **[T1.2] confirmed with one precision** — `Decision_Rules` is read (`design_system.py:385`) but only a fixed set of built-in condition keys (`if_ux_focused`, `if_data_heavy`, `must_have`…) can ever fire; custom keys like `if_internal_note` never match, so v1's routing was indeed inert. `Style_Priority` and `UI_Category` are read and used.
- **[T1.3] confirmed** — colour search reads only `Product Type` + `Notes` (`core.py:26`); products reads `Primary Style Recommendation`; styles searches `Style ID`, `Style Category`, `Aliases`, `Keywords`, `Best For`, `Type`, `AI Prompt Keywords`. Note: `Style ID` and `Parent Style ID` columns **do** exist in this plugin version (v1 used them correctly), but there is no inheritance of rule content — only a pointer — so everything is restated in the ENS row anyway.
- **[T1.6] tested** — `docx` (node), `pptxgenjs`, `python-docx`, `python-pptx` all present. **.docx and .pptx stay** as target formats.

---

## 1. ENS in the library

**Linking key — byte-identical in all files [T1.4]:** `ENS - Eng nei Schaff` (plain hyphen, single spaces).

**Match tokens (present in every searched column):** `ens, eng nei schaff, engneischaff, bettembourg, luxembourg, asbl, recyclage, jardinage, bricolage, transport, fse`

### products.csv [T1.3 column names fixed]
| Column (exact) | Value |
|---|---|
| Product Type | `ENS - Eng nei Schaff` |
| Keywords | ens, eng nei schaff, engneischaff, bettembourg, luxembourg, asbl, recyclage, jardinage, bricolage, transport, fse, note interne, formulaire, fiche, affiche, dépliant, présentation, facebook, courrier |
| Primary Style Recommendation | ENS Document Grid |
| Secondary Styles | Minimalism & Swiss Style, Flat Design |
| Landing Page Pattern | Trust & Authority |
| Dashboard Style (if applicable) | Data-Dense, light mode only |
| Color Palette Focus | ENS forest green structure + earth brown secondary; lime badge only in marketing |
| Key Considerations | ENS Eng nei Schaff Bettembourg. Printed documents filled by hand; many readers non-native French → short words, clear hierarchy, labels ≥ 8.5pt; FSE+ elements mandatory on funded material |

### colors.csv [T1.3 Product Type + Notes added; T2.8 contrast checked]
| Column | Value |
|---|---|
| Product Type | `ENS - Eng nei Schaff` |
| Primary / On Primary | #1F6F43 / #FFFFFF — 6.4:1 ✓ |
| Secondary / On Secondary | #8B5E3C / #FFFFFF — 5.6:1 ✓ |
| Accent / On Accent | #9ACD32 / #1E2A23 — 8.7:1 ✓ (accent is a **fill**, never text) |
| Background / Foreground | #F7F8F5 / #1E2A23 — 13.9:1 ✓ |
| Card / Card Foreground | #FFFFFF / #1E2A23 |
| Muted / Muted Foreground | #DCE8DF / #5B665F — 4.6:1 ✓ |
| Border | #D5DBD6 |
| Destructive / On Destructive | #B4261F / #FFFFFF — 6.9:1 ✓ |
| Ring | #1F6F43 |
| Notes | ENS Eng nei Schaff Bettembourg Luxembourg asbl. Green = structure/primary; brown = secondary; lime = filled badge with dark text only, never as text (fails contrast on white 1.6:1 and on green) |

### typography.csv [T1.3 columns split, Category + Best For filled]
| Column | Value |
|---|---|
| Font Pairing Name | ENS Manrope Inter |
| Category | Sans + Sans |
| Heading Font | Manrope |
| Body Font | Inter |
| Mood/Style Keywords | ens, eng nei schaff, reliable, clear, down-to-earth, functional, bettembourg |
| Best For | ENS Eng nei Schaff documents, forms, social posts, slides, internal tools; Luxembourg asbl recyclage jardinage bricolage |
| Google Fonts URL / CSS Import / Tailwind | Manrope 700;800 + Inter 400;500;600 |
| Notes | Embed Manrope/Inter in PDF, HTML, PNG and **PPTX (embedding ON, verified)** [T2.5]. Use Arial in editable Word/Excel. Never mix in one document. |

### styles.csv [T1.3 restated, no reliance on inheritance]
| Column | Value |
|---|---|
| Style Category | ENS Document Grid |
| Style ID | ens-document-grid |
| Aliases | ENS\|Eng nei Schaff\|ENS Grid |
| Type | Brand |
| Keywords | ens, eng nei schaff, bettembourg, grid-based, hairline rules, single accent, no fills, white space, high contrast, sans-serif, print-friendly, hand-fillable, photocopy-safe |
| Primary Colors | Forest green #1F6F43 rule + black text on white |
| Secondary Colors | Earth brown #8B5E3C secondary, hairline #B9C4BC, muted #5B665F |
| Effects & Animation | None (print); screen: 150–250ms hover only |
| Best For | ENS Eng nei Schaff internal notes, forms, fiches, letters, tables, slides, internal web tools |
| Do Not Use For | ENS social posts and banners (use ENS marketing rules) |
| Light/Dark | light only |
| Accessibility | contrast-text-4.5, photocopy-safe (no colour-only meaning) |
| Design System Variables | --radius: 0; --shadow: none; --rule-hair: 0.5pt #B9C4BC; --rule-strong: 1pt #1E2A23; --rule-brand: 1.6pt #1F6F43; --space: 4mm; --label: 8.5pt; --body: 11pt |
| Implementation Checklist | ☐ one green rule under title ☐ labels 8.5pt uppercase tracked ☐ tables hairlines only, no fills/zebra ☐ fields underline 6mm ☐ section numbers black ☐ footer address + page x/y ☐ no rounded boxes/badges/icons unless functional ☐ lime never as text |
| Parent Style ID | minimalism-and-swiss-style (pointer only) |
| Status | active |

### ui-reasoning.csv [T1.2 columns the code reads filled; JSON kept as documentation]
| Column | Value |
|---|---|
| UI_Category | `ENS - Eng nei Schaff` |
| Recommended_Pattern | Trust & Authority |
| Style_Priority | ENS Document Grid + Minimalism & Swiss Style |
| Color_Mood | ENS green structure + brown secondary |
| Typography_Mood | Clear + Functional hierarchy |
| Key_Effects | None (print) |
| Decision_Rules | `{"must_have":["style:ens-document-grid","constraint:ens-palette-only"],"if_data_heavy":["constraint:light-mode-only"]}` — only built-in keys; per-document routing is done in the trigger block, not here |
| Anti_Patterns | Decorative fills + coloured badges + rounded cards in documents + three accents on one page + emoji + gradients + navy/blue palettes + lime text |
| Severity | HIGH |

### Hard check on search output [T1.5]
New script `scripts/ens-search.sh` wraps `search.py`, greps its output for `ENS - Eng nei Schaff`, and prints `[NO ENS MATCH] — fix the query, do not proceed` when absent. The trigger block calls this wrapper, never `search.py` directly.

### Re-sync guard [T2.8]
Comment at the top of each ENS CSV row block and in README: ENS rows must survive `_sync_all.py`; Product Type text is the key — do not edit it.

---

## 2. Activation + trigger [T1.1]

### 2a. Frontmatter `description:` — rewritten on all 7 skills (this is what activates the plugin)
Each skill keeps its original functional description, prefixed with:

> Customised for **ENS – Eng nei Schaff a.s.b.l.** (Bettembourg, Luxembourg — recyclage, jardinage, bricolage, transport). Use this skill for ANY document or visual for this organisation, whether or not the user mentions ENS or a brand: note interne, courrier, formulaire, fiche (d'intervention, de suivi), affiche, dépliant, présentation, post Facebook/LinkedIn, bannière, tableau, outil interne. All ENS output must use the ENS brand rules — never generic or default styling.

The `ui-ux-pro-max` and `brand` skills additionally list the French trigger phrases verbatim: « fais-moi une note interne », « refais cette fiche », « un post pour Facebook », « une présentation pour le manager », « remake this file », « redesign ».

**Activation test to run after rebuild:** « fais-moi une note interne sur les congés » with no mention of ENS, brand or plugin → the skill must fire.

### 2b. Body trigger block (unchanged in spirit, wrapper + format rules added)
1. Classify the deliverable: `note-interne` · `formulaire` · `social` · `slides` · `web-tool`. Unclear → ask.
2. Read `brand/references/ens-document-rules.md` section for that type — fixed decisions.
3. Run `ens-search.sh "ENS <type>" --design-system`. If `[NO ENS MATCH]` appears, stop and fix the query.
4. Build with: ENS palette roles; font per output format (Manrope+Inter embedded in PDF/HTML/PNG/PPTX; Arial in DOCX/XLSX); the type's template.
5. Verify against the type checklist, render, and state which rules section + which search were used.

Never: choose a generic library style over ENS rules; drop a brand colour because a generic style says "single accent"; change content, fields, figures or legal text of a redesign; use emoji, gradients, navy/blue, or lime as text.

---

## 3. Per-document rules (`ens-document-rules.md`)

### Global
- French, « vous », guillemets, NBSP before : ; ! ?
- **Palette roles:** green = title rule, primary CTA, key numbers · brown = secondary labels / category markers · lime = **filled badge with dark text, marketing only, never text** [T2.6]. Text #1E2A23, muted #5B665F, hairline #B9C4BC.
- **Type scale (pt):** 8.5 label [T2.7] · 9 caption · 11 body · 12 lead · 16 H3 · 24 H1 documents. Legal/regulatory text: **mixed case, 8.5pt minimum** [T2.1].
- Logo: original colourful ENS logo, never recoloured, ≥ 15mm on A4, on white.
- Footer every printed page: `Eng nei Schaff a.s.b.l. · 144, Z.A.E. Wolser A · L-3225 Bettembourg · Tél. 00352 54 66 70` + `Page x / y`.
- Redesigns preserve content, numbering, figures, legal text verbatim; typo fixes listed to the user.
- Photocopy rule: nothing carries meaning by colour alone; section numbers and labels black [T2.3].

### A. `note-interne` — .docx (+ PDF)
- A4. **Text measure 130 mm** [T2.2]: margins 25 mm left / 55 mm right (side column stays free for dates/notes), body Arial **11pt**, line 1.35.
- Header line: logo left (17 mm) · kind centred · date right, 8.5pt muted.
- Title 30pt bold, subtitle 11pt muted, one 1.6pt green rule.
- Tables: uppercase tracked 8.5pt column labels, 1pt dark rule under header, 0.5pt hairlines, no fills/zebra. Emphasis = bold (green text allowed for one category, brown for a second) — never background.
- Remarks in their own column; numbered remarks with black number + tab; no bullets, boxes, side borders.
- Sign-off: role bold, company muted.

### B. `formulaire` — PDF, fonts embedded
- A4, 16/12 mm margins, 4 mm grid. Header: logo left, company block right 8.5pt, title 24pt Manrope 800, one green rule.
- Section header: **black** number 8.5pt bold + uppercase tracked label, 1pt dark rule [T2.3].
- Fields: label 9.5pt + underline field 6 mm (**or boxes — [À valider #4]**), 0.5pt hairlines between rows. `L-` prefix muted.
- Free text: ruled lines 6.2 mm. Tables as in A; code columns tabular figures. Checkboxes 3 mm, 0.7pt, square.
- Signatures: uppercase label, 11 mm space, underline.
- Only green element: the title rule. Legal text verbatim, **mixed case 8.5pt**, under its own green rule [T2.1].

### C. `social` — PNG 1080×1080 **(or 1080×1350 — [À valider #5])**, cover 1640×624
- 64 px margins, 16 px gaps, central 80 % safe zone.
- Green full-bleed or photo + green gradient. Photo in 20 px-radius card (only rounded element allowed).
- Kicker: lime filled pill, dark text, Inter 600 18–20 px. Headline Manrope 800 56–68 px white, ≤ 2 lines. Body Inter 23–27 px white; emphasis = **bold white**, not lime text [T2.6].
- Facts: ≤ 4 tiles, white 12 % fill, 1.5 px white 28 % border. One CTA bar, contact ≥ 25 px.
- QR regenerated from decoded link ≥ 200 px on white plate.
- FSE+ block when co-financed: EU emblem to spec + « Cofinancé par l'Union européenne », ENS logo, Ministère du Travail, white footer ≥ 120 px; all agreement figures on the image + full sentence in caption. Caption delivered as separate .txt.
- Brown: service category markers **[À valider #1]**.

### D. `slides` — .pptx (fonts **embedded, verified after export** [T2.5]); HTML on request
- 16:9, 48 px margins, white slides; title + section dividers full green.
- Title Manrope 700 36–40pt; **body 24pt default; 18–20pt only on explicitly data-dense slides** [T2.4]; one idea per slide, ≤ 5 bullets.
- Charts: green / brown / #2F6F9F info blue / muted — lime only as a filled highlight; gridlines #D5DBD6; no 3D/gradients.
- Footer: small logo left, slide number right.

### E. `web-tool` — HTML
- Light only. Bg #F7F8F5, white cards 1px #D5DBD6, radius 8 px (screen only).
- Buttons: primary green (hover #154D2F), secondary brown outline, destructive #B4261F. Inputs: label above, ≥ 44 px, 2px green focus ring.
- Tables as A; sticky header; zebra allowed on screen (#F3F6F3). Icons Lucide outline, SVG only.
- Copy short and verb-first (« Enregistrer », « Envoyer »).

---

## Decisions still open (ENS preference — no research basis)
1. **Brown's role** — secondary labels / category markers (proposal) **or** marketing only?
4. **Form fields** — underlines (current) **or** boxes (original)?
5. **Default social size** — 1080×1080 **or** 1080×1350?

Closed by the review: #2 lime never as text (applied) · #3 Arial in Word (applied) · #6 A3 affiche — **not added**; say if you want it and I'll add a print-production section (bleed, CMYK, 300 DPI) as a sixth type.

After your three answers: apply CSV rows → rewrite 7 descriptions + body blocks → write rules file + wrapper script → run the activation test and the three deliverables through it → send the `.plugin`.
