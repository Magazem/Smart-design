# rationale/doctypes.md

Written by `research/load-base.py`. **Do not hand-edit** -- the source is the
`Default Language` column of `research/26-t1-doctypes-draft.csv`.

Rule 2 (`09-library-schema.md:70`): rationale and provenance live in a sibling
`rationale/<table>.md`, not in a column.

## `Default Language` -- CONVENTION, no external authority (research/64 D-E)

Criterion: `fr`/`de` only when the doctype's OWN `Display Name` is authored in
that language. `quote-devis` and `invoice-tabular` stay `en` even though their
Keywords carry `devis`/`facture` -- those are alternate-language search tokens,
not a claim the rendered document is authored in French, and neither exists as a
separate French-only doctype row.

| `doc_key` | Default Language | why |
|---|---|---|
| `cv-dach` | de | Display Name "CV -- DACH (Lebenslauf)" -- Lebenslauf is German |
| `cv-france` | fr | Display Name "CV -- France" authored for the French market; cv-france is the only CV doctype whose Display Name and Reasoning Key both name a single French-speaking market |

All other 28 doctypes default to `en` (no market/language signal of their own
Display Name).