# research/designs-evidence/form-second-coder.md — independent second coder (falsifier), 2026-09-24

**Independence.** Coded from `research/82-design-ranking-protocol.md` §4/§5, `research/82a-general.md`
(colour use — form's identity "header" is replaced by field style per §4, unchanged; only colour
use is superseded), `research/82a-clarifications-1.md` through `-5.md` (including C29's form
literalism and C7-vs-box-grid rule), and `research/designs-evidence/form-items.csv` only. No
other file under `research/designs-evidence/` was opened; `research/91-family-status.md` and
`research/82b-shortfall-sources.md` were not opened. First-coder codes were never seen.

**Method.** All 4 ids in `form-items.csv` (`FMA:001` USWDS, `FMA:002` GOV.UK, `FMA:003` ABS,
`FMA:004` NHS):

```python
import math, random
ids = sorted(['FMA:001','FMA:002','FMA:003','FMA:004'])
n = max(min(10, len(ids)), math.ceil(0.25 * len(ids)))  # = 4
sample = random.Random("82a:form").sample(ids, n)  # = all 4, order immaterial
```

**Method note on "no raster" items.** None of the 4 items has a screenshot; the url and
preview_url columns are identical published pages. Per the task's instruction to "use the URL's
published page/CSS as the item itself," each page's own HTML and linked stylesheet were fetched
with `curl -s -A "smart-design-research"` and read directly (field border/radius rules, font-face
declarations, colour custom-properties/link colours). Where the specific page does not render a
live input example in its own markup (GOV.UK `/patterns/` is an index of links, not a worked
field), the page's own linked CSS is still "the page" for this purpose and was used, disclosed
per item below. ABS's page is itself prose guidance illustrating box-style fields; its own
embedded diagram images (`D10`, `D16`, both served from `abs.gov.au`) were fetched and
pixel-sampled directly to confirm field style and colour, since the page's guidance text alone
does not carry colour information. Contrast and hue values computed with
`skill/document-design-intelligence/scripts/lib/color.py`. Scratch files (HTML, CSS, diagram
PNGs, pixel probes) lived in `research/designs-evidence/tmp-sc2/form/` and are deleted at the end
of this task.

**Sample (n=4, all items):** `FMA:001, FMA:002, FMA:003, FMA:004`.

## Coding table

| id | columns | heading class | body class | colour use | field style | rules/boxes | density | admissible |
|---|---|---|---|---|---|---|---|---|
| FMA:001 (USWDS) | 2-sidebar (left `site-sidenav` holds secondary/navigational content, ≤40% width) | serif (page `<h1>` uses `Merriweather Web` per the site's own default `styles.css` rule; the alternate `Source Sans Pro` `h1` rule only applies under a `.sans-style` body class, absent on this page — confirmed from `<body class="page-form layout-styleguide ">`) | sans (`Source Sans Pro Web` body/paragraph font) | one-accent (`.usa-link{color:#005ea2}` is the only accent colour actually used on this page — the CSS also defines an error red `.usa-error-message{color:#b50909}`, but neither `usa-input--error` nor `usa-error-message` occurs in this page's own HTML, so that colour is not present here, disclosed) | box (`.usa-input,.usa-select{border-width:1px;border-color:#5c5c5c;border-style:solid;border-radius:0}` — a bordered rectangle, not an underline) | boxes (bordered inputs; #005ea2 is not an Office-default blue, no A7 concern) | dense (long guidance page: component description, do/don't guidance, accessibility notes, code examples) | yes |
| FMA:002 (GOV.UK) | 2-sidebar (`category-nav`/`app-subnav` side navigation, ≤40% width) | sans (`h1,.govuk-heading-xl{font-family:"GDS Transport",arial,sans-serif}`) | sans (`.govuk-body{font-family:"GDS Transport",arial,sans-serif}`) | one-accent (`--govuk-link-colour:#1a65a6`; no error state (`--govuk-error-colour:#ca3535`) is actually rendered on this specific `/patterns/` index page — it is a link list, not a worked form — disclosed) | box (`.govuk-input{border:2px solid;border-radius:0;border-color:var(--govuk-input-border-colour,#0b0c0c)}`, from the page's own linked stylesheet; no live `<input>` is rendered on this listing page itself, disclosed per the method note above) | boxes (box-style input rule; #1a65a6 is not an Office-default blue) | airy (the page itself is mostly a grouped list of links — "Ask users for…", "Help users to…", "Pages" — not running prose) | yes |
| FMA:003 (ABS) | 2-sidebar (`<aside id="left">` "On this page" TOC, ≤40% width) | sans (`body{font-family:Open Sans,...}`; only `Open Sans` is declared via `@font-face`, used for all heading levels) | sans (Open Sans) | one-accent — measured from the page's own embedded diagrams (D10, D16): the diagrams' pale-blue backdrop samples `#C0E8F8` (HSL L=0.86, S=0.80); at L<0.90 it is technically chromatic, but it covers the whole diagram canvas and reads as the diagram's background, excluded per B1a; the answer-box borders sample a distinct, saturated `#00A8E8`, appearing on every box in the grid (≥2 elements) — one hue, one cluster | box — the page's own text is explicit ("Outline answer box boundaries clearly," "Format ballot or tick boxes consistently") and its own diagram D16 (a numeric answer-box grid, i.e. the "contact grid" referenced in C29) and D10 (bordered instruction boxes) both show boxed fields, not underlines | boxes (bordered instruction panels and answer-box grids in the page's own diagrams; C29 disclosed: the box grid is field style, not a C7 all-cells data table, so C7 does not apply) | dense (long-form standards guidance text plus 20 embedded diagrams on one page) | yes |
| FMA:004 (NHS) | 2-sidebar (`app-side-nav`, ≤40% width) | sans (`Frutiger W01,arial,sans-serif`) | sans (Frutiger) | one-accent — `.nhsuk-input{border:2px solid #4c6272}`: HSL of `#4c6272` is H=205.3°, L=0.373, **S=0.200 exactly**, coded chromatic per C29's literal-boundary rule ("S >= 0.20 is chromatic, including exactly 0.2000"); NHS brand blue `#005eb8` (H=209.3°, S=1.0) is within 30° of the border hue, so both join one cluster → one-accent, matching C29's own worked outcome for NHS | box — `.nhsuk-input{border:2px solid #4c6272;border-radius:0}`, a bordered rectangle | boxes (bordered input; #005eb8/#4c6272 are not Office-default blues) | dense (long component-guidance page with prose, do/don't examples and code snippets) | yes |
