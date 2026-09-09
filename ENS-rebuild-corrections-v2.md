# Remaining corrections for ENS-plugin-rebuild-v2.md — three items, then build

Verified 2026-09-07 against the plugin source (research/08-verify-v2.md).
Tier 1 items 1.2, 1.4, 1.6 are APPLIED. Three remain. Your three design decisions
(brown = secondary category marker; underline fields; portrait social default) are
final — include them.

======================================================================
## R1  The new description is too long — it would be rejected or cut off
======================================================================
The ENS prefix (~480 chars) is PREPENDED to each skill's original description.
For ui-ux-pro-max the original is already ~1,050 chars, so the result is ~1,530.
The platform limit is 1,024 characters. Over that, the upload is rejected or the
text is truncated — and if truncated, the ENS triggers at the END are what's lost.
A stricter 200-char cap in the upload UI is also reported by one source and is
unconfirmed either way.

FIX:
  1. REPLACE each skill's description, do not prepend to it. Write one new
     description per skill, under 1,000 characters total.
  2. Put the essential triggers in the FIRST 200 characters — org name, "note
     interne", "formulaire", "fiche", "présentation", "post" — so that even a
     200-char cut keeps them.
  3. Print the final character count for each of the 7 skills in the rebuild
     report. Numbers, not "checked".

======================================================================
## R2  styles.csv still uses columns that do not exist
======================================================================
"Style ID", "Aliases", "Parent Style ID", "Status" are not in styles.csv. The real
header has 22 columns and none of these are among them; the plugin's code never
references them anywhere. v2 states they "DO exist... v1 used them correctly" —
that is incorrect.

Harmless at runtime (the style search ignores unknown columns), but:
FIX: remove the four invented columns from the styles.csv row, and remove the
claim that they were confirmed. Put the style name in "Style Category" and the
alias words in "Keywords" / "AI Prompt Keywords", which do exist.

======================================================================
## R3  The [NO ENS MATCH] wrapper only prints — it must fail
======================================================================
v2 says the wrapper "prints" the marker. A printed line that nothing checks is
the same ignorable instruction as before, just louder.

FIX: show the actual script, and make it exit non-zero. Minimum shape:

    #!/usr/bin/env bash
    # ens-search.sh — run search.py and refuse a non-ENS result
    out="$(python3 search.py "$@")"
    echo "$out"
    if ! grep -q "ENS - Eng nei Schaff" <<<"$out"; then
      echo "[NO ENS MATCH] query did not resolve to ENS — fix the query" >&2
      exit 1
    fi

Then change trigger-block Step 3 from "if the marker appears, fix the query" to:
"run ens-search.sh; if it exits non-zero, do not proceed — fix the query and rerun."

======================================================================
## One more thing, for the rebuild report
======================================================================
v2 stated that a "fixed built-in set" of Decision_Rules conditions is evaluated,
citing design_system.py:385. That line is unrelated text-wrapping code. A full
search of the plugin finds NOTHING that reads Decision_Rules back — it is written
into rows and never evaluated. The original finding stands. The fix applied in
1.2 was right; the stated reason for it was not.

This and R2 are both cases of reporting something as "confirmed" that was not.
In the rebuild report, please mark each claim as VERIFIED (with the file:line
read) or ASSUMED. Do not mark anything confirmed that was not directly checked.
