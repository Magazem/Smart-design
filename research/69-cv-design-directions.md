# CV/résumé design directions — grounded research (A2)

Sources fetched directly (used for citation): Butterick Practical Typography résumé page; Jobscan ATS-formatting-mistakes blog; Europass official CV page (europass.europa.eu); HR Dive summary of TheLadders 2018 eye-tracking study. Sources reached via search only (content corroborated across ≥2 secondary summaries, no single authoritative page fetchable — tagged accordingly below): Harvard OCS resume-format guidance (aggregated by cvowl.com, myperfectresume.com); German Lebenslauf photo convention (aggregated by talentvp.com, cv-creator.co.uk); Google Fonts pairing conventions (aggregated by pagecloud.com, zety.com). Anything with no external source is tagged **CONVENTION**.

## Direction 1 — "Harvard Reverse-Chronological" (US/UK entry–mid career)

One paragraph: a single-column, one-page, black-on-white résumé optimized for the two things known to actually decide outcomes: a 7.4-second recruiter scan and an ATS parser. No color signals seniority; hierarchy comes from type size and whitespace only.

Exemplars/authorities:
- [Butterick's Practical Typography — Résumés](https://practicaltypography.com/resumes.html) (fetched): recommends generous margins, shorter line length, never assume the reader reaches page 2, PDF export "so good typography survives."
- Harvard OCS format rules, as aggregated by [cvowl.com](https://www.cvowl.com/blog/harvard-resume-template-formatting-rules-you-must-follow) and [myperfectresume.com](https://www.myperfectresume.com/career-center/resumes/harvard-resume) (search-derived, not directly fetched): margins ≥0.75in, name largest, section titles 2pt below name, body ≥10pt, one page.
- [HR Dive — TheLadders 2018 eye-tracking study](https://www.hrdive.com/news/eye-tracking-study-shows-recruiters-look-at-resumes-for-7-seconds/541582/) (fetched): 7.4s average scan, E/F-pattern reading, single-column with bold titles + bulleted accomplishments wins; multi-column and dense text lose.
- [Jobscan — 5 Critical ATS Formatting Mistakes](https://www.jobscan.co/blog/ats-formatting-mistakes/) (fetched): single column only, no headers/footers/text boxes, standard section names ("Work Experience," "Education," "Skills").

Palette: `#1A1A1A` body text (near-black, softer than pure `#000000` per Butterick's advice against harsh contrast), `#FFFFFF` page, one accent `#0F3D57` (dark ink-blue) used only for the name/header rule — never for body links or icons. No default web-blue (`#0563C1`/`#1155CC`), which is the slop pattern this direction structurally avoids.

Typefaces: heading — Source Serif 4 (OFL, Google Fonts) or Lora; body — Source Sans 3 or Open Sans. Serif/sans pairing rule from the pagecloud.com/zety.com aggregation of Google Fonts pairing convention (search-derived): "one serif plus one sans-serif, never two of the same class." OS fallback: Georgia (heading) / Arial (body) — both preinstalled Win/macOS, both explicitly Jobscan-approved ATS-safe fonts.

Type scale: body 10.5pt/13pt leading; H1 (name) 20pt/22pt; H2 (section) 12pt/14pt, small-caps or bold, not colored; small (dates/location) 9.5pt/12pt. Sizing anchored to Harvard OCS's "name largest, section −2pt, body ≥10pt" rule and Jobscan's 10–12pt body / 14–16pt heading range.

Grid: US Letter or A4 per region, margins 0.75in (19mm) all sides (Harvard OCS), single column throughout (Jobscan: multi-column breaks ATS reading order; Ladders: multi-column loses the eye-tracking test), generous white space between sections rather than rules/borders — Butterick explicitly warns against "uncomfortably dense" layouts.

Slop avoided (pattern names per `research/68-slop-patterns.md`): **Default-blue-everywhere** (no Office/Tailwind accent blue; the one accent traces to the resolved Palette Key, not a tool default); **Mismatched fonts** (one serif/sans pair, each assigned a consistent role — Butterick's "few can tolerate a third" rule); **Bloated / over-informative text** (Butterick: put only what's load-bearing on page 1; no restating context); **Frames around everything** (section separation by whitespace, not borders/boxes — no rule around every block); the existing `icon-only-skill-bar` anti-pattern token (doc-reasoning.csv) is avoided by construction since this direction carries no skill-bar element at all.

Fits: `us-early`, `us-experienced`, `uk-early`, `uk-experienced` per `cv-regions.csv` — no photo (`negative-signal` for Photo/DOB/Nationality/Marital Status/Visa in both rows), reverse-chronological, English.

## Direction 2 — "DACH Tabellarisch" (photo, regional formality)

One paragraph: a two-column tabular layout (dates/labels left, content right) with a formal headshot top-right, built for markets where photo and structured personal data are still culturally expected despite anti-discrimination law formally not requiring them.

Exemplars/authorities:
- DACH Lebenslauf photo convention, aggregated by [talentvp.com](https://talentvp.com/en/german-cv) and [cv-creator.co.uk](https://cv-creator.co.uk/cv-advice/german-cv/) (search-derived): standard photo 4.5×6cm top-right, AGG law doesn't require it but cultural expectation persists; anonymized/international employers are the exception.
- `data/base/cv-regions.csv` rows `dach-early`/`dach-experienced` (repo data, cross-checked): Photo/DOB/Nationality/Marital Status = `customary`, Visa = `contested`, Education Before Experience = yes (early) / no (experienced).
- [Europass official CV page](https://europass.europa.eu/en/create-europass-cv) (fetched): confirms reverse-chronological order and photo as an accepted, not mandatory, element — used here as the EU-wide baseline this direction sits inside.

Palette: `#FFFFFF` page, `#222222` body text, `#2B2B2B` rule lines for the table grid (near-black, not colored — avoids the "default-blue corporate template" tell). No accent color; formality signaled by structure, not hue.

Typefaces: heading/labels — PT Serif or Merriweather (OFL); body — PT Sans or Noto Sans (broad diacritic/umlaut coverage, relevant for German). Fallback: Times New Roman (labels) / Arial (body). CONVENTION: no fetched pairing source specifically for DACH-market typefaces; pairing rule (serif label / sans body) follows the same Google Fonts pairing convention cited in Direction 1.

Type scale: body 10pt/13pt; H1 (name, top-left beside photo) 16pt/18pt; H2 (table section labels, left column) 10pt bold/13pt; small (personal-data block) 9pt/11pt.

Grid: A4, margins 20mm, two-column table (label column ~35mm, content column remainder), photo 4.5×6cm top-right per the aggregated DACH convention. Whitespace rule: consistent row padding rather than borders around every cell — avoids the "frames around everything" slop pattern.

Slop avoided (pattern names per `research/68-slop-patterns.md`): **Frames around everything** / **Odoo-clone invoice grids** (row separation by consistent padding, not a bordered cell grid — same underlying check the census flags for invoice tables applies to a personal-data table); **Default-blue-everywhere** (near-black rule lines, no accent-blue table grid); **Mismatched fonts** (one serif-label/sans-body pair only); **Bloated / over-informative text** (tabular format structurally has no room for narrative summary text).

Fits: `dach-early`, `dach-experienced`; adaptable to `eu-generic-*` and `france-*` rows (also `customary`/`contested` photo) by dropping the strict table grid to single-column with sidebar photo.

## Direction 3 — "Europass-Compatible Multilingual" (EU cross-border, early career / EU institutions)

One paragraph: a single-column, section-ordered CV matching the structure of the official Europass tool (education/training, work experience, skills, languages) so it can be produced as a native Europass export or a close visual match, for candidates targeting EU-wide or multinational roles where reviewers expect that shape.

Exemplars/authorities:
- [Europass official CV page](https://europass.europa.eu/en/create-europass-cv) (fetched): reverse-chronological order, "clear and simple language," strong verbs, photo permitted not mandatory.
- `cv-regions.csv` row `eu-europass-early`/`eu-europass-experienced`: Section Order = `contact;education;experience;languages;skills` (early) — languages get a dedicated slot, distinct from the US/UK order.
- [Jobscan ATS mistakes](https://www.jobscan.co/blog/ats-formatting-mistakes/) (fetched): standard section names and single-column apply equally here — a Europass-style CV must still parse if submitted through a non-EU ATS.

Palette: `#FFFFFF` page, `#1E1E1E` text, `#00457C` accent — the closest a defensible restrained value gets to the EU's own institutional dark-blue, used only for section-label underscores, never full-block fills. CONVENTION: exact hex not sourced from an EU brand-guideline fetch; treat as a suggested restrained blue, replaceable.

Typefaces: Public Sans or IBM Plex Sans (OFL, both designed for multilingual/diacritic coverage) for both heading and body, differentiated by weight only — avoids importing a second typeface family purely for headings, which reduces mismatched-font risk in multilingual documents where accented glyphs must render consistently. Fallback: Arial (all weights).

Type scale: body 10.5pt/13.5pt; H1 16pt/18pt; H2 11pt bold/14pt; small 9pt/11.5pt. Slightly larger leading than Direction 1 to accommodate longer localized section labels (e.g., German/French compound words).

Grid: A4 (EU default), margins 20mm, single column, explicit language-proficiency table (self-assessment grid is a real Europass structural element, not a slop pattern, since it maps to a recognized EU framework).

Slop avoided (pattern names per `research/68-slop-patterns.md`): **Default-blue-everywhere** (the one restrained accent is restricted to section-label underscores, not a full-block fill, and is explicitly flagged CONVENTION rather than presented as a sourced brand rule); the doc-reasoning.csv `photo` anti-pattern token (photo made conditional per target country's cv-regions.csv row, not default-on); **Bloated / over-informative text** (Europass favors itemized skills/languages tables over narrative summary prose); **Too much information** (one language-proficiency grid per the recognized EU framework, not stacked badges/icons competing for attention).

Fits: `eu-europass-early`, `eu-europass-experienced`, `eu-generic-early`, `eu-generic-experienced`.

## Comparison: current default vs the three directions

The skill's current CV default is `cv-restrained` / mono-ink / `safe-sans-arial` / Arial 11pt (per task brief; not independently re-verified against `doc-styles.csv` in this read-only research task).

| Aspect | Current default | Direction 1 (Harvard) | Direction 2 (DACH) | Direction 3 (Europass) |
|---|---|---|---|---|
| Already right | Mono-ink avoids default-blue slop; Arial is Jobscan-safe | — | — | — |
| Missing | No serif/sans pairing option; single font family only; no region-driven layout (photo/table) variation; type scale not differentiated by seniority | Two-typeface OFL pairing with fallback; explicit type scale tied to Harvard OCS ratios | Tabular two-column layout; photo block sizing; region-specific personal-data fields | Language-proficiency structure; EU section order; restrained accent option |
| Gap this fills | — | Gives entry/mid US/UK CVs a typographically considered but still ATS-safe alternative to plain Arial | Gives DACH candidates a structurally correct, non-slop tabular format the current mono-ink default can't express | Gives EU cross-border candidates the Europass-recognized section order and language grid |

Arial-only mono-ink is a defensible ATS-safe floor (matches Jobscan's approved font list) but under-serves: (a) US/UK candidates where Butterick-style spacing/hierarchy measurably helps the 7.4-second scan, (b) DACH candidates where a photo/table structure is culturally `customary` per `cv-regions.csv` and the current default has no path to express it, (c) EU cross-border candidates where Section Order differs (languages promoted) and the current default doesn't vary structure by region at all.

## Optional: three interview questions to pick a direction

1. **Seniority**: "Is this your first professional role, or do you have prior full-time experience?" → early-band CVs favor education-first ordering and 1-page constraint (Direction 1/3); experienced-band favors experience-first and allows 2 pages.
2. **Region**: "Which country/market is this CV going to?" → maps directly to `cv-regions.csv` region_key (us/uk → Direction 1; dach → Direction 2; eu-generic/eu-europass → Direction 3).
3. **Industry/tone**: "Is the target employer a formal/traditional organization (law, government, EU institution, DACH corporate) or an international/anonymized-hiring employer?" → formal/traditional pushes toward Direction 2's photo+table; anonymized/international pushes toward Direction 1 or 3 with photo omitted.
