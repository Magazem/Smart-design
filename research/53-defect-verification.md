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

---

# ADDENDUM — verified against the PUBLISHED v0.2.0 ASSET, not a local build

The check above ran against the local `skill/dist/document-design-intelligence-0.0.1-dev.zip`,
which is what the Coverage analyst exercised. Matching six reference values (five row counts and
the description) is **necessary but not sufficient**: none of those six would catch a difference
in `resolve.py`, `ddi.py` or the manifest, and the defect is precisely in manifest and resolver
behaviour. So the local run could not, on its own, establish that the SHIPPED product is
affected. I downloaded the real asset and re-ran everything.

    gh release download v0.2.0 --repo Magazem/Smart-design --pattern "*.zip"
    # document-design-intelligence-0.2.0.zip, 143209 bytes, VERSION reads 0.2.0

## THE DEFECT REPRODUCES EXACTLY ON THE PUBLISHED ASSET

| check | published v0.2.0 |
|---|---|
| `resolved.headings` entries for cv-uk | 63 |
| union of keys across all entries | `['key']` — nothing else |
| docx handoff matches for the authored wordings | 0 |
| plain-text path | `headings/contact-en-1` … bare ids |
| manifest `headings.display_columns` | ABSENT |
| manifest `headings.searchable_columns` | `[]` |
| manifest `headings.foreign_keys` | `[]` |

Hidden-column census on the published manifest — identical to the local figures, including both
corrections:

    headings:     4 cols, 0 shown, 4 hidden -> canonical_section, Heading Text, Language, Is Primary
    structures:   8 cols, 2 shown, 6 hidden -> Heading Language, Heading Depth Max, TOC Depth,
                                               Front Matter Numbering, Caption Position, Cross-Ref Style
    constraints:  7 cols, 3 shown, 4 hidden -> Applies To, Check, Threshold, Severity
    type-scales:  5 cols, 3 shown, 2 hidden -> scale_key, Leading Ratio

**The severity stands. This is a P0 in the shipped product, not an artefact of a dev build.**

## THE PLAIN-TEXT PATH IS ALSO AFFECTED — so "unreachable by ANY path" is exact
`resolve.py` has two display call sites (lines 548 and 577). I checked both. The plain-text path
prints `headings/contact-en-1` and so on, bare ids, same as the JSON path. The claim does not
overstate.

## THE PROVENANCE GAP IS CLOSED — the two md5 differences are cosmetic
`data/schema-manifest.json` and `scripts/ddi.py` had different md5s between the published asset
and the local build, which is what made this check necessary. Both turn out to be non-semantic:

- **schema-manifest.json** — `diff` after `json.tool` normalisation is EMPTY. The difference is
  key order or whitespace only.
- **ddi.py** — byte-identical after stripping CR. Both md5 to `09317cf262d3d8f6e914d9411556949e`.
  The local copy carries 1899 CR bytes against the published 1209, a difference of exactly 690,
  matching the 690 lines in the file. The local working copy has CRLF where the published has LF
  on those lines.
- `scripts/resolve.py` and `data/base/headings.csv` were already md5-identical.

So the Coverage analyst's local results were sound. They just could not be shown to be sound
from the six values it checked, and the two files that differed were the two that mattered most.

## ONE LOOSE THREAD FOR THE LEAD, not a blocker
RESUME.md records of the published asset: "Zero CR bytes." The published `ddi.py` contains 1209
CR bytes. That earlier claim may have been scoped to `SKILL.md` rather than the whole archive,
or it may be wrong. **I am not asserting it is wrong** — I checked one member, not the archive.
Worth a recheck by whoever owns the packaging claims before it is relied on again.
