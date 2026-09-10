# v0.2 Acceptance Set — fifteen prompts, one per newly covered family

Run each prompt below against the uploaded skill (v0.2 ZIP), fresh, with nothing else attached.
Every prompt carries its own content inline — do not add a file or paste extra text. The
expected section order for each family is quoted verbatim from
`skill/document-design-intelligence/data/base/structures.csv` (checked programmatically, see
Verification below). A response is scored PASS/FAIL against the two lines given per prompt.

**Rule: an acceptance prompt must not pre-supply the structure it is testing.** If the prompt
names the sections, the model only has to transcribe them, and the test proves nothing. Every
prompt below gives raw, unlabeled content plus a natural request for a document — never a list of
field names or colon-prefixed labels the model can just copy into headings.

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

> Kannst du mir daraus eine ordentliche Rechnung machen? Wir haben Baumann Maschinenbau AG aus
> der Industrieweg 4, 70565 Stuttgart beliefert — zwei CNC-Frässpindeln Modell FS-220 zu je
> 1.840,00 €, macht 3.680,00 €, dazu der Wartungsvertrag für Q3 2026 für 650,00 € und der
> Expressversand für 95,00 €. Das Leistungsdatum war der 28.08.2026, gestellt wird das Ganze am
> 03.09.2026 unter der Nummer RE-2026-0447 von uns, der Nordlicht Werkzeugbau GmbH, Hafenstraße
> 12, 20457 Hamburg, USt-IdNr. DE123456789. Die Zwischensumme liegt bei 4.425,00 €, die 19 % USt
> kommen auf 840,75 €, macht zusammen 5.265,75 €. Zahlung bitte netto innerhalb von 14 Tagen auf
> IBAN DE12 3456 7890 1234 5678 90.

**Expected section order:** issuer → bill-to → invoice-details → line-items → totals → tax → payment-terms
(German headings per the library: Rechnungssteller, Rechnungsempfänger, Rechnungsdetails, Positionen, Gesamtbetrag, Steuern, Zahlungsbedingungen)

**Pass:** Output (or clarifying question) keeps issuer and bill-to separate and first, line items before totals, tax broken out separately from totals, payment terms last — in German.
**Fail:** Tax folded into totals, payment terms merged into invoice-details, or the model answers in English without noting the German request.

---

## 2. Letter — `letter-standard` (French)

> Peux-tu rédiger une lettre commerciale bien formelle à partir de ça ? Ça vient de moi, Élise
> Fontaine, directrice des achats chez Atelier Rivoli SARL, 14 rue de Rivoli, 75004 Paris, et on
> est le 9 septembre 2026. Il faut l'envoyer à M. Thomas Weber, du service client de Solvex
> Distribution, 8 avenue Louise, 1050 Bruxelles. En gros je veux lui signaler qu'on a un retard de
> livraison de trois semaines sur la commande CMD-88213, passée le 2 août 2026, que ça perturbe
> notre planning de production, et qu'on veut une nouvelle date de livraison confirmée sous 5
> jours ouvrés, sinon on annule sans frais. Termine de façon polie, quelque chose comme "nous vous
> prions d'agréer nos salutations distinguées".

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

> Can you turn this into a proper internal memo? It needs to go out to all of engineering, it's
> from me, Priya Nathan, VP Engineering, dated September 9, 2026. Starting October 1 we're moving
> on-call shifts from weekly to five-day rotations, because people have been reporting fatigue in
> the last two retros. The new schedule goes up in PagerDuty by September 20. If anyone's got a
> scheduling conflict for the first rotation they should message their team lead by September 15.
> Give it a clear heading about the on-call change so people know what it's about at a glance.

**Expected section order:** to → from → date → subject → body

**Pass:** To/From/Date/Subject appear as a header block before the body, in that order, and the body is not split across other labeled sections.
**Fail:** Subject line missing or folded into the body, or To/From order reversed.

---

## 4. Form — `form-standard` (German)

> Mach mir daraus ein sauberes Anmeldeformular. Es geht um die Anmeldung zur Herbstkonferenz 2026
> der Handwerkskammer Leipzig. Die Leute sollen es bitte in Blockschrift ausfüllen und bis zum
> 20. September 2026 per E-Mail an anmeldung@hwk-leipzig.de zurückschicken, pro Person ein eigenes
> Formular. Es braucht Felder für den vollständigen Namen, die Firma, die Position, die
> E-Mail-Adresse, die Telefonnummer, ob man am Abendessen teilnimmt (ja/nein) und optional
> Ernährungshinweise. Am Ende soll noch Platz für eine Unterschrift und das Datum der Anmeldung
> sein.

**Expected section order:** header → instructions → fields → signature → date
(German headings: Formularkopf, Anweisungen, Formularfelder, Unterschrift, Datum)

**Pass:** Instructions appear before the field list, signature and date are the last two sections in that order, all in German.
**Fail:** Fields listed before instructions, or signature/date merged into one section.

---

## 5. Proposal — `proposal-standard` (English)

> Could you put this together as a proper business proposal? We're Arden Systems and we want to
> pitch Caldwell Logistics on a barcode-and-RFID inventory system that should cut their
> stock-count time by 60% within two quarters. Right now they're reconciling inventory by hand
> across three warehouses, which is causing about a 4% average stock discrepancy and racking up
> overtime costs every month. Our plan is to deploy RFID tagging at receiving, hand scanners for
> the floor staff, and a real-time dashboard hooked into their existing WMS — a site survey in
> weeks 1-2, installation across all three sites in weeks 3-6, training in weeks 7-8, then 90 days
> of hypercare running through week 20. We're pricing it at $184,000 fixed fee split across three
> milestones, net 30, with a 12-month hardware warranty and a cancellation clause after the first
> milestone. Wrap it up saying we're looking forward to partnering with them, and give it a title
> page naming the project and both companies.

**Expected section order:** cover → executive-summary → problem-statement → proposed-solution → scope-of-work → timeline → pricing → terms → closing

**Pass:** All nine sections present in this order; pricing and terms kept as distinct sections (not merged), timeline appears before pricing.
**Fail:** Scope-of-work and proposed-solution merged, or pricing/terms combined into one section.

---

## 6. Report (short) — `report-short` (French)

> Tu peux en faire un rapport court, bien structuré ? On a lancé le 1er juin 2026 un programme
> pilote de covoiturage d'entreprise auprès de 140 employés volontaires sur le site de Lyon, et ce
> rapport doit évaluer comment ça s'est passé. Le taux d'adoption chez les inscrits est de 61 %,
> l'économie moyenne par participant est de 38 € par mois, et on a réduit les émissions de 14
> tonnes de CO2 sur la période. Au global les trajets en voiture individuelle ont baissé de 22 %
> sur trois mois. Ça confirme que le covoiturage est viable à plus grande échelle sur ce site, donc
> on recommande d'étendre le programme aux sites de Marseille et Toulouse au T1 2027, avec une
> prime d'incitation de 20 € pour les nouveaux inscrits. Les chiffres viennent des données internes
> RH de juin à août 2026 et d'une enquête de satisfaction interne réalisée en août 2026.

**Expected section order:** executive-summary → introduction → findings → conclusion → recommendations → bibliography
(French headings: Résumé exécutif, Introduction, Résultats, Conclusion, Recommandations, Bibliographie)

**Pass:** Six sections in this order, in French; recommendations kept distinct from and after conclusion.
**Fail:** No table of contents added (this family has none — adding one is a FAIL, not an enhancement), or findings and conclusion merged.

---

## 7. Report (long, with TOC) — `report-long-toc` (English)

> Can you write this up as a full long-form report with a table of contents? This is the annual
> water quality assessment for 2026, prepared for the Ashford Regional Water Authority. We sampled
> six sites biweekly from January through August 2026, testing for turbidity, pH, nitrate, and
> coliform bacteria using EPA method 9223B. Water quality stayed within regulatory limits at every
> site except one exception at the Millbrook intake, where nitrate hit 11.2 mg/L in July, over the
> 10 mg/L threshold, while every other site stayed under 6 mg/L the whole time. That exceedance
> looks tied to upstream agricultural runoff after the heavy June rainfall. We think Millbrook
> sampling should go to weekly through Q4, and we should coordinate with the county on runoff
> mitigation upstream. Include the full sampling data table by site and date and the lab
> certification records as an appendix, and cite the EPA method 9223B documentation and the
> county's 2026 rainfall records as sources.

**Expected section order:** cover → table-of-contents → executive-summary → introduction → methodology → findings → conclusion → recommendations → appendices → bibliography

**Pass:** All ten sections present in order, and a table-of-contents section actually appears (distinguishing this family from `report-short`, which has none).
**Fail:** Table of contents omitted, methodology dropped, or appendices/bibliography reordered before recommendations.

---

## 8. Whitepaper — `whitepaper-standard` (German)

> Schreib mir daraus ein Whitepaper, herausgegeben von Vantek Systems, zum Thema Edge Computing in
> der Fertigungsindustrie. Fertigungsbetriebe stehen zunehmend vor Echtzeitanforderungen, die
> zentrale Cloud-Systeme nicht zuverlässig erfüllen können — bei cloudbasierter Sensorauswertung
> treten Latenzspitzen von über 200 ms auf, was in getakteten Fertigungslinien zu
> Produktionsausfällen führt. Unser Ansatz: lokale Edge-Knoten verarbeiten die Sensordaten direkt
> an der Maschine und schicken nur aggregierte Daten in die Cloud. Bei einem Automobilzulieferer
> haben wir das in einem Pilotprojekt getestet — die Latenz sank von 220 ms auf 35 ms, die
> Ausfallzeit um 47 %. Insgesamt zeigt das, dass sich Edge Computing für getaktete
> Fertigungslinien mit Echtzeitanforderungen wirtschaftlich rechnet, und Latenzzeiten um bis zu
> 80 % gegenüber reiner Cloud-Verarbeitung reduziert. Als Quellen dienen unsere eigene Pilotstudie
> von 2026 und ein IEEE-Artikel zu Edge-Latenz in der Fertigung von 2025.

**Expected section order:** cover → executive-summary → introduction → problem-statement → solution-approach → findings → conclusion → bibliography
(German headings: Deckblatt, Zusammenfassung, Einleitung, Problemstellung, Lösungsansatz, Ergebnisse, Schlussfolgerung, Literaturverzeichnis)

**Pass:** Eight sections in this order, in German; solution-approach kept distinct from and before findings.
**Fail:** Recommendations section invented (whitepaper-standard has none — that belongs to report families), or problem-statement/solution-approach merged.

---

## 9. One-pager — `one-pager-standard` (English)

> Turn this into a one-pager. FlowSeat cuts onboarding time in half — customers have gone from 9
> days down to 4 on average. It automates document collection, has e-signature built right in, and
> syncs with whatever HR system a company is already running. The push here is to get people to
> book a 15-minute demo this week, and they can reach us at sales@flowseat.io or
> +1 (415) 555-0199.

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

> Peux-tu me faire le contenu d'une brochure trois volets ? C'est pour Voltis, qui conçoit des
> valises cabine ultralégères pour les voyageurs fréquents — l'idée, c'est de voyager léger et
> d'arriver reposé. La valise pèse 1,9 kg, la coque est en polycarbonate renforcé, il y a un
> compartiment chargeur intégré et une garantie de 10 ans. On veut pousser les gens à commander
> avant le 30 septembre pour avoir la livraison gratuite. On peut nous joindre sur
> www.voltis-bagages.fr, à contact@voltis-bagages.fr, ou au 01 84 60 22 10.

**Expected section order:** headline → introduction → key-points → call-to-action → contact
(French headings: Accroche, Introduction, Points clés, Appel à l'action, Coordonnées)

**Pass:** Five sections in this order, in French.
**Fail:** Introduction dropped, or key points and call-to-action merged.

**Note — trap:** This section order is identical to `brochure-gatefold` (prompt 11). That's
correct and intentional — panel count isn't a content difference, it's a page-format difference
(see `page-formats.csv`). Don't flag either prompt's output as wrong for matching the other.

---

## 11. Brochure, gate-fold — `brochure-gatefold` (German)

> Erstell mir den Inhalt für eine Gatefold-Broschüre für SolarDach — mehr Energie sparen mit der
> Komplettlösung. Wir bieten Photovoltaikanlagen inklusive Installation und Wartung aus einer
> Hand. Die Amortisation liegt im Schnitt bei 7 Jahren, es gibt 25 Jahre Leistungsgarantie, eine
> kostenlose Vor-Ort-Beratung, und man kann eine Förderung nach KfW 270 bekommen. Die Leute
> sollen jetzt ihre kostenlose Dachanalyse vereinbaren — erreichbar sind wir über
> www.solardach-plus.de, beratung@solardach-plus.de oder 030 405060.

**Expected section order:** headline → introduction → key-points → call-to-action → contact
(German headings: Kernbotschaft, Einleitung, Kernpunkte, Handlungsaufruf, Kontakt)

**Pass:** Five sections in this order, in German.
**Fail:** Contact section dropped, or key points reworded into the introduction.

**Note — trap:** Same order as `brochure-3panel` (prompt 10) — intentional, see note there. If a
tester "corrects" one of these two prompts to look different, that's the finding, not a skill bug.

---

## 12. Flyer — `flyer-single-sheet` (English)

> Make me a flyer out of this. It's for the Saturday Farmers Market, every week, rain or shine,
> 8am to 1pm at Elm Street Plaza. There's 40+ local vendors, live music starting at 10am, free
> parking on Elm Street, and a kids' craft table. People can reach us at
> farmersmarket@elmtown.org. Make it feel like a see-you-there kind of invite.

**Expected section order:** headline → key-points → call-to-action → contact

**Pass:** Four sections in this order; no introduction section added (flyer has none, unlike brochure).
**Fail:** Introduction section invented, or key points and call-to-action combined.

---

## 13. Poster — `poster-single-canvas` (French)

> J'ai besoin d'une affiche avec ça. C'est pour le festival de musique de rue, du 18 au 20
> septembre, Place du Capitole. Entrée libre, tous publics, venez en famille.

**Expected section order:** headline → call-to-action

**Pass:** Exactly two sections, in this order, in French. Nothing else added.
**Fail:** A third section (key points, contact, etc.) is invented to "fill out" the poster.

**Note — trap:** Two sections is deliberate, not a gap in the model. A poster is read from a
distance in seconds; it only needs a headline and a call-to-action. If a tester or reviewer adds a
third section here because two "feels incomplete," that's the mistake — not the model.

---

## 14. Slide deck — `deck-standard` (German)

> Kannst du mir daraus die Gliederung für ein Pitch-Deck machen? Es geht um NovaGrid,
> intelligentes Lastmanagement für Gewerbeimmobilien. Gewerbeimmobilien zahlen
> Lastspitzenentgelte, die bis zu 30 % der Stromkosten ausmachen — das ist das Problem, und
> NovaGrid prognostiziert die Lastspitzen im Voraus und steuert die Verbraucher automatisch
> dagegen. Bei einem Pilotkunden hat das die Lastspitzenentgelte innerhalb von vier Monaten um
> 34 % gesenkt.
> Wir wollen daraus ein Pilotprojekt für Q1 2027 vereinbaren, erreichbar unter invest@novagrid.io
> oder +49 30 1234567. Die Übersicht am Anfang sollte kurz zeigen, dass es um Problem, Lösung,
> Ergebnisse und nächste Schritte geht.

**Expected section order:** cover → agenda → problem-statement → proposed-solution → findings → call-to-action → contact
(German headings: Deckblatt, Agenda, Problemstellung, Lösungsvorschlag, Ergebnisse, Handlungsaufruf, Kontakt)

**Pass:** Seven sections/slides in this order, in German; agenda appears right after the cover slide.
**Fail:** Agenda dropped, or findings placed before proposed-solution.

---

## 15. Cover letter — `cover-letter-standard` (English)

> Can you write this up as a cover letter for a job application? It's from me, Daniela Reyes,
> 2214 Birchwood Ave, Austin, TX 78704, dated September 9, 2026. It's going to the hiring
> committee at Meridian Analytics, 900 Congress Ave, Austin, TX 78701. I'm applying for the
> Senior Data Analyst role posted on their careers page. At my current job at Larkspur Retail I
> built a demand-forecasting model that cut inventory overstock by 18%, and I'd bring that same
> rigor to Meridian's forecasting team. Sign it off from me, Daniela Reyes.

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
