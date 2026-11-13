#!/usr/bin/env python3
"""Chapter 18 source, figure, contract, case, and optional integrated Word checks."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
s=(R/'manuscript/part-03-patterns/ch18-coordination-and-delegation-patterns/index.md').read_text()
ledger=json.loads((R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
words=len(re.findall(r"\b[\w'-]+\b",s))
check(words<=3000,f'chapter exceeds word cap: {words}/3000')
check(ledger['chapter_pages']['18']==12,'V12 chapter 18 allocation changed')
check((ledger['chapter_total_pages'],ledger['front_back_reserve_pages'],ledger['target_finished_pages'])==(485,65,550),'V12 total changed')
for t in ['CASE-204','$500','RF-1042','Design A','Design B','Design C','conditional','read-only','E1','E2','E3','E4','E5','E6','E7','E8','E9','C01','C02','C04','C05','C06','UNKNOWN','epoch','lease','fencing','registry','peer','supervisor','specialist','human stop','Chapter 19','cost per acceptable completed workflow','Kleppmann (2017)']:
 check(t.lower() in s.lower(),f'missing architectural/case marker: {t}')
check('RF-1043' in s and 'blind retry' in s.lower(),'missing negative provider outcome')
check('Figure 18.1' in s and 'Figure 18.2' in s,'missing named figure references')
check('Chapter 18' in (R/'references/source-register.md').read_text(),'source register mapping missing')
check('Chapters 1–22' in (R/'manuscript/backmatter/bibliography.md').read_text(),'bibliography coverage not updated to current manuscript')
media=set();doc=R/'dist/etis-agentic-ai-book.docx'
if doc.exists():
 with zipfile.ZipFile(doc) as z:media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
else:errors.append('integrated DOCX missing: run make book-docx before acceptance')
ns='{http://www.w3.org/2000/svg}'
for n in ('F18-01','F18-02'):
 master=R/f'assets/shared-figures/sources/{n}.svg';render=R/f'assets/shared-figures/rendered/{n}.svg';png=R/f'assets/shared-figures/rendered/{n}.png'
 if not all(x.exists() for x in (master,render,png)):
  errors.append(f'{n}: missing source/render');continue
 check(master.read_bytes()==render.read_bytes(),f'{n}: source/render mismatch')
 try:docsvg=ET.parse(master).getroot()
 except ET.ParseError as ex:errors.append(f'{n}: invalid svg: {ex}');continue
 check(docsvg.get('width')=='5.75in' and docsvg.get('viewBox','').startswith('0 0 1140 '),f'{n}: print dimensions incorrect')
 labels=list(docsvg.iter(ns+'text'))
 check(len(labels)>=15 and all(float(e.get('font-size','0'))>=19 and e.get('font-family','').startswith('Arial') for e in labels),f'{n}: labels/size/font fail')
 check(len(list(docsvg.iter(ns+'rect')))>=5,f'{n}: insufficient diagram structure')
 check(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{n}: PNG not embedded in integrated Word')
print(f'Chapter 18: {words}/3000 words; allocation 12 pages; {len(errors)} failure(s)')
for e in errors:print('FAIL:',e)
if errors:sys.exit(1)
print('PASS: structure, case, contracts, source scope, 7x10 figures, and current integrated Word fingerprints')
print('OPEN: native Mac Word pagination, visual print-size review, editorial six-lens signoff and source-page verification')
