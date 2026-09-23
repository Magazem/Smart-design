#!/usr/bin/env python3
"""Writes fixtures/T{1,2,3}-{pass,bad-hex,bad-order}.md -- hand-authored clean outputs plus two
one-change mutations each (an invented hex; two sections swapped). Re-run to regenerate."""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "fixtures"

T1 = """Doctype: cv-uk (UK region; experienced band, uk-experienced order). Design: CV -- Harvard
reverse-chronological (cv-us-uk-designed). Other designs for a designer's CV are listed in the pack;
tell me if you want one of them instead.

=== DOCUMENT ===
# Sam Okafor

## Contact
London | sam@okafor.design | 07700 900123 | okafor.design

## Summary
Graphic designer with six years' experience in branding, packaging and print.

## Experience
### Senior Designer, Northbank Studio (2021-now)
- Led the rebrand for 3 FTSE-250 clients.
- Managed 2 junior designers.

### Designer, Pixel & Pine (2018-2021)
- Packaging and print for retail.

## Education
### BA Graphic Design, Falmouth University (2018)

## Skills
Adobe CC, Figma, typography, art direction.

=== STYLE SHEET ===
```css
@page { size: 210mm 297mm; margin: 25mm; }
body { font-family: 'Source Sans 3', Arial, sans-serif; font-size: 10.5pt; line-height: 1.24;
       color: #1B1B1B; background: #FFFFFF; }
h1 { font-family: 'Source Serif 4', Georgia, serif; font-size: 20pt; }
h2 { font-family: 'Source Serif 4', Georgia, serif; font-size: 13pt;
     border-bottom: 1pt solid #1B1B1B; }
.rule { border-top: 0.5pt solid #CCCCCC; }
a { color: #005EA2; }
```
No file was produced; save the HTML and print it to PDF yourself.
"""

T2 = """Doctype: slide-deck-projection. Design: Slide deck, bold minimal (deck-generic).

=== DOCUMENT ===
# Loopa -- Seed Round

## Cover Page
### Loopa: freight invoice reconciliation, automated
- $2M seed round

## Agenda
- Problem, solution, traction, ask

## Problem Statement
### Reconciliation is manual
- Finance teams match invoices by hand
- Errors cost margin

## Proposed Solution
### Loopa automates matching
- B2B SaaS
- Freight invoices reconciled automatically

## Findings
### Traction
- $40k MRR
- 22% month-on-month growth

## Call to Action
### The ask
- Raising $2M

## Contact
- hello@loopa.example

=== STYLE SHEET ===
```css
body { font-family: Arial, sans-serif; background: #0F0F0F; color: #FFFFFF; }
h1 { font-size: 36pt; } p, li { font-size: 24pt; } .dense { font-size: 18pt; }
.accent { color: #FFD400; } .rule { border-top: 1pt solid #FFFFFF; }
```
Slide size 338.67 x 190.5 mm (13.333 x 7.5 in). No pptx file was produced.
"""

T3 = """Doctype : quote-devis. Design : Quote / devis, tabular (quote-devis).

=== DOCUMENT ===
# Devis

## Émetteur
Atelier Morel, SIRET 123 456 789 00012

## Devis pour
Mme Durand, 12 rue des Lilas, Lyon

## Détail du devis
Rénovation d'une salle de bain

## Détail des prestations
| Prestation | Montant |
|---|---|
| Dépose de l'existant | 850 € |
| Plomberie | 2 300 € |
| Carrelage | 1 900 € |

## Total
5 050 € HT

## Taxes
TVA 10 % : 505 €

## Date de validité
Devis valable 30 jours.

## Bon pour accord
Date et signature du client :

=== STYLE SHEET ===
```css
body { font-family: 'Public Sans', Arial, sans-serif; font-size: 11pt; line-height: 1.35;
       color: #1A1E22; background: #FFFFFF; }
h1 { font-size: 24pt; color: #22282E; }
table { border-top: 1pt solid #1A1E22; } th { border-bottom: 1pt solid #1A1E22; }
.legal { font-size: 8.5pt; color: #55606B; } .hair { border-top: 0.5pt solid #CED3D8; }
```
Aucun fichier n'a ete produit ; appliquez la feuille de style.
"""


def swap(text, a, b):
    la, lb = f"## {a}\n", f"## {b}\n"
    assert la in text and lb in text
    return text.replace(la, "@@A@@").replace(lb, la).replace("@@A@@", lb)


CASES = {
    "T1": (T1, "#005EA2", "#00A2FF", ("Contact", "Skills")),
    "T2": (T2, "#FFD400", "#FF8800", ("Agenda", "Findings")),
    "T3": (T3, "#22282E", "#123456", ("Total", "Taxes")),
}

for trial, (clean, real_hex, fake_hex, pair) in CASES.items():
    (OUT / f"{trial}-pass.md").write_text(clean, encoding="utf-8", newline="\n")
    assert real_hex in clean, (trial, real_hex)
    (OUT / f"{trial}-bad-hex.md").write_text(clean.replace(real_hex, fake_hex, 1), encoding="utf-8", newline="\n")
    (OUT / f"{trial}-bad-order.md").write_text(swap(clean, *pair), encoding="utf-8", newline="\n")
print("wrote", len(list(OUT.glob('*.md'))), "fixtures")
