#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Measure and test candidate I's packages without touching SKILL.md.

Reads the live description out of SKILL.md, builds each candidate-I package by
string substitution, prints measured length/bytes/headroom, then runs
scripts/tests/test_description_coverage.py against a temporary copy of the
skill tree with that description patched in. SKILL.md itself is never written.

Run from the repo root:  python3 research/38-verify-candidate-i.py
"""
import re, io, shutil, os, subprocess, tempfile, sys

SRC = 'skill/document-design-intelligence/SKILL.md'
BASE = 'skill/document-design-intelligence'
CAP = 1023

LIVE = re.search(r'^description:\s*"(.*)"\s*$',
                 io.open(SRC, encoding='utf-8').read(), re.M).group(1)

# I-min has since been applied: 'lettre' is now in the live description. Every
# package below was built by inserting it into the 964-character F+G+H string,
# so re-running against the current SKILL.md would insert a second copy and
# print numbers that mean nothing. Refuse rather than mislead.
if 'lettre' in LIVE:
    raise SystemExit(
        'I-min has landed: the live description already contains "lettre" '
        '(%d characters). This script measures candidate I against the '
        '964-character F+G+H description and is spent. Keep it as the record '
        'of how those numbers were produced; do not re-run it.' % len(LIVE))

A_OLD = 'Applies sourced layout, typography, color, print, and ATS rules.'
B_OLD = 'Not for web or app UI/UX design (use UI/UX Pro Max for screens).'
A_TIGHT = 'Applies sourced layout, typography, color, print, ATS rules.'
A_LEAN = 'Applies layout, typography, color, print, ATS rules.'
B_TIGHT = 'Not for web or app UI/UX design; use UI/UX Pro Max.'

NOUN = ', lettre'
FOUR = (', draft an invoice, write a memo, r\u00e9dige une facture, '
        'erstelle eine Rechnung')
THREE = ', r\u00e9dige une lettre, write a memo, r\u00e9dige un rapport'


def build(noun_ins, trig_ins, a=A_TIGHT, b=B_TIGHT, drop_monday=False):
    s = LIVE
    assert s.count('courrier,') == 1, 'noun anchor is not unique'
    assert s.count('erstelle ein Angebot;') == 1, 'trigger anchor is not unique'
    assert s.count(A_OLD) == 1 and s.count(B_OLD) == 1, 'tail anchors moved'
    if noun_ins:
        s = s.replace('courrier,', 'courrier' + noun_ins + ',', 1)
    if trig_ins:
        s = s.replace('erstelle ein Angebot;',
                      'erstelle ein Angebot' + trig_ins + ';', 1)
    s = s.replace(A_OLD, a, 1).replace(B_OLD, b, 1)
    if drop_monday:
        s = s.replace('I need slides for Monday', 'I need slides', 1)
    return s


PACKAGES = [
    ('I-min   lettre only, no tightening', build(NOUN, '', A_OLD, B_OLD)),
    ('I-full  four phrases, A+B tight only', build(NOUN, FOUR)),
    ('I-full  four phrases, A lean + B tight + no Monday',
     build(NOUN, FOUR, A_LEAN, B_TIGHT, True)),
    ('I-alt   three CSV-verbatim phrases, A+B tight', build(NOUN, THREE)),
]


def run_coverage_test(desc):
    tmp = tempfile.mkdtemp()
    try:
        dst = os.path.join(tmp, 'ddi')
        shutil.copytree(BASE, dst,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        path = os.path.join(dst, 'SKILL.md')
        lines = io.open(path, encoding='utf-8').read().split('\n')
        for i, line in enumerate(lines):
            if line.startswith('description: "'):
                lines[i] = 'description: "' + desc + '"'
                break
        io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
        proc = subprocess.run(
            [sys.executable, '-m', 'pytest',
             os.path.join(dst, 'scripts', 'tests', 'test_description_coverage.py'),
             '-q'], capture_output=True, text=True)
        out = (proc.stdout or proc.stderr).strip().splitlines()
        return out[-1] if out else '(no output)'
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    print('live description: %d chars, %d bytes, headroom %d\n'
          % (len(LIVE), len(LIVE.encode('utf-8')), CAP - len(LIVE)))
    for name, desc in PACKAGES:
        print('%-52s %4d chars %4d bytes headroom %4d'
              % (name, len(desc), len(desc.encode('utf-8')), CAP - len(desc)))
    print()
    for name, desc in PACKAGES:
        print('%-52s -> %s' % (name, run_coverage_test(desc)))
