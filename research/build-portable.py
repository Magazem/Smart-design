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
        return [f"  page format: {NOT_PRESENT}"]
    w, h = row.get("Trim W mm", ""), row.get("Trim H mm", "")
    top = row.get("Margin Top mm", "")
    bottom = row.get("Margin Bottom mm", "")
    inside = row.get("Margin Inside mm", "")
    outside = row.get("Margin Outside mm", "")
    bleed = row.get("Bleed mm", "")
    lines = [
        f"  page format: {row.get('Display Name', '')} ({row.get('page_format_key', '')})",
        f"    trim: {w}mm x {h}mm; margins top/bottom/inside/outside: "
        f"{top}/{bottom}/{inside}/{outside}mm; bleed: {bleed or '0'}mm",
    ]
    columns = row.get("Columns", "")
    measure = row.get("Measure mm", "")
    if columns or measure:
        lines.append(f"    columns: {columns or NOT_PRESENT}; measure: {measure or NOT_PRESENT}mm")
    return lines


def _typeface_lines(typeface_row, scale_rows):
    if not typeface_row:
        return [f"  typography: {NOT_PRESENT}"]
    heading = typeface_row.get("Heading Family", "")
    body = typeface_row.get("Body Family", "")
    heading_fb = typeface_row.get("Safe Stack Fallback", "")
    body_fb = typeface_row.get("Safe Stack Body Fallback", "") or heading_fb
    licence = typeface_row.get("Embedding Licence", "")
    lines = [
        f"  typography: {typeface_row.get('Display Name', '')} "
        f"({typeface_row.get('typeface_key', '')})",
        f"    heading: {heading}  (safe-stack fallback: {heading_fb or NOT_PRESENT})",
        f"    body: {body}  (safe-stack fallback: {body_fb or NOT_PRESENT})",
        f"    embedding licence: {licence or NOT_PRESENT}",
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
            lines.append(f"    type scale ({medium}): " + ", ".join(parts))
    return lines


def _palette_lines(row):
    if not row:
        return [f"  palette: {NOT_PRESENT}"]
    roles = ["Primary", "On Primary", "Secondary", "On Secondary", "Accent", "On Accent",
              "Background", "Foreground", "Muted", "On Muted"]
    hexes = ", ".join(f"{r}={row.get(r, '') or NOT_PRESENT}" for r in roles if row.get(r, ""))
    rules = (f"rule hair/strong/brand: {row.get('Rule Hair', '')}/"
             f"{row.get('Rule Strong', '')}/{row.get('Rule Brand', '') or NOT_PRESENT}")
    return [
        f"  palette: {row.get('Display Name', '')} ({row.get('palette_key', '')})",
        f"    {hexes}",
        f"    {rules}",
    ]


def _style_lines(row):
    if not row:
        return [f"  style: {NOT_PRESENT}"]
    lines = [
        f"  style: {row.get('Display Name', '')} ({row.get('style_key', '')})",
        f"    rules: hair {row.get('Rule Hair pt', '')}pt / strong {row.get('Rule Strong pt', '')}pt "
        f"/ brand {row.get('Rule Brand pt', '') or '0'}pt; corner radius: "
        f"{row.get('Corner Radius mm', '') or '0'}mm",
        f"    table rules: {row.get('Table Rules', '')}; table fills: {row.get('Table Fills', '')}; "
        f"emphasis: {row.get('Emphasis Mechanism', '')}; field style: {row.get('Field Style', '')}",
    ]
    checklist = _split(row.get("Checklist", ""))
    if checklist:
        lines.append("    checklist: " + "; ".join(checklist))
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
        return [f"  {label}: {NOT_PRESENT}"]
    index = _primary_headings_index(headings_rows)
    lines = [f"  {label} (headings en / fr / de where authored):"]
    for section in section_order:
        per_lang = []
        for lang in ("en", "fr", "de"):
            text = index.get((section, lang))
            if text:
                per_lang.append(f"{lang}: {text}")
        wording = " / ".join(per_lang) if per_lang else NOT_PRESENT
        lines.append(f"    {section} -- {wording}")
    return lines


def _cv_region_lines(resolved):
    rows = resolved.get("cv-regions", [])
    if not rows:
        return []
    lines = ["  regional CV variants (Seniority Band; Photo/DoB/Marital/Visa field norms):"]
    for row in sorted(rows, key=lambda r: (r.get("region_key", ""), r.get("Seniority Band", ""))):
        lines.append(
            f"    [{row.get('cv_region_key', '')}] band={row.get('Seniority Band', '')}, "
            f"max pages={row.get('Max Pages', '')}, photo={row.get('Photo', '')}, "
            f"date of birth={row.get('Date of Birth', '')}, marital status={row.get('Marital Status', '')}, "
            f"visa status={row.get('Visa Status', '')}, format={row.get('Format', '')}"
        )
        section_order = _split(row.get("Section Order", ""))
        if section_order:
            lines.append(f"      section order: {'; '.join(section_order)}")
    return lines


def _constraints_lines(resolved):
    rows = resolved.get("constraints", [])
    if not rows:
        return [f"  key constraints: {NOT_PRESENT}"]
    by_set = {}
    for row in rows:
        by_set.setdefault(row.get("Set Key", ""), []).append(row)
    lines = ["  key constraints (Set Key: Check -- severity):"]
    for set_key in sorted(by_set):
        for row in by_set[set_key]:
            lines.append(
                f"    [{set_key}] {row.get('Check', '')} "
                f"({row.get('Parameter', '') or 'no parameter'}) -- {row.get('Severity', '')}"
            )
    return lines


def _doctype_section(doc_key, doctype_row, resolved):
    lines = [f"### {doctype_row.get('Display Name', '')} (`{doc_key}`)", ""]
    keywords = _split(doctype_row.get("Keywords", ""), ",")
    if keywords:
        lines.append(f"  trigger keywords: {', '.join(keywords[:10])}")
    lines.append(f"  language: {doctype_row.get('Default Language', 'en')}")
    lines.extend(_page_format_lines(_first(resolved, "page-formats")))
    lines.extend(_typeface_lines(_first(resolved, "typefaces"), resolved.get("type-scales", [])))
    lines.extend(_palette_lines(_first(resolved, "palettes")))
    lines.extend(_style_lines(_first(resolved, "doc-styles")))
    structure_row = _first(resolved, "structures")
    section_order = _split(structure_row.get("Section Order", "")) if structure_row else []
    lines.extend(_section_order_lines(section_order, resolved.get("headings", [])))
    lines.extend(_cv_region_lines(resolved))
    lines.extend(_constraints_lines(resolved))
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
    source = row.get("Source Name", "") or "(unnamed source)"
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
    lines = ["### Designs (ranked)", "",
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
        roles = ["Primary", "Secondary", "Accent", "Background", "Foreground", "Muted"]
        hexes = ", ".join(f"{r}={row.get(r, '')}" for r in roles if row.get(r, ""))
        evidence = _provenance_line(provenance_rows, "palettes", row.get("palette_key", ""))
        lines.append(f"- **{row.get('Display Name', '')}** (`{row.get('palette_key', '')}`): "
                     f"{hexes} -- {evidence}")
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
            f"licence {licence}; scale {row.get('Scale Key', '') or NOT_PRESENT} -- {evidence}"
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


def _anti_slop_checklist(ctx):
    """Built only from shipped data (data/base/constraints.csv's slop-mechanical
    Set Key, plus doc-reasoning.csv's Anti-Pattern Tokens) -- short item names, not
    research prose, per research/80-v05-plan.md section 5 / research/68-slop-
    patterns.md's own note that research prose stays out of shipped tables."""
    lines = ["## Anti-slop checklist", "", "Mechanical checks (data/base/constraints.csv, "
             "Set Key `slop-mechanical`):", ""]
    constraint_rows = [r for r in ctx["all_rows"].get("constraints", [])
                        if r.get("Set Key", "") == "slop-mechanical"]
    # Several rows repeat the same Check/Parameter/Severity once per format
    # (docx, pptx, ...) via a distinct `constraint_key` -- grouped here by
    # what the check actually verifies, with the formats/doctypes it Applies
    # To folded in, instead of printing the same line once per format.
    grouped = {}
    for row in constraint_rows:
        check_key = (row.get("Check", ""), row.get("Parameter", ""), row.get("Severity", ""))
        grouped.setdefault(check_key, []).append(row.get("Applies To", ""))
    for (check, parameter, severity) in sorted(grouped):
        applies_to = ", ".join(sorted(set(grouped[(check, parameter, severity)])))
        lines.append(f"- {check} ({parameter}) -- {severity} -- applies to: {applies_to}")
    lines.append("")

    token_severity = {}
    for row in ctx["all_rows"].get("doc-reasoning", []):
        severity = row.get("Severity", "")
        for token in _split(row.get("Anti-Pattern Tokens", "")):
            if token_severity.get(token) != "fail":
                token_severity[token] = severity if severity == "fail" else token_severity.get(token, severity)
    lines.append("Anti-pattern tokens (data/base/doc-reasoning.csv, worst severity across "
                 "every doc_category that lists the token):")
    lines.append("")
    for token in sorted(token_severity):
        lines.append(f"- `{token}` -- {token_severity[token]}")
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
            lines.extend(_doctype_section(doc_key, row, resolved))
        lines.extend(_designs_table(family, ctx))

    lines.append("## Grand library")
    lines.append("")
    lines.extend(_grand_library_palettes(ctx))
    lines.extend(_grand_library_typefaces(ctx))
    lines.extend(_grand_library_type_scales(ctx))
    lines.extend(_anti_slop_checklist(ctx))

    return "\n".join(lines).rstrip("\n") + "\n"


# =============================================================================
# AGENTS.md
# =============================================================================

def _family_triggers(ctx):
    """{family: [keyword, ...]} -- deduplicated Keywords tokens pooled across
    every doctype in that family, in first-seen order, capped so the whole
    table stays inside AGENTS.md's character budget. Read off shipped data
    (doctypes.Keywords) rather than hand-authored, so this cannot drift from
    SKILL.md's own trigger words."""
    doctypes_by_family = {}
    for row in ctx["all_rows"]["doctypes"]:
        doctypes_by_family.setdefault(row.get("Family", ""), []).append(row)
    out = {}
    for family in ctx["families"]:
        pooled = []
        for row in sorted(doctypes_by_family.get(family, []), key=lambda r: r.get("doc_key", "")):
            pooled.extend(_split(row.get("Keywords", ""), ","))
        out[family] = _dedup_keep_order(pooled)[:6]
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
cover letter, letter, memo, form, brochure, flyer, poster, report, whitepaper,
proposal, quote, invoice, slide deck, one-pager, infographic) -- Claude,
ChatGPT, Grok, Gemini, or any other assistant, with or without code execution.
Read this file, then open `DDI-LIBRARY.md` for the exact values it references.

## 1. Identify the family and doctype

Match the user's request against a family below by its trigger words (the
request need not use these exact words -- match on intent, e.g. "Lebenslauf"
or "note interne" both count):

{chr(10).join(family_lines)}

Once you have a family, open `DDI-LIBRARY.md`'s `## Family: <family>` section
and pick the specific doctype whose trigger keywords and region/language best
match the request (e.g. family `cv` has separate doctypes for `cv-us`,
`cv-uk`, `cv-dach`, `cv-eu-europass`, `cv-academic`, ...).

## 2. Pick a design

Every doctype has a default design (the first one in that family's "Designs
(ranked)" table whose Style/Palette/Typeface match the doctype's own resolved
values in `DDI-LIBRARY.md`). Use the default UNLESS the user states a style,
tone, or industry preference ("editorial", "formal DACH-style", "for a design
portfolio") -- in that case, list the family's top 3 ranked designs (name,
evidence class, best for) and ask which one they want, then apply THAT
design's own Style/Palette/Typeface keys instead of the default.

## 3. Apply EXACT values from the pack

For the chosen doctype (and design, if overridden), copy from `DDI-LIBRARY.md`
verbatim:
  - page format: trim size + all four margins + bleed
  - fonts: heading and body family, with their safe-stack fallback if you
    cannot embed a font
  - type scale: size and leading per role (h1/h2/h3/lead/body/caption/label)
  - palette: hex value per role (primary/secondary/accent/background/
    foreground/muted) -- every pack palette already meets WCAG 4.5:1 text
    contrast on its own text-safe role pairs
  - section order and headings, in the user's own language (en/fr/de) where
    authored; if a section has no wording in that language, use whichever
    language IS authored and say so
  - the doc style's rule weights, table rules/fills, emphasis mechanism, and
    its checklist items
  - the doctype's key constraints and their severity (fail = must fix before
    delivering; warn = flag it, deliver anyway)

## 4. Never invent

Never introduce a font, colour, or size that is not in the resolved doctype's
own block in `DDI-LIBRARY.md`. Never add multi-column layouts, text boxes,
icon-only skill bars, photos, gradients, emoji, or decorative borders unless
the doctype's own style/checklist explicitly allows them -- see the anti-slop
checklist below.

## 5. Anti-slop checklist (run before returning the document)

`DDI-LIBRARY.md`'s `## Anti-slop checklist` lists every mechanical check and
anti-pattern token this library ships. Before returning a document, check it
does not contain any `fail`-severity item; flag (do not silently ignore)
`warn`-severity items to the user. A resolved doctype's own key-constraints
list (in its `DDI-LIBRARY.md` block) may add doctype-specific fail items on
top of these.

## 6. Prefer code execution when it is available

If you can run python3, prefer the actual skill instead of this pack: fetch
the `document-design-intelligence` skill ZIP (see `INSTALL.md`) and run
`python3 scripts/ddi.py resolve --query "<request>" --json`, then
`ddi.py handoff --json <result> --format docx|pptx|pdf|png`, then render and
run `ddi.py preflight <file>` on the result. That path resolves the SAME data
this pack is generated from, with live per-request search and a mechanical
preflight gate this static pack cannot run for you.

## 7. Building a brand kit from the grand library

If the user wants their own brand's document instead of a generic one, and
you have no code execution (so `make_brand_kit.py` is not available), compose
one by hand from `DDI-LIBRARY.md`'s `## Grand library`:
  - **Palette**: pick one generic palette whose tone matches the brand (e.g.
    restrained/neutral vs. high-contrast/bold); every listed palette already
    satisfies >=4.5:1 text contrast on its text-safe role pairs, so picking
    ANY one keeps that guarantee -- do not hand-mix roles from two palettes.
  - **Typeface pairing**: pick one pairing; keep it to the pairing's own
    families (heading + body -- at most 2 families total; do not add a third
    "just for emphasis", per the anti-slop checklist's font-family-count
    rule).
  - **Type scale**: pick the scale grouped for the right medium (print /
    projection / screen) for the doctype's own artifact class.
  - Apply the picked palette/pairing/scale the same way step 3 above applies
    a doctype's own resolved values -- do not invent a hex, family, or size
    outside the two tables you picked from.
"""
    return text


# =============================================================================
# INSTALL.md
# =============================================================================

INSTALL_MD = """# Installing the Document Design Intelligence pack

Two ways to use this project's design rules, depending on whether your
platform can execute code.

## Claude.ai (no code execution needed, or with it)

Upload the `document-design-intelligence` skill ZIP from this project's
GitHub Releases as a custom skill (Settings -> Capabilities -> Skills, or a
Project's file upload for Projects). Claude then follows `SKILL.md` and runs
`scripts/ddi.py` itself -- no extra setup.

## Claude Code

Copy (or symlink) `skill/document-design-intelligence/` into your skills
directory (see Claude Code's own skill-discovery docs for the exact path on
your platform). `SKILL.md` activates the same way any other skill does.

## ChatGPT

- **Custom GPT**: paste this pack's `AGENTS.md` into the GPT's Instructions
  field, and upload `DDI-LIBRARY.md` as Knowledge. The GPT has no code
  execution by default, so it follows `AGENTS.md`'s step-by-step instructions
  and reads exact values out of `DDI-LIBRARY.md`.
- **ChatGPT Project**: add `AGENTS.md` and `DDI-LIBRARY.md` as project files;
  reference them in the project's custom instructions.
- **Code Interpreter (Advanced Data Analysis)**: upload the skill ZIP instead
  and run `python3 scripts/ddi.py ...` directly -- this gets you the live
  per-request search and the mechanical `preflight` gate, which the static
  pack cannot run for you.

ChatGPT usage of this pack is **untested by this project's maintainers** --
the file format (plain markdown instructions + a markdown knowledge file) is
standard for Custom GPTs and Projects, but no live run against ChatGPT has
been recorded here.

## Grok

Add `AGENTS.md`'s contents to a Grok Project's custom instructions, and
upload `DDI-LIBRARY.md` as a project knowledge file. **Untested by this
project's maintainers** -- verify the two-file split is honoured the way it
is described here before relying on it.

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
