#!/usr/bin/env python3
"""Chapter 14 acceptance: semantic invariants, V12, V9 masters/renders, embedded figure identity."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
s=(root/'manuscript/part-02-architecture/ch14-enterprise-integration-and-business-truth-e6-e8/index.md').read_text()
errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
words=len(re.findall(r"\b[\w'-]+\b",s)); ledger=json.loads((root/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
check(words<=3000,f'Chapter 14 source cap exceeded: {words}/3000')
check(ledger['chapter_pages']['14']==14,'Chapter 14 V12 ceiling changed')
check((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'V12 totals changed')
for t in ['CASE-204','$500','RF-1042','Design A','Design B','Design C','read-only','enterprise integration (E6)','authoritative business systems (E8)','trusted execution and authority (E5)','durable operational state (E7)','idempotency key','not a secret','UNKNOWN','reconciliation','webhook','eventual consistency','provider operation ID','Chapter 15','source','version','authorization','credential']:
 check(t.lower() in s.lower(),f'Missing contract concept: {t}')
for bad in ['RF-1043','Design C executes','timeout means failed','a token authorizes','a webhook proves completion','200 proves completion']:
 check(bad.lower() not in s.lower(),f'Unsafe wording: {bad}')
check(s.count('![Figure 14.')==3,'Expected exactly three independent learning-objective diagrams')
media=set();doc=root/'dist/etis-agentic-ai-book.docx'
if doc.exists():
 with zipfile.ZipFile(doc) as z: media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
else:errors.append('Integrated DOCX missing; run make book-docx')
ns='{http://www.w3.org/2000/svg}'
for i in range(1,4):
 fid=f'F14-{i:02d}';src=root/f'assets/shared-figures/sources/{fid}.svg';svg=root/f'assets/shared-figures/rendered/{fid}.svg';png=root/f'assets/shared-figures/rendered/{fid}.png'
 if not all(p.is_file() for p in (src,svg,png)):
  errors.append(f'Missing figure master/render: {fid}');continue
 check(src.read_bytes()==svg.read_bytes(),f'{fid} SVG source/render mismatch')
 try: e=ET.fromstring(src.read_bytes());texts=[x for x in e.iter() if x.tag==ns+'text']
 except ET.ParseError as ex:errors.append(f'{fid} broken SVG: {ex}');continue
 check(e.attrib.get('width')=='5.75in',f'{fid} wrong print width')
 check(e.attrib.get('viewBox','').startswith('0 0 1140 '),f'{fid} wrong viewBox')
 check(len(texts)>=10 and all(float(x.attrib.get('font-size','0'))>=19 for x in texts),f'{fid} label size below 19px or too few labels')
 check(all(x.attrib.get('font-family','').startswith('Arial') for x in texts),f'{fid} font nonstandard')
 check(len([x for x in e.iter() if x.tag==ns+'rect'])>=5,f'{fid} inadequate nodes')
 check(len([x for x in e.iter() if x.tag==ns+'line'])>=4,f'{fid} inadequate connectors')
 check(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{fid} PNG missing/stale in integrated Word')
print(f'Chapter 14 source words: {words}/3000; planned ceiling: 14 finished pages')
if errors:print('FAIL:\n'+'\n'.join('- '+x for x in errors));sys.exit(1)
print('PASS: source semantic checks, V12 invariants, V9 master/render checks, embedded Word fingerprints')
print('MANUAL: Mac native Word print pagination and editorial signoff still required')
