# research/82a — Clarifications round 2 (orchestrator, 2026-09-24)

C11 **Item-list file for independence.** Twice (cv, deck) a second coder saw first-coder codes
    while locating the item list inside a combined evidence file. From now on every first coder
    ALSO writes `research/designs-evidence/<family>-items.csv` with ONLY: id, name, url,
    preview_url (one row per CODED item). Second coders read ONLY that csv plus §4/§5/82a, and are
    told the evidence .md files are off-limits. For cv and deck, the orchestrator generates the
    items csv by script before any re-run.
C12 **Exposure handling.** A second coder who sees first-coder codes discloses it; items seen are
    recoded blind by a fresh worker, or reported in a sensitivity run excluding them. Never silent.
