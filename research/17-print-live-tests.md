# Live Sandbox Print Tests

Three copy-paste prompts for claude.ai, settling the two unverified items in
`research/14-print-production-values.md` §5 plus network availability. Paste each
prompt verbatim in its own conversation.

---

## Test 1 — Bleed fill behaviour

**Prompt (paste verbatim):**

~~~
Run these steps in order and report results exactly as asked at the end.

1. Run `pip install "weasyprint>=67"` and print the installed version. Expect >=67
   (current release is 69.0); flag it if pip resolves something older.

2. Save the file between BEGIN_HTML and END_HTML below as bleed_test.html
   (do not include the BEGIN_HTML/END_HTML lines themselves):

BEGIN_HTML
```html
<!DOCTYPE html>
<html><head><style>
@page { size: 148mm 210mm; margin: 0; bleed: 3mm; marks: crop cross; }
html { margin: 0; background: #d81b60; }
body { margin: 0; }
</style></head><body></body></html>
```
END_HTML

3. Render it: `weasyprint bleed_test.html plain.pdf`

4. Save the script between BEGIN_PY and END_PY below as inspect.py and run it
   with `python inspect.py plain.pdf`. It must use only the stdlib (re, zlib) —
   no pypdf, no PyMuPDF, no other PDF library.

BEGIN_PY
```python
import re, zlib, sys

data = open(sys.argv[1], "rb").read()

def inflate_all(data):
    out = bytearray()
    pos = 0
    for m in re.finditer(rb'stream\r?\n', data):
        out += data[pos:m.start()]
        start = m.end()
        end = data.find(b'endstream', start)
        chunk = data[start:end]
        try:
            chunk = zlib.decompress(chunk)
        except Exception:
            pass
        out += b'\n' + chunk + b'\n'
        pos = end
    out += data[pos:]
    return bytes(out)

text = inflate_all(data)

def grab(pattern):
    m = re.search(pattern, text)
    return m.group(0).decode('latin1') if m else None

print("page count:", len(re.findall(rb'/Type\s*/Page[^s]', text)))
print("MediaBox:", grab(rb'/MediaBox\s*\[[^\]]*\]'))
print("TrimBox:", grab(rb'/TrimBox\s*\[[^\]]*\]'))
print("BleedBox:", grab(rb'/BleedBox\s*\[[^\]]*\]'))
```
END_PY

Report the script's printed output verbatim, plus your pip-installed WeasyPrint
version.
~~~

**PASS:** page count = 1. Trim size is A5 in points (148mm/210mm × 72/25.4 ≈
419.5 × 595.3pt). `BleedBox` is present and is exactly 8.5pt (3mm) larger than
`TrimBox` on every side — e.g. `TrimBox [8.5 8.5 428.0 603.8]` and
`BleedBox`/`MediaBox` `[0 0 436.5 612.3]` is the expected shape, **but the exact
origin convention (whether TrimBox is inset within a `[0 0 …]` MediaBox, or
some other offset) is inferred, not independently observed — the test result is
authoritative over this document.** The one number that must hold regardless of
origin: `BleedBox − TrimBox = 8.5pt on each side`.

**FAIL:** `BleedBox` absent, or equal to `TrimBox` (bleed declaration silently
dropped), or `MediaBox` clipped to `TrimBox` size (background never reaches the
declared bleed edge — the exact defect GitHub issues Kozea/WeasyPrint#934 and
#1446 describe).

**Consequence for schema:** PASS → T8's `pdf-weasyprint` row `Supports Bleed`
changes from `no` to `yes`, sourced to this test run + version number reported.
FAIL → `Supports Bleed` stays `no`; file the failing box values against the
GitHub issues above so the next retest has a version to watch for.

**Verified live (user's claude.ai sandbox, WeasyPrint 69.0):**

```
TrimBox  [0 0 419.527559 595.275591]
BleedBox [-8.503937 -8.503937 428.031496 603.779528]
MediaBox == BleedBox
```

**PASS, confirmed.** `BleedBox − TrimBox` is exactly 8.503937pt (3mm converted
precisely) on every side, matching this test's pass criterion exactly. Note the
origin convention that landed: `TrimBox` sits at `[0 0 …]` and `BleedBox` extends
*outward* into negative coordinates, not the other way around — the reverse of
this document's own inferred guess (§ above flagged the guess as unverified for
exactly this reason). `MediaBox == BleedBox` — the page canvas extends to the
bleed edge, which is the behavior the GitHub issues (#934, #1446) were about; this
run shows no sign of that defect at 69.0.

**Caveat, as reported by the user's Claude:** `MediaBox == BleedBox` with no extra
room beyond it for crop marks — expected here, since this test's HTML used
`marks: crop cross` in `@page` but a plain `BleedBox`-sized canvas is correct
PDF/X behavior regardless: crop marks are drawn *within* the existing bleed
allowance area in most RIP conventions, not added as extra canvas beyond it, so
their absence from the box dimensions isn't itself a finding. **What was not
checked:** whether the full-bleed color block's fill actually reaches the
`BleedBox` edge, as opposed to just the box existing with the right geometry. One
extra line settles it: render the PDF's first page to a PNG at the `MediaBox`
size (`weasyprint bleed_test.html check.png --resolution=72` or equivalent) and
confirm the fill (`#d81b60`) is the pixel color at `(0,0)` and at the far
corners — if the corners are white/background instead, the box is declared but
the paint doesn't reach it, which the box-geometry check alone cannot catch.

**T8 consequence, updated from conditional to confirmed:** `pdf-weasyprint`'s
`Supports Bleed` is `yes`, sourced to this run (WeasyPrint 69.0, user's claude.ai
sandbox), with the geometry check passing exactly. Not yet confirmed: that the
painted content (not just the box) extends to the bleed edge — see the one-line
check above. `pdf-weasyprint-pdfx4` / tier 2 remains unconfirmed pending Test 2's
result (still outstanding).

---

## Test 2 — PDF/X-4 + sRGB output intent validity

**Prompt (paste verbatim):**

~~~
Run these steps in order and report results exactly as asked at the end.

1. Run `pip install "weasyprint>=67"` and print the installed version.

2. Save the file between BEGIN_HTML and END_HTML below as pdfx4_test.html
   (reuse Test 1's file if you already have it — it's identical):

BEGIN_HTML
```html
<!DOCTYPE html>
<html><head><style>
@page { size: 148mm 210mm; margin: 0; bleed: 3mm; marks: crop cross; }
html { margin: 0; background: #d81b60; }
body { margin: 0; }
</style></head><body></body></html>
```
END_HTML

3. Render it as PDF/X-4 with an sRGB output intent:
   `weasyprint pdfx4_test.html pdfx4.pdf --pdf-variant=pdf/x-4 --output-intent=srgb`

4. Save the script between BEGIN_PY and END_PY below as inspect_x4.py and run
   it with `python inspect_x4.py pdfx4.pdf`. Stdlib only (re, zlib) — no PDF
   library.

BEGIN_PY
```python
import re, zlib, sys

data = open(sys.argv[1], "rb").read()

def inflate_all(data):
    out = bytearray()
    pos = 0
    for m in re.finditer(rb'stream\r?\n', data):
        out += data[pos:m.start()]
        start = m.end()
        end = data.find(b'endstream', start)
        chunk = data[start:end]
        try:
            chunk = zlib.decompress(chunk)
        except Exception:
            pass
        out += b'\n' + chunk + b'\n'
        pos = end
    out += data[pos:]
    return bytes(out)

text = inflate_all(data)

def grab(pattern):
    m = re.search(pattern, text, re.DOTALL)
    return m.group(0).decode('latin1', 'replace') if m else None

# PDF/X-4 identifies via XMP (pdfxid:GTS_PDFXVersion) more often than the
# legacy Info-dict key, so search broadly for either.
print("GTS_PDFXVersion mention:", grab(rb'GTS_PDFXVersion[^<)]{0,40}'))
print("OutputIntents block:", grab(rb'/OutputIntents\s*\[.{0,300}?\]'))
print("OutputConditionIdentifier:", grab(rb'/OutputConditionIdentifier\s*\([^)]*\)'))
print("DeviceRGB Group count:", len(re.findall(rb'/Group\s*<<[^>]*?/CS\s*/DeviceRGB', text)))
```
END_PY

Report the script's printed output verbatim, plus your pip-installed WeasyPrint
version. If you have access to a PDF/X validator (Acrobat Preflight, veraPDF, or
similar), run it too and report pass/fail and any error text.
~~~

**PASS:** `GTS_PDFXVersion mention` contains `PDF/X-4` (Info dict or XMP, either
counts). `OutputIntents block` is non-empty. `OutputConditionIdentifier` (or
nearby `/Info` string) contains `sRGB`. `DeviceRGB Group count` > 0 is expected
and benign here — WeasyPrint hardcodes DeviceRGB transparency groups
unconditionally, and that's only a spec violation when the output intent is
CMYK (Kozea/WeasyPrint#2723); with an sRGB output intent the two agree, so a
nonzero count is not itself a fail signal. If a real validator was run, it
reports no color-space/output-intent conflict — that validator result is what
actually confirms or refutes the #2723 caveat, not the count on its own.

**FAIL:** no `GTS_PDFXVersion` mention anywhere (file isn't tagged as PDF/X-4 at
all), or `OutputIntents block` empty/absent, or a validator flags the
`DeviceRGB Group` entries as inconsistent with the output intent regardless of
the count being "expected."

**Consequence for schema:** PASS on both boxes and a clean validator run → T8
gets a new row (or a `Colour Space` value) for a `pdf-weasyprint-x4-rgb` /
similar target: structurally press-ready, RGB, no CMYK ICC asset needed —
promote `professional` print mode from hard-fail to a real resolvable target
for this tier specifically (still not full CMYK press-ready). FAIL on the
validator specifically (boxes/intent present but validator rejects) → keep
`professional` hard-failing, but note in `rationale/render-targets.md` that the
blocker is the DeviceRGB-Group bug, not a licensing or capability gap, so it's
worth re-testing on a future WeasyPrint release rather than closing the door.

---

## Test 3 — pip network availability (fresh conversation, one line)

**Prompt (paste verbatim, in a brand-new conversation, no prior context):**

~~~
In this fresh conversation with no prior setup, run: pip install "weasyprint>=67"
Report only: did it succeed or fail, the exact error if it failed, and the
resolved version number if it succeeded.
~~~

**PASS:** succeeds, version ≥67 reported.

**FAIL:** any network/resolution error (no PyPI access from this sandbox by
default).

**Consequence for schema:** PASS → T8's `pdf-weasyprint` (and any new PDF/X-4
row from Test 2) can keep `Availability: pip` as a plain default. FAIL →
`Availability: pip` for every WeasyPrint-based row must be reclassified as
conditional/`unverified` per `09-library-schema.md:524` ("a doctype whose only
render target is pip-availability fails preflight when network is absent") —
this decides whether tier 2 (§1 of report 14) can ever be promised by default
or only opportunistically.
