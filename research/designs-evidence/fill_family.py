#!/usr/bin/env python3
"""Generic design-family fill (research/82 sections 6, 8, 9) -- generalised from generate_cv_fill.py.

    python3 research/designs-evidence/fill_family.py --family cv --write     # write the section-9 outputs
    python3 research/designs-evidence/fill_family.py --family cv --check     # rebuild in memory, diff vs committed
    python3 research/designs-evidence/fill_family.py --family deck --dry-run # print the proposed ranking, write nothing

WHAT IS RULE, WHAT IS DECISION.  The script has two layers, kept apart on purpose:

1. ENGINE (this file, deterministic, no taste).  Reads the family's coded evidence (corpus tables plus
   recode overlays, minus features the agreement gate dropped), applies the section-6 ranking, and
   proposes the section-8 fill from the base library rows: doc-style reuse-or-new, typeface by class
   and Google Fonts popularity, palette by hexes-derived class.  `--dry-run` prints exactly this for
   ANY family from current evidence and writes nothing.
2. DECISIONS (research/designs-evidence/fill-specs/<family>.json, authored by a human worker): only what the
   rules leave open -- names and wording, which archetype a seeded/L3 design codes to, `own_archetype` of
   unmatched seeds, authored text of NEW style rows (`style_row`), `pending` designs, fetched provenance URLs.
   Rank, Evidence Class, which designs ship, and every style / palette / typeface key are the ENGINE's
   (R7-4): a spec value that differs from the engine's proposal fails `--check` and blocks `--write`
   unless its entry carries `"override": "<82a file> <rule id>"` naming an existing ratified rule.

`--write` = spec + engine -> the four section-9 CSVs and `<family>-fill-log.md` (the generated decisions log:
engine ranking, plan, proposals, retirements, blanked bias tokens, violations). For cv and proposal the
committed CSVs are reproduced byte-for-byte (test_fill_family.py). Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parent
ROOT = RES.parent
SKILL_DATA = ROOT / "skill" / "document-design-intelligence" / "data" / "base"
LIB = RES / "library"
DESIGNS = RES / "designs"
PROV = RES / "provenance"
SPECS = HERE / "fill-specs"

DOC_STYLES_COLS = ["style_key", "Display Name", "Keywords", "Best For", "Not For", "Brand Scope",
                   "Rule Hair pt", "Rule Strong pt", "Rule Brand pt", "Corner Radius mm", "Table Rules",
                   "Table Fills", "Emphasis Mechanism", "Field Style", "Checklist"]
DOC_REASONING_COLS = ["doc_category", "Style Key", "Palette Key", "Typeface Key", "Style Bias Terms",
                      "Palette Bias Terms", "Typeface Bias Terms", "Doc Conditions", "Anti-Pattern Tokens",
                      "Severity", "Design Key"]
DESIGNS_COLS = ["design_key", "Display Name", "Family", "Rank", "Reasoning Key", "Keywords", "Best For",
                "Not For", "Evidence Class", "Brand Scope"]
PROV_COLS = ["prov_key", "Table", "Row Key", "Evidence Class", "Source Name", "Source URL",
             "Ranking Metric", "Rank Value", "Retrieved", "Fetch"]

#: candidate identity-feature columns, in the order an archetype code joins them (section 4);
#: a family uses the ones its coded tables actually carry unless fill-specs/<family>.json says otherwise
IDENTITY_CANDIDATES = ["columns", "heading", "colour", "header"]


# ============================================================================ markdown tables

def md_tables(text: str):
    """[(section_heading, header_cells, [row_cells...])] for every pipe table in `text`."""
    tables, section, lines, i = [], "", text.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            section = line.lstrip("#").strip()
        if (line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1])):
            header = _cells(line)
            rows, j = [], i + 2
            while j < len(lines) and lines[j].startswith("|"):
                rows.append(_cells(lines[j]))
                j += 1
            tables.append((section, header, rows))
            i = j
            continue
        i += 1
    return tables


def _cells(line: str):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    # escaped pipes (`\|`) live inside archetype codes; protect them
    body = body.replace("\\|", "\x00")
    return [c.strip().replace("\x00", "|") for c in body.split("|")]


def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()


# ================================================================================== evidence

class Item:
    __slots__ = ("id", "corpus", "pos", "name", "feats", "admissible")

    def __init__(self, id_, corpus, pos, name, feats, admissible):
        self.id, self.corpus, self.pos, self.name = id_, corpus, pos, name
        self.feats, self.admissible = feats, admissible


def _is_admissible(cell: str) -> bool:
    c = re.sub(r"[*`\"']", "", cell).strip().lower()
    return re.split(r"[\s(,;—-]", c, maxsplit=1)[0] in ("yes", "y")


#: column-name aliases across the families' coded tables -> one canonical feature name
CANON = {"head": "heading", "adm": "admissible", "dens": "density", "rules": "rules boxes",
         "bg": "background", "title": "title layout", "body class": "body",
         "declared font": "font", "font family": "font", "theme font": "font", "fonts": "font"}

#: identity-feature slots (section 4): a family uses the first present name of each slot
IDENTITY_SLOTS = [("columns", "panels", "background"), ("heading",), ("colour",),
                  ("header", "title layout", "field style")]


def canon(name: str) -> str:
    n = _norm(name)
    return CANON.get(n, n)


def identity_for(items: list) -> list:
    """The identity features a family's coded tables carry, in section-4 order."""
    have = set()
    for it in items:
        have |= set(it.feats)
    out = []
    for slot in IDENTITY_SLOTS:
        for name in slot:
            if name in have:
                out.append(name)
                break
    return out


def _slice_section(text: str, want: str) -> str:
    m = re.search(r"^#+ .*%s.*$" % re.escape(want), text, re.M)
    if not m:
        return text
    nxt = re.search(r"^#{1,%d} " % (len(m.group(0)) - len(m.group(0).lstrip("#"))), text[m.end():], re.M)
    return text[m.start(): m.end() + (nxt.start() if nxt else len(text))]


def _coded_table_items(section, header, rows, cfg):
    norm = [canon(h) for h in header]
    items = []
    for row in rows:
        if len(row) != len(header):
            continue
        rec = dict(zip(norm, row))
        raw_id = rec.get("id") or rec.get("pos") or rec.get("position") or ""
        raw_id = re.sub(r"[`\s].*$", "", raw_id.strip())
        m = re.search(r"(\d+)$", raw_id)
        if not m:
            continue
        pos = int(m.group(1))
        item_id = raw_id if ":" in raw_id else "%s:%0*d" % (cfg["id"], cfg.get("pos_width", 3), pos)
        name = re.sub(r"[`]", "", rec.get("repo") or rec.get("package") or rec.get("item") or rec.get("template") or "")
        feats = {k: re.sub(r"[*`]", "", v).strip() for k, v in rec.items()
                 if k not in ("id", "pos", "position", "admissible")}
        items.append(Item(item_id, cfg["id"], pos, name, feats, _is_admissible(rec.get("admissible", ""))))
    return items


def _is_coded_table(section: str, norm: list) -> bool:
    features = {"colour", "header", "title layout"} & set(norm)
    return "admissible" in norm and len(features) >= 2 and len(norm) >= 7 and (
        "coded" in section.lower() or "columns" in norm or "heading" in norm)


def load_corpus(cfg: dict, family_dir: Path = HERE):
    """Items of one corpus. `cfg`: id (prefix), file, section (optional heading substring that limits
    the search to one `##`/`###` block), n (denominator)."""
    text = (family_dir / cfg["file"]).read_text(encoding="utf-8")
    if cfg.get("section"):
        text = _slice_section(text, cfg["section"])
    for section, header, rows in md_tables(text):
        norm = [canon(h) for h in header]
        if _is_coded_table(section, norm):
            items = _coded_table_items(section, header, rows, cfg)
            if items:
                return items
    return []


def discover_corpora(family: str, family_dir: Path = HERE) -> list:
    """Every coded table in `<family>-corpus*.md` as one corpus (id prefix from its own item ids,
    N = its number of coded items). Used by --dry-run when no fill spec fixes the corpora."""
    out = []
    for path in sorted(family_dir.glob(f"{family}-corpus*.md")):
        text = path.read_text(encoding="utf-8")
        for section, header, rows in md_tables(text):
            norm = [canon(h) for h in header]
            if not _is_coded_table(section, norm):
                continue
            items = _coded_table_items(section, header, rows, {"id": path.stem.split("-")[-1].upper()[:4]})
            if not items:
                continue
            skipped = sum(1 for r in rows if len(r) != len(header))
            m_n = re.search(r"\bN\s*=\s*(\d+)", section)
            prefix = items[0].id.split(":")[0]
            for it in items:
                it.corpus = prefix
            if any(c["id"] == prefix and c["file"] == path.name for c in out):
                continue   # same corpus split over several tables: counted from the first
            out.append({"id": prefix, "file": path.name, "section": section,
                        "n": int(m_n.group(1)) if m_n else len(items), "level": "L1", "items": items,
                        "skipped_rows": skipped})
    return out


#: enum guards for recode overrides so a note column is never mistaken for a code
_VALID = {
    "header": {"plain-centered", "plain-left", "split", "band", "ruled", "image-hero"},
    "colour": {"mono", "one-accent", "multi", "fill-blocks"},
    "heading": {"sans", "serif", "mono", "display"},
    "columns": {"1", "2-sidebar", "2-equal", "3+", "grid", "2"},
    "background": {"light", "dark", "image"},
    "title layout": {"centered", "left", "split", "full-bleed-image"},
    "admissible": {"yes", "no"},
}


def apply_recodes(items: list, recode_files: list, family_dir: Path = HERE):
    """Later recode files override earlier codes. A column named `<feature>` or `<feature> (<round>)`
    overrides that feature; when a table has several such columns the LAST wins (r1 < r2 < r2a < r2ag).
    A recode `admissible` column (yes/no) overrides admissibility. Free-text note columns never match
    the enum guards, so they cannot overwrite a code."""
    by_id = {it.id: it for it in items}
    log = []
    for fname in recode_files:
        text = (family_dir / fname).read_text(encoding="utf-8")
        for _section, header, rows in md_tables(text):
            norm = [canon(h) for h in header]
            if "id" not in norm:
                continue
            feature_cols = {}
            for n, h in enumerate(norm):
                m = re.match(r"^(header|colour|heading|columns|background|title layout|admissible)\b", h)
                if m:
                    feature_cols[m.group(1)] = n
            for row in rows:
                if len(row) != len(header):
                    continue
                it = by_id.get(re.sub(r"[`\s].*$", "", row[norm.index("id")].strip()))
                if it is None:
                    continue
                for feat, n in feature_cols.items():
                    val = re.sub(r"\s*[(—-].*$", "", re.sub(r"[*`]", "", row[n])).strip().lower() \
                        if feat == "admissible" else re.sub(r"\s*\(.*$", "", re.sub(r"[*`]", "", row[n])).strip()
                    if not val or val not in _VALID.get(feat, {val}):
                        continue
                    if feat == "admissible":
                        new = val == "yes"
                        if new != it.admissible:
                            log.append((it.id, feat, it.admissible, new, fname))
                            it.admissible = new
                    elif val != it.feats.get(feat):
                        log.append((it.id, feat, it.feats.get(feat), val, fname))
                        it.feats[feat] = val
    return log


def archetype(item: Item, identity: list) -> str:
    return "|".join(item.feats.get(f, "?") for f in identity)


# ================================================================================== ranking (6)

def combined_table(items: list, corpora: list, identity: list):
    """{archetype: stats}. C21 / R7-1: k counts ADMISSIBLE exemplars only; every coded item (inadmissible
    included) stays in the denominator N. An inadmissible exemplar never enters `ex` (so it never breaks a
    tie, never sets a variant value) and never appears in a count; it is only tallied in `inadm` for the
    log. share = k/N, combined = unweighted mean over corpora (0 where absent), K = sum of k."""
    n_of = {c["id"]: c["n"] for c in corpora}
    table = {}
    for it in items:
        a = archetype(it, identity)
        row = table.setdefault(a, {"k": {c["id"]: 0 for c in corpora}, "adm": 0, "inadm": 0, "ex": []})
        if not it.admissible:
            row["inadm"] += 1
            continue
        row["k"][it.corpus] += 1
        row["adm"] += 1
        row["ex"].append(it)
    for a, row in table.items():
        row["share"] = {cid: row["k"][cid] / n_of[cid] for cid in n_of}
        row["combined"] = sum(row["share"].values()) / len(n_of)
        row["K"] = sum(row["k"].values())
        row["best_pos"] = min((e.pos for e in row["ex"]), default=10 ** 9)
        row["ncorpora"] = sum(1 for cid in n_of if row["k"][cid])
    return table


def corpus_order(corpora: list) -> list:
    """R7-6: the fixed order in which per-corpus shares break a tie, independent of the order the spec
    lists the corpora: higher evidence level first (L1 > L2 > L3 > L4), then the larger on-topic N, then
    corpus id in byte order."""
    return sorted(corpora, key=lambda c: (c.get("level", "L1"), -c["n"], c["id"]))


def rank_step1(table: dict, corpora: list, cap: int):
    """Section 6 step 1: ranked, K>=2 admissible exemplars, combined share desc; ties: per-corpus shares
    in `corpus_order` (R7-6) -> present in more corpora -> best native position -> archetype code in byte
    order. Returns (ordered, dropped_by_cap)."""
    order = [c["id"] for c in corpus_order(corpora)]
    eligible = [(a, r) for a, r in table.items() if r["K"] >= 2]

    def key(pair):
        a, r = pair
        return ((-round(r["combined"], 6),) + tuple(-round(r["share"][c], 6) for c in order)
                + (-r["ncorpora"], r["best_pos"], a))
    ordered = [a for a, _ in sorted(eligible, key=key)]
    return ordered[:cap], ordered[cap:]


# ==================================================================== section 8 proposals (rules)

def _lib_rows(name: str, sub: str = ""):
    """Rows of a base library table plus every research/library/<sub>/*.csv (new rows a family fill
    ADDED earlier), base first."""
    rows, seen = [], set()
    for path in [SKILL_DATA / f"{name}.csv"] + sorted((LIB / (sub or name)).glob("*.csv")):
        if path.is_file():
            with path.open(encoding="utf-8-sig", newline="") as f:
                for r in csv.DictReader(f):
                    sig = tuple(r.items())      # base tables already carry the library rows: read each once (F17)
                    if sig not in seen:
                        seen.add(sig)
                        rows.append(r)
    return rows


def modal_variant(exemplars: list, feature: str, n_of: dict | None = None, notes: list | None = None):
    """Modal value of a variant feature over an archetype's ADMISSIBLE exemplars (R7-1). A tie goes to the
    value held by the exemplar highest in its own corpus's native order: positions are compared as
    pos / N of the exemplar's corpus (R7 F4: raw positions of different corpora are not comparable);
    the tie is logged in `notes`."""
    n_of = n_of or {}
    counts = {}
    for it in exemplars:
        if not it.admissible:
            continue
        v = it.feats.get(feature)
        if v:
            counts.setdefault(v, [0, 10 ** 9])
            counts[v][0] += 1
            counts[v][1] = min(counts[v][1], it.pos / n_of.get(it.corpus, 1))
    if not counts:
        return None
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1][0], kv[1][1], kv[0]))
    if notes is not None and len(ranked) > 1 and ranked[0][1][0] == ranked[1][1][0]:
        notes.append(f"`{feature}` tie {ranked[0][1][0]}:{ranked[1][1][0]} between `{ranked[0][0]}` and "
                     f"`{ranked[1][0]}` broken by the higher-placed exemplar (pos/N)")
    return ranked[0][0]


STYLE_TABLE_RULES_HEADER_TOTAL = {"invoice", "quote", "report", "whitepaper", "proposal"}


#: agreement-file variant names -> the coded-table feature names items carry
VARIANT_ALIASES = {"rules_boxes": "rules boxes", "cover_page": "cover", "totals_position": "totals",
                   "table_rules": "table rules"}
_DROP_GATE = re.compile(r"dropped from filling.*?does not fail the gate:\s*([a-z_, ]+?)\.?\s*$", re.I)
_DROP_UNUSABLE = re.compile(r"\):\s*([a-z_, ]+?)\.\s*Not gating, not usable for filling", re.I)


def dropped_variants(family: str, spec: dict | None = None) -> set:
    """Variant features the family's agreement file(s) mark as dropped from filling (A_f < 0.80 -> the
    family default is used instead, section 7) or as unusable (no shared coded sample), plus any the spec
    lists under `dropped_variants`. Names are returned as the coded-table feature names."""
    names = set((spec or {}).get("dropped_variants", []))
    for path in sorted(HERE.glob(f"{family}-agreement*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            for pat in (_DROP_GATE, _DROP_UNUSABLE):
                m = pat.search(line)
                if m:
                    names |= {n.strip() for n in m.group(1).split(",") if n.strip()}
    return {VARIANT_ALIASES.get(n, n.replace("_", " ")) for n in names}


def family_default_style(family: str):
    """The doc-style row of the family's doctype default (section 8: 'the family default'): the base
    doctype of this family flagged `Family Default = y`, else its first; via its Reasoning Key."""
    with (SKILL_DATA / "doctypes.csv").open(encoding="utf-8", newline="") as f:
        docs = [r for r in csv.DictReader(f) if r["Family"] == family and r.get("Brand Scope", "generic") == "generic"]
    docs.sort(key=lambda r: r.get("Family Default", "") != "y")
    reasoning = {r["doc_category"]: r for r in _lib_rows("doc-reasoning")}
    styles = {r["style_key"]: r for r in _lib_rows("doc-styles")}
    for d in docs:
        row = styles.get(reasoning.get(d["Reasoning Key"], {}).get("Style Key", ""))
        if row:
            return row
    return None


def propose_style(family: str, arch: str, exemplars: list, identity: list,
                  dropped: frozenset = frozenset(), default_style: dict | None = None,
                  n_of: dict | None = None) -> dict:
    """Section 8 'Style' mapping, mechanically: rules/boxes, colour use and header treatment ->
    doc-styles columns; the checklist lines that carry columns/photo/boxes. A variant the agreement
    gate DROPPED (`dropped`) is not read from the corpus: the family default's value is used and the
    reason is recorded in `notes` (section 7, last sentence). Modal values are read over admissible
    exemplars only (R7-1)."""
    feats = dict(zip(identity, arch.split("|")))
    notes, checklist = [], []
    rb = modal_variant(exemplars, "rules boxes", n_of, notes) or modal_variant(exemplars, "rules", n_of, notes)
    if "rules boxes" in dropped and default_style:
        table_rules = default_style["Table Rules"]
        notes.append(f"rules/boxes dropped by the gate -> family default Table Rules `{table_rules}`")
    elif rb == "none":
        table_rules = "none"
    elif rb == "boxes":
        table_rules = "hairline"
        checklist.append("Border at most half of the blocks")
    else:
        table_rules = "header-and-total" if family in STYLE_TABLE_RULES_HEADER_TOTAL else "hairline"
    colour, header = feats.get("colour", ""), feats.get("header", "")
    emphasis = {"mono": "weight", "one-accent": "weight", "multi": "colour-text", "fill-blocks": "fill"}.get(colour, "weight")
    if header == "band":
        emphasis = "fill"
    rule_brand = "1" if header == "ruled" else "0"
    if feats.get("columns", "1") == "1":
        checklist.append("Keep single column")
    photo = None
    if "photo" in dropped:
        notes.append("photo dropped by the gate -> no photo line (family default)")
    else:
        photo = modal_variant(exemplars, "photo", n_of, notes)
        if photo == "no":
            checklist.append("Omit photo")
    return {"Table Rules": table_rules, "Table Fills": "none", "Emphasis Mechanism": emphasis,
            "Field Style": "none", "Rule Brand pt": rule_brand, "Checklist": checklist,
            "modal rules/boxes": rb, "photo": photo, "notes": notes}


#: R7-8: words that tie a library row to one region, standard or programme. A style row carrying one
#: cannot be reused for a design that is not that thing (it would import, e.g., the Europass section order).
FAMILY_SPECIFIC = re.compile(r"\b(europass|eu framework|dach|lebenslauf|tabellarisch\w*|harvard|din 5008|"
                             r"gov\.uk|france|gulf|gcc|academic|publications?|page limit)\b", re.I)
_PHOTO_OMIT = re.compile(r"\b(omit|no|without|avoid)\b[^;]*\bphoto", re.I)
_PHOTO_ALLOW = re.compile(r"\bphoto\b[^;]*\b(permitted|allowed|included|required)|\b(include|with|add)\b[^;]*\b"
                          r"(photo|headshot)", re.I)


def photo_contradiction(checklist: str, photo: str | None) -> bool:
    """R7-5 / section 8: a design coded photo=yes contradicts a checklist that omits it, photo=no
    contradicts one that permits/requires it."""
    if photo == "yes":
        return bool(_PHOTO_OMIT.search(checklist))
    if photo == "no":
        return bool(_PHOTO_ALLOW.search(checklist))
    return False


def reuse_candidates(proposal: dict, styles: list, family: str = "") -> list:
    """Existing doc-styles the mapping may reuse (section 8): Table Rules, Fills, Emphasis, Field Style and
    (Rule Brand>0) equal, and no checklist line contradicts the design: column count, photo (R7-5), or a
    region/standard token (R7-8). Several matches: rows prefixed with the family being filled first (R7-5:
    `<family>-`, not a hard-coded prefix), then key in byte order."""
    out, seen = [], set()
    for r in styles:
        if r["style_key"] in seen:
            continue
        seen.add(r["style_key"])
        if (r["Table Rules"], r["Table Fills"], r["Emphasis Mechanism"], r["Field Style"]) != (
                proposal["Table Rules"], proposal["Table Fills"], proposal["Emphasis Mechanism"], proposal["Field Style"]):
            continue
        if (float(r["Rule Brand pt"] or 0) > 0) != (float(proposal["Rule Brand pt"]) > 0):
            continue
        cl = r["Checklist"].lower()
        if "Keep single column" in proposal["Checklist"] and "multi-column" in cl and "avoid" not in cl:
            continue
        if photo_contradiction(r["Checklist"], proposal.get("photo")):
            continue
        if FAMILY_SPECIFIC.search(r["Checklist"] + " " + r.get("Keywords", "") + " " + r.get("Best For", "")):
            continue
        out.append(r["style_key"])
    prefix = f"{family}-" if family else "\x00"
    return sorted(out, key=lambda k: (not k.startswith(prefix), k))


def _hex_hsl(hexv: str):
    h = hexv.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (1 - abs(2 * l - 1))
    if mx == r:
        hue = ((g - b) / d) % 6
    elif mx == g:
        hue = (b - r) / d + 2
    else:
        hue = (r - g) / d + 4
    return hue * 60, s, l


def _lum(hexv: str) -> float:
    h = hexv.lstrip("#")
    chans = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        chans.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * chans[0] + 0.7152 * chans[1] + 0.0722 * chans[2]


def contrast(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
A7_BLUES = {"#4472c4", "#4f81bd", "#156082", "#0563c1"}       # section 5 rule A7: Office default blues


def palette_class(row: dict) -> str:
    """Section 4 colour-use class from a palette row's own hexes: chromatic = HSL S>=0.20 and
    0.12<=L<=0.90 over Primary, Secondary, Accent, Rule Brand; hues >=30 degrees apart count apart;
    0 -> mono, 1 -> one-accent, >=2 -> multi. (`fill-blocks` is a page-area property of a document, not
    a hue count: a palette SERVES a fill-blocks archetype when its Fill-Only Roles are non-empty, see
    palette_serves.)"""
    return _palette_hues(row)[0]


def _palette_hues(row: dict):
    hues = []
    for role in ("Primary", "Secondary", "Accent", "Rule Brand"):
        v = row.get(role, "")
        if not _HEX.match(v or ""):
            continue
        h, s, l = _hex_hsl(v)
        if s >= 0.20 and 0.12 <= l <= 0.90 and all(min(abs(h - o), 360 - abs(h - o)) >= 30 for o in hues):
            hues.append(h)
    return ("mono" if not hues else "one-accent" if len(hues) == 1 else "multi"), hues


def palette_serves(colour: str, row: dict) -> bool:
    if colour == "fill-blocks":
        return bool(row.get("Fill-Only Roles"))
    return palette_class(row) == colour


def palette_evidence_rank() -> dict:
    """{palette_key: rank} from every provenance row: 0 authority fetched, 1 authority search-corroborated
    (or any other Fetch), 2 ranked, 3 convention, 4 no provenance. Section 8 order: evidence class first
    (authority, then ranked), fetched before search-corroborated (82a R7-3 and
    82a-clarifications-6 R1)."""
    best = {}
    files = list(PROV.glob("*.csv")) + [SKILL_DATA / "provenance.csv"]
    for path in files:
        if not path.is_file():
            continue
        with path.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                if r.get("Table") != "palettes":
                    continue
                cls, fetch = r.get("Evidence Class", ""), r.get("Fetch", "")
                rank = (0 if fetch == "fetched" else 1) if cls == "authority" else 2 if cls == "ranked" else 3
                best[r["Row Key"]] = min(best.get(r["Row Key"], 4), rank)
    return best


def propose_palette(colour: str, palettes: list, evidence: dict, modal_hue: float | None = None) -> list:
    """Section 8 'Palette' candidates for an archetype's colour use, in order: (1) evidence strength,
    (2) accent hue bin (8 x 45 degrees) equal to the archetype's modal accent bin, when per-item hues
    exist (`modal_hue`), (3) Foreground/Background >= 4.5:1 and, for a one-accent palette, accent >= 4.5:1
    on Background (headline-only 3:1 is not available from the evidence), (4) not an A7 blue, (5) key.
    Returns [(key, evidence rank)]; no hex is invented."""
    seen, rows = set(), []
    for r in palettes:
        if r["palette_key"] in seen or r.get("Brand Scope", "generic") != "generic":
            continue
        seen.add(r["palette_key"])
        if not palette_serves(colour, r) or not (_HEX.match(r.get("Foreground", "")) and _HEX.match(r.get("Background", ""))):
            continue
        fg_ok = contrast(r["Foreground"], r["Background"]) >= 4.5
        acc = r.get("Accent", "")
        acc_ok = True
        if colour == "one-accent":
            acc_ok = bool(_HEX.match(acc)) and contrast(acc, r["Background"]) >= 4.5
        a7 = acc.lower() in A7_BLUES
        hue_bin_miss = 0
        if modal_hue is not None and _HEX.match(acc):
            hue_bin_miss = int(int(_hex_hsl(acc)[0] // 45) != int(modal_hue // 45))
        rows.append((evidence.get(r["palette_key"], 4), hue_bin_miss, not (fg_ok and acc_ok), a7, r["palette_key"]))
    rows.sort()
    return [(k, ev) for ev, _b, bad, _a7, k in rows if not bad]


def google_popularity() -> dict:
    """{family lower: popularity int} from the provenance rows the library typefaces carry (fetched
    from fonts.google.com/metadata/fonts by the typeface batch); no network here."""
    out = {}
    for path in PROV.glob("typefaces-*.csv"):
        with path.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                m = re.search(r"family:\s*(.+)$", r.get("Ranking Metric", ""))
                if m and str(r.get("Rank Value", "")).isdigit():
                    out[m.group(1).strip().lower()] = int(r["Rank Value"])
    return out


def scale_media() -> dict:
    """{scale_key: {Medium, ...}} over the base and library type-scales."""
    out = {}
    for r in _lib_rows("type-scales"):
        out.setdefault(r["scale_key"], set()).add(r["Medium"])
    return out


def family_medium(family: str) -> str:
    """Section 8: deck=projection, infographic=screen, else print."""
    return {"deck": "projection", "infographic": "screen"}.get(family, "print")


#: OS/Office-bundled faces (section 8 typeface branch 1) -> the class of the `safe-*` row that serves them
OS_BUNDLED = {"arial": "sans", "helvetica": "sans", "calibri": "sans", "verdana": "sans", "tahoma": "sans",
              "segoe ui": "sans", "trebuchet ms": "sans", "times new roman": "serif", "times": "serif",
              "georgia": "serif", "cambria": "serif", "garamond": "serif", "courier new": "mono"}


def propose_typeface(arch: str, identity: list, typefaces: list, pop: dict, modal_body: str | None = None,
                     medium: str = "print", media: dict | None = None, modal_font: str | None = None,
                     font_evaluable: bool = False) -> tuple:
    """Section 8 'Typeface'.
      * DECLARED-FONT BRANCH (R7-9): if the modal declared font of the archetype's exemplars
        (`modal_font`) is OS/Office-bundled, the candidates are the `safe-*` rows of that class (the row
        whose Heading Family is that font first). If it is not bundled the ordinary branch runs; if the
        corpus carries no declared fonts (`font_evaluable` False) the branch is logged as not evaluable.
      * ORDINARY BRANCH: rows whose Category Contrast (heading-body) equals the archetype's heading class
        and its modal body class (a row with the body class only when the corpus codes one); ordered by
        lowest Google Fonts popularity of the Heading Family (a row with none sorts last), then
        installable/editable licence, then key.
      * MEDIUM RULE (R7-2): the row's Scale Key must have the family's medium, else the next candidate;
        this holds for the declared-font branch too.
      * PAIRING FALLBACK (rule R2, research/82a-clarifications-6.md, ratified): if no row matches
        heading AND body, keep the IDENTITY feature and relax the VARIANT one; the relaxation is logged.
    Returns ([keys, best first, max 3], [notes])."""
    heading = dict(zip(identity, arch.split("|"))).get("heading", "")
    media = media or {}
    notes = []

    def rank(rows):
        keyed = []
        for r in rows:
            lic = 0 if r.get("Embedding Licence") in ("installable", "editable") else 1
            keyed.append((pop.get(r["Heading Family"].lower(), 10 ** 6), lic, r["typeface_key"], r))
        keyed.sort(key=lambda x: x[:3])
        return keyed

    def usable(keyed):
        ok, seen_keys = [], set()
        for _p, _l, key, r in keyed:
            if key in seen_keys:
                continue
            seen_keys.add(key)
            if media and medium not in media.get(r.get("Scale Key", ""), {medium}):
                if ok:      # a rejection only matters for a row ranked above the chosen one
                    continue
                notes.append(f"`{key}` rejected: Scale Key `{r.get('Scale Key', '')}` is medium "
                             f"{sorted(media.get(r.get('Scale Key', ''), []))}, not {medium} (medium rule)")
                continue
            if key not in ok:
                ok.append(key)
        return ok

    generic = [r for r in typefaces if r.get("Brand Scope", "generic") == "generic"]

    def classes(r):
        cc = r.get("Category Contrast", "")
        return tuple(cc.split("-")) if cc.count("-") == 1 else (None, None)

    if modal_font:
        fclass = OS_BUNDLED.get(modal_font.strip().lower())
        if fclass:
            safe = [r for r in generic if r["typeface_key"].startswith("safe-") and classes(r)[0] == fclass]
            safe.sort(key=lambda r: (r["Heading Family"].lower() != modal_font.strip().lower(), r["typeface_key"]))
            found = usable([(0, 0, r["typeface_key"], r) for r in safe])
            if found:
                notes.append(f"declared-font branch: modal font `{modal_font}` is OS/Office-bundled -> safe {fclass} row")
                return found[:3], notes
        else:
            notes.append(f"declared-font branch: modal font `{modal_font}` is not OS/Office-bundled -> ordinary branch")
    elif not font_evaluable:
        notes.append("declared-font branch not evaluable: the corpus carries no declared fonts")

    strict = [r for r in generic if classes(r)[0] == heading and (modal_body is None or classes(r)[1] == modal_body)]
    found = usable(rank(strict))
    if not found and modal_body is not None:
        relaxed = [r for r in generic if classes(r)[0] == heading]
        found = usable(rank(relaxed))
        if found:
            notes.append(f"no row pairs a {heading} heading with a {modal_body} body: body variant relaxed, "
                         f"heading class kept (rule R2, research/82a-clarifications-6.md)")
    return found[:3], notes


class Library:
    """The library tables the section-8 proposals read, loaded once. When `family` is given, the rows that
    family's PREVIOUS fill wrote are hidden (a re-run must not reuse its own earlier output)."""

    def __init__(self, family: str = ""):
        own = own_output_keys(family, "doc-styles", "style_key") if family else set()
        self.styles = [r for r in _lib_rows("doc-styles") if r["style_key"] not in own]
        self.typefaces = _lib_rows("typefaces")
        self.palettes = _lib_rows("palettes")
        self.pop = google_popularity()
        self.media = scale_media()
        self.evidence = palette_evidence_rank()


def section8_proposal(family: str, arch: str, exemplars: list, identity: list, lib: "Library",
                      dropped: frozenset, default_style: dict | None, n_of: dict | None = None,
                      font_evaluable: bool = False) -> dict:
    """Everything section 8 derives by rule for one archetype: style (gate-dropped variants read from the
    family default), reuse candidates, palette candidates (evidence strength -> hue bin -> contrast -> A7
    -> key), typeface candidates (declared font, class, popularity, medium rule, pairing fallback) and the
    notes each rule left. Exemplars are the archetype's ADMISSIBLE items."""
    feats = dict(zip(identity, arch.split("|")))
    style = propose_style(family, arch, exemplars, identity, dropped, default_style, n_of)
    tnotes0 = []
    modal_body = None if "body" in dropped else modal_variant(exemplars, "body", n_of, tnotes0)
    modal_font = modal_variant(exemplars, "font", n_of, tnotes0)
    typefaces, tnotes = propose_typeface(arch, identity, lib.typefaces, lib.pop, modal_body,
                                         family_medium(family), lib.media, modal_font,
                                         font_evaluable or any("font" in e.feats for e in exemplars))
    palettes = propose_palette(feats.get("colour", ""), lib.palettes, lib.evidence)
    return {"style": style, "reuse": reuse_candidates(style, lib.styles, family), "palettes": palettes,
            "typefaces": typefaces, "modal_body": modal_body, "modal_font": modal_font,
            "notes": style["notes"] + tnotes0 + tnotes}


# ================================================================================== building (9)

def _fmt_share(k: int, n: int) -> str:
    return "%.3f (%d/%d)" % (k / n, k, n)


def spec_identity(spec: dict) -> list:
    """The spec's identity features minus any the agreement gate dropped from the family's identity
    (section 7: a second failure removes the feature, disclosed; the family is then coarsened)."""
    return [f for f in spec["identity"] if f not in spec.get("dropped_identity", [])]


GATE_LINE = re.compile(r"(dropped from filling|removed from the family|disqualified from filling|"
                       r"identity gate: fail|below A_f)", re.I)


def gate_notes(family: str) -> list:
    """Lines of `<family>-agreement*.md` that record a gate outcome, so a dry-run shows which features
    the agreement file marks as failed/dropped. Informational: the decision to drop is the spec's."""
    notes = []
    for path in sorted(HERE.glob(f"{family}-agreement*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if GATE_LINE.search(line):
                notes.append(f"{path.name}: {line.strip()[:160]}")
    return notes


def engine_state(spec: dict):
    """Evidence -> items -> combined table, all from the spec's corpus/recode config."""
    corpora = spec["corpora"]
    items = []
    for cfg in corpora:
        items += load_corpus(cfg)
    changes = apply_recodes(items, spec.get("recodes", []))
    table = combined_table(items, corpora, spec_identity(spec))
    return items, changes, table


# ------------------------------------------------------------------ the engine decides (R7-4, R7-7)

CAP = 10          # section 6 / C29: the family's list has at most 10 designs, contiguous ranks 1..N


def protected_reasoning_keys(family: str) -> set:
    """Reasoning Keys that some generic doctype of the family points at: those designs are doctype
    defaults ('never changed and never promoted', section 6) and are always shipped (R7-7)."""
    with (SKILL_DATA / "doctypes.csv").open(encoding="utf-8", newline="") as f:
        return {r["Reasoning Key"] for r in csv.DictReader(f)
                if r["Family"] == family and r.get("Brand Scope", "generic") == "generic"}


def own_output_keys(family: str, sub: str, col: str) -> set:
    """Keys of the rows this family's PREVIOUS fill wrote to research/library/<sub>/<family>.csv. The base
    library already contains them after load-base.py; a re-run must not see its own earlier output."""
    path = LIB / sub / f"{family}.csv"
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8-sig", newline="") as f:
        return {r[col] for r in csv.DictReader(f)}


def plan_designs(family: str, spec: dict, table: dict) -> dict:
    """The section-6 list, decided by rule. `spec["designs"]` are the human decisions (names, wording,
    which archetype a seeded/L3 design codes to); the ENGINE decides which of them ship and in what order:

    * step 1: archetypes with K>=2 admissible exemplars in `rank_step1` order (R7-1, R7-6);
    * a design that codes to a step-1 archetype MERGES there (rank of the archetype, class `ranked`, its
      authority stays an extra provenance row). Two designs on one archetype: the doctype default first,
      then the one with L3 sources, then key; the other is retired (identity duplicate, R7-7);
    * L3 designs outside step 1 take L3 slots, unmatched doctype defaults are exempt from the L4 cap but
      still count towards the cap of 10 (R7-7), one non-default convention design takes the L4 slot after
      an identity-duplicate check on its own archetype (`own_archetype`, values only, never taste), ties
      by key;
    * total <= 10. A doctype default whose archetype falls outside the cap takes the place of the last
      ranked slot (R7-7);
    * `pending` designs (R7-10) are not shipped and are listed.
    Returns {"shipped": [...], "retired": [...], "pending": [...], "outside": [...], "missing": [...],
    "eligible": [...], "cap1": int}."""
    corpora = spec["corpora"]
    eligible, _ = rank_step1(table, corpora, cap=10 ** 6)
    protected = protected_reasoning_keys(family)
    live, pending = [], []
    for d in spec["designs"]:
        (pending if d.get("pending") else live).append(d)

    def prot(d):
        return d["Reasoning Key"] in protected

    retired, outside = [], []
    by_arch = {}
    for d in live:
        if d.get("archetype") in eligible:
            by_arch.setdefault(d["archetype"], []).append(d)
    winner = {}
    for a, ds in by_arch.items():
        ds.sort(key=lambda d: (not prot(d), not d["l3"], d["design_key"]))
        winner[a] = ds[0]
        retired += [(x["design_key"], f"identity duplicate of `{ds[0]['design_key']}` ({a})") for x in ds[1:]]
    merged_keys = {d["design_key"] for ds in by_arch.values() for d in ds}
    rest = [d for d in live if d["design_key"] not in merged_keys]
    l3_un = sorted([d for d in rest if d["l3"]], key=lambda d: d["design_key"])[:3]
    un_prot = sorted([d for d in rest if prot(d) and d not in l3_un], key=lambda d: d["design_key"])
    conv = sorted([d for d in rest if not prot(d) and d not in l3_un], key=lambda d: d["design_key"])
    for d in rest:
        if d not in l3_un and d not in un_prot and d not in conv:
            retired.append((d["design_key"], "more than 3 unmatched L3 designs"))
    # identity-duplicate retirement of the unmatched convention designs (R7-7): by identity values alone
    taken = {d.get("own_archetype") or d.get("archetype") for d in l3_un + un_prot} - {None}
    l4 = None
    for d in conv:
        own = d.get("own_archetype") or d.get("archetype")
        if d.get("archetype") and d["archetype"] not in eligible and not d["l3"]:
            outside.append((d["design_key"], f"archetype `{d['archetype']}` has fewer than 2 admissible exemplars"))
            continue
        if own and own in taken:
            retired.append((d["design_key"], f"identity duplicate: own archetype `{own}` is already shipped"))
        elif l4 is None:
            l4 = d
            taken.add(own)
        else:
            retired.append((d["design_key"], "the single L4 convention slot is taken"))
    # R6 (82a-clarifications-6): every doctype default counts INSIDE the cap of 10. Ranked slots k = 10 minus
    # the reserved slots (unmatched L3 / defaults / L4) minus the matched defaults whose archetype is not
    # among the first k ranked archetypes: the largest k for which everything fits.
    reserved = len(l3_un) + len(un_prot) + (1 if l4 else 0)
    k = min(max(CAP - reserved, 0), len(eligible))
    while True:
        forced = [a for a in eligible[k:] if a in winner and prot(winner[a])]
        if k + len(forced) + reserved <= CAP or k == 0:
            break
        k -= 1
    cap1 = k
    chosen = eligible[:k] + forced
    ranked_out = [a for a in eligible[k:] if a in winner and a not in forced]
    outside += [(winner[a]["design_key"], f"archetype `{a}` is outside the {k} ranked slots (cap {CAP} counts "
                 f"every default, R6)") for a in ranked_out]
    missing = [a for a in chosen if a not in winner]
    shipped = []
    for a in chosen:
        if a in winner:
            shipped.append({"design": winner[a], "archetype": a, "class": "ranked", "slot": "ranked"})
    for d in l3_un:
        shipped.append({"design": d, "archetype": d.get("archetype"), "class": "authority", "slot": "L3"})
    for d in un_prot:
        shipped.append({"design": d, "archetype": None, "class": "convention", "slot": "default"})
    if l4:
        shipped.append({"design": l4, "archetype": None, "class": "convention", "slot": "L4"})
    for n, s_ in enumerate(shipped, 1):
        s_["rank"] = n
    return {"shipped": shipped, "retired": retired, "pending": [(d["design_key"], d["pending"]) for d in pending],
            "outside": outside, "missing": missing, "eligible": eligible, "cap1": cap1}


def _override_ok(text: str) -> bool:
    """R7-4: `"override": "<82a file> <rule id>"` must point at an existing ratified rule: the file exists
    under research/, is not marked draft (a `RATIFIED` status wins over historical wording), and has a line that starts with the rule id."""
    parts = (text or "").split()
    if len(parts) < 2:
        return False
    path = RES / parts[0]
    if not path.is_file():
        return False
    body = path.read_text(encoding="utf-8")
    head = "\n".join(body.splitlines()[:20])
    if "RATIFIED" not in head and ("not ratified" in head.lower() or "draft" in head.lower()):
        return False
    rid = re.escape(parts[1])
    return bool(re.search(r"^[\s>*#-]*%s(\b|\s|$)" % rid, body, re.M))


def base_reasoning_keys(family: str) -> set:
    own = own_output_keys(family, "doc-reasoning", "doc_category")
    return {r["doc_category"] for r in _lib_rows("doc-reasoning")} - own


#: bias terms a design's own coding contradicts (R7-8): {feature test -> tokens to blank}
def blank_bias(defaults: dict, feats: dict, typeface_key: str) -> tuple:
    """Copy the family default's bias terms, blanking tokens the archetype contradicts (R7-8) and
    returning [(column, token, reason)] for the log."""
    out, blanked = dict(defaults), []

    def cut(col, hit, reason):
        kept = []
        for t in [x.strip() for x in out.get(col, "").split(",") if x.strip()]:
            if hit(t.lower()):
                blanked.append((col, t, reason))
            else:
                kept.append(t)
        out[col] = ", ".join(kept)
    if feats.get("colour", "mono") != "mono":
        cut("Palette Bias Terms", lambda t: t in {"monochrome", "ink on white"}, f"colour use is {feats.get('colour')}")
    if feats.get("columns", "1") != "1":
        cut("Style Bias Terms", lambda t: t == "single column", f"columns are {feats.get('columns')}")
    if feats.get("colour") == "fill-blocks":
        cut("Style Bias Terms", lambda t: t in {"no color blocks", "no colour blocks"}, "colour use is fill-blocks")
    if not typeface_key.startswith("safe-"):
        cut("Typeface Bias Terms", lambda t: bool(re.search(r"\bsafe\b|ubiquitous|no embedding", t)),
            f"typeface `{typeface_key}` is not a safe-* row")
    heading = feats.get("heading", "")
    if heading == "sans":
        cut("Typeface Bias Terms", lambda t: bool(re.search(r"\bserif\b", t)), "heading class is sans")
    elif heading == "serif":
        cut("Typeface Bias Terms", lambda t: bool(re.search(r"\bsans\b", t)), "heading class is serif")
    return out, blanked


STYLE_MAP_COLS = ("Table Rules", "Table Fills", "Emphasis Mechanism", "Field Style")


def resolve_family(family: str, spec: dict) -> dict:
    """Everything the engine decides for a family, in one object: evidence, plan, section-8 proposals,
    the resolved reasoning/style rows, blanked tokens, and every place the spec disagrees with the engine
    (`violations`; empty when the spec holds only ratified overrides)."""
    items, changes, table = engine_state(spec)
    corpora, identity = spec["corpora"], spec_identity(spec)
    n_of = {c["id"]: c["n"] for c in corpora}
    plan = plan_designs(family, spec, table)
    lib = Library(family)
    dropped = frozenset(dropped_variants(family, spec))
    default_style = family_default_style(family)
    font_ev = any("font" in it.feats for it in items)
    seeds = base_reasoning_keys(family)
    base_styles = {r["style_key"] for r in lib.styles}
    tf_by_key = {r["typeface_key"]: r for r in lib.typefaces}
    spec_rows = {r["doc_category"]: r for r in spec["reasoning"].get("rows", [])}
    spec_styles = {(s["style_key"] if isinstance(s, dict) else s[0]): (s if isinstance(s, dict) else dict(zip(DOC_STYLES_COLS, s)))
                   for s in spec.get("doc_styles", [])}
    violations, props, rows, styles_out, blanked_log = [], {}, [], {}, []
    defaults_row = default_reasoning_row(family)

    def check(label, value, expected, holder):
        if value != expected and not _override_ok(holder.get("override", "")):
            violations.append(f"{label}: spec `{value}` != engine `{expected}` (needs an `override` citing a "
                              f"ratified 82a rule)")

    for a in plan["missing"]:
        violations.append(f"engine ranks `{a}` but the spec decides no design for it")
    for s_ in plan["shipped"]:
        d, arch = s_["design"], s_["archetype"]
        rk = d["Reasoning Key"]
        if not arch or rk in seeds:
            continue                                   # seeded row (section 9: no new rows) or convention
        prop = section8_proposal(family, arch, table[arch]["ex"], identity, lib, dropped, default_style, n_of, font_ev)
        props[d["design_key"]] = prop
        row = spec_rows.get(rk, {})
        # ---- style: reuse an existing row when the mapping matches one, else the authored new row
        if prop["reuse"]:
            style_key = prop["reuse"][0]
            if d.get("style_row"):
                check(f"{d['design_key']} style_row", d["style_row"], style_key, d)
        else:
            style_key = d.get("style_row") or ""
            if not style_key or style_key not in spec_styles:
                violations.append(f"{d['design_key']}: no existing style matches the mapping and the spec authors none "
                                  f"(`style_row`)")
            else:
                for col in STYLE_MAP_COLS:
                    check(f"{d['design_key']} new style `{style_key}` {col}", spec_styles[style_key][col],
                          prop["style"][col], spec_styles[style_key])
                if (float(spec_styles[style_key]["Rule Brand pt"] or 0) > 0) != (float(prop["style"]["Rule Brand pt"]) > 0):
                    check(f"{d['design_key']} new style `{style_key}` Rule Brand", spec_styles[style_key]["Rule Brand pt"],
                          prop["style"]["Rule Brand pt"], spec_styles[style_key])
                styles_out[style_key] = spec_styles[style_key]
        if "Style Key" in row:
            check(f"{rk} Style Key", row["Style Key"], style_key, row)
            style_key = row["Style Key"]
        # ---- palette / typeface: the engine's first candidate, else the family default (gap)
        pal = prop["palettes"][0][0] if prop["palettes"] else (defaults_row or {}).get("Palette Key", "")
        tf = prop["typefaces"][0] if prop["typefaces"] else (defaults_row or {}).get("Typeface Key", "")
        if not prop["palettes"]:
            prop["notes"].append("palette-gap: no candidate -> family default palette")
        if not prop["typefaces"]:
            prop["notes"].append("scale-gap: no candidate -> family default typeface")
        if "Palette Key" in row:
            check(f"{rk} Palette Key", row["Palette Key"], pal, row)
            pal = row["Palette Key"]
        if "Typeface Key" in row:
            check(f"{rk} Typeface Key", row["Typeface Key"], tf, row)
            tf = row["Typeface Key"]
        trow = tf_by_key.get(tf, {})
        if trow and family_medium(family) not in lib.media.get(trow.get("Scale Key", ""), {family_medium(family)}):
            violations.append(f"{rk}: typeface `{tf}` Scale Key `{trow.get('Scale Key')}` is not medium "
                              f"{family_medium(family)} (medium rule, no override)")
        feats = dict(zip(identity, arch.split("|")))
        bias, blanked = blank_bias(spec["reasoning"]["defaults"], feats, tf)
        blanked_log += [(rk,) + b for b in blanked]
        toks = spec["reasoning"]["anti_tokens"]["default"].split(";")
        if prop["style"].get("photo") == "yes" and "photo" in toks:
            toks.remove("photo")
        if feats.get("columns", "1") != "1" and "multi-column" in toks:
            toks.remove("multi-column")
        rows.append({"doc_category": rk, "Style Key": style_key, "Palette Key": pal, "Typeface Key": tf,
                     "Style Bias Terms": bias["Style Bias Terms"], "Palette Bias Terms": bias["Palette Bias Terms"],
                     "Typeface Bias Terms": bias["Typeface Bias Terms"], "Doc Conditions": bias["Doc Conditions"],
                     "Anti-Pattern Tokens": ";".join(toks), "Severity": bias["Severity"], "Design Key": rk,
                     "_arch": arch, "_design": d["design_key"]})
    # rows the spec authors outright for unmatched designs with no seeded row (explicit keys, unchecked)
    for s_ in plan["shipped"]:
        d = s_["design"]
        if not s_["archetype"] and d["Reasoning Key"] not in seeds and d["Reasoning Key"] in spec_rows:
            r = spec_rows[d["Reasoning Key"]]
            bias = spec["reasoning"]["defaults"]
            rows.append({"doc_category": r["doc_category"], "Style Key": r["Style Key"], "Palette Key": r["Palette Key"],
                         "Typeface Key": r["Typeface Key"], "Style Bias Terms": bias["Style Bias Terms"],
                         "Palette Bias Terms": bias["Palette Bias Terms"], "Typeface Bias Terms": bias["Typeface Bias Terms"],
                         "Doc Conditions": bias["Doc Conditions"], "Anti-Pattern Tokens": spec["reasoning"]["anti_tokens"]["default"],
                         "Severity": bias["Severity"], "Design Key": r["doc_category"], "_arch": None, "_design": d["design_key"]})
            if r["Style Key"] in spec_styles:
                styles_out[r["Style Key"]] = spec_styles[r["Style Key"]]
        elif not s_["archetype"] and d["Reasoning Key"] not in seeds:
            violations.append(f"{d['design_key']}: no seeded reasoning row and no spec row")
    overrides = sum(1 for r in spec["reasoning"].get("rows", []) if r.get("override")) + \
        sum(1 for s in spec_styles.values() if s.get("override")) + sum(1 for d in spec["designs"] if d.get("override"))
    return {"items": items, "changes": changes, "table": table, "plan": plan, "props": props, "rows": rows,
            "styles": styles_out, "blanked": blanked_log, "violations": violations, "overrides": overrides,
            "lib": lib, "dropped": dropped, "n_of": n_of}


def default_reasoning_row(family: str):
    """The doc-reasoning row of the family's doctype default (the source of bias terms, gap fallbacks)."""
    with (SKILL_DATA / "doctypes.csv").open(encoding="utf-8", newline="") as f:
        docs = [r for r in csv.DictReader(f) if r["Family"] == family and r.get("Brand Scope", "generic") == "generic"]
    docs.sort(key=lambda r: r.get("Family Default", "") != "y")
    reasoning = {r["doc_category"]: r for r in _lib_rows("doc-reasoning")}
    for d in docs:
        if d["Reasoning Key"] in reasoning:
            return reasoning[d["Reasoning Key"]]
    return None


def best_corpus(table_row: dict, corpora: list) -> dict:
    """The corpus a design's archetype is best represented in (highest share; ties in corpus_order)."""
    ordered = corpus_order(corpora)
    return max(ordered, key=lambda c: (round(table_row["share"][c["id"]], 6), -ordered.index(c)))


def build(family: str) -> dict:
    """{relative path: text} for the four section-9 CSVs and the decisions log."""
    spec = load_spec(family)
    if spec is None:
        raise SystemExit(f"no fill-specs/{family}.json: only --dry-run is available for {family}")
    res = resolve_family(family, spec)
    table, plan, corpora = res["table"], res["plan"], spec["corpora"]
    date = spec["date"]
    by_corpus = {c["id"]: c for c in corpora}

    # ---- designs.csv: Rank and Evidence Class come from the engine's plan
    d_rows = [dict(zip(DESIGNS_COLS, [
        s["design"]["design_key"], s["design"]["Display Name"], family, s["rank"], s["design"]["Reasoning Key"],
        s["design"]["Keywords"], s["design"]["Best For"], s["design"]["Not For"], s["class"], "generic"]))
        for s in plan["shipped"]]

    # ---- doc-styles.csv, doc-reasoning.csv: new rows only, in the plan's order
    ds_rows = [dict(zip(DOC_STYLES_COLS, [r[c] for c in DOC_STYLES_COLS])) for r in res["styles"].values()]
    dr_rows = [{c: r[c] for c in DOC_REASONING_COLS} for r in res["rows"]]

    # ---- provenance.csv: L3 authority rows, ranked rows per corpus with k>0 (share from the engine's
    # admissible-only table), convention blanks, borrowed rows; then the fill-rule rows
    p_rows = []

    def add(row_key, table_name, ev_class, source_name, url, metric, value):
        n = len([r for r in p_rows if r["Row Key"] == row_key and r["Table"] == table_name]) + 1
        p_rows.append(dict(zip(PROV_COLS, [
            "%s:%s:%d" % (table_name, row_key, n), table_name, row_key, ev_class, source_name, url, metric,
            value, date, "" if ev_class == "convention" else "fetched"])))

    for s in plan["shipped"]:
        d = s["design"]
        for l3 in d["l3"]:
            add(d["design_key"], "designs", "authority", l3["source_name"], l3["url"], "authority:doc", "")
        if s["class"] == "ranked":
            row = table[s["archetype"]]
            for c in corpora:
                if row["k"][c["id"]]:
                    add(d["design_key"], "designs", "ranked", c["source_name"], c["url"], c["metric"],
                        _fmt_share(row["k"][c["id"]], c["n"]))
        if d.get("borrowed_from"):
            # 82b A5: copy the source design's provenance, labelled as borrowed
            src_family = d["borrowed_from"].split("-")[0]
            src_path = PROV / f"{src_family}.csv"
            if src_path.is_file():
                with src_path.open(encoding="utf-8-sig", newline="") as f:
                    for r in csv.DictReader(f):
                        if r["Table"] == "designs" and r["Row Key"] == d["borrowed_from"]:
                            add(d["design_key"], "designs", r["Evidence Class"], "borrowed: " + r["Source Name"],
                                r["Source URL"], "borrowed:" + r["Ranking Metric"], r["Rank Value"])
        if s["class"] == "convention":
            add(d["design_key"], "designs", "convention", "", "", "", "")
    arch_of = {r["doc_category"]: r["_arch"] for r in res["rows"]}
    style_user = {}
    for r in res["rows"]:
        if r["Style Key"] in res["styles"]:
            style_user.setdefault(r["Style Key"], r["_arch"])
    for key, arch in style_user.items():
        if arch:
            c = best_corpus(table[arch], corpora)
            add(key, "doc-styles", "ranked", f"{c['id']} {family} corpus, fill applied per rule", c["url"],
                spec["fill_rule_metric"], spec["fill_rule_value"])
    for r in res["rows"]:
        if r["_arch"]:
            c = best_corpus(table[r["_arch"]], corpora)
            add(r["doc_category"], "doc-reasoning", "ranked", f"{c['id']} {family} corpus archetype, fill applied per rule",
                c["url"], spec["fill_rule_metric"], spec["fill_rule_value"])

    return {
        f"library/doc-styles/{family}.csv": _csv_text(DOC_STYLES_COLS, ds_rows),
        f"library/doc-reasoning/{family}.csv": _csv_text(DOC_REASONING_COLS, dr_rows),
        f"designs/{family}.csv": _csv_text(DESIGNS_COLS, d_rows),
        f"provenance/{family}.csv": _csv_text(PROV_COLS, p_rows),
        f"designs-evidence/{family}-fill-log.md": decisions_log(family, spec, res),
    }


def _csv_text(cols, rows) -> str:
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def decisions_log(family: str, spec: dict, res: dict) -> str:
    """`<family>-fill-log.md`: the engine's ranking, plan and section-8 proposals beside what shipped,
    every retirement / cap decision, every blanked bias token and every spec-vs-engine disagreement."""
    corpora, identity, table, plan = spec["corpora"], spec_identity(spec), res["table"], res["plan"]
    shipped_by_arch = {s["archetype"]: s for s in plan["shipped"] if s["archetype"]}
    out = [f"# {family} -- fill decisions log (generated by fill_family.py; do not hand-edit)", "",
           f"Evidence: {', '.join(c['file'] for c in corpora)}; recodes: {', '.join(spec.get('recodes', [])) or 'none'} "
           f"({len(res['changes'])} code overrides applied); identity features: {'|'.join(identity)}.", "",
           f"Spec overrides (entries carrying a ratified `override`): **{res['overrides']}**; "
           f"spec-vs-engine violations: **{len(res['violations'])}**.", ""]
    for v in res["violations"]:
        out.append(f"- VIOLATION: {v}")
    out += ["", "## Engine ranking (section 6, step 1; k counts ADMISSIBLE exemplars only, C21)", "",
            "| # | archetype | combined | K | inadm (not counted) | " + " | ".join(c["id"] for c in corpus_order(corpora))
            + " | shipped design (rank) |",
            "|---|---|---|---|---|" + "---|" * (len(corpora) + 1)]
    for n, a in enumerate(plan["eligible"], 1):
        r = table[a]
        s = shipped_by_arch.get(a)
        out.append(f"| {n} | `{a}` | {r['combined']:.4f} | {r['K']} | {r['inadm']} | " +
                   " | ".join(f"{r['k'][c['id']]}/{c['n']}" for c in corpus_order(corpora)) +
                   f" | {(s['design']['design_key'] + ' (' + str(s['rank']) + ')') if s else '(not shipped)'} |")
    out += ["", f"Cap: {CAP} designs in total; ranked slots this family = {plan['cap1']}.", "",
            "## Plan: what ships, in rank order", ""]
    for s in plan["shipped"]:
        out.append(f"{s['rank']}. `{s['design']['design_key']}` -- {s['slot']} -- class `{s['class']}`"
                   + (f" -- archetype `{s['archetype']}`" if s["archetype"] else ""))
    for label, lst in (("Retired (identity duplicate / slot rule)", plan["retired"]),
                       ("Outside the cap", plan["outside"]), ("Pending (not shipped)", plan["pending"])):
        if lst:
            out += ["", f"### {label}", ""] + [f"- `{k}`: {why}" for k, why in lst]
    if plan["missing"]:
        out += ["", "### Ranked archetypes with no decided design", ""] + [f"- `{a}`" for a in plan["missing"]]
    out += ["", "## Section 8 proposals beside the resolved fill", ""]
    rowmap = {r["doc_category"]: r for r in res["rows"]}
    for s in plan["shipped"]:
        d = s["design"]
        prop = res["props"].get(d["design_key"])
        if not prop:
            out.append(f"- `{d['design_key']}`: seeded design -- keeps its base reasoning row (section 9)")
            continue
        r = rowmap.get(d["Reasoning Key"])
        st = prop["style"]
        pal = ", ".join(k for k, _e in prop["palettes"][:3]) or "none"
        out.append(f"- `{d['design_key']}` ({s['archetype']}): style proposal {st['Table Rules']}/{st['Table Fills']}/"
                   f"{st['Emphasis Mechanism']}/rule-brand {st['Rule Brand pt']}pt; reuse candidates: "
                   f"{', '.join(prop['reuse'][:4]) or 'none (new row)'}; palette candidates: {pal}; "
                   f"typeface candidates: {', '.join(prop['typefaces']) or 'none'}; "
                   f"resolved: style `{r['Style Key']}`, palette `{r['Palette Key']}`, typeface `{r['Typeface Key']}`")
        for note in prop["notes"]:
            out.append(f"  - {note}")
    if res["blanked"]:
        out += ["", "## Bias tokens blanked because the design contradicts them (R7-8)", ""]
        out += [f"- `{k}` {col}: `{tok}` ({why})" for k, col, tok, why in res["blanked"]]
    out.append("")
    return "\n".join(out)


# -------------------------------------------------------------------- 82b A5 borrowing (separate mode)

def _doctype_keys(family: str) -> dict:
    """{style, palette, page formats} of every base doctype of `family`, via its Reasoning Key."""
    reasoning = {r["doc_category"]: r for r in _lib_rows("doc-reasoning")}
    keys = {"style": set(), "palette": set(), "page_format": set()}
    with (SKILL_DATA / "doctypes.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["Family"] != family or r.get("Brand Scope", "generic") != "generic":
                continue
            dr = reasoning.get(r["Reasoning Key"], {})
            keys["style"].add(dr.get("Style Key", ""))
            keys["palette"].add(dr.get("Palette Key", ""))
            keys["page_format"].add(r["Page Format Key"])
    return keys


def twin_check(family: str, source: str) -> tuple:
    """82b A5: borrowing only between structural twins -- the same shipped Style, Palette and Page
    Format keys. Returns (is_twin, family keys, source keys)."""
    a, b = _doctype_keys(family), _doctype_keys(source)
    return (a == b and all(a.values())), a, b


def borrow_proposal(family: str, source: str, limit: int = 3) -> list:
    """The source family's best non-convention designs, labelled `borrowed:`, max 3 (A5); they rank
    AFTER the family's own evidence."""
    path = DESIGNS / f"{source}.csv"
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["Evidence Class"] != "convention"]
    rows.sort(key=lambda r: int(r["Rank"]))
    return [{"borrowed_from": r["design_key"], "Display Name": r["Display Name"], "Source Rank": r["Rank"],
             "Evidence Class": r["Evidence Class"], "label": "borrowed:" + r["design_key"]} for r in rows[:limit]]


def cmd_borrow(family: str, source: str) -> int:
    ok, fam_keys, src_keys = twin_check(family, source)
    print(f"[{family} <- {source}] structural twins (same Style, Palette, Page Format keys): "
          f"{'YES' if ok else 'NO'}")
    print(f"  {family}: {fam_keys}")
    print(f"  {source}: {src_keys}")
    if not ok:
        print("  82b A5 allows borrowing only between twins -- nothing proposed")
        return 0
    for p in borrow_proposal(family, source):
        print(f"  {p['label']}  ({p['Display Name']}, source rank {p['Source Rank']}, {p['Evidence Class']})")
    print("  (dry-run: nothing written; these rank after the family's own evidence, max 3)")
    return 0


def outputs_root() -> Path:
    return RES


def cmd_write(family: str) -> int:
    spec = load_spec(family)
    if spec is not None:
        bad = resolve_family(family, spec)["violations"]
        if bad:
            print(f"[{family}] refusing to write: the spec disagrees with the engine (R7-4):")
            for v in bad:
                print("  -", v)
            return 1
    files = build(family)
    for rel, text in files.items():
        path = RES / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        print("wrote", path, len(text.splitlines()), "lines")
    return 0


def cmd_check(family: str) -> int:
    """R7-4: FAIL when the spec differs from the engine's proposal without a ratified override; then rebuild
    in memory and compare each CSV byte-for-byte with the committed file."""
    bad = 0
    spec = load_spec(family)
    if spec is None:
        raise SystemExit(f"no fill-specs/{family}.json")
    for v in resolve_family(family, spec)["violations"]:
        print("VIOLATION", v)
        bad += 1
    for rel, text in build(family).items():
        if rel.endswith(".md"):
            continue
        path = RES / rel
        same = path.is_file() and path.read_bytes() == text.encode("utf-8")
        print(("same   " if same else "DIFFERS"), rel)
        bad += not same
    return 1 if bad else 0


# ============================================================================== CLI plumbing

def load_spec(family: str):
    path = SPECS / f"{family}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def dry_run(family: str) -> int:
    spec = load_spec(family)
    if spec:
        corpora = [dict(c) for c in spec["corpora"]]
        for c in corpora:
            c["items"] = load_corpus(c)
        recodes = spec.get("recodes", [])
    else:
        corpora = discover_corpora(family)
        recodes = sorted(p.name for p in HERE.glob(f"{family}-*recode*.md"))
    items = []
    for c in corpora:
        got = c["items"]
        warn = f"  ! {c['skipped_rows']} table row(s) skipped (cell count differs from header)"             if c.get("skipped_rows") else ""
        print(f"  corpus {c['id']:<6} {c['file']} [{c.get('section', '')[:40]}]: {len(got)} coded items "
              f"({sum(i.admissible for i in got)} admissible), N={c.get('n', len(got))}{warn}")
        items += got
    if not items:
        print(f"[{family}] no coded table could be parsed from the evidence files -- nothing to rank")
        return 1
    identity = spec_identity(spec) if spec else identity_for(items)
    changes = apply_recodes(items, recodes) if recodes else []
    print(f"  identity features: {'|'.join(identity)}; recode overrides applied: {len(changes)} from {recodes or 'none'}")
    for note in gate_notes(family)[:6]:
        print(f"  gate: {note}")
    for c in corpora:
        c.setdefault("n", len(c["items"]))
    table = combined_table(items, corpora, identity)
    used_identity = identity
    cap = (spec or {}).get("step1_cap", CAP)
    order, dropped = rank_step1(table, corpora, cap=cap)
    lib = Library(family)
    n_of = {c['id']: c['n'] for c in corpora}
    dropped_v = frozenset(dropped_variants(family, spec))
    default_style = family_default_style(family)
    if dropped_v:
        print(f"  variants dropped by the gate (family default used): {', '.join(sorted(dropped_v))}")
    print(f"\n[{family}] proposed step-1 ranking (K>=2 admissible exemplars; cap {cap}):")
    for n, a in enumerate(order, 1):
        r = table[a]
        shares = " ".join(f"{c['id']}:{r['k'][c['id']]}/{c['n']}" for c in corpora if r["k"][c["id"]])
        prop = section8_proposal(family, a, r["ex"], used_identity, lib, dropped_v, default_style, n_of)
        st = prop["style"]
        print(f"  {n:>2}. {a:<40} combined {r['combined']:.4f}  K={r['K']} (inadmissible not counted: {r['inadm']})  {shares}")
        print(f"      style {st['Table Rules']}/{st['Emphasis Mechanism']}/brand {st['Rule Brand pt']}pt "
              f"reuse={','.join(prop['reuse'][:3]) or 'new'}  palette={','.join(k for k, _e in prop['palettes'][:2]) or '-'}  "
              f"typeface={','.join(prop['typefaces']) or '-'}")
        for note in prop["notes"]:
            print(f"        note: {note}")
    if not order:
        print("  (no archetype reaches K>=2 with an admissible exemplar; singletons/L3/convention per section 6 "
              "steps 2-4 are decisions)")
    if dropped:
        print(f"  ({len(dropped)} further eligible archetype(s) fall outside the cap)")
    print("  (dry-run: nothing written)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--family", required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="print the proposed ranking, write nothing")
    mode.add_argument("--write", action="store_true", help="write the section-9 outputs from fill-specs/<family>.json")
    mode.add_argument("--check", action="store_true", help="rebuild in memory and diff against committed files")
    mode.add_argument("--borrow-from", metavar="SOURCE_FAMILY",
                      help="82b A5 mode: propose designs borrowed from a structural-twin family (dry-run only)")
    args = ap.parse_args(argv)
    if args.borrow_from:
        return cmd_borrow(args.family, args.borrow_from)
    if args.dry_run:
        return dry_run(args.family)
    if args.write:
        return cmd_write(args.family)
    return cmd_check(args.family)


if __name__ == "__main__":
    sys.exit(main())
