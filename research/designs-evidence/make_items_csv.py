#!/usr/bin/env python3
"""
Write <family>-items.csv (82a C11): id, name, url, preview_url -- one row per CODED item.

Reads the first-coder evidence files and touches ONLY the id/position, name, repo/source URL
and preview URL columns. Feature columns, admissibility and notes are never read into the
output or printed. Tables are recognised by their header cells, never by row content:

  - a "coded" table has an `Admissible`/`adm` header (the feature table);
  - a "sources" table has a `Preview URL...` header and no admissibility column.

Coded ids come from the coded table (explicit `id` column, or LABEL:NNN from `Pos`).
URL / preview are taken from the coded table if it carries them, else joined from the
sources table by the same id.

Usage:  python3 make_items_csv.py            # writes cv-, deck- and invoice-items.csv
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

FAMILIES = {
    "cv": [("GH", "cv-corpus-github.md"), ("NPM", "cv-corpus-npm-ms.md")],
    "deck": [("NPM", "deck-corpus-npm.md"), (None, "deck-corpus-lo-ms.md")],
    # LO is corroborate-only (no coded table).
    "invoice": [(None, "invoice-corpus.md")],
}

# Items with no per-item page get the catalogue they were listed on (evidence file, "Source").
CATALOGUE_URL = {
    ("invoice", "MS"): "https://create.microsoft.com/en-us/templates/invoices",
}

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
    return re.sub(r"[`*]", "", s).strip()


def url_of(s):
    s = clean(s)
    if not s or s == "-":
        return ""
    parts = [p.strip() for p in s.split(";") if p.strip()]
    parts = [p if p.startswith("http") else "https://" + p for p in parts]
    return "; ".join(parts)


def row_id(header, row, label):
    j = col(header, "id")
    if j is not None:
        return clean(row[j])
    j = col(header, "pos", "rank")
    digits = re.sub(r"[^0-9]", "", row[j])
    return f"{label}:{int(digits):03d}"


def extract(label, path):
    coded, sources = [], {}
    for header, rows in tables(path):
        has_adm = col(header, "admissible", "adm") is not None
        pv = col(header, "preview url", "thumbnail url")
        if has_adm and (col(header, "id") is not None or col(header, "pos") is not None):
            name_j = col(header, "repo", "package", "item", "template")
            url_j = col(header, "source url")
            for r in rows:
                rid = row_id(header, r, label)
                raw = r[name_j]
                m = LINK.search(raw)
                name = m.group(1) if m else clean(raw)
                url = m.group(2) if m else (url_of(r[url_j]) if url_j is not None else "")
                if not url and col(header, "repo") == name_j:
                    url = "https://github.com/" + name
                coded.append({"id": rid, "name": name, "url": url,
                              "preview_url": url_of(r[pv]) if pv is not None else ""})
        elif pv is not None and not has_adm:
            repo_j = col(header, "repo")
            for r in rows:
                sources[row_id(header, r, label)] = (
                    url_of(r[repo_j]) if repo_j is not None else "", url_of(r[pv]))
    for item in coded:
        if item["id"] in sources:
            u, p = sources[item["id"]]
            item["url"] = item["url"] or u
            item["preview_url"] = item["preview_url"] or p
    return coded


def main():
    for fam, files in FAMILIES.items():
        items = []
        for label, name in files:
            got = extract(label, HERE / name)
            print(f"{fam}: {name}: {len(got)} coded items")
            items += got
        for i in items:
            i["url"] = i["url"] or CATALOGUE_URL.get((fam, i["id"].split(":")[0]), "")
        ids =[i["id"] for i in items]
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
