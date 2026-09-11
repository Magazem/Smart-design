# INDEPENDENT VERIFICATION — the dropped-columns defect

Verified 2026-09-11 by the Workflow Orchestrator (sub-manager) at the lead's request, before
the finding goes into research/51-invoked-quality.md. Reported by the Coverage and Gap Analyst
in research/handover-coverage-invoked-quality.md, finding A and finding B.

**VERDICT: CONFIRMED, end to end, and slightly WORSE than reported.**

This was verified the way this project requires — by looking at what the thing actually
PRINTED, not by reading the data or trusting the gate. The gate passes. The rows are
well-formed. The output is empty.

## What I ran

    python3 scripts/resolve.py --doctype cv-uk --json > /tmp/cvuk.json
    python3 scripts/ddi.py handoff --json /tmp/cvuk.json --format docx

Note for the next person: `python` does NOT work on this machine (uv trampoline, "entity not
found"). **`python3` does** — 3.12.10. This is a different trap from the wc -m one and cost a
few minutes; both are now written down.

## 1. The resolved JSON carries bare ids and nothing else

`resolved.headings` for cv-uk:

    [{"key": "contact-en-1"}, {"key": "contact-en-2"}, {"key": "contact-en-3"}, ...]

The union of all keys present across every heading entry is exactly `["key"]`. `Heading Text`
— the actual wording, the thing the 204 rows exist to carry — is not in the payload.

## 2. The docx handoff for a UK CV contains ZERO heading wording

Grepped the full handoff output for the authored wordings (`Work Experience`,
`Employment History`, `Professional Summary`): **0 matches.** The handoff carries page
geometry, fonts, sizes, TOC heading LEVELS and a palette, but no heading TEXT. The levels are
structural (`h1 -> HeadingLevel.HEADING_1`); they are not the words.

`ddi.py handoff` reads only the resolved JSON (`json.loads` at line 624) and touches no CSV
anywhere in the file. So there is no path by which `Heading Text` reaches a renderer. The
analyst's claim is exact.

## 3. The mechanism, confirmed in the manifest

`scripts/resolve.py:_display_columns` (line 500) returns an explicit `display_columns` list if
the table declares one; otherwise it falls back to searchable columns plus foreign-key source
columns. The `headings` entry in `data/schema-manifest.json` declares **no `display_columns`,
an empty `searchable_columns`, and empty `foreign_keys`**, so the fallback returns an empty
list and every row prints as its key alone.

## 4. Hidden-column census — computed, not estimated

Applying `_display_columns`' own logic to the manifest, counting data columns excluding each
table's key column:

| table | data cols | shown | hidden | hidden columns |
|---|---|---|---|---|
| headings | 4 | 0 | 4 | canonical_section, Heading Text, Language, Is Primary |
| structures | 8 | 2 | 6 | Heading Language, Heading Depth Max, TOC Depth, Front Matter Numbering, Caption Position, Cross-Ref Style |
| constraints | 7 | 3 | 4 | Applies To, Check, Threshold, Severity |
| type-scales | 5 | 3 | 2 | scale_key, Leading Ratio |

**headings shows NOTHING. Zero of four.**

## TWO CORRECTIONS TO THE REPORTED FINDING

1. **constraints loses four columns, not two.** The analyst named Threshold and Severity; the
   census also finds `Applies To` and `Check` hidden. A constraint therefore reaches the output
   without what it applies to, what it checks, its limit, or whether it fails or warns.

2. **There are TWO distinct sub-causes, not one, and they need different fixes.**
   - `headings` and `structures` declare **no `display_columns` at all** and fall through to an
     empty or near-empty default. The fix is to give them one.
   - `constraints` and `type-scales` **do declare `display_columns`** — they are among the six
     tables that have it — and the declared list is simply **incomplete**. The fix is to extend
     the existing list.
   Treating this as one uniform "add display_columns" fix would half-fix it. Say which table is
   in which class.

## FIX SITE
`research/build-manifest.py`. The manifest is GENERATED — `data/schema-manifest.json` must
never be hand-edited. Whoever fixes this edits the generator and regenerates.

## WHAT THIS MEANS FOR v0.3
v0.2.0's headline was 15 families with heading rows in three languages. 204 of those rows are
authored, validated, gated, shipped and unreachable by any output path. This is the exact
defect shape the 2026-09-10 lesson describes: valid data, exit 0, empty answer, green gate.
It is not covered by any known limitation in RELEASE-NOTES.md.

On the evidence this belongs ahead of description and activation work on the v0.3 critical
path. That call is the lead's and the user's, not mine.
