#!/usr/bin/env python3
"""W2 parity test -- resolved == emitted for every path-applicable column.

Two independent stages, both against the REAL production data (not a test
fixture), because the census this test enforces (research/66-column-census.md)
is about the real schema-manifest.json and the real scripts/ddi.py builders,
not a toy manifest.

STAGE 1 (CSV -> resolved): for every one of the 14 tables in
data/schema-manifest.json, the raw CSV header (read straight off
data/base/<table>.csv, not the generated manifest's `columns` list, so this
stays independent of research/build-manifest.py's own bookkeeping) minus that
table's renamed key column minus any declared exclusion must equal exactly
the columns resolve.py's own `_display_columns(spec)` exposes. Declared
exclusions come from a `DISPLAY_EXCLUSIONS` dict in research/build-manifest.py
(table -> {column: reason}); that file has top-level side effects (it writes
data/schema-manifest.json on import), so it is never imported -- it is parsed
with `ast` and the dict is read via `ast.literal_eval` if present, else
treated as empty. Per Manager D7 the policy is include-all (figures and
font-substitutes covered too, Brand Scope included); no exclusions are
expected today.

STAGE 2 (resolved -> emitted): for every table reachable by at least one
doctype's FK walk (12 of 14 -- figures and font-substitutes have no FK
pointing at them anywhere in the manifest, confirmed unreachable by
research/66 SS1-2) x each of the 4 handoff paths (docx, pptx, pdf, png), the
resolved columns minus any declared HANDOFF_EXCLUSIONS must equal exactly the
columns that path's builder actually reads. "Reads" means EITHER a `.get()`
call OR a `[]` subscript on a resolved row -- captured by wrapping every
resolved row in a dict subclass that records both (Manager D9). This wraps
`_constraints_and_preflight_lines` (ddi.py:371) too, not just the four
`_FORMAT_BUILDERS`, since it is a separate function `_build_handoff_lines`
(ddi.py:810-815) calls once per format alongside the per-format builder.
HANDOFF_VOCAB (ddi.py:208-262) is a name map only and is never read as an
applicability source here. Declared exclusions come from a
`HANDOFF_EXCLUSIONS` dict in scripts/ddi.py, shape
`{table_name: {path: {column: reason}}}`; ddi.py has no import-time side
effects (guarded by `if __name__ == "__main__":`) so it is read with
`getattr(ddi, "HANDOFF_EXCLUSIONS", {})` -- empty today.

COVERAGE (Manager D9): every one of the 30 doctypes in data/base/doctypes.csv
is resolved and every reachable table's resolved/read columns are UNIONED
across all of them, so a data-dependent branch (e.g. constraints' page-flow
lines, which only fire for a resolved constraint row whose Parameter names a
docx_property) is exercised by at least one doctype rather than missed by
picking a single representative. Measured at ~0.3s for all 30 doctypes on
this machine -- well under the ~30s budget -- so no doctype was dropped.
"""
from __future__ import annotations

import ast
import csv
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
SKILL_ROOT = SCRIPTS_DIR.parent
REPO_ROOT = SKILL_ROOT.parent.parent
DATA_DIR = SKILL_ROOT / "data"

sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "lib"))

import resolve  # noqa: E402
import ddi  # noqa: E402
import data as datalib  # noqa: E402

FORMATS = ("docx", "pptx", "pdf", "png")
BUILD_MANIFEST_PY = REPO_ROOT / "research" / "build-manifest.py"


class TrackedRow(dict):
    """dict subclass recording every key read off it via EITHER `.get()` or
    `[]`, into a shared set (Manager D9 -- a `[]` read must count the same as
    a `.get()` read, even though no current builder uses `[]`)."""

    def __init__(self, data, sink):
        super().__init__(data)
        object.__setattr__(self, "_sink", sink)

    def get(self, key, default=""):
        self._sink.add(key)
        return dict.get(self, key, default)

    def __getitem__(self, key):
        self._sink.add(key)
        return dict.__getitem__(self, key)


def _read_display_exclusions():
    """DISPLAY_EXCLUSIONS from research/build-manifest.py, read without
    importing it (it writes data/schema-manifest.json at import time with no
    `if __name__ == "__main__":` guard). Absent today -> {} for every table."""
    tree = ast.parse(BUILD_MANIFEST_PY.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "DISPLAY_EXCLUSIONS" for t in node.targets
        ):
            return ast.literal_eval(node.value)
    return {}


def _csv_header(filename):
    with open(DATA_DIR / "base" / filename, encoding="utf-8-sig", newline="") as f:
        return next(csv.reader(f))


def _all_doc_keys(tables):
    entry_name = datalib.entry_table_name(tables)
    key_column = tables[entry_name]["key_column"]
    problems = datalib.ProblemLog()
    rows = datalib.load_table_rows(DATA_DIR, tables[entry_name], problems, table_name=entry_name)
    return [r.get(key_column, "") for r in rows if r.get(key_column, "")]


def _resolved_json(doc_key):
    import io
    import json
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        code = resolve.main(["--doctype", doc_key, "--json", "--data-dir", str(DATA_DIR)])
    if code != 0:
        return None
    return json.loads(buf.getvalue())


class TestStage1CsvToResolved(unittest.TestCase):
    """CSV header minus the renamed key column minus declared exclusions ==
    resolve.py's own `_display_columns(spec)`, for all 14 tables."""

    @classmethod
    def setUpClass(cls):
        cls.manifest = datalib.load_manifest(DATA_DIR)
        cls.tables = cls.manifest["tables"]
        cls.exclusions = _read_display_exclusions()

    def test_every_table_display_columns_matches_csv_minus_key_minus_exclusions(self):
        for table_name, spec in sorted(self.tables.items()):
            with self.subTest(table=table_name):
                header = _csv_header(spec["filename"])
                key_column = spec["key_column"]
                declared_exclusions = set(self.exclusions.get(table_name, {}).keys())
                expected = {c for c in header if c != key_column} - declared_exclusions
                actual = set(resolve._display_columns(spec))
                self.assertEqual(
                    expected, actual,
                    f"{table_name}: CSV-header-minus-key-minus-exclusions != "
                    f"resolve.py display_columns -- missing {expected - actual}, "
                    f"extra {actual - expected}",
                )


class TestStage2ResolvedToEmitted(unittest.TestCase):
    """resolved columns minus declared HANDOFF_EXCLUSIONS == columns each
    path's builder actually reads, for every reachable table x path, unioned
    over every doctype (Manager D9 coverage)."""

    @classmethod
    def setUpClass(cls):
        cls.manifest = datalib.load_manifest(DATA_DIR)
        cls.tables = cls.manifest["tables"]
        cls.all_table_names = sorted(cls.tables.keys())
        cls.doc_keys = _all_doc_keys(cls.tables)
        cls.handoff_exclusions = getattr(ddi, "HANDOFF_EXCLUSIONS", {})
        cls.resolved_columns, cls.read_columns, cls.reachable = cls._collect()

    @classmethod
    def _collect(cls):
        payloads = []
        for doc_key in cls.doc_keys:
            payload = _resolved_json(doc_key)
            if payload is not None and payload.get("status") == "resolved":
                payloads.append(payload)

        resolved_columns = {t: set() for t in cls.all_table_names}
        reachable = {t: False for t in cls.all_table_names}
        for payload in payloads:
            for tname, rows in payload.get("resolved", {}).items():
                if rows:
                    reachable[tname] = True
                    for row in rows:
                        resolved_columns[tname].update(k for k in row.keys() if k != "key")

        read_columns = {(t, f): set() for t in cls.all_table_names for f in FORMATS}
        for payload in payloads:
            resolved = payload.get("resolved", {})
            language = payload.get("language", {})
            for table_name in cls.all_table_names:
                if not resolved.get(table_name):
                    continue
                for fmt in FORMATS:
                    sink = set()
                    tracked = {}
                    for tname, trows in resolved.items():
                        this_sink = sink if tname == table_name else set()
                        tracked[tname] = [TrackedRow(r, this_sink) for r in trows]
                    ddi._FORMAT_BUILDERS[fmt](tracked, language)
                    ddi._constraints_and_preflight_lines(tracked, fmt)
                    read_columns[(table_name, fmt)] |= sink

        return resolved_columns, read_columns, reachable

    def test_every_reachable_table_path_reads_all_non_excluded_resolved_columns(self):
        for table_name in self.all_table_names:
            if not self.reachable[table_name]:
                continue
            for fmt in FORMATS:
                with self.subTest(table=table_name, path=fmt):
                    excluded = set(
                        self.handoff_exclusions.get(table_name, {}).get(fmt, {}).keys()
                    )
                    resolved = self.resolved_columns[table_name]
                    expected = resolved - excluded
                    actual = self.read_columns[(table_name, fmt)] & resolved
                    self.assertEqual(
                        expected, actual,
                        f"{table_name}/{fmt}: resolved-minus-exclusions != read -- "
                        f"dropped {expected - actual}",
                    )


if __name__ == "__main__":
    unittest.main()
