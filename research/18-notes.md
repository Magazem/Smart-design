# CV region rules + ATS heading dictionary — sourcing notes

## Files produced
`18-cv-region-rules.csv` (28 rows: 7 regions × 4 seniority bands), `18-ats-headings.csv`
(80 rows: 11 canonical sections × 3 languages × 2–5 variants each), `18-ats-headings-rejected.csv`
(15 rows, validator test fixtures).

## Sourcing summary

**Directly sourced to report 03 §A:** US and UK region rows (length, photo/DOB/marital-status
omission, section order, early-career education swap); the six English canonical headings
report 03 names explicitly (Experience, Work Experience, Employment History, Education,
Skills, Certifications); Gulf's photo/nationality/marital-status/visa inclusion norm and its
explicit framing as contradicting US/UK practice; EU/Europass's page range and the
country-varying photo convention.

**Extended beyond report 03, tagged as such in the `source` column of every affected row:**
EU-generic (a broad continental-Europe bucket report 03 only gestures at), DACH (report 03
mentions Germany/Austria's photo convention once, in passing, under the Europass
discussion — everything else in the DACH row is general HR/career-guidance convention I
supplied), France's non-photo cells (report 03 names only the photo trend), all English
heading synonyms beyond the six report 03 names, and all French/German headings entirely
(report 03 is English-language-focused; FR/DE were added because Luxembourg is the pilot
market). None of this is invented from nothing — it's standard professional CV-writing
convention — but it is weaker-sourced than the report-03-cited cells, and every row says so
rather than presenting it with false confidence.

**What I could not source, and flagged rather than guessed:**
- Any real evidence of a 3rd or 4th seniority-banding distinction beyond "early-career" vs.
  "experienced." mid/senior/executive are identical to each other within every region in
  the CSV — not because nothing changes with seniority, but because I have no sourced basis
  for a further split, and inventing one would be exactly the kind of unsourced threshold
  this project has been trying to avoid elsewhere (see research/16's discussion of the same
  problem for print type-scale floors).
- Europass's *current* template version's exact personal-data fields. Report 03 says DOB is
  "sometimes included"; I know the Europass platform was relaunched (~2020) with a more
  privacy-conscious template, but I don't have verified current-version documentation, so
  DOB and marital-status are marked `contested` for EU-Europass rather than picked.
- France's "CV anonyme" anti-discrimination initiative — real, but piloted/legislated in
  limited form over the years rather than a single settled universal requirement; cited as
  evidence of directional anti-discrimination pressure on photo/DOB/marital-status, not
  asserted as current blanket law. Flagged so it isn't over-cited as settled fact later.
- Whether "Qualifications" (English) should be a dictionary synonym at all. Real ATS/parser
  behavior treats it inconsistently (education vs. certifications vs. a match-scoring
  section depending on vendor) — I deliberately left it out of the primary dictionary and
  put it in the rejected/ambiguous file instead, as a hard case rather than a wrong guess.

## How a stdlib validator uses each file

**`18-ats-headings.csv`** — build a dict keyed on `(unicode-NFC-normalized, casefolded
heading_text, language)` → `(canonical_section, is_primary)`; extract each document's
actual section headings (DOCX: paragraph text styled as a heading; PDF: largest/boldest
text-run per section break), normalize the same way, and look up. **Exact match only** —
no fuzzy/edit-distance matching, because a heading dictionary that "sort of matches" is
exactly the ambiguity ATS vendors themselves don't resolve reliably (report 03 §5). A miss
is a miss, checked against `18-ats-headings-rejected.csv` as the negative-control test set
so the validator's false-negative rate on genuinely non-canonical headings is measurable,
not assumed.

**`18-cv-region-rules.csv`** — build a dict keyed on `(region, seniority_band)` tuple →
the row of facts. `region` and `seniority_band` are enum-constrained inputs resolved
upstream by the doctype/reasoning chain (or, for `seniority_band`, computed from parsed
Experience-section date ranges per the `us-cv-length-*` mechanism in
`research/16-t9-constraints-draft.csv`) — never free text, so this is a plain dict lookup,
no search/fuzzy-match layer needed at all.

## Where each asset lives in the schema

**`18-cv-region-rules.csv` should become its own small foreign-keyed table, not get
flattened into T1's doctype rows.** T1's own design notes (`09-library-schema.md:191-197`)
currently plan to resolve region entirely through existing keys — length/section-order via
`Structure Key` (T10), field inclusion via `Constraint Set Keys` (T9) — with one doctype
row per region variant (`cv-us-1page`, `cv-uk-2page`, `cv-eu-europass`, `cv-gulf`). That
works for 4 regions with implicit banding. At 7 regions × 4 bands it becomes 28 doctype
rows each restating photo/DOB/marital/visa/section-order facts — precisely the duplication
problem T6 was split out of T5 to avoid (`09-library-schema.md:429-431`, "~200 rows...
versus ~1,000 if every typeface carried its own"). Recommend: a new small table (e.g.
`cv-region-rules.csv`, this file's shape almost exactly), with T1's CV doctype rows
carrying a `Region Key` + `Seniority Band` FK into it instead of each doctype row
restating the facts. Also flag for reconciliation: T10 already has a
`Section Order Early Career` column (`09-library-schema.md:614,627-629`) covering the same
early-career swap this file's `education_before_experience` column covers — two sources of
truth for one fact, needs merging, not both kept.

**`18-ats-headings.csv` should back T10's existing `Canonical Headings` column via a
foreign key, not populate that column's cell directly.** T10's current shape
(`09-library-schema.md:615`) is a single pipe-separated text-list cell per structure row,
English-only in its example (`Experience|Work Experience|Employment History;Education;Skills`).
That shape cannot cleanly hold three languages without either inventing a
language-tagged mini-syntax inside the cell — which is exactly the "map in a cell" pattern
Rule 1 forbids — or multiplying structure rows per language, which duplicates every other
T10 column (`Section Order`, `Heading Depth Max`, etc.) that doesn't vary by language.
Recommend the same fix pattern as T6: split headings into their own long-format table
(this file), with `Canonical Headings` in T10 becoming a `Headings Key` FK instead of a
literal list.

**`18-ats-headings-rejected.csv` is not library content and doesn't belong in any T-numbered
table.** It's fixture/test data for `validate-canonical-headings`'s negative-control cases —
belongs wherever the project keeps validator test fixtures, not in the retrieval library
the model searches at runtime.
