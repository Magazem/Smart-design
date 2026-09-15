#!/usr/bin/env python3
"""research/heading_reach.py -- census of headings.csv rows reachable by an
actual (doctype, language) combination (research/64 D-E, A7).

"Reachable" means: the row's `canonical_section` is used by some structure's
or cv-region's `Section Order` that an actual doctype resolves (an "orphan"
row -- used by no doctype at all -- is a SEPARATE, pre-existing defect, not a
language failure, and is reported on its own rather than folded into the
language count), AND the row's `Language` is a language obtainable for that
doctype:

  BEFORE this fix: `structures."Heading Language"` was a hard-coded "en" on
  every row, so the only language ever resolved for ANY doctype was "en".
  AFTER: each doctype's own `Default Language` (doctypes.csv), PLUS every
  `resolve.py --lang` override (en/fr/de, any doctype) -- so a non-orphan
  section's heading row in ANY of the three languages becomes reachable.

Run from skill/document-design-intelligence/:
    python3 ../../research/heading_reach.py
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skill" / "document-design-intelligence"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(SKILL / "scripts" / "lib"))
import data as datalib  # noqa: E402

DATA_DIR = SKILL / "data"
LANGS = ("en", "fr", "de")


def main():
    manifest = datalib.load_manifest(DATA_DIR)
    tables = manifest["tables"]
    problems = datalib.ProblemLog()
    all_rows = datalib.load_all_tables(DATA_DIR, tables, problems)
    if problems:
        for line in problems.lines:
            print(line)
        return 1

    doctypes = all_rows["doctypes"]
    structures_by_key = {r["structure_key"]: r for r in all_rows["structures"]}
    headings = all_rows["headings"]
    cv_regions = all_rows["cv-regions"]

    sections_by_doctype = {}
    all_used_sections = set()
    for d in doctypes:
        sections = set()
        struct = structures_by_key.get(d.get("Structure Key", ""))
        if struct:
            sections |= {s for s in struct.get("Section Order", "").split(";") if s}
        region_key = d.get("Region Key", "")
        if region_key:
            for cvr in cv_regions:
                if cvr.get("region_key") == region_key:
                    sections |= {s for s in cvr.get("Section Order", "").split(";") if s}
        sections_by_doctype[d["doc_key"]] = sections
        all_used_sections |= sections

    def reachable_pairs(before):
        pairs = set()
        for d in doctypes:
            langs = {"en"} if before else set(LANGS)
            for section in sections_by_doctype[d["doc_key"]]:
                for lang in langs:
                    pairs.add((section, lang))
        return pairs

    def census(before):
        reachable = reachable_pairs(before)
        reached, unreached = [], []
        for h in headings:
            section = h["canonical_section"]
            if section not in all_used_sections:
                continue  # orphan, reported separately below
            target = (section, h["Language"])
            (reached if target in reachable else unreached).append(h["heading_key"])
        return reached, unreached

    orphans = [h["heading_key"] for h in headings
               if h["canonical_section"] not in all_used_sections]
    by_key = {h["heading_key"]: h for h in headings}

    before_reached, before_unreached = census(before=True)
    after_reached, after_unreached = census(before=False)

    def lang_breakdown(keys):
        counts = {lang: 0 for lang in LANGS}
        for k in keys:
            counts[by_key[k]["Language"]] += 1
        return ", ".join(f"{lang}={counts[lang]}" for lang in LANGS)

    print(f"headings.csv: {len(headings)} rows total, {len(orphans)} orphaned "
          f"(canonical_section used by no structure's/cv-region's Section Order "
          f"reachable from any doctype)")
    print()
    print("BEFORE (structures.'Heading Language' hard-coded 'en' on every row):")
    print(f"  reachable:   {len(before_reached)}  ({lang_breakdown(before_reached)})")
    print(f"  unreachable: {len(before_unreached)}  ({lang_breakdown(before_unreached)})")
    print()
    print("AFTER (doctypes.'Default Language' + resolve.py --lang override):")
    print(f"  reachable:   {len(after_reached)}  ({lang_breakdown(after_reached)})")
    print(f"  unreachable: {len(after_unreached)}  ({lang_breakdown(after_unreached)})")
    if after_unreached:
        print("  remaining unreachable (non-orphan) rows:")
        for hk in after_unreached:
            h = by_key[hk]
            print(f"    {hk}: canonical_section={h['canonical_section']} "
                  f"Language={h['Language']} -- no doctype resolves this section "
                  f"in this language even with --lang")
    print()
    if orphans:
        print(f"Orphaned rows ({len(orphans)}, separate pre-existing defect, "
              f"not a language failure -- their canonical_section is authored "
              f"in headings.csv but appears in no structure's or cv-region's "
              f"Section Order that any doctype resolves):")
        for hk in orphans:
            h = by_key[hk]
            print(f"    {hk}: canonical_section={h['canonical_section']!r} "
                  f"Language={h['Language']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
