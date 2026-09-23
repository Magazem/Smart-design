#!/usr/bin/env python3
"""Emit data/schema-manifest.json from research/09-library-schema.md Revision 4.

Runs from any cwd -- the default output path resolves relative to this script file;
an optional argv[1] overrides it (used by tests/test_schema_manifest.py).

One key is NOT from Revision 4: `distinct_token_columns`. Revision 4 does not describe it,
does not name it and rules nothing about it -- it was added at v0.2, after a repeated
`flyer a4` token in one `doctypes.Keywords` cell was found to double that term's retrieval
weight. Its provenance is this file plus `validate_data.py`, which implements the check, and
`data/schema-manifest-NOTES.md` section 1.5, which states the ruling. Treat the twelve
declarations below as authored here, not as transcribed from the schema, and do not
"reconcile" them against Revision 4 -- there is nothing there to reconcile with.
"""
import json, pathlib, re, sys

def group(table, column, is_list=False):
    """A foreign key whose target is a non-unique GROUPING column, not the target
    table's key_column (research/09 Revision 3, section 0.1.1 -- five of them).
    lib/data.py fk_spec() reads "group"; validate_data.py checks membership in
    that column rather than identity with that table's key."""
    spec = {"table": table, "column": column, "group": True}
    if is_list:
        spec["list"] = True
    return spec


FIELD_DIRECTION = ["expected", "customary", "neutral", "negative-signal", "contested"]
YN = ["yes", "no"]
YNA = ["yes", "no", "n/a"]

#: research/80-v05-plan.md §2A -- the 16 document families. One constant, shared by
#: `doctypes.Family` (catalogue grouping; HANDOFF_EXCLUSIONS on all 4 handoff paths --
#: see scripts/ddi.py, out of this generator's scope) and `designs.Family` (the family
#: each layout archetype belongs to). Filled in research/26.
FAMILIES = ["cv", "cover-letter", "letter", "memo", "form", "brochure", "flyer", "poster",
            "report", "whitepaper", "proposal", "quote", "invoice", "deck", "one-pager",
            "infographic"]

#: research/80-v05-plan.md §3 -- the evidence classes a designs/provenance row can carry,
#: in preference order (ranked > juried > authority > convention). Shared by
#: `designs."Evidence Class"` and `provenance."Evidence Class"`.
EVIDENCE_CLASSES = ["ranked", "juried", "authority", "convention"]

tables = {}

#: `display_columns` -- the columns a resolved row of this table SHOWS (resolve.py
#: `_display_columns`). Per Manager D7, the policy is include-all: every table exposes
#: every one of its own CSV columns (its key column excepted, since that is renamed to
#: `"key"` rather than dropped). `display_columns` is set for every table in the loop
#: below, right after all tables are defined, rather than hand-authored per table --
#: research/66's census found the old hand-authored-superset approach (a list written for
#: only the tables a handoff builder happened to read) silently dropped columns for six
#: other tables (`cv-regions`, `doc-reasoning`, `doc-styles`, `doctypes` had no declaration
#: at all; `typefaces`, `palettes`, `page-formats`, `render-targets` had one that was never
#: extended). Any future exclusion must be declared in `DISPLAY_EXCLUSIONS` below with a
#: reason string -- none is expected today.

tables["doctypes"] = {
    "filename": "doctypes.csv",
    "columns": ["doc_key", "Display Name", "Keywords", "Artifact Class", "Brand Scope",
                "Reasoning Key", "Page Format Key", "Render Target Keys",
                "Constraint Set Keys", "Structure Key", "Region Key", "Default Language",
                "Family"],
    "key_column": "doc_key",
    "role": "entry",
    # research/64 D-E: the language a doctype's document is normally authored in --
    # read the same generic way resolve.py already reads `description_column`
    # (resolve.py:653, `entry_spec.get("description_column", "Display Name")`).
    # Fixes the DOCTYPE, not the shared `structures."Heading Language"` constant:
    # several doctypes point at the same Structure Key (cv-experienced serves
    # cv-us through cv-gulf-gcc), so the authored language is a property of the
    # doctype, not of the section list it shares with six other doctypes.
    "language_column": "Default Language",
    # `Family` (research/80-v05-plan.md §2A): catalogue grouping used to pick a
    # doctype's `designs` rows (P1.2 loader task); non-nullable (no "" in the enum,
    # same idiom as every other required enum column here) and NOT in
    # `searchable_columns` -- it groups doctypes, it does not describe one for BM25.
    "enums": {"Artifact Class": ["canvas", "flow", "hybrid"],
              "Default Language": ["en", "fr", "de"],
              "Family": FAMILIES},
    "foreign_keys": {
        "Reasoning Key": "doc-reasoning.doc_category",
        "Page Format Key": "page-formats.page_format_key",
        "Structure Key": "structures.structure_key",
        "Render Target Keys": {"table": "render-targets", "column": "render_key", "list": True},
        "Constraint Set Keys": group("constraints", "Set Key", is_list=True),
        "Region Key": group("cv-regions", "region_key"),
    },
    # A `list: true` FK is declared HERE TOO. The FK checker splits the value and skips
    # empty tokens, so it can never see a leading/trailing/doubled `;` -- the
    # well-formedness loop is a separate pass over `list_columns` and is the only thing
    # that does. Proven by probe: a trailing `;` on this column moved the gate 82 -> 82,
    # the same malformation on a declared non-FK list column moved it 82 -> 83.
    # The four are LISTED, not derived, so adding a list FK stays an author decision;
    # the guard at the foot of this file makes forgetting one an error.
    "list_columns": {"Render Target Keys": ";", "Constraint Set Keys": ";"},
    # A cell in these columns must not repeat a token. `Keywords` is here and NOT in
    # `list_columns` on purpose: it is a `, `-separated search-token cell, not a `;`-list,
    # and the well-formedness loop's "no empty item" reading does not apply to it. What IS
    # true of it is that a repeated token silently doubles that term's BM25 frequency and
    # biases retrieval toward this row -- which is what `brochure-flyer-a4` (`flyer a4`
    # twice) did until v0.2. Declaring is per-column and opt-in because repetition is
    # legitimate in at least one list column (see `page-formats.Panels mm`).
    "distinct_token_columns": {"Keywords": ",", "Render Target Keys": ";",
                               "Constraint Set Keys": ";"},
    "searchable_columns": ["Display Name", "Keywords"],
    "typed_json_columns": [],
    "derived": [],
}

tables["doc-reasoning"] = {
    "filename": "doc-reasoning.csv",
    "columns": ["doc_category", "Style Key", "Palette Key", "Typeface Key",
                "Style Bias Terms", "Palette Bias Terms", "Typeface Bias Terms",
                "Doc Conditions", "Anti-Pattern Tokens", "Severity"],
    "key_column": "doc_category",
    "enums": {"Severity": ["fail", "warn"]},
    "foreign_keys": {
        "Style Key": "doc-styles.style_key",
        "Palette Key": "palettes.palette_key",
        "Typeface Key": "typefaces.typeface_key",
    },
    "list_columns": {"Anti-Pattern Tokens": ";"},
    "distinct_token_columns": {"Anti-Pattern Tokens": ";"},
    "searchable_columns": ["doc_category", "Style Bias Terms"],
    "typed_json_columns": [],
    "derived": [],
}

tables["doc-styles"] = {
    "filename": "doc-styles.csv",
    "columns": ["style_key", "Display Name", "Keywords", "Best For", "Not For",
                "Brand Scope", "Rule Hair pt", "Rule Strong pt", "Rule Brand pt",
                "Corner Radius mm", "Table Rules", "Table Fills", "Emphasis Mechanism",
                "Field Style", "Checklist"],
    "key_column": "style_key",
    "enums": {
        # `row-hairlines` added at A8: `hairline` alone was read by a renderer as
        # "box every cell" for `cv-dach-tabular` (research/72's judges, verbatim,
        # all three: fully boxed contact grid) despite the Checklist saying "row
        # padding rather than cell borders" -- the enum value itself carried no
        # semantic that ruled boxes out. `row-hairlines` states the DACH direction's
        # actual rule explicitly: horizontal separators between rows only, no
        # vertical rules, no cell boxes. `hairline` and `header-and-total` keep
        # their existing meanings (schema-manifest-NOTES.md documents all four).
        "Table Rules": ["hairline", "header-and-total", "none", "row-hairlines"],
        "Table Fills": ["none", "zebra", "header-only"],
        "Emphasis Mechanism": ["weight", "colour-text", "fill"],
        "Field Style": ["underline", "box", "none"],
    },
    "foreign_keys": {},
    "list_columns": {"Checklist": ";"},
    "distinct_token_columns": {"Checklist": ";"},
    "searchable_columns": ["Display Name", "Keywords", "Best For"],
    "typed_json_columns": [],
    "derived": [],
}

tables["palettes"] = {
    "filename": "palettes.csv",
    "columns": ["palette_key", "Display Name", "Keywords", "Brand Scope",
                "Primary", "On Primary", "Secondary", "On Secondary",
                "Accent", "On Accent", "Background", "Foreground", "Muted", "On Muted",
                "Rule Hair", "Rule Strong", "Rule Brand",
                "Text-Safe Roles", "Fill-Only Roles", "Category Marker Roles"],
    "key_column": "palette_key",
    "enums": {},
    "foreign_keys": {},
    "list_columns": {"Text-Safe Roles": ";", "Fill-Only Roles": ";",
                     "Category Marker Roles": ";"},
    "distinct_token_columns": {"Text-Safe Roles": ";", "Fill-Only Roles": ";",
                               "Category Marker Roles": ";"},
    "searchable_columns": ["Display Name", "Keywords"],
    "typed_json_columns": [],
    "derived": [
        {"check": "contrast_at_least", "column": "On Primary",
         "against_column": "Primary", "min_ratio": 4.5},
        {"check": "contrast_at_least", "column": "On Secondary",
         "against_column": "Secondary", "min_ratio": 4.5},
        {"check": "contrast_at_least", "column": "On Accent",
         "against_column": "Accent", "min_ratio": 4.5},
        {"check": "contrast_at_least", "column": "Foreground",
         "against_column": "Background", "min_ratio": 4.5},
        {"check": "contrast_at_least", "column": "On Muted",
         "against_column": "Muted", "min_ratio": 4.5},
    ],
}

tables["typefaces"] = {
    "filename": "typefaces.csv",
    "columns": ["typeface_key", "Display Name", "Keywords", "Best For", "Brand Scope",
                "Heading Family", "Body Family", "Mono Family", "Category Contrast",
                "Family Count", "Safe Stack Fallback", "Safe Stack Body Fallback",
                "Safe Stack Availability",
                "Embedding Licence", "Has Tabular Figures", "Scale Key"],
    "key_column": "typeface_key",
    "enums": {
        "Category Contrast": ["serif-sans", "sans-sans", "serif-serif", "superfamily"],
        "Safe Stack Availability": ["os-bundled", "office-bundled", "none"],
        "Embedding Licence": ["installable", "editable", "preview-print", "restricted", "unknown"],
        "Has Tabular Figures": ["yes", "unknown"],
    },
    "foreign_keys": {"Scale Key": group("type-scales", "scale_key")},
    "searchable_columns": ["Display Name", "Keywords", "Best For"],
    "typed_json_columns": [],
    # research/A4b: a single-family row (Family Count=1) has one real family,
    # so its heading and body safe-stack fallbacks can only legitimately be
    # the same string or the body cell left blank -- a single-family row
    # authoring a DIFFERENT body fallback would be a silent lie about what
    # font the body text falls back to.
    "derived": [
        {"check": "equal_or_blank_when", "column": "Safe Stack Body Fallback",
         "against_column": "Safe Stack Fallback", "when_column": "Family Count",
         "when_value": "1"},
    ],
}

tables["type-scales"] = {
    "filename": "type-scales.csv",
    "columns": ["scale_row_key", "scale_key", "Medium", "Role", "Size pt", "Leading Ratio"],
    "key_column": "scale_row_key",
    "enums": {
        "Medium": ["print", "projection", "screen"],
        # size-ordered, ascending; `legal` is the floor (schema Rev 4 T6 design note)
        "Role": ["legal", "label", "caption", "body", "body-dense", "lead", "h3", "h2", "h1"],
    },
    "foreign_keys": {},
    "searchable_columns": [],
    "typed_json_columns": [],
    "derived": [],
}

tables["page-formats"] = {
    "filename": "page-formats.csv",
    "columns": ["page_format_key", "Display Name", "Keywords", "Trim W mm", "Trim H mm",
                "Bleed mm", "Safe Margin mm", "Margin Top mm", "Margin Bottom mm",
                "Margin Inside mm", "Margin Outside mm", "Measure mm", "Columns",
                "Running Head", "Folio Style", "Fold Type", "Panels mm", "Stock gsm",
                "Print Mode", "Min DPI Raster", "Min DPI Line Art"],
    "key_column": "page_format_key",
    "enums": {
        "Running Head": ["none", "verso-recto", "centered"],
        "Folio Style": ["none", "arabic", "roman-front-arabic-body"],
        "Fold Type": ["none", "tri-fold", "z-fold", "gate-fold", "roll-fold"],
        "Print Mode": ["office", "photocopy", "professional"],
    },
    "foreign_keys": {},
    "list_columns": {"Panels mm": ";"},
    # NO `distinct_token_columns` entry for `Panels mm`, deliberately. It is a positional
    # sequence of panel widths, and equal panels are the normal case, not a defect:
    # `a4-trifold` is `99.5;99.5;98.0` and `letter-gatefold` is
    # `53.175;54.775;54.775;53.175`. A blanket "no repeated token in any list column"
    # rule would fail four correct rows here, which is why the check is opt-in.
    "searchable_columns": ["Display Name", "Keywords"],
    "typed_json_columns": [],
    "derived": [],
}

tables["render-targets"] = {
    "filename": "render-targets.csv",
    "columns": ["render_key", "Format", "Engine", "Engine Path", "Engine Min Version",
                "Engine Invocation", "Font Rule", "Supports Paged Media", "Supports Bleed",
                "Supports CMYK", "Print Tier Max", "Editable By Recipient", "Availability",
                "Fallback Render Key"],
    "key_column": "render_key",
    "enums": {
        "Format": ["pdf", "docx", "pptx", "png", "html"],
        "Font Rule": ["embed", "safe-stack", "inline-webfont"],
        "Supports Paged Media": YNA,
        "Supports Bleed": YNA,
        "Supports CMYK": YNA,
        "Print Tier Max": ["none", "submittable-rgb", "pdfx4-rgb", "cmyk-press"],
        "Editable By Recipient": YN,
        "Availability": ["preinstalled", "pip", "unverified"],
    },
    "foreign_keys": {"Fallback Render Key": "render-targets.render_key"},
    "searchable_columns": [],
    "typed_json_columns": [],
    "derived": [],
}

tables["constraints"] = {
    "filename": "constraints.csv",
    "columns": ["constraint_key", "Set Key", "Applies To", "Check", "Element Scope",
                "Parameter", "Threshold", "Severity"],
    "key_column": "constraint_key",
    "enums": {
        "Element Scope": ["", "body-paragraph", "table-cell", "caption-block",
                          "sidebar-column", "header-footer"],
        "Severity": ["fail", "warn"],
    },
    "foreign_keys": {},
    # `Threshold` is polymorphic (schema Revision 4 S0.1): a literal, OR a reference
    # `<manifest-table-name>:<Column Name>`. The pattern decides which, and a non-match
    # is SILENTLY a literal -- so it is tight on the left (a lowercase-letter table half
    # keeps the literal `16:9` out) and generous on the right (digits and hyphens, so a
    # future `page-formats:Trim W mm` resolves rather than being swallowed).
    # `Parameter` is a name=value map, not a list, and is deliberately not declared.
    "reference_columns": {
        "Threshold": {"pattern": "^[a-z][a-z-]*:[A-Za-z][A-Za-z0-9 -]*$",
                      "must_resolve": True},
    },
    "searchable_columns": [],
    "typed_json_columns": [],
    "derived": [],
}

tables["structures"] = {
    "filename": "structures.csv",
    "columns": ["structure_key", "Display Name", "Section Order", "Heading Language",
                "Heading Depth Max", "TOC Depth", "Front Matter Numbering",
                "Caption Position", "Cross-Ref Style"],
    "key_column": "structure_key",
    "enums": {
        "Heading Language": ["en", "fr", "de"],
        "Front Matter Numbering": ["none", "roman"],
        "Cross-Ref Style": ["numbered", "positional"],
    },
    "foreign_keys": {"Section Order": group("headings", "canonical_section", is_list=True)},
    "list_columns": {"Section Order": ";"},
    "distinct_token_columns": {"Section Order": ";"},
    "searchable_columns": ["Display Name"],
    "typed_json_columns": [],
    "derived": [],
}

tables["figures"] = {
    "filename": "figures.csv",
    "columns": ["chart_key", "Data Type", "Keywords", "Best Chart Type",
                "Secondary Options", "When to Use", "When NOT to Use",
                "Data Volume Threshold", "Accessibility Grade", "A11y Fallback",
                "Accessibility Notes", "Label Strategy", "Static Fallback",
                "Print Series Max", "Greyscale Safe", "Print Palette Roles",
                "Caption Required", "Caption Must State", "Anti-Patterns"],
    "key_column": "chart_key",
    "enums": {
        "Label Strategy": ["direct", "legend", "either"],
        "Greyscale Safe": ["yes", "needs-pattern", "no"],
        "Caption Required": YN,
        # Clean on 10 of 11 authored rows (`high` x5, `medium` x4, `low-medium` x1).
        # The eleventh, `tabular-lookup`, authored a 96-char sentence into it; the loader
        # normalises the cell to `high` and appends the sentence to `Accessibility Notes`,
        # exactly as it already does for `Caption Required` -> `Caption Must State`.
        "Accessibility Grade": ["high", "medium", "low-medium"],
    },
    "foreign_keys": {},
    # DO NOT declare `Anti-Patterns`, `Secondary Options`, `When NOT to Use` or
    # `Data Volume Threshold` as list columns. All four hold "; " as a SENTENCE
    # separator, not a delimiter -- cited prose, e.g. "3D bars (Tufte: ... chartjunk);
    # rainbow/spectral palette ...". A list check would PASS on them while meaning
    # something else. Schema Revision 4 erratum (09 S9) types all four `text`/`P`;
    # the same applies to cv-regions.`Language Expectation` below.
    # `Accessibility Notes` is the FIFTH column of this kind and the newest: at the
    # load-pass-3 erratum follow-on the loader began appending `; grade rationale: <...>`
    # to it, carrying `tabular-lookup`'s displaced Accessibility Grade sentence. That `; `
    # is a sentence separator too. Named here even though the column is left untyped in
    # 09 S9, precisely because an undeclared column acquiring a shape by accident is the
    # failure the erratum's own justification describes.
    "list_columns": {"Print Palette Roles": ";"},
    "distinct_token_columns": {"Print Palette Roles": ";"},
    "searchable_columns": ["Data Type", "Keywords", "Best Chart Type"],
    "typed_json_columns": [],
    "derived": [],
}

tables["cv-regions"] = {
    "filename": "cv-regions.csv",
    "columns": ["cv_region_key", "region_key", "Seniority Band", "Max Pages", "Photo",
                "Date of Birth", "Nationality", "Marital Status", "Visa Status",
                "Section Order", "Education Before Experience", "Format",
                "Language Expectation", "Evidence Class"],
    "key_column": "cv_region_key",
    "enums": {
        "Seniority Band": ["early", "experienced"],
        "Photo": FIELD_DIRECTION,
        "Date of Birth": FIELD_DIRECTION,
        "Nationality": FIELD_DIRECTION,
        "Marital Status": FIELD_DIRECTION,
        "Visa Status": FIELD_DIRECTION,
        "Education Before Experience": YN,
        "Format": ["reverse-chronological", "functional", "hybrid"],
        "Evidence Class": ["FACT", "CONVENTION", "CONTESTED"],
    },
    "foreign_keys": {"Section Order": group("headings", "canonical_section", is_list=True)},
    "list_columns": {"Section Order": ";"},
    "distinct_token_columns": {"Section Order": ";"},
    # DO NOT declare `Language Expectation` as a list column. 8 of 14 rows contain ";"
    # but they are clauses, not tokens ("English standard for multinational/private-sector
    # roles; Arabic for government/local-market roles"). Typed `text`/`P` by the schema
    # Revision 4 erratum (09 S9), same ruling as the four figures columns above.
    "searchable_columns": [],
    "typed_json_columns": [],
    "derived": [],
}

tables["headings"] = {
    "filename": "headings.csv",
    "columns": ["heading_key", "canonical_section", "Heading Text", "Language", "Is Primary"],
    "key_column": "heading_key",
    "enums": {"Language": ["en", "fr", "de"], "Is Primary": YN},
    "foreign_keys": {},
    "searchable_columns": [],
    "typed_json_columns": [],
    "derived": [],
}

tables["font-substitutes"] = {
    "filename": "font-substitutes.csv",
    "columns": ["substitute_key", "proprietary_family", "Substitute Family",
                "Lineage", "Licence", "Metric Identical", "Weights Covered"],
    "key_column": "substitute_key",
    "enums": {
        "Lineage": ["liberation", "croscore", "crosextra", "independent", "none"],
        "Licence": ["OFL-1.1", "Apache-2.0", "none"],
        "Metric Identical": ["", "yes", "no"],
    },
    "foreign_keys": {},
    "list_columns": {"Weights Covered": ";"},
    "distinct_token_columns": {"Weights Covered": ";"},
    "searchable_columns": [],
    "typed_json_columns": [],
    "derived": [],
}

tables["designs"] = {
    # research/80-v05-plan.md §2B / orchestrator ruling R-b: a "design" is a
    # `doc-reasoning` row, catalogued here per family so `ddi.py designs` can list,
    # rank and BM25-query them without walking `doc-reasoning` directly.
    "filename": "designs.csv",
    "columns": ["design_key", "Display Name", "Family", "Rank", "Reasoning Key",
                "Keywords", "Best For", "Not For", "Evidence Class", "Brand Scope"],
    "key_column": "design_key",
    "enums": {
        "Family": FAMILIES,
        # Evidence Class is non-nullable (no "" here): every design row is sourced
        # per §3, `convention` included -- it is a real (weakest) evidence class,
        # not an absence of one.
        "Evidence Class": EVIDENCE_CLASSES,
    },
    "foreign_keys": {"Reasoning Key": "doc-reasoning.doc_category"},
    # `Keywords` is a `, `-separated search-token cell, same shape and same
    # over-counting risk as `doctypes.Keywords` -- declared the same way, for the
    # same reason (see that column's comment above).
    "distinct_token_columns": {"Keywords": ","},
    "searchable_columns": ["Display Name", "Keywords", "Best For"],
    "typed_json_columns": [],
    "derived": [],
}

tables["provenance"] = {
    # research/80-v05-plan.md §2C / orchestrator ruling R-c: one provenance row per
    # source citing a designs/palettes/typefaces/doc-styles/doc-reasoning row.
    # Deliberately NOT FK-reachable from any other table (`Row Key` is a polymorphic
    # pointer resolved by `Table` + `Row Key` together, not a manifest `foreign_keys`
    # entry) -- checked instead by tests/test_provenance.py (P1.4), which is also
    # where the "every cited row has >=1 provenance row, ranked rows need URL/metric/
    # value/date, numeric Rank Value only when Fetch=fetched" rules from §2C live.
    # That deliberate non-reachability is recorded here too so a future FK-parity
    # sweep does not re-flag it as a gap (backlog item 6, §0 Facts found).
    "filename": "provenance.csv",
    "columns": ["prov_key", "Table", "Row Key", "Evidence Class", "Source Name",
                "Source URL", "Ranking Metric", "Rank Value", "Retrieved", "Fetch"],
    "key_column": "prov_key",
    "enums": {
        # The manifest's own table names, taken as of this point in the file --
        # i.e. every table declared above (`designs` included), not `provenance`
        # itself. A polymorphic `Table` cell can never legitimately name the
        # provenance table it lives in.
        "Table": sorted(tables.keys()),
        "Evidence Class": EVIDENCE_CLASSES,
        "Fetch": ["", "fetched", "search-corroborated"],  # blank only for convention (tests/test_provenance.py)
    },
    # `Row Key` is a polymorphic reference (resolved against whichever table `Table`
    # names), not a same-shaped `foreign_keys` entry -- see the table-level comment.
    "foreign_keys": {},
    "searchable_columns": [],
    "typed_json_columns": [],
    "derived": [],
}

#: DISPLAY_EXCLUSIONS -- table -> {column: reason}. The only place a column may be kept
#: out of `display_columns` (Manager D7's include-all policy). Read by
#: scripts/tests/test_column_parity.py (via `ast`, not import) to know which raw CSV
#: columns a table's resolved row is deliberately not showing. Empty today -- no
#: exclusion is expected; every column of every table (figures and font-substitutes
#: included, Brand Scope included) reaches resolve.py's resolved JSON.
DISPLAY_EXCLUSIONS = {}

for _name, _t in tables.items():
    _excluded = DISPLAY_EXCLUSIONS.get(_name, {})
    _t["display_columns"] = [c for c in _t["columns"]
                              if c != _t["key_column"] and c not in _excluded]

manifest = {"schemaVersion": 1, "tables": tables}

entry = [n for n, t in tables.items() if t.get("role") == "entry"]
assert entry == ["doctypes"], entry
for name, t in tables.items():
    assert t["key_column"] in t["columns"], name
    if "language_column" in t:
        assert t["language_column"] in t["columns"], (name, t["language_column"])
    for col in t["enums"]:
        assert col in t["columns"], (name, col)
    for col, ref in t["foreign_keys"].items():
        assert col in t["columns"], (name, col)
        tgt = ref["table"] if isinstance(ref, dict) else ref.split(".")[0]
        tgtcol = ref["column"] if isinstance(ref, dict) else ref.split(".")[1]
        assert tgt in tables, (name, tgt)
        if isinstance(ref, dict) and ref.get("group"):
            # A group FK targets a non-unique grouping column on purpose; the
            # only invariant left is that the column exists on the target.
            assert tgtcol in tables[tgt]["columns"], ("group FK column missing", name, ref)
        else:
            assert tables[tgt]["key_column"] == tgtcol, ("FK must target key column", name, ref)
    for col, delim in t.get("list_columns", {}).items():
        assert col in t["columns"], ("list_columns names no such column", name, col)
        assert delim == ";", (name, col, delim)
    # `distinct_token_columns` is INDEPENDENT of `list_columns`: it may name a column that
    # is not a `;`-list (doctypes.Keywords, delimiter `,`), and it may omit one that is
    # (page-formats.Panels mm, where repeats are correct). So the only guard it gets is
    # that the column exists and the delimiter is a single non-empty character.
    for col, delim in t.get("distinct_token_columns", {}).items():
        assert col in t["columns"], (
            "distinct_token_columns names no such column", name, col)
        assert isinstance(delim, str) and len(delim) == 1, (name, col, delim)
    # Every `list: true` FK must ALSO be declared in `list_columns`. This assertion
    # replaces its own inverse -- the old guard forbade the overlap, on the reading that
    # the FK checker "already splits" the column. It splits it and then skips the empty
    # tokens, so a malformed list passed both loops silently; the well-formedness check
    # ran on 8 non-FK list columns and 0 of the 4 FK ones. Declaring is the fix, and the
    # guard is inverted so the next list FK cannot be added without one.
    for col, ref in t["foreign_keys"].items():
        if isinstance(ref, dict) and ref.get("list"):
            assert col in t.get("list_columns", {}), (
                "a list FK must be declared in list_columns too, or its well-formedness "
                "is never checked", name, col)
    for col, ref in t.get("reference_columns", {}).items():
        assert col in t["columns"], ("reference_columns names no such column", name, col)
        assert "pattern" in ref, (name, col)
        re.compile(ref["pattern"])
    # `display_columns` overrides the default outright, so a name that does not exist here
    # does not fall back to anything -- it just never prints, which is the exact
    # silent-empty-field failure this key was added to end. Same idiom as the guards above.
    for col in t.get("display_columns", []):
        assert col in t["columns"], ("display_columns names no such column", name, col)
    for col in t["searchable_columns"]:
        assert col in t["columns"], (name, col)
    for d in t["derived"]:
        assert d["column"] in t["columns"] and d["against_column"] in t["columns"], name

out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "skill" / "document-design-intelligence" / "data" / "schema-manifest.json"
out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
n_fk = sum(len(t["foreign_keys"]) for t in tables.values())
n_group = sum(1 for t in tables.values() for r in t["foreign_keys"].values()
              if isinstance(r, dict) and r.get("group"))
n_list = sum(len(t.get("list_columns", {})) for t in tables.values())
n_ref = sum(len(t.get("reference_columns", {})) for t in tables.values())
n_distinct = sum(len(t.get("distinct_token_columns", {})) for t in tables.values())
n_display = sum(1 for t in tables.values() if "display_columns" in t)
print("wrote %s -- %d tables, %d columns, %d foreign keys (%d group), "
      "%d list columns, %d reference columns, %d distinct-token columns, "
      "%d tables with display_columns"
      % (out, len(tables), sum(len(t["columns"]) for t in tables.values()), n_fk, n_group,
         n_list, n_ref, n_distinct, n_display))
