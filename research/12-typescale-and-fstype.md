# Type-scale tuples and fsType-via-stdlib — answers to schema sub-questions

## Q1 — Type-scale tuples (T6)

**Definitive answer to the specific question: photocopy does not need a full scale, or
even a partial one.** Report 03 contains no photocopy-specific point-size threshold
anywhere. The photocopy risk I identified (ENS review, finding #10) is a **color/weight**
problem, not a size problem: a mid-lightness ink (e.g. #1F6F43, L*≈41) renders as gray on
a monochrome copy and that gray reads worse at small sizes than true black does at the
same size — but the mechanism is the color, not the point size. Recommend **cutting
`photocopy` as a `Medium` value in T6 entirely** and replacing it with a T9 constraint:
`photocopy-safe-color | validate-text-safe-color | role=label,legal | l_star_max=15 | warn`
(near-black only, for the smallest roles, in doctypes marked photocopy-safe) —
`Severity: warn`, because this is my own convention-level reasoning, not a report-03
[FACT] with a sourced number. The `photocopy-body-min: 8.5pt` row in T9's draft examples
should be dropped; I have no source for it as a size threshold.

**A more important finding: report 03 gives no absolute point-size floor for print at
all.** Its two print-typography rules are both *ratios/ranges relative to the reading
context*, not fixed numbers:
- Measure: 45–75 characters per line (Bringhurst) — a function of body size × column
  width, not a size on its own.
- Leading: 120–145% of body size — a ratio, not a size.

This means `Size pt` for any print role (body, label, caption, legal, h1–h3, lead,
footer) **cannot be filled from report 03 as a static lookup value.** Any number placed
there is either (a) a brand's own house choice — fine, but it's authored, not derived,
and should be validated by the *formula*, not by a floor — or (b) an invented threshold
with the same problem T11's `Min Physical Size mm` already got flagged for. Recommend
`validate-type-floor` for `medium=print` be rewritten as a **computed** check: resolve
body size × T7's column width (from page format/margins) → characters-per-line, assert
45–75; separately assert leading ∈ [1.20, 1.45] × body size. That is a join across T5/T6/T7,
not a per-role floor row — consistent with how `validate-contrast-print` already treats
L* delta as computed rather than authored (§ design notes, T4).

**What *is* sourced, by medium and role:**

| Medium | Role | Size pt | Leading | Tag | Source |
|---|---|---|---|---|---|
| projection | body | 24 (floor) | not established | CONVENTION | report 03 §B — general bullet/body floor, "never smaller" |
| projection | body-dense | 18 (floor) | not established | CONVENTION | report 03 §B — dense-data-callout exception only, not a default |
| projection | h1 (title) | 36–44 (range, not a point value) | not established | CONVENTION | report 03 §B |
| screen | body | 18–20 (floor) | not established | CONVENTION | report 03 §B — screen-only decks (webinar/shared-screen), explicitly distinct from projection |
| screen | h1 (title) | *no source* | *no source* | — | report 03 gives no screen-specific title size; do not assume it inherits projection's 36–44 without saying so |
| print | body | *no source* (formula only: leading 1.20–1.45×, CPL 45–75) | 1.20–1.45× body | CONVENTION (Bringhurst) | report 03 §D |
| print | label / caption / legal / lead / h1 / h2 / h3 / footer | *no source* | *no source* | — | report 03 never gives print role sizes — see finding above |
| photocopy | (any) | *no medium* — see recommendation above | — | — | not covered by report 03 as a size axis |

Not in T6 at all, but sourced and belongs somewhere (T9, density not size):
`deck-density`: max 5–6 bullets/slide, max ~6 words/bullet (6×6 heuristic) — report 03 §B,
CONVENTION, already correctly placed in T9's example rows, not T6.

**Net effect on T6:** the table's four-medium enum (`print`/`projection`/`screen`/
`photocopy`) is right for `projection` and `screen`, wrong for `photocopy` (cut it), and
structurally mismatched for `print` (report 03 doesn't produce lookup rows there — it
produces a formula T7 needs to feed). Fewer sourced rows: the honest projection+screen
table is 4 rows, not ~10–15 per scale_key the draft's "~200 rows" estimate implies. Print
rows that do end up in T6 (e.g. ENS's actual 11pt/24pt choices) are brand-authored
constants validated by the formula, not report-03-sourced floors, and should be labeled
that way in `rationale/constraints.md` so nobody mistakes them for a sourced minimum later.

---

## Q2 — Can `fsType` be read with Python stdlib only?

**Yes, reliably.** `fsType` is a fixed-offset `uint16` inside the `OS/2` table, which is
itself a fixed-offset entry in the sfnt table directory every `.ttf`/`.otf` starts with.
No variable-length or nested parsing is needed — `struct` + `open` is sufficient.

```python
import struct

def read_fstype(font_path):
    with open(font_path, 'rb') as f:
        head = f.read(64 * 1024)  # table directory is always near the start
    sfnt_tag = head[0:4]
    if sfnt_tag not in (b'\x00\x01\x00\x00', b'OTTO', b'true', b'typ1'):
        return None, f"not a TTF/OTF (sfnt tag {sfnt_tag!r})"
    num_tables = struct.unpack('>H', head[4:6])[0]
    os2_offset = None
    for i in range(num_tables):
        rec = 12 + i * 16
        tag, _cksum, offset, _length = struct.unpack('>4sIII', head[rec:rec + 16])
        if tag == b'OS/2':
            os2_offset = offset
            break
    if os2_offset is None:
        return None, "no OS/2 table present"
    with open(font_path, 'rb') as f:
        f.seek(os2_offset + 8)          # fsType is the 3rd field in OS/2, offset 8
        fs_type = struct.unpack('>H', f.read(2))[0]
    usage = fs_type & 0x000F
    labels = {0: "Installable embedding (no restriction)",
              2: "Restricted License embedding (must NOT be embedded)",
              4: "Preview & Print embedding only",
              8: "Editable embedding only"}
    label = labels.get(usage, f"unrecognized usage bits {usage}")
    if fs_type & 0x0100: label += "; no subsetting"
    if fs_type & 0x0200: label += "; bitmap embedding only"
    return fs_type, label
```

Tested against six fonts in `C:\Windows\Fonts`, both TrueType (`\x00\x01\x00\x00`) and
CFF-flavored OpenType (`OTTO`) — using `C:\Users\ysuliman\AppData\Local\Microsoft\
WindowsApps\python3.exe` (3.12.10; the repo's own venv python is broken — `uv` trampoline
fails to spawn — noting that as a separate, unrelated environment issue):

```
arial.ttf:               fsType=8 -> Editable embedding only
calibri.ttf:              fsType=8 -> Editable embedding only
times.ttf:                fsType=8 -> Editable embedding only
consola.ttf:              fsType=8 -> Editable embedding only
DavidCLM-Bold.otf:        fsType=0 -> Installable embedding (no restriction)
MiriamLibre-Regular.otf:  fsType=0 -> Installable embedding (no restriction)
```

This directly disproves the premise the analyst cut the column on. **The licence column
should come back** as a real preflight check, independent of and complementary to the
post-render `zipfile`/`ppt:embeddedFont` assertion already in T5's design notes — this
checks *permission*, that checks *outcome*; together they catch both "silently refused to
embed" and "embedded something it legally shouldn't have."

**GSUB / `tnum` — structurally similar difficulty, semantically weaker answer.**

Finding the `FeatureList` in `GSUB` and checking whether a `tnum` tag exists is **not**
materially harder to parse — same fixed-offset-then-array-of-tagged-records technique:

```python
def has_tnum_feature(font_path):
    with open(font_path, 'rb') as f:
        data = f.read()
    num_tables = struct.unpack('>H', data[4:6])[0]
    gsub_offset = None
    for i in range(num_tables):
        rec = 12 + i * 16
        tag, _c, offset, _l = struct.unpack('>4sIII', data[rec:rec + 16])
        if tag == b'GSUB':
            gsub_offset = offset
            break
    if gsub_offset is None:
        return None  # no GSUB table at all
    fl_off = struct.unpack('>H', data[gsub_offset + 6:gsub_offset + 8])[0]
    fl = gsub_offset + fl_off
    count = struct.unpack('>H', data[fl:fl + 2])[0]
    tags = {data[fl + 2 + i * 6: fl + 6 + i * 6] for i in range(count)}
    return b'tnum' in tags
```

Ran it on the same six fonts: Arial, Calibri, Times New Roman, and Miriam Libre all
report `tnum` present; **Consolas reports `tnum` absent** — and Consolas is monospaced,
so every glyph is already fixed-width without needing a switchable OpenType feature.
That's the concrete case that proves the real problem: **tag presence and "has tabular
figures" are not the same fact.** A `tnum` tag means "this font can switch to tabular
figures via a feature," not "this font's default digits are tabular" — and a *missing*
tag is ambiguous between "no tabular figures exist" and "always tabular, no feature
needed." DavidCLM/MiriamLibre also came back `tnum: False` despite having GSUB tables
with dozens of other features — I can't tell from this check alone whether their digits
are proportional or simply tabular-by-default like Consolas.

Recommend building it, but only as a **strengthener for `yes`**, matching T5's existing
`unknown` escape hatch: `tnum` present → `Has Tabular Figures: yes` (high confidence);
`tnum` absent → stays `unknown`, never demoted to `no` from this check alone. A true `no`
would need glyph-width comparison of the digit glyphs themselves (`glyf`/`CFF ` + `hmtx`
advance widths for `zero`–`nine`), which is a materially harder parse — variable-length
glyph data, not fixed-offset records — and I did not build that.
