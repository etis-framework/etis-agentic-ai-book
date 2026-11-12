#!/usr/bin/env python3
"""Ch15 deterministic semantic, budget, V9 vector, and embedded-Word fidelity gate."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
s=(root/'manuscript/part-02-architecture/ch15-durable-operational-state-and-assurance-e7-e9/index.md').read_text()
issues=[]
def test(ok,msg):
 if not ok:issues.append(msg)
count=len(re.findall(r"\b[\w'-]+\b",s));ledger=json.loads((root/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
test(count<=3000,f'source length {count}/3000')
test(ledger['chapter_pages']['15']==14,'V12 Ch15 ceiling not 14')
test((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'V12 total drift')
required=['CASE-204','$500','RF-1042','Design A','Design B','Design C','read-only','durable operational state (E7)','operational assurance (E9)','version','epoch','fencing','lease','transactional outbox','UNKNOWN','reconciliation','provider','idempotency key','not a credential','authorization','human intervention','fault-injection test','Chapter 16','RTO','RPO']
for phrase in required:test(phrase.lower() in s.lower(),f'missing contract {phrase}')
for bad in ['RF-1043` is the new','timeout proves failure','new refund after timeout','model approves payment']:
 test(bad.lower() not in s.lower(),f'unsafe assertion {bad}')
test(s.count('![Figure 15.')==3,'exactly three chapter diagrams required')
media=set();doc=root/'dist/etis-agentic-ai-book.docx'
if doc.is_file():
 with zipfile.ZipFile(doc) as z:media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
else:issues.append('integrated Word missing')
ns='{http://www.w3.org/2000/svg}'
for i in range(1,4):
 fid=f'F15-{i:02d}';src=root/f'assets/shared-figures/sources/{fid}.svg';svg=root/f'assets/shared-figures/rendered/{fid}.svg';png=root/f'assets/shared-figures/rendered/{fid}.png'
 if not all(x.is_file() for x in (src,svg,png)):
  issues.append(f'{fid} missing source/render');continue
 test(src.read_bytes()==svg.read_bytes(),f'{fid} SVG master mismatch')
 try:e=ET.fromstring(src.read_bytes());labels=[x for x in e.iter() if x.tag==ns+'text']
 except ET.ParseError as exc:issues.append(f'{fid} invalid XML: {exc}');continue
 test(e.attrib.get('width')=='5.75in',f'{fid} print width')
 test(e.attrib.get('viewBox','').startswith('0 0 1140 '),f'{fid} geometry')
 test(len(labels)>=10 and all(float(x.attrib.get('font-size','0'))>=19 for x in labels),f'{fid} too few or small labels')
 test(all(x.attrib.get('font-family','').startswith('Arial') for x in labels),f'{fid} nonstandard fonts')
 test(len([x for x in e.iter() if x.tag==ns+'rect'])>=5,f'{fid} too few nodes')
 test(len([x for x in e.iter() if x.tag==ns+'polyline'])>=4,f'{fid} too few connectors')
 test(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{fid} missing/stale PNG in Word')
print(f'Chapter 15 {count}/3000 source words; planned 14 finished pages')
if issues:
 print('FAIL: '+'; '.join(issues));sys.exit(1)
print('PASS: case, V12, V9 masters/renders, embedded Word PNG SHA256')
print('MANUAL: inspect native Word for Mac; measure final print pagination separately')
