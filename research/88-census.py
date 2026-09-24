#!/usr/bin/env python3
"""research/88 census: run `ddi.py resolve --query` on plain generic requests (no region or
variant cue) and print status + top-2 candidates. Usage: python3 research/88-census.py"""
import contextlib
import io
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skill" / "document-design-intelligence" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import resolve  # noqa: E402

QUERIES = {
    "cv": ["make me a CV for a marketing coordinator", "write my resume", "I need a curriculum vitae",
           "fais-moi un CV pour un poste de comptable", "erstelle einen Lebenslauf fuer eine Bewerbung"],
    "cover-letter": ["write my cover letter for a project manager job", "I need a motivation letter", "help me with a cover letter"],
    "letter": ["write a formal letter to my landlord", "I need a business letter", "ecris une lettre a mon proprietaire",
               "schreibe einen Brief an das Amt"],
    "memo": ["write a memo about the new office hours", "internal note to staff", "draft a memo"],
    "form": ["make a form for new clients to fill in", "I need a registration form", "create a fillable form"],
    "brochure": ["make a brochure for my dental clinic", "design a brochure for our tours", "I need a brochure"],
    "flyer": ["make a flyer for my bake sale", "design a flyer for a concert", "I need a flyer"],
    "poster": ["make a poster for our school fair", "design an event poster", "I need a poster"],
    "report": ["write a report on quarterly sales", "format my annual report", "I need a report"],
    "whitepaper": ["write a whitepaper about cloud security", "make a white paper", "I need a whitepaper"],
    "proposal": ["write a proposal for a website redesign", "make a project proposal", "I need a business proposal"],
    "quote": ["make a quote for a kitchen renovation", "prepare a price quotation", "fais-moi un devis pour une renovation",
              "erstelle ein Angebot fuer eine Renovierung"],
    "invoice": ["make an invoice for my consulting work", "I need an invoice", "fais-moi une facture",
                "erstelle eine Rechnung"],
    "deck": ["make slides for my team meeting", "build a presentation about our results", "I need a slide deck",
             "fais-moi une presentation", "erstelle eine Praesentation"],
    "one-pager": ["make a one pager about our product", "I need a one page summary", "create a fact sheet"],
    "infographic": ["make an infographic about recycling", "I need an infographic", "create a visual summary of our data"],
}

# round 3: a family noun plus incidental words (paper, page, size, print, US, A4, letter-size,
# template, simple, professional, modern, one, two) -- expected family in the key.
INCIDENTAL = [
    ("brochure", "make a brochure on 8.5x11 paper"), ("brochure", "I need a simple brochure template"),
    ("brochure", "design a modern brochure for print"), ("brochure", "professional brochure, two pages"),
    ("flyer", "make a flyer on 8.5x11 paper"), ("flyer", "flyer for US paper"),
    ("flyer", "a simple flyer template"), ("flyer", "professional flyer one page A4"),
    ("poster", "make a poster on A4 paper"), ("poster", "modern poster for print, large size"),
    ("report", "write a report, two page summary"), ("report", "professional report template"),
    ("whitepaper", "write a whitepaper, professional and modern"), ("whitepaper", "white paper template"),
    ("cv", "make a simple one page CV template"), ("cv", "professional CV on A4 paper"),
    ("invoice", "make a simple invoice template on A4 paper"), ("quote", "modern price quote, one page"),
    ("letter", "write a formal letter on letter-size paper"), ("cover-letter", "simple cover letter template, one page"),
    ("one-pager", "make a one pager on US letter paper"), ("form", "make a printable form on A4 paper"),
    ("deck", "modern slide deck template"), ("memo", "a one page memo on company paper"),
]



# round 4 (research/89 R5 review): repro queries with the EXPECTED DOCTYPE (not just family).
# Third column = expected `language.value` ("" = don't care).
R5 = [
    # F2 "letter" as a paper size must not name the letter family
    ("report on letter paper", "report-short", ""), ("memo on letter paper", "memo-internal", ""),
    ("a memo on US letter paper", "memo-internal", ""), ("invoice on letter paper", "invoice-tabular", ""),
    # F3 name particles must not flip language / region
    ("CV for Maria de la Cruz", "cv-generic", "en"), ("CV for Jean-Luc de la Fontaine", "cv-generic", "en"),
    ("resume for Anna von der Leyen", "cv-generic", "en"),
    ("CV for a cafe manager", "cv-*", "en"), ("a flyer for le petit cafe", "brochure-flyer-a4", "en"),
    # F4 US cue: pronoun "us" is not a size cue; "U.S." is
    ("make a flyer for us", "brochure-flyer-a4", ""), ("brochure for us", "brochure-trifold-a4", ""),
    ("flyer for the U.S. office", "brochure-flyer-letter", ""), ("a flyer for the US market", "brochure-flyer-letter", ""),
    # F5 query language applies on the direct BM25 path too
    ("fais-moi une presentation", "slide-deck-projection", "fr"), ("erstelle eine Praesentation", "slide-deck-projection", "de"),
    ("redige un rapport long avec sommaire", "report-long-toc", "fr"),
    # F6 plurals
    ("flyers", "brochure-flyer-a4", ""), ("invoices", "invoice-tabular", ""), ("posters", "poster", ""),
    ("CVs for my team", "cv-generic", ""),
    # F9 French with a non-France cue -> eu-generic, lang fr; no cue -> cv-france (orchestrator ruling)
    ("fais-moi un CV pour un poste a Bruxelles, Belgique", "cv-eu-generic", "fr"),
    ("redige mon CV pour Geneve en Suisse", "cv-eu-generic", "fr"),
    ("fais-moi un CV pour le Quebec", "cv-eu-generic", "fr"),
    ("fais-moi un CV pour un poste de comptable", "cv-france", "fr"),
    # F11 --lang feeds doctype choice (run separately in tests); F10 backlog: explicit A4 should win
    ("professional flyer one page A4", "brochure-flyer-a4", ""),
]
# F7 multi-family: expected to ABSTAIN with reason multiple-families
R5_MULTI = ["a CV and a cover letter", "slides for the report", "deck builder CV"]


def run_lang(query):
    """Like run() but also returns language.value ("" when abstained)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = resolve.main(["--query", query, "--json"])
    out = json.loads(buf.getvalue())
    if out.get("status") == "resolved":
        return "RESOLVED", [out["resolved"]["doctypes"][0]["key"]], out.get("language", {}).get("value", "")
    cands = out.get("candidates", [])
    return ("ABSTAIN(" + str(out.get("reason", "")) + ")",
            [f"{c['key']} {c.get('score', c.get('family', ''))}" for c in cands[:3]], "")


def run(query):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = resolve.main(["--query", query, "--json"])
    out = json.loads(buf.getvalue())
    if out.get("status") == "resolved":
        return "RESOLVED", [out["resolved"]["doctypes"][0]["key"]]
    cands = out.get("candidates", [])
    return "ABSTAIN(" + str(out.get("reason", "")) + ")", [f"{c['key']} {c['score']}" for c in cands[:2]]


def main():
    print("| family | query | status | top |")
    print("|---|---|---|---|")
    bad = 0
    for fam, qs in QUERIES.items():
        for q in qs:
            status, top = run(q)
            bad += status != "RESOLVED"
            print(f"| {fam} | {q} | {status} | {'; '.join(top)} |")
    print(f"\nnot resolved: {bad}/{sum(len(v) for v in QUERIES.values())}")
    print("\n### incidental-word requests (expected family in first column)\n")
    print("| expected family | query | status | top |")
    print("|---|---|---|---|")
    wrong = 0
    for fam, q in INCIDENTAL:
        status, top = run(q)
        ok = status == "RESOLVED" and fam.split("-")[0] in top[0]
        wrong += not ok
        print(f"| {fam} | {q} | {status} | {'; '.join(top)}{'' if ok else '  <-- WRONG/ABSTAIN'} |")
    print(f"\nwrong or abstained: {wrong}/{len(INCIDENTAL)}")
    print("\n### R5 repro queries (expected doctype [language])\n")
    print("| query | expected | status | got | ok |")
    print("|---|---|---|---|---|")
    wrong5 = 0
    for q, key, lang in R5:
        status, top, got_lang = run_lang(q)
        ok = (status == "RESOLVED" and (top[0] == key or (key.endswith("*") and top[0].startswith(key[:-1])))
              and (not lang or got_lang == lang))
        wrong5 += not ok
        exp = key + (" [" + lang + "]" if lang else "")
        got = "; ".join(top) + (" [" + got_lang + "]" if got_lang else "")
        print(f"| {q} | {exp} | {status} | {got} | {'ok' if ok else 'WRONG'} |")
    print(f"\nR5 wrong or abstained: {wrong5}/{len(R5)}")
    print("\n### R5 multi-family queries (expected: ABSTAIN(multiple-families))\n")
    print("| query | status | top |")
    print("|---|---|---|")
    for q in R5_MULTI:
        status, top, _ = run_lang(q)
        print(f"| {q} | {status} | {'; '.join(top)} |")


if __name__ == "__main__":
    main()
