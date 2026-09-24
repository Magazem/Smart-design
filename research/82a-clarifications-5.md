# research/82a — Clarifications round 5 (orchestrator, 2026-09-24)

C25 RATIFIED (report-corpus-ms.md RM.8): where a catalogue publishes only a cover thumbnail, body class may
    be read from the template file's DECLARED theme minor font and columns from the declared section
    columns (w:cols) — consistent with §4's "declared font wins". Features that cannot be observed
    (rules/boxes, density) are coded `unknown` (82a C7) and fall back to the family default in filling.
C26 Families coded before research/82a-general.md landed (report MS, proposal MS, poster, cover-letter,
    letter, invoice, brochure, flyer, memo, form) have header treatment and colour use RECODED by a fresh
    worker under 82a-general before their second-coder check; the first coders' header/colour values are
    kept as (r1) for the record only.
C27 (answers flyer/poster question, 2026-09-24) An A1 pool (several catalogues each <10 on-topic items,
    pooled to >=10) IS a corpus in its own right and MAY sit beside other corpora (L1 or L2 >=10) of the same
    family; the family's combined share is the unweighted mean across corpora (§6), the pool counting once.
    Items appearing in more than one corpus are deduplicated (keep the first by corpus order: L1, then L2,
    then pool). The pool must reach >=10 on-topic items AFTER dedup, else it stays corroboration-only.
    Flyer pool (LO + Typst + GH flyer/typst) and poster pool (MS 8 + Typst 8) are assembled by the GitHub
    worker, who alone can dedup against GitHub items.
C28 (extends C22a to all families, 2026-09-24) Routing / address / metadata blocks — sender, recipient, TO/FROM/
    CC/DATE/SUBJECT, issuer, bill-to/ship-to, reference/number/date panels — NEVER make a column or sidebar in ANY
    family, wherever they sit. `columns` counts running body text only. Applies to memo (MSM:006, OLM:009 -> 1),
    invoice, quote and any family coded later; already-coded items affected only by this rule are recoded in place
    with a note.
