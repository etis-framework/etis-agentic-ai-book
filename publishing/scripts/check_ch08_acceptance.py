#!/usr/bin/env python3
"""Chapter 8 hard gates: V9 source, rendered artwork, Word embedding and continuity.
Semantic meaning and 7x10 visual legibility still require actual print inspection.
"""
from pathlib import Path
import hashlib,re,sys,zipfile,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
ch=(root/'manuscript/part-02-architecture/ch08-from-requirements-to-a-reference-architecture/index.md').read_text()
part=(root/'manuscript/part-02-architecture/_part.md').read_text()
ch2=(root/'manuscript/part-01-foundations/ch02-historical-foundations/index.md').read_text()
errors=[]
def require(test,msg):
 if not test: errors.append(msg)
require(len(part.split())>=500,'Part II introduction insufficient depth (<500 words)')
require('The nine-chapter learning path' in part and all(f'**{n}.' in part for n in range(8,17)),'Part II chapter map incomplete')
require('non-authoritative' in ch.lower() and 'authorization status' in ch.lower(),'No clear definition of untrusted advice')
require('deterministic code can have bugs' in ch.lower(),'Trusted code overclaimed')
require('RF-1042' in part and 'CASE-204' in part,'Part II continuity missing')
require('R-1042' not in ch2.replace('RF-1042',''),'Chapter 2 operation identifier drift')
require(all(x in ch for x in ('DATA-01','AUTH-01','POL-02','PAY-03','OPS-01')),'Requirement trace incomplete')
require(len(ch.split())<=3000,'Chapter 8 source word cap exceeded')
require(ch.count("The diagram's separation is not cosmetic.")==1,'Duplicate paragraph')
media=set()
docx=root/'dist/etis-agentic-ai-book.docx'
if docx.exists():
 with zipfile.ZipFile(docx) as z:
  media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
else:errors.append('DOCX missing: run make book-docx')
for name in ('F08-01','F08-02'):
 master=root/f'assets/shared-figures/sources/{name}.svg'; render=root/f'assets/shared-figures/rendered/{name}.svg';png=root/f'assets/shared-figures/rendered/{name}.png'
 require(master.exists() and render.exists() and png.exists(),f'{name} master/render missing')
 if not all((master.exists(),render.exists(),png.exists())):continue
 a,b=master.read_bytes(),render.read_bytes()
 require(a==b,f'{name}: rendered SVG differs from master')
 require(b'width="5.75in"' in a,f'{name}: not at final print width')
 require(len(re.findall(rb'<rect ',a))>=6,f'{name}: missing composed SVG diagram objects')
 require(b'<polyline ' in a and b'<polygon ' in a,f'{name}: visible directional arrows absent')
 require(not (root/f'assets/shared-figures/sources/{name}.dot').exists(),f'{name}: obsolete DOT source remains')
 try:ET.fromstring(a)
 except Exception as ex:errors.append(f'{name}: SVG XML invalid: {ex}')
 require(hashlib.sha256(png.read_bytes()).hexdigest() in media,f'{name}: corrected PNG not embedded in built Word')
 require(png.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n',f'{name}: invalid PNG')
print('Chapter 8: ',len(ch.split()),'words, Part II:',len(part.split()),'words')
if errors:
 print('CH08 ACCEPTANCE GATES FAILED:\n'+'\n'.join(errors));sys.exit(1)
print('Chapter 8 structural/continuity/Word figure fingerprint checks PASS; manual print/technical acceptance remains required')
