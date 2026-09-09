#!/usr/bin/env python3
"""Unit tests for scripts/build_zip.py, focused on the data/brand/<slug>/
exclusion: a user's installed brand overlay must never ship inside the
public skill ZIP (privacy defect, not a tidiness one - see
research/brief-packaging.md step 3). Builds a synthetic skill tree in a
temp dir (--allow-empty-data, so the real data/base gate is not exercised
here) rather than touching the live skill dir.
"""
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import build_zip  # noqa: E402


def _make_fake_skill_dir(root: Path) -> Path:
    skill_dir = root / "document-design-intelligence"
    (skill_dir / "data" / "brand" / "ens" / "assets").mkdir(parents=True)
    (skill_dir / "scripts").mkdir(parents=True)

    (skill_dir / "SKILL.md").write_text(
        '---\nname: document-design-intelligence\ndescription: "test skill"\n---\nBody\n',
        encoding="utf-8",
    )
    (skill_dir / "VERSION").write_text("0.0.1\n", encoding="utf-8")
    (skill_dir / "scripts" / "foo.py").write_text("# placeholder\n", encoding="utf-8")

    # data/brand/'s own documentation - must still ship.
    (skill_dir / "data" / "brand" / "README.md").write_text("brand contract\n", encoding="utf-8")
    (skill_dir / "data" / "brand" / ".gitkeep").write_text("", encoding="utf-8")

    # which brand is active - user state, must NOT ship.
    (skill_dir / "data" / "brand" / "active.json").write_text('{"active": "ens"}', encoding="utf-8")

    # a user's installed brand overlay - must NOT ship.
    (skill_dir / "data" / "brand" / "ens" / "brand.md").write_text("slug: ens\n", encoding="utf-8")
    (skill_dir / "data" / "brand" / "ens" / "typefaces.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (skill_dir / "data" / "brand" / "ens" / "assets" / "logo.png").write_bytes(b"\x89PNG")

    return skill_dir


class TestBrandOverlayExcluded(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.skill_dir = _make_fake_skill_dir(self.root)
        self.dist_dir = self.root / "dist"

    def tearDown(self):
        self.tmp.cleanup()

    def test_is_brand_overlay_path_flags_slug_subdirs_and_active_json(self):
        f = build_zip.is_brand_overlay_path
        self.assertTrue(f(Path("data/brand/ens/brand.md")))
        self.assertTrue(f(Path("data/brand/ens/assets/logo.png")))
        self.assertTrue(f(Path("data/brand/active.json")))
        self.assertFalse(f(Path("data/brand/README.md")))
        self.assertFalse(f(Path("data/brand/.gitkeep")))
        self.assertFalse(f(Path("data/base/typefaces.csv")))

    def test_built_zip_excludes_brand_overlay_but_keeps_brand_readme(self):
        out_path = build_zip.build(self.skill_dir, self.dist_dir, allow_empty_data=True)
        with zipfile.ZipFile(out_path) as zf:
            names = zf.namelist()

        brand_state_paths = [
            n for n in names if "data/brand/ens/" in n or n.endswith("data/brand/active.json")
        ]
        self.assertEqual(
            brand_state_paths, [],
            f"brand overlay/state files leaked into the built ZIP: {brand_state_paths}",
        )
        self.assertTrue(any(n.endswith("data/brand/README.md") for n in names))
        self.assertTrue(any(n.endswith("SKILL.md") for n in names))


if __name__ == "__main__":
    unittest.main()
