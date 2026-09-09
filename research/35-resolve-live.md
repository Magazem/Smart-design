# 35 — resolve.py against live data/base (Mechanism Analyst, re-run for load pass 3)

## Gate: 31 problems (was 82)

```
$ python3 scripts/validate_data.py data/base
data\base\structures.csv: declared in manifest but file does not exist
data\base\doctypes.csv:2..31: Structure Key: '<key>' does not resolve to structures.structure_key   (x29)
data\base\palettes.csv:2:On Accent: cannot compute contrast: invalid hex color ''
31 problem(s) found
```

`structures.csv` was never created on disk (T1/T2/T4/T7 landed; `structures` did not).
Because `structures` is not the entry table, this is correctly a **tier-2** problem
(`lib/data.py` load_table_rows: "a missing base file is tier 1 only for the entry
table"), so `resolve.py` does not do a whole-dataset refusal this time — it runs
per-key degradation instead, which is the intended behavior verified in the prior
per-key task. Net effect: every doctype row with a non-empty `Structure Key` (29 of
31 rows) is individually poisoned, so every one of the 12 queries below reaches
BM25/FK-walk and only refuses at the last step, by name.

## Per-query results

| # | Query | Entry resolved to | Expected | Verdict |
|---|---|---|---|---|
| E1 | "build me an academic CV with my publications list" | `cv-academic` | `cv-academic` | pick correct; REFUSED PATH on `doctypes/cv-academic` (Structure Key) |
| E2 | "I need a leave-behind version of this deck for the client" | `slide-deck-handout` | `slide-deck-handout` | pick correct; REFUSED PATH |
| E3 | "make me a flyer" | **`cv-generic`** | ambiguous → abstain | **FAIL** — see Q1 below, this is a real bug, not noise |
| E4 | "draft an invoice for this order" | `invoice-tabular` | `invoice-tabular` | pick correct; REFUSED PATH |
| F1 no-brand | "fais-moi une note interne sur les congés" | `memo-internal` | `memo-internal` | pick correct; REFUSED PATH |
| F1 `--brand ens` | same | `memo-internal` (identical to no-brand) | `ens-note-interne` | **untestable** — `data/brand/` has no `ens` overlay at all (only a README); brand pass 1 finds zero rows, falls straight to generic pass. Not a resolver bug — there is no brand data loaded to distinguish the two passes. |
| F2 | "rédige un devis pour ce client" | `quote-devis` | `quote-devis` | pick correct; REFUSED PATH |
| F3 | "fais-moi un cv" | `cv-generic` | `cv-generic` (the "ideal" outcome) or abstain | **PASS** — see Q2 below |
| F4 | "rédige un rapport avec table des matières" | `report-long-toc` | `report-long-toc` | pick correct; REFUSED PATH |
| D1 | "erstelle einen tabellarischen lebenslauf" | `cv-dach` | `cv-dach` | pick correct; REFUSED PATH |
| D2 | "ich brauche ein anschreiben für diese bewerbung" | `cover-letter` | `cover-letter` | pick correct; REFUSED PATH |
| D3 | "erstelle eine präsentation" | **`slide-deck-projection`** | ambiguous → abstain | **FAIL** — same bug class as E3 |
| D4 | "erstelle einen europass lebenslauf" | `cv-eu-europass` | `cv-eu-europass` | pick correct; REFUSED PATH |

10/12 pick the right entry row (or the accepted "ideal" row for F3). 2/12 (E3, D3) —
both deliberately-ambiguous cases — fail by resolving *confidently* instead of
abstaining. F1's brand pass is blocked by missing overlay data, not by resolver logic.
Every query that reaches FK-walk still ends in REFUSED PATH because `structures.csv`
doesn't exist, so none of the 12 produced a final RESOLVED payload end-to-end; that is
a data gap (out of scope here — `data/` was not touched), not a resolver bug.

## Q1 — the flyer/cv-generic candidate-set question: NOT noise, a real mis-resolution

Traced with the actual `_resolve_entry`/`_search` call (bypassing the refusal so the
diagnostic is visible):

```
QUERY: make me a flyer
 resolved: cv-generic
 candidates: cv-generic=5.8756, cv-uk=5.0761, cv-us=4.6929, brochure-flyer-letter=4.5749, brochure-flyer-a4=4.4553
```

`cv-generic` is not "noise" listed alongside the real pick — it **is** the chosen,
margin-clearing top BM25 result, ahead of both flyer rows. Cause: no stopword
filtering in the BM25 tokenizer, and `cv-generic`'s Keywords cell literally contains
the phrase `"make me a resume"`, so it shares 3 of query's 4 tokens (`make`, `me`,
`a`) verbatim, each carrying nontrivial IDF because those words are otherwise rare in
the corpus — while `flyer`, the one real signal word, is worth less than the
accidental function-word overlap. `_touched_poison`/`_print_refused_path` already
only walk `resolved` (the actual chosen entry row's FK closure), never the abstain
candidate list — so **the REFUSED PATH block itself needs no fix**; it is correctly
reporting the chosen (wrong) path. The bug is upstream, in BM25 scoring/abstention
having no stopword handling — flagging for the lead, not fixing (out of scope: this
is an algorithm change, not the refusal-block formatting question the brief asked
about). Same root cause produces D3's failure (`präsentation` case).

## Q2 — cv-generic vs the seven regional CV rows

```
QUERY: fais-moi un cv
 resolved: cv-generic
 candidates: cv-generic=5.6909, cv-france=5.6032, cv-eu-generic=5.4897
```

Now that the data is complete, `cv-generic` wins by a real (if narrow, ~0.09) margin
over the keyword-denser regional rows — the risk flagged in `26-notes.md` did not
materialize here. This is the "ideal" outcome the notes named as acceptable. Margin is
thin enough that it's not a robust guarantee against future keyword additions to any
regional row, but as tested today, F3 passes.

## Q3 — empty Section Order message: not implemented, now landed

Grepped `scripts/` for the required string before touching anything — no match
anywhere; the per-key pass did not add it. Implemented in `resolve.py`
(`_field_value`, used by both `_print_resolved` and `_resolution_payload`): any
group-FK list column (manifest-driven, not hardcoded beyond the exact wording) that
resolves empty on a row now renders as `no <column-name-with-hyphens> guidance for
<doctype>` instead of a bare empty value, so an empty list can never surface as a
silent answer.

Could not be exercised against live `data/base` — `structures.csv` doesn't exist, so
every doctype with a Structure Key hits REFUSED PATH before a structures row is ever
displayed. Verified instead against a throwaway fixture outside `data/`
(`/tmp/ddi-verify`, deleted after use, nothing under `data/` or `research/*.csv`
touched):

```
$ python3 scripts/resolve.py --data-dir /tmp/ddi-verify --doctype flyer-a
RESOLVED  (method=doctype-direct)
  doctypes/flyer-a
    Display Name: Flyer A
    Keywords: flyer sheet
    Structure Key: struct-empty
  structures/struct-empty
    Display Name: Empty Structure
    Section Order: no section-order guidance for flyer-a
next: python3 scripts/preflight.py <rendered-file>  # verify fonts/DPI/print-boxes against this decision
```

Message appears exactly as ruled, in both text and `--json` output. Re-verify against
real data once `structures.csv` exists.

## Fix made

`skill/document-design-intelligence/scripts/resolve.py`: added `_field_value()`
(empty group-FK → named guidance message) and threaded `entry_key` through
`_print_resolved`/`_resolution_payload`. No change to the REFUSED PATH block — Q1
showed it already reports only the chosen path.

## Blocking data gaps (not fixed — `data/` out of scope)

1. `data/base/structures.csv` does not exist at all — blocks every doctype with a
   non-empty Structure Key from a full resolution, and blocks live verification of Q3.
2. `data/brand/` has no `ens` (or any) brand overlay — F1's two-pass brand test
   cannot be exercised; both passes silently degrade to the generic pass.

## Test count

`pytest -q` from the skill dir: **121 passed, 8 subtests passed** (was 119 + 8 — did
not go down).
