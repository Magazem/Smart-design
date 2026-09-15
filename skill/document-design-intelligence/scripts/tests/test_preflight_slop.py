#!/usr/bin/env python3
"""Unit tests for preflight.py's research/68-slop-patterns.md mechanical
facts (font families, emoji, border ratios, accent colours, background
image fills, per-page/slide object+word counts).

Fixtures are hand-built minimal OOXML zips, same technique as
tests/fixtures/make_ooxml_fixtures.py: only the parts preflight.py actually
reads are present (word/document.xml for docx, ppt/slides/slideN.xml for
pptx) -- stdlib zipfile does not require a full OPC package (no
[Content_Types].xml or _rels) to read a named member back out.
"""
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS_DIR = HERE.parent
sys.path.insert(0, str(SCRIPTS_DIR))
import preflight  # noqa: E402

_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
_P = "http://schemas.openxmlformats.org/presentationml/2006/main"

_EMOJI = chr(0x1F600)  # grinning face, well inside U+1F300-1FAFF


def _write_zip(tmp_path, parts):
    with zipfile.ZipFile(tmp_path, "w") as zf:
        for name, content in parts.items():
            zf.writestr(name, content)
    return tmp_path


def _docx(tmp_path, body_xml):
    document = (
        f'<?xml version="1.0" encoding="UTF-8"?>'
        f'<w:document xmlns:w="{_W}"><w:body>{body_xml}</w:body></w:document>'
    )
    return _write_zip(tmp_path, {"word/document.xml": document})


def _pptx(tmp_path, *slide_bodies):
    parts = {}
    for i, body_xml in enumerate(slide_bodies, start=1):
        slide = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<p:sld xmlns:p="{_P}" xmlns:a="{_A}"><p:cSld>{body_xml}</p:cSld></p:sld>'
        )
        parts[f"ppt/slides/slide{i}.xml"] = slide
    return _write_zip(tmp_path, parts)


class TestFontFamiliesUsed(unittest.TestCase):
    """Fact (a): distinct font families actually set on a run."""

    def test_docx_counts_distinct_rfonts_ascii_values(self):
        with tempfile.TemporaryDirectory() as d:
            path = _docx(
                Path(d) / "f.docx",
                '<w:p><w:r><w:rPr><w:rFonts w:ascii="Arial"/></w:rPr><w:t>a</w:t></w:r></w:p>'
                '<w:p><w:r><w:rPr><w:rFonts w:ascii="Georgia"/></w:rPr><w:t>b</w:t></w:r></w:p>'
                '<w:p><w:r><w:rPr><w:rFonts w:ascii="Arial"/></w:rPr><w:t>c</w:t></w:r></w:p>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["font_families"],
                              {"count": 2, "names": ["Arial", "Georgia"]})

    def test_pptx_counts_distinct_latin_typeface_values(self):
        with tempfile.TemporaryDirectory() as d:
            path = _pptx(
                Path(d) / "f.pptx",
                '<p:spTree><p:sp><p:txBody>'
                '<a:p><a:r><a:rPr><a:latin typeface="Calibri"/></a:rPr><a:t>x</a:t></a:r></a:p>'
                '</p:txBody></p:sp></p:spTree>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["font_families"], {"count": 1, "names": ["Calibri"]})


class TestEmojiCount(unittest.TestCase):
    """Fact (b): emoji/pictograph codepoints in body text."""

    def test_docx_counts_emoji_in_body_text(self):
        with tempfile.TemporaryDirectory() as d:
            path = _docx(
                Path(d) / "f.docx",
                f'<w:p><w:r><w:t>hello {_EMOJI}{_EMOJI} world</w:t></w:r></w:p>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["emoji_count"], 2)

    def test_pptx_counts_zero_when_no_emoji_present(self):
        with tempfile.TemporaryDirectory() as d:
            path = _pptx(
                Path(d) / "f.pptx",
                '<p:spTree><p:sp><p:txBody><a:p><a:r><a:t>plain text</a:t></a:r></a:p>'
                '</p:txBody></p:sp></p:spTree>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["emoji_count"], 0)


class TestTableCellBorderRatio(unittest.TestCase):
    """Fact (c): cells with all four borders set / all cells."""

    def test_docx_ratio_counts_only_cells_with_all_four_sides(self):
        with tempfile.TemporaryDirectory() as d:
            fully_bordered_tc = (
                '<w:tc><w:tcPr><w:tcBorders>'
                '<w:top w:val="single"/><w:left w:val="single"/>'
                '<w:bottom w:val="single"/><w:right w:val="single"/>'
                '</w:tcBorders></w:tcPr><w:p/></w:tc>'
            )
            partially_bordered_tc = (
                '<w:tc><w:tcPr><w:tcBorders>'
                '<w:top w:val="single"/><w:bottom w:val="nil"/>'
                '</w:tcBorders></w:tcPr><w:p/></w:tc>'
            )
            path = _docx(
                Path(d) / "f.docx",
                f'<w:tbl><w:tr>{fully_bordered_tc}{partially_bordered_tc}</w:tr></w:tbl>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["table_cell_border_ratio"],
                              {"bordered": 1, "total": 2, "ratio": 0.5})

    def test_pptx_ratio_zero_when_no_side_has_a_line(self):
        with tempfile.TemporaryDirectory() as d:
            path = _pptx(
                Path(d) / "f.pptx",
                '<p:spTree><a:tbl><a:tr><a:tc><a:tcPr/></a:tc></a:tr></a:tbl></p:spTree>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["table_cell_border_ratio"],
                              {"bordered": 0, "total": 1, "ratio": 0.0})


class TestBorderedBlockRatio(unittest.TestCase):
    """Fact (d): paragraphs/shapes with a visible border, against the total."""

    def test_docx_counts_paragraphs_with_pborder(self):
        with tempfile.TemporaryDirectory() as d:
            path = _docx(
                Path(d) / "f.docx",
                '<w:p><w:pPr><w:pBorder><w:top w:val="single"/></w:pBorder></w:pPr></w:p>'
                '<w:p><w:pPr/></w:p>'
                '<w:p></w:p>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["bordered_block_ratio"],
                              {"bordered": 1, "total": 3, "ratio": round(1 / 3, 3)})

    def test_pptx_counts_shapes_with_visible_outline(self):
        with tempfile.TemporaryDirectory() as d:
            bordered_sp = '<p:sp><p:spPr><a:ln><a:solidFill/></a:ln></p:spPr></p:sp>'
            unbordered_sp = '<p:sp><p:spPr><a:ln><a:noFill/></a:ln></p:spPr></p:sp>'
            path = _pptx(Path(d) / "f.pptx", f'<p:spTree>{bordered_sp}{unbordered_sp}</p:spTree>')
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["bordered_shape_ratio"],
                              {"bordered": 1, "total": 2, "ratio": 0.5})


class TestAccentColours(unittest.TestCase):
    """Fact (e): accent colours used (run colours, shape fills), as a hex list."""

    def test_docx_collects_run_colours_and_ignores_auto(self):
        with tempfile.TemporaryDirectory() as d:
            path = _docx(
                Path(d) / "f.docx",
                '<w:p><w:r><w:rPr><w:color w:val="FF00AA"/></w:rPr><w:t>x</w:t></w:r></w:p>'
                '<w:p><w:r><w:rPr><w:color w:val="auto"/></w:rPr><w:t>y</w:t></w:r></w:p>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["accent_colours"], ["FF00AA"])

    def test_pptx_collects_solid_fill_srgb_colours(self):
        with tempfile.TemporaryDirectory() as d:
            path = _pptx(
                Path(d) / "f.pptx",
                '<p:spTree><p:sp><p:spPr><a:solidFill><a:srgbClr val="4472C4"/></a:solidFill>'
                '</p:spPr></p:sp></p:spTree>',
            )
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["accent_colours"], ["4472C4"])


class TestBackgroundImageFills(unittest.TestCase):
    """Fact (f): background image fills per slide/page."""

    def test_pptx_counts_slides_with_a_blip_fill_background(self):
        with tempfile.TemporaryDirectory() as d:
            with_bg = (
                '<p:bg><p:bgPr><a:blipFill><a:blip/></a:blipFill></p:bgPr></p:bg>'
                '<p:spTree/>'
            )
            without_bg = '<p:spTree/>'
            path = _pptx(Path(d) / "f.pptx", with_bg, without_bg)
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["background_image_slide_count"], 1)

    def test_docx_zero_when_no_background_element(self):
        with tempfile.TemporaryDirectory() as d:
            path = _docx(Path(d) / "f.docx", "<w:p/>")
            result = preflight.run(str(path))
            self.assertEqual(result["slop"]["background_image_count"], 0)


class TestObjectsAndWordsPerPage(unittest.TestCase):
    """Fact (g): per-page/slide object count and words per slide."""

    def test_pptx_per_slide_object_and_word_counts(self):
        with tempfile.TemporaryDirectory() as d:
            slide1 = (
                '<p:spTree>'
                '<p:sp><p:txBody><a:p><a:r><a:t>three word slide</a:t></a:r></a:p></p:txBody></p:sp>'
                '<p:pic/>'
                '</p:spTree>'
            )
            path = _pptx(Path(d) / "f.pptx", slide1)
            result = preflight.run(str(path))
            per_slide = result["slop"]["per_slide"]
            self.assertEqual(len(per_slide), 1)
            self.assertEqual(per_slide[0]["objects"], 2)
            self.assertEqual(per_slide[0]["words"], 3)

    def test_docx_objects_and_words_per_section_are_approximate_averages(self):
        with tempfile.TemporaryDirectory() as d:
            path = _docx(
                Path(d) / "f.docx",
                '<w:p><w:r><w:t>one two three</w:t></w:r></w:p>'
                '<w:tbl><w:tr><w:tc><w:p/></w:tc></w:tr></w:tbl>'
                '<w:sectPr/>',
            )
            result = preflight.run(str(path))
            s = result["slop"]
            self.assertEqual(s["sections"], 1)
            self.assertEqual(s["objects_per_section"], 2.0)
            self.assertEqual(s["words_per_section"], 3.0)


if __name__ == "__main__":
    unittest.main()
