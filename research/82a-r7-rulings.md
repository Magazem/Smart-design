# research/82a — Rulings on R7 (research/92) (orchestrator, 2026-09-25)

All R7 findings are ACCEPTED. The committed fills (cv, proposal) are re-run with the fixed engine,
and outputs change wherever the rules below say so. Nobody may tune a rule to reproduce a
committed pick. A pick changes when the rule changes it.

R7-1 (F1, F4) C21 is literal: shares count ADMISSIBLE exemplars only. An inadmissible exemplar
     never breaks a tie, never sets a variant value, and never appears in a provenance count.
     Ranks and Rank Values are recomputed.
R7-2 (F5) §8 medium rule is enforced by the engine. A print design never gets a pairing whose
     Scale Key is screen/projection. Georgia designs fall to the print-scaled serif the rules yield.
R7-3 (F6) Palette picks follow §8's literal order: evidence class first (authority, then ranked),
     fetched before search-corroborated, then the colour-use class match. Remaining ties go to the
     lowest palette_key in byte order. research/82a-clarifications-6.md (engine rules) only becomes
     binding once the orchestrator marks it RATIFIED. A spec may not cite it before then.
R7-4 (F12) The engine is the authority. `fill_family.py --check` FAILS whenever a spec value
     differs from the engine proposal, unless that spec entry carries `"override": "<82a file>
     <rule id>"` pointing at an existing ratified rule. A test covers this.
R7-5 (F13, F14, F15) Style reuse is keyed by the family prefix of the family being filled, and
     rejects any photo contradiction (design photo=yes vs style photo=no, and the reverse). The
     typeface proposal honours body class.
R7-6 (F2) Ties between corpora are broken in a fixed order that does not depend on spec order.
     Higher evidence level wins (L1 > L2 > L3 > L4). Within the same level, the larger on-topic N
     wins. After that, corpus id in byte order.
R7-7 (F3) The cap of 10 is literal (C29). Ranked archetypes keep ranks 1..10. The doctype default
     (fitness) is always shipped: if it would fall outside the cap, it takes the place of rank 10.
     An archetype that duplicates a higher-ranked one (same 4 identity values) is retired. The
     retirement is decided by the identity values alone, never by taste.
R7-8 (F7, F8) A reused style or reasoning row must not carry family-specific or bias tokens that
     contradict the design, such as Europass order on a non-Europass design, or "monochrome" on an
     accent design. The engine blanks those tokens and logs each one.
R7-9 (F9) The declared-font branch of §8 is implemented and tested.
R7-10 (F11) cv-dach-tabular stays pending until the §12 F6 render check passes. It is not
     released if ATS text extraction breaks on its body table.
R7-11 (F16) Add a regression test for the palette colour-use classification.
Order of work: engine fixes, then re-run cv and proposal and re-audit them, then letter and
cover-letter.
