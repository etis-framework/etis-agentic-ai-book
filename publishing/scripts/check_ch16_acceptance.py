#!/usr/bin/env python3
"""Chapter 16 V12, E-domain semantics, V9 SVG geometry and embedded DOCX evidence."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
r=Path(__file__).resolve().parents[2]
p=r/'manuscript/part-02-architecture/ch16-trust-boundaries-and-deployment-views/index.md'
s=p.read_text(); errors=[]
def need(cond,label):
 if not cond:errors.append(label)
w=len(re.findall(r"\b[\w'-]+\b",s));ledger=json.loads((r/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
need(w<=3000,f'Chapter16 source words {w} > 3000')
need(ledger['chapter_pages']['16']==13,'Chapter16 page allocation drift')
need((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'V12 book total drift')
for t in ['CASE-204','$500','RF-1042','Design A','Design B','Design C','Figure 8.1','Chapter 15','Part III','E1','E2','E3','E4','E5','E6','E7','E8','E9','independent','credential','idempotency key','not a security credential','UNKNOWN','reconciliation','epoch','outbox','trust boundary','negative-path','Profile L','Profile M','Profile H','cost per','split brain','no direct','operator']:
 need(t.lower() in s.lower(),f'missing contract {t}')
need(s.count('![Figure 16.')==3,'expected three illustrations')
for phrase in ['model authorizes a refund','timeout proves failure','new RF-1043','agent holds provider credential']:
 need(phrase not in s.lower(),f'unsafe statement {phrase}')
need('A, B and C continue to differ in investigation, not payment authority' in s,'Part II case closure lost')
word=r/'dist/etis-agentic-ai-book.docx'
need(word.exists(),'integrated Word missing')
media=set()
if word.exists():
 with zipfile.ZipFile(word) as z:media={hashlib.sha256(z.read(k)).hexdigest() for k in z.namelist() if k.startswith('word/media/')}
ns='{http://www.w3.org/2000/svg}'
for i in range(1,4):
 f=f'F16-{i:02d}';master=r/f'assets/shared-figures/sources/{f}.svg';render=r/f'assets/shared-figures/rendered/{f}.svg';png=r/f'assets/shared-figures/rendered/{f}.png'
 if not all(k.exists() for k in [master,render,png]):errors.append(f'{f} source/render/PNG missing');continue
 need(master.read_bytes()==render.read_bytes(),f'{f} source/render mismatch')
 try:svg=ET.fromstring(master.read_bytes())
 except ET.ParseError as e:errors.append(f'{f} invalid svg {e}');continue
 need(svg.attrib.get('width')=='5.75in',f'{f} incorrect print width')
 need(svg.attrib.get('viewBox','').startswith('0 0 1140 '),f'{f} nonstandard viewBox')
 labels=[x for x in svg.iter(ns+'text')]
 need(len(labels)>=15 and all(float(x.get('font-size','0'))>=19 for x in labels),f'{f} illegible labels')
 need(all(x.get('font-family','').startswith('Arial') for x in labels),f'{f} font drift')
 need(len(list(svg.iter(ns+'rect')))>=5,f'{f} low diagram content')
 need(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{f} PNG not embedded in Word')
for p in (r/'manuscript/part-02-architecture').glob('ch*/index.md'):
 if 8<=int(p.parent.name[2:4])<=15:
  t=p.read_text();need('CASE-204' in t and 'RF-1042' in t,f'{p.parent.name} continuity drift')
print(f'Chapter 16 acceptance: {w}/3000 words; V12 13-page allocation; {len(errors)} error(s)')
if errors:
 for e in errors:print('FAIL:',e)
 sys.exit(1)
print('PASS: boundaries, case, canonical reference architecture, V9 master/render/Word fingerprints')
print('MANUAL: Word for Mac print-size inspection and native pagination remain open')
