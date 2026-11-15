#!/usr/bin/env python3
"""Chapter 34 bounded acceptance check: content, arithmetic, layout inputs, path scope; not certification."""
from pathlib import Path
import re,json,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
p=R/'manuscript/part-06-governance-operations/ch34-economics-risk-and-lifecycle-decisions/index.md';ch=p.read_text();checks={}
def check(label,ok):checks[label]=bool(ok)
words=len(re.findall(r"\b[\w'-]+\b",ch))
check('V12 12-page allocation and substantive length',2400<=words<=3000 and json.loads((R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())['chapter_pages']['34']==12)
check('developed manuscript and Part VI closing','STATUS: PLANNED' not in ch and 'Chapter 35 developed' in (R/'book.yaml').read_text() and 'Part VI conclusion' in ch)
check('first references and CASE-204',all(t in ch[:4200] for t in ['CASE-204','$500','RF-1042','Design A','Design B','Design C','admission and identity (E1)','independent trusted execution (E5)','C04','C05','C06','C07','C08','C09']))
check('no internal review vocabulary or catalog IDs',not re.search(r'CAB-001|BP-001|advanced student|six-lens|six lenses',ch,re.I))
check('economics unique to agentic systems',all(t in ch for t in ['cost per **acceptable completed workflow**','incremental cost','acceptable completions','human review','E5','UNKNOWN']))
check('illustrative costs internally consistent',(99000-84000)/(9000-8400)==25 and (123525-99000)/(9150-9000)==163.5 and '$25' in ch and '$163.50' in ch)
check('published economics explicitly not measured',all(t in ch for t in ['hypothetical assumptions','not observed results','no executable cost model','not Python fields','cannot establish production']))
check('risk is not authority',all(t in ch for t in ['valid E1 token','cannot be treated as a retryable inference','Hard gate','independent E5','current-owner-epoch']))
root=R/'examples/refund-reference-system';paths=['build3/service.py','build3/test_gate.py','security/test_adversarial_cases.py','build4/ledger.py','build4/test_provider.py','reliability/test_recovery_cases.py','build5/test_coordination.py','operations/incident.py','operations/test_incident.py','assurance/collect.py','assurance/test_collect.py'];check('all companion paths exist and are named',all((root/a).is_file() and a in ch for a in paths))
for i in range(1,4):
 n=f'F34-{i:02d}';a=R/f'assets/shared-figures/sources/{n}.svg';b=R/f'assets/shared-figures/rendered/{n}.svg';c=R/f'assets/shared-figures/rendered/{n}.png'
 try:rootxml=ET.parse(a).getroot();ok=rootxml.attrib.get('width')=='1000' and rootxml.attrib.get('height')=='600' and a.read_bytes()==b.read_bytes() and c.stat().st_size>30000 and n+'.png' in ch
 except Exception:ok=False
 check('figure '+n,ok)
check('appendix, source and figure trace',all('Chapter 34' in (R/rel).read_text() for rel in ['references/source-register.md','metadata/topic-traceability.md','manuscript/backmatter/appendices.md','metadata/figure-register.md']))
check('Part VII completed with development evidence','STATUS: PLANNED / NOT DRAFTED' not in (R/'manuscript/part-07-reference/ch36-exercises-reviews-and-adoption-roadmap/index.md').read_text() and 'Chapter 36 developed' in (R/'book.yaml').read_text())
for key,val in checks.items():print(('PASS' if val else 'FAIL')+': '+key)
print('Chapter 34 source words:',words,'; actual integrated Word/Mac pagination and production controls are independent gates')
sys.exit(not all(checks.values()))
