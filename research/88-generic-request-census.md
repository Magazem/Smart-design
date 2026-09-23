# research/88 -- generic-request census (resolver abstentions)

Date 2026-09-23. Script: `python3 research/88-census.py` (in-process `resolve.main`, 55 plain
requests, 3-5 per family, EN plus FR/DE for cv/letter/quote/invoice/deck, no region or
variant cue). Tests: `scripts/tests/test_resolve_generic.py`.

## Before (16 of 55 abstained)

CV, the reported case and its siblings (5 of 5 abstained):

| family | query | status | top-2 |
|---|---|---|---|
| cv | make me a CV for a marketing coordinator | ABSTAIN | cv-uk 2.4776; cv-gulf-gcc 2.4654 |
| cv | write my resume | ABSTAIN | cv-us 4.4563; cv-generic 3.9369 |
| cv | I need a curriculum vitae | ABSTAIN | cv-generic 4.0115; cv-france 3.6038 |
| cv | fais-moi un CV pour un poste de comptable | ABSTAIN | cv-uk 2.4776; cv-gulf-gcc 2.4654 |
| cv | erstelle einen Lebenslauf fuer eine Bewerbung | ABSTAIN | cv-dach 4.7313; cv-eu-generic 4.0714 |

Other abstentions before AND after the fix (11): brochure x3 (trifold-a4 4.10 vs gatefold 4.08),
flyer x3 (flyer-letter 4.49 vs flyer-a4 4.20), report x2 (short 5.07 vs long-toc 4.70), deck x2
(projection vs handout/document), quote-DE "Angebot" (proposal 2.79 vs quote-devis 2.62).

## Cause

`_search` abstains whenever the top two BM25 scores are within 15% (`_MIN_MARGIN_RATIO`). For
a CV request with no region the regional doctypes share almost all their keywords ("cv",
"curriculum vitae", "resume"), so several score within a hair of each other and the resolver,
correctly refusing to pick a *region*, refused to answer at all. The tie is between variants
of one Family, not a real ambiguity about what document is wanted.

## Orchestrator rulings (product decisions, applied in round 2)

1. The family default is **language-aware**: a German/French request must not resolve to an
   English `cv-generic` (that was worse than abstaining).
2. Designated defaults are **data**, not code: nullable `doctypes."Family Default"` (`y`/blank,
   at most one `y` per family): cv -> `cv-generic`, brochure -> `brochure-trifold-a4`,
   flyer -> `brochure-flyer-a4`, report -> `report-short`, deck -> `slide-deck-projection`. A
   US / "letter" / "8.5x11" cue swaps to the letter-size sibling.
3. Keyword gap: "ecris/ecris une lettre a mon proprietaire" -> `letter-formal`.
4. True cross-family ties keep abstaining (German "Angebot": proposal vs quote).

## Fix (resolve.py `_family_default`, round 2)

When the abstention is `ambiguous` and every candidate inside the margin band belongs to ONE
Family, choose, in order:

1. **language** -- if the query is detected as French or German (small stopword detector,
   `_LANG_WORDS`, diacritic-folded, en on tie/no signal; used only here) and exactly ONE
   family doctype has that `Default Language`: take it (cv-dach for de, cv-france for fr),
   and pass the language through (`language.source = "query"`) so headings come out in it;
2. the family's `Family Default = y` doctype;
3. derived: the family doctype whose Reasoning Key is the rank-1 design's and whose Region
   Key is blank, if exactly one.

Order note: the ruling listed "flagged, then language", but for cv the flagged default
(`cv-generic`, English) would then always beat the language rule, which is exactly the
regression being fixed, so language goes first. Then a US/letter cue replaces an `a4-<x>`
default with its `letter-<x>` sibling (same family, Page Format Key). Output reports
`method=family-default`. Explicit regions ("write my cv uk", clear margin) and cross-family
ties are untouched. Tests: `scripts/tests/test_resolve_generic.py`.

Keywords: `letter-formal` gained "ecris une lettre" (accented and plain), "lettre a mon
proprietaire" (accented and plain), "lettre au proprietaire". The tokenizer folds diacritics,
so the two forms score identically; both are listed only because the ruling asked for both.

## After round 2 (1 of 55 abstains)

Only the German "Angebot" cross-family tie (proposal 2.81 vs quote-devis 2.64) still
abstains, by design. The German CV resolves to `cv-dach` (language de), the French CV to
`cv-france` (language fr), the English CV to `cv-generic` (en). Brochure, flyer, report and
deck requests resolve to their designated defaults.

## Known limits

- The paper-size cue only acts when BM25 ties inside the family. A stray number can still
  win outright: "make a flyer on 8.5x11 paper" resolves to `whitepaper` on incidental tokens
  ("paper"), and "I need a flyer for US paper" likewise. Not fixed here (a tokenizer/keyword
  question, not the family-default step); "I need a flyer, 8.5x11" and "flyer for a US bake
  sale" work.
- `Family Default` is a resolver routing flag; handoff ignores it (HANDOFF_EXCLUSIONS).

## After table (full census output)

| family | query | status | top |
|---|---|---|---|
| cv | make me a CV for a marketing coordinator | RESOLVED | cv-generic |
| cv | write my resume | RESOLVED | cv-generic |
| cv | I need a curriculum vitae | RESOLVED | cv-generic |
| cv | fais-moi un CV pour un poste de comptable | RESOLVED | cv-france |
| cv | erstelle einen Lebenslauf fuer eine Bewerbung | RESOLVED | cv-dach |
| cover-letter | write my cover letter for a project manager job | RESOLVED | cover-letter |
| cover-letter | I need a motivation letter | RESOLVED | cover-letter |
| cover-letter | help me with a cover letter | RESOLVED | cover-letter |
| letter | write a formal letter to my landlord | RESOLVED | letter-formal |
| letter | I need a business letter | RESOLVED | letter-formal |
| letter | ecris une lettre a mon proprietaire | RESOLVED | letter-formal |
| letter | schreibe einen Brief an das Amt | RESOLVED | letter-formal |
| memo | write a memo about the new office hours | RESOLVED | memo-internal |
| memo | internal note to staff | RESOLVED | memo-internal |
| memo | draft a memo | RESOLVED | memo-internal |
| form | make a form for new clients to fill in | RESOLVED | form-handfilled |
| form | I need a registration form | RESOLVED | form-handfilled |
| form | create a fillable form | RESOLVED | form-handfilled |
| brochure | make a brochure for my dental clinic | RESOLVED | brochure-trifold-a4 |
| brochure | design a brochure for our tours | RESOLVED | brochure-trifold-a4 |
| brochure | I need a brochure | RESOLVED | brochure-trifold-a4 |
| flyer | make a flyer for my bake sale | RESOLVED | brochure-flyer-a4 |
| flyer | design a flyer for a concert | RESOLVED | brochure-flyer-a4 |
| flyer | I need a flyer | RESOLVED | brochure-flyer-a4 |
| poster | make a poster for our school fair | RESOLVED | poster |
| poster | design an event poster | RESOLVED | poster |
| poster | I need a poster | RESOLVED | poster |
| report | write a report on quarterly sales | RESOLVED | report-short |
| report | format my annual report | RESOLVED | report-long-toc |
| report | I need a report | RESOLVED | report-short |
| whitepaper | write a whitepaper about cloud security | RESOLVED | whitepaper |
| whitepaper | make a white paper | RESOLVED | whitepaper |
| whitepaper | I need a whitepaper | RESOLVED | whitepaper |
| proposal | write a proposal for a website redesign | RESOLVED | proposal |
| proposal | make a project proposal | RESOLVED | proposal |
| proposal | I need a business proposal | RESOLVED | proposal |
| quote | make a quote for a kitchen renovation | RESOLVED | quote-devis |
| quote | prepare a price quotation | RESOLVED | quote-devis |
| quote | fais-moi un devis pour une renovation | RESOLVED | quote-devis |
| quote | erstelle ein Angebot fuer eine Renovierung | ABSTAIN(ambiguous) | proposal 2.8079; quote-devis 2.6379 |
| invoice | make an invoice for my consulting work | RESOLVED | invoice-tabular |
| invoice | I need an invoice | RESOLVED | invoice-tabular |
| invoice | fais-moi une facture | RESOLVED | invoice-tabular |
| invoice | erstelle eine Rechnung | RESOLVED | invoice-tabular |
| deck | make slides for my team meeting | RESOLVED | slide-deck-projection |
| deck | build a presentation about our results | RESOLVED | slide-deck-projection |
| deck | I need a slide deck | RESOLVED | slide-deck-projection |
| deck | fais-moi une presentation | RESOLVED | slide-deck-projection |
| deck | erstelle eine Praesentation | RESOLVED | slide-deck-projection |
| one-pager | make a one pager about our product | RESOLVED | one-pager |
| one-pager | I need a one page summary | RESOLVED | one-pager |
| one-pager | create a fact sheet | RESOLVED | one-pager |
| infographic | make an infographic about recycling | RESOLVED | infographic |
| infographic | I need an infographic | RESOLVED | infographic |
| infographic | create a visual summary of our data | RESOLVED | infographic |

not resolved: 1/55
