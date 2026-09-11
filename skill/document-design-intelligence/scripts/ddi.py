#!/usr/bin/env python3
"""ddi.py -- the ONE entry point for the mandatory SKILL.md workflow.

Four steps, one command each, so the model calling this skill never has to
remember four separate scripts and their flags:

    ddi.py check                                            validate the data
    ddi.py resolve --query "<text>" [--brand <slug>] [--json]   resolve one request
    ddi.py preflight <file> [--json]                        verify a rendered file
    ddi.py handoff --json <resolved.json> --format docx|pptx|pdf|png   render-handoff block

Plus:
    ddi.py version    prints VERSION + SKILL.md's build stamp
    ddi.py            (no args) prints the four steps above, one line each --
                      this exact text is what SKILL.md quotes as the workflow.

Every subcommand except `handoff` (new here) is a thin passthrough to the
script that already implements it (resolve.py, preflight.py,
validate_data.py) -- this file adds no new resolution/validation logic of
its own, only routing, so there is exactly one implementation of each
check to keep correct. Exit codes propagate unchanged from whichever
script actually ran; see each subcommand's docstring below for its own
codes.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path


def _assert_stdlib_only(extra_allowed=()):
    """Fail loudly at import time if a non-stdlib import is ever added here.

    `extra_allowed` permits importing this project's own sibling stdlib-only
    modules without weakening the check for any genuine third-party package.
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


_assert_stdlib_only(extra_allowed={"validate_data", "resolve", "preflight"})

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import validate_data  # noqa: E402 - sibling script in this same directory
import resolve  # noqa: E402
import preflight  # noqa: E402

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPTS_DIR.parent
DEFAULT_DATA_DIR = SKILL_ROOT / "data"

#: The exact four-line workflow text SKILL.md quotes verbatim. Kept as one
#: literal here (not assembled from the subcommand docstrings) so that
#: what SKILL.md shows the model and what a human reads by running
#: `ddi.py` with no arguments can never drift apart from each other.
WORKFLOW_STEPS = (
    '1. ddi.py check                                          -- validate the data',
    '2. ddi.py resolve --query "<text>" [--brand <slug>] [--json]  -- resolve one request',
    "3. ddi.py preflight <file> [--json]                      -- verify a rendered file",
    "4. ddi.py handoff --json <resolved.json> --format docx|pptx|pdf|png  -- render-handoff block",
)


def cmd_check(argv):
    """`ddi.py check [--data-dir DIR]` -- validate_data.py's per-key
    degradation (research/brief-mechanism-perkey.md), not the strict
    build-time gate: a tier-1 structural problem (bad manifest,
    missing/malformed file, header mismatch, duplicate key) still refuses
    the whole dataset; a tier-2 row-level problem (bad enum/FK/reference/
    derived value on one row) is printed as a named warning -- table, key,
    and reason -- instead of failing the check, since `ddi.py resolve`
    will degrade around it per-key on its own.

    Exit codes: 0 clean or tier-2-only (warnings printed), 1 tier-1
    (structural) problem(s) found.
    """
    data_dir = DEFAULT_DATA_DIR
    if "--data-dir" in argv:
        idx = argv.index("--data-dir")
        data_dir = Path(argv[idx + 1])

    tier1_ok, tier1_lines, tier2_entries, summary = validate_data.validate_tiered(data_dir)
    if not tier1_ok:
        for line in tier1_lines:
            print(line)
        print(f"\n{len(tier1_lines)} structural problem(s) found -- refusing")
        return 1

    if tier2_entries:
        print(f"[DATA WARNING] {len(tier2_entries)} row-level problem(s) -- "
              "degraded to per-key refusal:")
        for entry in tier2_entries:
            key = entry["key"] or "(whole table)"
            print(f"  {entry['table']}/{key}: {entry['line']}")

    print(summary)
    return 0


def cmd_resolve(argv):
    """`ddi.py resolve ...` -- resolve.py passthrough, every flag forwarded
    as-is. Exit codes: propagated unchanged from resolve.main() (0
    resolved, 1 data invalid, 2 abstained, 3 brand refusal)."""
    return resolve.main(argv)


def cmd_preflight(argv):
    """`ddi.py preflight <file> [--json]` -- preflight.py passthrough.

    Exit code: always 0, propagated unchanged from preflight.main() (it
    reports facts, it never decides pass/fail)."""
    return preflight.main(argv)


# ---------------------------------------------------------------------------
# handoff -- new here, not a passthrough. Reads a resolve.py --json result
# and reshapes it into the render-handoff block a model hands to whichever
# built-in docx/pptx skill does the actual rendering, or uses itself for the
# native pdf and png paths -- speaking THAT TARGET'S vocabulary (docx-js's
# DXA/half-points/HeadingLevel, pptxgenjs's un-prefixed hex/charSpacing/
# LAYOUT_16x9, this project's own @page/font-face/engine-invocation shape
# for pdf, or its px/'#'hex/window-size CSS-screenshot shape for png),
# not our schema's mm/pt/#RRGGBB as stored. Every mismatch
# implemented below is one of the five research/24 section 3 "Resolver
# vocabulary mismatches" call-outs, each sourced to a research/23 line
# (Anthropic's own proprietary docx/pptx SKILL.md exports -- conventions
# read, nothing copied); the one that research/23 does not source at all
# (docx-js's half-point font-size unit) is marked UNSOURCED below rather
# than credited to a citation that isn't there. docx (npm) TextRun's
# characterSpacing was the other UNSOURCED mapping and has been removed
# from the docx handoff entirely (research/63-characterspacing-removal.md)
# rather than kept and marked -- unlike the font-size unit, it read a
# column no table carries, so it was permanently empty as well as unsourced.
#
# The real schema's table/column names now exist (data/schema-manifest.json)
# even though several tables (palettes, type-scales, doctypes among them)
# have no authored rows yet -- so every lookup below is still a plain dict
# .get() against HANDOFF_VOCAB's names, and a concept absent from the
# resolved JSON (wrong table never walked, right table with no matching
# column) prints "(not present in this resolution)" rather than crashing or
# fabricating a value. HANDOFF_VOCAB is the one place to edit once a name
# changes; nothing else in this file should need to.
# ---------------------------------------------------------------------------

#: 1 inch = 1440 DXA (research/23 docx:25) = 25.4 mm -> 1440/25.4 DXA per mm,
#: written to 4 dp per the task's own citation of this constant.
MM_TO_DXA = 56.6929
#: UNSOURCED in research/23's exported docx SKILL.md (no font-size example
#: appears in the excerpt) -- this is OOXML's own convention (the `sz`
#: attribute, and the `docx` npm package's `size` RunOptions field, are
#: both documented elsewhere as half-points), used here because docx-js
#: has no other way to take a point size.
PT_TO_HALF_POINTS = 2

#: research/23 pptx:454 -- pptxgenjs's default canvas before `pres.layout`
#: is set; not a print page format (research/24 section 3 item 2).
PPTX_DEFAULT_LAYOUT_NAME = "LAYOUT_16x9"
PPTX_DEFAULT_LAYOUT_IN = (10, 5.625)

#: CSS Values and Units (W3C): 1in = 96px = 72pt, so 1pt = 96/72 px. UNSOURCED
#: from research/23 (a headless-Chromium screenshot pipeline is not one of its
#: exported docx/pptx excerpts) -- this is the CSS specification's own fixed
#: ratio, used because png-social's canvas is px-native (a screenshot, not a
#: printed page), so handing it pt the way _build_pdf_lines does would be the
#: wrong unit for this target, not just an unconverted one.
PT_TO_PX = 96 / 72

#: png-social's Engine Invocation carries the screenshot's pixel dimensions as
#: a `--window-size=W,H` flag (its only source -- research/brief-packaging-
#: deck-and-png.md PART B says not to invent one). Parsed, not assumed: a
#: render row whose invocation lacks this flag, or has it malformed, must say
#: so rather than silently emitting nothing or a fabricated size.
WINDOW_SIZE_RE = re.compile(r"--window-size=(\d+),(\d+)")

#: render-targets."Print Tier Max" enum order (data/schema-manifest.json)
#: -- index used to test "tier > 1" (pdfx4-rgb or better) for @page bleed.
PRINT_TIER_ORDER = ["none", "submittable-rgb", "pdfx4-rgb", "cmyk-press"]

#: FINAL wording (research/05-SYNTHESIS.md:977-979, superseding the
#: research/14 draft's "conformance validated offline" -- research/28 found
#: no open tool can validate PDF/X at all, in-sandbox or not). Never swap
#: in the word "validated" anywhere near this.
PDFX4_TIER_WORDING = (
    "PDF/X-4 structurally emitted (WeasyPrint >=67); conformance not "
    "independently verifiable with open tooling."
)

NOT_PRESENT = "(not present in this resolution)"

HANDOFF_VOCAB = {
    "page_format_table": "page-formats",
    # source-mm-column -> DXA label shown alongside it (research/24 section 3
    # item 1 / research/23 docx:25).
    "page_format_mm_columns": {
        "Trim W mm": "Width DXA",
        "Trim H mm": "Height DXA",
        "Margin Top mm": "Margin Top DXA",
        "Margin Bottom mm": "Margin Bottom DXA",
        "Margin Inside mm": "Margin Inside DXA",
        "Margin Outside mm": "Margin Outside DXA",
    },
    "page_format_bleed_column": "Bleed mm",
    "typeface_table": "typefaces",
    "typeface_family_columns": ["Heading Family", "Body Family"],
    "typeface_fallback_column": "Safe Stack Fallback",
    "typeface_scale_group_column": "Scale Key",
    "type_scale_table": "type-scales",
    "type_scale_role_column": "Role",
    "type_scale_size_column": "Size pt",
    # Present on a type-scale (or, failing that, typeface) row once the real
    # schema grows one; absent from every table today, so this always
    # degrades to NOT_PRESENT under the correctly-named key below.
    "letter_spacing_pt_column": "Letter Spacing pt",
    "pptx_letter_spacing_key": "charSpacing",  # research/23 pptx:458
    "palette_table": "palettes",
    "palette_role_columns": ["Primary", "Secondary", "Accent", "Background", "Foreground"],
    "render_target_table": "render-targets",
    "render_target_format_column": "Format",
    "render_target_engine_column": "Engine",
    "render_target_engine_path_column": "Engine Path",
    "render_target_invocation_column": "Engine Invocation",
    "render_target_font_rule_column": "Font Rule",
    "render_target_tier_column": "Print Tier Max",
    "constraints_table": "constraints",
    "constraints_id_column": "Set Key",
    "constraints_element_scope_column": "Element Scope",
    "constraints_parameter_column": "Parameter",
    # research/54 part 3: `structures` and `headings` were absent from this
    # dict entirely, so declaring `display_columns` on them (part 1) put
    # heading wording into the resolved JSON but left the handoff printing
    # nothing from it -- the handoff only ever reads THIS dict's names.
    # `structures."Heading Language"` is the schema's OWN language selector
    # (data/base/structures.csv, one value per structure row, not invented
    # here); `headings."Is Primary"` picks the one wording per section once
    # that language is fixed. See `_section_headings` below.
    "structure_table": "structures",
    "structure_section_order_column": "Section Order",
    "structure_heading_language_column": "Heading Language",
    "headings_table": "headings",
    "headings_canonical_section_column": "canonical_section",
    "headings_text_column": "Heading Text",
    "headings_language_column": "Language",
    "headings_is_primary_column": "Is Primary",
}


def _first_row(resolved, table_name):
    rows = resolved.get(table_name)
    return rows[0] if rows else None


def _mm_to_dxa(mm_value):
    try:
        return round(float(mm_value) * MM_TO_DXA)
    except (TypeError, ValueError):
        return None


def _pt_to_half_points(pt_value):
    try:
        return round(float(pt_value) * PT_TO_HALF_POINTS, 1)
    except (TypeError, ValueError):
        return None


def _px_from_pt(pt_value):
    try:
        return round(float(pt_value) * PT_TO_PX, 1)
    except (TypeError, ValueError):
        return None


def _parse_window_size(invocation):
    """(width_px, height_px) parsed from a png render target's Engine
    Invocation, or None if the `--window-size=W,H` flag is absent or its
    value doesn't match -- callers must say so explicitly rather than
    guessing a canvas size."""
    if not invocation:
        return None
    m = WINDOW_SIZE_RE.search(invocation)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def _strip_hex(value):
    """pptxgenjs wants hex WITHOUT '#' -- research/23 pptx:455 ("#FF0000"
    and 8-digit alpha hex both "corrupt the file")."""
    return value[1:] if value.startswith("#") else value


def _letter_spacing_pt(typeface_row, scale_rows):
    """First non-empty 'Letter Spacing pt' value found on any resolved
    type-scale row, else the typeface row -- or None if the schema simply
    doesn't carry this yet (true everywhere today)."""
    column = HANDOFF_VOCAB["letter_spacing_pt_column"]
    for row in scale_rows:
        value = row.get(column, "")
        if value:
            return value
    if typeface_row:
        value = typeface_row.get(column, "")
        if value:
            return value
    return None


def _heading_roles(scale_rows):
    """Type-scale Role values shaped like h1/h2/h3 -- the roles a TOC needs
    a HeadingLevel for (research/23 docx:33), in ascending depth order."""
    role_column = HANDOFF_VOCAB["type_scale_role_column"]
    roles = {row.get(role_column, "") for row in scale_rows}
    heading_roles = [r for r in roles if re.fullmatch(r"h[0-9]+", r or "")]
    return sorted(heading_roles, key=lambda r: int(r[1:]))


def _section_headings(resolved):
    """(Heading Language, [(canonical_section, primary Heading Text or None), ...])
    for the resolved structure row, in Section Order -- the section list AND the
    wording a renderer needs (research/54 part 3), not just the structural TOC
    depth `_heading_roles` already gives. The language is read off the structure
    row itself (`Heading Language`), the schema's existing per-structure selector;
    nothing here invents a new one. A section with no primary heading in that
    language returns None for that section rather than silently dropping it."""
    v = HANDOFF_VOCAB
    structure_row = _first_row(resolved, v["structure_table"])
    if not structure_row:
        return None, []
    lang = structure_row.get(v["structure_heading_language_column"], "")
    order = structure_row.get(v["structure_section_order_column"], "")
    sections = [s for s in order.split(";") if s]
    primary_text = {}
    for row in resolved.get(v["headings_table"], []):
        if (row.get(v["headings_language_column"]) == lang
                and row.get(v["headings_is_primary_column"]) == "yes"):
            primary_text[row.get(v["headings_canonical_section_column"])] = \
                row.get(v["headings_text_column"], "")
    return lang, [(section, primary_text.get(section)) for section in sections]


def _sections_lines(resolved):
    lang, pairs = _section_headings(resolved)
    lines = [f"  sections (Section Order, wording in Heading Language={lang}):"
             if lang else "  sections:"]
    if not pairs:
        lines.append(f"    {NOT_PRESENT}")
        return lines
    for section, text in pairs:
        lines.append(f"    {section}: {text if text else NOT_PRESENT}")
    return lines


def _constraints_and_preflight_lines(resolved, target_format):
    lines = []
    constraint_rows = resolved.get(HANDOFF_VOCAB["constraints_table"], [])
    if constraint_rows:
        id_column = HANDOFF_VOCAB["constraints_id_column"]
        seen = []
        for row in constraint_rows:
            set_key = row.get(id_column, "")
            if set_key and set_key not in seen:
                seen.append(set_key)
        lines.append(f"  constraints to preflight (Set Keys): {', '.join(seen)}")
    else:
        lines.append("  constraints to preflight: (none found)")
    lines.append(f"next: python3 scripts/preflight.py <rendered-file>.{target_format}")
    return lines


def _parse_kv_parameter(param_string):
    """Split a constraints.csv `Parameter` cell (`key=value;key=value`) into
    a dict. Segments with no '=' are skipped rather than raising -- most
    constraint rows pack a single bare token here, not a key=value pair."""
    pairs = {}
    for segment in (param_string or "").split(";"):
        key, sep, value = segment.partition("=")
        if sep:
            pairs[key.strip()] = value.strip()
    return pairs


def _page_flow_constraints(resolved):
    """Resolved constraint rows whose Parameter names a docx_property --
    found by reading the schema (research/brief-mechanism.md: "READ THE
    PARAMETER, do not hardcode a second copy of this mapping"), not a
    hardcoded constraint_key list, so a newly authored page-flow constraint
    reaches the handoff block with no change here."""
    v = HANDOFF_VOCAB
    out = []
    for row in resolved.get(v["constraints_table"], []):
        params = _parse_kv_parameter(row.get(v["constraints_parameter_column"], ""))
        if params.get("docx_property"):
            out.append((row, params))
    return out


def _page_flow_docx_lines(resolved):
    lines = ["  page flow (OOXML paragraph/table properties, mapped from each "
              "constraint's own Parameter column -- convention, not sourced to any "
              "authority this library cites):"]
    v = HANDOFF_VOCAB
    flow = _page_flow_constraints(resolved)
    if not flow:
        lines.append(f"    {NOT_PRESENT}")
        return lines
    for row, params in flow:
        prop = params["docx_property"]
        block = params.get("applies_to_block") or row.get(v["constraints_element_scope_column"], "")
        detail = block or NOT_PRESENT
        binds_to = params.get("binds_to")
        if binds_to:
            detail = f"{detail} bound to {binds_to}"
        min_lines = params.get("min_lines_together")
        if min_lines:
            detail = f"{detail}, min_lines_together={min_lines}"
        lines.append(f"    {prop}: {detail}  [{row.get('key', '')}]")
    return lines


def _page_flow_pptx_lines(resolved):
    lines = ["  page flow: NOT APPLICABLE -- slides do not paginate, so docx's "
              "page-flow properties have no pptx equivalent:"]
    flow = _page_flow_constraints(resolved)
    if flow:
        properties = sorted({params["docx_property"] for _, params in flow})
        lines.append(f"    no pptx equivalent for: {', '.join(properties)}")
    else:
        lines.append(f"    {NOT_PRESENT}")
    return lines


def _build_docx_lines(resolved):
    v = HANDOFF_VOCAB
    lines = []

    page_row = _first_row(resolved, v["page_format_table"])
    lines.append("  page (docx-js DXA; 1 mm = 56.6929 DXA, 1 pt = 20 DXA -- research/23 docx:25):")
    if page_row:
        shown = False
        for mm_column, dxa_label in v["page_format_mm_columns"].items():
            mm_value = page_row.get(mm_column, "")
            if mm_value == "":
                continue
            dxa_value = _mm_to_dxa(mm_value)
            lines.append(f"    {mm_column}: {mm_value}mm  ->  {dxa_label}: {dxa_value}")
            shown = True
        if not shown:
            lines.append(f"    {NOT_PRESENT}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    typeface_row = _first_row(resolved, v["typeface_table"])
    lines.append("  fonts:")
    if typeface_row:
        shown = False
        for column in v["typeface_family_columns"]:
            value = typeface_row.get(column, "")
            if value:
                lines.append(f"    {column}: {value}")
                shown = True
        fallback = typeface_row.get(v["typeface_fallback_column"], "")
        if fallback:
            lines.append(f"    {v['typeface_fallback_column']}: {fallback}")
            shown = True
        # A resolved typefaces row that surfaces none of these columns is the same
        # state as no row at all, and must SAY so. Without this guard the section
        # printed its header and then nothing -- which is how v0.1.0 shipped an
        # empty `fonts:` that read as "no fonts needed" instead of "not resolved".
        # `page` and `palette` already had this guard; `fonts` did not.
        if not shown:
            lines.append(f"    {NOT_PRESENT}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    scale_rows = resolved.get(v["type_scale_table"], [])
    lines.append("  font sizes (docx-js half-points -- OOXML `sz` / docx `size`; UNSOURCED "
                 "from research/23, see module docstring):")
    if scale_rows:
        for row in scale_rows:
            role = row.get(v["type_scale_role_column"], "")
            size_pt = row.get(v["type_scale_size_column"], "")
            half_points = _pt_to_half_points(size_pt)
            lines.append(f"    {role}: {size_pt}pt  ->  {half_points} half-points")
    else:
        lines.append(f"    {NOT_PRESENT}")

    heading_roles = _heading_roles(scale_rows)
    lines.append("  TOC heading levels (docx-js HeadingLevel.* -- research/23 docx:33):")
    if heading_roles:
        for role in heading_roles:
            lines.append(f"    {role}  ->  HeadingLevel.HEADING_{role[1:]}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    lines.extend(_sections_lines(resolved))

    palette_row = _first_row(resolved, v["palette_table"])
    lines.append("  palette (hex as stored -- docx-js color-argument format not documented "
                 "in research/23, kept unmodified per research/24 section 3 item 3):")
    if palette_row:
        shown = False
        for role in v["palette_role_columns"]:
            value = palette_row.get(role, "")
            if value:
                lines.append(f"    {role}: {value}")
                shown = True
        if not shown:
            lines.append(f"    {NOT_PRESENT}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    lines.extend(_page_flow_docx_lines(resolved))

    return lines


def _build_pptx_lines(resolved):
    v = HANDOFF_VOCAB
    lines = []

    lines.append("  slide layout (pptxgenjs default -- research/23 pptx:454; NOT a print page "
                 "format, no page-formats row emitted -- research/24 section 3 item 2):")
    lines.append(f"    {PPTX_DEFAULT_LAYOUT_NAME}: {PPTX_DEFAULT_LAYOUT_IN[0]}in x {PPTX_DEFAULT_LAYOUT_IN[1]}in")

    typeface_row = _first_row(resolved, v["typeface_table"])
    lines.append("  fonts:")
    if typeface_row:
        shown = False
        for column in v["typeface_family_columns"]:
            value = typeface_row.get(column, "")
            if value:
                lines.append(f"    {column}: {value}")
                shown = True
        fallback = typeface_row.get(v["typeface_fallback_column"], "")
        if fallback:
            lines.append(f"    {v['typeface_fallback_column']}: {fallback}")
            shown = True
        # A resolved typefaces row that surfaces none of these columns is the same
        # state as no row at all, and must SAY so. Without this guard the section
        # printed its header and then nothing -- which is how v0.1.0 shipped an
        # empty `fonts:` that read as "no fonts needed" instead of "not resolved".
        # `page` and `palette` already had this guard; `fonts` did not.
        if not shown:
            lines.append(f"    {NOT_PRESENT}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    scale_rows = resolved.get(v["type_scale_table"], [])
    lines.append("  font sizes (pptxgenjs pt -- research/23 pptx:561-564,576, no conversion):")
    if scale_rows:
        for row in scale_rows:
            role = row.get(v["type_scale_role_column"], "")
            size_pt = row.get(v["type_scale_size_column"], "")
            lines.append(f"    {role}: {size_pt}pt")
    else:
        lines.append(f"    {NOT_PRESENT}")

    lines.extend(_sections_lines(resolved))

    spacing_pt = _letter_spacing_pt(typeface_row, scale_rows)
    lines.append(f"  {v['pptx_letter_spacing_key']} (pt -- research/23 pptx:458, "
                 f"letterSpacing is silently ignored):")
    lines.append(f"    {spacing_pt}pt" if spacing_pt is not None else f"    {NOT_PRESENT}")

    palette_row = _first_row(resolved, v["palette_table"])
    lines.append("  palette (hex without leading '#' -- research/23 pptx:455, '#' or an "
                 "8-digit alpha hex corrupts the file):")
    if palette_row:
        shown = False
        for role in v["palette_role_columns"]:
            value = palette_row.get(role, "")
            if value:
                lines.append(f"    {role}: {value}  ->  {_strip_hex(value)}")
                shown = True
        if not shown:
            lines.append(f"    {NOT_PRESENT}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    lines.extend(_page_flow_pptx_lines(resolved))

    return lines


def _build_pdf_lines(resolved):
    v = HANDOFF_VOCAB
    lines = []

    page_row = _first_row(resolved, v["page_format_table"])
    render_rows = [r for r in resolved.get(v["render_target_table"], [])
                   if r.get(v["render_target_format_column"]) == "pdf"]
    max_tier = max(
        (PRINT_TIER_ORDER.index(r.get(v["render_target_tier_column"], "none"))
         for r in render_rows if r.get(v["render_target_tier_column"], "none") in PRINT_TIER_ORDER),
        default=0,
    )

    lines.append("  @page (native HTML -> Chromium/WeasyPrint pipeline):")
    if page_row:
        w = page_row.get("Trim W mm", "")
        h = page_row.get("Trim H mm", "")
        lines.append(f"    size: {w}mm {h}mm")
        top = page_row.get("Margin Top mm", "")
        right = page_row.get("Margin Outside mm", "")
        bottom = page_row.get("Margin Bottom mm", "")
        left = page_row.get("Margin Inside mm", "")
        lines.append(f"    margin: {top}mm {right}mm {bottom}mm {left}mm  (top right bottom left)")
        if max_tier > 1:
            bleed = page_row.get(v["page_format_bleed_column"], "")
            lines.append(f"    bleed: {bleed}mm")
            lines.append("    marks: crop, registration")
    else:
        lines.append(f"    {NOT_PRESENT}")

    typeface_row = _first_row(resolved, v["typeface_table"])
    lines.append("  font-face stack (embed vs. safe-stack per render target's Font Rule):")
    if typeface_row and render_rows:
        for row in render_rows:
            engine = row.get(v["render_target_engine_column"], "")
            rule = row.get(v["render_target_font_rule_column"], "")
            if rule == "embed":
                families = " / ".join(
                    typeface_row.get(c, "") for c in v["typeface_family_columns"] if typeface_row.get(c, ""))
                lines.append(f"    {engine} ({rule}): {families}")
            else:
                fallback = typeface_row.get(v["typeface_fallback_column"], "")
                lines.append(f"    {engine} ({rule}): {fallback}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    # research/brief-packaging-display-columns.md PART 4: this builder read only
    # page_format_table, render_target_table and typeface_table -- never
    # type_scale_table or palette_table, both of which docx and pptx DO read.
    # invoice-tabular's only render target is pdf, so for that family there was
    # no other path that could ever deliver a size or a colour. CSS idiom below
    # (plain pt, '#'-prefixed hex, semantic <hN>), not docx's DXA/half-point
    # conversions -- this pipeline is native HTML -> Chromium/WeasyPrint, not OOXML.
    scale_rows = resolved.get(v["type_scale_table"], [])
    lines.append("  font sizes (CSS pt -- native unit for an HTML/Chromium/WeasyPrint "
                 "pipeline, no conversion needed):")
    if scale_rows:
        for row in scale_rows:
            role = row.get(v["type_scale_role_column"], "")
            size_pt = row.get(v["type_scale_size_column"], "")
            lines.append(f"    {role}: {size_pt}pt")
    else:
        lines.append(f"    {NOT_PRESENT}")

    heading_roles = _heading_roles(scale_rows)
    lines.append("  heading elements (semantic HTML, one <hN> per type-scale h<n> role):")
    if heading_roles:
        for role in heading_roles:
            lines.append(f"    {role}  ->  <h{role[1:]}>")
    else:
        lines.append(f"    {NOT_PRESENT}")

    palette_row = _first_row(resolved, v["palette_table"])
    lines.append("  palette (CSS hex colour, '#' kept -- unlike pptx, CSS requires the "
                 "leading '#'):")
    if palette_row:
        shown = False
        for role in v["palette_role_columns"]:
            value = palette_row.get(role, "")
            if value:
                lines.append(f"    {role}: {value}")
                shown = True
        if not shown:
            lines.append(f"    {NOT_PRESENT}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    lines.append("  render command:")
    if render_rows:
        for row in render_rows:
            engine = row.get(v["render_target_engine_column"], "")
            path = row.get(v["render_target_engine_path_column"], "")
            invocation = row.get(v["render_target_invocation_column"], "")
            command = f"{path} {invocation}".strip()
            lines.append(f"    {engine}: {command}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    if any(r.get(v["render_target_tier_column"]) == "pdfx4-rgb" for r in render_rows):
        lines.append(f"  tier: {PDFX4_TIER_WORDING}")

    return lines


def _build_png_lines(resolved):
    # research/brief-packaging-deck-and-png.md PART B: `infographic`'s only
    # render target is png-social (Format=png), and `_FORMAT_BUILDERS` had no
    # entry for it at all -- not missing wording, no handoff path whatsoever.
    # CSS/pixel idiom (px, '#'-prefixed hex) because the render pipeline is a
    # headless-Chromium SCREENSHOT of a fixed-size window, not a paginated
    # document: no docx DXA/half-points, no pdf mm `@page`. png-social's
    # `Supports Paged Media` is n/a and `Print Tier Max` is none, so bleed,
    # crop marks and paged-media constructs never apply to this format and
    # are called out as NOT APPLICABLE below rather than silently absent.
    v = HANDOFF_VOCAB
    lines = []

    render_rows = [r for r in resolved.get(v["render_target_table"], [])
                   if r.get(v["render_target_format_column"]) == "png"]

    lines.append("  canvas (CSS px -- parsed from the render target's own Engine "
                 "Invocation --window-size flag; a screenshot has no @page):")
    if render_rows:
        for row in render_rows:
            engine = row.get(v["render_target_engine_column"], "")
            invocation = row.get(v["render_target_invocation_column"], "")
            size = _parse_window_size(invocation)
            if size:
                lines.append(f"    {engine}: {size[0]}px x {size[1]}px")
            else:
                lines.append(f"    {engine}: --window-size not found or unparsable in "
                             f"Engine Invocation ({invocation or NOT_PRESENT})")
    else:
        lines.append(f"    {NOT_PRESENT}")

    typeface_row = _first_row(resolved, v["typeface_table"])
    lines.append("  font-face (CSS idiom, embed vs. safe-stack per render target's Font Rule):")
    if typeface_row and render_rows:
        for row in render_rows:
            engine = row.get(v["render_target_engine_column"], "")
            rule = row.get(v["render_target_font_rule_column"], "")
            if rule == "embed":
                families = " / ".join(
                    typeface_row.get(c, "") for c in v["typeface_family_columns"] if typeface_row.get(c, ""))
                lines.append(f"    {engine} ({rule}): {families or NOT_PRESENT}")
            else:
                fallback = typeface_row.get(v["typeface_fallback_column"], "")
                lines.append(f"    {engine} ({rule}): {fallback or NOT_PRESENT}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    scale_rows = resolved.get(v["type_scale_table"], [])
    lines.append("  font sizes (CSS px -- 1pt = 96/72px; the canvas above is already "
                 "px-native, so px is the right unit here, not pt):")
    if scale_rows:
        for row in scale_rows:
            role = row.get(v["type_scale_role_column"], "")
            size_pt = row.get(v["type_scale_size_column"], "")
            size_px = _px_from_pt(size_pt)
            lines.append(f"    {role}: {size_pt}pt  ->  {size_px}px")
    else:
        lines.append(f"    {NOT_PRESENT}")

    lines.extend(_sections_lines(resolved))

    palette_row = _first_row(resolved, v["palette_table"])
    lines.append("  palette (CSS hex colour, '#' kept):")
    if palette_row:
        shown = False
        for role in v["palette_role_columns"]:
            value = palette_row.get(role, "")
            if value:
                lines.append(f"    {role}: {value}")
                shown = True
        if not shown:
            lines.append(f"    {NOT_PRESENT}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    lines.append("  paged media (bleed / crop marks / @page): NOT APPLICABLE -- "
                 "png-social's Supports Paged Media is n/a and Print Tier Max is none; "
                 "a screenshot has no pages")

    lines.append("  render command:")
    if render_rows:
        for row in render_rows:
            engine = row.get(v["render_target_engine_column"], "")
            path = row.get(v["render_target_engine_path_column"], "")
            invocation = row.get(v["render_target_invocation_column"], "")
            command = f"{path} {invocation}".strip()
            lines.append(f"    {engine}: {command}")
    else:
        lines.append(f"    {NOT_PRESENT}")

    return lines


_FORMAT_BUILDERS = {
    "docx": _build_docx_lines,
    "pptx": _build_pptx_lines,
    "pdf": _build_pdf_lines,
    "png": _build_png_lines,
}


def _build_handoff_lines(resolved_payload, target_format):
    resolved = resolved_payload.get("resolved", {})
    lines = [f"HANDOFF (format={target_format})"]
    lines.extend(_FORMAT_BUILDERS[target_format](resolved))
    lines.extend(_constraints_and_preflight_lines(resolved, target_format))
    return lines


def cmd_handoff(argv):
    """`ddi.py handoff --json <resolved.json> --format docx|pptx|pdf|png`

    Reads a file previously produced by `ddi.py resolve --json > resolved.json`
    and prints the render-handoff block: target format, page format +
    margins, typeface (embed family + safe-stack fallback), palette roles
    as hex, and the constraint ids to preflight -- followed by the exact
    preflight command to run once the model has rendered the file.

    Exit codes: 0 printed successfully. 1 the input file is missing,
    unreadable, not valid JSON, or was not a "resolved" result (e.g. an
    abstained response saved by mistake) -- refuses to fabricate a handoff
    block from that. 2 bad usage (argparse: missing/invalid --format).
    """
    import argparse

    parser = argparse.ArgumentParser(prog="ddi.py handoff")
    parser.add_argument("--json", dest="json_path", required=True,
                         help="path to a resolve.py --json result")
    parser.add_argument("--format", required=True, choices=("docx", "pptx", "pdf", "png"))
    args = parser.parse_args(argv)

    try:
        payload = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"cannot read {args.json_path}: {exc}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"{args.json_path} is not valid JSON: {exc}")
        return 1

    if payload.get("status") != "resolved":
        print(f"{args.json_path} is not a resolved result (status={payload.get('status')!r}) "
              "-- refusing to build a handoff block from it")
        return 1

    for line in _build_handoff_lines(payload, args.format):
        print(line)
    return 0


def cmd_version(argv):
    """`ddi.py version` -- prints VERSION plus SKILL.md's build stamp, with
    no git dependency (both are plain files release.yml already writes;
    see that workflow's "Stamp version" step). Exit code: always 0."""
    version_path = SKILL_ROOT / "VERSION"
    skill_md_path = SKILL_ROOT / "SKILL.md"

    version = version_path.read_text(encoding="utf-8").strip() if version_path.exists() else "(no VERSION file)"
    print(f"VERSION: {version}")

    if skill_md_path.exists():
        first_line = skill_md_path.read_text(encoding="utf-8").splitlines()[0]
        if first_line.startswith("<!-- version:"):
            print(f"SKILL.md stamp: {first_line}")
        else:
            print("SKILL.md stamp: not yet stamped (no leading '<!-- version: ... -->' comment)")
    else:
        print("SKILL.md stamp: SKILL.md not found")
    return 0


COMMANDS = {
    "check": cmd_check,
    "resolve": cmd_resolve,
    "preflight": cmd_preflight,
    "handoff": cmd_handoff,
    "version": cmd_version,
}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv:
        for line in WORKFLOW_STEPS:
            print(line)
        return 0

    command, rest = argv[0], argv[1:]
    handler = COMMANDS.get(command)
    if handler is None:
        print(f"unknown command '{command}' -- expected one of: {', '.join(COMMANDS)}")
        return 2

    return handler(rest)


if __name__ == "__main__":
    raise SystemExit(main())
