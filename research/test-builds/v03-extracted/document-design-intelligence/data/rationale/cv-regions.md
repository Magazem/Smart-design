# rationale/cv-regions.md

Written by `research/load-base.py`. **Do not hand-edit** -- the source is the
`source` column of `research/18-cv-region-rules.csv`.

Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling
`rationale/<table>.md`, not in a column. T12's draft carries a `source` citation the
table does not have, and the 28 authored (region, seniority band) rows collapse to 14
(`early`, plus `experienced` = the widest page ceiling among mid/senior/executive), so
each entry below also records WHICH authored band the loaded row was taken from --
without it the citation cannot be traced back to the row it was written for.

One entry per row of `data/base/cv-regions.csv`, in file order.

| `cv_region_key` | region | loaded band | authored band used | source |
|---|---|---|---|---|
| `us-early` | US | early | early | report 03 §A — CONVENTION grounded in FACT: US EEOC anti-discrimination law creates employer liability incentive to avoid receiving protected-class info (age/marital status/photo-inferred traits) pre-interview |
| `us-experienced` | US | experienced | senior | report 03 §A — 2pp permitted at 10+ years experience; same EEOC-driven omission rationale |
| `uk-early` | UK | early | early | report 03 §A — '2 pages standard regardless of seniority'; Equality Act 2010 discourages employers from requesting photo/DOB pre-interview, same mechanism as US but not explicitly cited by report 03 (extended) |
| `uk-experienced` | UK | experienced | mid | report 03 §A — length invariant across seniority per report 03's explicit statement |
| `eu-generic-early` | EU-generic | early | early | general convention (continental Europe outside the specific Europass/DACH/France cases below; not explicitly detailed in report 03 — weakest-sourced row in this file) |
| `eu-generic-experienced` | EU-generic | experienced | mid | general convention (extended beyond report 03) |
| `eu-europass-early` | EU-Europass | early | early | report 03 §A — 'photo inclusion varies by country'; DOB/marital-status contested because the Europass template itself has been revised toward fewer personal-data fields and current-version specifics were not verified |
| `eu-europass-experienced` | EU-Europass | experienced | mid | report 03 §A — '2-3 pages, follows the structured Europass template sections' |
| `dach-early` | DACH | early | early | general convention (Lebenslauf norms; not covered by report 03 beyond the Germany/Austria photo mention under Europass — extended) |
| `dach-experienced` | DACH | experienced | mid | general convention (extended). CONFLICT FLAG: the traditional 'tabellarischer Lebenslauf' is a two-column table layout, which directly conflicts with this file's own ATS no-table/no-column rule (report 03 §A, also see research/16 constraint ats-no-multi-column). Resolver should default to ATS-safe single-column structure with DACH-appropriate field content/order, not the traditional visual table, for any doctype where ATS parsing matters. |
| `france-early` | France | early | early | report 03 §A — 'decreasingly common' photo inclusion named explicitly; DOB/nationality/marital-status contested for the same anti-discrimination-sensitivity reason (France has run 'CV anonyme' anti-discrimination pilots/legislation), not explicitly detailed in report 03 (extended) |
| `france-experienced` | France | experienced | senior | report 03 §A + extended — 2pp acceptable at senior level |
| `gulf-gcc-early` | Gulf-GCC | early | early | report 03 §A — Gulf inclusion norm 'directly contradicts US/UK practice'; nationality/visa-status relevance is a documented labor-market reality (nationality-based hiring-quota systems, e.g. Emiratisation/Saudization-style policy, and sponsorship-linked visa status), not merely stylistic preference |
| `gulf-gcc-experienced` | Gulf-GCC | experienced | mid | report 03 §A — same Gulf inclusion-norm rationale as early band |
