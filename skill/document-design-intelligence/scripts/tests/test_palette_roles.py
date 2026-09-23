#!/usr/bin/env python3
"""research/85 audit fix 1/2 -- Text-Safe Roles must actually clear 4.5:1.

`schema-manifest.json`'s own `derived` contrast checks for the `palettes`
table only cover the On-X/X and Foreground/Background pairs (see
`make_brand_kit.derive_palette_row`'s docstring: "Text-Safe / Fill-Only /
Category Marker roles: computed from contrast_ratio(role, Background) >=
4.5 among {primary, secondary, accent} only"). Nothing in the schema or in
`scripts/tests/test_validate_data.py` checks that a role actually listed in
a row's own `Text-Safe Roles` column clears that bar against that row's own
`Background` -- a row can claim a role is text-safe while it is well under
4.5:1 (research/85, ranked-colourlovers batch, 11 of 15 rows: `secondary`
claimed Text-Safe as low as 1.21:1 against Background).

This test is data-driven and cwd-independent (paths resolved from this
file's own location, per research's own "build-manifest cwd-independent"
fix): it checks every row of `data/base/palettes.csv` -- both the base
library and any `research/library/palettes/*.csv` batch already folded
into it -- not just the batch that prompted this fix.

Role name -> column mapping (per `schema-manifest.json`'s `palettes` table
and `make_brand_kit.derive_palette_row`, which is the same mapping already
in production use): `foreground` -> `Foreground`, `primary` -> `Primary`,
`secondary` -> `Secondary`, `accent` -> `Accent`, `muted` -> `Muted`. Each
role's contrast is checked against that row's own `Background` column,
using `lib.color.contrast_ratio` -- the same WCAG 2.x arithmetic the rest
of this schema already uses for every other contrast check.

`muted` is deliberately excluded from Text-Safe Roles by every current
producer of this table (`make_brand_kit.derive_palette_row` never adds it;
neither does any batch in `research/library/palettes/`), so it is not part
of the manifest's own {primary, secondary, accent} Text-Safe candidate
set. If a future row ever does list `muted` in Text-Safe Roles, this test
still checks it against Background at the same 4.5:1 bar -- Text-Safe
Roles is a claim about *any* role named in it, not just the three the
current producers happen to populate it from.
"""
import csv
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
SKILL_ROOT = SCRIPTS_DIR.parent
BASE_DIR = SKILL_ROOT / "data" / "base"
PALETTES_CSV = BASE_DIR / "palettes.csv"

sys.path.insert(0, str(SCRIPTS_DIR))
from lib import color  # noqa: E402

MIN_RATIO = 4.5

ROLE_TO_COLUMN = {
    "foreground": "Foreground",
    "primary": "Primary",
    "secondary": "Secondary",
    "accent": "Accent",
    "muted": "Muted",
}


def _read_rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _text_safe_roles(row):
    raw = (row.get("Text-Safe Roles") or "").strip()
    if not raw:
        return []
    return [tok.strip() for tok in raw.split(";") if tok.strip()]


class TestPaletteTextSafeRoles(unittest.TestCase):
    """Every role a palettes.csv row lists in Text-Safe Roles must clear
    4.5:1 contrast against that row's own Background."""

    def test_base_palettes_csv_exists(self):
        self.assertTrue(
            PALETTES_CSV.is_file(),
            f"expected {PALETTES_CSV} to exist -- run `python3 research/load-base.py` first",
        )

    def test_every_text_safe_role_clears_contrast_floor(self):
        rows = _read_rows(PALETTES_CSV)
        self.assertGreater(len(rows), 0, "palettes.csv has no data rows")

        failures = []
        for row in rows:
            key = row.get("palette_key", "<missing palette_key>")
            background = (row.get("Background") or "").strip()
            for role in _text_safe_roles(row):
                column = ROLE_TO_COLUMN.get(role)
                if column is None:
                    failures.append(
                        f"{key}: Text-Safe Roles names unknown role {role!r} "
                        f"(no column mapping)"
                    )
                    continue
                role_hex = (row.get(column) or "").strip()
                if not role_hex or not background:
                    failures.append(
                        f"{key}: role {role!r} (column {column!r}) or Background "
                        f"is blank, cannot be Text-Safe (role={role_hex!r}, "
                        f"background={background!r})"
                    )
                    continue
                ratio = color.contrast_ratio(role_hex, background)
                with self.subTest(palette_key=key, role=role):
                    self.assertGreaterEqual(
                        ratio,
                        MIN_RATIO,
                        f"{key}: Text-Safe role {role!r} ({column}={role_hex}) is only "
                        f"{ratio:.2f}:1 against Background={background} "
                        f"(needs >= {MIN_RATIO}:1)",
                    )
                if ratio < MIN_RATIO:
                    failures.append(
                        f"{key}: Text-Safe role {role!r} ({column}={role_hex}) is only "
                        f"{ratio:.2f}:1 against Background={background} "
                        f"(needs >= {MIN_RATIO}:1)"
                    )

        if failures:
            self.fail(
                f"{len(failures)} Text-Safe role(s) fail the 4.5:1 contrast floor "
                "against Background:\n  " + "\n  ".join(failures)
            )

    def test_fill_only_roles_do_not_overlap_text_safe_roles(self):
        """Sanity check on the two columns' own internal consistency: a role
        should never be claimed both Text-Safe and Fill-Only in the same
        row (schema-manifest.json does not already enforce this -- it only
        validates each list column's tokens against its own distinct-token
        rule, not cross-column disjointness)."""
        rows = _read_rows(PALETTES_CSV)
        failures = []
        for row in rows:
            key = row.get("palette_key", "<missing palette_key>")
            text_safe = set(_text_safe_roles(row))
            fill_only_raw = (row.get("Fill-Only Roles") or "").strip()
            fill_only = {tok.strip() for tok in fill_only_raw.split(";") if tok.strip()}
            overlap = text_safe & fill_only
            if overlap:
                failures.append(f"{key}: role(s) {sorted(overlap)} in both columns")
        if failures:
            self.fail("Text-Safe/Fill-Only overlap:\n  " + "\n  ".join(failures))


if __name__ == "__main__":
    unittest.main()
