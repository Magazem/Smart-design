# UI/UX Pro Max — Mechanism

## 1. Findings

All paths below are relative to `C:\Users\ysuliman\.claude\plugins\marketplaces\ui-ux-pro-max-skill\` unless noted. Author: `nextlevelbuilder`, MIT, v2.5.0 (`.claude-plugin/plugin.json:2-8`).

### 1.1 The router is a printed table, not code

`.claude/skills/ui-ux-pro-max/SKILL.md:50` says explicitly: *"For human/AI reference: follow priority 1→10 to decide which rule category to focus on first... Scripts do not read this table."* The 10-category priority table (lines 52-63) is prose guidance for the model to read, not a decision procedure any script executes. The actual decision procedure lives in Python (§1.2).

### 1.2 Real routing logic: BM25 + keyword auto-detect

`src/ui-ux-pro-max/scripts/core.py`:
- `CSV_CONFIG` (lines 17-73) maps 11 "domains" (`style`, `color`, `chart`, `landing`, `product`, `ux`, `typography`, `icons`, `react`, `web`, `google-fonts`) to a CSV file + `search_cols` (fields BM25 indexes) + `output_cols` (fields returned).
- `BM25` class (104-163) is a from-scratch BM25 implementation (k1=1.5, b=0.75) — no embeddings, no LLM call, pure term-frequency ranking over the CSV rows.
- `detect_domain()` (198-218) auto-picks a domain when `--domain` is omitted, via a hard-coded `domain_keywords` dict scored by regex word-boundary match, defaulting to `"style"` if nothing scores.
- `search()` / `search_stack()` (221-262) are the CLI entry points; everything downstream calls these.

This is the entire "search.py" tool: tokenize query → BM25-rank one CSV's rows → return top N. No model reasoning happens inside the script.

### 1.3 The `--design-system` pipeline (the actual style/palette/font decision procedure)

`src/ui-ux-pro-max/scripts/design_system.py`, class `DesignSystemGenerator.generate()` (163-246):
1. Search `product` domain, top-1 result → `category` (166-170).
2. `_apply_reasoning(category, {})` (88-120) looks up `category` in `ui-reasoning.csv` — exact match, then substring match, then keyword-token match (`_find_reasoning_rule`, 64-86) — and pulls `Style_Priority`, `Color_Mood`, `Typography_Mood`, `Key_Effects`, `Anti_Patterns`, and a `Decision_Rules` JSON blob (e.g. `{"if_ux_focused": "prioritize-minimalism", "if_data_heavy": "add-glassmorphism"}`, see `ui-reasoning.csv` row 2).
3. `_multi_domain_search()` (51-62) runs BM25 again on `style`/`color`/`landing`/`typography`, biasing the `style` query with the reasoning rule's `style_priority` keywords appended to the query string.
4. `_select_best_match()` (122-157) deterministically re-ranks the `style` hits: exact style-name match wins outright; otherwise a hand-weighted score (name match=10, keyword-field match=3, any-field match=1) picks the winner. No LLM judgment — closed-form tie-break.
5. Final dict (197-246) merges the BM25 hit's own columns with the reasoning rule as fallback for anything the CSV row didn't have.

So "product type → style/color/font" is: one BM25 lookup for category → CSV-driven reasoning rule → BM25 lookup again with a biased query → deterministic rerank. Two literal lookup tables (`products.csv`, `ui-reasoning.csv`) are doing what looks like "reasoning."

### 1.4 The generate → inherit loop — there are TWO, not one

**(a) `ui-ux-pro-max`'s own MASTER + overrides pattern** (`design_system.py:561-609`, `persist_design_system()`):
- Writes `design-system/<project-slug>/MASTER.md` (via `format_master_md`, 612-883: colors, typography, spacing tokens, shadow scale, CSS snippets for buttons/cards/inputs/modals, anti-pattern list, pre-delivery checklist — all generated as static markdown/CSS text, not real design tokens).
- Optionally writes `design-system/<project-slug>/pages/<page>.md` (`format_page_override_md`, 886-992) using `_generate_intelligent_overrides()` (995-1098), which re-runs BM25 searches on `style`/`ux`/`landing` seeded by the page name + a `_detect_page_type()` keyword table (1101-1133, e.g. "checkout/payment/cart" → "Checkout / Payment").
- **Retrieval is 100% convention, not code.** `.claude/skills/ui-ux-pro-max/SKILL.md:400-412` just instructs the model: *"first check `design-system/pages/[page-name].md`... If not, use `design-system/MASTER.md` exclusively."* Nothing in the codebase reads these files back in on a later invocation — the "inheritance" is the model being told, in this text, to open the file itself next time.

**(b) A separate skill, `ckm:brand`** (`.claude/skills/brand/`, frontmatter `author: claudekit` — a *different* author than ui-ux-pro-max/nextlevelbuilder, bundled in the same marketplace repo):
- Source of truth is a human/LLM-edited `docs/brand-guidelines.md` (brand `SKILL.md:52-55`).
- `scripts/sync-brand-to-tokens.cjs` regex-parses that markdown for hex colors (`extractColorsFromMarkdown`, lines 25-91) and writes `assets/design-tokens.json` as a primitive→semantic→component token tree (`updateDesignTokens`, 126-203), then shells out to `.claude/skills/design-system/scripts/generate-tokens.cjs` to flatten JSON references (`{primitive.color.x.500}`) into real CSS custom properties (`generate-tokens.cjs:80-138`).
- `scripts/inject-brand-context.cjs` separately regex-parses the same markdown into a `BRAND CONTEXT:` text block (`generatePromptAddition`, 268-305) meant to be pasted into a future prompt.
- Both scripts are invoked **manually**, per explicit numbered steps in `brand/references/update.md:44-64` ("Step 3: Run the sync script... Step 4: Verify Sync"). I grepped the whole plugin for `hooks` / automatic triggers of either script — zero results. There is no event-based automation anywhere; every "sync" step is a documented instruction for the agent to type a command.

### 1.5 Concrete anti-slop devices (code, not just prose)

- **`design-system/scripts/html-token-validator.py`** — hard-fails (`sys.exit(1)`) any HTML file missing the `design-tokens.css` import (line 129), or containing a hex/rgb/rgba/hardcoded-`font-family` literal (`FORBIDDEN_PATTERNS`, 33-40) outside a `<script>` block or an explicit allow-list of brand-derived rgba values / external CDN domains (`ALLOWED_RGBA_PATTERNS` 44-53, `ALLOWED_EXCEPTIONS` 56-59). It also *warns* (not fails) if a file has fewer than 5 `var(--...)` references (176-180) — a quantitative floor on actually using the tokens, not just importing them.
- **Contrast-safe color derivation is math, not a model guess.** `src/ui-ux-pro-max/data/_sync_all.py:22-31` computes relative luminance (WCAG formula) and picks white/`#0F172A` foreground text via `on_color()` based on that luminance — `colors.csv`'s "On Primary/On Secondary/On Accent" columns are generated this way, not hand-picked.
- **Forced, closed-form tie-breaking** in `_select_best_match()` (§1.3 above) — the model supplies a query; which style "wins" is arithmetic, not free choice.
- **Checklists are baked into the generator's own output**, not left as an instruction to remember: `format_ascii_box` (404-415), `format_markdown` (518-526) and `format_master_md` (864-881) each hard-code the same 7-10 checkbox items ("No emojis as icons," "cursor-pointer on all clickable elements," "4.5:1 contrast," "prefers-reduced-motion," fixed breakpoint list) appended to every generated design system regardless of query.
- **No emoji-as-icon rule appears 4 separate times** across `SKILL.md:568`, `quick-reference.md:267`, and both checklist generators above — redundant enforcement via repetition across every surface the model reads.

### 1.6 Templating (Q4) — the axis is "which coding tool," not "which project"

- `src/ui-ux-pro-max/templates/base/skill-content.md:1-4` is a literal placeholder file: `{{TITLE}}`, `{{DESCRIPTION}}`, `{{QUICK_REFERENCE}}`.
- `cli/src/utils/template.ts`, `renderSkillFile()` (123-157) does simple `.replace(/\{\{X\}\}/g, ...)` substitution using a per-platform JSON config (`templates/platforms/claude.json`, `cursor.json`, `windsurf.json`, etc. — 17 platform files).
- `cli/src/utils/detect.ts`, `detectAIType()` (10-77) fingerprints **which coding tool** the CLI is being run inside (checks for `.claude/`, `.cursor/`, `.windsurf/`, `.github/`, etc. in `cwd`) — it does not detect the user's tech stack.
- This substitution happens once, locally, when the user runs the plugin's install CLI (`cli/src/commands/init.ts`) — the resulting `SKILL.md` is then a static file copied into the target repo/home directory (`generatePlatformFiles`, `template.ts:187-218`). It is never re-rendered at query time.

### 1.7 Version drift discovered on this machine

`templates/platforms/claude.json:13,19` (repo source, current) advertises *"67 styles, 161 palettes... 16 stacks."* The **actually-installed** `.claude/skills/ui-ux-pro-max/SKILL.md:6-8` on this machine says *"50+ styles... 10 stacks"* and hardcodes *"Stack: React Native (this project's only tech stack)"* (line 359) with only one entry in its "Available Stacks" table (line 471). This is a stale generated snapshot — the installed skill was never refreshed via the CLI's `update` command after the source templates moved on. Because `SKILL.md` is static text, not re-derived per query, this drift is invisible until someone diffs it against the source repo, as I did here.

### 1.8 `design.csv` is orphaned, not a fifth comparable schema

The brief asked me to document `design.csv`'s columns alongside `styles.csv`/`colors.csv`/`typography.csv`/`ux-guidelines.csv`. It isn't comparable:
- `core.py`'s `CSV_CONFIG` (17-73) has no `"design"` key — nothing in the search engine touches this file.
- Repo-wide grep for the literal string `design.csv` returns **zero matches** anywhere in the plugin (scripts, SKILL.md files, references).
- Its content isn't a data table with columns at all — it's freeform Chinese-language style-prompt prose per style (e.g., "Bauhaus（包豪斯）" then a paragraph, then a `<design-system>` block describing a mobile Bauhaus theme). This looks like leftover/staging content for a different, unwired subsystem (possibly an early draft of the `design`/`banner-design` skills' style data), not a fifth queryable schema.

### 1.9 Column schemas (the four that are actually real)

- **`styles.csv`** (22 cols): `No, Style Category, Type, Keywords, Primary Colors, Secondary Colors, Effects & Animation, Best For, Do Not Use For, Light Mode ✓, Dark Mode ✓, Performance, Accessibility, Mobile-Friendly, Conversion-Focused, Framework Compatibility, Era/Origin, Complexity, AI Prompt Keywords, CSS/Technical Keywords, Implementation Checklist, Design System Variables`.
- **`colors.csv`** (19 cols): `No, Product Type, Primary, On Primary, Secondary, On Secondary, Accent, On Accent, Background, Foreground, Card, Card Foreground, Muted, Muted Foreground, Border, Destructive, On Destructive, Ring, Notes`. Every "On X" column is WCAG-luminance-derived (§1.5), not hand-authored.
- **`typography.csv`** (11 cols): `No, Font Pairing Name, Category, Heading Font, Body Font, Mood/Style Keywords, Best For, Google Fonts URL, CSS Import, Tailwind Config, Notes`.
- **`ux-guidelines.csv`** (10 cols): `No, Category, Issue, Platform, Description, Do, Don't, Code Example Good, Code Example Bad, Severity`. Same 10-column shape is reused verbatim for `react-performance.csv` and `app-interface.csv` (`core.py:58-67`).
- **`ui-reasoning.csv`** (9 cols, the "reasoning" table feeding §1.3): `No, UI_Category, Recommended_Pattern, Style_Priority, Color_Mood, Typography_Mood, Key_Effects, Decision_Rules, Anti_Patterns, Severity`.

## 2. Transferable

- **The BM25-over-CSV retrieval layer** (`core.py`'s `CSV_CONFIG` pattern) is cheap, deterministic, and needs no model call. Directly portable: define one CSV per document-design dimension (deck-pattern, CV-layout-family, color, typography, density) with the same `search_cols`/`output_cols` shape.
- **The two-stage `generate()` procedure** — classify → look up a reasoning-rule row → run biased sub-searches → deterministically rerank — is a good skeleton for "infer document type → apply category rules → search supporting dimensions biased by those rules."
- **The MASTER.md + `pages/<name>.md` override convention** is simple and model-legible; worth copying near-verbatim (e.g. a deck's MASTER.md plus per-slide override files).
- **The validator's hard/soft-fail split** (`html-token-validator.py`) — missing required import = hard error, low token usage = warning, everything else regex-checked against an explicit allow-list — is a transferable general pattern: don't just instruct "use the brand," grep the actual output and fail loudly when it doesn't.
- **WCAG-luminance-based foreground derivation** (`_sync_all.py`'s `lum`/`on_color`) is directly reusable code for guaranteeing contrast-safe text-on-background pairs in a generated palette, instead of trusting the model's contrast estimate.
- **Baking the checklist into the generator's own output**, not the instructions, is cheap and worth copying — append the same fixed self-critique list mechanically to every generated artifact.

## 3. Breaks

- **The whole "inherit across sessions" claim depends on a filesystem persistence guarantee the codebase does not control.** Every persistence mechanism here (`design-system/MASTER.md`, `assets/design-tokens.json`, `docs/brand-guidelines.md`) is a plain file write, read back only because a *later* invocation is told to open that path. Whether the Claude app's Skills/code-execution sandbox keeps a skill's working directory alive across **separate conversations** (not just within one long chat) is not something this code establishes one way or the other — it's an assumption baked into the SKILL.md prose, not a mechanism. This is the single biggest unproven load-bearing piece for a documents port targeting claude.ai (see Open Questions).
- **Node.js dependency is inconsistent with the plugin's own prerequisite check.** `ui-ux-pro-max`'s SKILL.md `Prerequisites` section (lines 308-331) only verifies/installs Python. But the brand↔design-system inherit loop (`sync-brand-to-tokens.cjs`, `inject-brand-context.cjs`, `generate-tokens.cjs`, `validate-tokens.cjs`) is entirely `.cjs` (Node). Nothing in this plugin confirms Node is available wherever these Python-prerequisite checks pass.
- **The CLI-time templating step (§1.6) has no analog in the Claude app.** `cli/src/commands/init.ts` runs locally, outside any chat, to bake a platform-specific `SKILL.md` before the conversation starts. A skill built for claude.ai can't rely on a local install step — the "which coding tool" templating axis is meaningless there; it collapses to one static file.
- **`html-token-validator.py` hard-codes a specific repo layout** (`PROJECT_ROOT / 'assets' / 'design-tokens.css'`, `ASSET_DIRS` pointing at `assets/designs/slides` and `assets/infographics`, lines 22-30). It validates a fixed project tree, not an arbitrary session workspace — would need rewriting for wherever a documents skill's scratch files actually live.
- **All the CSV content is UI-specific vocabulary** (glassmorphism, landing-page CTA placement, touch targets) — none of the data transfers, only the retrieval/reasoning/validation *structure*.

## 4. Gaps

- **No document-format output anywhere in the inspected code.** Every terminal artifact is CSS + HTML (slides, via Chart.js) or Markdown (MASTER.md, brand-guidelines.md). There is no `.docx`/`.pptx`/`.xlsx` writer, no OOXML handling, nothing analogous. The brief's open fork question ("must output be real Office files, or is HTML/PDF acceptable?") gets zero evidence toward "real files" from this codebase — it confirms the prior art's own pipeline terminates in HTML/CSS, full stop.
- **`Decision_Rules` JSON is stored but never evaluated.** `design_system.py:244` carries the reasoning rule's `decision_rules` dict (e.g. `{"if_data_heavy": "add-glassmorphism"}`) straight through into the output dict, but I found no code path anywhere that inspects those keys and branches on them. It looks like conditional logic but is currently decorative — a documents version that wants this to actually work needs to build the evaluator from scratch, not port one.
- **Nothing validates the MASTER.md inherit loop.** `html-token-validator.py` only checks slide/infographic HTML against `design-tokens.css`. Nothing checks that a later invocation that was supposed to read `design-system/MASTER.md` actually complied with it. The "inherit" half of "generate-then-inherit" is enforced by nothing but instruction text (§1.4a) — a documents skill wanting real inheritance guarantees needs a compliance-checking step that doesn't exist here.
- **No prose/voice-quality mechanism with any data or reasoning behind it.** `brand/references/voice-framework.md` and `visual-identity.md` are generic fill-in-the-blank markdown templates (see `visual-identity.md:36-78` — literally `[Font]`, `[Guidelines for proper logo use]` placeholders) with none of the BM25/reasoning-CSV machinery that the visual side has. A documents skill needs copy/tone quality control for CVs, brochures, decks — that's a from-scratch build; this prior art offers no pattern for it, only a template shell.

## 5. Open questions

- **Does claude.ai's Skills code-execution sandbox persist a skill's working-directory files across separate conversations?** This determines whether `design-system/MASTER.md` / `assets/design-tokens.json` can actually be read back by a *later, new* chat, or whether the user's positive experience only ever happened within one long-running conversation (or via a claude.ai "Projects" file-upload step this codebase knows nothing about). Settling it requires either testing directly in claude.ai (write a file via the skill in one chat, start a brand-new chat, ask it to read the file back) or checking Anthropic's Skills sandbox documentation for the persistence contract.
- **Is Node.js actually available in whatever sandbox runs the Python scripts in the user's claude.ai session?** The brand↔design-system inherit loop depends on it (§Breaks); the plugin's own prerequisite check never verifies it. Testable by asking the running skill instance to invoke `node --version`.
- **Which of the two inherit loops (§1.4a ui-ux-pro-max's MASTER.md, or §1.4b `ckm:brand`'s docs/brand-guidelines.md→tokens pipeline) actually produced the user's praised result** — or was it a manual sequence of both? They're different skills from different authors bundled in the same marketplace; the user's account ("V2 generated a brand plugin and a matching poster") doesn't indicate which ran. Settling this needs asking the user which command they used (`/brand:update` vs. `--design-system --persist`), or inspecting whichever of `docs/brand-guidelines.md` / `design-system/MASTER.md` still exists in their project.
- **Is the version drift found on this machine (§1.7) normal update lag, or a broken/never-run auto-update path?** I did not execute `cli/src/commands/update.ts` to observe what it actually does against a stale install — worth running if we want to know whether "update" is reliable prior art for our own update mechanism.
