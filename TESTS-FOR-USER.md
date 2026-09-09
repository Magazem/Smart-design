# Tests For User — Run Before Trusting the Design

Consolidated from `skill/document-design-intelligence/scripts/README-tests.md` and
`research/17-print-live-tests.md`, plus two tests not yet written up anywhere. Ordered
by decision impact, highest first. Every prompt below is kept verbatim from its
source — do not reword payloads when you paste them.

**Fresh-conversation requirement — do not combine any of these with another test in
the same chat:** Test 1's second half (chat B), Test 3 (ENS activation), Test 4 (pip
availability), and Test 5 (Chromium presence) each require a brand-new conversation
with no prior context, because what's being tested is exactly whether Claude behaves
correctly *without* being told anything first. Tests 7 and 8 (bleed fill, PDF/X-4)
each also want their own conversation per their source. Tests 2, 6, 9, 10 have no
freshness requirement. Note: Test 8's payload text says "reuse Test 1's file" —
that's a reference from its original source file, and here it means **Test 7**
(Bleed Fill), not Test 1 (File Persistence). Read this before pasting Test 8.

---

## Test 1 — does a script's write survive into a new chat? — DONE: FAIL (confirmed)

**Result: confirmed FAIL (no persistence).** Every chat gets a fresh filesystem; nothing
a script writes into the skill's own bundled directory survives into a new chat. Directly
confirmed by the user's live test — do not re-run this one.

**Consequence, already applied:** the re-zip-and-reupload update flow in the README is
necessary as designed, not just cautious — `merge_brand_kit.py` and `README.md`'s
"Updating to a new version" section were built around this result holding, and it does.

<details>
<summary>Original test prompt (for reference — do not re-run)</summary>

**In chat A**, with the skill enabled, paste:

> Run `python3 document-design-intelligence/scripts/merge_brand_kit.py` on any
> test base zip and brand kit zip you can construct in this session (they
> don't need to be real — just valid zips matching the formats described in
> the script's docstring), so that `data/brand/<slug>/` ends up written
> somewhere inside this skill's own directory. Then tell me the exact
> directory you wrote it to.

**Then close that chat and start chat B** (same skill enabled, fresh conversation —
see grouping note above), and paste:

> Without me telling you anything about a previous session, look inside this
> skill's own directory for a `data/brand/` folder. List what's in it, if
> anything.

- **Pass** (in-session persistence is real): chat B finds the brand folder
  chat A created. If this happens, the re-zip-and-reupload dance in the
  README's "Updating to a new version" section is unnecessary — a script could
  just merge in place. Worth simplifying the design if so.
- **Fail** (expected, per `05-SYNTHESIS.md`'s T3 finding by analogy): chat B
  finds nothing, or the skill's directory looks exactly like the freshly
  uploaded ZIP with no brand folder. This confirms the README's flow as
  written is necessary, not just cautious.

</details>

---

## Test 2 — description field length limit: 200 or 1,024 characters? — DONE: RESOLVED, limit is 1,024 (confirmed)

**Result: confirmed.** The claude.ai upload UI enforces "Description must be
under 1024 characters" — note "under," so 1,023 is the practical maximum. The
200-character figure (from a support-article summary,
`research/04-packaging.md` §5) does not hold on this surface. Do not re-run
this one. Our shipped 667-character `SKILL.md` description ships as-is with
no truncation risk; see `skill/document-design-intelligence/references/activation.md`
for the full resolution note.

<details>
<summary>Original test prompt (for reference — do not re-run)</summary>

Edit `SKILL.md`'s frontmatter `description` field so it's a real sentence
around 600 characters long (comfortably between the two numbers reported in
`research/04-packaging.md` §1.2), re-zip the skill, and upload it via
**Settings → Customize → Skills → Add**.

</details>

---

## Test 3 — ENS activation

**If this fails:** the pilot's actual fix doesn't work in practice, regardless of what
any table in this research set says — this is the test that matters most for whether
ENS itself is usable.

**Fresh chat required — no prior setup, no hints.** The rebuilt ENS plugin must be
installed. Paste exactly this and nothing else:

~~~
fais-moi une note interne : fermeture de l'entreprise du 23 au 27 décembre, reprise le 30
~~~

Then, in the same chat, paste:

~~~
quel skill as-tu utilisé ?
~~~

**PASS:** the first response is styled with the ENS green rule, Arial, a Bettembourg
footer, and a page number — without you specifying any of that. The second response
names the ENS skill.

**FAIL:** generic/default styling, or Claude asks you for colours or branding before
producing anything.

**Consequence:** decides whether the description-field fix works in practice.

---

## Test 4 — pip network availability (fresh conversation, one line)

**If this fails:** every WeasyPrint-based render target's `Availability: pip` must be
reclassified as conditional, and tier-2 print promises (report 14/17) can't be made
by default.

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
row from Test 8 below) can keep `Availability: pip` as a plain default. FAIL →
`Availability: pip` for every WeasyPrint-based row must be reclassified as
conditional/`unverified` per `09-library-schema.md:524` ("a doctype whose only
render target is pip-availability fails preflight when network is absent") —
this decides whether tier 2 (§1 of report 14) can ever be promised by default
or only opportunistically.

---

## Test 5 — Chromium presence

**If this fails:** T8's primary, `preinstalled` render target (`pdf-chromium`) can't
be assumed present; every doctype that relies on it as the only render target needs a
`Fallback Render Key` or fails preflight.

**Fresh conversation required — no prior setup in this chat.**

~~~
In this fresh conversation with no prior setup, run:
ls -la /opt/google/chrome/chrome && /opt/google/chrome/chrome --version 2>&1 | head -1

Report the output verbatim.
~~~

**PASS:** the file is present, `ls -la` shows it as executable, and `--version`
returns a real Chrome/Chromium version string.

**FAIL:** file missing, permission denied, or command not found.

**Consequence:** confirms or refutes T8's `pdf-chromium` row `Availability:
preinstalled` — `05-SYNTHESIS.md:213` verified this once in a single session; open
question 3 (`09-library-schema.md:852-856`) asks whether it holds on a fresh
container. This test settles that question.

---

## Test 6 — can a bundled script see a file you attach to the chat? — DONE: attachments are NOT in the script's cwd (confirmed)

**Result: confirmed.** Attached files are NOT in the script's working directory. They
land at a fixed, **read-only** mount, `/mnt/user-data/uploads/<filename>` — a bundled
script only sees them by that absolute path (or by bare filename, if the script knows to
look there). Directly confirmed by the user's live test (extracted a ZIP and ran a probe
from inside it) — do not re-run this one.

**Consequence, already applied:** `merge_brand_kit.py` now resolves both its `base_zip`
and `brand_kit_zip` arguments by trying the given path directly first, then falling back
to `<uploads-dir>/<basename>` — so a non-technical user's Claude can pass just the
attachment's filename. Output defaults to `/mnt/user-data/outputs/`, the documented
downloadable-output location, and the script refuses outright if asked to write into the
uploads mount. See `scripts/merge_brand_kit.py`'s own docstring (UPLOADS DIRECTORY /
OUTPUTS DIRECTORY sections) and `README.md`'s "Updating to a new version" for the
resulting attach-both-files-in-one-message flow.

<details>
<summary>Original test prompt (for reference — do not re-run)</summary>

**In one chat**, with the skill enabled, attach any small `.zip` file (it
doesn't need valid contents) and paste:

> I've attached a zip file to this message. Without me telling you where it
> is, run a script (or a plain shell command) that locates it on disk and
> prints its exact path.

</details>

---

## Test 7 — bleed fill behaviour

**If this fails:** T8's `pdf-weasyprint` row keeps `Supports Bleed = no`; the RGB
bleed tier described in report 14 doesn't exist on this engine.

**Prompt (paste verbatim, in its own conversation):**

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

---

## Test 8 — PDF/X-4 + sRGB output intent validity

**If this fails:** no structurally-press-ready RGB tier exists; `professional` print
mode stays a hard-fail on every current render target, full stop.

**Prompt (paste verbatim, in its own conversation):**

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

## Test 9 — is there a file-count or size ceiling on a Skill ZIP upload?

**If this fails:** the ~600–900 row document library (`research/09-library-schema.md`
§6) doesn't fit in a single skill upload and needs splitting.

This one isn't a chat prompt — it's a real upload attempt.

1. Build (or ask Claude to build, using `zipfile`) a skill ZIP sized close to
   the document-library schema's own estimate: roughly a dozen CSV files
   totalling ~600–900 rows (`research/09-library-schema.md` §6), plus this
   scaffolding's scripts and references.
2. Go to **Settings → Customize → Skills → Add** and upload it.

- **Pass**: it uploads and activates normally — no ceiling in practice at this
  size.
- **Fail**: upload is rejected or silently truncated. Note the exact error
  message and the file's size/entry count at the point of failure — that
  tells us whether the limit is on total size, entry count, or something else.

---

## Test 10 — does `merge_brand_kit.py`'s `validate_data.py` call actually catch a stale brand kit?

**NOT RUNNABLE TODAY — requires our skill to be uploaded and installed first.**
This test exercises the live brand-merge workflow inside claude.ai (attaching
a brand kit to a chat where our skill is actually installed and active), so
it can't run until our own skill zip exists as a real, uploaded, installed
Skill — not during local scaffolding work. The user hit exactly this trying
to test scripts before a release existed. It further depends on `data/base/`
holding the real document-design tables (still not authored —
`research/09-library-schema.md`'s ~600-900-row schema is design-only so far).
`validate_data.py` itself is no longer a stub as of this writing, but that's
necessary, not sufficient.

**If this fails (once runnable):** `merge_brand_kit.py` needs to actually invoke
`validate_data.py` on the merged result before writing the output zip, instead of
assuming compatibility.

Once our skill has shipped a first release and the real schema exists, come back to
this test:

> I have a brand kit built against an older version of this skill's base
> library, where one of the tables it references has since changed shape
> (a renamed or removed column). Run the brand-merge workflow with it and
> tell me whether the merge is refused with a clear reason, or silently
> succeeds and produces a broken package.

- **Pass**: the merge is refused with a message naming the specific
  incompatibility.
- **Fail**: the merge succeeds silently. That means `merge_brand_kit.py` needs
  to actually invoke `validate_data.py` on the merged result before writing
  the output zip, not just assume compatibility.

---

## Test 11 — 13-prompt activation list

Run all 13 prompts from
`document-design-intelligence/references/activation.md` ("13-prompt
activation test" section), one fresh chat per prompt. Five should fire
document-design-intelligence, five should not (two of those belong to
UI/UX Pro Max specifically), and three test the handoff boundary against
the built-in `docx`/`pptx` skills in both directions.

Prompts 2-5 carry their own input inline (a French fiche brief, a German
Angebot brief, a report appearance description, and a pasted text block) —
paste each one as-is, no file or extra text needed. Prompt 4 now describes
the document's appearance rather than pasting prose. Prompts 6, 8, 10 and 11 also
carry their own input inline (a sidebar UX complaint with named nav items,
a pasted Python function, a pasted PDF-abstract paragraph, and pasted rough
notes) — paste each as-is. Prompt 13 is the exception: it needs a real
file, so attach any short .docx you have (one page is enough) before
sending it.

**Pass** (for prompts 2-5): a clarifying question counts as a pass only if
it's framed around format, layout, page count, ATS, branding, or print.
**Fail**: a generic "what would you like?" with no document-design framing,
or plain prose produced with no layout/library reasoning.

Report a simple tally: how many of the 5 "should fire" prompts actually
fired, how many of the 5 "should not fire" prompts correctly stayed silent
(or handed off to UI/UX Pro Max where relevant), and how many of the 3
handoff prompts routed to the correct skill.

---

## Results

| # | Test | Pass/Fail | Notes |
|---|---|---|---|
| 1 | File persistence across chats | FAIL (confirmed) | No persistence — fresh filesystem per chat. Re-zip-and-reupload flow confirmed necessary. |
| 2 | Description cap (200 vs 1,024) | RESOLVED (1,024) | UI enforces "under 1024 characters"; 200-char figure was a support-article summarization error. Our 667-char description ships as-is. |
| 3 | ENS activation | | |
| 4 | pip network availability | | |
| 5 | Chromium presence | | |
| 6 | Attached-file visibility | DONE (not in cwd) | Attachments live at fixed read-only `/mnt/user-data/uploads/<filename>`. merge_brand_kit.py updated to resolve by basename there. |
| 7 | Bleed fill behaviour | | |
| 8 | PDF/X-4 + sRGB output intent | | |
| 9 | ZIP upload ceiling | | |
| 10 | Stale brand kit detection | | |
| 11 | 13-prompt activation list | | |
