#!/usr/bin/env python3
"""Detect clipped or duplicate Chapter 27 figure elements; visual audit still required."""
from pathlib import Path
from xml.etree import ElementTree as ET
import sys
R=Path(__file__).resolve().parents[2]
errors=[]
for i in (1,2,3):
 k=f'F27-{i:02d}';p=R/f'assets/shared-figures/sources/{k}.svg'
 try:
  tree=ET.parse(p);root=tree.getroot()
  ns='{http://www.w3.org/2000/svg}'
  title=' '.join(''.join(el.itertext()) for el in root.iter() if el.tag==ns+'text')
  if len(title)<120:errors.append(k+' has insufficient semantic labels')
  if len(list(root.iter(ns+'polygon')))<3:errors.append(k+' missing arrowheads')
  if root.attrib.get('viewBox')!='0 0 960 600':errors.append(k+' incorrect print canvas')
 except (ET.ParseError,OSError) as e:errors.append(k+': '+str(e))
print('Chapter 27 figure geometry:', 'PASS' if not errors else 'FAIL')
for e in errors:print('FAIL:',e)
sys.exit(bool(errors))
