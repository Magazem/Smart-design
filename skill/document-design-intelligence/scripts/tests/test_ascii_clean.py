#!/usr/bin/env python3
"""Regression guard: every string literal and docstring in the CLIs and
lib/ modules must be pure ASCII.

Non-ASCII punctuation (em dash, section sign, middle dot, curly quotes...)
renders as a broken byte on a non-UTF-8 console -- observed directly in
`resolve.py --help`'s output before this file existed. Checked via `ast`
over `Constant` nodes (stdlib only, matches this project's own
"no third-party imports" discipline) rather than a lexical/regex scan, so
it also catches a docstring (which is just the first Constant in a
module/function/class body) the same way as an ordinary string literal.
"""
import ast
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent

CHECKED_FILES = [
    SCRIPTS_DIR / "resolve.py",
    SCRIPTS_DIR / "preflight.py",
    SCRIPTS_DIR / "validate_data.py",
    SCRIPTS_DIR / "ddi.py",
    SCRIPTS_DIR / "lib" / "fonts.py",
    SCRIPTS_DIR / "lib" / "color.py",
    SCRIPTS_DIR / "lib" / "pdf.py",
    SCRIPTS_DIR / "lib" / "data.py",
]


def _non_ascii_string_constants(path):
    """Yield (lineno, offending_chars, snippet) for every string Constant
    in `path` that contains a character outside the ASCII range."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            bad = sorted({c for c in node.value if ord(c) > 0x7F})
            if bad:
                snippet = node.value.strip().splitlines()[0][:60] if node.value.strip() else ""
                yield node.lineno, bad, snippet


class TestAsciiOnlyStringLiterals(unittest.TestCase):
    def test_no_non_ascii_in_any_string_or_docstring(self):
        for path in CHECKED_FILES:
            if not path.exists():
                continue  # ddi.py may not exist yet depending on task ordering
            with self.subTest(file=str(path)):
                offenders = list(_non_ascii_string_constants(path))
                self.assertEqual(
                    offenders, [],
                    f"{path} has non-ASCII string literal(s): {offenders}",
                )

    def test_files_are_actually_checked(self):
        # Guards against every path in CHECKED_FILES silently going missing
        # (e.g. a rename) and the test above passing on an empty list.
        existing = [p for p in CHECKED_FILES if p.exists()]
        self.assertGreaterEqual(len(existing), 7)


if __name__ == "__main__":
    unittest.main()
