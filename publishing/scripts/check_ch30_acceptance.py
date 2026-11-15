#!/usr/bin/env python3
"""Chapter 30 source/code/evidence preflight; cannot certify live provider or printed book."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
ch=(R/'manuscript/part-05-reliability-security/ch30-reliability-observability-and-incident-response/index.md').read_text()
ops=R/'examples/refund-reference-system/operations'
source=(ops/'incident.py').read_text(); tests=(ops/'test_incident.py').read_text();readme=(ops/'README.md').read_text()
w=len(re.findall(r"\b[\w'-]+\b",ch))
checks={
 'Chapter 30 substantive V12 word cap': 2500 <=w<=3500,
 'Chapter 30 correct case, CAB, authority': all(k in ch for k in ('CASE-204','$500','RF-1042','E5','E7','E8','E9','C01','C02','C03','C04','C05','C06','C07','C08','C09','Design A','Design B','Design C')),
 'Operational SLO, runbook, roles, negative limits': all(k in ch for k in ('Table 30.1','Table 30.2','Table 30.3','Runbook 30-A','SEV1','SEV2','SEV3','UNKNOWN','NOT_FOUND','Chapter 31','not','close')),
 'E5 epoch and real provider limits remain open': 'E5 does not verify that epoch' in ch and 'protected immutable audit' in ch,
 'Chapter 30 source and test runner checked in': 'def assess(' in source and 'def test_' in tests and 'test_lost_ack_unknown' in tests,
 'Read-only observer SQL and output allowlist': all(k in source for k in ('?mode=ro','PRAGMA query_only=ON','as_record','READ_ONLY_RECONCILE_OR_ESCALATE','expected_epoch')) and not any(x in source for x in ('from adapter import','from workflow import','from client import','provider.send(','.executescript(')),
 'Reader educational docs and diagram': '![Chapter 30 source/module architecture and read-only trust boundary](architecture.svg)' in readme and 'not Build 6' in readme and 'Build 4' in readme and 'Build 5' in readme,
 'Handoff and evidence register': all('Chapter 30' in (R/p).read_text() for p in ('examples/refund-reference-system/ASSURANCE_HANDOFF_CH28_CH31.md','examples/refund-reference-system/IMPLEMENTATION_EVIDENCE_MAP.md','references/source-register.md','metadata/topic-traceability.md')),
 'Book status and navigation': 'Chapters 1–34 developed' in (R/'book.yaml').read_text() and 'Incident response and quarantine' in (R/'manuscript/backmatter/index.md').read_text(),
}
for i in (1,2,3):
 stem=f'F30-{i:02d}'
 try:
  a=R/f'assets/shared-figures/sources/{stem}.svg'
  b=R/f'assets/shared-figures/rendered/{stem}.svg'
  p=R/f'assets/shared-figures/rendered/{stem}.png'
  root=ET.parse(a).getroot()
  texts=[t for t in root.iter() if t.tag.endswith('text')]
  checks[f'{stem} source/PNG/build references']= (a.read_bytes()==b.read_bytes() and
      p.stat().st_size>30_000 and stem+'.png' in ch and
      int(root.attrib['width'])==1000 and int(root.attrib['height'])==600 and len(texts)>=10)
 except (ValueError,ET.ParseError,OSError):checks[f'{stem} source/PNG/build references']=False
try:ET.parse(ops/'architecture.svg');checks['Operations module diagram is parseable']=True
except (ET.ParseError,OSError):checks['Operations module diagram is parseable']=False
for k,v in checks.items():print(('PASS' if v else 'FAIL')+': '+k)
print('Chapter 30 words:',w,'; native Word print inspection and real-provider assurance are external gates')
sys.exit(not all(checks.values()))
