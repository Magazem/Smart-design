#!/usr/bin/env python3
"""Unit tests for scripts/validate_data.py — the manifest-driven harness.

Fixtures: tests/fixtures/manifest_ok/ (clean) and one tests/fixtures/
manifest_bad_<class>/ per failure class this harness must catch — see
tests/fixtures/make_manifest_fixtures.py for exactly what each fixture
changes relative to the clean one (one change each, by design).
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import validate_data  # noqa: E402

FIXTURES = HERE / "fixtures"


def _base(name):
    return FIXTURES / name / "base"


def _data_dir(name):
    return FIXTURES / name


class TestCleanFixturePasses(unittest.TestCase):
    def test_ok_fixture_passes(self):
        ok, problems, summary = validate_data.validate(_data_dir("manifest_ok"))
        self.assertTrue(ok, problems)
        self.assertEqual(problems, [])
        self.assertIn("2 table(s)", summary)
        # 2 base categories + 2 base widgets + 1 brand-overlay widget = 5.
        self.assertIn("5 row(s)", summary)

    def test_cli_exit_code_zero_on_clean(self):
        code = validate_data.main([str(_base("manifest_ok"))])
        self.assertEqual(code, 0)

    def test_brand_overlay_row_gets_brand_scope_from_directory_not_csv(self):
        # The fixture's brand CSV deliberately writes a wrong value in the
        # Brand Scope cell ("should-be-overwritten-by-harness") — the
        # harness must replace it with the directory name ("acme"),
        # regardless of what the CSV itself says.
        manifest = validate_data.json.loads(
            (_data_dir("manifest_ok") / "schema-manifest.json").read_text(encoding="utf-8")
        )
        problems = validate_data.datalib.ProblemLog()
        rows = validate_data.datalib.load_table_rows(
            _data_dir("manifest_ok"), manifest["tables"]["widgets"], problems
        )
        acme_rows = [r for r in rows if r["widget_key"] == "acme-wrench"]
        self.assertEqual(len(acme_rows), 1)
        self.assertEqual(acme_rows[0]["Brand Scope"], "acme")
        self.assertFalse(problems)


class TestFailureClasses(unittest.TestCase):
    def _assert_fails_with(self, fixture_name, expected_substring):
        ok, problems, _summary = validate_data.validate(_data_dir(fixture_name))
        self.assertFalse(ok, f"{fixture_name} should have failed")
        joined = "\n".join(problems)
        self.assertIn(expected_substring, joined, joined)

        code = validate_data.main([str(_base(fixture_name))])
        self.assertEqual(code, 1)

    def test_header_mismatch(self):
        self._assert_fails_with("manifest_bad_header", "header mismatch")

    def test_enum_violation(self):
        self._assert_fails_with("manifest_bad_enum", "not in allowed enum")

    def test_foreign_key_violation(self):
        self._assert_fails_with("manifest_bad_fk", "does not resolve to categories.category_key")

    def test_utf8_bom_rejected(self):
        self._assert_fails_with("manifest_bad_bom", "UTF-8 BOM present")

    def test_untyped_json_cell_rejected(self):
        self._assert_fails_with("manifest_bad_json_cell", "looks like untyped JSON")

    def test_contrast_below_threshold(self):
        self._assert_fails_with("manifest_bad_contrast", "is below required 4.5:1")

    def test_contrast_pair_both_cells_blank_is_skipped(self):
        # Branch 1 of the blank-handling rule: BOTH cells empty means the row
        # does not define that colour role, so there is no pair to rate and no
        # line. `palettes.mono-ink` ships `Accent`/`On Accent` blank on purpose.
        ok, problems, _summary = validate_data.validate(
            _data_dir("manifest_contrast_both_blank_ok"))
        self.assertTrue(ok, problems)
        self.assertEqual(problems, [])
        self.assertEqual(
            validate_data.main([str(_base("manifest_contrast_both_blank_ok"))]), 0)

    def test_contrast_pair_with_one_blank_cell_still_fails(self):
        # Branch 2: exactly ONE cell empty is an authoring bug, not an omission,
        # and must still fail -- in BOTH orderings. The fixture blanks
        # `On Primary` on row 2 and `Primary` on row 3, so two lines prove the
        # rule is not one-sided (the message is anchored to `column` either way).
        ok, problems, _summary = validate_data.validate(
            _data_dir("manifest_bad_contrast_half_blank"))
        self.assertFalse(ok)
        self.assertEqual(len(problems), 2, problems)
        for line in problems:
            self.assertIn("cannot compute contrast: invalid hex color ''", line)
            self.assertIn("On Primary", line)  # anchored to the rule's `column`
        self.assertIn(":2:", problems[0])
        self.assertIn(":3:", problems[1])
        self.assertEqual(
            validate_data.main([str(_base("manifest_bad_contrast_half_blank"))]), 1)

    def test_contrast_pair_both_present_and_failing_is_one_line(self):
        # Branch 3: both cells present and the ratio too low -- exactly one line,
        # unchanged by the blank-handling rule.
        ok, problems, _summary = validate_data.validate(_data_dir("manifest_bad_contrast"))
        self.assertFalse(ok)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("is below required 4.5:1", problems[0])

    def test_key_collision_across_base_and_brand(self):
        self._assert_fails_with("manifest_bad_key_collision", "duplicate key 'hammer'")

    def test_missing_declared_base_file(self):
        self._assert_fails_with("manifest_missing_base_file", "declared in manifest but file does not exist")


class TestProblemLineFormat(unittest.TestCase):
    def test_row_and_column_are_both_in_the_line(self):
        ok, problems, _ = validate_data.validate(_data_dir("manifest_bad_enum"))
        self.assertFalse(ok)
        self.assertEqual(len(problems), 1)
        # file:row:column: message — row 2 is the first data row (header is row 1).
        self.assertRegex(problems[0], r"categories\.csv:2:Status:")


class TestMalformedManifestItself(unittest.TestCase):
    def test_missing_manifest_file_is_a_clean_failure_not_a_crash(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            ok, problems, _ = validate_data.validate(Path(tmp))
            self.assertFalse(ok)
            self.assertTrue(problems)
            self.assertIn("cannot read manifest", problems[0])


class TestGroupForeignKey(unittest.TestCase):
    """research/09 Revision 2 shape: an FK whose target column is a
    non-unique grouping column, not the target table's key_column — see
    tests/fixtures/make_manifest_fixtures.py's GROUP_MANIFEST (tags/Group
    repeats across rows; items references it with "group": true, and with
    "group": true + "list": true combined)."""

    def test_group_fk_and_list_plus_group_combo_both_pass(self):
        ok, problems, summary = validate_data.validate(_data_dir("manifest_group_ok"))
        self.assertTrue(ok, problems)
        self.assertIn("3 table(s)", summary)

    def test_group_fk_value_not_in_target_column_fails(self):
        ok, problems, _ = validate_data.validate(_data_dir("manifest_bad_group_fk"))
        self.assertFalse(ok)
        self.assertIn("'nonexistent-group' does not resolve to tags.Group", "\n".join(problems))

    def test_group_membership_is_not_a_key_lookup(self):
        # "colors" and "shapes" each appear on TWO tags.csv rows (red/blue,
        # circle/square) — a key_column lookup would reject that as a
        # duplicate key; group membership must accept it.
        ok, problems, _ = validate_data.validate(_data_dir("manifest_group_ok"))
        self.assertTrue(ok, problems)
        self.assertNotIn("duplicate key", "\n".join(problems))


class TestListColumns(unittest.TestCase):
    def test_well_formed_list_passes(self):
        ok, problems, _ = validate_data.validate(_data_dir("manifest_group_ok"))
        self.assertTrue(ok, problems)

    def test_empty_item_between_delimiters_fails(self):
        ok, problems, _ = validate_data.validate(_data_dir("manifest_bad_list_column"))
        self.assertFalse(ok)
        self.assertIn("malformed ';'-delimited list", "\n".join(problems))


class TestDistinctTokenColumns(unittest.TestCase):
    def test_no_repeated_token_passes(self):
        ok, problems, _ = validate_data.validate(_data_dir("manifest_group_ok"))
        self.assertTrue(ok, problems)
        self.assertNotIn("duplicate token", "\n".join(problems))

    def test_repeated_token_in_comma_column_fails(self):
        # items.csv row "apple" has Keywords "apple, fruit, red, fruit" -- the
        # doctypes.Keywords shape: a `, `-separated search-token cell that is not
        # a `;`-list at all. A repeat doubles that term's frequency and biases
        # retrieval toward the row carrying the accidental duplicate.
        ok, problems, _ = validate_data.validate(_data_dir("manifest_bad_distinct_token"))
        self.assertFalse(ok)
        joined = "\n".join(problems)
        self.assertIn("duplicate token 'fruit' in ','-delimited list", joined)
        self.assertIn("Keywords", joined)

    def test_repeat_is_reported_once_per_token(self):
        _ok, problems, _ = validate_data.validate(_data_dir("manifest_bad_distinct_token"))
        self.assertEqual(1, sum("duplicate token" in line for line in problems))

    def test_repeat_in_undeclared_list_column_passes(self):
        # "Panels" is a declared list column with NO distinct_token_columns entry.
        # It stands in for page-formats."Panels mm", a positional sequence of panel
        # widths where "99.5;99.5;98.0" is a correct A4 trifold, not a defect. A
        # blanket rule over every list column would fail four real rows there,
        # which is why this check is opt-in per column.
        ok, problems, _ = validate_data.validate(
            _data_dir("manifest_repeat_in_undeclared_list_ok"))
        self.assertTrue(ok, problems)

    def test_duplicate_is_tier_2_tagged_with_its_own_key(self):
        tier1_ok, tier1, tier2, _ = validate_data.validate_tiered(
            _data_dir("manifest_bad_distinct_token"))
        self.assertTrue(tier1_ok, tier1)
        hits = [e for e in tier2 if "duplicate token" in e["line"]]
        self.assertEqual(1, len(hits))
        self.assertEqual("items", hits[0]["table"])
        self.assertEqual("apple", hits[0]["key"])


class TestReferenceColumns(unittest.TestCase):
    def test_literal_value_not_matching_pattern_is_not_checked(self):
        # checks.csv row c1's Threshold is "5" -- a literal, not a
        # "table:column" reference -- must not be flagged at all.
        ok, problems, _ = validate_data.validate(_data_dir("manifest_group_ok"))
        self.assertTrue(ok, problems)

    def test_valid_reference_resolves(self):
        ok, problems, _ = validate_data.validate(_data_dir("manifest_group_ok"))
        self.assertTrue(ok, problems)
        self.assertNotIn("names unknown table", "\n".join(problems))

    def test_reference_to_unknown_table_fails(self):
        ok, problems, _ = validate_data.validate(_data_dir("manifest_bad_reference_column"))
        self.assertFalse(ok)
        self.assertIn("names unknown table 'nonexistent-table'", "\n".join(problems))


class TestValidateTiered(unittest.TestCase):
    """research/brief-mechanism-perkey.md: tier 1 (structural) still gates
    the whole dataset; tier 2 (row-level) is returned per-key instead."""

    def test_clean_fixture_has_no_problems_of_either_tier(self):
        tier1_ok, tier1_lines, tier2_entries, summary = validate_data.validate_tiered(
            _data_dir("manifest_ok")
        )
        self.assertTrue(tier1_ok)
        self.assertEqual(tier1_lines, [])
        self.assertEqual(tier2_entries, [])
        self.assertIn("2 table(s)", summary)

    def test_header_mismatch_is_tier1(self):
        tier1_ok, tier1_lines, tier2_entries, _summary = validate_data.validate_tiered(
            _data_dir("manifest_bad_header")
        )
        self.assertFalse(tier1_ok)
        self.assertTrue(any("header mismatch" in line for line in tier1_lines))
        self.assertEqual(tier2_entries, [])

    def test_bad_enum_is_tier2_tagged_to_its_own_row(self):
        tier1_ok, tier1_lines, tier2_entries, _summary = validate_data.validate_tiered(
            _data_dir("manifest_bad_enum")
        )
        self.assertTrue(tier1_ok, tier1_lines)
        self.assertEqual(tier1_lines, [])
        self.assertEqual(len(tier2_entries), 1)
        self.assertEqual(tier2_entries[0]["table"], "categories")
        self.assertEqual(tier2_entries[0]["key"], "tools")
        self.assertIn("not in allowed enum", tier2_entries[0]["line"])

    def test_dangling_fk_is_tier2_tagged_to_the_referencing_row(self):
        # widgets/hammer's own FK is broken -- the poisoned key is the
        # widget itself, not the (perfectly fine) categories table.
        tier1_ok, tier1_lines, tier2_entries, _summary = validate_data.validate_tiered(
            _data_dir("manifest_bad_fk")
        )
        self.assertTrue(tier1_ok, tier1_lines)
        self.assertEqual(len(tier2_entries), 1)
        self.assertEqual(tier2_entries[0]["table"], "widgets")
        self.assertEqual(tier2_entries[0]["key"], "hammer")

    def test_missing_base_file_on_entry_table_is_tier1(self):
        # manifest_missing_base_file's missing file IS the entry table
        # (widgets, role=entry) -- resolve.py cannot start Stage 1 at all
        # without it, so this stays a whole-dataset refusal.
        tier1_ok, tier1_lines, _tier2_entries, _summary = validate_data.validate_tiered(
            _data_dir("manifest_missing_base_file")
        )
        self.assertFalse(tier1_ok)
        self.assertTrue(any("does not exist" in line for line in tier1_lines))

    def test_validate_unaffected_by_tiering_still_fails_on_any_problem(self):
        # validate() (the strict release.yml/build_zip.py gate) must keep
        # its existing all-problems-fail contract regardless of tier.
        ok, problems, _summary = validate_data.validate(_data_dir("manifest_bad_enum"))
        self.assertFalse(ok)
        self.assertEqual(len(problems), 1)


if __name__ == "__main__":
    unittest.main()
