#!/usr/bin/env python3
"""Chapter 36 integrated capstone acceptance; no production or print certification."""
from pathlib import Path
import sys,re,json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
p=next((R/'manuscript/part-07-reference').glob('ch36-*/index.md'));s=p.read_text();errors=[]
def need(t,msg):
 if not t:errors.append(msg)
word_count=len(re.findall(r"\b[\w'-]+\b",s))
need(2000<=word_count<=2900,'capstone chapter length outside expected concise range')
need('STATUS: PLANNED' not in s,'placeholder remains')
need(all(t in s[:2900] for t in ('Design A','Design B','Design C','CASE-204','$500','RF-1042','independent trusted execution (E5)')),'first-use orientation')
need(all(f'36.{i}' in s for i in range(1,9)),'section sequence')
need(all(f'Table 36.{i}' in s for i in range(1,4)),'capstone tables')
need(all(f'F36-{i:02d}.png' in s for i in range(1,3)),'capstone figures')
need(not re.search(r'CAB-001|BP-001|advanced student|six[- ]lens|six perspectives|production.certified',s,re.I),'internal terms or certification implication')
need('does not independently validate the current E2 ownership epoch inside E5' in s,'E5 epoch limit missing')
need('do **not** demonstrate independent production key custody' in s,'compromised-token limit missing')
need('No companion build contains measured enterprise return on investment' in s,'economics boundary missing')
root=R/'examples/refund-reference-system'
for path in ('README.md','IMPLEMENTATION_EVIDENCE_MAP.md','build1/README.md','build3/README.md','build4/README.md','build5/README.md','security/README.md','reliability/README.md','operations/README.md','assurance/README.md'):
 need((root/path).exists() and path in s,'missing companion path: '+path)
for i in (1,2):
 n=f'F36-{i:02d}'
 a=R/f'assets/shared-figures/sources/{n}.svg';b=R/f'assets/shared-figures/rendered/{n}.svg';c=R/f'assets/shared-figures/rendered/{n}.png'
 try:need(ET.parse(a).getroot().attrib.get('width')=='1000' and a.read_bytes()==b.read_bytes() and c.stat().st_size>15000,n+' source/render mismatch')
 except Exception:errors.append(n+' missing or malformed')
need(json.loads((R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())['chapter_pages']['36']==9,'V12 9-page allocation')
for rel in ('manuscript/backmatter/appendices.md','metadata/topic-traceability.md','references/source-register.md','metadata/figure-register.md'):
 need('Chapter 36' in (R/rel).read_text(),rel+' missing integration')
need('Chapter 36 placeholder' not in (R/'book.yaml').read_text(),'book status stale')
for e in errors:print('FAIL:',e)
print('Chapter 36 acceptance', 'PASS' if not errors else 'FAIL', f'{word_count} words;',len(errors),'findings')
sys.exit(bool(errors))
