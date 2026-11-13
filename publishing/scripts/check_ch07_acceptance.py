#!/usr/bin/env python3
"""Chapter 7 continuity, source and print-asset integrity; never substitutes for visual acceptance."""
import hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile
R=Path(__file__).resolve().parents[2]
s=(R/'manuscript/part-01-foundations/ch07-engineering-principles-and-requirements/index.md').read_text()
b=json.loads((R/'publishing/SINGLE_VOLUME_BUDGET_V10.json').read_text());cap=b['chapter_word_caps']['7'];wc=len(re.findall(r"\b[\w'-]+\b",s));err=[]
if wc>cap:err.append(f'over cap {wc}/{cap}')
for term in ['Design B','Design C','CASE-204','RF-1042','$500','UNKNOWN','OUTCOME_UNKNOWN','read-only','AUTH-01','PAY-03','DATA-01','POL-02','OPS-01','F07-01.png','F07-02.png','Part II','ISO/IEC/IEEE 29148']:
 if term not in s:err.append(f'missing {term}')
for n in ['F07-01','F07-02']:
 m=R/f'assets/shared-figures/sources/{n}.svg';v=R/f'assets/shared-figures/rendered/{n}.svg';p=R/f'assets/shared-figures/rendered/{n}.png'
 if not (m.is_file() and v.is_file() and p.is_file()):err.append(f'{n} missing');continue
 try:
  svg=ET.parse(m).getroot()
  if svg.get('width')!='5.75in':err.append(f'{n} wrong print width')
  if len(list(svg.iter('{http://www.w3.org/2000/svg}text')))<8:err.append(f'{n} labels missing')
 except Exception as e:err.append(f'{n}: {e}')
 if m.read_bytes()!=v.read_bytes():err.append(f'{n}: SVG master/render mismatch')
 if p.read_bytes()[:8]!=b'\x89PNG\r\n\x1a\n':err.append(f'{n}: invalid PNG')
word=R/'dist/etis-agentic-ai-book.docx'
if word.is_file():
 with ZipFile(word) as z:media={hashlib.sha256(z.read(q)).hexdigest() for q in z.namelist() if q.startswith('word/media/')}
 for n in ['F07-01','F07-02']:
  p=R/f'assets/shared-figures/rendered/{n}.png'
  if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() not in media:err.append(f'{n}: Word embedded image stale')
else:print('Word absent: embedded-image check deferred')
part=(R/'manuscript/part-01-foundations/_part.md').read_text()
if 'Chapters 1–7 constitute the current Part I development draft' not in part:err.append('Part I status stale')
print(f'Chapter 7: {wc}/{cap} source words; {len(err)} issue(s)')
for x in err:print('ERROR',x)
if err:sys.exit(1)
print('PASS automatic Chapter 7 checks; native Word and technical editorial signoff remain manual')
