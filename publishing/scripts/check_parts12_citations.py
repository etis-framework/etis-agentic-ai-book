#!/usr/bin/env python3
"""Targeted, executable citation-presence and scope guard for Parts I-II.

This does not certify full passage-level bibliographic support or native Word print layout.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
BIB = (ROOT / 'references/bibliography.bib').read_text()
BACK = (ROOT / 'manuscript/backmatter/bibliography.md').read_text()
REGISTER = (ROOT / 'references/source-register.md').read_text()
issues = []

REQUIRED = {
    8: {'8.2': ['Bass, Clements, and Kazman, 2021'], '8.4': ['Hohpe and Woolf, 2003']},
    9: {'9.2': ['Rose et al., 2020']},
    10: {'10.4': ['Lamport (1978)', 'Kleppmann (2017)']},
    11: {'11.2': ['Yao et al., 2023', 'Schick et al., 2023']},
    12: {'12.4': ['Lewis et al. (2020)']},
    13: {'13.2': ['Rose et al. (2020)']},
    14: {'14.2': ['Hohpe and Woolf (2003)'], '14.3': ['RFC 9110', '§9.2.2']},
    15: {'15.3': ['Gray and Reuter, 1992', 'Hohpe and Woolf, 2003'], '15.6': ['Beyer et al., 2016']},
    16: {'16.3': ['Rose et al., 2020']},
}
for n, sections in REQUIRED.items():
    matches=list(ROOT.glob(f'manuscript/part-02-architecture/ch{n:02d}-*/index.md'))
    if len(matches) != 1:
        issues.append(f'Chapter {n} manuscript not unique')
        continue
    text=matches[0].read_text()
    for section, needles in sections.items():
        if section == 'Sources and further reading':
            zone=text[text.find('**Sources and further reading'):]
        else:
            pat=rf'(?m)^## {re.escape(section)}\b.*$'
            m=re.search(pat,text)
            if not m:
                issues.append(f'Chapter {n} section {section} absent')
                continue
            later=re.search(r'(?m)^## ',text[m.end():])
            zone=text[m.end():m.end()+later.start()] if later else text[m.end():]
        for needle in needles:
            if needle not in zone:
                issues.append(f'Chapter {n} section {section} missing local citation: {needle}')
    if f'Ch{n} ' not in REGISTER:
        issues.append(f'Chapter {n} has no register mapping')

for key, snippet in {'nist_sp800_207_2020':'10.6028/NIST.SP.800-207','rfc9110_2022':'10.17487/RFC9110'}.items():
    if not re.search(r'@\w+\{' + key + r',',BIB):
        issues.append(f'BibTeX missing {key}')
    if snippet not in BIB or snippet not in BACK:
        issues.append(f'Bibliography missing identifier {snippet}')
    if f'`{key}`' not in REGISTER:
        issues.append(f'Source register missing {key}')

for source in ['RFC 9110 §9.2.2', 'does **not** establish payment-provider', 'original ETIS synthesis']:
    if source not in ''.join(p.read_text() for p in ROOT.glob('manuscript/part-02-architecture/ch*/index.md')):
        issues.append(f'Missing scope protection: {source}')

for n in range(1,8):
    if not list(ROOT.glob(f'manuscript/part-01-foundations/ch{n:02d}-*/index.md')):
        issues.append(f'Chapter {n} missing')

if issues:
    print('Parts I-II citation preflight FAIL:')
    for issue in issues: print(' -', issue)
    raise SystemExit(1)
print('Parts I-II citation preflight PASS: nine chapter mappings, local scope citations, two new bibliographic records')
print('MANUAL OPEN: exact source-page support, licensed standards, latest versions, final native Word pagination')
