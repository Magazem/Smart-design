#!/usr/bin/env python3
"""P6.5 scorer: implements research/87 section G's five falsifier clauses, deterministically.

    python3 research/p65/score.py --trial T1 --output run.md [--pack portable/DDI-LIBRARY.md]

Prints JSON: per-clause PASS/FAIL with the evidence, secondary counts, and `needs_human`
(clauses 2 and 5 are only heuristically checkable; section G says a human checks them).
A trial PASSES iff all five clauses pass. Stdlib only. Readings and their strictness are
documented in research/p65/README.md ("Interpretation").
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_PACK = Path(__file__).resolve().parent.parent.parent / "portable" / "DDI-LIBRARY.md"

#: expected doctype / family / heading language per pre-registered trial (research/87 section G)
TRIALS = {
    "T1": {"doctype": "cv-uk", "family": "cv", "language": "en"},
    "T2": {"doctype": "slide-deck-projection", "family": "deck", "language": "en"},
    "T3": {"doctype": "quote-devis", "family": "quote", "language": "fr"},
}

GENERIC_FONTS = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "inherit",
                 "initial", "unset", "ui-serif", "ui-sans-serif", "ui-monospace"}
DOC_START = "=== DOCUMENT ==="
STYLE_START = "=== STYLE SHEET ==="
DISCLOSE_RE = re.compile(r"omitted|omit\b|not provided|no content|left out|skipped|no information|"
                         r"not applicable|placeholder|left blank|did not (give|provide)|"
                         r"you (did not|didn't) (give|provide)|no [a-z ]{0,20}(given|provided)", re.I)
ASK_RE = re.compile(r"which (design|style)|would you like|do you want|please (choose|pick|tell)|"
                    r"choose (one|a design)|pick (one|a design)|options?:", re.I)
FILE_CLAIM_RE = re.compile(
    r"(i('| ha)ve|i've|here is|here's|attached|download|saved|created|generated|produced|exported)"
    r"[^.\n]{0,60}\.(docx|pptx|pdf)\b|\[[^\]]*\]\([^)]*\.(docx|pptx|pdf)\)|sandbox:", re.I)
CHECK_CLAIM_RE = re.compile(
    r"(preflight|validat\w*|checks?|checklist|constraints?|contrast|anti-slop)[^.\n]{0,40}"
    r"(passed|pass\b|ok\b|verified|all clear|satisfied)|all (checks|constraints) (pass|passed)", re.I)
UNVERIFIED_RE = re.compile(r"unverified|not verified|could not verify|cannot verify|can't verify|"
                           r"not able to (run|verify)|not checked", re.I)


# ----------------------------------------------------------------------------- pack parsing

def _blocks(pack):
    """{doc_key: block text} for every `### Name (`key`)` doctype block above the grand library."""
    head = pack.split("## Grand library")[0]
    out = {}
    for m in re.finditer(r"^### .*\(`([a-z0-9-]+)`\)\s*$", head, re.M):
        start = m.end()
        nxt = re.search(r"^(### |## )", head[start:], re.M)
        out[m.group(1)] = head[start: start + nxt.start()] if nxt else head[start:]
    return out


def _grand(pack):
    return pack.split("## Grand library", 1)[1] if "## Grand library" in pack else ""


def _hexes(text):
    return {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", text)}


def _pts(text):
    return {float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*pt\b", text)}


def _block_fonts(block):
    fonts = set()
    for m in re.finditer(r"^\s*- (?:heading|body): (.+?)\s+\(safe-stack fallback: (.+?)\)", block, re.M):
        fonts.update({m.group(1).strip().lower(), m.group(2).strip().lower()})
    return fonts


def _block_keys(block):
    def key(label):
        m = re.search(r"^- %s: .*\(([a-z0-9-]+)\)\s*$" % label, block, re.M)
        return m.group(1) if m else ""
    return key("style"), key("palette"), key("typography")


def _sections(block):
    """(headings, orders): headings {canonical: [texts in every language]}, orders [[canonical...]]
    -- the structure order plus every regional variant order the block lists."""
    headings, orders = {}, []
    m = re.search(r"^- section order[^\n]*\n((?:  - [^\n]*\n?)+)", block, re.M)
    if m:
        order = []
        for line in m.group(1).splitlines():
            mm = re.match(r"  - ([a-z0-9-]+) -- (.*)$", line)
            if not mm:
                continue
            order.append(mm.group(1))
            texts = [t.split(": ", 1)[1] for t in mm.group(2).split(" / ") if ": " in t]
            headings[mm.group(1)] = texts
        orders.append(order)
    for mm in re.finditer(r"^\s+- section order: (.+)$", block, re.M):
        orders.append([s.strip() for s in mm.group(1).split(";") if s.strip()])
    return headings, orders


def _designs(pack, family):
    """[{name, key, style, palette, typeface}] from the `### Designs (ranked) -- family: X` table."""
    m = re.search(r"^### Designs \(ranked\) -- family: %s\s*$" % re.escape(family), pack, re.M)
    if not m:
        return []
    rows = []
    for line in pack[m.end():].splitlines()[1:]:
        if line.startswith("###") or line.startswith("## "):
            break
        mm = re.match(r"\|\s*\d+\s*\|\s*(.+?) \(`([a-z0-9-]+)`\)\s*\|.*?\|\s*([a-z0-9-]+) / ([a-z0-9-]+) / "
                      r"([a-z0-9-]+)\s*\|", line)
        if mm:
            rows.append({"name": mm.group(1), "key": mm.group(2), "style": mm.group(3),
                         "palette": mm.group(4), "typeface": mm.group(5)})
    return rows


def _grand_line(grand, key):
    m = re.search(r"^- \*\*[^\n]*?\(`%s`\):[^\n]*$" % re.escape(key), grand, re.M)
    return m.group(0) if m else ""


def _design_values(grand, design):
    """{hexes, fonts, pts} the pack resolves for a design's Style/Palette/Typeface keys."""
    hexes, fonts, pts = set(), set(), set()
    hexes |= _hexes(_grand_line(grand, design["palette"]))
    tline = _grand_line(grand, design["typeface"])
    m = re.search(r"heading (.+?) / body (.+?) \(fallback (.+?) / (.+?)\)", tline)
    if m:
        fonts |= {g.strip().lower() for g in m.groups()}
    sm = re.search(r"type scale to use with it: ([a-z0-9-]+)", tline)
    if sm:
        m2 = re.search(r"^- \*\*%s\*\* \([a-z]+\): ([^\n]*)$" % re.escape(sm.group(1)), grand, re.M)
        if m2:
            pts |= _pts(m2.group(1))
    m3 = re.search(r"^- style: [^\n]*\(%s\)\n((?:  - [^\n]*\n)+)" % re.escape(design["style"]), grand, re.M)
    if m3:
        pts |= _pts(m3.group(1))
    return hexes, fonts, pts


def _all_known_fonts(pack):
    fonts = set()
    for m in re.finditer(r"heading (.+?) / body (.+?) \(fallback (.+?) / (.+?)\)", pack):
        fonts |= {g.strip().lower() for g in m.groups()}
    for m in re.finditer(r"^\s*- (?:heading|body): (.+?)\s+\(safe-stack fallback: (.+?)\)", pack, re.M):
        fonts |= {m.group(1).strip().lower(), m.group(2).strip().lower()}
    return {f for f in fonts if f and not f.startswith("(")}


# ----------------------------------------------------------------------------- output parsing

def split_output(text):
    """(document_part, whole). Markers are optional; without them the whole output is the
    document (the stricter reading: style-sheet headings then count as sections)."""
    if DOC_START in text:
        doc = text.split(DOC_START, 1)[1]
        doc = re.split(re.escape(STYLE_START) + r"|=== END DOCUMENT ===", doc)[0]
        return doc, text
    return text, text


def extract_headings(doc):
    """[(level, text)] from markdown `#` headings and HTML <h1>-<h6>."""
    found = []
    for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*#*\s*$", doc, re.M):
        found.append((m.start(), len(m.group(1)), m.group(2)))
    for m in re.finditer(r"<h([1-6])[^>]*>(.*?)</h\1>", doc, re.I | re.S):
        found.append((m.start(), int(m.group(1)), re.sub(r"<[^>]+>", "", m.group(2))))
    found.sort()
    return [(lvl, _norm(t)) for _, lvl, t in found]


def _norm(text):
    t = re.sub(r"[*_`]", "", text).strip().rstrip(":").strip()
    t = re.sub(r"^\d+[.)]\s+", "", t)
    return re.sub(r"\s+", " ", t).casefold()


def extract_fonts_declared(text):
    """Every font family the output declares: CSS `font-family:` lists and `Font: X` style lines."""
    declared = []
    for m in re.finditer(r"font-family\s*:\s*([^;}\n]+)", text, re.I):
        for f in m.group(1).split(","):
            f = f.strip().strip("'\"").strip()
            if f and f.lower() not in GENERIC_FONTS:
                declared.append(f)
    for m in re.finditer(r"(?i:\b(?:heading|body|display|title|text)?\s*(?:font|typeface|font family))\s*[:=]\s*"
                         r"\**([A-Z][A-Za-z0-9]*(?: [A-Z0-9][A-Za-z0-9]*){0,3})", text):
        declared.append(m.group(1).strip())
    return declared


# ----------------------------------------------------------------------------- scoring

def score(output, trial, pack):
    cfg = TRIALS[trial]
    blocks = _blocks(pack)
    block = blocks.get(cfg["doctype"], "")
    grand = _grand(pack)
    designs = _designs(pack, cfg["family"])
    doc, whole = split_output(output)
    low = output.casefold()

    # ---- which designs does the output name; is one an override of the doctype's own?
    named = [d for d in designs if d["key"] in low or d["name"].casefold() in low]
    style_k, palette_k, typeface_k = _block_keys(block)
    allowed_hex, allowed_pt = _hexes(block), _pts(block)
    allowed_fonts = _block_fonts(block)
    overrides = []
    for d in named:
        if (d["style"], d["palette"], d["typeface"]) != (style_k, palette_k, typeface_k):
            h, f, p = _design_values(grand, d)
            allowed_hex |= h
            allowed_fonts |= f
            allowed_pt |= p
            overrides.append(d["key"])

    result = {"trial": trial, "expected_doctype": cfg["doctype"], "clauses": {}, "secondary": {},
              "needs_human": []}

    # ---- clause 1: no out-of-pack font, hex or point size
    bad_hex = sorted(_hexes_all(whole) - allowed_hex)
    declared = extract_fonts_declared(whole)
    bad_fonts = sorted({f for f in declared if not any(f.lower().startswith(a) for a in allowed_fonts)})
    known = _all_known_fonts(pack)
    named_known = sorted(k for k in known if re.search(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(k), low)
                         and k not in allowed_fonts)
    bad_pts = sorted({float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*pt\b", whole)} - allowed_pt)
    bad_units = sorted(set(re.findall(r"font-size\s*:\s*[\d.]+\s*(px|em|rem|%|vw|vh)\b", whole, re.I)))
    c1 = not (bad_hex or bad_fonts or named_known or bad_pts or bad_units)
    result["clauses"]["1_out_of_pack_values"] = _clause(c1, {
        "hex_not_in_pack": bad_hex, "fonts_not_in_pack": bad_fonts,
        "pack_fonts_not_allowed_for_this_doctype": named_known, "pt_sizes_not_in_pack": bad_pts,
        "non_pt_font_sizes": bad_units, "design_overrides_applied": overrides})

    # ---- clause 2: a pack design is named, or the user is asked to choose among pack designs
    listed = [d["key"] for d in designs if d["key"] in low or d["name"].casefold() in low]
    asked = bool(ASK_RE.search(output)) and len(listed) >= 2
    c2 = bool(named) or asked
    result["clauses"]["2_named_design"] = _clause(c2, {"named": [d["key"] for d in named],
                                                       "asked_among_pack_designs": asked})
    result["needs_human"].append("2_named_design")

    # ---- clause 3: section order equals a pack order for the doctype
    headings, orders = _sections(block)
    c3, ev3 = _check_sections(doc, headings, orders, output)
    result["clauses"]["3_section_order"] = _clause(c3, ev3)

    # ---- clause 4: right doctype
    stated = re.findall(r"doctype[\s:=`*]+([a-z0-9-]+)", low)
    wrong = sorted({s for s in stated if s != cfg["doctype"] and s in blocks})
    present = cfg["doctype"] in low
    c4 = present and not wrong
    ev4 = {"expected_key_stated": present, "other_doctypes_stated": wrong}
    if trial == "T1":
        region = bool(re.search(r"\buk\b|united kingdom|region|country", low))
        c4 = c4 and region
        ev4["region_asked_or_disclosed"] = region
    result["clauses"]["4_doctype"] = _clause(c4, ev4)

    # ---- clause 5: no claimed file, no claimed passed check that could not have run
    file_claims = [m.group(0) for m in FILE_CLAIM_RE.finditer(output)]
    check_claims = [m.group(0) for m in CHECK_CLAIM_RE.finditer(output)]
    unverified = bool(UNVERIFIED_RE.search(output))
    c5 = not file_claims and not check_claims
    result["clauses"]["5_no_false_claims"] = _clause(c5, {
        "file_claims": file_claims, "check_pass_claims": check_claims, "mentions_unverified": unverified})
    result["needs_human"].append("5_no_false_claims")

    # ---- secondary counts (recorded, never decide PASS/FAIL)
    used_ok = sorted(_hexes_all(whole) & allowed_hex)
    result["secondary"] = {
        "out_of_pack_values": len(bad_hex) + len(bad_fonts) + len(named_known) + len(bad_pts) + len(bad_units),
        "in_pack_hexes_used": used_ok,
        "asked_or_disclosed": bool(asked or DISCLOSE_RE.search(output)),
    }
    if trial == "T1":
        result["secondary"]["cv_editorial_listed"] = "cv-editorial" in low
    if trial == "T2":
        result["secondary"]["deck_density_violations"] = _deck_density(doc)
    if trial == "T3":
        result["secondary"]["french_headings"] = ev3.get("matched_language_counts", {})

    result["pass"] = all(c["pass"] for c in result["clauses"].values())
    return result


def _hexes_all(text):
    out = set()
    for h in re.findall(r"#([0-9A-Fa-f]{3,8})\b", text):
        if len(h) == 6:
            out.add("#" + h.upper())
        elif len(h) == 3:
            out.add("#" + "".join(c * 2 for c in h).upper())
    return out


def _clause(ok, evidence):
    return {"pass": bool(ok), "result": "PASS" if ok else "FAIL", "evidence": evidence}


def _check_sections(doc, headings, orders, output):
    """Ordered-sequence check of the document's section headings against the pack orders."""
    lookup = {}
    for canon, texts in headings.items():
        for t in texts:
            lookup[_norm(t)] = canon
    langs = {"en": 0, "fr": 0, "de": 0}
    found = extract_headings(doc)
    if not found:
        return False, {"reason": "no headings in the document part"}
    matched_levels = [lvl for lvl, t in found if t in lookup]
    if not matched_levels:
        return False, {"reason": "no heading matches any pack section wording",
                       "headings": [t for _, t in found]}
    counts = {}
    for lvl in matched_levels:
        counts[lvl] = counts.get(lvl, 0) + 1
    section_level = min(l for l, n in counts.items() if n == max(counts.values()))
    sequence, extra = [], []
    for idx, (lvl, t) in enumerate(found):
        if lvl > section_level:
            continue                       # sub-items below the section level are content
        if t in lookup:
            if not sequence or sequence[-1] != lookup[t]:
                sequence.append(lookup[t])
        elif idx != 0:                     # the first heading is the document title / name
            extra.append(t)
    ev = {"section_level": section_level, "sequence": sequence, "extra_sections": extra}
    if extra:
        ev["reason"] = "section(s) not in the pack were added"
        return False, ev
    disclosed = bool(DISCLOSE_RE.search(output))
    best = None
    for order in orders:
        if any(s not in order for s in sequence):
            continue
        positions = [order.index(s) for s in sequence]
        if positions != sorted(positions) or len(set(positions)) != len(positions):
            continue
        missing = [s for s in order if s not in sequence]
        if not missing or disclosed:
            ev["matched_order"] = order
            ev["omitted_and_disclosed"] = missing
            return True, ev
        best = best or {"omitted_undisclosed": missing, "order": order}
    ev["reason"] = "sequence is not one pack order (or omissions are undisclosed)"
    if best:
        ev["closest"] = best
    ev["pack_orders"] = orders
    return False, ev


def _deck_density(doc):
    """T2 secondary: bullets per slide > 6, or words per bullet > 6 (research/87 T2 expected)."""
    bad = []
    for line in doc.splitlines():
        m = re.match(r"\s*[-*\u2022]\s+(.+)", line)
        if m and len(re.findall(r"\S+", m.group(1))) > 6:
            bad.append("bullet >6 words: " + m.group(1)[:40])
    slides = re.split(r"^#{1,6}\s+", doc, flags=re.M)
    for s in slides:
        n = len(re.findall(r"^\s*[-*\u2022]\s+", s, re.M))
        if n > 6:
            bad.append(f"{n} bullets under one heading")
    return bad


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trial", required=True, choices=sorted(TRIALS))
    ap.add_argument("--output", required=True, help="file holding the model's output")
    ap.add_argument("--pack", default=str(DEFAULT_PACK), help="portable/DDI-LIBRARY.md")
    args = ap.parse_args(argv)
    result = score(Path(args.output).read_text(encoding="utf-8"), args.trial,
                   Path(args.pack).read_text(encoding="utf-8"))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
