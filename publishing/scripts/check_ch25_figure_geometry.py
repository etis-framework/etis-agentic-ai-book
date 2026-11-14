#!/usr/bin/env python3
"""Chapter 25 SVG figure-head sizes, source/render identity, semantic split.

Mechanical geometry is not a substitute for print-size inspection in Word.
"""
from pathlib import Path
import math
import sys
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
errors=[]
for i,term in [(1,'architecture'),(2,'behavioral'),(3,'decision')]:
 name=f'F25-{i:02}'
 p=R/f'assets/shared-figures/sources/{name}.svg'
 try:
  root=ET.parse(p).getroot()
  assert root.get('viewBox')=='0 0 1100 720'
  figures=[e for e in root.iter() if e.tag.endswith('polygon')]
  if len(figures)<3:raise ValueError('missing bounded arrowheads')
  for node in figures:
   pairs=[tuple(map(float,point.split(','))) for point in node.attrib['points'].split()]
   if len(pairs)!=3:raise ValueError('nontriangular arrowhead')
   for x,y in pairs:
    if not (0<=x<=1100 and 0<=y<=720):raise ValueError('clipped arrowhead')
   side=max(math.dist(a,b) for a in pairs for b in pairs)
   if side>22:raise ValueError('oversized arrowhead')
  content=p.read_text()
  if i==1 and not all(t in content for t in ('IPC client.py','E5 service.py','E7 durable intent','DENY: no independent grant','No client-to-adapter route')):
   raise ValueError('Figure 25.1 missing single enforced request-path semantics')
  if i==2 and not all(t in content for t in ('Finance fixture*','ATTACK — real fixture identity token','APPROVED FIXTURE','no finance-to-E5 call exists','Grant is carried by client request')):
   raise ValueError('Figure 25.2 missing distinct issuer and attack semantics')
  if i==1 and not all(t in content for t in ('prepare() records RF-1042','dispatch() claims E7 state first','Mock E8 provider truth')):
   raise ValueError('Figure 25.1 missing durable-before-effect ordering')
  if i==2 and 'issue grant to harness' not in content:
   raise ValueError('Figure 25.2 missing grant-through-client route')
  if p.read_bytes()!=(R/f'assets/shared-figures/rendered/{name}.svg').read_bytes():
   raise ValueError('published SVG does not match master')
  if (R/f'assets/shared-figures/rendered/{name}.png').stat().st_size<10_000:
   raise ValueError('missing/empty PNG render')
  print(f'{name}: {len(figures)} bounded arrowheads; source equals rendered SVG')
 except (OSError,ET.ParseError,AssertionError,ValueError,KeyError) as exc:
  errors.append(f'{name}: {exc}')
print('Chapter 25 figure geometry '+('FAIL' if errors else 'PASS; manual printed Word inspection still open'))
if errors:print('\n'.join(errors))
sys.exit(bool(errors))
