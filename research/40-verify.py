import csv

BASE = r"C:\Users\ysuliman\Documents\Ai plugin"

expected_base_cols = ["heading_key", "canonical_section", "Heading Text", "Language", "Is Primary"]
expected_t40_cols = ["canonical_section", "heading_text", "language", "is_primary", "source"]


def read(path, expected_cols):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == expected_cols, (path, reader.fieldnames)
        return list(reader)


base_rows = read(BASE + r"\skill\document-design-intelligence\data\base\headings.csv", expected_base_cols)
t39_rows = read(BASE + r"\research\39-headings-transactional-draft.csv", expected_base_cols)
t40_rows = read(BASE + r"\research\40-headings-longform-draft.csv", expected_t40_cols)

# t40 uses research/18's raw draft shape (canonical_section, heading_text, language,
# is_primary, source). load-base.py generates heading_key itself as <section>-<lang>-<n>,
# n 1-based within (section, language) in file order -- mirror that here so the check
# reflects what will actually land in data/base/, not the draft file as typed.
t40_normalised = []
seen_n = {}
for r in t40_rows:
    key = (r["canonical_section"], r["language"])
    seen_n[key] = seen_n.get(key, 0) + 1
    t40_normalised.append({
        "heading_key": "%s-%s-%d" % (r["canonical_section"], r["language"], seen_n[key]),
        "canonical_section": r["canonical_section"],
        "Heading Text": r["heading_text"],
        "Language": r["language"],
        "Is Primary": r["is_primary"],
        "_source": r["source"],
    })

all_rows = []
for name, rows in (("base", base_rows), ("t39", t39_rows), ("t40", t40_normalised)):
    for r in rows:
        r = dict(r)
        r["_source_file"] = name
        all_rows.append(r)

# check 2: no duplicate heading_key across all three sources (generated, for t40)
keys = [r["heading_key"] for r in all_rows]
dupes = sorted({k for k in keys if keys.count(k) > 1})
print("Check 2 - duplicate heading_key across base+t39+t40 (t40 keys as load-base.py "
      "would generate them):", dupes if dupes else "NONE")


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


primary_check(t40_normalised, "new file only (t40)")
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

print("Check 4 - headings-draft.csv header match (research/18 shape):", expected_t40_cols)
print("Check 4 - section-orders.csv header match:", ["structure_key", "Section Order"])

# every t40 row has a non-empty source (loader files blanks under "(none given)" --
# every row here should be a deliberate citation, not a silent gap)
blank_source = [r["canonical_section"] + "/" + r["language"] for r in t40_rows if not r["source"].strip()]
print("Check 5 - t40 rows with blank source:", blank_source if blank_source else "NONE")
