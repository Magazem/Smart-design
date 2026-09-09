#!/usr/bin/env python3
"""PDF structural primitives for a Chromium- or WeasyPrint-emitted PDF.

Uses `re` + `zlib` only, per research/14-print-production-values.md section 3: PDF
is largely a plain-text object/dictionary format with FlateDecode
(zlib-deflate) compressed content and stream data, which makes dictionary
presence checks and content-stream token scans genuinely stdlib-feasible.
There is no PDF object model in the standard library, so this module is a
narrow, honest parser, not a general PDF reader. Known limitations, stated
once here rather than repeated in every function:

  - **Compressed object streams** (`/Type /ObjStm`, PDF 1.5+ cross-reference
    streams) are not decoded. An object that a writer chose to store inside
    a compressed object stream is invisible to every function below. The
    two engines this module targets (headless Chromium, WeasyPrint) were
    both verified in research/05-SYNTHESIS.md / this module's own tests to
    emit classic, uncompressed cross-reference tables for simple documents;
    this is a real gap for any *other* PDF writer, not a theoretical one.
  - **Page-tree attribute inheritance** (e.g. a `/MediaBox` set once on a
    `/Pages` node and inherited by every child `/Page` that doesn't repeat
    it) is not resolved. Only boxes present directly on the `/Page` object
    itself are reported.
  - **Object bodies are located with a regex up to the literal `endobj`
    keyword.** A stream whose own compressed binary payload happens to
    contain that byte sequence before the true terminator would truncate
    the match early. Not observed in testing; flagged because it is a real
    property of a regex-based (non-object-graph) parser, not a solved one.
  - Image placement resolution only follows the standard `cm`/`Do` content
    stream idiom (with correct `q`/`Q` graphics-state stack handling -- see
    `raster_dpi`). Inline images (`BI`/`ID`/`EI`) are not resolved.
"""

import ast
import math
import re
import struct
import sys
import zlib
from pathlib import Path


def _assert_stdlib_only():
    """Fail loudly at import time if a non-stdlib import is ever added here.

    See fonts.py for the identical guard and rationale.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    stdlib = sys.stdlib_module_names
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
            if name not in stdlib:
                raise AssertionError(
                    f"non-stdlib import '{name}' found in {__file__} -- "
                    "this module must be Python stdlib only"
                )


_assert_stdlib_only()


# ============ low-level object/dictionary parsing (module-private) ============

_OBJ_RE = re.compile(rb"(?P<num>\d+)\s+(?P<gen>\d+)\s+obj\b(?P<body>.*?)endobj", re.DOTALL)
_STREAM_START_RE = re.compile(rb"stream(\r\n|\n)")
_NUM = rb"[+-]?(?:\d+\.?\d*|\.\d+)"


def _extract_stream(obj_body):
    """Split one object's raw body into (dict_bytes, stream_bytes_or_None).

    Uses the dictionary's own `/Length` when it is a direct integer (the
    correct, spec-conformant way to find the end of stream data, since
    stream bytes are arbitrary binary and may legitimately contain the
    literal text "endstream"). Falls back to searching for the literal
    `endstream` keyword -- stripping one trailing EOL -- only when `/Length`
    is missing or is itself an indirect reference (unresolvable without a
    second pass over the whole object table); this fallback is the one
    place this parser can be fooled by binary data that happens to contain
    "endstream" before the real terminator.
    """
    sm = _STREAM_START_RE.search(obj_body)
    if not sm:
        return obj_body, None
    dict_bytes = obj_body[:sm.start()]
    data_start = sm.end()

    if re.search(rb"/Length\s+\d+\s+\d+\s+R", dict_bytes):
        length = None  # indirect -- not resolved here, use the fallback below
    else:
        m = re.search(rb"/Length\s+(\d+)", dict_bytes)
        length = int(m.group(1)) if m else None

    if length is not None:
        return dict_bytes, obj_body[data_start:data_start + length]

    em = re.search(rb"endstream", obj_body[data_start:])
    if not em:
        return dict_bytes, None
    raw = obj_body[data_start:data_start + em.start()]
    if raw.endswith(b"\r\n"):
        raw = raw[:-2]
    elif raw.endswith(b"\n") or raw.endswith(b"\r"):
        raw = raw[:-1]
    return dict_bytes, raw


def _iter_objects(data):
    """Return {object_number: (dict_bytes, stream_bytes_or_None)} for every
    top-level (non-compressed-object-stream) indirect object in the file."""
    objects = {}
    for m in _OBJ_RE.finditer(data):
        dict_bytes, stream_bytes = _extract_stream(m.group("body"))
        objects[int(m.group("num"))] = (dict_bytes, stream_bytes)
    return objects


def _maybe_inflate(dict_bytes, stream_bytes):
    """Return zlib-decompressed stream bytes if /Filter says FlateDecode,
    else None (either not Flate-filtered, or decompression failed)."""
    if stream_bytes is None or dict_bytes is None:
        return None
    if re.search(rb"/Filter\s*/FlateDecode", dict_bytes) or \
       re.search(rb"/Filter\s*\[\s*/FlateDecode", dict_bytes):
        try:
            return zlib.decompress(stream_bytes)
        except zlib.error:
            return None
    return None


def _value_span(data, start):
    """Return (raw_value_bytes, end_index) for the PDF value beginning at or
    after `start`, handling bracket-balanced `<<...>>` dicts and `[...]`
    arrays correctly (a non-greedy regex would stop at the first nested
    close bracket, which is wrong for nested dictionaries)."""
    i = start
    while i < len(data) and data[i:i + 1].isspace():
        i += 1
    if data[i:i + 2] == b"<<":
        depth, j = 0, i
        while j < len(data):
            if data[j:j + 2] == b"<<":
                depth += 1
                j += 2
            elif data[j:j + 2] == b">>":
                depth -= 1
                j += 2
                if depth == 0:
                    return data[i:j], j
            else:
                j += 1
        return data[i:], len(data)
    if data[i:i + 1] == b"[":
        depth, j = 0, i
        while j < len(data):
            if data[j:j + 1] == b"[":
                depth += 1
            elif data[j:j + 1] == b"]":
                depth -= 1
                if depth == 0:
                    return data[i:j + 1], j + 1
            j += 1
        return data[i:], len(data)
    m = re.match(rb"/[^\s/\[\]<>()]+|[^/\[\]<>]*", data[i:])
    return m.group(0), i + m.end()


def _get_raw(dict_bytes, key):
    """Return the raw value bytes following `/key` in `dict_bytes`, or None."""
    if dict_bytes is None:
        return None
    m = re.search(rb"/" + re.escape(key) + rb"(?![A-Za-z0-9])", dict_bytes)
    if not m:
        return None
    value, _end = _value_span(dict_bytes, m.end())
    return value.strip()


def _ref_num(dict_bytes, key):
    """Return the object number if `/key` is an indirect reference `N G R`."""
    raw = _get_raw(dict_bytes, key)
    if raw is None:
        return None
    m = re.fullmatch(rb"(\d+)\s+\d+\s+R", raw)
    return int(m.group(1)) if m else None


def _resolve(dict_bytes, key, objects):
    """Return the raw value for `key`, following one indirect reference
    through `objects` if present, else the inline value."""
    num = _ref_num(dict_bytes, key)
    if num is not None:
        entry = objects.get(num)
        return entry[0] if entry else None
    return _get_raw(dict_bytes, key)


def _as_name(raw):
    if raw is None:
        return None
    m = re.match(rb"/([^\s/\[\]<>()]+)", raw)
    return m.group(1).decode("latin-1") if m else None


def _as_int(raw):
    if raw is None:
        return None
    m = re.match(rb"\s*(-?\d+)", raw)
    return int(m.group(1)) if m else None


def _as_numbers(raw):
    if raw is None:
        return None
    inner = raw[1:-1] if raw.startswith(b"[") and raw.endswith(b"]") else raw
    try:
        return [float(tok) for tok in inner.split()]
    except ValueError:
        return None


def _refs_in(raw):
    if raw is None:
        return []
    return [int(m.group(1)) for m in re.finditer(rb"(\d+)\s+\d+\s+R", raw)]


def _names_to_refs(raw):
    """Parse a `<</Name1 N G R/Name2 N G R>>`-shaped dictionary into
    {name: object_number}. Works whether `raw` still carries its `<<`/`>>`
    wrapper or not -- only the inner `/name N G R` pattern is matched."""
    if not raw:
        return {}
    result = {}
    for m in re.finditer(rb"/([A-Za-z0-9._~!$&'*+,;=#-]+)\s+(\d+)\s+\d+\s+R", raw):
        result[m.group(1).decode("latin-1")] = int(m.group(2))
    return result


def _is_page(dict_bytes):
    return dict_bytes is not None and bool(re.search(rb"/Type\s*/Page(?!s)\b", dict_bytes))


def _page_content_bytes(page_dict, objects):
    """Return the concatenated, decompressed content stream(s) for one page,
    or None if /Contents is absent or unresolvable."""
    raw = _get_raw(page_dict, b"Contents")
    if raw is None:
        return None
    if raw.startswith(b"["):
        obj_nums = _refs_in(raw)
    else:
        m = re.fullmatch(rb"(\d+)\s+\d+\s+R", raw)
        obj_nums = [int(m.group(1))] if m else []
    parts = []
    for num in obj_nums:
        entry = objects.get(num)
        if entry is None or entry[1] is None:
            continue
        dict_bytes, stream_bytes = entry
        decoded = _maybe_inflate(dict_bytes, stream_bytes)
        parts.append(decoded if decoded is not None else stream_bytes)
    return b"\n".join(parts) if parts else None


# ============ public API ============

def page_count(path):
    """Number of pages in the PDF.

    Checks: counts top-level objects declaring `/Type /Page` (not
    `/Pages`); falls back to the `/Pages` root's own `/Count` entry if no
    bare `/Page` objects were found (e.g. they live inside a compressed
    object stream this parser cannot see).

    Cannot know the true count if both of the above are inside compressed
    object streams.

    Returns:
        int, or None if neither signal could be found at all.
    """
    with open(path, "rb") as f:
        data = f.read()
    objects = _iter_objects(data)
    pages = [n for n, (d, _s) in objects.items() if _is_page(d)]
    if pages:
        return len(pages)
    for _n, (d, _s) in objects.items():
        if d is not None and re.search(rb"/Type\s*/Pages\b", d):
            count = _as_int(_get_raw(d, b"Count"))
            if count is not None:
                return count
    return None


def page_boxes(path):
    """MediaBox/TrimBox/BleedBox for every page object found directly.

    Checks: `/MediaBox`, `/TrimBox`, `/BleedBox` arrays present directly on
    each `/Type /Page` object.

    Cannot know a box inherited from a parent `/Pages` node and not
    repeated on the page itself -- this does not walk the page tree (see
    module docstring). A page reported with `TrimBox: None` may still have
    a valid, inherited TrimBox that this function did not see.

    Returns:
        list of dicts, one per page object found, each
        `{"object_id": int, "MediaBox": [x0,y0,x1,y1] | None,
          "TrimBox": [...] | None, "BleedBox": [...] | None}`.
        Order matches object-number order, not necessarily reading order.
    """
    with open(path, "rb") as f:
        data = f.read()
    objects = _iter_objects(data)
    result = []
    for num in sorted(n for n, (d, _s) in objects.items() if _is_page(d)):
        d = objects[num][0]
        result.append({
            "object_id": num,
            "MediaBox": _as_numbers(_get_raw(d, b"MediaBox")),
            "TrimBox": _as_numbers(_get_raw(d, b"TrimBox")),
            "BleedBox": _as_numbers(_get_raw(d, b"BleedBox")),
        })
    return result


def embedded_fonts(path):
    """Every font actually referenced from a page's resources, and whether
    it carries an embedded font program.

    Checks: for each `/Type /Page` object, resolves `/Resources/Font` to a
    set of font objects; for each, resolves `/FontDescriptor` directly, or
    -- for a composite `/Type0` font -- via its `/DescendantFonts` child;
    "embedded" means that descriptor has `/FontFile`, `/FontFile2`, or
    `/FontFile3` (an indirect reference to the embedded font program). A
    `/BaseFont` with no resolvable `/FontDescriptor` at all is reported as
    not embedded -- per the task spec, this is the correct default, not an
    "unknown" state.

    Cannot know about a font resource dictionary hidden inside a
    compressed object stream (see module docstring) -- such a font simply
    will not appear in the returned list at all, it is not reported as
    "not embedded".

    Returns:
        list of (font_name: str, embedded: bool), one entry per distinct
        font object referenced from any page (deduplicated by object
        number, so a font shared across pages appears once).
    """
    with open(path, "rb") as f:
        data = f.read()
    objects = _iter_objects(data)

    font_obj_nums = set()
    for _num, (dict_bytes, _s) in objects.items():
        if not _is_page(dict_bytes):
            continue
        resources = _resolve(dict_bytes, b"Resources", objects)
        if resources is None:
            continue
        font_subdict = _resolve(resources, b"Font", objects)
        font_obj_nums.update(_names_to_refs(font_subdict).values())

    results = []
    for num in sorted(font_obj_nums):
        entry = objects.get(num)
        if entry is None:
            continue
        font_dict = entry[0]
        base_font = _as_name(_get_raw(font_dict, b"BaseFont")) or f"(unnamed, obj {num})"

        descriptor_num = _ref_num(font_dict, b"FontDescriptor")
        if descriptor_num is None:
            for d_num in _refs_in(_get_raw(font_dict, b"DescendantFonts")):
                d_entry = objects.get(d_num)
                if d_entry is None:
                    continue
                descriptor_num = _ref_num(d_entry[0], b"FontDescriptor")
                if descriptor_num is not None:
                    break

        embedded = False
        if descriptor_num is not None:
            d_entry = objects.get(descriptor_num)
            if d_entry is not None:
                descriptor_dict = d_entry[0]
                embedded = any(
                    _ref_num(descriptor_dict, key) is not None
                    for key in (b"FontFile", b"FontFile2", b"FontFile3")
                )
        results.append((base_font, embedded))
    return results


_IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
_CM_INNER_RE = re.compile(
    b"(" + _NUM + b")\\s+(" + _NUM + b")\\s+(" + _NUM + b")\\s+"
    b"(" + _NUM + b")\\s+(" + _NUM + b")\\s+(" + _NUM + b")\\s+cm"
)
_DO_INNER_RE = re.compile(rb"/([A-Za-z0-9._~!$&'*+,;=#-]+)\s+Do")
_TOKEN_RE = re.compile(
    rb"(?P<cm>" + _CM_INNER_RE.pattern + rb")"
    rb"|(?P<do>" + _DO_INNER_RE.pattern + rb")"
    rb"|(?P<q>(?<![A-Za-z0-9/])q(?![A-Za-z0-9]))"
    rb"|(?P<Q>(?<![A-Za-z0-9/])Q(?![A-Za-z0-9]))"
)


def _mat_mult(m1, m2):
    """m1 x m2 in PDF's row-vector convention (apply m1, then m2) -- used to
    concatenate a `cm` operand onto the current CTM: new = operand x old."""
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return (
        a1 * a2 + b1 * c2,
        a1 * b2 + b1 * d2,
        c1 * a2 + d1 * c2,
        c1 * b2 + d1 * d2,
        e1 * a2 + f1 * c2 + e2,
        e1 * b2 + f1 * d2 + f2,
    )


def _content_ctm_at_do(content):
    """Walk a decompressed content stream and yield (xobject_name, ctm) for
    every `Do` operator, maintaining the real `q`/`Q`/`cm` graphics-state
    matrix stack from an identity CTM at the top of the stream.

    This matters, verified empirically against a real Chromium-emitted
    PDF: a page-level `cm` (Chromium's device-pixel-to-point scale factor)
    sits outside any `q`, and every image's own placement `cm` is nested
    inside a `q ... Q` block -- the CTM at the point of `Do` is the product
    of *both*, not just the innermost `cm`. Reading only the innermost
    `cm` on that test fixture over-reported the placed size by ~4x (the
    inverse of the outer page scale), which would have silently corrupted
    every derived DPI figure.
    """
    stack = []
    current = _IDENTITY
    hits = []
    for m in _TOKEN_RE.finditer(content):
        kind = m.lastgroup
        if kind == "q":
            stack.append(current)
        elif kind == "Q":
            if stack:
                current = stack.pop()
        elif kind == "cm":
            inner = _CM_INNER_RE.match(m.group("cm"))
            nums = tuple(float(inner.group(i)) for i in range(1, 7))
            current = _mat_mult(nums, current)
        elif kind == "do":
            name = _DO_INNER_RE.match(m.group("do")).group(1).decode("latin-1")
            hits.append((name, current))
    return hits


def raster_dpi(path):
    """Effective DPI of every raster image XObject actually placed on a page.

    Checks: for each Image XObject's pixel `/Width`/`/Height`, resolves the
    full graphics-state transform matrix in effect at the point it is
    drawn (`Do`), composing every enclosing `cm`/`q`/`Q` from the top of
    the content stream -- not just the nearest preceding `cm` (see
    `_content_ctm_at_do` docstring for why that distinction is load-
    bearing). Placed width/height in points is the transformed unit
    square's edge lengths (`hypot(a,b)`, `hypot(c,d)`), which is exact for
    any axis-aligned or pure rotation+uniform-scale placement. Effective
    DPI = pixel width / (placed width in points / 72).

    Cannot know placement for: an image not drawn via `Do` from a page
    content stream (e.g. only referenced, or drawn from within a Form
    XObject's own nested content stream -- not recursed into); an image
    whose XObject dictionary or resources live inside a compressed object
    stream; genuine shear (non-zero rotation combined with independently
    non-uniform x/y scale can still be measured correctly by this
    formula, but a sheared parallelogram placement is not distinguished
    from a plain rotation -- reported as whatever `hypot` computes, which
    can overstate DPI in that specific case).

    Returns:
        list of (object_id: int, width_px: int|None, height_px: int|None,
        placed_width_pt: float|None, effective_dpi: float|None). DPI and
        placed width are None -- never guessed -- whenever no `Do` reference
        to that image could be resolved on any page, per the task's
        explicit "report width/height and DPI=None rather than guessing."
    """
    with open(path, "rb") as f:
        data = f.read()
    objects = _iter_objects(data)

    results = []
    seen = set()
    for _num, (dict_bytes, _s) in objects.items():
        if not _is_page(dict_bytes):
            continue
        resources = _resolve(dict_bytes, b"Resources", objects)
        if resources is None:
            continue
        xobject_subdict = _resolve(resources, b"XObject", objects)
        name_to_num = _names_to_refs(xobject_subdict)
        image_names = {
            name: onum for name, onum in name_to_num.items()
            if onum in objects and objects[onum][0] is not None
            and re.search(rb"/Subtype\s*/Image\b", objects[onum][0])
        }
        if not image_names:
            continue

        content = _page_content_bytes(dict_bytes, objects)
        placements = {}
        if content is not None:
            for name, ctm in _content_ctm_at_do(content):
                if name in image_names:
                    placements[image_names[name]] = ctm  # last placement wins

        for _name, onum in image_names.items():
            if onum in seen:
                continue
            seen.add(onum)
            img_dict = objects[onum][0]
            width_px = _as_int(_get_raw(img_dict, b"Width"))
            height_px = _as_int(_get_raw(img_dict, b"Height"))

            placed_width_pt = None
            dpi = None
            ctm = placements.get(onum)
            if ctm is not None and width_px:
                a, b, c, d, _e, _f = ctm
                w_pt = math.hypot(a, b)
                if w_pt > 0:
                    placed_width_pt = round(w_pt, 2)
                    dpi = round(width_px / (w_pt / 72.0), 1)

            results.append((onum, width_px, height_px, placed_width_pt, dpi))
    return results


if __name__ == "__main__":
    import sys as _sys

    for _path in _sys.argv[1:]:
        print(f"{_path}: pages={page_count(_path)}")
        for _box in page_boxes(_path):
            print("  ", _box)
        for _name, _emb in embedded_fonts(_path):
            print(f"   font {_name!r}: embedded={_emb}")
        for _row in raster_dpi(_path):
            print(f"   image obj {_row[0]}: {_row[1]}x{_row[2]}px "
                  f"placed={_row[3]}pt dpi={_row[4]}")
