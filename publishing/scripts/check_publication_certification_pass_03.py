#!/usr/bin/env python3
"""Pass 3 gates: manuscript navigation, bibliography, and author source checks.
This does not substitute for a native Word-for-Mac print proof.
"""
from pathlib import Path
import json,re,sys
from docx import Document
from docx.oxml.ns import qn
R=Path(__file__).resolve().parents[2];errors=[]
def require(ok,msg):
 if not ok:errors.append(msg)
source=(R/'manuscript/backmatter/about-the-author.md').read_text()
for phrase in ['IBM Distinguished Engineer','two Chief Technology Officer','ACM SIGMOD','VLDB','IEEE ICDE','11 U.S. patents','ETIS Engineering Studio','Loyola University Chicago','Princeton University','University of Toronto']:
 require(phrase in source,'Author bio missing '+phrase)
register=json.loads((R/'metadata/index-term-register.json').read_text())['entries']
require(len(register)>=150,'Index contains fewer than 150 professional entries')
terms=[e['term'] for e in register]
require(terms==sorted(terms,key=str.casefold),'Index sorting is incorrect')
require(len(set(x.casefold() for x in terms))==len(terms),'Duplicate index terms')
for e in register:
 require(bool(re.search(r'Chapter(?:s)?\s+\d+',e['locator']) or re.search(r'§\d+',e['locator'])),'Index entry lacks chapter/section navigation: '+e['term'])
path=R/'dist/etis-agentic-ai-book.docx'
if path.exists():
 d=Document(path)
 require(len(d.sections)>45,'Expected multi-section print layout')
 refs=[x.text or '' for x in d.element.body.findall('.//'+qn('w:instrText'))]
 require(sum('PAGEREF ' in x for x in refs)>=290,'Missing live Word reference fields')
else:errors.append('Full-book DOCX missing; run make book-docx')
print('Publication Pass 3:', 'PASS' if not errors else 'FAIL',len(errors),'findings; index entries',len(register))
for e in errors:print('FAIL',e)
sys.exit(bool(errors))
