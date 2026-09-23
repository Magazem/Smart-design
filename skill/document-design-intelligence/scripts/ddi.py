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

# Windows: a piped/redirected stdout (as opposed to a real console) falls
# back to the process's ANSI codepage, not UTF-8 -- non-ASCII heading text
# (accented French/German section names) would otherwise mojibake or raise
# UnicodeEncodeError for callers who capture this script's output. Force
# UTF-8 unconditionally so behavior doesn't depend on the caller's console
# codepage or PYTHONIOENCODING. `reconfigure` is Python 3.7+; guard it for
# anything older that might still run this stdlib-only script.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


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
    resolved, 1 data invalid, 2 abstained, 3 brand refusal, 4 --design refusal)."""
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

#: A8 (schema-manifest-NOTES.md section 9): `doc-styles.Table Rules` values
#: whose plain enum token a renderer could misread need the rule spelled
#: out. research/72's blind panel read `cv-dach-tabular`'s `hairline` table
#: as fully boxed despite the Checklist saying otherwise -- the bare token
#: carried no rule against cell borders. `row-hairlines` is the value this
#: was renamed to; only it needs the explicit line, since `hairline` and
#: `header-and-total` are not being misread and adding text for values that
#: are not confused would just be noise.
TABLE_RULES_INSTRUCTIONS = {
    "row-hairlines": ("table rules: horizontal hairlines between rows only; "
                       "no vertical rules; no cell borders"),
}

#: A8 (Manager ruling): research/72's judges 2 and 3 also flagged a
#: "heading collision" -- a section heading crowding cv-dach-tabular's table
#: with no space after it -- a defect the table-rules fix above does not
#: touch. cv-dach-tabular's Checklist carries the rule as prose (research/70
#: Direction 2 Spacing: body 10pt/13pt, "row padding = 1 leading unit"), but
#: a bare Checklist dump buries a structural rule among other bullets, so it
#: gets the same explicit-line treatment as TABLE_RULES_INSTRUCTIONS. Keyed
#: by style_key, not by an enum column, because this is a rule specific to
#: this one style's table/heading layout, not a value other styles share.
STYLE_SPACING_INSTRUCTIONS = {
    "cv-dach-tabular": ("space after every table and before every section "
                         "heading: one body leading (13pt); headings never "
                         "touch a table edge"),
}

#: FINAL wording (research/05-SYNTHESIS.md:977-979, superseding the
#: research/14 draft's "conformance validated offline" -- research/28 found
#: no open tool can validate PDF/X at all, in-sandbox or not). Never swap
#: in the word "validated" anywhere near this.
PDFX4_TIER_WORDING = (
    "PDF/X-4 structurally emitted (WeasyPrint >=67); conformance not "
    "independently verifiable with open tooling."
)

NOT_PRESENT = "(not present in this resolution)"

#: Library tables `ddi.py library` can browse (research/80-v05-plan.md
#: section 6 P1.6) -- the grand library minus designs (that's `ddi.py
#: designs`'s own job) and everything reached only via a doctype's FK walk.
LIBRARY_TABLES = ("palettes", "typefaces", "type-scales", "doc-styles")

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
    "typeface_body_fallback_column": "Safe Stack Body Fallback",
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
    # research/66: `doc-styles` had zero HANDOFF_VOCAB entries in any builder --
    # its design columns never reached a renderer even after (a) put them in the
    # resolved JSON. `Best For`/`Not For`/`Brand Scope`/`Display Name`/`Keywords`
    # are deliberately not read here; they are identity/guidance text, not a
    # renderable value (see HANDOFF_EXCLUSIONS below).
    "doc_style_table": "doc-styles",
    "doc_style_rule_hair_column": "Rule Hair pt",
    "doc_style_rule_strong_column": "Rule Strong pt",
    "doc_style_rule_brand_column": "Rule Brand pt",
    "doc_style_corner_radius_column": "Corner Radius mm",
    "doc_style_table_rules_column": "Table Rules",
    "doc_style_table_fills_column": "Table Fills",
    "doc_style_emphasis_column": "Emphasis Mechanism",
    "doc_style_field_style_column": "Field Style",
    "doc_style_checklist_column": "Checklist",
    # research/66 census's own flagship example of a stage-1 DEFECT: the only
    # column distinguishing `uk-early` from `uk-experienced` never reached a
    # renderer even after the stage-1 fix put it in the resolved JSON.
    "cv_region_table": "cv-regions",
    "cv_region_seniority_band_column": "Seniority Band",
    "cv_region_section_order_column": "Section Order",
}

#: HANDOFF_EXCLUSIONS -- table -> {path: {column: reason}}. research/66 stage 2 found
#: every resolved column of a reachable table that a path's builder does not read; this
#: makes that drop explicit and test-enforced (scripts/tests/test_column_parity.py) rather
#: than silent. Exactly two reason kinds, per Manager D8:
#: - "not applicable: <why>" -- the format/data cannot use this column (identity/search
#:   metadata never meant for a renderer, an FK routing pointer whose real content reaches
#:   the handoff through the table it points to, a construct the format has no equivalent
#:   for, or a code branch the CURRENT data/base/render-targets.csv rows can never take).
#: - "not yet wired: backlog <item>" -- a genuine DEFECT-classified design value
#:   (research/66 S2/S3/S4) that is not yet read by this path; wiring it in is future work,
#:   out of W3's scope (task instructions: this phase only makes drops explicit).
_IDENTITY = "not applicable: identity/search metadata, not a render value"
_ROUTING = ("not applicable: identity/FK-routing metadata; this table's real content "
            "reaches the handoff through the table(s) it points to")

HANDOFF_EXCLUSIONS = {
    "constraints": {
        "docx": {"Applies To": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                 "Check": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                 "Severity": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                 "Threshold": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)"},
        "pptx": {"Applies To": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                 "Check": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                 "Element Scope": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                 "Severity": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                 "Threshold": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)"},
        "pdf": {"Applies To": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Check": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Element Scope": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Parameter": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Severity": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Threshold": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)"},
        "png": {"Applies To": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Check": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Element Scope": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Parameter": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Severity": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)",
                "Threshold": "not yet wired: backlog data-dependent constraints columns (research/66 S3-4)"},
    },
    "cv-regions": {fmt: {
        "region_key": _ROUTING,
        "Max Pages": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
        "Photo": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
        "Date of Birth": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
        "Nationality": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
        "Marital Status": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
        "Visa Status": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
        "Education Before Experience": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
        "Format": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
        # research/64 D-E (A7): distinct from `doctypes."Default Language"` (the
        # RENDERED document's language, now wired via resolve.py's `language` block)
        # -- this column is free-text regional advisory prose about the CV
        # CONTENT's expected language ("English standard for multinational/
        # private-sector roles; Arabic for government/local-market roles"), not a
        # discrete renderable value. Same class as figures' four sentence-separator
        # columns and build-manifest.py's own comment on this column (schema
        # Revision 4 erratum). Not a backlog item -- no future wiring is expected.
        "Language Expectation": "not applicable: free-text regional advisory prose about the "
                                "CV CONTENT's expected language, not a discrete renderable "
                                "value -- distinct from doctypes.'Default Language' (the "
                                "rendered document's own language, wired via resolve.py's "
                                "language block)",
        "Evidence Class": "not yet wired: backlog cv-regions design columns (research/66 S2 DEFECT)",
    } for fmt in ("docx", "pptx", "pdf", "png")},
    "doc-reasoning": {fmt: {
        "Palette Key": _ROUTING,
        "Style Key": _ROUTING,
        "Typeface Key": _ROUTING,
        "Design Key": _ROUTING,
        "Anti-Pattern Tokens": "not yet wired: backlog doc-reasoning columns (research/66 S2 DEFECT)",
        "Doc Conditions": "not yet wired: backlog doc-reasoning columns (research/66 S2 DEFECT)",
        "Palette Bias Terms": "not yet wired: backlog doc-reasoning columns (research/66 S2 DEFECT)",
        "Severity": "not yet wired: backlog doc-reasoning columns (research/66 S2 DEFECT)",
        "Style Bias Terms": "not yet wired: backlog doc-reasoning columns (research/66 S2 DEFECT)",
        "Typeface Bias Terms": "not yet wired: backlog doc-reasoning columns (research/66 S2 DEFECT)",
    } for fmt in ("docx", "pptx", "pdf", "png")},
    "doc-styles": {fmt: {
        "Best For": _IDENTITY,
        "Not For": _IDENTITY,
        "Brand Scope": _IDENTITY,
        "Display Name": _IDENTITY,
        "Keywords": _IDENTITY,
    } for fmt in ("docx", "pptx", "pdf", "png")},
    "doctypes": {fmt: {
        "Artifact Class": _ROUTING,
        "Brand Scope": _IDENTITY,
        "Constraint Set Keys": _ROUTING,
        # research/64 D-E (A7): consumed by resolve.py's Stage 1 to build the
        # top-level `language` block (value + source), before `_fk_walk` ever
        # runs -- every handoff builder reads that block's argument, not this
        # cell of the resolved "doctypes" row.
        "Default Language": "not applicable: consumed by resolve.py to build the "
                             "top-level `language` block (value+source); no handoff "
                             "builder reads it as a doctypes table cell",
        "Display Name": _IDENTITY,
        # research/80-v05-plan.md §2A: catalogue grouping, not a render value -- it
        # exists so `ddi.py designs`/the loader can group doctypes by family; no
        # handoff builder has any reason to read it off a resolved doctypes row.
        "Family": "catalogue grouping, not a render value",
        "Keywords": _IDENTITY,
        "Page Format Key": _ROUTING,
        "Reasoning Key": _ROUTING,
        "Region Key": _ROUTING,
        "Render Target Keys": _ROUTING,
        "Structure Key": _ROUTING,
    } for fmt in ("docx", "pptx", "pdf", "png")},
    "page-formats": {
        "docx": {
            "Display Name": _IDENTITY, "Keywords": _IDENTITY,
            "Bleed mm": "not applicable: OOXML has no bleed/crop-mark construct "
                        "(render-targets.Supports Bleed declares bleed is per-render-target)",
            "Columns": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Fold Type": "not yet wired: backlog Fold Type / Panels mm -> research/64 D-C",
            "Folio Style": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Measure mm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Min DPI Line Art": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Min DPI Raster": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Panels mm": "not yet wired: backlog Fold Type / Panels mm -> research/64 D-C",
            "Print Mode": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Running Head": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Safe Margin mm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Stock gsm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
        },
        "pptx": {
            "Display Name": _IDENTITY, "Keywords": _IDENTITY,
            "Bleed mm": "not applicable: pptx has no print page geometry (fixed slide layout, "
                        "no page-formats row emitted -- research/24 section 3 item 2)",
            "Margin Bottom mm": "not applicable: pptx has no print page geometry (fixed slide "
                                "layout, no page-formats row emitted -- research/24 section 3 item 2)",
            "Margin Inside mm": "not applicable: pptx has no print page geometry (fixed slide "
                                "layout, no page-formats row emitted -- research/24 section 3 item 2)",
            "Margin Outside mm": "not applicable: pptx has no print page geometry (fixed slide "
                                 "layout, no page-formats row emitted -- research/24 section 3 item 2)",
            "Margin Top mm": "not applicable: pptx has no print page geometry (fixed slide "
                             "layout, no page-formats row emitted -- research/24 section 3 item 2)",
            "Columns": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Fold Type": "not yet wired: backlog Fold Type / Panels mm -> research/64 D-C",
            "Folio Style": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Measure mm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Min DPI Line Art": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Min DPI Raster": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Panels mm": "not yet wired: backlog Fold Type / Panels mm -> research/64 D-C",
            "Print Mode": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Running Head": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Safe Margin mm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Stock gsm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
        },
        "pdf": {
            "Display Name": _IDENTITY, "Keywords": _IDENTITY,
            "Columns": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Fold Type": "not yet wired: backlog Fold Type / Panels mm -> research/64 D-C",
            "Folio Style": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Measure mm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Min DPI Line Art": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Min DPI Raster": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Panels mm": "not yet wired: backlog Fold Type / Panels mm -> research/64 D-C",
            "Print Mode": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Running Head": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Safe Margin mm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Stock gsm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
        },
        "png": {
            "Display Name": _IDENTITY, "Keywords": _IDENTITY,
            "Bleed mm": "not applicable: png-social is a screenshot canvas, not a print page "
                       "(no page-formats row emitted)",
            "Margin Bottom mm": "not applicable: png-social is a screenshot canvas, not a print "
                               "page (no page-formats row emitted)",
            "Margin Inside mm": "not applicable: png-social is a screenshot canvas, not a print "
                               "page (no page-formats row emitted)",
            "Margin Outside mm": "not applicable: png-social is a screenshot canvas, not a print "
                                "page (no page-formats row emitted)",
            "Margin Top mm": "not applicable: png-social is a screenshot canvas, not a print "
                            "page (no page-formats row emitted)",
            "Trim H mm": "not applicable: png-social is a screenshot canvas, not a print page "
                        "(no page-formats row emitted)",
            "Trim W mm": "not applicable: png-social is a screenshot canvas, not a print page "
                        "(no page-formats row emitted)",
            "Columns": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Fold Type": "not yet wired: backlog Fold Type / Panels mm -> research/64 D-C",
            "Folio Style": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Measure mm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Min DPI Line Art": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Min DPI Raster": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Panels mm": "not yet wired: backlog Fold Type / Panels mm -> research/64 D-C",
            "Print Mode": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Running Head": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Safe Margin mm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
            "Stock gsm": "not yet wired: backlog page-formats print-production columns (research/66 S2 DEFECT)",
        },
    },
    "palettes": {fmt: {
        "Display Name": _IDENTITY, "Keywords": _IDENTITY, "Brand Scope": _IDENTITY,
        "Category Marker Roles": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "Fill-Only Roles": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "Text-Safe Roles": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "Muted": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "On Accent": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "On Muted": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "On Primary": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "On Secondary": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "Rule Brand": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "Rule Hair": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
        "Rule Strong": "not yet wired: backlog palettes columns (research/66 S2 DEFECT)",
    } for fmt in ("docx", "pptx", "pdf", "png")},
    "render-targets": {
        "docx": {
            "Availability": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Editable By Recipient": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Engine Invocation": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Engine Min Version": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Engine Path": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Fallback Render Key": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Print Tier Max": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports Bleed": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports CMYK": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports Paged Media": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
        },
        "pptx": {
            "Availability": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Editable By Recipient": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Engine Invocation": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Engine Min Version": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Engine Path": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Fallback Render Key": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Print Tier Max": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports Bleed": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports CMYK": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports Paged Media": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
        },
        "pdf": {
            "Availability": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Editable By Recipient": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Engine Min Version": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Fallback Render Key": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports Bleed": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports CMYK": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports Paged Media": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
        },
        "png": {
            "Availability": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Editable By Recipient": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Engine Min Version": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Fallback Render Key": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Print Tier Max": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports Bleed": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports CMYK": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
            "Supports Paged Media": "not yet wired: backlog render-targets columns not surfaced outside the render-command section (research/66 S3)",
        },
    },
    "structures": {fmt: {
        "Display Name": _IDENTITY,
        "Caption Position": "not yet wired: backlog structures follow-up columns (research/66 S4)",
        "Cross-Ref Style": "not yet wired: backlog structures follow-up columns (research/66 S4)",
        "Front Matter Numbering": "not yet wired: backlog structures follow-up columns (research/66 S4)",
        "Heading Depth Max": "not yet wired: backlog structures follow-up columns (research/66 S4)",
        "TOC Depth": "not yet wired: backlog structures follow-up columns (research/66 S4)",
    } for fmt in ("docx", "pptx", "pdf", "png")},
    "type-scales": {fmt: {
        "scale_key": _ROUTING,
        "Medium": "not yet wired: backlog type-scales columns (research/66 S2 DEFECT)",
        "Leading Ratio": "not yet wired: backlog type-scales columns (research/66 S2 DEFECT)",
    } for fmt in ("docx", "pptx", "pdf", "png")},
    "typefaces": {
        "docx": {
            "Best For": _IDENTITY, "Brand Scope": _IDENTITY, "Display Name": _IDENTITY, "Keywords": _IDENTITY,
            "Scale Key": _ROUTING,
            "Category Contrast": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Embedding Licence": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Family Count": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Has Tabular Figures": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Mono Family": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Safe Stack Availability": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Body Family": "not applicable: docx's only render target (docx-office) is "
                          "safe-stack; the embed branch's family columns are unreachable "
                          "with today's data",
            "Heading Family": "not applicable: docx's only render target (docx-office) is "
                             "safe-stack; the embed branch's family columns are unreachable "
                             "with today's data",
        },
        "pptx": {
            "Best For": _IDENTITY, "Brand Scope": _IDENTITY, "Display Name": _IDENTITY, "Keywords": _IDENTITY,
            "Scale Key": _ROUTING,
            "Category Contrast": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Embedding Licence": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Family Count": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Has Tabular Figures": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Mono Family": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Safe Stack Availability": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Safe Stack Fallback": "not applicable: pptx's only render target (pptx-office) is "
                                  "embed; the safe-stack branch's fallback column is "
                                  "unreachable with today's data",
            "Safe Stack Body Fallback": "not applicable: pptx's only render target (pptx-office) "
                                       "is embed; the safe-stack branch's fallback columns are "
                                       "unreachable with today's data",
        },
        "pdf": {
            "Best For": _IDENTITY, "Brand Scope": _IDENTITY, "Display Name": _IDENTITY, "Keywords": _IDENTITY,
            "Scale Key": _ROUTING,
            "Category Contrast": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Embedding Licence": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Family Count": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Has Tabular Figures": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Mono Family": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Safe Stack Availability": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Safe Stack Fallback": "not applicable: pdf's render targets (pdf-chromium, "
                                  "pdf-weasyprint, pdf-weasyprint-pdfx4, pdf-wkhtmltopdf) are "
                                  "all embed; the safe-stack branch's fallback column is "
                                  "unreachable with today's data",
            "Safe Stack Body Fallback": "not applicable: pdf's render targets (pdf-chromium, "
                                       "pdf-weasyprint, pdf-weasyprint-pdfx4, pdf-wkhtmltopdf) are "
                                       "all embed; the safe-stack branch's fallback columns are "
                                       "unreachable with today's data",
        },
        "png": {
            "Best For": _IDENTITY, "Brand Scope": _IDENTITY, "Display Name": _IDENTITY, "Keywords": _IDENTITY,
            "Scale Key": _ROUTING,
            "Category Contrast": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Embedding Licence": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Family Count": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Has Tabular Figures": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Mono Family": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Safe Stack Availability": "not yet wired: backlog typefaces columns (research/66 S2 DEFECT)",
            "Safe Stack Fallback": "not applicable: png-social is embed; the safe-stack "
                                  "branch's fallback column is unreachable with today's data",
            "Safe Stack Body Fallback": "not applicable: png-social is embed; the safe-stack "
                                       "branch's fallback columns are unreachable with today's "
                                       "data",
        },
    },
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


def _section_headings(resolved, language):
    """(target_lang, source, [(canonical_section, text_or_None, fallback_note_or_None), ...])
    for the resolved structure row, in Section Order -- the section list AND the
    wording a renderer needs (research/54 part 3), not just the structural TOC
    depth `_heading_roles` already gives.

    research/64 D-E (A7): `target_lang` is the document's ACTUAL language --
    resolve.py's top-level `language` block (an override or the doctype's own
    `Default Language`), not `structures."Heading Language"`. That column is now
    only the FALLBACK: a section with no primary heading authored in the target
    language falls back to it and the pair's third element carries the exact
    "(no <lang> wording authored; <fallback-lang> used)" note (never silent). A
    section missing a primary heading in BOTH languages still returns None with
    no note -- that is an unrelated data gap, not a language fallback."""
    v = HANDOFF_VOCAB
    structure_row = _first_row(resolved, v["structure_table"])
    if not structure_row:
        return None, None, []
    fallback_lang = structure_row.get(v["structure_heading_language_column"], "")
    target_lang = language.get("value") or fallback_lang
    source = language.get("source", "doctype-default")
    order = structure_row.get(v["structure_section_order_column"], "")
    sections = [s for s in order.split(";") if s]
    primary_text = {}
    for row in resolved.get(v["headings_table"], []):
        if row.get(v["headings_is_primary_column"]) == "yes":
            key = (row.get(v["headings_language_column"]), row.get(v["headings_canonical_section_column"]))
            primary_text[key] = row.get(v["headings_text_column"], "")
    pairs = []
    for section in sections:
        text = primary_text.get((target_lang, section))
        note = None
        if text is None and target_lang != fallback_lang:
            text = primary_text.get((fallback_lang, section))
            if text is not None:
                note = f"(no {target_lang} wording authored; {fallback_lang} used)"
        pairs.append((section, text, note))
    return target_lang, source, pairs


def _sections_lines(resolved, language):
    target_lang, source, pairs = _section_headings(resolved, language)
    lines = [f"  sections (Section Order, language={target_lang}, source={source}):"
             if target_lang else "  sections:"]
    if not pairs:
        lines.append(f"    {NOT_PRESENT}")
        return lines
    for section, text, note in pairs:
        line = f"    {section}: {text if text else NOT_PRESENT}"
        if note:
            line += f"  {note}"
        lines.append(line)
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


def _cv_region_lines(resolved):
    """cv-regions.Seniority Band -- research/66's flagship stage-1 DEFECT
    example: the only column distinguishing `uk-early` from `uk-experienced`,
    absent from every builder even after the stage-1 fix resolved it.

    research/64 D-B: a doctype like cv-uk resolves MULTIPLE cv-regions rows
    with different Section Orders -- `_first_row` printed only one band with
    no way to tell which Section Order it selects, silently dropping the
    other row entirely. Every resolved row is printed here, each with its
    own Section Order, so a consumer always knows which order goes with
    which band."""
    v = HANDOFF_VOCAB
    rows = resolved.get(v["cv_region_table"], [])
    lines = ["  cv region (data/base/cv-regions.csv):"]
    if not rows:
        lines.append(f"    {NOT_PRESENT}")
        return lines
    band_column = v["cv_region_seniority_band_column"]
    order_column = v["cv_region_section_order_column"]
    for row in rows:
        band = row.get(band_column, "")
        order = row.get(order_column, "")
        lines.append(f"    [{row.get('key', '')}] {band_column}: "
                     f"{band if band else NOT_PRESENT}, {order_column}: "
                     f"{order if order else NOT_PRESENT}")
    return lines


def _doc_style_lines(resolved):
    """doc-styles's visual specification -- rules, fills, emphasis, field
    style, checklist -- read the same way on every format (research/66: the
    table has no format-specific content, unlike page-formats or
    render-targets)."""
    v = HANDOFF_VOCAB
    row = _first_row(resolved, v["doc_style_table"])
    lines = ["  doc style (rules/fills/emphasis -- data/base/doc-styles.csv):"]
    if not row:
        lines.append(f"    {NOT_PRESENT}")
        return lines
    for column in (
        v["doc_style_rule_hair_column"], v["doc_style_rule_strong_column"],
        v["doc_style_rule_brand_column"], v["doc_style_corner_radius_column"],
        v["doc_style_table_rules_column"], v["doc_style_table_fills_column"],
        v["doc_style_emphasis_column"], v["doc_style_field_style_column"],
        v["doc_style_checklist_column"],
    ):
        value = row.get(column, "")
        lines.append(f"    {column}: {value if value else NOT_PRESENT}")
        if column == v["doc_style_table_rules_column"]:
            instruction = TABLE_RULES_INSTRUCTIONS.get(value)
            if instruction:
                lines.append(f"    {instruction}")
    spacing_instruction = STYLE_SPACING_INSTRUCTIONS.get(row.get("key", ""))
    if spacing_instruction:
        lines.append(f"    {spacing_instruction}")
    return lines


def _build_docx_lines(resolved, language):
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
    render_rows = [r for r in resolved.get(v["render_target_table"], [])
                   if r.get(v["render_target_format_column"]) == "docx"]
    # research/66 D8: docx printed both the family columns AND the safe-stack
    # fallback unconditionally -- pdf/png already branch on the render target's
    # own Font Rule (embed vs. safe-stack); this matches that.
    lines.append("  fonts: (embed vs. safe-stack per render target's Font Rule)")
    if typeface_row and render_rows:
        for row in render_rows:
            engine = row.get(v["render_target_engine_column"], "")
            rule = row.get(v["render_target_font_rule_column"], "")
            if rule == "embed":
                families = " / ".join(
                    typeface_row.get(c, "") for c in v["typeface_family_columns"] if typeface_row.get(c, ""))
                lines.append(f"    {engine} ({rule}): {families or NOT_PRESENT}")
            else:
                heading_fallback = typeface_row.get(v["typeface_fallback_column"], "")
                body_fallback = typeface_row.get(v["typeface_body_fallback_column"], "")
                if heading_fallback or body_fallback:
                    lines.append(f"    {engine} ({rule}): headings {heading_fallback or NOT_PRESENT} "
                                 f"/ body {body_fallback or heading_fallback or NOT_PRESENT}")
                else:
                    lines.append(f"    {engine} ({rule}): {NOT_PRESENT}")
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

    lines.extend(_sections_lines(resolved, language))

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

    lines.extend(_cv_region_lines(resolved))

    lines.extend(_doc_style_lines(resolved))

    lines.extend(_page_flow_docx_lines(resolved))

    return lines


def _build_pptx_lines(resolved, language):
    v = HANDOFF_VOCAB
    lines = []

    page_row = _first_row(resolved, v["page_format_table"])
    try:
        w_in = round(float(page_row["Trim W mm"]) / 25.4, 3)
        h_in = round(float(page_row["Trim H mm"]) / 25.4, 3)
    except (TypeError, KeyError, ValueError):
        w_in = h_in = None
    if w_in and h_in:
        # research/87 F5: pptxgenjs's built-in LAYOUT_16x9 is 10 x 5.625in, a third smaller
        # than the resolved page-formats row (13.333 x 7.5in); the type sizes are authored
        # for the row's size, so define a layout of exactly that trim.
        lines.append(f"  slide layout (from page-formats {page_row.get('key', '')} trim; "
                     "pptxgenjs `pres.defineLayout`, then `pres.layout = 'DDI_LAYOUT'`):")
        lines.append(f"    DDI_LAYOUT: {w_in:g}in x {h_in:g}in")
    else:
        lines.append("  slide layout (pptxgenjs default -- research/23 pptx:454; no page-formats "
                     "row resolved):")
        lines.append(f"    {PPTX_DEFAULT_LAYOUT_NAME}: {PPTX_DEFAULT_LAYOUT_IN[0]}in x {PPTX_DEFAULT_LAYOUT_IN[1]}in")

    typeface_row = _first_row(resolved, v["typeface_table"])
    render_rows = [r for r in resolved.get(v["render_target_table"], [])
                   if r.get(v["render_target_format_column"]) == "pptx"]
    # research/66 D8: pptx printed both the family columns AND the safe-stack
    # fallback unconditionally -- pdf/png already branch on the render target's
    # own Font Rule (embed vs. safe-stack); this matches that.
    lines.append("  fonts: (embed vs. safe-stack per render target's Font Rule)")
    if typeface_row and render_rows:
        for row in render_rows:
            engine = row.get(v["render_target_engine_column"], "")
            rule = row.get(v["render_target_font_rule_column"], "")
            if rule == "embed":
                families = " / ".join(
                    typeface_row.get(c, "") for c in v["typeface_family_columns"] if typeface_row.get(c, ""))
                lines.append(f"    {engine} ({rule}): {families or NOT_PRESENT}")
            else:
                heading_fallback = typeface_row.get(v["typeface_fallback_column"], "")
                body_fallback = typeface_row.get(v["typeface_body_fallback_column"], "")
                if heading_fallback or body_fallback:
                    lines.append(f"    {engine} ({rule}): headings {heading_fallback or NOT_PRESENT} "
                                 f"/ body {body_fallback or heading_fallback or NOT_PRESENT}")
                else:
                    lines.append(f"    {engine} ({rule}): {NOT_PRESENT}")
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

    lines.extend(_sections_lines(resolved, language))

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

    lines.extend(_cv_region_lines(resolved))

    lines.extend(_doc_style_lines(resolved))

    lines.extend(_page_flow_pptx_lines(resolved))

    return lines


def _build_pdf_lines(resolved, language):
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

    lines.extend(_sections_lines(resolved, language))

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

    lines.extend(_cv_region_lines(resolved))

    lines.extend(_doc_style_lines(resolved))

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


def _build_png_lines(resolved, language):
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

    lines.extend(_sections_lines(resolved, language))

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

    lines.extend(_cv_region_lines(resolved))

    lines.extend(_doc_style_lines(resolved))

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


def _load_full_designs(data_dir):
    """Fresh, standalone load of data/base/designs.csv (+ any brand
    overlay) -- NOT read off the resolve.py --json payload, so a plain
    `ddi.py resolve --doctype ...` (no --design) still gets a `design:`
    handoff line naming the doctype's own default design, and so `rank r
    of N` can be computed against the WHOLE family, not just whatever one
    design row (if any) happens to be in `resolved`. Returns [] (never
    raises) if the manifest can't be read or declares no `designs` table at
    all -- a data dir with no design library yet (this project's own toy
    test fixtures) must degrade to "no design line", not a crash."""
    try:
        manifest = resolve.datalib.load_manifest(data_dir)
    except (OSError, ValueError):
        return []
    spec = manifest.get("tables", {}).get("designs")
    if not spec:
        return []
    problems = resolve.datalib.ProblemLog()
    return resolve.datalib.load_table_rows(data_dir, spec, problems, table_name="designs")


def _design_handoff_line(resolved, data_dir):
    """research/80-v05-plan.md section 6 P1.5: `design: <Display Name>
    (rank r of N, <Evidence Class>)` -- the `--design`-overridden design if
    resolve.py included one in `resolved["designs"]`, else this doctype's
    own default (the family design whose Reasoning Key equals the resolved
    doctype row's own Reasoning Key). None (no line printed) if neither can
    be found -- e.g. the resolved payload carries no `doctypes` row at all
    (a non-doctype entry table, this project's own toy test fixtures) or
    the data dir has no designs library."""
    all_designs = _load_full_designs(data_dir)
    if not all_designs:
        return None

    design_row = None
    resolved_designs = resolved.get("designs", [])
    if resolved_designs:
        key = resolved_designs[0].get("key", "")
        design_row = next((d for d in all_designs if d.get("design_key", "") == key), None)

    if design_row is None:
        doctype_row = _first_row(resolved, "doctypes")
        if doctype_row is None:
            return None
        family = doctype_row.get("Family", "")
        reasoning_key = doctype_row.get("Reasoning Key", "")
        reasoning_row = _first_row(resolved, "doc-reasoning") or {}
        design_key = reasoning_row.get("Design Key", "")
        design_row = next((d for d in all_designs if design_key and d.get("design_key", "") == design_key
                           and d.get("Family", "") == family), None)
        if design_row is None:
            design_row = next(
                (d for d in all_designs
                 if d.get("Family", "") == family and d.get("Reasoning Key", "") == reasoning_key),
                None,
            )

    if design_row is None:
        return None

    family = design_row.get("Family", "")
    n_total = sum(1 for d in all_designs if d.get("Family", "") == family)
    return (f"design: {design_row.get('Display Name', '')} "
            f"(rank {design_row.get('Rank', '')} of {n_total}, "
            f"{design_row.get('Evidence Class', '')})")


def _build_handoff_lines(resolved_payload, target_format, data_dir=None):
    resolved = resolved_payload.get("resolved", {})
    language = resolved_payload.get("language", {})
    lines = [f"HANDOFF (format={target_format})"]
    design_line = _design_handoff_line(resolved, data_dir or DEFAULT_DATA_DIR)
    if design_line:
        lines.append(design_line)
    lines.extend(_FORMAT_BUILDERS[target_format](resolved, language))
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
    parser.add_argument("--data-dir", default=None,
                         help="data dir for the design-library lookup used by the `design:` "
                              "line (default: this skill's own data/)")
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

    data_dir = Path(args.data_dir) if args.data_dir else None
    for line in _build_handoff_lines(payload, args.format, data_dir):
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


# ---------------------------------------------------------------------------
# designs / library -- research/80-v05-plan.md section 6 P1.5/P1.6. Both read
# the real data/base tables directly (via resolve.datalib, resolve.BM25 --
# already-imported sibling modules, no new top-level import here so the
# stdlib-only guard above needs no change) rather than going through
# resolve.py's entry-table Stage 1, since neither is a doctype resolution:
# `designs` browses one family's designs.csv rows, `library` browses the
# palette/typeface/type-scale/doc-style tables directly.
# ---------------------------------------------------------------------------

def _provenance_line(provenance_rows, table_name, row_key):
    """One-line evidence summary for a designs/library entry: Source Name
    plus Ranking Metric/Rank Value if the provenance row carries them
    (research/80-v05-plan.md section 2C). `row_key` is looked up EXACTLY
    against provenance.csv's own polymorphic FK (Table, Row Key) -- no
    fuzzy matching, and the first match wins if more than one row is ever
    authored for the same (table, key)."""
    if not row_key:
        return "(no provenance recorded)"
    matches = [p for p in provenance_rows
               if p.get("Table", "") == table_name and p.get("Row Key", "") == row_key]
    if not matches:
        return "(no provenance recorded)"
    row = matches[0]
    source = row.get("Source Name", "")
    if not source:
        source = ("(convention -- no external source)"
                  if row.get("Evidence Class", "") == "convention" else "(unnamed source)")
    metric = row.get("Ranking Metric", "")
    value = row.get("Rank Value", "")
    if metric and value:
        return f"{source} ({metric}: {value})"
    if metric:
        return f"{source} ({metric})"
    return source


def cmd_designs(argv):
    """`ddi.py designs --doctype <doc_key> [--query "<text>"] [--json]`

    Lists the designs (data/base/designs.csv) whose Family matches the
    given doctype's own Family, in Rank order; marks the design whose
    Reasoning Key equals the doctype's own Reasoning Key as this doctype's
    default. With --query, re-ranks by BM25 (resolve.py's own
    implementation, reused rather than reimplemented) over Keywords + Best
    For + Display Name, ties broken by Rank. Each design's "rank r of N"
    always names its own authored Rank and family size, never its position
    in a --query-reordered list.

    Exit codes: 0 printed successfully (including an empty family). 1
    unknown --doctype, or a tier-1 (structural) data problem.
    """
    import argparse

    parser = argparse.ArgumentParser(prog="ddi.py designs")
    parser.add_argument("--doctype", required=True)
    parser.add_argument("--query", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--data-dir", default=None)
    args = parser.parse_args(argv)

    data_dir = Path(args.data_dir) if args.data_dir else DEFAULT_DATA_DIR
    datalib = resolve.datalib

    tier1_ok, tier1_lines, _tier2, _summary = validate_data.validate_tiered(data_dir)
    if not tier1_ok:
        for line in tier1_lines:
            print(line)
        print(f"\n{len(tier1_lines)} structural problem(s) found -- refusing")
        return 1

    manifest = datalib.load_manifest(data_dir)
    tables = manifest["tables"]
    problems = datalib.ProblemLog()
    all_rows = datalib.load_all_tables(data_dir, tables, problems)

    doctype_spec = tables.get("doctypes", {})
    doctype_key_col = doctype_spec.get("key_column", "doc_key")
    doctype_row = next(
        (r for r in all_rows.get("doctypes", []) if r.get(doctype_key_col, "") == args.doctype),
        None,
    )
    if doctype_row is None:
        print(f"[NO SUCH DOCTYPE] doctype={args.doctype!r} not found in doctypes table")
        return 1

    family = doctype_row.get("Family", "")
    default_reasoning_key = doctype_row.get("Reasoning Key", "")
    default_reasoning_row = next(
        (r for r in all_rows.get("doc-reasoning", []) if r.get("doc_category", "") == default_reasoning_key), {})
    default_design_key = default_reasoning_row.get("Design Key", "")

    design_spec = tables.get("designs", {})
    design_key_col = design_spec.get("key_column", "design_key")
    family_designs = [r for r in all_rows.get("designs", []) if r.get("Family", "") == family]
    family_designs.sort(key=lambda r: int(r.get("Rank", "0") or 0))
    n_total = len(family_designs)

    doc_reasoning_by_key = {r.get("doc_category", ""): r for r in all_rows.get("doc-reasoning", [])}
    provenance_rows = all_rows.get("provenance", [])

    order = list(range(len(family_designs)))
    method = "rank"
    scores = None
    if args.query:
        documents = [
            " ".join([r.get("Keywords", ""), r.get("Best For", ""), r.get("Display Name", "")])
            for r in family_designs
        ]
        bm25 = resolve.BM25()
        bm25.fit(documents)
        # R2 F4: a term present in EVERY design of the family carries no signal;
        # its IDF is ~0 and BM25 length noise would reorder the family.
        doc_tokens = [set(resolve.BM25.tokenize(d)) for d in documents]
        terms = [t for t in dict.fromkeys(resolve.BM25.tokenize(args.query))
                 if not all(t in dt for dt in doc_tokens)]
        if terms:
            scores = bm25.scores(" ".join(terms))
            if max(scores) > 0:
                order.sort(key=lambda i: (-scores[i], int(family_designs[i].get("Rank", "0") or 0)))
                method = "bm25"
            else:
                scores = None

    entries = []
    for i in order:
        row = family_designs[i]
        design_key = row.get(design_key_col, "")
        dr = doc_reasoning_by_key.get(row.get("Reasoning Key", ""), {})
        entry = {
            "design_key": design_key,
            "display_name": row.get("Display Name", ""),
            "rank": row.get("Rank", ""),
            "n": n_total,
            "evidence_class": row.get("Evidence Class", ""),
            "best_for": row.get("Best For", ""),
            "keywords": row.get("Keywords", ""),
            "is_default": (row.get(design_key_col, "") == default_design_key if default_design_key
                           else bool(row.get("Reasoning Key", ""))
                           and row.get("Reasoning Key", "") == default_reasoning_key),
            "evidence": _provenance_line(provenance_rows, "designs", design_key),
            "style_key": dr.get("Style Key", ""),
            "palette_key": dr.get("Palette Key", ""),
            "typeface_key": dr.get("Typeface Key", ""),
        }
        if scores is not None:
            entry["score"] = round(scores[i], 4)
        entries.append(entry)

    if args.json:
        print(json.dumps(
            {"doctype": args.doctype, "family": family, "query": args.query,
             "method": method, "designs": entries},
            indent=2,
        ))
        return 0

    print(f"DESIGNS for doctype={args.doctype!r} (family={family}, method={method})")
    for e in entries:
        default_marker = "  [DEFAULT for this doctype]" if e["is_default"] else ""
        print(f"  {e['display_name']}  [{e['design_key']}]  rank {e['rank']} of {e['n']}"
              f"{default_marker}")
        print(f"    Evidence Class: {e['evidence_class']}")
        print(f"    Best For: {e['best_for']}")
        print(f"    Evidence: {e['evidence']}")
        print(f"    Resolved: style={e['style_key'] or NOT_PRESENT} "
              f"palette={e['palette_key'] or NOT_PRESENT} typeface={e['typeface_key'] or NOT_PRESENT}")
        if "score" in e:
            print(f"    score: {e['score']}")
    return 0


def _library_key_values(table_name, row):
    if table_name == "palettes":
        return [f"Primary: {row.get('Primary', '') or NOT_PRESENT}",
                f"Accent: {row.get('Accent', '') or NOT_PRESENT}",
                f"Background: {row.get('Background', '') or NOT_PRESENT}"]
    if table_name == "typefaces":
        return [f"Heading Family: {row.get('Heading Family', '') or NOT_PRESENT}",
                f"Body Family: {row.get('Body Family', '') or NOT_PRESENT}",
                f"Embedding Licence: {row.get('Embedding Licence', '') or NOT_PRESENT}"]
    if table_name == "doc-styles":
        return [f"Table Rules: {row.get('Table Rules', '') or NOT_PRESENT}",
                f"Emphasis Mechanism: {row.get('Emphasis Mechanism', '') or NOT_PRESENT}",
                f"Field Style: {row.get('Field Style', '') or NOT_PRESENT}"]
    return []


_LIBRARY_KEY_COLUMNS = {
    "palettes": "palette_key",
    "typefaces": "typeface_key",
    "doc-styles": "style_key",
}


def _library_simple(table_name, rows, provenance_rows, query):
    """palettes/typefaces/doc-styles -- one library entry per row, BM25 over
    Keywords + Display Name + Best For when --query is given."""
    key_col = _LIBRARY_KEY_COLUMNS[table_name]
    order = list(range(len(rows)))
    method = "authored-order"
    scores = None
    if query:
        documents = [
            " ".join([r.get("Keywords", ""), r.get("Display Name", ""), r.get("Best For", "")])
            for r in rows
        ]
        bm25 = resolve.BM25()
        bm25.fit(documents)
        scores = bm25.scores(query)
        if max(scores, default=0) > 0:
            order.sort(key=lambda i: -scores[i])
            method = "bm25"
        else:
            scores, method = None, "rank"

    entries = []
    for i in order:
        row = rows[i]
        key = row.get(key_col, "")
        entry = {
            "key": key,
            "name": row.get("Display Name", ""),
            "key_values": _library_key_values(table_name, row),
            "evidence": _provenance_line(provenance_rows, table_name, key),
        }
        if scores is not None:
            entry["score"] = round(scores[i], 4)
        entries.append(entry)
    return entries, method


def _brand_slugs(all_rows):
    """Every non-generic Brand Scope value present in any loaded table."""
    return {r.get("Brand Scope", "") for rows in all_rows.values() for r in rows
            if r.get("Brand Scope", "") not in ("", "generic")}


def _scale_in_scope(scale_key, scope, brand_slugs):
    """type-scales has no Brand Scope column; a brand kit's scales are keyed
    `<slug>-...` (make_brand_kit), so scope is read off the key prefix."""
    owner = next((b for b in brand_slugs if scale_key.startswith(b + "-")), "generic")
    return owner == scope


def _library_type_scales(rows, provenance_rows, query):
    """type-scales has no Keywords/Display Name/Best For at all -- rows are
    grouped by scale_key first (one library entry per ratio-family x
    medium, not per role row), and --query searches scale_key + Medium."""
    groups = {}
    order_keys = []
    for row in rows:
        key = row.get("scale_key", "")
        if key not in groups:
            groups[key] = []
            order_keys.append(key)
        groups[key].append(row)

    def size_for(member_rows, role):
        return next((r.get("Size pt", "") for r in member_rows if r.get("Role", "") == role), "")

    keys = list(order_keys)
    method = "authored-order"
    scores_by_key = None
    if query:
        documents = [f"{key} {groups[key][0].get('Medium', '') if groups[key] else ''}"
                     for key in order_keys]
        bm25 = resolve.BM25()
        bm25.fit(documents)
        scores = bm25.scores(query)
        if max(scores, default=0) > 0:
            scores_by_key = dict(zip(order_keys, scores))
            keys = sorted(order_keys, key=lambda k: -scores_by_key[k])
            method = "bm25"
        else:
            method = "rank"

    entries = []
    for key in keys:
        member_rows = groups[key]
        medium = member_rows[0].get("Medium", "") if member_rows else ""
        body = size_for(member_rows, "body")
        h1 = size_for(member_rows, "h1")
        row_key_for_prov = member_rows[0].get("scale_row_key", "") if member_rows else ""
        entry = {
            "key": key,
            "name": key,
            "key_values": [f"Medium: {medium or NOT_PRESENT}",
                           f"body: {body or NOT_PRESENT}pt",
                           f"h1: {h1 or NOT_PRESENT}pt"],
            "evidence": _provenance_line(provenance_rows, "type-scales", row_key_for_prov),
        }
        if scores_by_key is not None:
            entry["score"] = round(scores_by_key[key], 4)
        entries.append(entry)
    return entries, method


def cmd_library(argv):
    """`ddi.py library <palettes|typefaces|type-scales|doc-styles>
    [--query "<text>"] [--json] [--limit N] [--brand <slug>]`

    Browses the grand library (data/base/{palettes,typefaces,type-scales,
    doc-styles}.csv) with each entry's provenance evidence line. Only
    Brand Scope=="generic" rows are shown unless --brand names a scope to
    show INSTEAD (brand rows only, not brand + generic). type-scales has
    no Brand Scope column, so its scope is read off the `<slug>-` key prefix.

    Exit codes: 0 printed successfully. 1 unknown --brand, or a tier-1
    (structural) data problem. 2 bad usage (argparse), including an
    unknown library name.
    """
    import argparse

    parser = argparse.ArgumentParser(prog="ddi.py library")
    parser.add_argument("table", choices=LIBRARY_TABLES)
    parser.add_argument("--query", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--brand", default=None)
    parser.add_argument("--data-dir", default=None)
    args = parser.parse_args(argv)

    data_dir = Path(args.data_dir) if args.data_dir else DEFAULT_DATA_DIR
    datalib = resolve.datalib

    tier1_ok, tier1_lines, _tier2, _summary = validate_data.validate_tiered(data_dir)
    if not tier1_ok:
        for line in tier1_lines:
            print(line)
        print(f"\n{len(tier1_lines)} structural problem(s) found -- refusing")
        return 1

    manifest = datalib.load_manifest(data_dir)
    tables = manifest["tables"]
    problems = datalib.ProblemLog()
    all_rows = datalib.load_all_tables(data_dir, tables, problems)
    provenance_rows = all_rows.get("provenance", [])

    scope = args.brand or "generic"
    brand_slugs = _brand_slugs(all_rows)
    if args.brand and args.brand not in brand_slugs:
        print(f"[NO SUCH BRAND] brand={args.brand!r} has no rows in any table "
              f"(known: {', '.join(sorted(brand_slugs)) or 'none'})")
        return 1

    if args.table == "type-scales":
        scale_rows = [r for r in all_rows.get("type-scales", [])
                      if _scale_in_scope(r.get("scale_key", ""), scope, brand_slugs)]
        entries, method = _library_type_scales(scale_rows, provenance_rows, args.query)
    else:
        rows = [r for r in all_rows.get(args.table, []) if r.get("Brand Scope", "") == scope]
        entries, method = _library_simple(args.table, rows, provenance_rows, args.query)

    if args.limit is not None:
        entries = entries[: args.limit]

    if args.json:
        print(json.dumps(
            {"table": args.table, "query": args.query, "method": method, "entries": entries},
            indent=2,
        ))
        return 0

    print(f"LIBRARY {args.table} (method={method})")
    for e in entries:
        print(f"  {e['name']}  [{e['key']}]")
        for line in e["key_values"]:
            print(f"    {line}")
        print(f"    Evidence: {e['evidence']}")
        if "score" in e:
            print(f"    score: {e['score']}")
    return 0


COMMANDS = {
    "check": cmd_check,
    "resolve": cmd_resolve,
    "preflight": cmd_preflight,
    "handoff": cmd_handoff,
    "designs": cmd_designs,
    "library": cmd_library,
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
