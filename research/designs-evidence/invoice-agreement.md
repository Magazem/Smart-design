# Agreement computation — family: invoice

Identity features (gating): columns, heading, colour, header, admissible.
Variant features (non-gating, dropped from filling on failure): body, rules_boxes, density, totals_position, table_rules.

## Inputs

- First coder [GH] `research/designs-evidence/invoice-corpus.md`: 48 coded rows found (2 coded table(s) detected).
- Second coder `research/designs-evidence/invoice-second-coder.md`: 12 coded rows found (1 coded table(s) detected).

## Sample

12 ids: GH:004, GH:027, GH:030, GH:054, GH:075, GH:090, GH:097, GH:119, MS:001, MS:005, MS:006, MS:007


## id-scheme check

All sampled ids matched a first-coder row directly by id (no name-based fallback needed).

### Per-feature agreement (full sample)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 12 | 11 | 0.9167 | 0.0000 | PASS |
| heading | identity | 12 | 11 | 0.9167 | 0.8000 | PASS |
| colour | identity | 12 | 6 | 0.5000 | 0.2871 | FAIL |
| header | identity | 12 | 4 | 0.3333 | 0.2558 | FAIL |
| body | variant | 12 | 11 | 0.9167 | 0.7500 | PASS |
| rules_boxes | variant | 12 | 11 | 0.9167 | 0.8333 | PASS |
| density | variant | 12 | 7 | 0.5833 | 0.2405 | FAIL |
| totals_position | variant | 12 | 11 | 0.9167 | 0.8154 | PASS |
| table_rules | variant | 12 | 7 | 0.5833 | 0.4495 | FAIL |
| admissible | admit/exclude | 12 | 12 | 1.0000 | 1.0000 | PASS |

### Disagreements (full sample)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| GH:004 | colour | one-accent | mono |
| GH:004 | header | split | ruled |
| GH:004 | density | standard | dense |
| GH:004 | table_rules | header-and-total | row-hairlines |
| GH:027 | density | dense | standard |
| GH:030 | colour | one-accent | mono |
| GH:054 | colour | one-accent | mono |
| GH:054 | header | plain-centered | ruled |
| GH:075 | colour | multi | one-accent |
| GH:075 | header | split | ruled |
| GH:097 | colour | multi | mono |
| GH:097 | header | split | plain-left |
| GH:097 | density | standard | airy |
| GH:119 | header | plain-centered | ruled |
| GH:119 | density | dense | standard |
| GH:119 | totals_position | full-width-bottom | right-bottom |
| GH:119 | table_rules | header-and-total | row-hairlines |
| MS:001 | heading | sans | serif |
| MS:001 | header | plain-left | ruled |
| MS:001 | density | dense | standard |
| MS:005 | colour | mono | one-accent |
| MS:005 | header | split | plain-left |
| MS:005 | table_rules | header-and-total | row-hairlines |
| MS:006 | header | split | ruled |
| MS:006 | body | sans | serif |
| MS:006 | rules_boxes | rules | none |
| MS:006 | table_rules | header-and-total | none |
| MS:007 | columns | 1 | 2-sidebar |
| MS:007 | table_rules | header-and-total | row-hairlines |

### Gate verdict

FAIL — identity feature(s) colour, header below A_f >= 0.80 (falsifier gate).

Variant feature(s) below A_f >= 0.80, dropped from filling (family default used instead), per §7's last sentence — does not fail the gate: density, table_rules.
