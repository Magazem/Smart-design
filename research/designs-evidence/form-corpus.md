# Form corpus — L3 authority only (USWDS, GOV.UK Design System); no L2 catalogue reachable

Coder: Design Researcher. Counts only (research/82 §1). Retrieved 2026-09-23. **Plain statement: this is a Shortfall family. Evidence is two web-UI design-system authorities coding to ONE archetype; no ranked (L1/L2) evidence exists.** Values below are read from the authorities' own published CSS/text (fetched raw with curl), not from a model paraphrase.

## Fm.1 Sources
| Authority | Pages fetched | Ranking Metric (§2) |
|---|---|---|
| USWDS | `https://designsystem.digital.gov/components/form/`, `.../components/text-input/`, CSS `https://designsystem.digital.gov/assets/css/styles.css` | `authority:USWDS form component` |
| GOV.UK Design System | `https://design-system.service.gov.uk/patterns/` (index), `.../components/text-input/`, `.../components/error-message/`, `.../patterns/question-pages/`, CSS `https://design-system.service.gov.uk/stylesheets/main-474eaefb2b0b7a31f2ea78a1079e0727.css` | `authority:GOV.UK Design System patterns` |

**L2 attempts:** MS(forms) and MS(form-templates) both redirect (HTTP 200) to the generic `https://m365.cloud.microsoft/create?...` landing page: an SPA with no static item cards (0 template cards in the payload) → **unreachable 2026-09-23**, disclosed, not reconstructed (82a C5). research/82's probe had already found no forms category. LibreOffice not counted (§10 lists none for form; `q=form` is full-text noise).

## Fm.2 What each authority prescribes (prescription → coded feature)
| Feature | USWDS | GOV.UK |
|---|---|---|
| Label position | `.usa-label` is `display:block`, above the `.usa-input`; label max-width 30rem | "You should align labels above the text input they refer to"; sentence case, no trailing colon |
| Field style | box: `.usa-input` `border:1px solid #5c5c5c; border-radius:0; height:2.5rem; max-width:30rem; padding:.5rem` | box: `.govuk-input` `border:2px solid #0b0c0c; border-radius:0; height:2.5rem; padding:5px` |
| Spacing | `.usa-form-group` margin-top 1.5rem; label margin-top 1.5rem, input margin-top .5rem | `.govuk-form-group` margin-bottom 20px in the base rule (responsive overrides not read) |
| Layout | "Keep your form blocks in a vertical pattern" (single column) | one thing per page; fieldset/legend with a large heading for the question |
| Colour use | greys for input/hint (#5c5c5c border, #757575 hint); red only for state: `.usa-input--error` 0.25rem #b50909 border, bold red message; red asterisk for required | near-black borders; red only for state: `#ca3535` border and message on error |
| Required/optional | red asterisk + explanatory text; optional fields marked "(optional)" | not asserted in the pages read |
| Placeholders | "Avoid placeholder text" | "Do not use placeholder text in place of a label" |

## Fm.3 Coded authority archetypes (§4 applied to the prescribed design)
Archetype = `columns|heading|colour|field style` (field style replaces header treatment).

| id | Authority | columns | heading | colour | field | rules/boxes | Admissible |
|---|---|---|---|---|---|---|---|
| FMA:001 | USWDS | 1 | sans (Source Sans Pro Web / Helvetica stack) | mono at rest (red is state-only) | box | boxes | y — no C7 all-cells table, no A1-A8 hit |
| FMA:002 | GOV.UK | 1 | sans (GDS Transport / Arial stack) | mono at rest (red is state-only) | box | boxes | y — same |

Both code to the **same archetype `1|sans|mono|box`** → one design with two independent L3 sources (§6 step 2: authority, ordered by number of sources = 2).

## Fm.4 Frequency and rank
No corpus is coded, so there is no k/N and no Rank Value. Rank list = L3 only:
1. `1|sans|mono|box` — `authority:USWDS form component` + `authority:GOV.UK Design System patterns` (2 sources).

Everything else is convention (L4, max 1) and the seeded doctype default.

## Fm.5 Shortfall (plain)
- Non-convention designs shippable: **1** (target 1-3 per §10, lower end; the floor of 5 is not reachable).
- **Caveat that matters for filling:** both authorities are screen web-UI systems. They prescribe boxed inputs; neither prescribes or discusses **underline** fields, the common print/office form style. So `field style = box` is evidence about web forms, not printed or Word forms, and cannot by itself justify demoting `underline`. The archetype reconstructs *their* component, not a paper form.
- `colour = mono` is my §4 reading of a form page whose only red is error state; a reviewer could code that as `one-accent`.
- C7 (`all-cells` table rules fail for forms) does not apply: neither prescribes a bordered grid table.

## Fm.6 Bias statement
Two public-sector design systems (US federal, UK government): accessibility-first, English, screen-first, single-column. No commercial or print form evidence. Authority is not popularity (§13).

## Fm.7 Ambiguities met
1. GOV.UK spacing: only the base `margin-bottom:20px` was read; responsive overrides not checked.
2. WebFetch alone returned "not explicitly prescribed" for USWDS label/field style; the raw CSS was fetched with curl to obtain the values above.
3. No second-coder list (nothing coded from a corpus).
