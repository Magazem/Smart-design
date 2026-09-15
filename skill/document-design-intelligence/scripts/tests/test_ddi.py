#!/usr/bin/env python3
"""Unit tests for scripts/ddi.py -- the single entry point.

Every subcommand except `handoff` is a thin passthrough to a script
already covered by its own test suite (test_validate_data.py,
test_resolve.py, test_preflight.py) -- these tests check the ROUTING
(right script called, right exit code propagated), not the underlying
logic again.
"""
import json
import re
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
    RULING N -- see TOC_HEADING_ROLES.
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


class TestDroppedColumnsReachResolvedOutput(unittest.TestCase):
    """research/54: `headings` and `structures` declared NO `display_columns` at
    all, so `resolve.py`'s `_display_columns` fell through to an empty default
    -- every resolved row was a bare `{"key": "contact-en-1"}`, union of keys
    across all of them exactly `["key"]`. `constraints` and `type-scales` DID
    declare `display_columns`, but the list was incomplete (missing Applies To/
    Check/Threshold/Severity, and scale_key/Leading Ratio respectively). Both
    are wrong for a different reason and both are checked here.

    what this test would say if the feature produced NOTHING AT ALL: every
    `assertIn`/`assertTrue` below reads a NAMED column out of a resolved row
    dict. A resolved row with only `{"key": ...}` fails `column in row` for
    every one of them, and an empty-string value on a column this data
    genuinely populates fails the non-blank check too -- so "nothing reached
    the output" is not a passing state here, unlike a test that only checks
    exit 0, row counts, or that the manifest declares a key (all of which
    passed throughout v0.2.0 while the handoff printed nothing).
    """

    #: Every non-key column each table is authored with (research/build-manifest.py
    #: "columns", minus key_column) -- fixed here independently of the manifest,
    #: so a future edit that silently drops one back out of `display_columns`
    #: is still caught, rather than this test trivially agreeing with whatever
    #: the manifest currently says.
    EXPECTED_COLUMNS = {
        "headings": ("canonical_section", "Heading Text", "Language", "Is Primary"),
        "structures": ("Display Name", "Section Order", "Heading Language",
                       "Heading Depth Max", "TOC Depth", "Front Matter Numbering",
                       "Caption Position", "Cross-Ref Style"),
        "constraints": ("Set Key", "Applies To", "Check", "Element Scope",
                        "Parameter", "Threshold", "Severity"),
        "type-scales": ("scale_key", "Medium", "Role", "Size pt", "Leading Ratio"),
    }
    #: `constraints."Element Scope"` is a real enum value of "" (schema allows
    #: it, and every constraint attached to cv-uk happens to be doc-level, not
    #: element-scoped) -- blank here is authored data, not a dropped column, so
    #: it is exempted from the "some row has content" half of the check. Every
    #: other column in EXPECTED_COLUMNS is genuinely populated for cv-uk.
    ALLOWED_ALL_BLANK = {("constraints", "Element Scope")}

    def _resolved(self, doctype="cv-uk"):
        proc = _run(["resolve", "--doctype", doctype, "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)["resolved"]

    #: Duplicated from TestHandoffEndToEndOnRealData rather than subclassed --
    #: subclassing it would also inherit and re-run every one of ITS test_*
    #: methods under this class name, which is not what's wanted here.
    _sections = staticmethod(TestHandoffEndToEndOnRealData._sections)
    _section_values = TestHandoffEndToEndOnRealData._section_values

    def test_every_authored_column_reaches_the_resolved_json(self):
        resolved = self._resolved()
        for table, columns in self.EXPECTED_COLUMNS.items():
            rows = resolved.get(table, [])
            self.assertTrue(rows, f"{table}: no rows resolved for cv-uk at all")
            for column in columns:
                with self.subTest(table=table, column=column):
                    self.assertTrue(
                        all(column in row for row in rows),
                        f"{table}.{column} is absent from at least one resolved row -- "
                        f"sample row: {rows[0]!r}")
                    if (table, column) not in self.ALLOWED_ALL_BLANK:
                        non_blank = [row[column] for row in rows if row.get(column)]
                        self.assertTrue(
                            non_blank,
                            f"{table}.{column} is present but BLANK on every resolved "
                            f"row -- sample row: {rows[0]!r}")

    def test_headings_carry_the_actual_authored_wording_not_bare_ids(self):
        """The exact failure shape research/53 verified against the published
        v0.2.0 asset: `resolved.headings` entries carried a `key` and nothing
        else. Checking "some content exists" would not catch a partial
        regression that drops `Heading Text` specifically while keeping other
        columns; naming the real authored wordings does."""
        rows = self._resolved()["headings"]
        texts = {row.get("Heading Text") for row in rows}
        for wording in ("Experience", "Work Experience", "Employment History",
                        "Professional Summary"):
            with self.subTest(wording=wording):
                self.assertIn(wording, texts)

    #: A CV family (2-3 wordings per canonical_section, per research/50) and a
    #: non-CV family (single wording per section, per RESUME.md's v0.3 backlog
    #: note that non-CV headings carry only one variant) -- the same
    #: two-doctype-not-one precedent TestHandoffEndToEndOnRealData already
    #: applies above, so a fix that only works where multiple wordings compete
    #: for "primary" is caught here.
    HANDOFF_SECTIONS_DOCTYPES = {
        "cv-uk": {"experience": "Experience", "contact": "Contact"},
        "report-long-toc": {"introduction": "Introduction",
                            "bibliography": "References"},
    }

    def test_handoff_docx_sections_carry_primary_heading_wording(self):
        """research/54 part 3: `display_columns` alone (the two tests above)
        puts wording into the resolved JSON, but `ddi.py`'s HANDOFF_VOCAB named
        neither `structures` nor `headings`, so the docx/pptx handoff -- the
        thing actually handed to a renderer -- printed nothing from either
        table. This runs the full resolve -> handoff pipeline exactly as a
        model invoking this skill would, and checks the rendered `sections`
        block, not the intermediate JSON, on both a CV family and a non-CV
        family (report-long-toc's 10 sections each carry exactly one
        authored wording, not 2-3 like a CV section, so this also proves the
        fix doesn't depend on "primary" having competition to pick from)."""
        for doctype, expected in self.HANDOFF_SECTIONS_DOCTYPES.items():
            with self.subTest(doctype=doctype):
                resolved = _run(["resolve", "--doctype", doctype, "--json"])
                self.assertEqual(resolved.returncode, 0, resolved.stderr)
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "resolved.json"
                    path.write_text(resolved.stdout, encoding="utf-8")
                    proc = _run(["handoff", "--json", str(path), "--format", "docx"])
                self.assertEqual(proc.returncode, 0, proc.stderr)
                sections = self._sections(proc.stdout)
                _, values = self._section_values(sections, "sections ")
                self.assertTrue(
                    all(v != ddi.NOT_PRESENT for v in values if v),
                    f"{doctype}: sections block has a {ddi.NOT_PRESENT} entry: {values}")
                for section, text in expected.items():
                    with self.subTest(section=section):
                        self.assertIn(f"{section}: {text}", proc.stdout)


class TestDocxSafeStackFallbackIsAHeadingBodyPair(unittest.TestCase):
    """A4b: `typefaces` carried exactly one `Safe Stack Fallback` value per
    row. For a two-family pairing (Heading Family != Body Family) the
    docx-office safe-stack line printed only that ONE value -- e.g.
    cv-uk's source-serif-sans row (heading Source Serif 4, body Source
    Sans 3, Safe Stack Fallback=Georgia) printed
    `python-docx (safe-stack): Georgia` with no signal at all for the body
    family, so python-docx had nothing to fall the BODY text back to and
    the whole rendered document collapsed onto the heading fallback
    (Georgia) everywhere. This runs the real resolve -> handoff pipeline on
    the two doctypes that actually hit docx-office with a two-family
    pairing (cv-uk -> source-serif-sans, cv-dach -> pt-serif-sans) and
    checks BOTH families' fallbacks are named, separately, in the docx
    handoff."""

    #: (heading fallback, body fallback) -- data/base/typefaces.csv's
    #: source-serif-sans and pt-serif-sans rows.
    EXPECTED = {
        "cv-uk": ("Georgia", "Arial"),
        "cv-dach": ("Times New Roman", "Arial"),
    }

    def test_docx_handoff_names_heading_and_body_fallback_separately(self):
        for doctype, (heading_fallback, body_fallback) in self.EXPECTED.items():
            with self.subTest(doctype=doctype):
                resolved = _run(["resolve", "--doctype", doctype, "--json"])
                self.assertEqual(resolved.returncode, 0, resolved.stderr)
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "resolved.json"
                    path.write_text(resolved.stdout, encoding="utf-8")
                    proc = _run(["handoff", "--json", str(path), "--format", "docx"])
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertIn(
                    f"python-docx (safe-stack): headings {heading_fallback} / "
                    f"body {body_fallback}",
                    proc.stdout,
                    proc.stdout,
                )


class TestPdfHandoffCarriesTypeScaleAndPalette(unittest.TestCase):
    """research/brief-packaging-display-columns.md PART 4: `_build_pdf_lines`
    read only page_format_table, render_target_table and typeface_table --
    never type_scale_table or palette_table, even though docx and pptx both
    do. The failure shape was worse than a blank value: the `font sizes`,
    `heading elements` and `palette` HEADERS themselves never printed, not
    just their content, because the section is entirely absent from the
    function rather than present-and-empty. A missing block is invisible in
    a way `(not present in this resolution)` is not -- that invisibility is
    exactly what let this ship. `invoice-tabular`'s ONLY render target is
    pdf, so for that family there was no other handoff path that could ever
    have delivered a size or a colour.

    what this test would say if the feature produced NOTHING AT ALL:
    `_section_values` (reused from TestHandoffEndToEndOnRealData) calls
    `self.fail()` outright if no section header matching the prefix is found
    at all -- so a still-missing block fails immediately, before ever
    reaching the content assertions below it.
    """

    _sections = staticmethod(TestHandoffEndToEndOnRealData._sections)
    _section_values = TestHandoffEndToEndOnRealData._section_values

    def _pdf_handoff(self, doctype):
        resolved = _run(["resolve", "--doctype", doctype, "--json"])
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(resolved.stdout, encoding="utf-8")
            proc = _run(["handoff", "--json", str(path), "--format", "pdf"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def test_invoice_tabular_pdf_only_family_gets_sizes_and_palette(self):
        """`invoice-tabular` has no h1/h2/h3 in its type scale (`form-print`
        is body/legal only), so `heading elements` legitimately reads
        NOT_PRESENT here -- that column is checked on `poster` below instead.
        `font sizes` and `palette` are real data for this family and must
        show it."""
        stdout = self._pdf_handoff("invoice-tabular")
        sections = self._sections(stdout)
        _, size_lines = self._section_values(sections, "font sizes ")
        self.assertTrue(size_lines and all("pt" in l for l in size_lines), size_lines)
        _, palette_lines = self._section_values(sections, "palette ")
        self.assertTrue(
            palette_lines and all(re.match(r"^[A-Za-z ]+: #[0-9A-Fa-f]{6}$", l) for l in palette_lines),
            palette_lines)

    def test_poster_pdf_gets_sizes_headings_and_palette(self):
        """`poster` (pdf-weasyprint-pdfx4 / pdf-chromium, `report-print` scale)
        carries h1/h2/h3, so this is the doctype that proves the
        `heading elements` block specifically, not just that it degrades to
        NOT_PRESENT gracefully."""
        stdout = self._pdf_handoff("poster")
        sections = self._sections(stdout)
        _, size_lines = self._section_values(sections, "font sizes ")
        self.assertTrue(size_lines and all(l != ddi.NOT_PRESENT for l in size_lines), size_lines)
        _, heading_lines = self._section_values(sections, "heading elements")
        self.assertEqual(
            sorted(l.split()[0] for l in heading_lines), ["h1", "h2", "h3"], heading_lines)
        self.assertIn("h1  ->  <h1>", stdout)
        _, palette_lines = self._section_values(sections, "palette ")
        self.assertTrue(palette_lines and all(l != ddi.NOT_PRESENT for l in palette_lines), palette_lines)

    def test_quote_devis_pdf_gets_a_sections_block(self):
        """research/brief-packaging-pdf-sections.md: `_build_pdf_lines` never
        called `_sections_lines` at all (unlike the docx/pptx/png builders),
        so pdf's `sections` header did not print, not just its content -- the
        same "missing block, not empty block" shape as the type-scale/palette
        gap this class already covers above. `quote-devis`'s ONLY render
        target is pdf-chromium, so for this family (and the other 8 pdf-only
        doctypes) the handoff's heading wording reached NO renderer at all.
        `_section_values` fails outright if the `sections` header is absent,
        so a still-missing block fails here before the wording check below
        ever runs."""
        stdout = self._pdf_handoff("quote-devis")
        sections = self._sections(stdout)
        _, values = self._section_values(sections, "sections ")
        self.assertTrue(
            values and any(v != ddi.NOT_PRESENT for v in values),
            f"quote-devis: pdf sections block is empty: {values}")
        self.assertIn("issuer: From", values)


class TestPngHandoffBuilder(unittest.TestCase):
    """research/brief-packaging-deck-and-png.md PART B: `_FORMAT_BUILDERS`
    (ddi.py:683 at the time) covered docx/pptx/pdf only. `infographic`'s ONLY
    render target is `png-social` (Format=png), so that family had NO
    handoff path at all -- not missing wording, no builder. `infographic` is
    the only shipped doctype whose `Render Target Keys` includes `png-social`
    (data/base/doctypes.csv), so it is also the only doctype these tests can
    exercise against real data.

    `infographic`'s `doc-reasoning` row (`infographic-scaffold`) has empty
    Style/Palette/Typeface Key (a separate, already-tracked defect --
    research/51-invoked-quality.md D4). That means `font-face`, `font sizes`,
    `sections` and `palette` legitimately have nothing to show for this
    doctype today; what matters here is that each HEADER still prints with
    `ddi.NOT_PRESENT` rather than the block being silently absent -- that is
    exactly the failure shape D4/D2 already named ("a missing block is
    invisible; an empty one is a fact"). `canvas` and `render command` ARE
    real data for `infographic` (png-social's own Engine Invocation) and are
    checked for actual content, not just presence.
    """

    _sections = staticmethod(TestHandoffEndToEndOnRealData._sections)
    _section_values = TestHandoffEndToEndOnRealData._section_values

    def _png_handoff(self, doctype):
        resolved = _run(["resolve", "--doctype", doctype, "--json"])
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(resolved.stdout, encoding="utf-8")
            proc = _run(["handoff", "--json", str(path), "--format", "png"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def test_infographic_canvas_and_render_command_are_real_px_data(self):
        """png-social's Engine Invocation is the only source for the
        screenshot's pixel dimensions (the brief: do not invent one) --
        1080x1350 parsed straight off its `--window-size` flag, and the
        render command line must carry the invocation verbatim."""
        stdout = self._png_handoff("infographic")
        sections = self._sections(stdout)
        _, canvas_lines = self._section_values(sections, "canvas ")
        self.assertEqual(canvas_lines, ["headless-chromium: 1080px x 1350px"], canvas_lines)
        _, command_lines = self._section_values(sections, "render command")
        self.assertTrue(
            command_lines and "--window-size=1080,1350" in command_lines[0], command_lines)

    def test_infographic_paged_media_is_explicitly_not_applicable(self):
        """png-social's Supports Paged Media is n/a and Print Tier Max is
        none -- bleed/crop-marks/@page must be called out as NOT APPLICABLE,
        not simply absent, per the same "don't omit the block" rule."""
        self.assertIn("NOT APPLICABLE", self._png_handoff("infographic"))

    def test_infographic_empty_reasoning_columns_degrade_to_not_present_not_omission(self):
        """The headers for font-face/font sizes/sections/palette must all
        still print even when the resolved payload carries none of that data
        -- proving the builder didn't just skip these blocks the way the
        pre-fix code skipped the whole format.

        A synthetic empty payload, not a live doctype: this used to resolve
        `infographic`, the one doctype whose `infographic-scaffold` row had
        empty Style/Palette/Typeface Key (D4). `infographic` shipped as a real
        family since (research/59-infographic-content.md) and now resolves
        real values there, which is what broke this test -- pinning a
        degrade-path test to a doctype staying broken forever was itself a
        latent bug. Empty-resolved is already the established pattern for
        this (see TestHandoffPageFlow's pptx not-applicable test)."""
        empty = {"status": "resolved", "resolved": {}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(json.dumps(empty), encoding="utf-8")
            proc = _run(["handoff", "--json", str(path), "--format", "png"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        sections = self._sections(proc.stdout)
        for prefix in ("font-face ", "font sizes ", "sections", "palette "):
            with self.subTest(section=prefix):
                _, values = self._section_values(sections, prefix)
                self.assertTrue(values, f"section {prefix!r} header printed but body is empty")
                self.assertTrue(all(v == ddi.NOT_PRESENT for v in values), values)

    def test_cli_format_choices_include_png(self):
        """`--format` used to reject `png` outright (choices was docx/pptx/pdf
        only); this is the CLI half of the same gap."""
        resolved = _run(["resolve", "--doctype", "infographic", "--json"])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(resolved.stdout, encoding="utf-8")
            proc = _run(["handoff", "--json", str(path), "--format", "png"])
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_parse_window_size_says_so_when_absent_or_malformed(self):
        """Unit-level, since no shipped render-targets row is malformed on
        purpose: `_parse_window_size` must return None (not a guessed size)
        for a missing flag and for a value that doesn't match `W,H`, and
        `_build_png_lines` must turn that into an explicit message rather
        than a bare NOT_PRESENT that reads like "no render target" instead
        of "this render target's invocation didn't parse"."""
        self.assertIsNone(ddi._parse_window_size(""))
        self.assertIsNone(ddi._parse_window_size("--headless --no-sandbox"))
        self.assertIsNone(ddi._parse_window_size("--window-size=1080"))
        self.assertEqual(ddi._parse_window_size("--window-size=1080,1350 %i"), (1080, 1350))

        resolved = {
            "render-targets": [{
                "key": "png-broken", "Format": "png", "Engine": "headless-chromium",
                "Engine Invocation": "--headless --screenshot=%o %i",
                "Font Rule": "embed",
            }],
        }
        lines = ddi._build_png_lines(resolved)
        canvas_line = next(l for l in lines if l.strip().startswith("headless-chromium:"))
        self.assertIn("not found or unparsable", canvas_line)


class TestHandoffBuilderParity(unittest.TestCase):
    """research/brief-packaging-pdf-sections.md addition, ruled by the lead:
    `_build_pdf_lines` (this task's fix) picked up `_sections_lines` a whole
    release cycle after `_build_png_lines` did, and nobody noticed until the
    acceptance gate ran on a pdf-only doctype. A per-builder test catches a
    missed CALL for the builder it targets; nothing before this class checked
    that every _FORMAT_BUILDERS entry stays in sync with every other one, so
    the NEXT format-specific omission (a fifth builder someday, or a
    regression re-dropping the pdf call this task just added) would again
    ship silent.

    The four builders legitimately differ in most of their content --
    `@page` vs. DXA page math vs. slide layout vs. a px canvas are all
    correct, format-specific blocks, and a test asserting identical headers
    across formats would be WRONG. What must NOT differ is that each of
    these four concepts gets a block at all: `sections`, `fonts`/`font-face`,
    `font sizes`, and `palette` are read from the same four resolved tables
    (`headings`+`structures`, `typefaces`, `type-scales`, `palette`) by
    every one of the four builders today (`_build_docx_lines`,
    `_build_pptx_lines`, `_build_pdf_lines`, `_build_png_lines` -- see each
    function's own `_first_row`/`resolved.get` calls), so a format silently
    skipping one of the four is a missed call site, not a legitimate format
    difference. `page`/`page flow` and `render command` were deliberately
    left OUT of the shared core: docx has no `render command` (it does not
    self-render) and pptx's `page flow` is intentionally `NOT APPLICABLE`
    text rather than a block with content -- both are real, correct
    per-format differences, not omissions.

    Each header must be present AND carry at least one line under it --
    `(not present in this resolution)` counts as present, an empty block
    (header with zero lines) does not, matching the "don't omit, degrade
    explicitly" rule already enforced per-format elsewhere in this file
    (e.g. TestPngHandoffBuilder's degrade test above).

    Verified this test WOULD catch the defect this task fixed: with
    `_build_pdf_lines`'s `lines.extend(_sections_lines(resolved))` call
    temporarily removed, `test_all_four_builders_emit_the_shared_core`
    failed on `format=pdf, concept=sections` with "no handoff section
    starting..."; restoring the call made it pass again. Both checked by
    hand before this test was added to the suite.
    """

    _sections = staticmethod(TestHandoffEndToEndOnRealData._sections)

    #: Concept label -> ordered candidate header prefixes. Two formats use
    #: `fonts:` (docx, pptx); the other two use `font-face` (pdf, png) --
    #: both candidates are tried so the SAME concept check works across all
    #: four without asserting they share identical wording.
    SHARED_CORE = {
        "sections": ("sections ",),
        "fonts": ("fonts:", "font-face"),
        "font sizes": ("font sizes ",),
        "palette": ("palette ",),
    }

    #: Read from `_FORMAT_BUILDERS` itself, not a hardcoded tuple -- a
    #: hardcoded list would not catch a FIFTH builder someday skipping the
    #: shared core, since a new `_FORMAT_BUILDERS` entry with no matching
    #: tuple update would just never get exercised here.
    FORMATS = tuple(ddi._FORMAT_BUILDERS)

    #: report-long-toc: already the fixture TestHandoffEndToEndOnRealData
    #: uses for docx/pptx: its resolved payload (page/typeface/type-scale/
    #: palette/headings/structures rows) is format-agnostic, so requesting
    #: pdf or png handoff for it exercises those builders' shared-core reads
    #: exactly as it would for any doctype -- confirmed above to emit all
    #: four concepts cleanly on all four formats before this test was written.
    DOCTYPE = "report-long-toc"

    def _handoff(self, fmt):
        resolved = _run(["resolve", "--doctype", self.DOCTYPE, "--json"])
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(resolved.stdout, encoding="utf-8")
            proc = _run(["handoff", "--json", str(path), "--format", fmt])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def _find(self, sections, candidates):
        for header, values in sections.items():
            if any(header.startswith(c) for c in candidates):
                return header, values
        return None, None

    def test_all_four_builders_emit_the_shared_core(self):
        for fmt in self.FORMATS:
            sections = self._sections(self._handoff(fmt))
            for concept, candidates in self.SHARED_CORE.items():
                with self.subTest(format=fmt, concept=concept):
                    header, values = self._find(sections, candidates)
                    self.assertIsNotNone(
                        header,
                        f"format={fmt}: no section header starting with any of "
                        f"{candidates!r} for concept {concept!r}; got {list(sections)}")
                    self.assertTrue(
                        values,
                        f"format={fmt}: {concept!r} section {header!r} header "
                        f"printed but carries no lines at all")


class TestCvRegionRowCoverage(unittest.TestCase):
    """research/64 D-B: cv-uk resolves TWO cv-regions rows (`uk-early`,
    `uk-experienced`) with DIFFERENT Section Orders, but `_cv_region_lines`
    used `_first_row` and printed only the first row's Seniority Band --
    silently dropping `uk-experienced` and its Section Order entirely. "a
    consumer receives two alternative section orders and nothing that says
    which one applies" (the complaint) is not fixed by picking one row and
    calling it done; every resolved cv-regions row must reach the handoff,
    each with its OWN Section Order, on all four format paths."""

    DOCTYPE = "cv-uk"
    FORMATS = tuple(ddi._FORMAT_BUILDERS)

    #: cv-uk's two authored cv-regions rows (data/base/cv-regions.csv), each
    #: with a genuinely different Section Order -- confirmed by resolving
    #: cv-uk directly before writing this test.
    EXPECTED_ROWS = {
        "early": "contact;summary;education;experience;skills",
        "experienced": "contact;summary;experience;education;skills",
    }

    def _handoff(self, fmt):
        resolved = _run(["resolve", "--doctype", self.DOCTYPE, "--json"])
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "resolved.json"
            path.write_text(resolved.stdout, encoding="utf-8")
            proc = _run(["handoff", "--json", str(path), "--format", fmt])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def test_every_resolved_cv_region_row_and_its_own_section_order_appears(self):
        for fmt in self.FORMATS:
            output = self._handoff(fmt)
            for band, section_order in self.EXPECTED_ROWS.items():
                with self.subTest(format=fmt, band=band):
                    self.assertIn(
                        band, output,
                        f"format={fmt}: Seniority Band {band!r} missing from "
                        f"handoff -- a resolved cv-regions row was dropped")
                    self.assertIn(
                        section_order, output,
                        f"format={fmt}: Section Order {section_order!r} (for "
                        f"band {band!r}) missing from handoff")


if __name__ == "__main__":
    unittest.main()
