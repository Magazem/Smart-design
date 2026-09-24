# Agreement computation — family: proposal

Identity features (gating): columns, heading, colour, header, admissible.
Variant features (non-gating, dropped from filling on failure): body, rules_boxes, density, cover_page.

## Inputs

- First coder [GH] `research/designs-evidence/proposal-corpus-github.md`: 40 coded rows found (1 coded table(s) detected).
- First coder [MSP] `research/designs-evidence/proposal-corpus-ms.md`: 0 coded rows found (0 coded table(s) detected).
- Second coder `research/designs-evidence/proposal-second-coder.md`: 12 coded rows found (1 coded table(s) detected).

## Sample

12 ids: GH:012, GH:014, GH:018, GH:025, GH:027, GH:029, GH:036, GH:037, GH:063, GH:092, MSP:006, MSP:007


## WARNING: unmatched sample ids (no first-coder row by id or name)

- MSP:006
- MSP:007

## id-scheme check

All sampled ids matched a first-coder row directly by id (no name-based fallback needed).

### Per-feature agreement (full sample)

| Feature | Role | n | Agreements | A_f | Cohen's kappa | Gate (>=0.80) |
|---|---|---|---|---|---|---|
| columns | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| heading | identity | 10 | 8 | 0.8000 | 0.6226 | PASS |
| colour | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| header | identity | 10 | 10 | 1.0000 | 1.0000 | PASS |
| body | variant | 10 | 10 | 1.0000 | 1.0000 | PASS |
| rules_boxes | variant | 10 | 6 | 0.6000 | 0.3750 | FAIL |
| density | variant | 10 | 3 | 0.3000 | -0.1290 | FAIL |
| cover_page | variant | 0 | - | n/a (no shared coded sample) | n/a | n/a |
| admissible | admit/exclude | 10 | 10 | 1.0000 | 1.0000 | PASS |

### Disagreements (full sample)

| id | feature | coder1 | coder2 |
|---|---|---|---|
| GH:012 | heading | sans | serif |
| GH:012 | rules_boxes | rules | none |
| GH:018 | rules_boxes | boxes | none |
| GH:025 | density | airy | standard |
| GH:027 | density | standard | airy |
| GH:029 | density | dense | standard |
| GH:036 | rules_boxes | none | rules |
| GH:036 | density | airy | standard |
| GH:037 | density | airy | standard |
| GH:063 | density | standard | airy |
| GH:092 | heading | display | serif |
| GH:092 | rules_boxes | boxes | none |
| GH:092 | density | dense | standard |

### Gate verdict

PASS — every identity feature (and admissible) A_f >= 0.80.

Variant feature(s) below A_f >= 0.80, dropped from filling (family default used instead), per §7's last sentence — does not fail the gate: rules_boxes, density.

Variant feature(s) with n=0 shared coded sample (e.g. all sampled items were `unknown` for both coders): cover_page. Not gating, not usable for filling either — family default used.
