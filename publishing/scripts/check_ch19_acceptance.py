#!/usr/bin/env python3
"""Chapter 19 source, architecture, citation and current embedded figure acceptance.
Non-automatable controls remain expressly open; cannot certify editorial comprehension or print pagination.
"""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
src=R/'manuscript/part-03-patterns/ch19-tools-adapters-and-effect-isolation/index.md'
s=src.read_text()
ledger=json.loads((R/'publishing/SINGLE_VOLUME_FINISHED_PAGE_LEDGER_V12.json').read_text())
errors=[]
def need(v,msg):
 if not v:errors.append(msg)
words=len(re.findall(r"\b[\w'-]+\b",s))
need(words<=3000, f'Chapter 19 source-word cap exceeded: {words}/3000')
need(ledger['chapter_pages']['19']==13,'Chapter 19 V12 allocation changed')
need((ledger['target_finished_pages'],ledger['chapter_total_pages'],ledger['front_back_reserve_pages'])==(550,485,65),'V12 total changed')
for term in ['CASE-204','$500','Design A','Design B','Design C','conditional','read-only','RF-1042','RF-1043','C04','C05','C06','C07','C08','E1','E2','E3','E4','E5','E6','E7','E8','E9','UNKNOWN','idempotency','reconciliation','provider','negative','human stop','Chapter 20','Figure 19.1','Figure 19.2','Fielding','OWASP','Fowler','Kleppmann']:
 need(term.casefold() in s.casefold(),f'Missing marker: {term}')
need('new payment architecture' in s and 'not build stages' in s, 'Missing architectural decisions boundary')
need('not a grant of permission' in s and 'not a recovery technique' in s,'Missing safety boundary')
for name in ('F19-01','F19-02'):
 master=R/f'assets/shared-figures/sources/{name}.svg'; rend=R/f'assets/shared-figures/rendered/{name}.svg'; png=R/f'assets/shared-figures/rendered/{name}.png'
 need(all(p.exists() for p in (master,rend,png)),f'{name} files missing')
 if not all(p.exists() for p in (master,rend,png)):continue
 need(master.read_bytes()==rend.read_bytes(),f'{name} source/render SVG mismatch')
 try:root=ET.parse(master).getroot()
 except Exception as e:errors.append(f'{name} XML invalid: {e}');continue
 ns='{http://www.w3.org/2000/svg}'
 txt=list(root.iter(ns+'text'))
 need(root.get('width')=='5.75in' and root.get('viewBox','').startswith('0 0 1140 '),f'{name} print geometry')
 need(len(txt)>=12 and all(float(x.get('font-size','0'))>=19 for x in txt),f'{name} font size/labels')
 need(all(x.get('font-family','').startswith('Arial') for x in txt),f'{name} font family')
 need(len(list(root.iter(ns+'rect')))>=5,f'{name} diagram structure')
 need(png.stat().st_size>15000,f'{name} missing usable render')
# Never claim integrated embedding if full book not built.
doc=R/'dist/etis-agentic-ai-book.docx'
need(doc.exists(),'Full Word build missing: make book-docx')
if doc.exists():
 with zipfile.ZipFile(doc) as z:
  media={hashlib.sha256(z.read(x)).hexdigest() for x in z.namelist() if x.startswith('word/media/')}
 for name in ('F19-01','F19-02'):
  png=R/f'assets/shared-figures/rendered/{name}.png'
  need(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{name} not current in Word')
need('Chapter 19 — tools, adapters' in (R/'references/source-register.md').read_text(),'Source register mapping missing')
need('Chapters 1–22' in (R/'manuscript/backmatter/bibliography.md').read_text(),'Bibliography scope not updated')
print(f'Chapter 19: {words}/3000 source words; allocated 13 finished pages; {len(errors)} failures')
for e in errors:print('FAIL:',e)
if errors:sys.exit(1)
print('PASS: source, CAB-aligned markers, 7x10 SVG print constraints, source-render identity, current embedded PNG fingerprints, citations and V12 control')
print('OPEN: Mac Word finished pagination, actual-size diagram review, six-lens editorial signoff, exact source edition/page audit')
