#!/usr/bin/env python3
"""Unit tests for scripts/resolve.py — the manifest-driven runtime engine.

All tests run against tests/fixtures/manifest_ok, the same toy manifest
validate_data.py's tests use (widgets = entry table, FK to categories,
plus one `;`-list FK "Related Category Keys" and one brand overlay row —
see tests/fixtures/make_manifest_fixtures.py for the exact data).

Two BM25 test queries are deliberately chosen from hand-verified math, not
just "ran it and it happened to work":
  - "hammer dice" scores widgets/hammer and widgets/dice EXACTLY equally
    under BM25 with a single-token-per-document corpus (symmetric IDF,
    equal document length) — a genuine tie, margin=0, so it is the
    canonical case for margin-based abstention, not a contrived one.
  - "hammer acme" for the brand two-pass test: "hammer" is a real,
    scoring token against the GENERIC widgets/hammer row, but pass 1 only
    ever searches the brand-scoped subset (just widgets/acme-wrench),
    which never sees "hammer" as vocabulary at all — proving brand
    resolution wins because of restricted scope, not because it happened
    to out-score a generic competitor.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import resolve  # noqa: E402

DATA_DIR = HERE / "fixtures" / "manifest_ok"
PYTHON = sys.executable
RESOLVE_PY = SCRIPTS_DIR / "resolve.py"


def _run_cli(args):
    proc = subprocess.run(
        [PYTHON, str(RESOLVE_PY), "--data-dir", str(DATA_DIR), *args],
        capture_output=True, text=True,
    )
    return proc


class TestIdentityShortCircuit(unittest.TestCase):
    def test_exact_key_match_skips_bm25(self):
        code = resolve.main(["--data-dir", str(DATA_DIR), "--query", "hammer", "--json"])
        self.assertEqual(code, 0)

    def test_identity_method_reported(self):
        proc = _run_cli(["--query", "hammer", "--json"])
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["method"], "identity")
        self.assertEqual(payload["resolved"]["widgets"][0]["key"], "hammer")

    def test_display_name_also_matches_identity(self):
        proc = _run_cli(["--query", "Dice", "--json"])
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["method"], "identity")
        self.assertEqual(payload["resolved"]["widgets"][0]["key"], "dice")


class TestDiacriticFolding(unittest.TestCase):
    """research/brief-mechanism.md: accented and ASCII/transliterated
    spellings of a word must tokenize identically, symmetric between query
    and document text. Accented characters are built via chr() here, not
    written as literal source characters, per test_ascii_clean.py's rule
    (which scans this repo's non-test scripts, but there is no reason to
    add a fresh non-ASCII literal to a project that keeps its source
    ASCII-clean everywhere else)."""

    def test_umlaut_and_german_ae_digraph_converge(self):
        a_umlaut = chr(0xE4)  # LATIN SMALL LETTER A WITH DIAERESIS
        self.assertEqual(
            resolve.BM25.tokenize("pr" + a_umlaut + "sentation"),
            resolve.BM25.tokenize("praesentation"),
        )

    def test_eszett_and_ss_converge(self):
        eszett = chr(0xDF)  # LATIN SMALL LETTER SHARP S
        self.assertEqual(
            resolve.BM25.tokenize("stra" + eszett + "e"),
            resolve.BM25.tokenize("strasse"),
        )

    def test_french_accent_folds_to_ascii_cognate(self):
        e_acute = chr(0xE9)  # LATIN SMALL LETTER E WITH ACUTE
        self.assertEqual(
            resolve.BM25.tokenize("pr" + e_acute + "sentation"),
            resolve.BM25.tokenize("presentation"),
        )

    def test_folding_is_symmetric_between_document_and_query(self):
        # A document indexed under the accented spelling must be findable
        # by an ASCII-transliterated query -- not just that tokenize()
        # agrees with itself in isolation.
        a_umlaut = chr(0xE4)
        bm = resolve.BM25()
        bm.fit(["pr" + a_umlaut + "sentation deck"])
        self.assertGreater(bm.scores("praesentation")[0], 0.0)


class TestBm25Hit(unittest.TestCase):
    def test_extra_word_falls_through_to_bm25_and_still_resolves(self):
        proc = _run_cli(["--query", "hammer tool", "--json"])
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["method"], "bm25")
        self.assertEqual(payload["resolved"]["widgets"][0]["key"], "hammer")


class TestAbstention(unittest.TestCase):
    def test_zero_overlap_is_no_match_not_ambiguous(self):
        # "spaceship" shares no vocabulary with any Display Name in the
        # fixture -> top-1 scores 0.0 for every row. This must read as "no
        # match" and list NOTHING -- offering 0.0-scoring rows would imply
        # a narrowing that never happened (research/brief-mechanism.md).
        proc = _run_cli(["--query", "spaceship"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("NO MATCH", proc.stdout)
        self.assertNotIn("ABSTAIN", proc.stdout)
        self.assertNotIn("score=", proc.stdout)

    def test_zero_overlap_json_has_no_match_status_and_no_candidates(self):
        proc = _run_cli(["--query", "spaceship", "--json"])
        self.assertEqual(proc.returncode, 2)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "no_match")
        self.assertEqual(payload["reason"], "no-match")
        self.assertEqual(payload["candidates"], [])

    def test_margin_tie_abstains_not_a_coin_flip(self):
        # Hand-verified exact tie (see module docstring) — must abstain,
        # not silently pick whichever sorts first. Real competing
        # candidates with a nonzero top score -> "ambiguous", distinct from
        # the zero-score "no match" case above, but still status=abstained.
        proc = _run_cli(["--query", "hammer dice", "--json"])
        self.assertEqual(proc.returncode, 2)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "abstained")
        self.assertEqual(payload["reason"], "ambiguous")
        scores = {c["key"]: c["score"] for c in payload["candidates"]}
        self.assertAlmostEqual(scores["hammer"], scores["dice"], places=6)

    def test_abstain_reports_top_three_candidates(self):
        # Ambiguous case (nonzero, tied top score) still lists candidates.
        proc = _run_cli(["--query", "hammer dice", "--json"])
        payload = json.loads(proc.stdout)
        self.assertLessEqual(len(payload["candidates"]), 3)
        self.assertGreaterEqual(len(payload["candidates"]), 1)


class TestMarginRatioBoundary(unittest.TestCase):
    """The abstain margin (_MIN_MARGIN_RATIO, research/35-notes.md) is
    relative -- (top - runner_up) / top -- not absolute, so it scales with
    corpus size instead of being tuned to one dataset. Exercises `_search`
    directly against hand-computed BM25 scores (not through the CLI/fixture
    data) so the boundary itself is verified against real math, the same
    standard as the module docstring's hammer/dice tie: two documents whose
    only difference is one extra occurrence of the shared token "red" (3x
    vs 2x) produce a small but genuine, non-tied score gap -- weak top must
    abstain, clear win must not, at exactly the same relative-margin logic
    the tie case (test_margin_tie_abstains_not_a_coin_flip) uses at ratio=0."""

    KEY_COLUMN = "key"
    SEARCHABLE = ["Text"]

    @staticmethod
    def _rows(*texts):
        return [{"key": f"doc{i}", "Display Name": f"doc{i}", "Text": t}
                 for i, t in enumerate(texts)]

    def test_weak_top_abstains(self):
        # "red blue" vs "red blue yellow" on query "red blue": ratio ~=
        # 0.073 (hand-verified via resolve.BM25 directly) -- nonzero,
        # not tied, and clearly below _MIN_MARGIN_RATIO (0.15).
        rows = self._rows("red red blue green", "red blue yellow")
        row, diag = resolve._search(rows, self.KEY_COLUMN, self.SEARCHABLE, "red blue", "Display Name")
        self.assertIsNone(row)
        self.assertEqual(diag["reason"], "ambiguous")
        self.assertGreater(diag["top_score"], 0)
        self.assertNotAlmostEqual(diag["top_score"], diag["runner_up_score"], places=6)

    def test_zero_top_score_is_no_match_with_no_candidates(self):
        # Query shares no token with any document's vocabulary -> every
        # row scores 0.0. Must report "no-match" and list zero candidates,
        # never the top-N zero-scoring rows (research/brief-mechanism.md).
        rows = self._rows("red red blue green", "red blue yellow")
        row, diag = resolve._search(rows, self.KEY_COLUMN, self.SEARCHABLE, "spaceship", "Display Name")
        self.assertIsNone(row)
        self.assertEqual(diag["reason"], "no-match")
        self.assertEqual(diag["candidates"], [])
        self.assertEqual(diag["top_score"], 0.0)

    def test_clear_win_resolves(self):
        # Same shape, wider gap: ratio ~= 0.25, above _MIN_MARGIN_RATIO --
        # must resolve, not abstain, despite still being a nonzero runner-up.
        rows = self._rows("alpha alpha alpha beta gamma delta",
                           "alpha beta gamma delta epsilon zeta")
        row, diag = resolve._search(rows, self.KEY_COLUMN, self.SEARCHABLE, "alpha beta", "Display Name")
        self.assertIsNotNone(row)
        self.assertEqual(row["key"], "doc0")
        self.assertEqual(diag["method"], "bm25")


class TestBrandTwoPass(unittest.TestCase):
    def test_brand_row_wins_despite_generic_keyword_overlap(self):
        # "hammer" genuinely scores against the GENERIC widgets/hammer row;
        # pass 1 never sees it because the brand-scoped corpus (just
        # acme-wrench) doesn't contain that token at all.
        proc = _run_cli(["--query", "hammer acme", "--brand", "acme", "--json"])
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["pass"], "brand")
        self.assertEqual(payload["resolved"]["widgets"][0]["key"], "acme-wrench")

    def test_falls_back_to_generic_when_brand_pass_abstains(self):
        proc = _run_cli(["--query", "dice", "--brand", "nonexistent-brand", "--json"])
        # No "nonexistent-brand" rows exist at all -> brand pass abstains
        # immediately (no-rows-to-search) -> generic pass resolves "dice"
        # via identity -> then validate-brand-resolution refuses to emit
        # since the resolved set has no nonexistent-brand row.
        self.assertEqual(proc.returncode, 3)
        self.assertIn("NO BRAND ROW", proc.stdout)

    def test_brand_scope_set_from_directory_is_what_gets_matched(self):
        # The brand fixture CSV's own Brand Scope cell is garbage
        # ("should-be-overwritten-by-harness") — resolution only works at
        # all because the loader (lib/data.py) overwrote it with "acme".
        proc = _run_cli(["--query", "acme wrench", "--brand", "acme", "--json"])
        self.assertEqual(proc.returncode, 0)


class TestBrandRefusal(unittest.TestCase):
    def test_no_brand_row_at_all_refuses(self):
        proc = _run_cli(["--query", "dice", "--brand", "acme"])
        self.assertEqual(proc.returncode, 3)
        self.assertIn("[NO BRAND ROW] brand=acme", proc.stdout)
        self.assertIn("refusing to emit", proc.stdout)


class TestForeignKeyWalk(unittest.TestCase):
    def test_single_value_fk_resolved(self):
        proc = _run_cli(["--doctype", "hammer", "--json"])
        payload = json.loads(proc.stdout)
        self.assertIn("categories", payload["resolved"])
        self.assertEqual(payload["resolved"]["categories"][0]["key"], "tools")

    def test_list_fk_resolves_every_referenced_row(self):
        proc = _run_cli(["--doctype", "dice", "--json"])
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        category_keys = {row["key"] for row in payload["resolved"]["categories"]}
        # "dice" has Category Key=games AND Related Category Keys=games;tools
        # -> both games and tools must appear, deduplicated, exactly once each.
        self.assertEqual(category_keys, {"games", "tools"})
        self.assertEqual(len(payload["resolved"]["categories"]), 2)

    def test_never_dumps_a_whole_table(self):
        proc = _run_cli(["--doctype", "hammer", "--json"])
        payload = json.loads(proc.stdout)
        # widget_key/Category Key/Related Category Keys/Brand Scope minus
        # what's shown: only searchable + FK columns appear, not every
        # column the underlying row actually has.
        widget_out = payload["resolved"]["widgets"][0]
        self.assertNotIn("Brand Scope", widget_out)


class TestEndToEnd(unittest.TestCase):
    def test_full_resolution_stdout_is_small(self):
        proc = _run_cli(["--doctype", "dice"])
        self.assertEqual(proc.returncode, 0)
        lines = [l for l in proc.stdout.splitlines() if l.strip()]
        self.assertLess(len(lines), 40)

    def test_tier1_structural_problem_refuses_before_any_search(self):
        # Header mismatch is tier 1 (structural, research/brief-mechanism-
        # perkey.md) -- still a whole-dataset refusal, before Stage 1 runs.
        bad_dir = HERE / "fixtures" / "manifest_bad_header"
        proc = subprocess.run(
            [PYTHON, str(RESOLVE_PY), "--data-dir", str(bad_dir), "--query", "hammer"],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("DATA INVALID", proc.stdout)


class TestPerKeyDegradation(unittest.TestCase):
    """research/brief-mechanism-perkey.md: a tier-2 (row-level) problem
    must refuse only the resolution paths that touch the broken key --
    everything else answers normally, with a warning header present.
    `manifest_bad_fk` (tests/fixtures/make_manifest_fixtures.py) sets
    widgets/hammer's Category Key to a nonexistent category -- a dangling
    FK tagged to widgets/hammer itself, leaving widgets/dice untouched."""

    BAD_FK_DIR = HERE / "fixtures" / "manifest_bad_fk"

    def _run_bad_fk(self, args):
        proc = subprocess.run(
            [PYTHON, str(RESOLVE_PY), "--data-dir", str(self.BAD_FK_DIR), *args],
            capture_output=True, text=True,
        )
        return proc

    def test_touching_path_is_refused_by_name(self):
        proc = self._run_bad_fk(["--doctype", "hammer"])
        self.assertEqual(proc.returncode, 1)
        self.assertIn("[REFUSED PATH]", proc.stdout)
        self.assertIn("widgets/hammer", proc.stdout)
        self.assertIn("does not resolve to categories.category_key", proc.stdout)

    def test_untouched_path_resolves_normally_with_warning_header(self):
        proc = self._run_bad_fk(["--doctype", "dice"])
        self.assertEqual(proc.returncode, 0)
        self.assertIn("[DATA WARNING]", proc.stdout)
        self.assertNotIn("[REFUSED PATH]", proc.stdout)
        self.assertIn("RESOLVED", proc.stdout)

    def test_json_mode_omits_warning_header_but_still_resolves(self):
        # --json output must stay valid JSON -- the warning header is
        # plain-text-only, printed before it, never mixed in.
        proc = self._run_bad_fk(["--doctype", "dice", "--json"])
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "resolved")


class TestGroupFkGuidanceMessage(unittest.TestCase):
    """research/brief-mechanism.md item 3, v0.2: no row in data/base still
    ships an empty group-FK list column (commit aec56f4 loaded Section
    Order for all 17 structure rows), so this exercises `_field_value`
    directly against a synthetic row -- the fixture pattern
    TestMarginRatioBoundary already uses for hand-built rows -- rather
    than a CSV fixture directory, since no shipping data can trigger this
    path any more."""

    SPEC = {
        "foreign_keys": {
            "Section Order": {
                "table": "headings",
                "column": "canonical_section",
                "group": True,
                "list": True,
            }
        }
    }

    def test_empty_group_fk_list_returns_named_guidance_message(self):
        row = {"structure_key": "struct-empty", "Section Order": ""}
        value = resolve._field_value(row, "Section Order", self.SPEC, "struct-empty")
        self.assertEqual(value, "no section-order guidance for struct-empty")

    def test_populated_group_fk_list_returns_real_value_not_guidance(self):
        row = {"structure_key": "cv-academic", "Section Order": "contact;summary"}
        value = resolve._field_value(row, "Section Order", self.SPEC, "cv-academic")
        self.assertEqual(value, "contact;summary")


if __name__ == "__main__":
    unittest.main()
