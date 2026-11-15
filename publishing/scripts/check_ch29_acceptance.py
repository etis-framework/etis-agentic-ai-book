#!/usr/bin/env python3
"""Chapter 29 source and adversarial-evidence preflight.

Checks can reject incomplete artifacts; they cannot prove OS isolation or
replace 7x10 print review, six-lens reading, or external citation verification.
"""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[2]
chapter = (R / 'manuscript/part-05-reliability-security/ch29-security-and-adversarial-agent-behavior/index.md').read_text()
companion = R / 'examples/refund-reference-system/security'
qa = (companion / 'test_adversarial_cases.py').read_text()
readme = (companion / 'README.md').read_text()
checks = {
    'Complete chapter under V12 source band': 2400 <= len(re.findall(r"\b[\w'-]+\b", chapter)) <= 3500,
    'Source status updated': bool(re.search(r'Chapters 1–(?:29|3[0-6]) developed', (R / 'book.yaml').read_text())),
    'Core case, approval and epoch gaps': all(x in chapter for x in ('CASE-204', '$500', 'RF-1042', 'valid E1', 'finance grant', 'E5', 'Build 5', 'epoch')),
    'CAB contracts and responsibilities': all(x in chapter for x in ('C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9')),
    'Credential custody and delegation chapter coverage': all(x in chapter for x in ('Workload identity, credential custody, and delegated authority', 'Table 29.3', 'Table 29.4', 'confused-deputy', 'wrong-audience', 'read-only C08', 'revocation', 'key rotation', 'not implement')),
    'Decision, attack and limitations tables': all(x in chapter for x in ('Table 29.1','Table 29.2','Table 29.3','## 29.9','Multi-perspective architecture review')),
    'Same-UID and fixture scope explicit': all(x in chapter for x in ('same-UID','not implemented','production','DENIED','no E7','no E8')),
    'Six executable tests': len(re.findall(r'^    def test_', qa, re.M)) >= 6 and all(x in qa for x in ('test_valid_identity_without_finance_grant_denied_without_effect','test_authorized_positive_control_uses_same_gate','test_forged_advisory_fields_denied','test_valid_token_cannot_be_repurposed_as_finance_grant')),
    'Real subprocess, client, no local effect assertion': all(x in qa for x in ('subprocess.Popen','build3','from client import request','assert_no_financial_side_effect','operations.sqlite3','provider.sqlite3')),
    'Reader README architecture and caveat': all(x in readme for x in ('![Actual source/module test architecture](architecture.svg)', 'same-UID', 'not', 'Build 6')),
    'Reader handoff updated': 'Chapter 29 implemented adversarial harness' in (R / 'examples/refund-reference-system/ASSURANCE_HANDOFF_CH28_CH31.md').read_text(),
    'Source and backmatter updated': 'Chapter 29 — security' in (R / 'references/source-register.md').read_text() and 'Security falsifier' in (R / 'manuscript/backmatter/glossary.md').read_text(),
}
for n in range(1, 4):
    stem = f'F29-{n:02d}'
    source = R / f'assets/shared-figures/sources/{stem}.svg'
    rendered = R / f'assets/shared-figures/rendered/{stem}.svg'
    png = R / f'assets/shared-figures/rendered/{stem}.png'
    try:
        rt = ET.parse(source).getroot()
        w = float(rt.get('width',0));h = float(rt.get('height',0))
        anchors = [x for x in rt.iter() if x.tag.endswith('text')]
        geom = 800 <= w <= 1100 and 500 <= h <= 650 and len(anchors) >= 12
        geom &= all(0 < float(t.get('x',0)) < w and 0 < float(t.get('y',0)) < h for t in anchors)
        checks[stem + ' render/placement/anchor bounds'] = geom and source.read_bytes() == rendered.read_bytes() and png.stat().st_size > 30000 and stem+'.png' in chapter
    except (OSError,ValueError,ET.ParseError):
        checks[stem + ' render/placement/anchor bounds'] = False
for label, passed in checks.items():print(('PASS: ' if passed else 'FAIL: ')+label)
print('NOTE: Visual print QA, attack-model limits and real secret custody require independent review.')
sys.exit(not all(checks.values()))
