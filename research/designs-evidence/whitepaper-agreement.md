# Agreement computation — family: whitepaper

Identity features (gating): columns, heading, colour, header, admissible.
Variant features (non-gating, dropped from filling on failure): body, rules_boxes, density, cover_page.

## Inputs

- First coder [WP] `research/designs-evidence/whitepaper-corpus-github.md`: 8 coded rows found (1 coded table(s) detected).
- First coder [WP] `research/designs-evidence/whitepaper-corpus.md`: 3 coded rows found (1 coded table(s) detected).
- Second coder `research/designs-evidence/whitepaper-second-coder.md`: 10 coded rows found (1 coded table(s) detected).

## Sample

10 ids: WP:001, WP:002, WP:003, WP:005, WP:006, WP:012, WP:013, WP:017, WPL:001, WPO:001


## id-scheme check

All sampled ids matched a first-coder row directly by id (no name-based fallback needed).

## Unknown/uncoded values excluded from n (82a C7) — 2 cell(s)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| WPO:001 | rules_boxes | unknown | none |
| WPO:001 | density | unknown | airy |

### Per-feature agreement (full sample)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| heading | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| colour | identity | 10 | 9 | 0.9000 | 0.7059 | PASS |
| header | identity | 10 | 9 | 0.9000 | 0.8333 | PASS |
| body | variant | 10 | 9 | 0.9000 | 0.6154 | PASS |
| rules_boxes | variant | 9 | 4 | 0.4444 | 0.1964 | FAIL |
| density | variant | 9 | 4 | 0.4444 | 0.1964 | FAIL |
| cover_page | variant | 0 | - | n/a (no shared coded sample) | n/a | n/a |
| admissible | admit/exclude | 10 | 10 | 1.0000 | 1.0000 | PASS |

### Disagreements (full sample)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| WP:001 | body | serif | sans |
| WP:001 | rules_boxes | rules | none |
| WP:001 | density | dense | standard |
| WP:002 | rules_boxes | boxes | rules |
| WP:002 | density | dense | airy |
| WP:003 | header | plain-centered | ruled |
| WP:003 | rules_boxes | none | rules |
| WP:005 | density | standard | airy |
| WP:006 | colour | one-accent | multi |
| WP:006 | rules_boxes | none | rules |
| WP:012 | density | dense | standard |
| WP:013 | density | standard | dense |
| WPL:001 | rules_boxes | boxes | rules |

### Gate verdict

PASS — every identity feature (and admissible) A_f >= 0.80.

Variant feature(s) below A_f >= 0.80, dropped from filling (family default used instead), per §7's last sentence — does not fail the gate: rules_boxes, density.

Variant feature(s) with n=0 shared coded sample (e.g. all sampled items were `unknown` for both coders): cover_page. Not gating, not usable for filling either — family default used.
