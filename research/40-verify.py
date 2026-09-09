import csv

BASE = r"C:\Users\ysuliman\Documents\Ai plugin"

files = {
    "base": BASE + r"\skill\document-design-intelligence\data\base\headings.csv",
    "t39": BASE + r"\research\39-headings-transactional-draft.csv",
    "t40": BASE + r"\research\40-headings-longform-draft.csv",
}

expected_heading_cols = ["heading_key", "canonical_section", "Heading Text", "Language", "Is Primary"]

rows_by_source = {}
for name, path in files.items():
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == expected_heading_cols, (name, reader.fieldnames)
        rows_by_source[name] = list(reader)

all_rows = []
for name, rows in rows_by_source.items():
    for r in rows:
        r["_source"] = name
        all_rows.append(r)

# check 2: no duplicate heading_key across all three sources
keys = [r["heading_key"] for r in all_rows]
dupes = sorted({k for k in keys if keys.count(k) > 1})
print("Check 2 - duplicate heading_key across base+t39+t40:", dupes if dupes else "NONE")

# check 3a: exactly one Is Primary=yes per (canonical_section, Language) - new file only
def primary_check(rows, label):
    from collections import defaultdict
    primaries = defaultdict(list)
    all_langs = defaultdict(set)
    for r in rows:
        key = (r["canonical_section"], r["Language"])
        all_langs[r["canonical_section"]].add(r["Language"])
        if r["Is Primary"] == "yes":
            primaries[key].append(r["heading_key"])
    bad = {k: v for k, v in primaries.items() if len(v) != 1}
    missing_lang = {cs: langs for cs, langs in all_langs.items() if langs != {"en", "fr", "de"}}
    print(f"Check 3 - {label} - (section,lang) with != 1 primary:", bad if bad else "NONE")
    print(f"Check 3 - {label} - sections missing a language (not en/fr/de all three):", missing_lang if missing_lang else "NONE")

primary_check(rows_by_source["t40"], "new file only (t40)")
primary_check(all_rows, "union of base+t39+t40")

# check 1: every Section Order token resolves against base + t39 + t40 canonical_section
canonical_sections = {r["canonical_section"] for r in all_rows}

so_path = BASE + r"\research\40-t10-section-orders-longform.csv"
with open(so_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    assert reader.fieldnames == ["structure_key", "Section Order"], reader.fieldnames
    so_rows = list(reader)

unresolved = {}
for row in so_rows:
    tokens = row["Section Order"].split(";")
    missing = [t for t in tokens if t not in canonical_sections]
    if missing:
        unresolved[row["structure_key"]] = missing

print("Check 1 - unresolved Section Order tokens:", unresolved if unresolved else "NONE - all resolve")
print("Check 1 - structure_key -> token count:", {r["structure_key"]: len(r["Section Order"].split(";")) for r in so_rows})

print("Check 4 - headings.csv header match:", expected_heading_cols)
print("Check 4 - section-orders.csv header match:", ["structure_key", "Section Order"])
