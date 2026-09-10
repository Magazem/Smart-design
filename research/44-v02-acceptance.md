# v0.2 Acceptance Set — fifteen prompts, one per newly covered family

Run each prompt below against the uploaded skill (v0.2 ZIP), fresh, with nothing else attached.
Every prompt carries its own content inline — do not add a file or paste extra text. The
expected section order for each family is quoted verbatim from
`skill/document-design-intelligence/data/base/structures.csv` (checked programmatically, see
Verification below). A response is scored PASS/FAIL against the two lines given per prompt.

General FAIL conditions that apply to all fifteen, not repeated per prompt:
- Sections appear out of order, merged, or a section is dropped/added versus the expected order.
- The model produces content with no visible structural/section reasoning.
- A clarifying question that is generic ("What would you like me to make?") with no document-design
  framing (format, layout, page count, sections, branding, print).

A clarifying question is a PASS only if it reasons in document-design terms (e.g. "single-sided or
gate-fold?", "how many line items?", "print or on-screen?") **and** shows it already knows the
section set for this family.

---

## 1. Invoice — `invoice-standard` (German)

> Ich brauche eine Rechnung für unseren Kunden. Bitte alles sauber strukturieren.
>
> Rechnungssteller: Nordlicht Werkzeugbau GmbH, Hafenstraße 12, 20457 Hamburg, USt-IdNr. DE123456789
> Rechnungsempfänger: Baumann Maschinenbau AG, Industrieweg 4, 70565 Stuttgart
> Rechnungsnummer: RE-2026-0447, Rechnungsdatum: 03.09.2026, Leistungsdatum: 28.08.2026
> Positionen:
> 1. CNC-Frässpindel, Modell FS-220, Menge 2, Einzelpreis 1.840,00 €, Gesamt 3.680,00 €
> 2. Wartungsvertrag Q3 2026, Menge 1, Einzelpreis 650,00 €, Gesamt 650,00 €
> 3. Expressversand, Menge 1, Einzelpreis 95,00 €, Gesamt 95,00 €
> Zwischensumme: 4.425,00 €, USt (19 %): 840,75 €, Gesamtbetrag: 5.265,75 €
> Zahlungsbedingungen: zahlbar innerhalb von 14 Tagen netto, Bankverbindung IBAN DE12 3456 7890 1234 5678 90

**Expected section order:** issuer → bill-to → invoice-details → line-items → totals → tax → payment-terms
(German headings per the library: Rechnungssteller, Rechnungsempfänger, Rechnungsdetails, Positionen, Gesamtbetrag, Steuern, Zahlungsbedingungen)

**Pass:** Output (or clarifying question) keeps issuer and bill-to separate and first, line items before totals, tax broken out separately from totals, payment terms last — in German.
**Fail:** Tax folded into totals, payment terms merged into invoice-details, or the model answers in English without noting the German request.

---

## 2. Letter — `letter-standard` (French)

> Rédigez une lettre commerciale formelle. Voici le contenu :
>
> Expéditeur : Élise Fontaine, Directrice des Achats, Atelier Rivoli SARL, 14 rue de Rivoli, 75004 Paris
> Destinataire : M. Thomas Weber, Service Client, Solvex Distribution, 8 avenue Louise, 1050 Bruxelles
> Date : 9 septembre 2026
> Formule d'appel : Monsieur Weber,
> Corps : Nous vous écrivons pour signaler un retard de livraison de trois semaines sur la commande
> n° CMD-88213, passée le 2 août 2026. Ce retard perturbe notre planning de production. Nous vous
> demandons de confirmer une nouvelle date de livraison sous 5 jours ouvrés, faute de quoi nous nous
> réservons le droit d'annuler la commande sans frais.
> Formule de politesse : Nous vous prions d'agréer, Monsieur Weber, l'expression de nos salutations distinguées.

**Expected section order:** sender → recipient → date → salutation → body → closing
(French headings: Expéditeur, Destinataire, Date, Formule d'appel, Corps du texte, Formule de politesse)

**Pass:** All six sections present in this order, in French, with the complaint content placed under body and nowhere else.
**Fail:** Salutation and closing swapped, date dropped, or body content bled into the closing.

**Note — trap:** `letter-standard` and `cover-letter-standard` (prompt 15) share the *identical*
section order (sender;recipient;date;salutation;body;closing). This is not in the brief's listed
trap pair but is the same situation as brochure-3panel/gatefold: the two families are told apart by
tone/register and other model dimensions, not by section order. Don't mark this prompt's or
prompt 15's output wrong just because the orders match — they're supposed to.

---

## 3. Memo — `memo-standard` (English)

> Write an internal memo with this content:
>
> To: All Engineering Staff
> From: Priya Nathan, VP Engineering
> Date: September 9, 2026
> Subject: Change to on-call rotation starting October 1
> Body: Starting October 1, on-call shifts move from weekly to five-day rotations to reduce fatigue
> reported in the last two retros. The new schedule will be published in PagerDuty by September 20.
> Anyone with a scheduling conflict for the first rotation should message their team lead by September 15.

**Expected section order:** to → from → date → subject → body

**Pass:** To/From/Date/Subject appear as a header block before the body, in that order, and the body is not split across other labeled sections.
**Fail:** Subject line missing or folded into the body, or To/From order reversed.

---

## 4. Form — `form-standard` (German)

> Erstellen Sie ein Anmeldeformular mit folgendem Inhalt:
>
> Formularkopf: Anmeldung zur Herbstkonferenz 2026 der Handwerkskammer Leipzig
> Anweisungen: Bitte in Blockschrift ausfüllen und bis zum 20. September 2026 per E-Mail an
> anmeldung@hwk-leipzig.de zurücksenden. Pro Person ist ein separates Formular auszufüllen.
> Formularfelder: Vollständiger Name; Firma; Position; E-Mail-Adresse; Telefonnummer; Teilnahme am
> Abendessen (Ja/Nein); Ernährungshinweise (freiwillig)
> Unterschrift: Unterschrift des Antragstellers
> Datum: Datum der Anmeldung

**Expected section order:** header → instructions → fields → signature → date
(German headings: Formularkopf, Anweisungen, Formularfelder, Unterschrift, Datum)

**Pass:** Instructions appear before the field list, signature and date are the last two sections in that order, all in German.
**Fail:** Fields listed before instructions, or signature/date merged into one section.

---

## 5. Proposal — `proposal-standard` (English)

> Draft a business proposal using this content:
>
> Cover: Proposal for Warehouse Inventory Automation — prepared for Caldwell Logistics by Arden Systems
> Executive summary: Arden Systems proposes a barcode-and-RFID inventory system to cut Caldwell's
> stock-count time by 60% within two quarters.
> Problem statement: Caldwell currently reconciles inventory manually across three warehouses, causing
> a 4% average stock discrepancy and monthly overtime costs.
> Proposed solution: Deploy RFID tagging at receiving, handheld scanners for floor staff, and a
> real-time dashboard integrated with Caldwell's existing WMS.
> Scope of work: Site survey, hardware installation across 3 sites, staff training, 90-day hypercare.
> Timeline: Site survey (Weeks 1-2), installation (Weeks 3-6), training (Weeks 7-8), hypercare (Weeks 9-20).
> Pricing: $184,000 fixed fee, payable in three milestones.
> Terms: Net 30, 12-month hardware warranty, cancellation clause after milestone 1.
> Closing: We look forward to partnering with Caldwell Logistics on this project.

**Expected section order:** cover → executive-summary → problem-statement → proposed-solution → scope-of-work → timeline → pricing → terms → closing

**Pass:** All nine sections present in this order; pricing and terms kept as distinct sections (not merged), timeline appears before pricing.
**Fail:** Scope-of-work and proposed-solution merged, or pricing/terms combined into one section.

---

## 6. Report (short) — `report-short` (French)

> Rédigez un rapport court avec ce contenu :
>
> Résumé exécutif : Le programme pilote de covoiturage d'entreprise a réduit les trajets en voiture
> individuelle de 22 % sur trois mois.
> Introduction : Ce rapport évalue le programme pilote lancé le 1er juin 2026 auprès de 140 employés
> volontaires du site de Lyon.
> Résultats : Taux d'adoption de 61 % parmi les inscrits ; économie moyenne de 38 € par mois et par
> participant ; réduction de 14 tonnes de CO2 sur la période.
> Conclusion : Le pilote confirme la viabilité du covoiturage à grande échelle sur ce site.
> Recommandations : Étendre le programme aux sites de Marseille et Toulouse au T1 2027 ; ajouter une
> prime d'incitation de 20 € pour les nouveaux inscrits.
> Bibliographie : Données internes RH, juin-août 2026 ; enquête de satisfaction interne, août 2026.

**Expected section order:** executive-summary → introduction → findings → conclusion → recommendations → bibliography
(French headings: Résumé exécutif, Introduction, Résultats, Conclusion, Recommandations, Bibliographie)

**Pass:** Six sections in this order, in French; recommendations kept distinct from and after conclusion.
**Fail:** No table of contents added (this family has none — adding one is a FAIL, not an enhancement), or findings and conclusion merged.

---

## 7. Report (long, with TOC) — `report-long-toc` (English)

> Write a long-form report with a table of contents, using this content:
>
> Cover: Annual Water Quality Assessment 2026 — Prepared for the Ashford Regional Water Authority
> Executive summary: Water quality across all six monitored sites remained within regulatory limits,
> with one exception flagged at the Millbrook intake.
> Introduction: This report covers quarterly sampling at six sites from January through August 2026.
> Methodology: Samples were collected biweekly and tested for turbidity, pH, nitrate, and coliform
> bacteria per EPA method 9223B.
> Findings: Millbrook intake showed elevated nitrate levels (11.2 mg/L) in July, exceeding the 10 mg/L
> threshold; all other sites remained under 6 mg/L throughout.
> Conclusion: The Millbrook exceedance appears linked to upstream agricultural runoff following heavy
> June rainfall.
> Recommendations: Increase Millbrook sampling to weekly through Q4; coordinate with the county on
> runoff mitigation upstream.
> Appendices: Full sampling data table by site and date, lab certification records.
> Bibliography: EPA Method 9223B documentation; county rainfall records, 2026.

**Expected section order:** cover → table-of-contents → executive-summary → introduction → methodology → findings → conclusion → recommendations → appendices → bibliography

**Pass:** All ten sections present in order, and a table-of-contents section actually appears (distinguishing this family from `report-short`, which has none).
**Fail:** Table of contents omitted, methodology dropped, or appendices/bibliography reordered before recommendations.

---

## 8. Whitepaper — `whitepaper-standard` (German)

> Verfassen Sie ein Whitepaper mit folgendem Inhalt:
>
> Deckblatt: Whitepaper — Edge Computing in der Fertigungsindustrie, herausgegeben von Vantek Systems
> Zusammenfassung: Edge Computing reduziert Latenzzeiten in Produktionslinien um bis zu 80 % gegenüber
> reiner Cloud-Verarbeitung.
> Einleitung: Fertigungsbetriebe stehen zunehmend vor Echtzeitanforderungen, die zentrale Cloud-Systeme
> nicht zuverlässig erfüllen können.
> Problemstellung: Latenzspitzen von über 200 ms bei cloudbasierter Sensorauswertung führen zu
> Produktionsausfällen in getakteten Fertigungslinien.
> Lösungsansatz: Lokale Edge-Knoten verarbeiten Sensordaten direkt an der Maschine und senden nur
> aggregierte Daten in die Cloud.
> Ergebnisse: In einem Pilotprojekt bei einem Automobilzulieferer sank die Latenz von 220 ms auf 35 ms,
> die Ausfallzeit um 47 %.
> Schlussfolgerung: Edge Computing ist für getaktete Fertigungslinien mit Echtzeitanforderungen wirtschaftlich sinnvoll.
> Literaturverzeichnis: Vantek Pilotstudie 2026; IEEE-Artikel zu Edge-Latenz in der Fertigung, 2025.

**Expected section order:** cover → executive-summary → introduction → problem-statement → solution-approach → findings → conclusion → bibliography
(German headings: Deckblatt, Zusammenfassung, Einleitung, Problemstellung, Lösungsansatz, Ergebnisse, Schlussfolgerung, Literaturverzeichnis)

**Pass:** Eight sections in this order, in German; solution-approach kept distinct from and before findings.
**Fail:** Recommendations section invented (whitepaper-standard has none — that belongs to report families), or problem-statement/solution-approach merged.

---

## 9. One-pager — `one-pager-standard` (English)

> Create a one-pager with this content:
>
> Headline: Cut onboarding time in half with FlowSeat
> Key points: Automated document collection; e-signature built in; syncs with existing HR systems;
> average customer onboarding time dropped from 9 days to 4
> Call to action: Book a 15-minute demo this week
> Contact: sales@flowseat.io, +1 (415) 555-0199

**Expected section order:** headline → key-points → call-to-action → contact

**Pass:** Four sections in this order; key points stay as a distinct list, not folded into the headline.
**Fail:** Contact info placed before call-to-action, or an introduction section added (this family has none).

**Note — trap:** This section order is identical to `flyer-single-sheet` (prompt 12). That is
correct and intentional, the same way the two brochures match each other: a one-pager and a
flyer carry the same content arc, and what separates them is format, not structure. Do not flag
either prompt's output as wrong for matching the other. There are exactly THREE such pairs in
the library -- the two brochures, letter and cover-letter, and this one.

---

## 10. Brochure, tri-fold — `brochure-3panel` (French)

> Créez le contenu d'une brochure trois volets avec ce texte :
>
> Accroche : Voyagez léger, arrivez reposé — la valise cabine Voltis
> Introduction : Voltis conçoit des valises cabine ultralégères pensées pour les voyageurs fréquents.
> Points clés : Poids de 1,9 kg ; coque en polycarbonate renforcé ; compartiment chargeur intégré ;
> garantie 10 ans
> Appel à l'action : Commandez avant le 30 septembre et bénéficiez de la livraison gratuite
> Coordonnées : www.voltis-bagages.fr, contact@voltis-bagages.fr, 01 84 60 22 10

**Expected section order:** headline → introduction → key-points → call-to-action → contact
(French headings: Accroche, Introduction, Points clés, Appel à l'action, Coordonnées)

**Pass:** Five sections in this order, in French.
**Fail:** Introduction dropped, or key points and call-to-action merged.

**Note — trap:** This section order is identical to `brochure-gatefold` (prompt 11). That's
correct and intentional — panel count isn't a content difference, it's a page-format difference
(see `page-formats.csv`). Don't flag either prompt's output as wrong for matching the other.

---

## 11. Brochure, gate-fold — `brochure-gatefold` (German)

> Erstellen Sie den Inhalt für eine Gatefold-Broschüre mit diesem Text:
>
> Kernbotschaft: Mehr Energie sparen mit der SolarDach-Komplettlösung
> Einleitung: SolarDach bietet Photovoltaikanlagen inklusive Installation und Wartung aus einer Hand.
> Kernpunkte: Amortisation in durchschnittlich 7 Jahren; 25 Jahre Leistungsgarantie; kostenlose
> Vor-Ort-Beratung; Förderung nach KfW 270 möglich
> Handlungsaufruf: Vereinbaren Sie jetzt Ihre kostenlose Dachanalyse
> Kontakt: www.solardach-plus.de, beratung@solardach-plus.de, 030 405060

**Expected section order:** headline → introduction → key-points → call-to-action → contact
(German headings: Kernbotschaft, Einleitung, Kernpunkte, Handlungsaufruf, Kontakt)

**Pass:** Five sections in this order, in German.
**Fail:** Contact section dropped, or key points reworded into the introduction.

**Note — trap:** Same order as `brochure-3panel` (prompt 10) — intentional, see note there. If a
tester "corrects" one of these two prompts to look different, that's the finding, not a skill bug.

---

## 12. Flyer — `flyer-single-sheet` (English)

> Design a flyer with this content:
>
> Headline: Saturday Farmers Market — Every week, rain or shine
> Key points: 40+ local vendors; live music from 10am; free parking on Elm Street; kids' craft table
> Call to action: See you there — Saturdays, 8am to 1pm, Elm Street Plaza
> Contact: farmersmarket@elmtown.org

**Expected section order:** headline → key-points → call-to-action → contact

**Pass:** Four sections in this order; no introduction section added (flyer has none, unlike brochure).
**Fail:** Introduction section invented, or key points and call-to-action combined.

---

## 13. Poster — `poster-single-canvas` (French)

> Créez le contenu d'une affiche avec ce texte :
>
> Accroche : Festival de musique de rue — 18-20 septembre, Place du Capitole
> Appel à l'action : Entrée libre, tous publics — venez en famille

**Expected section order:** headline → call-to-action

**Pass:** Exactly two sections, in this order, in French. Nothing else added.
**Fail:** A third section (key points, contact, etc.) is invented to "fill out" the poster.

**Note — trap:** Two sections is deliberate, not a gap in the model. A poster is read from a
distance in seconds; it only needs a headline and a call-to-action. If a tester or reviewer adds a
third section here because two "feels incomplete," that's the mistake — not the model.

---

## 14. Slide deck — `deck-standard` (German)

> Erstellen Sie die Gliederung für ein Pitch-Deck mit diesem Inhalt:
>
> Deckblatt: NovaGrid — Intelligentes Lastmanagement für Gewerbeimmobilien
> Agenda: Problem, Lösung, Ergebnisse, nächste Schritte
> Problemstellung: Gewerbeimmobilien zahlen Lastspitzenentgelte, die bis zu 30 % der Stromkosten ausmachen.
> Lösungsvorschlag: NovaGrid prognostiziert Lastspitzen und steuert Verbraucher automatisch gegen.
> Ergebnisse: Pilotkunde reduzierte Lastspitzenentgelte um 34 % innerhalb von vier Monaten.
> Handlungsaufruf: Pilotprojekt für Q1 2027 vereinbaren
> Kontakt: invest@novagrid.io, +49 30 1234567

**Expected section order:** cover → agenda → problem-statement → proposed-solution → findings → call-to-action → contact
(German headings: Deckblatt, Agenda, Problemstellung, Lösungsvorschlag, Ergebnisse, Handlungsaufruf, Kontakt)

**Pass:** Seven sections/slides in this order, in German; agenda appears right after the cover slide.
**Fail:** Agenda dropped, or findings placed before proposed-solution.

---

## 15. Cover letter — `cover-letter-standard` (English)

> Write a cover letter for a job application, using this content:
>
> Sender: Daniela Reyes, 2214 Birchwood Ave, Austin, TX 78704
> Recipient: Hiring Committee, Meridian Analytics, 900 Congress Ave, Austin, TX 78701
> Date: September 9, 2026
> Salutation: Dear Hiring Committee,
> Body: I am applying for the Senior Data Analyst position posted on your careers page. In my current
> role at Larkspur Retail, I built a demand-forecasting model that cut inventory overstock by 18%. I
> would bring that same rigor to Meridian's forecasting team.
> Closing: Sincerely, Daniela Reyes

**Expected section order:** sender → recipient → date → salutation → body → closing

**Pass:** Six sections in this order.
**Fail:** Salutation missing, or body content merged into the closing.

**Note — trap:** Same section order as `letter-standard` (prompt 2) — intentional, see the note
there. Do not treat the match as a defect in either family.

---

## Verification

Section orders above were checked against `structures.csv` programmatically:

```
invoice-standard: issuer;bill-to;invoice-details;line-items;totals;tax;payment-terms
letter-standard: sender;recipient;date;salutation;body;closing
memo-standard: to;from;date;subject;body
form-standard: header;instructions;fields;signature;date
proposal-standard: cover;executive-summary;problem-statement;proposed-solution;scope-of-work;timeline;pricing;terms;closing
report-short: executive-summary;introduction;findings;conclusion;recommendations;bibliography
report-long-toc: cover;table-of-contents;executive-summary;introduction;methodology;findings;conclusion;recommendations;appendices;bibliography
whitepaper-standard: cover;executive-summary;introduction;problem-statement;solution-approach;findings;conclusion;bibliography
one-pager-standard: headline;key-points;call-to-action;contact
brochure-3panel: headline;introduction;key-points;call-to-action;contact
brochure-gatefold: headline;introduction;key-points;call-to-action;contact
flyer-single-sheet: headline;key-points;call-to-action;contact
poster-single-canvas: headline;call-to-action
deck-standard: cover;agenda;problem-statement;proposed-solution;findings;call-to-action;contact
cover-letter-standard: sender;recipient;date;salutation;body;closing
missing_from_csv: []
duplicate_keys_in_list: []
count: 15
```

All fifteen keys present exactly once, no CSV mismatches.

Language split: French — prompts 2, 6, 10, 13 (4). German — prompts 1, 4, 8, 11, 14 (5). English —
prompts 3, 5, 7, 9, 12, 15 (6).
