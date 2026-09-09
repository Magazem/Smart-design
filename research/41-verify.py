import csv

BASE = r"C:\Users\ysuliman\Documents\Ai plugin"

expected_base_cols = ["heading_key", "canonical_section", "Heading Text", "Language", "Is Primary"]
expected_draft_cols = ["canonical_section", "heading_text", "language", "is_primary", "source"]


def read(path, expected_cols):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == expected_cols, (path, reader.fieldnames)
        return list(reader)


base_rows = read(BASE + r"\skill\document-design-intelligence\data\base\headings.csv", expected_base_cols)
t39_rows = read(BASE + r"\research\39-headings-transactional-draft.csv", expected_draft_cols)
t40_rows = read(BASE + r"\research\40-headings-longform-draft.csv", expected_draft_cols)
t41_rows = read(BASE + r"\research\41-headings-marketing-draft.csv", expected_draft_cols)


def normalise(rows, tag):
    out = []
    seen_n = {}
    for r in rows:
        key = (r["canonical_section"], r["language"])
        seen_n[key] = seen_n.get(key, 0) + 1
        out.append({
            "heading_key": "%s-%s-%d" % (r["canonical_section"], r["language"], seen_n[key]),
            "canonical_section": r["canonical_section"],
            "Heading Text": r["heading_text"],
            "Language": r["language"],
            "Is Primary": r["is_primary"],
            "_source": r["source"],
        })
    return out


# single shared counter per (canonical_section, language) across ALL FOUR sources,
# in source order (base, t39, t40, t41) -- matches load-base.py's load order.
all_normalised = []
seen_n = {}
for name, rows, is_base in (("base", base_rows, True), ("t39", t39_rows, False),
                             ("t40", t40_rows, False), ("t41", t41_rows, False)):
    for r in rows:
        if is_base:
            key = (r["canonical_section"], r["Language"])
            seen_n[key] = seen_n.get(key, 0) + 1
            all_normalised.append({
                "heading_key": "%s-%s-%d" % (r["canonical_section"], r["Language"], seen_n[key]),
                "canonical_section": r["canonical_section"],
                "Heading Text": r["Heading Text"],
                "Language": r["Language"],
                "Is Primary": r["Is Primary"],
                "_source_file": name,
            })
        else:
            key = (r["canonical_section"], r["language"])
            seen_n[key] = seen_n.get(key, 0) + 1
            all_normalised.append({
                "heading_key": "%s-%s-%d" % (r["canonical_section"], r["language"], seen_n[key]),
                "canonical_section": r["canonical_section"],
                "Heading Text": r["heading_text"],
                "Language": r["language"],
                "Is Primary": r["is_primary"],
                "_source_file": name,
            })

# check 2: no duplicate heading_key across base+t39+t40+t41 (single shared counter)
keys = [r["heading_key"] for r in all_normalised]
dupes = sorted({k for k in keys if keys.count(k) > 1})
print("Check 2 - duplicate heading_key across base+t39+t40+t41 (shared counter):", dupes if dupes else "NONE")


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


t41_normalised = normalise(t41_rows, "t41")
primary_check(t41_normalised, "new file only (t41)")
primary_check(all_normalised, "union of base+t39+t40+t41")

# check 1: every Section Order token resolves against base + t39 + t40 + t41 canonical_section
canonical_sections = {r["canonical_section"] for r in all_normalised}

so_path = BASE + r"\research\41-t10-section-orders-marketing.csv"
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

print("Check 4 - headings-draft.csv header match (research/18 shape):", expected_draft_cols)
print("Check 4 - section-orders.csv header match:", ["structure_key", "Section Order"])

blank_source = [r["canonical_section"] + "/" + r["language"] for r in t41_rows if not r["source"].strip()]
print("Check 5 - t41 rows with blank source:", blank_source if blank_source else "NONE")

# check that all six expected structure_keys are present, exactly once
expected_keys = {"brochure-3panel", "brochure-gatefold", "flyer-single-sheet",
                  "poster-single-canvas", "deck-standard", "cover-letter-standard"}
actual_keys = [r["structure_key"] for r in so_rows]
print("Check 6 - structure_key set matches the six, no dupes:",
      "OK" if sorted(actual_keys) == sorted(expected_keys) and len(actual_keys) == len(set(actual_keys)) else (actual_keys, expected_keys))
