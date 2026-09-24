#!/usr/bin/env python3
"""Build portable/ -- a self-contained markdown knowledge pack for AI agents that
cannot execute code (research/80-v05-plan.md section 5, P6.1/P6.2).

`ddi.py` (scripts/ddi.py) is the mandatory workflow for an agent that CAN run
python3: resolve, preflight, handoff. An agent without code execution (a Custom
GPT, a Grok/Gemini project with only a knowledge-file upload, a plain-chat
assistant) can still be pointed at the exact same design rules if they are
flattened into plain markdown ahead of time -- that is what this script does.

Writes three files under `portable/` (sibling of `research/` and `skill/`):
  - AGENTS.md         platform-neutral operating instructions (< 8000 chars)
  - DDI-LIBRARY.md    every doctype's fully resolved values + the grand library
  - INSTALL.md        how to load this pack into each platform

Stdlib only, deterministic (sorted iteration, no timestamps), LF line endings,
UTF-8. Runs from any cwd -- every path below is resolved relative to this
file, not the process's working directory.

Reuses, rather than reimplements, the skill's own resolution mechanism:
`scripts/resolve.py`'s `_fk_walk` (foreign-key walk from an already-known
entry row) is imported and called directly, once per doctype, with no
--query/BM25 step -- a doctype's own key is already known here, so there is
nothing to search for. This is the same FK walk `ddi.py resolve --doctype`
runs, so this pack cannot silently diverge from what the code-execution path
actually resolves for the same doctype (short of an --design override, which
the per-family designs table already carries as its own rows).
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


def _assert_stdlib_only(extra_allowed=()):
    """Fail loudly at import time if a non-stdlib import is ever added here.

    Same guard, for the same reason, as scripts/ddi.py and scripts/resolve.py:
    this generator ships to platforms with no package manager, so it must
    never grow a dependency only a code-execution sandbox happens to have.
    `extra_allowed` permits importing this project's own sibling stdlib-only
    modules (resolve.py, which is itself stdlib-only and asserts so on its
    own import).
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


_assert_stdlib_only(extra_allowed={"resolve"})

HERE = Path(__file__).resolve().parent               # research/
REPO_ROOT = HERE.parent
SKILL_ROOT = REPO_ROOT / "skill" / "document-design-intelligence"
SCRIPTS_DIR = SKILL_ROOT / "scripts"
DEFAULT_DATA_DIR = SKILL_ROOT / "data"
PORTABLE_DIR = REPO_ROOT / "portable"

sys.path.insert(0, str(SCRIPTS_DIR))
import resolve  # noqa: E402 -- sibling script; itself stdlib-only, asserts so on import

datalib = resolve.datalib
validate_data = resolve.validate_data

NOT_PRESENT = "(not present)"
AGENTS_MD_CHAR_LIMIT = 8000


# =============================================================================
# data loading -- one full load + one FK walk per doctype, all from data/base
# (generic scope only; brand overlays are a per-user artifact, not part of a
# knowledge pack meant to serve any agent for any user).
# =============================================================================

def load_context(data_dir=None):
    """Everything the three builders need, loaded once: the manifest, every
    base table, and a per-doctype resolved FK-walk keyed by doc_key.

    Raises RuntimeError if the data fails validate_data.py's tier-1
    (structural) gate -- a portable pack built from invalid data would ship
    silently wrong values, and this generator has no per-key degradation
    story of its own (unlike ddi.py resolve, which is used interactively).
    """
    data_dir = Path(data_dir) if data_dir else DEFAULT_DATA_DIR

    tier1_ok, tier1_lines, _tier2, _summary = validate_data.validate_tiered(data_dir)
    if not tier1_ok:
        raise RuntimeError(
            "data/base fails validate_data.py's structural gate -- refusing to "
            "build a portable pack from it:\n" + "\n".join(tier1_lines)
        )

    manifest = datalib.load_manifest(data_dir)
    tables_spec = manifest["tables"]
    problems = datalib.ProblemLog()
    all_rows = datalib.load_all_tables(data_dir, tables_spec, problems)
    # G1 (research/87): load_all_tables merges every data/brand/<slug>/ overlay. A knowledge
    # pack is generic by definition, so keep only rows that came from data/base -- this is
    # table-agnostic (doc-reasoning and type-scales have no Brand Scope column).
    base_dir = (data_dir / "base").resolve()
    all_rows = {
        name: [r for r in rows if base_dir in Path(r.get("__file__", base_dir / "x")).resolve().parents]
        for name, rows in all_rows.items()
    }

    families = list(tables_spec["doctypes"]["enums"]["Family"])  # manifest's own order

    rows_by_key = {
        name: {r.get(spec["key_column"], ""): r for r in all_rows[name]}
        for name, spec in tables_spec.items() if spec.get("key_column")
    }

    doctype_key_col = tables_spec["doctypes"]["key_column"]
    resolved_by_doctype = {}
    for row in all_rows["doctypes"]:
        key = row.get(doctype_key_col, "")
        resolved_by_doctype[key] = resolve._fk_walk(
            "doctypes", row, tables_spec, all_rows, rows_by_key
        )

    return {
        "tables_spec": tables_spec,
        "all_rows": all_rows,
        "rows_by_key": rows_by_key,
        "families": families,
        "resolved_by_doctype": resolved_by_doctype,
    }


def _first(resolved, table):
    rows = resolved.get(table)
    return rows[0] if rows else None


def _split(value, sep=";"):
    return [t.strip() for t in (value or "").split(sep) if t.strip()]


def _dedup_keep_order(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


# =============================================================================
# DDI-LIBRARY.md
# =============================================================================

def _page_format_lines(row):
    if not row:
        return ["- page format: " + NOT_PRESENT]
    w, h = row.get("Trim W mm", ""), row.get("Trim H mm", "")
    top = row.get("Margin Top mm", "")
    bottom = row.get("Margin Bottom mm", "")
    inside = row.get("Margin Inside mm", "")
    outside = row.get("Margin Outside mm", "")
    bleed = row.get("Bleed mm", "")
    lines = [
        f"- page format: {row.get('Display Name', '')} ({row.get('page_format_key', '')})",
        f"  - trim: {w}mm x {h}mm; margins top/bottom/inside/outside: "
        f"{top}/{bottom}/{inside}/{outside}mm; bleed: {bleed or '0'}mm",
    ]
    columns = row.get("Columns", "")
    measure = row.get("Measure mm", "")
    if columns or measure:
        lines.append(f"  - columns: {columns or NOT_PRESENT}; measure: {measure or NOT_PRESENT}mm")
    # F2 (research/87): every remaining non-empty print-geometry column
    extras = [("safe margin", "Safe Margin mm", "mm"), ("fold", "Fold Type", ""),
              ("panels", "Panels mm", "mm"), ("stock", "Stock gsm", "gsm"),
              ("print mode", "Print Mode", ""), ("min DPI raster", "Min DPI Raster", ""),
              ("min DPI line art", "Min DPI Line Art", ""), ("folio", "Folio Style", ""),
              ("running head", "Running Head", "")]
    parts = [f"{label}: {row.get(col, '')}{unit}" for label, col, unit in extras
             if row.get(col, "") and row.get(col, "") != "none"]
    if parts:
        lines.append("  - print geometry: " + "; ".join(parts))
    return lines


def _typeface_lines(typeface_row, scale_rows):
    if not typeface_row:
        return ["- typography: " + NOT_PRESENT]
    heading = typeface_row.get("Heading Family", "")
    body = typeface_row.get("Body Family", "")
    heading_fb = typeface_row.get("Safe Stack Fallback", "")
    body_fb = typeface_row.get("Safe Stack Body Fallback", "") or heading_fb
    licence = typeface_row.get("Embedding Licence", "")
    lines = [
        f"- typography: {typeface_row.get('Display Name', '')} "
        f"({typeface_row.get('typeface_key', '')})",
        f"  - heading: {heading}  (safe-stack fallback: {heading_fb or NOT_PRESENT})",
        f"  - body: {body}  (safe-stack fallback: {body_fb or NOT_PRESENT})",
        f"  - embedding licence: {licence or NOT_PRESENT}",
    ]
    by_medium = {}
    for row in scale_rows:
        by_medium.setdefault(row.get("Medium", ""), []).append(row)
    role_order = ["h1", "h2", "h3", "lead", "body", "body-dense", "caption", "label", "legal"]
    for medium in sorted(by_medium):
        rows_by_role = {r.get("Role", ""): r for r in by_medium[medium]}
        parts = []
        for role in role_order:
            r = rows_by_role.get(role)
            if r:
                parts.append(f"{role} {r.get('Size pt', '')}pt/{r.get('Leading Ratio', '')}")
        if parts:
            lines.append(f"  - type scale ({medium}): " + ", ".join(parts))
    return lines


def _palette_lines(row):
    if not row:
        return ["- palette: " + NOT_PRESENT]
    roles = ["Primary", "On Primary", "Secondary", "On Secondary", "Accent", "On Accent",
              "Background", "Foreground", "Muted", "On Muted"]
    hexes = ", ".join(f"{r}={row.get(r, '') or NOT_PRESENT}" for r in roles if row.get(r, ""))
    rules = (f"rule hair/strong/brand: {row.get('Rule Hair', '')}/"
             f"{row.get('Rule Strong', '')}/{row.get('Rule Brand', '') or NOT_PRESENT}")
    return [
        f"- palette: {row.get('Display Name', '')} ({row.get('palette_key', '')})",
        f"  - {hexes}",
        f"  - {rules}",
        f"  - {_palette_roles(row)}",
    ]


def _palette_roles(row):
    """F3 (research/87): which roles may carry text and which are fill-only."""
    def roles(col):
        return "; ".join(_split(row.get(col, ""))) or "none"
    return (f"text-safe roles (may carry text on Background): {roles('Text-Safe Roles')}; "
            f"fill-only roles (never set text in these): {roles('Fill-Only Roles')}; "
            f"category-marker roles: {roles('Category Marker Roles')}")


def _style_lines(row):
    if not row:
        return ["- style: " + NOT_PRESENT]
    lines = [
        f"- style: {row.get('Display Name', '')} ({row.get('style_key', '')})",
        f"  - rules: hair {row.get('Rule Hair pt', '')}pt / strong {row.get('Rule Strong pt', '')}pt "
        f"/ brand {row.get('Rule Brand pt', '') or '0'}pt; corner radius: "
        f"{row.get('Corner Radius mm', '') or '0'}mm",
        f"  - table rules: {row.get('Table Rules', '')}; table fills: {row.get('Table Fills', '')}; "
        f"emphasis: {row.get('Emphasis Mechanism', '')}; field style: {row.get('Field Style', '')}",
    ]
    checklist = _split(row.get("Checklist", ""))
    if checklist:
        lines.append("  - checklist: " + "; ".join(checklist))
    return lines


def _primary_headings_index(headings_rows):
    """{(canonical_section, language): heading text} over every resolved
    headings row whose Is Primary is yes."""
    out = {}
    for row in headings_rows:
        if row.get("Is Primary") == "yes":
            out[(row.get("canonical_section", ""), row.get("Language", ""))] = row.get("Heading Text", "")
    return out


def _section_order_lines(section_order, headings_rows, label="section order"):
    if not section_order:
        return [f"- {label}: {NOT_PRESENT}"]
    index = _primary_headings_index(headings_rows)
    lines = [f"- {label} (headings en / fr / de where authored):"]
    for section in section_order:
        per_lang = []
        for lang in ("en", "fr", "de"):
            text = index.get((section, lang))
            if text:
                per_lang.append(f"{lang}: {text}")
        wording = " / ".join(per_lang) if per_lang else NOT_PRESENT
        lines.append(f"  - {section} -- {wording}")
    return lines


def _cv_region_lines(resolved):
    rows = resolved.get("cv-regions", [])
    if not rows:
        return []
    lines = ["- regional CV variants (a variant's section order OVERRIDES the structure order above "
             "for that region and seniority band; photo: customary = include only if the user "
             "supplies one, negative-signal = omit):"]
    for row in sorted(rows, key=lambda r: (r.get("region_key", ""), r.get("Seniority Band", ""))):
        lines.append(
            f"  - [{row.get('cv_region_key', '')}] band={row.get('Seniority Band', '')}, "
            f"max pages={row.get('Max Pages', '')}, photo={row.get('Photo', '')}, "
            f"date of birth={row.get('Date of Birth', '')}, marital status={row.get('Marital Status', '')}, "
            f"visa status={row.get('Visa Status', '')}, format={row.get('Format', '')}, "
            f"education before experience={row.get('Education Before Experience', '')}"
        )
        section_order = _split(row.get("Section Order", ""))
        if section_order:
            lines.append(f"    - section order: {'; '.join(section_order)}")
    return lines


_REF_RE = re.compile(r"^[a-z][a-z-]*:[A-Za-z][A-Za-z0-9 -]*$")


def _threshold_text(threshold, resolved, tables_spec):
    """F1: a `table:Column` threshold is a reference -- print the value(s) it points to
    in this doctype's resolved rows, not the reference."""
    if not threshold:
        return ""
    if not _REF_RE.match(threshold):
        return threshold
    table, column = threshold.split(":", 1)
    rows = resolved.get(table, [])
    key_col = tables_spec.get(table, {}).get("key_column", "")
    vals = [(r.get(key_col, ""), r.get(column, "")) for r in rows if r.get(column, "")]
    if not vals:
        return f"{threshold} (not resolved for this doctype)"
    if len({v for _, v in vals}) == 1:
        return vals[0][1]
    return "; ".join(f"{k}={v}" for k, v in vals)


def _constraints_lines(resolved, tables_spec):
    rows = resolved.get("constraints", [])
    if not rows:
        return [f"- key constraints: {NOT_PRESENT}"]
    by_set = {}
    for row in rows:
        by_set.setdefault(row.get("Set Key", ""), []).append(row)
    lines = ["- key constraints ([Set Key] Check: Parameter = limit -- severity [applies to]):"]
    for set_key in sorted(by_set):
        for row in by_set[set_key]:
            param = row.get("Parameter", "")
            limit = _threshold_text(row.get("Threshold", ""), resolved, tables_spec)
            expr = f"{param} = {limit}" if param and limit else (param or limit or "no parameter")
            lines.append(
                f"  - [{set_key}] {row.get('Check', '')}: {expr} -- {row.get('Severity', '')} "
                f"[{row.get('Applies To', '')}]"
            )
    return lines


def _reasoning_lines(resolved):
    """F6: the doctype's own anti-pattern tokens (with severity) and Doc Conditions."""
    row = _first(resolved, "doc-reasoning")
    if not row:
        return []
    lines = []
    tokens = _split(row.get("Anti-Pattern Tokens", ""))
    if tokens:
        lines.append(f"- anti-patterns ({row.get('Severity', '')}): " + "; ".join(tokens))
    if row.get("Doc Conditions", ""):
        lines.append("- conditional constraints (apply the named constraint set only when the "
                     "condition holds): " + row["Doc Conditions"].replace("=", " -> "))
    return lines


def _render_lines(resolved):
    """F4: per-format font rule for this doctype's render targets."""
    rows = resolved.get("render-targets", [])
    if not rows:
        return []
    parts = sorted({f"{r.get('Format', '')} = {r.get('Font Rule', '')}" for r in rows})
    return ["- font rule by output format: " + "; ".join(parts)]


def _doctype_section(doc_key, doctype_row, resolved, tables_spec):
    lines = [f"### {doctype_row.get('Display Name', '')} (`{doc_key}`)", ""]
    keywords = _split(doctype_row.get("Keywords", ""), ",")
    if keywords:
        lines.append(f"- trigger keywords: {', '.join(keywords[:10])}")
    lines.append(f"- language: {doctype_row.get('Default Language', 'en')}")
    lines.append("")
    lines.append(f"#### {doc_key} -- page / type / colour / style")
    lines.append("")
    lines.extend(_page_format_lines(_first(resolved, "page-formats")))
    lines.extend(_typeface_lines(_first(resolved, "typefaces"), resolved.get("type-scales", [])))
    lines.extend(_palette_lines(_first(resolved, "palettes")))
    lines.extend(_style_lines(_first(resolved, "doc-styles")))
    lines.extend(_render_lines(resolved))
    lines.append("")
    lines.append(f"#### {doc_key} -- structure / constraints")
    lines.append("")
    structure_row = _first(resolved, "structures")
    section_order = _split(structure_row.get("Section Order", "")) if structure_row else []
    lines.extend(_section_order_lines(section_order, resolved.get("headings", [])))
    if structure_row:
        extra = [f"{label}: {structure_row.get(col, '')}" for label, col in
                 (("caption position", "Caption Position"), ("cross-refs", "Cross-Ref Style"))
                 if structure_row.get(col, "")]
        if extra:
            lines.append("- " + "; ".join(extra))
    lines.extend(_cv_region_lines(resolved))
    lines.extend(_reasoning_lines(resolved))
    lines.extend(_constraints_lines(resolved, tables_spec))
    lines.append("")
    return lines


def _provenance_line(provenance_rows, table_name, row_key):
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
    metric, value = row.get("Ranking Metric", ""), row.get("Rank Value", "")
    if metric and value:
        return f"{source} ({metric}: {value})"
    if metric:
        return f"{source} ({metric})"
    return source


def _designs_table(family, ctx):
    all_designs = ctx["all_rows"].get("designs", [])
    family_designs = sorted(
        (r for r in all_designs if r.get("Family", "") == family),
        key=lambda r: int(r.get("Rank", "0") or 0),
    )
    if not family_designs:
        return []
    doc_reasoning_by_key = ctx["rows_by_key"].get("doc-reasoning", {})
    provenance_rows = ctx["all_rows"].get("provenance", [])
    lines = [f"### Designs (ranked) -- family: {family}", "",
             "| Rank | Design (key) | Evidence | Best for | Style / Palette / Typeface | Provenance |",
             "|---|---|---|---|---|---|"]
    for row in family_designs:
        dr = doc_reasoning_by_key.get(row.get("Reasoning Key", ""), {})
        style_palette_typeface = (
            f"{dr.get('Style Key', '') or NOT_PRESENT} / "
            f"{dr.get('Palette Key', '') or NOT_PRESENT} / "
            f"{dr.get('Typeface Key', '') or NOT_PRESENT}"
        )
        evidence_line = _provenance_line(provenance_rows, "designs", row.get("design_key", ""))
        best_for = row.get("Best For", "").replace("|", "/")
        lines.append(
            f"| {row.get('Rank', '')} | {row.get('Display Name', '')} "
            f"(`{row.get('design_key', '')}`) | {row.get('Evidence Class', '')} | {best_for} | "
            f"{style_palette_typeface} | {evidence_line} |"
        )
    lines.append("")
    return lines


def _grand_library_palettes(ctx):
    rows = [r for r in ctx["all_rows"].get("palettes", []) if r.get("Brand Scope", "") == "generic"]
    provenance_rows = ctx["all_rows"].get("provenance", [])
    lines = ["### Palettes (generic, hex by role)", ""]
    for row in sorted(rows, key=lambda r: r.get("palette_key", "")):
        roles = ["Primary", "On Primary", "Secondary", "On Secondary", "Accent", "On Accent",
                 "Background", "Foreground", "Muted", "On Muted"]
        hexes = ", ".join(f"{r}={row.get(r, '')}" for r in roles if row.get(r, ""))
        evidence = _provenance_line(provenance_rows, "palettes", row.get("palette_key", ""))
        lines.append(f"- **{row.get('Display Name', '')}** (`{row.get('palette_key', '')}`): "
                     f"{hexes}; rule hair/strong/brand: {row.get('Rule Hair', '')}/"
                     f"{row.get('Rule Strong', '')}/{row.get('Rule Brand', '') or NOT_PRESENT}; "
                     f"{_palette_roles(row)} -- {evidence}")
    lines.append("")
    return lines


def _grand_library_typefaces(ctx):
    rows = [r for r in ctx["all_rows"].get("typefaces", []) if r.get("Brand Scope", "") == "generic"]
    provenance_rows = ctx["all_rows"].get("provenance", [])
    lines = ["### Typeface pairings (generic)", ""]
    for row in sorted(rows, key=lambda r: r.get("typeface_key", "")):
        heading, body = row.get("Heading Family", ""), row.get("Body Family", "")
        fallback = row.get("Safe Stack Fallback", "")
        body_fallback = row.get("Safe Stack Body Fallback", "") or fallback
        licence = row.get("Embedding Licence", "")
        evidence = _provenance_line(provenance_rows, "typefaces", row.get("typeface_key", ""))
        lines.append(
            f"- **{row.get('Display Name', '')}** (`{row.get('typeface_key', '')}`): "
            f"heading {heading} / body {body} (fallback {fallback} / {body_fallback}); "
            f"licence {licence}; tabular figures: {row.get('Has Tabular Figures', '') or NOT_PRESENT}; "
            f"type scale to use with it: {row.get('Scale Key', '') or NOT_PRESENT} -- {evidence}"
        )
    lines.append("")
    return lines


def _grand_library_type_scales(ctx):
    rows = ctx["all_rows"].get("type-scales", [])
    provenance_rows = ctx["all_rows"].get("provenance", [])
    groups = {}
    order = []
    for row in rows:
        key = row.get("scale_key", "")
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(row)
    role_order = ["h1", "h2", "h3", "lead", "body", "body-dense", "caption", "label", "legal"]
    lines = ["### Type scales (generic, grouped by scale_key)", ""]
    for key in sorted(order):
        member_rows = groups[key]
        medium = member_rows[0].get("Medium", "") if member_rows else ""
        by_role = {r.get("Role", ""): r for r in member_rows}
        parts = [f"{role} {by_role[role].get('Size pt', '')}pt/{by_role[role].get('Leading Ratio', '')}"
                 for role in role_order if role in by_role]
        row_key_for_prov = member_rows[0].get("scale_row_key", "") if member_rows else ""
        evidence = _provenance_line(provenance_rows, "type-scales", row_key_for_prov)
        lines.append(f"- **{key}** ({medium}): " + ", ".join(parts) + f" -- {evidence}")
    lines.append("")
    return lines


def _grand_library_doc_styles(ctx):
    """I2: a design's Style Key must be resolvable inside the pack."""
    rows = [r for r in ctx["all_rows"].get("doc-styles", []) if r.get("Brand Scope", "") == "generic"]
    lines = ["### Doc styles (generic; a design's Style Key points here)", ""]
    for row in sorted(rows, key=lambda r: r.get("style_key", "")):
        lines.extend(_style_lines(row))
    lines.append("")
    return lines


def _grand_library_output_formats(ctx):
    """F4: font rule per output format, and the metric-identical font substitutes."""
    targets = ctx["all_rows"].get("render-targets", [])
    rules = {}
    for r in targets:
        rules.setdefault(r.get("Format", ""), set()).add(r.get("Font Rule", ""))
    lines = ["### Font rule by output format", "",
             "`safe-stack` = name the design's safe-stack fallback fonts (the design's own font "
             "may not be installed on the reader's machine); `embed` = the design's own fonts "
             "may be embedded; `inline-webfont` = webfont in the HTML.", ""]
    for fmt in sorted(rules):
        lines.append(f"- {fmt}: {' / '.join(sorted(x for x in rules[fmt] if x))}")
    lines += ["", "### Font substitutes (metric-identical replacements when a proprietary font is "
              "not installed)", ""]
    for r in sorted(ctx["all_rows"].get("font-substitutes", []), key=lambda r: r.get("substitute_key", "")):
        lines.append(f"- {r.get('proprietary_family', '')} -> {r.get('Substitute Family', '')} "
                     f"({r.get('Licence', '')}; metric identical: {r.get('Metric Identical', '')}; "
                     f"weights: {r.get('Weights Covered', '')})")
    lines.append("")
    return lines


def _anti_slop_checklist(ctx):
    """Built only from shipped data (data/base/constraints.csv's slop-mechanical
    Set Key, plus doc-reasoning.csv's Anti-Pattern Tokens) -- short item names, not
    research prose."""
    lines = ["## Anti-slop checklist", "", "Mechanical checks (data/base/constraints.csv, "
             "Set Key `slop-mechanical`):", ""]
    constraint_rows = [r for r in ctx["all_rows"].get("constraints", [])
                        if r.get("Set Key", "") == "slop-mechanical"]
    grouped = {}
    for row in constraint_rows:
        check_key = (row.get("Check", ""), row.get("Parameter", ""), row.get("Threshold", ""),
                     row.get("Severity", ""))
        grouped.setdefault(check_key, []).append(row.get("Applies To", ""))
    for (check, parameter, threshold, severity) in sorted(grouped):
        applies_to = ", ".join(sorted(set(grouped[(check, parameter, threshold, severity)])))
        limit = f" = {threshold}" if threshold else ""
        lines.append(f"- {check} ({parameter}{limit}) -- {severity} -- applies to: {applies_to}")
    lines.append("")

    # G2: severity belongs to the (token, doc_category) pair, never folded across categories
    per_token = {}
    for row in ctx["all_rows"].get("doc-reasoning", []):
        for token in _split(row.get("Anti-Pattern Tokens", "")):
            per_token.setdefault(token, {}).setdefault(row.get("Severity", ""), []).append(
                row.get("doc_category", ""))
    lines.append("Anti-pattern tokens (data/base/doc-reasoning.csv). A token is forbidden ONLY "
                 "in the doc categories listed against it, at that severity -- each doctype's "
                 "own `anti-patterns` line names its category's tokens:")
    lines.append("")
    for token in sorted(per_token):
        sev = "; ".join(f"{sv}: {', '.join(sorted(cats))}" for sv, cats in sorted(per_token[token].items()))
        lines.append(f"- `{token}` -- {sev}")
    lines.append("")
    return lines


def build_ddi_library_md(ctx):
    lines = ["# DDI Library -- portable knowledge pack", "",
              "Generated by `research/build-portable.py` from `data/base/*.csv` -- do not "
              "hand-edit; the next regeneration will discard the edit. One block per "
              "document family (manifest `doctypes.Family` enum order), each doctype's "
              "fully resolved page format, typography, palette, style, section order and "
              "constraints, followed by that family's ranked designs. The grand library "
              "(all generic palettes/typefaces/type-scales, for building a brand kit) and "
              "an anti-slop checklist follow.", ""]

    doctypes_by_family = {}
    for row in ctx["all_rows"]["doctypes"]:
        doctypes_by_family.setdefault(row.get("Family", ""), []).append(row)

    for family in ctx["families"]:
        family_doctypes = sorted(doctypes_by_family.get(family, []), key=lambda r: r.get("doc_key", ""))
        if not family_doctypes:
            continue
        lines.append(f"## Family: {family}")
        lines.append("")
        for row in family_doctypes:
            doc_key = row.get("doc_key", "")
            resolved = ctx["resolved_by_doctype"][doc_key]
            lines.extend(_doctype_section(doc_key, row, resolved, ctx["tables_spec"]))
        lines.extend(_designs_table(family, ctx))

    lines.append("## Grand library")
    lines.append("")
    lines.extend(_grand_library_palettes(ctx))
    lines.extend(_grand_library_typefaces(ctx))
    lines.extend(_grand_library_type_scales(ctx))
    lines.extend(_grand_library_doc_styles(ctx))
    lines.extend(_grand_library_output_formats(ctx))
    lines.extend(_anti_slop_checklist(ctx))

    return "\n".join(lines).rstrip("\n") + "\n"


# =============================================================================
# AGENTS.md
# =============================================================================

TRIGGERS_PER_FAMILY = 6
TRIGGER_MAX_LEN = 24


def _family_triggers(ctx):
    """{family: [keyword, ...]} read off shipped doctypes.Keywords. Round-robin: one
    keyword per doctype in turn (doctypes sorted by key, each doctype's own keyword
    order), so no single doctype fills the list (research/87 I1); over-long phrases are
    skipped and the family's own bare noun is always present."""
    doctypes_by_family = {}
    for row in ctx["all_rows"]["doctypes"]:
        doctypes_by_family.setdefault(row.get("Family", ""), []).append(row)
    out = {}
    for family in ctx["families"]:
        lists = [[k for k in _split(r.get("Keywords", ""), ",") if len(k) <= TRIGGER_MAX_LEN]
                 for r in sorted(doctypes_by_family.get(family, []), key=lambda r: r.get("doc_key", ""))]
        pooled = []
        for i in range(max((len(l) for l in lists), default=0)):
            pooled.extend(l[i] for l in lists if i < len(l))
        words = _dedup_keep_order(pooled)[:TRIGGERS_PER_FAMILY]
        noun = family.replace("-", " ")
        if lists and noun not in words and family not in words:
            words = [noun] + words[:TRIGGERS_PER_FAMILY - 1]
        out[family] = words
    return out


def build_agents_md(ctx):
    triggers = _family_triggers(ctx)
    family_lines = []
    for family in ctx["families"]:
        words = triggers.get(family, [])
        if not words:
            continue
        family_lines.append(f"- **{family}** -- {', '.join(words)}")

    text = f"""# AGENTS.md -- Document Design Intelligence (portable)

Operating instructions for ANY AI agent producing a print/office document (CV,
letter, memo, form, brochure, flyer, poster, report, whitepaper, proposal, quote,
invoice, slide deck, one-pager, infographic), with or without code execution.
Read this file, then use `DDI-LIBRARY.md` for the exact values it references.

## 1. Identify the family and doctype

Match the request to a family by intent (e.g. "Lebenslauf", "note interne"):

{chr(10).join(family_lines)}

Open `DDI-LIBRARY.md` `## Family: <family>` and pick the doctype whose keywords
and region/language fit (family `cv`: `cv-us`, `cv-uk`, `cv-dach`, ...). CV with
no country stated: ask once for the target country, or use `cv-generic` and say
so. Write in the user's language; a doctype's `language:` is only a default.

## 2. Pick a design

The default design is the family design whose Style/Palette/Typeface equal the
doctype's own. Use it UNLESS the user states a style, tone or industry
("editorial", "for a design portfolio"): then list up to 3 designs from the
family's "Designs (ranked)" table whose Best-for fits their wording (fewer if
the family has fewer) and ask. An override replaces Style/Palette/Typeface with
the design's: look them up under `## Grand library` (Doc styles, Palettes,
Typeface pairings) and use the typeface's own type scale. Page format, section
order and constraints stay the doctype's.

## 3. Apply EXACT values

Copy verbatim from the doctype block (and chosen design): page format (trim,
margins, bleed, print geometry: panels, DPI, folio), fonts, type scale, palette
hexes, the doc style's rules/tables/emphasis/checklist, section order with
headings, the doctype's anti-patterns and constraints WITH their limits.
- Fonts: obey the block's `font rule by output format`: `safe-stack` (docx)
  means name the fallback fonts, not the design's own; `embed` may use the
  design's fonts.
- Colour: text only in text-safe roles; fill-only roles are fills, never text.
- Missing role size (e.g. no h1): reuse the nearest listed role with weight
  emphasis; never create a size.
- CV: the regional variant for the user's country and seniority band (early =
  under ~3 years or a recent graduate) sets section order and limits over the
  structure order. Photo only if the variant says `customary` AND the user
  supplies one; ATS-strict target: never.
- `conditional constraints` apply only when their condition holds (e.g.
  professional-print only if going to a print shop).

## 4. Never invent

No font, colour or size outside the doctype block or the chosen design's
resolved values. Add no layout or decoration the doctype's own anti-patterns,
style and checklist forbid; an anti-pattern listed for another category does
not bind this one.

## 5. Check before returning

Check the document against its doctype's `anti-patterns` and `key constraints`
and the `## Anti-slop checklist`. `fail` = fix before delivering; `warn` = flag
it. Checks you cannot verify without tools (embedded fonts, PDF/X, DPI): list
them as "unverified", never as passed.

## 6. Delivering without code execution

Never claim to have produced a .docx/.pptx/.pdf you did not create. Deliver
either (1) one self-contained HTML file (CSS `@page` size and margins, font stack
with fallback, exact hex and pt values) to print or save as PDF, or (2) the
content in section order plus an exact style sheet (named styles: font, size,
leading, colour per role; page setup and margins) to apply in Word/PowerPoint.
With code: install the skill ZIP (see `INSTALL.md`) and run `python3
scripts/ddi.py resolve --query "<request>" --json`, then `ddi.py handoff`, render,
`ddi.py preflight` -- same data, plus live search and a mechanical gate.

## 7. Brand kit from the grand library (no code)

Interview first (field, three tone adjectives, colours/logo, families, languages, formats).
Pick ONE palette whose tone fits (never mix roles across palettes); if the user has a brand
colour, make it the single accent and take the other roles from one neutral palette, keeping
text in text-safe roles at >= 4.5:1. Pick ONE typeface pairing (max 2 families) with its own
type scale per medium (print/projection/screen). For every family the brand needs choose a
design from that family's table (rank 1 unless Best-for fits the tone). Then write the
user's `brand.md` (slug, palette hexes, typeface names, doctypes, one design per family,
scales). Invent no hex, family or size outside the tables you used. Procedure with commands:
`references/brand-kit-builder.md` in the skill.
"""
    return text


# =============================================================================
# INSTALL.md
# =============================================================================

INSTALL_MD = """# Installing the Document Design Intelligence pack

Two ways to use this project's design rules, depending on whether your
platform can execute code.

## Claude.ai

Skills **require code execution** to be enabled (individual plans: Settings >
Capabilities). With it on, upload the `document-design-intelligence` skill ZIP
from this project's GitHub Releases as a custom skill (Customize > Skills > +
> Create skill > upload the ZIP). Claude then follows `SKILL.md` and runs
`scripts/ddi.py` itself. Uploading the ZIP to a Project's files does NOT
install a skill. With code execution off, use this portable pack instead: paste
`AGENTS.md` into the Project's instructions and add `DDI-LIBRARY.md` as
Project knowledge.

## Claude Code

Copy (or symlink) `skill/document-design-intelligence/` into your skills
directory (see Claude Code's own skill-discovery docs for the exact path on
your platform). `SKILL.md` activates the same way any other skill does.

## ChatGPT

- **Custom GPT**: paste this pack's `AGENTS.md` into the GPT's Instructions
  field (limit 8,000 characters; `AGENTS.md` is under it), and upload
  `DDI-LIBRARY.md` as Knowledge. Unless you enable Code Interpreter & Data
  Analysis in the GPT's Capabilities it cannot run code, so it follows
  `AGENTS.md`'s instructions and reads exact values out of `DDI-LIBRARY.md`
  (Knowledge is retrieved in chunks, not read whole -- each block is headed
  with its doctype key for that reason).
- **ChatGPT Project**: add `AGENTS.md` and `DDI-LIBRARY.md` as project files
  and reference them in the project's instructions.
- **Code Interpreter (Advanced Data Analysis)**: upload the skill ZIP instead
  and run `python3 scripts/ddi.py ...` directly -- this gets you the live
  per-request search and the mechanical `preflight` gate, which the static
  pack cannot run for you.

ChatGPT usage of this pack is **untested by this project's maintainers** --
the file format (plain markdown instructions + a markdown knowledge file) is
standard for Custom GPTs and Projects, but no live run against ChatGPT has
been recorded here.

## Grok

Grok Projects (instructions + files) could not be verified against xAI's own
documentation, so treat this as **unverified and untested**: add `AGENTS.md`'s
contents to the project's instructions and upload `DDI-LIBRARY.md` as a project
file. Fallback: paste `AGENTS.md` into Settings > Customize Grok and attach
`DDI-LIBRARY.md` in each chat.

## Gemini Gems

Create a Gem, paste `AGENTS.md` into its instructions, and attach
`DDI-LIBRARY.md` as a knowledge file. **Untested by this project's
maintainers.**

## Any other agent (the AGENTS.md convention)

Any assistant or tool that reads a repo-root `AGENTS.md` for operating
instructions can point it at this pack's `AGENTS.md` directly, with
`DDI-LIBRARY.md` alongside it as a reference file. This is the generic,
platform-agnostic fallback the other sections above specialise.
"""


def build_install_md():
    return INSTALL_MD


# =============================================================================
# driver
# =============================================================================

def generate_all(data_dir=None):
    """{filename: text} for every file this generator writes -- used by
    both `main()` (writes to disk) and the sync test (regenerates in
    memory and compares)."""
    ctx = load_context(data_dir)
    return {
        "AGENTS.md": build_agents_md(ctx),
        "DDI-LIBRARY.md": build_ddi_library_md(ctx),
        "INSTALL.md": build_install_md(),
    }


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    data_dir = Path(argv[0]) if argv else None

    files = generate_all(data_dir)

    agents_len = len(files["AGENTS.md"])
    if agents_len >= AGENTS_MD_CHAR_LIMIT:
        print(f"AGENTS.md is {agents_len} chars -- must be < {AGENTS_MD_CHAR_LIMIT}")
        return 1

    PORTABLE_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        path = PORTABLE_DIR / name
        path.write_bytes(text.encode("utf-8"))
        print(f"wrote {path} -- {len(text)} chars, {len(text.encode('utf-8'))} bytes")

    print(f"AGENTS.md: {agents_len} chars (limit {AGENTS_MD_CHAR_LIMIT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
