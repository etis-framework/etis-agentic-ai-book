#!/usr/bin/env python3
from pathlib import Path
import re,sys
root=Path(__file__).resolve().parents[2]
chap=list((root/'manuscript').glob('part-*/ch*/index.md'))
fig=list((root/'assets/shared-figures/rendered').glob('[!._]*.svg'))
issues=[]
if len(chap)!=36:issues.append(f'Expected 36 chapter files; got {len(chap)}')
if len(fig)<29:issues.append(f'Expected at least 29 figure SVGs (CAB-001 plus Chapter 1–2 figures); got {len(fig)}')
for p in chap:
 if not p.read_text().startswith('# Chapter '):issues.append(f'Chapter heading missing: {p}')
for p in (root/'assets/shared-figures/rendered').glob('[!._]*.svg'):
 if '<svg' not in p.read_text(errors='ignore'):issues.append(f'Invalid SVG header: {p}')
print(f'Chapters: {len(chap)}; SVG masters: {len(fig)}')
print('\n'.join(issues) if issues else 'Structural checks passed. Semantic QA still required.')
sys.exit(bool(issues))
