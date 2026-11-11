#!/usr/bin/env python3
"""Chapter 5 deterministic acceptance gates; print-size visual signoff is separate."""
from pathlib import Path
from zipfile import ZipFile
import re, hashlib, json, sys, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
chapter=next((R/'manuscript/part-01-foundations').glob('ch05*/index.md'))
s=chapter.read_text();fail=[]
words=len(re.findall(r"\b[\w'-]+\b",s));budget=json.loads((R/'publishing/SINGLE_VOLUME_BUDGET_V10.json').read_text()); cap=budget['chapter_word_caps']['5']
if words>cap:fail.append(f'Word cap {words}>{cap}')
for term in ['Design B','Design C','$500','UNKNOWN','10,000','$77,000','$103,000','8,572','19,200','Chapter 6']:
 if term not in s:fail.append(f'Missing continuity/economics term: {term}')
assert 10000*5.90 + 18000 == 77000
assert 10000*5.50 + 48000 == 103000
assert (80000-77000)==3000 and (80000-103000)==-23000
assert round(18000/(8-5.90))==8571 or round(18000/(8-5.90))==8572
assert 48000/(8-5.50)==19200
for fig in ['F05-01','F05-02']:
 master=R/f'assets/shared-figures/sources/{fig}.svg';svg=R/f'assets/shared-figures/rendered/{fig}.svg';png=R/f'assets/shared-figures/rendered/{fig}.png'
 for f in [master,svg,png]:
  if not f.exists():fail.append(f'Missing: {f.relative_to(R)}')
 try:
  root=ET.parse(master).getroot()
  if root.attrib.get('width')!='5.75in':fail.append(f'{fig} must be authored at 5.75in')
  if len(list(root.iter('{http://www.w3.org/2000/svg}text')))<8:fail.append(f'{fig}: too few textual elements')
  if master.read_bytes()!=svg.read_bytes():fail.append(f'{fig}: rendered SVG differs from master')
 except Exception as e:fail.append(f'{fig}: SVG parse: {e}')
 if f'{fig}.png' not in s: fail.append(f'{fig} not referenced by chapter')
 if png.exists():
  with open(png,'rb') as f:
   if f.read(8)!=b'\x89PNG\r\n\x1a\n':fail.append(f'{fig}: invalid PNG signature')
# Word image bytes must contain exact accepted output, without assuming arbitrary renamed OOXML media names
word=R/'dist/etis-agentic-ai-book.docx'
if word.exists():
 with ZipFile(word) as z:
  media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
 for fig in ['F05-01','F05-02']:
  png=R/f'assets/shared-figures/rendered/{fig}.png'
  if hashlib.sha256(png.read_bytes()).hexdigest() not in media:fail.append(f'{fig} generated PNG not embedded in current Word build')
else:print('Word build absent: built-image check skipped (run make book-docx)')
print(f'Chapter 5: {words}/{cap} words; exact figure master + print-width + economic continuity checks.')
if fail:print('FAIL: '+'; '.join(fail));sys.exit(1)
print('Chapter 5 deterministic acceptance PASS; native Word and print visual review remain manual.')
