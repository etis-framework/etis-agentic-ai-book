#!/usr/bin/env python3
"""Chapter 22 controlled structural/semantic/figure/reference/source gates."""
import hashlib, json, re, sys, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
r=Path(__file__).resolve().parents[2]
p=r/'manuscript/part-04-implementation/ch22-build-0-deterministic-refund-baseline/index.md'
s=p.read_text();part=(r/'manuscript/part-04-implementation/_part.md').read_text();errors=[]
def check(x,msg):
 if not x: errors.append(msg)
w=len(re.findall(r"\b[\w'-]+\b",s))
check(1700 <= w <= 2700,f'Chapter 22 text: {w} words outside provisional 1700–2700 guard')
ledger=json.loads((r/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
check(ledger['chapter_pages']['22']==14 and ledger['part_pages']['IV']==85,'V12 allocation changed')
for v in ['CASE-204','$500','RF-1042','Design A','Design B','Design C','conditional initial production candidate','C01','C02','C03','C04','C05','C06','C07','C08','C09','E1','E2','E3','E4','E5','E6','E7','E8','E9','UNKNOWN','not a deployed','Figure 22.1','Figure 22.2','Gray and Reuter','Kleppmann','RFC 9110','NIST AI RMF']:
 check(v.lower() in s.lower(),f'Chapter 22 missing {v}')
for v in ['Build 0','Build 1','Build 2','Build 3','Build 4','Build 5','optional','UNKNOWN','RF-1042','does not mandate C']:
 check(v.lower() in part.lower(),f'Part IV missing {v}')
for n in ['F22-01','F22-02']:
 files=[r/f'assets/shared-figures/{folder}/{n}.{ext}' for folder,ext in [('sources','svg'),('rendered','svg'),('rendered','png')]]
 check(all(q.exists() for q in files),f'{n} source/outputs missing')
 if not all(q.exists() for q in files):continue
 check(files[0].read_bytes()==files[1].read_bytes(),f'{n} stale svg')
 try:
  tree=ET.parse(files[0]);root=tree.getroot()
  text=[x for x in root.iter() if x.tag.endswith('text')]
  check(root.attrib.get('width')=='5.75in' and root.attrib.get('viewBox')=='0 0 1140 840',f'{n} print geometry')
  check(len(text)>=12 and min(float(x.get('font-size','0')) for x in text)>=21,f'{n} effective source label size')
  check(all('Arial' in x.get('font-family','') for x in text),f'{n} font family')
 except Exception as e:errors.append(str(e))
 check(files[2].stat().st_size>15000,f'{n} suspicious PNG size')
for path,needle in [('README.md','| 22 | Build 0 |'),('references/source-register.md','## Chapter 22'),('metadata/topic-traceability.md','## Chapter 22'),('manuscript/backmatter/bibliography.md','Selected research, standards and professional sources'),('examples/refund-reference-system/README.md','## Run Build 1')]:
 check(needle in (r/path).read_text(),f'Stale integration record: {path}')
book=r/'dist/etis-agentic-ai-book.docx'
check(book.exists(),'Build whole book before Chapter 22 acceptance')
if book.exists():
 with zipfile.ZipFile(book) as z:
  hashes={hashlib.sha256(z.read(q)).hexdigest() for q in z.namelist() if q.startswith('word/media/')}
 for n in ['F22-01','F22-02']:
  check(hashlib.sha256((r/f'assets/shared-figures/rendered/{n}.png').read_bytes()).hexdigest() in hashes,f'{n} absent/stale in DOCX')
print('Chapter 22:',w,'words; V12 14-page planning ceiling; issues',len(errors))
for x in errors:print('FAIL:',x)
if errors:sys.exit(1)
print('PASS structural/semantic/figure/current Word identity/source map; OPEN native Mac Word pagination, print-image acceptance, source-page certification')
