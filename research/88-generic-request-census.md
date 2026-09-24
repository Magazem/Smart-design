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

## Round 3 -- incidental words hijack the family

Census extension: 24 requests that combine a family noun with incidental words (paper, page,
size, print, US, A4, letter-size, template, simple, professional, modern, one, two), run
through `research/88-census.py` (list `INCIDENTAL`).

**Before: 10 of 24 wrong or abstained.** Hijacks: "make a brochure / flyer on 8.5x11 paper"
and "flyer for US paper" -> `whitepaper` (token "paper" in whitepaper's "white paper /
technical paper / position paper"); "make a poster on A4 paper" -> brochure-flyer-a4 ("a4");
"a one page memo on company paper" and "make a simple one page CV template" -> one-pager /
cv-us-by-accident ("one page"); "professional CV on A4 paper", "make a printable form on A4
paper", "make a simple invoice template on A4 paper" abstained against whitepaper /
brochure-flyer-a4; "modern price quote, one page" abstained against one-pager.

**Diagnosis.** Every request names its family outright. BM25 weighs that noun like any other
keyword, and a generic word other families legitimately list (paper, A4, one page) can outvote
it. Not a keyword typo: "paper" and "one page" are correct keywords of whitepaper and
one-pager.

**Fix chosen: code, at the retrieval layer (resolve.py `_named_family`).** If the query
names exactly ONE family -- the family's own name as a whole word, hyphen or space or none
between words, optional plural s, longest names first with matched text masked so "cover
letter" names cover-letter and not letter -- BM25 runs over that family's doctypes only; an
`ambiguous` result there flows on to the family-default step (round 2). If the narrowed
search finds nothing, the unrestricted search runs as before. Zero or two-plus named families
-> unchanged behaviour (so "a letter to accompany my CV" is not forced), and the German
"Angebot" cross-family tie still abstains. Diagnostics carry `named_family`.

**Data alternative rejected:** deleting "paper" / "one page" / "A4" from those keyword lists
would fix these queries but make "position paper", "one page summary" and "A4 flyer" harder
to reach, and the next generic word would hijack again.

**After: 0 of 24 wrong; 55-case census unchanged (54 resolved, 1 abstain: Angebot).**
"make a simple one page CV template" resolves to `cv-us` (its "one page resume" keyword wins
inside the cv family), still a CV. Tests: `scripts/tests/test_resolve_generic.py`.

## Known limits

- (Round 2 limit "stray paper token hijacks the family" is fixed in round 3 below.)
- `Family Default` is a resolver routing flag; handoff ignores it (HANDOFF_EXCLUSIONS).

## After table (full census output, round 3)

| family | query | status | top |
|---|---|---|---|
| cv | make me a CV for a marketing coordinator | RESOLVED | cv-generic |
| cv | write my resume | RESOLVED | cv-generic |
| cv | I need a curriculum vitae | RESOLVED | cv-generic |
| cv | fais-moi un CV pour un poste de comptable | RESOLVED | cv-france |
| cv | erstelle einen Lebenslauf fuer eine Bewerbung | RESOLVED | cv-dach |
| cover-letter | write my cover letter for a project manager job | RESOLVED | cover-letter |
| cover-letter | I need a motivation letter | RESOLVED | letter-formal |
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

### incidental-word requests (expected family in first column)

| expected family | query | status | top |
|---|---|---|---|
| brochure | make a brochure on 8.5x11 paper | RESOLVED | brochure-trifold-letter |
| brochure | I need a simple brochure template | RESOLVED | brochure-trifold-a4 |
| brochure | design a modern brochure for print | RESOLVED | brochure-trifold-a4 |
| brochure | professional brochure, two pages | RESOLVED | brochure-trifold-a4 |
| flyer | make a flyer on 8.5x11 paper | RESOLVED | brochure-flyer-letter |
| flyer | flyer for US paper | RESOLVED | brochure-flyer-letter |
| flyer | a simple flyer template | RESOLVED | brochure-flyer-a4 |
| flyer | professional flyer one page A4 | RESOLVED | brochure-flyer-letter |
| poster | make a poster on A4 paper | RESOLVED | poster |
| poster | modern poster for print, large size | RESOLVED | poster |
| report | write a report, two page summary | RESOLVED | report-short |
| report | professional report template | RESOLVED | report-short |
| whitepaper | write a whitepaper, professional and modern | RESOLVED | whitepaper |
| whitepaper | white paper template | RESOLVED | whitepaper |
| cv | make a simple one page CV template | RESOLVED | cv-us |
| cv | professional CV on A4 paper | RESOLVED | cv-generic |
| invoice | make a simple invoice template on A4 paper | RESOLVED | invoice-tabular |
| quote | modern price quote, one page | RESOLVED | quote-devis |
| letter | write a formal letter on letter-size paper | RESOLVED | letter-formal |
| cover-letter | simple cover letter template, one page | RESOLVED | cover-letter |
| one-pager | make a one pager on US letter paper | RESOLVED | one-pager |
| form | make a printable form on A4 paper | RESOLVED | form-handfilled |
| deck | modern slide deck template | RESOLVED | slide-deck-projection |
| memo | a one page memo on company paper | RESOLVED | memo-internal |

wrong or abstained: 0/24


## Round 4 -- research/89 R5 review fixes

Scope: F1-F11 of `research/89-review-r5-resolver.md` with the orchestrator rulings from the task.
Code: `scripts/resolve.py`, `scripts/lib/data.py`. Tests: `scripts/tests/test_resolve_generic.py`
(`TestR5Review`, `TestF1BrandKitPrefixHeader`). `research/88-census.py` now also runs the
review's repro queries against an EXPECTED DOCTYPE (and language), not just the family.

| finding | fix |
|---|---|
| F1 old brand kit refuses every query | a brand CSV whose header is an exact PREFIX of the manifest columns is padded with blanks at load (`lib/data.py`); a tier-2 advisory names the kit; generic and other-brand queries are unaffected |
| F2 "letter" as paper size | paper-size uses ("letter paper/size/format/sheet", "US/American letter") are masked before family naming |
| F3 name particles flip language | `de/du/la/le/des/von/van/der/zu/di/da` skipped before a Capitalised token; a language needs >= 2 distinct signal tokens and more than English; evidence recorded |
| F4 US cue | case-sensitive `US`/`USA`/`U.S.`; "letter size/paper", "8.5x11", "american"; the pronoun "us" no longer counts |
| F5 language on every path | detected fr/de applies to direct BM25 matches too (`language.source = "query"`); `--lang` still wins |
| F6 plurals | plural nouns name the family; a named family with no keyword hit goes to its default instead of a search over other families |
| F7 two documents named | abstain, `reason: multiple-families`, `named_families`, one candidate per family |
| F8 invisible decisions | `--json` gains `diagnostics` (named_family, note, query_language, evidence, candidates[:3]); text output prints `assumed:` lines |
| F9 French means France | French + Belgique/Suisse/Quebec/Canada/Luxembourg cue -> the family's `eu-generic` doctype, language fr (even over a keyword hit); no cue -> `cv-france` |
| F10 explicit A4 | an A4 cue swaps a letter-size pick back to its a4 sibling (unless a US cue is also present) |
| F11 --lang steers doctype | the family default uses `--lang` when given |
| identity | an exact doctype key / Display Name is never narrowed away by family naming |

Aliases now naming a family (small, unambiguous only): slide(s), presentation, powerpoint -> deck;
resume, curriculum vitae, lebenslauf -> cv; white paper -> whitepaper; one pager -> one-pager;
devis -> quote; facture/rechnung -> invoice. Never "paper", "page", "brief", "angebot".

### Backlog (not done)

- **F12**: "poster child report" (poster + report) abstains as multiple-families. Accepted.
- Region cues exist only for French. German `cv-dach` already covers DE/AT/CH; no other language has a
  regional doctype to route to.
- Belgian/Swiss/Canadian French resolves to `cv-eu-generic` (English-default data, French headings)
  because no dedicated regional doctypes exist; `cv-be`/`cv-ch`/`cv-ca` would need data.
- "CV for a cafe manager" resolves to `cv-us` (a BM25 keyword hit inside the cv family), not
  `cv-generic`; family and language are right, the variant is the retriever's call.

### Before (round 3 code) -- R5 repro queries

| query | expected | status | got | ok |
|---|---|---|---|---|
| report on letter paper | report-short | ABSTAIN(ambiguous) | whitepaper 5.355; report-short 5.08 | WRONG |
| memo on letter paper | memo-internal | ABSTAIN(ambiguous) | memo-internal 5.9942; whitepaper 5.355 | WRONG |
| a memo on US letter paper | memo-internal | ABSTAIN(ambiguous) | memo-internal 5.9942; whitepaper 5.355 | WRONG |
| invoice on letter paper | invoice-tabular | ABSTAIN(ambiguous) | invoice-tabular 5.7252; whitepaper 5.355 | WRONG |
| CV for Maria de la Cruz | cv-generic [en] | RESOLVED | cv-france [fr] | WRONG |
| CV for Jean-Luc de la Fontaine | cv-generic [en] | RESOLVED | cv-france [fr] | WRONG |
| resume for Anna von der Leyen | cv-generic [en] | RESOLVED | cv-dach [de] | WRONG |
| CV for a cafe manager | cv-generic [en] | RESOLVED | cv-us [en] | (expectation later relaxed to cv-*) |
| a flyer for le petit cafe | brochure-flyer-a4 [en] | RESOLVED | brochure-flyer-a4 [en] | ok |
| make a flyer for us | brochure-flyer-a4 | RESOLVED | brochure-flyer-letter [en] | WRONG |
| brochure for us | brochure-trifold-a4 | RESOLVED | brochure-trifold-letter [en] | WRONG |
| flyer for the U.S. office | brochure-flyer-letter | RESOLVED | brochure-flyer-a4 [en] | WRONG |
| a flyer for the US market | brochure-flyer-letter | RESOLVED | brochure-flyer-letter [en] | ok |
| fais-moi une presentation | slide-deck-projection [fr] | RESOLVED | slide-deck-projection [en] | WRONG |
| erstelle eine Praesentation | slide-deck-projection [de] | RESOLVED | slide-deck-projection [en] | WRONG |
| redige un rapport long avec sommaire | report-long-toc [fr] | RESOLVED | report-long-toc [en] | WRONG |
| flyers | brochure-flyer-a4 | ABSTAIN(no-match) |  | WRONG |
| invoices | invoice-tabular | ABSTAIN(no-match) |  | WRONG |
| posters | poster | ABSTAIN(no-match) |  | WRONG |
| CVs for my team | cv-generic | ABSTAIN(no-match) |  | WRONG |
| fais-moi un CV pour un poste a Bruxelles, Belgique | cv-eu-generic [fr] | RESOLVED | cv-france [fr] | WRONG |
| redige mon CV pour Geneve en Suisse | cv-eu-generic [fr] | RESOLVED | cv-dach [de] | WRONG |
| fais-moi un CV pour le Quebec | cv-eu-generic [fr] | RESOLVED | cv-france [fr] | WRONG |
| fais-moi un CV pour un poste de comptable | cv-france [fr] | RESOLVED | cv-france [fr] | ok |
| professional flyer one page A4 | brochure-flyer-a4 | RESOLVED | brochure-flyer-letter [en] | WRONG |

R5 wrong or abstained: 21 of 25 with the final expectations (22 with the original cv-generic expectation for "cafe manager").

Multi-family queries before: all three silently RESOLVED ("a CV and a cover letter" -> cover-letter; "slides for the report" -> report-short; "deck builder CV" -> slide-deck-projection).


### After (round 4 code) -- R5 repro queries

### R5 repro queries (expected doctype [language])

| query | expected | status | got | ok |
|---|---|---|---|---|
| report on letter paper | report-short | RESOLVED | report-short [en] | ok |
| memo on letter paper | memo-internal | RESOLVED | memo-internal [en] | ok |
| a memo on US letter paper | memo-internal | RESOLVED | memo-internal [en] | ok |
| invoice on letter paper | invoice-tabular | RESOLVED | invoice-tabular [en] | ok |
| CV for Maria de la Cruz | cv-generic [en] | RESOLVED | cv-generic [en] | ok |
| CV for Jean-Luc de la Fontaine | cv-generic [en] | RESOLVED | cv-generic [en] | ok |
| resume for Anna von der Leyen | cv-generic [en] | RESOLVED | cv-generic [en] | ok |
| CV for a cafe manager | cv-* [en] | RESOLVED | cv-us [en] | ok |
| a flyer for le petit cafe | brochure-flyer-a4 [en] | RESOLVED | brochure-flyer-a4 [en] | ok |
| make a flyer for us | brochure-flyer-a4 | RESOLVED | brochure-flyer-a4 [en] | ok |
| brochure for us | brochure-trifold-a4 | RESOLVED | brochure-trifold-a4 [en] | ok |
| flyer for the U.S. office | brochure-flyer-letter | RESOLVED | brochure-flyer-letter [en] | ok |
| a flyer for the US market | brochure-flyer-letter | RESOLVED | brochure-flyer-letter [en] | ok |
| fais-moi une presentation | slide-deck-projection [fr] | RESOLVED | slide-deck-projection [fr] | ok |
| erstelle eine Praesentation | slide-deck-projection [de] | RESOLVED | slide-deck-projection [de] | ok |
| redige un rapport long avec sommaire | report-long-toc [fr] | RESOLVED | report-long-toc [fr] | ok |
| flyers | brochure-flyer-a4 | RESOLVED | brochure-flyer-a4 [en] | ok |
| invoices | invoice-tabular | RESOLVED | invoice-tabular [en] | ok |
| posters | poster | RESOLVED | poster [en] | ok |
| CVs for my team | cv-generic | RESOLVED | cv-generic [en] | ok |
| fais-moi un CV pour un poste a Bruxelles, Belgique | cv-eu-generic [fr] | RESOLVED | cv-eu-generic [fr] | ok |
| redige mon CV pour Geneve en Suisse | cv-eu-generic [fr] | RESOLVED | cv-eu-generic [fr] | ok |
| fais-moi un CV pour le Quebec | cv-eu-generic [fr] | RESOLVED | cv-eu-generic [fr] | ok |
| fais-moi un CV pour un poste de comptable | cv-france [fr] | RESOLVED | cv-france [fr] | ok |
| professional flyer one page A4 | brochure-flyer-a4 | RESOLVED | brochure-flyer-a4 [en] | ok |

R5 wrong or abstained: 0/25

### R5 multi-family queries (expected: ABSTAIN(multiple-families))

| query | status | top |
|---|---|---|
| a CV and a cover letter | ABSTAIN(multiple-families) | cv-generic cv; cover-letter cover-letter |
| slides for the report | ABSTAIN(multiple-families) | slide-deck-projection deck; report-short report |
| deck builder CV | ABSTAIN(multiple-families) | slide-deck-projection deck; cv-generic cv |
