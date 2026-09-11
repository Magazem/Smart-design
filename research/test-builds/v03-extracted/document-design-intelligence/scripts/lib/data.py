#!/usr/bin/env python3
"""Manifest-driven data loader -- shared by validate_data.py and resolve.py.

This is the ONE place that reads `data/schema-manifest.json` and merges
`data/base/<table>.csv` with every `data/brand/<slug>/<table>.csv` overlay.
`validate_data.py` uses it to check the data; `resolve.py` uses the exact
same function to load it at runtime, so there is no second implementation
of "what does base+brand merging mean" to drift out of sync -- the resolver
literally cannot see a merged row shape the validator didn't already check.

MANIFEST FORMAT (data/schema-manifest.json) -- see validate_data.py's module
docstring for the full field-by-field description; the one field this
module (not validate_data.py) gives special meaning to:

    "tables": {
      "<table_name>": {
        ...,
        "role": "entry"    # optional; exactly one table in a real manifest
      }                    # should carry this -- it's resolve.py's single
    }                      # fuzzy-search entry point (research/09's T1).
"""
from __future__ import annotations

import ast
import csv
import json
import sys
from pathlib import Path


def _assert_stdlib_only(extra_allowed=()):
    """Fail loudly at import time if a non-stdlib import is ever added here.

    See fonts.py for the identical guard and rationale.
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


_assert_stdlib_only()


_UTF8_BOM = b"\xef\xbb\xbf"


class ProblemLog:
    """Collects `file:row:column: message` problem lines in report order.

    Each entry also carries a `tier` (1 = structural, whole-dataset-untrust
    -- bad manifest, missing/malformed file, header mismatch, duplicate
    key; 2 = row-level -- bad enum/FK/reference/derived-check value on one
    row) plus, for tier 2, the `table`/`key` of the row the problem was
    found on -- this is what lets a caller (resolve.py, ddi.py check)
    degrade per-key instead of refusing the whole dataset on any problem.
    `tier` defaults to 1 because every existing call site (manifest-level
    and file-level checks) is structural; only validate_data.py's per-row
    checks pass tier=2 explicitly.
    """

    def __init__(self):
        self.lines = []
        self.entries = []

    def add(self, file, message, row=None, column=None, tier=1, table=None, key=None):
        loc = str(file)
        if row is not None:
            loc += f":{row}"
        if column is not None:
            loc += f":{column}"
        line = f"{loc}: {message}"
        self.lines.append(line)
        self.entries.append({"line": line, "tier": tier, "table": table, "key": key})

    def __bool__(self):
        return bool(self.lines)

    def __len__(self):
        return len(self.lines)


def fk_spec(raw):
    """Normalize a manifest foreign-key entry to (table, column, is_list, is_group).

    Three accepted shapes:
      "table.column"                                       single value, key lookup
      {"table":.., "column":.., "list": true}               ;-list, key lookup
      {"table":.., "column":.., "group": true}              single value, GROUP
                                                             membership: the value must
                                                             appear somewhere in that
                                                             column, which need not be
                                                             unique (unlike key_column)
      {"table":.., "column":.., "group": true, "list": true}  ;-list, group membership

    "group" exists for FKs whose real target is a non-unique grouping column
    (research/09 Revision 2, e.g. doctypes."Constraint Set Keys" ->
    constraints."Set Key" -- many constraint rows share one Set Key). A plain
    key lookup cannot express "must exist in that column", only "must exist
    as that table's key" -- that is what "group" adds.
    """
    if isinstance(raw, str):
        table, _, column = raw.partition(".")
        return table, column, False, False
    return (raw["table"], raw["column"],
            bool(raw.get("list", False)), bool(raw.get("group", False)))


def load_manifest(data_dir):
    """Parse data/schema-manifest.json. Raises OSError or
    json.JSONDecodeError on failure -- callers decide how to report that
    (validate_data.py turns it into a problem line; resolve.py refuses to
    start)."""
    manifest_path = Path(data_dir) / "schema-manifest.json"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def entry_table_name(tables_spec):
    """Return the single table name whose spec declares `"role": "entry"`.

    Raises ValueError if zero or more than one table claims that role --
    the resolver's one fuzzy-search entry point must be unambiguous, and
    this is the one place that invariant is enforced, so both
    validate_data.py (as a manifest-level check) and resolve.py (which
    calls this directly) see the same failure mode.
    """
    entries = [name for name, spec in tables_spec.items() if spec.get("role") == "entry"]
    if len(entries) != 1:
        raise ValueError(
            f"manifest must declare exactly one table with \"role\": \"entry\", "
            f"found {len(entries)}: {entries}"
        )
    return entries[0]


def read_csv_rows(path, problems):
    """Return (header, data_rows) as lists of raw strings, after checking
    the file is UTF-8 without a BOM. Returns (None, None) on a hard read
    failure (missing file, BOM, invalid UTF-8, no header row at all) --
    callers must treat that as "this file contributes zero rows", the
    problem is already logged."""
    try:
        raw = path.read_bytes()
    except OSError as exc:
        problems.add(path, f"cannot read file: {exc}")
        return None, None

    if raw.startswith(_UTF8_BOM):
        problems.add(path, "UTF-8 BOM present -- file must be UTF-8 without BOM")
        return None, None

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        problems.add(path, f"not valid UTF-8: {exc}")
        return None, None

    rows = list(csv.reader(text.splitlines()))
    if not rows:
        problems.add(path, "empty file, no header row")
        return None, None
    return rows[0], rows[1:]


def check_header(path, header, expected, problems):
    if header == expected:
        return True
    missing = [c for c in expected if c not in header]
    extra = [c for c in header if c not in expected]
    detail = []
    if missing:
        detail.append(f"missing {missing}")
    if extra:
        detail.append(f"extra {extra}")
    if not missing and not extra:
        detail.append(f"wrong order -- expected {expected}, got {header}")
    problems.add(path, "header mismatch: " + "; ".join(detail))
    return False


def load_table_rows(data_dir, spec, problems, table_name=None):
    """Load base + every brand overlay for one table into a flat list of
    dict rows (each carrying its own __file__/__row__ for problem
    reporting), enforcing header exactness and cross-source key collisions
    as it goes, and setting `Brand Scope` from the brand directory name
    (not from whatever the CSV itself says) on every brand-sourced row.
    Returns the merged row list.

    A missing base file is tier 1 (whole-dataset refusal) only for the
    entry table -- resolve.py cannot even start Stage 1 without it. For
    any other table it is tier 2: the table simply contributes zero rows,
    which the per-row foreign-key check already turns into a named,
    per-referencing-row problem (see validate_data.py's `_validate_rows`)
    -- exactly the "unauthored table" case this per-key degradation exists
    for (research/brief-mechanism-perkey.md)."""
    data_dir = Path(data_dir)
    filename = spec["filename"]
    columns = spec["columns"]
    key_column = spec.get("key_column")
    has_brand_scope = "Brand Scope" in columns

    combined = []
    key_origin = {}  # key value -> "file:row" it was first seen at

    base_path = data_dir / "base" / filename
    if not base_path.exists():
        tier = 1 if spec.get("role") == "entry" else 2
        problems.add(base_path, "declared in manifest but file does not exist",
                     tier=tier, table=table_name)
    else:
        header, rows = read_csv_rows(base_path, problems)
        if header is not None and check_header(base_path, header, columns, problems):
            for line_no, row in enumerate(rows, start=2):
                record = dict(zip(columns, row))
                record["__file__"], record["__row__"] = base_path, line_no
                if key_column:
                    key_val = record.get(key_column, "")
                    origin = key_origin.get(key_val)
                    if origin is not None:
                        problems.add(base_path,
                                     f"duplicate key '{key_val}' (already defined at {origin})",
                                     row=line_no, column=key_column)
                        continue
                    key_origin[key_val] = f"{base_path}:{line_no}"
                combined.append(record)

    brand_root = data_dir / "brand"
    if brand_root.is_dir():
        for brand_dir in sorted(p for p in brand_root.iterdir() if p.is_dir()):
            brand_path = brand_dir / filename
            if not brand_path.exists():
                continue  # a brand need not override every table
            header, rows = read_csv_rows(brand_path, problems)
            if header is None or not check_header(brand_path, header, columns, problems):
                continue
            for line_no, row in enumerate(rows, start=2):
                record = dict(zip(columns, row))
                if has_brand_scope:
                    record["Brand Scope"] = brand_dir.name
                record["__file__"], record["__row__"] = brand_path, line_no
                if key_column:
                    key_val = record.get(key_column, "")
                    origin = key_origin.get(key_val)
                    if origin is not None:
                        problems.add(brand_path,
                                     f"duplicate key '{key_val}' (already defined at {origin})",
                                     row=line_no, column=key_column)
                        continue
                    key_origin[key_val] = f"{brand_path}:{line_no}"
                combined.append(record)

    return combined


def load_all_tables(data_dir, tables_spec, problems):
    """Load every table declared in the manifest. Returns {table_name:
    [row dicts]} -- the same merged, brand-scoped, collision-checked shape
    `load_table_rows` produces, for every table at once."""
    return {name: load_table_rows(data_dir, spec, problems, table_name=name)
            for name, spec in tables_spec.items()}


def keys_by_table(tables_spec, all_rows):
    """Return {table_name: {key values}} for every table that declares a
    key_column -- used for foreign-key resolution (both the validator's FK
    integrity check and the resolver's FK walk read this same shape)."""
    result = {}
    for name, spec in tables_spec.items():
        key_column = spec.get("key_column")
        if key_column:
            result[name] = {r.get(key_column, "") for r in all_rows[name]}
    return result


def column_values(rows, column):
    """Every non-empty value that appears anywhere in `column` across
    `rows` -- the membership set a "group" foreign key checks against
    (fk_spec's `is_group`), as opposed to `keys_by_table`'s unique-key set."""
    return {v for v in (r.get(column, "") for r in rows) if v}
