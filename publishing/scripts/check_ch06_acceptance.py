#!/usr/bin/env python3
"""Ch06 deterministic regression gates; manual/native Word signoff separate."""
from pathlib import Path
from zipfile import ZipFile
import hashlib,json,re,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
F=next((R/'manuscript/part-01-foundations').glob('ch06*/index.md'))
s=F.read_text(); b=json.loads((R/'publishing/SINGLE_VOLUME_BUDGET_V10.json').read_text());cap=b['chapter_word_caps']['6'];words=len(re.findall(r"\b[\w'-]+\b",s));errors=[]
if words>cap:errors.append(f'chapter word cap exceeded: {words}>{cap}')
for need in ['Design B','Design C','CASE-204','RF-1042','$500','UNKNOWN','OUTCOME_UNKNOWN','read-only','NIST AI 600-1','Chapter 7','F06-01.png','F06-02.png']:
 if need not in s:errors.append(f'missing continuity term {need}')
for n in ('F06-01','F06-02'):
 m=R/f'assets/shared-figures/sources/{n}.svg'; v=R/f'assets/shared-figures/rendered/{n}.svg';p=R/f'assets/shared-figures/rendered/{n}.png'
 if not all(x.exists() for x in (m,v,p)):errors.append(f'{n}: missing master/render');continue
 try:
  rt=ET.parse(m).getroot()
  if rt.attrib.get('width')!='5.75in':errors.append(f'{n}: not 5.75in wide')
  if len(list(rt.iter('{http://www.w3.org/2000/svg}text')))<8:errors.append(f'{n}: labels missing')
 except Exception as ex:errors.append(f'{n}: XML: {ex}')
 if m.read_bytes()!=v.read_bytes():errors.append(f'{n}: source SVG differs from render')
 if p.read_bytes()[:8]!=b'\x89PNG\r\n\x1a\n':errors.append(f'{n}: bad PNG')
 if n not in s:errors.append(f'{n}: missing chapter reference')
w=R/'dist/etis-agentic-ai-book.docx'
if w.exists():
 with ZipFile(w) as z:hs={hashlib.sha256(z.read(k)).hexdigest() for k in z.namelist() if k.startswith('word/media/')}
 for n in ('F06-01','F06-02'):
  p=R/f'assets/shared-figures/rendered/{n}.png'
  if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() not in hs:errors.append(f'{n}: embedded Word image stale')
else:print('Word not built: embedded checks pending')
part=(R/'manuscript/part-01-foundations/_part.md').read_text()
if 'Chapters 1–6 contain substantive draft material; Chapter 7 remains planned.' not in part:errors.append('Part I status not updated')
print(f'Chapter 6 acceptance: {words}/{cap} words, remaining headroom {cap-words}; {len(errors)} issue(s)')
for e in errors:print('ERROR '+e)
if errors:sys.exit(1)
print('PASS (native Word and technical editorial signoff still manual)')
