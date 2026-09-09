# Notes — 39: transactional-class section model

## Doctype mapping confirmed (data/base/doctypes.csv)
- `quote-devis` → `invoice-standard` (not proposal-standard) — confirmed per brief.
- `invoice-tabular` → `invoice-standard` too.
- `proposal` → `proposal-standard`.
- `letter-formal` → `letter-standard`, `memo-internal` → `memo-standard`, `form-handfilled` → `form-standard`.

## 28 new canonical sections (none of the 11 existing CV sections reused)
- invoice-standard: issuer, bill-to, invoice-details, line-items, totals, tax, payment-terms
- letter-standard: sender, recipient, date, salutation, body, closing
- memo-standard: to, from, subject (+ reuses date, body from letter set)
- form-standard: header, instructions, fields, signature (+ reuses date)
- proposal-standard: cover, executive-summary, problem-statement, proposed-solution,
  scope-of-work, timeline, pricing, terms (+ reuses closing from letter set)

`date`, `body`, `closing` are shared across the new sections themselves (letter/memo/form/proposal),
not with the 11 existing CV sections.

## Rejected reuse: `summary` (existing CV canonical section) for proposal's executive summary
Considered reusing the existing `summary` canonical_section for the proposal's executive summary,
since both are "short overview" sections. Rejected: `summary`'s existing primary translations
(fr "Profil", de "Profil") are CV-specific ("profile", as in a person's profile) and wrong for a
business document's executive summary. Reusing the section would force those primaries onto
proposal-standard's render (a new fr/de row for `summary` cannot also be Is Primary=yes). Created
`executive-summary` as its own canonical section instead so its own accurate primaries apply.

## Sourced vs. conventional
- **Sourced** (standard vocabulary from real-world templates/conventions for each doc type):
  invoice terms (issuer/bill-to/invoice-details/line-items/totals/tax/payment-terms — standard
  invoicing fields); DIN 5008-style German business letter terms (Anrede, Grußformel, Betreff);
  French invoice/letter conventions (Facturé à, Formule d'appel, Formule de politesse); German
  "Allgemeine Geschäftsbedingungen" (AGB) for terms and conditions.
- **Conventional / my own choice** (no single canonical source, picked for clarity and
  consistency with the existing en/fr/de pattern): the memo skeleton (to/from/date/subject/body)
  is a common but not standardized shorthand — I chose short single-word headings rather than
  the more email-like "To:"/"From:" punctuation. The proposal's nine-section order
  (cover → executive-summary → problem-statement → proposed-solution → scope-of-work →
  timeline → pricing → terms → closing) is a common narrative-proposal shape but not the only
  valid one — no single "correct" proposal outline exists industry-wide. Form-standard's
  header/instructions/fields/signature breakdown is likewise a reasonable generic model for a
  hand-filled form, not a cited standard (forms vary too much by purpose to have one).
- French/German tax section uses generic "Taxes"/"Steuern" rather than VAT-specific terms
  (TVA/Mehrwertsteuer) since invoice-standard also serves generic quotes across jurisdictions
  where VAT may not apply — conventional choice for genericity.
