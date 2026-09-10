#!/usr/bin/env python3
"""Reproduces every measured claim in Candidate L (research/38-description-
candidate.md). Reads the live description out of SKILL.md, builds the L
package by moving the existing H sentence to the front of a temporary copy
of the skill tree, and runs scripts/tests/test_description_coverage.py
against it three ways: unpatched (fails), with a naive marker rename
(still fails), and with the two-marker fix Candidate L proposes (passes).
Never writes to SKILL.md or the real test file.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "skill" / "document-design-intelligence"
SKILL_MD = SRC / "SKILL.md"

H_SENTENCE = (
    "Creating any document type above is still this skill's job even as Word "
    "or PowerPoint; defer to that format's own skill only when the user "
    "names it for a plain conversion or edit with no design ask."
)


def live_description():
    text = SKILL_MD.read_text(encoding="utf-8")
    m = re.search(r'description: "(.*)"\n', text)
    return m.group(1)


def build_candidate_l(desc):
    assert desc.count(H_SENTENCE) == 1, "H sentence not found verbatim; live description changed"
    rest = desc.replace(H_SENTENCE + " ", "", 1)
    moved = H_SENTENCE.replace("above", "below")
    return moved + " " + rest


def run(desc, live_desc, patch_marker=None, label=""):
    with tempfile.TemporaryDirectory() as tmp:
        dst = Path(tmp) / "document-design-intelligence"
        shutil.copytree(SRC, dst)
        skill_md = dst / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8").replace(live_desc, desc), encoding="utf-8"
        )
        test_file = dst / "scripts" / "tests" / "test_description_coverage.py"
        if patch_marker:
            test_file.write_text(patch_marker(test_file.read_text(encoding="utf-8")), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", str(test_file)],
            cwd=str(dst), capture_output=True, text=True,
        )
        print(f"--- {label} ---")
        print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(no output)")
        return r.returncode == 0


def naive_rename(text):
    old = 'NEGATIVE_SCOPE_MARKER = "Creating any document type above"'
    new = 'NEGATIVE_SCOPE_MARKER = "Creating any document type below"'
    assert old in text
    return text.replace(old, new)


def two_marker_fix(text, moved_sentence):
    old_line = 'NEGATIVE_SCOPE_MARKER = "Creating any document type above"'
    new_lines = (
        'NEGATIVE_HEAD_MARKER = %r\n'
        'NEGATIVE_SCOPE_MARKER = "Not for web or app UI/UX design"'
    ) % moved_sentence
    text = text.replace(old_line, new_lines)
    old_ctor = (
        "    def __init__(self, raw):\n"
        "        cut = raw.find(NEGATIVE_SCOPE_MARKER)\n"
        "        if cut < 0:\n"
    )
    new_ctor = (
        "    def __init__(self, raw):\n"
        "        head_cut = raw.find(NEGATIVE_HEAD_MARKER)\n"
        "        if head_cut < 0:\n"
        "            raise AssertionError('NEGATIVE_HEAD_MARKER not found')\n"
        "        head_start = head_cut + len(NEGATIVE_HEAD_MARKER)\n"
        "        cut = raw.find(NEGATIVE_SCOPE_MARKER, head_start)\n"
        "        if cut < 0:\n"
    )
    text = text.replace(old_ctor, new_ctor)
    return text.replace("self.positive = raw[:cut]", "self.positive = raw[head_start:cut]")


if __name__ == "__main__":
    desc = live_description()
    print("live description:", len(desc), "chars,", len(desc.encode("utf-8")), "bytes")
    candidate_l = build_candidate_l(desc)
    assert len(candidate_l) == len(desc), "reorder must not change length"
    print("candidate L:", len(candidate_l), "chars,", len(candidate_l.encode("utf-8")), "bytes")
    for token in ["lettre", "sourced", "UI/UX Pro Max", "Word or PowerPoint",
                  "only when the user names it for a plain conversion or edit with no design ask"]:
        assert candidate_l.count(token) == 1, token

    ok1 = run(desc, desc, None, "baseline, unpatched test")
    ok2 = run(candidate_l, desc, None, "candidate L, unpatched test (expected: fails loudly)")
    ok3 = run(candidate_l, desc, naive_rename, "candidate L, marker renamed only (expected: still fails)")
    moved = H_SENTENCE.replace("above", "below")
    ok4 = run(candidate_l, desc, lambda t: two_marker_fix(t, moved),
              "candidate L, two-marker fix applied (expected: passes)")
    assert ok1 and not ok2 and not ok3 and ok4, "verification did not match the claims in the brief"
    print("\nAll claims reproduced.")
