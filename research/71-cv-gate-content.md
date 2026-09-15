# 71 — Pre-registered CV gate content and prompts (Manager, 2026-09-15)

Written BEFORE any render or browser run (rule: preregister-falsifier). Both gates use this
content verbatim: A5 (local render, old default vs new directions) and A6 (claude.ai, with
skill vs without). Nothing here may be edited after the first run starts; corrections go in a
new numbered file.

## Fixed content

### C1 — cv-uk, early band (Direction 1 target)
Name: Priya Raman. Location: Manchester, UK. Email: priya.raman@example.com. Phone: +44 7700 900123.
Summary: Recent BSc Computer Science graduate (2:1, University of Manchester, 2025) seeking a
junior software engineering role. Built a course-timetabling web app used by 300 students.
Education: BSc Computer Science, University of Manchester, 2022–2025, 2:1. A-levels: Maths (A),
Physics (A), Computer Science (B), Altrincham Grammar, 2022.
Experience: Software Engineering Intern, Co-op Digital, Manchester, Jun–Sep 2024: built two
internal React components, wrote unit tests, fixed 14 accessibility defects. Student Ambassador,
University of Manchester, 2023–2025: ran open-day sessions for 40+ visitors.
Skills: Python, JavaScript, React, SQL, Git, Jest. Languages: English (native), Tamil (fluent).

### C2 — cv-dach, experienced band (Direction 2 target)
Name: Markus Weber. Location: München, Deutschland. Email: markus.weber@example.de. Phone: +49 170 1234567.
Geburtsdatum: 12.03.1986. Staatsangehörigkeit: deutsch. Familienstand: verheiratet.
Berufserfahrung: Senior Projektleiter, Siemens Mobility, München, 2019–heute: Leitung eines
Teams von 12, Verantwortung für ein Signaltechnik-Projekt mit 40 Mio. EUR Budget, Lieferung
termingerecht 2023. Projektleiter, Knorr-Bremse, München, 2014–2019: Einführung eines
PLM-Systems an drei Standorten. Ingenieur, MTU Aero Engines, 2011–2014.
Ausbildung: Dipl.-Ing. Maschinenbau, TU München, 2005–2011, Note 1,7.
Kenntnisse: MS Project, SAP PS, PRINCE2 Practitioner. Sprachen: Deutsch (Muttersprache),
Englisch (verhandlungssicher), Französisch (Grundkenntnisse).

### C3 — cv-generic, experienced band (Direction 1 default)
Name: Amina Yusuf. Location: Dubai, UAE. Email: amina.yusuf@example.com. Phone: +971 50 123 4567.
Summary: Marketing manager with nine years in consumer goods across the Gulf and East Africa;
led a rebrand that lifted category share by 4 points.
Experience: Marketing Manager, Unilever Gulf, Dubai, 2020–present: managed a team of 6 and a
USD 3M media budget; launched two product lines. Brand Manager, Nairobi, 2016–2020: rebrand and
distribution expansion to 1,200 outlets.
Education: MBA, INSEAD, 2016. BCom Marketing, University of Nairobi, 2013.
Skills: brand strategy, media planning, P&L ownership, Arabic (fluent), Swahili (native),
English (fluent).

## A5 (local) protocol
Render each of C1–C3 twice: OLD = pre-A4 defaults, NEW = A4 defaults, following the handoff
block mechanically with python-docx. Page 1 PNG at 150 dpi. Three Opus judges, blind, order
randomised. Rubric and pass condition: board task A5 (fixed 2026-09-14).

## A6 (browser) prompts, verbatim
Each prompt is sent twice in fresh conversations: once with the skill installed and the sentence
"Use the document-design-intelligence skill." appended, once with the skill uninstalled and no
such sentence. Account custom instructions recorded first and OFF during the run.

P1: "Make me a one-page CV as a Word document for a junior software engineering role in the
UK, using exactly this information and nothing invented: [C1 content pasted verbatim]"

P2: "Erstelle mir einen tabellarischen Lebenslauf als Word-Dokument für eine Bewerbung in
Deutschland, mit genau diesen Angaben und nichts Erfundenem: [C2 content pasted verbatim]"

P3: "Make me a CV as a Word document for a senior marketing role with an international
employer, using exactly this information and nothing invented: [C3 content pasted verbatim]"

Kill signal (A6): if the without-skill document is preferred on 2 of 3 prompts by the blind
panel, the CV directions do not ship as defaults in v0.4.0.
