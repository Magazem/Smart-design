#!/usr/bin/env python3
"""Manifest-driven build-time data validator -- the release.yml gate.

Usage: python3 validate_data.py <path-to-data/base>

(Argument is the `base/` directory, matching the existing release.yml call
-- `data/schema-manifest.json` and `data/brand/` are found as
`<base>/../schema-manifest.json` and `<base>/../brand/`, i.e. siblings of
`base/` under the same `data/` root. This preserves the CI workflow's
existing invocation with no change needed there.)

The real schema (research/09-library-schema.md, revision pending) is
unknown to this file by design: table names, columns, enums, foreign keys
and derived checks are all read from `data/schema-manifest.json` at
runtime, not hard-coded here. That's the point -- this harness validates
whatever manifest+CSVs exist today (an example two-toy-table manifest ships
so the tests are real), and the real schema drops in tomorrow as *data*,
with no code change to this file. See MANIFEST FORMAT below for exactly
what a manifest entry must declare, and the "what the manifest needs from
the schema author" note in this project's PR description / task report for
the version of this file that shipped it.

The base+brand loading mechanics (header exactness, key-collision
detection, Brand Scope from directory) live in lib/data.py -- resolve.py
uses that exact same loader at runtime, so this file and the resolver can
never disagree about what a "row" is.

MANIFEST FORMAT (data/schema-manifest.json):
    {
      "schemaVersion": 1,
      "tables": {
        "<table_name>": {
          "filename": "<table_name>.csv",
          "columns": ["col1", "col2", ...],              # exact header, in order
          "key_column": "col1",                            # primary key column
          "role": "entry",                                  # optional -- exactly ONE table in
                                                             # the whole manifest may carry this;
                                                             # it's resolve.py's single fuzzy-
                                                             # search entry point (research/09's
                                                             # T1). Omit on every other table.
          "enums": {"col2": ["value-a", "value-b"]},        # optional
          "foreign_keys": {                                 # optional
            "col3": "other_table.other_key_column",
            "col4": {"table": "other_table", "column": "other_key_column", "list": true},
            "col5": {"table": "other_table", "column": "grouping_column", "group": true}
          },
          "distinct_token_columns": {"col6": ";",             # optional -- a delimited cell in
                                     "col2": ","},             # one of these columns may not
                                                               # repeat a token. INDEPENDENT of
                                                               # `list_columns`: opt-in per
                                                               # column, any single-character
                                                               # delimiter
          "list_columns": {"col6": ";"},                    # optional -- `;`-list columns to
                                                             # check for well-formedness (no
                                                             # empty items). Declare a `list`
                                                             # FK here TOO: the FK loop splits
                                                             # the value but skips empty
                                                             # tokens, so only this loop can
                                                             # see a stray/doubled `;`
          "reference_columns": {                            # optional -- a column that is
            "col7": {"pattern": "^[a-z-]+:[A-Za-z ]+$",      # EITHER a literal (anything not
                     "must_resolve": true}                   # matching `pattern`) OR a
          },                                                 # "table:column" reference that,
                                                             # if `must_resolve`, must name an
                                                             # existing table + one of its
                                                             # declared columns
          "searchable_columns": ["col1", "col2"],           # optional, informational only --
                                                             # not checked by this harness, but
                                                             # required so a future search-index
                                                             # builder doesn't need a second pass
                                                             # over the manifest's intent
          "typed_json_columns": ["col5"],                   # optional -- cells allowed to hold
                                                             # a JSON object/array (Rule 1's one
                                                             # named exception, see below)
          "derived": [                                      # optional
            {"check": "contrast_at_least", "column": "On Primary",
             "against_column": "Primary", "min_ratio": 4.5}
          ]
        }
      }
    }

A foreign-key value is one of three shapes:
  - the string "table.column" -- single value, looked up against the target
    table's key_column (must be unique there)
  - {"table":.., "column":.., "list": true} -- a `;`-separated multi-value
    FK column (research/09's `Render Target Keys`-style columns), each
    token looked up the same way
  - {"table":.., "column":.., "group": true} -- the value must appear
    SOMEWHERE in that column, which need NOT be unique (research/09
    Revision 2's shape: many rows sharing one grouping value, e.g.
    `constraints."Set Key"` -- a plain key lookup cannot express this,
    "the value is a member of this column" is a different check than
    "the value is this table's key"). Composable with "list": true for a
    `;`-separated list of group memberships.

`reference_columns`' `pattern` is matched against the RAW cell value; a
value that doesn't match is assumed to be a literal and is not checked at
all (e.g. a numeric threshold isn't a table reference). A value that does
match is split on the FIRST `:` into (table, column); if `must_resolve` is
true (the default), that table must exist in the manifest and that column
must be one of its declared `columns` -- this checks the reference is
STRUCTURALLY valid, not that every row actually has a value there.

CHECKS (all per the task's brief; this harness fails closed -- any problem
found means a nonzero exit, this file never silently drops a check):
  - exactly one table declares `"role": "entry"` -- resolve.py depends on
    this being unambiguous; checked here so a bad manifest never reaches it
  - the base file for every manifest table exists (a manifest that declares
    a table with no `data/base/<file>` at all is itself a failure -- a
    schema author's typo or an accidentally-unshipped file must not pass
    silently)
  - header exactness: the CSV's first row must equal `columns` exactly,
    same names, same order -- any diff (missing / extra / reordered) fails
    with the diff shown
  - UTF-8 without a BOM (checked before anything else touches the bytes)
  - enum membership: every value in an enum column must be one of the
    declared allowed values (empty string is only valid if explicitly
    listed in `enums[column]` -- no implicit "blank is fine" exception)
  - foreign-key integrity: a non-empty FK value must match, byte-for-byte,
    either an existing key in the referenced table's key column (plain/list
    FKs), or an existing VALUE anywhere in the referenced grouping column
    (group FKs) -- built from that table's own base+brand rows either way.
    An empty FK value is treated as "nullable, no reference" and skipped --
    matching this schema's own nullable Style/Palette/Typeface Key design.
  - list_columns well-formedness: a non-empty value in a declared
    `list_columns` entry must not split into any empty item -- no leading,
    trailing, or doubled delimiter. This is a shape check only; it does not
    know what a "correct" item looks like, only that a `;`-list isn't
    missing pieces.
  - distinct_token_columns: a non-empty value in a declared column, split
    on that column's delimiter and stripped, must not contain the same
    token twice. Deliberately NOT derived from `list_columns`, in both
    directions. It covers `doctypes.Keywords`, which is a `, `-separated
    search-token cell and no kind of `;`-list, because a repeated keyword
    doubles that term's frequency and quietly biases retrieval toward the
    row carrying the accidental repeat. It does NOT cover
    `page-formats.Panels mm`, which IS a declared list column but is a
    positional sequence of panel widths where equal panels are correct
    (`a4-trifold` is `99.5;99.5;98.0`). Repetition is a defect in a set and
    normal in a sequence, and only the schema author knows which a column
    is, so this is declared per column rather than inferred.
  - reference_columns: see the format note above -- a value matching the
    declared `pattern` must name a real table and one of its declared
    columns.
  - no cell holds untyped JSON: a cell whose value starts with `{` or `[`
    fails, unless its column is listed in that table's
    `typed_json_columns` -- this is the schema's Rule 1 ("no cell may
    contain logic") made mechanical rather than a review-time convention.
  - the one derived check implemented: `contrast_at_least` -- WCAG contrast
    (via lib/color.py, the exact formula ported from this project's own
    upstream research) between two named columns must clear a minimum
    ratio. BLANK HANDLING, and it is deliberately not the same as an FK's:
    the pair is skipped only when BOTH cells are empty (the row does not
    define that colour role -- `palettes.mono-ink` ships `Accent`/`On
    Accent` blank on purpose), and a pair with EXACTLY ONE cell empty still
    fails, because an ink with no ground is an authoring bug, not an
    omission. So a blank FK is skipped one cell at a time while a contrast
    rule is skipped only pairwise. Declared here and in research/09-library-
    schema.md T4 so neither behaviour is folklore.
  - brand overlay merge: every `data/brand/<slug>/<table>.csv` present is
    loaded as additional rows for that table (only if the table declares a
    `Brand Scope` column -- its value is *set* to `<slug>` for every row
    loaded from that directory, overwriting whatever the CSV itself says,
    since the directory a row lives in is the authoritative signal for
    which brand it belongs to, not free text a contributor could get
    wrong). A brand row's key colliding with an existing key -- from base OR
    from an earlier-processed brand -- is a hard failure, not a silent
    override (see data/brand/README.md for the resulting contract).

Every problem is printed as one line, `file:row:column: message` (row
counts the header as row 1, so "row 2" is the first data row -- matching
what you'd see opening the CSV in a plain text editor), a summary count,
then exit 1. A clean run prints one "OK: ..." line and exits 0.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path


def _assert_stdlib_only(extra_allowed=()):
    """Fail loudly at import time if a non-stdlib import is ever added here.

    `extra_allowed` permits importing this project's own sibling stdlib-only
    lib/ modules without weakening the check for any genuine third-party
    package.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    allowed = set(sys.stdlib_module_names) | set(extra_allowed)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level or node.module is None:
                continue
            names = [node.module.split(".")[0]]
        else:
            continue
        for name in names:
            if name not in allowed:
                raise AssertionError(
                    f"non-stdlib import '{name}' found in {__file__} -- "
                    "this module must be Python stdlib only"
                )


_assert_stdlib_only(extra_allowed={"color", "data"})

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import color  # noqa: E402
import data as datalib  # noqa: E402


_JSON_CELL_RE = re.compile(r"^\s*[\{\[]")


def _validate_rows(table_name, spec, rows, all_keys, all_rows, tables, problems):
    """Row-level checks -- every problem raised here is tier 2 (per-key
    degradation, see research/brief-mechanism-perkey.md): each is tagged
    with the OFFENDING row's own key (the row a caller must refuse to
    resolve through), not the table it happens to point at, so a caller
    can name exactly which resolution path is broken and let every other
    row answer normally."""
    columns = spec["columns"]
    key_column = spec.get("key_column")
    enums = spec.get("enums", {})
    foreign_keys = spec.get("foreign_keys", {})
    typed_json_columns = set(spec.get("typed_json_columns", []))
    list_columns = spec.get("list_columns", {})
    distinct_token_columns = spec.get("distinct_token_columns", {})
    reference_columns = spec.get("reference_columns", {})
    derived = spec.get("derived", [])

    for record in rows:
        file, row_no = record["__file__"], record["__row__"]
        row_key = record.get(key_column, "") if key_column else None

        def _add(message, column=None):
            problems.add(file, message, row=row_no, column=column,
                         tier=2, table=table_name, key=row_key)

        for column, allowed in enums.items():
            value = record.get(column, "")
            if value not in allowed:
                _add(f"'{value}' not in allowed enum {allowed}", column=column)

        for column, raw_spec in foreign_keys.items():
            ref_table, ref_column, is_list, is_group = datalib.fk_spec(raw_spec)
            value = record.get(column, "")
            if not value:
                continue  # nullable FK, no reference to check
            tokens = [t.strip() for t in value.split(";")] if is_list else [value]
            if is_group:
                # Group FK: the value must appear SOMEWHERE in ref_column,
                # which need not be unique -- not "be that table's key".
                valid_values = datalib.column_values(all_rows.get(ref_table, []), ref_column)
            else:
                valid_values = all_keys.get(ref_table, set())
            for token in tokens:
                if token and token not in valid_values:
                    _add(f"'{token}' does not resolve to {ref_table}.{ref_column}", column=column)

        for column, delimiter in list_columns.items():
            value = record.get(column, "")
            if not value:
                continue
            parts = value.split(delimiter)
            if any(part == "" for part in parts):
                _add(f"malformed {delimiter!r}-delimited list (empty item): {value!r}", column=column)

        for column, delimiter in distinct_token_columns.items():
            value = record.get(column, "")
            if not value:
                continue
            seen, repeated = set(), []
            for token in (part.strip() for part in value.split(delimiter)):
                if not token:
                    continue  # empty items are the list_columns loop's problem, not this one
                if token in seen and token not in repeated:
                    repeated.append(token)
                seen.add(token)
            for token in repeated:
                _add(f"duplicate token {token!r} in {delimiter!r}-delimited list", column=column)

        for column, ref_spec in reference_columns.items():
            value = record.get(column, "")
            if not value:
                continue
            pattern = ref_spec.get("pattern")
            if pattern and not re.match(pattern, value):
                continue  # doesn't look like a reference -> treated as a literal
            if not ref_spec.get("must_resolve", True):
                continue
            ref_table, _sep, ref_column = value.partition(":")
            target_spec = tables.get(ref_table)
            if target_spec is None:
                _add(f"reference '{value}' names unknown table '{ref_table}'", column=column)
            elif ref_column not in target_spec.get("columns", []):
                _add(f"reference '{value}' names unknown column '{ref_column}' on table '{ref_table}'",
                     column=column)

        for column in columns:
            if column in typed_json_columns:
                continue
            value = record.get(column, "")
            if _JSON_CELL_RE.match(value):
                _add(f"cell looks like untyped JSON ('{value[:40]}') -- "
                     "logic does not belong in a cell (schema Rule 1)", column=column)

        for rule in derived:
            if rule.get("check") != "contrast_at_least":
                continue  # only kind implemented, per the task brief
            fg_col, bg_col = rule["column"], rule["against_column"]
            fg, bg = record.get(fg_col, ""), record.get(bg_col, "")
            if not fg and not bg:
                # BOTH cells empty -> the row does not define this colour role at
                # all, so there is no pair to rate. Same reading as the nullable-FK
                # skip above: absent is not wrong. `palettes.mono-ink` ships
                # `Accent`/`On Accent` blank deliberately and is the schema's own
                # generic worked example (research/09-library-schema.md T4).
                # Exactly ONE cell empty is NOT skipped -- a half-filled pair is an
                # authoring bug (an ink with no ground, or a ground with no ink) and
                # must still fail below. The asymmetry is declared in T4's
                # "Blank cells" note and in this file's CHECKS list.
                continue
            try:
                ratio = color.contrast_ratio(fg, bg)
            except ValueError as exc:
                _add(f"cannot compute contrast: {exc}", column=fg_col)
                continue
            min_ratio = rule.get("min_ratio", 4.5)
            if ratio < min_ratio - 1e-9:
                _add(f"contrast {ratio:.2f}:1 against {bg_col} '{bg}' is below "
                     f"required {min_ratio}:1", column=fg_col)


def _collect(data_dir):
    """Shared collection step behind both `validate()` and
    `validate_tiered()` -- the one place manifest+data loading and every
    check happens, so the two entry points can never see a different
    picture of what's wrong. Returns (problems, summary) on success (even
    if `problems` is non-empty), or (None, [early_failure_line]) if the
    manifest itself couldn't be read at all (too broken to run any
    per-table check against)."""
    data_dir = Path(data_dir)
    manifest_path = data_dir / "schema-manifest.json"
    try:
        manifest = datalib.load_manifest(data_dir)
    except OSError as exc:
        return None, [f"{manifest_path}: cannot read manifest: {exc}"]
    except json.JSONDecodeError as exc:
        return None, [f"{manifest_path}: invalid JSON: {exc}"]

    tables = manifest.get("tables", {})
    if not tables:
        return None, [f"{manifest_path}: manifest declares no tables"]

    problems = datalib.ProblemLog()
    try:
        datalib.entry_table_name(tables)
    except ValueError as exc:
        problems.add(manifest_path, str(exc))  # tier 1: default

    all_rows = datalib.load_all_tables(data_dir, tables, problems)
    all_keys = datalib.keys_by_table(tables, all_rows)

    for name, spec in tables.items():
        _validate_rows(name, spec, all_rows[name], all_keys, all_rows, tables, problems)

    total_rows = sum(len(v) for v in all_rows.values())
    summary = f"OK: validated {len(tables)} table(s), {total_rows} row(s)"
    return problems, summary


def validate(data_dir):
    """Run every check against `data_dir` (the directory containing
    schema-manifest.json, base/, and brand/). Returns (ok: bool,
    problem_lines: list[str], summary: str). This is the strict,
    all-problems-fail gate (the release.yml build-time check, and every
    build_zip.py/make_brand_kit.py caller that wants a single yes/no) --
    unchanged by the per-key degradation ruling. See `validate_tiered` for
    the two-tier version resolve.py/ddi.py's runtime checks use instead."""
    problems, early_or_summary = _collect(data_dir)
    if problems is None:
        return False, early_or_summary, ""
    return not problems, problems.lines, early_or_summary


def validate_tiered(data_dir):
    """Two-tier version of the same checks (research/brief-mechanism-
    perkey.md): tier 1 (structural -- bad manifest, missing/malformed
    file, header mismatch, duplicate key) still means the whole dataset
    can't be trusted; tier 2 (row-level -- bad enum/FK/reference/derived
    value on one row) is returned per-key instead of failing the run, so a
    caller can refuse only the resolution paths that touch a broken key.

    Returns (tier1_ok: bool, tier1_lines: list[str],
    tier2_entries: list[{"table", "key", "line"}], summary: str).
    """
    problems, early_or_summary = _collect(data_dir)
    if problems is None:
        return False, early_or_summary, [], ""
    tier1_lines = [e["line"] for e in problems.entries if e["tier"] == 1]
    tier2_entries = [e for e in problems.entries if e["tier"] == 2]
    return not tier1_lines, tier1_lines, tier2_entries, early_or_summary


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print("usage: validate_data.py <path-to-data/base>")
        return 2

    base_dir = Path(argv[0])
    data_dir = base_dir.parent

    ok, problem_lines, summary = validate(data_dir)
    for line in problem_lines:
        print(line)

    if not ok:
        print(f"\n{len(problem_lines)} problem(s) found")
        return 1

    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
