#!/usr/bin/env python3
"""Font-file primitives: OpenType fsType (embedding permission) and a tnum
(tabular-figures) feature-tag presence check.

Both functions parse raw sfnt (TTF/OTF) binary structures directly with
`struct`. No font-shaping library is used or needed for either check: fsType
is a fixed-offset field, and a GSUB feature tag is a fixed-offset,
fixed-record-size array once the GSUB table's own offset is known.

Ported from the verified implementation and findings in
research/12-typescale-and-fstype.md (Q2), which tested these against six
fonts in C:\\Windows\\Fonts including both TrueType (`\\x00\\x01\\x00\\x00`)
and CFF-flavored OpenType (`OTTO`) sfnt files.
"""

import ast
import struct
import sys
from pathlib import Path


def _assert_stdlib_only():
    """Fail loudly at import time if a non-stdlib import is ever added here.

    Parses this file's own source and checks every top-level import against
    `sys.stdlib_module_names` (Python 3.10+). This is the "no third-party
    imports anywhere" guard the task asked for, enforced mechanically rather
    than by convention.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    stdlib = sys.stdlib_module_names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level or node.module is None:
                continue  # relative import (e.g. sibling lib module) -- allowed
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


_SFNT_TAGS = (b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1")

# OpenType OS/2.fsType, low nibble: usage permissions (bits 0-3, spec-defined
# as small integer values, not independently combinable in the original spec
# revision this checks against).
_FSTYPE_USAGE_LABELS = {
    0x0000: "installable",
    0x0002: "restricted",
    0x0004: "preview-print",
    0x0008: "editable",
}


def _find_table_offset(data, tag):
    """Return the byte offset of `tag` in the sfnt table directory, or None."""
    if len(data) < 12:
        return None
    sfnt_tag = data[0:4]
    if sfnt_tag not in _SFNT_TAGS:
        return None
    num_tables = struct.unpack(">H", data[4:6])[0]
    for i in range(num_tables):
        rec = 12 + i * 16
        if rec + 16 > len(data):
            break
        rec_tag, _cksum, offset, _length = struct.unpack(">4sIII", data[rec:rec + 16])
        if rec_tag == tag:
            return offset
    return None


def read_fstype(path):
    """Read the OS/2.fsType embedding-permission field from a TTF/OTF file.

    Checks: the fixed-offset sfnt table directory for an `OS/2` table entry,
    then the fsType uint16 at OS/2 offset +8 (OpenType spec, OS/2 table
    version 0+). Decodes the low nibble (usage permission: installable /
    restricted / preview-print / editable) and two independent high bits
    (0x0100 = no subsetting, 0x0200 = bitmap embedding only).

    Cannot know: whether the file is a valid font beyond having a
    recognizable sfnt tag and an OS/2 table -- this does not validate
    checksums, table lengths, or any other table's structure. Cannot know
    the *effective* legal permission for a given use case; fsType only
    states what the font vendor declared.

    Returns:
        (fs_type: int, label: str) on success.
        (None, reason: str) if the file is not a recognizable TTF/OTF sfnt
        file, or has no OS/2 table -- this is the failure return; it is not
        raised as an exception because "not a font" and "font with no
        embedding-permission field" are both facts a caller may want to
        record, not treat as a crash.
    """
    with open(path, "rb") as f:
        head = f.read(64 * 1024)  # table directory is always near the start

    if head[0:4] not in _SFNT_TAGS:
        return None, f"not a TTF/OTF (sfnt tag {head[0:4]!r})"

    os2_offset = _find_table_offset(head, b"OS/2")
    if os2_offset is None:
        return None, "no OS/2 table present"

    with open(path, "rb") as f:
        f.seek(os2_offset + 8)  # fsType is the 3rd field in OS/2, offset 8
        raw = f.read(2)
    if len(raw) != 2:
        return None, "OS/2 table truncated before fsType field"
    fs_type = struct.unpack(">H", raw)[0]

    usage = fs_type & 0x000F
    label = _FSTYPE_USAGE_LABELS.get(usage, f"reserved usage bits ({usage})")
    if fs_type & 0x0100:
        label += "+no-subsetting"
    if fs_type & 0x0200:
        label += "+bitmap-only"
    return fs_type, label


def has_tnum(path):
    """Check whether the font's GSUB table declares a `tnum` feature tag.

    Checks: the fixed-offset sfnt table directory for a `GSUB` table, then
    GSUB's FeatureList offset (fixed-offset field within GSUB), then scans
    that FeatureList's fixed-size (6 bytes: 4-byte tag + 2-byte offset)
    feature records for the tag `tnum`.

    Cannot know whether the font's *default* digit glyphs are tabular-width.
    A `tnum` GSUB tag means "this font can switch to tabular figures via an
    OpenType feature" -- it says nothing about whether digits are already
    tabular by default. A monospaced font (e.g. Consolas) has no `tnum` tag
    at all because every glyph, digits included, is already fixed-width --
    confirmed empirically in research/12-typescale-and-fstype.md Q2: Arial,
    Calibri, Times New Roman and Miriam Libre all report the tag present;
    Consolas does not, despite having genuinely tabular digits. Absence is
    therefore ambiguous between "no tabular figures" and "always tabular,
    no feature needed" -- resolving that ambiguity would require comparing
    digit glyph advance widths directly (`hmtx`), which is materially
    harder (variable-length glyph data, not fixed-offset records) and is
    not implemented here.

    Returns:
        "yes" if the `tnum` tag is present (a strengthener only -- never
        weakened back to "unknown" once found).
        "unknown" in every other case: no GSUB table, malformed/truncated
        GSUB data, not a recognizable TTF/OTF, or the tag is simply absent.
        Deliberately never returns "no" -- see docstring above and
        research/12's Consolas finding.
    """
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return "unknown"

    if len(data) < 12 or data[0:4] not in _SFNT_TAGS:
        return "unknown"

    try:
        gsub_offset = _find_table_offset(data, b"GSUB")
        if gsub_offset is None:
            return "unknown"
        fl_off = struct.unpack(">H", data[gsub_offset + 6:gsub_offset + 8])[0]
        fl = gsub_offset + fl_off
        count = struct.unpack(">H", data[fl:fl + 2])[0]
        tags = {
            data[fl + 2 + i * 6: fl + 6 + i * 6]
            for i in range(count)
        }
    except (struct.error, IndexError):
        return "unknown"

    return "yes" if b"tnum" in tags else "unknown"


if __name__ == "__main__":
    import sys as _sys

    for _path in _sys.argv[1:]:
        _fs, _label = read_fstype(_path)
        print(f"{_path}: fsType={_fs} -> {_label}; tnum={has_tnum(_path)}")
