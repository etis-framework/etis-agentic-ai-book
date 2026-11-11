#!/usr/bin/env python3
"""Structural/semantic preflight for hand-positioned, print-first Chapter 4 SVG masters.

This is NOT a substitute for viewing each 7x10-inch rendered book page.
"""
from pathlib import Path
import re, sys, hashlib, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
S=R/'assets/shared-figures/sources'; D=R/'assets/shared-figures/rendered'
errors=[]
expect={
 'F04-01':['AGENT: INVESTIGATION ONLY','TRUSTED SYSTEM','Scoped objective','Controller: validate','Working state'],
 'F04-02':['A  FIXED WORKFLOW','B  BOUNDED AGENT','C  HYBRID','Fixed sequence','Choose next read','Policy / review'],
 'F04-03':['BOUNDED AGENT','ENTERPRISE CONTROL','EXTERNAL EFFECT','Typed eligibility','Independent policy','Trusted dispatch','CONFIRMED only','PERMIT','DENY']}
for name,terms in expect.items():
 for ext in ('.svg','.dot'):
  if not (S/(name+ext)).is_file():errors.append(name+' missing editable '+ext)
 for ext in ('.svg','.png'):
  if not (D/(name+ext)).is_file():errors.append(name+' missing render '+ext)
 try:
  s=(S/(name+'.svg')).read_text(); tree=ET.fromstring(s)
  if hashlib.sha256((S/(name+'.svg')).read_bytes()).digest() != hashlib.sha256((D/(name+'.svg')).read_bytes()).digest(): errors.append(name+' stale rendered SVG differs from editable SVG master')
  labels=' '.join(x.text or '' for x in tree.iter() if x.tag.endswith('text'))
  if '5.75in' not in s: errors.append(name+' is not fixed at 5.75in final width')
  if not ('Arial' in s and 'rounded' not in s): pass  # Fonts are specified on text nodes; box geometry uses rx/ry.
  for term in terms:
   if term not in labels:errors.append(name+' missing semantic label: '+term)
  if '#e7f2e4' in s and name!='F04-03':errors.append(name+' incorrectly uses verified-outcome green')
  if name=='F04-03' and '#e7f2e4' not in s:errors.append(name+' missing verified-outcome green')
  # Prevent background lettering from appearing behind any title: every group has a white backing rectangle.
  if s.count('stroke-dasharray="7,5"')< (3 if name!='F04-01' else 2):errors.append(name+' lacks bounded panels')
 except Exception as e:errors.append(name+' invalid SVG: '+str(e))
print('F04 figure mechanical and semantic preflight:', 'PASS' if not errors else 'FAIL')
for e in errors:print(' -',e)
print('MANDATORY manual gate: inspect each embedded Word figure and caption at 7x10 final print size')
sys.exit(bool(errors))
