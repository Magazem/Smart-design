#!/usr/bin/env python3
"""Preflight CLI -- structural facts about a rendered PDF, DOCX, or PPTX.

Usage:
    python3 preflight.py <file.pdf|.docx|.pptx> [--json]

This reports; it does not decide. Every check below states a fact (a count,
a yes/no, a size) with no severity attached -- pass/fail thresholds belong to
the constraints table (T9) once it exists, not to this script. Exit code is
always 0: a malformed or unsupported file produces an error *fact* in the
output, not a nonzero exit, so this can always be piped into something else
without special-casing failure.

PDF: uses lib/pdf.py (page_count, page_boxes, embedded_fonts, raster_dpi) --
see that module for what each check can and cannot know. Boxes are reported
in both pt (native PDF units) and mm.

DOCX/PPTX: zipfile + xml.etree.ElementTree only, no OOXML library. Font
embedding is resolved the correct way for each format (not just "does a
fonts/ folder exist"): DOCX via word/fontTable.xml's <w:embedRegular>-style
children resolved through word/_rels/fontTable.xml.rels to a real zip
member under word/fonts/; PPTX via ppt/presentation.xml's
<p:embeddedFontLst> resolved through ppt/_rels/presentation.xml.rels to a
real zip member under ppt/fonts/. This is the post-render embedding
assertion research/09-library-schema.md's T5 design notes specify
(`validate-font-embedded`).

DOCX also reports the ATS structural breakers from research/16-t9-
constraints-notes.md: multi-column sections (`w:cols` with `w:num > 1`),
tables in the body (`w:tbl`), text boxes (`w:txbxContent` / `v:textbox`),
and whether contact-like content (an "@", or a phone-shaped digit run)
appears in the first body paragraph versus only in header parts -- the
specific ATS failure mode of a CV whose contact info an ATS parser strips
along with the header it lives in.
"""
from __future__ import annotations

import ast
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def _assert_stdlib_only(extra_allowed=()):
    """Fail loudly at import time if a non-stdlib import is ever added here.

    `extra_allowed` permits importing this project's own sibling stdlib-only
    modules (lib/pdf.py, lib/fonts.py) without weakening the check for any
    genuine third-party package -- those names are still rejected.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    allowed = set(sys.stdlib_module_names) | set(extra_allowed)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level or node.module is None:
                continue
            names = [node.module.split(".")[0]]
        else:
            continue
        for name in names:
            if name not in allowed:
                raise AssertionError(
                    f"non-stdlib import '{name}' found in {__file__} -- "
                    "this module must be Python stdlib only"
                )


_assert_stdlib_only(extra_allowed={"pdf", "fonts"})

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import pdf as pdflib  # noqa: E402
import fonts as fontslib  # noqa: E402


# ============ shared XML namespaces (OOXML) ============

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"
_V = "{urn:schemas-microsoft-com:vml}"
_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

_PHONE_RE = re.compile(r"(?:\+?\d[\d\-.\s()]{7,}\d)")
_PT_TO_MM = 25.4 / 72.0

# research/68-slop-patterns.md "Detection" column, mechanical rows. Emoji/pictograph
# ranges per the task brief: misc symbols & pictographs through supplemental symbols
# and pictographs (U+1F300-1FAFF), the misc-symbols/dingbats block AI tools draw single
# glyphs from (U+2600-27BF), and the variation selector that forces emoji presentation
# (U+FE0F) on an otherwise-text-presentation codepoint.
_EMOJI_RANGES = ((0x1F300, 0x1FAFF), (0x2600, 0x27BF), (0xFE0F, 0xFE0F))
_EMOJI_RE = re.compile(
    "[" + "".join(f"{chr(lo)}-{chr(hi)}" for lo, hi in _EMOJI_RANGES) + "]"
)
_HEX_COLOR_RE = re.compile(r"[0-9A-Fa-f]{6}")


def _count_emoji(text):
    return len(_EMOJI_RE.findall(text or ""))


def _pt_to_mm(value):
    return None if value is None else round(value * _PT_TO_MM, 2)


def _box_both_units(box):
    if box is None:
        return None
    return {"pt": [round(v, 2) for v in box], "mm": [_pt_to_mm(v) for v in box]}


# ============ PDF ============

def preflight_pdf(path):
    """Structural facts about one PDF, via lib/pdf.py.

    Returns a dict; see module docstring for what each field can and cannot
    know (inherited directly from lib/pdf.py's own documented limits).
    """
    page_count = pdflib.page_count(path)
    boxes = pdflib.page_boxes(path)
    font_rows = pdflib.embedded_fonts(path)
    image_rows = pdflib.raster_dpi(path)

    pages_out = [
        {
            "object_id": box["object_id"],
            "MediaBox": _box_both_units(box["MediaBox"]),
            "TrimBox": _box_both_units(box["TrimBox"]),
            "BleedBox": _box_both_units(box["BleedBox"]),
        }
        for box in boxes
    ]
    fonts_out = [{"name": name, "embedded": embedded} for name, embedded in font_rows]
    images_out = [
        {
            "object_id": obj_id,
            "width_px": width_px,
            "height_px": height_px,
            "placed_width_pt": placed_width_pt,
            "effective_dpi": dpi,
        }
        for obj_id, width_px, height_px, placed_width_pt, dpi in image_rows
    ]

    embedded_count = sum(1 for _n, e in font_rows if e)
    resolved_dpi_count = sum(1 for row in image_rows if row[4] is not None)
    has_print_boxes = any(b["TrimBox"] or b["BleedBox"] for b in boxes)

    verdicts = [
        {
            "check": "fonts-embedded",
            "detail": f"{embedded_count}/{len(font_rows)} fonts embedded",
            "pass": len(font_rows) > 0 and embedded_count == len(font_rows),
        },
        {
            "check": "raster-placement-resolved",
            "detail": f"{resolved_dpi_count}/{len(image_rows)} images with a resolved placed size",
            "pass": resolved_dpi_count == len(image_rows),
        },
        {
            "check": "print-production-boxes",
            "detail": (
                "TrimBox/BleedBox present on at least one page"
                if has_print_boxes
                else "no TrimBox/BleedBox on any page -- plain print-shop-submittable "
                     "at best, not press-ready (research/14-print-production-values.md section 1)"
            ),
            "pass": has_print_boxes,
        },
    ]

    return {
        "file_type": "pdf",
        "page_count": page_count,
        "pages": pages_out,
        "fonts": fonts_out,
        "images": images_out,
        "verdicts": verdicts,
    }


# ============ OOXML shared helpers ============

def _parse_rels(zf, rels_path):
    """Return {r:id: target} from a .rels part, or {} if the part is absent
    or unparseable -- a missing .rels part means "nothing is embedded", not
    an error worth surfacing to a caller that only wants a yes/no."""
    try:
        data = zf.read(rels_path)
    except KeyError:
        return {}
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return {}
    return {rel.get("Id"): rel.get("Target") for rel in root.findall(f"{_PR}Relationship")}


def _resolve_target(base_dir, target):
    """Resolve a .rels Target (commonly relative, e.g. 'fonts/x.odttf')
    against the referencing part's own directory into a zip member name."""
    if not target:
        return None
    if target.startswith("/"):
        return target.lstrip("/")
    return str(Path(base_dir, target).as_posix())


def _text_of(root, w_ns):
    """Concatenate every w:t descendant's text under `root`."""
    return "".join(t.text or "" for t in root.findall(f".//{w_ns}t"))


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


# ============ DOCX ============

_EMBED_TAGS = ("embedRegular", "embedBold", "embedItalic", "embedBoldItalic")


def _docx_fonts(zf):
    try:
        data = zf.read("word/fontTable.xml")
    except KeyError:
        return []
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return []

    rels = _parse_rels(zf, "word/_rels/fontTable.xml.rels")
    member_names = set(zf.namelist())

    results = []
    for font_el in root.findall(f"{_W}font"):
        name = font_el.get(f"{_W}name") or "(unnamed)"
        embedded = False
        for tag in _EMBED_TAGS:
            embed_el = font_el.find(f"{_W}{tag}")
            if embed_el is None:
                continue
            rid = embed_el.get(f"{_R}id")
            target = _resolve_target("word", rels.get(rid))
            if target and target in member_names:
                embedded = True
                break
        results.append({"name": name, "embedded": embedded})
    return results


def _docx_structure(zf):
    try:
        doc_root = ET.fromstring(zf.read("word/document.xml"))
    except (KeyError, ET.ParseError):
        return {
            "multi_column_sections": None,
            "tables": None,
            "text_boxes": None,
            "contact_in_first_body_paragraph": None,
            "contact_in_header": None,
            "contact_only_in_header": None,
        }

    cols_elements = doc_root.findall(f".//{_W}cols")
    multi_col_count = sum(
        1 for c in cols_elements if (_safe_int(c.get(f"{_W}num")) or 0) > 1
    )

    table_count = len(doc_root.findall(f".//{_W}tbl"))

    textbox_count = (
        len(doc_root.findall(f".//{_W}txbxContent"))
        + len(doc_root.findall(f".//{_V}textbox"))
    )

    body = doc_root.find(f"{_W}body")
    first_para_text = ""
    if body is not None:
        first_p = body.find(f"{_W}p")
        if first_p is not None:
            first_para_text = _text_of(first_p, _W)

    contact_in_body = "@" in first_para_text or bool(_PHONE_RE.search(first_para_text))

    header_text = ""
    rels = _parse_rels(zf, "word/_rels/document.xml.rels")
    for target in rels.values():
        if not target or "header" not in target.lower():
            continue
        resolved = _resolve_target("word", target)
        try:
            header_root = ET.fromstring(zf.read(resolved))
        except (KeyError, ET.ParseError, TypeError):
            continue
        header_text += _text_of(header_root, _W)

    contact_in_header = "@" in header_text or bool(_PHONE_RE.search(header_text))

    return {
        "multi_column_sections": multi_col_count,
        "tables": table_count,
        "text_boxes": textbox_count,
        "contact_in_first_body_paragraph": contact_in_body,
        "contact_in_header": contact_in_header,
        "contact_only_in_header": contact_in_header and not contact_in_body,
    }


# ============ DOCX -- research/68-slop-patterns.md mechanical facts ============

def _docx_font_families(doc_root):
    """Distinct font families actually set on a run (w:rFonts), not merely
    listed in fontTable.xml -- a family can be referenced there and never
    used, or used without a fontTable entry at all."""
    families = set()
    for rfonts in doc_root.findall(f".//{_W}rFonts"):
        for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
            val = rfonts.get(f"{_W}{attr}")
            if val:
                families.add(val)
    return families


def _docx_all_borders_set(borders_el):
    for side in ("top", "left", "bottom", "right"):
        side_el = borders_el.find(f"{_W}{side}")
        if side_el is None:
            return False
        val = side_el.get(f"{_W}val")
        if not val or val in ("nil", "none"):
            return False
    return True


def _docx_table_cell_border_ratio(doc_root):
    cells = doc_root.findall(f".//{_W}tc")
    total = len(cells)
    bordered = 0
    for tc in cells:
        tc_pr = tc.find(f"{_W}tcPr")
        borders = tc_pr.find(f"{_W}tcBorders") if tc_pr is not None else None
        if borders is not None and _docx_all_borders_set(borders):
            bordered += 1
    return bordered, total


def _docx_bordered_block_ratio(doc_root):
    """Paragraphs with a visible border (w:pPr/w:pBorder), against all
    paragraphs -- the "frames around everything" pattern applied to blocks
    rather than table cells (see _docx_table_cell_border_ratio)."""
    paragraphs = doc_root.findall(f".//{_W}p")
    total = len(paragraphs)
    bordered = 0
    for p in paragraphs:
        p_pr = p.find(f"{_W}pPr")
        if p_pr is not None and p_pr.find(f"{_W}pBorder") is not None:
            bordered += 1
    return bordered, total


def _docx_accent_colours(zf, doc_root):
    colours = set()
    for color_el in doc_root.findall(f".//{_W}color"):
        val = (color_el.get(f"{_W}val") or "").strip()
        if val.lower() != "auto" and _HEX_COLOR_RE.fullmatch(val):
            colours.add(val.upper())
    try:
        theme_root = ET.fromstring(zf.read("word/theme/theme1.xml"))
    except (KeyError, ET.ParseError):
        theme_root = None
    if theme_root is not None:
        accent1 = theme_root.find(f".//{_A}clrScheme/{_A}accent1/{_A}srgbClr")
        if accent1 is not None and accent1.get("val"):
            colours.add(accent1.get("val").upper())
    return sorted(colours)


def _docx_background_image_count(zf, doc_root):
    """0 or 1: DOCX has a single document-wide background (w:background),
    not a per-page one -- present only if it resolves to a real image
    relationship, matching how font embedding is resolved above."""
    bg = doc_root.find(f"{_W}background")
    if bg is None:
        return 0
    rid = bg.get(f"{_R}id")
    if not rid:
        return 0
    rels = _parse_rels(zf, "word/_rels/document.xml.rels")
    return 1 if _resolve_target("word", rels.get(rid)) in set(zf.namelist()) else 0


def _docx_objects_and_words_per_section(doc_root):
    """Per-section object count and words are approximate: docx has no
    per-page layout fact available from the XML alone, so this divides the
    body's paragraph+table count and word count across its w:sectPr count."""
    body = doc_root.find(f"{_W}body")
    if body is None:
        return {"sections": 0, "objects_per_section": None, "words_per_section": None}
    sections = len(doc_root.findall(f".//{_W}sectPr")) or 1
    object_count = len(body.findall(f"{_W}p")) + len(body.findall(f"{_W}tbl"))
    word_count = len(_text_of(body, _W).split())
    return {
        "sections": sections,
        "objects_per_section": round(object_count / sections, 1),
        "words_per_section": round(word_count / sections, 1),
    }


def _docx_slop_facts(zf, doc_root):
    families = sorted(_docx_font_families(doc_root))
    emoji_count = _count_emoji(_text_of(doc_root, _W))
    cell_bordered, cell_total = _docx_table_cell_border_ratio(doc_root)
    block_bordered, block_total = _docx_bordered_block_ratio(doc_root)
    return {
        "font_families": {"count": len(families), "names": families},
        "emoji_count": emoji_count,
        "table_cell_border_ratio": {
            "bordered": cell_bordered, "total": cell_total,
            "ratio": round(cell_bordered / cell_total, 3) if cell_total else None,
        },
        "bordered_block_ratio": {
            "bordered": block_bordered, "total": block_total,
            "ratio": round(block_bordered / block_total, 3) if block_total else None,
        },
        "accent_colours": _docx_accent_colours(zf, doc_root),
        "background_image_count": _docx_background_image_count(zf, doc_root),
        **_docx_objects_and_words_per_section(doc_root),
    }


def preflight_docx(path):
    with zipfile.ZipFile(path) as zf:
        fonts_out = _docx_fonts(zf)
        structure = _docx_structure(zf)
        try:
            doc_root = ET.fromstring(zf.read("word/document.xml"))
        except (KeyError, ET.ParseError):
            doc_root = None
        slop = _docx_slop_facts(zf, doc_root) if doc_root is not None else None
    return {"file_type": "docx", "fonts": fonts_out, "structure": structure, "slop": slop}


# ============ PPTX ============

_IGNORED_THEME_PLACEHOLDERS = {"+mn-lt", "+mj-lt", "+mn-ea", "+mj-ea", "+mn-cs", "+mj-cs"}
_EMBED_FONT_STYLE_TAGS = ("regular", "bold", "italic", "boldItalic")


def _pptx_fonts(zf):
    member_names = set(zf.namelist())

    referenced = set()
    for member in member_names:
        if not re.match(r"ppt/(slides|theme)/[^/]+\.xml$", member):
            continue
        try:
            root = ET.fromstring(zf.read(member))
        except ET.ParseError:
            continue
        for el in root.iter():
            typeface = el.get("typeface")
            if typeface and typeface not in _IGNORED_THEME_PLACEHOLDERS:
                referenced.add(typeface)

    embedded = set()
    try:
        pres_root = ET.fromstring(zf.read("ppt/presentation.xml"))
    except (KeyError, ET.ParseError):
        pres_root = None

    if pres_root is not None:
        rels = _parse_rels(zf, "ppt/_rels/presentation.xml.rels")
        for embedded_font in pres_root.findall(f".//{_P}embeddedFontLst/{_P}embeddedFont"):
            font_el = embedded_font.find(f"{_P}font")
            if font_el is None:
                continue
            typeface = font_el.get("typeface")
            has_file = False
            for tag in _EMBED_FONT_STYLE_TAGS:
                style_el = embedded_font.find(f"{_P}{tag}")
                if style_el is None:
                    continue
                rid = style_el.get(f"{_R}id")
                target = _resolve_target("ppt", rels.get(rid))
                if target and target in member_names:
                    has_file = True
                    break
            if has_file:
                embedded.add(typeface)
                referenced.add(typeface)

    return [
        {"name": name, "embedded": name in embedded}
        for name in sorted(referenced)
    ]


# ============ PPTX -- research/68-slop-patterns.md mechanical facts ============

def _pptx_slide_members(zf):
    return sorted(m for m in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", m))


def _pptx_slide_roots(zf):
    for member in _pptx_slide_members(zf):
        try:
            yield ET.fromstring(zf.read(member))
        except ET.ParseError:
            continue


def _pptx_font_families(zf):
    """Distinct typefaces actually set on a run/default run (a:latin), not
    merely referenced in the theme -- the "used" counterpart to _pptx_fonts,
    which resolves embedding for typefaces referenced anywhere at all."""
    families = set()
    for root in _pptx_slide_roots(zf):
        for latin in root.iter(f"{_A}latin"):
            typeface = latin.get("typeface")
            if typeface and typeface not in _IGNORED_THEME_PLACEHOLDERS:
                families.add(typeface)
    return families


def _pptx_body_text(zf):
    return "".join(
        " ".join(t.text or "" for t in root.iter(f"{_A}t"))
        for root in _pptx_slide_roots(zf)
    )


def _pptx_all_borders_set(tc_pr):
    for tag in ("lnL", "lnR", "lnT", "lnB"):
        ln = tc_pr.find(f"{_A}{tag}")
        if ln is None or ln.find(f"{_A}noFill") is not None:
            return False
    return True


def _pptx_table_cell_border_ratio(zf):
    total = 0
    bordered = 0
    for root in _pptx_slide_roots(zf):
        for tc in root.iter(f"{_A}tc"):
            total += 1
            tc_pr = tc.find(f"{_A}tcPr")
            if tc_pr is not None and _pptx_all_borders_set(tc_pr):
                bordered += 1
    return bordered, total


def _pptx_bordered_shape_ratio(zf):
    """Shapes (p:sp) with a visible outline (a:ln, not a:noFill), against all
    shapes -- the deck-level counterpart to _docx_bordered_block_ratio."""
    total = 0
    bordered = 0
    for root in _pptx_slide_roots(zf):
        for sp in root.iter(f"{_P}sp"):
            total += 1
            sp_pr = sp.find(f"{_P}spPr")
            ln = sp_pr.find(f"{_A}ln") if sp_pr is not None else None
            if ln is not None and ln.find(f"{_A}noFill") is None:
                bordered += 1
    return bordered, total


def _pptx_accent_colours(zf):
    colours = set()
    for root in _pptx_slide_roots(zf):
        for srgb in root.iter(f"{_A}srgbClr"):
            val = (srgb.get("val") or "").strip()
            if _HEX_COLOR_RE.fullmatch(val):
                colours.add(val.upper())
    try:
        theme_root = ET.fromstring(zf.read("ppt/theme/theme1.xml"))
    except (KeyError, ET.ParseError):
        theme_root = None
    if theme_root is not None:
        accent1 = theme_root.find(f".//{_A}clrScheme/{_A}accent1/{_A}srgbClr")
        if accent1 is not None and accent1.get("val"):
            colours.add(accent1.get("val").upper())
    return sorted(colours)


def _pptx_background_image_slide_count(zf):
    count = 0
    for root in _pptx_slide_roots(zf):
        bg = root.find(f"{_P}cSld/{_P}bg")
        if bg is not None and bg.find(f".//{_A}blipFill") is not None:
            count += 1
    return count


_SLIDE_OBJECT_TAGS = ("sp", "pic", "graphicFrame", "grpSp", "cxnSp")


def _pptx_objects_and_words_per_slide(zf):
    per_slide = []
    for member, root in zip(_pptx_slide_members(zf), _pptx_slide_roots(zf)):
        sp_tree = root.find(f"{_P}cSld/{_P}spTree")
        object_count = (
            sum(len(sp_tree.findall(f"{_P}{tag}")) for tag in _SLIDE_OBJECT_TAGS)
            if sp_tree is not None else 0
        )
        words = len(" ".join(t.text or "" for t in root.iter(f"{_A}t")).split())
        per_slide.append({"slide": member, "objects": object_count, "words": words})
    return per_slide


def _pptx_slop_facts(zf):
    families = sorted(_pptx_font_families(zf))
    emoji_count = _count_emoji(_pptx_body_text(zf))
    cell_bordered, cell_total = _pptx_table_cell_border_ratio(zf)
    shape_bordered, shape_total = _pptx_bordered_shape_ratio(zf)
    return {
        "font_families": {"count": len(families), "names": families},
        "emoji_count": emoji_count,
        "table_cell_border_ratio": {
            "bordered": cell_bordered, "total": cell_total,
            "ratio": round(cell_bordered / cell_total, 3) if cell_total else None,
        },
        "bordered_shape_ratio": {
            "bordered": shape_bordered, "total": shape_total,
            "ratio": round(shape_bordered / shape_total, 3) if shape_total else None,
        },
        "accent_colours": _pptx_accent_colours(zf),
        "background_image_slide_count": _pptx_background_image_slide_count(zf),
        "per_slide": _pptx_objects_and_words_per_slide(zf),
    }


#: research/87 F10 / research/90 F10: python-pptx cannot embed fonts, so a bare "fonts must be
#: embedded" check was unsatisfiable for that renderer. `pptx-font-embedded`
#: (constraints.csv, Threshold `present-or-declared`) passes when every referenced font is
#: embedded OR the file DECLARES the safe-stack fallback: the deck's core-properties `keywords`
#: contain this token (python-pptx: `prs.core_properties.keywords = "ddi-font-rule=safe-stack"`),
#: which the pptx handoff instructs whenever the typeface's licence forbids embedding or the
#: renderer cannot embed.
FONT_RULE_DECLARATION = "ddi-font-rule=safe-stack"


def _pptx_font_rule_declared(zf):
    """True if docProps/core.xml keywords (or a docProps/custom.xml property) carries the
    safe-stack declaration."""
    for member in ("docProps/core.xml", "docProps/custom.xml"):
        try:
            data = zf.read(member).decode("utf-8", "replace")
        except KeyError:
            continue
        if FONT_RULE_DECLARATION in data or "ddi-font-rule" in data and "safe-stack" in data:
            return True
    return False


def pptx_font_verdict(fonts, declared):
    """The `pptx-font-embedded` verdict: PASS iff every referenced font is embedded, or the
    safe-stack fallback is declared; FAIL only when neither holds."""
    embedded = sum(1 for f in fonts if f["embedded"])
    all_embedded = bool(fonts) and embedded == len(fonts)
    if all_embedded:
        detail = f"{embedded}/{len(fonts)} fonts embedded"
    elif declared:
        detail = (f"{embedded}/{len(fonts)} fonts embedded; safe-stack fallback declared "
                  f"({FONT_RULE_DECLARATION})")
    else:
        detail = (f"{embedded}/{len(fonts)} fonts embedded and no `{FONT_RULE_DECLARATION}` declaration -- "
                  "embed the fonts, or declare the safe-stack fallback")
    return {"check": "pptx-font-embedded", "detail": detail, "pass": all_embedded or declared}


def preflight_pptx(path):
    with zipfile.ZipFile(path) as zf:
        fonts_out = _pptx_fonts(zf)
        slop = _pptx_slop_facts(zf)
        declared = _pptx_font_rule_declared(zf)
    return {"file_type": "pptx", "fonts": fonts_out, "slop": slop, "font_rule_declared": declared,
            "verdicts": [pptx_font_verdict(fonts_out, declared)]}


# ============ output formatting ============

def _print_human_pdf(result, path):
    print(f"{path}  (pdf)")
    print(f"  pages: {result['page_count']}")
    for page in result["pages"]:
        def fmt(box):
            if box is None:
                return "none"
            pt = ",".join(f"{v:.2f}" for v in box["pt"])
            mm = ",".join(f"{v:.2f}" for v in box["mm"])
            return f"[{pt}] pt  /  [{mm}] mm"
        print(f"  page (obj {page['object_id']}):")
        print(f"    MediaBox: {fmt(page['MediaBox'])}")
        print(f"    TrimBox:  {fmt(page['TrimBox'])}")
        print(f"    BleedBox: {fmt(page['BleedBox'])}")
    print("  fonts:")
    for font in result["fonts"]:
        print(f"    {font['name']}: embedded={'yes' if font['embedded'] else 'no'}")
    print("  images:")
    for image in result["images"]:
        dpi = image["effective_dpi"]
        placed = image["placed_width_pt"]
        print(
            f"    obj {image['object_id']}: {image['width_px']}x{image['height_px']}px "
            f"placed={placed if placed is not None else 'unresolved'}pt "
            f"dpi={dpi if dpi is not None else 'unresolved'}"
        )
    print("  verdicts:")
    for verdict in result["verdicts"]:
        mark = "PASS" if verdict["pass"] else "FAIL"
        print(f"    [{mark}] {verdict['check']}: {verdict['detail']}")


def _print_human_docx(result, path):
    print(f"{path}  (docx)")
    print("  fonts referenced:")
    for font in result["fonts"]:
        print(f"    {font['name']}: embedded={'yes' if font['embedded'] else 'no'}")
    s = result["structure"]
    print("  structure (facts only -- no severity):")
    print(f"    multi-column sections: {s['multi_column_sections']}")
    print(f"    tables: {s['tables']}")
    print(f"    text boxes: {s['text_boxes']}")
    print(f"    contact-like content in first body paragraph: {s['contact_in_first_body_paragraph']}")
    print(f"    contact-like content in a header part: {s['contact_in_header']}")
    print(f"    contact-like content only in a header part: {s['contact_only_in_header']}")
    _print_human_slop(result.get("slop"))


def _print_human_slop(slop):
    print("  slop facts (facts only -- no severity):")
    if slop is None:
        print("    (unavailable -- main document part missing or unparseable)")
        return
    ff = slop["font_families"]
    print(f"    font families used: {ff['count']} ({', '.join(ff['names']) or 'none'})")
    print(f"    emoji/pictograph codepoints: {slop['emoji_count']}")
    for key, label in (("table_cell_border_ratio", "table-cell border ratio"),
                        ("bordered_block_ratio", "bordered-block ratio"),
                        ("bordered_shape_ratio", "bordered-shape ratio")):
        if key not in slop:
            continue
        r = slop[key]
        ratio = f"{r['ratio']:.3f}" if r["ratio"] is not None else "n/a"
        print(f"    {label}: {r['bordered']}/{r['total']} ({ratio})")
    print(f"    accent colours: {', '.join(slop['accent_colours']) or 'none'}")
    if "background_image_count" in slop:
        print(f"    background image fills: {slop['background_image_count']}")
        print(f"    sections: {slop['sections']}  "
              f"objects/section (approx): {slop['objects_per_section']}  "
              f"words/section (approx): {slop['words_per_section']}")
    if "background_image_slide_count" in slop:
        print(f"    background image fills (slides): {slop['background_image_slide_count']}")
        for row in slop["per_slide"]:
            print(f"    {row['slide']}: objects={row['objects']} words={row['words']}")


def _print_human_pptx(result, path):
    print(f"{path}  (pptx)")
    print("  fonts referenced:")
    for font in result["fonts"]:
        print(f"    {font['name']}: embedded={'yes' if font['embedded'] else 'no'}")
    print("  verdicts:")
    for verdict in result.get("verdicts", []):
        mark = "PASS" if verdict["pass"] else "FAIL"
        print(f"    [{mark}] {verdict['check']}: {verdict['detail']}")
    _print_human_slop(result.get("slop"))


_PRINTERS = {"pdf": _print_human_pdf, "docx": _print_human_docx, "pptx": _print_human_pptx}
_HANDLERS = {"pdf": preflight_pdf, "docx": preflight_docx, "pptx": preflight_pptx}


def run(path_str):
    """Dispatch on file extension and return a result dict. Never raises for
    a normal usage error (unsupported extension, missing/unreadable file) --
    those become an {"error": ...} fact in the returned dict, per this
    script's "report, don't decide" contract."""
    path = Path(path_str)
    ext = path.suffix.lower().lstrip(".")
    if ext not in _HANDLERS:
        return {"error": f"unsupported file type '.{ext}' (expected .pdf, .docx, or .pptx)"}
    try:
        return _HANDLERS[ext](str(path))
    except FileNotFoundError:
        return {"error": f"file not found: {path}"}
    except (zipfile.BadZipFile, OSError) as exc:
        return {"error": f"could not read {path}: {exc}"}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    positional = [a for a in argv if not a.startswith("--")]

    if not positional:
        print("usage: preflight.py <file.pdf|.docx|.pptx> [--json]")
        return 0

    result = run(positional[0])

    if as_json:
        print(json.dumps(result, indent=2))
        return 0

    if "error" in result:
        print(f"{positional[0]}: {result['error']}")
        return 0

    _PRINTERS[result["file_type"]](result, positional[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
