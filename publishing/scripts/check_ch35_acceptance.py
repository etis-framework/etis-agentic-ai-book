#!/usr/bin/env python3
"""Chapter 35 artifact-to-source checks; not a full print or production certificate."""
from pathlib import Path
import re,json,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
p=R/'manuscript/part-07-reference/ch35-contracts-schemas-and-reference-artifacts/index.md'
s=p.read_text();part=(R/'manuscript/part-07-reference/_part.md').read_text();root=R/'examples/refund-reference-system';issues=[]
def req(ok,msg):
 if not ok:issues.append(msg)
words=len(re.findall(r"\b[\w'-]+\b",s))
req(2100<=words<=2700 and json.loads((R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())['chapter_pages']['35']==10,'10-page ledger/source length')
req('STATUS: PLANNED' not in s and 'First-edition manuscript frozen; companion source aligned with edition' in (R/'book.yaml').read_text(),'chapter status')
req(not re.search(r'CAB-001|BP-001|advanced student|six[- ]lens|six perspectives',s,re.I),'internal QA/catalog vocabulary')
req(all(t in s[:3200] for t in ['Design A','Design B','Design C','CASE-204','$500','RF-1042','admission and identity (E1)','independent trusted execution (E5)']),'early first references')
req(all('C0'+str(i) in s for i in range(1,10)),'contract catalog')
req(all('Table 35.'+str(i) in s for i in range(1,5)),'four reference tables')
req('does **not** execute' in s and 'does not independently validate the current E2 ownership epoch' in s,'non-composition and epoch limits')
paths=re.findall(r'`((?:build[0-5]|security|reliability|operations|assurance)/[\w.-]+(?:/[\w.-]+)?)`',s)
req(all((root/x).is_file() for x in paths), 'companion references exist: '+str([x for x in paths if not (root/x).is_file()]))
for i in (1,2):
 name=f'F35-{i:02d}';a=R/f'assets/shared-figures/sources/{name}.svg';b=R/f'assets/shared-figures/rendered/{name}.svg';c=R/f'assets/shared-figures/rendered/{name}.png'
 try:fig=ET.parse(a).getroot();ok=fig.attrib.get('width')=='1000' and fig.attrib.get('height')=='600' and a.read_bytes()==b.read_bytes() and c.stat().st_size>15000 and name+'.png' in s
 except Exception:ok=False
 req(ok,name+' figure source/render')
for rel in ['manuscript/backmatter/appendices.md','references/source-register.md','metadata/topic-traceability.md','metadata/figure-register.md']:
 req('Chapter 35' in (R/rel).read_text(), 'traceability '+rel)
req('Chapter 36' in part and 'planned' not in part.lower(),'Part VII reader intro')
for x in issues:print('FAIL:',x)
print('Chapter 35 acceptance:', 'PASS' if not issues else 'FAIL', '; words',words,'; path references',len(paths))
sys.exit(bool(issues))
