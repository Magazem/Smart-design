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


class TestHandoffEndToEndOnRealData(unittest.TestCase):
    """RULING M: the handoff block is what the docx skill is HANDED. It shipped
    all through v0.1.0 with no page size, no fonts and no palette, because the
    six tables it reads carried no `display_columns` -- resolve attached the
    right rows and then surfaced only their searchable/FK columns, so every
    lookup found a row and no values in it.

    This test runs the real pipeline (`ddi.py resolve` -> `ddi.py handoff`) on
    real data/, on TWO doctypes, and asserts those sections carry CONTENT. A
    test that only checked exit 0 would have passed for the whole of v0.1.0 --
    that is the gap this closes. `TOC heading levels` is asserted too, as of
    RULING N -- see TOC_HEADING_ROLES. `characterSpacing` is still deliberately
    NOT asserted: see the docstring on the test below it.
    """

    DOCTYPES = ("report-long-toc", "cv-generic")
    #: RULING N: the heading roles each doctype's type scale is authored to carry.
    #: Checked as a SET, not merely for presence, so a missing level is a failure
    #: rather than a shorter list -- and so cv-generic states that h3 is ABSENT
    #: on purpose instead of leaving it unsaid.
    TOC_HEADING_ROLES = {"report-long-toc": ("h1", "h2", "h3"),
                         "cv-generic": ("h1", "h2")}
    #: `  <label...>:` at two spaces, its values indented four. Splitting on the
    #: indent rather than matching each label keeps this test from having to
    #: restate ddi.py's exact (long, citation-bearing) section headers.
    REQUIRED_SECTIONS = ("page ", "fonts:", "font sizes ", "palette ")

    def _handoff(self, doctype, fmt="docx"):
        resolved = _run(["resolve", "--doctype", doctype, "--json"])
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(resolved.stdout, encoding="utf-8")
            proc = _run(["handoff", "--json", str(path), "--format", fmt])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    @staticmethod
    def _sections(stdout):
        """{section-header: [value lines]} -- headers are indented two spaces,
        their values four."""
        out, current = {}, None
        for line in stdout.splitlines():
            if line.startswith("    "):
                if current is not None:
                    out[current].append(line.strip())
            elif line.startswith("  "):
                current = line[2:]
                out[current] = []
        return out

    def _section_values(self, sections, prefix):
        for header, values in sections.items():
            if header.startswith(prefix):
                return header, values
        self.fail(f"no handoff section starting {prefix!r}; got {list(sections)}")

    def test_required_sections_are_non_empty_on_both_doctypes(self):
        for doctype in self.DOCTYPES:
            sections = self._sections(self._handoff(doctype))
            for prefix in self.REQUIRED_SECTIONS:
                with self.subTest(doctype=doctype, section=prefix):
                    header, values = self._section_values(sections, prefix)
                    real = [v for v in values if v and v != ddi.NOT_PRESENT]
                    self.assertTrue(
                        real,
                        f"{doctype}: handoff section {header!r} is EMPTY -- this is the "
                        "v0.1.0 blocker, not a formatting nit")

    def test_page_and_font_sizes_are_numeric_where_they_claim_to_be(self):
        for doctype in self.DOCTYPES:
            sections = self._sections(self._handoff(doctype))
            with self.subTest(doctype=doctype, section="page"):
                _, values = self._section_values(sections, "page ")
                for line in values:
                    mm, _, dxa = line.partition("  ->  ")
                    self.assertRegex(mm, r"^[A-Za-z ]+: [0-9.]+mm$", line)
                    label, _, number = dxa.partition(": ")
                    self.assertTrue(number.isdigit() and int(number) > 0, line)
            with self.subTest(doctype=doctype, section="font sizes"):
                _, values = self._section_values(sections, "font sizes ")
                for line in values:
                    role, _, rest = line.partition(": ")
                    pt, _, half = rest.partition("pt  ->  ")
                    self.assertTrue(role, line)
                    self.assertGreater(float(pt), 0, line)
                    self.assertGreater(float(half.split()[0]), 0, line)

    def test_palette_values_are_six_digit_hex(self):
        for doctype in self.DOCTYPES:
            with self.subTest(doctype=doctype):
                _, values = self._section_values(
                    self._sections(self._handoff(doctype)), "palette ")
                for line in values:
                    self.assertRegex(line, r"^[A-Za-z ]+: #[0-9A-Fa-f]{6}$", line)

    def test_constraint_set_keys_line_names_the_sets(self):
        """The hand-added `display_columns` omitted `Set Key`, so this line
        rendered as a bare label with nothing after the colon."""
        for doctype in self.DOCTYPES:
            with self.subTest(doctype=doctype):
                line = [l for l in self._handoff(doctype).splitlines()
                        if "constraints to preflight" in l]
                self.assertEqual(len(line), 1, line)
                self.assertTrue(line[0].split(":", 1)[1].strip(), line[0])

    def test_toc_heading_levels_name_the_scale_roles_and_carry_their_sizes(self):
        """RULING N. `report-long-toc` is the doctype named for its table of
        contents, and this section printed NOT_PRESENT right up until the five
        authored type-scale heading rows were loaded: `report-print` and
        `cv-print` carried a `body` row and nothing else, so _heading_roles()
        found nothing shaped like h<n> to emit a HeadingLevel for.

        Asserting the section is merely NON-EMPTY would not have closed that gap
        -- it passes on `h2, h3` alone, which is a table of contents with no top
        level. So the roles are checked as a SET against what each scale is
        authored to carry, and every role listed must then appear in `font sizes`
        with a real point value. A HeadingLevel with no size behind it is the same
        empty handoff wearing a label.

        cv-generic asserts h3 is ABSENT. `cv-print` has no h3 by decision: a CV's
        third tier is weight contrast, not a size (research/46-notes.md).
        """
        for doctype, expected in self.TOC_HEADING_ROLES.items():
            with self.subTest(doctype=doctype):
                sections = self._sections(self._handoff(doctype))
                header, values = self._section_values(sections, "TOC heading levels")
                roles = [line.split("->")[0].strip() for line in values
                         if line and line != ddi.NOT_PRESENT]
                self.assertEqual(
                    sorted(roles), sorted(expected),
                    f"{doctype}: handoff section {header!r} carries {roles}, expected "
                    f"{list(expected)} -- TOC heading levels are the type-scale h<n> "
                    "rows, so a missing level means the scale row is not in data/base")
                _, size_lines = self._section_values(sections, "font sizes ")
                sizes = {}
                for line in size_lines:
                    role, _, rest = line.partition(": ")
                    sizes[role] = rest.partition("pt")[0]
                for role in roles:
                    self.assertIn(
                        role, sizes,
                        f"{doctype}: TOC heading levels lists {role} but `font sizes` "
                        "carries no size for it")
                    self.assertGreater(
                        float(sizes[role]), 0,
                        f"{doctype}: TOC heading level {role} has no positive size")
