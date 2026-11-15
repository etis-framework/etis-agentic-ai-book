#!/usr/bin/env python3
"""Chapter 33 acceptance: editorial, path, architecture and figure source integrity; not certification."""
from pathlib import Path
import re,sys,json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
ch=(R/'manuscript/part-06-governance-operations/ch33-release-engineering-and-operational-readiness/index.md').read_text()
part=(R/'manuscript/part-06-governance-operations/_part.md').read_text()
checks={}
def check(name,v): checks[name]=bool(v)
words=len(re.findall(r"\b[\w'-]+\b",ch))
check('substantive source and V12 13-page allocation',2300<=words<=3100 and json.loads((R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())['chapter_pages']['33']==13)
check('developed status and truthful forward reference','STATUS: PLANNED' not in ch and 'Chapter 35 developed' in (R/'book.yaml').read_text() and not re.search(r'Chapter (34|35|36).{0,30}(planned|not written|not drafted)',ch+part,re.I))
check('first reference and running scenario', all(t in ch[:4200] for t in ['Design A','Design B','Design C','CASE-204','RF-1042','$500','admission and identity (E1)','independently trusted execution (E5)','C04','C05','C06','C07','C08','C09']))
check('no internal manuscript identifiers / QA personas',not re.search(r'CAB-001|BP-001|advanced student|six-lens|six lenses',ch,re.I))
check('architectural negative evidence',all(t in ch for t in ['UNKNOWN','NOT_FOUND','no C07 blind retry','E5 current-owner epoch','independent E5','protected','no live deploy']))
check('release-specific engineering',all(t.casefold() in ch.casefold() for t in ['canary','policy hot reload','tool allowlist','release candidate manifest','rollback','Runbook 33-A','Table 33.1','Table 33.2','Table 33.3']))
check('runbook label defined','first *manuscript* runbook in this chapter' in ch and 'Runbooks 30-A and 32-A' in ch)
check('proposed fields versus actual implementation','not a Python class' in ch and 'not statuses emitted by the Python examples' in ch and 'not a deployment pipeline' in ch)
paths=['build3/service.py','build3/test_gate.py','security/test_adversarial_cases.py','build4/ledger.py','build4/test_provider.py','reliability/test_recovery_cases.py','build5/test_coordination.py','operations/incident.py','operations/test_incident.py','assurance/collect.py','assurance/test_collect.py']
root=R/'examples/refund-reference-system';check('11 actual implementation paths and navigation',all((root/p).is_file() and p in ch for p in paths) and all((root/(p+'/README.md')).is_file() and p+'/README.md' in ch for p in ['security','operations','reliability','assurance']))
for i in range(1,4):
 n=f'F33-{i:02d}';s=R/f'assets/shared-figures/sources/{n}.svg';v=R/f'assets/shared-figures/rendered/{n}.svg';p=R/f'assets/shared-figures/rendered/{n}.png'
 try:r=ET.parse(s).getroot();ok=r.attrib['width']=='1000' and r.attrib['height']=='600' and s.read_bytes()==v.read_bytes() and p.stat().st_size>30000 and f'{n}.png' in ch
 except (OSError,KeyError,ET.ParseError):ok=False
 check(n+' master, render and reference',ok)
check('appendices and source trace',all('Chapter 33' in (R/f).read_text() for f in ['manuscript/backmatter/appendices.md','references/source-register.md','metadata/topic-traceability.md']))
check('no implementation overclaim','not one certified deployment' in ch and 'not production certification' in ch and 'E5 does **not** independently enforce current-owner epoch' in ch)
for k,v in checks.items():print(('PASS' if v else 'FAIL')+': '+k)
print(f'Chapter 33 regex words: {words}; native Mac Word proof and external production checks remain outstanding')
sys.exit(not all(checks.values()))
