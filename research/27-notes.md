# Notes for 27-t14-font-substitutes-draft.csv

15 rows, matching T14's exact 5 columns (`09-library-schema.md:1419-1425`) —
`proprietary_family`, `Substitute Family`, `Lineage`, `Licence`, `Metric Identical`.
Validated with `csv.reader`: header 5 cols, 15 data rows, no malformed rows.

**Why 15, not the assignment's "~10–14":** 8 of the 15 rows are three families
(Arial, Times New Roman, Courier New) each carrying two rows — one Liberation, one
Croscore — because both lineages independently claim metric compatibility with the
same target under different licences, and the schema's own T14 example block already
does this for Arial (`09-library-schema.md:1430-1431`, both `Liberation Sans` and
`Arimo` as separate rows). Splitting matches established precedent rather than
picking one lineage arbitrarily; a project with a licence constraint needs both
options visible. 15 is the honest count once that pattern is applied consistently
across all three Liberation/Croscore-covered families, not padding.

**`Metric Identical` is left blank, not `no`, on the six no-substitute rows**
(Candara, Corbel, Constantia, Consolas, Verdana, Trebuchet MS) — a deliberate
deviation from the schema's own example rows, which use `no`
(`09-library-schema.md:1437-1439`). Reasoning: the column describes a property of an
actual substitution: does the reflow match. Where `Substitute Family` is blank there
is no substitution to be identical or not, and `no` on that value collapses "a
substitute exists but its metrics differ" (a real, different case — Helvetica→Arial
is exactly this, and is *not* in this CSV for that reason) into the same signal as
"no substitute exists at all." `validate-substitute-available` needs to tell those
two cases apart to know whether a `safe-stack` target has any fallback identity at
all; a blank cell preserves that distinction, `no` erases it. Flagging in case the
schema author prefers to keep the example's convention regardless.

T14 has no column for source URL, "bundled by," or caveats — same situation as T7 in
the previous task, and handled the same way: those live here, keyed by row, not
invented as extra CSV columns.

---

## Flag for the schema author: `Lineage` enum has no slot for Gelasio

T14's `Lineage` column is a closed enum: `liberation`\|`croscore`\|`crosextra`\|`none`
(`09-library-schema.md:1423`). Gelasio (Georgia's substitute) is none of the three —
it's an independent project by Sorkin Type Co, not a Google Croscore/Crosextra release
and not Liberation. I did not force it into one of the three wrong buckets, and I did
not silently drop a real, sourced substitute to make the enum happy. The CSV ships the
row with `Lineage=other`, which is **not currently a valid enum value** — flagging
explicitly rather than let `validate-checks-implemented`-style enum checking discover
it silently. The schema needs either a fourth enum value (`other`, or name it after
the foundry) or a policy for independent-project substitutes if more of these turn up
(nothing else in this batch needed it — Gelasio is the only one).

---

## §1 — Sources, per row

**Liberation → Arial / Times New Roman / Courier New** (rows 1, 3, 5). OFL-1.1.
Project: [github.com/liberationfonts/liberation-fonts](https://github.com/liberationfonts/liberation-fonts)
("The Liberation™ Fonts is a font family which aims at metric compatibility with
Arial, Times New Roman, and Courier New"). **The README confirms the three-family
target as a set but doesn't name the individual font-to-font mapping** (which of the
family's own font files maps to which target). Row 5's specific pairing (Liberation
Mono ↔ Courier New) is carried forward from `19-notes.md` line 120-121, a teammate's
summary, not independently re-confirmed against the README this round — same
carried-forward treatment as the Croscore mappings below, flagged the same way for
consistency. **Caveat, sourced and worth the task's explicit call-out:** pre-2.0 Liberation was built on Ascender Corp's original
commissioned metrics under GPL-with-font-exception; **2.0.0 onward was rebuilt on
Croscore's metrics and re-licensed to OFL** ([Fedora Features/Liberation_Fonts_2
wiki](https://fedoraproject.org/wiki/Features/Liberation_Fonts_2); confirmed via the
project's own GitHub). Both generations target the same three Microsoft fonts, but
they are not the same underlying design — if a doctype or a bundled OS ships an old
1.x Liberation build, don't assume it matches whatever 2.x metrics a newer reference
used to validate against. Bundled by: LibreOffice default (`19-notes.md` §
"Metric-compatible-substitute logic").

**Croscore → Arial / Times New Roman / Courier New** (rows 2, 4, 6). Apache-2.0.
Arimo/Tinos/Cousine, Google via Ascender. Sources: [Croscore fonts,
Wikipedia](https://en.wikipedia.org/wiki/Croscore_fonts) (already verified against
current sources in `19-notes.md`, not re-verified independently this round —
carried forward); Google Fonts specimens
[Arimo](https://fonts.google.com/specimen/Arimo),
[Tinos](https://fonts.google.com/specimen/Tinos),
[Cousine](https://fonts.google.com/specimen/Cousine). Bundled by: Chrome OS.

**Crosextra → Calibri / Cambria** (rows 7, 8). OFL-1.1 (not Apache — `19-notes.md`
flags this as a self-correction against an initial wrong assumption, confirmed this
round against [Carlito's own GitHub](https://github.com/googlefonts/carlito) and the
[Debian wiki's substitution
page](https://wiki.debian.org/SubstitutingCalibriAndCambriaFonts)). **Caveat per the
task's explicit ask:** Carlito ships only 2 weights — Regular (400) and Bold (700),
each with a matching italic, i.e. 4 total styles (Regular/Bold/Italic/Bold Italic) —
confirmed against [fonts.google.com/specimen/Carlito](https://fonts.google.com/specimen/Carlito)
and the GitHub repo. If a doctype's T5 row calls for a Calibri weight outside that set
(Light, SemiBold, etc.), Carlito has no matching weight and the substitution silently
degrades to the nearest available one — not flagged by `Metric Identical: yes`, which
only speaks to the weights that do exist. Bundled by: LibreOffice (Carlito and Caladea
are both LibreOffice's Calibri/Cambria substitution defaults, same source as
Liberation's LibreOffice-default note in `19-notes.md`).

**Georgia → Gelasio** (row 13). OFL-1.1. Independent project, Sorkin Type Co
(also behind Merriweather, already in the T5 catalog per `19-notes.md` §2). Project's
own statement, not a blog, per the task's requirement: "Gelasio is an original
typeface which is metrics compatible with Georgia in its Regular, Bold, Italic and
Bold Italic weights" —
[github.com/SorkinType/Gelasio](https://github.com/SorkinType/Gelasio) README, also
mirrored at [fonts.google.com/specimen/Gelasio](https://fonts.google.com/specimen/Gelasio).
**Same weight-coverage caveat as Carlito, sourced from the same README**: newer
Gelasio weights (Medium, Medium Italic, SemiBold, SemiBold Italic) have **no Georgia
equivalent** — the metric-compatibility claim is scoped to Regular/Bold/Italic/Bold
Italic only. The README also notes Gelasio deliberately omits kerning to preserve
functional parity with Georgia. Bundled by: not OS/Office-bundled anywhere found;
download-only.

**Candara / Corbel / Constantia / Consolas → none** (rows 9–12). Confirmed no
established metric-compatible substitute exists, carried forward from `19-notes.md`
§1 (already checked against current web sources there, not re-verified independently
this round). These four are Office-bundled, not OS-bundled, on both Windows and Mac
(`19-notes.md` line 40-43) — a `safe-stack` target needing one of these four has no
safe fallback identity at all if the recipient might open the file outside Microsoft
Office.

**Verdana → none** (row 14). **Checked and rejected a candidate, per the task's
explicit instruction not to offer a look-alike.** DejaVu Sans is widely repeated
across secondary/SEO font-comparison sites as "metrically compatible with Verdana,"
but I could not find that claim on the DejaVu project's own site
([dejavu-fonts.github.io](https://dejavu-fonts.github.io/) — fetched directly, no
mention of Verdana or metric compatibility anywhere on the page) or in
[Wikipedia's DejaVu fonts article](https://en.wikipedia.org/wiki/DejaVu_fonts) (which
states DejaVu is derived from Bitstream Vera and says nothing about Verdana metrics).
DejaVu Sans is a genuinely similar-looking, well-regarded open sans — it is not a
sourced metric-compatible substitute, which is the specific claim this table exists
to make reliably. Reported `none` rather than a plausible-but-unverified row.

**Trebuchet MS → none** (row 15). No project claiming metric compatibility with
Trebuchet MS found in any search this round — not even a secondary-source rumor the
way Verdana/DejaVu had one. Reported `none`.

---

## §2 — "No substitute exists" list

Candara, Corbel, Constantia, Consolas, Verdana, Trebuchet MS. Six families, no
established metric-compatible open substitute. A `safe-stack` render target resolving
to any of these has no safe fallback identity and must embed the real font or avoid
the family — exactly the case `validate-substitute-available` exists to catch
(`09-library-schema.md:1460-1462`).

Not covered by this task and not included: Helvetica (`19-notes.md` line 48 already
notes Arial as "the conventional stand-in," explicitly **not** metric-identical —
would need its own `Metric Identical: no` row if the schema wants it) and Aptos
(already a `none` example row in the schema itself, `09-library-schema.md:1439` — not
duplicated here).
