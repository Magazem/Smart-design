#!/usr/bin/env python3
"""Write <family>-items.csv (82a C11) for brochure, flyer, memo, form.

Prints/writes ONLY id, name, url, preview_url -- one row per CODED item (a row
in the family's own "coded" pipe table that is not marked removed-from-N).
Feature columns (panels/columns, head, body, colour, header, rules, dens,
reason/note, admissible, field, etc.) are parsed only to locate the id/adm/
preview cells; their VALUES are never read into a variable used for output,
never printed, and the rest of each row's cells are discarded immediately
after the id/adm/preview cells are pulled out.

Sources read (evidence files, first-coder tables only -- never inspected for
feature codes beyond what is needed to find id/adm/preview cells):
  - brochure-corpus.md: B.2 raw list (id, Item link) + B.3 coded table (id, adm, preview)
  - flyer-corpus.md:    F.2 raw list (id, Template link) + F.3 coded table (id, adm, thumbnail)
  - memo-corpus.md:     no coded table exists (M.2 is corroboration only, explicitly
                        "NOT counted, NOT ranked, no admissibility applied") -> 0 rows
  - form-corpus.md:     Fm.3 coded table (id, Authority, no preview col) + Fm.1
                        source table (Authority -> pages fetched), joined on Authority
                        name since form items are L3 authority pages, not raster previews

Usage: python3 make_items_csv_82ag.py
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep(row):
    return row and all(re.fullmatch(r":?-{2,}:?", c) for c in row if c)


def tables(path):
    """Yield (header, rows) for every pipe table in the file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and is_sep(cells(lines[i + 1])):
            header = [h.lower() for h in cells(lines[i])]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            yield header, rows
        else:
            i += 1


def col(header, *names):
    for n in names:
        for j, h in enumerate(header):
            if h == n or h.startswith(n):
                return j
    return None


def clean(s):
    return re.sub(r"[`*]", "", s or "").strip()


def name_url(cell):
    """Split a markdown-link cell into (name, url); plain text -> (text, '')."""
    c = clean(cell)
    m = LINK.search(c)
    if m:
        return m.group(1), m.group(2)
    return c, ""


def brochure(path):
    raw_name = {}
    for header, rows in tables(path):
        if col(header, "id") is not None and col(header, "item") is not None and col(header, "adm") is None:
            id_j, item_j = col(header, "id"), col(header, "item")
            for r in rows:
                rid = clean(r[id_j])
                if rid:
                    raw_name[rid] = name_url(r[item_j])
    items = []
    for header, rows in tables(path):
        adm_j = col(header, "adm")
        id_j = col(header, "id")
        pv_j = col(header, "preview")
        if adm_j is None or id_j is None or pv_j is None:
            continue
        for r in rows:
            rid = clean(r[id_j])
            adm = clean(r[adm_j])
            if not rid or adm == "-":
                continue  # not a coded item (removed from N)
            name, url = raw_name.get(rid, (rid, ""))
            items.append({"id": rid, "name": name, "url": url, "preview_url": clean(r[pv_j])})
        break  # only the first adm-bearing table (B.3)
    return items


def flyer(path):
    raw_name = {}
    for header, rows in tables(path):
        if col(header, "id") is not None and col(header, "template") is not None and col(header, "adm") is None:
            id_j, item_j = col(header, "id"), col(header, "template")
            for r in rows:
                rid = clean(r[id_j])
                if rid:
                    raw_name[rid] = name_url(r[item_j])
    items = []
    seen = set()
    for header, rows in tables(path):
        adm_j = col(header, "adm")
        id_j = col(header, "id")
        pv_j = col(header, "thumbnail", "preview")
        item_j = col(header, "template")
        if adm_j is None or id_j is None or pv_j is None:
            continue
        for r in rows:
            rid = clean(r[id_j])
            adm = clean(r[adm_j])
            if not rid or adm == "-" or rid in seen:
                continue
            seen.add(rid)
            if item_j is not None and LINK.search(r[item_j]):
                name, url = name_url(r[item_j])
            else:
                name, url = raw_name.get(rid, (rid, ""))
            items.append({"id": rid, "name": name, "url": url, "preview_url": clean(r[pv_j])})
    return items


def memo(path):
    # M.2 (the original ~35-line file) is explicit corroboration only ("NOT counted, NOT
    # ranked, no admissibility applied"). Design Researcher 3's M.6 addendum (82b A1) added
    # a real coded table (M.6.2, id | source (pos) | template | ... | adm | ... | preview),
    # already coded under research/82a-general.md itself (M.6, "Coded from the start under
    # research/82a-general.md"), so this extracts it like brochure/flyer's coded tables.
    items = []
    seen = set()
    for header, rows in tables(path):
        id_j = col(header, "id")
        adm_j = col(header, "adm")
        item_j = col(header, "template")
        pv_j = col(header, "preview")
        if id_j is None or adm_j is None or item_j is None or pv_j is None:
            continue
        for r in rows:
            rid = clean(r[id_j])
            adm = clean(r[adm_j])
            if not rid or adm == "-" or rid in seen:
                continue
            seen.add(rid)
            name, url = name_url(r[item_j])
            pv = clean(r[pv_j])
            items.append({"id": rid, "name": name, "url": url or pv, "preview_url": pv})
    return items


def form(path):
    pages = {}
    for header, rows in tables(path):
        if col(header, "authority") is not None and col(header, "pages fetched") is not None:
            a_j, p_j = col(header, "authority"), col(header, "pages fetched")
            for r in rows:
                a = clean(r[a_j])
                if a:
                    first_url = re.search(r"https?://\S+", r[p_j])
                    pages[a] = clean(first_url.group(0)).rstrip("`,") if first_url else ""
    items = []
    seen = set()
    for header, rows in tables(path):
        id_j = col(header, "id")
        auth_j = col(header, "authority")
        adm_j = col(header, "admissible", "adm")
        if id_j is None or auth_j is None or adm_j is None:
            continue
        for r in rows:
            rid = clean(r[id_j])
            if not rid or rid in seen:
                continue
            seen.add(rid)
            auth = clean(r[auth_j])
            page = pages.get(auth)
            if page is None:
                first_word = auth.split()[0] if auth.split() else auth
                for k, v in pages.items():
                    if k.startswith(auth) or auth.startswith(k) or first_word in k:
                        page = v
                        break
            page = page or ""
            items.append({"id": rid, "name": auth, "url": page, "preview_url": page})
    return items


FAMILIES = {
    "brochure": ("brochure-corpus.md", brochure),
    "flyer": ("flyer-corpus.md", flyer),
    "memo": ("memo-corpus.md", memo),
    "form": ("form-corpus.md", form),
}


def main():
    for fam, (fname, fn) in FAMILIES.items():
        path = HERE / fname
        items = fn(path)
        ids = [i["id"] for i in items]
        dup = {x for x in ids if ids.count(x) > 1}
        if dup:
            sys.exit(f"{fam}: duplicate ids {sorted(dup)}")
        out = HERE / f"{fam}-items.csv"
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["id", "name", "url", "preview_url"], lineterminator="\n")
            w.writeheader()
            w.writerows(items)
        missing = sum(1 for i in items if not i["preview_url"])
        print(f"{fam}: wrote {out.name}: {len(items)} rows, {missing} without preview_url")


if __name__ == "__main__":
    main()
