#!/usr/bin/env python3
"""Part II reference-architecture editorial and source-to-Word acceptance gates."""
from pathlib import Path
import hashlib, re, sys, zipfile, xml.etree.ElementTree as ET
r=Path(__file__).resolve().parents[2];part=(r/'manuscript/part-02-architecture/_part.md').read_text()
c8=next((r/'manuscript/part-02-architecture').glob('ch08-*/index.md')).read_text()
errors=[]
def need(b,m):
 if not b: errors.append(m)
need('target-state logical reference architecture' in part.lower(),'Part II target-state frame absent')
need(all(str(n) in part for n in range(9,17)),'Part II chapter map incomplete')
need('neither a prescribed call sequence nor nine required microservices' in part,'Domain misconception not addressed')
need('CASE-204' in part and 'RF-1042' in part,'Running case absent')
need(all(f'F08-0{i}.png' in c8 for i in range(1,4)),'Three figures not referenced')
need([c8.index(f'F08-0{i}.png') for i in range(1,4)] == sorted(c8.index(f'F08-0{i}.png') for i in range(1,4)),'Incorrect figure order')
for n in (9,10,11,12,14,15):
 s=next((r/'manuscript/part-02-architecture').glob(f'ch{n:02}-*/index.md')).read_text()
 need('Figure 8.1' in s,f'Chapter {n} missing architectural trace')
for n in range(8,16):
 s=next((r/'manuscript/part-02-architecture').glob(f'ch{n:02}-*/index.md')).read_text()
 need('CASE-204' in s and 'RF-1042' in s,f'Chapter {n} case continuity')
 need('Design A' in s and 'Design B' in s and 'Design C' in s,f'Chapter {n} alternatives continuity')
 need(len(s.split())<=3000,f'Chapter {n} exceeds 3000 words')
p=r/'assets/shared-figures/sources/F08-01.svg';b=p.read_bytes();need(b'width="5.75in"' in b,'Canonical figure width not print-correct')
need(all(f'E{i} '.encode() in b for i in range(1,10)),'One or more E1-E9 labels missing in figure')
need(all(term in b for term in (b'INDEPENDENT', b'EXTERNAL PROVIDER', b'UNKNOWN', b'ASSURANCE', b'BUSINESS TRUTH')) or (b'Independent gate' in b and b'EXTERNAL PROVIDER' in b and b'UNKNOWN' in b),'Key trust/uncertainty boundaries missing')
need(all(term in b for term in (b'INTERACTION AND ADMISSION', b'COORDINATION AND AGENTIC', b'TRUSTED CONSEQUENTIAL', b'ENTERPRISE SYSTEMS')),'Layered architecture not explicit')
need(b'not mandated services' in b and b'span all layers' in b,'Layer and cross-cutting semantics missing')
try:ET.fromstring(b)
except Exception as e:errors.append(f'Invalid SVG: {e}')
need(b==(r/'assets/shared-figures/rendered/F08-01.svg').read_bytes(),'SVG master/render mismatch')
doc=r/'dist/etis-agentic-ai-book.docx'
need(doc.exists(),'Integrated Word missing')
if doc.exists():
 with zipfile.ZipFile(doc) as z:
  hashes={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
 for n in range(1,4):
  png=r/f'assets/shared-figures/rendered/F08-0{n}.png'
  need(hashlib.sha256(png.read_bytes()).hexdigest() in hashes,f'F08-0{n} PNG absent from Word')
print('Part II target-state architecture acceptance:', 'PASS' if not errors else 'FAIL')
if errors:print('\n'.join(errors));sys.exit(1)
print('Native Word 7x10 visual and semantic review remain manual gates')
