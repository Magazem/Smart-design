#!/usr/bin/env python3
"""research/87 I7: every doctype's resolved type scale (doctype -> Reasoning Key ->
Typeface Key -> Scale Key) must carry `body` plus every heading role h1..hN up to
its structure's `Heading Depth Max`."""
import csv
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent / "data" / "base"


def _rows(name):
    with open(BASE / f"{name}.csv", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class TestScaleCoversStructureDepth(unittest.TestCase):
    def test_every_doctype_scale_has_body_and_headings_to_depth(self):
        roles = {}
        for r in _rows("type-scales"):
            roles.setdefault(r["scale_key"], set()).add(r["Role"])
        typefaces = {r["typeface_key"]: r for r in _rows("typefaces")}
        reasoning = {r["doc_category"]: r for r in _rows("doc-reasoning")}
        structures = {r["structure_key"]: r for r in _rows("structures")}
        for d in _rows("doctypes"):
            with self.subTest(doc_key=d["doc_key"]):
                scale = typefaces[reasoning[d["Reasoning Key"]]["Typeface Key"]]["Scale Key"]
                depth = 0
                if d["Structure Key"]:
                    depth = int(structures[d["Structure Key"]]["Heading Depth Max"] or 0)
                need = {"body"} | {f"h{i}" for i in range(1, depth + 1)}
                missing = need - roles.get(scale, set())
                self.assertFalse(missing, f"{d['doc_key']}: scale {scale!r} lacks {sorted(missing)}")


if __name__ == "__main__":
    unittest.main()
