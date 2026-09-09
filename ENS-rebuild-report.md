# ENS plugin rebuild — report (built 2026-09-07, plugin version 2.13.0-ens.2)

Every claim below is tagged **VERIFIED** (I read or ran the thing, with file:line or command output) or **ASSUMED** (not directly checkable from here).

## R1 — descriptions replaced, not prepended — VERIFIED
Final `description:` lengths (characters), all parse as valid YAML:

| Skill | Chars | Org + all document types inside first 200 chars |
|---|---|---|
| ui-ux-pro-max | 707 | yes (window ends at char 192, word boundary) |
| brand | 531 | yes |
| design | 605 | yes |
| banner-design | 543 | yes |
| slides | 442 | yes |
| design-system | 449 | yes |
| ui-styling | 524 | yes |

First 150 chars of every description are identical: `ENS - Eng nei Schaff a.s.b.l. (Bettembourg): note interne, formulaire, fiche, courrier, affiche, dépliant, présentation, post Facebook.` — so even a 200-char cut keeps every trigger. Manifest description: 432 chars (limit 500).

**Activation test — ASSUMED.** Skill activation happens in the host app, not in this container; I cannot run « fais-moi une note interne sur les congés » against the installed plugin from here. Please run it once after installing and tell me whether the skill fired.

## R2 — styles.csv columns — VERIFIED, with a correction to the correction
The installed plugin (v2.13.0) has a **29-column** `styles.csv` header, read with `csv.reader` on `data/styles.csv` line 1. It **does** contain `Style Category`, `Style ID`, `Aliases`, `Status`, `Parent Style ID`. `scripts/core.py:21` lists `"Style ID"` and `"Aliases"` among the searched columns, and `core.py:740–748` follows `Parent Style ID` / `Replacement ID`. The reviewer's 22-column header belongs to an older upstream version. So the four columns are real here — but I did what R2 asked anyway, because it costs nothing and survives a downgrade: the style name is in `Style Category` (`ENS Document Grid`) and the alias words are in `Keywords` and `AI Prompt Keywords`; `Style ID`/`Aliases`/`Parent Style ID` are filled too. No rule content relies on inheritance.

## R3 — wrapper fails, not prints — VERIFIED
`scripts/ens-search.sh` (also mirrored to `src/`). Exits 1 when `search.py` fails or when its output lacks `ENS - Eng nei Schaff` / `ENS Document Grid` / `ENS Manrope Inter`. Test run:

```
ens-search.sh "ENS formulaire" --design-system      → exit 0; STYLE: ENS Document Grid; Primary #1F6F43; Secondary #8B5E3C; TYPOGRAPHY: Manrope / Inter
ens-search.sh "internal document form b2b" --design-system → exit 1; stderr: [NO ENS MATCH] query did not resolve to ENS - fix the query ...
--domain product|color|typography|style "ens eng nei schaff" → ENS row first on all four
```
Trigger-block step 3 now reads: run the wrapper; if it exits non-zero, do not proceed — fix the query and rerun.

## Decision_Rules — VERIFIED, reviewer's line reference is for a different version
In the installed copy, `scripts/design_system.py:385–386` are literally:
```
decision_rules = parse_decision_rules(rule.get("Decision_Rules", "{}"))
applied = apply_decision_rules(decision_rules, query)
```
and `scripts/reasoning_contract.py:7` defines `CONDITION_SIGNALS` — a fixed dictionary (`if_booking`, `if_data_heavy`, `if_dashboard`, …). Custom keys such as `if_internal_note` are never in that dictionary, so v1's routing would indeed never have fired. The fix from 1.2 stands: `UI_Category` and `Style_Priority` filled; `Decision_Rules` holds only built-in keys (`must_have`, `if_data_heavy`); per-document routing is in the trigger block + `ens-document-rules.md`.

## Data integrity — VERIFIED by the plugin's own validator
`python3 scripts/validate_data.py` → `OK: validated 12 domain files, 22 stack files, and ui-reasoning.csv`. To get there I had to fix what it caught (all real):
- duplicate `No` on the styles row; `Dark Mode ✓` must be one of `supported|conditional|not-recommended`; AI prompt ≤ 40 words; `Confidence` must be 0–1 (now 0.9).
- the validator hard-codes 192 rows for products/colors/reasoning → changed to 193 (`validate_data.py:343–344`, commented). Noted in README.
- provenance records for the two ENS entities added with `sla: needs-review` and derived sources (the validator only accepts an allow-listed set of "official" sources).
- `catalog-summary.json` regenerated (`scripts/generate-catalog-summary.py --verified-at 2026-09-07`).
- Per `CLAUDE.md` sync rules, `src/ui-ux-pro-max/data`, `validate_data.py` and `ens-search.sh` are mirrored into `src/`.

Join key `ENS - Eng nei Schaff` (plain hyphen) is byte-identical in `products.csv`, `colors.csv`, `ui-reasoning.csv` — VERIFIED by the `--domain` tests above resolving on all three.

## Your three decisions — applied
- Brown = secondary category marker (rules Global + A, C; `colors.csv` Notes; brand guideline §1).
- Form fields = underlines, 6 mm (rules B).
- Social default = 1080 × 1350 portrait (rules C; banner-design description).

## Tier 2 items — applied in `ens-document-rules.md`
Legal text mixed case ≥ 8.5pt (B) · note body Arial 11pt on a 130 mm measure (A) · black section numbers (B) · slides body 24pt default (D) · PPTX embedding verified after export (D) · lime never as text anywhere, filled badge only in C · labels 8.5pt (Global) · On-colours contrast: green/white 6.4:1, brown/white 5.6:1, lime/dark 8.7:1, muted 4.6:1, destructive 6.9:1 — computed, VERIFIED.

## What is NOT done
- The three earlier deliverables (post, fiche, fermetures) have **not** been re-run through the rebuilt plugin. Say the word and I re-run them as the acceptance test.
- A3 affiche type not added (deliberately, per review).

## Files changed (all inside the plugin)
`.claude-plugin/plugin.json` · 7 × `.claude/skills/*/SKILL.md` (description + body block) · `brand/references/ens-brand-guidelines.md` (palette roles, logo, fonts) · **new** `brand/references/ens-document-rules.md` · **new** `ui-ux-pro-max/scripts/ens-search.sh` · `ui-ux-pro-max/data/{products,colors,typography,styles,ui-reasoning}.csv` (+1 row each) · `data-provenance.json` · `catalog-summary.json` · `scripts/validate_data.py` (193) · `README.md` · mirrored into `src/`.
