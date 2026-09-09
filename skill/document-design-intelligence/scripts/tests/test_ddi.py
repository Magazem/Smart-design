#!/usr/bin/env python3
"""Unit tests for scripts/ddi.py -- the single entry point.

Every subcommand except `handoff` is a thin passthrough to a script
already covered by its own test suite (test_validate_data.py,
test_resolve.py, test_preflight.py) -- these tests check the ROUTING
(right script called, right exit code propagated), not the underlying
logic again.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import ddi  # noqa: E402

DATA_DIR = HERE / "fixtures" / "manifest_ok"
PDF_FIXTURE = SCRIPTS_DIR / "lib" / "tests" / "fixtures" / "sample.pdf"
PYTHON = sys.executable
DDI_PY = SCRIPTS_DIR / "ddi.py"


def _run(args):
    return subprocess.run([PYTHON, str(DDI_PY), *args], capture_output=True, text=True)


class TestNoArgsWorkflowText(unittest.TestCase):
    def test_prints_four_steps_exit_zero(self):
        proc = _run([])
        self.assertEqual(proc.returncode, 0)
        lines = [l for l in proc.stdout.splitlines() if l.strip()]
        self.assertEqual(len(lines), 4)
        for i, line in enumerate(lines, 1):
            self.assertTrue(line.startswith(f"{i}."), line)

    def test_mentions_all_four_subcommands(self):
        proc = _run([])
        for name in ("check", "resolve", "preflight", "handoff"):
            self.assertIn(f"ddi.py {name}", proc.stdout)

    def test_output_is_pure_ascii(self):
        proc = _run([])
        self.assertTrue(all(ord(c) < 128 for c in proc.stdout))


class TestCheck(unittest.TestCase):
    def test_clean_data_exit_zero(self):
        code = ddi.main(["check", "--data-dir", str(DATA_DIR)])
        self.assertEqual(code, 0)

    def test_tier1_structural_problem_exit_one(self):
        # Header mismatch is tier 1 (structural) per research/brief-
        # mechanism-perkey.md -- still a whole-dataset refusal.
        code = ddi.main(["check", "--data-dir", str(HERE / "fixtures" / "manifest_bad_header")])
        self.assertEqual(code, 1)

    def test_tier2_row_level_problem_exit_zero_with_named_warning(self):
        # A bad enum value is tier 2 (row-level) -- degrades to a named
        # warning instead of failing the check.
        proc = _run(["check", "--data-dir", str(HERE / "fixtures" / "manifest_bad_enum")])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("[DATA WARNING]", proc.stdout)
        self.assertIn("categories/tools", proc.stdout)
        self.assertIn("not in allowed enum", proc.stdout)


class TestResolvePassthrough(unittest.TestCase):
    def test_forwards_all_flags_and_exit_code(self):
        code = ddi.main(["resolve", "--data-dir", str(DATA_DIR), "--doctype", "dice", "--json"])
        self.assertEqual(code, 0)

    def test_abstain_exit_code_propagates(self):
        code = ddi.main(["resolve", "--data-dir", str(DATA_DIR), "--query", "spaceship"])
        self.assertEqual(code, 2)

    def test_brand_refusal_exit_code_propagates(self):
        code = ddi.main(["resolve", "--data-dir", str(DATA_DIR), "--query", "dice", "--brand", "acme"])
        self.assertEqual(code, 3)


@unittest.skipUnless(PDF_FIXTURE.exists(), "sample.pdf fixture not present")
class TestPreflightPassthrough(unittest.TestCase):
    def test_forwards_and_always_exits_zero(self):
        code = ddi.main(["preflight", str(PDF_FIXTURE), "--json"])
        self.assertEqual(code, 0)


class TestHandoff(unittest.TestCase):
    def _resolved_json_path(self, tmpdir, doctype="dice"):
        proc = _run(["resolve", "--data-dir", str(DATA_DIR), "--doctype", doctype, "--json"])
        self.assertEqual(proc.returncode, 0)
        path = Path(tmpdir) / "resolved.json"
        path.write_text(proc.stdout, encoding="utf-8")
        return path

    def test_degrades_gracefully_on_a_schema_with_no_document_vocabulary_yet(self):
        # The toy manifest has none of page-formats/typefaces/palettes --
        # handoff must say so plainly, not crash or fabricate values.
        with tempfile.TemporaryDirectory() as tmp:
            path = self._resolved_json_path(tmp)
            proc = _run(["handoff", "--json", str(path), "--format", "docx"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("HANDOFF (format=docx)", proc.stdout)
        self.assertIn("(not present in this resolution)", proc.stdout)
        self.assertIn("constraints to preflight: (none found)", proc.stdout)

    def test_ends_with_the_exact_preflight_command_for_the_chosen_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._resolved_json_path(tmp)
            proc = _run(["handoff", "--json", str(path), "--format", "pptx"])
        self.assertIn("scripts/preflight.py <rendered-file>.pptx", proc.stdout)

    def test_refuses_an_abstained_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "abstained.json"
            path.write_text(json.dumps({"status": "abstained", "candidates": []}), encoding="utf-8")
            code = ddi.main(["handoff", "--json", str(path), "--format", "docx"])
        self.assertEqual(code, 1)

    def test_missing_input_file_exit_one_not_a_crash(self):
        code = ddi.main(["handoff", "--json", "does-not-exist.json", "--format", "docx"])
        self.assertEqual(code, 1)

    def test_invalid_format_choice_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._resolved_json_path(tmp)
            proc = _run(["handoff", "--json", str(path), "--format", "epub"])
        self.assertNotEqual(proc.returncode, 0)


class TestVersion(unittest.TestCase):
    def test_prints_version_and_exits_zero(self):
        code = ddi.main(["version"])
        self.assertEqual(code, 0)

    def test_output_names_both_sources(self):
        proc = _run(["version"])
        self.assertIn("VERSION:", proc.stdout)
        self.assertIn("SKILL.md stamp:", proc.stdout)


class TestUnknownCommand(unittest.TestCase):
    def test_unknown_subcommand_exit_two(self):
        code = ddi.main(["frobnicate"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
