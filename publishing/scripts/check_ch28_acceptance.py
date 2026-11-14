#!/usr/bin/env python3
"""Chapter 28 focused structure, boundaries, figures and evidence QA."""
from pathlib import Path
import re,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
chapter=(ROOT/'manuscript/part-05-reliability-security/ch28-distributed-failure-and-recoverable-effects/index.md').read_text()
part=(ROOT/'manuscript/part-05-reliability-security/_part.md').read_text()
checks={
 'chapter complete, within editorial source band':2600<=len(re.findall(r"\b[\w'-]+\b",chapter))<=3900,
 'Part V transition and complete case':all(s in part for s in ('CASE-204','$500','RF-1042','E2','E5','E7','E8','Chapter 31')),
 'CAB continuity and all six reader lenses':all(s in chapter for s in ('C01','C02','C04','C05','C06','C07','C08','C09','E1','E2','E3','E4','E5','E6','E7','E8','E9','Implementing engineer','Enterprise architect','Advanced student','Security and assurance','SRE and operations','Business owner')),
 'no inferred failure from absent provider proof':('UNKNOWN is not FAILED' in chapter and 'NOT_FOUND' in chapter and ('never mint another refund ID' in chapter or 'Never mint another refund identifier' in chapter) and ('does not consume, validate or compare' in chapter or 'does not consume, validate, or compare' in chapter)),
 'Tables and assessment':all(s in chapter for s in ('Table 28.1','Table 28.2','## 28.10','## 28.9')),
 'book status': 'Chapters 1–29 developed' in (ROOT/'book.yaml').read_text(),
 'recovery test and mapping':(ROOT/'examples/refund-reference-system/reliability/test_recovery_cases.py').exists() and 'Chapter 28 reliability evidence' in (ROOT/'examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md').read_text(),
 'source and index update':'Chapter 28 distributed recovery claims' in (ROOT/'references/source-register.md').read_text() and 'Crash-point matrix' in (ROOT/'metadata/index-term-register.json').read_text(),
}
for i in (1,2,3):
 name=f'F28-{i:02d}'
 try:
  src=ROOT/f'assets/shared-figures/sources/{name}.svg';render=ROOT/f'assets/shared-figures/rendered/{name}.svg';png=ROOT/f'assets/shared-figures/rendered/{name}.png'
  ET.parse(src)
  checks[f'{name} source/render/placement']=src.read_bytes()==render.read_bytes() and png.stat().st_size>30000 and name+'.png' in chapter
 except (OSError,ET.ParseError):checks[f'{name} source/render/placement']=False
for label,passed in checks.items():print(('PASS: ' if passed else 'FAIL: ')+label)
sys.exit(not all(checks.values()))
