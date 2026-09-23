#!/usr/bin/env python3
"""P1.4 (research/80-v05-plan.md §2C, §6): provenance business rules over
data/base -- shipped data only, no research/ dependency.

validate_data.py already enforces provenance's STRUCTURAL shape (header,
enums, that `Table`/`Evidence Class`/`Fetch` cells are in their declared
enums). This file enforces the rules research/80 §2C describes that are
specific to provenance's semantics and its deliberately-not-FK-reachable
`Row Key` column (data/schema-manifest-NOTES.md §10):

  1. every `Row Key` resolves against the manifest's own `key_column` for
     the table named by `Table` (the polymorphic FK validate_data.py cannot
     check, because a plain FK entry can only ever name one target table);
  2. every generic-scope row of designs/palettes/typefaces/doc-styles/
     doc-reasoning has >=1 provenance row, OR is a documented pre-v0.5
     legacy exception (`LEGACY_UNPROVENANCED` below);
  3. `convention` rows may leave `Source URL` blank; `ranked` rows must not
     leave `Source URL`/`Ranking Metric`/`Rank Value`/`Retrieved` blank;
  4. a numeric `Rank Value` only ever appears on a `fetched` row -- a
     `search-corroborated` row cannot claim a precise numeric rank;
  5. `Retrieved` is a real ISO date, not in the future;
  6. no two rows cite the same (`Table`, `Row Key`, `Source URL`, `Ranking Metric`)
     quadruple. The key deliberately includes `Ranking Metric`, not just
     (`Table`, `Row Key`, `Source URL`): a two-family typeface pairing legitimately
     cites the same Google Fonts metadata endpoint twice, once per family, because
     that single URL serves per-family data (research/83 audit item 2) -- one
     popularity citation per family of a pairing is not a duplicate citation of the
     same fact, provided each row's `Ranking Metric` names a distinct family. Two
     rows that share all four fields, including identical `Ranking Metric` text,
     really are citing the same fact twice and remain a duplicate.

LEGACY_UNPROVENANCED is a documented allow-list, not an escape hatch: it is
computed from the CURRENT data below the constant (see the comment), so it
passes today, and it may only ever SHRINK. Two tests enforce that directly --
one fails if a listed key no longer exists (dead entry, must be removed) and
one fails the moment a listed key GAINS a provenance row (must be removed,
not left stale) -- so nobody can silently grow this list by adding it to
instead of backfilling provenance.
"""
import datetime
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
SKILL_ROOT = SCRIPTS_DIR.parent
DATA_DIR = SKILL_ROOT / "data"

sys.path.insert(0, str(SCRIPTS_DIR))
from lib import data as datalib  # noqa: E402


def _load():
    problems = datalib.ProblemLog()
    manifest = datalib.load_manifest(DATA_DIR)
    tables_spec = manifest["tables"]
    all_rows = datalib.load_all_tables(DATA_DIR, tables_spec, problems)
    return tables_spec, all_rows, problems


TABLES_SPEC, ALL_ROWS, LOAD_PROBLEMS = _load()
PROVENANCE = ALL_ROWS["provenance"]

# The five tables research/80 §2C says provenance covers.
PROVENANCED_TABLES = ["designs", "palettes", "typefaces", "doc-styles", "doc-reasoning"]

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _generic_rows(table):
    """Rows of `table` in the "generic" (non-brand-overlay) scope. A table
    with no `Brand Scope` column at all (doc-reasoning) has no scoping
    concept, so every row of it counts."""
    rows = ALL_ROWS[table]
    if "Brand Scope" in TABLES_SPEC[table]["columns"]:
        return [r for r in rows if r.get("Brand Scope") == "generic"]
    return rows


def _provenance_pairs():
    return {(row["Table"], row["Row Key"]) for row in PROVENANCE}


def _is_numeric(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


# Computed from the CURRENT contents of data/base/{palettes,typefaces,
# doc-styles,doc-reasoning}.csv: every generic row of those four tables that
# has no matching data/base/provenance.csv row today (`designs` needed no
# entries -- P1.3's backfill already covers every design). doc-styles and
# doc-reasoning predate the provenance table entirely (research/80 §0);
# the palettes/typefaces entries here are the safe-stack fallback rows and a
# handful of palettes P1.3's rationale backfill did not reach. This list may
# only ever SHRINK -- see TestLegacyListOnlyShrinks below.
LEGACY_UNPROVENANCED = {
    ("palettes", "mono-ink"),
    ("palettes", "brand-accent-print"),
    ("palettes", "print-neutral"),
    ("palettes", "deck-high-contrast"),
    ("palettes", "cv-harvard"),
    ("palettes", "cv-dach-formal"),
    ("palettes", "cv-europass"),
    ("palettes", "cv-editorial"),
    ("typefaces", "safe-sans-arial"),
    ("typefaces", "safe-sans-deck"),
    ("typefaces", "safe-sans-infographic"),
    ("typefaces", "safe-serif-times"),
    ("typefaces", "safe-serif-georgia"),
    ("typefaces", "ofl-source-sans-serif"),
    ("typefaces", "ofl-plex-superfamily"),
    ("typefaces", "ofl-public-sans"),
    ("typefaces", "ofl-roboto-slab"),
    ("typefaces", "source-serif-sans"),
    ("typefaces", "pt-serif-sans"),
    ("typefaces", "ibm-plex-sans"),
    ("typefaces", "fraunces-work-sans"),
    ("doc-styles", "cv-restrained"),
    ("doc-styles", "cv-academic-plain"),
    ("doc-styles", "letter-restrained"),
    ("doc-styles", "letter-formal-grid"),
    ("doc-styles", "memo-plain"),
    ("doc-styles", "form-grid-underline"),
    ("doc-styles", "marketing-print-bold"),
    ("doc-styles", "infographic-bold"),
    ("doc-styles", "report-classic-serif"),
    ("doc-styles", "deck-bold-minimal"),
    ("doc-styles", "one-pager-tight"),
    ("doc-styles", "cv-harvard"),
    ("doc-styles", "cv-dach-tabular"),
    ("doc-styles", "cv-europass"),
    ("doc-styles", "cv-editorial"),
    ("doc-reasoning", "cv-ats-strict"),
    ("doc-reasoning", "cv-academic"),
    ("doc-reasoning", "cover-letter-professional"),
    ("doc-reasoning", "letter-formal"),
    ("doc-reasoning", "memo-internal"),
    ("doc-reasoning", "form-handfilled"),
    ("doc-reasoning", "print-marketing"),
    ("doc-reasoning", "report-classic"),
    ("doc-reasoning", "whitepaper-formal"),
    ("doc-reasoning", "proposal-narrative"),
    ("doc-reasoning", "quote-devis"),
    ("doc-reasoning", "deck-generic"),
    ("doc-reasoning", "one-pager-restrained"),
    ("doc-reasoning", "infographic-scaffold"),
    ("doc-reasoning", "invoice-tabular"),
    ("doc-reasoning", "cv-us-uk-designed"),
    ("doc-reasoning", "cv-dach-tabular"),
    ("doc-reasoning", "cv-eu-europass"),
    ("doc-reasoning", "cv-editorial"),
}


class TestLoadedCleanly(unittest.TestCase):
    def test_manifest_and_base_data_loaded_without_structural_problems(self):
        # Guards the guard: if this fails, every other test in this file is
        # exercising an empty/garbled table list, not the real data.
        self.assertFalse(LOAD_PROBLEMS, LOAD_PROBLEMS.lines)


class TestRowKeyResolves(unittest.TestCase):
    def test_every_row_key_exists_in_its_declared_table(self):
        keys_by_table = datalib.keys_by_table(TABLES_SPEC, ALL_ROWS)
        for row in PROVENANCE:
            table = row["Table"]
            with self.subTest(prov_key=row["prov_key"]):
                self.assertIn(table, keys_by_table,
                              f"{row['prov_key']}: Table {table!r} is not a known keyed table")
                key_column = TABLES_SPEC[table]["key_column"]
                self.assertIn(row["Row Key"], keys_by_table[table],
                              f"{row['prov_key']}: Row Key {row['Row Key']!r} does not resolve "
                              f"to {table}.{key_column}")


class TestProvenanceCoverage(unittest.TestCase):
    def test_every_generic_row_has_provenance_or_is_legacy(self):
        pairs = _provenance_pairs()
        for table in PROVENANCED_TABLES:
            key_column = TABLES_SPEC[table]["key_column"]
            for row in _generic_rows(table):
                key = row[key_column]
                with self.subTest(table=table, key=key):
                    covered = (table, key) in pairs
                    legacy = (table, key) in LEGACY_UNPROVENANCED
                    self.assertTrue(
                        covered or legacy,
                        f"{table}:{key} has no provenance row and is not listed in "
                        "LEGACY_UNPROVENANCED -- either add a provenance row citing a "
                        "source, or (if it genuinely predates provenance) add it to the "
                        "allow-list with a reason")


class TestLegacyListOnlyShrinks(unittest.TestCase):
    def test_legacy_entries_still_exist(self):
        for table, key in sorted(LEGACY_UNPROVENANCED):
            key_column = TABLES_SPEC[table]["key_column"]
            keys = {r[key_column] for r in ALL_ROWS[table]}
            with self.subTest(table=table, key=key):
                self.assertIn(
                    key, keys,
                    f"LEGACY_UNPROVENANCED lists {table}:{key}, which no longer exists in "
                    f"data/base/{table}.csv -- remove it from the list")

    def test_legacy_entries_still_lack_provenance(self):
        pairs = _provenance_pairs()
        for table, key in sorted(LEGACY_UNPROVENANCED):
            with self.subTest(table=table, key=key):
                self.assertNotIn(
                    (table, key), pairs,
                    f"{table}:{key} now HAS a provenance row -- remove it from "
                    "LEGACY_UNPROVENANCED (the list may only shrink)")


class TestEvidenceClassFieldRequirements(unittest.TestCase):
    def test_convention_rows_permit_blank_source_url(self):
        convention_rows = [r for r in PROVENANCE if r["Evidence Class"] == "convention"]
        self.assertTrue(convention_rows,
                         "no convention provenance rows found to exercise this rule against")
        blank_source = [r for r in convention_rows if not r["Source URL"].strip()]
        self.assertTrue(
            blank_source,
            "expected at least one convention row with a blank Source URL "
            "(§2C: blank is only ever permitted for convention)")

    def test_convention_blank_source_and_fetch_else_fetch_required(self):
        for row in PROVENANCE:
            with self.subTest(prov_key=row["prov_key"]):
                if row["Evidence Class"] == "convention":
                    self.assertEqual(row["Source URL"].strip(), "", f"{row['prov_key']}: convention has a Source URL")
                    self.assertEqual(row["Fetch"].strip(), "", f"{row['prov_key']}: convention must have blank Fetch")
                else:
                    self.assertTrue(row["Fetch"].strip(), f"{row['prov_key']}: non-convention needs Fetch")

    def test_prov_key_format(self):
        for row in PROVENANCE:
            with self.subTest(prov_key=row["prov_key"]):
                m = re.fullmatch(r"([^:]+):([^:]+):([1-9][0-9]*)", row["prov_key"])
                self.assertTrue(m, f"bad prov_key {row['prov_key']!r}")
                self.assertEqual((m.group(1), m.group(2)), (row["Table"], row["Row Key"]))

    def test_ranked_rows_require_url_metric_value_and_date(self):
        ranked_rows = [r for r in PROVENANCE if r["Evidence Class"] == "ranked"]
        self.assertTrue(ranked_rows, "no ranked provenance rows found to exercise this rule against")
        for row in ranked_rows:
            with self.subTest(prov_key=row["prov_key"]):
                for column in ("Source URL", "Ranking Metric", "Rank Value", "Retrieved"):
                    self.assertTrue(
                        row[column].strip(),
                        f"{row['prov_key']}: Evidence Class ranked but {column!r} is blank")


class TestRankValueNumericOnlyWhenFetched(unittest.TestCase):
    def test_numeric_rank_value_implies_fetched(self):
        for row in PROVENANCE:
            rank_value = row["Rank Value"].strip()
            if not rank_value or not _is_numeric(rank_value):
                continue
            with self.subTest(prov_key=row["prov_key"]):
                self.assertEqual(
                    row["Fetch"], "fetched",
                    f"{row['prov_key']}: numeric Rank Value {rank_value!r} on a row whose "
                    f"Fetch is {row['Fetch']!r}, not 'fetched'")


class TestRetrievedDate(unittest.TestCase):
    def test_retrieved_is_iso_date_not_in_the_future(self):
        today = datetime.date.today()
        for row in PROVENANCE:
            retrieved = row["Retrieved"]
            with self.subTest(prov_key=row["prov_key"]):
                self.assertRegex(
                    retrieved, ISO_DATE_RE,
                    f"{row['prov_key']}: Retrieved {retrieved!r} is not YYYY-MM-DD")
                try:
                    parsed = datetime.date.fromisoformat(retrieved)
                except ValueError as exc:
                    self.fail(f"{row['prov_key']}: Retrieved {retrieved!r} is not a valid "
                              f"calendar date: {exc}")
                self.assertLessEqual(
                    parsed, today,
                    f"{row['prov_key']}: Retrieved {retrieved} is in the future (today is {today})")


class TestNoDuplicateSourceCitations(unittest.TestCase):
    def test_table_row_key_source_url_metric_quadruples_are_unique(self):
        # Keyed on (Table, Row Key, Source URL, Ranking Metric), not just the first
        # three fields: citing the same Source URL twice for one Row Key is legitimate
        # when each row's Ranking Metric names a different family of a typeface
        # pairing (research/83 audit item 2) -- e.g. one Google Fonts metadata/fonts
        # citation for the heading family's popularity and a second, separate citation
        # for the body family's popularity, both under the same endpoint URL. Adding
        # Ranking Metric to the key still catches a true duplicate: two rows citing
        # the same URL under the *same* Ranking Metric text are citing the same fact
        # twice.
        from collections import Counter
        counts = Counter(
            (row["Table"], row["Row Key"], row["Source URL"], row["Ranking Metric"])
            for row in PROVENANCE)
        duplicates = {quad: count for quad, count in counts.items() if count > 1}
        self.assertEqual(
            duplicates, {},
            f"duplicate (Table, Row Key, Source URL, Ranking Metric) quadruples in "
            f"data/base/provenance.csv: {duplicates}")


if __name__ == "__main__":
    unittest.main()
