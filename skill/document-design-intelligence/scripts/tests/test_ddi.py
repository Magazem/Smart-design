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


class TestHandoffPageFlow(unittest.TestCase):
    """Ruling K step 3 (research/brief-mechanism.md): page-flow constraints
    (keepNext/widowControl/cantSplit/tblHeader) must reach the docx handoff
    block, and the pptx block must say plainly that pagination properties
    have no slide equivalent -- a hand-built resolved.json rather than the
    manifest_ok toy fixture, since that fixture's constraints table carries
    no Parameter data and growing it is out of this task's scope."""

    _RESOLVED = {
        "status": "resolved",
        "resolved": {
            "constraints": [
                {"key": "report-heading-keep-with-next", "Element Scope": "",
                 "Parameter": "docx_property=keepNext;applies_to_block=heading;binds_to=body-paragraph"},
                {"key": "report-widow-orphan-control", "Element Scope": "body-paragraph",
                 "Parameter": "docx_property=widowControl;min_lines_together=2"},
                {"key": "report-table-row-no-split", "Element Scope": "table-cell",
                 "Parameter": "docx_property=cantSplit;applies_to_block=table-row"},
                {"key": "report-table-header-repeat", "Element Scope": "table-cell",
                 "Parameter": "docx_property=tblHeader;applies_to_block=table-header-row"},
                {"key": "report-figure-caption-keep-together", "Element Scope": "",
                 "Parameter": "docx_property=keepNext;applies_to_block=figure;binds_to=caption-block"},
                # same Set Key, no docx_property -- must be skipped, not crash
                {"key": "report-measure-cpl", "Element Scope": "body-paragraph",
                 "Parameter": "cpl_min=45;cpl_max=75"},
            ],
        },
    }

    def _write(self, tmpdir, payload):
        path = Path(tmpdir) / "resolved.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_docx_block_carries_all_five_page_flow_properties(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = _run(["handoff", "--json", str(self._write(tmp, self._RESOLVED)), "--format", "docx"])
        self.assertEqual(proc.returncode, 0)
        for expected in (
            "keepNext: heading bound to body-paragraph",
            "widowControl: body-paragraph, min_lines_together=2",
            "cantSplit: table-row",
            "tblHeader: table-header-row",
            "keepNext: figure bound to caption-block",
        ):
            self.assertIn(expected, proc.stdout)
        self.assertNotIn("cpl_min", proc.stdout)

    def test_pptx_block_states_no_equivalent_and_names_each_property(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = _run(["handoff", "--json", str(self._write(tmp, self._RESOLVED)), "--format", "pptx"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("NOT APPLICABLE", proc.stdout)
        self.assertIn("slides do not paginate", proc.stdout)
        for prop in ("keepNext", "widowControl", "cantSplit", "tblHeader"):
            self.assertIn(prop, proc.stdout)

    def test_pptx_states_not_applicable_even_with_no_page_flow_constraints_resolved(self):
        empty = {"status": "resolved", "resolved": {}}
        with tempfile.TemporaryDirectory() as tmp:
            proc = _run(["handoff", "--json", str(self._write(tmp, empty)), "--format", "pptx"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("NOT APPLICABLE", proc.stdout)


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
