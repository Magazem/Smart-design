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

_PHONE_RE = re.compile(r"(?:\+?\d[\d\-.\s()]{7,}\d)")
_PT_TO_MM = 25.4 / 72.0


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


def preflight_docx(path):
    with zipfile.ZipFile(path) as zf:
        fonts_out = _docx_fonts(zf)
        structure = _docx_structure(zf)
    return {"file_type": "docx", "fonts": fonts_out, "structure": structure}


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


def preflight_pptx(path):
    with zipfile.ZipFile(path) as zf:
        fonts_out = _pptx_fonts(zf)
    return {"file_type": "pptx", "fonts": fonts_out}


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


def _print_human_pptx(result, path):
    print(f"{path}  (pptx)")
    print("  fonts referenced:")
    for font in result["fonts"]:
        print(f"    {font['name']}: embedded={'yes' if font['embedded'] else 'no'}")


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
