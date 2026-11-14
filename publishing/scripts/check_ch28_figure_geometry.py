#!/usr/bin/env python3
"""Chapter 28 source/render and print-measure preflight; visual review still required.

Check the three different diagram TYPES, not only matching PNG file names.
This cannot prove text collision absence; inspect actual 7x10 Word proof.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
import re
import sys

R=Path(__file__).resolve().parents[2]
source=R/'assets/shared-figures/sources'
render=R/'assets/shared-figures/rendered'
errors=[]
for i,expected in ((1,'layered'),(2,'sequence'),(3,'decision')):
 name=f'F28-{i:02d}'
 p=source/f'{name}.svg'
 try:
  root=ET.parse(p).getroot()
  b=root.attrib
  assert b.get('width') == '5.75in', 'wrong print width'
  assert b.get('height','').endswith('in'), 'print height missing'
  box=[float(x) for x in b['viewBox'].split()]
  assert box[0]==box[1]==0 and box[2]==1140, 'wrong viewBox'
  assert 0<box[3]<=1200, 'unbounded figure height'
  assert p.read_bytes()==(render/f'{name}.svg').read_bytes(), 'source/render mismatch'
  assert (render/f'{name}.png').stat().st_size>30_000, 'missing raster render'
  text=' '.join((e.text or '') for e in root.iter() if e.tag.endswith('text'))
  if expected=='layered':
   for term in ('E1','E2','E3','E4','E5','E6','E7','E8','E9','ownership','dispatch','provider truth'):
    assert term.lower() in text.lower(),f'missing {term}'
  if expected=='sequence':
   assert sum(e.tag.endswith('line') for e in root.iter())>=5,'missing lifelines'
   for term in ('RF-1042','Reply lost','Read-only lookup','NO SECOND SEND'):
    assert term in text,f'missing sequence {term}'
  if expected=='decision':
   assert sum(e.tag.endswith('polygon') for e in root.iter())>=2,'missing decision diamonds'
   for term in ('UNKNOWN','Read-only status','Confirm original RF-1042'):
    assert term in text,f'missing decision {term}'
  print(f'PASS {name}: {expected} SVG/master/raster and 5.75-inch print width')
 except (OSError,ET.ParseError,AssertionError,KeyError,ValueError) as e:
  errors.append(f'{name}: {e}')
for e in errors:print('FAIL',e)
if errors:sys.exit(1)
print('Chapter 28 figure preflight PASS; inspect all figures at actual 7x10 print size separately')
