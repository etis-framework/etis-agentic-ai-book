#!/usr/bin/env python3
"""Catch missing or unreadable F26 SVG labels and incorrect figure multiplicity.

Automated geometric bounds cannot certify visual legibility; print QA remains.
"""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
errors=[]
for n in range(1,4):
 path=R/f'assets/shared-figures/sources/F26-{n:02}.svg'
 tree=ET.parse(path)
 root=tree.getroot()
 w=float(root.get('width','0'));h=float(root.get('height','0'))
 if not (1000<=w<=1200 and 650<=h<=900):errors.append(f'F26-{n:02}: unusual viewport')
 texts=[x for x in root.iter() if x.tag.endswith('text')]
 if len(texts)<14:errors.append(f'F26-{n:02}: too little diagram semantic labeling')
 for t in texts:
  x=float(t.get('x','0'));y=float(t.get('y','0'))
  if not (0<x<w and 0<y<h):errors.append(f'F26-{n:02}: text anchor outside figure at {x},{y}')
 source=path.read_text()
 if n==1 and not all(x in source for x in ('E5 trusted execution','E7 durable ledger','E6 provider adapter','Mock E8 provider')):errors.append('F26-01: key responsibilities absent')
 if n==2 and not all(x in source for x in ('Read-only status query','Matching provider proof','E7 CONFIRMED')):errors.append('F26-02: reconciliation sequence incomplete')
 if n==3 and not all(x in source for x in ('NOT_FOUND is not FAILED','UNKNOWN + escalation')):errors.append('F26-03: unsafe retry decision?')
print('F26 source figure geometry/semantic QA:', 'PASS' if not errors else 'FAIL')
for e in errors:print('FAIL:',e)
sys.exit(bool(errors))
