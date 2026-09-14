# A0: Request-volume ranking of document types on Claude/ChatGPT

## Method and honesty note

Published usage data from OpenAI and Anthropic classifies conversations by broad *topic* (e.g., "Writing," "Practical Guidance," "Computer and Mathematical occupations"), not by the specific document families this skill targets (CV, invoice, brochure, etc.). Only one family — CV/resume + cover letter — has a hard, citable number behind it. Everything else below is either a named-but-unquantified use case, or has no published data at all. A Google Trends proxy comparison was attempted for the undocumented families (resume/invoice/brochure/infographic "AI maker" tool searches) but returned no usable comparative data, so those families stay unranked rather than guessed.

## Ranked table

| Rank tier | Document family | Evidence | Source | Confidence |
|---|---|---|---|---|
| 1 — evidenced | CV/resume + cover letter | Résumé/cover-letter prep ≈ one-third of job-search conversations; job-search ≈ 3.5% of all ChatGPT conversations (combined figure, not split by sub-type) | [OpenAI Global Affairs, "Finding Work With AI"](https://openaiglobalaffairs.substack.com/p/finding-work-with-ai) | Medium (real number, but CV and cover letter aren't distinguished from each other) |
| 2 — named, unquantified | Slide deck | Listed by name as a recurring Claude.ai workday output alongside business correspondence and marketing copy | [Anthropic Economic Index, "Cadences" (June 2026)](https://www.anthropic.com/research/economic-index-june-2026-report) | Low (named, no share given) |
| 2 — named, unquantified | Letter/memo | Covered under "business correspondence," same Cadences report; also consistent with OpenAI's "Writing" topic being the largest work-related category (~40% of work messages per secondary summary of the NBER paper) | [Anthropic Cadences report](https://www.anthropic.com/research/economic-index-june-2026-report); [Originality.AI summary of NBER w34255](https://originality.ai/blog/how-people-use-chatgpt-openai-study) | Low |
| 2 — named, unquantified | Report/whitepaper | Consistent with rising "Office and Administrative Support" share (13% of API conversations, Nov 2025) and "Arts, Design, and Media" growth tied to writing/copyediting tasks, but not broken out as a distinct document type | [Anthropic Economic Index reports, 2025–2026](https://www.anthropic.com/research/anthropic-economic-index-january-2026-report) | Low |
| 3 — no data | Invoice/quote | No published usage or category data found distinguishing this family | — | None |
| 3 — no data | Brochure/flyer/poster | No published usage or category data found | — | None |
| 3 — no data | Form | No published usage or category data found | — | None |
| 3 — no data | One-pager | No published usage or category data found | — | None |
| 3 — no data | Infographic | No published usage or category data found; visual/design-output volume is not separated from text output in either report | — | None |

Not independently rankable: the OpenAI NBER paper (["How People Use ChatGPT," w34255](https://www.nber.org/papers/w34255)) confirms "Writing" is one of the three largest topics — together with "Practical Guidance" and "Seeking Information," these account for ~80% of all conversations — but the paper's PDF was not machine-readable via fetch, so its internal sub-breakdown of writing tasks (beyond the "two-thirds edits vs. one-third new content" split reported secondhand) could not be directly verified and is not used here as a primary number.

## Recommendation

**CV/resume** is the defensible first family for Phase A — not because it's provably the single highest-volume document type overall (the data doesn't support that claim), but because it's the only family in this list backed by an actual measured share of real usage (≈1.2% of all ChatGPT conversations, derived from 3.5% job-search × ~⅓ résumé/cover-letter). Every other candidate is either a named-but-unsized use case (slide deck, letter/memo, report) or has zero published evidence (invoice, brochure, form, one-pager, infographic). Starting where the evidence is strongest reduces the risk of building Phase A around a family nobody is actually asking for.

## Sources

- [OpenAI Global Affairs — "Finding Work With AI"](https://openaiglobalaffairs.substack.com/p/finding-work-with-ai)
- [NBER Working Paper No. w34255 — "How People Use ChatGPT"](https://www.nber.org/papers/w34255)
- [Originality.AI — secondary summary of the NBER study](https://originality.ai/blog/how-people-use-chatgpt-openai-study)
- [Anthropic Economic Index report — "Cadences" (June 2026)](https://www.anthropic.com/research/economic-index-june-2026-report)
- [Anthropic Economic Index report — "Economic Primitives" (January 2026)](https://www.anthropic.com/research/anthropic-economic-index-january-2026-report)
