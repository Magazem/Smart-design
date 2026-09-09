# Local PDF/X-4 conformance check — preparation

**Headline finding, before anything else: veraPDF does not validate PDF/X.** It is
installed, confirmed working, and its report format is documented below — but the
task's premise (use veraPDF's `--flavour` flag to check PDF/X-4 conformance) doesn't
hold. veraPDF's built-in profiles are PDF/A (`1a`…`4e`), PDF/UA (`ua1`, `ua2`) and
WTPDF (`wt1r`, `wt1a`) only — confirmed by running the installed CLI's own `--list`
(below), and independently by veraPDF's own site ("Industry Supported **PDF/A**
Validation", verapdf.org) and docs.verapdf.org. There is no `--flavour` value for any
part of ISO 15930 (PDF/X). This isn't a version or install problem; the project has
never covered PDF/X — it was built under the PREFORMA archival-preservation program,
whose scope is PDF/A/UA, not prepress exchange.

I did not find a free, open-source, locally-runnable PDF/X-4 conformance validator
anywhere. What exists: Adobe Acrobat Preflight, callas pdfToolbox/pdfaPilot, Enfocus
PitStop, 3-Heights PDF Validator, VeryUtils PDF Validator — all commercial. Coherent
PDF (`cpdf`) can *report* a file's declared PDF/X conformance level but that is
metadata reading, not rule validation. No substitute proposed here — flagging the gap
honestly rather than presenting a partial check as more than it is.

**What this file actually delivers:** (1) veraPDF installed and proven to work, ready
if PDF/A/UA validation is ever needed elsewhere in this project; (2) a stdlib-only
structural inspection script — the same approach as `17-print-live-tests.md` Test 2,
extended — that checks the specific markers ISO 15930-7 requires; explicitly **not**
full conformance validation, since no tool available here can do that; (3) three
sourced, commonly-cited PDF/X-4 failure clauses to watch for; (4) the result of
running that script against `research/pdfx4.pdf`, which appeared during this task.

---

## 1. veraPDF — installed and confirmed working

| | |
|---|---|
| Version | 1.30.2 (Greenfield implementation) |
| Downloaded from | `https://software.verapdf.org/releases/verapdf-installer.zip` |
| SHA-256 (this download) | `6cc6341cb1af644044054b81f00a6590a7918abb18f762243de115258bcad838` |
| Signature | GPG-verified: `gpg --verify` reports "Good signature from Carl Wilson <techlead@verapdf.org>", fingerprint `13DD 102B 4DD6 9354 D12D E5A8 3184 8632 78B1 7FE7` — matches the fingerprint published at docs.verapdf.org/install/ exactly. No SHA-256 is published upstream (GPG is the vendor's verification method, not a checksum); the SHA-256 above is recorded for future-download comparison, not as a verified-against value. |
| Installed to | `C:\Users\ysuliman\tools\verapdf\` (outside the repo, as asked) |
| Runtime dependency | Needs a JVM; none was present on this machine. Installed a portable Eclipse Temurin 21 JRE (Adoptium, checksum-verified against the Adoptium API) at `C:\Users\ysuliman\tools\jre-temurin\`, self-contained, not added to system PATH — set `JAVACMD` per-invocation instead so nothing about the machine's default Java setup changed |
| Confirmed running | `verapdf.bat --version` → `veraPDF 1.30.2`, built 2026-06-03 |

**Confirmed against a real file.** Generated a tiny PDF locally with headless
Chromium (`C:\Program Files\Google\Chrome\Application\chrome.exe --headless
--no-sandbox --disable-gpu --print-to-pdf=...`) and validated it:

```
$env:JAVACMD = "C:\Users\ysuliman\tools\jre-temurin\jdk-21.0.12.1+1-jre\bin\java.exe"
& "C:\Users\ysuliman\tools\verapdf\verapdf.bat" --flavour 4 --format text probe.pdf
```
```
FAIL C:\Users\ysuliman\tools\verapdf-test\probe.pdf 4
```
Exit code 1. **FAIL is the correct, expected result** — a Chromium `printToPDF`
output is plain RGB with no PDF/A metadata at all, so it fails PDF/A-4 (`--flavour
4`) exactly as it should. This confirms the installed binary runs, parses a real
PDF, applies a profile, and reports pass/fail correctly — it's just checking the
wrong specification family for this project's needs.

---

## 2. veraPDF's actual profile list (why `--flavour 4` is not PDF/X-4)

```
veraPDF supported PDF/A and PDF/UA profiles:
  1a - PDF/A-1a validation profile      2a/2b/2u - PDF/A-2 profiles
  3a/3b/3u - PDF/A-3 profiles           4/4f/4e  - PDF/A-4 profiles
  ua1 - PDF/UA-1                        ua2 - PDF/UA-2 + Tagged PDF
  wt1r - WTPDF 1.0 Reuse                wt1a - WTPDF 1.0 Accessibility
```
`--flavour 4` is **PDF/A-4**, not PDF/X-4 — the numbering coincidence (both
standards happen to have a "part 4") is the trap here. Confirmed by running the
Chromium probe through it: the resulting XML report's `<releaseDetails
id="validation-model">` and rule `specification` attributes read
`"ISO 19005-4:2020"` — ISO 19005 is PDF/A, not ISO 15930 (PDF/X).

---

## 3. Report format — what pass/fail actually look like

**`--format text`:** one line, `PASS`/`FAIL <path> <flavour>`. Exit code 0 on pass,
1 on fail (or on error — the two aren't distinguished by exit code alone, check
stdout).

**`--format xml`** (the default) is the detailed report. Structure, from the probe
run:
```xml
<report>
  <buildInformation>
    <releaseDetails id="core" version="1.30.2" .../>
    <releaseDetails id="validation-model" version="1.30.2" .../>
  </buildInformation>
  <jobs>
    <job>
      <validationReport profileName="..." statement="...">
        ...
        <rule specification="ISO 19005-4:2020" clause="6.1.2" testNumber="1" status="failed">
          <description>...</description>
          <object>...</object>
        </rule>
        ...
```
Each failed rule carries a `clause` (the ISO clause number), a `testNumber`, and a
`status` of `failed`/`passed`. A PASS report has the same shape with every rule's
`status="passed"` (or the rule omitted, depending on `--maxfailuresdisplayed`) and
the top-level job summary reporting `isCompliant="true"`.

Other useful flags: `--format json`/`html` for other renderings, `--list` to enumerate
profiles, `-x <feature>` to extract PDF features (fonts, ICC profiles, output
intents, etc.) independent of pass/fail — this could be a useful building block even
without PDF/X validation, since it's real structural extraction, not a guess.

---

## 4. Three most likely PDF/X-4 failure clauses for a WeasyPrint-emitted file

Sourced, not guessed — these are the clauses prepress preflight tools (Enfocus,
DUON-portal) most commonly flag on PDF/X-4 files in general, checked here against
what WeasyPrint is actually known to emit:

1. **`/Trapped` key missing or not `/True`, `/False`, or `/Unknown`.** A commonly
   cited PDF/X preflight failure — the key is required, an absent key fails the
   check even though "unset" and "/Unknown" mean almost the same thing semantically
   (Enfocus Preflight documentation, "Trapped key not true or false").
2. **A PDF/X conformance key present in the classic Document Info Dictionary
   instead of, or in addition to, XMP.** PDF/X-4 requires the conformance
   declaration ONLY in XMP metadata (`pdfxid:GTS_PDFXVersion`) — a value also
   present in the legacy Info dict (the pre-XMP PDF/X-1a/X-3 convention) is a
   flagged violation on its own (DUON-portal: "PDF/X entry in Document info present
   (must only be present in XMP metadata) [PDF/X-4]").
3. **Output-intent ICC profile validity/version issues.** ISO 15930-7 requires the
   output intent to carry a real embedded ICC profile (`/DestOutputProfile`);
   preflight tools separately flag profiles that parse but are an ICC spec version
   newer than the checking tool/RIP expects (Enfocus: "(Output Intent) ICC profile
   version is newer than (X)"). This is exactly the class of check no available
   local tool can actually run — verifying an ICC profile is real, current-spec,
   and internally consistent needs ICC parsing this project doesn't have (Python
   stdlib has none, and no free local tool that reaches this deep was found).

---

## 5. Verdict on `research/pdfx4.pdf`

**Note on filename:** the task named `research/pdfx4-sample.pdf`; the file that
actually appeared is `research/pdfx4.pdf`. Same directory, same purpose — used it.

Ran the stdlib structural-inspection script (re + zlib, same technique as
`17-print-live-tests.md` Test 2, extended with `/Trapped` and an XMP-vs-Info-dict
check) directly against it. Results:

| Check | Result |
|---|---|
| `TrimBox` | `[0 0 419.527559 595.275591]` |
| `BleedBox` / `MediaBox` | `[-8.503937 -8.503937 428.031496 603.779528]` — exactly 8.503937pt (3mm) bleed on every side, matching the earlier live-sandbox report exactly |
| `/Trapped` | `/False` — **present and correctly set.** Candidate failure #1 above does not occur on this file |
| `GTS_PDFXVersion` | `PDF/X-4`, declared via **both** `pdfxid:GTS_PDFXVersion` (modern namespace) and `pdfx:GTS_PDFXVersion` + `pdfx:GTS_PDFXConformance` (classic extension schema), all inside the XMP packet. **Scoped re-check for candidate #2:** searched the entire decompressed file specifically for the PDF-syntax legacy form (`/GTS_PDFXVersion (…)`, parenthesized string, the pre-XMP PDF/X-1a/X-3 convention) — zero matches anywhere, not just "none found outside the XMP block." Could not independently isolate and print the `/Info 12 0 R` object's own body to confirm this by direct inspection (this file's cross-reference structure doesn't expose it to a plain `N 0 obj…endobj` regex — likely a compressed object stream), but the whole-file regex already covers that object's content once decompressed, so the negative result stands. Candidate failure #2 above does not occur on this file |
| `/OutputIntents` | present, `/S /GTS_PDFX`, `/OutputConditionIdentifier` = `"IEC 61966-2-1 Default RGB Colour Space - sRGB"`, `/DestOutputProfile` present as an indirect reference to an embedded stream |
| ICC profile internal validity | **not checkable** — this is candidate failure #3, and it's exactly the thing no available local tool can verify (see §4.3) |
| DeviceRGB transparency `Group` count | `0` — the Kozea/WeasyPrint#2723 concern (`14-print-production-values.md` §1 caveat 3) does not occur, consistent with the earlier live-sandbox finding |
| Fonts | **0 font dictionaries found.** This sample has no text content at all (it's the bleed/colour-block test artifact) — font-embedding conformance simply cannot be assessed from this file, in either direction |

**Verdict: structurally consistent with every marker this project's stdlib
inspection can check, on both checked candidate failure clauses that apply to a
file with no text.** This is **not** an ISO 15930-7 conformance PASS — no tool
available in this preparation can issue one. It's the honest ceiling: everything a
regex-plus-zlib script can verify about this specific file checks out; genuine
third-party conformance validation (veraPDF doesn't cover PDF/X at all; a real
PDF/X-4 validator is commercial-only) remains unverified.

---

## 6. A bug this task found in its own tooling

An XMP-detection pattern written for this task's first inspection pass over
`pdfx4.pdf` (matching `<?xpacket begin=` followed by an assumed byte-order-mark
value, up through `<?xpacket end="w"?>`) **returned a false negative** -- it
reported "no XMP packet found" when a complete, correctly-formed XMP packet was
present, because the real file used `begin=""` (empty string) instead of the
byte-order-mark form. Found by grepping for the bare markers `xpacket`,
`x:xmpmeta`, `pdfxid` directly, which located the packet at byte offset ~6993
immediately. **The fix, applied to the script section 5's results actually came
from:** match `<?xpacket begin=` without assuming which `begin=` value a given
writer uses, and separately confirm `x:xmpmeta`/`rdf:RDF` markers rather than
requiring the exact closing-tag byte sequence.

**Checked `17-print-live-tests.md` Test 2's script specifically -- it does not have
this bug.** That script never tried to detect the `xpacket` wrapper as a unit; it
searches directly for the bare `GTS_PDFXVersion` substring, which is exactly the
robust approach this fix converges on. No cross-file fix needed -- recording the
false negative here because it's a real finding about a script this task wrote,
not because it propagated anywhere else.

---

## 7. What's now on disk

`C:\Users\ysuliman\tools\jre-temurin\` (~150MB extracted, portable Temurin 21 JRE)
and `C:\Users\ysuliman\tools\verapdf-dl\` (~35MB, the original installer zip plus
its extracted contents, no longer needed post-install) in addition to
`C:\Users\ysuliman\tools\verapdf\` (the actual install, ~50MB). All three are
outside the repo and safe to delete independently — `verapdf-dl` first (pure
install artifact), the JRE only if nothing else on this machine is later pointed at
it via `JAVACMD`.
