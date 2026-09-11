# rationale/headings.md

Written by `research/load-base.py`. **Do not hand-edit** -- the source is the
`source` column of the 4 heading inputs (`research/18-ats-headings.csv`, `research/39-headings-transactional-draft.csv`, `research/40-headings-longform-draft.csv`, `research/41-headings-marketing-draft.csv`).

Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling
`rationale/<table>.md`, not in a column.

T13 is the table where that citation carries the most weight and repeats the most:
204 rows over 49 distinct citations. No single distinction runs through all of them,
because the rows arrive from four inputs authored against different evidence.

The 81 CV rows (`18-ats-headings.csv`) are the ones that measure themselves against **report 03**:
6 name it as their source and 75 are convention, of which 59 carry the identical
`convention (not in report 03)` string.

The remaining 123 transactional, long-form and marketing rows are cited against
different evidence, over 33 distinct strings. **Not one of them names report 03 as
a source.** 35 mention it at all, and only to disclaim it (`not in report 03`) --
report 03 is a CV document, and these classes are outside it. 25 carry a `sourced`
citation to a standard or convention of their own, and 86 name the phase A notes
file beside their draft. Grouped by citation rather than listed per row, so the
shape of the evidence is visible instead of buried in the repetition.

## The reuse rule for `canonical_section`

Never reuse a `canonical_section` across document classes when its **FR or DE**
primary heading text reads as a word belonging to the other class. Check the actual
heading text in all three languages before reusing a section, not just the English
canonical name -- an English name that fits is exactly what makes a wrong reuse look
right.

Three worked examples, quoting the shipped rows:

- `summary` was refused for a proposal's executive summary. Its EN primary is
  "Summary", which fits, but its FR primary is "Profil" and its DE primary "Profil" -- a CV
  word in both. `executive-summary` was authored instead (FR "Résumé exécutif", DE "Zusammenfassung").
- `references` was refused for a report's bibliography. Its DE primary "Referenzen"
  reads as testimonials, not as a list of works cited. `bibliography` was authored
  instead (DE "Literaturverzeichnis").
- `proposed-solution` was refused for a whitepaper: its DE primary "Lösungsvorschlag" carries a
  commercial-bid flavour a whitepaper's solution section does not have, so
  `solution-approach` (DE "Lösungsansatz") was authored for it. That same `proposed-solution`
  was then REUSED for a pitch deck, where the bid flavour is correct. The rule cuts
  both ways -- it forbids the wrong reuse, not reuse.

## Citations

### convention (not in report 03)

59 heading(s): `education-en-3`, `skills-en-2`, `skills-en-3`, `skills-en-4`, `summary-en-2`, `certifications-en-2`, `certifications-en-3`, `projects-en-1`, `projects-en-2`, `projects-en-3`, `publications-en-1`, `publications-en-2`, `languages-en-1`, `languages-en-2`, `contact-en-1`, `contact-en-2`, `references-en-1`, `references-en-2`, `volunteering-en-1`, `volunteering-en-2`, `volunteering-en-3`, `volunteering-en-4`, `experience-fr-2`, `education-fr-1`, `education-fr-2`, `education-fr-3`, `skills-fr-1`, `skills-fr-2`, `summary-fr-1`, `certifications-fr-1`, `certifications-fr-2`, `projects-fr-1`, `publications-fr-1`, `languages-fr-1`, `contact-fr-1`, `contact-fr-2`, `references-fr-1`, `volunteering-fr-1`, `volunteering-fr-3`, `experience-de-2`, `education-de-1`, `education-de-2`, `skills-de-1`, `skills-de-2`, `skills-de-3`, `summary-de-1`, `summary-de-2`, `summary-de-3`, `certifications-de-1`, `certifications-de-2`, `projects-de-1`, `publications-de-1`, `languages-de-1`, `languages-de-2`, `contact-de-1`, `contact-de-3`, `references-de-1`, `volunteering-de-1`, `volunteering-de-2`

### convention (proposal nine-section narrative shape, one of several valid outlines; see 39-notes.md)

23 heading(s): `cover-en-1`, `cover-fr-1`, `cover-de-1`, `executive-summary-en-1`, `executive-summary-fr-1`, `executive-summary-de-1`, `problem-statement-en-1`, `problem-statement-fr-1`, `problem-statement-de-1`, `proposed-solution-en-1`, `proposed-solution-fr-1`, `proposed-solution-de-1`, `scope-of-work-en-1`, `scope-of-work-fr-1`, `scope-of-work-de-1`, `timeline-en-1`, `timeline-fr-1`, `timeline-de-1`, `pricing-en-1`, `pricing-fr-1`, `pricing-de-1`, `terms-en-1`, `terms-fr-1`

### sourced (standard invoicing field; see 39-notes.md)

18 heading(s): `issuer-en-1`, `issuer-fr-1`, `issuer-de-1`, `bill-to-en-1`, `bill-to-de-1`, `invoice-details-en-1`, `invoice-details-fr-1`, `invoice-details-de-1`, `line-items-en-1`, `line-items-fr-1`, `line-items-de-1`, `totals-en-1`, `totals-fr-1`, `totals-de-1`, `tax-en-1`, `payment-terms-en-1`, `payment-terms-fr-1`, `payment-terms-de-1`

### convention (standard report-writing convention; not in report 03)

16 heading(s): `introduction-en-1`, `introduction-fr-1`, `introduction-de-1`, `findings-en-1`, `findings-fr-1`, `findings-de-1`, `conclusion-en-1`, `conclusion-fr-1`, `conclusion-de-1`, `recommendations-en-1`, `recommendations-fr-1`, `recommendations-de-1`, `appendices-en-1`, `appendices-fr-1`, `appendices-de-1`, `bibliography-en-1`

### convention (generic hand-filled-form model, not a cited standard; see 39-notes.md)

12 heading(s): `header-en-1`, `header-fr-1`, `header-de-1`, `instructions-en-1`, `instructions-fr-1`, `instructions-de-1`, `fields-en-1`, `fields-fr-1`, `fields-de-1`, `signature-en-1`, `signature-fr-1`, `signature-de-1`

### convention (standard business-letter convention; see 39-notes.md)

6 heading(s): `sender-en-1`, `sender-fr-1`, `sender-de-1`, `recipient-en-1`, `recipient-fr-1`, `recipient-de-1`

### report 03 §A

6 heading(s): `experience-en-1`, `experience-en-2`, `experience-en-3`, `education-en-1`, `skills-en-1`, `certifications-en-1`

### convention (memo skeleton; single-word heading chosen over email-style "From:"; see 39-notes.md)

3 heading(s): `from-en-1`, `from-fr-1`, `from-de-1`

### convention (memo skeleton; single-word heading chosen over email-style "To:"; see 39-notes.md)

3 heading(s): `to-en-1`, `to-fr-1`, `to-de-1`

### convention (standard business-letter convention; shared across letter/memo/form; see 39-notes.md)

3 heading(s): `date-en-1`, `date-fr-1`, `date-de-1`

### convention (standard business-letter convention; shared across letter/memo; see 39-notes.md)

3 heading(s): `body-en-1`, `body-fr-1`, `body-de-1`

### convention (standard document convention; not in report 03)

3 heading(s): `table-of-contents-en-1`, `table-of-contents-fr-1`, `table-of-contents-de-1`

### convention (standard report/academic-writing convention; not in report 03)

3 heading(s): `methodology-en-1`, `methodology-fr-1`, `methodology-de-1`

### sourced (DIN 5008 German business-letter term; see 39-notes.md)

3 heading(s): `salutation-de-1`, `closing-de-1`, `subject-de-1`

### convention (UK-common; not in report 03)

2 heading(s): `summary-en-3`, `summary-en-5`

### convention (coined for whitepaper-standard to avoid proposal-standard's bid-flavored wording; see 40-notes.md)

2 heading(s): `solution-approach-en-1`, `solution-approach-fr-1`

### convention (marketing-collateral vocabulary; not in report 03)

2 heading(s): `headline-en-1`, `key-points-en-1`

### convention (memo skeleton; single-word heading chosen over email-style "Subject:"; see 39-notes.md)

2 heading(s): `subject-en-1`, `subject-fr-1`

### convention (résumé-writing convention; not explicitly named in report 03)

2 heading(s): `experience-en-4`, `experience-en-5`

### convention (standard English business-letter convention; see 39-notes.md)

2 heading(s): `salutation-en-1`, `closing-en-1`

### convention (standard French marketing-collateral term; not in report 03)

2 heading(s): `headline-fr-1`, `key-points-fr-1`

### convention (standard German marketing-collateral term; not in report 03)

2 heading(s): `headline-de-1`, `key-points-de-1`

### convention (Europass wording; not in report 03)

1 heading(s): `contact-en-4`

### convention (Europass-influenced wording; not in report 03)

1 heading(s): `education-en-2`

### convention (French business-deck loanword, in common practical use; more formal alternative "Ordre du jour" reserved for meeting minutes, not slide decks; not in report 03)

1 heading(s): `agenda-fr-1`

### convention (German business-deck loanword, in common practical use; more formal alternative "Tagesordnung" reserved for meeting minutes, not slide decks; not in report 03)

1 heading(s): `agenda-de-1`

### convention (UK/EU-common; not in report 03)

1 heading(s): `contact-en-3`

### convention (coined for whitepaper-standard; avoids proposal-standard's `Lösungsvorschlag`

1 heading(s): `solution-approach-de-1`

### convention (dated but still recognized; not in report 03)

1 heading(s): `summary-en-4`

### convention (dated; not in report 03)

1 heading(s): `summary-fr-3`

### convention (distinct French CV convention — short pitch line; not in report 03)

1 heading(s): `summary-fr-2`

### convention (general DE résumé convention; not in report 03; added for Luxembourg pilot)

1 heading(s): `experience-de-1`

### convention (general FR résumé convention; not in report 03; added for Luxembourg pilot)

1 heading(s): `experience-fr-1`

### convention (generic "Steuern" chosen over VAT-specific "Mehrwertsteuer" for cross-jurisdiction genericity; see 39-notes.md)

1 heading(s): `tax-de-1`

### convention (generic "Taxes" chosen over VAT-specific "TVA" for cross-jurisdiction genericity; see 39-notes.md)

1 heading(s): `tax-fr-1`

### convention (not in report 03; report 03 discusses summary content in §A but does not name a canonical heading string)

1 heading(s): `summary-en-1`

### convention (standard French marketing term; not in report 03)

1 heading(s): `call-to-action-fr-1`

### convention (standard French report/academic term; not in report 03)

1 heading(s): `bibliography-fr-1`

### convention (standard German academic/report term -- deliberately not `Referenzen`

1 heading(s): `bibliography-de-1`

### convention (standard German marketing term; not in report 03)

1 heading(s): `call-to-action-de-1`

### convention (standard deck/meeting agenda-slide term; not in report 03)

1 heading(s): `agenda-en-1`

### convention (standard marketing term; not in report 03)

1 heading(s): `call-to-action-en-1`

### convention (traditional/formal personal-details block; not in report 03)

1 heading(s): `contact-fr-3`

### convention — common in ASBL-adjacent contexts; not in report 03

1 heading(s): `volunteering-fr-2`

### convention — traditional Lebenslauf personal-data block; not in report 03

1 heading(s): `contact-de-2`

### sourced (French invoice convention: "Facturé à"; see 39-notes.md)

1 heading(s): `bill-to-fr-1`

### sourced (French letter convention: "Formule d'appel"; see 39-notes.md)

1 heading(s): `salutation-fr-1`

### sourced (French letter convention: "Formule de politesse"; see 39-notes.md)

1 heading(s): `closing-fr-1`

### sourced (German "Allgemeine Geschäftsbedingungen" (AGB) -- standard term for terms and conditions; see 39-notes.md)

1 heading(s): `terms-de-1`

